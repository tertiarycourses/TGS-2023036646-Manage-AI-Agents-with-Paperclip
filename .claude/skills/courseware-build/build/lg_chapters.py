"""
Learner Guide reference chapters — Manage AI Agents with Paperclip (TGS-2023036646).

Every technical assertion here is taken from the official documentation at
https://docs.paperclip.ing/ (harvested 28 August 2026). Where the docs give an
exact value — a default, a threshold, a state name, a type key, an error string —
that exact value is used. Nothing here is invented.

The module exposes CHAPTERS: an ordered list of blocks in the LG builder's own DSL:
    ("h1", text) ("h2", text) ("h3", text) ("p", text)
    ("bullets", [str, ...])
    ("code", text)
    ("note", text)
    ("table", (caption, [headers], [[row], ...]))
    ("rule",)
    ("check", [str, ...])        # self-check questions
"""

# ══════════════════════════════════════════════════════════════════ Part A
PART_A = [
 ("h1", "Part A — Foundations: Agentic AI and the Paperclip Control Plane"),

 ("h2", "A1. From a language model to an agent"),
 ("p", "A large language model, on its own, answers. Give it a prompt and it returns text. "
       "It has no memory of yesterday, cannot act on the world, and cannot tell you whether "
       "the thing it just asserted is true. That is not a criticism — it is the shape of the "
       "tool. The moment you want the model to DO something rather than SAY something, you "
       "have to add machinery around it."),
 ("p", "An agent is that machinery. It is a language model plus four additions, and it is "
       "worth being precise about each, because the whole of this course is about what "
       "happens when you have several of them at once."),
 ("table", ("The four additions that turn a model into an agent",
   ["Addition", "What it provides", "What breaks without it"],
   [["Reasoning / planning", "The model decomposes a goal into steps before acting, and "
     "re-plans when a step fails.", "The system answers in one shot and cannot recover from "
     "a wrong first move."],
    ["Tool use", "The model calls functions, CLIs and APIs to read live data and take real "
     "action.", "The system can only talk about the work; it cannot do it."],
    ["Memory / state", "Context carries across turns and — in Paperclip — across separate "
     "execution windows.", "Every wake-up starts from nothing and repeats work already done."],
    ["Autonomy", "The system decides which tool, which order, and when it is finished.",
     "A human has to drive every step, which is just a chatbot with extra latency."]])),
 ("p", "Add a fifth ingredient — several agents that divide the work — and you have a "
       "multi-agent system. That is where the interesting failures start, and it is where a "
       "control plane earns its place."),

 ("h2", "A2. Why coordination is the hard part"),
 ("p", "Running one agent is a prompting problem. Running five is an organisational problem, "
       "and the difficulties are not the ones people expect. They are rarely about model "
       "quality. They are about the things any organisation has to solve:"),
 ("bullets", [
   "DIRECTION — each agent needs to know not only what to do but why, or it optimises the "
   "wrong thing very efficiently.",
   "AUTHORITY — who may hire, who may spend, who may ship. Left implicit, it defaults to "
   "'whatever the agent decided to try'.",
   "ISOLATION — two agents writing to the same place at the same time corrupts both pieces "
   "of work and destroys your ability to attribute either.",
   "COST — an agent in a retry loop does not get tired. Without a hard ceiling you discover "
   "the problem on the invoice.",
   "EVIDENCE — 'the agent says it is done' is not the same as 'it is done'. Someone has to "
   "be able to check, later, without taking anyone's word for it.",
 ]),
 ("note", "These five are exactly the concerns Paperclip's twelve subsystems address. When "
          "you meet a subsystem later in this guide, map it back to the concern it solves — "
          "that is the fastest way to remember the architecture."),

 ("h2", "A3. What Paperclip is"),
 ("p", "Paperclip is an open-source control plane for AI agents: a Node.js server with a "
       "React user interface, backed by PostgreSQL, that gives a team of agents an "
       "organisational structure. The documentation's own definitions are worth learning "
       "verbatim, because the assessment uses this vocabulary:"),
 ("table", ("Core vocabulary, as defined by the official documentation",
   ["Term", "Official definition"],
   [["Company", "\"A self-contained AI organisation with a single goal, a team of agents, a "
     "task board, and a budget.\""],
    ["Agent", "\"An AI employee — a configured role with a specific job, a manager, and a "
     "monthly budget.\""],
    ["Task (issue)", "\"A unit of work — like a ticket on a project board, except it's "
     "assigned to an AI agent, not a human.\""],
    ["Heartbeat", "\"A scheduled execution window — the moment when an agent wakes up, "
     "checks its inbox, and does work.\""],
    ["Adapter", "\"The connection between Paperclip and the AI system that actually runs "
     "your agent.\""],
    ["Budget", "\"A monthly spending cap — a dollar limit that Paperclip enforces "
     "automatically so your agents never overspend.\""],
    ["Approval", "\"A governance gate — a checkpoint where Paperclip pauses and asks you to "
     "sign off before an important action proceeds.\""]])),
 ("p", "Notice what is absent from that list: nothing about prompting, nothing about model "
       "selection, nothing about how an agent reasons. That is deliberate."),

 ("h2", "A4. The boundary that matters most"),
 ("p", "If you remember one sentence from this course, make it this one:"),
 ("note", "Paperclip manages the company. Adapters run the agents."),
 ("p", "Paperclip does not perform the reasoning. It never sees a token of your model's "
       "thinking except as a cost figure and a run log. The actual work is done by a "
       "RUNTIME — Claude Code, Codex, Gemini CLI, Cursor, a bash process, an HTTP endpoint — "
       "reached through an adapter. The project's own phrasing is \"if it can receive a "
       "heartbeat, it's hired.\""),
 ("p", "This boundary has a practical consequence you will meet in Lab 1. A healthy Paperclip "
       "API proves the CONTROL PLANE is up. It proves nothing whatsoever about whether any "
       "agent runtime is ready, because the runtime is a separate process that must be "
       "installed and authenticated OUTSIDE Paperclip. The only thing that proves a runtime "
       "is a marker run that puts a real artifact in the right workspace."),
 ("p", "It also tells you what Paperclip is NOT, which saves a great deal of wasted "
       "evaluation time:"),
 ("bullets", [
   "NOT an agent framework — it does not dictate how your agent reasons, prompts or calls tools.",
   "NOT a chatbot — there is no conversational surface for you to talk to a model through.",
   "NOT a workflow builder — there is no drag-and-drop canvas of nodes and edges.",
   "NOT a prompt manager — prompts live with the runtime and the skill, not in a prompt library.",
   "NOT for a single agent — one agent does not need an org chart, and the coordination "
   "overhead would be pure cost.",
 ]),

 ("h2", "A5. The twelve subsystems"),
 ("p", "The platform is conventionally described as twelve subsystems. You do not need to "
       "recite them, but you should be able to say which one owns a given problem, because "
       "that is how you know where to look when something misbehaves."),
 ("table", ("The twelve subsystems and the question each answers",
   ["Subsystem", "The question it answers"],
   [["Identity", "Who is this — human or agent — and are they who they claim to be?"],
    ["Org chart", "Who reports to whom, and what is each role allowed to do?"],
    ["Work", "What needs doing, who owns it right now, and what state is it in?"],
    ["Heartbeat", "When does an agent wake, and what does it do when it does?"],
    ["Workspaces", "Where does this agent's work physically live, and who else can touch it?"],
    ["Governance", "Which actions require a human decision before they take effect?"],
    ["Budget", "What is the ceiling, and what happens when we reach it?"],
    ["Routines", "What recurring work should happen without anyone asking?"],
    ["Plugins", "How do we extend the platform without forking it?"],
    ["Secrets", "Where do credentials live, and how do they reach a run without leaking?"],
    ["Activity", "What actually happened, in order, durably?"],
    ["Portability", "How do we move a whole company somewhere else?"]])),

 ("h2", "A6. Feasibility — when a multi-agent company earns its cost"),
 ("p", "This is the most commercially useful judgement in the course, and the one learners "
       "most often get wrong in the assessment. The instinct is to reach for a team. The "
       "correct instinct is to reach for ONE agent and be argued out of it."),
 ("p", "The test is a single question: are the INPUTS, TOOLS, AUTHORITY and VERIFICATION the "
       "same across the whole task? If yes, use one agent. Splitting adds nothing but "
       "surface area."),
 ("table", ("The feasibility scan",
   ["Factor", "Points to ONE agent", "Points to a TEAM"],
   [["Separability", "One instruction still describes the job clearly.",
     "The instruction has become a list of unrelated responsibilities."],
    ["Expertise", "One skill set covers it.",
     "Genuinely different expertise is required for different parts."],
    ["Independent evidence", "The doer can reasonably check their own work.",
     "Evidence must be produced INDEPENDENTLY of whoever will consume it."],
    ["Observability", "Inputs and outputs are already observable.",
     "Same — this is a prerequisite either way, not a reason to split."],
    ["Cost of coordination", "Low volume, short task.",
     "The work recurs often enough to amortise the setup."]])),
 ("note", "Complexity you do not need is still complexity you must debug, budget and audit. "
          "Every additional agent is another workspace, another instruction file, another "
          "budget line and another audit trail — forever."),
 ("p", "A useful sanity check before you build anything: write the mission as one sentence. "
       "If you cannot, you do not yet understand the work well enough to delegate it — to an "
       "agent or to a person."),

 ("check", [
   "In your own words, state the boundary between the Paperclip control plane and an agent runtime.",
   "Give three reasons a healthy /api/health response does not prove an agent will run.",
   "Name the four additions that turn a language model into an agent.",
   "A colleague wants five agents for a task with one input file and one output report. "
   "What single question decides whether they are right?",
   "Which subsystem owns each of: a runaway spend, a lost credential, an unattributable file change?",
 ]),
 ("rule",),
]

