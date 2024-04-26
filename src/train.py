from sklearn.ensemble import RandomForestClassifier
import joblib
from dataclasses import dataclass
from typing import Union, List
import pandas as pd
import inspect

from logger import Logger
from utils import cls_se_log, get_params_config, load_data

SHOW_LOG = True

@dataclass
class RandomForestConfig:
    """_summary_
    """
    n_estimators: int = 100
    criterion: str = 'gini'
    max_depth: Union[None, int] = None
    min_samples_split: int = 2
    min_samples_leaf: int = 1
    min_weight_fraction_leaf: int = 0.0
    max_features: str = 'sqrt'
    max_leaf_nodes: Union[None, int] = None
    min_impurity_decrease: float = 0.0
    bootstrap: bool = True
    oob_score: bool = False
    random_state: Union[int, None] = None
    warm_start: bool = False
    class_weight: Union[str, None] = None
    ccp_alpha: float = 0.0
    max_samples: Union[None, float, int] = None
    monotonic_cst: Union[None, List[int]] = None

    @classmethod
    def from_dict(cls, dict_config):      
        return cls(**{
            k: v for k, v in dict_config.items() 
            if k in inspect.signature(cls).parameters
        })

class Trainer:
    """_summary_
    """
    def __init__(self, config: RandomForestConfig) -> None:
        """_summary_

        Args:
            config (RandomForestConfig): _description_
        """
        logger = Logger(SHOW_LOG)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating Trainer-class")

        self.config = config 
        self.model = RandomForestClassifier(**config.__dict__)
        

    @cls_se_log(info="Model training")
    def train(self, inputs, targets, verbose: int=0, n_jobs: Union[None, int]=None) -> None:
        """_summary_

        Args:
            verbose (int, optional): _description_. Defaults to 0.
            n_jobs (Union[None, int], optional): _description_. Defaults to None.
        """
        self.model.verbose = verbose
        self.model.n_jobs = n_jobs
        
        self.model.fit(inputs, targets)

    @cls_se_log(info="Saving model")
    def save(self, save_file: str) -> None:
        """_summary_

        Args:
            save_file (str): _description_
        """
        joblib.dump(self.model, save_file)
        

if __name__ == "__main__":
    PARAMS_YAML_PATH = "./params.yaml"
    TRAIN_PATH = './data/train_part.csv'
    MODEL_SAVE_PATH = './experiments/model.pkl'

    params = get_params_config(params_path=PARAMS_YAML_PATH)
    rf_config = RandomForestConfig.from_dict(params.train.to_dict())

    trainer = Trainer(rf_config)
    inputs, targets = load_data(TRAIN_PATH)

    trainer.train(inputs, targets, verbose=params.train.verbose, n_jobs=params.train.n_jobs)
    trainer.save(MODEL_SAVE_PATH)