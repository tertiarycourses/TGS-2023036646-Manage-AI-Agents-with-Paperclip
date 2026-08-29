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
    """One bold boxed rule at the bottom of a concept slide.

    The band occupies 6.28"-6.94". A tile_grid (or any body component) lays its
    content out over the full 1.95"-6.73" area, so the band would otherwise be
    drawn ON TOP of the bottom row and clip it. Before drawing, therefore, we
    SCALE the existing body shapes vertically into the space that remains above
    the band — geometry only, so every component keeps its own styling.
    """
    BAND_Y, BAND_H = Inches(6.28), Inches(0.66)
    GAP = Inches(0.16)
    BODY_TOP = Inches(1.95)                 # where every body component starts
    limit = BAND_Y - GAP                    # bottom the body must respect

    body = [sh for sh in s.shapes
            if sh.top is not None and sh.height is not None
            and sh.top >= BODY_TOP - Inches(0.05)
            and sh.top < Inches(7.0)]
    if body:
        bottom = max(sh.top + sh.height for sh in body)
        if bottom > limit:
            avail = limit - BODY_TOP
            span = bottom - BODY_TOP
            k = avail / span
            for sh in body:
                mid = sh.top + sh.height / 2.0        # keep each shape's centre
                new_mid = BODY_TOP + (mid - BODY_TOP) * k
                # Circular badges (and the number sitting inside them) must not be
                # squashed into ellipses — recentre them at their original size.
                square = abs(sh.width - sh.height) < Inches(0.06)
                h = sh.height if square else max(1, int(sh.height * k))
                sh.height = int(h)
                sh.top = int(new_mid - h / 2.0)

    rect(s, Inches(0.85), BAND_Y, Inches(11.6), BAND_H, LIGHT)
    rect(s, Inches(0.85), BAND_Y, Inches(0.1), BAND_H, color)
    txt(s, Inches(1.15), BAND_Y, Inches(11.2), BAND_H,
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
    ("Five triggers", "A schedule/interval tick, a task assignment, an @-mention, a "
     "manual Run Heartbeat, or an approval being resolved."),
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
        compare_table("The Four Additions That Make an Agent",
            ["Addition", "What it provides", "What breaks without it"],
            [["Reasoning / planning", "Decomposes a goal into steps before acting, and "
              "re-plans when a step fails.",
              "Answers in one shot; cannot recover from a wrong first move."],
             ["Tool use", "Calls functions, CLIs and APIs to read live data and take real "
              "action.", "The system can only talk about the work; it cannot do it."],
             ["Memory / state", "Context carries across turns and across separate execution "
              "windows.", "Every wake-up starts from nothing and repeats work already done."],
             ["Autonomy", "Decides which tool, in which order, and when it is finished.",
              "A human drives every step — a chatbot with extra latency."]],
            kicker="LO1 · FROM A LANGUAGE MODEL TO AN AGENT", accent=BLUE,
            note="Add a fifth ingredient — several agents dividing the work — and you have a "
                 "multi-agent system. That is where the interesting failures start.")
        takeaway(tile_grid("Why Coordination Is the Hard Part", [
            ("DIRECTION", "Each agent must know not only what to do but WHY — or it optimises "
             "the wrong thing very efficiently."),
            ("AUTHORITY", "Who may hire, spend and ship. Left implicit it defaults to "
             "'whatever the agent decided to try'."),
            ("ISOLATION", "Two agents writing to the same place corrupts both pieces of work "
             "and destroys attribution."),
            ("COST", "An agent in a retry loop does not get tired. Without a ceiling you "
             "discover the problem on the invoice."),
            ("EVIDENCE", "'The agent says it is done' is not 'it is done'. Someone must check "
             "later, without taking anyone's word."),
            ("THE MAPPING", "These five concerns are exactly what the twelve subsystems "
             "address — map each subsystem back to one.")],
            kicker="LO1 · FIVE ORGANISATIONAL PROBLEMS, NOT MODEL PROBLEMS",
            cols=2, size=13, accent=VIOLET),
            "Running one agent is a prompting problem. Running five is an organisational one.")
        compare_table("The Official Vocabulary — Learn It Verbatim",
            ["Term", "The documentation's own definition"],
            [["Company", "A self-contained AI organisation with a single goal, a team of "
              "agents, a task board, and a budget."],
             ["Agent", "An AI employee — a configured role with a specific job, a manager, "
              "and a monthly budget."],
             ["Task (issue)", "A unit of work — like a ticket on a project board, except it "
              "is assigned to an AI agent, not a human."],
             ["Heartbeat", "A scheduled execution window — when an agent wakes up, checks its "
              "inbox, and does work."],
             ["Adapter", "The connection between Paperclip and the AI system that actually "
              "runs your agent."],
             ["Budget", "A monthly spending cap that Paperclip enforces automatically so your "
              "agents never overspend."],
             ["Approval", "A governance gate — a checkpoint where Paperclip pauses and asks "
              "you to sign off before an action proceeds."]],
            kicker="LO1 · THE ASSESSMENT USES THIS VOCABULARY", accent=TEAL,
            note="Notice what is absent: nothing about prompting, model selection or how an "
                 "agent reasons. That omission is deliberate.")
        compare_table("LLM vs Agent vs Agent Company",
            ["Dimension", "A language model", "A single agent", "A Paperclip company"],
            [["What it does", "Answers", "Acts", "Coordinates several actors"],
             ["Memory", "None beyond the prompt", "Within one session",
              "Across heartbeats, in the control plane"],
             ["Authority", "None", "Whatever you allow implicitly",
              "Explicit — org chart, roles and approvals"],
             ["Cost visibility", "Per request", "Discovered on the invoice",
              "Capped at checkout by company, project and agent"],
             ["Evidence", "The reply text", "Scrollback you must trust",
              "Runs, comments, diffs and a durable activity log"]],
            kicker="LO1 · THREE LAYERS, THREE DIFFERENT PROBLEMS", accent=VIOLET,
            note="Paperclip is the third layer. It does not make your agents smarter — it "
                 "makes a team of them accountable.")
        takeaway(tile_grid("What Paperclip Is NOT", [
            ("NOT an agent framework", "It does not dictate how your agent reasons, prompts "
             "or calls tools. That is the adapter's job."),
            ("NOT a chatbot", "There is no conversational surface for you to talk to a model "
             "through."),
            ("NOT a workflow builder", "There is no drag-and-drop canvas of nodes and edges "
             "to wire together."),
            ("NOT a prompt manager", "Prompts live with the runtime and the skill, not in a "
             "prompt library inside Paperclip."),
            ("NOT for a single agent", "One agent does not need an org chart — the "
             "coordination overhead would be pure cost."),
            ("SO WHAT IS IT?", "An organisational control plane: Node.js plus React on port "
             "3100, backed by PostgreSQL on port 54329.")],
            kicker="LO1 · SCOPING THE TOOL SAVES WASTED EVALUATION TIME",
            cols=2, size=13, accent=AMBER),
            "Paperclip manages the company. Adapters run the agents.")
        compare_table("The Feasibility Scan — One Agent or a Team?",
            ["Factor", "Points to ONE agent", "Points to a TEAM"],
            [["Separability", "One instruction still describes the job clearly.",
              "The instruction has become a list of unrelated responsibilities."],
             ["Expertise", "One skill set covers it.",
              "Genuinely different expertise is required for different parts."],
             ["Independent evidence", "The doer can reasonably check their own work.",
              "Evidence must be produced INDEPENDENTLY of whoever consumes it."],
             ["Observability", "Inputs and outputs are already observable.",
              "The same — a prerequisite either way, not a reason to split."],
             ["Cost of coordination", "Low volume, short task.",
              "The work recurs often enough to amortise the setup."]],
            kicker="LO1 · THE MOST COMMERCIALLY USEFUL JUDGEMENT", accent=TEAL,
            note="The test is one question: are the INPUTS, TOOLS, AUTHORITY and VERIFICATION "
                 "the same across the whole task? If yes, use one agent.")
        decision_map("Should This Work Become an Agent Company?",
            "Are the inputs, tools,\nauthority and verification\nthe SAME across the\nwhole task?",
            ("YES — stay with ONE agent",
             "One instruction still describes the job clearly. Splitting adds nothing but "
             "surface area to debug, budget and audit."),
            ("NO — build the company",
             "Different expertise, or evidence must be produced independently of whoever will "
             "consume it. Split into roles, one transformation each."),
            kicker="LO1 · REACH FOR ONE AGENT AND BE ARGUED OUT OF IT", color=VIOLET,
            note="Sanity check before you build anything: write the mission as one sentence. If "
                 "you cannot, you do not understand the work well enough to delegate it.")
        compare_table("Twelve Subsystems — Who Owns Which Problem?",
            ["Subsystem", "The question it answers"],
            [["Identity · Org chart", "Who is this, who do they report to, and what may they do?"],
             ["Work · Heartbeat", "What needs doing, who owns it now, and when does an agent wake?"],
             ["Workspaces", "Where does this agent's work live, and who else can touch it?"],
             ["Governance · Budget", "Which actions need a human decision, and what is the ceiling?"],
             ["Routines · Plugins", "What recurs unasked, and how do we extend without forking?"],
             ["Secrets", "Where do credentials live, and how do they reach a run without leaking?"],
             ["Activity · Portability", "What happened, in order and durably — and how do we move it?"]],
            kicker="LO1 · KNOW WHERE TO LOOK WHEN SOMETHING MISBEHAVES", accent=BLUE,
            note="You do not need to recite the twelve. You should be able to say which one "
                 "owns a given problem — that is how you know where to look.")
    elif num == 2:
        img_points("The Agent Org Chart", "diagram-org-chart.png", [
            ("Board approves", "Hires, strategy and material exceptions stay with the human."),
            ("The CEO owns alignment", "Goal alignment, decomposition and final synthesis."),
            ("Specialists own transformations", "One distinct job, one authority boundary, "
             "one deliverable."),
            ("Six fields per agent", "Role · manager · adapter · instructions · heartbeat · "
             "budget.")],
            kicker="LO2 · ACCOUNTABILITY HAS A SHAPE", accent=BLUE)
        compare_table("A Role Instruction Is a Contract, Not a Personality",
            ["Section", "What it states", "Why it matters"],
            [["Purpose", "The single transformation this role owns", "Prevents scope drift"],
             ["Allowed inputs", "Which files, data and sources may be read", "Confines the blast radius"],
             ["Output schema", "The artifact, its path and its required fields", "Makes acceptance objective"],
             ["Exclusions", "What this role must never do", "The most valuable section"],
             ["Escalation", "When to stop and ask the board", "Keeps authority explicit"]],
            kicker="LO2 · WRITING THE ROLE", accent=TEAL,
            note="If two roles could both plausibly do the task, your instructions are not finished.")
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
        compare_table("The Six Fields That Define Every Agent",
            ["Field", "What it controls", "Get it wrong and"],
            [["Role", "What this agent is for — the single transformation it owns.",
              "Scope drifts into a neighbouring role's work."],
             ["Manager", "Its reporting line. Exactly one, except for the CEO.",
              "Accountability has no shape; nobody owns the outcome."],
             ["Adapter", "Which runtime actually executes its work.",
              "The agent is configured but can never run."],
             ["Instructions", "Its contract: purpose, inputs, output schema, exclusions, escalation.",
              "Acceptance becomes a matter of opinion."],
             ["Heartbeat", "When it wakes, and on which triggers.",
              "It either never wakes, or wakes and bills when idle."],
             ["Budget", "Its individual monthly ceiling.",
              "A retry loop spends until someone reads the invoice."]],
            kicker="LO2 · HIRING IS A CONFIGURATION DECISION", accent=BLUE,
            note="Paperclip enforces a strict hierarchy: every agent reports to exactly ONE "
                 "manager, and the CEO is the only agent with no manager.")
        compare_table("The Five Instruction Sections and Why Each Matters",
            ["Section", "States", "Why it matters"],
            [["PURPOSE", "The single transformation this role owns",
              "Prevents scope drift into a neighbouring role's work."],
             ["ALLOWED INPUTS", "Which files, data and sources may be read",
              "Confines the blast radius when something goes wrong."],
             ["OUTPUT SCHEMA", "The artifact, its path, and its required fields",
              "Makes acceptance objective rather than a matter of opinion."],
             ["EXCLUSIONS", "What this role must NEVER do",
              "The most valuable section — and the one people leave out."],
             ["ESCALATION", "When to stop and ask the board",
              "Keeps human authority explicit instead of assumed."]],
            kicker="LO2 · A CONTRACT, NOT A PERSONALITY", accent=TEAL,
            note="Tone does not constrain behaviour; structure does. If two roles could each "
                 "plausibly claim the same task, your instructions are not finished.")
        compare_table("Suggested Starting Budgets by Seniority",
            ["Role", "Suggested monthly budget", "The reasoning"],
            [["CEO", "$30–50 per month",
              "Owns alignment, decomposition and synthesis — it wakes on more events than "
              "anyone else."],
             ["Manager (CTO or CMO)", "$20–40 per month",
              "Coordinates a sub-team, so it runs more often than a worker but less than the CEO."],
             ["Worker agent", "$10–25 per month",
              "One transformation, run on assignment. The cheapest role to cap tightly."],
             ["Company (total)", "Set BEFORE the first hire",
              "Enforcement happens at checkout, so the cap must exist before anyone can check "
              "out work."]],
            kicker="LO2 · FROM THE OFFICIAL DOCUMENTATION", accent=VIOLET,
            note="These are a sanity check on your own numbers, not a rule. A cap you would be "
                 "unhappy to actually pay is set too high.")
        process_map("The Six-Step Heartbeat Execution Arc", [
            ("Trigger", "Schedule, assignment, mention, manual or approval"),
            ("Adapter invocation", "Paperclip calls the configured adapter"),
            ("Process spawn", "The runtime process starts in the workspace"),
            ("Paperclip API calls", "The agent reads work and writes results back"),
            ("Result capture", "Output, artifacts and token usage recorded")],
            kicker="LO2 · ALMOST EVERY FAULT IS 'WHICH STEP FAILED?'", color=BLUE,
            synthesis=("STEP 6 · RUN RECORD STORAGE",
                       "The run, its cost and its activity entries are persisted. This rarely "
                       "fails — but if it does, the audit trail has a gap you must explain."))
        compare_table("Where Each Heartbeat Step Fails",
            ["Step", "The usual failure", "First thing to check"],
            [["1 · Trigger", "Nothing assigned and the interval is off (the default)",
              "The assignee. Creating an issue does not wake anyone."],
             ["2 · Adapter invocation", "Adapter misconfigured, or runtime not authenticated",
              "Run the runtime's own CLI directly and sign in."],
             ["3 · Process spawn", "The binary is missing, or the sandbox cannot start",
              "The runtime install, outside Paperclip."],
             ["4 · API calls", "Checkout conflict (409), or the cross-issue write limit of 20",
              "Whether another agent already holds the issue."],
             ["5 · Result capture", "The process is lost mid-run — error kind process_lost",
              "The run log. Resume recovers it; a fresh run is not needed."]],
            kicker="LO2 · DIAGNOSING A HEARTBEAT", accent=AMBER,
            note="Session persistence records a session ID before and after each run. If the "
                 "pair differs the session rotated; if it matches, the conversation continued.")
        takeaway(tile_grid("The Seven Agent States", [
            ("active", "Enabled and ready for heartbeats."),
            ("idle", "Active, but no heartbeat is currently running."),
            ("running", "A heartbeat is in progress right now."),
            ("error", "The last heartbeat failed — not working, and did not stop gracefully."),
            ("paused", "Deliberately stopped, by you or automatically on hitting the budget limit."),
            ("terminated", "Permanently deactivated. NOT reversible."),
            ("pending_approval", "Hired but awaiting board approval before it may run."),
            ("Run statuses differ", "Runs are queued, running, succeeded, failed, timed out or "
             "cancelled — plus the error kind process_lost.")],
            kicker="LO2 · READ THE STATE BEFORE YOU DIAGNOSE", cols=2, size=13, accent=BLUE),
            "Pause is reversible. Terminate is not. Read the menu item twice before clicking.")
        compare_table("The Four Instruction Files",
            ["File", "Answers", "Loaded"],
            [["AGENTS.md", "The operating manual — the entry file, and the default.",
              "Every run. Keep it the map, not the whole territory."],
             ["SOUL.md", "Persona and decision philosophy — how this role weighs trade-offs.",
              "When judgement is needed, not on every wake."],
             ["HEARTBEAT.md", "The per-heartbeat checklist — what to do on every single wake.",
              "Every run. This is the file that costs you on every heartbeat."],
             ["TOOLS.md", "Available tools and API notes — what this role may call.",
              "When the agent needs to know its own capability surface."]],
            kicker="LO2 · MANAGED BUNDLE OR EXTERNAL VIA ROOTPATH", accent=TEAL,
            note="The split matters for cost as much as clarity: material needed on every run "
                 "is separated from material that is only occasionally relevant.")
        compare_table("Reading the Dashboard at a Glance",
            ["Signal", "Healthy", "Needs attention"],
            [["Agents enabled", "Mostly active or running",
              "Any in error, or unexpectedly paused"],
             ["Tasks in progress", "Work is moving",
              "Nothing in progress for hours, or many blocked"],
             ["Month spend", "Climbing predictably",
              "A sudden jump, or active budget incidents"],
             ["Pending approvals", "Queue manageable", "Approvals piling up unattended"],
             ["Recent activity", "Steady, understandable motion",
              "Long silence, or repeated failures"]],
            kicker="LO2 · COCKPIT INSTRUMENTS, NOT AN INVESTIGATION TOOL", accent=AMBER,
            note="The healthy pattern for a small company is ONE agent running while the "
                 "others stay active — otherwise you cannot attribute a change by timing alone.")
        tile_grid("Adapter Type Keys — The Eleven", [
            ("claude_local", "Claude Code running locally."),
            ("codex_local", "OpenAI Codex CLI running locally."),
            ("gemini_local", "Gemini CLI running locally."),
            ("opencode_local", "OpenCode running locally."),
            ("cursor", "Cursor — local and cloud variants exist."),
            ("pi_local", "Pi running locally."),
            ("hermes_local", "Hermes running locally."),
            ("grok_local", "Grok running locally."),
            ("process", "An arbitrary local process."),
            ("http", "An HTTP or webhook endpoint."),
            ("openclaw_gateway", "OpenClaw via its gateway.")],
            kicker="LO2 · THE LAST THREE SHOW AS 'COMING SOON' IN THE UI",
            cols=2, size=13, accent=VIOLET)
        takeaway(tile_grid("Adapter Defaults That Cost You Money", [
            ("maxTurnsPerRun · 300", "The Claude Code adapter defaults to a maximum of 300 "
             "turns per run. That is a lot of tokens if a loop goes wrong."),
            ("dangerouslySkipPermissions · true", "The Claude Code adapter default. Know it is "
             "set before you let an agent run unattended."),
            ("Sandbox timeout · 14,400s", "Four hours. A stuck run holds the workspace for "
             "that long unless you intervene."),
            ("Look before you leave it", "Every one of these is a number you should read "
             "during configuration, not after an incident.")],
            kicker="LO2 · READ THE DEFAULTS BEFORE UNATTENDED OPERATION",
            cols=2, size=14, accent=AMBER),
            "Adapter readiness is proved by a marker run — never by a saved configuration.")
        flow_h("The Workspace Lifecycle", [
            "provisioning — being created",
            "validating — being checked",
            "ready — usable by the agent",
            "degraded — usable, but something is wrong",
            "repairing — being fixed",
            "failed / archived — unusable, or retired"],
            kicker="LO2 · A DEGRADED WORKSPACE LOOKS LIKE A LAZY AGENT", color=TEAL)
        worked_example("Skills — Capability on Demand, Not in Every Prompt",
            "A skill is a reusable instruction document an agent loads only when relevant. "
            "The economy is the point: ten skills, but not ten skills loaded per heartbeat.",
            ["skills/",
             "└── code-review/",
             "    ├── SKILL.md",
             "    └── references/",
             "        └── examples.md",
             "",
             "# SKILL.md frontmatter",
             "---",
             "name: code-review",
             "description: >",
             "  Use when asked to review a pull",
             "  request or code diff.",
             "  Don't use when writing new code",
             "  from scratch.",
             "---"],
            [("DESCRIPTION IS DECISION LOGIC",
              "Write when to use it AND when not to — that sentence is what the agent reads "
              "to decide whether to load the skill at all."),
             ("COMPANY-SCOPED",
              "Skills are never shared across companies. Folders may nest up to four levels "
              "deep."),
             ("ATTACHED AT HIRE OR LATER",
              "Via desiredSkills at hire time, or later through the skills sync endpoint with "
              "mode add, remove or replace."),
             ("A DOCUMENTED CONTRADICTION",
              "The Skills API says bundled skills are force-unioned into every agent; the "
              "newer CLI page says they are not. Verify on your own install.")],
            kicker="LO2 · CONTEXT ECONOMY", accent=VIOLET)
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
        compare_table("The Seven Issue States",
            ["State", "The documentation's own definition"],
            [["backlog", "The issue exists and has been identified, but no one is working on "
              "it yet."],
             ["todo", "The issue is ready to start. An agent has been assigned and is waiting "
              "to check it out."],
             ["in_progress", "An agent has checked out the issue and is actively working on "
              "it. Only ONE agent may hold this state at a time."],
             ["in_review", "The agent has completed the work and moved the issue to review. "
              "It is waiting for sign-off."],
             ["done", "TERMINAL. The work is complete."],
             ["blocked", "The agent cannot move forward. Something is preventing progress."],
             ["cancelled", "TERMINAL. The issue is no longer needed and will not be completed."]],
            kicker="LO3 · THE ASSESSMENT EXPECTS THESE BY NAME", accent=BLUE,
            note="Issues do not move backwards. A terminal issue is revived only through an "
                 "explicit reopen — never by editing its status.")
        flow_h("The Normal Issue Path", [
            "backlog — identified, nobody working",
            "todo — assigned, waiting to check out",
            "in_progress — checked out, exclusive",
            "in_review — done, awaiting sign-off",
            "done — terminal"],
            kicker="LO3 · WITH BLOCKED AND CANCELLED AS DEPARTURES", color=TEAL)
        compare_table("Checkout Discipline — Four Common Mistakes",
            ["Mistake", "What to do instead"],
            [["PATCHing status directly to in_progress",
              "Never do this. Use the checkout mechanism — a direct status write bypasses the "
              "lock entirely."],
             ["Retrying after a 409 Conflict",
              "Treat 409 as TERMINAL. Another agent holds the issue; retrying will not win "
              "the race."],
             ["Expecting a cancelled blocker to unblock its dependents",
              "Cancelled blockers never auto-unblock dependents. Resolve the dependency "
              "explicitly."],
             ["Editing a done issue's status to reopen it",
              "Terminal issues reopen only via an explicit reopen flag, not a status edit."],
             ["Writing to the whole board from one run",
              "CROSS_ISSUE_INFLUENCE_LIMIT is 20 — one heartbeat may write to at most twenty "
              "other issues."]],
            kicker="LO3 · THE RULE THAT PREVENTS DOUBLE WORK", accent=AMBER,
            note="Runs identify themselves with a run-id header. That is how a write is "
                 "attributed to the execution that made it.")
        takeaway(tile_grid("The Five Heartbeat Triggers", [
            ("Schedule / interval", "The configured interval ticks — whether or not there is "
             "any work waiting."),
            ("Task assignment", "An issue is assigned to the agent. THIS is what makes "
             "assignment the real trigger for work."),
            ("Comment mention", "Someone @-mentions the agent in a comment on an issue."),
            ("Manual invoke", "A human presses Run Heartbeat."),
            ("Approval resolution", "An approval the agent was waiting on is finally decided."),
            ("Most people name three", "The two people miss are approval resolution and the "
             "@-mention — and both explain 'why did it just wake?'")],
            kicker="LO3 · BETWEEN HEARTBEATS THE AGENT DOES NOT EXIST",
            cols=2, size=13, accent=BLUE),
            "Heartbeat on interval is OFF by default — and that default is the right one.")
        compare_table("Paused versus Heartbeat-Off",
            ["Condition", "Wakes on interval", "Wakes on assignment, comment, routine, on-demand"],
            [["Heartbeat off", "No", "YES — the agent still responds to events"],
             ["Paused", "No", "No — a paused agent wakes on nothing at all"],
             ["Why it matters", "An interval costs money on every tick, work or not",
              "Event-driven waking costs nothing when nothing is happening"],
             ["The recommendation", "Interval OFF",
              "Wake-on-demand ON. The interval is a floor, not a guarantee."]],
            kicker="LO3 · TWO THINGS THAT LOOK THE SAME AND ARE NOT", accent=VIOLET,
            note="A busy agent may run MORE often than its interval, because events trigger "
                 "wakes independently of the clock.")
        compare_table("Acceptance Criteria — Activity versus Evidence",
            ["Fails — describes activity", "Works — names evidence"],
            [["The research is done.",
              "workspace/research-analyst/research.md exists and contains claim, source, date "
              "accessed and confidence for every claim."],
             ["Reconcile the control accounts.",
              "reconciliation.md lists every control account with ledger balance, statement "
              "balance and variance."],
             ["Review for compliance.",
              "exceptions.md lists each variance above SGD 500 with a stated cause and a "
              "recommended treatment."]],
            kicker="LO3 · THE HIGHEST-LEVERAGE WRITING SKILL IN THE COURSE", accent=TEAL,
            note="The test: could a stranger with no knowledge of the conversation look at the "
                 "workspace and say yes or no? If not, the criterion is not finished.")
        process_map("The Evidence Chain — One Thread, Five Places", [
            ("Issue ID", "What was asked, under which lineage"),
            ("Run log", "What actually executed, and whether it errored"),
            ("Comment", "What was accepted, by whom, on what basis"),
            ("Workspace diff", "What changed on disk — the strongest evidence"),
            ("Cost entry", "What it spent, and whether that is plausible")],
            kicker="LO3 · VERIFYING BETWEEN DISPARATE COMPONENTS", color=BLUE,
            synthesis=("STATUS IS NOT EVIDENCE",
                       "An issue marked done with no linked artifact and no diff is an "
                       "unverified claim, however confident the agent's summary sounds."))
        compare_table("Execution Policy Parameters",
            ["Parameter", "Value", "What it does"],
            [["maxReviewRounds", "Default 3 · range 1–50",
              "Caps how many times work can bounce back. A null value means the server "
              "default of 3."],
             ["approvalsNeeded", "Fixed at 1",
              "One approval advances the stage. This is not configurable."],
             ["changesRequestedCount", "Counts review rounds",
              "Escalates to a named reviewer once the cap is reached."],
             ["Comment-required backstop", "retry_queued → retry_exhausted",
              "The fallback path when a required comment never arrives."]],
            kicker="LO3 · A REVIEW WORKFLOW ENFORCED BY THE PLATFORM", accent=VIOLET,
            note="Once a reviewer is escalated to, only that reviewer may advance the stage. A "
                 "422 'only the escalated reviewer' error is the policy working, not a bug.")
        takeaway(tile_grid("Decomposition and Assignment Discipline", [
            ("Create everything COLD", "Parent synthesis issue and all children UNASSIGNED — "
             "assignment is a heartbeat trigger."),
            ("Why unassigned matters", "An issue created with an assignee wakes an agent "
             "before you have written the acceptance criteria or checked the caps."),
            ("Assign ONE child at a time", "Sequential runs are individually attributable; "
             "overlapping runs are not."),
            ("The proof you lose", "If two specialists ran simultaneously you cannot "
             "demonstrate the second consumed the first's output."),
            ("The parent waits", "The synthesis issue stays unassigned until every child has "
             "produced its artifact."),
            ("Bound every wait", "An unbounded wait hides a failed adapter behind apparent "
             "patience.")],
            kicker="LO3 · SEQUENCE IS A CONTROL, NOT A PREFERENCE",
            cols=2, size=13, accent=TEAL),
            "Creating an issue does not wake anyone. Assigning it does.")
        compare_table("Goal Lineage — What Each Level Supplies",
            ["Level", "What it carries", "What breaks if it is missing"],
            [["Company mission", "The measurable outcome the company exists for",
              "Agents optimise a local goal that does not serve the business."],
             ["Project goal", "A budgeted scope the agent reads at runtime",
              "Work has no boundary and no lifetime cap."],
             ["Parent issue", "The synthesis that consumes every child's output",
              "Nobody assembles the pieces; you do it by hand."],
             ["Child issue", "One specialist transformation with named evidence",
              "The instruction becomes a list of unrelated responsibilities."]],
            kicker="LO3 · LINEAGE IS FOUR LEVELS, NOT ONE SENTENCE", accent=BLUE,
            note="If you re-explain the goal in every issue body, your lineage is broken — and "
                 "you are paying for the same context repeatedly.")
        takeaway(tile_grid("Hand-Off Acceptance Tests", [
            ("Consumable without a question", "The receiving agent can use the artifact "
             "without asking the producer anything at all."),
            ("If the receiver must ask", "The output schema in the PRODUCER's instruction was "
             "under-specified. Fix the contract, not the artifact."),
            ("Limitations are stated", "An agent that reports what it could NOT establish is "
             "more useful than one that quietly guesses."),
            ("Idempotent", "One event should not create many outcomes — re-running must not "
             "duplicate the work."),
            ("Traceable", "Every claim points back to a named source inside the allowed inputs."),
            ("The diff is read first", "An agent describing its own work is a witness with an "
             "interest in the verdict.")],
            kicker="LO3 · WHAT YOU ARE ACTUALLY CHECKING", cols=2, size=13, accent=TEAL),
            "Accept artifacts and explicit limitations — never a status change on its own.")
        compare_table("Projects — Lifecycle and the Lifetime Cap",
            ["Project state", "Meaning", "Operator action"],
            [["backlog", "Identified, not yet scheduled", "Write the goal before you plan it."],
             ["planned", "Scoped and budgeted, not started",
              "Confirm the LIFETIME budget cap now — it is distinct from monthly caps."],
             ["in_progress", "Issues are being worked",
              "Watch the utilisation bar and the run cadence."],
             ["completed", "The goal has been met", "Close the audit map before you archive."],
             ["cancelled", "Abandoned", "Record why. A cancelled project is still evidence."]],
            kicker="LO3 · PROJECTS HOLD GOALS, ISSUES AND A LIFETIME BUDGET", accent=AMBER,
            note="Company and agent budgets are MONTHLY. The project budget is a LIFETIME cap "
                 "for an execution-bound project — a different period, not a different ring.")
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

        compare_table("The Three Budget Scopes — Parallel, Not Nested",
            ["Scope", "Period", "Applies to"],
            [["Company budget", "Monthly", "The total ceiling for the entire company."],
             ["Per-agent budget", "Monthly", "One individual agent's ceiling."],
             ["Project budget", "Lifetime",
              "An execution-bound project, for the whole of its life."],
             ["The consequence", "They are independent",
              "An agent can be paused by its OWN budget limit even if the company has "
              "remaining budget."]],
            kicker="LO4 · THE MOST EXPENSIVE MISUNDERSTANDING IN THE COURSE", accent=VIOLET,
            note="Do not picture nested rings where the outer one always binds first. Picture "
                 "three separate trip switches, any one of which can fire.")
        takeaway(tile_grid("Thresholds and Utilisation Colours", [
            ("80% utilisation", "A WARNING is recorded so you can intervene. The agent "
             "CONTINUES running — nothing stops."),
            ("100% utilisation", "The agent is automatically PAUSED. No further heartbeats "
             "fire, and pauseReason is set to budget."),
            ("Green · below 70%", "Read the utilisation bar for company health at a glance."),
            ("Yellow · 70 to 90%", "Look closer. Something is either busier or more expensive "
             "than you planned."),
            ("Red · above 90%", "Intervene now — the hard stop at 100% is close."),
            ("Enforced AT CHECKOUT", "Before the work runs, not when the invoice arrives. "
             "That is what makes unattended operation safe.")],
            kicker="LO4 · A TWO-STAGE CIRCUIT BREAKER", cols=2, size=13, accent=AMBER),
            "A cap you would be unhappy to actually pay is set too high.")
        compare_table("Inference Spend versus Finance Events",
            ["", "Inference spend", "Finance events"],
            [["What it records", "Per-request model cost",
              "Subscriptions, invoices, credits, refunds, adjustments"],
             ["Tracked by", "Provider, model, agent and project",
              "The commercial relationship, not the run"],
             ["Drives the cap", "YES — this is what utilisation measures",
              "No — a credit does not raise an agent's ceiling"],
             ["The mistake", "Reading one and thinking you have seen the other",
              "The Costs page separates them deliberately"]],
            kicker="LO4 · TOKEN-LEVEL COSTING IS WHAT MAKES A CAP MEANINGFUL", accent=BLUE,
            note="Baseline current spend and expected run frequency BEFORE you rely on a cap. "
                 "A ceiling you have not calibrated is a guess with a number on it.")
        tile_grid("The Three Approval Types", [
            ("CEO Strategy", "Raised when the CEO produces a strategic plan after its first "
             "heartbeat. The CEO cannot move tasks to in-progress until you approve it."),
            ("Hire Agent", "Raised when an agent — usually the CEO or a manager — proposes a "
             "subordinate."),
            ("The hire payload", "Name, role, capabilities, adapter configuration, monthly "
             "budget and reporting line. Read every field before approving."),
            ("Budget Override", "Raised when a budget policy hits a hard stop and someone asks "
             "to proceed anyway. This is the one to slow down on."),
            ("Approvals never expire", "An agent waiting on a pending approval pauses "
             "indefinitely. A silent company is very often an unattended queue."),
            ("The board override", "The board may pause any agent and resume any paused agent, "
             "bypassing the approval flow entirely.")],
            kicker="LO4 · WHERE HUMAN AUTHORITY IS MADE EXPLICIT",
            cols=2, size=13, accent=BLUE)
        tile_grid("The Three Approval Responses", [
            ("APPROVE", "The action proceeds. For a hire, the agent is created, configured and "
             "queued to wake automatically."),
            ("REJECT", "The action is denied. The requesting agent is notified and will not "
             "retry unless instructed."),
            ("REQUEST REVISION", "You are not approving as-is, but you are not saying no. The "
             "agent revises and resubmits. This is the one people forget exists."),
            ("The state machine", "pending goes to approved, rejected, or revision_requested — "
             "then resubmitted, and back to pending."),
            ("RECORD THE RATIONALE", "One sentence explaining why is the difference between a "
             "decision and an unaudited event."),
            ("Months later", "The rationale is the only thing that will tell you — or a "
             "regulator — what you were thinking.")],
            kicker="LO4 · THE THIRD RESPONSE IS THE USEFUL ONE",
            cols=2, size=13, accent=TEAL)
        process_map("The Routine Safety Sequence", [
            ("Create it PAUSED", "Never live before it has ever succeeded"),
            ("State the trigger", "Cron expression AND an IANA timezone"),
            ("Name the artifact", "Or the run succeeds but is unverifiable"),
            ("Run once by hand", "Bounded wait; read issue, run and cost"),
            ("Only then unpause", "The schedule now owns reviewed work")],
            kicker="LO4 · AUTOMATION EARNS THE SCHEDULE", color=TEAL,
            synthesis=("WHY THE TIMEZONE IS NOT A FORMALITY",
                       "A cron expression without a timezone runs in whatever zone the host "
                       "happens to be in — fine until the host moves, the clock changes, or "
                       "someone deploys to another region. Write Asia/Singapore explicitly."))
        takeaway(tile_grid("Routine States and Defaults", [
            ("active", "The only status that actually fires. Everything else is dormant."),
            ("paused", "Created here, and it stays here until you have proved it by hand."),
            ("archived", "Retired. Kept for the audit trail, not for execution."),
            ("draft · running · succeeded · failed", "List-view badges, not statuses — do not "
             "confuse a badge with the routine's real state."),
            ("Five-minute granularity", "The routine editor snaps minutes to five-minute "
             "increments. Plan the schedule around that."),
            ("Coalesce if active, skip missed", "The concurrency default: a routine already "
             "running will not start a second copy, and a missed window is skipped.")],
            kicker="LO4 · ONLY ONE STATUS ACTUALLY FIRES", cols=2, size=13, accent=VIOLET),
            "A routine stuck in running with nothing happening usually means a lost process.")
        compare_table("The Intervention Ladder — Least Irreversible First",
            ["Rung", "Action", "Reversible?", "Use when"],
            [["1", "INSPECT — read task, run, cost and activity evidence",
              "Yes — nothing changes", "Always. Never act before you have looked."],
             ["2", "PAUSE — stop new heartbeats, keep all state", "Yes",
              "The agent is doing something wrong and must stop now."],
             ["3", "REASSIGN — move the work to another role", "Yes",
              "The work is valid but this agent is the wrong owner."],
             ["4", "TERMINATE — retire the agent", "NO",
              "The role should not exist at all. Last resort only."]],
            kicker="LO4 · ESCALATE ONLY WHEN THE RUNG BELOW HAS FAILED", accent=AMBER,
            note="Practise Terminate only on a role you deliberately created as disposable — "
                 "never as a first response to a misbehaving production agent.")
        compare_table("RBAC — Company Roles and Their Grants",
            ["Role", "Description", "Implicit grants"],
            [["Owner", "The people who run the company",
              "All eight — agents, skills, environments, users, tasks and joins"],
             ["Admin", "Trusted operators who onboard people and agents",
              "As Owner, MINUS users:manage_permissions"],
             ["Operator", "Hands-on members who help run the work", "tasks:assign"],
             ["Viewer", "Read-only observers", "None"],
             ["Unset", "No implicit grants at all",
              "Hand-picked explicit grants only — the tightest configuration available"]],
            kicker="LO4 · FOUR ROLES, AN UNSET STATE, 21 PERMISSION KEYS", accent=BLUE,
            note="Owner's eight: agents:create, agents:configure, skills:create, "
                 "environments:manage, users:invite, users:manage_permissions, tasks:assign, "
                 "joins:approve. An explicit grant PERSISTS across a role change, and there is "
                 "NO DENY LAYER — you cannot subtract a permission.")
        compare_table("Deployment Modes — Exposure Is a Decision",
            ["Mode", "Login", "Use it when"],
            [["local_trusted (the default)", "No login required",
              "A single operator on their own machine. This is the mode used throughout this "
              "course."],
             ["authenticated + private", "Login required, not publicly reachable",
              "A small team on a trusted network or a private mesh."],
             ["authenticated + public", "Login required, publicly reachable",
              "A hosted deployment. Requires the most care: real auth, real secrets, real "
              "exposure."]],
            kicker="LO4 · THREE MODES, THREE LEVELS OF EXPOSURE", accent=TEAL,
            note="Set with configure --section server, or the PAPERCLIP_DEPLOYMENT_MODE "
                 "environment variable. You inherit the default only if you never decide.")
        tile_grid("Environment Variables You Cannot Skip", [
            ("PAPERCLIP_AGENT_JWT_SECRET", "Signs agent tokens. REQUIRED — and it doubles as "
             "the fallback for the auth secret."),
            ("DATABASE_URL", "The PostgreSQL connection string. REQUIRED."),
            ("TOOL_ACTION_SIGNING_SECRET", "The PAPERCLIP_ prefixed variable that signs "
             "tool-action approvals. Documented as required, with NO fallback."),
            ("PAPERCLIP_ALLOWED_HOSTNAMES", "The hostnames the server will answer for. Add "
             "your custom domain here."),
            ("PAPERCLIP_TELEMETRY_DISABLED", "Set to 1 to disable telemetry. DO_NOT_TRACK "
             "works the same way."),
            ("Roughly seventy in total", "Across nine categories. You do not need to memorise "
             "them — you do need to know which are required.")],
            kicker="LO4 · TWO ARE MARKED REQUIRED; A THIRD HAS NO FALLBACK",
            cols=2, size=13, accent=AMBER)
        takeaway(tile_grid("The Mission-to-Evidence Audit Map", [
            ("Mission claim", "One row per claim the company makes about what it achieved."),
            ("Issue", "Which unit of work was supposed to produce it, and under which lineage."),
            ("Run", "Which execution actually ran, and whether it errored."),
            ("Artifact", "The file on disk, at a named path, with the fields you specified."),
            ("Cost", "What it spent — and whether that is plausible for the work claimed."),
            ("Approval", "The human decision, with its recorded rationale.")],
            kicker="LO4 · CONCRETELY, WHAT AN AUDITOR WOULD ASK YOU FOR",
            cols=2, size=13, accent=BLUE),
            "The loop closes when the whole operation reconstructs from the log alone.")
        compare_table("Reading the Activity Log for Gaps",
            ["What you see", "What it usually means", "What to do"],
            [["A steady, ordered sequence of runs", "The audit loop is closed",
              "Nothing. This is the state you are working towards."],
             ["A workspace change with no run",
              "Work was done OUTSIDE a run — typically hand-edited",
              "Record it honestly. The gap is itself an audit finding."],
             ["Long silence, no runs and no spend", "An unattended approval queue",
              "Open Approvals first. Approvals never expire on their own."],
             ["An agent stopped mid-work", "The budget hard stop at 100%",
              "Check utilisation and pauseReason. Raise the cap deliberately, or let it stop."]],
            kicker="LO4 · ACTIVITY IS WHAT MAKES EVERYTHING ELSE DEFENSIBLE", accent=VIOLET,
            note="Concealing a gap is far worse than having one. An honest note explaining a "
                 "hand-edit costs you nothing; a silent gap costs you the whole audit.")
        takeaway(tile_grid("Cost Engineering Levers", [
            ("Turn the interval OFF", "It is off by default. An interval wakes the agent "
             "whether or not there is work, and each wake costs money."),
            ("Split the instruction files", "Only HEARTBEAT.md is needed on every wake. Move "
             "occasional material out of the per-run path."),
            ("Use skills, not bigger prompts", "Ten skills does not mean ten skills loaded per "
             "heartbeat — the agent loads only what it decides is relevant."),
            ("Cap at the agent, not just the company", "The scopes are parallel, so the agent "
             "cap is what stops one runaway role."),
            ("Read the adapter defaults", "300 turns per run and a four-hour sandbox timeout "
             "are large numbers to leave unexamined."),
            ("Keep lineage intact", "Re-explaining the goal in every issue body means paying "
             "for the same context over and over.")],
            kicker="LO4 · WHERE THE MONEY ACTUALLY GOES", cols=2, size=13, accent=TEAL),
            "Every lever here reduces tokens per run — which is the only cost that compounds.")
        takeaway(tile_grid("Portability — A Company Is Data, Not a Craft Object", [
            ("Export the whole company", "Org chart, projects, issues, routines and "
             "configuration move together as one unit."),
            ("Secrets are scrubbed", "Credentials do not travel in the export. They are "
             "re-provisioned at the destination."),
            ("Collisions are re-mapped", "Identifier clashes at the destination are resolved "
             "on import rather than failing the whole load."),
            ("Back up before a risky change", "The cheapest insurance available before you "
             "restructure an org chart."),
            ("Clone a proven structure", "A second business line starts from a shape you have "
             "already debugged."),
            ("Laptop to hosted", "This is how a course company becomes a production one — and "
             "how you hand it to a colleague.")],
            kicker="LO4 · MOVING A WHOLE COMPANY", cols=2, size=13, accent=VIOLET),
            "If you are afraid to touch a configuration, it is not portable — it is a liability.")


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
