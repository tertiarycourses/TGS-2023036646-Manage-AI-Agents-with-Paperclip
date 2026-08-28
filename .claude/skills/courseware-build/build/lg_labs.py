"""
Learner Guide lab walkthroughs — Manage AI Agents with Paperclip (TGS-2023036646).

Part E of the Learner Guide. One expanded walkthrough per lab, keyed to the six
lab definitions in data_domain1.py .. data_domain4.py. Every command and UI path
reproduced here is taken verbatim from those modules; nothing has been invented,
renamed or "improved". Every product fact — state names, thresholds, defaults,
type keys, error strings, ports — is taken from the official documentation at
https://docs.paperclip.ing/ (harvested 28 August 2026).

All company data in these labs is SYNTHETIC. The six simulated companies do not
exist; their ledgers, leads, candidates, watchlists and price histories were
fabricated for classroom use only.

The module exposes LAB_CHAPTERS: an ordered list of blocks in the LG builder's
own DSL, identical to lg_chapters.CHAPTERS:
    ("h1", text) ("h2", text) ("h3", text) ("p", text)
    ("bullets", [str, ...])
    ("code", text)
    ("note", text)
    ("table", (caption, [headers], [[row], ...]))
    ("rule",)
    ("check", [str, ...])
"""

# ══════════════════════════════════════════════════════════════════ Part E head
INTRO = [
 ("h1", "Part E — Lab Walkthroughs"),

 ("p", "Parts A to D told you how Paperclip works. Part E is where you make it work. "
       "Six labs run across the two days, each one simulating a different one-person "
       "company in a different sector, and each one adding exactly one layer of control "
       "to the layer you proved in the lab before. By the end of Lab 6 you will have "
       "built, governed, intervened in and audited a running agent company — and you will "
       "have the evidence files to prove each step, which is the part an assessor, a "
       "client or a regulator actually asks for."),

 ("p", "The labs are deliberately cumulative. Lab 1 proves the platform. Lab 2 creates a "
       "company, a mission and a CEO. Lab 3 turns one agent into an org chart. Lab 4 turns "
       "a mission into assigned work. Lab 5 puts that work on a schedule and tests every "
       "budget layer against it. Lab 6 governs the whole thing and closes the audit loop. "
       "Skipping a lab does not save time; it removes the foundation the next lab stands on."),

 ("note", "EVERY COMPANY, FIGURE AND PERSON IN THESE LABS IS SYNTHETIC. ClipReel Studio, "
          "BrightFunnel Marketing, Meridian Finance Desk, Ledgerly Accounting, NorthPoint "
          "Trading Research and TalentBridge People Ops are fictional businesses invented "
          "for this course. The ledgers, leads, candidates, symbols and price histories in "
          "labs/lab-0N-*/data/ are fabricated. None of it is real financial data, real "
          "market data or real applicant data, and none of it should be quoted outside the "
          "classroom."),

 ("h2", "How to read a lab walkthrough"),
 ("p", "Every one of the six sections that follow has the same eight parts, in the same "
       "order, so that you can navigate any of them the moment you know your way around "
       "the first."),
 ("table", ("The structure of every lab section in Part E",
   ["Section", "What it gives you"],
   [["Why this lab exists", "The real business problem the lab teaches, in the company's own "
     "commercial context. Read this before touching a keyboard."],
    ["The company", "The simulated business, its mission, its roles and the exact synthetic "
     "data files it works from."],
    ["Before you begin", "What must already be true — from earlier labs and from your own "
     "machine — before the first command will succeed."],
    ["Walkthrough", "Every step restated, then explained: why it comes in that position, "
     "what breaks if you skip it, and the exact command or UI path."],
    ["What good looks like", "The verification criterion expanded into what you should "
     "actually be able to see on screen and in your evidence file."],
    ["Common failures", "Each documented symptom expanded into cause, fix and prevention."],
    ["Going further", "The stretch challenge, with hints for learners who finish early."],
    ["Think about it", "The reflection question, discussed, with a model answer."]])),

 ("p", "Two habits will save you more time across the two days than any other advice in "
       "this guide. First, keep an evidence file open from the start of every lab and write "
       "into it as you go — reconstructing evidence afterwards is slower and less honest "
       "than recording it live. Second, when something fails, read the EARLIEST error in "
       "the output, not the last one. Later errors are usually consequences."),

 ("note", "Never record a credential. Your evidence files should contain versions, statuses, "
          "run IDs, issue IDs, paths, costs and decisions. They should never contain an API "
          "key, a token, a connection string, a cookie or the contents of an environment "
          "dump. This is not merely a classroom rule — an evidence pack that leaks a "
          "provider key is a security incident."),
]

# ══════════════════════════════════════════════════════════════════ Lab 1
LAB1 = [
 ("rule",),
 ("h2", "E1. Lab 1 — Install Paperclip and Prove the Control Plane (ClipReel Studio)"),

 ("p", "TOPIC 1 · Fundamentals of Agentic AI and Paperclip · approximately 45 minutes · "
       "maps to LO1: explain the control-plane / runtime boundary and verify a healthy "
       "local Paperclip installation with observable evidence."),

 ("h3", "Why this lab exists"),
 ("p", "Almost every difficult failure you will meet in the rest of this course looks the "
       "same from the outside. An agent does not wake. An artifact does not appear. A run "
       "shows a cost of zero. In each case there are at least four candidate causes — the "
       "platform, the adapter runtime, the configuration and the work itself — and if you "
       "have never established which of those was healthy and when, you will debug all four "
       "simultaneously and fix none of them. Lab 1 exists to remove the first candidate "
       "permanently, by producing a dated, recorded, clean baseline of the control plane "
       "before a single agent exists to blame."),
 ("p", "The commercial version of that argument is sharper. ClipReel Studio is a one-person "
       "short-video production company: the founder writes, films and edits vertical video "
       "for small local brands and publishes on their own channels as a showcase. The "
       "bottleneck is not filming — it is the research-and-scripting front half of the "
       "pipeline. That founder has perhaps two hours a week to spend on tooling. If they "
       "adopt an agent platform and then lose an evening to a failed installation they "
       "cannot characterise, they will abandon the platform, and they will be right to. A "
       "verified baseline is what converts \"it doesn't work\" into \"the control plane is "
       "fine, so the problem is downstream\", which is a five-minute conversation instead of "
       "an evening."),
 ("p", "There is a conceptual payload here too, and it is the single most important idea in "
       "the course. Paperclip manages the company; adapters run the agents. Paperclip is a "
       "Node.js server with a React interface and a PostgreSQL database. It never performs "
       "the reasoning and never sees a token of the model's thinking except as a cost figure "
       "and a run log. So a healthy Paperclip API tells you the control plane is up and says "
       "absolutely nothing about whether Claude Code, Codex, Gemini CLI or Cursor is "
       "installed, authenticated and reachable. Learners who do not internalise that "
       "boundary in Lab 1 spend Lab 2 trying to fix an adapter problem in the platform's "
       "settings screens."),

 ("h3", "The company"),
 ("p", "ClipReel Studio is a fictional one-person short-video production company operating "
       "from a home studio in Singapore. Its simulated mission is stated in three parts, "
       "because a mission that cannot be split this way cannot be verified afterwards:"),
 ("table", ("ClipReel Studio's synthetic mission, decomposed",
   ["Property", "Value"],
   [["Target", "8 short-form videos per month"],
    ["Metric", "Average watch-through rate"],
    ["Boundary", "At least 5%, blended across all three channels"]])),
 ("p", "The company publishes to three simulated channels — TikTok (4 videos per month, "
       "target watch-through 5.5%), Instagram Reels (2 per month, 5.0%) and YouTube Shorts "
       "(2 per month, 4.5%) — for a blended target of at least 5.0%. The simulated baseline "
       "for the quarter shows the shape of the problem: June published 6 videos at 4.1%, "
       "July 7 at 4.6%, August 8 at 4.9%. Volume has been solved; the rate has not. A small, "
       "persistent gap of that kind is exactly the sort of problem worth putting a "
       "repeatable process against rather than a one-off push."),
 ("p", "The simulated operating budget allocates SGD 220.00 per month, of which SGD 40.00 is "
       "the ceiling for AI agent runtime and tooling. That SGD 40.00 figure is the one that "
       "matters for this course: it is the outermost budget ring, and the brief is explicit "
       "that it is set before any agent is hired."),
 ("p", "ClipReel's agent company has three roles, which you do NOT create in Lab 1 — Lab 1 "
       "proves the control plane only — but which shape everything that follows:"),
 ("bullets", [
   "HEAD OF CONTENT (CEO) — owns the mission, decomposes it into work, and synthesises the "
   "final publishing plan. Reports to nobody. Never films, edits or publishes directly.",
   "TREND RESEARCHER — identifies emerging formats, sounds and hooks, and reports each with "
   "a stated confidence and a stated limitation. Reports to the Head of Content. Never "
   "writes scripts.",
   "SCRIPT WRITER — turns an accepted trend finding into a shootable script with a hook, a "
   "body and a call to action, sized to the target channel. Reports to the Head of Content. "
   "Never sources its own trends; it consumes the researcher's accepted artifact.",
 ]),
 ("p", "The lab's only data file is labs/lab-01-clipreel-studio/data/clipreel-company-brief.md, "
       "which contains the mission, the channel table, the quarterly baseline, the budget and "
       "the three role definitions. You copy it into your practice root in step 8 so that "
       "later labs have a realistic synthetic mission to work from."),

 ("h3", "Before you begin"),
 ("bullets", [
   "A NORMAL, NON-ADMINISTRATIVE SHELL. Close any elevated Administrator or root terminal "
   "before you start. The documentation is explicit: do not run onboarding with sudo or from "
   "a root shell, because the default setup starts embedded PostgreSQL and PostgreSQL "
   "refuses to run as an administrative user.",
   "Node.js 20 or later on the PATH, with npm/npx available, and access to the public npm "
   "registry at https://registry.npmjs.org.",
   "Permission to create a local practice folder and to download an npm package.",
   "A modern browser able to reach http://localhost:3100 on the same machine.",
   "Nothing from an earlier lab — this is the first lab, and everything that follows depends "
   "on it.",
 ]),
 ("note", "Two ports matter and they are easy to confuse. The Paperclip API and user "
          "interface listen on 3100. The embedded PostgreSQL listens on 54329. If you are "
          "checking whether something is running, check the right one."),

 ("h3", "Walkthrough"),

 ("h3", "Step 1 — Create the ClipReel practice root"),
 ("p", "Create the practice root with separate workspace and evidence folders, and keep this "
       "root for the whole course."),
 ("p", "The folder layout is not housekeeping; it is the first control you set. The three "
       "workspace subfolders correspond to the three ClipReel roles, and separate roots are "
       "what will later make a file change attributable to exactly one agent. The separate "
       "evidence folder keeps your record of what happened outside any workspace an agent "
       "can write to — which is precisely what you want if you are ever asked to show that "
       "the evidence was not produced by the thing being evidenced. Skip this step and you "
       "will find yourself in Lab 3 with three agents writing into one directory and no way "
       "to tell whose marker file is whose."),
 ("code", "mkdir -p paperclip-tgs/clipreel/workspace/{head-of-content,trend-researcher,script-writer} \\\n"
          "         paperclip-tgs/clipreel/evidence\ncd paperclip-tgs/clipreel"),

 ("h3", "Step 2 — Verify the runtime"),
 ("p", "Node.js must report major version 20 or later. Record both lines in your evidence "
       "note — a version mismatch is the single most common cause of a failed onboard."),
 ("p", "This check comes second, before anything is downloaded, because an unsupported Node "
       "version produces a failure that surfaces much later and much less clearly. Paperclip "
       "requires Node.js 20 or newer, and the CLI's own doctor command checks it explicitly. "
       "If you skip the check and onboarding fails halfway, you will be reading a stack "
       "trace from a partially initialised database instead of a one-line version mismatch. "
       "Record both the Node and npm versions: the npm version tells you which registry "
       "behaviour and lockfile format you are dealing with if step 3 misbehaves."),
 ("code", "node --version\nnpm --version"),

 ("h3", "Step 3 — Onboard Paperclip"),
 ("p", "Run the official onboarding command from a NORMAL user shell. The first run "
       "downloads Paperclip, writes the configuration, initialises the embedded PostgreSQL, "
       "starts the server and opens the browser. Do not prepend sudo."),
 ("p", "Onboarding is a single command that does five things at once, which is why it comes "
       "after the version check and before every other step. It writes the instance "
       "configuration to ~/.paperclip/instances/default/config.json, provisions the agent JWT "
       "secret, creates the local secrets master key, brings up the embedded database and "
       "starts the server. The explicit registry flag exists because a machine configured "
       "against a private or corporate npm registry will otherwise resolve the package "
       "somewhere unexpected and fail in a way that looks like a Paperclip problem."),
 ("p", "The sudo prohibition is worth stating twice. The embedded PostgreSQL will refuse to "
       "start under an administrative user, and the failure message points at the database "
       "rather than at your shell, so learners routinely spend ten minutes debugging "
       "PostgreSQL when the actual fix is to close the terminal and open a normal one."),
 ("code", "npx --registry https://registry.npmjs.org paperclipai onboard --yes"),
 ("note", "Back up ~/.paperclip/instances/default/secrets/master.key somewhere safe. It is a "
          "32-byte key and it encrypts every API key and secret stored in Paperclip. Lose it "
          "and you lose access to all of them."),

 ("h3", "Step 4 — Keep the server running"),
 ("p", "If onboarding is still attached to the terminal, leave it running and open a second "
       "terminal in the same folder. If you stopped it, start it again."),
 ("p", "This step exists because of a specific and very common learner error: pressing "
       "Ctrl-C to \"get the prompt back\", which stops the server, and then concluding from "
       "the resulting connection refused that the installation failed. The server is a "
       "long-running process. Give it its own terminal and do the rest of the lab in a "
       "second one. The run command is idempotent in the sense that matters here — if a "
       "valid configuration already exists it reuses it rather than re-onboarding."),
 ("code", "npx paperclipai run"),
 ("note", "If the instance is already active under a background service manager, run will "
          "refuse to start rather than launch a second server. Two servers sharing one port "
          "and one database is not a state you want, and the refusal is the tool protecting "
          "you from it."),

 ("h3", "Step 5 — Run the built-in diagnostic"),
 ("p", "Run doctor and fix the EARLIEST reported dependency or configuration error before "
       "continuing — never change several settings at once."),
 ("p", "Doctor is the platform's self-assessment, and running it before you touch the "
       "browser is deliberate. It checks configuration validity, deployment and auth mode "
       "compatibility, the agent JWT secret, the secrets adapter, storage, database "
       "connectivity, the LLM provider, the log directory, the listen port, the Node.js "
       "runtime and the managed install and background service. Each of those is a "
       "prerequisite for something you will do later, so a doctor failure is a preview of a "
       "lab that is about to fail."),
 ("p", "The discipline of fixing only the earliest error matters more than it sounds. These "
       "checks are ordered, and later failures are frequently consequences of earlier ones — "
       "a database check fails because the configuration check failed, which failed because "
       "the data directory was not writable. Change one thing, re-run, re-read. Changing "
       "three settings at once and getting a pass tells you nothing about which change "
       "mattered, and you will need to know that the next time it breaks."),
 ("code", "npx paperclipai doctor"),

 ("h3", "Step 6 — Prove the health endpoint"),
 ("p", "Query the health endpoint and confirm it reports an ok status. This is the control "
       "plane answering for itself."),
 ("p", "This is the heart of the lab. Doctor is the CLI's opinion of the installation; "
       "/api/health is the running server's own answer, over the same HTTP surface every "
       "agent and every integration will later use. The documentation describes it as the "
       "fastest way to check whether the server is up and whether the database is reachable, "
       "and it returns runtime metadata including deployment mode, auth readiness and "
       "feature flags. Proving it now means that for the rest of the course you can "
       "distinguish \"the platform is down\" from \"the platform is fine and something "
       "downstream is wrong\" with a single command."),
 ("p", "Note what this does NOT prove. It says nothing about whether any agent runtime is "
       "installed or authenticated, because runtimes are separate processes reached through "
       "adapters and living entirely outside the control plane. Hold that thought — it is "
       "the reflection question at the end of this lab."),
 ("code", "# macOS / Linux\ncurl -sS http://localhost:3100/api/health\n\n"
          "# Windows PowerShell\nInvoke-RestMethod -Uri 'http://localhost:3100/api/health' | ConvertTo-Json -Depth 8"),

 ("h3", "Step 7 — Load the dashboard"),
 ("p", "Open the dashboard in a browser and confirm the Paperclip start or onboarding screen "
       "loads without a connection error. Do NOT create the company yet — that is Lab 2."),
 ("p", "The browser check is a third, independent confirmation, and it exercises a different "
       "path from the two before it: the static user interface and the browser's own network "
       "stack. A machine where curl succeeds and the browser fails is telling you something "
       "specific about proxies or host resolution rather than about Paperclip. The "
       "instruction not to create a company yet is not fussiness — Lab 2 asks for an exact "
       "company name and an exact mission string so that your evidence matches the marking "
       "guide, and a company created early with the wrong name has to be removed."),
 ("code", "http://localhost:3100"),

 ("h3", "Step 8 — Copy the ClipReel brief into the practice root"),
 ("p", "Copy the mock brief so later labs have a realistic, synthetic mission to work from."),
 ("p", "The brief is copied at the end rather than the beginning for a reason the brief "
       "itself states: the mission comes first, the control plane is proved second, and only "
       "then is anybody hired. Having the brief in the practice root also means the mission, "
       "the channel targets and the three role definitions travel with the instance rather "
       "than living in a course folder you may not have open in a later lab."),
 ("code", "cp labs/lab-01-clipreel-studio/data/clipreel-company-brief.md ./"),

 ("h3", "Step 9 — Write the evidence note"),
 ("p", "Record the date, Node and npm versions, the Paperclip version if shown, the doctor "
       "summary, the health status and the dashboard URL. Do NOT copy environment values, "
       "connection strings, cookies, tokens or provider keys."),
 ("p", "The evidence note is the deliverable, not a courtesy. It is what converts a "
       "successful installation into a durable claim you can make tomorrow, and it is what "
       "an assessor marks. Write it while the outputs are still on screen; reconstructing "
       "versions from memory is how wrong numbers enter a record."),
 ("p", "The redaction rule is absolute and it is a habit worth forming here, in the lab where "
       "it costs nothing, rather than in Lab 6 where an evidence pack is a governance "
       "artifact. Paperclip prints board tokens (prefix pcp_board_) and agent API keys once "
       "at creation and never again, precisely because they are secrets; an evidence file "
       "that contains one has turned a training record into a credential store."),
 ("code", "evidence/lab01-installation.md"),

 ("h3", "What good looks like"),
 ("p", "You have passed Lab 1 when four things are simultaneously true, and you can show "
       "each of them:"),
 ("bullets", [
   "npx paperclipai doctor completes with NO unresolved blocking error. Warnings you have "
   "read and understood are acceptable; an unread blocking error is not.",
   "GET http://localhost:3100/api/health returns a status of ok, from the same machine, over "
   "HTTP, with the server running in another terminal.",
   "The browser loads the Paperclip user interface at http://localhost:3100 without a "
   "connection error — the start or onboarding screen, with no company created.",
   "evidence/lab01-installation.md records all three checks, dated, and contains no "
   "credential, connection string or personal identifier.",
 ]),
 ("p", "A useful additional signal: you should be able to state, in one sentence and without "
       "looking it up, what your evidence file does NOT prove. If you can say \"it proves the "
       "control plane is healthy and says nothing about any agent runtime\", you have the "
       "concept as well as the artifact."),

 ("h3", "Common failures"),
 ("h3", "Embedded PostgreSQL refuses to start"),
 ("bullets", [
   "SYMPTOM — Onboarding aborts partway through with a database error, or doctor reports "
   "that database connectivity fails, and the message points at PostgreSQL rather than at "
   "your shell.",
   "WHY IT HAPPENS — The shell is elevated. The default setup starts embedded PostgreSQL, "
   "and PostgreSQL refuses to run as an administrative user. It can also happen when the "
   "practice directory is owned by a different user from the one running the command.",
   "HOW TO FIX — Confirm the shell is NOT elevated. Stop the process and re-run onboarding "
   "as the normal user who owns the practice folder.",
   "HOW TO AVOID — Close every Administrator or root terminal before you start the lab, and "
   "create the practice root as the same user who will run Paperclip.",
 ]),
 ("h3", "The browser cannot reach port 3100"),
 ("bullets", [
   "SYMPTOM — The dashboard shows a connection refused or a timeout, even though onboarding "
   "appeared to succeed.",
   "WHY IT HAPPENS — Most often the server is simply not running: the terminal that was "
   "hosting it was closed or interrupted. Less often the server is bound to a different "
   "interface, or something else already holds the port.",
   "HOW TO FIX — Run npx paperclipai doctor, then npx paperclipai run, and query /api/health "
   "again BEFORE touching any firewall setting.",
   "HOW TO AVOID — Give the server its own terminal and do everything else in a second one. "
   "Reaching for the firewall first is the classic time sink here: firewall rules rarely "
   "block loopback traffic, so a local connection failure is almost never a firewall problem.",
 ]),
 ("h3", "npx resolves against a private registry"),
 ("bullets", [
   "SYMPTOM — npx cannot find the package, downloads something unexpected, or fails with an "
   "authentication error from a host that is not registry.npmjs.org.",
   "WHY IT HAPPENS — The machine has a corporate or private npm registry configured "
   "globally, and npx honours it.",
   "HOW TO FIX — Retry with the explicit registry flag, then review the global npm registry "
   "configuration afterwards so the next command behaves predictably.",
   "HOW TO AVOID — Use the explicit registry form the lab gives you, which is why step 3 "
   "includes it by default rather than as a fallback.",
 ]),
 ("code", "npx --registry https://registry.npmjs.org paperclipai onboard --yes"),

 ("h3", "Going further"),
 ("p", "CHALLENGE — Run npx paperclipai env and record ONLY the non-sensitive instance name, "
       "bind mode and port in your evidence note. Do not paste the full output."),
 ("p", "HINT — The env command prints the environment variables a deployment needs, in two "
       "sections, Required and Optional, marking each as set, default or missing. The two "
       "required variables are PAPERCLIP_AGENT_JWT_SECRET and DATABASE_URL. That is exactly "
       "why the challenge tells you not to paste the output: one of those two is a signing "
       "secret and the other is a connection string, and both belong in your instance, not "
       "in your evidence file. The skill being examined is redaction under time pressure — "
       "reading a rich diagnostic output and extracting only the three facts that are safe "
       "to keep. If you find yourself wanting to paste \"just this one line\", that is the "
       "moment the habit is being formed."),

 ("h3", "Think about it"),
 ("p", "REFLECTION — Why does a healthy Paperclip API prove the control plane but say "
       "nothing about whether a Claude Code, Codex, Gemini or Cursor runtime is ready?"),
 ("p", "MODEL ANSWER — Because they are different processes with different failure modes, "
       "separated by a deliberate architectural boundary. Paperclip is the control plane: a "
       "Node.js server with a React interface over PostgreSQL that stores companies, agents, "
       "issues, budgets, approvals and run records, and decides WHEN an agent should wake and "
       "WHAT it is allowed to do. The reasoning itself happens in a separate runtime — Claude "
       "Code, Codex, Gemini CLI, Cursor and the rest — reached through an adapter. Those "
       "runtimes must be installed and authenticated OUTSIDE Paperclip; Paperclip cannot "
       "authenticate them for you. So /api/health returning ok tells you the server is "
       "listening and the database is reachable. It cannot tell you that the Claude Code "
       "binary exists on the PATH, that an ANTHROPIC_API_KEY is present and valid, or that "
       "the runtime has a working session. The only evidence that a runtime is genuinely "
       "connected is an artifact it produced in the workspace you expected — which is exactly "
       "the marker run you will build in Lab 3. A green badge on a configuration screen "
       "records that a value was saved; an artifact records that work was done."),
]

