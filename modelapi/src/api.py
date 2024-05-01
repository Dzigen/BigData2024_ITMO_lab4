from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

from src.predict import Evaluator
from src.mongo import MongoModel
from src.logger import Logger

PROD_MODEL_PATH = '../models/prod_model.pkl'
SHOW_LOG = True

class Body(BaseModel):
    inputs: List[List[float]]

logger = Logger(SHOW_LOG)        
app = FastAPI()

@app.post("/make_predictions/")
async def predict(body: Body):
    log = logger.get_logger(__name__)

    log.info("Strat label-preditions...")
    evaluator = Evaluator(PROD_MODEL_PATH)
    predictions = evaluator.predict(body.inputs)

    log.info("Logging prediction in database...")
    db = MongoModel()
    log_item = {'inputs': body.inputs,'predictions': predictions}
    log.info(f"log_item: {log_item}")
    db_output = db.insert(log_item)
    db.client.close()
    log.info(f"db response: {db_output}")

    response = {'predictions': predictions, 'log_id': str(db_output.inserted_id)}
    log.info(f"modelapi response: {response}")
    log.info("Done!")

    return response
