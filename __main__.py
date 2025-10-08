import webview
import os
import subprocess
import sys
from config import SERVER_PORT, logger


def run_app(path: str):
    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", path, "--server.headless", "true", "--server.port", str(SERVER_PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


if __name__ == "__main__":
    # start web server
    proc = run_app(os.path.join("app", "app.py"))
    app_url = f"http://localhost:{SERVER_PORT}/?embed=true"
    logger.info(f"Run local server with url: {app_url}")

    # start browser window
    webview.create_window("Steam Swap Account", app_url, width=800, height=1000)
    webview.start()