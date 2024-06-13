import pytest
import requests
import json
from my_fixtures import broker_checker, api_checker, URL
from urllib3.exceptions import NewConnectionError

TEST_BODIES = [{'inputs': [[1.4896,3.4288,-4.0309,-1.4259]]}, {'inputs': []}, {'inputs': "Invaild Input"}, {}]
TEST_RESPONSES = [{'predictions': [0]}, {'predictions': []}, {'predictions': []}, {'predictions': []}]

@pytest.mark.parametrize("body,expected_code,expected_response", [
    (TEST_BODIES[0], 200, TEST_RESPONSES[0]),
    (TEST_BODIES[1], 200, TEST_RESPONSES[1]),
    (TEST_BODIES[2], 422, TEST_RESPONSES[2]),
    (TEST_BODIES[3], 422, TEST_RESPONSES[3]),
])
def test_api_handler(broker_checker, api_checker, body, expected_code, expected_response):
    
    output = requests.post(URL, json=body)

    print(output.content)

    actual_response = json.loads(output.content.decode())
    actual_code = output.status_code

    assert actual_code == expected_code
    if actual_code == 200:
        assert actual_response['predictions'] == expected_response['predictions']