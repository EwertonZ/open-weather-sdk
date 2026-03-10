[![PyPI version](https://img.shields.io/pypi/v/weather-sdk-challenge.svg)](https://pypi.org/project/weather-sdk-challenge/)

# OpenWeather SDK

A lightweight and developer-friendly Python SDK for interacting with the
**OpenWeather API**.

This library provides a clean interface for retrieving:

-   Geographic coordinates for cities
-   Current weather conditions
-   5‑day weather forecasts

The SDK handles authentication, parameter injection, retries, and error
handling internally so developers can focus on building features.

------------------------------------------------------------------------

## Features

-   Simple and intuitive API
-   Automatic injection of required OpenWeather parameters
-   Built-in HTTP retry strategy
-   Custom exception handling
-   Typed response models using `dataclasses`
-   Fully tested with **pytest**
-   \~95% test coverage

------------------------------------------------------------------------

## Installation

### Install from source

Clone the repository and install in editable mode:

``` bash
pip install -e .
```

Or using **uv**:

``` bash
uv pip install -e .
```

------------------------------------------------------------------------

## Quick Start

``` python
from openweather_sdk import OpenWeatherClient

client = OpenWeatherClient(api_key="YOUR_API_KEY")
```

------------------------------------------------------------------------

## Get City Coordinates

``` python
coords = client.get_coordinates("São Paulo", country_code="BR")

print(coords.lat)
print(coords.lon)
```

Example return:

``` python
Coordinates(lat=-23.55, lon=-46.63)
```

------------------------------------------------------------------------

## Get Current Weather

``` python
from openweather_sdk import Coordinates

coords = Coordinates(lat=-23.55, lon=-46.63)

weather = client.get_current_weather(coords)

print(weather.temperature)
print(weather.description)
print(weather.icon)
```

Example return:

``` python
WeatherData(
    temperature=25.0,
    feels_like=27.0,
    min_temperature=24.0,
    max_temperature=26.0,
    humidity=70,
    pressure=1013,
    description="scattered clouds",
    icon="03d"
)
```

------------------------------------------------------------------------

## Get Weather Forecast

``` python
forecast = client.get_forecast(coords)

for item in forecast:
    print(item.dt_txt, item.weather.temperature)
```

Returns forecast data at **3‑hour intervals** for the next **5 days**.

------------------------------------------------------------------------

## Error Handling

The SDK raises custom exceptions for common API errors.

  Exception             Description
  --------------------- -------------------------
  AuthenticationError   Invalid API key
  NotFoundError         Resource not found
  RateLimitError        API rate limit exceeded
  OpenWeatherError      Generic API error

Example:

``` python
from openweather_sdk.exceptions import AuthenticationError

try:
    client.get_current_weather(coords)
except AuthenticationError:
    print("Invalid API key")
```

------------------------------------------------------------------------

## Running Tests

The project uses **pytest**.

Run tests:

``` bash
pytest
```

Run tests with coverage:

``` bash
pytest --cov=openweather_sdk --cov-report=term-missing
```

------------------------------------------------------------------------

## Project Structure

    open_weather_sdk/
    │
    ├── src/
    │   └── openweather_sdk/
    │       ├── client.py
    │       ├── http.py
    │       ├── models.py
    │       ├── exceptions.py
    │       └── __init__.py
    │
    ├── tests/
    │   ├── conftest.py
    │   ├── test_client.py
    │   └── test_http_client.py
    │
    ├── pyproject.toml
    └── README.md

------------------------------------------------------------------------

## Requirements

-   Python 3.10+
-   requests

Development dependencies:

-   pytest
-   pytest-cov

------------------------------------------------------------------------

## Contributing

Contributions are welcome!

If you would like to contribute:

1.  Fork the repository
2.  Create a feature branch
3.  Write tests for your changes
4.  Open a Pull Request

------------------------------------------------------------------------

## License

MIT License
