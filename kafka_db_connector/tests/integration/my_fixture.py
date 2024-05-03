import pytest
import sys
from pathlib import Path

ROOT_DIR = str(Path.joinpath(Path("."),"src").resolve())
print(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)

print(sys.path)

from kafka_db_connector.src.mongo import MongoModel

@pytest.fixture
def mongo_obj():
    return MongoModel()