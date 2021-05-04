import csv
import numpy as np
import pandas as pd


# Read the csv file into a pandas Dataframe as float16 to save space
def read_csv(file_path, nrows=None, save_memory=True):

    with open(file_path, 'r') as f:
        column_names = next(csv.reader(f))

    if save_memory:
        dtypes = {x: np.float16 for x in column_names if x.startswith(('feature', 'target'))}
        df = pd.read_csv(file_path, dtype=dtypes, index_col=0, low_memory=False, nrows=nrows)
    else:
        df = pd.read_csv(file_path, index_col=0, low_memory=False, nrows=nrows)

    # Memory constrained? Try this instead (slower, but more memory efficient)
    # see https://forum.numer.ai/t/saving-memory-with-uint8-features/254
    # dtypes = {f"target": np.float16}
    # to_uint8 = lambda x: np.uint8(float(x) * 4)
    # converters = {x: to_uint8 for x in column_names if x.startswith('feature')}
    # df = pd.read_csv(file_path, dtype=dtypes, converters=converters)

    return df
