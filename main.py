from steam.auto_login_user_reg import AutoLoginUser
from steam.login_users_vdf_helper import LoginUsersVDF
import config


def main():
    users_vdf = LoginUsersVDF(config.STEAM_PATH)
    print(users_vdf)


if __name__ == "__main__":
    main()