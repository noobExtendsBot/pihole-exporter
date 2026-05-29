class BadAuthError(Exception):
    def __init__(self, message="Authentication failed, check your password.", status_code=401):
        self.status_code = 401
        super().__init__(message)
