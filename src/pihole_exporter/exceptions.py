class BadAuthError(Exception):
    def __init__(self, message: str = "Authentication failed, check your password.", status_code: int = 401) -> None:
        self.status_code = 401
        super().__init__(message)


class PiholeRequestError(Exception):
    def __init__(self, message: str, cause: Exception) -> None:
        self.cause = cause
        super().__init__(message)
