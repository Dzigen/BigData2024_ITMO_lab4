import pymongo
from settings import DB_USER_NAME, DB_USER_PWD, DB_NAME, TABLE_NAME
from typing import List, Dict
from logger import Logger

SHOW_LOG = True

class MongoModel:
    def __init__(self) -> None:
        logger = Logger(SHOW_LOG)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating MongoModel-class")
        self.log.info(f"{DB_USER_NAME} , {DB_USER_PWD} , {DB_NAME}")

        self.client = pymongo.MongoClient("mongodb://mongo:27017", 
                                          username=DB_USER_NAME, password=DB_USER_PWD,
                                          authSource=DB_NAME)
        self.log_db = self.client[DB_NAME]
        self.requests_collection = self.log_db[TABLE_NAME]

    @Logger.cls_se_log(info="Insert item to database")
    def insert(self, data: Dict[str,object]) -> pymongo.results.InsertManyResult:
        response = self.requests_collection.insert_one(data)
        return response
    
if __name__ == "__main__":
    db = MongoModel()
    
    data = [{"val1": 1, "val2": 2}, {"val3": 3}]
    resp = db.insert(data)

    print(resp)