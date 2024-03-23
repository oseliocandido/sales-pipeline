import logging
from pathlib import Path

logger = logging.getLogger(__name__)
log_file_path = Path.cwd().parent / "logs/error.log"
handler = logging.FileHandler(filename=log_file_path)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
