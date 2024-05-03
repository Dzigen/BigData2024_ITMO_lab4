import sys
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, KafkaException
import json

from src.logger import Logger
from src.mongo import MongoModel

CONFIG = {
    'bootstrap.servers': 'kafka_cntname:9092',  # Список серверов Kafka
    'group.id': 'mygroup',                  # Идентификатор группы потребителей
    'auto.offset.reset': 'earliest'         # Начальная точка чтения ('earliest' или 'latest')
}
KAFKA_TOPIC = 'modelapi_logs'
SHOW_LOG = True

if __name__ == "__main__":
    logger = Logger(SHOW_LOG)
    log = logger.get_logger(__name__)
    
    # Create Consumer instance
    consumer = Consumer(CONFIG)
    consumer.subscribe([KAFKA_TOPIC])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # ожидание сообщения
            if msg is None:                   # если сообщений нет
                continue
            if msg.error():                   # обработка ошибок
                raise KafkaException(msg.error())
            else:
                # действия с полученным сообщением
                data = json.loads(msg.value().decode('utf-8'))
                print(f"Received message: {data}")

                log.info("Logging prediction in database...")
                db = MongoModel()
                db_output = db.insert(data)
                db.client.close()
                log.info(f"db response: {db_output}")
    finally:
        consumer.close()