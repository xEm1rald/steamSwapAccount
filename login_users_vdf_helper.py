import os
import vdf

from dataclasses import dataclass, asdict


@dataclass
class UserVDF:
    SteamID64: int | None
    PersonaName: str | None
    AccountName: str | None
    RememberPassword: int | None
    WantsOfflineMode: int | None
    SkipOfflineModeWarning: int | None
    AllowAutoLogin: int | None
    MostRecent: int | None
    Timestamp: int | None


class LoginUsersVDF:
    def __init__(self, steam_path: str):
        self._path = os.path.join(steam_path, "config", "loginusers.vdf")
        data = self._get()
        print(data)
        self.users: list[UserVDF, ...] = [
            UserVDF(
                SteamID64 = user_steamid64,
                PersonaName = data.get('PersonaName'),
                AccountName = data.get('AccountName'),
                RememberPassword = data.get('RememberPassword'),
                WantsOfflineMode = data.get('WantsOfflineMode'),
                SkipOfflineModeWarning = data.get('SkipOfflineModeWarning'),
                AllowAutoLogin = data.get('AllowAutoLogin'),
                MostRecent = data.get('MostRecent'),
                Timestamp = data.get('Timestamp')
            ) for user_steamid64, data in data.get("users", {}).items()
        ]

    def __iter__(self):
        self._counter = 0
        return self

    def __next__(self):
        if self._counter < len(self.users):
            value = self.users[self._counter]
            self._counter += 1
            return value
        else:
            raise StopIteration

    def __str__(self):
        users = {}

        for user in self.users:
            user: UserVDF
            data = asdict(user)
            data.pop("SteamID64")
            users[user.SteamID64] = data

        return vdf.dumps({"users": users}, pretty=True)

    def _get(self) -> dict:
        """:return: accounts: list"""
        if not os.path.exists(self._path):
            return None

        with open(self._path, "r", encoding="utf-8") as f:
            content = vdf.load(f)

        return content

    def write_to(self, fp: str = None, disable_backup: bool = None) -> None:
        if not fp:
            fp = self._path

        if os.path.exists(fp) and os.path.samefile(self._path, os.path.abspath(fp)) and not disable_backup:
            storage = "backup"
            os.makedirs(storage, exist_ok=True)
            with open(self._path, "r", encoding="utf-8") as f:
                data = f.read()
            fp = os.path.join(storage, "loginusers_autobackup.vdf")
            with open(fp, "w", encoding="utf-8") as f:
                f.write(data)

        with open(fp, "w", encoding="utf-8") as f:
            f.write(self.__str__())