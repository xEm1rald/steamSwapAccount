import logging
import sys
import os
from utils import get_reg


def setup_logger(name: str, log_file: str=None, level=logging.INFO, disable_console: bool=False):
    formatter = logging.Formatter(
        "%(asctime)s | %(process)s | %(levelname)-7s | %(name)-4s | %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )

    file_handler = None
    if log_file:
        file_handler = logging.FileHandler(os.path.join("logs", log_file), encoding="utf-8")
        file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        if log_file and file_handler:
            os.makedirs("logs", exist_ok=True)
            logger.addHandler(file_handler)
        if not disable_console:
            logger.addHandler(console_handler)

    return logger


logger = setup_logger("LOG", level=logging.DEBUG)

STEAM_REGISTRY_PATH = r"Software\Valve\Steam"
STEAM_PATH = get_reg(STEAM_REGISTRY_PATH, "SteamPath")
