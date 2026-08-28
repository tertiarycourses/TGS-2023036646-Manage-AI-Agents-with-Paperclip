"""
Learner Guide Part G — Command and API Reference.
Manage AI Agents with Paperclip (TGS-2023036646).

Every command, flag, endpoint, default and error string in this module is
reproduced from the official Paperclip documentation at https://docs.paperclip.ing/
(harvested 28 August 2026). Command syntax is reproduced EXACTLY as documented.
Where a command family is not documented in the harvested source, it is omitted
rather than guessed at.

The module exposes CLI_CHAPTERS: an ordered list of blocks in the LG builder's
own DSL:
    ("h1", text) ("h2", text) ("h3", text) ("p", text)
    ("bullets", [str, ...])
    ("code", text)
    ("note", text)
    ("table", (caption, [headers], [[row], ...]))
    ("rule",)
    ("check", [str, ...])
"""

# ══════════════════════════════════════════════════════════ Part G — opening

_G_INTRO = [
 ("h1", "Part G — Command and API Reference"),

 ("p", "This part is a reference, not a tutorial. It exists so that after the course you can "
       "find the exact command or endpoint you need without re-reading the narrative chapters "
       "or guessing at a flag. It is organised by SUBJECT — setup, authentication, company, "
       "project, issue, agent, run, routine, approval, cost, workspace, skills, secrets and "
       "then the REST API — and within each subject it follows the same shape: a short "
       "paragraph on what the command family is for, then the exact syntax, then the gotchas "
       "that cost people an afternoon."),
 ("p", "Two disciplines make it useful. First, treat the syntax blocks as literal: "
       "placeholders appear in angle brackets — <company-id>, <agent-id>, <issue-id> — and "
       "everything outside those brackets is typed as written. Second, remember what the CLI "
       "is. \"Agents do not run inside the CLI.\" Every command below is a control-plane "
       "call; the reasoning, the tool calls and the file writes all happen server-side in the "
       "runtime and its adapters."),
 ("note", "Reproduce these commands exactly. A flag that looks like an obvious synonym — "
          "--company instead of --company-id, --force instead of --yes — is not accepted. "
          "Where the documentation states a default, that default is given here in bold text "
          "in the tables; where it does not, none is invented."),

 ("h2", "G0. How to read this reference"),
 ("p", "Three conventions run through every Paperclip command family, and learning them once "
       "saves learning them fourteen times."),
 ("bullets", [
   "COMPANY SCOPE IS PER-COMMAND. Almost every business object belongs to exactly one "
   "company, so most commands need to know which. That is supplied with -C or --company-id, "
   "or inherited from an environment variable or a stored profile. The project reference is "
   "explicit that company scope is per-command \"rather than inherited globally\".",
   "PAYLOADS ARE JSON, PARSED LOCALLY. Several families take a --payload-json (or --payload) "
   "flag carrying a JSON object. The CLI parses it with JSON.parse before sending anything, "
   "so malformed JSON fails on your machine with Invalid JSON: ... rather than producing a "
   "confusing server error.",
   "DESTRUCTIVE ACTIONS ARE GUARDED. Deletion commands refuse to run without --yes, and the "
   "most dangerous of them (company delete, secrets delete) additionally require --confirm "
   "with a value you must repeat by hand.",
 ]),
 ("p", "One more convention is worth stating on its own because it is the single most common "
       "source of lost credentials in a first week: several commands print a secret exactly "
       "once. That rule has its own section below, and it is not a suggestion."),
]

# ══════════════════════════════════════════════════════ G1. Global usage

_G1 = [
 ("rule",),
 ("h2", "G1. Global usage — the binary, the common options, output and credentials"),

 ("h3", "G1.1 The binary"),
 ("p", "The CLI ships as a single binary named paperclipai, distributed as the npm package "
       "paperclipai. There are three documented ways to invoke it, and which one you use "
       "changes nothing about the syntax that follows the binary name."),
 ("code",
  "# Run without installing anything (quick start)\n"
  "npx paperclipai onboard --yes\n"
  "\n"
  "# Global npm install\n"
  "npm install -g paperclipai\n"
  "paperclipai --help\n"
  "\n"
  "# Managed install (recommended by the docs)\n"
  "npx paperclipai install\n"
  "\n"
  "# In a monorepo / git checkout, the docs use pnpm\n"
  "pnpm paperclipai <command>"),
 ("p", "The managed install places the binary at ~/.local/bin/paperclipai with automatic "
       "updates and rollback, and keeps its managed store at ~/.paperclip/cli. Node.js 20 or "
       "newer must be on PATH; the documented check is node --version, which must report "
       "v20.x or higher."),
 ("table", ("Flags accepted by paperclipai install",
   ["Flag", "Purpose"],
   [["--canary", "Install npm canary channel"],
    ["--version <version>", "Install exact published version"],
    ["--ref <ref>", "Install from GitHub branch/tag/commit"],
    ["-y, --yes", "Non-interactive consent"]])),

 ("h3", "G1.2 Common options that apply everywhere"),
 ("p", "The following client flags are shared across the command families. They are not "
       "repeated in every section below; assume they are available unless a section says "
       "otherwise."),
 ("table", ("Shared client flags (Common Options reference)",
   ["Flag", "Purpose", "Notes"],
   [["-d, --data-dir <path>", "\"Isolates all local state (config, context, db, logs, "
     "storage, secrets) away from ~/.paperclip\"", "Enables clean test instances"],
    ["--api-base <url>", "\"Base URL for the Paperclip API. Highest-priority override\"",
     "Normalises trailing slashes"],
    ["--api-key <token>", "\"Bearer token for authenticated calls. Highest-priority "
     "credential\"", "Disables interactive recovery"],
    ["--context <path>", "\"Path to the CLI context file to read and write\"",
     "Defaults to ~/.paperclip/context.json"],
    ["--profile <name>", "\"Which context profile to use\"",
     "Defaults to the context's current profile"],
    ["-c, --config <path>", "\"Used only to infer a local server port\"",
     "When no API base is given"],
    ["--json", "\"Emit raw JSON instead of the human-readable inline format\"",
     "For scripting and automation"],
    ["-C, --company-id <id>", "\"Company ID. Overrides the profile's default company\"",
     "Company-scoped commands only"]])),

 ("h3", "G1.3 How the CLI decides which server to talk to"),
 ("p", "When a command needs an API base URL and you have not supplied one, the CLI works "
       "down a fixed list. Knowing the order turns \"it connected to the wrong instance\" "
       "from a mystery into a two-second check."),
 ("bullets", [
   "1. The --api-base flag.",
   "2. The PAPERCLIP_API_URL environment variable.",
   "3. The profile's stored apiBase.",
   "4. A locally inferred http://<host>:<port> — host from PAPERCLIP_SERVER_HOST, port from "
   "PAPERCLIP_SERVER_PORT or the config file.",
   "5. The fallback http://localhost:3100.",
 ]),
 ("p", "Company scope resolves down a shorter list: --company-id or -C first, then "
       "PAPERCLIP_COMPANY_ID, then the profile's stored companyId."),

 ("h3", "G1.4 How the CLI decides which credential to use"),
 ("p", "Credentials resolve in their own documented order, and each source is labelled in the "
       "CLI's own authSource field, which is what you inspect when a call is authenticating "
       "as somebody you did not expect."),
 ("table", ("Credential resolution order",
   ["Priority", "Source", "authSource label"],
   [["1", "--api-key <token>", "explicit"],
    ["2", "PAPERCLIP_API_KEY environment variable", "env"],
    ["3", "Environment variable named by the profile's apiKeyEnvVarName", "profile_env"],
    ["4", "Stored board credential for the resolved API base", "stored_board"]])),
 ("note", "From the Common Options page, and worth memorising: \"The profile never stores a "
          "plaintext token. It stores the _name_ of an environment variable.\" A stolen "
          "context.json is therefore not a stolen credential."),

 ("h3", "G1.5 Context profiles"),
 ("p", "A profile bundles an API base, a company, a persona and the NAME of the environment "
       "variable holding the token. Profiles are how you keep a training instance and a "
       "production instance apart without retyping flags."),
 ("code",
  "paperclipai context show\n"
  "paperclipai context show --profile staging --json\n"
  "paperclipai context list\n"
  "paperclipai context use staging\n"
  "paperclipai context set --profile prod --api-base https://paperclip.example.com \\\n"
  "  --persona board --api-key-env-var-name PAPERCLIP_API_KEY --use"),
 ("p", "context set accepts --profile <name>, --api-base <url>, --company-id <id>, "
       "--persona <persona>, --agent-id <id>, --agent-name <name>, "
       "--api-key-env-var-name <name> and --use. Profile discovery walks --context flag → "
       "PAPERCLIP_CONTEXT environment variable → .paperclip/context.json walking upward → "
       "~/.paperclip/context.json. The stored fields are apiBase, companyId, persona "
       "(board or agent), agentId, agentName and apiKeyEnvVarName."),

 ("h3", "G1.6 Output and scripting"),
 ("p", "Every command family documents --json, and the guidance is consistent across pages: "
       "use it whenever you script. The human-readable output is a compact summary designed "
       "for a terminal; the JSON output is the full record. The run reference gives the "
       "canonical scripting idiom."),
 ("code", "paperclipai run live --json | jq '.[].id'"),
 ("p", "The cost reference makes the same point from the operations side: \"Reads are cheap "
       "and idempotent. Wire cost summary, budget overview, and cost window-spend into a "
       "monitoring loop with --json and pipe the output into your own dashboards or "
       "alerting.\""),

 ("h3", "G1.7 Environment variables the CLI itself reads"),
 ("table", ("CLI-facing environment variables",
   ["Variable", "Effect"],
   [["PAPERCLIP_API_URL", "API base URL, second in the resolution order"],
    ["PAPERCLIP_COMPANY_ID", "Default company, second in the company-scope order"],
    ["PAPERCLIP_AGENT_ID", "Agent identity for agent-persona use"],
    ["PAPERCLIP_API_KEY", "Bearer credential, second in the credential order"],
    ["PAPERCLIP_CONTEXT", "Path to the CLI context file"],
    ["PAPERCLIP_SERVER_HOST / PAPERCLIP_SERVER_PORT", "Used for local API-base inference"]])),
 ("table", ("Local config paths",
   ["Path", "Holds"],
   [["~/.paperclip", "Default local config directory"],
    ["~/.paperclip/context.json", "Profiles storage"],
    ["~/.paperclip/cli", "Managed install store"],
    ["~/.codex/skills", "Codex skills installation"],
    ["~/.claude/skills", "Claude skills installation"]])),
]

# ═══════════════════════════════════════════════ G2. Setup and service

_G2 = [
 ("rule",),
 ("h2", "G2. Setup and service — onboard, run, doctor, configure, env"),

 ("p", "This family gets an instance existing, running and healthy. It is the only family you "
       "use before you have any credential at all, because in the default local_trusted mode "
       "the board operator is implicitly trusted and no login is required."),

 ("h3", "G2.1 The one-command path"),
 ("p", "paperclipai run is the composite command: it bootstraps and starts a local server in "
       "one step. Its documented sequence is worth knowing because it explains why the first "
       "run takes so much longer than the second: it resolves the instance ID, creates "
       "directories, runs onboard if needed, executes doctor with repair enabled, starts the "
       "server, and generates a bootstrap CEO invite if the instance is in authenticated mode "
       "with an embedded database."),
 ("code",
  "paperclipai run\n"
  "paperclipai run --instance dev\n"
  "paperclipai run --data-dir ./tmp/paperclip-dev\n"
  "paperclipai run --no-repair"),
 ("table", ("paperclipai run flags",
   ["Flag", "Use"],
   [["-c, --config <path>", "Path to the config file"],
    ["-d, --data-dir <path>", "Isolate all local state from ~/.paperclip"],
    ["-i, --instance <id>", "Local instance id (default: default)"],
    ["--bind <mode>", "Onboarding reachability preset: loopback, lan, or tailnet"],
    ["--no-repair", "Disable automatic repairs during doctor"],
    ["--force", "Run even when the same instance is active under the service manager"]])),
 ("note", "Documented warning: \"before anything else, run checks whether this instance is "
          "already active under the service manager. If it is, run refuses to start — two "
          "servers on one port and one database is not a state you want.\""),

 ("h3", "G2.2 onboard"),
 ("p", "onboard is the interactive first-run setup. It writes the configuration to "
       "~/.paperclip/instances/<id>/config.json, provisions PAPERCLIP_AGENT_JWT_SECRET in "
       ".env, and creates the local secrets key file."),
 ("code",
  "paperclipai onboard\n"
  "paperclipai onboard --yes\n"
  "paperclipai onboard --run\n"
  "paperclipai onboard --bind lan"),
 ("table", ("paperclipai onboard flags",
   ["Flag", "Use"],
   [["-c, --config <path>", "Path to the config file"],
    ["-d, --data-dir <path>", "Isolate all local state from ~/.paperclip"],
    ["--bind <mode>", "Quickstart reachability preset"],
    ["-y, --yes", "Accept Quickstart defaults non-interactively"],
    ["--install-service", "Install background service after onboarding"],
    ["--no-install-service", "Skip service installation"],
    ["--run", "Start server immediately after saving config"]])),
 ("note", "Documented note: \"If a valid config already exists, onboard preserves it "
          "unchanged, ensures the agent JWT secret and secrets key exist, and prints "
          "next-step commands. Use configure to change settings on an existing install "
          "rather than re-onboarding.\" And the --bind tip: it \"only matters on the very "
          "first run, when it forwards the preset to onboarding.\""),

 ("h3", "G2.3 doctor"),
 ("p", "doctor is the diagnostic sweep, with optional repair. Reach for it before you reach "
       "for a firewall rule; most first-week failures are one of the checks it already runs."),
 ("code",
  "paperclipai doctor\n"
  "paperclipai doctor --repair\n"
  "paperclipai doctor --repair --yes"),
 ("table", ("paperclipai doctor flags",
   ["Flag", "Use"],
   [["-c, --config <path>", "Path to the config file"],
    ["-d, --data-dir <path>", "Isolate all local state from ~/.paperclip"],
    ["--repair (alias --fix)", "Attempt to repair fixable issues"],
    ["-y, --yes", "Skip per-repair confirmation prompts"]])),
 ("p", "The documented check list is: config validity; deployment/auth mode compatibility; "
       "agent JWT secret; secrets adapter; storage; database connectivity; LLM provider; log "
       "directory; listen port; Node.js runtime (requires Node.js 20+); managed install "
       "(store, shim, PATH, payload retention); and background service (definition, runtime, "
       "health, version)."),
 ("note", "Documented warning: \"--repair can create or update local files (the JWT .env, the "
          "secrets key, the log directory) when a check knows how to fix the problem. Review "
          "the output before running it against a shared or production-like instance.\""),

 ("h3", "G2.4 env"),
 ("p", "env prints the environment variables a deployment needs, together with their sources. "
       "The output has two sections, Required and Optional, and marks each variable set, "
       "default or missing. The required variables are PAPERCLIP_AGENT_JWT_SECRET and "
       "DATABASE_URL."),
 ("code", "paperclipai env"),
 ("p", "Flags: -c, --config <path> and -d, --data-dir <path>."),

 ("h3", "G2.5 configure"),
 ("p", "configure changes settings on an EXISTING install — the correct alternative to "
       "re-running onboard. It is section-driven."),
 ("code",
  "paperclipai configure\n"
  "paperclipai configure --section server\n"
  "paperclipai configure --section database\n"
  "paperclipai configure --section storage\n"
  "paperclipai configure --section secrets\n"
  "paperclipai configure --section logging\n"
  "paperclipai configure --section llm"),
 ("table", ("configure sections and what each changes",
   ["Section", "Changes"],
   [["server", "Deployment mode, exposure, host binding, port, UI, auth base URL"],
    ["database", "Embedded vs. external PostgreSQL, connection string, backup settings"],
    ["storage", "Provider (local_disk or s3) and options"],
    ["secrets", "Provider, strict mode, local key file"],
    ["logging", "Logging mode and directory"],
    ["llm", "LLM provider and API key"]])),
 ("p", "Flags: -c, --config <path>, -d, --data-dir <path>, -s, --section <section>."),

 ("h3", "G2.6 Backups and hostname allowlisting"),
 ("code",
  "paperclipai db:backup\n"
  "paperclipai db:backup --dir /backups/paperclip\n"
  "paperclipai db:backup --retention-days 14\n"
  "paperclipai db:backup --json"),
 ("table", ("paperclipai db:backup flags",
   ["Flag", "Use"],
   [["--dir <path>", "Backup output directory"],
    ["--retention-days <days>", "Retention window for daily pruning (default 30)"],
    ["--filename-prefix <prefix>", "Backup filename prefix (default paperclip)"],
    ["--json", "Print backup metadata as JSON"]])),
 ("note", "Documented tip: \"For the embedded database you can run a backup without the "
          "server up — db:backup connects on the embedded port directly.\""),
 ("code",
  "paperclipai allowed-hostname dotta-macbook-pro\n"
  "paperclipai allowed-hostname my-host.ts.net"),
 ("p", "The <host> argument is normalised and lowercased. Two constraints apply and both bite "
       "in the classroom: the change takes effect only after a server restart, and it is only "
       "enforced in authenticated + private mode."),

 ("h3", "G2.7 The background service"),
 ("p", "The documentation covers service installation from two angles. The installation guide "
       "shows the service install command alongside the managed install, and doctor checks "
       "the background service's definition, runtime, health and version. onboard can install "
       "or skip the service through --install-service and --no-install-service."),
 ("code",
  "npx paperclipai install\n"
  "paperclipai service install\n"
  "npx paperclipai run          # restart\n"
  "sudo journalctl -u paperclip -f"),
 ("note", "The harvested documentation does not enumerate further service subcommands or "
          "their flags — a dedicated CLI service page exists in the navigation but its "
          "contents were not harvested. Do not assume service status, service logs or "
          "service uninstall exist in that exact form; check paperclipai --help on your own "
          "install before relying on them."),

 ("h3", "G2.8 Updates, rollback and release channels"),
 ("p", "The managed install path is the documented route to updates: npx paperclipai install "
       "\"installs to ~/.local/bin/paperclipai with automatic updates and rollback\", and "
       "doctor verifies the managed store, shim, PATH and payload retention. The docs "
       "changelog records four release channels — stable, beta, nightly and canary — "
       "surfaced by the paperclipai channels command, which \"shows which one your install "
       "follows\". The install command's own --canary, --version <version> and --ref <ref> "
       "flags pin a specific build."),
 ("note", "Since v2026.824.1, after onboard installs the background service it \"waits for "
          "the port the service actually bound, prints the dashboard URL, and opens it in "
          "your browser. Headless runs print the URL, and PAPERCLIP_NO_BROWSER=1 opts out of "
          "the browser launch.\""),

 ("h3", "G2.9 Local instance layout"),
 ("code",
  "~/.paperclip/instances/<instance-id>/\n"
  "|-- config.json          (Config)\n"
  "|-- db/                  (Embedded database)\n"
  "|-- logs/                (Logs)\n"
  "|-- data/storage/        (Local disk storage)\n"
  "`-- secrets/master.key   (Secrets key)"),
 ("p", "The default instance ID is default. Embedded PostgreSQL listens on port 54329 with "
       "data in ~/.paperclip/instances/default/db; the server's own default port is 3100, "
       "bound to 127.0.0.1."),
 ("note", "Three warnings from the installation guide, all of which have ended somebody's "
          "afternoon: \"Do not run this command with sudo or from a root/admin shell\" "
          "(PostgreSQL refuses to run as an administrative user); \"Do not open port 3100 to "
          "the internet\"; and \"Back up secrets/master.key somewhere safe. It encrypts every "
          "API key and secret stored in Paperclip — if you lose it, you lose access to all of "
          "them.\""),
]

