from providers.exceptions.provider_exception import ProviderException

class ProviderValidationException(ProviderException):
    """HTTP 400 - Bad Request a la API del proveedor."""
    def __init__(self, message: str, provider: str = None, raw_response: dict = None):
        super().__init__(message, status_code=400, provider=provider, raw_response=raw_response)

class ProviderServerException(ProviderException):
    """HTTP 502/503 - Fallo del lado del proveedor (reintentable)."""
    def __init__(self, message: str, provider: str = None, raw_response: dict = None, status_code: int = 502):
        super().__init__(message, status_code=status_code, provider=provider, raw_response=raw_response)

class ProviderTimeoutException(ProviderException):
    """HTTP 504 - Timeout al conectar a la API del proveedor."""
    def __init__(self, message: str, provider: str = None):
        super().__init__(message, status_code=504, provider=provider)