# ══════════════════════════════════════════════════════════════════ Part B
PART_B = [
 ("h1", "Part B — Building the Company: Installation, Org Chart and Runtimes"),

 ("h2", "B1. Installing the control plane"),
 ("p", "Paperclip requires Node.js 20 or later. This is the single most common cause of a "
       "failed onboarding, so check it first and record the output — you will want it in your "
       "evidence note when something later goes wrong."),
 ("code", "node --version          # must print v20.x.x or higher\n"
          "npm install -g corepack\n"
          "corepack enable\n"
          "corepack prepare pnpm@latest --activate\n"
          "npx paperclipai onboard --yes"),
 ("p", "Onboarding downloads Paperclip, writes the local configuration, initialises an "
       "embedded PostgreSQL, starts the server and normally opens your browser. Two ports "
       "matter and they are easy to confuse:"),
 ("table", ("Ports and paths you will need",
   ["What", "Value"],
   [["API and UI", "http://localhost:3100 (default host 127.0.0.1)"],
    ["Embedded PostgreSQL", "port 54329"],
    ["Health endpoint", "GET /api/health"],
    ["Master key size", "32 bytes"],
    ["Config, database, uploads, logs, secrets, workspaces", "~/.paperclip/instances/"],
    ["Managed CLI install", "~/.paperclip/cli, entry point ~/.local/bin/paperclipai"]])),
 ("note", "Run onboarding from a NORMAL user shell. Never prepend sudo and never use an "
          "elevated Administrator or root terminal — the embedded PostgreSQL refuses to "
          "start when the data directory is owned by a different user than the process."),

 ("h2", "B2. Proving the install before you build on it"),
 ("p", "Two checks, in this order. The diagnostic first, because it tells you what is wrong; "
       "the health endpoint second, because it tells you the server is answering for itself."),
 ("code", "npx paperclipai doctor          # fix the EARLIEST reported error first\n"
          "npx paperclipai doctor --repair # attempt automatic remediation\n"
          "curl -sS http://localhost:3100/api/health   # expect an ok status"),
 ("p", "The discipline that matters here is the DIAGNOSIS LADDER. Faults are almost always "
       "at the lowest broken rung, and fixing something higher up while a lower rung is "
       "broken produces confusing, misleading results."),
 ("table", ("The diagnosis ladder — always work upward from rung 1",
   ["Rung", "What must be true", "How you prove it"],
   [["1 · Host", "Node 20+, a normal non-elevated user, a writable practice root",
     "node --version, and check who owns the folder"],
    ["2 · Control plane", "doctor is clean and the server answers",
     "npx paperclipai doctor, then GET /api/health"],
    ["3 · Adapter", "the runtime is installed AND authenticated outside Paperclip",
     "run the runtime's own CLI directly, then Verify connection"],
    ["4 · Agent", "the agent produces a real artifact in the correct workspace",
     "a marker run, then git status in that workspace"]])),
 ("note", "Change ONE setting at a time and re-verify. If you change three things and the "
          "fault clears, you have not fixed it — you have lost the ability to say what was "
          "wrong, and it will come back."),

 ("h2", "B3. Deployment modes and exposure"),
 ("p", "Exposure is a deliberate decision, not a default you inherit. Paperclip's deployment "
       "modes are set with `paperclipai configure --section server` or the "
       "PAPERCLIP_DEPLOYMENT_MODE environment variable."),
 ("table", ("Deployment modes",
   ["Mode", "Login", "Use it when"],
   [["local_trusted (default)", "No login required",
     "A single operator on their own machine. This is the mode used throughout this course."],
    ["authenticated + private", "Login required, not publicly reachable",
     "A small team on a trusted network or a private mesh."],
    ["authenticated + public", "Login required, publicly reachable",
     "A hosted deployment. Requires the most care: real auth, real secrets, real exposure."]])),
 ("p", "`paperclipai env` marks exactly TWO variables as required: PAPERCLIP_AGENT_JWT_SECRET "
       "and DATABASE_URL. A third, PAPERCLIP_TOOL_ACTION_SIGNING_SECRET, is separately "
       "documented as required with no fallback for tool-action approvals."),
 ("table", ("Environment variables you cannot skip",
   ["Variable", "Purpose"],
   [["PAPERCLIP_AGENT_JWT_SECRET", "Signs agent tokens. Required."],
    ["DATABASE_URL", "Connection string for PostgreSQL. Required."],
    ["PAPERCLIP_TOOL_ACTION_SIGNING_SECRET", "Signs TOOL-ACTION approvals. Documented as "
     "required, with no fallback."],
    ["PAPERCLIP_ALLOWED_HOSTNAMES", "Hostnames the server will answer for. Add custom domains."],
    ["PAPERCLIP_TELEMETRY_DISABLED / DO_NOT_TRACK", "Set to 1 to disable telemetry."]])),
 ("note", "There are roughly seventy environment variables across nine categories. You do not "
          "need to memorise them. You DO need to know which are required, and that "
          "PAPERCLIP_AGENT_JWT_SECRET also acts as the fallback for BETTER_AUTH_SECRET."),

 ("h2", "B4. The company and its mission"),
 ("p", "A company is the isolation boundary: one goal, one team of agents, one task board, "
       "one budget. Companies do not share agents, skills, issues or costs. One deployment "
       "can host many."),
 ("p", "The mission is the single most important text you will write, because everything "
       "downstream inherits from it. A mission must be MEASURABLE, which means three "
       "properties:"),
 ("table", ("What makes a mission verifiable",
   ["Property", "Question it answers", "Example"],
   [["Target", "How much?", "8 short-form videos per month"],
    ["Metric", "Measured how?", "average watch-through rate"],
    ["Boundary", "Within what limit?", "at or above 5%"]])),
 ("p", "\"Grow the channel\" has none of these and cannot be verified by anyone, including "
       "the agent. \"Publish 8 short-form videos per month at an average watch-through rate "
       "of at least 5%\" has all three, and an agent can tell whether it is winning."),
 ("note", "Set the COMPANY budget cap BEFORE you hire anyone. A company that gains a runtime "
          "before it gains a ceiling can spend without limit, and budget enforcement happens "
          "at checkout — so the cap must exist before any agent is able to check out work."),

 ("h2", "B5. The org chart"),
 ("p", "Paperclip enforces a strict hierarchy, and the rule is absolute: every agent reports "
       "to exactly one manager, and the CEO is the only agent with no manager. There are no "
       "matrix reporting lines and no unmanaged agents."),
 ("p", "The CEO is the first hire. It owns goal alignment, decomposition and final synthesis, "
       "and it may propose further hires — subject to approval, which you will meet in Part D."),
 ("table", ("The six fields that define every agent",
   ["Field", "What it controls"],
   [["Role", "What this agent is for — the single transformation it owns."],
    ["Manager", "Its reporting line. Exactly one, except for the CEO."],
    ["Adapter", "Which runtime actually executes its work."],
    ["Instructions", "Its contract: purpose, inputs, output schema, exclusions, escalation."],
    ["Heartbeat", "When it wakes, and on which triggers."],
    ["Budget", "Its individual monthly ceiling."]])),
 ("p", "The documentation gives starting budget guidance by seniority, which is a useful "
       "sanity check on your own numbers:"),
 ("table", ("Suggested starting budgets (from the official documentation)",
   ["Role", "Typical starting budget"],
   [["CEO", "$30–50 per month"],
    ["Manager (CTO, CMO, …)", "$20–40 per month"],
    ["Worker agent", "$10–25 per month"]])),

 ("h2", "B6. Role instructions are a contract, not a personality"),
 ("p", "The most common beginner error is writing an instruction that describes a character "
       "— \"you are a meticulous financial analyst who loves detail\" — instead of a "
       "contract. Tone does not constrain behaviour. Structure does."),
 ("table", ("The five sections every role instruction needs",
   ["Section", "States", "Why it matters"],
   [["PURPOSE", "The single transformation this role owns",
     "Prevents scope drift into a neighbouring role's work."],
    ["ALLOWED INPUTS", "Which files, data and sources may be read",
     "Confines the blast radius when something goes wrong."],
    ["OUTPUT SCHEMA", "The artifact, its path, and its required fields",
     "Makes acceptance objective rather than a matter of opinion."],
    ["EXCLUSIONS", "What this role must NEVER do",
     "The most valuable section, and the one people leave out."],
    ["ESCALATION", "When to stop and ask the board",
     "Keeps human authority explicit instead of assumed."]])),
 ("note", "Test: if two of your roles could each plausibly claim the same task, your "
          "instructions are not finished. Ambiguity in the org chart shows up later as two "
          "agents doing the same work and neither being accountable for it."),

 ("h2", "B7. Adapters — connecting real runtimes"),
 ("p", "An adapter is the connection between Paperclip and the system that actually runs your "
       "agent. The documentation devotes about twenty pages to adapters; the type keys "
       "below are the eleven that appear in the adapters overview, and they matter because "
       "they appear in configuration and in the API:"),
 ("table", ("Adapter type keys",
   ["Type key", "Runtime"],
   [["claude_local", "Claude Code running locally"],
    ["codex_local", "OpenAI Codex CLI running locally"],
    ["gemini_local", "Gemini CLI running locally"],
    ["opencode_local", "OpenCode running locally"],
    ["cursor", "Cursor (local and cloud variants exist)"],
    ["pi_local", "Pi running locally"],
    ["hermes_local", "Hermes running locally"],
    ["process", "An arbitrary local process"],
    ["http", "An HTTP / webhook endpoint"],
    ["grok_local", "Grok running locally"],
    ["openclaw_gateway", "OpenClaw via its gateway"]])),
 ("note", "process, http and openclaw_gateway are functional in the runtime but appear as "
          "\"Coming soon\" in the UI dropdown. If you need them today, configure them through "
          "the API rather than the picker."),
 ("p", "Adapters carry their own defaults which materially affect cost and safety. The Claude "
       "Code adapter, for example, defaults to a maximum of 300 turns per run, has "
       "dangerouslySkipPermissions set to true, and a sandbox timeout of 14,400 seconds "
       "(four hours). Every one of those is a number you should look at before you let an "
       "agent run unattended."),
 ("p", "Adapter readiness is proved by a MARKER RUN, never by a saved configuration. A marker "
       "run is a deliberately trivial task whose only purpose is to produce one named file in "
       "one named workspace. If the file appears in the right place, the boundary is real. If "
       "it appears somewhere else, the workspace path is misbound — correct it on the AGENT, "
       "delete the stray file, and run the marker again."),

 ("h2", "B8. Workspaces, secrets and skills"),
 ("p", "A workspace is where an agent's work physically lives. Each agent gets its own root, "
       "so that every change on disk is attributable to exactly one role. Workspaces have "
       "their own lifecycle, and a degraded or failed workspace is a common cause of an agent "
       "that appears to do nothing:"),
 ("bullets", [
   "provisioning — being created",
   "validating — being checked",
   "ready — usable",
   "degraded — usable but something is wrong",
   "repairing — being fixed",
   "failed — unusable",
   "archived — retired",
 ]),
 ("p", "Commit an empty Git baseline in each workspace before any agent runs. It costs one "
       "command and it is what makes every later diff readable:"),
 ("code", "git -C workspace/<role> init -q\n"
          "git -C workspace/<role> commit -q --allow-empty -m 'baseline'"),
 ("p", "Secrets never belong in a prompt, a lab note or Git. They live in the runtime or in "
       "Paperclip's secret store and are injected at heartbeat time with a defined scope. "
       "Two operational limits are worth knowing: secret proposals are capped at 20 pending "
       "and 20 per minute, and they expire after 14 days."),
 ("note", "Board tokens (pcp_board_*) and agent keys are printed ONCE at creation and never "
          "shown again — including the key minted by `agent local-cli`. Capture it at the "
          "moment of creation or mint a new one."),
 ("p", "A skill is a reusable instruction document an agent loads on demand. The point is "
       "context economy: an agent with ten skills does not load all ten on every heartbeat, "
       "only the relevant ones. That means fewer tokens per run, cleaner context, and one "
       "place to update a procedure that many agents share."),
 ("code", "skills/\n"
          "└── code-review/\n"
          "    ├── SKILL.md\n"
          "    └── references/\n"
          "        └── examples.md"),
 ("p", "SKILL.md carries YAML frontmatter with name, description, slug, key and metadata. "
       "The description should be written as DECISION LOGIC — when to use this skill and when "
       "not to — because that is what the agent reads to decide whether to load it:"),
 ("code", "---\n"
          "name: code-review\n"
          "description: >\n"
          "  Use when asked to review a pull request or code diff.\n"
          "  Don't use when writing new code from scratch.\n"
          "---"),
 ("bullets", [
   "Skills are COMPANY-SCOPED and are never shared across companies.",
   "Folders may nest up to four levels deep.",
   "Skills are attached at hire time via desiredSkills, or later via "
   "POST /api/agents/{agentId}/skills/sync with mode add, remove or replace.",
   "paperclip_bundled skills: the behaviour CHANGED between documentation surfaces — see the "
   "note below before relying on either description.",
 ]),
 ("note", "A known contradiction in the official documentation. The Skills API reference states "
          "that paperclip_bundled skills are force-unioned into every agent, so removing one has "
          "no effect. The newer CLI Skills page states that the server NO LONGER force-attaches "
          "them, and that they remain in the company library as read-only entries. Treat the CLI "
          "page as the current behaviour, verify on your own install with the skills commands in "
          "Part G, and do not design a control that depends on either behaviour persisting."),

 ("check", [
   "Why must the company budget cap be set before the first hire?",
   "State the three properties of a measurable mission, and rewrite "
   "'improve our reporting' so it has all three.",
   "Name the five sections of a role instruction and say which one learners most often omit.",
   "An agent is configured, the adapter shows connected, but nothing appears in its "
   "workspace. Work the diagnosis ladder aloud from rung 1.",
   "Why is a marker run stronger evidence than a green 'connection verified' badge?",
 ]),
 ("rule",),
]


