from xgboost import XGBRegressor

from numebot.models.numerai_model import NumeraiModel
from numebot.data.data_manager import DataManager


class ExampleModel(NumeraiModel):

    def load_model(self):
        class_name = str(self.__class__).rstrip('>\'').split('.')[-1]
        print(f'Creating {class_name}')
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
            self.model_ready = True
        else:
            print(f'WARNING: Model for {self.name} is not trained: Run train!')
    
        return model

    def train_model(self, data: DataManager):
        print('Training set:  ', data.train.shape)
        print("Training model...")
        
        self.model.fit(data.feature_names, data.train['target'])

        if not self.testing:
            self.save_model()
        else:
            print('Testing mode: trained model not saved.')
        
        self.model_ready = True
        print('Training finished!')
