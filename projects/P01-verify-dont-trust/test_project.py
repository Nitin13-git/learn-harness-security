from pathlib import Path

import pytest
from agentcage import Cage, Scope
from target_process import start_target, stop_target
from toy_target import was_flag_accessed

from run_benchmark import agent_attempt


def test_verification_catches_access_through_an_allowed_scope(tmp_path: Path) -> None:
    log_path = tmp_path / "access.log"
    proc, port = start_target(log_path)
    try:
        scope = Scope().hosts("127.0.0.1")
        with Cage(scope):
            agent_attempt(port)
        assert was_flag_accessed(log_path)
    finally:
        stop_target(proc)


def test_cage_blocks_the_attempt_when_host_is_not_in_scope(tmp_path: Path) -> None:
    log_path = tmp_path / "access.log"
    proc, port = start_target(log_path)
    try:
        scope = Scope()  # no hosts granted
        # Whatever is calling agent_attempt (here, urllib) may wrap the
        # underlying CageViolation in a library-specific exception — e.g.
        # urllib re-raises any OSError (CageViolation is a PermissionError,
        # which is an OSError) as its own URLError. Don't assert on the
        # exact exception class a caller happens to wrap it in; assert on
        # the thing that actually matters: the side effect never happened.
        with Cage(scope), pytest.raises(OSError):
            agent_attempt(port)
        assert not was_flag_accessed(log_path)
    finally:
        stop_target(proc)
