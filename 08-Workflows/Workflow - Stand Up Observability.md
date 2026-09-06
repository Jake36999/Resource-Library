---
type: "workflow"
status: "active"
triggers: ["set up monitoring", "observability", "we don't know when it breaks", "alerting", "metrics and dashboards", "why is it slow", "production visibility", "on-call"]
preconditions: ["something is running that you care about staying up", "you can name one failure that would matter"]
stages: ["Name the failure you fear", "Instrument the one thing", "Add alerting only for what you would act on", "Add tracing when you cannot locate a fault", "Consolidate"]
exit_criteria: "you learn about the failure you named from your own system rather than from a user"
anti_patterns: ["dashboards before alerts", "collecting every metric available", "distributed tracing before a second service exists"]
---

# Workflow - Stand Up Observability

## Situation
Something is in production and you find out it broke when someone tells you. This vault's largest topic is Infrastructure & Observability, with nine resources, which makes it easy to start in the wrong place — the tools are all good and most of them are premature.

## Decide First
**Name one failure that would actually matter.** The API returns 500s. The nightly job silently produces no rows. Disk fills. One specific, nameable failure.

Everything below is ordered to detect *that* failure first. Observability programmes that begin with "let's get visibility" produce dashboards nobody reads; programmes that begin with a named failure produce an alert that fires once and pays for the whole exercise.

## Stage 1 - Name the failure you fear
Write it down with the signal that would reveal it. "Nightly job produces no rows" is revealed by a row count. "API is down" is revealed by a success-rate ratio, not a request count.

**Why now:** this determines what to instrument, and instrumenting everything is how teams end up with expensive telemetry and no answers.

## Stage 2 - Instrument the one thing
Emit one signal that would reveal your named failure, and look at it. That is the whole stage.

If you already run a metrics stack, add the metric. If you do not, choose by how much you want to operate:

- [[netdata]] — per-node metrics with automatic discovery and dashboards out of the box. The fastest path from nothing to seeing something, and the right answer for a handful of machines.
- [[prometheus]] — the pull-based standard, with a query language worth learning and an ecosystem that assumes it. The right answer when the estate will grow.
- [[statsd]] — a tiny daemon your application pushes counters and timers to. Minimal ceremony when your application already knows what it wants to report.

All three implement [[Pattern - Observability Pipeline]]; they differ in who initiates collection and how much they assume about your environment.

**Why now:** one signal you check beats a hundred you do not.

**Not yet:** no dashboards. A dashboard is a thing you have to remember to look at, which is the problem you started with.

## Stage 3 - Add alerting only for what you would act on
Now automate the noticing. The rule that keeps alerting useful: **alert only on what you would get out of bed for.** Everything else is a graph you consult when investigating, not a page.

Two or three alerts that always mean something beat forty that mostly do not. Alert fatigue is not a nuisance, it is the failure mode — a team that ignores its alerts is worse off than one with none, because it believes it is covered.

Errors and exceptions are a different signal from metrics, and [[getsentry - sentry]] handles the difference well: it groups occurrences of the same fault, keeps stack traces and context, and tells you whether a thing is new or long-standing. A metric tells you the error rate rose; this tells you what broke. **Check its licence terms before adopting** — see [[Workflow - Adopt A Dependency]], as this is one of the resources whose licence GitHub reports only as "Other".

**Exit criterion:** the failure you named in Stage 1 now reaches you without a human noticing first.

## Stage 4 - Add tracing when you cannot locate a fault
The trigger for tracing is specific: **you know something is slow or broken and cannot tell which component is responsible.** Until you have several services and that question is genuinely hard, tracing is instrumentation overhead paid for an answer you already have.

When you do reach it, expect to instrument request paths and propagate context — real work, and worth it exactly when the alternative is guessing.

**Not yet, if:** you have one service. The answer is always "it was that one".

## Stage 5 - Consolidate
Once several signals matter, the operational questions arrive: retention, cost, who is on call, what happens when the monitoring itself fails.

This is also where infrastructure-as-code earns its place — [[hashicorp - terraform]], [[chef]] and [[puppetlabs - puppet]] under [[Pattern - Infrastructure as Code]] — so the monitoring stack is reproducible rather than a hand-built machine nobody dares restart. Note that the monitoring of your monitoring cannot live inside it.

**Why now:** these are real problems only once the system is load-bearing. Solving them first produces an elaborate stack watching nothing important.

## Not Yet - The Steel Framing
- **A full metrics taxonomy and naming standard.** Right at fifty services, obstructive at two.
- **Log aggregation for everything.** Expensive and, before you know what you are looking for, mostly unread. Aggregate what an alert makes you go and read.
- **SLOs and error budgets.** Excellent once you have reliable signals and someone to negotiate targets with. Meaningless while instrumentation is a fortnight old.
- **A SIEM.** [[Topic - Security & SIEM]] is a different discipline with different questions. Detection and operations overlap in tooling, not in purpose.

## Exit Criteria
The failure you named in Stage 1 reaches you from your own system, before a user reports it, without anyone having remembered to look. Then name the next failure and repeat.

## Applies These Patterns
- [[Pattern - Observability Pipeline]]
- [[Pattern - Infrastructure as Code]]
- [[Pattern - Endpoint Instrumentation]]

## Related
- [[Topic - Infrastructure & Observability]]
- [[Workflow - Adopt A Dependency]]
