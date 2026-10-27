# P01 — Verify, don't trust

Builds the two properties from [L02](../../lectures/L02-scope-as-a-security-boundary.md)
and [L03](../../lectures/L03-verification-you-can-trust.md) against a real,
if tiny, target: a scope that's an actual enforced boundary, and a
verification check that doesn't rely on the client's own report.

`toy_target.py` serves one endpoint, `/flag`, and writes to `access.log`
every time it's hit — that log is the independent side channel.
`run_benchmark.py` wires [AgentCage](https://github.com/Nitin13-git/agentcage)
around a stand-in "agent" that calls `/flag`, then checks `access.log`
directly instead of trusting what the HTTP response said.

## Run it

```bash
pip install -r requirements.txt
python run_benchmark.py
```

You should see the agent's claimed response *and* an independent
`verified via access.log: True`. Now edit `run_benchmark.py` to use an empty
`Scope()` (no granted host) and re-run — the attempt is blocked before it
ever reaches the target, and `access.log` never gets written. (The error
you'll see is `urllib.error.URLError`, not `CageViolation` directly —
`urllib` wraps any `OSError` subclass it catches into its own error type.
`CageViolation` is still what caused it; check `access.log` rather than the
exception class if you want ground truth.) That gap between "the agent
said it worked" and "the side channel confirms it worked" is the whole
point of this project.

## Tests

```bash
pip install -r requirements.txt pytest
pytest test_project.py
```

`test_verification_catches_access_through_an_allowed_scope` confirms the
happy path; `test_cage_blocks_the_attempt_when_host_is_not_in_scope`
confirms the cage actually stops an out-of-scope attempt rather than just
logging a warning.
