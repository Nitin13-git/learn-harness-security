# Learn Harness Security

**Read it live: https://nitin13-git.github.io/learn-harness-security/**

A course on harness engineering for a specific, under-taught case: running
an agent against adversarial, security-benchmark tasks (xbow/xben-style
challenges) without the harness itself becoming the thing that gets
exploited.

General agent-harness material (see
[`learn-harness-engineering`](https://walkinglabs.github.io/learn-harness-engineering/en/)
for a broad treatment of the topic) covers state, verification, scope, and
lifecycle for *cooperative* tasks — the agent is trying to succeed, and the
harness's job is mostly to keep it honest and on-task. Security benchmarking
flips the assumption: the task itself may try to break out of its sandbox,
the "verification" has to independently confirm an exploit worked rather
than trust the agent's report, and scope has to be adversarially sound, not
just a convenience boundary. This course is built around that case, using
my own tools ([HCP](https://github.com/Nitin13-git/hcp),
[AgentCage](https://github.com/Nitin13-git/agentcage),
[HarnessBench](https://github.com/Nitin13-git/harnessbench),
[VerifyLoop](https://github.com/Nitin13-git/verifyloop),
[ReceiptLedger](https://github.com/Nitin13-git/receiptledger),
[EvoBench](https://github.com/Nitin13-git/evobench)) as the worked
reference implementation, not a fork of any existing course.

## Structure

- [`docs/lectures/`](docs/lectures/) — 6 lectures, one question each, with
  Mermaid diagrams — built and deployed as a [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
  site via GitHub Pages.
- [`docs/experiments/`](docs/experiments/) — real data and real test output,
  not hypotheticals: an 8-model security-benchmark scoreboard, and
  EvoBench's regression-mining loop run end to end.
- [`projects/`](projects/) — hands-on exercises against a toy vulnerable
  target, using the tools above.
- [`resources/`](resources/) — copy-ready templates (`AGENTS.md`,
  `feature_list.json`) adapted for a security-benchmarking harness.

## Building the docs locally

```bash
pip install mkdocs-material
mkdocs serve
```

## Status

6 lectures, 1 hands-on project, 2 data-backed experiments. Treat this as a
living draft — more is coming as the underlying tools mature.

## License

MIT
