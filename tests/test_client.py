from unittest.mock import Mock
from openweather_sdk import Coordinates, ForecastData, WeatherData


def test_get_coordinates_returns_coordinates(client, monkeypatch):
    mock_response = [
        {
            "lat": -23.55,
            "lon": -46.63
        }
    ]

    mock_get = Mock(return_value=mock_response)

    monkeypatch.setattr(client.http, "get", mock_get)

    coords = client.get_coordinates("São Paulo", country_code="BR", state_code="SP")

    assert isinstance(coords, Coordinates)
    assert coords.lat == -23.55
    assert coords.lon == -46.63

def test_get_coordinates_returns_none_when_city_not_found(client, monkeypatch):
    mock_response = []

    mock_get = Mock(return_value=mock_response)

    monkeypatch.setattr(client.http, "get", mock_get)

    coords = client.get_coordinates("Cidade Inexistente")

    assert coords is None

def test_get_coordinates_returns_none_when_lat_lon_missing(client, monkeypatch):
    mock_response = [
        {
            "name": "São Paulo"
        }
    ]

    mock_get = Mock(return_value=mock_response)

    monkeypatch.setattr(client.http, "get", mock_get)

    coords = client.get_coordinates("São Paulo")

    assert coords is None

def test_get_current_weather(client, monkeypatch):
    mock_api_response = {
        "main": {
            "temp": 25.0,
            "feels_like": 27.0,
            "temp_min": 24.0,
            "temp_max": 26.0,
            "humidity": 60,
            "pressure": 1012
        },
        "weather": [
            {
                "description": "nublado",
                "icon": "04d"
            }
        ]
    }

    mock_get = Mock(return_value=mock_api_response)

    monkeypatch.setattr(
        client.http,
        "get",
        mock_get
    )

    coords = Coordinates(lat=-23.55, lon=-46.63)

    weather = client.get_current_weather(coords)

    assert isinstance(weather, WeatherData)
    assert weather.temperature == 25.0
    assert weather.description == "nublado"
    assert weather.icon == "04d"

def test_get_forecast_returns_list(client, monkeypatch):
    mock_api_response = {
        "list": [
            {
                "dt": 1710000000,
                "dt_txt": "2024-03-09 12:00:00",
                "main": {
                    "temp": 24,
                    "feels_like": 25,
                    "temp_min": 23,
                    "temp_max": 25,
                    "humidity": 65,
                    "pressure": 1010
                },
                "weather": [
                    {
                        "description": "light rain",
                        "icon": "10d"
                    }
                ]
            }
        ]
    }

    mock_get = Mock(return_value=mock_api_response)

    monkeypatch.setattr(
        client.http,
        "get",
        mock_get
    )

    coords = Coordinates(lat=-23.55, lon=-46.63)

    forecast = client.get_forecast(coords)

    assert isinstance(forecast, list)
    assert isinstance(forecast[0], ForecastData)
    assert forecast[0].weather.temperature == 24