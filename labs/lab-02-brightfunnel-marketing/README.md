# Lab 2 — Create the BrightFunnel Company, Mission and CEO (Digital Marketing)

**Course:** Manage AI Agents with Paperclip (TGS-2023036646)  
**Version:** v1.0  
**Release date:** 28 August 2026  
**Topic 2:** Building AI Agents with Paperclip  
**Maps to:** LO2: Create a goal-aligned Paperclip company with a measurable mission, a hardened CEO agent and enforced company-level caps.  
**Tools:** Paperclip onboarding wizard, Agent Configuration, one approved adapter runtime, text editor  
**Simulated company:** BrightFunnel Marketing — Digital Marketing

**Suggested duration:** 60 minutes  
**Prerequisites:**
- Lab 1 complete: Paperclip is running, `doctor` is clean and `/api/health` reports ok.
- One trainer-approved agent runtime installed and already authenticated OUTSIDE Paperclip.
- The `paperclip-tgs` practice root retained, with its `workspace/` and `evidence/` folders.
- A text editor for writing the CEO role-contract instruction file.

---

## Goal

LO2: Create a goal-aligned Paperclip company with a measurable mission, a hardened CEO agent and enforced company-level caps.

## What You Will Do

You stand up BrightFunnel Marketing — a one-person digital marketing company — as a Paperclip company. You write a MEASURABLE mission (a target, a metric and a boundary), hire the Marketing Director as CEO, connect one trainer-approved agent runtime, and set the company budget cap BEFORE any agent is allowed to run. The order matters: a company that gains a runtime before it gains a cap can spend without a ceiling.

## What You Will Build

A BrightFunnel company in Paperclip with the exact synthetic mission, a hardened Marketing Director CEO on a verified adapter, a saved company budget cap, a dedicated workspace and a redacted configuration baseline in evidence/.

> **Data note.** Every figure, name and record in `data/` is SYNTHETIC and was fabricated for training. BrightFunnel Marketing is a simulated company; the data is not real business, market or personal data and must never be presented as such. Keep runtime credentials in the runtime or in Paperclip's secret store — never in prompts, lab notes or Git.

## Steps

**1. Open the Paperclip dashboard and start company creation. Use the exact synthetic company name so your evidence matches the marking guide.**

```text
http://localhost:3100   →   Companies → New Company
Name: BrightFunnel Marketing
```

**2. Enter the MEASURABLE mission from the mock brief. A mission needs a target, a metric and a boundary — 'grow the funnel' is not verifiable, this is.**

```text
Increase qualified inbound leads by 30% in one quarter
while keeping blended cost per qualified lead under SGD 45.
```

**3. Set the company-level budget cap BEFORE hiring. This is the outermost ring of the layered budget model and it must exist first.**

```text
Company → Settings → Budget
Monthly cap: SGD 40.00
```

**4. Hire the CEO. The Marketing Director owns goal alignment, decomposition and final synthesis for BrightFunnel.**

```text
Agents → Hire → Role: Marketing Director
Reports to: (none — top of org chart)
```

**5. Write the CEO instruction file. State PURPOSE, ALLOWED INPUTS, OUTPUT SCHEMA, EXCLUSIONS and ESCALATION — a role contract, not a personality.**

```text
workspace/marketing-director/INSTRUCTIONS.md
(copy the template from data/brightfunnel-ceo-instructions.md)
```

**6. Attach a dedicated workspace so the CEO's files and evidence stay confined to one root and every change is attributable.**

```text
Agent → Workspace → Path: ./workspace/marketing-director
```

**7. Select and verify the agent runtime adapter. Verification means Paperclip reports a successful connectivity check, not merely that a value was saved.**

```text
Agent → Runtime → (trainer-approved adapter)
Click Verify connection
```

**8. Set the CEO's individual agent budget BELOW the company cap so the inner ring always binds first.**

```text
Agent → Budget → Monthly cap: SGD 15.00
```

**9. Import the BrightFunnel mock lead and channel data so the company has realistic synthetic material to reason over.**

```text
cp -r labs/lab-02-brightfunnel-marketing/data ./workspace/marketing-director/data
```

**10. Record a redacted configuration baseline: company name, mission, CEO role, adapter NAME only, both budget caps and the workspace path. Never record keys.**

```text
evidence/lab02-brightfunnel-baseline.md
```

## Test It

BrightFunnel exists with the exact mission text; the Marketing Director is the sole top-level agent with a verified adapter, a confined workspace and an instruction file; the agent cap (SGD 15) is below the company cap (SGD 40); and the baseline note contains no key, token or connection string.

## Checkpoint

Keep BrightFunnel selected, the Marketing Director idle with no runs, both budget caps active and the workspace confined. Lab 3 repeats this pattern at three-agent scale and then proves each runtime boundary with a marker run.

## Troubleshooting

- **The adapter verification fails** — Confirm the underlying CLI runtime is installed and authenticated OUTSIDE Paperclip first, then re-verify. Paperclip cannot authenticate a runtime for you.
- **The mission field rejects the text** — Remove smart quotes and line breaks pasted from a word processor; enter the mission as plain text.
- **The budget cap will not save** — Set the company cap before the agent cap — an agent cap above a missing or smaller company cap is rejected.

## Challenge

Rewrite the BrightFunnel mission so it would FAIL a feasibility scan, then state in one sentence exactly which property (target, metric or boundary) you removed.

## Reflection

Why is setting the company budget cap before hiring the CEO a control decision rather than an administrative one?

---

[← Lab 1](../lab-01-clipreel-studio/README.md) · [Labs index](../README.md) · [Lab 3 →](../lab-03-meridian-finance/README.md)