# ══════════════════════════════════════════════════════════════════ Lab 2
LAB2 = [
 ("rule",),
 ("h2", "E2. Lab 2 — Create the BrightFunnel Company, Mission and CEO (Digital Marketing)"),

 ("p", "TOPIC 2 · Building AI Agents with Paperclip · approximately 60 minutes · maps to "
       "LO2: create a goal-aligned Paperclip company with a measurable mission, a hardened "
       "CEO agent and enforced company-level caps."),

 ("h3", "Why this lab exists"),
 ("p", "A company in Paperclip is defined by the documentation as a self-contained AI "
       "organisation: one goal, a team of agents, a task board, a budget. Three of those four "
       "are created in this lab, and the ORDER in which you create them is the lesson. Most "
       "people, left alone with the interface, hire an agent first because that is the "
       "exciting part, then write a goal because a field asks for one, and set a budget last "
       "or never. That sequence produces a company that can spend before it has a ceiling and "
       "act before it has a direction. Lab 2 reverses it deliberately: mission, then cap, "
       "then hire."),
 ("p", "BrightFunnel Marketing makes the cost of getting this wrong concrete. It is a "
       "one-person digital marketing consultancy whose entire commercial proposition is cost "
       "per qualified lead. Its simulated channel data shows the spread plainly: Referral "
       "produces qualified leads at SGD 13.30 each, Email Nurture at SGD 10.64, Organic "
       "Search at SGD 15.89 — while LinkedIn Ads costs SGD 58.28 per qualified lead and Meta "
       "Ads SGD 42.23. A consultant whose business is telling clients where their money "
       "leaks cannot credibly run an agent company with no ceiling on its own spend. The "
       "budget cap is not administration; it is the same discipline the company sells."),
 ("p", "The second thing this lab teaches is what a mission has to contain to be usable. The "
       "documentation warns that vague goals give agents nothing concrete to anchor their "
       "work to, and its own example replaces \"grow the business\" with a target, a metric "
       "and a timeframe. BrightFunnel's mission is written to the same standard: a target "
       "(30% increase), a metric (qualified inbound leads), a timeframe (one quarter) and a "
       "boundary (blended cost per qualified lead under SGD 45). Every one of those four "
       "parts is something you could later hold an agent's output against. \"Improve the "
       "funnel\" is not — and an agent will happily optimise it, very efficiently, in a "
       "direction you did not intend."),

 ("h3", "The company"),
 ("p", "BrightFunnel Marketing is a fictional one-person digital marketing company. Its "
       "synthetic mission, entered verbatim in step 2, is:"),
 ("code", "Increase qualified inbound leads by 30% in one quarter\n"
          "while keeping blended cost per qualified lead under SGD 45."),
 ("p", "The single agent role created in this lab is the MARKETING DIRECTOR, hired as CEO. "
       "It owns goal alignment, decomposition and final synthesis. In Paperclip's model the "
       "first agent you create is always the CEO — the documentation is blunt that there is "
       "no way around this and no point in trying to avoid it — and the CEO is the only "
       "agent with no manager. Every other agent, in this and every later lab, reports to "
       "exactly one manager."),
 ("p", "The lab works from two synthetic data files in labs/lab-02-brightfunnel-marketing/data/:"),
 ("table", ("BrightFunnel's synthetic data files",
   ["File", "Shape", "What it is for"],
   [["leads.csv", "Daily rows: date, channel, campaign, spend_sgd, leads, qualified_leads, "
     "covering July–August 2026", "The transaction-level record the Marketing Director "
     "reasons over. Roughly forty rows — small enough to check by hand, which is what makes "
     "it a teaching set."],
    ["channels.csv", "Six aggregated channel rows: channel, campaign, total_spend_sgd, "
     "total_leads, total_qualified_leads, cost_per_qualified_lead_sgd, qualification_rate_pct",
     "The summary view. Because it aggregates leads.csv, you can verify an agent's arithmetic "
     "against a second file rather than taking its word for a total."],
    ["brightfunnel-ceo-instructions.md", "A role-contract template with marked <...> "
     "sections", "The starting point for the CEO instruction file in step 5. Copy it; edit "
     "only where marked."]])),
 ("p", "The six simulated channels are Google Search (BF-SEM-Q3-Brand), Meta Ads "
       "(BF-SOC-Q3-Retarget), LinkedIn Ads (BF-LIN-Q3-SME-Owners), Organic Search "
       "(BF-SEO-Q3-Guides), Email Nurture (BF-EML-Q3-Reactivate) and Referral "
       "(BF-REF-Q3-Partners). Qualification rates range from 27.4% on Meta retargeting to "
       "63.2% on referral. Every figure is fabricated for the classroom and describes no "
       "real campaign."),

 ("h3", "Before you begin"),
 ("bullets", [
   "LAB 1 COMPLETE — Paperclip is running, doctor is clean, and /api/health reports ok. If "
   "any of those three is untrue, go back; every failure in this lab will otherwise have two "
   "candidate causes instead of one.",
   "ONE TRAINER-APPROVED AGENT RUNTIME installed and ALREADY AUTHENTICATED OUTSIDE "
   "Paperclip. This is the boundary from Lab 1 becoming a prerequisite: Paperclip cannot "
   "authenticate a runtime for you.",
   "The paperclip-tgs practice root retained, with its workspace/ and evidence/ folders.",
   "A text editor for writing the CEO role-contract instruction file.",
 ]),
 ("note", "You will need a provider API key for the adapter you choose — Anthropic keys begin "
          "sk-ant-, OpenAI keys begin sk-. Enter it in the agent's environment variables as "
          "the adapter requires, or store it as a secret and reference it. Do not put it in "
          "your evidence file, your instruction file, or any file inside a workspace."),

 ("h3", "Walkthrough"),

 ("h3", "Step 1 — Start company creation"),
 ("p", "Open the Paperclip dashboard and start company creation. Use the exact synthetic "
       "company name so your evidence matches the marking guide."),
 ("p", "The company is the outermost container in Paperclip's model and everything else — "
       "agents, issues, budgets, skills, secrets — is scoped inside it. That scoping is real "
       "isolation, not a label: skills are company-scoped and are never shared across "
       "companies, and an agent authenticated to one company cannot act in another. Creating "
       "the company first therefore establishes the boundary that every later object lives "
       "within. The company name itself is a label for reference only and does not affect "
       "agent functionality, but using the exact name given makes your evidence directly "
       "comparable against the marking guide, and it can be renamed later in company settings "
       "if you must."),
 ("code", "http://localhost:3100   →   Companies → New Company\nName: BrightFunnel Marketing"),

 ("h3", "Step 2 — Enter the measurable mission"),
 ("p", "A mission needs a target, a metric and a boundary — \"grow the funnel\" is not "
       "verifiable, this is."),
 ("p", "The goal is described in the documentation as the north star that every agent in the "
       "company can see, and it is the text the CEO reads first on its very first heartbeat "
       "before proposing any strategy. That is why it is entered now, at creation, rather "
       "than added later: the quality of the first strategy proposal is bounded by the "
       "quality of the goal it was derived from. A goal with no metric produces a strategy "
       "with no acceptance criteria, which produces issues no one can close honestly."),
 ("p", "Enter the mission as plain text exactly as given. It states a target (30%), a metric "
       "(qualified inbound leads), a timeframe (one quarter) and a boundary (blended cost per "
       "qualified lead under SGD 45). Keep the boundary — a mission with a target but no "
       "boundary is an instruction to buy the metric at any price, and in a marketing company "
       "that is precisely the failure mode."),
 ("code", "Increase qualified inbound leads by 30% in one quarter\n"
          "while keeping blended cost per qualified lead under SGD 45."),

 ("h3", "Step 3 — Set the company budget cap BEFORE hiring"),
 ("p", "This is the outermost ring of the layered budget model and it must exist first."),
 ("p", "Paperclip enforces budgets at three scopes — company monthly, per-agent monthly and "
       "project lifetime — and the documentation is emphatic that these are PARALLEL and "
       "simultaneous rather than nested. An agent can be paused by its own budget limit even "
       "while the company has remaining budget, and a project can be paused regardless of "
       "either. Setting the company cap first does not make the other two automatic; it makes "
       "the outermost ceiling exist before anything is able to spend against it."),
 ("p", "Enforcement is two-stage and the numbers are exact. At 80% utilisation Paperclip "
       "records a warning and the agent CONTINUES running. At 100% the agent is automatically "
       "paused with pauseReason set to budget, and no further heartbeats fire — the "
       "documented default is pauseOnExceed = true. The utilisation bar reads green below "
       "70%, yellow from 70 to 90%, red above 90%. Skip this step and the first agent you "
       "hire is a process with an API key and no ceiling."),
 ("code", "Company → Settings → Budget\nMonthly cap: SGD 40.00"),
 ("note", "Monthly budgets reset to zero on the 1st of each UTC month. Project budgets are "
          "lifetime and never reset. An auto-paused agent does not lose its work: tasks it "
          "had in progress remain assigned to it and resume when the agent is resumed."),

 ("h3", "Step 4 — Hire the CEO"),
 ("p", "The Marketing Director owns goal alignment, decomposition and final synthesis for "
       "BrightFunnel."),
 ("p", "This is the first agent, so Paperclip makes it the CEO automatically and the hire "
       "form gives it no Reports To field — the CEO reports to the board, meaning you. That "
       "single structural rule is what makes the org chart a tree rather than a graph: every "
       "agent reports to exactly one manager, and the CEO is the only agent with no manager. "
       "It matters operationally as well as conceptually, because Paperclip raises an Invalid "
       "Org Chain banner when a reporting chain is broken, and a broken chain blocks work "
       "assignment."),
 ("p", "Hiring after the cap, rather than before, means the agent exists inside a ceiling "
       "from its first second. Note also that hiring now does not start anything: heartbeat "
       "on interval is OFF by default, and the agent will sit in idle until something wakes "
       "it. That is the intended state at this point in the lab."),
 ("code", "Agents → Hire → Role: Marketing Director\nReports to: (none — top of org chart)"),

 ("h3", "Step 5 — Write the CEO instruction file"),
 ("p", "State PURPOSE, ALLOWED INPUTS, OUTPUT SCHEMA, EXCLUSIONS and ESCALATION — a role "
       "contract, not a personality."),
 ("p", "Instructions are how an agent knows what it is for. Paperclip's own recommended "
       "structure separates an operating manual (AGENTS.md, the default entry file) from "
       "persona and decision philosophy (SOUL.md), a per-heartbeat execution checklist "
       "(HEARTBEAT.md) and tool notes (TOOLS.md), and the guidance for the persona file is to "
       "keep it under about forty short lines and avoid generic advice. The template in "
       "data/brightfunnel-ceo-instructions.md follows the same philosophy in a single file "
       "appropriate to a one-agent company."),
 ("p", "The five sections are not stylistic. PURPOSE anchors the agent to the mission. "
       "ALLOWED INPUTS bounds what it may read, which is what stops a marketing agent "
       "wandering into a finance folder. OUTPUT SCHEMA is what makes acceptance possible at "
       "all — you cannot verify an artifact whose shape was never specified. EXCLUSIONS are "
       "the highest-value lines in the file, because they are the only place you say what "
       "must never happen. ESCALATION tells the agent what to do when it is stuck, which is "
       "the difference between a blocked issue with a stated blocker and an agent quietly "
       "inventing a way forward."),
 ("code", "workspace/marketing-director/INSTRUCTIONS.md\n"
          "(copy the template from data/brightfunnel-ceo-instructions.md)"),
 ("note", "Instruction changes take effect on the agent's NEXT heartbeat, not immediately. If "
          "you edit the file mid-run, the run in flight is still working from what it read "
          "when it woke."),

 ("h3", "Step 6 — Attach a dedicated workspace"),
 ("p", "Attach a dedicated workspace so the CEO's files and evidence stay confined to one "
       "root and every change is attributable."),
 ("p", "The working directory is the folder on your machine where the agent does its work. "
       "Confining it now, while there is only one agent, establishes the pattern you will "
       "depend on in Lab 3 where three agents must not write into one another's space. "
       "Attribution is the reason: if two agents share a root, a file appearing in it is "
       "evidence that SOMETHING ran, not that a particular agent ran. In Lab 3 you will prove "
       "each boundary with a marker run, and that proof is only meaningful if the roots are "
       "separate to begin with."),
 ("code", "Agent → Workspace → Path: ./workspace/marketing-director"),

 ("h3", "Step 7 — Select and verify the runtime adapter"),
 ("p", "Verification means Paperclip reports a successful connectivity check, not merely "
       "that a value was saved."),
 ("p", "The adapter is the connection between Paperclip and the AI system that actually runs "
       "your agent. The documented type keys are claude_local, codex_local, gemini_local, "
       "opencode_local, cursor, pi_local and hermes_local, plus process, http and "
       "openclaw_gateway — eleven in total, of which the last three are functional but shown "
       "as coming soon in the interface. Use whichever your trainer has approved for the "
       "room; the discipline is identical across all of them."),
 ("p", "Verification is a distinct action from saving, and the distinction is the point of "
       "the step. Saving records that a value exists in a field. Verifying asks Paperclip to "
       "attempt a real connectivity check against the runtime — which is the first moment the "
       "Lab 1 boundary is actually tested. If the runtime is not installed, or not "
       "authenticated outside Paperclip, this is where you find out, and no amount of "
       "re-typing the key inside Paperclip will fix it."),
 ("code", "Agent → Runtime → (trainer-approved adapter)\nClick Verify connection"),
 ("note", "Changing the adapter type resets the form to that adapter's defaults. If you "
          "switch adapters after configuring one, re-check every field rather than assuming "
          "your earlier values survived."),

 ("h3", "Step 8 — Set the CEO's individual agent budget"),
 ("p", "Set it BELOW the company cap so the inner ring always binds first."),
 ("p", "The per-agent budget is a separate policy from the company budget and both apply "
       "simultaneously. Setting the agent cap at SGD 15.00 against a company cap of SGD 40.00 "
       "means the agent stops first, which is what you want: a single misbehaving agent hits "
       "its own ceiling and pauses, while the company retains headroom for everything else. "
       "If the two caps were equal, the first agent to misbehave would consume the entire "
       "company's monthly ceiling before anything stopped it."),
 ("p", "For orientation, the documentation's own starting guidance is USD 30–50 per month for "
       "a CEO, USD 20–40 for a manager such as a CTO or CMO, and USD 10–25 for a worker "
       "agent, with an expectation of USD 5–20 to experiment and USD 20–100 per month for an "
       "active company. The classroom figures in this course are deliberately lower, in "
       "Singapore dollars, and sized so that a two-day course cannot run up a surprising "
       "bill."),
 ("code", "Agent → Budget → Monthly cap: SGD 15.00"),

 ("h3", "Step 9 — Import the mock lead and channel data"),
 ("p", "Import the BrightFunnel mock data so the company has realistic synthetic material to "
       "reason over."),
 ("p", "Copying the data into the CEO's workspace rather than pointing at the course folder "
       "keeps the ALLOWED INPUTS section of the instruction file honest: the agent may read "
       "what is inside its own root, and the material it needs is there. It also means the "
       "workspace is self-contained if you later inspect it with git, which is how Labs 3, 4 "
       "and 6 verify work."),
 ("code", "cp -r labs/lab-02-brightfunnel-marketing/data ./workspace/marketing-director/data"),

 ("h3", "Step 10 — Record the redacted configuration baseline"),
 ("p", "Record company name, mission, CEO role, adapter NAME only, both budget caps and the "
       "workspace path. Never record keys."),
 ("p", "This baseline is what you will compare against when something changes later, and it "
       "is the second half of the evidence discipline you started in Lab 1. Record the "
       "adapter NAME — that it is, say, claude_local — and never the key, the environment "
       "block or the connection details. Paperclip itself follows this convention: reads of "
       "an agent's configuration redact secrets, and the CLI's own configuration command is "
       "documented as safe to print and share precisely because it masks them."),
 ("code", "evidence/lab02-brightfunnel-baseline.md"),

 ("h3", "What good looks like"),
 ("bullets", [
   "BrightFunnel Marketing exists as a company, with the EXACT mission text — target, metric, "
   "timeframe and boundary all present and unedited.",
   "The Marketing Director is the SOLE top-level agent: no Reports To, no siblings, and the "
   "org view shows a single node.",
   "The adapter shows a SUCCESSFUL verification, not merely a saved value — you clicked "
   "Verify and Paperclip answered.",
   "The agent has a confined workspace at ./workspace/marketing-director and an instruction "
   "file with all five sections present.",
   "The agent cap (SGD 15.00) is strictly BELOW the company cap (SGD 40.00), and both are "
   "saved rather than merely typed.",
   "evidence/lab02-brightfunnel-baseline.md contains no key, token or connection string.",
 ]),
 ("p", "A good baseline note fits on one page and could be handed to a colleague who would "
       "then be able to rebuild the same company without asking you a question — except for "
       "the credential, which they must obtain themselves. If your note fails that test, it "
       "is either missing a fact or containing a secret."),

 ("h3", "Common failures"),
 ("h3", "The adapter verification fails"),
 ("bullets", [
   "SYMPTOM — Verify connection returns an error, or the agent later sits in error status "
   "with an adapter message in its run transcript.",
   "WHY IT HAPPENS — The underlying CLI runtime is not installed on this machine, or it is "
   "installed but not signed in. Paperclip reaches the runtime as a separate process; it "
   "does not hold your provider session for you.",
   "HOW TO FIX — Confirm the runtime is installed and authenticated OUTSIDE Paperclip first "
   "— run its own CLI directly and sign in — then re-verify. Paperclip cannot authenticate a "
   "runtime for you.",
   "HOW TO AVOID — Treat runtime authentication as a prerequisite of the lab, not a step "
   "within it. Verify the runtime works standalone before you open Paperclip at all.",
 ]),
 ("h3", "The mission field rejects the text"),
 ("bullets", [
   "SYMPTOM — The mission will not save, or saves with visible mangling.",
   "WHY IT HAPPENS — The text was pasted from a word processor, carrying smart quotes, "
   "non-breaking spaces or hard line breaks.",
   "HOW TO FIX — Remove smart quotes and line breaks; enter the mission as plain text.",
   "HOW TO AVOID — Type or paste through a plain-text editor. This matters beyond the form: "
   "a mission containing typographic quotes is a mission your later grep and diff checks "
   "will silently fail to match.",
 ]),
 ("h3", "The budget cap will not save"),
 ("bullets", [
   "SYMPTOM — The budget field rejects the value or reverts on save.",
   "WHY IT HAPPENS — The ordering was inverted: an agent cap was set against a company cap "
   "that is missing or smaller.",
   "HOW TO FIX — Set the company cap BEFORE the agent cap. An agent cap above a missing or "
   "smaller company cap is rejected.",
   "HOW TO AVOID — Follow the lab order exactly: mission, company cap, hire, agent cap. The "
   "order is the lesson, and this failure is the lesson enforcing itself.",
 ]),

 ("h3", "Going further"),
 ("p", "CHALLENGE — Rewrite the BrightFunnel mission so it would FAIL a feasibility scan, "
       "then state in one sentence exactly which property (target, metric or boundary) you "
       "removed."),
 ("p", "HINT — Do not write a bad mission at random; remove exactly one property and leave "
       "the rest intact, so the damage is attributable. Removing the TARGET gives you "
       "\"Increase qualified inbound leads while keeping blended cost per qualified lead "
       "under SGD 45\" — an agent can satisfy this by producing one extra lead. Removing the "
       "METRIC gives you \"Improve marketing performance in one quarter under SGD 45 per "
       "unit\" — nobody can say what was measured. Removing the BOUNDARY gives you \"Increase "
       "qualified inbound leads by 30% in one quarter\" — which reads well and is the most "
       "dangerous of the three, because it instructs the agent to buy the target at any "
       "price. Given that BrightFunnel's own data shows LinkedIn Ads at SGD 58.28 per "
       "qualified lead against Referral at SGD 13.30, an unbounded mission would rationally "
       "select the most expensive channel. Write the sentence naming which property you "
       "removed and what the agent could now legitimately do."),

 ("h3", "Think about it"),
 ("p", "REFLECTION — Why is setting the company budget cap before hiring the CEO a control "
       "decision rather than an administrative one?"),
 ("p", "MODEL ANSWER — Because the cap is the only mechanism that stops spend without a human "
       "being present, and an agent hired before the cap exists has a window in which nothing "
       "stops it. Paperclip's budget enforcement is automatic and two-stage: at 80% "
       "utilisation it records a warning and the agent keeps running, and at 100% it pauses "
       "the agent automatically with pauseReason set to budget so that no further heartbeats "
       "fire. That is a control in the governance sense — it acts on its own, at a defined "
       "threshold, whether or not anyone is watching. Sequencing therefore changes the risk "
       "profile, not just the paperwork: hire first and there is a period, however short, in "
       "which a misconfigured instruction file or a retry loop can spend against no ceiling, "
       "and an agent in a retry loop does not get tired. There is a second, subtler reason. "
       "The three budget scopes are parallel rather than nested — company monthly, agent "
       "monthly and project lifetime all enforce simultaneously, and an agent can be paused "
       "by its own limit while the company still has headroom. Establishing the outermost "
       "ceiling first makes that relationship visible from the beginning, so that when you "
       "set the agent cap at SGD 15.00 against a company cap of SGD 40.00 you are making a "
       "deliberate statement about which ring should bind first, rather than discovering the "
       "interaction the month you get a surprising bill."),
]

