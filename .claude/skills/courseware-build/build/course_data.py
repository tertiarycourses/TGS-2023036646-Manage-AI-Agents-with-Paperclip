"""
SINGLE SOURCE OF TRUTH — WSQ Manage AI Agents with Paperclip (TGS-2023036646).

Every artifact (PPT, LP, LG, LG.md, labs index, assessment) is generated from
this module plus data_domain1..4.py so they can never drift apart.

Course record (lms-tms.tertiaryinfotech.com, course b93f56ca-…):
    title            Manage AI Agents with Paperclip
    courseCode       TGS-2023036646
    tscTitle/Code    Applications Integration / ICT-DIT-3003-1.1
    trainingHours    14   assessmentHours 2   → 16 total, 2 days
    courseType       WSQ  modeOfLearning Physical
"""

# ------------------------------------------------------------------ metadata
TITLE        = "Manage AI Agents with Paperclip (TGS-2023036646)"
SHORT_TITLE  = "Manage AI Agents with Paperclip (TGS-2023036646)"
COURSE_CODE  = "TGS-2023036646"
VERSION      = "v1.0"
VERSION_DATE = "28 August 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr. Alfred Ang"
DAYS         = 2

TSC_TITLE    = "Applications Integration"
TSC_CODE     = "ICT-DIT-3003-1.1"

TRAINING_HOURS   = 14
ASSESSMENT_HOURS = 2

COURSE_URL = "https://www.tertiarycourses.com.sg/wsq-manage-ai-agents-with-paperclip.html"
REPO_URL   = "https://github.com/tertiarycourses/TGS-2023036646-Manage-AI-Agents-with-Paperclip"

# ------------------------------------------------------------------ outcomes
# Retargeted to Paperclip while preserving the assessed verb structure of the
# registered TSC (identify & scan feasibility · integrate & develop · test &
# verify between disparate components · resolve issues & modify).
LEARNING_OUTCOMES = [
    "LO1: Identify agentic AI opportunities and perform feasibility scans to determine "
    "when a Paperclip-managed multi-agent company is the appropriate solution.",
    "LO2: Utilise Paperclip to integrate agent runtimes, data and skills, and develop a "
    "goal-aligned AI agent company with an org chart, workspaces and budgets.",
    "LO3: Perform tests in Paperclip to verify that agents, issues, hand-offs and routines "
    "function correctly between disparate components.",
    "LO4: Resolve technical issues in Paperclip and implement modifications to the agent "
    "company, its governance controls and its cost boundaries.",
]

LO_SHORT = [
    ("LO1 · Identify & scan feasibility",
     "Explain the Paperclip control-plane model and judge when a managed multi-agent "
     "company earns its coordination cost."),
    ("LO2 · Integrate & develop",
     "Install Paperclip, create a goal-aligned company, build the reporting tree and "
     "connect agent runtimes, skills and workspaces safely."),
    ("LO3 · Test & verify",
     "Decompose a mission into issues, run bounded heartbeats and verify hand-offs "
     "through runs, comments, artifacts and the activity log."),
    ("LO4 · Resolve & modify",
     "Diagnose adapter, budget and routine failures, and modify governance, approvals "
     "and cost boundaries to keep the operation safe."),
]

