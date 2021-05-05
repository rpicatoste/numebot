from xgboost import XGBRegressor

from numebot.models.numerai_model import NumeraiModel


class ExampleModel(NumeraiModel):

    def load_model(self):
        class_name = str(self.__class__).rstrip('>\'').split('.')[-1]
        print(f'\nCreating {class_name}')
        model_file = self.names.model_path(self.name, suffix='xgb')

        # This is the model that generates the included example predictions file.
        # Taking too long? Set learning_rate=0.1 and n_estimators=200 to make this run faster.
        # Remember to delete example_model.xgb if you change any of the parameters below.
        model = XGBRegressor(max_depth=5, 
                             learning_rate=0.01, 
                             n_estimators=2000, 
                             n_jobs=-1, 
                             colsample_bytree=0.1)

        if model_file.exists():
            print("Loading pre-trained model...")
            model.load_model(model_file)
        else:
            print(f'WARNING: Model for {self.name} is not trained: Run training!')
    
        return model
