import pymongo
from typing import List, Dict

from src.settings import secrets
from src.logger import Logger

SHOW_LOG = True

class MongoModel:
    def __init__(self) -> None:
        logger = Logger(SHOW_LOG)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating MongoModel-class")

        self.client = pymongo.MongoClient("mongodb://mongo:27017", 
                                          username=secrets.MONGO_MODELDB_USER_USERNAME, 
                                          password=secrets.MONGO_MODELDB_USER_PASSWORD,
                                          authSource=secrets.MONGO_MODELDB_NAME)
        self.log_db = self.client[secrets.MONGO_MODELDB_NAME]
        self.requests_collection = self.log_db[secrets.MONGO_TABLE_NAME]

    @Logger.cls_se_log(info="Insert item to database")
    def insert(self, data: Dict[str,object]) -> pymongo.results.InsertManyResult:
        response = self.requests_collection.insert_one(data)
        return response
    
if __name__ == "__main__":
    db = MongoModel()
    
    data = [{"val1": 1, "val2": 2}, {"val3": 3}]
    resp = db.insert(data)

    print(resp)