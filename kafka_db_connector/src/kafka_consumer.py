from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from logger import Logger
import time

class KafkaModel:

    def __init__(self, log, config) -> None:
        self.config = config
        self.log = log

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

    @Logger.cls_se_log(info="Initializing kafka-consumer")
    def init_consumer(self, c_id, g_id):
        self.consumer = KafkaConsumer(
            self.config['topic'], group_id=g_id,
            bootstrap_servers=self.config['server'],
            client_id=c_id,
            api_version=self.config['version'])