# ═══════════════════════════════════════════ G3. Authentication and tokens

_G3 = [
 ("rule",),
 ("h2", "G3. Authentication and tokens"),

 ("p", "Paperclip recognises two identity classes — BOARD (a human or operator) and AGENT (a "
       "runtime) — and the whole authentication surface follows from that split. Board "
       "identities are the ones that decide; agent identities are the ones that request. "
       "Every command in this section produces or inspects one of those two."),

 ("h3", "G3.1 The interactive wizard"),
 ("p", "connect is the TTY-only setup wizard. It is the shortest path from a fresh terminal "
       "to a working profile."),
 ("code",
  "paperclipai connect\n"
  "paperclipai connect --persona agent --token-name laptop-cli"),
 ("p", "Flags: --persona <persona>, --api-key-env-var-name <name>, --token-name <name>."),

 ("h3", "G3.2 Board login and identity"),
 ("code",
  "paperclipai auth login\n"
  "paperclipai auth login --instance-admin\n"
  "paperclipai auth login --company-id <company-id>\n"
  "paperclipai auth login --no-browser\n"
  "\n"
  "paperclipai auth whoami --json\n"
  "paperclipai auth logout\n"
  "paperclipai auth revoke-current"),
 ("p", "auth login flags are --instance-admin, --company-id <id> and --no-browser. The login "
       "flow is a browser approval: the CLI raises a challenge and a browser session approves "
       "it. auth whoami is the fastest confirmation of which identity a credential actually "
       "resolves to, and is the first thing to run when a command behaves as though it "
       "belongs to somebody else."),

 ("h3", "G3.3 bootstrap-ceo — minting the first board credential"),
 ("p", "On a server install there is no board user yet, and no browser session to approve a "
       "login with. auth bootstrap-ceo is the headless escape hatch: it mints the first board "
       "credential and emits an invite link."),
 ("code",
  "paperclipai auth bootstrap-ceo\n"
  "paperclipai auth bootstrap-ceo --expires-hours 24\n"
  "paperclipai auth bootstrap-ceo --force\n"
  "paperclipai auth bootstrap-ceo --base-url https://paperclip.example.com"),
 ("table", ("auth bootstrap-ceo flags",
   ["Flag", "Use"],
   [["--force", "Create a new invite if an admin already exists"],
    ["--expires-hours <hours>", "Invite lifetime in hours (1-720; default 72)"],
    ["--base-url <url>", "Public base URL for the invite link"],
    ["--db-url <URL>", "Database URL (listed on the installation guide's flag list)"]])),
 ("p", "The output is an invite URL of the form https://paperclip.example.com/invite/<token>. "
       "In authenticated mode the equivalent board-claim URL takes the form "
       "/board-claim/<token>?code=<code>."),
 ("note", "Documented warning: \"Treat the claim URL as sensitive — it's a one-time ownership "
          "transfer, not something to share. If it expires before you use it, restart the "
          "server to mint a fresh one.\""),

 ("h3", "G3.4 Board tokens"),
 ("p", "A board token carries full instance authority. Create one for automation that must act "
       "as an operator — a release bot, an external administration tool — and give it the "
       "shortest life the job allows."),
 ("code",
  "paperclipai token board create --name external-admin\n"
  "paperclipai token board create --name short-lived --ttl-days 7\n"
  "paperclipai token board create --name release-bot --company-id <id> "
  "--expires-at 2026-12-31T00:00:00Z\n"
  "paperclipai token board create --name forever --never-expires\n"
  "paperclipai token board list\n"
  "paperclipai token board revoke <key-id>"),
 ("p", "Flags for token board create: --company-id <id>, --name <name>, "
       "--expires-at <iso8601>, --ttl-days <days>, --never-expires. Board API keys carry the "
       "prefix pcp_board_ and are long-lived by design."),

 ("h3", "G3.5 Agent keys"),
 ("p", "An agent key is scoped to one company and one agent. It is what a runtime uses to talk "
       "back to the control plane as itself."),
 ("code",
  "paperclipai token agent create --company-id <id> --agent <agent-id-or-name> "
  "--name external-worker\n"
  "paperclipai token agent list --company-id <id> --agent <agent-id-or-name>\n"
  "paperclipai token agent revoke --company-id <id> --agent <agent-id-or-name> <key-id>"),
 ("p", "Flags: --company-id <id> (required), --agent <agent> (required), --name <name>."),

 ("h3", "G3.6 The once-only display rule"),
 ("note", "From the CLI authentication reference, verbatim: \"Both credential types are shown "
          "in full **only at creation time**. The token string is printed once and never "
          "again.\" The agent reference repeats it for the local-cli bootstrap: \"The minted "
          "API key's plaintext token is shown **once**, in the command output. Treat the "
          "output as a secret, and revoke the key with token agent revoke when the local "
          "session is done.\" The API reference states the same rule for POST "
          "/api/agents/{agentId}/keys."),
 ("p", "The consequence is unforgiving: lose the token and you do not recover it — you "
       "revoke the key and mint a new one. Capture the output into a secret store at the "
       "moment of creation, never into a scrollback buffer."),

 ("h3", "G3.7 Token types at a glance"),
 ("table", ("Token types (API authentication reference)",
   ["Token type", "Prefix", "Purpose", "Lifetime"],
   [["Board API Key", "pcp_board_", "CLI / automation", "Long-lived"],
    ["Agent API Key", "(none documented)", "Agent requests", "Long-lived"],
    ["Local Agent JWT", "(none documented)", "Heartbeat / adapter code", "Short-lived"]])),
 ("p", "The local agent JWT carries required claims sub (agent ID), company_id, adapter_type, "
       "run_id, iat and exp. It is accepted only when the signature is valid, it has not "
       "expired, the agent exists and is not terminated or pending_approval, and the agent "
       "belongs to the same company as the token claims."),
 ("p", "Agent API key creation is REJECTED when the agent's status is pending_approval or "
       "terminated. Terminating an agent revokes all of its API keys."),
]

# ═════════════════════════════════════════════════════════ G4. Company

_G4 = [
 ("rule",),
 ("h2", "G4. Company commands"),

 ("p", "A company is the top-level tenant boundary: \"Every agent, project, issue, approval, "
       "cost event, and asset belongs to exactly one company, and the API enforces that "
       "boundary on every company-scoped route.\" The command family divides cleanly into "
       "safe reads, payload-driven writes, portability and — behind two separate guards — "
       "deletion."),

 ("h3", "G4.1 Reads"),
 ("code",
  "paperclipai company list\n"
  "paperclipai company get <company-id>\n"
  "paperclipai company current\n"
  "paperclipai company stats"),

 ("h3", "G4.2 Create and update"),
 ("code",
  "paperclipai company create --payload-json '{...}'\n"
  "paperclipai company update <company-id> --payload-json '{...}'\n"
  "paperclipai company branding:update <company-id> --payload-json '{...}'"),
 ("p", "The company object's documented fields are id, name, description, status (active, "
       "paused or archived), issuePrefix, issueCounter, budgetMonthlyCents, spentMonthlyCents, "
       "requireBoardApprovalForNewAgents, brandColor, logoAssetId, logoUrl, createdAt and "
       "updatedAt. On create, \"If budgetMonthlyCents is greater than 0, Paperclip also "
       "creates the matching monthly budget policy in UTC calendar-month mode.\""),

 ("h3", "G4.3 Archive, export, import"),
 ("code",
  "paperclipai company archive <company-id>\n"
  "\n"
  "paperclipai company export <company-id> --out ./path\n"
  "paperclipai company import ./path --target new|existing\n"
  "\n"
  "paperclipai company export:preview <company-id> --payload-json '{...}'\n"
  "paperclipai company export:api <company-id> --payload-json '{...}'\n"
  "paperclipai company import:preview <company-id> --payload-json '{...}'\n"
  "paperclipai company import:apply <company-id> --payload-json '{...}'\n"
  "\n"
  "paperclipai company feedback:list --company-id <id>\n"
  "paperclipai company feedback:export --company-id <id>"),
 ("table", ("Company command flags",
   ["Flag", "Purpose"],
   [["--payload-json", "Required for create/update; raw JSON payload"],
    ["--out <path>", "Output directory for exports"],
    ["--include <values>", "Comma-separated: company,agents,projects,issues,skills"],
    ["--yes", "Safety flag for deletion"],
    ["--confirm <value>", "Must match the target company ID or prefix"],
    ["--json", "Machine-readable output"]])),

 ("h3", "G4.4 Deletion"),
 ("code", "paperclipai company delete <company-id> --yes --confirm <value>"),
 ("bullets", [
   "\"Archiving is the reversible way to take a company out of active rotation\" — deletion "
   "is not.",
   "Deletion requires PAPERCLIP_ENABLE_COMPANY_DELETION enabled server-side.",
   "\"There is no undo\" for company deletion.",
   "IMPORTED AGENTS HAVE TIMER HEARTBEATS DISABLED BY DEFAULT — a restored company is quiet "
   "until you re-enable them, which is a feature, not a fault.",
 ]),
 ("note", "Archiving is not passive. The documented cascade \"pauses every active agent in "
          "the company (pause reason company_archived) and cancels their queued or in-flight "
          "wake-up requests.\""),
]

# ═════════════════════════════════════════════════════════ G5. Project

_G5 = [
 ("rule",),
 ("h2", "G5. Project commands"),

 ("p", "Projects group work and carry two things agents care about: a lead agent and, "
       "optionally, an execution-workspace policy and an env binding. The command family is "
       "small, which makes its two idioms — shortname resolution and the literal \"null\" — "
       "worth learning properly."),

 ("h3", "G5.1 At a glance"),
 ("code",
  "paperclipai project list --company-id <company-id>\n"
  "paperclipai project get <project-id-or-shortname> [--company-id <company-id>]\n"
  "paperclipai project create --company-id <company-id> --name \"Launch Site\" "
  "[--goal-ids <id1,id2>] [--lead-agent-id <agent-id>]\n"
  "paperclipai project update <project-id-or-shortname> --status in_progress "
  "[--company-id <company-id>]\n"
  "paperclipai project delete <project-id-or-shortname> --yes [--company-id <company-id>]"),

 ("h3", "G5.2 Create"),
 ("code",
  "paperclipai project create \\\n"
  "  --company-id <company-id> \\\n"
  "  --name \"Launch Site\" \\\n"
  "  --description \"Public marketing launch\" \\\n"
  "  --status planned \\\n"
  "  --goal-ids <goal-id-1>,<goal-id-2> \\\n"
  "  --lead-agent-id <agent-id> \\\n"
  "  --color \"#3b82f6\""),
 ("table", ("project create flags",
   ["Flag", "Use"],
   [["-C, --company-id <id>", "Company to create the project in. Required."],
    ["--name <name>", "Project name. Required."],
    ["--description <text>", "Free-text description."],
    ["--status <status>", "Initial project status."],
    ["--goal-ids <csv>", "Comma-separated list of goal IDs to link."],
    ["--goal-id <id>", "Deprecated single goal ID. Prefer --goal-ids."],
    ["--lead-agent-id <id>", "Agent that leads the project."],
    ["--target-date <date>", "Target/target-completion date."],
    ["--color <value>", "Project color."],
    ["--env-json <json>", "Project env binding as a JSON object."],
    ["--execution-workspace-policy-json <json>",
     "Execution workspace policy as a JSON object."]])),
 ("note", "On --status values: the project reference documents the flag as \"Initial project "
          "status\" and shows planned and in_progress in its own worked examples. It does not "
          "publish a closed enumeration on that page, so treat any value beyond those two as "
          "unverified until your own instance's schema confirms it. The create payload \"is "
          "validated against the server's create-project schema before the request is sent, "
          "so an out-of-range value fails locally with a clear error rather than a server "
          "round-trip\" — which is, conveniently, how you discover the valid set safely."),

 ("h3", "G5.3 Update, archive and the \"null\" idiom"),
 ("code",
  "paperclipai project update <project-id-or-shortname> --status in_progress\n"
  "paperclipai project update launch-site --company-id <company-id> --name \"Launch v2\"\n"
  "\n"
  "# Clear the lead agent and unarchive in one call\n"
  "paperclipai project update <project-id> --lead-agent-id null --archived-at null\n"
  "\n"
  "# Archive a project\n"
  "paperclipai project update <project-id> --archived-at 2026-06-01T00:00:00Z"),
 ("table", ("project update flags",
   ["Flag", "Use"],
   [["-C, --company-id <id>", "Company ID for shortname lookup."],
    ["--name <name>", "New project name."],
    ["--description <text|null>", "New description, or null to clear it."],
    ["--status <status>", "New project status."],
    ["--goal-ids <csv>", "Replace the linked goal IDs with this comma-separated list."],
    ["--goal-id <id|null>", "Deprecated single goal ID, or null to clear."],
    ["--lead-agent-id <id|null>", "New lead agent, or null to clear."],
    ["--target-date <date|null>", "New target date, or null to clear."],
    ["--color <value|null>", "New color, or null to clear."],
    ["--env-json <json|null>", "Replace the env binding, or null to clear it."],
    ["--execution-workspace-policy-json <json|null>",
     "Replace the execution workspace policy, or null to clear it."],
    ["--archived-at <iso8601|null>", "Archive timestamp, or null to unarchive."]])),
 ("p", "The clearing rule is stated once and applies across the whole flag set: \"pass the "
       "literal string null to clear the value, omit the flag to leave it unchanged.\" It "
       "applies to --description, --goal-id, --lead-agent-id, --target-date, --color, "
       "--env-json, --execution-workspace-policy-json and --archived-at. That is also the "
       "archiving semantics in full: archiving is a timestamp you set, and unarchiving is "
       "that same timestamp cleared with null. There is no separate archive subcommand for "
       "projects."),
 ("note", "Documented note on goals: \"--goal-ids replaces the entire set of linked goals on "
          "the project. Pass the full list you want, not a delta.\""),

 ("h3", "G5.4 JSON fields"),
 ("code",
  "paperclipai project create \\\n"
  "  --company-id <company-id> \\\n"
  "  --name \"Ops\" \\\n"
  "  --env-json '{\"OPENAI_API_KEY\":{\"kind\":\"secret\",\"secretName\":\"openai-api-key\"}}'\n"
  "\n"
  "paperclipai project update <project-id> \\\n"
  "  --execution-workspace-policy-json "
  "'{\"enabled\":true,\"defaultMode\":\"shared_workspace\"}'\n"
  "\n"
  "paperclipai project update <project-id> --execution-workspace-policy-json null"),

 ("h3", "G5.5 Delete"),
 ("code",
  "paperclipai project delete <project-id-or-shortname> --yes\n"
  "paperclipai project delete launch-site --company-id <company-id> --yes"),
 ("bullets", [
   "delete \"refuses to run without --yes — the command fails fast with \\\"Deletion requires "
   "--yes.\\\" if the flag is missing.\"",
   "Documented warning: \"Deleting a project is immediate once --yes is supplied. Confirm the "
   "reference resolves to the right project with project get before you delete it, especially "
   "when using a shortname.\"",
   "get, update and delete accept either the project UUID or its shortname. Pass --company-id "
   "when using a shortname so the server can resolve it; on get it \"adds a companyId query "
   "parameter\".",
   "Both JSON flags are parsed with JSON.parse client-side; invalid JSON fails locally with "
   "Invalid JSON: ... \"before any request is made\".",
 ]),
 ("table", ("project list default (non-JSON) output fields",
   ["Field", "Meaning"],
   [["id", "The project UUID."],
    ["name", "The project's display name."],
    ["status", "The project's current status."],
    ["urlKey", "The project's stable shortname/URL key."],
    ["goalIds", "Comma-separated goal IDs the project is linked to."],
    ["leadAgentId", "The agent leading the project, if set."]])),
]

# ═══════════════════════════════════════════════════════════ G6. Issue

