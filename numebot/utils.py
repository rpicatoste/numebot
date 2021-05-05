from datetime import datetime
import os
from pathlib import Path


def to_camel_case(snake_str):
    # We capitalize the first letter of each component with the 'title' method and join them 
    # together.
    components = snake_str.split('_')
    
    return ''.join(x.title() for x in components)


def save_bak_version(path):
    path = pathify(path)
    
    new_name = path.name + f'.bak_{str(datetime.now().strftime("%Y-%m-%d-%H_%M_%S"))}'
    new_path = path.parent / new_name

    os.rename(path, new_path)
    print(f'Renamed {path.name} to {new_path.name}.')


def pathify(path):
    if isinstance(path, Path):
        return path
    
    return Path(path)
