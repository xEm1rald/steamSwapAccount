import winreg
import vdf
import os


def get_reg(path: str, obj: str) -> tuple[str, str] | None:
    """:return: steam_path: str, auto_login: str"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
        query_obj = winreg.QueryValueEx(key, obj)[0]
        winreg.CloseKey(key)

        return query_obj
    except WindowsError:
        return

def set_reg(path: str, obj: str, new_value: str) -> None:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, obj, 0, winreg.REG_SZ, new_value)
        winreg.CloseKey(key)
    except WindowsError:
        return


def create_steam_login(steam_id64: str, username: str, script_path=None, steam_run_args=None) -> None:
    """create .ps1 file"""

    if not script_path:
        script_path = f"{username}.ps1"

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

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(powershell_script)

    print(f"File '{script_path}' successfully created.")