_G6 = [
 ("rule",),
 ("h2", "G6. Issue commands"),

 ("p", "Issues are the unit of work, and the issue family is the largest in the CLI, "
       "presented here in the groups the documentation itself uses. Two things matter more "
       "than the command list: the checkout discipline and the status transitions. Get those "
       "wrong and you produce a race condition that is hard to debug after the fact."),

 ("h3", "G6.1 CRUD"),
 ("code",
  "paperclipai issue list -C <company-id> --status todo,in_review "
  "--assignee-agent-id <agent-id> --match \"billing\"\n"
  "paperclipai issue get PC-12\n"
  "paperclipai issue create -C <company-id> --title \"Fix invoice rounding\" --priority high "
  "--assignee-agent-id <agent-id>\n"
  "paperclipai issue update <issue-id> --status in_review --comment \"Ready for review\"\n"
  "paperclipai issue delete <issue-id> --yes"),

 ("h3", "G6.2 Checkout and release — the discipline"),
 ("code",
  "paperclipai issue checkout <issue-id> --agent-id <agent-id>\n"
  "paperclipai issue checkout <issue-id> --agent-id <agent-id> "
  "--expected-statuses todo,in_review\n"
  "paperclipai issue release <issue-id>\n"
  "paperclipai issue force-release <issue-id>"),
 ("p", "Checkout is the ONLY correct way for an agent to claim an issue. The todo to "
       "in_progress transition is atomic, performed by POST /api/issues/{id}/checkout, and "
       "the body carries agentId plus expectedStatuses — a non-empty list of the statuses you "
       "are prepared to find. That makes the claim conditional: if the issue has moved since "
       "you read it, the claim fails rather than trampling somebody else's work."),
 ("table", ("The checkout rules that matter",
   ["Rule", "Detail"],
   [["Only one holder", "\"Only one agent can hold an issue 'in progress' at a time.\""],
    ["Agents claim as themselves", "\"An agent can only checkout as itself.\""],
    ["409 is terminal", "Checkout returns 409 Conflict when the issue does not match one "
     "expectedStatuses value, when the project is paused, or when the workspace is a closed "
     "isolated workspace. \"Never retry a 409 — pick a different issue.\""],
    ["Idempotent for the same holder", "Checkout is idempotent if the same agent already owns "
     "the task."],
    ["Reclaim deliberately", "To reclaim a stale in_progress issue, include in_progress in "
     "expectedStatuses with a NEW run id in X-Paperclip-Run-Id."],
    ["Run id on updates", "Agent updates to checked-out in_progress issues require "
     "X-Paperclip-Run-Id."]])),
 ("p", "release is the clean way to let go: it \"Clears assigneeAgentId, checkoutRunId; sets "
       "status todo; preserves assigneeUserId.\" force-release exists for the case where the "
       "holder is not coming back."),

 ("h3", "G6.3 Status values and transitions"),
 ("table", ("Issue status values",
   ["Status", "Meaning", "Terminal?"],
   [["backlog", "Parked, unscheduled; not in default inbox", "No"],
    ["todo", "Ready and actionable; waiting for agent checkout", "No"],
    ["in_progress", "Checked out by agent; actively executing; exclusive", "No"],
    ["in_review", "Paused pending reviewer/approver/board/user", "No"],
    ["blocked", "Cannot proceed until blocker resolved", "No"],
    ["done", "Work complete", "Yes"],
    ["cancelled", "Intentionally abandoned", "Yes"]])),
 ("table", ("State machine transitions",
   ["From", "To", "Triggered by"],
   [["backlog", "todo", "Manual scheduling, ready-for-work signal"],
    ["todo", "in_progress", "POST /api/issues/{id}/checkout (atomic)"],
    ["in_progress", "in_review", "PATCH with status: \"in_review\""],
    ["in_progress", "done", "PATCH with status: \"done\" (sets completedAt)"],
    ["in_progress", "blocked",
     "PATCH with status: \"blocked\" plus blocker comment or blockedByIssueIds"],
    ["in_review", "in_progress", "Reviewer requested changes"],
    ["in_review", "done", "Reviewer/approver advanced"],
    ["blocked", "todo",
     "Blocker resolved (manual, release, or auto issue_blockers_resolved wake)"],
    ["any non-terminal", "cancelled", "PATCH with status: \"cancelled\" (sets cancelledAt)"],
    ["done / cancelled", "todo",
     "PATCH with reopen: true (the ONLY path back from terminal)"]])),
 ("note", "The single most common transition error: sending PATCH status: \"todo\" on a done "
          "issue. Terminal transitions require reopen. Send PATCH { reopen: true, comment: "
          "\"...\" } instead. And note that cancelled blockers do NOT count as resolved — "
          "replace or remove the cancelled id from blockedByIssueIds explicitly."),

 ("h3", "G6.4 Comments"),
 ("code",
  "paperclipai issue comment <issue-id> --body \"Picking this up now\"\n"
  "paperclipai issue comment <issue-id> --body \"Re-opening, the fix regressed\" --reopen\n"
  "paperclipai issue comment <issue-id> --body \"Any update?\" --resume\n"
  "paperclipai issue comments <issue-id> --order asc --limit 50\n"
  "paperclipai issue comment:get <issue-id> <comment-id>\n"
  "paperclipai issue comment:delete <issue-id> <comment-id>"),
 ("p", "Comment listing accepts after / afterCommentId, order (asc or desc) and limit, which "
       "is capped at 500. Comment bodies are markdown. @mentions in a comment trigger wakeups "
       "for matching agents — the syntax is @AgentName, case-insensitive, and it must match "
       "the agent's name field exactly. Two documented cautions on that: \"Don't overuse "
       "mentions — each mention triggers a budget-consuming heartbeat\" and \"Don't use "
       "mentions for assignment — create or assign a task instead.\""),

 ("h3", "G6.5 Documents, work products and attachments"),
 ("code",
  "paperclipai issue documents <issue-id> --include-system\n"
  "paperclipai issue document:get <issue-id> spec\n"
  "paperclipai issue document:put <issue-id> spec --title \"Spec\" --body-file ./spec.md "
  "--change-summary \"Initial draft\"\n"
  "paperclipai issue document:lock <issue-id> spec\n"
  "paperclipai issue document:unlock <issue-id> spec\n"
  "paperclipai issue document:revisions <issue-id> spec\n"
  "paperclipai issue document:restore <issue-id> spec <revision-id>\n"
  "paperclipai issue document:delete <issue-id> <key>\n"
  "\n"
  "paperclipai issue work-products <issue-id>\n"
  "paperclipai issue work-product:create <issue-id> --payload-json "
  "'{\"kind\":\"report\",\"title\":\"Q2 analysis\"}'\n"
  "paperclipai issue work-product:update <work-product-id> --payload-json "
  "'{\"title\":\"Q2 analysis (final)\"}'\n"
  "paperclipai issue work-product:delete <work-product-id>\n"
  "\n"
  "paperclipai issue attachments <issue-id>\n"
  "paperclipai issue attachment:upload <issue-id> -C <company-id> --file ./diagram.png\n"
  "paperclipai issue attachment:upload <issue-id> -C <company-id> --file ./log.txt "
  "--comment-id <comment-id>\n"
  "paperclipai issue attachment:download <attachment-id> --out ./diagram.png\n"
  "paperclipai issue attachment:delete <attachment-id>"),
 ("p", "Document bodies are markdown only, up to 512 KiB, and updates require a baseRevisionId. "
       "A stale baseRevisionId returns 409 Conflict with the current revision id, and an "
       "existing key sent without baseRevisionId is rejected outright. Restoring a revision "
       "\"does not overwrite history. It creates a new revision that becomes the latest "
       "body.\" Document keys must be lowercase, with numbers, underscore and hyphen allowed."),
 ("note", "Locked documents behave differently by caller class. A USER caller gets 409 "
          "Conflict with { \"error\": \"Document is locked\", \"key\": \"...\", \"lockedAt\": "
          "\"...\" }. An AGENT caller has its write routed to a derived document — plan-2 if "
          "plan is locked — and the response carries redirectedFromLockedDocument."),

 ("h3", "G6.6 Interactions, labels, approvals and inbox state"),
 ("code",
  "paperclipai issue interactions <issue-id>\n"
  "paperclipai issue interaction:create <issue-id> --payload-json '{ ... }'\n"
  "paperclipai issue interaction:accept <issue-id> <interaction-id> "
  "--selected-client-keys a,b\n"
  "paperclipai issue interaction:reject <issue-id> <interaction-id> --reason \"Out of scope\"\n"
  "paperclipai issue interaction:cancel <issue-id> <interaction-id> "
  "--reason \"No longer needed\"\n"
  "paperclipai issue interaction:respond <issue-id> <interaction-id> --answers-json "
  "'[{\"key\":\"q1\",\"value\":\"yes\"}]' --summary-markdown \"Confirmed scope\"\n"
  "\n"
  "paperclipai issue label:list -C <company-id>\n"
  "paperclipai issue label:create -C <company-id> --name \"needs-review\" "
  "--color \"#4f46e5\"\n"
  "paperclipai issue label:delete <label-id>\n"
  "\n"
  "paperclipai issue approvals <issue-id>\n"
  "paperclipai issue approval:link <issue-id> <approval-id>\n"
  "paperclipai issue approval:unlink <issue-id> <approval-id>\n"
  "\n"
  "paperclipai issue read <issue-id>\n"
  "paperclipai issue unread <issue-id>\n"
  "paperclipai issue archive <issue-id>\n"
  "paperclipai issue unarchive <issue-id>"),
 ("table", ("Interaction kinds and when to use each",
   ["Kind", "When to use"],
   [["suggest_tasks", "Agent identified next work; board chooses which subtasks to spin up"],
    ["ask_user_questions", "Agent needs structured info (multiple choice, short text)"],
    ["request_confirmation",
     "Agent has a proposal (plan revision, destructive action); needs explicit acceptance"],
    ["request_checkbox_confirmation",
     "Agent needs a decision over explicitly listed checkbox options"],
    ["request_item_verdicts", "Agent needs a verdict for each item in a supplied list"]])),
 ("p", "Pending interactions expire automatically when an issue moves to done or cancelled: "
       "status becomes expired with result.outcome: \"issue_closed\". Creating a new card on "
       "a closed issue returns 409 \"Cannot create an interaction on a closed issue\". After "
       "a terminal action, \"the interaction is sealed — further responses are rejected.\""),

 ("h3", "G6.7 Trees, holds, recovery and runs"),
 ("code",
  "paperclipai issue tree-state <root-issue-id>\n"
  "paperclipai issue tree-preview <root-issue-id> --payload-json '{\"mode\":\"pause\"}'\n"
  "paperclipai issue tree-holds <root-issue-id> --status active --mode pause "
  "--include-members\n"
  "paperclipai issue tree-hold:create <root-issue-id> --payload-json "
  "'{\"mode\":\"pause\",\"reason\":\"awaiting budget\"}'\n"
  "paperclipai issue tree-hold:get <root-issue-id> <hold-id>\n"
  "paperclipai issue tree-hold:release <root-issue-id> <hold-id> --payload-json '{}'\n"
  "\n"
  "paperclipai issue recovery-actions <issue-id>\n"
  "paperclipai issue recovery:resolve <issue-id> --outcome restored "
  "--source-issue-status todo --resolution-note \"Re-queued\"\n"
  "paperclipai issue runs <issue-id>\n"
  "paperclipai issue live-runs <issue-id>\n"
  "paperclipai issue active-run <issue-id>\n"
  "paperclipai issue child:create <parent-issue-id> --payload-json '{\"title\":\"Subtask\"}'\n"
  "\n"
  "paperclipai issue feedback:votes <issue-id>\n"
  "paperclipai issue feedback:vote <issue-id> --payload-json "
  "'{\"targetType\":\"comment\",\"targetId\":\"<id>\",\"vote\":\"up\"}'\n"
  "paperclipai issue feedback:list <issue-id> --vote down --status open --include-payload\n"
  "paperclipai issue feedback:export <issue-id> --from 2026-01-01 --format ndjson "
  "--out ./feedback.ndjson\n"
  "\n"
  "paperclipai issue heartbeat-context <issueId>"),

 ("h3", "G6.8 The cross-issue influence cap"),
 ("note", "CROSS_ISSUE_INFLUENCE_LIMIT = 20. \"A single heartbeat run may make at most "
          "CROSS_ISSUE_INFLUENCE_LIMIT = 20 cross-issue comments or task updates combined — "
          "writes to run's own source issue don't count.\" The budget resets per run. Before "
          "CROSS_ISSUE_INFLUENCE_ENFORCE_AT = 2026-08-11T00:00:00.000Z the mode was log_only; "
          "from then on it is hard-enforced with 429 and the code "
          "cross_issue_influence_cap_exceeded."),
 ("table", ("Denial codes for cross-issue writes",
   ["Code", "Status", "Meaning"],
   [["issue_write_not_visible", "403",
     "Target issue not visible; all write channels closed"],
    ["issue_write_actor_class_excluded", "403",
     "Default-open writes are a standard-trust privilege"],
    ["issue_write_responsible_user_ceiling", "403", "Responsible user not authorised"],
    ["issue_write_responsible_user_unavailable", "403",
     "Responsible user removed/deactivated"],
    ["issue_write_assignee_run_lock", "409",
     "Assignee checked out; field edits belong to the lock-holder"],
    ["cross_issue_influence_cap_exceeded", "429",
     "Per-run cross-issue write budget spent"],
    ["cross_issue_influence_run_context_required", "403",
     "Write arrived without a valid heartbeat run"],
    ["issue_write_attribution_spoof_rejected", "422",
     "onBehalfOfUserId derived from actor, never from body"]])),
]

# ═══════════════════════════════════════════════════════════ G7. Agent

_G7 = [
 ("rule",),
 ("h2", "G7. Agent commands"),

 ("p", "The agent family covers the whole employment lifecycle — identity, hiring, "
       "configuration, lifecycle transitions and the local bootstrap that turns a laptop CLI "
       "into a working agent runtime. Note the distinction the documentation draws between "
       "create and hire: they are different governance paths, not synonyms."),

 ("h3", "G7.1 Identity and inbox"),
 ("code",
  "paperclipai agent me\n"
  "paperclipai agent inbox\n"
  "paperclipai agent inbox-mine --user-id <board-user-id> --status todo,in_progress"),
 ("table", ("Identity commands",
   ["Command", "Use"],
   [["agent me", "\"Show the current agent identity (GET /api/agents/me). The fastest way to "
     "confirm which agent a key or profile resolves to.\""],
    ["agent inbox", "\"List the current agent's assigned inbox items — a compact view of "
     "issues awaiting it.\""],
    ["agent inbox-mine --user-id <id>", "\"List the current agent's inbox items touched or "
     "archived by a specific board user. --status <csv> narrows by issue status (for example "
     "todo,in_progress).\""]])),

 ("h3", "G7.2 Listing, creating and hiring"),
 ("code",
  "paperclipai agent list --company-id <company-id>\n"
  "paperclipai agent get <agent-id>\n"
  "\n"
  "paperclipai agent create --company-id <company-id> \\\n"
  "  --payload-json '{\"name\":\"Builder\",\"adapterType\":\"codex_local\"}'\n"
  "\n"
  "paperclipai agent hire --company-id <company-id> \\\n"
  "  --payload-json '{\"name\":\"CTO\",\"role\":\"cto\",\"reason\":\"Lead engineering\"}'"),
 ("table", ("create versus hire",
   ["Command", "Use"],
   [["agent create", "\"Create an agent directly from a CreateAgent JSON payload (POST "
     "/api/companies/{id}/agents). Use this when you have board authority and want the agent "
     "to exist immediately.\""],
    ["agent hire", "\"Create an agent _hire request_ (POST /api/companies/{id}/agent-hires). "
     "Use this when hiring is governed and must pass through the board approval flow rather "
     "than landing as a live agent.\""]])),
 ("p", "Common agent create/update fields are name, role, title, reportsTo, capabilities, "
       "adapterType, adapterConfig, runtimeConfig (heartbeat settings), budgetMonthlyCents, "
       "desiredSkills, metadata, and permissions (through the dedicated PATCH only)."),

 ("h3", "G7.3 Update, delete and lifecycle"),
 ("code",
  "paperclipai agent update <agent-id> --payload-json '{\"title\":\"Senior Builder\"}'\n"
  "paperclipai agent delete <agent-id> --yes\n"
  "\n"
  "paperclipai agent pause <agent-id>\n"
  "paperclipai agent resume <agent-id>\n"
  "paperclipai agent approve <agent-id>\n"
  "paperclipai agent terminate <agent-id>"),
 ("p", "The documentation is explicit about which of the two ends an agent's employment: "
       "\"agent terminate: Terminate an agent. Use this to retire a worker rather than "
       "deleting its record.\" Termination revokes all of the agent's API keys, and "
       "\"Terminated agents are hidden from list and org-chart responses\" though they remain "
       "fetchable by direct ID. Deletion is a hard delete with runtime-state cleanup."),
 ("note", "Pause and heartbeat-off are NOT the same thing, and confusing them produces an "
          "agent that appears broken. With HEARTBEAT OFF, timer ticks stop but the agent "
          "still wakes on assignment, on comment, on routine and on demand, and still shows "
          "as active. With PAUSED, nothing wakes it at all and it does not show as active."),

 ("h3", "G7.4 Waking an agent"),
 ("code",
  "paperclipai agent wake <agent-id-or-shortname> \\\n"
  "  --company-id <company-id> \\\n"
  "  --reason \"Pick up the new spec\" \\\n"
  "  --payload '{\"issueId\":\"<issue-id>\"}'"),
 ("table", ("agent wake flags",
   ["Flag", "Use"],
   [["--source <source>", "\"Invocation source: timer, assignment, on_demand, or automation. "
     "Defaults to on_demand.\""],
    ["--trigger <trigger>", "\"Trigger detail: manual, ping, callback, or system. Defaults to "
     "manual.\""],
    ["--reason <text>", "\"Human-readable reason for the wakeup.\""],
    ["--payload <json>", "\"A JSON object passed to the run. Anything that is not a JSON "
     "object is rejected.\""],
    ["--idempotency-key <key>", "\"Dedupe key so a re-sent wakeup does not double-fire.\""],
    ["--force-fresh-session", "\"Request a fresh adapter session instead of resuming the "
     "existing one.\""]])),
 ("code",
  "paperclipai agent heartbeat:invoke <agent-id>\n"
  "paperclipai agent claude-login <agent-id>"),

 ("h3", "G7.5 Permissions, configuration and revisions"),
 ("code",
  "paperclipai agent permissions:update <agent-id> \\\n"
  "  --payload-json '{\"canCreateAgents\":true,\"canAssignTasks\":true}'\n"
  "\n"
  "paperclipai agent configuration <agent-id>\n"
  "paperclipai agent config-revisions <agent-id>\n"
  "paperclipai agent config-revision:get <agent-id> <revision-id>\n"
  "paperclipai agent config-revision:rollback <agent-id> <revision-id>"),
 ("p", "agent configuration returns the REDACTED configuration: \"Secrets are masked, so this "
       "is safe to print and share.\" Configuration revisions record the timestamp, changed "
       "keys and diffs, with up to the ten most recent shown; rollback restores the exact "
       "prior configuration atomically, and \"Rollbacks themselves saved as new revisions.\" "
       "The documented permission keys are agents:create, tasks:assign, tasks:assign_scope, "
       "environments:manage, users:invite, users:manage_permissions and joins:approve."),

 ("h3", "G7.6 Runtime state, sessions, skills and instructions"),
 ("code",
  "paperclipai agent runtime-state <agent-id>\n"
  "paperclipai agent runtime-state:reset-session <agent-id> --task-key <key>\n"
  "paperclipai agent task-sessions <agent-id>\n"
  "\n"
  "paperclipai agent skills <agent-id>\n"
  "paperclipai agent skills:sync <agent-id> --desired-skills paperclip,github\n"
  "\n"
  "paperclipai agent instructions-path:update <agent-id> \\\n"
  "  --payload-json "
  "'{\"path\":\"/tmp/AGENTS.md\",\"adapterConfigKey\":\"instructionsFilePath\"}'\n"
  "\n"
  "paperclipai agent instructions-bundle <agent-id>\n"
  "paperclipai agent instructions-bundle:update <agent-id> --payload-json "
  "'{\"mode\":\"managed\"}'\n"
  "\n"
  "paperclipai agent instructions-file:get <agent-id> --path AGENTS.md\n"
  "paperclipai agent instructions-file:put <agent-id> --path AGENTS.md "
  "--content-file ./AGENTS.md\n"
  "paperclipai agent instructions-file:delete <agent-id> --path AGENTS.md"),

 ("h3", "G7.7 local-cli — the laptop bootstrap and the once-only key"),
 ("p", "local-cli is the command that turns a local Claude Code or Codex install into a "
       "Paperclip agent runtime. Its documented process is: \"Mints a long-lived agent API "
       "key, installs bundled Paperclip skills into ~/.codex/skills and ~/.claude/skills as "
       "symlinks, prints shell export lines.\""),
 ("code",
  "paperclipai agent local-cli <agent-id-or-shortname> --company-id <company-id>\n"
  "paperclipai agent local-cli codexcoder --company-id <company-id> --key-name workstation\n"
  "paperclipai agent local-cli claudecoder --company-id <company-id> --no-install-skills"),
 ("table", ("agent local-cli flags",
   ["Flag", "Use"],
   [["-C, --company-id <id>", "\"Required. The company the agent belongs to.\""],
    ["--key-name <name>", "\"Label for the created API key. Defaults to local-cli.\""],
    ["--no-install-skills",
     "\"Skip installing skills into ~/.codex/skills and ~/.claude/skills.\""]])),
 ("note", "The once-only rule again, because this is where learners most often lose a key: "
          "\"The minted API key's plaintext token is shown **once**, in the command output. "
          "Treat the output as a secret, and revoke the key with token agent revoke when the "
          "local session is done.\""),
]

