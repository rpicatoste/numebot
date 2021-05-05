from numebot.data.data_constants import NC
from numebot.data.data_reader import read_csv
from numebot.file_names_getter import FileNamesGetter


class DataManager:

    def __init__(self, file_names: FileNamesGetter, nrows: int, save_memory=True) -> None:

        self.names = file_names

        self._training = None
        self._tournament = None
        self._val = None
        self._test = None
        self._live = None

        self.save_memory = save_memory
        self.nrows = nrows

    @property
    def training(self):
        if self._training is None:
            rows_txt = 'full' if self.nrows is None else f'{self.nrows} from'
            print(f'Loading {rows_txt} training data ...')
            self._training = read_csv(self.names.data_training_path,
                                      nrows=self.nrows,
                                      save_memory=self.save_memory)
            self._training[NC.era] = self._training[NC.era].str.lstrip('era').astype(int)
        
        return self._training

    @property
    def tournament(self):
        if self._tournament is None:
            rows_txt = 'full' if self.nrows is None else f'{self.nrows} from'
            print(f'Loading {rows_txt} tournament data ...')
            self._tournament = read_csv(self.names.data_tournament_path, 
                                        nrows=self.nrows, 
                                        save_memory=self.save_memory)
        
        return self._tournament

    @property
    def val(self):
        if self._val is None:
            self._val = self.tournament[self.tournament[NC.data_type] == NC.val].copy()
            self._val[NC.era] = self._val[NC.era].str.lstrip('era').astype(int)

        return self._val

    @property
    def test(self):
        if self._test is None:
            self._test = self.tournament[self.tournament[NC.data_type] == NC.test].copy()
            self._test[NC.era] = self._test[NC.era].str.lstrip('era').astype(int)
                    
        return self._test

    @property
    def live(self):
        if self._live is None:
            self._live = self.tournament[self.tournament[NC.data_type] == NC.live].copy()
            self._live[NC.era] = self._live[NC.era].str.lstrip('era')

        return self._live
