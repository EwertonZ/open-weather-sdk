from .http import HttpClient


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