# ------------------------------------------------------------------ topics
TOPICS = [
    dict(num=1, code="01",
         title="Fundamentals of Agentic AI and Paperclip",
         subtitle="Agentic AI foundations · the control-plane model · the twelve subsystems · "
                  "feasibility and when NOT to use multi-agent",
         weighting="25%",
         concepts=[
            "Agentic AI adds reasoning, tool use, memory and autonomy on top of a language "
            "model, so the system completes work rather than only producing text.",
            "Paperclip is an organisational control plane — a Node.js server with a React UI "
            "that coordinates agents, goals, work, cost and governance. It is not an agent "
            "framework and it does not perform the reasoning itself.",
            "The defining separation: Paperclip manages the company; adapters run the agents. "
            "Organisational authority, runtime capability and verification evidence stay apart.",
            "A company is the boundary for one mission, its human members, AI employees, "
            "projects, issues, budget and activity history. One deployment holds many companies.",
            "The four pillars are the agentic task manager, the org chart for agents, agent "
            "employee training (skills and evaluations) and the agentic OS (runtime, sandboxing, "
            "MCP, RBAC and cost control).",
            "Twelve subsystems make up the platform: identity, org chart, work, heartbeat, "
            "workspaces, governance, budget, routines, plugins, secrets, activity and portability.",
            "A heartbeat is a bounded execution burst triggered by a timer, an assignment, an "
            "on-demand wake or a routine. Between heartbeats the agent is dormant, not idling.",
            "Work is checked out atomically with an execution lock, so two heartbeats can never "
            "double-work the same issue or race past a budget ceiling.",
            "'If it can receive a heartbeat, it's hired' — adapters exist for Claude Code, Codex, "
            "Cursor, Gemini CLI, bash processes and HTTP/webhook bots.",
            "Feasibility comes before architecture: use one agent when the inputs, tools, "
            "authority and verification are the same across the whole task.",
            "Add a specialist only when different expertise is genuinely required, or when "
            "evidence must be produced independently of the agent that will use it.",
            "Installation is ready only when Node.js, the Paperclip configuration, the embedded "
            "database, server health, the browser UI and the doctor diagnostic all agree.",
         ]),
    dict(num=2, code="02",
         title="Building AI Agents with Paperclip",
         subtitle="Install and verify · company and mission · the CEO · org chart · runtime "
                  "adapters · workspaces, instructions and secrets",
         weighting="25%",
         concepts=[
            "Onboarding with `paperclipai onboard --yes` downloads Paperclip, writes the "
            "configuration, initialises the embedded PostgreSQL and serves the UI on port 3100.",
            "Bind mode is a security decision: the default trusted loopback is the least exposed; "
            "`--bind lan` and `--bind tailnet` widen reach and require authentication.",
            "The onboarding wizard captures the company name, the mission statement and the team "
            "lead, then verifies connectivity to your chosen local agent runtime.",
            "A mission must be measurable. 'Grow the channel' cannot be verified; 'publish 8 "
            "short videos per month at ≥5% average watch-through' can.",
            "The CEO is the first hire and the top of the org chart — it owns goal alignment, "
            "decomposition and final synthesis, and it may hire further agents under approval.",
            "Every agent carries a role, a manager, an adapter, an instruction file, a heartbeat "
            "and an individual budget. Those six fields are the agent's whole contract.",
            "A role instruction states purpose, allowed inputs, the output schema, explicit "
            "exclusions and the escalation path — not a personality.",
            "Each agent gets a dedicated workspace: a separate local root for one role's files "
            "and evidence, isolated with git worktrees so changes are attributable.",
            "Secrets live in the runtime or in Paperclip's secret store with scoped injection at "
            "heartbeat time. They never appear in prompts, lab notes or Git.",
            "Skills are reusable agent capabilities imported from a path or URL into an org-wide "
            "library, then attached to specific agents — capability without retraining.",
            "Adapter readiness is proved by a marker run, not by the presence of configuration: "
            "an agent that cannot produce an observable artifact is not connected.",
            "Diagnose along a ladder — host, control plane, adapter, agent — and fix the earliest "
            "broken link before changing anything downstream.",
         ]),
    dict(num=3, code="03",
         title="Developing Intelligent Multi-Agent Systems",
         subtitle="Projects, goals and lineage · issue decomposition · assignment and hand-off · "
                  "sequential specialists · verifying between disparate components",
         weighting="25%",
         concepts=[
            "Projects hold goals and issues and supply the context an agent reads at runtime, so "
            "tasks carry full goal ancestry — the agent sees why, not only what.",
            "Goal lineage flows downward: company mission → project goal → parent issue → child "
            "issue. An agent that cannot trace its lineage is working without direction.",
            "Decompose into a parent synthesis issue plus specialist child issues. Create every "
            "issue unassigned first, so creation cannot accidentally wake an agent.",
            "Assignment is the trigger. Assign one child at a time to keep runs sequential, "
            "observable and individually attributable.",
            "An acceptance criterion must name the evidence: which artifact, at which path, "
            "containing which fields — never 'the research is done'.",
            "A hand-off is accepted only when the receiving agent can consume the artifact "
            "without asking the producer a question.",
            "Verification between disparate components means tracing one thread across issue ID, "
            "run log, comment, workspace diff and cost entry, and finding them consistent.",
            "Status is not evidence. An issue marked Done with no linked artifact and no diff is "
            "an unverified claim.",
            "Explicit limitations are part of a good deliverable — an agent that reports what it "
            "could not establish is more useful than one that quietly guesses.",
            "One event should not create many outcomes: choose a single trigger for the first "
            "controlled run and keep the work idempotent.",
            "Bound every wait. An unbounded wait for a heartbeat hides a failed adapter behind "
            "what looks like patience.",
            "The workspace diff is the strongest evidence you have — read what actually changed "
            "on disk before accepting any agent's summary of it.",
         ]),
    dict(num=4, code="04",
         title="Deploying and Managing AI Agents",
         subtitle="Routines and schedules · layered budgets · approvals and audit · operator "
                  "intervention · deployment, portability and troubleshooting",
         weighting="25%",
         concepts=[
            "A routine is recurring work triggered by cron, webhook or API. Create it paused, "
            "prove it once by hand, and only then let the schedule own it.",
            "A schedule trigger is explicit — `30 16 * * *` with an IANA timezone such as "
            "Asia/Singapore. An implicit timezone is a production incident waiting to happen.",
            "Budgets are layered: company, project, agent. Enforcement happens at checkout, so a "
            "runaway loop stops at the ceiling instead of after you read the invoice.",
            "Treat the budget as a two-stage circuit breaker — warn, then stop — and record the "
            "baseline spend and expected run frequency before you rely on it.",
            "Cost is tracked at token level by provider, model, agent and project, which is what "
            "makes the per-agent cap meaningful rather than notional.",
            "Approvals are the board's authority made explicit: the agent proposes a hire, a "
            "strategy or a risky action, and a human decides with a recorded rationale.",
            "The activity log is a durable record of mutations, heartbeats, cost events and "
            "approvals — the audit loop closes when the whole operation reconstructs from it.",
            "Use the least irreversible control first: inspect, then pause, then reassign, then "
            "terminate. Retirement is the last rung of the ladder, not the first.",
            "Deployment options run from local loopback through LAN or tailnet binding to a "
            "hosted container with an external PostgreSQL and a persistent volume.",
            "A production deployment needs the signing secret for tool approvals, the allowed "
            "hostnames list and a health check on /api/health.",
            "Portability means an entire company exports and imports with secrets scrubbed and "
            "collisions handled — the org chart is data, not a hand-built configuration.",
            "Troubleshooting is a discipline: reproduce, isolate the layer, change one setting, "
            "re-verify with evidence, and record what the fix actually proved.",
         ]),
]

