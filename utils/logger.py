import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "flipper_bot.log")

# Logger raiz do bot
logger = logging.getLogger("flipper_bot")

if not logger.handlers:
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Console
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)

    # Arquivo rotativo
    fh = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)

    logger.addHandler(sh)
    logger.addHandler(fh)

    # Evita log duplicado se existir logger root configurado
    logger.propagate = False


def get_logger(name: str | None = None) -> logging.Logger:
    if name:
        return logging.getLogger(f"flipper_bot.{name}")
    return logger