# ══════════════════════════════════════════════════════════════════ Lab 3
LAB3 = [
 ("rule",),
 ("h2", "E3. Lab 3 — Build the Meridian Reporting Tree and Validate Runtime Boundaries (Finance)"),

 ("p", "TOPIC 2 · Building AI Agents with Paperclip · approximately 75 minutes · maps to "
       "LO2: build a multi-agent reporting hierarchy with distinct, budgeted and confined "
       "workspaces, and prove each runtime boundary with a marker run."),

 ("h3", "Why this lab exists"),
 ("p", "Lab 2 produced a company with one agent, which is a prompting problem with extra "
       "steps. Lab 3 produces an organisation, and organisations have properties a single "
       "agent does not: a reporting line, divided responsibility, separate budgets and — the "
       "part everyone underestimates — separate places to work. This lab exists to teach that "
       "a list of agents is not an org chart, and that a configured connection is not a "
       "proven one."),
 ("p", "Meridian Finance Desk is the right sector for the lesson because finance is where "
       "attribution is not optional. Its mission is to produce a board-ready monthly "
       "financial pack within three working days of month end, with every figure traceable to "
       "a source ledger extract. Traceable is the operative word. If an FP&A figure and a "
       "treasury figure both appear in the pack and you cannot say which analyst produced "
       "which, the pack is not board-ready no matter how correct the arithmetic is. In a real "
       "finance function this is the difference between a review and an investigation. "
       "Separate workspaces, separate instruction files and separate budgets are what make "
       "that attribution structural rather than a matter of trust."),
 ("p", "The second and larger idea in this lab is the MARKER RUN. Configuration screens are "
       "generous: they will show you a saved value and a green indicator, and both are true "
       "statements about the database rather than about the world. A marker run is a "
       "deliberately trivial task whose only purpose is to produce one named artifact in one "
       "named place. It is the smallest possible experiment that distinguishes \"Paperclip "
       "believes this agent has a runtime and a workspace\" from \"this agent's runtime "
       "actually executed and actually wrote to the folder I expected\". Once you have run "
       "one, you will never again accept a badge as proof — and you will have a two-minute "
       "diagnostic for every adapter problem in Labs 4, 5 and 6."),

 ("h3", "The company"),
 ("p", "Meridian Finance Desk is a fictional finance function. Its synthetic mission, entered "
       "at company creation, is to produce a board-ready monthly financial pack within three "
       "working days of month end, with every figure traceable to a source ledger extract. "
       "Its company monthly cap is SGD 45.00."),
 ("p", "It has three agent roles, and unlike Lab 2 the shape of the tree matters as much as "
       "the roles themselves:"),
 ("table", ("The Meridian reporting tree",
   ["Role", "Reports to", "Monthly cap", "Owns"],
   [["Finance Lead (CEO)", "None — top of the org chart", "SGD 20.00",
     "Mission alignment, decomposition, final synthesis of the pack."],
    ["FP&A Analyst", "Finance Lead", "SGD 10.00",
     "Analysis against the trial balance; variance narrative."],
    ["Treasury Analyst", "Finance Lead", "SGD 10.00",
     "Cash and bank position against the statement extract."]])),
 ("p", "The three caps total SGD 40.00 against a company cap of SGD 45.00, which is the "
       "arithmetic the verification step checks. Note that this is a deliberate design "
       "choice rather than a platform rule: because the three budget scopes enforce in "
       "parallel, keeping the sum of agent caps below the company cap means the company "
       "ceiling is a genuine backstop rather than the first thing to bind."),
 ("p", "The synthetic ledger lives in labs/lab-03-meridian-finance/data/ledger/ and is copied "
       "to a shared read-only data folder so both specialists reason over identical source "
       "figures:"),
 ("table", ("Meridian's synthetic ledger extracts",
   ["File", "Shape", "Why it is shaped that way"],
   [["trial-balance-2026-09.csv", "account_code, account_name, ledger_balance_sgd — around "
     "twenty accounts", "The ledger side of every comparison. Includes cash accounts such as "
     "1010 Cash at Bank - DBS Operating and 1020 Cash at Bank - OCBC Reserve."],
    ["bank-statement-2026-09.csv", "date, description, type, amount_sgd, "
     "running_balance_sgd — around twenty-five movements from an opening balance",
     "The independent side. Because it carries a running balance, an agent's reconciliation "
     "can be checked without recomputing the whole month."],
    ["meridian-role-instructions/fpa-analyst.md", "A role contract with PURPOSE, allowed "
     "inputs, output schema, exclusions and escalation", "Copied to "
     "workspace/fpa-analyst/INSTRUCTIONS.md in step 5."],
    ["meridian-role-instructions/treasury-analyst.md", "The same structure for the treasury "
     "role", "Copied to workspace/treasury-analyst/INSTRUCTIONS.md. The two differ mainly in "
     "their EXCLUSIONS, which is the point."]])),
 ("note", "Every figure in these extracts is fabricated for the classroom. They are not real "
          "financial data and must never be treated as such, quoted outside the room, or "
          "reused in any real reporting."),

 ("h3", "Before you begin"),
 ("bullets", [
   "LAB 2 COMPLETE — BrightFunnel exists with a verified CEO adapter and layered caps saved. "
   "You should be able to create a company, enter a mission and set a cap without referring "
   "back to the instructions.",
   "GIT INSTALLED, with a local practice user.name and user.email configured, so each "
   "workspace can commit a baseline without contacting a remote.",
   "ABSOLUTE PATHS AVAILABLE for the three Meridian workspace roots. Relative paths that "
   "resolve differently depending on which terminal you are in are the most common cause of "
   "a misbound workspace.",
   "The same trainer-approved adapter may be reused for all three agents — this lab tests "
   "boundaries between agents, not between adapters.",
 ]),

 ("h3", "Walkthrough"),

 ("h3", "Step 1 — Create the Meridian company"),
 ("p", "Create the company with its measurable mission and a company budget cap, using the "
       "same order you proved in Lab 2."),
 ("p", "This step is deliberately a repetition. Lab 2 taught the order — mission, then cap, "
       "then hire — and repeating it here without the scaffolding is how it becomes a habit "
       "rather than a procedure you followed once. Note the mission's shape: \"within 3 "
       "working days of month end\" is the timeframe, \"board-ready monthly financial pack\" "
       "is the target and \"every figure traceable to a source ledger extract\" is the "
       "boundary. That last clause is what the whole lab then goes on to make structurally "
       "true."),
 ("code", "Companies → New Company\nName: Meridian Finance Desk\n"
          "Mission: Produce a board-ready monthly financial pack within 3 working days of\n"
          "month end, with every figure traceable to a source ledger extract.\n"
          "Company monthly cap: SGD 45.00"),

 ("h3", "Step 2 — Hire the tree, with reporting lines set explicitly"),
 ("p", "Hire the Finance Lead as CEO, then hire the two specialists AND set the reporting "
       "line explicitly. A flat list of agents is not an org chart."),
 ("p", "The Finance Lead must be hired first because the first agent in any company is "
       "always the CEO and has no Reports To field. The two analysts are then hired with "
       "Reports To pointing at the Finance Lead. Setting that field is not decoration: the "
       "reporting chain is what Paperclip uses for escalation, and it validates the chain "
       "actively. An agent whose manager is missing, terminated, or part of a loop triggers "
       "an Invalid Org Chain banner, and the documented impact is that it BLOCKS WORK "
       "ASSIGNMENT. Separately, an Escalation Path Paused banner appears when a paused agent "
       "sits anywhere up the reports-to chain, with escalations refused until you unpause the "
       "manager or change the assignment."),
 ("p", "This is why a flat list fails in practice rather than merely in principle. Three "
       "agents with no reporting lines will each accept work and none of them will have a "
       "functioning escalation path, so the first time one of them gets stuck, the blockage "
       "has nowhere to go."),
 ("code", "Agents → Hire\n  Finance Lead      (reports to: none)\n"
          "  FP&A Analyst      (reports to: Finance Lead)\n"
          "  Treasury Analyst  (reports to: Finance Lead)"),

 ("h3", "Step 3 — Create one workspace root per agent"),
 ("p", "Separate roots are what make a later diff attributable to exactly one role."),
 ("p", "This is the physical half of the org chart. The reporting line says who answers to "
       "whom; the workspace roots say where each of them may write. Create all three before "
       "binding any of them, so that step 7 is a straightforward mapping exercise rather than "
       "a sequence of create-and-bind operations in which it is easy to lose track of which "
       "path you actually typed."),
 ("code", "mkdir -p workspace/{finance-lead,fpa-analyst,treasury-analyst}"),

 ("h3", "Step 4 — Initialise Git and commit an empty baseline in each workspace"),
 ("p", "So that every later change is a readable diff against a known-clean state."),
 ("p", "This is the step that turns \"I think the agent wrote something\" into evidence. An "
       "empty baseline commit gives each workspace a defined zero point, so that git status "
       "afterwards reports exactly what a run produced and nothing else. Without it, the "
       "workspace already contains the instruction file and the copied data, and any status "
       "output is a mixture of things you put there and things the agent did — which is "
       "precisely the ambiguity the lab is trying to eliminate."),
 ("p", "Do this BEFORE the marker runs, not after. A baseline taken after a run cannot "
       "distinguish the run's output from the pre-existing state, and re-running to "
       "compensate wastes budget you have deliberately capped."),
 ("code", "for w in finance-lead fpa-analyst treasury-analyst; do \\\n"
          "  git -C workspace/$w init -q && \\\n"
          "  git -C workspace/$w commit -q --allow-empty -m 'baseline'; done"),

 ("h3", "Step 5 — Write a role instruction file for each specialist"),
 ("p", "State purpose, allowed inputs, output schema, exclusions and escalation. The "
       "exclusions matter most."),
 ("p", "Two agents with identical instructions are one agent running twice, at double the "
       "cost. What actually differentiates the FP&A Analyst from the Treasury Analyst is not "
       "their titles but their EXCLUSIONS — the explicit statements of what each must not do, "
       "which prevent them producing overlapping, contradictory analysis of the same numbers. "
       "Read both templates side by side before you copy them; the differences are the design."),
 ("p", "The escalation section earns its place here in a way it did not in a one-agent "
       "company. These specialists have a manager, so \"escalate to the Finance Lead\" is now "
       "a real instruction with a real destination, and the reporting line you set in step 2 "
       "is what makes it executable."),
 ("code", "workspace/fpa-analyst/INSTRUCTIONS.md\n"
          "workspace/treasury-analyst/INSTRUCTIONS.md\n"
          "(templates in data/ledger/meridian-role-instructions/)"),

 ("h3", "Step 6 — Load the ledger extracts into a shared read-only data folder"),
 ("p", "So both specialists reason over identical source figures."),
 ("p", "This is the one place in the lab where sharing is correct rather than dangerous. "
       "Workspaces are separated so that OUTPUTS are attributable; inputs are shared so that "
       "the two analyses are comparable. If each specialist held its own copy of the trial "
       "balance, a discrepancy between their outputs could be a difference in reasoning or a "
       "difference in the data, and you would have no way to tell which."),
 ("code", "cp -r labs/lab-03-meridian-finance/data/ledger ./data/ledger"),

 ("h3", "Step 7 — Bind each agent to its workspace, adapter and budget"),
 ("p", "Bind each agent to its own workspace path and its own adapter, then set an individual "
       "budget for each so the caps are layered company → agent."),
 ("p", "Three bindings per agent, done together so nothing is left half-configured. Use "
       "absolute paths or verify the relative ones resolve from the directory Paperclip "
       "actually runs in — a misbound workspace is the single most common failure in this "
       "lab and it is silent until the marker run exposes it. The individual budgets create "
       "the layering: SGD 20.00 for the lead, SGD 10.00 for each analyst, totalling SGD 40.00 "
       "against a SGD 45.00 company cap."),
 ("p", "Remember that these two scopes enforce in parallel. The Treasury Analyst hitting SGD "
       "10.00 pauses the Treasury Analyst and nothing else — the FP&A Analyst continues, the "
       "Finance Lead continues, and the company still has headroom. That is the behaviour the "
       "stretch challenge asks you to observe directly."),
 ("code", "Each agent → Workspace + Runtime + Budget\n"
          "  Finance Lead     SGD 20.00\n  FP&A Analyst     SGD 10.00\n"
          "  Treasury Analyst SGD 10.00"),

 ("h3", "Step 8 — Run a marker run for each agent"),
 ("p", "Assign a trivial task whose only output is a single named file. This is how you prove "
       "the runtime boundary is real."),
 ("p", "The task is deliberately as small as a task can be: create one file, containing one "
       "role name and one date, and do nothing else. Its triviality is the design. A marker "
       "run costs almost nothing, completes quickly, and produces an unambiguous binary "
       "result — the file is in the right root or it is not. A complex first task confounds "
       "three questions at once (did the runtime execute, did it write where I expected, did "
       "it do the work correctly) and gives you no clean answer to any of them."),
 ("p", "Note the mechanism as well as the purpose. Assignment is one of the five documented "
       "heartbeat triggers — schedule or interval, task assignment, comment mention, manual "
       "invoke via Run Heartbeat, and approval resolution — so assigning this issue is what "
       "wakes the agent. Creating an issue and leaving it unassigned wakes nobody, which is a "
       "property Lab 4 depends on entirely."),
 ("code", "Issues → New\nTitle: Marker run — <agent>\n"
          "Body: Create a file named marker.md in your workspace root containing only\n"
          "      your agent role name and the current date. Do nothing else."),

 ("h3", "Step 9 — Inspect each run and confirm the artifact landed correctly"),
 ("p", "Confirm the artifact landed in the CORRECT workspace — and nowhere else. A marker in "
       "the wrong root is a boundary failure, not a success."),
 ("p", "Check all three roots, not just the one you expect. The failure this catches is the "
       "one that looks like a success: a marker file exists, the run reports success, and it "
       "is in the wrong folder because two agents share a misbound path. Checking only the "
       "expected root would confirm the file exists and miss entirely that a second agent "
       "wrote it. Because you committed empty baselines in step 4, git status --short in each "
       "root shows exactly one untracked marker.md in exactly one place if the boundaries "
       "hold."),
 ("code", "git -C workspace/fpa-analyst status --short\n"
          "git -C workspace/treasury-analyst status --short\n"
          "git -C workspace/finance-lead status --short"),

 ("h3", "Step 10 — Record the evidence"),
 ("p", "Record the org chart, the three budgets, the three marker-run IDs and the three "
       "artifact paths in your evidence note."),
 ("p", "Run IDs are the key that connects everything else. Paperclip's run records hold the "
       "invocation source, the token counts and cost, the transcript with tool calls inline, "
       "the logs and the list of touched issues, and every issue state change made by an "
       "agent carries the run ID in the X-Paperclip-Run-Id header. Recording the ID now means "
       "that in Lab 6, when you reconstruct an entire operation from the activity log, you "
       "have the identifiers to join the record together."),
 ("code", "evidence/lab03-meridian-org.md"),

 ("h3", "What good looks like"),
 ("bullets", [
   "The org view shows a THREE-AGENT TREE with both analysts reporting to the Finance Lead — "
   "one root, two children, no orphans and no Invalid Org Chain banner.",
   "Each workspace contains exactly ONE marker.md, attributable to its own agent, and the "
   "other two roots contain none.",
   "Every agent has an individual cap, and the sum of the agent caps (SGD 40.00) does not "
   "exceed the company cap (SGD 45.00).",
   "Each marker run has a recorded run ID in your evidence note, alongside the artifact path "
   "it produced.",
 ]),
 ("p", "The strongest version of this evidence is three git status outputs, each showing one "
       "untracked file, plus three run IDs. That pairing — a platform record and an "
       "independent filesystem observation of the same event — is what makes the claim hard "
       "to dispute. Either alone is weaker: the run record could describe work that went "
       "somewhere unexpected, and the file could have been created by hand."),

 ("h3", "Common failures"),
 ("h3", "A marker file appears in the wrong workspace"),
 ("bullets", [
   "SYMPTOM — git status shows marker.md in a root belonging to a different agent, or the "
   "same root shows two markers.",
   "WHY IT HAPPENS — The agent's workspace path is misbound: typically a relative path that "
   "resolved from an unexpected directory, or a path copied from another agent and not "
   "edited.",
   "HOW TO FIX — Correct the path on the AGENT (not the company), delete the stray file, and "
   "re-run the marker.",
   "HOW TO AVOID — Use absolute paths, and bind all three agents in one sitting so you can "
   "read the three paths together and see the difference between them.",
 ]),
 ("h3", "A specialist never wakes"),
 ("bullets", [
   "SYMPTOM — The issue sits in todo, the agent stays idle, no run appears.",
   "WHY IT HAPPENS — Almost always the issue is not assigned. Creating an issue does not "
   "wake anyone; assignment is the trigger. Heartbeat on interval is off by default, so "
   "there is no timer to rescue you. Other causes: the agent is paused, or it has no budget "
   "headroom.",
   "HOW TO FIX — Confirm the issue is ASSIGNED to that agent. Then check the agent's adapter "
   "verification and its budget headroom.",
   "HOW TO AVOID — Learn the five triggers and check them in order — assignment, mention, "
   "manual invoke, schedule, approval resolution. Also remember the distinction between "
   "paused and heartbeat-off: an agent with heartbeats off still wakes on assignment, "
   "comment, routine and on demand, whereas a PAUSED agent wakes on nothing at all.",
 ]),
 ("h3", "Git reports the workspace is dirty before the marker run"),
 ("bullets", [
   "SYMPTOM — git status shows changes before you have assigned anything.",
   "WHY IT HAPPENS — Something was written outside a run: a hand edit, a stray copy, or an "
   "earlier run you had forgotten.",
   "HOW TO FIX — Reset to the baseline commit and re-run, so the diff means what you think "
   "it means.",
   "HOW TO AVOID — Commit the empty baseline AFTER copying instructions and data, and then "
   "do not touch the workspace by hand. Anything a human writes into an agent workspace "
   "becomes an unexplained gap in an audit trail — a point Lab 6 makes explicitly.",
 ]),

 ("h3", "Going further"),
 ("p", "CHALLENGE — Set the Treasury Analyst's cap to SGD 0.01, re-run its marker task, and "
       "record exactly where and how Paperclip reports the budget stop."),
 ("p", "HINT — You are inducing the 100% condition deliberately in the cheapest possible "
       "place. Look in three locations and compare what each tells you. On the AGENT, expect "
       "the status to become paused with pauseReason budget, since the documented default is "
       "pauseOnExceed = true. On the DASHBOARD, the agent status panel counts paused agents "
       "separately from active, running and error, and the paused definition covers agents "
       "stopped deliberately OR automatically at their budget limit. In COSTS, watch the "
       "utilisation bar cross the thresholds — green below 70%, yellow 70–90%, red above 90% "
       "— and note that 80% records a warning while the agent CONTINUES, and only 100% pauses "
       "it. Record which surface told you first and which told you most precisely; that is "
       "the operationally useful finding. Then note the recovery path: a hard stop at agent "
       "level creates a Budget Override approval, and you resume by raising the limit "
       "deliberately or resolving that approval. Restore the SGD 10.00 cap afterwards."),

 ("h3", "Think about it"),
 ("p", "REFLECTION — Why is a marker run stronger evidence of a working runtime than a green "
       "\"connection verified\" badge in the configuration screen?"),
 ("p", "MODEL ANSWER — Because they test different things, and only one of them tests the "
       "thing you actually care about. A verification badge records that Paperclip performed "
       "a connectivity check at a moment in time and the check passed. That is genuinely "
       "useful — it is how you catch a missing runtime or an unauthenticated session in Lab 2 "
       "— but it is a statement about reachability, not about execution. It does not "
       "establish that the adapter can spawn an agent process, that the process can complete "
       "a turn, that the working directory is bound to the folder you intended, or that the "
       "agent has permission to write there. A marker run tests the whole chain end to end: "
       "the heartbeat fires on assignment, the adapter is invoked, the agent process spawns, "
       "the agent calls back to the Paperclip API, work is performed, an artifact is written "
       "to disk and a run record is stored with a cost. If any link in that chain is broken, "
       "no marker.md appears — and if the workspace is misbound, the marker appears in the "
       "wrong place, which a badge could never have told you. There is also an evidential "
       "difference. The badge is Paperclip's own testimony about itself. The marker file is "
       "an independent observation you make with git, outside Paperclip, about the "
       "filesystem. Configuration that has never produced an artifact is not a connection; it "
       "is an intention."),
]

