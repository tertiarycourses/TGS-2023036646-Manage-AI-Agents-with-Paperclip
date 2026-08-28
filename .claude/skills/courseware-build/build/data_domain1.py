"""Topic 1 — Fundamentals of Agentic AI and Paperclip. Lab 1: ClipReel Studio."""

DOMAIN1 = [
    dict(
        num=1,
        topic=1,
        title="Install Paperclip and Prove the Control Plane (ClipReel Studio)",
        objective="LO1: Explain the control-plane / runtime boundary and verify a healthy local "
                  "Paperclip installation with observable evidence.",
        desc=(
            "You prepare a dedicated synthetic practice root for ClipReel Studio, a one-person "
            "short-video production company, verify the supported Node.js runtime, onboard "
            "Paperclip as a normal (non-elevated) user, and then inspect BOTH the built-in "
            "diagnostic and the live health endpoint. Proving the control plane before you hire "
            "any agent matters because every later adapter, budget or heartbeat failure is far "
            "easier to isolate when the platform itself has a recorded clean baseline."
        ),
        build="A running Paperclip instance at http://localhost:3100 plus "
              "evidence/lab01-installation.md recording the Node/npm versions, the doctor "
              "summary and the /api/health response — with no credentials captured.",
        services="Node.js 20+, npm/npx, Paperclip CLI, browser, terminal or PowerShell",
        company="ClipReel Studio (Short Video Production)",
        flow=[
            ("Prepare the practice root", "separate workspace + evidence folders"),
            ("Verify Node.js 20+", "the top cause of a failed onboard"),
            ("Onboard Paperclip", "normal user shell — never sudo"),
            ("Run doctor", "fix the EARLIEST error first"),
            ("Prove /api/health", "record the clean baseline"),
        ],
        steps=[
            ("Create the ClipReel practice root with separate workspace and evidence folders. "
             "Keep this root for the whole course.",
             "mkdir -p paperclip-tgs/clipreel/workspace/{head-of-content,trend-researcher,script-writer} \\\n"
             "         paperclip-tgs/clipreel/evidence\ncd paperclip-tgs/clipreel"),
            ("Verify the runtime. Node.js must report major version 20 or later. Record both "
             "lines in your evidence note — a version mismatch is the single most common "
             "cause of a failed onboard.",
             "node --version\nnpm --version"),
            ("Run the official onboarding command from a NORMAL user shell. The first run "
             "downloads Paperclip, writes the configuration, initialises the embedded "
             "PostgreSQL, starts the server and opens the browser. Do not prepend sudo.",
             "npx --registry https://registry.npmjs.org paperclipai onboard --yes"),
            ("If onboarding is still attached to the terminal, leave it running and open a "
             "second terminal in the same folder. If you stopped it, start it again.",
             "npx paperclipai run"),
            ("Run the built-in diagnostic. Fix the EARLIEST reported dependency or "
             "configuration error before continuing — never change several settings at once.",
             "npx paperclipai doctor"),
            ("Query the health endpoint and confirm it reports an ok status. This is the "
             "control plane answering for itself.",
             "# macOS / Linux\ncurl -sS http://localhost:3100/api/health\n\n"
             "# Windows PowerShell\nInvoke-RestMethod -Uri 'http://localhost:3100/api/health' | ConvertTo-Json -Depth 8"),
            ("Open the dashboard in a browser and confirm the Paperclip start or onboarding "
             "screen loads without a connection error. Do NOT create the company yet — that "
             "is Lab 2.",
             "http://localhost:3100"),
            ("Copy the ClipReel mock brief into the practice root so later labs have a "
             "realistic, synthetic mission to work from.",
             "cp labs/lab-01-clipreel-studio/data/clipreel-company-brief.md ./"),
            ("Write evidence/lab01-installation.md recording the date, Node and npm versions, "
             "the Paperclip version if shown, the doctor summary, the health status and the "
             "dashboard URL. Do NOT copy environment values, connection strings, cookies, "
             "tokens or provider keys.",
             "evidence/lab01-installation.md"),
        ],
        test="`npx paperclipai doctor` completes with no unresolved blocking error, "
             "GET http://localhost:3100/api/health returns status ok, the browser loads the "
             "Paperclip UI, and evidence/lab01-installation.md records all three checks with "
             "no credential or personal identifier.",
        troubleshoot=[
            ("Embedded PostgreSQL refuses to start",
             "Confirm the shell is NOT elevated. Stop the process and re-run onboarding as the "
             "normal user who owns the practice folder."),
            ("The browser cannot reach port 3100",
             "Run `npx paperclipai doctor`, then `npx paperclipai run`, and query /api/health "
             "again BEFORE touching any firewall setting."),
            ("npx resolves against a private registry",
             "Retry with `npx --registry https://registry.npmjs.org paperclipai onboard --yes` "
             "and review the global npm registry configuration afterwards."),
        ],
        challenge="Run `npx paperclipai env` and record ONLY the non-sensitive instance name, "
                  "bind mode and port in your evidence note. Do not paste the full output.",
        reflection="Why does a healthy Paperclip API prove the control plane but say nothing "
                   "about whether a Claude Code, Codex, Gemini or Cursor runtime is ready?",
    ),
]
