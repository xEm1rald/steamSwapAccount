import logging
import sys
import os
from loguru import logger

from utils import get_reg

logger = logger

STEAM_REGISTRY_PATH = r"Software\Valve\Steam"
STEAM_PATH = get_reg(STEAM_REGISTRY_PATH, "SteamPath")

SERVER_PORT = 8997