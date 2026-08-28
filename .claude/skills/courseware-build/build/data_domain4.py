"""Topic 4 — Deploying and Managing AI Agents. Lab 6: TalentBridge People Ops."""

DOMAIN4 = [
    dict(
        num=6,
        topic=4,
        title="Run the Governed TalentBridge Operation and Close the Audit Loop (HR)",
        objective="LO4: Resolve issues and modify a running agent company through approvals, the "
                  "operator intervention ladder and a reconstructed audit trail.",
        desc=(
            "TalentBridge People Ops is the highest-stakes simulation in the course: hiring "
            "decisions affect real people, so every control you have learned is now mandatory "
            "rather than advisable. You complete the sourcing-to-onboarding operation, review "
            "the final synthesis against a workspace DIFF before the board closes it, process a "
            "bounded hire approval with a recorded rationale, practise the intervention ladder on "
            "a disposable role only, and finally reconstruct the entire operation from the "
            "activity log. The audit loop closes when the log alone tells the whole story."
        ),
        build="A diff-reviewed TalentBridge hiring brief, a separately confined reviewer with a "
              "recorded approval rationale, a lifecycle intervention record, and a "
              "mission-to-evidence audit map reconstructed from the activity log alone.",
        services="Paperclip Issues, Agents, Runs, Approvals, Activity, Costs and local Markdown "
                 "artifacts",
        company="TalentBridge People Ops (HR — sourcing, interview, policy, onboarding)",
        flow=[
            ("Create TalentBridge", "synthetic candidates only"),
            ("Run the issue tree", "children accepted before the parent"),
            ("Review the workspace diff", "not the agent's own summary"),
            ("Decide the approval", "record the rationale"),
            ("Close the audit loop", "reconstruct from Activity alone"),
        ],
        steps=[
            ("Create the TalentBridge company with a People Operations Lead as CEO, a Talent "
             "Sourcer and a Policy & Onboarding Specialist, with layered caps.",
             "Companies → New Company: TalentBridge People Ops\n"
             "Mission: Fill each open role within 30 days with a fair, documented and auditable\n"
             "process from sourcing through to day-one onboarding.\n"
             "Company cap SGD 45 · CEO SGD 20 · each specialist SGD 10"),
            ("Load the synthetic candidate pipeline, the interview rubric and the onboarding "
             "checklist. Every candidate record is fabricated — never use real applicant data.",
             "cp -r labs/lab-06-talentbridge-hr/data/hiring ./data/hiring"),
            ("Build the issue tree as in Lab 4: an unassigned parent plus two children, then run "
             "the two specialists sequentially and accept each on named evidence.",
             "Parent (unassigned): Produce the Support Engineer hiring brief\n"
             "  Child 1 → Shortlist candidates against the rubric  (Talent Sourcer)\n"
             "  Child 2 → Draft policy-compliant onboarding plan   (Policy & Onboarding)"),
            ("Only after BOTH children are accepted, assign the parent so the CEO synthesises. "
             "Assigning the parent early is what produces a synthesis of incomplete work.",
             "Parent → Assignee: People Operations Lead   ·   bound the wait to 10 minutes"),
            ("Review the final synthesis against the workspace DIFF, not against the agent's own "
             "summary. The diff is the strongest evidence you have.",
             "git -C workspace/people-ops-lead diff HEAD --stat\n"
             "git -C workspace/people-ops-lead diff HEAD -- hiring-brief.md"),
            ("Confirm fairness controls in the brief: every shortlisting reason must trace to the "
             "published rubric, and no protected characteristic may appear as a criterion.",
             "grep -nEi 'age|gender|race|religion|marital|nationality' \\\n"
             "  workspace/people-ops-lead/hiring-brief.md   # expect: no criteria hits"),
            ("Close the parent only after board sign-off, recording WHO approved and on what "
             "evidence. A close without a rationale is an unaudited decision.",
             "Issue → Comment: approved by <name> on diff <sha>, rubric-traceable\n"
             "Issue → Status: Done"),
            ("Process a bounded HIRE APPROVAL: let the CEO propose one additional agent, then "
             "decide it yourself and record the rationale in the approval.",
             "Approvals → (pending hire proposal)\n"
             "Decide: Approve or Reject   ·   Rationale: <why, in one sentence>"),
            ("Confine the newly approved reviewer to its OWN workspace and its own budget before "
             "it ever runs — a new hire inherits nothing by default.",
             "Agent → Workspace: ./workspace/interview-reviewer\nAgent → Budget: SGD 5.00"),
            ("Practise the operator INTERVENTION LADDER on the disposable reviewer role only, in "
             "order: inspect → pause → reassign → terminate. Use the least irreversible control "
             "that resolves the situation.",
             "Agent → Inspect runs and costs\nAgent → Pause\n"
             "Issue → Reassign to People Operations Lead\nAgent → Terminate  (disposable role ONLY)"),
            ("Reconstruct the whole operation from the ACTIVITY LOG alone — company creation, "
             "hires, issues, runs, costs, the approval and the interventions, in order.",
             "Activity → filter: TalentBridge People Ops → export or transcribe in order"),
            ("Write the mission-to-evidence audit map: one row per mission claim, linking the "
             "issue, the run, the artifact, the cost entry and the approval that evidences it.",
             "evidence/lab06-talentbridge-audit-map.md\n"
             "| Mission claim | Issue | Run | Artifact | Cost | Approval |"),
        ],
        test="The hiring brief is the only later People Ops Lead workspace change and its diff "
             "passes the rubric-traceability and fairness checks; the approval carries a recorded "
             "rationale; the intervention ladder was applied to the disposable role only and in "
             "order; and the audit map reconstructs every mission claim from activity-log entries "
             "with no gap.",
        troubleshoot=[
            ("The CEO synthesises incomplete work",
             "The parent was assigned before both children were accepted. Reopen the parent, "
             "accept the outstanding child on named evidence, then re-assign."),
            ("The approval cannot be decided",
             "Approvals do not expire on their own — an undecided approval simply waits, and "
             "any agent blocked on it waits too. Open Approvals and approve, reject or "
             "request revision."),
            ("Terminate removes more than intended",
             "Terminate is the LAST rung and is not reversible. Pause and reassign first; only "
             "terminate the role you deliberately created as disposable."),
            ("The activity log has a gap",
             "Work was done outside a run — for example hand-edited in the workspace. Note it "
             "honestly in the audit map; an unexplained gap is itself an audit finding."),
        ],
        challenge="Export the TalentBridge company, confirm the export scrubs secrets, then import "
                  "it as a second company and record which identifiers Paperclip had to "
                  "re-map on collision.",
        reflection="Your audit map is the deliverable a regulator would actually ask for. Which "
                   "single row in it is the weakest, and what evidence would strengthen it?",
    ),
]
