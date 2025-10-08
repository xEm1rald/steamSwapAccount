from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class UserVDF:
    SteamID64: Optional[int] = None
    PersonaName: Optional[str] = None
    AccountName: Optional[str] = None
    RememberPassword: Optional[int] = None
    WantsOfflineMode: Optional[int] = None
    SkipOfflineModeWarning: Optional[int] = None
    AllowAutoLogin: Optional[int] = None
    MostRecent: Optional[int] = None
    Timestamp: Optional[int] = None

    def todict(self):
        return asdict(self)