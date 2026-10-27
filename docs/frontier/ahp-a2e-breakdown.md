# Frontier Harness Design Breakdowns — AHP and A2E

Two other efforts are standardizing close to the same thing
[HCP](../lectures/l05-the-four-subsystems-as-a-protocol.md) does. Worth
being upfront about that rather than writing as if this were an empty
field: **AHP** (Agent Harness Protocol, a Rust crate, `a3s-ahp`) and **A2E**
(Agent-to-Environment, a Python SDK pitched as "POSIX for AI agents").

!!! note "Sourcing"
    Read from primary sources where possible — AHP's crate page and GitHub
    repo, A2E's docs blog post and GitHub repo — not secondary summaries.
    Where something couldn't be independently verified (noted below), it's
    flagged rather than asserted.

## The most important finding: neither is an established standard

Before comparing designs, the adoption numbers matter more than the
pitches do. As of this writing:

| | AHP | A2E | HCP |
|---|---|---|---|
| GitHub stars | 7 | 1 | — |
| Contributors | not checked | 1 | 1 |
| Repo created | March 2026 | May 2026 | October 2026 |
| Most recent commit | Sept 2026 | Oct 2026 | (active) |
| Commits | 30 | — | — |

This is not "a newcomer walking into an established space." It's three
solo-or-near-solo efforts, all started within months of each other, all
converging on the same underlying problem independently. That's the
honest frame for everything below — and it's also why alignment is worth
proposing at all: none of us have won yet, and fragmentation this early
helps no one, the same lesson [OpenTelemetry](https://cncf.io/blog/2019/05/21/a-brief-history-of-opentelemetry-so-far)
learned by merging OpenTracing and OpenCensus in 2019 rather than letting
users keep guessing which one would survive.

## AHP (a3s-ahp)

A Rust crate, v2.4.0, MIT licensed, by the "A3S Lab Team." Implements
JSON-RPC 2.0 over stdio, HTTP, WebSocket, or Unix socket (gRPC is a
placeholder only). Core methods: `ahp/handshake`, `ahp/event`,
`ahp/query`, `ahp/batch`.

The design center is different from HCP's: AHP models a harness as a
**supervisor that makes decisions**, not a set of independent subsystems.
An agent sends an event at a control point (before a tool runs, during
planning, at a memory-recall step) and the harness returns a decision —
blocking events need a response, fire-and-forget ones don't. HCP's
`ScopeEnforcer.check()` is a yes/no gate called by the harness code itself;
AHP's model puts the *agent* in the loop asking permission at each step,
which is a real architectural difference, not just different naming for
the same idea.

AHP's docs mention "non-blocking runtime contract events for run
lifecycle, task lists, and verification" — so it has a verification-
adjacent concept. I did not read far enough into AHP's source to compare
how rigorously that enforces independent evidence (the property
[L03](../lectures/l03-verification-you-can-trust.md) treats as
non-negotiable) versus being another agent-reported event; that's a gap
in this breakdown, not a claim either way.

## A2E

A Python SDK (`pip install a2e` per its own docs — I could not
independently confirm this resolves on PyPI; the package JSON API
returned 404 when checked, which could mean a naming mismatch, a
transient issue, or that it isn't actually published under that exact
name). NDJSON wire format, Pydantic-validated, 80+ message types across
**10 capability namespaces**: `tools`, `memory` (three tiers), `env`
(RL-style reset/step/observe), `proc`, `learn`, `skills`, `toolkits`,
`chains`, `mcp` (an explicit bridge *to* MCP, worth noting — it treats MCP
as one namespace among ten, not a parallel concern the way HCP and MCP
sit side by side), and `subagents`.

That's a genuinely broader surface than HCP's four interfaces — A2E is
trying to standardize substantially more of an agent's environment, not
just the harness around it.

**And it has no dedicated verification namespace.** Evaluation happens
through `learn`: feedback carries a polarity, a score, and a dimension
(the docs list four dimensions in one place and five elsewhere —
correctness, helpfulness, safety, plan quality, tone), sourced from human
annotation, environment signals, or **model self-critique**. That last
source is exactly the failure mode
[L03](../lectures/l03-verification-you-can-trust.md) argues against: a
model judging its own transcript is still reading something the model
under test produced, one remove away from a self-report, not independent
of it. This is the same gap an April 2026 survey flagged as weak across
harness systems generally — A2E has more protocol surface than HCP
everywhere except exactly the place this course argues matters most for
adversarial tasks.

A2E's example code snippets reference names (`policy`, `select_action`,
`merge`) not defined on the page itself, so they read as illustrative
rather than verified-runnable; I didn't find test output or a working
quickstart to confirm otherwise.

## Where this leaves HCP

Narrower than both — four interfaces, not ten namespaces or an
event-decision model — but the narrowness is deliberate: HCP treats
verification as a first-class, independently-structured interface
(`run(target) -> VerificationReport` with evidence, not a feedback score)
specifically because that's the subsystem the rest of this space is
weakest on. That's a real differentiator grounded in what AHP and A2E's
own docs actually say, not a claim made in a vacuum.

It's also, honestly, the smallest and newest of the three by commit
history. The draft outreach in
[`hcp/outreach/`](https://github.com/Nitin13-git/hcp/tree/main/outreach)
proposes finding out whether AHP's or A2E's maintainers see the overlap
the same way, rather than three solo efforts quietly duplicating each
other's work for another year.
