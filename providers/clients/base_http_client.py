import logging
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from providers.exceptions import ProviderException


logger = logging.getLogger(__name__)


class BaseHTTPClient:
    """
    Cliente HTTP base para consumo de APIs externas.

    Provee:
    - Session con retry automático (3 intentos, backoff 0.5s)
    - Logging estructurado (provider, endpoint, status, duration)
    - Manejo de errores centralizado → ProviderException
    - Métodos públicos: request(), get(), post(), put(), delete()

    Subclases deben definir:
    - provider_name: str
    - Configurar base_url, headers en __init__
    """

    provider_name: str = "base"

    def __init__(self, base_url: str, headers: dict = None, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

        if headers:
            self.session.headers.update(headers)

        # Retry automático para errores de servidor
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def request(self, method: str, path: str, **kwargs) -> dict:
        """
        Ejecuta un request HTTP con logging y manejo de errores.

        Args:
            method: GET, POST, PUT, DELETE
            path: ruta relativa al base_url (ej: /v1/Viaje/Post)
            **kwargs: argumentos adicionales para requests (json, params, etc)

        Returns:
            dict con la respuesta JSON del servidor

        Raises:
            ProviderException: si el servidor responde con error
        """
        url = f"{self.base_url}{path}"
        start_time = time.time()

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs,
            )
        except requests.RequestException as e:
            duration = time.time() - start_time
            logger.error(
                "provider_request_failed",
                extra={
                    "provider": self.provider_name,
                    "method": method,
                    "endpoint": path,
                    "duration": round(duration, 3),
                    "error": str(e),
                },
            )
            raise ProviderException(
                message=f"Request failed: {e}",
                provider=self.provider_name,
            ) from e

        duration = time.time() - start_time

        logger.info(
            "provider_request",
            extra={
                "provider": self.provider_name,
                "method": method,
                "endpoint": path,
                "status": response.status_code,
                "duration": round(duration, 3),
            },
        )

        self._handle_errors(response, path)

        # Algunos endpoints devuelven vacío (ej: Cancel → 200 sin body)
        if not response.content:
            return {}

        return response.json()

    def get(self, path: str, **kwargs) -> dict:
        """GET request."""
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> dict:
        """POST request."""
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> dict:
        """PUT request."""
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> dict:
        """DELETE request."""
        return self.request("DELETE", path, **kwargs)

    def _handle_errors(self, response: requests.Response, path: str):
        """
        Manejo centralizado de errores HTTP.
        Lanza excepciones específicas según el status code para permitir manejo diferencial.
        """
        if response.status_code >= 400:
            try:
                body = response.json()
            except ValueError:
                body = {"raw": response.text}

            msg = f"[{self.provider_name}] {response.status_code} en {path}: {body}"
            
            if response.status_code == 400:
                from providers.exceptions import ProviderValidationException
                raise ProviderValidationException(msg, provider=self.provider_name, raw_response=body)
            elif response.status_code in [502, 503]:
                from providers.exceptions import ProviderServerException
                raise ProviderServerException(msg, provider=self.provider_name, raw_response=body, status_code=response.status_code)
            elif response.status_code == 504:
                from providers.exceptions import ProviderTimeoutException
                raise ProviderTimeoutException(msg, provider=self.provider_name)
            
            raise ProviderException(
                message=msg,
                status_code=response.status_code,
                provider=self.provider_name,
                raw_response=body,
            )
