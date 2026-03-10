import pytest
import requests
from unittest.mock import Mock

from openweather_sdk.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    OpenWeatherError,
)

def test_http_get_success(http_client, monkeypatch):
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {"foo": "bar"}

    mock_get = Mock(return_value=mock_response)

    monkeypatch.setattr(
        http_client.session,
        "get",
        mock_get
    )

    result = http_client.get("/test")

    assert result == {"foo": "bar"}

def test_http_get_auth_error(http_client, monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = {"message": "Invalid API key"}
    mock_response.raise_for_status.side_effect = requests.HTTPError()

    mock_get = Mock(return_value=mock_response)

    monkeypatch.setattr(
        http_client.session,
        "get",
        mock_get
    )

    with pytest.raises(AuthenticationError):
        http_client.get("/test")

def test_http_get_not_found(http_client, monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"message": "Not found"}
    mock_response.raise_for_status.side_effect = requests.HTTPError()

    mock_get = Mock(return_value=mock_response)

    monkeypatch.setattr(
        http_client.session,
        "get",
        mock_get
    )

    with pytest.raises(NotFoundError):
        http_client.get("/test")
    
def test_http_get_rate_limit(http_client, monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.json.return_value = {"message": "Too many requests"}
    mock_response.raise_for_status.side_effect = requests.HTTPError()

    mock_get = Mock(return_value=mock_response)

    monkeypatch.setattr(
        http_client.session,
        "get",
        mock_get
    )

    with pytest.raises(RateLimitError):
        http_client.get("/test")

def test_http_get_generic_error(http_client, monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"message": "Internal error"}
    mock_response.raise_for_status.side_effect = requests.HTTPError()

    mock_get = Mock(return_value=mock_response)

    monkeypatch.setattr(
        http_client.session,
        "get",
        mock_get
    )

    with pytest.raises(OpenWeatherError):
        http_client.get("/test")
