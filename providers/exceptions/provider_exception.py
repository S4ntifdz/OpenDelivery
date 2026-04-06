class ProviderException(Exception):
    """
    Excepción base para errores de providers externos.

    El dominio solo captura esta excepción, nunca errores HTTP directos.
    Cada provider puede crear subclases específicas.
    """

    def __init__(self, message: str, status_code: int = None, provider: str = None, raw_response: dict = None):
        self.status_code = status_code
        self.provider = provider
        self.raw_response = raw_response
        super().__init__(message)
