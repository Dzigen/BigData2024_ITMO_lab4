from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

from src.predict import Evaluator
from src.logger import Logger
from src.producer import MyProducer, CONFIG, KAFKA_TOPIC

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
    log_data = {'predictions': predictions, 'inputs': body.inputs}
    kafka_producer = MyProducer(CONFIG)
    kafka_producer.send_message(KAFKA_TOPIC, log_data)

    response = {'predictions': predictions}
    log.info(f"modelapi response: {response}")
    log.info("Done!")

    return response
