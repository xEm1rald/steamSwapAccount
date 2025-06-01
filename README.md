# Swap Steam Account (PowerShell)

This Python script allows you to easily switch between Steam accounts on Windows.  
It automatically generates a `.ps1` PowerShell script that updates the Windows registry and `loginusers.vdf` to set a specific account for auto-login and restarts Steam.


## How to use? Example:
```
Last Auto-Login: myaccount
SteamID: 76561198xxxxxx | AccountName: myaccount
SteamID: 76561199xxxxxx | AccountName: secondaccount

Select Account to create shortcut (SteamID): 76561199xxxxxx
File 'secondaccount.ps1' successfully created.
```

---

## 🖥 Requirements

- Windows
- Python 3.10+
- Steam installed (at least one user must have logged in)
- PowerShell
- Permissions to edit the Windows registry

---

## 📦 Installation

```bash
git clone https://github.com/steamSwapAccount/steam-account-switcher.git
cd steam-account-switcher
python steam_switcher.py
```