# ══════════════════════════════════════════════════════════════════ Part B-extra
PART_B2 = [
 ("h2", "B9. Anatomy of a heartbeat run"),
 ("p", "It is worth knowing what actually happens when an agent wakes, because almost every "
       "diagnostic question resolves to \"which of these six steps failed?\""),
 ("table", ("The six-step execution arc",
   ["Step", "What happens", "Fails when"],
   [["1. Trigger", "A schedule tick, an assignment, an @-mention, a manual invoke or an "
     "approval resolution wakes the agent.", "Nothing is assigned and the interval is off — "
     "the usual reason an agent 'does nothing'."],
    ["2. Adapter invocation", "Paperclip calls the configured adapter.",
     "The adapter is misconfigured or the runtime is not authenticated."],
    ["3. Agent process spawn", "The runtime process starts.",
     "The binary is missing, or the sandbox cannot start."],
    ["4. Paperclip API calls", "The agent reads its work and writes results back.",
     "Checkout conflicts (409), or the cross-issue write limit is hit."],
    ["5. Result capture", "Output, artifacts and token usage are captured.",
     "The process is lost mid-run — recorded as the error kind process_lost."],
    ["6. Run record storage", "The run, its cost and its activity entries are persisted.",
     "Rarely fails; if it does, the audit trail has a gap you must explain."]])),
 ("p", "Agents keep conversation context across heartbeats through SESSION PERSISTENCE. Each "
       "run records a session ID before and a session ID after. If the pair differs the "
       "session rotated during the run; if it matches, the agent continued the same "
       "conversation. When an agent seems to have forgotten prior context, that pair is the "
       "first thing to look at."),

 ("h2", "B10. Agent states and what each one means"),
 ("table", ("The seven agent states",
   ["State", "Meaning"],
   [["active", "Enabled and ready for heartbeats."],
    ["idle", "Active, but no heartbeat is currently running."],
    ["running", "A heartbeat is in progress right now."],
    ["error", "The last heartbeat failed. Not working, and did not stop gracefully."],
    ["paused", "Deliberately stopped — by you, or automatically on hitting the budget limit."],
    ["terminated", "Permanently deactivated. Not reversible."],
    ["pending_approval", "Hired but awaiting board approval before it may run."]])),
 ("p", "Runs have their own statuses — queued, running, succeeded, failed, timed out and "
       "cancelled — plus the error kind process_lost, which is recoverable via Resume rather "
       "than requiring a fresh run."),
 ("note", "Pause is reversible; Terminate is not. The agent overflow menu offers both, and "
          "the documentation is explicit that Terminate is \"permanent; use Pause for "
          "reversible pause\". Read that twice before clicking."),

 ("h2", "B11. Structuring an agent's instructions"),
 ("p", "Paperclip can either own the instruction files itself (a MANAGED bundle) or point at "
       "an existing folder you control (an EXTERNAL bundle, via rootPath). Either way, the "
       "documentation recommends a four-file structure, and it is a good structure because "
       "each file answers a different question:"),
 ("table", ("The recommended instruction files",
   ["File", "Answers"],
   [["AGENTS.md", "The operating manual — the entry file, and the default."],
    ["SOUL.md", "Persona and decision philosophy — how this role weighs trade-offs."],
    ["HEARTBEAT.md", "The per-heartbeat checklist — what to do on every single wake."],
    ["TOOLS.md", "Available tools and API notes — what this role may call."]])),
 ("p", "The split matters for cost as well as clarity. Material that belongs in every run "
       "(HEARTBEAT.md) is separated from material that is only occasionally relevant, which "
       "is the same economy that makes skills worthwhile."),

 ("h2", "B12. Reading the dashboard"),
 ("p", "The dashboard is the page you will return to most. The documentation likens it to "
       "cockpit instruments, and the analogy is apt: you are not reading it for detail, you "
       "are reading it to decide whether to look closer."),
 ("bullets", [
   "Agents Enabled — how many agents can work, and how many are running, paused or in error.",
   "Tasks In Progress — how many issues are being worked, plus open and blocked counts.",
   "Month Spend — spend this month against the company budget.",
   "Pending Approvals — how many decisions are waiting on you.",
 ]),
 ("table", ("Reading the dashboard at a glance",
   ["Signal", "Healthy", "Needs attention"],
   [["Agents", "Mostly active or running", "Any in error, or unexpectedly paused"],
    ["Tasks in progress", "Work is moving", "Nothing in progress for hours, or many blocked"],
    ["Month spend", "Climbing predictably", "A sudden jump, or active budget incidents"],
    ["Approvals", "Queue manageable", "Pending approvals piling up"],
    ["Recent activity", "Steady, understandable motion", "Long silence, or repeated failures"]])),
 ("note", "The healthy pattern for a small company is ONE agent running while the others stay "
          "active. Several agents running at once is not automatically wrong, but it does "
          "mean you can no longer attribute a workspace change to a single run by timing "
          "alone. The activity feed is a pulse check, not an investigation tool."),
]

