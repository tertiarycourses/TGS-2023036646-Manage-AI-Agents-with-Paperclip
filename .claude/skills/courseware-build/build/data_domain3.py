"""Topic 3 — Developing Intelligent Multi-Agent Systems. Labs 4 (Ledgerly) and 5 (NorthPoint)."""

DOMAIN3 = [
    dict(
        num=4,
        topic=3,
        title="Translate the Ledgerly Mission into Assigned Issues and Hand-Offs (Accounting)",
        objective="LO3: Decompose a mission into a parent and specialist child issues, run the "
                  "specialists sequentially and verify each hand-off against acceptance evidence.",
        desc=(
            "You turn the Ledgerly Accounting mission into actual work. You create a budgeted "
            "month-end close project, then a PARENT synthesis issue and two specialist CHILD "
            "issues — all created UNASSIGNED, so that creating work cannot accidentally wake an "
            "agent. Only after every acceptance criterion names its evidence do you assign one "
            "child at a time. This is the core discipline of the topic: assignment is the "
            "trigger, and sequential assignment is what makes each run individually verifiable."
        ),
        build="A capped Ledgerly close project with an unassigned parent issue, two sequentially "
              "completed specialist children, clean workspace manifests, and an evidence record "
              "linking issue IDs, run IDs, comments, statuses and artifact paths.",
        services="Paperclip Projects, Budgets, Issues, Agents and Runs; approved adapter runtime; "
                 "Git; Markdown workspaces",
        company="Ledgerly Accounting (Accounting)",
        flow=[
            ("Create the close project", "its own budget cap"),
            ("Parent issue, unassigned", "creation must not wake anyone"),
            ("Two child issues", "acceptance names the evidence"),
            ("Assign child 1 only", "assignment is the trigger"),
            ("Accept, then assign child 2", "sequential and attributable"),
        ],
        steps=[
            ("Create the Ledgerly company, hire the Practice Manager as CEO plus a "
             "Reconciliation Specialist and a Compliance Reviewer, and set layered caps — the "
             "pattern you proved in Labs 2 and 3.",
             "Companies → New Company: Ledgerly Accounting\n"
             "Mission: Close the books each month with zero unexplained variances above SGD 500\n"
             "and a complete reconciliation trail for every control account.\n"
             "Company cap SGD 45 · CEO SGD 20 · each specialist SGD 10"),
            ("Create the project and give it its OWN budget cap. The project ring sits between "
             "the company and the agent, and it is what stops one project consuming the company.",
             "Projects → New\nName: October Month-End Close\n"
             "Goal: Close October with every control account reconciled and evidenced.\n"
             "Project cap: SGD 25.00"),
            ("Load the Ledgerly mock trial balance and bank statement extracts into a shared "
             "read-only data folder.",
             "cp -r labs/lab-04-ledgerly-accounting/data/close ./data/close"),
            ("Create the PARENT synthesis issue UNASSIGNED. Its acceptance criterion names the "
             "artifact, its path and the fields it must contain.",
             "Issues → New  (Assignee: leave EMPTY)\n"
             "Title: Produce the October close pack\n"
             "Accept: workspace/practice-manager/close-pack.md exists and contains, for every\n"
             "control account: account, ledger balance, statement balance, variance, explanation."),
            ("Create the two CHILD issues, both unassigned, each parented to the synthesis "
             "issue so goal lineage is explicit and traceable.",
             "Child 1 → Reconcile control accounts   (parent: Produce the October close pack)\n"
             "Child 2 → Review compliance exceptions (parent: Produce the October close pack)"),
            ("Write an acceptance criterion for each child that names the EVIDENCE, not the "
             "activity. 'Reconciliation done' is unverifiable; a named file with named fields is.",
             "Child 1 accept: workspace/reconciliation-specialist/reconciliation.md lists every\n"
             "  control account with ledger balance, statement balance and variance.\n"
             "Child 2 accept: workspace/compliance-reviewer/exceptions.md lists each variance\n"
             "  above SGD 500 with a stated cause and a recommended treatment."),
            ("Assign CHILD 1 ONLY. Assignment is the trigger — this is the moment the "
             "Reconciliation Specialist wakes.",
             "Child 1 → Assignee: Reconciliation Specialist"),
            ("Wait for the heartbeat with a BOUND. Inspect the run log rather than the issue "
             "status — an unbounded wait hides a failed adapter behind apparent patience.",
             "Runs → (latest)   ·   bound the wait to 10 minutes\n"
             "git -C workspace/reconciliation-specialist status --short"),
            ("Accept child 1 ONLY if the named artifact exists with the named fields. Record "
             "the run ID and the artifact path in a comment on the issue, then close it.",
             "Issue → Comment: run <run-id> produced reconciliation.md (<n> accounts)\n"
             "Issue → Status: Done"),
            ("Now assign CHILD 2. Running the specialists sequentially is what keeps each run "
             "individually attributable and each hand-off inspectable.",
             "Child 2 → Assignee: Compliance Reviewer"),
            ("Verify the HAND-OFF: confirm the Compliance Reviewer consumed child 1's artifact "
             "without needing to ask the producer a question.",
             "grep -c 'SGD' workspace/compliance-reviewer/exceptions.md\n"
             "git -C workspace/compliance-reviewer diff --stat HEAD"),
            ("Record the evidence chain — for each child: issue ID, run ID, artifact path, "
             "comment and final status — in one table.",
             "evidence/lab04-ledgerly-handoffs.md"),
        ],
        test="The Ledgerly project shows a saved cap above actual spend; the parent issue is "
             "still open and unassigned; both children are Done with a linked artifact and a "
             "recorded run ID; the two specialists ran SEQUENTIALLY (non-overlapping run "
             "timestamps); and the exceptions file demonstrably references the reconciliation "
             "figures.",
        troubleshoot=[
            ("Both specialists wake at the same time",
             "A child was assigned before the previous one was accepted. Pause the second agent, "
             "let the first run settle, then re-assign so the runs are sequential."),
            ("The child artifact exists but is missing fields",
             "The acceptance criterion was written as an activity, not as evidence. Rewrite it "
             "naming the required fields and re-run — do not hand-edit the agent's artifact."),
            ("The parent issue wakes unexpectedly",
             "It was assigned during creation. Clear the assignee; the parent stays unassigned "
             "until both children are accepted (that is Lab 6)."),
        ],
        challenge="Add a third child issue whose acceptance criterion deliberately names an "
                  "artifact the previous child never produces, and record precisely how the "
                  "failure surfaces in the run log.",
        reflection="Why does creating every issue unassigned change the risk profile of a "
                   "multi-agent company, compared with assigning at creation time?",
    ),
    dict(
        num=5,
        topic=3,
        title="Verify NorthPoint Routines and Layered Budget Controls (Stock Trading Research)",
        objective="LO3: Test a scheduled routine and verify that every budget layer holds, using "
                  "one bounded manual run before automation is allowed to own the schedule.",
        desc=(
            "NorthPoint Trading Research needs a daily pre-market brief — which makes it the "
            "right place to learn routines. You create the readiness routine PAUSED, add an "
            "explicit cron trigger with an IANA timezone, prove the routine once by hand, and "
            "leave it paused afterwards. You then verify all three budget layers against actual "
            "recorded spend. The rule the lab teaches: automation earns the schedule only after "
            "a human has watched it succeed once. This is research only — the company never "
            "places or recommends a trade."
        ),
        build="A paused NorthPoint readiness routine with a saved 07:00 Asia/Singapore trigger, "
              "exactly one reviewed manual run, and a control table proving company, project and "
              "agent budget layers all remain above recorded spend.",
        services="Paperclip Routines, Costs and Budgets, Agent Budget tabs, Project settings, "
                 "Activity",
        company="NorthPoint Trading Research (Stock Trading — research only)",
        flow=[
            ("Create NorthPoint", "research only — never a trade"),
            ("Create the routine PAUSED", "unproven automation stays off"),
            ("Add the cron trigger", "0 7 * * * with Asia/Singapore"),
            ("Run once, bounded", "the human review earns the schedule"),
            ("Check every budget layer", "company, project and agent"),
        ],
        steps=[
            ("Create the NorthPoint company with a Research Director CEO, a Market Data Analyst "
             "and a Risk Reviewer, with layered caps. Note the research-only boundary in the "
             "mission — the company must never recommend a trade.",
             "Companies → New Company: NorthPoint Trading Research\n"
             "Mission: Deliver a daily pre-market research brief on a fixed synthetic watchlist\n"
             "by 07:30 SGT, with every claim sourced and every limitation stated.\n"
             "Company cap SGD 40 · CEO SGD 15 · each analyst SGD 10"),
            ("Load the synthetic watchlist and price history. This data is fabricated for "
             "training and must never be presented as market data.",
             "cp -r labs/lab-05-northpoint-trading/data/market ./data/market"),
            ("Create the routine and set it PAUSED at creation. A routine that is live before it "
             "has ever succeeded is an unreviewed scheduled spend.",
             "Routines → New\nName: Daily pre-market readiness check\nState: PAUSED"),
            ("Add the schedule trigger EXPLICITLY, with the cron expression and the IANA "
             "timezone. An implicit timezone is a production incident waiting to happen.",
             "Trigger → Schedule\nCron: 0 7 * * *\nTimezone: Asia/Singapore"),
            ("Write what the routine actually does, naming the artifact it must produce so the "
             "run is verifiable rather than merely successful.",
             "Body: Produce workspace/market-data-analyst/premarket-brief.md summarising each\n"
             "watchlist symbol from ./data/market ONLY. State sources and limitations.\n"
             "Do not recommend any trade."),
            ("Run the routine ONCE manually while it is still paused, and bound the wait. This "
             "is the human review that earns the schedule.",
             "Routine → Run now   ·   bound the wait to 10 minutes"),
            ("Inspect the generated issue and the run — confirm the routine created work "
             "correctly and that the named artifact exists.",
             "Issues → (routine-generated issue)\nRuns → (latest)\n"
             "cat workspace/market-data-analyst/premarket-brief.md | head -30"),
            ("Read the recorded COST for that run. This actual figure is what you will compare "
             "every budget layer against.",
             "Costs → filter by agent: Market Data Analyst\nRecord the run cost"),
            ("Confirm the routine is STILL paused after the manual run. Leaving it live is the "
             "most common mistake in this lab.",
             "Routines → Daily pre-market readiness check → State: PAUSED"),
            ("Verify every budget layer against actual spend and record the three-row control "
             "table: company, project and agent — each cap, each spend, each headroom.",
             "evidence/lab05-northpoint-budgets.md\n"
             "| Layer | Cap | Spend | Headroom |"),
            ("Confirm the audit trail: the activity log must show the routine creation, the "
             "trigger addition, the manual run and the cost event as separate entries.",
             "Activity → filter: NorthPoint Trading Research"),
        ],
        test="The routine carries an explicit `0 7 * * *` Asia/Singapore trigger, has exactly ONE "
             "successful reviewed manual run, and finishes PAUSED; the brief exists and cites only "
             "the synthetic data with limitations stated and no trade recommendation; and the "
             "control table shows all three budget layers above recorded spend.",
        troubleshoot=[
            ("The routine fires unexpectedly",
             "It was left active after the manual run. Pause it, then check the activity log for "
             "any additional runs and record them — do not delete the evidence."),
            ("The cost shows as zero",
             "The run may have failed before invoking the runtime. Read the run log for an "
             "adapter error rather than assuming the work was free."),
            ("The timezone reverts or the schedule fires an hour out",
             "The trigger was saved without an explicit IANA timezone and inherited the host's. "
             "Re-save the trigger with Asia/Singapore stated explicitly."),
        ],
        challenge="Lower the Market Data Analyst cap below the recorded run cost, run the routine "
                  "once more, and record exactly which layer stops the run and where it is "
                  "reported.",
        reflection="Why must a routine be proved by one bounded manual run before the schedule is "
                   "allowed to own it?",
    ),
]
