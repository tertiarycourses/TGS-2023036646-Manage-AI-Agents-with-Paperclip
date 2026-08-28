# Lab 3 — Build the Meridian Reporting Tree and Validate Runtime Boundaries (Finance)

**Course:** Manage AI Agents with Paperclip (TGS-2023036646)  
**Version:** v1.0  
**Release date:** 28 August 2026  
**Topic 2:** Building AI Agents with Paperclip  
**Maps to:** LO2: Build a multi-agent reporting hierarchy with distinct, budgeted and confined workspaces, and prove each runtime boundary with a marker run.  
**Tools:** Paperclip Agents, Org and Runs pages; approved adapter runtime; Git; Markdown editor  
**Simulated company:** Meridian Finance Desk — Finance

**Suggested duration:** 75 minutes  
**Prerequisites:**
- Lab 2 complete: BrightFunnel exists with a verified CEO adapter and layered caps saved.
- Git installed, with a local practice `user.name` and `user.email` configured so each workspace can commit a baseline without contacting a remote.
- Absolute paths available for the three Meridian workspace roots.
- The same trainer-approved adapter may be reused for all three agents.

---

## Goal

LO2: Build a multi-agent reporting hierarchy with distinct, budgeted and confined workspaces, and prove each runtime boundary with a marker run.

## What You Will Do

You extend the pattern into Meridian Finance Desk and build a real three-agent org chart: a Finance Lead with an FP&A Analyst and a Treasury Analyst reporting to it. Each specialist receives its OWN workspace, its OWN instruction file and its OWN budget. You then prove every runtime boundary with a marker run — a deliberately trivial task whose only purpose is to produce an observable artifact in the correct workspace. Configuration that has never produced an artifact is not a connection.

## What You Will Build

A three-agent Meridian org chart with separate budgeted workspaces, role instruction files, clean Git baselines and one marker-run artifact per agent proving its runtime boundary.

> **Data note.** Every figure, name and record in `data/` is SYNTHETIC and was fabricated for training. Meridian Finance Desk is a simulated company; the data is not real business, market or personal data and must never be presented as such. Keep runtime credentials in the runtime or in Paperclip's secret store — never in prompts, lab notes or Git.

## Steps

**1. Create the Meridian company with its measurable mission and a company budget cap, using the same order you proved in Lab 2.**

```text
Companies → New Company
Name: Meridian Finance Desk
Mission: Produce a board-ready monthly financial pack within 3 working days of
month end, with every figure traceable to a source ledger extract.
Company monthly cap: SGD 45.00
```

**2. Hire the Finance Lead as CEO, then hire the two specialists AND set the reporting line explicitly. A flat list of agents is not an org chart.**

```text
Agents → Hire
  Finance Lead      (reports to: none)
  FP&A Analyst      (reports to: Finance Lead)
  Treasury Analyst  (reports to: Finance Lead)
```

**3. Create one workspace root per agent. Separate roots are what make a later diff attributable to exactly one role.**

```text
mkdir -p workspace/{finance-lead,fpa-analyst,treasury-analyst}
```

**4. Initialise Git in each workspace and commit an empty baseline, so every later change is a readable diff against a known-clean state.**

```text
for w in finance-lead fpa-analyst treasury-analyst; do \
  git -C workspace/$w init -q && \
  git -C workspace/$w commit -q --allow-empty -m 'baseline'; done
```

**5. Write a role instruction file for each specialist stating purpose, allowed inputs, output schema, exclusions and escalation. The exclusions matter most.**

```text
workspace/fpa-analyst/INSTRUCTIONS.md
workspace/treasury-analyst/INSTRUCTIONS.md
(templates in data/ledger/meridian-role-instructions/)
```

**6. Load the Meridian mock ledger extracts into a shared read-only data folder so both specialists reason over identical source figures.**

```text
cp -r labs/lab-03-meridian-finance/data/ledger ./data/ledger
```

**7. Bind each agent to its own workspace path and its own adapter, then set an individual budget for each so the caps are layered company → agent.**

```text
Each agent → Workspace + Runtime + Budget
  Finance Lead     SGD 20.00
  FP&A Analyst     SGD 10.00
  Treasury Analyst SGD 10.00
```

**8. Run a MARKER RUN for each agent: assign a trivial task whose only output is a single named file. This is how you prove the runtime boundary is real.**

```text
Issues → New
Title: Marker run — <agent>
Body: Create a file named marker.md in your workspace root containing only
      your agent role name and the current date. Do nothing else.
```

**9. Inspect each run and confirm the artifact landed in the CORRECT workspace — and nowhere else. A marker in the wrong root is a boundary failure, not a success.**

```text
git -C workspace/fpa-analyst status --short
git -C workspace/treasury-analyst status --short
git -C workspace/finance-lead status --short
```

**10. Record the org chart, the three budgets, the three marker-run IDs and the three artifact paths in your evidence note.**

```text
evidence/lab03-meridian-org.md
```

## Test It

`paperclip → Org` shows a three-agent tree with both analysts reporting to the Finance Lead; each workspace contains exactly ONE marker.md attributable to its own agent; every agent has an individual cap and the sum of agent caps does not exceed the company cap; and each marker run has a recorded run ID.

## Checkpoint

Keep the three-agent Meridian tree, the clean Git baselines and all three agent caps. Leave every interval trigger off. Lab 4 adds the project budget ring before any specialist is assigned real work.

## Troubleshooting

- **A marker file appears in the wrong workspace** — The agent's workspace path is misbound. Correct the path on the AGENT (not the company), delete the stray file, and re-run the marker.
- **A specialist never wakes** — Confirm the issue is ASSIGNED to that agent — creating an issue does not wake anyone. Then check the agent's adapter verification and its budget headroom.
- **Git reports the workspace is dirty before the marker run** — Something was written outside a run. Reset to the baseline commit and re-run so the diff means what you think it means.

## Challenge

Set the Treasury Analyst's cap to SGD 0.01, re-run its marker task, and record exactly where and how Paperclip reports the budget stop.

## Reflection

Why is a marker run stronger evidence of a working runtime than a green 'connection verified' badge in the configuration screen?

---

[← Lab 2](../lab-02-brightfunnel-marketing/README.md) · [Labs index](../README.md) · [Lab 4 →](../lab-04-ledgerly-accounting/README.md)