# ═══════════════════════════════════════════════════ G8. Run (heartbeat)

_G8 = [
 ("rule",),
 ("h2", "G8. Run commands — triggering and inspecting heartbeats"),

 ("p", "\"A _heartbeat run_ is a single server-side execution of an agent.\" The run family "
       "is where you go when you want to know what an agent actually did, as opposed to what "
       "it reported. Remember that these are observation commands: \"Agents do not run inside "
       "the CLI.\""),

 ("h3", "G8.1 Listing and watching"),
 ("code",
  "paperclipai run list --company-id <company-id>\n"
  "paperclipai run list --company-id <company-id> --agent-id <agent-id> --limit 50\n"
  "\n"
  "paperclipai run live --company-id <company-id>\n"
  "paperclipai run live --company-id <company-id> --limit 50 --min-count 5"),
 ("p", "run list accepts --agent-id <id> and --limit <n>. run live accepts --limit <n> and "
       "--min-count <n>. In text mode both print id, status, agentId, invocationSource, "
       "triggerDetail, startedAt, finishedAt and logBytes."),

 ("h3", "G8.2 Inspecting one run"),
 ("code",
  "paperclipai run get <run-id>\n"
  "paperclipai run events <run-id> --after-seq 0 --limit 200\n"
  "\n"
  "paperclipai run log <run-id> --offset 0 --limit-bytes 16384\n"
  "paperclipai run log <run-id> --text\n"
  "\n"
  "paperclipai run issues <run-id>\n"
  "paperclipai run cancel <run-id>\n"
  "paperclipai run workspace-operations <run-id>\n"
  "paperclipai run workspace-log <operation-id> --offset 0 --limit-bytes 16384\n"
  "paperclipai run workspace-log <operation-id> --text"),
 ("p", "run events accepts --after-seq <n> (default 0) and --limit <n> (default 200), and "
       "prints seq, eventType, stream, level and message. run log accepts --offset <bytes> "
       "(default 0), --limit-bytes <bytes> and --text. run workspace-operations prints id, "
       "status, phase, command, cwd and logBytes."),
 ("note", "Documented, and important when an agent has gone wrong: \"Cancelling a run does not "
          "roll back what the agent already did.\" Cancellation stops the execution; it does "
          "not undo the files written, the comments posted or the money spent."),

 ("h3", "G8.3 Watchdog decisions"),
 ("code",
  "paperclipai run watchdog-decision <run-id> --decision continue --reason \"text\"\n"
  "paperclipai run watchdog-decision <run-id> --decision snooze "
  "--snoozed-until 2026-06-01T18:00:00Z\n"
  "paperclipai run watchdog-decision <run-id> --decision dismissed_false_positive "
  "--evaluation-issue-id <id>"),

 ("h3", "G8.4 Triggering a single heartbeat and watching it"),
 ("p", "The setup-commands page documents a dedicated command for the case where you want to "
       "watch ONE run unfold rather than fire and forget."),
 ("code",
  "paperclipai heartbeat run --agent-id <agent-id>\n"
  "paperclipai heartbeat run --agent-id <agent-id> --source on_demand --trigger manual\n"
  "paperclipai heartbeat run --agent-id <agent-id> --timeout-ms 120000 --debug"),
 ("table", ("paperclipai heartbeat run flags",
   ["Flag", "Use"],
   [["-a, --agent-id <agentId>", "Required. Agent to invoke"],
    ["--source <source>",
     "timer, assignment, on_demand, automation (default on_demand)"],
    ["--trigger <trigger>", "manual, ping, callback, system (default manual)"],
    ["--timeout-ms <ms>",
     "Max wait time before timeout (default 0 = no client-side timeout)"],
    ["--json", "Output raw JSON"],
    ["--debug", "Show raw adapter stdout/stderr JSON chunks"]])),
 ("note", "Documented tip: \"For routine agent wake-ups during normal operation, prefer agent "
          "wake and the prompt-handoff flow in prompt. Reach for heartbeat run when you "
          "specifically want to watch a single run unfold.\""),
 ("p", "Common flags across all run subcommands are --data-dir <path>, --api-base <url>, "
       "--api-key <token>, --context <path>, --profile <name>, --json, and -C, --company-id "
       "<id> for list and live."),
]

# ═════════════════════════════════════════════════════════ G9. Routine

_G9 = [
 ("rule",),
 ("h2", "G9. Routine commands"),

 ("p", "Routines are recurring work that happens without anyone asking. The framing is the "
       "documentation's own: \"A routine does not do the work itself. It creates a run, and "
       "that run usually creates or links to an execution issue for the assigned agent.\" "
       "These commands create, configure, fire and observe routines through the API — they do "
       "not execute the work themselves."),

 ("h3", "G9.1 Two command groups — routine and routines"),
 ("table", ("The singular and plural groups are NOT the same thing",
   ["Group", "Talks to", "Use it when"],
   [["routine (singular)", "The control-plane REST API",
     "Day-to-day: list, create, update, fire, and inspect routines and their triggers."],
    ["routines (plural)", "The configured local database directly",
     "Local maintenance only — pausing every routine in one company on a local instance."]])),

 ("h3", "G9.2 The routine family"),
 ("code",
  "paperclipai routine list --company-id <company-id>\n"
  "paperclipai routine list --company-id <company-id> --project-id <project-id>\n"
  "\n"
  "paperclipai routine get <routine-id>\n"
  "\n"
  "paperclipai routine create --company-id <company-id> --payload-json '{\n"
  "  \"name\": \"Nightly status digest\",\n"
  "  \"description\": \"Summarize the day's closed issues\",\n"
  "  \"status\": \"active\"\n"
  "}'\n"
  "\n"
  "paperclipai routine update <routine-id> --payload-json '{\"status\": \"paused\"}'\n"
  "\n"
  "paperclipai routine revisions <routine-id>\n"
  "paperclipai routine revision:restore <routine-id> <revision-id>\n"
  "\n"
  "paperclipai routine runs <routine-id>\n"
  "paperclipai routine runs <routine-id> --limit 50\n"
  "\n"
  "paperclipai routine run <routine-id>\n"
  "paperclipai routine run <routine-id> --payload-json "
  "'{\"reason\": \"manual smoke test\"}'"),
 ("table", ("routine flags",
   ["Command", "Flag", "Use"],
   [["routine list", "-C, --company-id <id>",
     "Company to list routines for. Required (falls back to your context's company)."],
    ["routine list", "--project-id <id>",
     "Filter to routines attached to a single project."],
    ["routine create", "-C, --company-id <id>", "Company to create the routine in. Required."],
    ["routine create", "--payload-json <json>",
     "Routine definition as a JSON string. Required."],
    ["routine update", "--payload-json <json>",
     "Fields to update as a JSON string. Required."],
    ["routine runs", "--limit <n>",
     "Cap the number of runs returned. Omit for the server default."],
    ["routine run", "--payload-json <json>", "Run input as a JSON string. Defaults to {}."]])),

 ("h3", "G9.3 Triggers"),
 ("code",
  "paperclipai routine trigger:create <routine-id> --payload-json '{\n"
  "  \"kind\": \"schedule\",\n"
  "  \"schedule\": \"0 7 * * *\"\n"
  "}'\n"
  "paperclipai routine trigger:update <trigger-id> --payload-json "
  "'{\"schedule\": \"0 */2 * * *\"}'\n"
  "paperclipai routine trigger:delete <trigger-id>\n"
  "paperclipai routine trigger:rotate-secret <trigger-id>\n"
  "paperclipai routine trigger:fire <public-id>\n"
  "paperclipai routine trigger:fire <public-id> --payload-json "
  "'{\"event\": \"deploy.finished\"}'"),
 ("table", ("Trigger kinds",
   ["Trigger kind", "Fires the routine when...", "Notes"],
   [["schedule", "A cron/recurrence schedule is due.",
     "The standard \"run nightly / hourly / weekly\" trigger. Its behaviour under overlap and "
     "missed windows is governed by concurrency and catch-up."],
    ["webhook", "An external system POSTs to the trigger's webhook URL.",
     "Carries a secret you can rotate. Use it to turn inbound events into Paperclip work."],
    ["api (public)", "A caller fires its public endpoint by publicId.",
     "Fired with routine trigger:fire; the public id is shareable without exposing the "
     "routine id."]])),
 ("note", "An argument trap worth circling: trigger:update, trigger:delete and "
          "trigger:rotate-secret take the TRIGGER id, not the routine id. trigger:fire takes "
          "the publicId. And routine revision:restore takes its arguments positionally in "
          "order — routine id first, then revision id."),

 ("h3", "G9.4 The payload-json shape"),
 ("p", "The routine CLI passes --payload-json straight through to the REST API, so the API "
       "reference is the authority on the fields it accepts."),
 ("table", ("POST /api/companies/{companyId}/routines body",
   ["Field", "Required", "Notes"],
   [["title", "yes", "Routine name. Can use routine variables in the text."],
    ["description", "no", "Human-readable routine description. Can also use variables."],
    ["assigneeAgentId", "yes", "Agent who receives each run."],
    ["projectId", "no", "Project to associate with the routine."],
    ["goalId", "no", "Goal to link routine-created work to."],
    ["parentIssueId", "no", "Parent issue for routine-created execution issues."],
    ["priority", "no", "critical, high, medium default, low."],
    ["status", "no",
     "Defaults to active when an assignee exists, otherwise paused."],
    ["concurrencyPolicy", "no", "Defaults to coalesce_if_active."],
    ["catchUpPolicy", "no", "Defaults to skip_missed."],
    ["activityGatePolicy", "no", "always (default) or require_external_activity."],
    ["activityGateScope", "no",
     "company (default) or project. Only used when the policy is "
     "require_external_activity."],
    ["variables", "no",
     "Template variables for the routine title, description, and run payloads."]])),
 ("table", ("POST /api/routines/{routineId}/run body",
   ["Field", "Required", "Notes"],
   [["source", "no", "Defaults to manual. The code also accepts api."],
    ["triggerId", "no", "If present, it must belong to the routine and be enabled."],
    ["payload", "no", "Arbitrary JSON payload stored on the run."],
    ["variables", "no", "Explicit variable overrides."],
    ["projectId", "no", "Overrides the routine's project for this run."],
    ["assigneeAgentId", "no", "Overrides the routine's default assignee for this run."],
    ["idempotencyKey", "no",
     "Deduplicates repeated requests with the same source/trigger combination."],
    ["executionWorkspaceId", "no", "Optional workspace binding for the created issue."],
    ["executionWorkspacePreference", "no",
     "Optional workspace preference for the created issue."],
    ["executionWorkspaceSettings", "no",
     "Optional workspace settings object for the created issue."]])),
 ("code",
  "// schedule trigger payload\n"
  "{\n"
  "  \"kind\": \"schedule\",\n"
  "  \"label\": \"Monday morning\",\n"
  "  \"enabled\": true,\n"
  "  \"cronExpression\": \"0 9 * * 1\",\n"
  "  \"timezone\": \"Europe/Amsterdam\"\n"
  "}\n"
  "\n"
  "// webhook trigger payload\n"
  "{\n"
  "  \"kind\": \"webhook\",\n"
  "  \"label\": \"Stripe event bridge\",\n"
  "  \"enabled\": true,\n"
  "  \"signingMode\": \"bearer\",\n"
  "  \"replayWindowSec\": 300\n"
  "}\n"
  "\n"
  "// api trigger payload\n"
  "{\n"
  "  \"kind\": \"api\"\n"
  "}"),

 ("h3", "G9.5 Statuses and run outcomes"),
 ("table", ("Routine status values",
   ["Status", "Meaning"],
   [["active", "The routine can fire and create runs."],
    ["paused", "The routine is stored but does not fire automatically."],
    ["archived", "The routine is retired. Archived routines do not fire."]])),
 ("table", ("Routine run statuses",
   ["Status", "Meaning"],
   [["received", "The run was accepted and is being processed."],
    ["coalesced", "A live execution already existed, so this run linked to it."],
    ["skipped", "The run did not create work. Read failureReason to tell the causes apart."],
    ["issue_created", "A new execution issue was created."],
    ["completed", "The execution issue later moved to done."],
    ["failed", "The execution issue failed, was cancelled, or the dispatch failed."]])),

 ("h3", "G9.6 disable-all — the plural group"),
 ("code",
  "paperclipai routines disable-all --company-id <company-id>\n"
  "paperclipai routines disable-all --company-id <company-id> --json"),
 ("table", ("routines disable-all flags",
   ["Flag", "Use"],
   [["-C, --company-id <id>",
     "Company whose routines to pause. Required (falls back to PAPERCLIP_COMPANY_ID)."],
    ["-c, --config <path>", "Path to the Paperclip config file, if not the default."],
    ["-d, --data-dir <path>",
     "Paperclip data directory root, to isolate state from ~/.paperclip."],
    ["--json", "Output the raw result object instead of a human summary."]])),
 ("code",
  "Paused 3 routine(s) for company <company-id> (1 already paused, 0 archived)."),
 ("p", "With --json the command returns companyId, totalRoutines, pausedCount, "
       "alreadyPausedCount and archivedCount. Its precise behaviour is: reads every routine "
       "for the company from the LOCAL database; sets each routine whose status is not "
       "already paused or archived to paused; leaves already-paused and archived routines "
       "untouched."),
 ("note", "Documented warning, and the reason this command belongs in a reference rather than "
          "a habit: \"disable-all operates on the **local** instance's database... It is not "
          "the way to pause routines on a remote control plane — for that, pause each routine "
          "with routine update <routine-id> --payload-json '{\"status\":\"paused\"}'. There is "
          "no bulk re-enable command: turn routines back on individually with routine update "
          "once you have resolved the problem.\""),

 ("h3", "G9.7 Revisions, limits and the rules that surprise people"),
 ("bullets", [
   "\"Every update creates a new revision.\"",
   "revision:restore \"does not rewind history — it makes the chosen revision the current "
   "definition by creating a new latest revision from it, so the rollback is itself "
   "auditable.\"",
   "trigger:rotate-secret: \"The old secret stops working once rotated, so update the caller "
   "that posts to the webhook in the same change.\"",
   "GET /api/routines/{routineId}/runs: \"The limit defaults to 50 and is capped at 200.\"",
   "Replay windows \"must be between 30 and 86,400 seconds. The default is 300 seconds.\"",
   "POST /api/routines/{routineId}/run returns 202 Accepted.",
   "\"You cannot have an active routine without an assignee agent.\" The API normalises to "
   "paused or rejects the activation.",
   "\"Agents can only create routines assigned to themselves.\"",
   "\"Schedule triggers only work if the routine's required variables can be resolved.\"",
   "The webhook trigger's webhookUrl and webhookSecret are \"only shown to you when the "
   "trigger is created or when the secret is rotated.\"",
 ]),
 ("p", "Webhook signing modes are bearer, hmac_sha256, github_hmac and none; \"The default is "
       "bearer.\" The accepted headers per mode are: bearer uses Authorization: Bearer "
       "<secret>; hmac_sha256 uses X-Paperclip-Signature or X-Hub-Signature-256; github_hmac "
       "uses X-Hub-Signature-256 or X-Paperclip-Signature plus X-Paperclip-Timestamp; none "
       "requires no signature."),
 ("note", "The activity gate has one behaviour that reads as a bug until you know it: \"A "
          "routine set to activityGateScope: \"project\" without a projectId can never match "
          "anything, so it will never fire on a schedule. Set a project first.\" The gate is "
          "also \"only consulted for scheduled ticks. Webhook firings and manual runs through "
          "POST /api/routines/{routineId}/run dispatch regardless of the policy.\""),
 ("p", "The documented wiring order is: 1. create the routine; 2. attach a schedule or webhook "
       "trigger; 3. inspect the created webhook material if needed; 4. list runs to confirm "
       "the routine is firing as expected. Routine-created issues are found by filtering "
       "issues on originKind=routine_execution."),
]

