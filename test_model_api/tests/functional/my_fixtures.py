import pytest
import time
from kafka import KafkaAdminClient
from kafka.errors import NoBrokersAvailable
import requests
from requests.exceptions import ConnectionError

ROOT_URL = "http://model_api:4567/"
URL = f"{ROOT_URL}make_predictions/"

@pytest.fixture
def broker_checker():
    connected = False
    while not connected:
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers="kafka_cntname:9092", client_id='test_python',
                api_version=(2,8,1))
            connected = True
        except NoBrokersAvailable:
            time.sleep(2)

    admin_client.close()

    print("broker exists")

@pytest.fixture
def api_checker():
    code = -1
    while code != 200:
        try:
            x = requests.head(ROOT_URL)
            code = x.status_code
        except ConnectionError:
            time.sleep(2)

    print("api is up")