"""Topic 2 — Building AI Agents with Paperclip. Labs 2 (BrightFunnel) and 3 (Meridian)."""

DOMAIN2 = [
    dict(
        num=2,
        topic=2,
        title="Create the BrightFunnel Company, Mission and CEO (Digital Marketing)",
        objective="LO2: Create a goal-aligned Paperclip company with a measurable mission, a "
                  "hardened CEO agent and enforced company-level caps.",
        desc=(
            "You stand up BrightFunnel Marketing — a one-person digital marketing company — as a "
            "Paperclip company. You write a MEASURABLE mission (a target, a metric and a "
            "boundary), hire the Marketing Director as CEO, connect one trainer-approved agent "
            "runtime, and set the company budget cap BEFORE any agent is allowed to run. The "
            "order matters: a company that gains a runtime before it gains a cap can spend "
            "without a ceiling."
        ),
        build="A BrightFunnel company in Paperclip with the exact synthetic mission, a hardened "
              "Marketing Director CEO on a verified adapter, a saved company budget cap, a "
              "dedicated workspace and a redacted configuration baseline in evidence/.",
        services="Paperclip onboarding wizard, Agent Configuration, one approved adapter runtime, "
                 "text editor",
        company="BrightFunnel Marketing (Digital Marketing)",
        flow=[
            ("Create the company", "the exact measurable mission"),
            ("Set the company cap", "the outermost ring, before hiring"),
            ("Hire the CEO", "Marketing Director owns alignment"),
            ("Write the role contract", "purpose, inputs, schema, exclusions"),
            ("Confine + verify runtime", "own workspace, then agent cap"),
        ],
        steps=[
            ("Open the Paperclip dashboard and start company creation. Use the exact synthetic "
             "company name so your evidence matches the marking guide.",
             "http://localhost:3100   →   Companies → New Company\nName: BrightFunnel Marketing"),
            ("Enter the MEASURABLE mission from the mock brief. A mission needs a target, a "
             "metric and a boundary — 'grow the funnel' is not verifiable, this is.",
             "Increase qualified inbound leads by 30% in one quarter\n"
             "while keeping blended cost per qualified lead under SGD 45."),
            ("Set the company-level budget cap BEFORE hiring. This is the outermost ring of "
             "the layered budget model and it must exist first.",
             "Company → Settings → Budget\nMonthly cap: SGD 40.00"),
            ("Hire the CEO. The Marketing Director owns goal alignment, decomposition and "
             "final synthesis for BrightFunnel.",
             "Agents → Hire → Role: Marketing Director\nReports to: (none — top of org chart)"),
            ("Write the CEO instruction file. State PURPOSE, ALLOWED INPUTS, OUTPUT SCHEMA, "
             "EXCLUSIONS and ESCALATION — a role contract, not a personality.",
             "workspace/marketing-director/INSTRUCTIONS.md\n"
             "(copy the template from data/brightfunnel-ceo-instructions.md)"),
            ("Attach a dedicated workspace so the CEO's files and evidence stay confined to "
             "one root and every change is attributable.",
             "Agent → Workspace → Path: ./workspace/marketing-director"),
            ("Select and verify the agent runtime adapter. Verification means Paperclip "
             "reports a successful connectivity check, not merely that a value was saved.",
             "Agent → Runtime → (trainer-approved adapter)\nClick Verify connection"),
            ("Set the CEO's individual agent budget BELOW the company cap so the inner ring "
             "always binds first.",
             "Agent → Budget → Monthly cap: SGD 15.00"),
            ("Import the BrightFunnel mock lead and channel data so the company has realistic "
             "synthetic material to reason over.",
             "cp -r labs/lab-02-brightfunnel-marketing/data ./workspace/marketing-director/data"),
            ("Record a redacted configuration baseline: company name, mission, CEO role, "
             "adapter NAME only, both budget caps and the workspace path. Never record keys.",
             "evidence/lab02-brightfunnel-baseline.md"),
        ],
        test="BrightFunnel exists with the exact mission text; the Marketing Director is the "
             "sole top-level agent with a verified adapter, a confined workspace and an "
             "instruction file; the agent cap (SGD 15) is below the company cap (SGD 40); and "
             "the baseline note contains no key, token or connection string.",
        troubleshoot=[
            ("The adapter verification fails",
             "Confirm the underlying CLI runtime is installed and authenticated OUTSIDE "
             "Paperclip first, then re-verify. Paperclip cannot authenticate a runtime for you."),
            ("The mission field rejects the text",
             "Remove smart quotes and line breaks pasted from a word processor; enter the "
             "mission as plain text."),
            ("The budget cap will not save",
             "Set the company cap before the agent cap — an agent cap above a missing or "
             "smaller company cap is rejected."),
        ],
        challenge="Rewrite the BrightFunnel mission so it would FAIL a feasibility scan, then "
                  "state in one sentence exactly which property (target, metric or boundary) "
                  "you removed.",
        reflection="Why is setting the company budget cap before hiring the CEO a control "
                   "decision rather than an administrative one?",
    ),
    dict(
        num=3,
        topic=2,
        title="Build the Meridian Reporting Tree and Validate Runtime Boundaries (Finance)",
        objective="LO2: Build a multi-agent reporting hierarchy with distinct, budgeted and "
                  "confined workspaces, and prove each runtime boundary with a marker run.",
        desc=(
            "You extend the pattern into Meridian Finance Desk and build a real three-agent org "
            "chart: a Finance Lead with an FP&A Analyst and a Treasury Analyst reporting to it. "
            "Each specialist receives its OWN workspace, its OWN instruction file and its OWN "
            "budget. You then prove every runtime boundary with a marker run — a deliberately "
            "trivial task whose only purpose is to produce an observable artifact in the correct "
            "workspace. Configuration that has never produced an artifact is not a connection."
        ),
        build="A three-agent Meridian org chart with separate budgeted workspaces, role "
              "instruction files, clean Git baselines and one marker-run artifact per agent "
              "proving its runtime boundary.",
        services="Paperclip Agents, Org and Runs pages; approved adapter runtime; Git; "
                 "Markdown editor",
        company="Meridian Finance Desk (Finance)",
        flow=[
            ("Create Meridian", "company mission and cap"),
            ("Hire the tree", "two analysts report to the lead"),
            ("Split the workspaces", "one root per role"),
            ("Git baseline each root", "so the diff means something"),
            ("Marker run per agent", "prove the runtime boundary"),
        ],
        steps=[
            ("Create the Meridian company with its measurable mission and a company budget cap, "
             "using the same order you proved in Lab 2.",
             "Companies → New Company\nName: Meridian Finance Desk\n"
             "Mission: Produce a board-ready monthly financial pack within 3 working days of\n"
             "month end, with every figure traceable to a source ledger extract.\n"
             "Company monthly cap: SGD 45.00"),
            ("Hire the Finance Lead as CEO, then hire the two specialists AND set the reporting "
             "line explicitly. A flat list of agents is not an org chart.",
             "Agents → Hire\n  Finance Lead      (reports to: none)\n"
             "  FP&A Analyst      (reports to: Finance Lead)\n"
             "  Treasury Analyst  (reports to: Finance Lead)"),
            ("Create one workspace root per agent. Separate roots are what make a later diff "
             "attributable to exactly one role.",
             "mkdir -p workspace/{finance-lead,fpa-analyst,treasury-analyst}"),
            ("Initialise Git in each workspace and commit an empty baseline, so every later "
             "change is a readable diff against a known-clean state.",
             "for w in finance-lead fpa-analyst treasury-analyst; do \\\n"
             "  git -C workspace/$w init -q && \\\n"
             "  git -C workspace/$w commit -q --allow-empty -m 'baseline'; done"),
            ("Write a role instruction file for each specialist stating purpose, allowed inputs, "
             "output schema, exclusions and escalation. The exclusions matter most.",
             "workspace/fpa-analyst/INSTRUCTIONS.md\n"
             "workspace/treasury-analyst/INSTRUCTIONS.md\n"
             "(templates in data/ledger/meridian-role-instructions/)"),
            ("Load the Meridian mock ledger extracts into a shared read-only data folder so both "
             "specialists reason over identical source figures.",
             "cp -r labs/lab-03-meridian-finance/data/ledger ./data/ledger"),
            ("Bind each agent to its own workspace path and its own adapter, then set an "
             "individual budget for each so the caps are layered company → agent.",
             "Each agent → Workspace + Runtime + Budget\n"
             "  Finance Lead     SGD 20.00\n  FP&A Analyst     SGD 10.00\n"
             "  Treasury Analyst SGD 10.00"),
            ("Run a MARKER RUN for each agent: assign a trivial task whose only output is a "
             "single named file. This is how you prove the runtime boundary is real.",
             "Issues → New\nTitle: Marker run — <agent>\n"
             "Body: Create a file named marker.md in your workspace root containing only\n"
             "      your agent role name and the current date. Do nothing else."),
            ("Inspect each run and confirm the artifact landed in the CORRECT workspace — and "
             "nowhere else. A marker in the wrong root is a boundary failure, not a success.",
             "git -C workspace/fpa-analyst status --short\n"
             "git -C workspace/treasury-analyst status --short\n"
             "git -C workspace/finance-lead status --short"),
            ("Record the org chart, the three budgets, the three marker-run IDs and the three "
             "artifact paths in your evidence note.",
             "evidence/lab03-meridian-org.md"),
        ],
        test="`paperclip → Org` shows a three-agent tree with both analysts reporting to the "
             "Finance Lead; each workspace contains exactly ONE marker.md attributable to its "
             "own agent; every agent has an individual cap and the sum of agent caps does not "
             "exceed the company cap; and each marker run has a recorded run ID.",
        troubleshoot=[
            ("A marker file appears in the wrong workspace",
             "The agent's workspace path is misbound. Correct the path on the AGENT (not the "
             "company), delete the stray file, and re-run the marker."),
            ("A specialist never wakes",
             "Confirm the issue is ASSIGNED to that agent — creating an issue does not wake "
             "anyone. Then check the agent's adapter verification and its budget headroom."),
            ("Git reports the workspace is dirty before the marker run",
             "Something was written outside a run. Reset to the baseline commit and re-run so "
             "the diff means what you think it means."),
        ],
        challenge="Set the Treasury Analyst's cap to SGD 0.01, re-run its marker task, and "
                  "record exactly where and how Paperclip reports the budget stop.",
        reflection="Why is a marker run stronger evidence of a working runtime than a green "
                   "'connection verified' badge in the configuration screen?",
    ),
]
