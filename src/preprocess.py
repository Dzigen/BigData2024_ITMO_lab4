from sklearn.model_selection import train_test_split
import pandas as pd
from typing import Tuple, List, Union
import typing_extensions

from src.logger import Logger
from src.utils import BaseUtils

SHOW_LOG = True


class Preparator(BaseUtils):
    """Класс предобработки датасетов
    """

    def __init__(self, train_s: float = 0.8, seed: int = 2, save_dir: str = '.') -> None:
        """

        Args:
            train_s (float, optional): Размер тренировочной выборки в пропорции от исходного датасета. Defaults to 0.8.
            seed (int, optional): зерно для используемых генераторов псевдо-случайных чисел. Defaults to 2.
            save_dir (str, optional): Директория для сохранения формируемых файлов в рамках данного класса. Defaults to '.'.
        """
        logger = Logger(SHOW_LOG)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating Preparator-class")

        self.train_s = train_s
        self.seed = seed
        self.save_dir = save_dir

    @Logger.cls_se_log(info="Split dataset on train/test parts")
    def split(self, dataset_path: str, y_label='class',
              train_savep: Union[None, str] = None, test_savep: Union[None, str] = None) -> Tuple[pd.DataFrame, pd.DataFrame,
                                                                                                  pd.DataFrame, pd.DataFrame]:
        """Разбиение датасета на тренировочную и тестовую части.

        Args:
            dataset_path (str): Путь до датасета, для которого будет проводиться разбиение.
            y_label (str, optional):  Название столбца в датасете, где хранятся целевые значения. Defaults to 'class'.
            train_savep (Union[None, str], optional): Названия файла для сохранения тренировочной части. Defaults to None.
            test_savep (Union[None, str], optional): Название файла для сохранения тестовой части. Defaults to None.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: _description_
        """

        dataset: pd.DataFrame = pd.read_csv(dataset_path, sep=',')

        target_col: List[str] = [y_label]
        features_cols: List[str] = list(
            set(dataset.columns).difference(target_col))

        X_train, X_test, y_train, y_test = train_test_split(
            dataset[features_cols], dataset[target_col],
            train_size=self.train_s, random_state=self.seed,
            stratify=dataset[target_col],
            shuffle=True)

        self.log.info(f"Train X/y sizes: {X_train.shape}/{y_train.shape}")
        self.log.info(f"Test X/y sizes: {X_test.shape}/{y_test.shape}")

        if train_savep is not None:
            self.log.info("Saving train part")
            train_part: pd.DataFrame = pd.concat(
                [X_train, y_train], axis=1).reset_index(drop=True)
            train_part.to_csv(
                f"{self.save_dir}/{train_savep}", index=False, sep=',')

        if test_savep is not None:
            self.log.info("Saving test part")
            test_part: pd.DataFrame = pd.concat(
                [X_test, y_test], axis=1).reset_index(drop=True)
            test_part.to_csv(f"{self.save_dir}/{test_savep}",
                             index=False, sep=',')

        return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    PARAMS_YAML_FILE = "./params.yaml"
    SAVE_DIR = "./experiments"
    DATASET_PATH = "./data/BankNote_Authentication.csv"
    TRAIN_SAVE_FILE = "train_part.csv"
    TEST_SAVE_FILE = "test_part.csv"

    params = Preparator.get_params_config(params_path=PARAMS_YAML_FILE)
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