# ══════════════════════════════════════════════════════════════════ Part C
PART_C = [
 ("h1", "Part C — Running the Operation: Work, Heartbeats and Verification"),

 ("h2", "C1. Projects, goals and lineage"),
 ("p", "A project holds goals and issues and supplies the context an agent reads at runtime. "
       "The reason this matters is LINEAGE: work carries its full ancestry, so an agent can "
       "see why a task exists and not merely what it says."),
 ("code", "company mission\n"
          "  └── project goal\n"
          "        └── parent issue  (synthesis)\n"
          "              ├── child issue  (specialist A)\n"
          "              └── child issue  (specialist B)"),
 ("p", "Projects have their own lifecycle — backlog, planned, in_progress, completed, "
       "cancelled — and can carry a LIFETIME budget cap, distinct from the monthly caps "
       "applied to companies and agents."),
 ("note", "An agent that cannot trace its lineage is working without direction. If you find "
          "yourself re-explaining the goal in every issue body, your lineage is broken and "
          "you are paying for the same context repeatedly."),

 ("h2", "C2. Issues — the seven states"),
 ("p", "Work in Paperclip is an issue, and issues move through a defined state machine. Learn "
       "these seven; the assessment expects them by name."),
 ("table", ("Issue states, with the documentation's own definitions",
   ["State", "Definition"],
   [["backlog", "\"The issue exists and has been identified, but no one is working on it yet.\""],
    ["todo", "\"The issue is ready to start. An agent has been assigned and is waiting to "
     "check it out.\""],
    ["in_progress", "\"An agent has checked out the issue and is actively working on it. "
     "Only one agent can hold an issue in this state at a time.\""],
    ["in_review", "\"The agent has completed the work and moved the issue to review. It's "
     "waiting for sign-off.\""],
    ["done", "Terminal. The work is complete."],
    ["blocked", "\"The agent can't move forward. Something is preventing progress.\""],
    ["cancelled", "\"The issue is no longer needed and won't be completed.\" Also terminal."]])),
 ("note", "Issues do not move backwards. done and cancelled are TERMINAL states — a terminal "
          "issue can only be revived through an explicit reopen, never by editing its status."),
 ("p", "The normal path is backlog → todo → in_progress → in_review → done, with blocked and "
       "cancelled available as departures from it."),

 ("h2", "C3. Checkout — the rule that prevents double work"),
 ("p", "When an agent picks up a task it CHECKS IT OUT, claiming exclusive ownership. Only "
       "one agent can hold an issue in in_progress at a time. This is enforced by the "
       "platform, not by convention, and there are hard rules around it that trip up almost "
       "everyone integrating through the API:"),
 ("table", ("Checkout discipline — common mistakes",
   ["Mistake", "What to do instead"],
   [["PATCHing status directly to in_progress", "Never do this. Use the checkout mechanism; "
     "a direct status write bypasses the lock."],
    ["Retrying after a 409 Conflict", "Treat 409 as TERMINAL. Another agent holds the issue; "
     "retrying will not win the race."],
    ["Expecting a cancelled blocker to unblock its dependents", "Cancelled blockers never "
     "auto-unblock dependents. Resolve the dependency explicitly."],
    ["Editing a done issue's status to reopen it", "Terminal issues reopen only via an "
     "explicit reopen: true."]])),
 ("p", "Runs identify themselves with an X-Paperclip-Run-Id header, which is how a write is "
       "attributed to the execution that made it. There is also a hard limit worth knowing: "
       "CROSS_ISSUE_INFLUENCE_LIMIT is 20 — a single heartbeat run may write to at most "
       "twenty other issues, which exists to stop one confused agent rewriting the whole board."),

 ("h2", "C4. Heartbeats — the execution model"),
 ("p", "A heartbeat is a scheduled execution window: the agent wakes, checks its inbox, does "
       "work, and goes dormant again. Between heartbeats the agent is not idling and not "
       "billing — it does not exist as a running process."),
 ("p", "There are FIVE triggers. Most people can name three and are surprised by the other two:"),
 ("table", ("The five heartbeat triggers",
   ["Trigger", "Fires when"],
   [["Schedule / interval", "The configured interval ticks — whether or not there is work."],
    ["Task assignment", "An issue is assigned to the agent. THIS is what makes assignment "
     "the real trigger for work."],
    ["Comment mention", "Someone @-mentions the agent in a comment."],
    ["Manual invoke", "A human presses Run Heartbeat."],
    ["Approval resolution", "An approval the agent was waiting on is decided."]])),
 ("note", "\"Heartbeat on interval\" is OFF BY DEFAULT, and the recommended combination is "
          "interval OFF with wake-on-demand ON. The interval is described as \"a floor, not a "
          "guarantee\" — a busy agent may run more often because events trigger wakes."),
 ("p", "This default is a good one and you should think hard before changing it. An interval "
       "means the agent wakes whether or not there is anything to do, and each wake costs "
       "money. Event-driven waking costs nothing when nothing is happening."),
 ("p", "There is also an important distinction between two things that look similar:"),
 ("table", ("Paused versus heartbeat-off",
   ["", "Wakes on interval", "Wakes on assignment / comment / routine / on-demand"],
   [["Heartbeat off", "No", "YES"],
    ["Paused", "No", "No — paused wakes on nothing"]])),

 ("h2", "C5. Decomposition and assignment"),
 ("p", "The pattern you will use in every lab: create a PARENT synthesis issue and its "
       "specialist CHILD issues, all UNASSIGNED, then assign one child at a time."),
 ("p", "Creating issues unassigned is a control decision, not a stylistic one. Assignment is a "
       "heartbeat trigger — so an issue created with an assignee wakes an agent immediately, "
       "before you have finished writing the acceptance criteria and before you have checked "
       "the caps. Create everything cold, then start the work deliberately."),
 ("p", "Assign ONE child at a time. Sequential runs are individually attributable; overlapping "
       "runs are not. If two specialists ran simultaneously you cannot demonstrate that the "
       "second consumed the first's output, which means you cannot prove the hand-off happened."),

 ("h2", "C6. Acceptance criteria that name evidence"),
 ("p", "An acceptance criterion must name the EVIDENCE, not the activity. This is the single "
       "highest-leverage writing skill in the course."),
 ("table", ("Activity versus evidence",
   ["Fails — describes activity", "Works — names evidence"],
   [["\"The research is done.\"",
     "\"workspace/research-analyst/research.md exists and contains claim, source, date "
     "accessed and confidence for every claim.\""],
    ["\"Reconcile the control accounts.\"",
     "\"reconciliation.md lists every control account with ledger balance, statement "
     "balance and variance.\""],
    ["\"Review for compliance.\"",
     "\"exceptions.md lists each variance above SGD 500 with a stated cause and a "
     "recommended treatment.\""]])),
 ("p", "The test for a good criterion: could a stranger, with no knowledge of the "
       "conversation, look at the workspace and say yes or no? If judging it requires asking "
       "the agent what it meant, the criterion is not finished."),

 ("h2", "C7. Verification — one thread, five places"),
 ("p", "Verifying that work between disparate components actually functioned means tracing "
       "ONE thread across five places and finding them consistent."),
 ("table", ("The evidence chain",
   ["Place", "What it tells you"],
   [["Issue ID", "What was asked, and under which lineage."],
    ["Run log", "What actually executed, and whether it errored."],
    ["Comment", "What was accepted, by whom, on what basis."],
    ["Workspace diff", "What changed on disk. The strongest evidence you have."],
    ["Cost entry", "What it spent — and whether that is plausible for the work claimed."]])),
 ("note", "STATUS IS NOT EVIDENCE. An issue marked done with no linked artifact and no diff "
          "is an unverified claim, however confident the agent's summary sounds."),
 ("p", "Read the diff before accepting any summary. An agent describing its own work is a "
       "witness with an interest in the verdict; the diff is the record."),
 ("p", "A hand-off is accepted only when the receiving agent can consume the artifact WITHOUT "
       "asking the producer a question. If the receiver needs clarification, the output schema "
       "in the producer's instruction was under-specified — fix the contract, do not patch "
       "the artifact by hand."),
 ("p", "Finally, value explicit limitations. An agent that reports what it could NOT establish "
       "is more useful than one that quietly guesses, and a deliverable with a stated "
       "limitations section is a sign of a well-written role, not a weak one."),

 ("h2", "C8. Execution policy and review rounds"),
 ("p", "Paperclip can enforce a review workflow on an issue's execution. The parameters are "
       "small in number but consequential:"),
 ("table", ("Execution policy parameters",
   ["Parameter", "Value"],
   [["maxReviewRounds", "Default 3. Range 1–50. A null value means the server default of 3."],
    ["approvalsNeeded", "Fixed at 1."],
    ["changesRequestedCount", "Counts review rounds; escalates when the cap is reached."],
    ["Comment-required backstop", "retry_queued → retry_exhausted"]])),
 ("p", "Once a reviewer has been escalated to, only that reviewer may advance the stage. "
       "Attempting otherwise returns 422 Unprocessable Entity with the message \"Only the "
       "escalated reviewer can advance the current execution stage\". If you see that error, "
       "you are not blocked by a bug — you are blocked by the policy working."),

 ("check", [
   "List the seven issue states and identify the two terminal ones.",
   "Why does creating issues unassigned change the risk profile of a company?",
   "Name the five heartbeat triggers.",
   "You receive a 409 Conflict when checking out an issue. What does it mean and what do you do?",
   "Rewrite 'the analysis is complete' as an acceptance criterion that names evidence.",
   "Two child issues show overlapping run timestamps. What can you no longer prove?",
 ]),
 ("rule",),
]