# ══════════════════════════════════════════════════════════════════ Lab 4
LAB4 = [
 ("rule",),
 ("h2", "E4. Lab 4 — Translate the Ledgerly Mission into Assigned Issues and Hand-Offs (Accounting)"),

 ("p", "TOPIC 3 · Developing Intelligent Multi-Agent Systems · approximately 90 minutes · "
       "maps to LO3: decompose a mission into a parent and specialist child issues, run the "
       "specialists sequentially and verify each hand-off against acceptance evidence."),

 ("h3", "Why this lab exists"),
 ("p", "Labs 2 and 3 built the organisation. Lab 4 gives it work, and it is where most of the "
       "genuinely hard judgement in the course lives. Decomposition — turning a mission into "
       "issues that an agent can actually complete and a human can actually verify — is the "
       "skill that separates a multi-agent company that produces evidence from one that "
       "produces confident prose. The platform will not do this for you. Paperclip enforces "
       "checkout, review stages and comment requirements, but it cannot tell you whether an "
       "acceptance criterion is checkable."),
 ("p", "Ledgerly Accounting exists to make that concrete in the least forgiving domain "
       "available. Its mission is to close the books each month with zero unexplained "
       "variances above SGD 500 and a complete reconciliation trail for every control "
       "account. A month-end close is inherently a decomposition problem with a hand-off in "
       "the middle: somebody reconciles, somebody else reviews the exceptions that the "
       "reconciliation surfaced, and a third party synthesises the pack. It is also a domain "
       "where \"reconciliation done\" is a meaningless status and \"here is the file listing "
       "every control account with its ledger balance, statement balance and variance\" is a "
       "deliverable. The lab's central discipline follows directly: write acceptance criteria "
       "that name the EVIDENCE, not the ACTIVITY."),
 ("p", "The second discipline is sequencing, and it rests on a mechanical fact you proved in "
       "Lab 3. Assignment is one of the five heartbeat triggers, so creating an issue "
       "unassigned wakes nobody, and assigning it is the deliberate act that starts work. "
       "Creating every issue unassigned therefore separates PLANNING from EXECUTION "
       "completely — you can build an entire issue tree, review its acceptance criteria, "
       "correct them, and only then spend money. Assigning one child at a time keeps each run "
       "individually attributable: two agents running concurrently produce interleaved run "
       "records and overlapping timestamps, and if the second one's output depends on the "
       "first one's artifact, you have also created a race."),

 ("h3", "The company"),
 ("p", "Ledgerly Accounting is a fictional accounting practice. Its synthetic mission is to "
       "close the books each month with zero unexplained variances above SGD 500 and a "
       "complete reconciliation trail for every control account. Its caps are layered: "
       "company SGD 45.00, CEO SGD 20.00, each specialist SGD 10.00, plus a PROJECT cap of "
       "SGD 25.00 introduced for the first time in this lab."),
 ("table", ("The Ledgerly roles",
   ["Role", "Reports to", "Cap", "Owns"],
   [["Practice Manager (CEO)", "None", "SGD 20.00", "The close pack synthesis; the parent "
     "issue, assigned only in a later lab."],
    ["Reconciliation Specialist", "Practice Manager", "SGD 10.00", "Child 1 — reconciling "
     "every control account against the statement extract."],
    ["Compliance Reviewer", "Practice Manager", "SGD 10.00", "Child 2 — reviewing every "
     "variance above SGD 500 and recommending a treatment."]])),
 ("p", "The synthetic close data lives in labs/lab-04-ledgerly-accounting/data/close/ and is "
       "built so that the hand-off has something real to hand over:"),
 ("table", ("Ledgerly's synthetic close extracts",
   ["File", "Shape", "Why it matters to the lab"],
   [["trial-balance-2026-10.csv", "account_code, account_name, ledger_balance_sgd — around "
     "nineteen accounts", "The ledger side. Runs from 1010 Cash at Bank - UOB Operating "
     "through to 3020 Retained Earnings."],
    ["bank-statement-2026-10.csv", "date, description, type, amount_sgd, running_balance_sgd "
     "— around thirty movements", "The independent statement side for the cash accounts."],
    ["control-accounts.csv", "account_code, account_name, ledger_balance_sgd, "
     "statement_balance_sgd, variance_sgd, source_document", "The file that makes the "
     "hand-off testable. It already contains the variances, so you can verify the "
     "specialist's arithmetic rather than trusting it."]])),
 ("p", "The control accounts file contains exactly four non-zero variances, and they are "
       "sized deliberately around the SGD 500 threshold in the mission — which is what gives "
       "the Compliance Reviewer a real filtering decision to make rather than a formality:"),
 ("table", ("The four synthetic variances, and what each tests",
   ["Account", "Variance (SGD)", "Source document", "What the reviewer must decide"],
   [["1100 Accounts Receivable - Trade", "1,242.65", "AR ageing 2026-10-31",
     "Above SGD 500 — must appear in the exceptions file with a cause and a treatment."],
    ["1210 GST Input Tax Receivable", "869.50", "IRAS GST F5 Q3",
     "Above SGD 500 — must appear."],
    ["2020 Accrued Expenses", "-2,124.90", "Accrual schedule",
     "Above SGD 500 in magnitude and NEGATIVE — tests whether the agent filters on absolute "
     "value or is caught by the sign."],
    ["2100 Deferred Revenue", "-637.25", "Contract schedule",
     "Above SGD 500 in magnitude and negative — the second sign test."]])),
 ("note", "Every figure in these extracts is fabricated. Ledgerly Accounting is not a real "
          "firm, the account balances are invented, and nothing here constitutes accounting "
          "guidance."),

 ("h3", "Before you begin"),
 ("bullets", [
   "LABS 2 AND 3 COMPLETE — you can create a company, hire a tree and set layered caps "
   "unaided. This lab does that in a single compressed step and does not re-teach it.",
   "THE MARKER-RUN TECHNIQUE proved for every adapter you intend to use. If a specialist "
   "fails in this lab, you want to already know its runtime works.",
   "GIT INSTALLED and each workspace committed to a clean baseline, so the specialists' "
   "output is readable as a diff.",
   "AT LEAST 30 MINUTES OF UNINTERRUPTED TIME — the two specialist runs must be SEQUENTIAL, "
   "and the whole point is lost if you start the second before the first has settled.",
 ]),

 ("h3", "Walkthrough"),

 ("h3", "Step 1 — Create Ledgerly and hire the three roles"),
 ("p", "Create the company, hire the Practice Manager as CEO plus a Reconciliation Specialist "
       "and a Compliance Reviewer, and set layered caps — the pattern you proved in Labs 2 "
       "and 3."),
 ("p", "Compressed into one step because you have now done it twice. The only new element is "
       "the mission's threshold: \"zero unexplained variances above SGD 500\" is a boundary "
       "with a number in it, and that number reappears in the child 2 acceptance criterion in "
       "step 6. A mission whose threshold cannot be traced into an acceptance criterion is a "
       "mission that will not be tested."),
 ("code", "Companies → New Company: Ledgerly Accounting\n"
          "Mission: Close the books each month with zero unexplained variances above SGD 500\n"
          "and a complete reconciliation trail for every control account.\n"
          "Company cap SGD 45 · CEO SGD 20 · each specialist SGD 10"),

 ("h3", "Step 2 — Create the project and give it its own budget cap"),
 ("p", "The project ring sits between the company and the agent, and it is what stops one "
       "project consuming the company."),
 ("p", "A project in Paperclip binds a body of work to a concrete place — a repository, a "
       "working directory, a budget envelope and a set of execution workspaces. The "
       "documentation's framing is worth keeping: if goals answer why are we doing this and "
       "issues answer what exactly needs doing, projects sit in between. Projects have their "
       "own status values — backlog, planned, in_progress, completed and cancelled — and "
       "their status communicates state without preventing agent work."),
 ("p", "The budget behaviour is the reason this step exists. A project budget's window is "
       "LIFETIME rather than monthly, its metric is billed_cents, its warn threshold defaults "
       "to 80%, and when hard stop is enabled, exceeding the cap pauses the PROJECT — "
       "surfaced as a red \"Paused by budget hard stop\" pill at the top of the project page. "
       "Crucially this is the third parallel scope, not a subdivision of the others: a "
       "project budget hit pauses the project regardless of agent headroom, an agent budget "
       "hit stops the agent regardless of project headroom, and the company budget is the "
       "overall ceiling. All three enforce simultaneously."),
 ("code", "Projects → New\nName: October Month-End Close\n"
          "Goal: Close October with every control account reconciled and evidenced.\n"
          "Project cap: SGD 25.00"),
 ("note", "Because project budgets are lifetime, they do not reset on the first of the month "
          "the way agent and company monthly budgets do. A long-running project accumulates "
          "against its cap indefinitely, which is exactly what you want from an envelope "
          "around a defined piece of work."),

 ("h3", "Step 3 — Load the close data"),
 ("p", "Load the mock trial balance and bank statement extracts into a shared read-only data "
       "folder."),
 ("p", "As in Lab 3, inputs are shared so that both specialists reason over identical "
       "figures, while outputs remain separated so they stay attributable. Here it does more "
       "work than in Lab 3, because child 2's job is to review variances that child 1 "
       "computed from this same data — if the two specialists were reading different copies, "
       "a disagreement between their outputs would be uninterpretable."),
 ("code", "cp -r labs/lab-04-ledgerly-accounting/data/close ./data/close"),

 ("h3", "Step 4 — Create the PARENT synthesis issue, unassigned"),
 ("p", "Its acceptance criterion names the artifact, its path and the fields it must contain."),
 ("p", "Leave the assignee EMPTY. This is the mechanical heart of the lab: assignment is a "
       "heartbeat trigger, so an unassigned issue wakes nobody and costs nothing. That lets "
       "you build the entire tree, read it back, and fix a badly worded criterion before a "
       "single agent has spent anything. Note also that a new issue defaults to status "
       "backlog and priority medium unless you say otherwise — backlog meaning the issue "
       "exists and has been identified but nobody is working on it yet."),
 ("p", "Read the acceptance criterion carefully, because it is the model for everything that "
       "follows. It names a PATH (workspace/practice-manager/close-pack.md), it says the file "
       "must EXIST, and it lists the FIELDS every row must contain: account, ledger balance, "
       "statement balance, variance, explanation. Someone who has never seen the work can "
       "check that. \"Produce a close pack\" cannot be checked by anybody."),
 ("code", "Issues → New  (Assignee: leave EMPTY)\n"
          "Title: Produce the October close pack\n"
          "Accept: workspace/practice-manager/close-pack.md exists and contains, for every\n"
          "control account: account, ledger balance, statement balance, variance, explanation."),

 ("h3", "Step 5 — Create the two CHILD issues, parented and unassigned"),
 ("p", "Both unassigned, each parented to the synthesis issue so goal lineage is explicit and "
       "traceable."),
 ("p", "Setting the parent is a first-class link, not a note in the description. Paperclip "
       "uses parentage structurally: when all of an issue's children reach a terminal state, "
       "the parent is woken with the reason issue_children_completed. That is a real "
       "mechanism you will rely on in Lab 6, and it only works if the relationship is "
       "recorded as a parent rather than described in prose. The same principle applies to "
       "dependencies — the documentation is explicit that \"A is blocked by B\" must be "
       "expressed as a first-class blockedByIssueIds link and not as a free-text comment, "
       "because a dependent expressed in prose never auto-wakes."),
 ("code", "Child 1 → Reconcile control accounts   (parent: Produce the October close pack)\n"
          "Child 2 → Review compliance exceptions (parent: Produce the October close pack)"),

 ("h3", "Step 6 — Write acceptance criteria that name the evidence"),
 ("p", "\"Reconciliation done\" is unverifiable; a named file with named fields is."),
 ("p", "This is the step the whole lab is built around, so give it the time. Each criterion "
       "names a path, states what must be in the file, and — for child 2 — carries the "
       "mission's SGD 500 threshold into the work itself. Read the two criteria against the "
       "synthetic data and notice that they are genuinely testable: control-accounts.csv "
       "contains nineteen accounts, so child 1's file should list nineteen; four variances "
       "exceed SGD 500 in magnitude, so child 2's file should contain four entries, two of "
       "them negative."),
 ("p", "That last detail is a deliberate trap worth pointing out to learners. Two of the four "
       "material variances are NEGATIVE — accrued expenses at −2,124.90 and deferred revenue "
       "at −637.25. An agent that filters on \"variance greater than 500\" rather than "
       "\"absolute variance greater than 500\" will silently produce a two-row exceptions "
       "file that looks perfectly reasonable. This is exactly why acceptance is checked "
       "against named evidence rather than against a claim of completion."),
 ("code", "Child 1 accept: workspace/reconciliation-specialist/reconciliation.md lists every\n"
          "  control account with ledger balance, statement balance and variance.\n"
          "Child 2 accept: workspace/compliance-reviewer/exceptions.md lists each variance\n"
          "  above SGD 500 with a stated cause and a recommended treatment."),

 ("h3", "Step 7 — Assign CHILD 1 only"),
 ("p", "Assignment is the trigger — this is the moment the Reconciliation Specialist wakes."),
 ("p", "One assignment, one agent, one run. Everything up to this point cost nothing; this is "
       "the first line item. Assigning only child 1 means that when you inspect the run "
       "afterwards you know with certainty which agent produced which artifact, and there is "
       "no possibility of the reviewer starting before the thing it reviews exists."),
 ("p", "Behind the scenes the agent follows the documented heartbeat protocol: it identifies "
       "itself, fetches its assignments, picks work, and CHECKS OUT the issue via the "
       "checkout endpoint with the X-Paperclip-Run-Id header — an atomic claim that moves the "
       "issue to in_progress and records the run that owns it. Only one agent can hold an "
       "issue in progress at a time. It is worth knowing that the correct claim is a checkout "
       "and never a status patch to in_progress, because a patch skips checkout, leaves the "
       "checkout run ID empty and is race-prone."),
 ("code", "Child 1 → Assignee: Reconciliation Specialist"),

 ("h3", "Step 8 — Wait for the heartbeat, with a bound"),
 ("p", "Inspect the run log rather than the issue status — an unbounded wait hides a failed "
       "adapter behind apparent patience."),
 ("p", "Bounding the wait is an operational discipline, not impatience. An issue sitting in "
       "todo looks identical whether the agent is thinking, the adapter has failed, the agent "
       "is paused or the budget is exhausted; the RUN LOG distinguishes them immediately. The "
       "run detail carries status and timing, token counts and cost, the invocation card, the "
       "full transcript with tool calls inline and the stdout/stderr logs. A live run streams "
       "its transcript, so you can watch progress rather than infer it."),
 ("p", "Ten minutes is a sensible bound for a task of this size. If nothing has happened by "
       "then, something is wrong, and the fastest diagnosis is the run log followed by the "
       "agent's status. Remember that an agent in error status will not fire new heartbeats "
       "until the underlying issue is resolved — the error does not fix itself."),
 ("code", "Runs → (latest)   ·   bound the wait to 10 minutes\n"
          "git -C workspace/reconciliation-specialist status --short"),

 ("h3", "Step 9 — Accept child 1 only on named evidence"),
 ("p", "Accept ONLY if the named artifact exists with the named fields. Record the run ID and "
       "the artifact path in a comment, then close the issue."),
 ("p", "Open the file and check it against the criterion. Does it list every control account, "
       "or only the interesting ones? Does each row carry a ledger balance, a statement "
       "balance and a variance? If a field is missing, the correct response is to fix the "
       "CRITERION and re-run, not to hand-edit the agent's artifact — an artifact you edited "
       "is no longer evidence of what the agent did."),
 ("p", "The comment is the durable record. Paperclip's execution policy makes commenting a "
       "runtime invariant for agents — every agent run must post a comment back to the issue, "
       "and if it does not, the run's issueCommentStatus becomes retry_queued and the agent "
       "is woken with the reason missing_issue_comment; if the comment is still absent it "
       "becomes retry_exhausted and the failure is recorded. Your own comment, naming the run "
       "ID and the artifact, holds you to the same standard the platform holds the agent to."),
 ("p", "Then set the status to done. Done is TERMINAL — issues do not move backwards, and the "
       "only route back from done or cancelled is an explicit reopen. Setting done also has "
       "documented side effects: it stamps completedAt, wakes any issue whose blockers are "
       "now fully resolved, and wakes the parent if all its children are terminal."),
 ("code", "Issue → Comment: run <run-id> produced reconciliation.md (<n> accounts)\n"
          "Issue → Status: Done"),

 ("h3", "Step 10 — Now assign CHILD 2"),
 ("p", "Running the specialists sequentially is what keeps each run individually attributable "
       "and each hand-off inspectable."),
 ("p", "Only now, with child 1 accepted and its artifact on disk, does the Compliance Reviewer "
       "have something to review. Assigning both children at the start would have created a "
       "race whose outcome depends on which adapter happened to be faster — and on a bad day "
       "the reviewer would produce a confident exceptions file derived from nothing at all."),
 ("code", "Child 2 → Assignee: Compliance Reviewer"),

 ("h3", "Step 11 — Verify the hand-off"),
 ("p", "Confirm the Compliance Reviewer consumed child 1's artifact without needing to ask the "
       "producer a question."),
 ("p", "This is the actual test of the design. A hand-off works when the receiving specialist "
       "can do its job from the artifact alone. If the reviewer had to ask the reconciler a "
       "question, the artifact was underspecified — which is a criterion problem, not an "
       "agent problem. The grep counts SGD mentions as a crude proxy for whether real figures "
       "were carried across, and the diff --stat shows the shape of what the reviewer "
       "actually wrote."),
 ("p", "Read the exceptions file properly as well as counting it. Four variances exceed SGD "
       "500 in magnitude; a file with two entries has almost certainly fallen into the "
       "negative-variance trap described in step 6, and that is a finding worth recording "
       "rather than quietly fixing."),
 ("code", "grep -c 'SGD' workspace/compliance-reviewer/exceptions.md\n"
          "git -C workspace/compliance-reviewer diff --stat HEAD"),

 ("h3", "Step 12 — Record the evidence chain"),
 ("p", "For each child: issue ID, run ID, artifact path, comment and final status — in one "
       "table."),
 ("p", "One row per child, five columns. This table is the direct ancestor of the "
       "mission-to-evidence audit map you build in Lab 6, and building it now, while the work "
       "is fresh, teaches the shape. Note the run timestamps too: non-overlapping start and "
       "finish times are your proof that the runs were genuinely sequential, which is one of "
       "the verification criteria."),
 ("code", "evidence/lab04-ledgerly-handoffs.md"),

 ("h3", "What good looks like"),
 ("bullets", [
   "The Ledgerly project shows a saved cap (SGD 25.00) ABOVE actual spend — the envelope "
   "held.",
   "The parent issue is STILL OPEN and STILL UNASSIGNED. Synthesis is Lab 6's job; a parent "
   "closed here means it was assigned early.",
   "Both children are DONE, each with a linked artifact and a recorded run ID in a comment.",
   "The two specialists ran SEQUENTIALLY — non-overlapping run timestamps, which you can "
   "read directly off the two run records.",
   "The exceptions file demonstrably REFERENCES the reconciliation figures rather than "
   "restating the source data independently.",
 ]),
 ("p", "The subtle marker of a good result is that someone else could audit it without you. "
       "Given your evidence table, a colleague should be able to open two issues, follow two "
       "run IDs, open two files and agree or disagree with your acceptance decision — without "
       "asking you a single question. If they would need to ask, a column is missing."),

 ("h3", "Common failures"),
 ("h3", "Both specialists wake at the same time"),
 ("bullets", [
   "SYMPTOM — Two runs appear with overlapping timestamps; the exceptions file references "
   "figures that do not exist yet, or is thin and generic.",
   "WHY IT HAPPENS — A child was assigned before the previous one was accepted. Assignment "
   "is the trigger, so two assignments means two wakes.",
   "HOW TO FIX — Pause the second agent, let the first run settle, then re-assign so the runs "
   "are sequential.",
   "HOW TO AVOID — Assign one child, accept it, and only then assign the next. Remember that "
   "pausing is the reversible control here: a paused agent wakes on nothing at all, whereas "
   "an agent with heartbeats merely off would still wake on the assignment you are trying to "
   "prevent.",
 ]),
 ("h3", "The child artifact exists but is missing fields"),
 ("bullets", [
   "SYMPTOM — reconciliation.md is present but omits the statement balance, or exceptions.md "
   "lists causes without treatments.",
   "WHY IT HAPPENS — The acceptance criterion was written as an activity, not as evidence. "
   "The agent completed the activity it was given.",
   "HOW TO FIX — Rewrite the criterion naming the required fields and re-run. Do NOT "
   "hand-edit the agent's artifact.",
   "HOW TO AVOID — Before assigning anything, read each criterion and ask: could a stranger "
   "hold this file next to this sentence and say yes or no? If not, it is not yet a criterion.",
 ]),
 ("h3", "The parent issue wakes unexpectedly"),
 ("bullets", [
   "SYMPTOM — The Practice Manager runs and produces a close pack while the children are "
   "still in progress.",
   "WHY IT HAPPENS — The parent was assigned during creation, so creating it woke the CEO.",
   "HOW TO FIX — Clear the assignee. The parent stays unassigned until both children are "
   "accepted, which is Lab 6's work.",
   "HOW TO AVOID — Create every issue with the assignee field empty, without exception, and "
   "treat assignment as a separate deliberate act. This is the habit the whole lab is built "
   "to instil.",
 ]),

 ("h3", "Going further"),
 ("p", "CHALLENGE — Add a third child issue whose acceptance criterion deliberately names an "
       "artifact the previous child never produces, and record precisely how the failure "
       "surfaces in the run log."),
 ("p", "HINT — You are manufacturing a dependency failure in a controlled way, so make the "
       "impossibility unambiguous: name a specific path that nothing in the tree writes, for "
       "example a summary the reconciler was never asked to produce. Then watch what the "
       "agent does when the input does not exist, because there are several possible "
       "behaviours and they are not equally good. Does it move the issue to BLOCKED with a "
       "stated blocker, which is the correct response and the one the documentation's own "
       "advice about first-class blocker links supports? Does it comment and stop? Or does it "
       "invent a plausible file and proceed, which is the failure mode you most want to be "
       "able to recognise? Record the exact status the issue reached, the comment text and "
       "the relevant lines from the run transcript. Note also whether the failure cost money "
       "— it almost certainly did, which is the practical argument for reviewing acceptance "
       "criteria BEFORE assigning rather than discovering their flaws through spend."),

 ("h3", "Think about it"),
 ("p", "REFLECTION — Why does creating every issue unassigned change the risk profile of a "
       "multi-agent company, compared with assigning at creation time?"),
 ("p", "MODEL ANSWER — Because it separates planning from execution, and in an agent company "
       "execution is irreversible and costs money. Assignment is one of the five documented "
       "heartbeat triggers, alongside schedule or interval, comment mention, manual invoke "
       "and approval resolution. Assigning at creation therefore fuses two decisions that "
       "should be distinct: deciding that work SHOULD exist, and deciding that it should "
       "START NOW. Once they are fused, every draft issue is a live instruction. A "
       "half-written acceptance criterion becomes a real run against a real budget, a "
       "mistakenly parented issue wakes an agent you did not intend to involve, and a tree "
       "you were still thinking about becomes a set of concurrent runs whose interleaved "
       "artifacts you must then untangle. Creating unassigned gives you a free planning "
       "phase: the whole tree can be built, read back, criticised and corrected at zero cost, "
       "because nothing has woken. It also makes sequencing possible at all, which is what "
       "keeps each run individually attributable and each hand-off inspectable — you cannot "
       "run specialists one at a time if creating their issues already started them. And it "
       "changes what happens when you are wrong. With unassigned creation, a bad criterion is "
       "an edit. With assignment at creation, a bad criterion is a completed run, a spent "
       "budget, an artifact you must not hand-edit, and an issue that may already have "
       "reached a terminal state from which the only route back is an explicit reopen."),
]

