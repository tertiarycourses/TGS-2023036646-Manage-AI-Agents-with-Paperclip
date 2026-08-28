# Lab 1 — Install Paperclip and Prove the Control Plane (ClipReel Studio)

**Course:** Manage AI Agents with Paperclip (TGS-2023036646)  
**Version:** v1.0  
**Release date:** 28 August 2026  
**Topic 1:** Fundamentals of Agentic AI and Paperclip  
**Maps to:** LO1: Explain the control-plane / runtime boundary and verify a healthy local Paperclip installation with observable evidence.  
**Tools:** Node.js 20+, npm/npx, Paperclip CLI, browser, terminal or PowerShell  
**Simulated company:** ClipReel Studio — Short Video Production

**Suggested duration:** 45 minutes  
**Prerequisites:**
- A normal, non-administrative shell. Close any elevated Administrator or root terminal before starting.
- Node.js 20 or later, npm/npx, and internet access to the public npm registry.
- Permission to create a local practice folder and download the Paperclip npm package.
- A modern browser able to reach `http://localhost:3100` on the same machine.

---

## Goal

LO1: Explain the control-plane / runtime boundary and verify a healthy local Paperclip installation with observable evidence.

## What You Will Do

You prepare a dedicated synthetic practice root for ClipReel Studio, a one-person short-video production company, verify the supported Node.js runtime, onboard Paperclip as a normal (non-elevated) user, and then inspect BOTH the built-in diagnostic and the live health endpoint. Proving the control plane before you hire any agent matters because every later adapter, budget or heartbeat failure is far easier to isolate when the platform itself has a recorded clean baseline.

## What You Will Build

A running Paperclip instance at http://localhost:3100 plus evidence/lab01-installation.md recording the Node/npm versions, the doctor summary and the /api/health response — with no credentials captured.

> **Data note.** Every figure, name and record in `data/` is SYNTHETIC and was fabricated for training. ClipReel Studio is a simulated company; the data is not real business, market or personal data and must never be presented as such. Keep runtime credentials in the runtime or in Paperclip's secret store — never in prompts, lab notes or Git.

## Steps

**1. Create the ClipReel practice root with separate workspace and evidence folders. Keep this root for the whole course.**

```text
mkdir -p paperclip-tgs/clipreel/workspace/{head-of-content,trend-researcher,script-writer} \
         paperclip-tgs/clipreel/evidence
cd paperclip-tgs/clipreel
```

**2. Verify the runtime. Node.js must report major version 20 or later. Record both lines in your evidence note — a version mismatch is the single most common cause of a failed onboard.**

```text
node --version
npm --version
```

**3. Run the official onboarding command from a NORMAL user shell. The first run downloads Paperclip, writes the configuration, initialises the embedded PostgreSQL, starts the server and opens the browser. Do not prepend sudo.**

```text
npx --registry https://registry.npmjs.org paperclipai onboard --yes
```

**4. If onboarding is still attached to the terminal, leave it running and open a second terminal in the same folder. If you stopped it, start it again.**

```text
npx paperclipai run
```

**5. Run the built-in diagnostic. Fix the EARLIEST reported dependency or configuration error before continuing — never change several settings at once.**

```text
npx paperclipai doctor
```

**6. Query the health endpoint and confirm it reports an ok status. This is the control plane answering for itself.**

```text
# macOS / Linux
curl -sS http://localhost:3100/api/health

# Windows PowerShell
Invoke-RestMethod -Uri 'http://localhost:3100/api/health' | ConvertTo-Json -Depth 8
```

**7. Open the dashboard in a browser and confirm the Paperclip start or onboarding screen loads without a connection error. Do NOT create the company yet — that is Lab 2.**

```text
http://localhost:3100
```

**8. Copy the ClipReel mock brief into the practice root so later labs have a realistic, synthetic mission to work from.**

```text
cp labs/lab-01-clipreel-studio/data/clipreel-company-brief.md ./
```

**9. Write evidence/lab01-installation.md recording the date, Node and npm versions, the Paperclip version if shown, the doctor summary, the health status and the dashboard URL. Do NOT copy environment values, connection strings, cookies, tokens or provider keys.**

```text
evidence/lab01-installation.md
```

## Test It

`npx paperclipai doctor` completes with no unresolved blocking error, GET http://localhost:3100/api/health returns status ok, the browser loads the Paperclip UI, and evidence/lab01-installation.md records all three checks with no credential or personal identifier.

## Checkpoint

Keep Paperclip running and retain the `paperclip-tgs/clipreel` root. Labs 2–6 reuse the same instance, the same `workspace/` convention and the same `evidence/` directory.

## Troubleshooting

- **Embedded PostgreSQL refuses to start** — Confirm the shell is NOT elevated. Stop the process and re-run onboarding as the normal user who owns the practice folder.
- **The browser cannot reach port 3100** — Run `npx paperclipai doctor`, then `npx paperclipai run`, and query /api/health again BEFORE touching any firewall setting.
- **npx resolves against a private registry** — Retry with `npx --registry https://registry.npmjs.org paperclipai onboard --yes` and review the global npm registry configuration afterwards.

## Challenge

Run `npx paperclipai env` and record ONLY the non-sensitive instance name, bind mode and port in your evidence note. Do not paste the full output.

## Reflection

Why does a healthy Paperclip API prove the control plane but say nothing about whether a Claude Code, Codex, Gemini or Cursor runtime is ready?

---

[Labs index](../README.md) · [Lab 2 →](../lab-02-brightfunnel-marketing/README.md)