# ══════════════════════════════════════════════════════════════════ Part D
PART_D = [
 ("h1", "Part D — Governing the Operation: Budgets, Approvals, Routines and Audit"),

 ("h2", "D1. Budgets — three scopes, enforced together"),
 ("p", "This is the section most often misunderstood, and the misunderstanding is expensive. "
       "Paperclip has THREE budget scopes and they are enforced in PARALLEL, not nested."),
 ("table", ("The three budget scopes",
   ["Scope", "Period", "Applies to"],
   [["Company budget", "Monthly", "The total ceiling for the entire company."],
    ["Per-agent budget", "Monthly", "One individual agent's ceiling."],
    ["Project budget", "Lifetime", "An execution-bound project, for its whole life."]])),
 ("note", "The scopes are independent. The documentation is explicit: \"an agent can be "
          "paused by its own budget limit even if the company has remaining budget.\" Do not "
          "picture nested rings where the outer one always binds first — picture three "
          "separate trip switches, any of which can fire."),
 ("p", "Enforcement is a two-stage circuit breaker with exact thresholds:"),
 ("table", ("Budget enforcement thresholds",
   ["Utilisation", "What happens"],
   [["80%", "A warning is recorded so you can intervene. The agent CONTINUES running."],
    ["100%", "The agent is automatically PAUSED. No further heartbeats fire. "
     "pauseReason = \"budget\"."]])),
 ("p", "The utilisation bar is colour-coded so you can read a company's health at a glance: "
       "green below 70%, yellow from 70 to 90%, red above 90%."),
 ("p", "Enforcement happens AT CHECKOUT — before the work runs, not when the invoice arrives. "
       "That is what makes unattended operation safe: a runaway retry loop stops at the "
       "ceiling instead of running all night."),
 ("note", "A cap you would be unhappy to actually pay is set too high. Set it at the number "
          "you are genuinely willing to lose to a bug, because one day you will."),
 ("p", "Costs are tracked at token level by provider, model, agent and project, and the Costs "
       "page separates INFERENCE spend (per-request model cost) from FINANCE events "
       "(subscriptions, invoices, credits, refunds, adjustments) — do not read one and think "
       "you have seen the other."),

 ("h2", "D2. Approvals — where human authority is made explicit"),
 ("p", "An approval is a governance gate: Paperclip pauses and asks a human to sign off "
       "before an important action proceeds. There are three types you will meet:"),
 ("table", ("Approval types",
   ["Type", "Raised when"],
   [["CEO Strategy", "The CEO produces a strategic plan after its first heartbeat. "
     "\"The CEO cannot move tasks to 'in progress' until you approve its strategy.\""],
    ["Hire Agent", "An agent (usually the CEO or a manager) proposes a subordinate. The "
     "payload includes name, role, capabilities, adapter configuration, monthly budget and "
     "reporting line."],
    ["Budget Override", "A budget policy hits a hard stop and someone asks to proceed anyway."]])),
 ("p", "You have three possible responses, and the third is the one people forget exists:"),
 ("bullets", [
   "APPROVE — the action proceeds. For a hire, the agent is created, configured and queued "
   "to wake automatically.",
   "REJECT — the action is denied. The requesting agent is notified and will not retry "
   "unless instructed.",
   "REQUEST REVISION — you are not approving as-is, but you are not saying no. The agent "
   "revises and resubmits.",
 ]),
 ("p", "The state machine reflects that third option:"),
 ("code", "pending ──→ approved\n"
          "        ├─→ rejected\n"
          "        └─→ revision_requested ──→ resubmitted ──→ pending"),
 ("note", "Approvals do NOT expire on their own. An agent waiting on a pending approval "
          "pauses at that point indefinitely. A silent, stalled company is very often an "
          "unattended approval queue — check it first."),
 ("p", "The board also holds override powers that bypass the approval flow entirely: pause "
       "any agent, and resume any paused agent. These are blunt instruments and belong in the "
       "intervention ladder, not in routine operation."),
 ("p", "Whatever you decide, RECORD THE RATIONALE. One sentence explaining why is the "
       "difference between a decision and an unaudited event. Months later, the rationale is "
       "the only thing that will tell you — or a regulator — what you were thinking."),

 ("h2", "D3. Routines — automation earns the schedule"),
 ("p", "A routine is recurring work triggered by cron, webhook or API. The rule for "
       "introducing one is a discipline, and it exists because a routine that has never "
       "succeeded is simply scheduled spend nobody has reviewed."),
 ("bullets", [
   "1. Create the routine PAUSED.",
   "2. Add the schedule trigger EXPLICITLY — a cron expression AND an IANA timezone.",
   "3. Name the artifact the routine must produce, or the run is successful but unverifiable.",
   "4. Run it ONCE manually, with a bounded wait, and read the generated issue, the run and "
   "the cost.",
   "5. Leave it paused until you have done step 4. Only then let the schedule own it.",
 ]),
 ("p", "The timezone is not a formality. `30 16 * * *` without a timezone runs at 16:30 in "
       "whatever zone the host happens to be in, which is fine until the host moves, the "
       "clock changes, or someone deploys to a different region. Write Asia/Singapore and "
       "the ambiguity disappears."),
 ("note", "The routine editor snaps minutes to FIVE-MINUTE increments. Concurrency defaults "
          "are \"coalesce if active, skip missed\" — a routine already running will not start "
          "a second copy, and a missed window is skipped rather than backfilled."),
 ("p", "Routine states are paused, draft, archived, succeeded, failed and running. A routine "
       "left in running when nothing is happening usually means a lost process — check the "
       "run log for a process_lost error kind."),

 ("h2", "D4. The activity log and closing the audit loop"),
 ("p", "Activity is the durable record of mutations, heartbeats, cost events and approvals. "
       "It is the subsystem that makes everything else defensible."),
 ("p", "The audit loop CLOSES when the entire operation can be reconstructed from the log "
       "alone — company creation, hires, issues, runs, costs, approvals and interventions, in "
       "order, with no unexplained gap."),
 ("p", "Build a mission-to-evidence audit map. One row per mission claim, linking the issue, "
       "the run, the artifact, the cost entry and the approval that evidences it. This is, "
       "concretely, the artifact a regulator or an auditor would ask you for."),
 ("code", "| Mission claim | Issue | Run | Artifact | Cost | Approval |\n"
          "|---------------|-------|-----|----------|------|----------|"),
 ("note", "An unexplained gap in the activity log usually means work was done OUTSIDE a run — "
          "typically hand-edited in the workspace. Record it honestly. The gap is itself an "
          "audit finding, and concealing it is far worse than having it."),

 ("h2", "D5. The operator intervention ladder"),
 ("p", "When an agent misbehaves, use the LEAST IRREVERSIBLE control that resolves the "
       "situation. Escalate only when the rung below has genuinely failed."),
 ("table", ("The intervention ladder",
   ["Rung", "Action", "Reversible?", "Use when"],
   [["1", "INSPECT — read task, run, cost and activity evidence", "Yes, nothing changes",
     "Always. Never act before you have looked."],
    ["2", "PAUSE — stop new heartbeats, keep all state", "Yes",
     "The agent is doing something wrong and you need it to stop now."],
    ["3", "REASSIGN — move the work to another role", "Yes",
     "The work is valid but this agent is the wrong owner."],
    ["4", "TERMINATE — retire the agent", "NO", "The role should not exist. Last resort."]])),
 ("note", "Terminate is not reversible. Practise it only on a role you deliberately created "
          "as disposable, and never as a first response to a misbehaving production agent."),

 ("h2", "D6. Roles and permissions"),
 ("p", "Human members of a company hold roles, and roles imply permission grants. There are "
       "four roles plus an unset state, and twenty-one permission keys."),
 ("table", ("Company roles and their implicit grants",
   ["Role", "Description", "Implicit grants"],
   [["Owner", "\"The people who run the company\"",
     "agents:create, agents:configure, skills:create, environments:manage, users:invite, "
     "users:manage_permissions, tasks:assign, joins:approve"],
    ["Admin", "\"Trusted operators who onboard people and agents\"",
     "As Owner, MINUS users:manage_permissions"],
    ["Operator", "\"Hands-on members who help run the work\"", "tasks:assign"],
    ["Viewer", "\"Read-only observers\"", "None"],
    ["Unset", "No implicit grants", "Hand-picked explicit grants only"]])),
 ("note", "Two rules with real consequences: an explicit grant PERSISTS across a role change, "
          "and there is NO DENY LAYER. You cannot subtract a permission from a role — you can "
          "only choose a role that does not include it, or leave the role unset and grant "
          "explicitly."),

 ("h2", "D7. Portability — moving a company"),
 ("p", "A whole company exports and imports, with secrets scrubbed and identifier collisions "
       "re-mapped. This is what makes a Paperclip organisation data rather than a hand-built "
       "configuration you are afraid to touch."),
 ("p", "Practical uses: backing up before a risky change, cloning a proven structure for a "
       "second business line, moving from a laptop to a hosted deployment, and handing a "
       "working company to a colleague."),

 ("check", [
   "State the three budget scopes and their periods. Are they nested or parallel?",
   "At what utilisation does Paperclip warn, and at what utilisation does it pause the agent?",
   "Name the three approval types and the three possible responses.",
   "Your company has gone quiet — no runs, no errors, no spend. What do you check first, and why?",
   "Put the intervention ladder in order and say which rung is irreversible.",
   "What does an unexplained gap in the activity log usually mean, and what should you do about it?",
 ]),
 ("rule",),
]

