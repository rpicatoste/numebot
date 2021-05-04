from abc import abstractmethod, ABC
import pandas as pd

from numebot.file_names_getter import FileNamesGetter


class NumeraiModel(ABC):

    def __init__(self, config_row: pd.Series, file_names: FileNamesGetter) -> None:
        self.name = config_row.name
        self.model_code = config_row['model_code']
        
        self.names = file_names

        self.model = self.load_model()

    def info(self):
        print(f'\nModel name: {self.name}')
        print(f' - Code: {self.model_code}')
        
        print(f' - Model folder: {self.names.model_folder(self.name)}')
        print(f' - Model file: {self.names.model_path(self.name).name}')

    def predict(self, numerai_data_set: pd.DataFrame, save_for_submission=False):
        print(f'\nRunning prediction for model {self.name} ...')
        print(f' - Rows: {len(numerai_data_set)}, columns: {len(numerai_data_set.columns)}')
        
        feature_cols = [f for f in numerai_data_set.columns if f.startswith("feature")]
        
        output_values = self.model.predict(numerai_data_set[feature_cols])
        output = pd.DataFrame({'prediction': output_values}, index=numerai_data_set.index)

        if save_for_submission:
            self.save_for_submission(output)
            
        return output

    def save_for_submission(self, output):
        submission_path = self.names.model_submission_path(self.name)
        print(f'  Saving results into: {submission_path}')
        output.to_csv(submission_path, header=True)
        print('  Saved!')

    @abstractmethod
    def load_model(self):
        # How the model is loaded belongs to each specific model
        pass
