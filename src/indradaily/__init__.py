import os
from datetime import datetime
from importlib.metadata import version
from pathlib import Path

import yaml

__version__ = version(__name__)

def set_custom_loggers(level='DEBUG'):

    current_month = datetime.now().strftime("%Y-%m")

    base_logger_path = Path("logs")
    debug_logger_path = base_logger_path / Path(f"indrafetch-{current_month}-debug.log")

    os.makedirs(base_logger_path, exist_ok=True)

    loggers_config = dict()
    loggers_config['indrafetch'] = {
        'level': level,
        'filename': debug_logger_path,
    }

    return loggers_config

def get_params(yaml_path):
    with open(yaml_path, 'r') as file:
        params = yaml.safe_load(file)
    return params

all = ['set_custom_loggers', 'get_params']
