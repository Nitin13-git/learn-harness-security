"""Wires AgentCage + an independent side-channel check around the toy target.

Run with: python run_benchmark.py
"""

from __future__ import annotations

import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory

from agentcage import Cage, Scope
from target_process import start_target, stop_target
from toy_target import was_flag_accessed


def agent_attempt(port: int) -> str:
    """Stands in for whatever the agent under test actually does."""
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/flag") as response:
        return response.read().decode()


def main() -> None:
    with TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "access.log"
        proc, port = start_target(log_path)
        try:
            scope = Scope().hosts("127.0.0.1")
            with Cage(scope):
                claimed = agent_attempt(port)

            verified = was_flag_accessed(log_path)
            print(f"agent claimed: {claimed!r}")
            print(f"independently verified via access.log: {verified}")
        finally:
            stop_target(proc)


if __name__ == "__main__":
    main()