# ══════════════════════════════════════════════════════════════════ Lab 5
LAB5 = [
 ("rule",),
 ("h2", "E5. Lab 5 — Verify NorthPoint Routines and Layered Budget Controls (Stock Trading Research)"),

 ("p", "TOPIC 3 · Developing Intelligent Multi-Agent Systems · approximately 75 minutes · "
       "maps to LO3: test a scheduled routine and verify that every budget layer holds, using "
       "one bounded manual run before automation is allowed to own the schedule."),

 ("h3", "Why this lab exists"),
 ("p", "Everything you have built so far runs because you assigned something. Lab 5 "
       "introduces the first mechanism that runs because TIME PASSED, and that is a "
       "categorically different risk. A routine on a cron schedule will fire whether or not "
       "you are watching, whether or not last night's run succeeded, and whether or not the "
       "instruction you wrote at 5pm on Friday still makes sense on Monday morning. The "
       "single rule this lab teaches is therefore: automation earns the schedule only after a "
       "human has watched it succeed once."),
 ("p", "NorthPoint Trading Research is the right company for the lesson because it needs a "
       "genuinely recurring deliverable — a daily pre-market brief before the market opens — "
       "which is the archetypal routine. It is also the company where an unreviewed automated "
       "run does the most reputational damage, which is why the mission carries a hard "
       "boundary: the company produces research only and must never place or recommend a "
       "trade. That constraint is not decoration for a training scenario. It is the kind of "
       "boundary that in a real regulated context separates a research function from a "
       "regulated advisory activity, and an agent that quietly crosses it on an unattended "
       "6am run is a problem discovered by somebody else."),
 ("p", "The lab's second half is the payoff for everything you set up in Labs 2, 3 and 4. You "
       "now have three budget scopes in play at once — company monthly, project lifetime and "
       "agent monthly — and this is where you verify all three against ACTUAL recorded spend "
       "rather than against your intention. The documentation is explicit that the scopes are "
       "parallel and simultaneous rather than nested: an agent can be paused by its own limit "
       "while the company has remaining budget, and a project can be paused regardless of "
       "either. A control table with three rows and real numbers in it is how you turn that "
       "sentence into something you actually believe."),

 ("h3", "The company"),
 ("p", "NorthPoint Trading Research is a fictional research desk. Its synthetic mission is to "
       "deliver a daily pre-market research brief on a fixed synthetic watchlist by 07:30 "
       "SGT, with every claim sourced and every limitation stated. Its caps are company SGD "
       "40.00, CEO SGD 15.00 and SGD 10.00 for each analyst."),
 ("table", ("The NorthPoint roles",
   ["Role", "Reports to", "Cap", "Owns"],
   [["Research Director (CEO)", "None", "SGD 15.00", "Mission alignment; the research-only "
     "boundary."],
    ["Market Data Analyst", "Research Director", "SGD 10.00", "The daily pre-market brief "
     "produced by the routine."],
    ["Risk Reviewer", "Research Director", "SGD 10.00", "Reviewing that claims are sourced "
     "and limitations stated."]])),
 ("p", "The synthetic market data lives in labs/lab-05-northpoint-trading/data/market/ and "
       "every part of it is fabricated:"),
 ("table", ("NorthPoint's fabricated market data",
   ["File", "Shape", "Notes"],
   [["watchlist.csv", "symbol, company_name, sector, listing_board, currency, added_date, "
     "notes — eight symbols", "All invented: NPX.SI Northpoint Example Holdings, FKT.SI "
     "Fictional Kaya Toast Group, MOCK.SI Mockingbird Marine Engineering, SMPL.SI Sample "
     "Semiconductor Assembly, DUMY.SI Dummyfield Logistics Trust, TSTX.SI Testex Renewable "
     "Power, PLCB.SI Placebo Biosciences and ZZZQ.SI Zedzed Quantum Data Centres. These "
     "companies do not exist."],
    ["price-history.csv", "date, symbol, open, high, low, close, volume — around 160 rows",
     "Invented prices. Not a quote, not a price feed, not market data."],
    ["news-headlines.csv", "date, symbol, headline, tone, source_label — around sixteen rows",
     "Fabricated headlines attributed to fictional publications such as \"Fabricated Wire\" "
     "and \"Invented Daily\", so that a sourced claim is visibly sourced to something "
     "obviously unreal."]])),
 ("note", "THIS IS FABRICATED TRAINING DATA AND NOT MARKET DATA. The symbols, companies, "
          "prices and headlines were invented for this course. Nothing in this lab is a "
          "quote, a price feed or investment advice, and NorthPoint must never place or "
          "recommend a trade — including in any artifact an agent produces."),

 ("h3", "Before you begin"),
 ("bullets", [
   "LAB 4 COMPLETE — you have run a specialist to a named artifact and accepted it on "
   "evidence, and you have seen a project budget in use.",
   "THE HOST CLOCK AND TIMEZONE ARE CORRECT, and you can state the machine's IANA timezone. "
   "You will be reasoning about a schedule, and a machine whose clock you cannot describe "
   "makes that impossible.",
   "PERMISSION TO CREATE A ROUTINE BUT NOT TO LEAVE IT LIVE AFTER CLASS. Leaving a routine "
   "enabled on a training machine is unattended scheduled spend.",
   "AN UNDERSTANDING THAT THIS IS RESEARCH ONLY — the company never places or recommends a "
   "trade, and any artifact that does so is a failed run regardless of how well written it "
   "is.",
 ]),

 ("h3", "Walkthrough"),

 ("h3", "Step 1 — Create the NorthPoint company"),
 ("p", "Create the company with a Research Director CEO, a Market Data Analyst and a Risk "
       "Reviewer, with layered caps. Note the research-only boundary in the mission."),
 ("p", "Put the research-only constraint IN THE MISSION rather than only in an instruction "
       "file. The mission is the north star every agent in the company can see, and a "
       "boundary stated there is visible to every agent and every later hire, including any "
       "agent you did not personally configure. An exclusion that lives only in one agent's "
       "instruction file protects only that agent."),
 ("code", "Companies → New Company: NorthPoint Trading Research\n"
          "Mission: Deliver a daily pre-market research brief on a fixed synthetic watchlist\n"
          "by 07:30 SGT, with every claim sourced and every limitation stated.\n"
          "Company cap SGD 40 · CEO SGD 15 · each analyst SGD 10"),

 ("h3", "Step 2 — Load the synthetic watchlist and price history"),
 ("p", "This data is fabricated for training and must never be presented as market data."),
 ("p", "Loading the data before creating the routine matters because the routine's "
       "instruction will name this folder as its only permitted source. A routine that fires "
       "against a missing data directory produces either a failure or, worse, an agent that "
       "fills the gap from its own training data — which in a market-research context is "
       "exactly the fabrication risk the sourcing requirement exists to prevent."),
 ("code", "cp -r labs/lab-05-northpoint-trading/data/market ./data/market"),

 ("h3", "Step 3 — Create the routine, PAUSED"),
 ("p", "A routine that is live before it has ever succeeded is an unreviewed scheduled spend."),
 ("p", "A routine is a reusable job definition with a trigger attached, and its documented "
       "states are paused, draft, archived, succeeded, failed and running. Creating it paused "
       "means the definition exists and can be reviewed while nothing can fire. This mirrors "
       "the unassigned-issue discipline from Lab 4 exactly: build the thing, read it back, "
       "and only then let it act."),
 ("p", "The failure mode being prevented is specific and expensive. A routine created live "
       "with a five-minute cron and a broken instruction can fire hundreds of times "
       "overnight, each firing consuming budget, until an agent cap pauses it — at which "
       "point you have a paused agent, a large cost line and a night of failed runs to read "
       "through."),
 ("code", "Routines → New\nName: Daily pre-market readiness check\nState: PAUSED"),

 ("h3", "Step 4 — Add the schedule trigger explicitly, with the IANA timezone"),
 ("p", "An implicit timezone is a production incident waiting to happen."),
 ("p", "Routines support two trigger kinds — a schedule, expressed as a cron expression in "
       "your timezone, and a webhook, which is a signed URL callable from outside Paperclip. "
       "You are using a schedule. The expression 0 7 * * * means 07:00 every day, which gives "
       "the brief thirty minutes of headroom against the mission's 07:30 SGT commitment."),
 ("p", "State Asia/Singapore explicitly. A trigger saved without an explicit IANA timezone "
       "inherits whatever the host thinks it is, which is fine on your laptop and wrong the "
       "moment the instance moves to a server, a container or a colleague's machine. The "
       "resulting failure is the nastiest kind: the routine works, produces a correct brief, "
       "and delivers it an hour late every day."),
 ("p", "One product detail to know for the assessment: the interface shows hours in 12-hour "
       "format with AM/PM while the underlying cron is 24-hour, and MINUTES SNAP TO "
       "FIVE-MINUTE INCREMENTS. 0 7 * * * satisfies that rule, as does a half-past schedule; "
       "an expression asking for minute 7 does not."),
 ("code", "Trigger → Schedule\nCron: 0 7 * * *\nTimezone: Asia/Singapore"),
 ("note", "Routine defaults for concurrency and catch-up are \"coalesce if active, skip "
          "missed\": if a run is already active the new tick coalesces into a single queued "
          "follow-up, and windows missed while the instance was down are skipped rather than "
          "replayed. That default is the safe one — it is why a laptop closed overnight does "
          "not produce a burst of eight brief runs when you open it in the morning."),

 ("h3", "Step 5 — Write what the routine actually does"),
 ("p", "Name the artifact it must produce so the run is verifiable rather than merely "
       "successful."),
 ("p", "The body is an acceptance criterion in disguise, and it carries the same discipline "
       "as Lab 4's child issues: it names a path, restricts the sources, and states an "
       "exclusion. Restricting the agent to ./data/market ONLY is what makes the sourcing "
       "requirement enforceable — a brief citing anything else is citing something that "
       "cannot exist in this company. \"Do not recommend any trade\" is the research-only "
       "boundary restated at the point of work, which is where it will actually be read."),
 ("p", "\"State sources and limitations\" deserves its place too. A research brief that "
       "asserts a conclusion without saying what it could not establish is exactly the "
       "artifact that gets an analyst into trouble, and requiring a limitations line is a "
       "cheap structural defence against an agent's tendency to sound more certain than its "
       "inputs justify."),
 ("code", "Body: Produce workspace/market-data-analyst/premarket-brief.md summarising each\n"
          "watchlist symbol from ./data/market ONLY. State sources and limitations.\n"
          "Do not recommend any trade."),

 ("h3", "Step 6 — Run the routine once, manually, while it is still paused"),
 ("p", "Bound the wait. This is the human review that earns the schedule."),
 ("p", "This single manual run is the whole thesis of the lab. It tests the definition, the "
       "instruction, the agent binding and the cost — everything the schedule would exercise "
       "— with a human present to watch it. Running it while the routine remains paused is "
       "the point: you are testing the job, not enabling the automation."),
 ("p", "Bound the wait as you did in Lab 4, for the same reason. If nothing has happened in "
       "ten minutes, read the run log rather than waiting longer; patience is not a "
       "diagnostic."),
 ("code", "Routine → Run now   ·   bound the wait to 10 minutes"),

 ("h3", "Step 7 — Inspect the generated issue and the run"),
 ("p", "Confirm the routine created work correctly and that the named artifact exists."),
 ("p", "A routine does not do work directly; it hands the agent an issue to execute, which is "
       "the fourth of the documented ways an agent wakes — automation. So there are two "
       "things to inspect, not one. First the ISSUE the routine generated: does it carry the "
       "instruction you wrote, is it assigned to the agent you expected? Then the RUN: did it "
       "succeed, what did it cost, and what did the transcript show it doing?"),
 ("p", "One filtering behaviour worth knowing: routine-generated issues are excluded from the "
       "default issue listing unless you opt in, so if you cannot find the issue on the "
       "board, that is why rather than evidence that nothing was created."),
 ("p", "Then read the brief itself, and read it as a reviewer rather than as its author. Does "
       "every claim name a source from the synthetic data? Are limitations stated? And "
       "critically — does anything in it read as a trade recommendation? A brief that says a "
       "symbol \"looks attractive at these levels\" has crossed the boundary regardless of "
       "how carefully it was hedged elsewhere."),
 ("code", "Issues → (routine-generated issue)\nRuns → (latest)\n"
          "cat workspace/market-data-analyst/premarket-brief.md | head -30"),

 ("h3", "Step 8 — Read the recorded cost for that run"),
 ("p", "This actual figure is what you will compare every budget layer against."),
 ("p", "Up to now your budget work has been about setting caps. This is where a cap meets a "
       "number. The Costs view carries the headline tiles — inference spend with token count, "
       "budget utilisation with incident count, finance net, and finance events — and filters "
       "by agent. Take the figure for THIS run specifically, not the month's total, because "
       "the control table you are about to build is a statement about what one routine "
       "execution costs and therefore about what the schedule would cost per day."),
 ("p", "That extrapolation is the practical value. If one run costs a known amount and the "
       "routine would fire daily, you can compute the monthly cost of enabling the schedule "
       "and compare it against the analyst's SGD 10.00 cap before you enable anything. That "
       "is a decision you can defend."),
 ("code", "Costs → filter by agent: Market Data Analyst\nRecord the run cost"),

 ("h3", "Step 9 — Confirm the routine is STILL paused"),
 ("p", "Leaving it live is the most common mistake in this lab."),
 ("p", "This step exists because the mistake is so easy and so quiet. You ran the routine "
       "manually, it worked, you moved on to the budget table — and if the manual run "
       "enabled it, or you enabled it to test and forgot, the routine is now live on a daily "
       "07:00 trigger on a training machine that nobody will look at tomorrow. Check "
       "explicitly rather than assuming. The routine list shows the state badge and an "
       "Enabled toggle in its own column, so the check takes seconds."),
 ("code", "Routines → Daily pre-market readiness check → State: PAUSED"),
 ("note", "If you ever need to stop everything at once, the CLI can pause every non-archived "
          "routine in a company in a single command. Note that there is no single "
          "enable-all counterpart — re-enabling is per routine, deliberately."),

 ("h3", "Step 10 — Verify every budget layer against actual spend"),
 ("p", "Record the three-row control table: company, project and agent — each cap, each "
       "spend, each headroom."),
 ("p", "Three rows, because there are three parallel scopes and each can stop work "
       "independently. Fill in the actual figures rather than the intended ones. The exercise "
       "is only worth doing with real numbers, because the insight it produces is arithmetic: "
       "you can see which layer would bind FIRST if the routine ran daily for a month, and "
       "that is almost always the agent, which is exactly the design."),
 ("p", "While you are there, look at the utilisation bar's colour on each layer and connect it "
       "to the thresholds: green below 70%, yellow 70 to 90%, red above 90%, with a warning "
       "recorded at 80% and an automatic pause at 100%. Being able to read the state of a "
       "budget at a glance from a colour is a genuinely useful operational skill."),
 ("code", "evidence/lab05-northpoint-budgets.md\n"
          "| Layer | Cap | Spend | Headroom |"),

 ("h3", "Step 11 — Confirm the audit trail"),
 ("p", "The activity log must show the routine creation, the trigger addition, the manual run "
       "and the cost event as SEPARATE entries."),
 ("p", "This is a rehearsal for Lab 6, where you reconstruct an entire operation from the "
       "activity log alone. The test here is smaller but the principle is identical: four "
       "distinct actions should produce four distinct, ordered, readable entries. If they do, "
       "you can reconstruct what happened without your own notes. If an action you performed "
       "has left no trace, that is a gap, and gaps are findings rather than embarrassments — "
       "note it honestly."),
 ("code", "Activity → filter: NorthPoint Trading Research"),

 ("h3", "What good looks like"),
 ("bullets", [
   "The routine carries an EXPLICIT 0 7 * * * trigger with Asia/Singapore stated, not "
   "inherited.",
   "It has exactly ONE successful, reviewed manual run — not zero, and not several.",
   "It finishes the lab PAUSED. This is checked explicitly because it is the most commonly "
   "missed criterion in the whole course.",
   "The brief exists, cites ONLY the synthetic data, states its limitations, and contains NO "
   "trade recommendation of any kind.",
   "The control table shows all three budget layers — company, project and agent — above "
   "recorded spend, with real figures.",
 ]),
 ("p", "Read your own brief one final time with a single question in mind: if a compliance "
       "officer read this cold, would they conclude it was research or advice? That question "
       "is the actual deliverable of the NorthPoint scenario, and it is more important than "
       "the cron expression."),

 ("h3", "Common failures"),
 ("h3", "The routine fires unexpectedly"),
 ("bullets", [
   "SYMPTOM — Runs appear that you did not trigger; costs accumulate between sessions.",
   "WHY IT HAPPENS — The routine was left active after the manual run.",
   "HOW TO FIX — Pause it, then check the activity log for any additional runs and record "
   "them. Do NOT delete the evidence.",
   "HOW TO AVOID — Make step 9 a non-negotiable checkpoint. The instruction to record rather "
   "than delete unexpected runs is itself a governance lesson: an operator who tidies away "
   "inconvenient history has destroyed the audit trail they were supposed to be keeping.",
 ]),
 ("h3", "The cost shows as zero"),
 ("bullets", [
   "SYMPTOM — The run appears in the list but the recorded cost is zero, and the control "
   "table has nothing to compare against.",
   "WHY IT HAPPENS — The run probably failed before invoking the runtime, so no tokens were "
   "consumed. Zero cost is not evidence of efficiency; it is usually evidence that nothing "
   "happened.",
   "HOW TO FIX — Read the run log for an adapter error rather than assuming the work was "
   "free. Check whether the artifact actually exists — that is the independent test.",
   "HOW TO AVOID — Always pair a cost figure with an artifact check. Cost without an artifact "
   "is a failed run; an artifact without cost is a file somebody created by hand.",
 ]),
 ("h3", "The timezone reverts or the schedule fires an hour out"),
 ("bullets", [
   "SYMPTOM — The saved trigger loses its timezone, or the routine consistently fires at the "
   "wrong local hour.",
   "WHY IT HAPPENS — The trigger was saved without an explicit IANA timezone and inherited "
   "the host's.",
   "HOW TO FIX — Re-save the trigger with Asia/Singapore stated explicitly.",
   "HOW TO AVOID — Always state the IANA zone, never rely on the host, and remember that "
   "minutes snap to five-minute increments so a schedule you thought you set may have been "
   "adjusted.",
 ]),

 ("h3", "Going further"),
 ("p", "CHALLENGE — Lower the Market Data Analyst cap below the recorded run cost, run the "
       "routine once more, and record exactly which layer stops the run and where it is "
       "reported."),
 ("p", "HINT — This is the Lab 3 budget challenge again, but now with three layers live at "
       "once, so the interesting part is not THAT it stops but WHICH layer stops it. Set the "
       "analyst's cap just below the figure you recorded in step 8 and predict the answer "
       "before you run: the agent layer should bind first, because the company and project "
       "caps still have headroom. That prediction is the whole point — the scopes are "
       "parallel, not nested, so an agent can be paused by its own limit while the company "
       "has budget remaining. Then verify where each surface reports it: the agent's own "
       "status and pauseReason, the dashboard's paused count, and the Costs view's "
       "utilisation. Note whether a Budget Override approval was raised, since an agent-level "
       "hard stop creates one and it will sit in the queue until somebody acts — approvals do "
       "not expire on their own. Restore the cap afterwards and record both the stop and the "
       "recovery, because the recovery path is the half most people forget to document."),

 ("h3", "Think about it"),
 ("p", "REFLECTION — Why must a routine be proved by one bounded manual run before the "
       "schedule is allowed to own it?"),
 ("p", "MODEL ANSWER — Because a schedule removes the human from the loop, and everything a "
       "schedule automates it also automates the failure of. An unproven routine that is "
       "wrong is wrong repeatedly, unattended, and at a cadence you chose for convenience "
       "rather than for safety. The manual run is the cheapest possible test of every "
       "component the schedule depends on: the routine definition, the instruction body, the "
       "agent binding, the adapter, the data path, the artifact and the cost — all exercised "
       "once, with a person watching, before any of it is delegated to a clock. It also "
       "produces the one number you need to make the enabling decision responsibly. Knowing "
       "what a single run costs lets you multiply by the firing frequency and compare that "
       "against the agent's cap BEFORE you enable anything, rather than discovering the "
       "answer through an automatic pause at 100% utilisation. And there is a governance "
       "dimension beyond cost. In NorthPoint's case the routine produces a research brief "
       "under a hard constraint — the company must never place or recommend a trade — and the "
       "only way to know the instruction actually holds that line is to read one real output. "
       "A schedule enabled on an unread instruction is an organisation asserting that "
       "something will comply without ever having checked. Reviewing one run is what converts "
       "that assertion into evidence, and the review is precisely what earns the automation "
       "its schedule."),
]

