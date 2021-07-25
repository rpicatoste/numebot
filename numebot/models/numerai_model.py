from abc import abstractmethod, ABC
from datetime import datetime
from numerapi.numerapi import NumerAPI
import numpy as np
import pandas as pd

from numebot.data.data_constants import NC
from numebot.data.data_manager import DataManager
from numebot.file_names_getter import FileNamesGetter
from numebot.utils import save_bak_version


class NumeraiModel(ABC):

    def __init__(
        self, config_row: pd.Series, file_names: FileNamesGetter, napi: NumerAPI, testing: bool
    ):
        self.name = config_row.name
        self.model_code = config_row['model_code']
        self.testing = testing

        self.names = file_names
        self.napi = napi
        self.model_ready = False
        self.model = self.load_model()

        self._models_dict = None
        self._leaderboard = None


    def info(self):
        print(f'\nModel name: {self.name}')
        print(f' - Code: {self.model_code}')
        
        print(f' - Model folder: {self.names.model_folder(self.name)}')
        print(f' - Model file: {self.names.model_path(self.name).name}')

    def predict(self, data: DataManager, to_be_saved_for_submission=False):
        numerai_data_set = data.tournament
        if not self.model_ready:
            print(f'Model {self.name} is not ready, it needs to be trained or loaded.')
            return None

        print(f'\nRunning prediction for model {self.name} ...')
        print(f' - Rows: {len(numerai_data_set)}, columns: {len(numerai_data_set.columns)}')
        
        feature_cols = [f for f in numerai_data_set.columns if f.startswith("feature")]
        
        output_values = self.model.predict(numerai_data_set[feature_cols])
        output = pd.DataFrame({'prediction': output_values}, index=numerai_data_set.index)

        if to_be_saved_for_submission and not self.testing:
            self.save_for_submission(output)
            
        return output

    def save_for_submission(self, output):
        submission_path = self.names.model_submission_path(self.name)
        print(f'  Saving results into: {submission_path}')
        submission_path.parent.mkdir(parents=True, exist_ok=True)
        output.to_csv(submission_path, header=True)
        print('  Saved!')

    @abstractmethod
    def load_model(self):
        # How the model is loaded belongs to each specific model
        pass

    @property
    def models_dict(self):
        if self._models_dict is None:
            self._models_dict = self.napi.get_models()
        
        return self._models_dict

    @property
    def leaderboard(self):
        # Get leaderboard for the current round
        if self._leaderboard is None:
            leaderboard = self.napi.get_leaderboard(limit=10000)
            self._leaderboard = {competitor['username']:competitor for competitor in leaderboard}
            
        return self._leaderboard

    def submit_predictions(self, force_resubmission=False):
        file_path = self.names.model_submission_path(self.name)
        if not file_path.exists():
            print(f'\nPredictions for model {self.name} do not exist. Continue with next model')
            return None

        model_id = self.models_dict[self.name]
        
        if self.round_submission_done() and not force_resubmission:
            print(f'Submission for model {self.name} already done, no resubmission requested.')
            return

        print(f'\nUploading file for model {self.name}: {file_path}')
        if not self.testing:
            submission_id = self.napi.upload_predictions(file_path, model_id=model_id)
        else:
            print(f' - WARNING: Test mode, no file is submitted or checked.')
            return

        return submission_id

    def get_weekly_submission_status(self, to_be_saved=False):
        """
        Get the submission status information provided by numerai en store it in a csv to keep the 
        history of metrics.
        This is done weekly, with each submission.
        """
        if self.name not in self.models_dict.keys():
            print(f'No data available for {self.name} yet.')
            return pd.DataFrame()
            
        model_id = self.models_dict[self.name]
        model_info_path = self.names.model_submission_status_log_path(self.name)
        round = self.napi.get_current_round()
        
        # Get status, make it dataframe friendly, convert None to nan.
        model_status = self.napi.submission_status(model_id=model_id)
        model_status = {key: [value if value is not None else np.nan] 
                        for key, value in model_status.items()}
        
        # Add date
        timestamp = datetime.now()
        model_status[NC.timestamp] = [timestamp]

        df = pd.DataFrame(model_status, index=[round])
        df.index.name = 'round'
        
        if model_info_path.exists():
            previous_df = pd.read_csv(model_info_path).set_index('round')
            if round in previous_df.index:
                previous_df.loc[round, :] = df.loc[round]
                full_df = previous_df
            else:
                full_df = pd.concat([previous_df, df]).sort_index()
        else:
            full_df = df

        # Sort columns
        cols = full_df.columns
        sorted_cols = []   # Add here when I know what I want to see first in the table.
        sorted_cols = sorted_cols + [col for col in cols if col not in sorted_cols]
        full_df = full_df[sorted_cols]

        if to_be_saved:
            full_df.to_csv(model_info_path)

        print(f'Saved submission status from Numerai about model {self.name}, total rows: {len(full_df)}')

        return full_df


    def get_daily_leaderboard(self, to_be_saved=False):
        """
        Get the leaderboard information provided by numerai and store it in a csv to keep the 
        history.
        This is done daily.
        """
        model_leaderboard_path = self.names.model_leaderboard_log_path(self.name)
        round = self.napi.get_current_round()
        
        # If there is no data about this model, return an empty DataFrame.
        if self.name not in self.leaderboard.keys():
            return pd.DataFrame()

        # Get leaderboard info, make it dataframe friendly, convert None to nan.
        model_leaderboard = self.leaderboard[self.name]
        model_leaderboard = {key: [value if value is not None else np.nan] 
                             for key, value in model_leaderboard.items()}
        
        # Add date and round
        timestamp = datetime.now()
        date = timestamp.date()
        model_leaderboard[NC.timestamp] = [timestamp]
        model_leaderboard[NC.round] = [round]

        df = pd.DataFrame(model_leaderboard, index=[date])
        df.index.name = 'date'
        
        if model_leaderboard_path.exists():
            previous_df = pd.read_csv(model_leaderboard_path, 
                                      parse_dates=True,
                                      infer_datetime_format=True,
                                      low_memory=False)
                                    
            previous_df['date'] = previous_df['date'].astype(np.datetime64).dt.date
            previous_df.set_index('date', inplace=True)
            
            if date in previous_df.index:
                previous_df.loc[date, :] = df.loc[date]
                full_df = previous_df
            else:
                full_df = pd.concat([previous_df, df]).sort_index()
        else:
            full_df = df

        # Sort columns
        cols = full_df.columns
        sorted_cols = [NC.username, NC.round, NC.rank, NC.prevRank]
        sorted_cols = sorted_cols + [col for col in cols if col not in sorted_cols]
        full_df = full_df[sorted_cols]

        if to_be_saved:
            full_df.to_csv(model_leaderboard_path)

        print(f'Saved data from Numerai about model {self.name}, total rows: {len(full_df)}')

        return full_df

    def save_model(self):
        if self.testing:
            print(f'Running in test mode, model for {self.name} NOT saved.')
            return
        
        model_path = self.names.model_path(self.name)
        if model_path.exists():
            save_bak_version(model_path)

        model_path.parent.mkdir(parents=True, exist_ok=True)
        self.model.save_model(model_path)
        print(f'Model {self.name} saved to {model_path}')

    def round_submission_done(self):
        # If the submission is not done, the request for status will fail.
        try:
            _ = self.napi.submission_status(self.models_dict[self.name])
            return True
        except:
            pass

        return False
