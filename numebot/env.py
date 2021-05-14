import dotenv
import os
from pathlib import Path

env_path = Path(os.path.dirname(os.path.realpath(__file__))).parent/".env"
print(f'Loading environment variables:')
print(f' - Current folder:', os.getcwd())
print(f' - .env path:  ', env_path)

envs_dict = dotenv.dotenv_values(env_path)
print(' - Variables loaded:', envs_dict.keys())
locals().update(envs_dict)
