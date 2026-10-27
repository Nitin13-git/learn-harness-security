"""Starts/stops the toy target as a real subprocess, and waits for it to be ready."""

from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path


def start_target(log_path: Path) -> tuple[subprocess.Popen, int]:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]

    script = Path(__file__).parent / "toy_target.py"
    proc = subprocess.Popen([sys.executable, str(script), str(port), str(log_path)])
    _wait_until_listening(port)
    return proc, port


def stop_target(proc: subprocess.Popen) -> None:
    proc.terminate()
    proc.wait(timeout=5)


def _wait_until_listening(port: int, *, timeout_s: float = 5.0) -> None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return
        except OSError:
            time.sleep(0.05)
    raise RuntimeError(f"toy target never started listening on port {port}")