# ------------------------------------------------------------------ day themes
DAY_THEMES = {
    1: "Agentic AI foundations, the Paperclip control plane, and building your first "
       "goal-aligned AI agent company",
    2: "Multi-agent operations: decomposition, hand-offs, routines, budgets, approvals "
       "and the closed audit loop",
}

# ------------------------------------------------------------------ the six simulated companies
# One per lab. Each lab folder ships its own mock data set.
COMPANIES = [
    dict(lab=1, code="CLIPREEL", name="ClipReel Studio",
         sector="Short Video Production",
         mission="Publish 8 short-form videos per month across TikTok, Reels and Shorts at an "
                 "average watch-through rate of at least 5%.",
         ceo="Head of Content",
         roles=["Head of Content", "Trend Researcher", "Script Writer"],
         currency="SGD"),
    dict(lab=2, code="BRIGHTFN", name="BrightFunnel Marketing",
         sector="Digital Marketing",
         mission="Increase qualified inbound leads by 30% in one quarter while keeping blended "
                 "cost per qualified lead under SGD 45.",
         ceo="Marketing Director",
         roles=["Marketing Director", "SEO Analyst", "Campaign Copywriter"],
         currency="SGD"),
    dict(lab=3, code="MERIDIAN", name="Meridian Finance Desk",
         sector="Finance",
         mission="Produce a board-ready monthly financial pack within 3 working days of month "
                 "end, with every figure traceable to a source ledger extract.",
         ceo="Finance Lead",
         roles=["Finance Lead", "FP&A Analyst", "Treasury Analyst"],
         currency="SGD"),
    dict(lab=4, code="LEDGERLY", name="Ledgerly Accounting",
         sector="Accounting",
         mission="Close the books each month with zero unexplained variances above SGD 500 and a "
                 "complete reconciliation trail for every control account.",
         ceo="Practice Manager",
         roles=["Practice Manager", "Reconciliation Specialist", "Compliance Reviewer"],
         currency="SGD"),
    dict(lab=5, code="NORTHPT", name="NorthPoint Trading Research",
         sector="Stock Trading (research only)",
         mission="Deliver a daily pre-market research brief on a fixed synthetic watchlist by "
                 "07:30 SGT, with every claim sourced and every limitation stated.",
         ceo="Research Director",
         roles=["Research Director", "Market Data Analyst", "Risk Reviewer"],
         currency="SGD"),
    dict(lab=6, code="TALENTB", name="TalentBridge People Ops",
         sector="HR — sourcing, interviewing, policy and onboarding",
         mission="Fill each open role within 30 days with a fair, documented and auditable "
                 "process from sourcing through to day-one onboarding.",
         ceo="People Operations Lead",
         roles=["People Operations Lead", "Talent Sourcer", "Policy & Onboarding Specialist"],
         currency="SGD"),
]

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 5 questions, 1 hour, open book.",
    practical="Practical Performance (PP) — 4 hands-on Paperclip tasks, 1 hour, open book.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)

