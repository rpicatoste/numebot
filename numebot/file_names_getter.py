from pathlib import Path

class FileNamesGetter:

    def __init__(self, numerai_folder, current_round) -> None:
        self.folder = Path(numerai_folder)
        assert self.folder.exists(), f'ERROR: Numerai folder does not exist: {self.folder}'
        self.round = current_round

    # Data
    @property
    def data_folder(self) -> Path:
        return self.folder/'data'

    @property
    def data_round_folder(self) -> Path:
        return self.data_folder/f'numerai_dataset_{self.round}'

    @property
    def data_training_path(self) -> Path:
        return self.data_round_folder/f'numerai_training_data.csv'

    @property
    def data_tournament_path(self) -> Path:
        return self.data_round_folder/f'numerai_tournament_data.csv'

    @property
    def example_predictions_path(self) -> Path:
        return self.data_round_folder/f'example_predictions.csv'

    # Models
    @property
    def models_folder(self) -> Path:
        return self.folder/'models'

    def model_folder(self, model: str) -> Path:
        return self.models_folder/model

    def model_path(self, model: str, suffix: str='xgb') -> Path:
        return self.model_folder(model)/f'model_{model}.{suffix}'

    def model_submission_path(self, model: str) -> Path:
        return self.model_folder(model)/'submissions'/f'{model}_submission_{self.round}.csv'

    def model_submission_status_log_path(self, model: str) -> Path:
        return self.model_folder(model)/f'{model}_submission_status_info.csv'

    def model_leaderboard_log_path(self, model: str) -> Path:
        return self.model_folder(model)/f'{model}_leaderboard_info.csv'

    @property
    def model_configs_path(self) -> Path:
        return self.models_folder/'model_configs.csv'

    @property
    def monitoring_round_details_path(self) -> Path:
        return self.models_folder/'round_details.csv'
