import logging
import logging.handlers

from pathlib import Path

def setup_logging(log_dir: str = "logs", level=logging.INFO) -> None:
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_path / "pihole_exporter.log",
        when="midnight",
        backupCount=30,
        encoding="utf-8"
    )
    file_handler.setFormatter(fmt)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt)

    logging.basicConfig(level=level, handlers=[file_handler, stream_handler])