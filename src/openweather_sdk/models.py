from dataclasses import dataclass

@dataclass
class Coordinates:
    lat: float
    lon: float

@dataclass
class WeatherData:
    temperature: float
    feels_like: float
    min_temperature: float
    max_temperature: float
    humidity: int
    pressure: int
    description: str
    icon: str

@dataclass
class ForecastData:
    timestamp: int
    dt_txt: str
    weather: WeatherData