# ══════════════════════════════════════════════════════════════════ Appendices
APPENDICES = [
 ("h1", "Appendix A — Command Reference"),
 ("p", "The commands you will actually use in this course, grouped by purpose. The CLI binary "
       "is `paperclipai`; the npm package has the same name."),
 ("h3", "Install and verify"),
 ("code", "node --version                        # must be v20 or later\n"
          "npx paperclipai onboard --yes         # download, configure, initialise, start\n"
          "npx paperclipai run                   # start an already-configured instance\n"
          "npx paperclipai doctor                # diagnose\n"
          "npx paperclipai doctor --repair       # diagnose and attempt repair\n"
          "npx paperclipai configure             # edit configuration\n"
          "npx paperclipai configure --section server   # deployment mode / binding\n"
          "npx paperclipai env                   # show non-sensitive instance settings\n"
          "curl -sS http://localhost:3100/api/health"),
  ("h3", "Managed install and service"),
 ("code", "npx paperclipai install                # installs to ~/.local/bin/paperclipai\n"
          "paperclipai service install            # register the background service\n"
          "paperclipai channels                   # stable | beta | nightly | canary\n"
          "sudo journalctl -u paperclip -f        # follow the service log (Linux/WSL2)"),
 ("note", "The managed install at ~/.local/bin/paperclipai carries automatic updates and "
          "rollback. Beyond `service install` the documentation does not publish a full "
          "`service` subcommand list — check `paperclipai service --help` on your own "
          "install rather than assuming a subcommand exists."),
 ("h3", "Verification in a workspace"),
 ("code", "git -C workspace/<role> init -q\n"
          "git -C workspace/<role> commit -q --allow-empty -m 'baseline'\n"
          "git -C workspace/<role> status --short\n"
          "git -C workspace/<role> diff HEAD --stat\n"
          "git -C workspace/<role> diff HEAD -- <artifact>"),
 ("note", "The CLI reference in the official documentation runs to more than thirty pages "
          "covering company, project, goal, issue, agent, prompt, run, routine, adapter, "
          "approval, activity, dashboard, cost, workspace, skills, secrets and more. Treat "
          "the list above as the working subset for this course, not the whole surface."),

 ("h1", "Appendix B — API Notes"),
 ("p", "Paperclip exposes a REST API on the same port as the UI. You do not need it for the "
       "labs, but the following facts explain behaviour you will see and are worth knowing "
       "before you automate anything."),
 ("bullets", [
   "Runs identify themselves with the X-Paperclip-Run-Id header — this is how a write is "
   "attributed to a specific execution.",
   "Checkout returns 409 Conflict when another agent holds the issue. Treat 409 as TERMINAL, "
   "not as a retry signal.",
   "Never PATCH an issue's status directly to in_progress; use the checkout mechanism.",
   "Terminal issues (done, cancelled) reopen only via an explicit reopen: true.",
   "Skills sync via POST /api/agents/{agentId}/skills/sync with mode add, remove or replace.",
   "CROSS_ISSUE_INFLUENCE_LIMIT is 20 cross-issue writes per heartbeat run.",
   "Board tokens are prefixed pcp_board_ and are shown once at creation only.",
 ]),

 ("h1", "Appendix C — Defaults, Limits and Thresholds"),
 ("p", "A consolidated reference. Every value here comes from the official documentation."),
 ("table", ("Numeric defaults and limits",
   ["Item", "Value"],
   [["Node.js minimum", "20"],
    ["API / UI port", "3100 (default host 127.0.0.1)"],
    ["Embedded PostgreSQL port", "54329"],
    ["Master key size", "32 bytes"],
    ["Budget warning threshold", "80% utilisation"],
    ["Budget hard stop", "100% — agent paused, pauseReason = \"budget\""],
    ["Utilisation bar colours", "green <70%, yellow 70–90%, red >90%"],
    ["Suggested CEO budget", "$30–50 / month"],
    ["Suggested manager budget", "$20–40 / month"],
    ["Suggested worker budget", "$10–25 / month"],
    ["maxReviewRounds", "default 3, range 1–50"],
    ["approvalsNeeded", "fixed at 1"],
    ["Cross-issue writes per run", "20"],
    ["Heartbeat on interval", "OFF by default"],
    ["Suggested starting interval", "once per hour"],
    ["Routine minute granularity", "snaps to 5-minute increments"],
    ["Routine concurrency default", "coalesce if active, skip missed"],
    ["Secret proposals", "20 pending, 20 per minute, 14-day expiry"],
    ["Skill folder nesting", "up to 4 levels"],
    ["Claude Code maxTurnsPerRun", "300"],
    ["Claude Code sandbox timeout", "14,400 seconds (4 hours)"],
    ["Config revisions shown", "10 most recent"],
    ["Agent dashboard chart window", "14 days"]])),

 ("h1", "Appendix D — State Machines at a Glance"),
 ("table", ("Every state machine you may be asked about",
   ["Entity", "States"],
   [["Issue / task", "backlog → todo → in_progress → in_review → done; plus blocked, "
     "cancelled. done and cancelled are terminal."],
    ["Agent", "active, idle, running, error, paused, terminated, pending_approval"],
    ["Run", "queued, running, succeeded, failed, timed out, cancelled"],
    ["Approval", "pending → approved / rejected / revision_requested → resubmitted → pending"],
    ["Project", "backlog, planned, in_progress, completed, cancelled"],
    ["Workspace", "provisioning, validating, ready, degraded, repairing, failed, idle, "
     "in review, running, archived, cleanup_failed"],
    ["Routine (status)", "active, paused, archived — only active fires. "
     "draft/running/succeeded/failed are list-view badges, not statuses."],
    ["Membership", "active, pending, suspended"],
    ["Issue execution state", "idle, pending, changes_requested, completed"]])),

 ("h1", "Appendix E — Troubleshooting Playbook"),
 ("table", ("Symptom → likely cause → first action",
   ["Symptom", "Likely cause", "First action"],
   [["Onboarding fails; PostgreSQL will not start", "Elevated shell, or a data directory "
     "owned by another user", "Close the elevated terminal. Re-run as the normal user who "
     "owns the practice folder."],
    ["Browser cannot reach port 3100", "Server not running, or bound to another interface",
     "npx paperclipai doctor, then npx paperclipai run, then re-check /api/health BEFORE "
     "touching any firewall."],
    ["Adapter verification fails", "Runtime not authenticated outside Paperclip",
     "Run the runtime's own CLI directly and sign in. Paperclip cannot authenticate it for you."],
    ["Agent never wakes", "Issue not assigned; interval off (the default); agent paused",
     "Check the assignee first — creating an issue does not wake anyone."],
    ["Everything is quiet: no runs, no spend", "An unattended approval queue",
     "Open Approvals. Approvals never expire on their own."],
    ["Agent stopped mid-work", "Budget hard stop at 100%",
     "Check the agent's utilisation and pauseReason. Raise the cap deliberately or let it stop."],
    ["Marker file in the wrong workspace", "Workspace path misbound on the agent",
     "Fix the path on the AGENT, delete the stray file, re-run the marker."],
    ["409 Conflict on checkout", "Another agent holds the issue",
     "Stop. 409 is terminal — do not retry."],
    ["422 'Only the escalated reviewer…'", "Execution policy escalation is active",
     "The escalated reviewer must advance the stage. This is the policy working, not a bug."],
    ["Routine fires at the wrong hour", "Trigger saved without an explicit IANA timezone",
     "Re-save the trigger with Asia/Singapore stated explicitly."],
    ["The approvals queue is not moving", "Approvals do not expire on their own — one is "
     "simply waiting for a human decision",
     "Open Approvals and decide. This is the documented cause of a stalled queue."],
    ["Workspace shows degraded or failed", "Provisioning or validation problem",
     "Read the workspace state and repair before blaming the agent."]])),
]

CHAPTERS  = PART_A + PART_B + PART_B2 + PART_C + PART_D
# Appendices are exported separately so the LG builder can place them AFTER Part G.
APPENDIX_CHAPTERS = APPENDICES
