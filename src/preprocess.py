from sklearn.model_selection import train_test_split
import pandas as pd
from typing import Tuple, List, Union
import typing_extensions

from utils import get_params_config
from logger import Logger

SHOW_LOG = True

class Preparator:
    """_summary_
    """    

    def __init__(self, train_s: float = 0.8, seed: int = 2, save_dir: str='.') -> None:
        """_summary_

        Args:
            test_s (float, optional): _description_. Defaults to 0.8.
            seed (int, optional): _description_. Defaults to 2.
            save_dir (str, optional): _description_. Defaults to '.'.
        """               
        self.train_s = train_s
        self.seed = seed
        self.save_dir = save_dir

        logger = Logger(SHOW_LOG)
        self.log = logger.get_logger(__name__)

        self.log.info("Initiating Preparator-class")


    def split(self, dataset_path: str, y_label='class', 
              train_savep: Union[None, str]=None, test_savep: Union[None, str]=None) -> Tuple[pd.DataFrame, pd.DataFrame, 
                                                                                              pd.DataFrame, pd.DataFrame]:
        """_summary_

        Args:
            dataset_path (str): _description_
            y_label (str, optional):  _description_. Defaults to 'class'.
            train_savep (Union[None, str], optional): _description_. Defaults to None.
            test_savep (Union[None, str], optional): _description_. Defaults to None.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: _description_
        """        

        self.log.info("Loading dataset")
        dataset: pd.DataFrame = pd.read_csv(dataset_path, sep=',')
        
        target_col: List[str] = [y_label]
        features_cols: List[str] = list(set(dataset.columns).difference(target_col))

        self.log.info("Spliting dataset on train/test parts")
        X_train, X_test, y_train, y_test = train_test_split(
            dataset[features_cols], dataset[target_col], 
            train_size=self.train_s, random_state=self.seed,
            stratify=dataset[target_col],
            shuffle=True)
        
        if train_savep is not None:
            self.log.info("Saving train part")
            train_part: pd.DataFrame = pd.concat([X_train, y_train], axis=1).reset_index(drop=True)
            train_part.to_csv(f"{self.save_dir}/{train_savep}", index=False)

        if test_savep is not None:
            self.log.info("Saving test part")
            test_part: pd.DataFrame = pd.concat([X_test, y_test], axis=1).reset_index(drop=True)
            test_part.to_csv(f"{self.save_dir}/{test_savep}", index=False)

        return X_train, X_test, y_train, y_test
        
if __name__ == "__main__":
    PARAMS_YAML_FILE = "./params.yaml"
    SAVE_DIR = "./data"
    DATASET_PATH = "./data/BankNote_Authentication.csv"
    TRAIN_SAVE_FILE = "train_part.csv"
    TEST_SAVE_FILE = "test_part.csv"

    params = get_params_config(params_path=PARAMS_YAML_FILE)
    train_size = params.prepare.train_size
    seed = params.prepare.seed

    prep = Preparator(
        train_s=train_size,
        seed=seed,
        save_dir=SAVE_DIR
    )

    prep.split(
        DATASET_PATH, train_savep=TRAIN_SAVE_FILE, 
        test_savep=TEST_SAVE_FILE)