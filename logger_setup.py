import logging
from pathlib import Path

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("app_logger