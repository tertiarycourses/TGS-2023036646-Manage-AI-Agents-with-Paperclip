#!/usr/bin/env python3
"""
Generate the deck's visual assets (diagrams + charts) as PNGs.

House style: Arial, white background, brand palette, 150 dpi, bbox_inches='tight'.
Output → .claude/skills/courseware-build/assets/images/
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]

BLUE   = "#1F6FEB"
TEAL   = "#10B981"
INK    = "#161B26"
GREY   = "#5B6372"
VIOLET = "#7C3AED"
AMBER  = "#F59E0B"
RED    = "#DC2626"
LIGHT  = "#F5F8FC"
LINE   = "#D7DEE8"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.normpath(os.path.join(HERE, "..", "assets", "images"))
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  wrote", name)


def box(ax, x, y, w, h, label, sub="", fc="white", ec=BLUE, tc=INK,
        fs=11, subfs=8.6, lw=1.8, radius=0.02):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.006,rounding_size={radius}",
                 fc=fc, ec=ec, lw=lw, zorder=2))
    if sub:
        ax.text(x + w / 2, y + h * 0.60, label, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=tc, zorder=3)
        ax.text(x + w / 2, y + h * 0.26, sub, ha="center", va="center",
                fontsize=subfs, color=GREY, zorder=3)
    else:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=tc, zorder=3)


def arrow(ax, x1, y1, x2, y2, color=GREY, lw=1.7, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                 mutation_scale=13, color=color, lw=lw, zorder=1,
                 shrinkA=0, shrinkB=0))


def canvas(w=12, h=6.2):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.axis("off"); fig.patch.set_facecolor("white")
    return fig, ax


# ---------------------------------------------------------------- 1. architecture
def control_plane_architecture():
    fig, ax = canvas(12, 6.4)
    ax.text(50, 96, "Paperclip manages the company · adapters run the agents",
            ha="center", fontsize=13.5, fontweight="bold", color=INK)

    # Board layer
    box(ax, 33, 80, 34, 11, "BOARD  ·  YOU", "Set direction · approve · intervene",
        fc=LIGHT, ec=VIOLET, fs=12)

    # Control plane  (taller box, grid fully inside it)
    ax.add_patch(FancyBboxPatch((6, 40), 88, 34,
                 boxstyle="round,pad=0.006,rounding_size=0.02",
                 fc="white", ec=BLUE, lw=2.4, zorder=2))
    ax.text(50, 70.6, "PAPERCLIP CONTROL PLANE", ha="center", fontsize=11.5,
            fontweight="bold", color=BLUE, zorder=3)
    ax.text(50, 67.2, "Node.js server + React UI  ·  embedded PostgreSQL  ·  :3100",
            ha="center", fontsize=8.8, color=GREY, zorder=3)

    subs = ["Identity", "Org chart", "Work", "Heartbeat",
            "Workspaces", "Governance", "Budget", "Routines",
            "Plugins", "Secrets", "Activity", "Portability"]
    x0, bw, bh, gx, gy = 9.5, 19.4, 6.6, 20.6, 7.4
    for i, sname in enumerate(subs):
        r, c = divmod(i, 4)
        box(ax, x0 + c * gx, 57.2 - r * gy, bw, bh, sname,
            fc=LIGHT, ec=LINE, tc=INK, fs=9.2, lw=1.2)

    # Adapters / runtimes
    ax.text(50, 30.0, "ADAPTERS  ·  \u201cif it can receive a heartbeat, it\u2019s hired\u201d",
            ha="center", fontsize=10, fontweight="bold", color=TEAL)
    runt = ["Claude Code", "Codex", "Cursor", "Gemini CLI", "bash", "HTTP / webhook"]
    rw, gxr = 13.6, 15.0
    for i, r in enumerate(runt):
        box(ax, 6.5 + i * gxr, 16.5, rw, 9, r, fc="white", ec=TEAL, fs=9, lw=1.6)

    ax.text(50, 7.5, "The runtimes do the reasoning and the tool use.  "
                     "Paperclip never replaces them \u2014 it schedules, budgets and audits them.",
            ha="center", fontsize=9.4, color=GREY, style="italic")

    arrow(ax, 50, 80, 50, 74.4, VIOLET, 2.0)
    arrow(ax, 50, 40, 50, 33.0, TEAL, 2.0)
    save(fig, "arch-control-plane.png")


# ---------------------------------------------------------------- 2. org chart
def org_chart():
    fig, ax = canvas(12, 5.6)
    ax.text(50, 95, "The agent org chart — authority, budget and workspace per role",
            ha="center", fontsize=13.5, fontweight="bold", color=INK)

    box(ax, 36, 74, 28, 13, "BOARD (human)", "approves hires, strategy, exceptions",
        fc=LIGHT, ec=VIOLET, fs=11.5)
    box(ax, 36, 48, 28, 13, "CEO agent", "goal alignment · decomposition · synthesis",
        fc="white", ec=BLUE, fs=11.5)

    spec = [("Specialist A", "own workspace · own budget"),
            ("Specialist B", "own workspace · own budget"),
            ("Reviewer", "independent evidence")]
    for i, (t, s) in enumerate(spec):
        box(ax, 5 + i * 32, 19, 26, 13, t, s, fc="white", ec=TEAL, fs=10.5)
        arrow(ax, 50, 48, 18 + i * 32, 32, GREY, 1.6)

    arrow(ax, 50, 74, 50, 61, VIOLET, 2.0)
    ax.text(50, 8, "Each agent = role + manager + adapter + instructions + heartbeat + budget",
            ha="center", fontsize=10, color=GREY, style="italic")
    save(fig, "diagram-org-chart.png")


# ---------------------------------------------------------------- 3. heartbeat
def heartbeat_cycle():
    fig, ax = canvas(12, 5.4)
    ax.text(50, 95, "The heartbeat — a bounded execution burst, not a running process",
            ha="center", fontsize=13.5, fontweight="bold", color=INK)

    stages = [("Dormant", "no cost"), ("Trigger", "timer · assignment\nwake · routine"),
              ("Check out", "atomic lock"), ("Budget check", "at checkout"),
              ("Execute", "adapter runs"), ("Record", "run · cost · activity")]
    bw, gx = 14.2, 15.9
    for i, (t, s) in enumerate(stages):
        col = GREY if i == 0 else (AMBER if i == 3 else BLUE)
        box(ax, 3.5 + i * gx, 45, bw, 20, t, s, fc="white", ec=col, fs=10.2, subfs=8.2)
        if i:
            arrow(ax, 3.5 + (i - 1) * gx + bw, 55, 3.5 + i * gx, 55, GREY, 1.6)

    # loop back
    ax.add_patch(FancyArrowPatch((3.5 + 5 * gx + bw / 2, 45), (3.5 + bw / 2, 45),
                 connectionstyle="arc3,rad=0.32", arrowstyle="-|>",
                 mutation_scale=13, color=TEAL, lw=1.8, zorder=1))
    ax.text(50, 21, "back to dormant", ha="center", fontsize=9.6,
            color=TEAL, fontweight="bold")
    ax.text(50, 10.5, "Between heartbeats the agent is dormant — it is not idling and it is not billing.",
            ha="center", fontsize=10, color=GREY, style="italic")
    save(fig, "diagram-heartbeat.png")


# ---------------------------------------------------------------- 4. layered budgets
def layered_budgets():
    fig, ax = canvas(11, 5.8)
    ax.text(50, 95, "Layered budgets — enforced at checkout, so the loop stops at the ceiling",
            ha="center", fontsize=13.2, fontweight="bold", color=INK)

    rings = [(6, 12, 88, 72, "COMPANY CAP", BLUE, LIGHT),
             (17, 20, 66, 50, "PROJECT CAP", TEAL, "white"),
             (29, 29, 42, 28, "AGENT CAP", VIOLET, LIGHT)]
    for x, y, w, h, lab, ec, fc in rings:
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                     boxstyle="round,pad=0.006,rounding_size=0.02",
                     fc=fc, ec=ec, lw=2.4, zorder=2))
        ax.text(x + 2.4, y + h - 4.4, lab, fontsize=10.4,
                fontweight="bold", color=ec, zorder=3)

    ax.text(50, 41, "actual spend", ha="center", fontsize=10.6,
            fontweight="bold", color=INK, zorder=4)
    ax.text(50, 35.5, "must stay inside every ring", ha="center",
            fontsize=9, color=GREY, zorder=4)

    ax.text(50, 6.5, "Warn, then stop.  The innermost cap that binds is the one that fires first.",
            ha="center", fontsize=10, color=GREY, style="italic")
    save(fig, "diagram-layered-budgets.png")


# ---------------------------------------------------------------- 5. issue lineage
def goal_lineage():
    fig, ax = canvas(12, 5.4)
    ax.text(50, 95, "Goal lineage — every issue carries the reason it exists",
            ha="center", fontsize=13.5, fontweight="bold", color=INK)

    chain = [("COMPANY MISSION", "measurable outcome", VIOLET),
             ("PROJECT GOAL", "budgeted scope", BLUE),
             ("PARENT ISSUE", "synthesis · unassigned", TEAL),
             ("CHILD ISSUES", "specialist work · assigned one at a time", AMBER)]
    for i, (t, s, c) in enumerate(chain):
        y = 72 - i * 18
        box(ax, 16 + i * 4, y, 62 - i * 2, 13.5, t, s, fc="white", ec=c, fs=11, subfs=8.6)
        if i:
            arrow(ax, 50, y + 18, 50, y + 13.5, GREY, 1.7)

    ax.text(50, 8, "An agent that cannot trace its lineage is working without direction.",
            ha="center", fontsize=10, color=GREY, style="italic")
    save(fig, "diagram-goal-lineage.png")


# ---------------------------------------------------------------- 6. evidence chain
def evidence_chain():
    fig, ax = canvas(12, 4.6)
    ax.text(50, 92, "Verifying between disparate components — one thread, five places",
            ha="center", fontsize=13.2, fontweight="bold", color=INK)

    items = [("Issue ID", "what was asked"), ("Run log", "what executed"),
             ("Comment", "what was accepted"), ("Workspace diff", "what changed on disk"),
             ("Cost entry", "what it spent")]
    bw, gx = 17.0, 19.2
    for i, (t, s) in enumerate(items):
        box(ax, 2.5 + i * gx, 38, bw, 24, t, s, fc="white",
            ec=(TEAL if i == 3 else BLUE), fs=10.4, subfs=8.4)
        if i:
            arrow(ax, 2.5 + (i - 1) * gx + bw, 50, 2.5 + i * gx, 50, GREY, 1.6)

    ax.text(50, 20, "Consistent across all five  =  verified.    "
                    "Status alone  =  an unverified claim.",
            ha="center", fontsize=10.6, fontweight="bold", color=INK)
    ax.text(50, 9, "The workspace diff is the strongest evidence you have — read it before "
                   "accepting any agent's summary of it.",
            ha="center", fontsize=9.4, color=GREY, style="italic")
    save(fig, "diagram-evidence-chain.png")


# ---------------------------------------------------------------- 7. intervention ladder
def intervention_ladder():
    fig, ax = canvas(11, 5.4)
    ax.text(50, 95, "The operator intervention ladder — least irreversible control first",
            ha="center", fontsize=13.2, fontweight="bold", color=INK)

    rungs = [("1 · INSPECT", "read task, run, cost and activity evidence", TEAL),
             ("2 · PAUSE", "stop new heartbeats, keep all state", BLUE),
             ("3 · REASSIGN", "move the work to another role", AMBER),
             ("4 · TERMINATE", "last rung — not reversible", RED)]
    for i, (t, s, c) in enumerate(rungs):
        y = 68 - i * 16
        box(ax, 12 + i * 3, y, 76 - i * 6, 12.5, t, s, fc="white", ec=c, fs=11, subfs=8.6)
        if i:
            arrow(ax, 50, y + 16, 50, y + 12.5, GREY, 1.6)

    ax.text(50, 7, "Escalate only when the rung below has genuinely failed — "
                   "and terminate only a role you created as disposable.",
            ha="center", fontsize=9.6, color=GREY, style="italic")
    save(fig, "diagram-intervention-ladder.png")


# ---------------------------------------------------------------- 8. six companies
def six_companies():
    fig, ax = canvas(12, 5.2)
    ax.text(50, 94, "Six one-person AI agent companies — one per lab",
            ha="center", fontsize=13.5, fontweight="bold", color=INK)

    comps = [("Lab 1", "ClipReel Studio", "Short Video Production", BLUE),
             ("Lab 2", "BrightFunnel", "Digital Marketing", TEAL),
             ("Lab 3", "Meridian", "Finance", VIOLET),
             ("Lab 4", "Ledgerly", "Accounting", AMBER),
             ("Lab 5", "NorthPoint", "Stock Trading (research)", BLUE),
             ("Lab 6", "TalentBridge", "HR · People Ops", TEAL)]
    bw, bh, gx, gy = 29.5, 27, 32.5, 31
    for i, (lab, nm, sec, c) in enumerate(comps):
        r, cc = divmod(i, 3)
        x = 3.5 + cc * gx
        y = 46 - r * gy
        ax.add_patch(FancyBboxPatch((x, y), bw, bh,
                     boxstyle="round,pad=0.006,rounding_size=0.03",
                     fc="white", ec=c, lw=2.0, zorder=2))
        ax.add_patch(FancyBboxPatch((x, y + bh - 3.0), bw, 3.0,
                     boxstyle="square,pad=0", fc=c, ec=c, lw=0, zorder=3))
        ax.text(x + 2.2, y + bh - 6.8, lab, fontsize=9, fontweight="bold",
                color=c, zorder=4)
        ax.text(x + bw / 2, y + bh * 0.47, nm, ha="center", fontsize=12,
                fontweight="bold", color=INK, zorder=4)
        ax.text(x + bw / 2, y + bh * 0.20, sec, ha="center", fontsize=8.8,
                color=GREY, zorder=4)

    ax.text(50, 5, "Every data set is synthetic — built for training, never real "
                   "company, market or candidate data.",
            ha="center", fontsize=9.6, color=GREY, style="italic")
    save(fig, "diagram-six-companies.png")


# ---------------------------------------------------------------- 9. feasibility decision
def feasibility_decision():
    fig, ax = canvas(11.5, 5.2)
    ax.text(50, 95, "Feasibility scan — does coordination earn its cost?",
            ha="center", fontsize=13.5, fontweight="bold", color=INK)

    ax.add_patch(FancyBboxPatch((30, 66), 40, 20,
                 boxstyle="round,pad=0.006,rounding_size=0.04",
                 fc=LIGHT, ec=VIOLET, lw=2.2, zorder=2))
    ax.text(50, 79.5, "Are the inputs, tools, authority", ha="center",
            fontsize=10.4, color=INK, zorder=3)
    ax.text(50, 74.5, "and verification the SAME", ha="center",
            fontsize=10.4, color=INK, zorder=3)
    ax.text(50, 69.6, "across the whole task?", ha="center",
            fontsize=10.4, color=INK, zorder=3)

    box(ax, 4, 30, 40, 24, "YES — use ONE agent",
        "Simpler to build, cheaper to run\nand far easier to debug.\nMost business tasks stop here.",
        fc="white", ec=TEAL, fs=11.2, subfs=9)
    box(ax, 56, 30, 40, 24, "NO — add a specialist",
        "Different expertise is required,\nor evidence must be produced\nindependently of its consumer.",
        fc="white", ec=BLUE, fs=11.2, subfs=9)

    arrow(ax, 40, 66, 24, 54, TEAL, 1.8)
    arrow(ax, 60, 66, 76, 54, BLUE, 1.8)

    ax.text(50, 15, "Complexity you do not need is complexity you must still debug, "
                    "budget and audit.",
            ha="center", fontsize=10.4, fontweight="bold", color=INK)
    ax.text(50, 7.5, "Start single. Split only when one instruction can no longer "
                     "describe the job clearly.",
            ha="center", fontsize=9.4, color=GREY, style="italic")
    save(fig, "diagram-feasibility.png")


# ---------------------------------------------------------------- 10. topic weighting chart
def chart_topic_weighting():
    fig, ax = plt.subplots(figsize=(9.6, 4.9))
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    labels = ["T1 · Fundamentals of\nAgentic AI & Paperclip",
              "T2 · Building AI Agents\nwith Paperclip",
              "T3 · Developing Intelligent\nMulti-Agent Systems",
              "T4 · Deploying and\nManaging AI Agents"]
    vals = [25, 25, 25, 25]
    cols = [BLUE, TEAL, VIOLET, AMBER]
    bars = ax.bar(labels, vals, color=cols, width=0.62, zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.9, f"{v}%", ha="center",
                fontsize=12, fontweight="bold", color=INK, zorder=4)
    ax.set_ylim(0, 32)
    ax.set_ylabel("Share of course time (%)", fontsize=10.5, color=GREY)
    ax.set_title("Where course time goes — 14 training hours across 4 topics",
                 fontsize=13, fontweight="bold", color=INK, pad=14)
    ax.tick_params(axis="x", labelsize=9.4, colors=INK)
    ax.tick_params(axis="y", labelsize=9.4, colors=GREY)
    ax.grid(axis="y", color=LINE, lw=0.9, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(LINE)
    fig.tight_layout()
    save(fig, "chart-topic-weighting.png")


# ---------------------------------------------------------------- 11. budget burn-down
def chart_budget_burndown():
    fig, ax = plt.subplots(figsize=(9.6, 4.9))
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    runs = np.arange(0, 13)
    ungoverned = 1.9 * runs ** 1.42
    governed = np.minimum(2.6 * runs, 15.0)

    ax.plot(runs, ungoverned, color=RED, lw=2.6, marker="o", ms=5,
            label="No cap — a runaway loop", zorder=3)
    ax.plot(runs, governed, color=TEAL, lw=2.6, marker="o", ms=5,
            label="Agent cap enforced at checkout", zorder=3)
    ax.axhline(15.0, color=VIOLET, lw=2.0, ls="--", zorder=2)
    ax.text(0.25, 16.0, "AGENT CAP  SGD 15", fontsize=9.6, fontweight="bold",
            color=VIOLET, zorder=4,
            bbox=dict(fc="white", ec="none", pad=1.6))

    ax.annotate("stops at the ceiling", xy=(9.2, 15.0), xytext=(7.4, 27),
                fontsize=9.6, color=TEAL, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.6),
                bbox=dict(fc="white", ec="none", pad=1.6))
    ax.annotate("you find out on the invoice", xy=(11.6, ungoverned[-1]),
                xytext=(5.0, 44), fontsize=9.6, color=RED, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6),
                bbox=dict(fc="white", ec="none", pad=1.6))

    ax.set_xlabel("Heartbeat runs", fontsize=10.5, color=GREY)
    ax.set_ylabel("Cumulative spend (SGD)", fontsize=10.5, color=GREY)
    ax.set_title("Why the cap is enforced at checkout, not at billing",
                 fontsize=13, fontweight="bold", color=INK, pad=14)
    ax.set_xlim(0, 12.6); ax.set_ylim(0, 52)
    ax.grid(color=LINE, lw=0.9, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(LINE)
    ax.legend(fontsize=9.6, frameon=False, loc="upper left")
    ax.tick_params(labelsize=9.4, colors=GREY)
    fig.tight_layout()
    save(fig, "chart-budget-burndown.png")


# ---------------------------------------------------------------- 12. sequential vs parallel
def chart_sequential_runs():
    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")

    # sequential (good)
    ax.barh(3.0, 4.0, left=0.0, height=0.55, color=TEAL, zorder=3)
    ax.barh(2.3, 3.4, left=4.4, height=0.55, color=BLUE, zorder=3)
    ax.text(0.15, 3.0, "Child 1 · Reconciliation", va="center",
            fontsize=9.4, color="white", fontweight="bold", zorder=4)
    ax.text(4.55, 2.3, "Child 2 · Compliance", va="center",
            fontsize=9.4, color="white", fontweight="bold", zorder=4)
    ax.text(-0.15, 3.7, "SEQUENTIAL — each run individually attributable",
            fontsize=10.2, fontweight="bold", color=TEAL, ha="left")

    # parallel (bad)
    ax.barh(0.9, 4.0, left=0.0, height=0.55, color=AMBER, zorder=3)
    ax.barh(0.2, 3.4, left=1.1, height=0.55, color=RED, zorder=3)
    ax.text(0.15, 0.9, "Child 1", va="center", fontsize=9.4,
            color="white", fontweight="bold", zorder=4)
    ax.text(1.25, 0.2, "Child 2 (overlapping)", va="center", fontsize=9.4,
            color="white", fontweight="bold", zorder=4)
    ax.text(-0.15, 1.6, "OVERLAPPING — hand-off cannot be verified",
            fontsize=10.2, fontweight="bold", color=RED, ha="left")

    ax.set_xlabel("Elapsed time (minutes)", fontsize=10.5, color=GREY)
    ax.set_title("Assign one child at a time — assignment is the trigger",
                 fontsize=13, fontweight="bold", color=INK, pad=14)
    ax.set_xlim(-0.2, 9.0); ax.set_ylim(-0.35, 4.3)
    ax.set_yticks([])
    ax.grid(axis="x", color=LINE, lw=0.9, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(LINE)
    ax.tick_params(labelsize=9.4, colors=GREY)
    fig.tight_layout()
    save(fig, "chart-sequential-runs.png")


# ---------------------------------------------------------------- 13. deployment options
def deployment_options():
    fig, ax = canvas(12, 4.8)
    ax.text(50, 93, "Deployment options — exposure is a deliberate decision",
            ha="center", fontsize=13.5, fontweight="bold", color=INK)

    opts = [("LOOPBACK", "default · least exposed", "127.0.0.1:3100\nno auth surface", TEAL),
            ("LAN", "--bind lan", "reachable on your\nnetwork · auth required", BLUE),
            ("TAILNET", "--bind tailnet", "private mesh ·\nauth required", VIOLET),
            ("HOSTED", "container + Postgres", "volume · signing secret\nallowed hostnames", AMBER)]
    bw, gx = 22.0, 24.5
    for i, (t, mode, det, c) in enumerate(opts):
        x = 2.5 + i * gx
        ax.add_patch(FancyBboxPatch((x, 26), bw, 46,
                     boxstyle="round,pad=0.006,rounding_size=0.03",
                     fc="white", ec=c, lw=2.0, zorder=2))
        ax.add_patch(FancyBboxPatch((x, 68), bw, 4.0,
                     boxstyle="square,pad=0", fc=c, ec=c, lw=0, zorder=3))
        ax.text(x + bw / 2, 61, t, ha="center", fontsize=11.4,
                fontweight="bold", color=INK, zorder=4)
        ax.text(x + bw / 2, 54, mode, ha="center", fontsize=9,
                color=c, fontweight="bold", zorder=4)
        ax.text(x + bw / 2, 40, det, ha="center", fontsize=8.8,
                color=GREY, zorder=4, linespacing=1.6)

    ax.text(50, 15, "Exposure increases left to right — and so does the "
                    "authentication you must configure.",
            ha="center", fontsize=10.2, fontweight="bold", color=INK)
    ax.text(50, 7, "/api/health is the readiness probe at every one of these levels.",
            ha="center", fontsize=9.4, color=GREY, style="italic")
    save(fig, "diagram-deployment.png")


# ---------------------------------------------------------------- 14. approval loop
def approval_loop():
    fig, ax = canvas(12, 4.6)
    ax.text(50, 92, "The approval and audit loop — human authority stays explicit",
            ha="center", fontsize=13.2, fontweight="bold", color=INK)

    st = [("Propose", "agent submits a hire,\nstrategy or risky action", BLUE),
          ("Hold", "the action does not\nexecute while pending", AMBER),
          ("Decide", "a human approves or rejects\nWITH a recorded rationale", VIOLET),
          ("Execute or stop", "the decision is applied", TEAL),
          ("Audit", "activity log keeps the\nwhole chain durable", TEAL)]
    bw, gx = 17.4, 19.4
    for i, (t, s, c) in enumerate(st):
        box(ax, 2.4 + i * gx, 34, bw, 30, t, s, fc="white", ec=c, fs=10.6, subfs=8.3)
        if i:
            arrow(ax, 2.4 + (i - 1) * gx + bw, 49, 2.4 + i * gx, 49, GREY, 1.6)

    ax.text(50, 20, "A close without a recorded rationale is an unaudited decision.",
            ha="center", fontsize=10.4, fontweight="bold", color=INK)
    ax.text(50, 10, "In a hosted deployment, tool approvals require "
                    "PAPERCLIP_TOOL_ACTION_SIGNING_SECRET to be configured.",
            ha="center", fontsize=9.2, color=GREY, style="italic")
    save(fig, "diagram-approval-loop.png")


# ---------------------------------------------------------------- 15. diagnosis ladder
def diagnosis_ladder():
    fig, ax = canvas(11.5, 5.0)
    ax.text(50, 94, "Diagnosis ladder — fix the earliest broken link, one change at a time",
            ha="center", fontsize=13.2, fontweight="bold", color=INK)

    rungs = [("1 · HOST", "Node 20+, a normal (non-elevated) user, a writable practice root",
              "node --version", TEAL),
             ("2 · CONTROL PLANE", "doctor is clean and /api/health returns ok",
              "npx paperclipai doctor", BLUE),
             ("3 · ADAPTER", "the runtime authenticates OUTSIDE Paperclip first",
              "verify connection", VIOLET),
             ("4 · AGENT", "a marker run puts a real artifact in the right workspace",
              "git status --short", AMBER)]
    for i, (t, s, cmd, c) in enumerate(rungs):
        y = 70 - i * 17
        ax.add_patch(FancyBboxPatch((6, y), 88, 13.5,
                     boxstyle="round,pad=0.006,rounding_size=0.02",
                     fc="white", ec=c, lw=2.0, zorder=2))
        ax.text(9, y + 8.6, t, fontsize=11, fontweight="bold", color=c, zorder=3)
        ax.text(9, y + 3.6, s, fontsize=9, color=GREY, zorder=3)
        ax.text(91, y + 6.6, cmd, fontsize=8.8, color=INK, ha="right",
                family="monospace", zorder=3,
                bbox=dict(fc=LIGHT, ec=LINE, lw=0.9, pad=2.6))
        if i:
            arrow(ax, 50, y + 17, 50, y + 13.5, GREY, 1.5)

    ax.text(50, 6, "Never change several settings at once — you lose the "
                   "ability to say what actually fixed it.",
            ha="center", fontsize=9.8, color=GREY, style="italic")
    save(fig, "diagram-diagnosis-ladder.png")


if __name__ == "__main__":
    print(f"Generating deck images → {OUT}")
    control_plane_architecture()
    org_chart()
    heartbeat_cycle()
    layered_budgets()
    goal_lineage()
    evidence_chain()
    intervention_ladder()
    six_companies()
    feasibility_decision()
    chart_topic_weighting()
    chart_budget_burndown()
    chart_sequential_runs()
    deployment_options()
    approval_loop()
    diagnosis_ladder()
    print("Done.")
