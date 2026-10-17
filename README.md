# WSQ — Manage AI Agents with Paperclip

**Course Code:** TGS-2023036646 · **2 days · 16 hours** (14 training + 2 assessment)
**TSC:** Applications Integration (ICT-DIT-3003-1.1)
Conducted by **Tertiary Infotech Academy Pte Ltd** · UEN 201200696W

[![Register](https://img.shields.io/badge/Register-tertiarycourses.com.sg-1F6FEB?style=for-the-badge)](https://www.tertiarycourses.com.sg/wsq-manage-ai-agents-with-paperclip.html)
[![SkillsFuture](https://img.shields.io/badge/SkillsFuture-Claimable-10B981?style=for-the-badge)](https://courses.myskillsfuture.gov.sg/courses/TGS-2023036646)
[![Paperclip](https://img.shields.io/badge/Paperclip-Open%20Source-7C3AED?style=for-the-badge)](https://github.com/paperclipai/paperclip)

---

## About This Course

Running one AI agent is easy. Running a **team** of them — with direction, spending limits,
approval gates and an audit trail someone else can check — is an organisational problem, not a
prompting one.

[Paperclip](https://github.com/paperclipai/paperclip) is an open-source **control plane** for AI
agents: a Node.js server with a React UI that gives a team of agents an org chart, issues,
budgets, routines, approvals and a durable activity log. It does **not** replace your agent
runtime — Claude Code, Codex, Cursor, Gemini CLI, a bash process or an HTTP bot still do the
reasoning and the tool use. Paperclip schedules, budgets, governs and audits them.

> **Paperclip manages the company. Adapters run the agents.**

Over two days you build and govern **six different one-person AI agent companies** — one per lab —
so you see the same control model applied across six very different businesses.

## Learning Outcomes

| | Outcome |
|---|---|
| **LO1** | Identify agentic AI opportunities and perform feasibility scans to determine when a Paperclip-managed multi-agent company is the appropriate solution. |
| **LO2** | Utilise Paperclip to integrate agent runtimes, data and skills, and develop a goal-aligned AI agent company with an org chart, workspaces and budgets. |
| **LO3** | Perform tests in Paperclip to verify that agents, issues, hand-offs and routines function correctly between disparate components. |
| **LO4** | Resolve technical issues in Paperclip and implement modifications to the agent company, its governance controls and its cost boundaries. |

## Course Outline

| Topic | Covers |
|---|---|
| **1 · Fundamentals of Agentic AI and Paperclip** | Agentic AI foundations · the control-plane model · the four pillars and twelve subsystems · the heartbeat · feasibility and when *not* to use multi-agent |
| **2 · Building AI Agents with Paperclip** | Install and verify · company and measurable mission · the CEO and org chart · runtime adapters · workspaces, instructions and secrets |
| **3 · Developing Intelligent Multi-Agent Systems** | Projects, goals and lineage · issue decomposition · assignment and hand-off · sequential specialists · verifying between disparate components |
| **4 · Deploying and Managing AI Agents** | Routines and schedules · layered budgets · approvals and audit · the operator intervention ladder · deployment, portability and troubleshooting |

## The Six Simulated Companies

Each lab builds a **different one-person company**, with its own synthetic data set.

| Lab | Company | Sector | You Build |
|---|---|---|---|
| [1](labs/lab-01-clipreel-studio/) | **ClipReel Studio** | Short Video Production | A verified Paperclip control plane with recorded evidence of a healthy instance |
| [2](labs/lab-02-brightfunnel-marketing/) | **BrightFunnel Marketing** | Digital Marketing | A goal-aligned company with a measurable mission, a hardened CEO and layered caps |
| [3](labs/lab-03-meridian-finance/) | **Meridian Finance Desk** | Finance | A three-agent reporting tree with confined workspaces, proven by marker runs |
| [4](labs/lab-04-ledgerly-accounting/) | **Ledgerly Accounting** | Accounting | A parent/child issue tree run sequentially, with verified hand-offs |
| [5](labs/lab-05-northpoint-trading/) | **NorthPoint Trading Research** | Stock Trading *(research only)* | A paused routine with an explicit cron trigger and a budget control table |
| [6](labs/lab-06-talentbridge-hr/) | **TalentBridge People Ops** | HR — sourcing, interview, policy, onboarding | A governed operation with an approval, the intervention ladder and a closed audit loop |

> **All data in this repository is synthetic**, fabricated for training. The NorthPoint market data
> is not market data. The TalentBridge candidate file deliberately records **no protected
> characteristics**. Never load real company, market, financial or candidate data into a practice
> instance, and never place a real credential in a prompt, a lab note or Git.

## Repository Layout

```
courseware/
  Manage AI Agents with Paperclip (TGS-2023036646)-v2.0.pptx   Trainer slide deck
  Manage AI Agents with Paperclip (TGS-2023036646)-v2.0.pdf    Learner slides
  LP-Manage AI Agents with Paperclip (TGS-2023036646).docx/.pdf  Lesson Plan
  LG-Manage AI Agents with Paperclip (TGS-2023036646).docx/.pdf  Learner Guide
labs/                Six lab folders — each with its README and its own data/ set
  lab-01-clipreel-studio/
  lab-02-brightfunnel-marketing/
  lab-03-meridian-finance/
  lab-04-ledgerly-accounting/
  lab-05-northpoint-trading/
  lab-06-talentbridge-hr/
LG-*.md              Learner Guide (Markdown mirror of the DOCX)
```

The assessment set is **confidential** and is not published here.

## Prerequisites

- **Node.js 20 or later** — Paperclip will not onboard on an older runtime.
- A **normal, non-elevated shell** — the embedded PostgreSQL refuses to start under root/Administrator.
- One agent runtime (e.g. Claude Code, Codex or Gemini CLI), installed **and authenticated outside Paperclip**.
- **Git**, used to baseline each agent workspace so every change is a readable, attributable diff.

## Quick Start

```bash
node --version                 # must report v20 or later
npx --registry https://registry.npmjs.org paperclipai onboard --yes
npx paperclipai doctor         # fix the EARLIEST error first
curl -sS http://localhost:3100/api/health   # expect status ok
```

Then open <http://localhost:3100> and begin [Lab 1](labs/lab-01-clipreel-studio/).

## Assessment

| Instrument | Format |
|---|---|
| **Written Assessment (WA)** | 5 open-ended short-answer questions (K1–K5) · 1 hour · open book |
| **Practical Performance (PP)** | 4 hands-on Paperclip tasks (A1–A4) · 1 hour · open book |

A minimum of **75% attendance** is required to be eligible for assessment and funding.
Learners are graded **Competent (C)** or **Not Yet Competent (NYC)** on each instrument.

## Funding

Up to **70%** SkillsFuture course fee funding for eligible learners (50% baseline for SG/PR 21+, 70% MCES / SME). Eligibility and terms apply — see the [course page](https://www.tertiarycourses.com.sg/wsq-manage-ai-agents-with-paperclip.html).

| | Amount |
|---|---|
| Full fee (before GST) | $900.00 |
| Baseline nett (SG/PR 21+) | $531.00 |
| MCES / SME nett (SG 40+) | $351.00 |

Eligible for SkillsFuture Credit, SFEC, PSEA, Absentee Payroll and UTAP.

## Further Reading

- [Paperclip on GitHub](https://github.com/paperclipai/paperclip) — the source, docs and releases
- [paperclip.inc](https://paperclip.inc/) — the hosted control plane

---

© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.
[www.tertiarycourses.com.sg](https://www.tertiarycourses.com.sg) · enquiry@tertiaryinfotech.com · +65 6100 0613
