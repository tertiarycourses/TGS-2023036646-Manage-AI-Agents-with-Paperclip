# Lab 6 — Run the Governed TalentBridge Operation and Close the Audit Loop (HR)

**Course:** Manage AI Agents with Paperclip (TGS-2023036646)  
**Version:** v1.0  
**Release date:** 28 August 2026  
**Topic 4:** Deploying and Managing AI Agents  
**Maps to:** LO4: Resolve issues and modify a running agent company through approvals, the operator intervention ladder and a reconstructed audit trail.  
**Tools:** Paperclip Issues, Agents, Runs, Approvals, Activity, Costs and local Markdown artifacts  
**Simulated company:** TalentBridge People Ops — HR — sourcing, interviewing, policy and onboarding

**Suggested duration:** 90 minutes  
**Prerequisites:**
- Labs 4 and 5 complete: sequential children, bounded waits, and all three budget layers verified.
- Approvals reachable in your deployment (in a hosted instance the tool-action signing secret must be set).
- Git installed, with clean workspace baselines so the synthesis diff is readable.
- A willingness to terminate ONLY the disposable role you deliberately create in this lab.

---

## Goal

LO4: Resolve issues and modify a running agent company through approvals, the operator intervention ladder and a reconstructed audit trail.

## What You Will Do

TalentBridge People Ops is the highest-stakes simulation in the course: hiring decisions affect real people, so every control you have learned is now mandatory rather than advisable. You complete the sourcing-to-onboarding operation, review the final synthesis against a workspace DIFF before the board closes it, process a bounded hire approval with a recorded rationale, practise the intervention ladder on a disposable role only, and finally reconstruct the entire operation from the activity log. The audit loop closes when the log alone tells the whole story.

## What You Will Build

A diff-reviewed TalentBridge hiring brief, a separately confined reviewer with a recorded approval rationale, a lifecycle intervention record, and a mission-to-evidence audit map reconstructed from the activity log alone.

> **Data note.** Every figure, name and record in `data/` is SYNTHETIC and was fabricated for training. TalentBridge People Ops is a simulated company; the data is not real business, market or personal data and must never be presented as such. Keep runtime credentials in the runtime or in Paperclip's secret store — never in prompts, lab notes or Git.

## Steps

**1. Create the TalentBridge company with a People Operations Lead as CEO, a Talent Sourcer and a Policy & Onboarding Specialist, with layered caps.**

```text
Companies → New Company: TalentBridge People Ops
Mission: Fill each open role within 30 days with a fair, documented and auditable
process from sourcing through to day-one onboarding.
Company cap SGD 45 · CEO SGD 20 · each specialist SGD 10
```

**2. Load the synthetic candidate pipeline, the interview rubric and the onboarding checklist. Every candidate record is fabricated — never use real applicant data.**

```text
cp -r labs/lab-06-talentbridge-hr/data/hiring ./data/hiring
```

**3. Build the issue tree as in Lab 4: an unassigned parent plus two children, then run the two specialists sequentially and accept each on named evidence.**

```text
Parent (unassigned): Produce the Support Engineer hiring brief
  Child 1 → Shortlist candidates against the rubric  (Talent Sourcer)
  Child 2 → Draft policy-compliant onboarding plan   (Policy & Onboarding)
```

**4. Only after BOTH children are accepted, assign the parent so the CEO synthesises. Assigning the parent early is what produces a synthesis of incomplete work.**

```text
Parent → Assignee: People Operations Lead   ·   bound the wait to 10 minutes
```

**5. Review the final synthesis against the workspace DIFF, not against the agent's own summary. The diff is the strongest evidence you have.**

```text
git -C workspace/people-ops-lead diff HEAD --stat
git -C workspace/people-ops-lead diff HEAD -- hiring-brief.md
```

**6. Confirm fairness controls in the brief: every shortlisting reason must trace to the published rubric, and no protected characteristic may appear as a criterion.**

```text
grep -nEi 'age|gender|race|religion|marital|nationality' \
  workspace/people-ops-lead/hiring-brief.md   # expect: no criteria hits
```

**7. Close the parent only after board sign-off, recording WHO approved and on what evidence. A close without a rationale is an unaudited decision.**

```text
Issue → Comment: approved by <name> on diff <sha>, rubric-traceable
Issue → Status: Done
```

**8. Process a bounded HIRE APPROVAL: let the CEO propose one additional agent, then decide it yourself and record the rationale in the approval.**

```text
Approvals → (pending hire proposal)
Decide: Approve or Reject   ·   Rationale: <why, in one sentence>
```

**9. Confine the newly approved reviewer to its OWN workspace and its own budget before it ever runs — a new hire inherits nothing by default.**

```text
Agent → Workspace: ./workspace/interview-reviewer
Agent → Budget: SGD 5.00
```

**10. Practise the operator INTERVENTION LADDER on the disposable reviewer role only, in order: inspect → pause → reassign → terminate. Use the least irreversible control that resolves the situation.**

```text
Agent → Inspect runs and costs
Agent → Pause
Issue → Reassign to People Operations Lead
Agent → Terminate  (disposable role ONLY)
```

**11. Reconstruct the whole operation from the ACTIVITY LOG alone — company creation, hires, issues, runs, costs, the approval and the interventions, in order.**

```text
Activity → filter: TalentBridge People Ops → export or transcribe in order
```

**12. Write the mission-to-evidence audit map: one row per mission claim, linking the issue, the run, the artifact, the cost entry and the approval that evidences it.**

```text
evidence/lab06-talentbridge-audit-map.md
| Mission claim | Issue | Run | Artifact | Cost | Approval |
```

## Test It

The hiring brief is the only later People Ops Lead workspace change and its diff passes the rubric-traceability and fairness checks; the approval carries a recorded rationale; the intervention ladder was applied to the disposable role only and in order; and the audit map reconstructs every mission claim from activity-log entries with no gap.

## Checkpoint

Retain the three core agents, the final artifacts and the full evidence pack. Leave every interval trigger off and the routine paused so no practice company can continue spending after the course.

## Troubleshooting

- **The CEO synthesises incomplete work** — The parent was assigned before both children were accepted. Reopen the parent, accept the outstanding child on named evidence, then re-assign.
- **The approval cannot be decided** — Approvals do not expire on their own — an undecided approval simply waits, and any agent blocked on it waits too. Open Approvals and approve, reject or request revision.
- **Terminate removes more than intended** — Terminate is the LAST rung and is not reversible. Pause and reassign first; only terminate the role you deliberately created as disposable.
- **The activity log has a gap** — Work was done outside a run — for example hand-edited in the workspace. Note it honestly in the audit map; an unexplained gap is itself an audit finding.

## Challenge

Export the TalentBridge company, confirm the export scrubs secrets, then import it as a second company and record which identifiers Paperclip had to re-map on collision.

## Reflection

Your audit map is the deliverable a regulator would actually ask for. Which single row in it is the weakest, and what evidence would strengthen it?

---

[← Lab 5](../lab-05-northpoint-trading/README.md) · [Labs index](../README.md)
