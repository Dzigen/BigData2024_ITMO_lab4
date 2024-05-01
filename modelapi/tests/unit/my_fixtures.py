import pytest
import sys
from pathlib import Path

ROOT_DIR = Path.joinpath(Path("."),"src").resolve()
print(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)

print(sys.path)

from src.predict import Evaluator
from src.train import Trainer, RandomForestConfig
from src.preprocess import Preparator
from src.utils import BaseUtils

@pytest.fixture
def preparator_obj():
    return Preparator()

@pytest.fixture
def trainer_obj():
    rf_config = RandomForestConfig()
    return Trainer(rf_config)

@pytest.fixture
def evaluator_obj():
    return Evaluator()

@pytest.fixture
def baseutils_obj():
    return BaseUtils()