from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

from src.predict import Evaluator
from src.logger import Logger
from src.kafka_producer import KafkaModel
from src.settings import secrets

PROD_MODEL_PATH = '../models/prod_model.pkl'
SHOW_LOG = True

class Body(BaseModel):
    inputs: List[List[float]]

logger = Logger(SHOW_LOG)        
log = logger.get_logger(__name__)

config = {'topic': secrets.KAFKA_TOPIC_NAME,
        'partitions': secrets.KAFKA_PARTITIONS_COUNT,
        'replications': secrets.KAFKA_REPLICATION_COUNT,
        'server': secrets.KAFKA_BOOTSTRAP_SERVER,
        'version': tuple(secrets.KAFKA_VERSION)}
kafka = KafkaModel(log, config)
kafka.init_schema("shema-init")


app = FastAPI()

@app.post("/make_predictions/")
async def predict(body: Body):
    log.info("Start predict labels by model...")
    evaluator = Evaluator(PROD_MODEL_PATH)
    predictions = evaluator.predict(body.inputs)
    response = {'predictions': predictions}

    log.info("Start logging predictions in database...")
    log_data = {'predictions': predictions, 'inputs': body.inputs}
    kafka.init_producer()
    kafka.send_message(log_data)

    log.info(f"modelapi response: {response}")
    log.info("Request handled successfully!")

    return response
