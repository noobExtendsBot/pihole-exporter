from dataclasses import dataclass


@dataclass
class PiholeConfig:
    base_url: str
    password: str
    timeout: int = 10
    verify_ssl: bool = True
    session_buffer_seconds: int = 30

    def __post__init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
