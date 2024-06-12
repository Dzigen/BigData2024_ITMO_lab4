from kafka import KafkaProducer
import json

from src.logger import Logger 

class KafkaModel:
    def __init__(self, log, config) -> None:
        self.config = config
        self.log = log

    @Logger.cls_se_log(info="Initializing kafka-producer")
    def init_producer(self, c_id):
        self.producer = KafkaProducer(
            bootstrap_servers=self.config['server'],
            client_id=c_id, api_version=self.config['version'])

    @Logger.cls_se_log(info="Serializing data from json to dump")
    def serialize_data(self, data):
        return json.dumps(data).encode('utf-8')

    @Logger.cls_se_log(info="Sending message in kafka-topic")
    def send_message(self, data):
        data_dump = self.serialize_data(data)
        self.producer.send(self.config['topic'], data_dump)
        self.producer.flush()

