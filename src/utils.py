import typing
import typing_extensions
from box import ConfigBox
from ruamel.yaml import YAML
import functools

yaml = YAML(typ="safe")

def get_params_config(params_path: str='params.yaml') -> ConfigBox:
    """_summary_

    Args:
        params_path (str, optional): _description_. Defaults to 'params.yaml'.

    Returns:
        ConfigBox: _description_
    """    
    return ConfigBox(yaml.load(open(params_path, encoding="utf-8")))

def cls_se_log(info):
    def wrap(func):
        @functools.wraps(func)
        def wrapped_f(self, *args, **kwargs):
            self.log.info('START_METHOD: ' + info)
            value = func(self, *args, **kwargs)
            self.log.info('END_METHOD: ' + info)
            return value
        return wrapped_f
    return wrap