from sklearn.ensemble import RandomForestClassifier
import joblib
from dataclasses import dataclass
from typing import Union, List, Dict
import pandas as pd
import inspect
import json
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score, recall_score, precision_score

from src.logger import Logger
from src.utils import BaseUtils

SHOW_LOG = True


class Evaluator(BaseUtils):
    """_summary_
    """

    def __init__(self, model_path: Union[str, None] = None) -> None:
        """_summary_

        Args:
            model_path (Union[str, None], optional): _description_. Defaults to None.
        """
        super(Evaluator, self).__init__()

        logger = Logger(SHOW_LOG)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating Evaluator-class")

        if model_path is not None:
            self.load_model(model_path)

    @Logger.cls_se_log(info="Load model")
    def load_model(self, model_path):
        self.model = joblib.load(model_path)

    @Logger.cls_se_log(info="Predicting labels by trained model")
    def predict(self, inputs: List[List[float]]) -> List[int]:
        """_summary_

        Args:
            inputs (List[List[float]]): _description_

        Returns:
            List[int]: _description_
        """
        
        predictions = []
        if len(inputs):
            predictions = self.model.predict(inputs).tolist()

        return predictions

    @Logger.cls_se_log(info="Compute scores")
    def compute_scores(self, targets: List[float], predictions: List[float], save_path: str = None) -> Dict[str, float]:
        """_summary_

        Args:
            targets (List[float]): _description_
            predictions (List[float]): _description_
            save_path (str, optional): _description_. Defaults to None.

        Returns:
            Dict[str, float]: _description_
        """
        metrics = {
            'roc_auc': roc_auc_score(targets, predictions),
            'accuracy': accuracy_score(targets, predictions),
            'f1_binary': f1_score(targets, predictions, average='binary'),
            'recall': recall_score(targets, predictions),
            'precision': precision_score(targets, predictions)
        }

        if save_path is not None:
            with open(save_path, 'w', encoding='utf-8') as fd:
                fd.write(json.dumps(metrics, indent=2))

        return metrics


if __name__ == "__main__":
    PARAMS_YAML_PATH = './params.yaml'
    MODEL_PATH = './experiments/model.pkl'
    TEST_PATH = './experiments/test_part.csv'
    METRICS_SAVE_PATH = './experiments/metrics.json'

    evaluator = Evaluator(MODEL_PATH)
    inputs, targets = evaluator.load_data(TEST_PATH)

    predictions = evaluator.predict(inputs)
    metrics = evaluator.compute_scores(
        targets, predictions, save_path=METRICS_SAVE_PATH)
