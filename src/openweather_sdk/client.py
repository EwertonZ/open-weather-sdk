from .http import HttpClient
from .models import Coordinates, ForecastData, WeatherData


class OpenWeatherClient:
    """
    A client for interacting with the OpenWeather API.
    """

    def __init__(
            self,
            api_key: str,
            lang: str = "pt_br",
            units: str = "metric",
            timeout: int = 10,
            retries: int = 3,
            backoff_factor: float = 1
    ):
        """
        Initialize the OpenWeatherClient with the given configuration.

        Args:
            api_key: OpenWeather API key used for authentication.
            lang: Language code used in API responses (default is "pt_br").
            units: Unit system used in the API responses (default is "metric"). Possible values include "standard", "metric", and "imperial".
            timeout: Timeout in seconds for HTTP requests (default is 10).
            retries: Number of times to retry a request in case of failure (default is 3).
            backoff_factor: Factor used to calculate delay between retries (default is 1).
        """
        self.http = HttpClient(
            api_key=api_key,
            lang=lang,
            units=units,
            timeout=timeout,
            retries=retries,
            backoff_factor=backoff_factor
        )
    
    def _build_location_query(
            self, 
            city_name: str, 
            country_code: str | None = None, 
            state_code: str | None = None
    ) -> str:
        """
        Build a location query string for the geocoding API.

        Args:
            city_name: Name of the city to get coordinates for.
            country_code: Optional ISO 3166 country code to disambiguate cities with the same name.
            state_code: Optional state code to further disambiguate cities with the same name.
        """
        parts = [city_name]

        if state_code:
            parts.append(state_code)
        if country_code:
            parts.append(country_code)

        return ",".join(parts)

    def get_coordinates(
            self, 
            city_name: str, 
            country_code: str | None = None, 
            state_code: str | None = None
    ) -> Coordinates | None:
        """
        Get the geographical coordinates (latitude and longitude) for a given city.

        Args:
            city_name: Name of the city to get coordinates for.
            country_code: Optional ISO 3166 country code to disambiguate cities with the same name.
            state_code: Optional state code to further disambiguate cities with the same name.
        
        Returns:
            Coordinates | None: Coordinates of the city if found, otherwise None.
        
        Raises:
            AuthenticationError: If the API key is invalid or unauthorized.
            RateLimitError: If the API rate limit is exceeded.
            OpenWeatherError: For other API errors returned by the API.

        Examples:
            >>> client = OpenWeatherClient(api_key="my_key")
            >>> client.get_coordinates("São Paulo", country_code="BR")
            Coordinates(lat=-23.55, lon=-46.63)
        """
        
        query = self._build_location_query(city_name, country_code, state_code)

        response = self.http.get("/geo/1.0/direct", params={"q": query, "limit": 1})

        if not response:
            return None
        
        location = response[0]

        lat = location.get("lat")
        lon = location.get("lon")

        if lat is None or lon is None:
            return None
        
        return Coordinates(lat=lat, lon=lon)

    def get_current_weather(self, coordinates: Coordinates) -> WeatherData:
        """
        Get the current weather conditions for the specified coordinates.

        Args:
            coordinates: Coordinates object containing latitude and longitude.

        Returns:
            WeatherData: Current weather data returned by the API.

        Raises:
            AuthenticationError: If the API key is invalid or unauthorized.
            RateLimitError: If the API rate limit is exceeded.
            OpenWeatherError: For any other errors returned by the API. 
        
        Examples:
            >>> client = OpenWeatherClient(api_key="my_key")
            >>> coords = Coordinates(lat=-23.55, lon=-46.63)
            >>> client.get_current_weather(coords)
            WeatherData(temperature=25.0, feels_like=27.0, ...)
        """
        params = {
            "lat": coordinates.lat,
            "lon": coordinates.lon
        }

        data = self.http.get("/data/2.5/weather", params=params)

        return WeatherData(
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            min_temperature=data["main"]["temp_min"],
            max_temperature=data["main"]["temp_max"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            description=data["weather"][0]["description"],
            icon=data["weather"][0]["icon"]
        )
    
    def get_forecast(self, coordinates: Coordinates) -> list[ForecastData]:
        """
        Get the weather forecast for the next 5 days at 3-hour intervals for the specified coordinates.

        Args:
            coordinates: Coordinates object containing latitude and longitude.

        Returns:
            list[ForecastData]: A list of forecast data for the forecast periods.

        Raises:
            AuthenticationError: If the API key is invalid or unauthorized.
            RateLimitError: If the API rate limit is exceeded.
            OpenWeatherError: For any other errors returned by the API.
        """
        params = {
            "lat": coordinates.lat,
            "lon": coordinates.lon
        }

        data = self.http.get("/data/2.5/forecast", params=params)

        return [
            ForecastData(
                timestamp=item["dt"],
                dt_txt=item["dt_txt"],
                weather=WeatherData(
                    temperature=item["main"]["temp"],
                    feels_like=item["main"]["feels_like"],
                    min_temperature=item["main"]["temp_min"],
                    max_temperature=item["main"]["temp_max"],
                    humidity=item["main"]["humidity"],
                    pressure=item["main"]["pressure"],
                    description=item["weather"][0]["description"],
                    icon=item["weather"][0]["icon"]
                )
            )
            for item in data.get("list", [])
        ]