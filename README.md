# Learn Harness Security

A course on harness engineering for a specific, under-taught case: running
an agent against adversarial, security-benchmark tasks (xbow/xben-style
challenges) without the harness itself becoming the thing that gets
exploited.

General agent-harness material (see
[`learn-harness-engineering`](https://github.com/walkinglabs/learn-harness-engineering)
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
[ReceiptLedger](https://github.com/Nitin13-git/receiptledger)) as the
worked reference implementation, not a fork of any existing course.

## Structure

- [`lectures/`](lectures/) — the theory, one question per lecture.
- [`projects/`](projects/) — hands-on exercises against a toy vulnerable
  target, using the tools above.
- [`resources/`](resources/) — copy-ready templates (`AGENTS.md`,
  `feature_list.json`) adapted for a security-benchmarking harness.

## Status

Early — 3 lectures and 1 project are written; more are coming as the tools
above mature. Treat this as a living draft, not a finished syllabus.

## License

MIT
