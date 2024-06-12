from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import json
from kafka.errors import NoBrokersAvailable
import time

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

    @Logger.cls_se_log(info="Initializing kafka-schema")
    def init_schema(self, id):
        
        #
        trials,connected = 5, False
        for _ in range(trials):
            try:
                admin_client = KafkaAdminClient(
                    bootstrap_servers=self.config['server'], client_id=id,
                    api_version=self.config['version'])
                connected = True
                break
            except NoBrokersAvailable:
                time.sleep(2)
        if not connected:
            raise NoBrokersAvailable
        
        # check if shema already exists
        existing_topics = admin_client.list_topics()
        self.log.info(f"Existing topics: {existing_topics}")
        if self.config['topic'] in existing_topics:
            self.log.info("Shema already applied. Operation omitted")
            return
        
        # create topics by schema
        topic_list = []
        topic_list.append(NewTopic(
            name=self.config['topic'], 
            num_partitions=self.config['partitions'], 
            replication_factor=self.config['replications']))
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        
        admin_client.close()

