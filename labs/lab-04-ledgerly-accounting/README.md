# Lab 4 — Translate the Ledgerly Mission into Assigned Issues and Hand-Offs (Accounting)

**Course:** Manage AI Agents with Paperclip (TGS-2023036646)  
**Version:** v1.0  
**Release date:** 28 August 2026  
**Topic 3:** Developing Intelligent Multi-Agent Systems  
**Maps to:** LO3: Decompose a mission into a parent and specialist child issues, run the specialists sequentially and verify each hand-off against acceptance evidence.  
**Tools:** Paperclip Projects, Budgets, Issues, Agents and Runs; approved adapter runtime; Git; Markdown workspaces  
**Simulated company:** Ledgerly Accounting — Accounting

**Suggested duration:** 90 minutes  
**Prerequisites:**
- Labs 2 and 3 complete: you can create a company, hire a tree and set layered caps unaided.
- The marker-run technique from Lab 3 proved for every adapter you intend to use.
- Git installed and each workspace committed to a clean baseline.
- At least 30 minutes of uninterrupted time — the two specialist runs must be SEQUENTIAL.

---

## Goal

LO3: Decompose a mission into a parent and specialist child issues, run the specialists sequentially and verify each hand-off against acceptance evidence.

## What You Will Do

You turn the Ledgerly Accounting mission into actual work. You create a budgeted month-end close project, then a PARENT synthesis issue and two specialist CHILD issues — all created UNASSIGNED, so that creating work cannot accidentally wake an agent. Only after every acceptance criterion names its evidence do you assign one child at a time. This is the core discipline of the topic: assignment is the trigger, and sequential assignment is what makes each run individually verifiable.

## What You Will Build

A capped Ledgerly close project with an unassigned parent issue, two sequentially completed specialist children, clean workspace manifests, and an evidence record linking issue IDs, run IDs, comments, statuses and artifact paths.

> **Data note.** Every figure, name and record in `data/` is SYNTHETIC and was fabricated for training. Ledgerly Accounting is a simulated company; the data is not real business, market or personal data and must never be presented as such. Keep runtime credentials in the runtime or in Paperclip's secret store — never in prompts, lab notes or Git.

## Steps

**1. Create the Ledgerly company, hire the Practice Manager as CEO plus a Reconciliation Specialist and a Compliance Reviewer, and set layered caps — the pattern you proved in Labs 2 and 3.**

```text
Companies → New Company: Ledgerly Accounting
Mission: Close the books each month with zero unexplained variances above SGD 500
and a complete reconciliation trail for every control account.
Company cap SGD 45 · CEO SGD 20 · each specialist SGD 10
```

**2. Create the project and give it its OWN budget cap. The project ring sits between the company and the agent, and it is what stops one project consuming the company.**

```text
Projects → New
Name: October Month-End Close
Goal: Close October with every control account reconciled and evidenced.
Project cap: SGD 25.00
```

**3. Load the Ledgerly mock trial balance and bank statement extracts into a shared read-only data folder.**

```text
cp -r labs/lab-04-ledgerly-accounting/data/close ./data/close
```

**4. Create the PARENT synthesis issue UNASSIGNED. Its acceptance criterion names the artifact, its path and the fields it must contain.**

```text
Issues → New  (Assignee: leave EMPTY)
Title: Produce the October close pack
Accept: workspace/practice-manager/close-pack.md exists and contains, for every
control account: account, ledger balance, statement balance, variance, explanation.
```

**5. Create the two CHILD issues, both unassigned, each parented to the synthesis issue so goal lineage is explicit and traceable.**

```text
Child 1 → Reconcile control accounts   (parent: Produce the October close pack)
Child 2 → Review compliance exceptions (parent: Produce the October close pack)
```

**6. Write an acceptance criterion for each child that names the EVIDENCE, not the activity. 'Reconciliation done' is unverifiable; a named file with named fields is.**

```text
Child 1 accept: workspace/reconciliation-specialist/reconciliation.md lists every
  control account with ledger balance, statement balance and variance.
Child 2 accept: workspace/compliance-reviewer/exceptions.md lists each variance
  above SGD 500 with a stated cause and a recommended treatment.
```

**7. Assign CHILD 1 ONLY. Assignment is the trigger — this is the moment the Reconciliation Specialist wakes.**

```text
Child 1 → Assignee: Reconciliation Specialist
```

**8. Wait for the heartbeat with a BOUND. Inspect the run log rather than the issue status — an unbounded wait hides a failed adapter behind apparent patience.**

```text
Runs → (latest)   ·   bound the wait to 10 minutes
git -C workspace/reconciliation-specialist status --short
```

**9. Accept child 1 ONLY if the named artifact exists with the named fields. Record the run ID and the artifact path in a comment on the issue, then close it.**

```text
Issue → Comment: run <run-id> produced reconciliation.md (<n> accounts)
Issue → Status: Done
```

**10. Now assign CHILD 2. Running the specialists sequentially is what keeps each run individually attributable and each hand-off inspectable.**

```text
Child 2 → Assignee: Compliance Reviewer
```

**11. Verify the HAND-OFF: confirm the Compliance Reviewer consumed child 1's artifact without needing to ask the producer a question.**

```text
grep -c 'SGD' workspace/compliance-reviewer/exceptions.md
git -C workspace/compliance-reviewer diff --stat HEAD
```

**12. Record the evidence chain — for each child: issue ID, run ID, artifact path, comment and final status — in one table.**

```text
evidence/lab04-ledgerly-handoffs.md
```

## Test It

The Ledgerly project shows a saved cap above actual spend; the parent issue is still open and unassigned; both children are Done with a linked artifact and a recorded run ID; the two specialists ran SEQUENTIALLY (non-overlapping run timestamps); and the exceptions file demonstrably references the reconciliation figures.

## Checkpoint

Keep both child artifacts, their comments and their Done statuses intact, and leave the parent issue OPEN and UNASSIGNED. Lab 5 adds a paused routine and re-verifies every budget layer; the parent is synthesised in Lab 6.

## Troubleshooting

- **Both specialists wake at the same time** — A child was assigned before the previous one was accepted. Pause the second agent, let the first run settle, then re-assign so the runs are sequential.
- **The child artifact exists but is missing fields** — The acceptance criterion was written as an activity, not as evidence. Rewrite it naming the required fields and re-run — do not hand-edit the agent's artifact.
- **The parent issue wakes unexpectedly** — It was assigned during creation. Clear the assignee; the parent stays unassigned until both children are accepted (that is Lab 6).

## Challenge

Add a third child issue whose acceptance criterion deliberately names an artifact the previous child never produces, and record precisely how the failure surfaces in the run log.

## Reflection

Why does creating every issue unassigned change the risk profile of a multi-agent company, compared with assigning at creation time?

---

[← Lab 3](../lab-03-meridian-finance/README.md) · [Labs index](../README.md) · [Lab 5 →](../lab-05-northpoint-trading/README.md)
