import utils
from config import STEAM_REGISTRY_PATH


class AutoLoginUser:
    @staticmethod
    def get():
        return utils.get_reg(STEAM_REGISTRY_PATH, "AutoLoginUser")

    @staticmethod
    def set(username: str):
        utils.set_reg(STEAM_REGISTRY_PATH, "AutoLoginUser", username)