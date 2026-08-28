# Lab 5 — Verify NorthPoint Routines and Layered Budget Controls (Stock Trading Research)

**Course:** Manage AI Agents with Paperclip (TGS-2023036646)  
**Version:** v1.0  
**Release date:** 28 August 2026  
**Topic 3:** Developing Intelligent Multi-Agent Systems  
**Maps to:** LO3: Test a scheduled routine and verify that every budget layer holds, using one bounded manual run before automation is allowed to own the schedule.  
**Tools:** Paperclip Routines, Costs and Budgets, Agent Budget tabs, Project settings, Activity  
**Simulated company:** NorthPoint Trading Research — Stock Trading (research only)

**Suggested duration:** 75 minutes  
**Prerequisites:**
- Lab 4 complete: you have run a specialist to a named artifact and accepted it on evidence.
- The host clock and timezone are correct; you can state the machine's IANA timezone.
- Permission to create a routine but NOT to leave it live after class.
- An understanding that this is research only — the company never places or recommends a trade.

---

## Goal

LO3: Test a scheduled routine and verify that every budget layer holds, using one bounded manual run before automation is allowed to own the schedule.

## What You Will Do

NorthPoint Trading Research needs a daily pre-market brief — which makes it the right place to learn routines. You create the readiness routine PAUSED, add an explicit cron trigger with an IANA timezone, prove the routine once by hand, and leave it paused afterwards. You then verify all three budget layers against actual recorded spend. The rule the lab teaches: automation earns the schedule only after a human has watched it succeed once. This is research only — the company never places or recommends a trade.

## What You Will Build

A paused NorthPoint readiness routine with a saved 07:00 Asia/Singapore trigger, exactly one reviewed manual run, and a control table proving company, project and agent budget layers all remain above recorded spend.

> **Data note.** Every figure, name and record in `data/` is SYNTHETIC and was fabricated for training. NorthPoint Trading Research is a simulated company; the data is not real business, market or personal data and must never be presented as such. Keep runtime credentials in the runtime or in Paperclip's secret store — never in prompts, lab notes or Git.

## Steps

**1. Create the NorthPoint company with a Research Director CEO, a Market Data Analyst and a Risk Reviewer, with layered caps. Note the research-only boundary in the mission — the company must never recommend a trade.**

```text
Companies → New Company: NorthPoint Trading Research
Mission: Deliver a daily pre-market research brief on a fixed synthetic watchlist
by 07:30 SGT, with every claim sourced and every limitation stated.
Company cap SGD 40 · CEO SGD 15 · each analyst SGD 10
```

**2. Load the synthetic watchlist and price history. This data is fabricated for training and must never be presented as market data.**

```text
cp -r labs/lab-05-northpoint-trading/data/market ./data/market
```

**3. Create the routine and set it PAUSED at creation. A routine that is live before it has ever succeeded is an unreviewed scheduled spend.**

```text
Routines → New
Name: Daily pre-market readiness check
State: PAUSED
```

**4. Add the schedule trigger EXPLICITLY, with the cron expression and the IANA timezone. An implicit timezone is a production incident waiting to happen.**

```text
Trigger → Schedule
Cron: 0 7 * * *
Timezone: Asia/Singapore
```

**5. Write what the routine actually does, naming the artifact it must produce so the run is verifiable rather than merely successful.**

```text
Body: Produce workspace/market-data-analyst/premarket-brief.md summarising each
watchlist symbol from ./data/market ONLY. State sources and limitations.
Do not recommend any trade.
```

**6. Run the routine ONCE manually while it is still paused, and bound the wait. This is the human review that earns the schedule.**

```text
Routine → Run now   ·   bound the wait to 10 minutes
```

**7. Inspect the generated issue and the run — confirm the routine created work correctly and that the named artifact exists.**

```text
Issues → (routine-generated issue)
Runs → (latest)
cat workspace/market-data-analyst/premarket-brief.md | head -30
```

**8. Read the recorded COST for that run. This actual figure is what you will compare every budget layer against.**

```text
Costs → filter by agent: Market Data Analyst
Record the run cost
```

**9. Confirm the routine is STILL paused after the manual run. Leaving it live is the most common mistake in this lab.**

```text
Routines → Daily pre-market readiness check → State: PAUSED
```

**10. Verify every budget layer against actual spend and record the three-row control table: company, project and agent — each cap, each spend, each headroom.**

```text
evidence/lab05-northpoint-budgets.md
| Layer | Cap | Spend | Headroom |
```

**11. Confirm the audit trail: the activity log must show the routine creation, the trigger addition, the manual run and the cost event as separate entries.**

```text
Activity → filter: NorthPoint Trading Research
```

## Test It

The routine carries an explicit `0 7 * * *` Asia/Singapore trigger, has exactly ONE successful reviewed manual run, and finishes PAUSED; the brief exists and cites only the synthetic data with limitations stated and no trade recommendation; and the control table shows all three budget layers above recorded spend.

## Checkpoint

Leave the routine PAUSED and retain every budget policy and the recorded control table. Lab 6 uses this same controlled environment to complete a synthesis, process an approval and practise operator intervention.

## Troubleshooting

- **The routine fires unexpectedly** — It was left active after the manual run. Pause it, then check the activity log for any additional runs and record them — do not delete the evidence.
- **The cost shows as zero** — The run may have failed before invoking the runtime. Read the run log for an adapter error rather than assuming the work was free.
- **The timezone reverts or the schedule fires an hour out** — The trigger was saved without an explicit IANA timezone and inherited the host's. Re-save the trigger with Asia/Singapore stated explicitly.

## Challenge

Lower the Market Data Analyst cap below the recorded run cost, run the routine once more, and record exactly which layer stops the run and where it is reported.

## Reflection

Why must a routine be proved by one bounded manual run before the schedule is allowed to own it?

---

[← Lab 4](../lab-04-ledgerly-accounting/README.md) · [Labs index](../README.md) · [Lab 6 →](../lab-06-talentbridge-hr/README.md)