# ════════════════════════════════════════════════════════ G10. Approval

_G10 = [
 ("rule",),
 ("h2", "G10. Approval commands"),

 ("p", "\"Approvals are the governance layer that sits between what an agent _wants_ to do and "
       "what it is _allowed_ to do.\" The family is small and the semantics are the whole "
       "point: three different ways of saying no, only one of which is final."),
 ("note", "Documented note on persona: \"Approvals are decided with a **board** persona. An "
          "agent persona is scoped to one company and one agent and is the side that "
          "_requests_ an approval; clearing the queue is board work.\""),

 ("h3", "G10.1 The command set"),
 ("table", ("Approval commands",
   ["Command", "What it does"],
   [["approval list", "List approvals for a company, optionally filtered by status."],
    ["approval get", "Fetch one approval by ID."],
    ["approval create", "Create an approval request for a governed action."],
    ["approval approve", "Approve a pending request."],
    ["approval reject", "Reject a request."],
    ["approval request-revision",
     "Send the request back to the requester for changes."],
    ["approval resubmit", "Resubmit a request, optionally with a new payload."],
    ["approval comment", "Add a comment to an approval."]])),
 ("code",
  "paperclipai approval list --company-id <company-id>\n"
  "paperclipai approval list --company-id <company-id> --status pending\n"
  "paperclipai approval list --company-id <company-id> --status pending --json\n"
  "\n"
  "paperclipai approval get <approval-id>\n"
  "\n"
  "paperclipai approval create \\\n"
  "  --company-id <company-id> \\\n"
  "  --type hire_agent \\\n"
  "  --payload '{\"name\":\"CTO\",\"role\":\"engineering_lead\"}' \\\n"
  "  --requested-by-agent-id <agent-id> \\\n"
  "  --issue-ids <issue-id-1>,<issue-id-2>\n"
  "\n"
  "paperclipai approval approve <approval-id> --decision-note "
  "\"Cleared budget; proceed with the hire.\"\n"
  "paperclipai approval reject <approval-id> --decision-note "
  "\"Out of scope for this quarter.\"\n"
  "paperclipai approval request-revision <approval-id> --decision-note "
  "\"Tighten the role to backend only, then resubmit.\"\n"
  "\n"
  "# Resubmit unchanged\n"
  "paperclipai approval resubmit <approval-id>\n"
  "# Resubmit with a corrected payload\n"
  "paperclipai approval resubmit <approval-id> --payload "
  "'{\"name\":\"CTO\",\"role\":\"backend_lead\"}'\n"
  "\n"
  "paperclipai approval comment <approval-id> --body "
  "\"What is the projected monthly cost of this hire?\""),

 ("h3", "G10.2 Flags"),
 ("table", ("approval create flags",
   ["Flag", "Use"],
   [["-C, --company-id <id>", "Required. The company the approval belongs to."],
    ["--type <type>", "Required. The approval type: hire_agent or approve_ceo_strategy."],
    ["--payload <json>",
     "Required. The approval payload as a JSON object (not an array or scalar)."],
    ["--requested-by-agent-id <id>", "The agent making the request."],
    ["--issue-ids <csv>", "Comma-separated issue IDs to link to the approval."]])),
 ("table", ("Decision flags (shared by approve, reject, request-revision)",
   ["Flag", "Use"],
   [["--decision-note <text>", "A short note explaining the decision."],
    ["--decided-by-user-id <id>", "The user ID to attribute the decision to."]])),
 ("p", "approval resubmit takes --payload <json>, \"An optional replacement payload, as a JSON "
       "object.\" approval comment takes --body <text>, \"Required. The comment text.\" "
       "approval list takes -C, --company-id <id> (required) and --status <status>, which "
       "filters to a single status such as pending."),

 ("h3", "G10.3 The worked triage sequence"),
 ("p", "The documentation gives a complete triage loop. Learn this shape; it is the sequence "
       "you will actually run every morning."),
 ("code",
  "# 1. See what is waiting\n"
  "paperclipai approval list --company-id <company-id> --status pending\n"
  "\n"
  "# 2. Inspect the one that needs attention\n"
  "paperclipai approval get <approval-id> --json\n"
  "\n"
  "# 3a. If it's good, approve it\n"
  "paperclipai approval approve <approval-id> --decision-note \"Approved.\"\n"
  "\n"
  "# 3b. If it needs work, send it back\n"
  "paperclipai approval request-revision <approval-id> --decision-note "
  "\"Narrow the scope, then resubmit.\"\n"
  "\n"
  "# 4. The requester fixes and resubmits\n"
  "paperclipai approval resubmit <approval-id> --payload '{\"...\":\"...\"}'"),
 ("table", ("Which decision to reach for",
   ["Command", "When to reach for it"],
   [["approve", "The request is sound and you authorise the action."],
    ["reject", "The request should not proceed at all."],
    ["request-revision", "The request is close but needs changes — sends it back to the "
     "requester rather than killing it."]])),
 ("note", "Documented tips: \"Start every triage session with approval list --status pending. "
          "It is the shortest route from 'what needs me' to a decision.\" And: \"A short, "
          "concrete decision note is worth more than a long one. The requester should be able "
          "to act on your feedback without guessing — that is the entire point of "
          "request-revision.\" Use comments to negotiate details before you decide; reserve "
          "request-revision for the moment you actually want the proposal changed."),

 ("h3", "G10.4 Types, state machine and gotchas"),
 ("table", ("Approval types (API enum)",
   ["Type", "Meaning"],
   [["hire_agent", "New agent hire or pending activation needs board review"],
    ["approve_ceo_strategy", "CEO strategy proposal requires approval before execution"],
    ["budget_override_required", "Budget action needs board intervention"],
    ["request_board_approval", "General agent/workflow request for board review"]])),
 ("p", "The CLI approval page documents only two values on --type: hire_agent and "
       "approve_ceo_strategy. The other two appear in the API's approval-type enum. The state "
       "machine is: pending -> approved / rejected / revision_requested -> pending."),
 ("bullets", [
   "Scope: \"The company-scoped subcommands (list, create) additionally require -C, "
   "--company-id. Single-approval subcommands operate on an approval ID and do not need a "
   "company.\" approval get is \"company-agnostic — the approval ID is globally addressable\".",
   "--payload \"is parsed as JSON and must be a JSON object — passing a list or a bare string "
   "is rejected with an Invalid payload JSON error.\"",
   "--issue-ids \"is split on commas, trimmed, and blank entries dropped.\"",
   "Documented warning: \"Quote the --payload value as a single shell argument and keep the "
   "JSON valid. A truncated or array-shaped payload fails before the request ever reaches the "
   "server.\"",
   "Board-only endpoints: approve, reject, request-revision. Agents cannot resubmit others' "
   "approvals.",
   "\"Approvals don't expire on their own. If an approval is pending, agents that are waiting "
   "on it will pause at that point until you take action.\"",
 ]),
]

# ═══════════════════════════════════════════ G11. Cost, finance, budget

_G11 = [
 ("rule",),
 ("h2", "G11. Cost, finance and budget commands"),

 ("p", "There is no separate budget reference page — budget commands live on the cost page, "
       "and the three groups are designed to be used together. The framing sentence is worth "
       "quoting in full: \"This is the single most important part of running a company "
       "headlessly: set budgets before you turn agents loose, not after.\""),

 ("h3", "G11.1 Cost reads"),
 ("code",
  "paperclipai cost summary --company-id <company-id>\n"
  "paperclipai cost by-agent --company-id <company-id>\n"
  "paperclipai cost by-agent-model --company-id <company-id>\n"
  "paperclipai cost by-provider --company-id <company-id>\n"
  "paperclipai cost by-biller --company-id <company-id>\n"
  "paperclipai cost by-project --company-id <company-id>\n"
  "paperclipai cost window-spend --company-id <company-id>\n"
  "paperclipai cost quota-windows --company-id <company-id>\n"
  "\n"
  "paperclipai cost issue <issue-id>\n"
  "paperclipai cost event:create --company-id <company-id> --payload-json '{...}'"),
 ("table", ("What each cost command answers",
   ["Command", "Answers"],
   [["cost summary", "The headline total for the company. Start here."],
    ["cost by-agent", "Which agents are spending. Use it to spot a runaway agent."],
    ["cost by-agent-model", "Spend per agent broken down by the model each one used. The "
     "finest view for tuning model choices."],
    ["cost by-provider", "Spend grouped by upstream provider."],
    ["cost by-biller", "Spend grouped by who is billed."],
    ["cost by-project",
     "Spend grouped by project, so you can attribute cost to the work that incurred it."],
    ["cost window-spend", "Spend inside the current rolling budget windows — the number a "
     "budget policy actually checks against."],
    ["cost quota-windows",
     "The configured quota windows themselves (their periods and limits)."]])),

 ("h3", "G11.2 Finance"),
 ("code",
  "paperclipai finance event:create --company-id <company-id> --payload-json '{...}'\n"
  "paperclipai finance events --company-id <company-id>\n"
  "paperclipai finance summary --company-id <company-id>\n"
  "paperclipai finance by-biller --company-id <company-id>\n"
  "paperclipai finance by-kind --company-id <company-id>"),
 ("table", ("Finance commands",
   ["Command", "Use"],
   [["finance event:create", "Record a finance event. --payload-json is required and POSTed "
     "to the company's finance-events endpoint."],
    ["finance events", "List the recorded finance events for the company."],
    ["finance summary", "The aggregate finance picture for the company."],
    ["finance by-biller", "Finance totals grouped by biller."],
    ["finance by-kind", "Finance totals grouped by event kind."]])),

 ("h3", "G11.3 Budget"),
 ("code",
  "paperclipai budget overview --company-id <company-id>\n"
  "paperclipai budget policy:upsert --company-id <company-id> --payload-json '{...}'\n"
  "paperclipai budget company:update --company-id <company-id> --payload-json "
  "'{\"...\":\"...\"}'\n"
  "paperclipai budget agent:update <agent-id> --payload-json '{\"...\":\"...\"}'\n"
  "paperclipai budget incident:resolve <incident-id> --company-id <company-id>\n"
  "paperclipai budget incident:resolve <incident-id> --company-id <company-id> "
  "--payload-json '{\"...\":\"...\"}'"),
 ("table", ("Which endpoint each budget command reaches",
   ["Command", "Underlying call"],
   [["cost event:create", "POSTs to the company's cost-events endpoint."],
    ["finance event:create", "POSTs to the company's finance-events endpoint."],
    ["budget policy:upsert",
     "POSTs --payload-json to the company's budgets/policies endpoint."],
    ["budget company:update",
     "PATCHes the company's budget with an UpdateBudget JSON payload."],
    ["budget agent:update <agent-id>",
     "PATCHes a single agent's budget with an UpdateBudget JSON payload."],
    ["budget incident:resolve", "POSTs to budget-incidents/<incident-id>/resolve; payload "
     "type ResolveBudgetIncident."]])),

 ("h3", "G11.4 The documented budget workflow"),
 ("bullets", [
   "1. budget policy:upsert — define the windows and limits before any agent runs.",
   "2. budget company:update — set the company-wide ceiling.",
   "3. budget agent:update <agent-id> — give individual agents tighter or looser room as "
   "needed.",
   "4. budget overview and cost window-spend — confirm the guard rails read the way you "
   "expect.",
   "5. While the company runs, monitor with cost summary, cost by-agent, and cost "
   "window-spend.",
   "6. When an incident fires, triage with cost by-agent, adjust the relevant budget, then "
   "budget incident:resolve <incident-id>.",
 ]),

 ("h3", "G11.5 Scope, flags and gotchas"),
 ("bullets", [
   "\"Every read is non-destructive; the only commands that change state are event:create, "
   "policy:upsert, company:update, agent:update, and incident:resolve.\"",
   "Two commands are scoped by POSITIONAL argument and take no --company-id: cost issue "
   "<issue-id> and budget agent:update <agent-id>.",
   "cost issue accepts an issue id or human identifier — \"such as PAP-39\".",
   "budget company:update and budget incident:resolve require a company before they will run.",
   "budget incident:resolve's --payload-json is optional and defaults to {}.",
   "cost event:create and finance event:create require --payload-json (a valid JSON object).",
   "\"Most cost is recorded automatically by the server-side runtime as agents run.\"",
 ]),
 ("note", "Documented warnings. On JSON: \"--payload-json is parsed with JSON.parse. Malformed "
          "JSON fails the command before any request is sent. Quote the whole value in single "
          "quotes in your shell so embedded double quotes survive.\" On incidents: \"Resolving "
          "an incident clears the gate it raised. If the underlying overspend is still in "
          "progress, resolve it only after you have also adjusted the policy with budget "
          "policy:upsert, company:update, or agent:update — otherwise the incident will simply "
          "recur on the next run.\""),
 ("p", "One relationship is easy to get backwards: \"A company-wide budget and per-agent "
       "budgets work together. Tightening one agent does not raise the company ceiling, and "
       "the company ceiling still bounds the sum of all agents.\" And the fastest triage path "
       "is stated for you: \"When a budget alert fires, the fastest triage path is cost "
       "window-spend to see how far over you are, then cost by-agent to find the source.\""),
]

# ═══════════════════════════════════════════════════════ G12. Workspace

_G12 = [
 ("rule",),
 ("h2", "G12. Workspace, org and environment commands"),

 ("p", "\"Execution workspaces are the server-side sandboxes where heartbeat runs do their "
       "work.\" This page groups four related families — org chart rendering, agent "
       "configurations, execution workspaces and environments, plus project workspaces. All "
       "of them are \"read-and-control wrappers over the Paperclip API. They TRIGGER and "
       "OBSERVE server-side state; the actual execution... runs on the Paperclip runtime, not "
       "in the CLI.\""),

 ("h3", "G12.1 Org chart"),
 ("code",
  "paperclipai org get --company-id <company-id>\n"
  "paperclipai org svg --company-id <company-id> --out org.svg\n"
  "paperclipai org png --company-id <company-id> --out org.png\n"
  "paperclipai org png -C <company-id> > org.png"),
 ("p", "org get returns the org chart as structured JSON; org svg and org png return rendered "
       "images. \"With --out <path>, the bytes are written to that file and the command prints "
       "a small { out, bytes } summary. Without --out, the raw image bytes stream to stdout.\""),

 ("h3", "G12.2 Agent configurations"),
 ("code", "paperclipai agent-config list --company-id <company-id>"),
 ("p", "agent-config list is company-scoped and read-only."),

 ("h3", "G12.3 Execution workspaces"),
 ("code",
  "paperclipai workspace list --company-id <company-id>\n"
  "paperclipai workspace get <execution-workspace-id>\n"
  "paperclipai workspace close-readiness <execution-workspace-id>\n"
  "paperclipai workspace operations <execution-workspace-id>\n"
  "paperclipai workspace update <execution-workspace-id> --payload-json '{...}'\n"
  "paperclipai workspace runtime-service <execution-workspace-id> start "
  "--payload-json '{...}'\n"
  "paperclipai workspace runtime-command <execution-workspace-id> run "
  "--payload-json '{...}'\n"
  "\n"
  "paperclipai workspace runtime-service <execution-workspace-id> restart "
  "--payload-json '{\"service\":\"dev-server\"}'\n"
  "paperclipai workspace runtime-command <execution-workspace-id> run "
  "--payload-json '{\"command\":\"npm test\"}'"),
 ("table", ("workspace subcommands",
   ["Command", "Arguments", "Use"],
   [["list", "--company-id <id>", "List all execution workspaces in a company."],
    ["get", "<id>", "Fetch a single execution workspace."],
    ["close-readiness", "<id>",
     "Check whether the workspace is safe to close (no in-flight work that would be lost)."],
    ["operations", "<id>", "List the workspace's operation history."],
    ["update", "<id> --payload-json <json>", "Patch the workspace with a JSON body."],
    ["runtime-service", "<id> <action> [--payload-json <json>]",
     "Control a runtime service in the workspace."],
    ["runtime-command", "<id> <action> [--payload-json <json>]",
     "Run a runtime command in the workspace."]])),
 ("p", "The <action> for runtime-service and runtime-command is one of start, stop, restart or "
       "run — for both workspace and project-workspace. The --payload-json for those runtime "
       "commands defaults to {} when omitted."),
 ("note", "Documented warning: \"runtime-service stop/restart act on live runtime processes a "
          "run may be depending on. Confirm with workspace get and workspace operations that "
          "nothing critical is mid-flight first.\" And the tip: \"Run workspace "
          "close-readiness <id> before you tear down or close a workspace. It tells you "
          "whether closing it now would interrupt active work.\""),

 ("h3", "G12.4 Environments"),
 ("code",
  "paperclipai environment list --company-id <company-id>\n"
  "paperclipai environment capabilities --company-id <company-id>\n"
  "paperclipai environment create --company-id <company-id> --payload-json '{...}'\n"
  "paperclipai environment get <environment-id>\n"
  "paperclipai environment leases <environment-id>\n"
  "paperclipai environment lease <lease-id>\n"
  "paperclipai environment update <environment-id> --payload-json '{...}'\n"
  "paperclipai environment delete <environment-id>\n"
  "paperclipai environment probe <environment-id>\n"
  "paperclipai environment probe-config --company-id <company-id> --payload-json '{...}'\n"
  "\n"
  "# Validate a config before committing it, then create the environment.\n"
  "paperclipai environment probe-config --company-id <company-id> --payload-json "
  "'{\"kind\":\"ssh\",\"host\":\"build-01.internal\"}'\n"
  "paperclipai environment create --company-id <company-id> --payload-json "
  "'{\"name\":\"build-01\",\"kind\":\"ssh\",\"host\":\"build-01.internal\"}'\n"
  "paperclipai environment probe <environment-id>"),
 ("table", ("environment subcommands",
   ["Command", "Arguments", "Use"],
   [["list", "--company-id <id>", "List a company's environments."],
    ["capabilities", "--company-id <id>",
     "Report the environment capabilities available to the company."],
    ["create", "--company-id <id> --payload-json <json>",
     "Create an environment from a JSON body."],
    ["get", "<environment-id>", "Fetch a single environment."],
    ["leases", "<environment-id>", "List the leases held against an environment."],
    ["lease", "<lease-id>", "Fetch a single environment lease by its own id."],
    ["update", "<environment-id> --payload-json <json>",
     "Patch an environment with a JSON body."],
    ["delete", "<environment-id>", "Delete an environment."],
    ["probe", "<environment-id>", "Probe an existing environment for reachability/health."],
    ["probe-config", "--company-id <id> --payload-json <json>",
     "Probe a candidate config before you create the environment."]])),
 ("p", "\"A lease is a claim on an environment by a workspace.\" environment lease <lease-id> "
       "hits /api/environment-leases/{leaseId}."),
 ("note", "Documented tip: \"probe-config is the dry-run path — it checks a candidate "
          "configuration without persisting anything. probe validates an environment that "
          "already exists. Probe first, create second.\""),

 ("h3", "G12.5 Project workspaces"),
 ("code",
  "paperclipai project-workspace list <project-id>\n"
  "paperclipai project-workspace create <project-id> --payload-json '{...}'\n"
  "paperclipai project-workspace update <project-id> <workspace-id> --payload-json '{...}'\n"
  "paperclipai project-workspace delete <project-id> <workspace-id>\n"
  "paperclipai project-workspace runtime-service <project-id> <workspace-id> restart "
  "--payload-json '{...}'\n"
  "paperclipai project-workspace runtime-command <project-id> <workspace-id> run "
  "--payload-json '{...}'\n"
  "\n"
  "paperclipai project-workspace runtime-command <project-id> <workspace-id> run "
  "--payload-json '{\"command\":\"pnpm build\"}'"),
 ("note", "Documented note on argument order: \"update requires the workspace id positional — "
          "the command rejects the call if you omit it. create takes only the project id, "
          "since the workspace does not exist yet.\""),
 ("p", "Every command in this family accepts --data-dir, --api-base, --api-key, --context, "
       "--profile and --json; company-scoped ones also take -C, --company-id <id>; \"ID- and "
       "project-scoped subcommands take the id as a positional argument instead.\""),
]

