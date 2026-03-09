class OpenWeatherError(Exception):
    """
    Base exception for all errors raised by the OpenWeather SDK.
    """


class AuthenticationError(OpenWeatherError):
    """
    Raised when the API key is invalid or unauthorized.
    """


class NotFoundError(OpenWeatherError):
    """
    Raised when the requested resource is not found.
    """


class RateLimitError(OpenWeatherError):
    """
    Raised when the API rate limit is exceeded.
    """