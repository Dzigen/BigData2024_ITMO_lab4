import typing
import typing_extensions
from box import ConfigBox
from ruamel.yaml import YAML

yaml = YAML(typ="safe")

def get_params_config(params_path: str='params.yaml') -> ConfigBox:
    """_summary_

    Args:
        params_path (str, optional): _description_. Defaults to 'params.yaml'.

    Returns:
        ConfigBox: _description_
    """    
    return ConfigBox(yaml.load(open(params_path, encoding="utf-8")))