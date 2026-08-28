#!/usr/bin/env python3
"""Generate the CompTIA PenTest+ (PT0-003) Lesson Plan (LP) DOCX in the Tertiary house format.

Cover page + Document Version Control Record + auto TOC + Arial 11pt body +
colour-coded 3-day schedule tables (9:00am-6:00pm, 8 training hours/day, 1h
lunch, tea within, final assessment Day 3 4:00pm). Topics/labs come from
course_data + the domain data files so the LP stays aligned with the deck,
guide and labs.
"""
import os, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
import importlib
ACT = []
for _i in range(1, 13):
    try:
        _m = importlib.import_module(f"data_domain{_i}")
    except ModuleNotFoundError:
        continue
    ACT += getattr(_m, f"DOMAIN{_i}", [])
import prodoc
def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE); ASSETS=os.path.join(os.path.dirname(HERE),"assets")

BRAND=RGBColor(0x1F,0x6F,0xEB); DARK=RGBColor(0x11,0x18,0x27); GREY=RGBColor(0x55,0x5B,0x66)
HEADER_FILL="1F6FEB"; TOPIC_FILL="E8F0FE"; BREAK_FILL="FFF4E5"; LUNCH_FILL="FDE9D9"; ASSESS_FILL="E8F7EE"

def lab_titles(nums):
    return "; ".join(f"Lab {a['num']}: {a['title']}" for a in ACT if a['num'] in nums)

# ------------------------------------------------ schedule (single source of truth for timing)
# (start, end, minutes, kind, activity_text)  kind: admin/topic/lab/break/lunch/assess/recap
SCHEDULE = {
 1: (C.DAY_THEMES[1], [
    ("9:00","9:30",30,"admin","Welcome, course introduction, ground rules, learning outcomes and mandatory SSG digital attendance (AM)"),
    ("9:30","11:00",90,"topic","Topic 1 — Fundamentals of Agentic AI and Paperclip: what makes a system agentic; Paperclip as an organisational control plane; the four pillars and twelve subsystems; the heartbeat execution model; feasibility — when a multi-agent company earns its coordination cost (concepts + demo)"),
    ("11:00","11:15",15,"break","Tea break"),
    ("11:15","13:00",105,"lab","Topic 1 continued: control-plane vs runtime boundary and the diagnosis ladder. Hands-on: "+lab_titles([1])),
    ("13:00","14:00",60,"lunch","Lunch break · mandatory SSG digital attendance (PM)"),
    ("14:00","15:30",90,"topic","Topic 2 — Building AI Agents with Paperclip: onboarding and bind modes; a measurable mission; the CEO and the org chart; role instructions as contracts; workspaces, secrets and skills; adapter readiness (concepts + demo)"),
    ("15:30","15:45",15,"break","Tea break"),
    ("15:45","17:45",120,"lab","Hands-on: "+lab_titles([2,3])),
    ("17:45","18:00",15,"recap","Day 1 recap, Q&A and PM digital attendance"),
 ]),
 2: (C.DAY_THEMES[2], [
    ("9:00","9:15",15,"recap","Day 1 recap and mandatory SSG digital attendance (AM)"),
    ("9:15","10:30",75,"topic","Topic 3 — Developing Intelligent Multi-Agent Systems: projects, goals and lineage; parent/child issue decomposition; assignment as the trigger; acceptance criteria that name evidence; verifying hand-offs between disparate components (concepts + demo)"),
    ("10:30","10:45",15,"break","Tea break"),
    ("10:45","12:30",105,"lab","Hands-on: "+lab_titles([4,5])),
    ("12:30","13:30",60,"lunch","Lunch break · mandatory SSG digital attendance (PM)"),
    ("13:30","14:30",60,"topic","Topic 4 — Deploying and Managing AI Agents: routines and explicit schedule triggers; layered budgets enforced at checkout; approvals and the activity log; the operator intervention ladder; deployment, portability and troubleshooting (concepts + demo)"),
    ("14:30","14:45",15,"break","Tea break"),
    ("14:45","15:15",30,"lab","Hands-on: "+lab_titles([6])),
    ("15:15","15:45",30,"recap","Course recap, TRAQOM survey and assessment preparation"),
    ("15:45","16:00",15,"brief","Briefing for Assessment · mandatory SSG digital attendance (Assessment)"),
    ("16:00","17:00",60,"assess","Written Assessment (WA) — Short-Answer Questions (SAQ), 5 questions, 1 hour, open book"),
    ("17:00","18:00",60,"assess","Practical Performance (PP) — 4 hands-on Paperclip tasks, 1 hour, open book"),
 ]),
}

# ------------------------------------------------ build document
doc=Document()
normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
prodoc.style_headings(doc)

prodoc.add_cover_page(doc,"LESSON PLAN",C.TITLE,C.VERSION.lstrip("v"),
                      org_logo=os.path.join(ASSETS,"tertiary-infotech-logo.png"),
                      course_logo=os.path.join(ASSETS,"paperclip-course-logo.png"),
                      course_code=C.COURSE_CODE)
prodoc.add_version_control(doc,[
 (C.VERSION.lstrip("v"),C.VERSION_DATE,
  "Initial release — 2-day lesson plan for Manage AI Agents with Paperclip (TGS-2023036646), "
  "aligned to the four topics and the six hands-on labs (one simulated one-person company per lab).",
  C.TRAINER),
])
prodoc.add_toc(doc)

def H(text,level=1):
    h=doc.add_heading(text,level=level); return h

