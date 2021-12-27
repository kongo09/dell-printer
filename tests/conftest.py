import pytest

@pytest.fixture()
def response_information():
    with open("tests/fixtures/response_information.html", "r") as mock_response:
        return mock_response.read()

@pytest.fixture()
def response_status():
    with open("tests/fixtures/response_status.html", "r") as mock_response:
        return mock_response.read()

@pytest.fixture()
def response_printer_volume():
    with open("tests/fixtures/response_printer_volume.html", "r") as mock_response:
        return mock_response.read()
