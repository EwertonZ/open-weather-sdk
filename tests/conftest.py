import pytest
from openweather_sdk import OpenWeatherClient
from openweather_sdk.http import HttpClient


@pytest.fixture
def client():
    return OpenWeatherClient(api_key="test_api_key")

@pytest.fixture
def http_client():
    return HttpClient(api_key="test_api_key")