H("Course Information",1)
info=[("Course Title",C.TITLE),("WSQ Course Reference",C.COURSE_CODE),
      ("Training Provider",C.ORG+"  ("+C.UEN.replace('UEN: ','UEN ')+")"),
      ("Duration",f"{C.DAYS} days · {C.TRAINING_HOURS} training hours + {C.ASSESSMENT_HOURS} assessment hours ({C.TRAINING_HOURS+C.ASSESSMENT_HOURS} hours total)"),
      ("Daily Timing","9:00 am – 6:00 pm (1-hour lunch; tea breaks within training time)"),
      ("Mode","Instructor-led (physical), hands-on Paperclip labs building six simulated one-person AI agent companies on synthetic data"),
      ("TSC",f"{C.TSC_TITLE} · {C.TSC_CODE}"),
      ("Trainer",C.TRAINER)]
t=doc.add_table(rows=0,cols=2); t.style="Table Grid"
for k,v in info:
    c=t.add_row().cells; c[0].text=""; r=c[0].paragraphs[0].add_run(k); r.bold=True; r.font.size=Pt(10)
    prodoc._shade_cell(c[0],TOPIC_FILL)
    c[1].text=""; c[1].paragraphs[0].add_run(v).font.size=Pt(10)

H("Learning Outcomes",1)
doc.add_paragraph("On completion of this course, learners will be able to:")
for lo in C.LEARNING_OUTCOMES:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(lo).font.size=Pt(10.5)

H("Assessment",1)
for a in [C.ASSESSMENT["written"],C.ASSESSMENT["practical"],
          "Format: Open Book — course slides, Learner Guide and approved materials only.",
          "Final assessment is conducted on Day 2 after the Briefing for Assessment.",C.ASSESSMENT["note"]]:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(a).font.size=Pt(10.5)

def set_cell(cell,text,bold=False,size=9.5,color=None,fill=None,align=None):
    cell.text=""; p=cell.paragraphs[0]
    if align: p.alignment=align
    r=p.add_run(text); r.bold=bold; r.font.size=Pt(size); r.font.name="Arial"
    if color: r.font.color.rgb=color
    if fill: prodoc._shade_cell(cell,fill)

KIND_FILL={"topic":TOPIC_FILL,"break":BREAK_FILL,"lunch":LUNCH_FILL,"assess":ASSESS_FILL,"brief":ASSESS_FILL,
           "admin":"F3F5F8","recap":"F3F5F8","lab":None}

H("Course Schedule",1)
DAY_INSTR={}; DAY_ASSESS={}
for day,(theme,rows) in SCHEDULE.items():
    H(f"Day {day} — {theme}",2)
    tbl=doc.add_table(rows=0,cols=3); tbl.style="Table Grid"; tbl.alignment=WD_TABLE_ALIGNMENT.CENTER
    hdr=tbl.add_row().cells
    for i,htext in enumerate(["Time","Duration","Topic / Activity"]):
        set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
    training=0
    for start,end,mins,kind,text in rows:
        cells=tbl.add_row().cells; fill=KIND_FILL.get(kind)
        set_cell(cells[0],f"{start}–{end}",bold=(kind in ("topic","assess","brief")),size=9.5,fill=fill)
        set_cell(cells[1],f"{mins} min",size=9.5,fill=fill)
        set_cell(cells[2],text,bold=(kind in ("topic","assess","brief")),size=9.5,fill=fill)
        if kind!="lunch": training+=mins
    # widths
    for row in tbl.rows:
        row.cells[0].width=Inches(1.15); row.cells[1].width=Inches(0.9); row.cells[2].width=Inches(4.75)
    assess_mins=sum(m for _s,_e,m,k,_t in rows if k=="assess")
    instr=training-assess_mins
    p=doc.add_paragraph()
    _lbl=(f"Total instructional time: {instr} minutes ({instr//60} hours)"
          + (f"  ·  assessment: {assess_mins} minutes ({assess_mins//60} hours)." if assess_mins else "."))
    r=p.add_run(_lbl); r.italic=True; r.font.size=Pt(9.5); r.font.color.rgb=GREY
    DAY_INSTR[day]=instr; DAY_ASSESS[day]=assess_mins

_tot_instr=sum(DAY_INSTR.values()); _tot_assess=sum(DAY_ASSESS.values())
assert _tot_instr==C.TRAINING_HOURS*60, (
    f"instructional minutes {_tot_instr} != registered {C.TRAINING_HOURS*60}")
assert _tot_assess==C.ASSESSMENT_HOURS*60, (
    f"assessment minutes {_tot_assess} != registered {C.ASSESSMENT_HOURS*60}")

H("Lab Reference (aligned to the four topics)",1)
tt=doc.add_table(rows=0,cols=3); tt.style="Table Grid"
hdr=tt.add_row().cells
for i,htext in enumerate(["Topic","Weighting","Labs"]):
    set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
for tp in C.TOPICS:
    acts=[a for a in ACT if a["topic"]==tp["num"]]
    cells=tt.add_row().cells
    set_cell(cells[0],f"Topic {tp['code']}: {tp['title']}",bold=True,size=9.5,fill=TOPIC_FILL)
    set_cell(cells[1],tp["weighting"],size=9.5,fill=TOPIC_FILL)
    set_cell(cells[2],", ".join(f"Lab {a['num']}" for a in acts),size=9.5)

prodoc.add_page_numbers(doc)
prodoc.enable_update_fields(doc)
OUT=os.path.join(REPO,"courseware",f"LP-{C.SHORT_TITLE}.docx")
doc.save(OUT)
print("Saved",OUT)
