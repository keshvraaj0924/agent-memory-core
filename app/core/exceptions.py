class AppException(Exception):
    """Base application exception with a stable public error code."""

    def __init__(self, message: str, code: str = "application_error") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class ConfigurationError(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="configuration_error")
