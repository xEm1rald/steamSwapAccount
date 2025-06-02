# Swap Steam Account (PowerShell)

This Python script allows you to easily switch between Steam accounts on Windows.  
It automatically generates a `.ps1` PowerShell script that updates the Windows registry and `loginusers.vdf` to set a specific account for auto-login and restarts Steam.

I take no responsibility for the use of this program. Use at your own risk.

## How to use? Example:
```
Last Auto-Login: PigTwig13
SteamID: 76561198xxxxxx | AccountName: PigTwig13
SteamID: 76561199xxxxxx | AccountName: SunShine41

Select Account to create shortcut (SteamID): 76561199xxxxxx
File 'SunShine41.ps1' successfully created.
```

---

## 🖥 Requirements

- Windows
- Python 3.10+
- Steam installed (at least one user must have logged in)
- PowerShell
- Permissions to edit the Windows registry