# ══════════════════════════════════════════════════════════ G13. Skills

_G13 = [
 ("rule",),
 ("h2", "G13. Skills commands"),

 ("p", "\"Skills are how you teach an agent a repeatable procedure (open a pull request, run a "
       "browser, follow a review checklist) without rewriting its prompt every time.\" Two "
       "command groups exist: a plural skills group with reference resolution and safety "
       "prompts, and a singular skill group that is lower-level and payload-driven."),

 ("h3", "G13.1 The three operations"),
 ("table", ("What each operation changes",
   ["Operation", "Commands", "What it changes"],
   [["Company install", "skills install, import, create, scan-projects",
     "Adds or updates a skill in the company's library. Available to the whole company; does "
     "NOT attach it to any agent."],
    ["Agent attach", "skills agent sync, skills agent clear",
     "Changes an agent's DESIRED company-skill set. sync takes a required --mode (add, "
     "remove, or replace); clear empties it."],
    ["Adapter runtime sync", "reported by skills agent list; triggered by sync/clear",
     "The server-side adapter reconciles the desired set with files on disk and returns an "
     "AgentSkillSnapshot."]])),
 ("note", "The distinction between install and attach is the one learners most often collapse. "
          "Installing a skill puts it in the company library. It does nothing for any agent "
          "until you ATTACH it. \"Bundled Paperclip skills still live in the company library "
          "as read-only entries, but the server no longer force-attaches them to an agent.\""),

 ("h3", "G13.2 Catalog"),
 ("code",
  "paperclipai skills browse --kind bundled --category github\n"
  "paperclipai skills search \"pull request\" --kind bundled\n"
  "paperclipai skills inspect github-pr-workflow\n"
  "\n"
  "paperclipai skills install github-pr-workflow --company-id <company-id>\n"
  "paperclipai skills install github-pr-workflow --as review-prs "
  "--company-id <company-id>"),
 ("table", ("Browse/search filters and install flags",
   ["Flag", "Use"],
   [["--kind <kind>", "Filter by catalog kind: bundled or optional."],
    ["--category <slug>", "Filter by catalog category slug."],
    ["--query <text>",
     "Free-text search (browse only; search uses its positional argument)."],
    ["--as <slug>", "(install) Override the company skill slug."],
    ["--force", "(install) Replace a same-key catalog-managed skill when the server allows "
     "it. Never bypasses hard validation or hard-stop audit findings."]])),
 ("note", "Documented note: \"Catalog commands are for the app-shipped catalog only. GitHub, "
          "skills.sh, local-path, and plain-URL sources go through skills import instead.\""),

 ("h3", "G13.3 The company library — import and create"),
 ("code",
  "paperclipai skills list --company-id <company-id>\n"
  "paperclipai skills show <skill-ref> --company-id <company-id>\n"
  "paperclipai skills file <skill-ref> --path SKILL.md --company-id <company-id>\n"
  "paperclipai skills import <source> --company-id <company-id>\n"
  "paperclipai skills create --name \"Review PRs\" --slug review-prs --body-file SKILL.md "
  "--company-id <company-id>\n"
  "paperclipai skills scan-projects --project-id <project-id> --company-id <company-id>"),
 ("table", ("skills create options",
   ["Flag", "Use"],
   [["--name <name>", "Required. Skill name."],
    ["--slug <slug>", "Optional explicit slug."],
    ["--description <text>", "Optional description."],
    ["--body-file <path>", "Markdown body file. Use - to read the body from stdin."]])),
 ("p", "skills scan-projects takes --project-id <id> and --workspace-id <id>, each of which "
       "may be repeated. With neither supplied, the scan \"covers the company's projects and "
       "workspaces\". The import source formats accepted by the underlying endpoint include a "
       "GitHub repository URL, a tree or blob URL, an owner/repo shorthand, an "
       "owner/repo/skill shorthand, a skills.sh URL, an npx skills add command line, a plain "
       "URL to a SKILL.md and a local filesystem path."),
 ("code",
  "{ \"source\": \"https://github.com/paperclipai/paperclip\" }\n"
  "{ \"source\": \"https://github.com/paperclipai/paperclip/tree/main/skills/paperclip\" }\n"
  "{ \"source\": "
  "\"https://github.com/paperclipai/paperclip/blob/main/skills/paperclip/SKILL.md\" }\n"
  "{ \"source\": \"paperclipai/paperclip\" }\n"
  "{ \"source\": \"paperclipai/paperclip/paperclip-create-agent\" }\n"
  "{ \"source\": \"https://skills.sh/paperclipai/paperclip/paperclip-create-agent\" }\n"
  "{ \"source\": \"npx skills add paperclipai/paperclip --skill paperclip-create-agent\" }\n"
  "{ \"source\": \"https://example.com/raw/SKILL.md\" }\n"
  "{ \"source\": \"/Users/me/code/my-project/skills/code-review\" }"),

 ("h3", "G13.4 The maintenance loop"),
 ("code",
  "paperclipai skills check --company-id <company-id>\n"
  "paperclipai skills update <skill-ref> --company-id <company-id>\n"
  "paperclipai skills update --all --company-id <company-id>\n"
  "paperclipai skills audit <skill-ref> --company-id <company-id>\n"
  "paperclipai skills reset <skill-ref> --yes --company-id <company-id>\n"
  "paperclipai skills remove <skill-ref> --yes --company-id <company-id>"),
 ("table", ("Maintenance commands",
   ["Command", "Use"],
   [["check [skillRef]", "Report update status: supported, hasUpdate, currentRef/latestRef, "
     "installedHash/originHash, any updateHoldReason, and the auditVerdict."],
    ["update [skillRef]", "Install the pinned update for one skill."],
    ["update --all", "Check every skill and update only those with hasUpdate=true; "
     "supported-but-current and unsupported skills are skipped with a reason."],
    ["audit [skillRef]", "Re-scan installed bytes and report findings (severity, code, path, "
     "message) without executing anything."],
    ["reset <skillRef>",
     "Reinstall a catalog-managed skill from its pinned origin, discarding local edits."]])),
 ("p", "The skill reference is OPTIONAL on check, update and audit — omit it to operate over "
       "the whole library. --force discards local-modification and soft-audit holds, but hard-"
       "stop audit findings still block the operation; a fail verdict \"is what hard-blocks "
       "install-update\". --yes on reset confirms without the interactive prompt and is "
       "required when not in a TTY."),
 ("note", "Documented warning: \"Pass either a skill reference or --all to update, never both "
          "— the command rejects that combination.\""),

 ("h3", "G13.5 Attaching skills to an agent"),
 ("code",
  "paperclipai skills agent list <agent-ref> --company-id <company-id>\n"
  "paperclipai skills agent sync <agent-ref> --skill review-prs --skill agent-browser "
  "--mode add --company-id <company-id>\n"
  "paperclipai skills agent clear <agent-ref> --yes --company-id <company-id>"),
 ("table", ("Agent-attach flags",
   ["Flag", "Use"],
   [["--skill <skillRef>", "(sync) A desired company skill id, key, or slug. Repeat for "
     "several. At least one is required."],
    ["--mode <mode>", "(sync) Required. Merge mode: add keeps other skills; remove deletes "
     "only named skills; replace destructively overwrites the complete set."],
    ["--yes", "(clear) Confirm without the interactive prompt."]])),
 ("p", "The merge-mode semantics are unforgiving and worth reading twice: \"With --mode "
       "replace you must list the complete desired set every time — anything you omit is "
       "detached — while --mode add and --mode remove only touch the skills you name. clear "
       "detaches everything.\" skills agent clear \"empties the set outright (it uses replace "
       "internally with an empty list)\"."),
 ("table", ("Adapter sync modes reported by skills agent list",
   ["Mode", "Behaviour"],
   [["persistent",
     "Adapter writes files to working directory; leaves them between runs"],
    ["ephemeral", "Files materialised per run, cleaned up after"],
    ["unsupported",
     "Assignment recorded but cannot push files into runtime"]])),

 ("h3", "G13.6 The singular skill group"),
 ("code",
  "paperclipai skill list -C <company-id>\n"
  "paperclipai skill get <skill-id> -C <company-id>\n"
  "paperclipai skill file <skill-id> --path SKILL.md -C <company-id>\n"
  "paperclipai skill file:update <skill-id> --payload-json "
  "'{\"path\":\"SKILL.md\",\"content\":\"...\"}' -C <company-id>\n"
  "paperclipai skill update-status <skill-id> -C <company-id>\n"
  "paperclipai skill install-update <skill-id> -C <company-id>\n"
  "paperclipai skill delete <skill-id> -C <company-id>"),
 ("p", "The singular group \"does not resolve key/slug references — every subcommand takes a "
       "literal <skillId>.\" Its create, import and scan-projects subcommands all require "
       "--payload-json."),

 ("h3", "G13.7 Reference resolution and its failure modes"),
 ("bullets", [
   "<catalogRef> = catalog skill id, key, or a UNIQUE slug.",
   "<skillRef> resolves against the company library by id, canonical key, or UNIQUE slug. "
   "\"An ambiguous slug is rejected — use an id or key instead.\"",
   "<agentRef> = agent id or shortname/url-key.",
   "Server-side resolution order: exact UUID match on id, then normalised key match, then "
   "normalised slug match \"but only when exactly one skill in the company has that slug\".",
   "Ambiguous references fail with \"Invalid company skill selection (ambiguous references: "
   "<slug>; ...)\"; unknown ones with \"Invalid company skill selection (unknown references: "
   "<reference>; ...)\".",
   "skills remove and skills agent clear \"prompt for confirmation in an interactive terminal "
   "and require --yes when run non-interactively.\"",
 ]),
 ("p", "Skills are company-scoped: \"A skill installed in Company A is invisible to Company "
       "B.\" Trust level derives from the highest classification in the skill's inventory, "
       "ordered markdown_only < assets < scripts_executables (references/ = reference, "
       "scripts/ = script, assets/ = asset)."),
]

# ═════════════════════════════════════════════════════════ G14. Secrets

_G14 = [
 ("rule",),
 ("h2", "G14. Secrets commands"),

 ("p", "The secrets family keeps credentials out of configuration files, shell history and "
       "exports. Read its central guarantee as a design constraint on your own scripts, not "
       "merely as a feature."),
 ("note", "Documented warning, verbatim: \"Paperclip never prints secret values. secrets list, "
          "declarations, usage, and access-events return metadata only — names, keys, "
          "providers, status, and references — never the plaintext. The value is shown only "
          "at the moment you set it (and even then, prefer --value-env so it never lands in "
          "your shell history). Treat that as a hard guarantee and design your scripts around "
          "it.\""),

 ("h3", "G14.1 The command index"),
 ("table", ("Secrets commands",
   ["Command", "Use"],
   [["secrets list", "See the secret metadata that exists for a company."],
    ["secrets declarations", "See the portable env declarations a company export emits (what "
     "a target instance must supply)."],
    ["secrets create", "Store a new Paperclip-managed secret value."],
    ["secrets link", "Register an external provider-owned secret without copying its value "
     "into Paperclip."],
    ["secrets update", "Patch a secret's metadata."],
    ["secrets rotate", "Replace a managed secret's value."],
    ["secrets usage", "Find where a secret is referenced (which agents/projects)."],
    ["secrets access-events", "Audit when and by whom a secret was read."],
    ["secrets delete", "Remove a secret (guarded by --yes + --confirm)."],
    ["secrets doctor", "Run provider health checks through the API."],
    ["secrets providers", "List the secret provider descriptors available to a company."],
    ["secrets provider-configs (+ subcommands)",
     "Manage per-company provider vault configs."],
    ["secrets remote-import / remote-import:preview",
     "Pull secrets in from a configured remote source."],
    ["secrets migrate-inline-env",
     "Convert inline sensitive agent env values into secret references."]])),

 ("h3", "G14.2 Reading, creating, linking"),
 ("code",
  "paperclipai secrets list --company-id <company-id>\n"
  "paperclipai secrets list --company-id <company-id> --json\n"
  "\n"
  "paperclipai secrets declarations --company-id <company-id>\n"
  "paperclipai secrets declarations --company-id <company-id> --include agents,projects "
  "--kind secret\n"
  "\n"
  "# Preferred: the value is read from the env var, not typed on the command line\n"
  "export ANTHROPIC_API_KEY=sk-ant-...\n"
  "paperclipai secrets create --company-id <company-id> --name anthropic-api-key "
  "--value-env ANTHROPIC_API_KEY\n"
  "\n"
  "# Discouraged: --value puts the secret into shell history\n"
  "paperclipai secrets create --company-id <company-id> --name anthropic-api-key "
  "--value 'sk-ant-...'\n"
  "\n"
  "paperclipai secrets link \\\n"
  "  --company-id <company-id> \\\n"
  "  --name prod-stripe-key \\\n"
  "  --provider aws_secrets_manager \\\n"
  "  --external-ref "
  "arn:aws:secretsmanager:us-east-1:123456789012:secret:prod/stripe-AbCdEf"),
 ("table", ("secrets create flags",
   ["Flag", "Use"],
   [["--name <name>", "Required. Secret display name."],
    ["--key <key>", "Portable secret key (the stable key other resources reference)."],
    ["--provider <provider>",
     "Secret provider id. Omit to use the company default (managed local encryption)."],
    ["--value <value>", "The secret value. Mutually exclusive with --value-env."],
    ["--value-env <name>", "Read the value from this environment variable. Mutually "
     "exclusive with --value. Errors if the variable is empty or unset."],
    ["--description <text>", "Free-text description."]])),
 ("table", ("secrets link flags",
   ["Flag", "Use"],
   [["--name <name>", "Required. Secret display name."],
    ["--provider <provider>", "Required. Secret provider id (e.g. aws_secrets_manager)."],
    ["--external-ref <ref>", "Required. Provider secret ARN, name, path, or reference."],
    ["--key <key>", "Portable secret key."],
    ["--provider-version-ref <ref>", "Provider version id or label to pin to."],
    ["--description <text>", "Free-text description."]])),
 ("table", ("secrets declarations flags",
   ["Flag", "Use"],
   [["--include <values>", "Comma-separated include set for the export preview. One or more "
     "of company,agents,projects,issues,tasks,skills. Default: company,agents,projects."],
    ["--kind <kind>", "Filter declarations to all, secret, or plain. Default: all."]])),
 ("note", "\"Always prefer --value-env: it reads the value from a named environment variable "
          "so the plaintext never appears in your shell history, your scrollback, or the "
          "process argument list.\" Passing both --value and --value-env, or neither, is an "
          "error."),

 ("h3", "G14.3 Updating, rotating, auditing, deleting"),
 ("code",
  "paperclipai secrets update <secret-id> --payload-json "
  "'{\"description\":\"Rotated quarterly by ops\"}'\n"
  "\n"
  "export ANTHROPIC_API_KEY=sk-ant-new...\n"
  "paperclipai secrets rotate <secret-id> --value-env ANTHROPIC_API_KEY\n"
  "\n"
  "paperclipai secrets usage <secret-id>\n"
  "paperclipai secrets access-events <secret-id> --json\n"
  "\n"
  "paperclipai secrets delete <secret-id> --yes --confirm <secret-id>\n"
  "\n"
  "paperclipai secrets doctor --company-id <company-id>\n"
  "paperclipai secrets providers --company-id <company-id>"),
 ("p", "secrets update \"changes metadata, not the value. To change the value, use rotate.\" "
       "The API states the same rule from its own side: PATCH /api/secrets/{secretId} \"does "
       "not change the secret value.\" Rotation creates an immutable new version and advances "
       "latestVersion."),
 ("table", ("secrets delete flags",
   ["Flag", "Use"],
   [["--yes", "Required safety flag confirming the destructive action."],
    ["--confirm <secretId>", "Required. Must repeat the same secret ID passed as the "
     "argument."]])),
 ("note", "\"secrets delete is intentionally hard to run by accident.\" If --yes is missing, "
          "or --confirm does not match the argument, the command refuses to proceed. And "
          "before you delete: \"Run secrets usage first whenever you plan to delete a secret. "
          "Deleting a secret that an agent's env still references will break that agent's "
          "runs.\" At the API level DELETE /api/secrets/{secretId} is a HARD delete — it "
          "\"Deletes the secret and its version history\"."),

 ("h3", "G14.4 Provider vaults and remote import"),
 ("code",
  "# List existing configs\n"
  "paperclipai secrets provider-configs --company-id <company-id>\n"
  "\n"
  "# Create a config\n"
  "paperclipai secrets provider-config:create --company-id <company-id> "
  "--payload-json '{ ... }'\n"
  "\n"
  "# Preview which secrets a vault would discover, without importing them\n"
  "paperclipai secrets provider-config:discovery-preview --company-id <company-id> "
  "--payload-json '{ ... }'\n"
  "\n"
  "# Inspect, update, default, health-check, or delete a single config\n"
  "paperclipai secrets provider-config:get <config-id>\n"
  "paperclipai secrets provider-config:update <config-id> --payload-json '{ ... }'\n"
  "paperclipai secrets provider-config:default <config-id>\n"
  "paperclipai secrets provider-config:health <config-id>\n"
  "paperclipai secrets provider-config:delete <config-id>\n"
  "\n"
  "paperclipai secrets remote-import:preview --company-id <company-id> "
  "--payload-json '{ ... }'\n"
  "paperclipai secrets remote-import --company-id <company-id> --payload-json '{ ... }'"),
 ("table", ("Provider-config subcommand scoping",
   ["Subcommand", "Scope", "Required flags"],
   [["provider-configs", "company", "-C"],
    ["provider-config:create", "company", "-C, --payload-json"],
    ["provider-config:discovery-preview", "company", "-C, --payload-json"],
    ["provider-config:get <configId>", "config", "-"],
    ["provider-config:update <configId>", "config", "--payload-json"],
    ["provider-config:default <configId>", "config", "-"],
    ["provider-config:health <configId>", "config", "-"],
    ["provider-config:delete <configId>", "config", "-"]])),
 ("note", "\"Always preview first: remote-import:preview shows what _would_ be imported, and "
          "remote-import performs the selected import.\" On AWS specifically: \"Do not store "
          "AWS bootstrap credentials _inside_ Paperclip secrets — let the runtime resolve "
          "them from the standard AWS credential chain, and use doctor to confirm that chain "
          "is wired up.\""),

 ("h3", "G14.5 Migrating inline environment values"),
 ("code",
  "# Dry run: report agents to update, secrets to create, secrets to rotate\n"
  "paperclipai secrets migrate-inline-env --company-id <company-id>\n"
  "\n"
  "# Commit the migration\n"
  "paperclipai secrets migrate-inline-env --company-id <company-id> --apply"),
 ("p", "migrate-inline-env is a DRY RUN by default; --apply persists the changes. The dry-run "
       "output reports agentsToUpdate, secretsToCreate, secretsToRotate and the full candidate "
       "list. With --apply, \"newly created secrets use the managed local-encrypted provider, "
       "existing same-named secrets are rotated to the current inline value, and each affected "
       "agent's env binding is replaced with a secret_ref pointing at version: latest.\""),
 ("note", "Documented note on what counts as sensitive: \"'Sensitive' is detected by env key "
          "name — keys matching patterns like *_token, api_key, password, secret, private_key, "
          "jwt, and similar. Inline values that are not flagged as sensitive are left "
          "untouched, so review the dry run before applying.\""),

 ("h3", "G14.6 Scopes, references and proposal limits"),
 ("p", "A secret reference is how a secret reaches a run without the value ever appearing in "
       "configuration. Its shape is fixed."),
 ("code",
  "{\n"
  "  \"env\": {\n"
  "    \"ANTHROPIC_API_KEY\": {\n"
  "      \"type\": \"secret_ref\",\n"
  "      \"secretId\": \"secret-uuid\",\n"
  "      \"version\": \"latest\"\n"
  "    }\n"
  "  }\n"
  "}\n"
  "\n"
  "// Pin a numeric version instead\n"
  "{ \"type\": \"secret_ref\", \"secretId\": \"secret-uuid\", \"version\": 2 }"),
 ("p", "Omitting version is treated as latest. Use latest for rotatable values and pin numeric "
       "versions for fixed historical values. The default provider is local_encrypted, storing "
       "material \"AES-GCM encrypted using the local master key\" with a SHA-256 hash. "
       "managedMode is either paperclip_managed (Paperclip owns, creates, stores and rotates "
       "the value) or external_reference (the value lives in an external vault and externalRef "
       "is the pointer). Delivery modes are env (plaintext injected into the agent environment "
       "at launch), api (the agent fetches on demand) and both."),
 ("table", ("secrets list output fields, and what they are not",
   ["Field", "Shows"],
   [["id, name, key", "Identity of the secret record"],
    ["provider", "Which provider holds the material"],
    ["status", "Record status"],
    ["managedMode", "paperclip_managed or external_reference"],
    ["latestVersion", "The current version pointer"],
    ["externalRef", "Whether an external reference is set (yes/no) — never the value"]])),
 ("h3", "G14.7 Agent secret proposals — the limits"),
 ("p", "\"Agents propose, people decide. An agent can raise a proposal and watch its status, "
       "but only a board member can approve it.\" The limits on that mechanism are hard "
       "numbers, and they are what stops a looping agent from flooding the queue."),
 ("bullets", [
   "MAX 20 PENDING PROPOSALS PER AGENT, and MAX 20 PER MINUTE.",
   "Proposals EXPIRE AFTER 14 DAYS, transitioned by a background sweep. On resolution "
   "ciphertextScrubbedAt is stamped and the value is wiped.",
   "A secret proposal's value field is plaintext, MAX 65536 BYTES, encrypted immediately.",
   "Proposal statuses: pending, approved, rejected, withdrawn, expired.",
   "Proposal list pagination: limit default 100, max 200, plus offset; response headers "
   "X-Page-Limit, X-Page-Offset, X-Next-Offset.",
   "Binding proposals use a configPath of env.<KEY> or access.<ALIAS>, and the target policy "
   "is self_and_reports.",
   "Reject requires a non-empty reason. Approve accepts cascade plus overrides.name, "
   "overrides.description and overrides.providerConfigId.",
   "Documented approval failures: \"Expired proposals cannot be approved\"; \"Binding proposal "
   "requires pending secret proposal <id>; retry with cascade=true\".",
 ]),
 ("p", "Run-bound value reads are deliberately narrow. POST /api/agents/me/secrets/{key}/value "
       "returns { \"key\", \"value\", \"version\" } with Cache-Control: no-store; every read "
       "is logged to the security audit trail and the activity log; it requires a live "
       "heartbeat token and secrets:read. \"Low-trust, task-bridge and skill-test tokens are "
       "denied run-bound secret access on purpose.\""),
 ("p", "Strict mode (PAPERCLIP_SECRETS_STRICT_MODE) requires secret references for sensitive "
       "env keys — *_API_KEY, *_TOKEN, *_SECRET — and rejects inline plaintext. It applies to "
       "agent adapterConfig.env, project env, hire-agent approvals and company imports. Two "
       "caveats: \"Strict mode blocks new inline sensitive values. It does not automatically "
       "migrate what is already stored,\" and it does NOT apply to paperclipai configure "
       "--section llm."),
]

