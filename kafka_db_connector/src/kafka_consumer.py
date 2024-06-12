from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient
from kafka.errors import NoBrokersAvailable, KafkaError
import time

from src.logger import Logger

class KafkaModel:

    def __init__(self, log, config) -> None:
        self.config = config
        self.log = log

    def wait_topic_creation(self, id):
        # connecting to broker
        trials,connected = 5, False
        for i in range(trials):
            try:
                admin_client = KafkaAdminClient(
                    bootstrap_servers=self.config['server'], client_id=id,
                    api_version=self.config['version'])
                connected = True
                self.log.info("Broker exists!")
                break
            except NoBrokersAvailable:
                self.log.info(f"Waiting for broker creation ({i}/{trials}) ...")
                time.sleep(2)

        if not connected:
            raise NoBrokersAvailable
        
        # check if needed topic exists
        topic_exists, check_counter = False, 0
        while not topic_exists:
            check_counter +=1
            existing_topics = admin_client.list_topics()
            self.log.info(f"Existing topics: {existing_topics}")
            if self.config['topic'] in existing_topics:
                self.log.info("Needed topic exists!")
                topic_exists = True
            else:
                self.log.info(f"Waiting for spec-topic creation (trial {check_counter}) ...")
                time.sleep(2)
        
        admin_client.close()

    @Logger.cls_se_log(info="Initializing kafka-consumer")
    def init_consumer(self, c_id, g_id):

        self.wait_topic_creation(c_id)

        self.consumer = KafkaConsumer(
            self.config['topic'], group_id=g_id,
            bootstrap_servers=self.config['server'],
            api_version=self.config['version'])