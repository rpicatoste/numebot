import dotenv
import os
from pathlib import Path

env_path = Path(os.path.dirname(os.path.realpath(__file__))).parent/".secret"
print(f'Loading credential data:')
print(f' - Current folder:', os.getcwd())
print(f' - .secret path:  ', env_path)

envs_dict = dotenv.dotenv_values(env_path)
print(' - Credentials loaded:', envs_dict.keys())
locals().update(envs_dict)
