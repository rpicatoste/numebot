import importlib
import numerapi
import pandas as pd
from typing import Dict

from numebot import DataManager
from numebot.data.data_constants import NC
from numebot.file_names_getter import FileNamesGetter
from numebot.models.numerai_model import NumeraiModel
from numebot.monitoring.metrics_manager import MetricsManager
from numebot.utils import to_camel_case, pathify


class RoundManager:

    def __init__(
        self, numerai_folder, model_configs_path, 
        public_id=None, secret_key=None, 
        nrows=None, save_memory=True, testing=False, verbose=False
    ):
        """
        nrows: Limit the lines in each csv read to nrows.
        """
        self.testing = testing
        self.napi = numerapi.NumerAPI(verbosity="info", public_id=public_id, secret_key=secret_key)

        self.current_round = self.napi.get_current_round()

        # Check if new round is open.
        if not self.napi.check_round_open():
            print(f'Round {self.current_round} is not open, exiting ...')
            return

        print(f'Current open round: {self.current_round}')

        self.names = FileNamesGetter(numerai_folder, 
                                     model_configs_path=model_configs_path, 
                                     current_round=self.current_round)
        self.data = self.load_data_manager(nrows, save_memory)
        
        self.models_dict = self.load_models(verbose=verbose)
        self.model_names = list(self.models_dict.keys())

        # Download current dataset, only if its unzipped folder does not exist yet.
        dest_filename = f'numerai_dataset_{self.current_round}'
        if not (self.names.data_folder/dest_filename).exists():
            self.napi.download_current_dataset(dest_path=self.names.data_folder, 
                                               dest_filename=dest_filename,
                                               unzip=True)
        else:
            print('Round data already downloaded and unzipped, continuing ...')

        self.mm = MetricsManager(napi=self.napi, 
                                 model_names=self.model_names,
                                 file_names=self.names)

    def load_data_manager(self, nrows, save_memory) -> DataManager:
        """
        A function is used to load the data manager so it can be overriden by a parent class of RoundManager.
        """
        return DataManager(file_names=self.names, nrows=nrows, save_memory=save_memory)
        
    def __getitem__(self, index_or_key):
        """
        Easy interface to get the models.
        """
        if isinstance(index_or_key, int):
            return self.models_dict[list(self.models_dict.keys())[index_or_key]]
        
        return self.models_dict[index_or_key]
        
    def load_models(self, verbose=False) -> Dict[str, NumeraiModel]:
        self.model_cfgs = pd.read_csv(self.names.model_configs_path)
        self.model_cfgs.set_index('numerai_name', drop=True, inplace=True)
        # In the csv, the single quotes are read sometimes as back/forward ticks. Replace by single 
        # quotes. This applies when the parameters column is present.
        if NC.parameters in self.model_cfgs.columns:
            for ch in '´`‘’':
                self.model_cfgs.loc[:, NC.parameters] = self.model_cfgs.loc[:, NC.parameters].str.replace(ch, '\'')

        models_dict = {}
        for name, config_row in self.model_cfgs.iterrows():
            try:
                print(f'\nPreparing model {name}')
                model_class = _import_class(config_row[NC.model_code], verbose=verbose)
                models_dict[name] = model_class(config_row, 
                                                file_names=self.names, 
                                                napi=self.napi, 
                                                testing=self.testing)

            except Exception as exc:
                print(f'\nERROR: Model {name} could not be added to the models list.')
                print(exc)
                
        return models_dict

    def models_info(self):
        for _, model in self.models_dict.items():
            model.info()
        else:
            print(f'\nFinished showing {len(self.models_dict.keys())} models\' info')

    def generate_predictions_for_all_models(self):
        for model_name, model in self.models_dict.items():
            if self.names.model_submission_path(model_name).exists():
                print(f'Predictions already exist for {model_name}, skipping ...')
                continue
                
            if not model.model_ready:
                print(f'Model {model.name} is not ready, it needs to be trained or loaded.')
                continue

            _ = model.predict(self.data, to_be_saved_for_submission=True)

    def submit_predictions(self, force_resubmission=False):
        for _, model in self.models_dict.items():
            try:
                model.submit_predictions(force_resubmission=force_resubmission)
            except:
                print(f'ERROR: Problem with model {model.name}, submission not done.')
            
        print('All models\' predictions submitted.')

    def get_submission_status_and_leaderboard_for_all_models(self, to_be_saved=True):
        models_status, models_leaderboard = [], []
        for model_name, model in self.models_dict.items():
            weekly_df = model.get_weekly_submission_status(to_be_saved=to_be_saved)
            cols = list(weekly_df.columns)
            weekly_df['model'] = model_name
            models_status.append(weekly_df[['model'] + cols])
            models_leaderboard.append(model.get_daily_leaderboard(to_be_saved=to_be_saved))

        models_status = pd.concat(models_status)
        models_leaderboard = pd.concat(models_leaderboard)

        return models_status, models_leaderboard

    def generate_dummy_input_for_model_init(self, model_name):
        """
        Use this function to pass to models that doesn't have their code settled yet (they are being
        developed or tested). Example: 
        dummy_param = rm.generate_dummy_input_for_model_init(model_name='test_model')
        model = MyNewModel(**dummy_param)
        """
        config_row = pd.Series(['code-path-TBD'], 
                               index=[NC.model_code],
                               name=model_name)

        return {'config_row': config_row,
                'file_names': self.names,
                'napi': self.napi}


def _import_class(module_name: str, verbose= False) -> type:
    """Import class from a module, e.g. 'text_recognizer.models.MLP'"""
    # It is assumed that the class name is the camel case version of the module name.
    if verbose: print(module_name)
    class_name = to_camel_case(module_name.rsplit(".", 1)[1])
    
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)

    return class_
