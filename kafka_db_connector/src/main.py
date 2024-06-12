from kafka.errors import KafkaError
import json

from src.logger import Logger
from src.mongo import MongoModel
from src.settings import secrets
from src.kafka_consumer import KafkaModel

SHOW_LOG = True

if __name__ == "__main__":
    logger = Logger(SHOW_LOG)
    log = logger.get_logger(__name__)

    #
    config = {'topic': secrets.KAFKA_TOPIC_NAME,
            'partitions': secrets.KAFKA_PARTITIONS_COUNT,
            'replications': secrets.KAFKA_REPLICATION_COUNT,
            'server': secrets.KAFKA_BOOTSTRAP_SERVER,
            'version': tuple(secrets.KAFKA_VERSION)}
    kafka = KafkaModel(log, config)

    #
    kafka.init_schema("shema-init")
    kafka.init_consumer("python-consumer", 'mygroup')

    log.info("Start waiting for new messages...")
    try:
        for message in kafka.consumer:
            data = json.loads(message.value.decode('utf-8'))
            log.info(f"Received message: {data}")
            
            log.info("Start logging predictions in database...")
            db = MongoModel()
            db_output = db.insert(data)
            db.client.close()
            log.info(f"db response: {db_output}")
            
    except KafkaError as e:
        log.error(str(e))
        kafka.consumer.close()