# ═══════════════════════════════════════════════════ G15. REST API essentials

_G15 = [
 ("rule",),
 ("h2", "G15. REST API essentials"),

 ("p", "Everything the CLI does, it does over this API, and there are situations — a "
       "plugin, a webhook receiver, an agent runtime you wrote yourself — where you call it "
       "directly. This section gives the base URL, the authentication header, the key "
       "endpoint tables, and the behaviours that most often catch people out."),

 ("h3", "G15.1 Base URL, content type and errors"),
 ("code",
  "http://localhost:3100/api\n"
  "\n"
  "# Company-scoped path convention\n"
  "/api/companies/{companyId}/..."),
 ("table", ("Instance-level endpoints",
   ["Method", "Path", "Purpose"],
   [["GET", "/api/health", "\"The fastest way to check whether the server is up and whether "
     "the database is reachable.\" Returns runtime metadata including deployment mode, auth "
     "readiness and feature flags."],
    ["GET", "/api/companies/{companyId}", "Verify access to a specific company resource."],
    ["GET", "/api/openapi.json",
     "\"Machine-readable description of its REST surface\""]])),
 ("p", "Content-Type is application/json. The error response shape is {\"error\": \"message\"}, "
       "and some errors add a details field."),
 ("table", ("HTTP status codes",
   ["Code", "Meaning", "Cause"],
   [["400", "Bad request", "Validation failed or payload malformed"],
    ["401", "Unauthorized", "No valid caller identity provided"],
    ["403", "Forbidden", "Authenticated but not permitted"],
    ["404", "Not found", "Resource doesn't exist or outside scope"],
    ["409", "Conflict", "Resource locked or in conflicting state"],
    ["422", "Unprocessable entity", "Business rules reject valid structure"],
    ["503", "Service unavailable", "Database unreachable"],
    ["500", "Internal server error", "Unexpected failure"]])),

 ("h3", "G15.2 Authentication"),
 ("code",
  "Authorization: Bearer <token>\n"
  "X-Paperclip-Run-Id: <run_id>"),
 ("table", ("Authentication by caller type",
   ["Caller type", "Authentication", "Notes"],
   [["Board user (local_trusted)", "Implicit board access", "No login required"],
    ["Board user (authenticated mode)", "Session cookie from the web app",
     "Browser sessions work for API clients"],
    ["Board user with API token", "Authorization: Bearer <board-token>",
     "Long-lived board API keys"],
    ["Agent", "Authorization: Bearer <agent-key-or-jwt>",
     "Long-lived keys or short-lived run JWTs"]])),
 ("p", "The resolution order is fixed: no bearer token in a local_trusted deployment gives a "
       "board actor with full local trust; no bearer token in an authenticated deployment "
       "resolves a web session; a bearer token is checked as a board API key first, then "
       "against agent API keys, then as a local agent JWT; no match leaves the request "
       "unauthenticated. \"Bearer tokens always win over cookies.\""),
 ("code",
  "curl -s http://localhost:3100/api/cli-auth/me \\\n"
  "  -H \"Authorization: Bearer pcp_board_your_token_here\"\n"
  "\n"
  "curl -s http://localhost:3100/api/agents/me \\\n"
  "  -H \"Authorization: Bearer $PAPERCLIP_API_KEY\" \\\n"
  "  -H \"X-Paperclip-Run-Id: run_123\""),
 ("code",
  "POST /api/cli-auth/challenges\n"
  "GET  /api/cli-auth/challenges/:id\n"
  "POST /api/cli-auth/challenges/:id/approve\n"
  "POST /api/cli-auth/challenges/:id/cancel\n"
  "GET  /api/cli-auth/me\n"
  "POST /api/cli-auth/revoke-current\n"
  "\n"
  "POST /api/agents/:id/keys      # create agent API key\n"
  "GET  /api/agents/me            # agent-only endpoint"),

 ("h3", "G15.3 The X-Paperclip-Run-Id header"),
 ("note", "X-Paperclip-Run-Id must be sent on issue checkout and on issue state changes "
          "(PATCH /api/issues/{issueId}). \"Always include the X-Paperclip-Run-Id header on "
          "state changes.\" The deploy reference states the general rule: \"Mutating API "
          "requests should include X-Paperclip-Run-Id: $PAPERCLIP_RUN_ID for attribution.\" "
          "Forgetting it on an agent update is rejected as a checkout-ownership violation."),
 ("p", "The value is the current heartbeat run id, which the runtime receives as "
       "PAPERCLIP_RUN_ID. Its purpose is attribution: it is what makes the activity trail "
       "answer \"which run did this\" rather than merely \"which agent\"."),

 ("h3", "G15.4 Agents"),
 ("table", ("Agent endpoints",
   ["Method", "Path", "Purpose"],
   [["GET", "/api/companies/{companyId}/agents", "\"Lists agents for a company\""],
    ["POST", "/api/companies/{companyId}/agents", "Create new agent in company"],
    ["GET", "/api/agents/{agentId}", "Retrieve single agent by UUID or shortname"],
    ["GET", "/api/agents/me", "\"Returns the authenticated agent itself\""],
    ["PATCH", "/api/agents/{agentId}", "Update existing agent configuration"],
    ["DELETE", "/api/agents/{agentId}", "Hard delete agent and cleanup runtime state"],
    ["POST", "/api/agents/{agentId}/pause", "Temporarily suspend agent work intake"],
    ["POST", "/api/agents/{agentId}/resume", "Reactivate paused agent"],
    ["POST", "/api/agents/{agentId}/terminate",
     "Permanently disable agent; revokes all API keys"],
    ["PATCH", "/api/agents/{agentId}/permissions",
     "\"Updates the agent-level permissions block\""],
    ["POST", "/api/companies/{companyId}/agent-hires",
     "Create agent through approval-aware flow with optional source issues"],
    ["POST", "/api/agents/{agentId}/wakeup",
     "Queue work with context (issue ID, reason, payload)"],
    ["POST", "/api/agents/{agentId}/heartbeat/invoke",
     "Trigger straightforward on-demand heartbeat"],
    ["GET", "/api/agents/me/inbox-lite", "\"Compact assignment list an agent needs at the "
     "start of a heartbeat\""]])),
 ("code",
  "GET    /api/agents/{agentId}/keys\n"
  "POST   /api/agents/{agentId}/keys          # token shown once only\n"
  "DELETE /api/agents/{agentId}/keys/{keyId}\n"
  "\n"
  "GET  /api/agents/{agentId}/configuration\n"
  "GET  /api/agents/{agentId}/config-revisions\n"
  "GET  /api/agents/{agentId}/config-revisions/{revisionId}\n"
  "POST /api/agents/{agentId}/config-revisions/{revisionId}/rollback\n"
  "GET  /api/companies/{companyId}/agent-configurations\n"
  "\n"
  "GET /api/companies/{companyId}/org\n"
  "GET /api/companies/{companyId}/org.svg\n"
  "GET /api/companies/{companyId}/org.png"),

 ("h3", "G15.5 Issues"),
 ("table", ("Core issue endpoints",
   ["Method", "Path", "Purpose"],
   [["GET", "/api/companies/{companyId}/issues", "List company issues (filterable)"],
    ["GET", "/api/issues/{issueId}", "Fetch one issue"],
    ["GET", "/api/issues/{issueId}/heartbeat-context", "Fetch the heartbeat context"],
    ["POST", "/api/companies/{companyId}/issues", "Create an issue"],
    ["PATCH", "/api/issues/{issueId}", "Update an issue"],
    ["POST", "/api/issues/{issueId}/checkout", "Atomically claim an issue"],
    ["POST", "/api/issues/{issueId}/release", "Release a claimed issue"]])),
 ("p", "Listing accepts status (or a comma-separated list such as todo,in_progress), "
       "assigneeAgentId, participantAgentId, assigneeUserId, touchedByUserId, "
       "inboxArchivedByUserId, unreadForUserId, projectId, executionWorkspaceId, "
       "parentId/parentIssueId, labelId, originKind (for example manual or "
       "routine_execution), originId, includeRoutineExecutions (default FALSE), q (full-text "
       "over title, identifier, description and comments) and limit. On create, only title is "
       "required; status defaults to BACKLOG and priority defaults to MEDIUM."),
 ("note", "\"Routine execution issues are excluded by default unless you opt in with "
          "includeRoutineExecutions=true.\" This is the reason a routine can appear to be "
          "doing nothing when it is in fact working."),
 ("code",
  "GET    /api/issues/{issueId}/comments\n"
  "GET    /api/issues/{issueId}/comments/{commentId}\n"
  "POST   /api/issues/{issueId}/comments\n"
  "\n"
  "GET    /api/issues/{issueId}/documents\n"
  "GET    /api/issues/{issueId}/documents/{key}\n"
  "PUT    /api/issues/{issueId}/documents/{key}\n"
  "DELETE /api/issues/{issueId}/documents/{key}          # board-only\n"
  "POST   /api/issues/{issueId}/documents/{key}/lock\n"
  "POST   /api/issues/{issueId}/documents/{key}/unlock\n"
  "GET    /api/issues/{issueId}/documents/{key}/revisions\n"
  "POST   /api/issues/{issueId}/documents/{key}/revisions/{revisionId}/restore\n"
  "\n"
  "GET    /api/issues/{issueId}/attachments\n"
  "POST   /api/companies/{companyId}/issues/{issueId}/attachments   # multipart/form-data\n"
  "GET    /api/attachments/{attachmentId}/content\n"
  "GET    /api/attachments/{attachmentId}/content?download=1\n"
  "DELETE /api/attachments/{attachmentId}\n"
  "\n"
  "GET    /api/issues/{issueId}/approvals\n"
  "POST   /api/issues/{issueId}/approvals            # body: approvalId\n"
  "DELETE /api/issues/{issueId}/approvals/{approvalId}\n"
  "\n"
  "GET  /api/issues/{issueId}/interactions\n"
  "POST /api/issues/{issueId}/interactions\n"
  "POST /api/issues/{issueId}/interactions/{interactionId}/accept\n"
  "POST /api/issues/{issueId}/interactions/{interactionId}/reject\n"
  "POST /api/issues/{issueId}/interactions/{interactionId}/respond\n"
  "POST /api/issues/{issueId}/interactions/{interactionId}/withdraw\n"
  "POST /api/issues/{issueId}/interactions/{interactionId}/cancel     # board-only\n"
  "\n"
  "POST /api/issues/{issueId}/scheduled-retry/retry-now      # board-only\n"
  "GET  /api/issues/{issueId}/recovery-actions\n"
  "POST /api/issues/{issueId}/recovery-actions/resolve\n"
  "POST /api/issues/{issueId}/file-resources/availability\n"
  "POST /api/issues/{id}/monitor/check-now"),

 ("h3", "G15.6 409 is terminal, and reopen:true"),
 ("note", "Two rules that between them prevent most multi-agent data corruption. FIRST: treat "
          "409 from checkout as TERMINAL. \"Retrying 409 Conflict from checkout... Thrashes "
          "lock; steals ownership. Treat 409 as terminal; pick different issue.\" SECOND: a "
          "terminal issue cannot be revived by setting its status. \"Reopening with PATCH "
          "status: 'todo' on done issue... Rejected — terminal transitions require reopen. "
          "Send PATCH { reopen: true, comment: \"...\" }.\""),
 ("table", ("The documented common mistakes, in full",
   ["Mistake", "What goes wrong", "Do this instead"],
   [["PATCH status: \"in_progress\" to claim a task",
     "Skips checkout; leaves checkoutRunId empty; race-prone",
     "Always claim via POST /api/issues/{id}/checkout with expectedStatuses and "
     "X-Paperclip-Run-Id"],
    ["Retrying 409 Conflict from checkout", "Thrashes lock; steals ownership",
     "Treat 409 as terminal; pick a different issue"],
    ["Free-text \"blocked by PAP-XYZ\" comment", "Dependent never auto-wakes",
     "Set blockedByIssueIds on create/PATCH"],
    ["Cancelling a blocker and expecting auto-unblock",
     "cancelled blockers don't count as resolved",
     "Replace/remove the cancelled id from blockedByIssueIds explicitly"],
    ["Approving an in_review issue without being current participant",
     "Server returns 422", "Inspect executionState.currentParticipant first"],
    ["Reopening with PATCH status: \"todo\" on a done issue",
     "Rejected — terminal transitions require reopen",
     "Send PATCH { reopen: true, comment: \"...\" }"],
    ["Forgetting X-Paperclip-Run-Id on agent updates",
     "Server rejects as checkout-ownership violation",
     "Always pass the current heartbeat run id"]])),

 ("h3", "G15.7 Approvals"),
 ("table", ("Approval endpoints",
   ["Method", "Path", "Purpose"],
   [["GET", "/api/companies/{companyId}/approvals",
     "List company approvals with optional status filter"],
    ["GET", "/api/approvals/{approvalId}", "Retrieve single approval record"],
    ["POST", "/api/companies/{companyId}/approvals", "Create new approval request"],
    ["GET", "/api/approvals/{approvalId}/issues", "Fetch issues linked to approval"],
    ["POST", "/api/approvals/{approvalId}/approve",
     "Board-only: approve pending/revision request"],
    ["POST", "/api/approvals/{approvalId}/reject",
     "Board-only: reject pending/revision request"],
    ["POST", "/api/approvals/{approvalId}/request-revision",
     "Board-only: send pending to revision state"],
    ["GET", "/api/approvals/{approvalId}/comments", "List approval comments"],
    ["POST", "/api/approvals/{approvalId}/comments", "Add comment to approval thread"],
    ["POST", "/api/approvals/{approvalId}/resubmit",
     "Requester: resubmit revision_requested approval"]])),
 ("p", "The create body requires type and payload (free-form JSON whose shape varies by type); "
       "requestedByAgentId is optional and is set automatically when the caller is an agent; "
       "issueIds links issues within the same company only. Failure codes are 403 for missing "
       "board access or an unauthorised agent action, 404 for an approval or issue outside "
       "company scope, and 422 for a wrong approval state or a cross-company constraint "
       "violation."),

 ("h3", "G15.8 Secrets"),
 ("code",
  "GET    /api/companies/{companyId}/secret-providers\n"
  "GET    /api/companies/{companyId}/secrets\n"
  "GET    /api/companies/{companyId}/secrets/catalog\n"
  "POST   /api/companies/{companyId}/secrets\n"
  "PATCH  /api/secrets/{secretId}\n"
  "POST   /api/secrets/{secretId}/rotate\n"
  "DELETE /api/secrets/{secretId}\n"
  "\n"
  "# Run-bound agent access\n"
  "GET  /api/agents/me/secrets\n"
  "POST /api/agents/me/secrets/{key}/value\n"
  "\n"
  "# Secret proposals\n"
  "POST   /api/agents/me/secret-proposals\n"
  "GET    /api/agents/me/secret-proposals\n"
  "DELETE /api/agents/me/secret-proposals/{id}\n"
  "GET    /api/companies/{companyId}/secret-proposals\n"
  "POST   /api/companies/{companyId}/secret-proposals/{id}/approve\n"
  "POST   /api/companies/{companyId}/secret-proposals/{id}/reject"),
 ("table", ("POST /api/companies/{companyId}/secrets body",
   ["Field", "Required", "Notes"],
   [["name", "Yes", "Unique within company"],
    ["value", "Yes", "Plaintext secret value"],
    ["provider", "No", "Defaults to local_encrypted"],
    ["description", "No", "Human-readable note"],
    ["externalRef", "No", "Required by some external providers"]])),
 ("p", "GET /api/agents/me/secrets \"Returns just the aliases this agent is allowed to reach\". "
       "POST /api/agents/me/secrets/{key}/value retrieves the plaintext and sends "
       "Cache-Control: no-store. The company secret-proposals list accepts "
       "?status=pending|approved|rejected|withdrawn|expired."),

 ("h3", "G15.9 Runs and heartbeat runs"),
 ("note", "There is no /reference/api/runs page — it returns 404. The documented run endpoints "
          "appear on the costs page, and the CLI run family is the primary documented "
          "interface for inspecting runs."),
 ("code",
  "GET   /api/companies/{companyId}/heartbeat-runs\n"
  "GET   /api/heartbeat-runs/{runId}"),
 ("p", "A heartbeat run's usageJson carries costUsd, cacheAdjustedCostUsd, token counts, and "
       "provider, biller, model, costStatus and billingType. The nine-step heartbeat protocol "
       "the documentation gives to agent developers is worth reproducing because it is the "
       "canonical sequence a runtime should follow: 1. identity via GET /api/agents/me; 2. "
       "approval follow-up if PAPERCLIP_APPROVAL_ID is set; 3. get assignments via GET "
       "/api/companies/{companyId}/issues?assigneeAgentId={yourId}"
       "&status=todo,in_progress,in_review,blocked; 4. pick work (prioritise in_progress, then "
       "in_review, then todo); 5. checkout via POST /api/issues/{issueId}/checkout with the "
       "X-Paperclip-Run-Id header; 6. understand context; 7. do the work; 8. update status via "
       "PATCH /api/issues/{issueId} with the run id header; 9. delegate subtasks if needed."),

 ("h3", "G15.10 Routines"),
 ("code",
  "GET    /api/companies/{companyId}/routines\n"
  "GET    /api/routines/{routineId}\n"
  "POST   /api/companies/{companyId}/routines          Content-Type: application/json\n"
  "PATCH  /api/routines/{routineId}                    Content-Type: application/json\n"
  "POST   /api/routines/{routineId}/triggers           Content-Type: application/json\n"
  "PATCH  /api/routine-triggers/{triggerId}            Content-Type: application/json\n"
  "DELETE /api/routine-triggers/{triggerId}\n"
  "POST   /api/routine-triggers/{triggerId}/rotate-secret\n"
  "POST   /api/routines/{routineId}/run                Content-Type: application/json\n"
  "POST   /api/routine-triggers/public/{publicId}/fire\n"
  "GET    /api/routines/{routineId}/runs?limit=50"),
 ("code",
  "curl -X POST \"http://localhost:3100/api/companies/company-1/routines\" \\\n"
  "  -H \"Authorization: Bearer <board-token>\" \\\n"
  "  -H \"Content-Type: application/json\" \\\n"
  "  -d '{\n"
  "    \"title\": \"Weekly CEO briefing for {{company_name}}\",\n"
  "    \"description\": \"Compile a weekly summary and prepare the next priorities.\",\n"
  "    \"assigneeAgentId\": \"agent-1\",\n"
  "    \"projectId\": \"project-1\",\n"
  "    \"goalId\": \"goal-1\",\n"
  "    \"priority\": \"medium\",\n"
  "    \"status\": \"active\",\n"
  "    \"concurrencyPolicy\": \"coalesce_if_active\",\n"
  "    \"catchUpPolicy\": \"skip_missed\"\n"
  "  }'"),

 ("h3", "G15.11 Costs and budgets"),
 ("code",
  "POST  /api/companies/{companyId}/cost-events\n"
  "GET   /api/companies/{companyId}/costs/summary\n"
  "GET   /api/companies/{companyId}/costs/by-agent\n"
  "GET   /api/companies/{companyId}/costs/by-agent-model\n"
  "GET   /api/companies/{companyId}/costs/by-provider\n"
  "GET   /api/companies/{companyId}/costs/by-biller\n"
  "GET   /api/companies/{companyId}/costs/by-project\n"
  "GET   /api/companies/{companyId}/costs/window-spend\n"
  "GET   /api/companies/{companyId}/costs/quota-windows\n"
  "\n"
  "PATCH /api/companies/{companyId}/budgets\n"
  "PATCH /api/agents/{agentId}/budgets\n"
  "GET   /api/companies/{companyId}/budgets/overview\n"
  "POST  /api/companies/{companyId}/budgets/policies\n"
  "POST  /api/companies/{companyId}/budget-incidents/{incidentId}/resolve\n"
  "\n"
  "POST  /api/companies/{companyId}/finance-events\n"
  "GET   /api/companies/{companyId}/costs/finance-summary\n"
  "GET   /api/companies/{companyId}/costs/finance-by-biller\n"
  "GET   /api/companies/{companyId}/costs/finance-by-kind\n"
  "GET   /api/companies/{companyId}/costs/finance-events"),
 ("p", "A cost event requires agentId, provider, model, costCents and occurredAt. biller "
       "defaults to provider, billingType defaults to unknown and costStatus defaults to "
       "reported, each when omitted. Both budget PATCH endpoints take the same body: "
       "{ \"budgetMonthlyCents\": 5000 }. Budget policy defaults are metric = billed_cents, "
       "windowKind = calendar_month_utc for company and agent scopes but lifetime for project "
       "scopes, warnPercent = 80, hardStopEnabled = true, notifyEnabled = true and isActive = "
       "true. Incident resolution allows keep_paused or raise_budget_and_resume, and \"If you "
       "raise the budget, you must supply a new amount that exceeds the current observed "
       "spend.\""),
 ("note", "Documented warning: \"Hard-stop budget enforcement pauses the affected scope and "
          "cancels work for that scope. A budget increase only resumes the scope if the new "
          "budget is above current observed spend.\" And on units: \"cacheAdjustedCostUsd and "
          "costUsd are in dollars, while costCents on cost events is in cents. Don't mix the "
          "two units when you reconcile a run against its ledger entry.\""),
 ("p", "The documented reading order for a cost investigation is: GET /costs/summary, then "
       "/costs/by-agent, then /costs/by-project, then /budgets/overview, then "
       "/costs/window-spend."),

 ("h3", "G15.12 Projects"),
 ("note", "/reference/api/projects/ returns 404; the navigation lists "
          "/reference/api/goals-and-projects/ instead, and that page was not harvested. The "
          "project surface is therefore documented here only through the CLI project family "
          "in section G5 and through the project-scoped fields on other endpoints "
          "(projectId on issues, routines and cost events; "
          "GET /api/companies/{companyId}/costs/by-project). No project REST paths are "
          "invented."),

 ("h3", "G15.13 Companies"),
 ("code",
  "GET    /api/companies\n"
  "GET    /api/companies/{companyId}\n"
  "POST   /api/companies\n"
  "PATCH  /api/companies/{companyId}\n"
  "PATCH  /api/companies/{companyId}/branding\n"
  "POST   /api/companies/{companyId}/logo            Content-Type: multipart/form-data\n"
  "GET    /api/companies/stats\n"
  "GET    /api/companies/{companyId}/artifacts\n"
  "GET    /api/companies/{companyId}/feedback-traces\n"
  "POST   /api/companies/{companyId}/archive\n"
  "DELETE /api/companies/{companyId}"),
 ("table", ("Export and import routes",
   ["Route", "Purpose", "Who can call it"],
   [["POST /api/companies/{companyId}/export", "Export a company bundle",
     "Any caller with access to the company"],
    ["POST /api/companies/{companyId}/exports/preview", "Preview a company export",
     "Board or CEO of that company"],
    ["POST /api/companies/{companyId}/exports",
     "Export a company bundle with the stricter portability flow",
     "Board or CEO of that company"],
    ["POST /api/companies/import/preview",
     "Preview an import into a new or existing company", "Board only"],
    ["POST /api/companies/{companyId}/imports/preview",
     "Preview an import into the same company", "Board or CEO of that company"],
    ["POST /api/companies/{companyId}/imports/apply",
     "Apply an import into the same company", "Board or CEO of that company"]])),
 ("p", "GET /api/companies and GET /api/companies/stats are board-only, as is GET "
       "/feedback-traces. CEO agents may call PATCH /api/companies/{companyId} \"but only with "
       "branding fields\", and PATCH /branding \"only for their own company.\" A logo upload "
       "does not attach the logo: after the upload succeeds, send the returned assetId to "
       "PATCH /api/companies/{companyId} or PATCH /api/companies/{companyId}/branding as "
       "logoAssetId."),

 ("h3", "G15.14 Skills endpoints and the sync modes"),
 ("table", ("Company skill management endpoints",
   ["Action", "Endpoint"],
   [["List skills", "GET /api/companies/{companyId}/skills"],
    ["Skill detail", "GET /api/companies/{companyId}/skills/{skillId}"],
    ["Read file",
     "GET /api/companies/{companyId}/skills/{skillId}/files?path=SKILL.md"],
    ["Update file", "PATCH /api/companies/{companyId}/skills/{skillId}/files"],
    ["Update status",
     "GET /api/companies/{companyId}/skills/{skillId}/update-status"],
    ["Install update",
     "POST /api/companies/{companyId}/skills/{skillId}/install-update"],
    ["Delete", "DELETE /api/companies/{companyId}/skills/{skillId}"],
    ["Create empty", "POST /api/companies/{companyId}/skills"],
    ["Import from source", "POST /api/companies/{companyId}/skills/import"],
    ["Scan projects", "POST /api/companies/{companyId}/skills/scan-projects"]])),
 ("code",
  "GET /api/skills/catalog                       # filters: kind (bundled/optional), "
  "category, q\n"
  "GET /api/skills/catalog/{catalogId}\n"
  "GET /api/skills/catalog/{catalogId}/files\n"
  "\n"
  "POST /api/companies/{companyId}/skills/install-catalog\n"
  "POST /api/companies/{companyId}/skills/{skillId}/audit\n"
  "POST /api/companies/{companyId}/skills/{skillId}/reset\n"
  "GET  /api/companies/{companyId}/skills/{skillId}/versions"),
 ("p", "\"Mutating routes require either agents:create permission or "
       "permissions.canCreateAgents=true.\""),
 ("h3", "G15.15 The skills sync endpoint and its modes"),
 ("code",
  "GET  /api/agents/{agentId}/skills\n"
  "POST /api/agents/{agentId}/skills/sync     # mode: \"add\" | \"remove\" | \"replace\""),
 ("p", "The sync request body carries desiredSkills — an array of UUIDs, keys or slugs — and "
       "mode, which is REQUIRED and must be one of add, remove or replace. Version pinning is "
       "expressed by replacing a bare reference with an object."),
 ("code",
  "{ \"desiredSkills\": [\"paperclip\", \"code-review\"] }\n"
  "\n"
  "{\n"
  "  \"desiredSkills\": [\n"
  "    \"code-review\",\n"
  "    { \"key\": \"paperclipai/paperclip/paperclip\", \"versionId\": \"<uuid>\" }\n"
  "  ]\n"
  "}"),
 ("p", "GET /api/agents/{agentId}/skills returns an AgentSkillSnapshot with the fields "
       "adapterType, supported, mode, desiredSkills, entries[] and warnings. Version pinning "
       "is gated: \"If any entry carries a non-null versionId while enableBetaSkills is off, "
       "the request fails with 400 and the message Beta skill version pins require the Beta "
       "skills experimental setting to be enabled.\" The enableBetaSkills instance setting "
       "defaults to OFF, and with it off \"saved pins are ignored rather than deleted, and "
       "every agent resolves to the live skill.\""),
 ("note", "The replace mode is the one that bites. It is destructive: whatever you omit from "
          "desiredSkills is detached. Read the current set with GET "
          "/api/agents/{agentId}/skills before you send a replace, or use add and remove, "
          "which touch only what you name."),
]

