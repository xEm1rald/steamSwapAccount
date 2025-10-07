import webview
import os
import subprocess
import sys


def run_app(path: str):
    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", path, "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


if __name__ == "__main__":
    # start web server
    proc = run_app(os.path.join("app", "app.py"))

    # start browser window
    webview.create_window("Steam Swap Account", "http://localhost:8501/", frameless=False, width=1500, height=700)
    webview.start()