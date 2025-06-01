import re
import os
import winreg


def get_reg() -> tuple[str, str]:
    """:return: steam_path: str, auto_login: str"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        auto_login = winreg.QueryValueEx(key, "AutoLoginUser")[0]
        steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
        winreg.CloseKey(key)

        return steam_path, auto_login
    except WindowsError:
        return


def create_steam_login(steam_id64: str, username: str, bat_path=None, steam_run_args=None) -> None:
    """create .ps1 file"""

    if not bat_path:
        bat_path = f"{username}.ps1"

    if not steam_run_args:
        steam_run_args = '-silent'

    powershell_script = \
(r"""$steamPath = (Get-ItemProperty "HKCU:\Software\Valve\Steam").SteamPath
$configFile = "$steamPath\config\loginusers.vdf"
"""
f"""
$steamID = "{steam_id64}"
$username = "{username}"
"""
r"""
# Check current (AutoLoginUser) in registry
$currentLogin = (Get-ItemProperty -Path "HKCU:\Software\Valve\Steam" -Name AutoLoginUser -ErrorAction SilentlyContinue).AutoLoginUser

if ($currentLogin -eq $username) {
    Write-Host "Account already is $username. Exit."
    exit
}

# Edit (AutoLoginUser) in registry
Set-ItemProperty -Path "HKCU:\\Software\\Valve\\Steam" -Name AutoLoginUser -Value $username

# Read & Edit (loginusers.vdf)
Write-Host "Editing loginusers.vdf..."
$content = Get-Content $configFile -Raw

# Set all fields to zero
$content = $content -replace '("MostRecent"\\s*")\\d(")', '${1}0${2}'

# Set one for selected SteamID
$pattern = '("' + [regex]::Escape($steamID) + '"\\s*\\{[^}]*?)("AllowAutoLogin"\\s*")0(")'
$content = [regex]::Replace($content, $pattern, '${1}${2}1${3}')
$pattern = '("' + [regex]::Escape($steamID) + '"\\s*\\{[^}]*?)("MostRecent"\\s*")0(")'
$content = [regex]::Replace($content, $pattern, '${1}${2}1${3}')

# Write to file
Set-Content -Path $configFile -Value $content -Encoding UTF8

# Close Steam
Write-Host "Closing Steam..."
Stop-Process -Name steam -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

# Run Steam
Write-Host "Start Steam..."
"""
f"""Start-Process "$steamPath\\Steam.exe" -ArgumentList "{steam_run_args}"

Write-Host "Account swapped to $username ($steamID)" """)

    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(powershell_script)

    print(f"File '{bat_path}' successfully created.")


def parse_login_users(steam_path) -> list:
    """:return: accounts: list"""
    loginusers_path = os.path.join(steam_path, "config", "loginusers.vdf")
    if not os.path.exists(loginusers_path):
        return None

    with open(loginusers_path, "r", encoding="utf-8") as f:
        content = f.read()

    accounts = re.findall(r'"([0-9]+)"\s*{\s*"AccountName"\s*"([^"]+)"', content)
    return accounts


def main():
    steam_path, auto_login = get_reg()
    if not steam_path or not auto_login:
        print("Something missing in registry. Are you logged in account?")
        return

    print(f"Last Auto-Login: {auto_login}")

    accounts = parse_login_users(steam_path)
    for steam_id, account_name in accounts:
        print(f"SteamID: {steam_id} | AccountName: {account_name}")

    selected_steamid = input("Select Account to create shortcut (SteamID): ")

    accounts = {steam_id: account_name for steam_id, account_name in accounts}
    if not selected_steamid in accounts.keys():
        print("Invalid SteamID.")
        return

    selected_steam_account = accounts[selected_steamid]

    create_steam_login(
        steam_id64=selected_steamid,
        username=selected_steam_account,
    )


if __name__ == '__main__':
    main()
