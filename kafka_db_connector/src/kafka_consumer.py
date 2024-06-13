from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import NoBrokersAvailable, KafkaError
import time

from src.logger import Logger

class KafkaModel:

    def __init__(self, log, config) -> None:
        self.config = config
        self.log = log

    @Logger.cls_se_log(info="Initializing kafka-consumer")
    def init_consumer(self):
        self.consumer = KafkaConsumer(
            self.config['topic'], group_id=None,
            bootstrap_servers=self.config['server'],
            api_version=self.config['version'], 
            auto_offset_reset='earliest')
        
    @Logger.cls_se_log(info="Initializing kafka-schema")
    def init_schema(self):
        
        #
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
                self.log.info(f"Waiting for broker creation ({i}/{trials}) ...")
                self.log.error(str(e))
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
        
        # updated kafka schema
        existing_topics = admin_client.list_topics()
        self.log.info(f"Updated topics: {existing_topics}")

        admin_client.close()