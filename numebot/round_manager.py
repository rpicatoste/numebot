import importlib
import numerapi
import pandas as pd

from numebot.data.data_constants import NC
from numebot.data.data_manager import DataManager
from numebot.file_names_getter import FileNamesGetter
from numebot.utils import to_camel_case


class RoundManager:

    def __init__(self, numerai_folder, nrows=None, public_id=None, secret_key=None) -> None:
        """
        nrows: Limit the lines in each csv read to nrows.
        """

        self.napi = numerapi.NumerAPI(verbosity="info", public_id=public_id, secret_key=secret_key)

        self.current_round = self.napi.get_current_round()
        print(f'Current round: {self.current_round}')

        self.names = FileNamesGetter(numerai_folder, current_round=self.current_round)
        self.data = DataManager(file_names=self.names, nrows=nrows)
        self.models_dict = self.load_models()

        # Download current dataset
        self.napi.download_current_dataset(dest_path=self.names.data_folder, unzip=True)

    def load_models(self):
        self.model_cfgs = pd.read_csv(self.names.model_configs_path).set_index('numerai_name', drop=True)

        models_dict = {}
        for name, config_row in self.model_cfgs.iterrows():
            try:
                model_class = _import_class(config_row[NC.model_code])
                models_dict[name] = model_class(config_row, file_names=self.names)

            except Exception as exc:
                print(f'\nERROR: Model {name} could not be added to the models list.')
                print(exc)
                
        return models_dict

    def models_info(self):
        for _, model in self.models_dict.items():
            model.info()

    def generate_predictions_for_all_models(self,):
        for model_name, model in self.models_dict.items():
            if self.names.model_submission_path(model_name).exists():
                print(f'Predictions already exist for {model_name}, skipping ...')
                continue

            _ = model.predict(self.data.tournament, save_for_submission=True)

    def submit_predictions(self):
        models_dict = self.napi.get_models()

        for model_name, model in self.models_dict.items():
            model_id = models_dict[model_name]
            
            # upload predictions
            file_path = self.names.model_submission_path(model_name)
            if not file_path.exists():
                print(f'\nPredictions for model {model_name} do not exist. Continue with next model')
                continue

            print(f'\nUploading file for model {model_name}: {file_path}')
            submission_id = self.napi.upload_predictions(file_path, model_id=model_id)
            print('submission_id:', submission_id)
            # check submission status
            print('Submission status/scores:')
            print(self.napi.submission_status(model_id=model_id))
            
        print('All models\' predictions submitted.')

def _import_class(module_name: str) -> type:
    """Import class from a module, e.g. 'text_recognizer.models.MLP'"""
    # It is assumed that the class name is the camel case version of the module name.
    class_name = to_camel_case(module_name.rsplit(".", 1)[1])
    
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)

    return class_
