# L01 — Why security-benchmark harnesses are different

A coding-agent harness assumes the agent is on your side: it might overreach
a config file or declare victory too early, but it isn't trying to defeat
the harness itself. Point the same agent at a security benchmark — "find
and exploit the vulnerability in this service" — and that assumption
breaks. The task now actively rewards escaping scope, lying about results,
and finding the cheapest path to "looks solved."

Three consequences follow directly from that, and they're the spine of this
course:

**Scope has to be adversarially sound, not just convenient.** A normal
harness grants broad filesystem access because it's annoying to scope
narrowly and nothing is trying to abuse the gap. A security-benchmark
harness has to assume the agent *will* try the gap, because finding gaps is
literally the task. This is why [AgentCage](https://github.com/Nitin13-git/agentcage)
denies by default at the process level — `open()`, `subprocess`, and
`socket.connect` are all checked against an explicit allowlist — rather
than trusting the agent to stay in its lane.

**Verification cannot ask the agent what happened.** "I got a shell on the
target" is not evidence. The harness needs to independently confirm the
claimed outcome — check that a flag file was actually read, that a
privileged command actually ran, that a specific response actually came
back from the target — using a channel the agent doesn't control. This is
the entire reason [HCP](https://github.com/Nitin13-git/hcp)'s `Verifier`
interface is a separate concern from the agent's own output, and why
[VerifyLoop](https://github.com/Nitin13-git/verifyloop) parses an external
test run's output rather than a self-report.

**Comparisons across models need the same adversarial task run the same
way.** If you're benchmarking which model is best at a security task, the
scope, the target, and the verification method all have to be held fixed —
otherwise a "better" score might just mean a looser cage.
[HarnessBench](https://github.com/Nitin13-git/harnessbench) exists to hold
everything but the model constant.

The projects in this course build these three properties into a toy
benchmark step by step, starting with the cage.