# ══════════════════════════════════════════════════════════════════ Lab 6
LAB6 = [
 ("rule",),
 ("h2", "E6. Lab 6 — Run the Governed TalentBridge Operation and Close the Audit Loop (HR)"),

 ("p", "TOPIC 4 · Deploying and Managing AI Agents · approximately 90 minutes · maps to LO4: "
       "resolve issues and modify a running agent company through approvals, the operator "
       "intervention ladder and a reconstructed audit trail."),

 ("h3", "Why this lab exists"),
 ("p", "This is the highest-stakes simulation in the course and the only one where every "
       "control you have learned becomes mandatory rather than advisable. The reason is "
       "simple: hiring decisions affect real people. A marketing brief that is wrong wastes "
       "money. A reconciliation that is wrong is corrected next month. A shortlist that is "
       "wrong for the wrong reason denies someone a job, and does so in a way that may be "
       "unlawful, is certainly unfair, and is invisible unless somebody can reconstruct how "
       "the decision was made."),
 ("p", "That last clause is the lab. Everything before this point has produced artifacts; "
       "Lab 6 asks whether those artifacts constitute an AUDIT TRAIL — a record from which a "
       "third party could reconstruct what happened, in order, without asking you. You "
       "complete the sourcing-to-onboarding operation, but the operational work is almost "
       "incidental. The four things being examined are: reviewing a synthesis against a "
       "workspace DIFF rather than against the agent's own summary; processing a hire "
       "approval with a recorded rationale; applying the intervention ladder in order and "
       "against the least irreversible control that resolves the situation; and finally "
       "reconstructing the entire operation from the activity log alone."),
 ("p", "TalentBridge People Ops is a fictional HR function whose synthetic data has been "
       "designed to make one particular control testable. Its candidate file deliberately "
       "records NO protected characteristics — no age, date of birth, gender, race, "
       "ethnicity, religion, marital or family status, nationality, photograph or address — "
       "and states explicitly that if an agent asks for one of those fields, that is an "
       "escalation, not a data gap. This is a structural control rather than a policy "
       "aspiration: an agent cannot shortlist on a characteristic that does not exist in its "
       "inputs. Your job in step 6 is to verify that the structural control held all the way "
       "through to the final brief."),

 ("h3", "The company"),
 ("p", "TalentBridge People Ops is a fictional HR function covering sourcing, interviewing, "
       "policy and onboarding. Its synthetic mission is to fill each open role within 30 days "
       "with a fair, documented and auditable process from sourcing through to day-one "
       "onboarding. Caps are company SGD 45.00, CEO SGD 20.00 and SGD 10.00 for each "
       "specialist, plus SGD 5.00 for the disposable reviewer created later in the lab."),
 ("table", ("The TalentBridge roles",
   ["Role", "Reports to", "Cap", "Owns"],
   [["People Operations Lead (CEO)", "None", "SGD 20.00", "The synthesis — the hiring brief "
     "— and final accountability for fairness."],
    ["Talent Sourcer", "People Operations Lead", "SGD 10.00", "Child 1 — shortlisting "
     "candidates against the published rubric."],
    ["Policy & Onboarding Specialist", "People Operations Lead", "SGD 10.00", "Child 2 — the "
     "policy-compliant day-one onboarding plan."],
    ["Interview Reviewer (created via approval)", "People Operations Lead", "SGD 5.00",
     "Nothing of consequence. This is the DISPOSABLE role, created deliberately so the "
     "intervention ladder can be practised without destroying real work."]])),
 ("p", "The synthetic hiring data lives in labs/lab-06-talentbridge-hr/data/hiring/:"),
 ("table", ("TalentBridge's synthetic hiring data",
   ["File", "Shape", "What it is for"],
   [["candidates.csv", "candidate_id, pseudonym, years_experience, skills, source_channel, "
     "application_date — around eighteen pseudonymised candidates for one Support Engineer "
     "role", "The shortlisting input. Candidates are pseudonyms such as \"Candidate A-01\", "
     "and the file records NO protected characteristics by design."],
    ["interview-rubric.md", "The published assessment criteria for the Support Engineer role",
     "The only legitimate basis for a shortlisting reason. Every reason in the final brief "
     "must trace to this document."],
    ["hiring-policy.md", "A fair-hiring policy written in the spirit of the Singapore "
     "Tripartite Guidelines on Fair Employment Practices", "The governing document for both "
     "humans and agents in the process. It is a training artifact and NOT legal advice."],
    ["onboarding-checklist.md", "A day-one checklist owned by the Policy & Onboarding "
     "Specialist and approved by the People Operations Lead", "Child 2's reference "
     "document."]])),
 ("note", "Every candidate is fabricated and pseudonymised by design. Never substitute real "
          "applicant data into this lab. The hiring policy is a classroom artifact written in "
          "the spirit of the Tripartite Guidelines on Fair Employment Practices; it is not "
          "legal advice and must not be used as a real workplace policy."),

 ("h3", "Before you begin"),
 ("bullets", [
   "LABS 4 AND 5 COMPLETE — sequential children, bounded waits, and all three budget layers "
   "verified. This lab assumes all of it and re-teaches none of it.",
   "APPROVALS REACHABLE IN YOUR DEPLOYMENT. In a hosted instance the tool-action signing "
   "secret is documented as required, with no fallback, for TOOL-ACTION approvals.",
   "GIT INSTALLED, with clean workspace baselines, so the synthesis diff is readable. The "
   "diff is the central evidence of this lab and a dirty baseline destroys it.",
   "A WILLINGNESS TO TERMINATE ONLY the disposable role you deliberately create in this lab. "
   "Terminate is permanent.",
 ]),

 ("h3", "Walkthrough"),

 ("h3", "Step 1 — Create the TalentBridge company"),
 ("p", "Create the company with a People Operations Lead as CEO, a Talent Sourcer and a "
       "Policy & Onboarding Specialist, with layered caps."),
 ("p", "Note what the mission carries: \"fair, documented and auditable\" are three separate "
       "commitments, and each is tested later in the lab — fair in step 6, documented in step "
       "7, auditable in steps 11 and 12. A mission whose adjectives cannot each be traced to "
       "a check is decoration."),
 ("code", "Companies → New Company: TalentBridge People Ops\n"
          "Mission: Fill each open role within 30 days with a fair, documented and auditable\n"
          "process from sourcing through to day-one onboarding.\n"
          "Company cap SGD 45 · CEO SGD 20 · each specialist SGD 10"),

 ("h3", "Step 2 — Load the hiring data"),
 ("p", "Load the synthetic candidate pipeline, the interview rubric and the onboarding "
       "checklist. Every candidate record is fabricated — never use real applicant data."),
 ("p", "Loading all three together matters because they function as a set: the candidates are "
       "the input, the rubric is the only legitimate basis for a decision about them, and the "
       "policy governs both. An agent given candidates without a rubric will invent criteria, "
       "and invented criteria are precisely what the fairness check in step 6 is designed to "
       "catch."),
 ("code", "cp -r labs/lab-06-talentbridge-hr/data/hiring ./data/hiring"),

 ("h3", "Step 3 — Build the issue tree and run the specialists sequentially"),
 ("p", "An unassigned parent plus two children, then run the two specialists sequentially and "
       "accept each on named evidence — as in Lab 4."),
 ("p", "This is Lab 4's discipline applied without the scaffolding, which is the point: by "
       "now, creating unassigned and assigning one at a time should be automatic. The two "
       "children are genuinely independent — a shortlist and an onboarding plan do not depend "
       "on each other — but you still run them sequentially, because attributability is worth "
       "more here than the few minutes concurrency would save. In a hiring process, being able "
       "to say exactly which agent produced which artifact at which time is not a nicety."),
 ("code", "Parent (unassigned): Produce the Support Engineer hiring brief\n"
          "  Child 1 → Shortlist candidates against the rubric  (Talent Sourcer)\n"
          "  Child 2 → Draft policy-compliant onboarding plan   (Policy & Onboarding)"),

 ("h3", "Step 4 — Only after BOTH children are accepted, assign the parent"),
 ("p", "Assigning the parent early is what produces a synthesis of incomplete work."),
 ("p", "This is the moment Lab 4 was building towards and deliberately stopped short of. The "
       "parent has been sitting unassigned since it was created, which is why nothing has "
       "synthesised anything prematurely. Now that both children are terminal, assigning the "
       "parent wakes the People Operations Lead with both artifacts on disk to work from."),
 ("p", "Paperclip also has its own mechanism here: completing an issue wakes the parent when "
       "all of its children are terminal, with the reason issue_children_completed. Knowing "
       "that helps you interpret what you see — a parent that stirs on its own is the "
       "platform doing what it is designed to do, not a stray trigger. Bound the wait, as "
       "always."),
 ("code", "Parent → Assignee: People Operations Lead   ·   bound the wait to 10 minutes"),

 ("h3", "Step 5 — Review the synthesis against the workspace DIFF"),
 ("p", "Not against the agent's own summary. The diff is the strongest evidence you have."),
 ("p", "This is the single most important review technique in the course. An agent's summary "
       "is a description of the work produced by the same process that did the work, so it "
       "shares all of that process's blind spots. If the agent misread the rubric, the "
       "summary will confidently describe a correct application of a rubric it misread. The "
       "diff is different in kind: it is an observation of what changed on disk, made outside "
       "Paperclip by a tool with no interest in the outcome."),
 ("p", "Read it in two passes. The --stat view first, to see the SHAPE of the change: how "
       "many files were touched and how large the change is. A synthesis that touched six "
       "files when you expected one is telling you something before you have read a word. "
       "Then the full diff of the brief itself, to read the content as a reviewer. This "
       "two-pass habit catches the class of problem where the right file is correct and a "
       "second file you did not expect has also been written."),
 ("code", "git -C workspace/people-ops-lead diff HEAD --stat\n"
          "git -C workspace/people-ops-lead diff HEAD -- hiring-brief.md"),

 ("h3", "Step 6 — Confirm the fairness controls"),
 ("p", "Every shortlisting reason must trace to the published rubric, and no protected "
       "characteristic may appear as a criterion."),
 ("p", "The grep is a screen, not a proof, and understanding the difference matters. A clean "
       "grep tells you those specific words do not appear; it cannot tell you that no proxy "
       "for a protected characteristic was used. A criterion such as \"recent graduate\" "
       "contains none of the searched words and is an age proxy. So run the grep, and then "
       "read the brief properly with the rubric open beside it, asking of every shortlisting "
       "reason: which rubric line is this?"),
 ("p", "Interpret hits carefully too. The expectation is no CRITERIA hits — a brief that "
       "says \"candidates were assessed without regard to age, gender or nationality\" will "
       "match the pattern while being exactly the right sentence. What you are hunting is a "
       "protected characteristic used as a REASON. Remember also that the source data "
       "contains none of these fields, so any that appear were introduced by an agent rather "
       "than read from the file — which makes the finding both more serious and easier to "
       "trace."),
 ("code", "grep -nEi 'age|gender|race|religion|marital|nationality' \\\n"
          "  workspace/people-ops-lead/hiring-brief.md   # expect: no criteria hits"),

 ("h3", "Step 7 — Close the parent only after board sign-off"),
 ("p", "Record WHO approved and on what evidence. A close without a rationale is an unaudited "
       "decision."),
 ("p", "Naming the diff SHA in the comment is what makes the record durable. \"Approved\" tells "
       "a future reader that somebody was satisfied; \"approved by <name> on diff <sha>, "
       "rubric-traceable\" tells them who, on what exact state of the files, and against which "
       "standard — and lets them go and look at that same state themselves. That is the "
       "difference between a record and an assertion."),
 ("p", "Paperclip's own execution policy takes the same view for its formal review stages: "
       "both approvals and change requests REQUIRE a comment, empty bodies are rejected, and "
       "every decision is recorded with actor, outcome, comment and run ID. Your manual close "
       "should meet the standard the platform enforces on its agents."),
 ("code", "Issue → Comment: approved by <name> on diff <sha>, rubric-traceable\n"
          "Issue → Status: Done"),

 ("h3", "Step 8 — Process a bounded hire approval"),
 ("p", "Let the CEO propose one additional agent, then decide it yourself and record the "
       "rationale in the approval."),
 ("p", "Hiring is one of the two primary approval types in Paperclip — hire agent and CEO "
       "strategy — and the hire payload includes the proposed name, role, capabilities, "
       "adapter configuration, monthly budget and reporting line. There are exactly three "
       "responses available to you: APPROVE, in which case the agent is created, configured "
       "and queued to wake automatically; REJECT, in which case the requesting agent is "
       "notified and will not retry unless instructed; and REQUEST REVISION, which means you "
       "are not approving as-is but not saying no, and the agent will revise and resubmit."),
 ("p", "Two properties of the approvals system are worth holding on to. First, approvals do "
       "not expire on their own — an unattended queue is not a self-clearing problem, and any "
       "agent waiting on a pending approval simply pauses at that point until you act. That "
       "makes an unattended approvals queue one of the classic causes of a company that has "
       "gone mysteriously quiet. Second, approval resolution is itself one of the five "
       "heartbeat triggers, so your decision wakes the requester — deciding is an action with "
       "consequences, not merely a filing exercise."),
 ("p", "Record the rationale in one sentence. This is the same discipline as step 7 applied "
       "to a governance gate, and it is the sentence a reviewer will read first if the hire "
       "is ever questioned."),
 ("code", "Approvals → (pending hire proposal)\n"
          "Decide: Approve or Reject   ·   Rationale: <why, in one sentence>"),

 ("h3", "Step 9 — Confine the newly approved reviewer before it runs"),
 ("p", "Give it its OWN workspace and its own budget — a new hire inherits nothing by default."),
 ("p", "An approved hire is created and queued to wake automatically, which means the window "
       "between approval and first run is short. Confine it in that window. The two controls "
       "are the ones you have applied to every agent since Lab 2 — a dedicated workspace root "
       "so its output is attributable, and its own cap so it cannot consume the company's "
       "headroom — and the SGD 5.00 cap is deliberately small because this agent exists to be "
       "disposed of in the next step."),
 ("code", "Agent → Workspace: ./workspace/interview-reviewer\nAgent → Budget: SGD 5.00"),

 ("h3", "Step 10 — Practise the intervention ladder, on the disposable role only"),
 ("p", "In order: inspect → pause → reassign → terminate. Use the least irreversible control "
       "that resolves the situation."),
 ("p", "The ladder is ordered by reversibility, and each rung is a real, distinct capability "
       "the board holds without going through any approval. INSPECT costs nothing and changes "
       "nothing: read the runs, the transcript and the costs, because most situations that "
       "look like they need intervention turn out to need information. PAUSE is fully "
       "reversible, and the distinction from heartbeat-off matters — an agent with heartbeats "
       "off still wakes on assignment, comment, routine and on demand, whereas a PAUSED agent "
       "wakes on nothing at all. A paused agent also refuses new work outright: Paperclip "
       "answers an attempt to assign to one with \"Cannot assign work to a paused agent.\" "
       "REASSIGN moves the work rather than punishing the worker, which is usually what you "
       "actually wanted. TERMINATE is last and is permanent — it revokes the agent's API keys "
       "and hides it from lists and the org chart, though the record is preserved."),
 ("p", "Terminate and delete are different things and the documentation draws the line "
       "explicitly: terminating stops the agent permanently and PRESERVES it as a terminated "
       "record, whereas deletion is the destructive action. For an audit trail, that "
       "distinction is everything — a terminated agent still has a history you can read."),
 ("p", "One further consequence to notice: pausing an agent that has reports raises an "
       "Escalation Path Paused banner on the agents below it, because escalations up a paused "
       "chain are refused. That is why the ladder is practised on a leaf role with no reports, "
       "and it is a good illustration of why intervention on a manager is a heavier act than "
       "intervention on a worker."),
 ("code", "Agent → Inspect runs and costs\nAgent → Pause\n"
          "Issue → Reassign to People Operations Lead\nAgent → Terminate  (disposable role ONLY)"),
 ("note", "Terminate ONLY the Interview Reviewer you created in step 8 for this purpose. Do "
          "not practise the last rung on any agent that produced real work in this lab."),

 ("h3", "Step 11 — Reconstruct the operation from the activity log alone"),
 ("p", "Company creation, hires, issues, runs, costs, the approval and the interventions, in "
       "order."),
 ("p", "Close your notes and work only from the log. This is the actual test of whether the "
       "operation was auditable, and it is deliberately uncomfortable: you know what happened, "
       "so the temptation to fill gaps from memory is strong. Resist it. The question is not "
       "\"can I describe what happened\" but \"can the log describe what happened to someone "
       "who was not there\"."),
 ("p", "The activity feed records task status changes, comments, approvals, agent state "
       "changes and budget events across the whole company. Work through it in order and "
       "check that each of your major actions has an entry. Where you find a gap, note it "
       "rather than papering over it — a gap you have identified and explained is a much "
       "better artifact than a smooth narrative that quietly omits it."),
 ("code", "Activity → filter: TalentBridge People Ops → export or transcribe in order"),

 ("h3", "Step 12 — Write the mission-to-evidence audit map"),
 ("p", "One row per mission claim, linking the issue, the run, the artifact, the cost entry "
       "and the approval that evidences it."),
 ("p", "This is the deliverable of the whole course. Every previous evidence file was a "
       "record of one lab; this one starts from the MISSION and works forwards, asking of "
       "each claim the company makes about itself: where is the evidence? The mission promises "
       "a process that is fair, documented and auditable within thirty days, so each of those "
       "commitments needs a row, and each row needs five links that a stranger could follow."),
 ("p", "Building it in this direction, rather than by listing what you did, is what exposes "
       "the weaknesses. You will almost certainly find at least one claim whose evidence is "
       "thinner than the others — which is precisely what the reflection question asks you to "
       "identify, and identifying it honestly is the skill being assessed."),
 ("code", "evidence/lab06-talentbridge-audit-map.md\n"
          "| Mission claim | Issue | Run | Artifact | Cost | Approval |"),

 ("h3", "What good looks like"),
 ("bullets", [
   "The hiring brief is the ONLY later change in the People Operations Lead's workspace, and "
   "its diff passes both the rubric-traceability and the fairness checks.",
   "The approval carries a RECORDED RATIONALE — one sentence saying why, attached to the "
   "approval itself rather than remembered.",
   "The intervention ladder was applied to the DISPOSABLE ROLE ONLY, and IN ORDER: inspect, "
   "pause, reassign, terminate.",
   "The audit map reconstructs EVERY mission claim from activity-log entries with no gap — "
   "or with any gap explicitly noted and explained.",
 ]),
 ("p", "The strongest possible outcome here is not a perfect map. It is a map with one row "
       "that you have marked as weak, with a specific statement of what evidence would "
       "strengthen it. An operator who can identify the weakest link in their own audit trail "
       "is more trustworthy than one who claims there isn't one."),

 ("h3", "Common failures"),
 ("h3", "The CEO synthesises incomplete work"),
 ("bullets", [
   "SYMPTOM — The hiring brief references a shortlist or an onboarding plan that does not "
   "exist, or is vague where it should be specific.",
   "WHY IT HAPPENS — The parent was assigned before both children were accepted, so the "
   "synthesis ran against a partial set of artifacts.",
   "HOW TO FIX — Reopen the parent, accept the outstanding child on named evidence, then "
   "re-assign.",
   "HOW TO AVOID — Keep the parent unassigned until both children are terminal. Note that "
   "reopening a done issue requires an explicit reopen — done is terminal and a plain status "
   "change back to todo is rejected.",
 ]),
 ("h3", "The approval cannot be decided"),
 ("bullets", [
   "SYMPTOM — Approve and Reject do nothing, or the approval stays pending indefinitely.",
   "WHY IT HAPPENS — In a hosted deployment the tool-action signing secret is not "
   "configured. Note the docs tie this secret to tool-action approvals, not to the board "
   "approvals queue — an undecided board approval is simply waiting for a human.",
   "HOW TO FIX — Check PAPERCLIP_TOOL_ACTION_SIGNING_SECRET. It is required and has no "
   "fallback.",
   "HOW TO AVOID — Verify approvals are reachable as a prerequisite of the lab. Remember that "
   "a stuck approval is not a quiet problem: approvals never expire on their own, and any "
   "agent waiting on one pauses at that point until it is resolved.",
 ]),
 ("h3", "Terminate removes more than intended"),
 ("bullets", [
   "SYMPTOM — An agent you needed is gone from the list and the org chart, and its API keys "
   "no longer work.",
   "WHY IT HAPPENS — Terminate was used as a first response rather than a last one. It is "
   "the last rung of the ladder and it is not reversible.",
   "HOW TO FIX — There is no undo. Terminated agents are preserved as records rather than "
   "deleted, so their history survives, but the agent does not come back.",
   "HOW TO AVOID — Pause and reassign first. Only terminate the role you deliberately created "
   "as disposable. If you are unsure which rung to use, you are on the wrong rung — go down "
   "one.",
 ]),
 ("h3", "The activity log has a gap"),
 ("bullets", [
   "SYMPTOM — Something you know happened has no corresponding entry, so the reconstruction "
   "does not join up.",
   "WHY IT HAPPENS — Work was done outside a run: hand-edited in the workspace, or performed "
   "some other way that the platform never saw.",
   "HOW TO FIX — Note it honestly in the audit map. An unexplained gap is itself an audit "
   "finding.",
   "HOW TO AVOID — Never hand-edit an agent workspace. If an artifact is wrong, fix the "
   "acceptance criterion and re-run, so that the correction is itself recorded. Every "
   "shortcut you take by editing directly is a hole in the record you will later be asked to "
   "explain.",
 ]),

 ("h3", "Going further"),
 ("p", "CHALLENGE — Export the TalentBridge company, confirm the export scrubs secrets, then "
       "import it as a second company and record which identifiers Paperclip had to re-map on "
       "collision."),
 ("p", "HINT — Export is reachable from the org chart header or the Settings shortcut, and by "
       "default it includes company metadata, every non-terminated agent, every non-archived "
       "project and every issue. The tree is searchable and every entry has a checkbox, with "
       "the README and .paperclip.yaml regenerated on the fly to reflect your selection. Open "
       "the package before importing it and look specifically for anything that should not be "
       "there — that inspection IS the exercise."),
 ("p", "On import, the two controls to observe are the target dropdown (create a new company, "
       "which is the default, or apply to an existing one) and the COLLISION STRATEGY: rename "
       "on conflict, which is the default and proposes a new name such as gstack-CEO; skip on "
       "conflict, which keeps the existing item and drops the incoming copy; or replace "
       "existing. Use Preview import before applying, which produces three sections — the "
       "renames list, the adapters list where new agents default to the target company's "
       "CEO's adapter, and a file tree with a create, update, skip or replace badge on every "
       "row. Record which identifiers had to be re-mapped, because that answer tells you "
       "which parts of a company are globally unique and which are only unique within a "
       "company. One safety note worth knowing: incoming issues are always created as new, "
       "and the server blocks replace on an existing-company import, so this route is "
       "non-destructive by design. Avoid re-zipping the archive in Finder or Explorer — use "
       "the download from the export page."),

 ("h3", "Think about it"),
 ("p", "REFLECTION — Your audit map is the deliverable a regulator would actually ask for. "
       "Which single row in it is the weakest, and what evidence would strengthen it?"),
 ("p", "MODEL ANSWER — There is no single correct row, and the assessment is of the reasoning "
       "rather than the choice; but in most learners' maps the weakest row is the FAIRNESS "
       "claim, and it is worth understanding why. Every other row is evidenced by something "
       "that either exists or does not: an artifact is on disk or it is not, a run has an ID "
       "or it does not, a cost is recorded or it is zero, an approval carries a rationale or "
       "it is blank. Those are positive facts. Fairness is evidenced by an ABSENCE — that no "
       "protected characteristic was used as a criterion — and absence is much harder to "
       "prove. The grep in step 6 screens for six words in one file; it cannot detect a proxy "
       "such as \"recent graduate\" standing in for age, or \"local candidate preferred\" "
       "standing in for nationality, and it says nothing about the reasoning that led to the "
       "shortlist rather than the words that describe it. Several things would strengthen the "
       "row. A rubric-line citation against every shortlisting reason would convert the claim "
       "from an absence into a positive trace, since a reason that names a rubric line is "
       "evidenced by that line. An independent reviewer — a second agent or a human — "
       "checking the shortlist against the rubric without seeing the sourcer's reasoning would "
       "provide evidence produced independently of the thing being evidenced, which is exactly "
       "the property the fairness claim currently lacks. Paperclip's execution policy offers a "
       "structural version of this: a review stage with a named participant, where the "
       "decision is recorded with actor, outcome, comment and run ID, and where change "
       "requests bound the loop at maxReviewRounds, three by default. And the structural "
       "control already present in the data — a candidate file that records no protected "
       "characteristics at all — should be stated in the map as evidence in its own right, "
       "because a criterion that cannot be read from the inputs is much harder to apply than "
       "one that merely was not. The general lesson generalises well beyond hiring: claims "
       "evidenced by absence are always your weakest rows, and the fix is to convert them "
       "into claims evidenced by an independent, positive trace."),
]

