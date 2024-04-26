import typing
import typing_extensions
from box import ConfigBox
from ruamel.yaml import YAML
import functools
import pandas as pd
from typing import List, Tuple

yaml = YAML(typ="safe")

def get_params_config(params_path: str='params.yaml') -> ConfigBox:
    """_summary_

    Args:
        params_path (str, optional): _description_. Defaults to 'params.yaml'.

    Returns:
        ConfigBox: _description_
    """    
    return ConfigBox(yaml.load(open(params_path, encoding="utf-8")))

def cls_se_log(info: str):
    """Декаратор с аргументами для логирования старта и завершения работы вложенного метода

    Args:
        info (str): _description_
    """
    def wrap(func):
        @functools.wraps(func)
        def wrapped_f(self, *args, **kwargs):
            self.log.info('START_METHOD: ' + info)
            value = func(self, *args, **kwargs)
            self.log.info('END_METHOD: ' + info)
            return value
        return wrapped_f
    return wrap


def load_data(train_path: str, y_label: str = 'class') -> Tuple[List[List[float]],List[int]]:
    """_summary_

    Args:
        train_path (str): _description_
        y_label (_type_): _description_

    Returns:
        Tuple[List[List[float]],List[int]]: _description_
    """
    data = pd.read_csv(train_path, sep=',')
    
    print(f"Dataset size: {data.shape}")

    target_col = [y_label]
    features_cols = list(set(data.columns).difference(target_col))

    inputs = data[features_cols].values.tolist()
    targets = data[target_col].values.ravel().tolist()

    return inputs, targets