# Knowledge codes (WA) and Ability codes (PP) — every K must appear in the WA and
# every A in the PP. Counts are fixed to the registered paper: 5 SAQ, 4 PP tasks.
KNOWLEDGE = [
    ("K1", "Agentic AI and the Paperclip control-plane model — what Paperclip is, "
           "what it is not, and the control-plane / runtime separation."),
    ("K2", "Feasibility of a multi-agent company — when coordination earns its cost and "
           "when a single agent is the correct choice."),
    ("K3", "The company, mission, CEO, org chart, adapter and workspace model used to "
           "integrate and develop an agent company."),
    ("K4", "Issues, goal lineage, assignment, heartbeats and hand-off acceptance used to "
           "verify behaviour between disparate components."),
    ("K5", "Routines, layered budgets, approvals, the activity log and the operator "
           "intervention ladder used to resolve issues and modify the operation."),
]

ABILITY = [
    ("A1", "Install and verify a Paperclip control plane and record observable evidence "
           "of a healthy instance."),
    ("A2", "Create a goal-aligned company with a measurable mission, a CEO and a budgeted "
           "reporting tree with confined workspaces."),
    ("A3", "Decompose a mission into a parent and specialist child issues, run them "
           "sequentially and verify each hand-off against acceptance evidence."),
    ("A4", "Apply a paused routine, layered budget caps and an approval gate, then "
           "reconstruct the operation from the activity log."),
]

RECOMMENDED_COURSES = [
    "WSQ - Develop Multi AI Agent Applications with Gemini Agent ADK",
    "WSQ - Build LLM Applications Using Flowise and LangChain",
    "WSQ - Generative AI for Productivity",
    "WSQ - Prompt Engineering for Business",
]
