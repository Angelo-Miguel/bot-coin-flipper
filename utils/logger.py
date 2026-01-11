import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "flipper_bot.log")

# Basic logger configuration
logger = logging.getLogger("flipper_bot")
if not logger.handlers:
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    fh = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
    fh.setFormatter(fmt)
    logger.addHandler(fh)


def get_logger(name: str | None = None) -> logging.Logger:
    if name:
        return logging.getLogger(f"flipper_bot.{name}")
    return logger
