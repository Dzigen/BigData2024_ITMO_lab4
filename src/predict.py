from sklearn.ensemble import RandomForestClassifier
import joblib
from dataclasses import dataclass
from typing import Union, List
import pandas as pd
import inspect
import json
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score, recall_score, precision_score

from logger import Logger
from utils import cls_se_log, get_params_config, load_data

SHOW_LOG = True

class Evaluator:
    def __init__(self, model_path: Union[str, None]=None) -> None:
        logger = Logger(SHOW_LOG)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating Evaluator-class")

        if model_path is not None:
            self.load_model(model_path)

    @cls_se_log(info="Load model")
    def load_model(self, model_path):
        self.model = joblib.load(model_path)
    
    @cls_se_log(info="Evaluating model")
    def predict(self, inputs: List[List[float]], targets: List[float], save_path: Union[str,None] = None) -> dict[str, float]:
        
        predictions = self.model.predict(inputs)

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
    TEST_PATH = './data/test_part.csv'
    METRICS_SAVE_PATH = './experiments/metrics.json'

    params = get_params_config(params_path=PARAMS_YAML_PATH)
    evaluator = Evaluator(MODEL_PATH)
    inputs, targets = load_data(TEST_PATH)

    metrics = evaluator.predict(inputs, targets, save_path=METRICS_SAVE_PATH)