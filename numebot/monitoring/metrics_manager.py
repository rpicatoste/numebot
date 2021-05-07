from numerapi.numerapi import NumerAPI
import numpy as np
import pandas as pd
from typing import List

from numebot.data.data_constants import NC
from numebot.file_names_getter import FileNamesGetter


class MetricsManager:

    def __init__(self, napi: NumerAPI, model_names: List[str], file_names: FileNamesGetter):
        self.napi = napi
        self.model_names = model_names
        self.names = file_names

    def get_active_rounds(self):
        all_rounds_df = pd.DataFrame(self.napi.get_competitions())
        active_rounds_df = all_rounds_df[all_rounds_df['resolvedGeneral'] == False]
        active_rounds = sorted(active_rounds_df['number'].values.tolist())

        return active_rounds

    def download_round_details(self, download_only_active_rounds=True):
        active_rounds = self.get_active_rounds()
        current_round = self.napi.get_current_round()
        round_number = current_round

        download_only_active_rounds = download_only_active_rounds and self.names.monitoring_round_details_path.exists()
        if download_only_active_rounds:
            print(f'Downloading only data for active rounds {active_rounds} for models:\n\t{self.model_names}')
            full_df = self.load_round_details_csv()
        else:
            print(f'Downloading all the round details for models:\n\t{self.model_names}')
            full_df = pd.DataFrame()

        while round_number > 0:
            if download_only_active_rounds and round_number not in active_rounds:
                round_number -= 1
                continue

            print(f'Getting round {round_number}')
            round_details_dict = self.napi.round_details(round_number)
            own_items = [item for item in round_details_dict 
                         if item[NC.model_name] in self.model_names]
            own_round_df = pd.DataFrame(own_items)

            if len(own_round_df) == 0 and round_number not in active_rounds:
                print(f'No own models in {round_number}, stopping download.')
                break
                
            own_round_df[NC.round] = round_number 
            full_df = pd.concat([full_df, own_round_df])
            round_number -= 1

        else:
            print(f'Finished.')
        self.save_round_details_csv(full_df)

        return full_df

    def load_round_details_csv(self):
        df = pd.read_csv(self.names.monitoring_round_details_path, parse_dates=[NC.date])
        df[NC.date] = df[NC.date].dt.date.astype(np.datetime64)

        return df

    def save_round_details_csv(self, full_df: pd.DataFrame):
        full_df.reset_index(drop=True, inplace=True)
        full_df[NC.date] = full_df[NC.date].dt.date.astype(np.datetime64)
        full_df.sort_values([NC.model_name, NC.round, NC.date], inplace=True)
        full_df.drop_duplicates([NC.model_name, NC.round, NC.date], inplace=True)
        ordered_cols = [NC.model_name, NC.round, NC.date]
        ordered_cols = ordered_cols + [col for col in full_df.columns if col not in ordered_cols]
        full_df[ordered_cols].to_csv(self.names.monitoring_round_details_path, index=False)
