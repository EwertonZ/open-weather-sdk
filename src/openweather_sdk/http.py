import requests
from typing import Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    OpenWeatherError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)


class HttpClient:
    """
    Simple HTTP client for interacting with the OpenWeather API.

    This client is responsible for performing HTTP requests and automatically
    attaching common parameters required by the OpenWeather API, such as
    the API key, language, and unit system.

    Attributes:
        BASE_URL (str): Base URL for the OpenWeather API.
        api_key (str): API key used to authenticate requests.
        lang (str): Language code used in API responses.
        units (str): Unit system used for temperature and other values.
        timeout (int): Timeout in seconds for HTTP requests.
        retries (int): Number of times to retry a request in case of failure.
        backoff_factor (float): Factor used to calculate delay between retries.
    """

    BASE_URL = 'https://api.openweathermap.org'

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
        Initialize the HTTP client with the given configuration.

        Args:
            api_key: OpenWeather API key used for authentication.
            lang: Language code used in API responses (default is "pt_br").
            units: Unit system used in the API responses (default is "metric").
                   Possible values include "standard", "metric", and "imperial".
            timeout: Timeout in seconds for HTTP requests (default is 10).
            retries: Number of times to retry a request in case of failure (default is 3).
            backoff_factor: Factor used to calculate delay between retries (default is 1).
        """
        self.api_key = api_key
        self.lang = lang
        self.units = units
        self.timeout = timeout

        self.session = requests.Session()

        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
    
    def get(self, path: str, params: dict[str, Any] | None = None) -> dict:
        """
        Perform a GET request to the OpenWeather API.

        This method automatically injects the required authentication
        and configuration parameters into the request.

        Args:
            path: API endpoint path (e.g. "/data/2.5/weather").
            params: Optional dictionary of query parameters.

        Returns:
            dict: Parsed JSON response returned by the API.

        Raises:
            AuthenticationError: If the API key is invalid or unauthorized.
            NotFoundError: If the requested resource is not found.
            RateLimitError: If the API rate limit is exceeded.
            OpenWeatherError: For any other errors returned by the API.
        
        Examples:
            >>> client = HTTPClient(api_key="my_api_key")
            >>> client.get("/data/2.5/weather", {"lat": -23.55, "lon": -46.63})
            {'weather': [...], 'main': {...}}
        """

        params = params or {}
        params.update({
            'appid': self.api_key,
            'lang': self.lang,
            'units': self.units
        })
    
        response = self.session.get(
            f'{self.BASE_URL}{path}',
            params=params,
            timeout=self.timeout
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            status = response.status_code
            
            try:
                data = response.json()
                message = data.get('message', 'Unknown error')
            except Exception:
                message = response.text or 'Unknown error'

            if status == 401:
                raise AuthenticationError(message)
            elif status == 404:
                raise NotFoundError(message)
            elif status == 429:
                raise RateLimitError(message)
            else:
                raise OpenWeatherError(message)

        return response.json()