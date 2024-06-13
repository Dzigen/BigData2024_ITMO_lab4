import pytest
import sys
from pathlib import Path

ROOT_DIR = Path.joinpath(Path("."),"src").resolve()
print(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)

print(sys.path)

from src.kafka_producer import KafkaModel

@pytest.fixture
def kafka_obj():
    return KafkaModel()