from confluent_kafka import Producer
import json

CONFIG = {
    'bootstrap.servers': 'kafka_cntname:9092'
}
KAFKA_TOPIC = 'modelapi_logs'

class MyProducer:
    def __init__(self, config) -> None:
        self.client = Producer(config)

    # функция для сериализации данных в JSON
    def serialize_data(self, data):
        return json.dumps(data)

    # функция для отправки сообщения
    def send_message(self, topic, data):
        data_dump = self.serialize_data(data)
        self.client.produce(topic, value=data_dump)
        self.client.flush()

