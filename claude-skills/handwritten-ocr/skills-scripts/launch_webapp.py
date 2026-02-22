#!/usr/bin/env python3
"""
Web app launcher for the handwritten OCR Flask application.

Checks if the server is already running on port 5001.
If not, starts it in the background using the app's venv.
Then opens http://127.0.0.1:5001 in the default browser.
"""

import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

APP_DIR = Path("/Users/ranjithgonugunta/Documents/Python/claude-skills/handwritten-ocr")
VENV_PYTHON = APP_DIR / ".venv" / "bin" / "python"
APP_SCRIPT = APP_DIR / "app.py"
HOST = "127.0.0.1"
PORT = 5001
URL = f"http://{HOST}:{PORT}"


def is_port_in_use(host: str, port: int) -> bool:
    """Return True if something is already listening on host:port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0


def start_server() -> subprocess.Popen:
    """Start the Flask app in the background using the app's venv Python."""
    if not VENV_PYTHON.exists():
        print(f"Error: venv not found at {VENV_PYTHON}")
        print("Run this to set it up:")
        print(f"  cd {APP_DIR} && python3 -m venv .venv && source .venv/bin/activate")
        print(f"  pip install flask python-dotenv PyMuPDF anthropic python-docx PyPDF2 pikepdf")
        sys.exit(1)

    proc = subprocess.Popen(
        [str(VENV_PYTHON), str(APP_SCRIPT)],
        cwd=str(APP_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return proc


def wait_for_server(timeout: int = 15) -> bool:
    """Poll until the server is accepting connections or timeout expires."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if is_port_in_use(HOST, PORT):
            return True
        time.sleep(0.5)
    return False


# ── Main ──────────────────────────────────────────────────────────────────────

print(f"\nHandwritten OCR — Web App Mode")
print(f"{'─' * 50}")

if is_port_in_use(HOST, PORT):
    print(f"Server already running at {URL}")
else:
    print("Starting Flask server in the background...")
    start_server()
    print("Waiting for server to be ready...", end=" ", flush=True)
    if wait_for_server(timeout=15):
        print("ready!")
    else:
        print("\nError: Server did not start within 15 seconds.")
        print(f"Try starting it manually:")
        print(f"  cd {APP_DIR} && source .venv/bin/activate && python app.py")
        sys.exit(1)

print(f"\nOpening browser at {URL}")
webbrowser.open(URL)
print(f"{'─' * 50}")
print(f"Web app is running at: {URL}")
print(f"To stop it later run:  lsof -ti:{PORT} | xargs kill -9")
print(f"{'─' * 50}\n")
