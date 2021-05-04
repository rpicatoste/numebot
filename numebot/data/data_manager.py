from numebot.data.data_reader import read_csv
from numebot.file_names_getter import FileNamesGetter


class DataManager:

    def __init__(self, file_names: FileNamesGetter, nrows: int) -> None:

        self.names = file_names

        self._training = None
        self._tournament = None
        self.nrows = nrows

    @property
    def training(self):
        if self._training is None:
            rows_txt = 'full' if self.nrows is None else f'{self.nrows} from'
            print(f'Loading {rows_txt} training data ...')
            self._training = read_csv(self.names.data_training_path, nrows=self.nrows)
        
        return self._training

    @property
    def tournament(self):
        if self._tournament is None:
            rows_txt = 'full' if self.nrows is None else f'{self.nrows} from'
            print(f'Loading {rows_txt} tournament data ...')
            self._tournament = read_csv(self.names.data_tournament_path, nrows=self.nrows)
        
        return self._tournament