# ══════════════════════════════════════════════════════════════════ Close
CLOSE = [
 ("rule",),
 ("h2", "E7. Across the six labs"),

 ("p", "The six labs are one argument delivered in six instalments, and it is worth stating "
       "the argument in one place now that you have executed it. Each lab added exactly one "
       "control, and each control was made real by an artifact rather than by a setting."),
 ("table", ("What each lab added, and what proved it",
   ["Lab", "Company", "The control it added", "The artifact that proved it"],
   [["1", "ClipReel Studio", "A verified control plane, separated conceptually from any "
     "agent runtime.", "A clean doctor run, an ok health response and a redacted evidence "
     "note."],
    ["2", "BrightFunnel Marketing", "A measurable mission and a company cap, both set BEFORE "
     "the first hire.", "A baseline note with the exact mission and two layered caps, and no "
     "credentials."],
    ["3", "Meridian Finance Desk", "A reporting tree with confined, individually budgeted "
     "workspaces.", "One marker.md per agent, in the correct root, with a recorded run ID."],
    ["4", "Ledgerly Accounting", "Decomposition into unassigned issues with evidence-based "
     "acceptance, run sequentially.", "Two accepted children with artifacts, comments and "
     "non-overlapping run timestamps."],
    ["5", "NorthPoint Trading Research", "A routine proved by one bounded manual run, and "
     "three parallel budget layers verified against real spend.", "A paused routine with an "
     "explicit trigger, one reviewed run, and a three-row control table."],
    ["6", "TalentBridge People Ops", "Governance: diff-based review, recorded approval "
     "rationales, the intervention ladder, and a closed audit loop.", "A mission-to-evidence "
     "audit map reconstructed from the activity log alone."]])),

 ("p", "Five habits recur in every lab, and they are what you should take back to work "
       "whether or not you ever use Paperclip specifically:"),
 ("bullets", [
   "ORDER IS A CONTROL. Mission before cap, cap before hire, create before assign, prove "
   "before schedule, children before parent. Every one of those orderings exists because the "
   "reverse creates a window in which something can go wrong unobserved.",
   "AN ARTIFACT BEATS A BADGE. A saved setting is a statement about a database. A file in the "
   "expected place, observed with a tool that has no stake in the outcome, is a statement "
   "about the world.",
   "ACCEPTANCE NAMES EVIDENCE, NOT ACTIVITY. If a stranger cannot hold the artifact next to "
   "your criterion and say yes or no, you do not yet have a criterion.",
   "THE LEAST IRREVERSIBLE CONTROL FIRST. Inspect before pause, pause before reassign, "
   "reassign before terminate. Reaching for the strongest tool first destroys the information "
   "you would need to know whether it was warranted.",
   "RECORD AS YOU GO, AND RECORD GAPS HONESTLY. An audit trail assembled afterwards is a "
   "reconstruction, and a reconstruction with no acknowledged gaps is usually a "
   "reconstruction that concealed one.",
 ]),

 ("check", [
   "Which lab proved the boundary between the control plane and the agent runtime, and what "
   "single artifact demonstrated it?",
   "State the exact order used in Lab 2 to create a company, and explain why reversing any "
   "two steps weakens a control.",
   "Why is a marker run stronger evidence than a verified-connection indicator?",
   "What is the difference between an acceptance criterion that names an activity and one "
   "that names evidence? Give an example of each from Lab 4.",
   "Name the three budget scopes, state whether they are nested or parallel, and give the two "
   "enforcement thresholds with what happens at each.",
   "List the five heartbeat triggers. Which of them does an unassigned issue fire?",
   "State the four rungs of the intervention ladder in order, and explain what distinguishes "
   "a paused agent from one with heartbeats turned off.",
   "In your Lab 6 audit map, which row is evidenced by an absence rather than by a positive "
   "trace, and how would you convert it?",
 ]),
]

LAB_CHAPTERS = INTRO + LAB1 + LAB2 + LAB3 + LAB4 + LAB5 + LAB6 + CLOSE
