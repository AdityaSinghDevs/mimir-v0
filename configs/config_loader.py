import yaml
from pathlib import Path 
from typing import Dict

CONFIG_DIR = Path(__file__).parent

def load_configs(filename:str)-> Dict:
    if not filename:
        raise ValueError("Config file not specified")
    
    config_path = CONFIG_DIR / f"{filename}.yaml"

    with open (config_path, "r") as f:
        cfg = yaml.safe_load(f)

    return cfg