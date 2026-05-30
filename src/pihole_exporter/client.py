import logging
import time
from typing import Any, Optional

import requests
import urllib3

from .config import PiholeConfig
from .exceptions import BadAuthError, PiholeRequestError
from .models import AuthResponse

logger = logging.getLogger(__name__)


class PiholeClient:

    def __init__(self, config: PiholeConfig) -> None:
        self._config = config
        self._sid: Optional[str] = None
        self._sid_expires_at: float = 0.0
        self._http = requests.Session()
        self._http.verify = config.verify_ssl
        if not config.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _url(self, path: str) -> str:
        return f"{self._config.base_url}{path}"

    def _is_session_valid(self) -> bool:
        return bool(self._sid) and (time.monotonic() < self._sid_expires_at - self._config.session_buffer_seconds)

    def authenticate(self) -> None:
        resp = self._http.post(
            self._url("/auth"), json={"password": self._config.password}, timeout=self._config.timeout
        )
        if resp.status_code == 401:
            logger.warning("Check your auth variables")
            raise BadAuthError

        auth = AuthResponse.model_validate(resp.json())
        self._sid = auth.session.sid
        self._sid_expires_at = time.monotonic() + auth.session.validity
        self._http.headers.update({"X-FTL-SID": self._sid})

    def get(self, path: str) -> dict[str, Any]:
        if not self._is_session_valid():
            self.authenticate()
        try:
            resp = self._http.get(self._url(path=path))
            data: dict[str, Any] = resp.json()
            return data
        except Exception as ex:
            logger.error(f"Could not process your request: {ex}")
            raise PiholeRequestError(f"Request to {path} failed", cause=ex) from ex
