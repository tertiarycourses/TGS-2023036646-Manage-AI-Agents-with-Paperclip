#!/usr/bin/env python3
"""
Build the "Manage AI Agents with Paperclip" (TGS-2023036646) WSQ slide deck.

All-white Tertiary house style. Content is driven ENTIRELY by course_data.py +
data_domainN.py so the deck stays 100% aligned with the LP, LG and labs.

Highly visual: every concept block is a tile grid, process map, comparison
table, decision map, chart or a generated diagram image — never a bullet wall.
Step-by-step procedure detail lives in the LEARNER GUIDE, not here: lab slides
carry the briefing, the process map, the verification and the troubleshooting.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# The shared engine (helpers + palette + prs) extracted from the v2 reference.
from _engine import *          # noqa: F401,F403
from _engine import (prs, slide, rect, oval, txt, bullets, head, footer, _logo,
                     cover as _cover_unused, section, content, two_col, cards3,
                     big_statement, tile_grid, flow_h, process_map, decision_map,
                     compare_table, worked_example, steps_slide, chart_slide,
                     trainer_slide, activity_overview, test_slide, brk,
                     _transition, PAGE, ASSETS, REPO, _ellipsis, _short_cmd,
                     BLUE, TEAL, AMBER, INK, GREY, LIGHT, WHITE, LINE, VIOLET)
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

import course_data as C
from data_domain1 import DOMAIN1
from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
from data_domain4 import DOMAIN4
ACTIVITIES = DOMAIN1 + DOMAIN2 + DOMAIN3 + DOMAIN4

IMG = os.path.join(ASSETS, "images")



# ------------------------------------------------------------------ image slides
def _img(name):
    p = os.path.join(IMG, name)
    return p if os.path.exists(p) else None


def _wrapped_lines(text, chars_per_line):
    """Estimate rendered line count for a body caption at a given wrap width."""
    import textwrap
    n = 0
    for para in str(text).split("\n"):
        n += max(1, len(textwrap.wrap(para, chars_per_line)) or 1)
    return n


def img_points(title, image, points, kicker=None, accent=BLUE):
    """THE default concept slide: big image left, 3-4 takeaway tiles right.

    Card heights are computed from the MEASURED wrapped line count of each caption
    (rather than an equal split), so a long caption can never descend through its
    card border or overlap the card below. Body font steps down if the column is tight.
    """
    p = _img(image)
    if not p:
        return tile_grid(title, points, kicker=kicker, cols=1, size=15, accent=accent)
    s = head(slide(), title, kicker, kcolor=accent)
    # aspect-fit into the left column
    iw, ih = Image.open(p).size
    maxw, maxh = Inches(7.45), Inches(4.62)
    sc = min(maxw / iw, maxh / ih)
    w, h = int(iw * sc), int(ih * sc)
    s.shapes.add_picture(p, int(Inches(0.85) + (maxw - w) / 2),
                         int(Inches(1.98) + (maxh - h) / 2), width=w, height=h)

    x0, tw = Inches(8.62), Inches(3.86)
    TOP, AVAIL, GAP = Inches(1.98), Inches(4.62), Inches(0.16)
    items = list(points[:4])
    n = max(1, len(items))

    # Pick the largest body size whose measured height fits the column.
    CPL = {12.0: 40, 11.0: 44, 10.0: 48, 9.0: 53}   # chars per line at 3.86in wide
    for body_sz in (12.0, 11.0, 10.0, 9.0):
        line_h = Pt(body_sz * 1.28)
        heights = []
        for it in items:
            cap = it[1] if isinstance(it, tuple) else it
            lines = _wrapped_lines(cap, CPL[body_sz])
            hdr = Inches(0.46) if isinstance(it, tuple) else Inches(0.0)
            heights.append(int(hdr + lines * line_h + Inches(0.30)))
        if sum(heights) + GAP * (n - 1) <= AVAIL:
            break
    # Distribute any slack evenly so the column stays visually balanced.
    slack = AVAIL - (sum(heights) + GAP * (n - 1))
    if slack > 0:
        heights = [hh + int(slack / n) for hh in heights]

    PAL = [BLUE, TEAL, VIOLET, AMBER]
    y = TOP
    for i, it in enumerate(items):
        ch = heights[i]
        col = PAL[i % 4]
        rect(s, x0, y, tw, ch, LIGHT)
        rect(s, x0, y, tw, Inches(0.09), col)
        if isinstance(it, tuple):
            txt(s, x0 + Inches(0.22), y + Inches(0.18), tw - Inches(0.44),
                Inches(0.34), [[(it[0], 13.5, col, True)]])
            txt(s, x0 + Inches(0.22), y + Inches(0.56), tw - Inches(0.44),
                int(ch - Inches(0.66)), [[(it[1], body_sz, INK, False)]])
        else:
            txt(s, x0 + Inches(0.22), y + Inches(0.16), tw - Inches(0.44),
                int(ch - Inches(0.28)), [[(it, body_sz, INK, False)]],
                anchor=MSO_ANCHOR.MIDDLE)
        y += ch + GAP
    footer(s)
    return s


def img_full(title, image, kicker=None, caption=None, accent=BLUE):
    """Full-width image with an optional caption band."""
    p = _img(image)
    if not p:
        return None
    s = head(slide(), title, kicker, kcolor=accent)
    iw, ih = Image.open(p).size
    maxw = Inches(11.6)
    maxh = Inches(4.25) if caption else Inches(4.75)
    sc = min(maxw / iw, maxh / ih)
    w, h = int(iw * sc), int(ih * sc)
    s.shapes.add_picture(p, int(Inches(0.85) + (maxw - w) / 2), Inches(1.98),
                         width=w, height=h)
    if caption:
        y = Inches(6.32)
        rect(s, Inches(0.85), y, Inches(11.6), Inches(0.62), LIGHT)
        rect(s, Inches(0.85), y, Inches(0.1), Inches(0.62), accent)
        txt(s, Inches(1.12), y, Inches(11.2), Inches(0.62),
            [[(caption, 13, INK, False)]], anchor=MSO_ANCHOR.MIDDLE)
    footer(s)
    return s


def takeaway(s, text, color=BLUE):
    """One bold boxed rule at the bottom of a concept slide."""
    y = Inches(6.28)
    rect(s, Inches(0.85), y, Inches(11.6), Inches(0.66), LIGHT)
    rect(s, Inches(0.85), y, Inches(0.1), Inches(0.66), color)
    txt(s, Inches(1.15), y, Inches(11.2), Inches(0.66),
        [[(text, 13.5, INK, True)]], anchor=MSO_ANCHOR.MIDDLE)
    return s


def lab_card(a, accent=TEAL):
    """One briefing slide per lab — company, goal, what you build, tools.
    NO step-by-step here: the procedure lives in the Learner Guide."""
    s = head(slide(), a["title"], f"LAB {a['num']}  ·  HANDS-ON", kcolor=accent)
    # company chip
    rect(s, Inches(0.85), Inches(1.95), Inches(11.6), Inches(0.62), LIGHT)
    rect(s, Inches(0.85), Inches(1.95), Inches(0.1), Inches(0.62), VIOLET)
    txt(s, Inches(1.15), Inches(1.95), Inches(11.2), Inches(0.62),
        [[("SIMULATED COMPANY  ·  " + a.get("company", ""), 13, VIOLET, True)]],
        anchor=MSO_ANCHOR.MIDDLE)
    # description
    txt(s, Inches(0.85), Inches(2.75), Inches(11.6), Inches(1.42),
        [[(a["desc"], 13.5, INK, False)]])
    # you'll build
    rect(s, Inches(0.85), Inches(4.3), Inches(7.4), Inches(1.72), LIGHT)
    rect(s, Inches(0.85), Inches(4.3), Inches(7.4), Inches(0.09), TEAL)
    txt(s, Inches(1.1), Inches(4.45), Inches(6.9), Inches(0.36),
        [[("YOU'LL BUILD", 12, TEAL, True)]])
    txt(s, Inches(1.1), Inches(4.83), Inches(6.9), Inches(1.1),
        [[(a["build"], 11.5, INK, False)]])
    # maps to
    rect(s, Inches(8.55), Inches(4.3), Inches(3.9), Inches(1.72), LIGHT)
    rect(s, Inches(8.55), Inches(4.3), Inches(3.9), Inches(0.09), BLUE)
    txt(s, Inches(8.8), Inches(4.45), Inches(3.4), Inches(0.36),
        [[("MAPS TO", 12, BLUE, True)]])
    txt(s, Inches(8.8), Inches(4.83), Inches(3.4), Inches(1.1),
        [[(a["objective"], 10.5, INK, False)]])
    txt(s, Inches(0.85), Inches(6.2), Inches(11.6), Inches(0.7),
        [[("Tools:  " + a["services"], 11, GREY, False)],
         [("Full step-by-step procedure: Learner Guide, Lab %d  ·  labs/ folder"
           % a["num"], 11, GREY, False)]], space=3)
    footer(s)
    return s


def lab_troubleshoot(a, accent=AMBER):
    s = head(slide(), a["title"], f"LAB {a['num']}  ·  TROUBLESHOOTING", kcolor=accent)
    items = [(sym, fix) for sym, fix in a.get("troubleshoot", [])][:4]
    n = max(1, len(items))
    th = int((Inches(3.5) - Inches(0.2) * (n - 1)) / n)
    for i, (sym, fix) in enumerate(items):
        y = int(Inches(1.98) + (th + Inches(0.2)) * i)
        rect(s, Inches(0.85), y, Inches(11.6), th, LIGHT)
        rect(s, Inches(0.85), y, Inches(0.1), th, AMBER)
        txt(s, Inches(1.15), y + Inches(0.14), Inches(11.1), Inches(0.36),
            [[("⚠  " + sym, 13, INK, True)]])
        txt(s, Inches(1.15), y + Inches(0.54), Inches(11.1), int(th - Inches(0.66)),
            [[(fix, 11.5, GREY, False)]])
    y2 = Inches(5.72)
    rect(s, Inches(0.85), y2, Inches(5.7), Inches(1.1), LIGHT)
    rect(s, Inches(0.85), y2, Inches(0.1), Inches(1.1), VIOLET)
    txt(s, Inches(1.15), y2 + Inches(0.1), Inches(5.3), Inches(0.32),
        [[("CHALLENGE", 11.5, VIOLET, True)]])
    txt(s, Inches(1.15), y2 + Inches(0.44), Inches(5.3), Inches(0.6),
        [[(a.get("challenge", ""), 10.5, INK, False)]])
    rect(s, Inches(6.75), y2, Inches(5.7), Inches(1.1), LIGHT)
    rect(s, Inches(6.75), y2, Inches(0.1), Inches(1.1), BLUE)
    txt(s, Inches(7.05), y2 + Inches(0.1), Inches(5.3), Inches(0.32),
        [[("REFLECTION", 11.5, BLUE, True)]])
    txt(s, Inches(7.05), y2 + Inches(0.44), Inches(5.3), Inches(0.6),
        [[(a.get("reflection", ""), 10.5, INK, False)]])
    footer(s)
    return s


def cover():
    s = slide(); rect(s, 0, 0, SW, SH, WHITE)
    rect(s, 0, 0, SW, Inches(0.22), BLUE); rect(s, 0, Inches(7.28), SW, Inches(0.22), TEAL)
    org = _logo("tertiary-infotech-logo.png")
    if org:
        s.shapes.add_picture(org, Inches(0.85), Inches(0.7), height=Inches(1.05))
    rect(s, Inches(10.6), Inches(0.66), Inches(2.0), Inches(1.12), BLUE)
    txt(s, Inches(10.6), Inches(0.78), Inches(2.0), Inches(0.52),
        [[("PAPERCLIP", 17, WHITE, True)]], align=PP_ALIGN.CENTER)
    txt(s, Inches(10.6), Inches(1.32), Inches(2.0), Inches(0.4),
        [[("AI AGENT COMPANY OS", 8, WHITE, True)]], align=PP_ALIGN.CENTER)
    txt(s, Inches(0.9), Inches(2.3), Inches(12), Inches(0.6),
        [[("COURSE SLIDES  ·  WSQ", 16, BLUE, True)]])
    txt(s, Inches(0.9), Inches(2.85), Inches(12.0), Inches(1.9),
        [[("Manage AI Agents with Paperclip", 40, INK, True)]])
    rect(s, Inches(0.92), Inches(4.75), Inches(2.4), Inches(0.06), TEAL)
    txt(s, Inches(0.9), Inches(5.05), Inches(12), Inches(1.4),
        [[(f"WSQ Course Code: {C.COURSE_CODE}", 16, GREY, False)],
         [(f"TSC: {C.TSC_TITLE}  ·  {C.TSC_CODE}", 13, GREY, False)],
         [("Conducted by Tertiary Infotech Academy Pte Ltd  ·  UEN 201200696W", 13, GREY, False)]],
        space=6)
    txt(s, Inches(0.9), Inches(6.5), Inches(12), Inches(0.4),
        [[(f"Version {C.VERSION}  ·  {C.VERSION_DATE}", 12, GREY, False)]])
    txt(s, Inches(0.9), Inches(6.85), Inches(12), Inches(0.34),
        [[("© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.  ·  "
           "www.tertiarycourses.com.sg", 10, GREY, False)]])


# ============================================================ BUILD
cover()

# ------------------------------------------------------------- ADMIN
section("COURSE ADMINISTRATION", "Welcome & Housekeeping", "")
tile_grid("Digital Attendance (Mandatory)", [
    ("Three times a day", "Take the AM, PM and Assessment digital attendance — "
     "mandatory for every WSQ-funded course."),
    ("Trainer shows the QR", "The trainer or administrator displays the digital "
     "attendance QR code from the SSG portal."),
    ("Scan and submit", "Scan the QR code with your mobile phone camera and submit "
     "your attendance."),
    ("75% minimum", "A minimum of 75% attendance is required to be eligible for "
     "assessment and funding.")],
    kicker="TRAQOM · SSG DIGITAL ATTENDANCE", cols=2, size=15)
trainer_slide("YOUR TRAINER · GENERAL", "Your Trainer",
              "General Trainer template —\nto be completed by the trainer",
              [("Name", ""), ("Title / Designation", ""), ("Qualifications", ""),
               ("Areas of expertise", ""), ("Training & industry experience", ""),
               ("Contact", "")], initials="?", accent=GREY)
trainer_slide("YOUR TRAINER", C.TRAINER,
              "Principal Trainer\nTertiary Infotech Academy Pte Ltd",
              [("Role", "Principal Trainer, Tertiary Infotech Academy Pte Ltd"),
               ("Expertise", "Generative AI, large language models, agentic AI systems "
                "and applied machine learning."),
               ("Delivers", "WSQ courses on AI, agentic AI, LLM application development, "
                "prompt engineering and data science."),
               ("Founder", "Founder and lead instructor at Tertiary Infotech / "
                "Tertiary Courses.")], initials="AA", accent=BLUE)
tile_grid("Let's Know Each Other", [
    ("Who you are", "Your name, your organisation and the role you play in it."),
    ("What you've used", "Your experience with AI agents, automation or command-line tools — "
     "if any. No experience needed."),
    ("What you'd delegate", "One task in your work you would hand to a team of AI agents."),
    ("What you wouldn't", "One task you would NOT delegate — and the reason why. "
     "We come back to this in Topic 1.")],
    kicker="ICE-BREAKER", cols=2, size=15, accent=VIOLET)
tile_grid("Ground Rules", [
    "Set your mobile phone to silent mode.",
    "Participate actively — no question is too small.",
    "Mutual respect: agree to disagree.",
    "One conversation at a time.",
    "Be punctual; return from breaks on time.",
    "75% attendance is required."],
    kicker="HOUSEKEEPING", cols=2, size=15)
tile_grid("Download Your Course Material", [
    ("Go to the LMS portal", "Open https://lms-tms.tertiaryinfotech.com in your browser."),
    ("Log in", "Sign in with the account e-mail you used to register for this course."),
    ("Open this course", "Select 'Manage AI Agents with Paperclip'."),
    ("Download", "Download the Trainer Slides, Learner Guide and Lesson Plan (PDF)."),
    ("Get the labs", "Clone the lab repository from GitHub — the link is on the course page."),
    ("Keep them open", "You may use these materials during the open-book assessment.")],
    kicker="LMS / TMS  ·  lms-tms.tertiaryinfotech.com", cols=2, size=14)
tile_grid("Skills Framework Alignment", [
    ("TSC Title", C.TSC_TITLE),
    ("TSC Code", C.TSC_CODE),
    ("Training hours", f"{C.TRAINING_HOURS} hours across {C.DAYS} days"),
    ("Assessment hours", f"{C.ASSESSMENT_HOURS} hours — Written Assessment + Practical Performance"),
    ("Level", "Beginner to Intermediate"),
    ("Mode", "Physical, instructor-led with hands-on labs")],
    kicker="SKILLS FRAMEWORK  ·  TSC", cols=2, size=14, accent=VIOLET)
two_col("Lesson Plan — 2 Days, 8 hours/day",
        [(f"Day 1 — {C.DAY_THEMES[1]}", 0),
         ("Digital Attendance (AM) · Introductions · Learning Outcomes", 1),
         ("Topic 1: Fundamentals of Agentic AI and Paperclip (Lab 1)", 1),
         ("Lunch Break · Digital Attendance (PM)", 1),
         ("Topic 2: Building AI Agents with Paperclip (Labs 2–3)", 1),
         ("Day 1 recap", 1)],
        [(f"Day 2 — {C.DAY_THEMES[2]}", 0),
         ("Digital Attendance (AM) · Day 1 recap", 1),
         ("Topic 3: Developing Intelligent Multi-Agent Systems (Labs 4–5)", 1),
         ("Lunch Break · Digital Attendance (PM)", 1),
         ("Topic 4: Deploying and Managing AI Agents (Lab 6)", 1),
         ("TRAQOM Survey · Digital Attendance (Assessment)", 1),
         ("Final Assessment (WA + PP) — 2 hours", 1)],
        kicker="SCHEDULE", lhead="Day 1", rhead="Day 2")
tile_grid("Learning Outcomes", C.LO_SHORT,
          kicker="WHAT YOU'LL ACHIEVE", cols=2, size=15)
tile_grid("Course Outline", [
    (f"Topic {t['code']} — {t['title']}", t["subtitle"]) for t in C.TOPICS],
    kicker="FOUR TOPICS  ·  6 HANDS-ON LABS", cols=1, size=15)
img_full("Six One-Person AI Agent Companies", "diagram-six-companies.png",
         kicker="THE COURSE SIMULATION",
         caption="Each lab builds a different one-person company — so you see the same "
                 "control model applied to six very different businesses.",
         accent=VIOLET)
tile_grid("Briefing for Assessment", [
    ("Do · Clear your desk", "Place phones and other materials under the table or on the floor."),
    ("Don't · No recording", "No photos or recording of assessment scripts."),
    ("Don't · No discussion", "Work individually — no discussion during the assessment."),
    ("Do · Black or blue pen", "Use a black or blue pen for hard-copy assessments."),
    ("Don't · No correction fluid", "No liquid paper or correction tape may be used."),
    ("Do · Stop on time", "Scripts are collected when time is up.")],
    kicker="BEFORE YOU START", cols=2, size=14, accent=AMBER)
tile_grid("Assessment", [
    ("Written Assessment (WA)", "Short-Answer Questions (SAQ) · 5 questions · 1 hour · "
     "open book. Tests the underpinning knowledge (K1–K5)."),
    ("Practical Performance (PP)", "4 hands-on Paperclip tasks · 1 hour · open book. "
     "Tests the ability you built in the labs (A1–A4)."),
    ("Open book", "You may use the course slides, the Learner Guide and approved materials only."),
    ("Eligibility", "A minimum of 75% attendance is required to be eligible for assessment "
     "and funding."),
    ("Result", "You are assessed as Competent (C) or Not Yet Competent (NYC) on each instrument."),
    ("Appeals", "An appeal process is available if you wish to contest an assessment outcome.")],
    kicker="FINAL ASSESSMENT", cols=2, size=14)
process_map("Assessment Flow", [
    ("TRAQOM survey", "Scan the QR code on the LMS"),
    ("Digital attendance", "Scan the SSG assessment QR"),
    ("Sit WA then PP", "Open book · 1 hour each"),
    ("Submit on the LMS", "Upload your completed answers"),
    ("Sign the record", "Sign the Assessment Summary Record")],
    kicker="ON ASSESSMENT DAY", color=BLUE,
    synthesis=("REMEMBER", "All five steps are mandatory for WSQ funding — missing the "
               "digital attendance or the TRAQOM survey can invalidate your claim."))
tile_grid("Practice Exam", [
    ("Practise before the real thing", "Try the practice questions at "
     "https://exams.tertiaryinfotech.com before the final assessment."),
    ("Same format", "Short-answer knowledge questions in the same style as the "
     "Written Assessment."),
    ("Self-marked", "Use it to find the topics you need to revisit, not to score yourself."),
    ("Free and unlimited", "Attempt it as many times as you like during the course.")],
    kicker="EXAMS.TERTIARYINFOTECH.COM", cols=2, size=15, accent=TEAL)
tile_grid("Criteria for Funding", [
    ("Attendance", "A minimum attendance rate of 75%, based on the SSG Digital Attendance record."),
    ("Assessment", "Complete both assessment components and be assessed as 'Competent'."),
    ("Digital attendance", "Scan the SSG QR code for AM, PM and Assessment on every training day."),
    ("TRAQOM survey", "Complete the mandatory TRAQOM course feedback survey on the LMS.")],
    kicker="WSQ FUNDING", cols=2, size=15, accent=AMBER)
tile_grid("Set Up Before We Start", [
    ("Node.js 20 or later", "Paperclip requires Node 20+. Check with `node --version`."),
    ("A normal user shell", "Never run onboarding from an elevated Administrator or root shell."),
    ("An agent runtime", "One trainer-approved CLI runtime (e.g. Claude Code, Codex, Gemini CLI)."),
    ("Git", "Used to baseline each agent workspace so every change is a readable diff."),
    ("Lab repository", "Clone the course labs — the link is on your LMS course page."),
    ("Synthetic data only", "All six company data sets are fabricated for training. "
     "Never load real company, market or candidate data.")],
    kicker="LAB ENVIRONMENT", cols=2, size=14, accent=TEAL)

# ------------------------------------------------------------- CORE CONCEPTS
section("CORE CONCEPTS", "From a Single Agent to a Managed Agent Company", "")
tile_grid("What Makes a System 'Agentic'?", [
    ("Reasoning", "The model plans a sequence of steps instead of answering in one shot."),
    ("Tool use", "It calls functions, CLIs and APIs to fetch live data or take real actions."),
    ("Memory", "State carries context across turns — and, in Paperclip, across heartbeats."),
    ("Autonomy", "It decides which tool to use and when the work is actually finished."),
    ("Collaboration", "Several specialised agents divide the work and hand off between themselves."),
    ("Guardrails", "Policies, budgets and approvals constrain what the agent may do.")],
    kicker="THE SIX INGREDIENTS", cols=2, size=14, accent=VIOLET)
big_statement("An LLM answers. An agent acts. A company coordinates.",
              "Paperclip is the third layer — it does not make your agents smarter, it makes "
              "a team of them accountable.", "WHY A CONTROL PLANE", color=BLUE)
img_points("Paperclip Control-Plane Architecture", "arch-control-plane.png", [
    ("Board · you", "You set direction, approve governed actions and intervene. "
     "Authority never leaves the human."),
    ("The control plane", "Stores companies, org charts, issues, budgets, secrets and "
     "the audit trail. Node.js + React on port 3100."),
    ("The adapters", "Claude Code, Codex, Cursor, Gemini CLI, bash or an HTTP bot — "
     "these do the actual reasoning."),
    ("The separation", "Organisational authority, runtime capability and verification "
     "evidence are kept deliberately apart.")],
    kicker="LO1 · ORCHESTRATE, DO NOT REPLACE, THE RUNTIME", accent=BLUE)
takeaway(tile_grid("What Paperclip Is — and Is Not", [
    ("IS · an organisational control plane", "Org charts, issues, budgets, approvals "
     "and a durable audit trail for a team of agents."),
    ("IS · a runtime-agnostic scheduler", "'If it can receive a heartbeat, it's hired.' "
     "It schedules and budgets agents without replacing them."),
    ("IS NOT · an agent framework", "It does not dictate how your agent reasons, prompts "
     "or calls tools. That is the adapter's job."),
    ("IS NOT · a chatbot or workflow builder", "No drag-and-drop canvas, no prompt manager, "
     "and not designed for a single-agent use case.")],
    kicker="LO1 · SCOPE THE TOOL CORRECTLY", cols=2, size=14, accent=TEAL),
    "Choosing Paperclip is an organisational decision, not a modelling decision.")
img_full("The Four Pillars of Paperclip", "paperclip-four-pillars.png",
         kicker="LO1 · THE PRODUCT MODEL",
         caption="Agentic task manager · org chart for agents · agent employee training · "
                 "agentic OS. Source: the official Paperclip project.",
         accent=BLUE)
tile_grid("The Twelve Subsystems", [
    ("Identity & org chart", "Who exists, who reports to whom, and what each role may do."),
    ("Work & heartbeat", "Issues with atomic checkout, woken by bounded execution bursts."),
    ("Workspaces & runtime", "Isolated roots (git worktrees) and the adapter that runs there."),
    ("Governance & budget", "Approval gates and caps enforced at checkout, not at billing."),
    ("Routines & plugins", "Scheduled recurring work, and the skills library agents draw on."),
    ("Secrets, activity & portability", "Scoped injection, a durable audit log, and "
     "export/import of a whole company.")],
    kicker="LO1 · WHAT THE PLATFORM ACTUALLY CONTAINS", cols=2, size=14)
img_points("The Heartbeat — Bounded Execution, Not a Running Process",
           "diagram-heartbeat.png", [
    ("Dormant by default", "Between heartbeats the agent is not idling and not billing."),
    ("Four triggers", "A timer, an assignment, an on-demand wake, or a routine."),
    ("Atomic checkout", "An execution lock means two heartbeats can never double-work "
     "the same issue."),
    ("Budget checked first", "The cap is tested at checkout — a runaway loop stops at the "
     "ceiling.")],
    kicker="LO1 · THE EXECUTION MODEL", accent=BLUE)
img_points("Feasibility Scan — Does Coordination Earn Its Cost?",
           "diagram-feasibility.png", [
    ("Use ONE agent", "When inputs, tools, authority and verification are the same across "
     "the whole task."),
    ("Add a specialist", "Only when different expertise is required, or evidence must be "
     "produced independently."),
    ("The real cost", "Every extra agent is another workspace, budget, instruction and "
     "audit trail to maintain."),
    ("Start single", "Split only when one instruction can no longer describe the job clearly.")],
    kicker="LO1 · THE MOST IMPORTANT DECISION IN THE COURSE", accent=VIOLET)
compare_table("One Agent vs a Paperclip Agent Company",
    ["Dimension", "One agent, run by hand", "A Paperclip agent company"],
    [["Direction", "Restated in every prompt", "A mission that flows down as goal lineage"],
     ["Memory", "Ends with the session", "Persists across heartbeats in the control plane"],
     ["Cost", "Discovered on the invoice", "Capped at checkout per company, project and agent"],
     ["Authority", "Implicit — whatever you allow", "Explicit — org chart, roles and approvals"],
     ["Evidence", "Scrollback you must trust", "Runs, comments, diffs and a durable activity log"],
     ["Main risk", "Context saturation", "Coordination overhead you did not need"]],
    kicker="LO1 · WHEN THE CONTROL PLANE PAYS FOR ITSELF", accent=BLUE,
    note="The right answer is often still ONE agent. Reach for the company when the work has "
         "genuinely separable roles that must each be evidenced.")
chart_slide("Where Course Time Goes — Topic Weighting",
    [f"Topic {t['code']}" for t in C.TOPICS],
    [("Share of course (%)", [int(str(t["weighting"]).replace("%", "")) for t in C.TOPICS])],
    kicker="LESSON PLAN · TIME ALLOCATION", accent=BLUE, kind="column",
    insight="The four topics carry equal weighting — but Topics 3 and 4 are where the "
            "assessable practical skill sits, because that is where governance and "
            "verification are actually exercised.",
    number_format='0"%"')

# ------------------------------------------------------------- TOPICS + LABS
TOPIC_ACTS = {t["num"]: [a for a in ACTIVITIES if a["topic"] == t["num"]] for t in C.TOPICS}

# Per-topic extra visual concept slides, keyed by topic number.
def topic_extras(num):
    if num == 1:
        img_points("Diagnosis Ladder — Fix the Earliest Broken Link",
                   "diagram-diagnosis-ladder.png", [
            ("Host first", "Node 20+, a normal non-elevated user, a writable practice root."),
            ("Then the control plane", "`doctor` is clean and /api/health returns ok."),
            ("Then the adapter", "The runtime must authenticate OUTSIDE Paperclip first."),
            ("Then the agent", "A marker run puts a real artifact in the right workspace.")],
            kicker="LO4 · TROUBLESHOOTING DISCIPLINE", accent=AMBER)
        takeaway(tile_grid("Installation Is Ready Only When Everything Agrees", [
            ("Node.js", "Major version 20 or later — the most common cause of a failed onboard."),
            ("Configuration & database", "Written by `onboard`; the embedded PostgreSQL starts "
             "as the normal user."),
            ("Server health", "GET /api/health returns an ok status."),
            ("Browser UI", "http://localhost:3100 loads without a connection error."),
            ("Doctor", "`npx paperclipai doctor` completes with no blocking error."),
            ("Evidence", "All of the above recorded — with no credential ever captured.")],
            kicker="LO2 · THE READINESS CHECKLIST", cols=2, size=14),
            "A green badge is not evidence. An observable artifact is.")
    elif num == 2:
        img_points("The Agent Org Chart", "diagram-org-chart.png", [
            ("Board approves", "Hires, strategy and material exceptions stay with the human."),
            ("The CEO owns alignment", "Goal alignment, decomposition and final synthesis."),
            ("Specialists own transformations", "One distinct job, one authority boundary, "
             "one deliverable."),
            ("Six fields per agent", "Role · manager · adapter · instructions · heartbeat · "
             "budget.")],
            kicker="LO2 · ACCOUNTABILITY HAS A SHAPE", accent=BLUE)
        takeaway(compare_table("A Role Instruction Is a Contract, Not a Personality",
            ["Section", "What it states", "Why it matters"],
            [["Purpose", "The single transformation this role owns", "Prevents scope drift"],
             ["Allowed inputs", "Which files, data and sources may be read", "Confines the blast radius"],
             ["Output schema", "The artifact, its path and its required fields", "Makes acceptance objective"],
             ["Exclusions", "What this role must never do", "The most valuable section"],
             ["Escalation", "When to stop and ask the board", "Keeps authority explicit"]],
            kicker="LO2 · WRITING THE ROLE", accent=TEAL),
            "If two roles could both plausibly do the task, your instructions are not finished.")
        tile_grid("Workspaces, Secrets and Skills", [
            ("Dedicated workspace", "One local root per role, isolated with git worktrees so "
             "every change is attributable to exactly one agent."),
            ("Git baseline", "Commit an empty baseline so the later diff means what you think "
             "it means."),
            ("Secrets stay out", "Credentials live in the runtime or the Paperclip secret "
             "store, injected at heartbeat time — never in prompts, notes or Git."),
            ("Skills are capability", "Import a skill from a path or URL into the org-wide "
             "library, then attach it to a specific agent."),
            ("Adapters bridge capability", "Match role complexity, session needs and tool "
             "access to the adapter you choose."),
            ("Prove it with a marker run", "Configuration that has never produced an artifact "
             "is not a connection.")],
            kicker="LO2 · SEPARATE CONTEXT FROM AUTHORITY", cols=2, size=14, accent=VIOLET)
    elif num == 3:
        img_points("Goal Lineage — Every Issue Carries Its Reason",
                   "diagram-goal-lineage.png", [
            ("Mission", "One measurable outcome defines why the company exists."),
            ("Project goal", "A budgeted scope the agent reads at runtime."),
            ("Parent issue", "The synthesis — created unassigned so it cannot wake early."),
            ("Child issues", "Specialist work, assigned ONE AT A TIME.")],
            kicker="LO3 · THE AGENT SEES WHY, NOT ONLY WHAT", accent=VIOLET)
        img_points("Assign One Child at a Time", "chart-sequential-runs.png", [
            ("Assignment is the trigger", "Creating an issue does not wake anyone — assigning "
             "it does."),
            ("Sequential = attributable", "Non-overlapping runs let you tie each artifact to "
             "exactly one run."),
            ("Overlapping = unverifiable", "If both ran at once you cannot prove the hand-off "
             "actually happened."),
            ("Bound every wait", "An unbounded wait hides a failed adapter behind apparent "
             "patience.")],
            kicker="LO3 · WHY SEQUENCE MATTERS", accent=TEAL)
        img_points("Verifying Between Disparate Components",
                   "diagram-evidence-chain.png", [
            ("Five places, one thread", "Issue ID, run log, comment, workspace diff and cost "
             "entry must agree."),
            ("The diff is king", "Read what actually changed on disk before accepting any "
             "agent's summary."),
            ("Status is not evidence", "'Done' with no artifact and no diff is an unverified "
             "claim."),
            ("Name the evidence", "An acceptance criterion states the artifact, its path and "
             "its fields.")],
            kicker="LO3 · WHAT 'VERIFIED' ACTUALLY MEANS", accent=BLUE)
        takeaway(tile_grid("Hand-Off Acceptance — What You Are Actually Checking", [
            ("Consumable without a question", "The receiving agent can use the artifact "
             "without asking the producer anything."),
            ("Limitations stated", "An agent that reports what it could NOT establish is more "
             "useful than one that quietly guesses."),
            ("Idempotent", "One event should not create many outcomes — re-running must not "
             "duplicate the work."),
            ("Traceable", "Every claim in the deliverable points back to a named source in "
             "the allowed inputs.")],
            kicker="LO3 · ACCEPTING WORK", cols=2, size=14, accent=TEAL),
            "Accept artifacts and explicit limitations — never a status change on its own.")
    elif num == 4:
        img_points("Layered Budgets — Warn, Then Stop",
                   "diagram-layered-budgets.png", [
            ("Three rings", "Company, project and agent — the innermost cap that binds fires "
             "first."),
            ("Enforced at checkout", "Not at billing. The loop stops at the ceiling."),
            ("Baseline first", "Record current spend and expected run frequency before you "
             "rely on a cap."),
            ("Token-level costing", "Tracked by provider, model, agent and project — which is "
             "what makes the cap meaningful.")],
            kicker="LO4 · COST CONTROL AS A CIRCUIT BREAKER", accent=VIOLET)
        img_points("Why the Cap Is Enforced at Checkout",
                   "chart-budget-burndown.png", [
            ("Without a cap", "A runaway loop keeps spending until someone notices the "
             "invoice."),
            ("With a cap", "Spend flattens at the ceiling and the agent simply stops."),
            ("The cap is a control", "Not a budget estimate — it is the thing that makes "
             "unattended operation safe."),
            ("Set it below the pain", "A cap you would be unhappy to actually pay is set too "
             "high.")],
            kicker="LO4 · THE ENGINEERING ARGUMENT", accent=AMBER)
        takeaway(tile_grid("Routines — Automation Earns the Schedule", [
            ("Create it PAUSED", "A routine live before it has ever succeeded is unreviewed "
             "scheduled spend."),
            ("State the trigger explicitly", "`30 16 * * *` WITH an IANA timezone such as "
             "Asia/Singapore."),
            ("Prove it once by hand", "One bounded manual run, reviewed by a human."),
            ("Leave it paused", "Until you have read the generated issue, the run and the "
             "cost."),
            ("Name the artifact", "The routine body must state what file it produces, or the "
             "run is unverifiable."),
            ("Watch for concurrency", "One event should not create many outcomes.")],
            kicker="LO4 · SCHEDULED WORK", cols=2, size=14, accent=TEAL),
            "An implicit timezone is a production incident waiting to happen.")
        img_points("The Approval and Audit Loop", "diagram-approval-loop.png", [
            ("Propose, then hold", "The governed action does not execute while it is pending."),
            ("A human decides", "With a RECORDED rationale — that sentence is the audit."),
            ("The log is durable", "Mutations, heartbeats, cost events and approvals all land "
             "in Activity."),
            ("The loop closes", "When the whole operation can be reconstructed from the log "
             "alone.")],
            kicker="LO4 · HUMAN AUTHORITY STAYS EXPLICIT", accent=BLUE)
        img_points("The Operator Intervention Ladder",
                   "diagram-intervention-ladder.png", [
            ("Inspect", "Read task, run, cost and activity evidence BEFORE acting."),
            ("Pause", "Stop new heartbeats while keeping all state."),
            ("Reassign", "Move the work to another role."),
            ("Terminate", "The last rung — and it is not reversible.")],
            kicker="LO4 · USE THE LEAST IRREVERSIBLE CONTROL", accent=AMBER)
        img_points("Deployment Options — Exposure Is a Decision",
                   "diagram-deployment.png", [
            ("Loopback", "The default and least exposed — trusted local only."),
            ("LAN / tailnet", "`--bind lan` or `--bind tailnet` widen reach and REQUIRE "
             "authentication."),
            ("Hosted", "Container plus external PostgreSQL, a persistent volume, a signing "
             "secret and an allowed-hostnames list."),
            ("Portability", "A whole company exports and imports with secrets scrubbed and "
             "collisions re-mapped.")],
            kicker="LO4 · TAKING IT BEYOND THE LAPTOP", accent=TEAL)


for t in C.TOPICS:
    section(f"TOPIC {t['code']}", t["title"], t["code"], t["subtitle"])
    cons = t["concepts"]
    third = (len(cons) + 2) // 3
    for ci in range(0, len(cons), third):
        chunk = cons[ci:ci + third]
        if not chunk:
            continue
        suffix = "" if ci == 0 else " (continued)"
        tile_grid(f"Key Concepts — {t['title']}{suffix}", chunk,
                  kicker=f"TOPIC WEIGHTING {t['weighting']}", cols=2, size=13)
    topic_extras(t["num"])
    acts = TOPIC_ACTS[t["num"]]
    if acts:
        cards3(f"Hands-On Labs — {t['title']}",
               [(c, f"Lab {a['num']}", [a["title"], a.get("company", "")])
                for c, a in zip([BLUE, TEAL, VIOLET], acts)] +
               [(AMBER, "—", ["—"])] * (3 - len(acts)) if len(acts) < 3 else
               [(c, f"Lab {a['num']}", [a["title"], a.get("company", "")])
                for c, a in zip([BLUE, TEAL, VIOLET], acts)],
               kicker="WHAT YOU'LL DO")
    for a in acts:
        lab_card(a)
        # Stage captions come from the lab's authored `flow` (short phrases sized to
        # the chip). Falling back to slicing a step sentence produced captions cut
        # mid-word, so the flow list is the single source for the process map.
        stg = [(_ellipsis(lbl, 44), _ellipsis(cap, 58))
               for lbl, cap in a.get("flow", [])][:5]
        if len(stg) >= 3:
            process_map(f"How Lab {a['num']} Runs", stg,
                        kicker=f"LAB {a['num']} · PROCESS MAP", color=TEAL,
                        synthesis=("THE POINT", a["objective"]))
        test_slide(a["title"], a["test"], kicker=f"LAB {a['num']} · VERIFY",
                   troubleshoot=a.get("troubleshoot"))
        lab_troubleshoot(a)
    content(f"Recap — {t['title']}",
            ["You can now: " + a["objective"] for a in acts] +
            [c for c in t["concepts"][:3]],
            kicker="TOPIC RECAP", size=15)

# ------------------------------------------------------------- CLOSE
section("WRAP-UP", "Course Summary & Next Steps", "")
tile_grid("What You Achieved", C.LO_SHORT,
          kicker="LEARNING OUTCOMES", cols=2, size=14)
tile_grid("A Governed Multi-Agent Operating Checklist", [
    ("Mission is measurable", "A target, a metric and a boundary — or it cannot be verified."),
    ("Caps exist before runtimes", "Company, then project, then agent — set before anything runs."),
    ("Every role is confined", "Its own workspace, instruction file, adapter and budget."),
    ("Issues are created unassigned", "Assignment is the trigger; assign one at a time."),
    ("Acceptance names the evidence", "The artifact, its path and its required fields."),
    ("The audit reconstructs", "Activity alone tells the whole story, with no unexplained gap.")],
    kicker="TAKE THIS BACK TO WORK", cols=2, size=14, accent=TEAL)
tile_grid("Continue Your Learning", [
    ("Official project", "https://github.com/paperclipai/paperclip — the source, the docs "
     "and the release notes."),
    ("Hosted Paperclip", "https://paperclip.inc — the managed control plane if you do not "
     "want to self-host."),
    ("Rebuild the labs", "Redo each of the six companies from scratch until the control "
     "sequence is automatic."),
    ("Start with one real workflow", "Choose an internal task whose inputs and outputs are "
     "already observable."),
    ("Keep the caps low", "Your first real company should be capped far below what you "
     "would be willing to pay."),
    ("Audit before you scale", "Prove you can reconstruct one operation before you run two.")],
    kicker="NEXT STEPS", cols=2, size=14)
tile_grid("Recommended Courses", [(rc, "") for rc in C.RECOMMENDED_COURSES],
          kicker="CONTINUE WITH TERTIARY INFOTECH", cols=1, size=15)
tile_grid("Support", [
    ("Email", "enquiry@tertiaryinfotech.com"),
    ("Telephone", "+65 6100 0613"),
    ("Website", "www.tertiarycourses.com.sg"),
    ("LMS / TMS", "https://lms-tms.tertiaryinfotech.com"),
    ("Practice exam", "https://exams.tertiaryinfotech.com"),
    ("Course page", "www.tertiarycourses.com.sg/wsq-manage-ai-agents-with-paperclip.html")],
    kicker="WE'RE HERE TO HELP — DURING AND AFTER THE CLASS", cols=2, size=14)
tile_grid("Briefing for Assessment", [
    ("Do · Clear your desk", "Place phones and other materials under the table or on the floor."),
    ("Don't · No recording", "No photos or recording of assessment scripts."),
    ("Don't · No discussion", "Work individually — no discussion during the assessment."),
    ("Do · Black or blue pen", "Use a black or blue pen for hard-copy assessments."),
    ("Don't · No correction fluid", "No liquid paper or correction tape may be used."),
    ("Do · Stop on time", "Scripts are collected when time is up.")],
    kicker="BEFORE YOU START", cols=2, size=14, accent=AMBER)
tile_grid("Assessment", [
    ("Written Assessment (SAQ)", "5 short-answer knowledge questions · 1 hour · open book."),
    ("Practical Performance (PP)", "4 hands-on Paperclip tasks · 1 hour · open book."),
    ("Digital attendance", "Remember to take the Assessment digital attendance before you start."),
    ("Submit on the LMS", "Upload your completed answers at https://lms-tms.tertiaryinfotech.com/")],
    kicker="WRAP-UP", cols=2, size=15)
process_map("Assessment Flow", [
    ("TRAQOM survey", "Scan the QR code on the LMS"),
    ("Digital attendance", "Scan the SSG assessment QR"),
    ("Sit WA then PP", "Open book · 1 hour each"),
    ("Submit on the LMS", "Upload your completed answers"),
    ("Sign the record", "Sign the Assessment Summary Record")],
    kicker="ON ASSESSMENT DAY", color=BLUE,
    synthesis=("REMEMBER", "All five steps are mandatory for WSQ funding — missing the "
               "digital attendance or the TRAQOM survey can invalidate your claim."))
tile_grid("Digital Attendance (Mandatory)", [
    ("Three times a day", "Take the AM, PM and Assessment digital attendance — mandatory "
     "for every WSQ-funded course."),
    ("Trainer shows the QR", "The trainer or administrator displays the digital attendance "
     "QR code from the SSG portal."),
    ("Scan and submit", "Scan the QR code with your mobile phone camera and submit your "
     "attendance."),
    ("75% minimum", "A minimum of 75% attendance is required to be eligible for assessment "
     "and funding.")],
    kicker="TRAQOM · SSG DIGITAL ATTENDANCE", cols=2, size=15)
big_statement("Thank You!",
              "You can now build, coordinate and govern a Paperclip AI agent company from "
              "mission to audited outcome.", "HAPPY BUILDING", color=TEAL)

# ------------------------------------------------------------- motion pass
for s in prs.slides:
    joined = " ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame)
    is_div = any(k in joined for k in ("COURSE ADMINISTRATION", "CORE CONCEPTS", "WRAP-UP")) or \
             any(t["title"] in joined and f"TOPIC {t['code']}" in joined for t in C.TOPICS)
    _transition(s, "push" if is_div else "fade", speed="med" if is_div else "fast")

OUT = os.path.join(REPO, "courseware", f"{C.SHORT_TITLE}-{C.VERSION}.pptx")
prs.save(OUT)
print(f"Saved {OUT}  ({len(prs.slides._sldIdLst)} slides)")
