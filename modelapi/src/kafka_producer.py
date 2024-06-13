from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient
from kafka.errors import NoBrokersAvailable, KafkaError
import json
import time

from src.logger import Logger 

class KafkaModel:
    def __init__(self, log, config) -> None:
        self.config = config
        self.log = log

    @Logger.cls_se_log(info="Waiting of kafka-topic creation")
    def wait_topic_creation(self):
        # connecting to broker
        trials,connected = 10, False
        for i in range(trials):
            try:
                admin_client = KafkaAdminClient(
                    bootstrap_servers=self.config['server'],
                    api_version=self.config['version'])
                connected = True
                self.log.info("Broker exists!")
                break
            except (NoBrokersAvailable, AssertionError) as e:
                self.log.error(str(e))
                self.log.info(f"Waiting for broker creation ({i}/{trials}) ...")
                time.sleep(2)

        if not connected:
            raise NoBrokersAvailable
        
        # check if needed topic exists
        trials, topic_exists = 10, False
        for i in range(trials):
            existing_topics = admin_client.list_topics()
            self.log.info(f"Existing topics: {existing_topics}")
            if self.config['topic'] in existing_topics:
                self.log.info("Needed topic exists!")
                topic_exists = True
                break
            else:
                self.log.info(f"Waiting for spec-topic creation ({i}/{trials}) ...")
                time.sleep(2)
        
        if not topic_exists:
            raise KafkaError

        admin_client.close()

    @Logger.cls_se_log(info="Initializing kafka-producer")
    def init_producer(self):
        self.producer = KafkaProducer(
            bootstrap_servers=self.config['server'],
            api_version=self.config['version'],
            acks='all')

    @Logger.cls_se_log(info="Serializing data from json to dump")
    def serialize_data(self, data):
        return json.dumps(data).encode('utf-8')

    @Logger.cls_se_log(info="Sending message in kafka-topic")
    def send_message(self, data):
        data_dump = self.serialize_data(data)
        self.producer.send(self.config['topic'], data_dump)
        self.producer.flush()
        self.producer.close()

