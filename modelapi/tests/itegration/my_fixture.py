import pytest
import sys
from pathlib import Path

ROOT_DIR = Path.joinpath(Path("."),"src").resolve()
print(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)

print(sys.path)

from src.mongo import MongoModel

@pytest.fixture
def mongo_obj():
    return MongoModel()