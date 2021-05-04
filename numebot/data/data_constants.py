from dataclasses import dataclass


@dataclass
class NumeraiColumns:
    # Dataframe column-related names
    target: str = 'target'
    prediction: str = 'prediction'

    # models_configs.csv columns
    name: str = 'numerai_name'
    model_code: str = 'model_code'


NC = NumeraiColumns()
