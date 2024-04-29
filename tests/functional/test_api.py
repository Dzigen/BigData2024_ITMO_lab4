import pytest
import requests
import json

TEST_BODIES = [{'inputs': [[1,2,3,4]]}]
TEST_RESPONSES = [{'predictions': [0]}]
URL = "http://127.0.0.1:4567/make_predictions/"

@pytest.mark.parametrize("body,expected_code,expected_response", [
    (TEST_BODIES[0], 200, TEST_RESPONSES[0])
])
def test_api_handler(body, expected_code, expected_response):
    output = requests.post(URL, json=body)

    actual_response = json.loads(output.content.decode())
    actual_code = output.status_code

    assert actual_code == expected_code
    assert actual_response == expected_response