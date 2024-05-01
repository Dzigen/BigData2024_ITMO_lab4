import pytest
import requests
import json

TEST_BODIES = [{'inputs': [[1,2,3,4]]}, {'inputs': []}]
TEST_RESPONSES = [{'predictions': [0]}, {'predictions': []}]
URL = "http://model_api:4567/make_predictions/"

@pytest.mark.parametrize("body,expected_code,expected_response", [
    (TEST_BODIES[0], 200, TEST_RESPONSES[0]),
    (TEST_BODIES[1], 200, TEST_RESPONSES[1])
])
def test_api_handler(body, expected_code, expected_response):
    output = requests.post(URL, json=body)

    print(output.content)

    actual_response = json.loads(output.content.decode())
    actual_code = output.status_code

    assert actual_code == expected_code
    assert actual_response['predictions'] == expected_response['predictions']