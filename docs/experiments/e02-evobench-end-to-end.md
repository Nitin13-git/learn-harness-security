# E02 — EvoBench, end to end

L06 described the mine → store → bench loop in the abstract. This is the
same loop, run for real, with the actual test and its actual output — not a
hypothetical. The full source is
[`evobench/tests/test_integration.py`](https://github.com/Nitin13-git/evobench/blob/main/tests/test_integration.py).

## The setup

A deliberately simple failure: a test suite that asserts `2 + 2 == 5`.

```python
_FAILING_SUITE = """
def test_adds_wrong():
    assert (2 + 2) == 5
"""
```

## Step 1 — something fails, caught by VerifyLoop

```python
test_file = tmp_path / "test_target.py"
test_file.write_text(_FAILING_SUITE)
result = run(f"{sys.executable} -m pytest -q {test_file}")
assert not result.ok
```

`result` is a real `verifyloop.TestRunResult` — parsed from an actual
pytest subprocess run, not constructed by hand.

## Step 2 — mine it, autonomously

```python
suite = Suite(tmp_path / "suite.jsonl", tmp_path / "manifest.json")
observe(
    suite,
    task_id="arithmetic-regression-1",
    prompt="what is 2 + 2?",
    bad_output="5",
    run_result=result,
)
```

One call. No one wrote `arithmetic-regression-1` as a benchmark task by
hand — `observe()` derived it from the failure itself, including pulling
`AssertionError` as the failure category from VerifyLoop's triage of
`result`.

## Step 3 — every model gets checked against it

```python
buggy_model = MockAdapter("buggy-model", lambda _: "5")
fixed_model = MockAdapter("fixed-model", lambda _: "4")

results = BenchmarkRunner([buggy_model, fixed_model], suite.as_harnessbench_tasks()).run()
summaries = {s.model: s for s in summarize(results)}

assert summaries["buggy-model"].success_rate == 0.0
assert summaries["fixed-model"].success_rate == 1.0
```

`suite.as_harnessbench_tasks()` reconstructs a real `harnessbench.Task` from
what was stored — the mined regression check (`"5" not in output`) actually
discriminates between a model that would repeat the original bug and one
that wouldn't.

## Real output

```text
$ pytest -v tests/test_integration.py
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0
collecting ... collected 1 item

tests/test_integration.py::test_a_real_failure_becomes_a_discriminating_regression_task PASSED [100%]

============================== 1 passed in 0.25s ===============================
```

## What this actually demonstrates, and what it doesn't

It demonstrates that the loop is mechanically real: a failure caught by one
package (VerifyLoop) becomes durable state in another (ReceiptLedger, via
`Suite`) becomes a runnable task in a third (HarnessBench), with no manual
step in between, and the resulting task genuinely tells two different model
behaviors apart.

It does **not** demonstrate that pattern-matching on `bad_output` is a good
regression check for every kind of failure — L04's "what's worth keeping in
state" question applies here too: a literal-text check is cheap and
unambiguous, but it would miss a model that reproduces the *same bug*
phrased differently. That's the honest limitation flagged in EvoBench's own
README, not glossed over here: richer mining (re-running the original
reproduction automatically, rather than matching text) is the natural next
step, not yet built.

## Try it yourself

```bash
git clone https://github.com/Nitin13-git/evobench
cd evobench
pip install -e ".[dev]"
pytest -v tests/test_integration.py
```
