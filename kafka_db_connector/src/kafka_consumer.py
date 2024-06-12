from kafka import KafkaConsumer
from logger import Logger

class KafkaModel:

    def __init__(self, log, config) -> None:
        self.config = config
        self.log = log

    @Logger.cls_se_log(info="Initializing kafka-consumer")
    def init_consumer(self, c_id, g_id):
        self.consumer = KafkaConsumer(
            self.config['topic'], group_id=g_id,
            bootstrap_servers=self.config['server'],
            client_id=c_id,
            api_version=self.config['version'])