# ═══════════════════════════════════════════════════════ Closing checks

_G_CLOSE = [
 ("rule",),
 ("h2", "G16. Coverage note — what this reference does not contain"),
 ("p", "This appendix is bounded by the documentation that was harvested. Several CLI "
       "groups appear in the official navigation but their reference pages were not captured, "
       "so no syntax is given for them here and none should be assumed: output-and-scripting, "
       "service, dev-environments, connect (beyond G3.1), token (beyond G3.4 and G3.5), goal, "
       "prompt, adapter, activity, dashboard, access, teams, cloud, plugin, asset and "
       "feedback."),
 ("p", "On the API side, the following pages exist in the navigation and were not harvested: "
       "built-in-agents, cases, attention, decisions, checkbox-confirmations, "
       "goals-and-projects, resource-memberships, folders, company-skill-policy, "
       "inbox-agent-policy, activity, decision-training, summary-slots, status-cards, "
       "dashboard, adapters, teams-catalog, plugins, tool-gateway and instance-admin. Three "
       "URLs were confirmed to return HTTP 404 and have no content at all: "
       "/reference/cli/budget/, /reference/api/runs/ and /reference/api/projects/."),
 ("note", "When you need one of those surfaces, go to the live documentation or run "
          "paperclipai <group> --help against your own install. Do not extrapolate a flag "
          "from a neighbouring family — Paperclip's command groups are deliberately "
          "inconsistent in places (routine versus routines, skills versus skill, --payload "
          "versus --payload-json) and a plausible guess is usually wrong."),

 ("h2", "G17. Self-check"),
 ("check", [
   "Which flag do you add to any command to get machine-readable output, and why does the "
   "documentation recommend it for every scripted call?",
   "An agent's checkout returns 409 Conflict. What is the correct next action, and what must "
   "you never do?",
   "You want to move a done issue back into the queue. Which field must the PATCH body carry, "
   "and why will setting status to todo fail?",
   "State the once-only rule for tokens in your own words, and name two commands it applies "
   "to.",
   "In paperclipai project update, what does passing the literal string null do, and how does "
   "it differ from omitting the flag entirely?",
   "How do you archive a project, and how do you reverse that in the same command family?",
   "Which two cost/budget commands take no --company-id, and why not?",
   "What are the three valid values of --mode on skills agent sync, and which one is "
   "destructive?",
   "Name the two hard limits on agent secret proposals, and say how long a proposal survives "
   "before it expires.",
   "Which HTTP header must accompany an issue checkout and every agent-initiated issue state "
   "change, and where does its value come from?",
   "What is the difference between paperclipai routine and paperclipai routines, and why does "
   "the difference matter operationally?",
   "Why is there no bulk re-enable command for routines, and what do you use instead?",
 ]),
]

CLI_CHAPTERS = (
    _G_INTRO + _G1 + _G2 + _G3 + _G4 + _G5 + _G6 + _G7 + _G8 + _G9
    + _G10 + _G11 + _G12 + _G13 + _G14 + _G15 + _G_CLOSE
)
