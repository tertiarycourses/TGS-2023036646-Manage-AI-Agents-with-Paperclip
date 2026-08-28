#!/usr/bin/env python3
"""Generate the CompTIA PenTest+ (PT0-003) Learner Guide as BOTH a Markdown mirror (LG-*.md at repo
root) and a DOCX (courseware/LG-*.docx) from one source, so they never diverge.

House format: cover page, Document Version Control Record, auto TOC, Arial 11pt
body, one section per lab (Objective · Goal · What you'll build · Step-by-step
with commands · Test it), plus setup, exam-prep and glossary. All content is
driven by course_data + the domain data files, keeping the LG 100% aligned with
the slide deck, Lesson Plan and labs.
"""
import os, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

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

# ---------------- block DSL (single content stream → MD + DOCX) ----------------
B=[]
def h1(t): B.append(("h1",t))
def h2(t): B.append(("h2",t))
def h3(t): B.append(("h3",t))
def p(t):  B.append(("p",t))
def bullets(xs): B.append(("bullets",xs))
def steps(xs): B.append(("steps",xs))
def code(t): B.append(("code",t))
def note(t): B.append(("note",t))
def rule(): B.append(("rule",))

# ---------------- content ----------------
h1("Introduction")
p(f"This Learner Guide accompanies the WSQ course {C.TITLE}, conducted by {C.ORG}. "
  "It gives the full step-by-step procedure for all six hands-on labs, organised by the four course "
  "topics. Each lab builds a DIFFERENT simulated one-person AI agent company — short-video "
  "production, digital marketing, finance, accounting, stock-trading research and HR people "
  "operations — so you see the same control model applied across six very different businesses.")
p("Paperclip is an organisational control plane for AI agents: an open-source Node.js server with a "
  "React UI that gives a team of agents an org chart, issues, budgets, approval gates and a durable "
  "audit trail. It does not replace your agent runtime. The runtimes — Claude Code, Codex, Cursor, "
  "Gemini CLI, a bash process or an HTTP bot — still do the reasoning and the tool use; Paperclip "
  "schedules, budgets and audits them. Keeping that boundary clear is the single most useful idea "
  "in this course.")
p("Use this guide alongside the course slides and the lab folders in labs/ of the course repository. "
  "Every data set in this course is SYNTHETIC and fabricated for training. Never load real company, "
  "market, financial or candidate data into a practice instance, and never place a real credential "
  "in a prompt, a lab note or Git.")

h1("Course Learning Outcomes")
bullets(C.LEARNING_OUTCOMES)

h1("Before You Start — Environment Setup")
h3("What you need")
bullets([
 "Node.js 20 or later, and npm/npx. Paperclip will not onboard on an older runtime — check with `node --version` first.",
 "A NORMAL, non-elevated shell. Close any Administrator or root terminal before you begin: the embedded PostgreSQL refuses to start under an elevated user.",
 "One trainer-approved agent runtime (for example Claude Code, Codex or Gemini CLI), already installed AND authenticated OUTSIDE Paperclip.",
 "Git, used to baseline each agent workspace so that every later change is a readable, attributable diff.",
 "Permission to create a local practice folder and to download the Paperclip npm package.",
 "The course lab repository, cloned from the link on your LMS course page.",
])
h3("Install and verify Paperclip")
p("Onboarding downloads Paperclip, writes the local configuration, initialises the embedded "
  "PostgreSQL database, starts the server on port 3100 and normally opens your browser. Run it from "
  "a normal user shell — never with sudo. Then prove the control plane is healthy BEFORE you create "
  "any company: the diagnostic and the health endpoint together are your clean baseline, and every "
  "later adapter or budget failure is far easier to isolate because you recorded one.")
code("node --version                 # must report v20 or later\n"
     "npm --version\n"
     "npx --registry https://registry.npmjs.org paperclipai onboard --yes\n"
     "npx paperclipai doctor         # fix the EARLIEST error first\n"
     "curl -sS http://localhost:3100/api/health   # expect status ok")
h3("Conventions used in every lab")
bullets([
 "Commands are run from a normal user terminal in the lab's practice root. A leading sudo is never required.",
 "Each lab uses its own simulated company and its own synthetic data set, supplied in that lab's data/ folder.",
 "Each agent gets a DEDICATED workspace folder; artifacts must land in the right one, and a marker in the wrong root is a boundary failure.",
 "Every issue is created UNASSIGNED — assignment is the trigger that wakes an agent.",
 "Bound every wait (about 10 minutes). An unbounded wait hides a failed adapter behind apparent patience.",
 "Record evidence as you go in evidence/lab0N-*.md, and never copy a key, token, cookie or connection string into it.",
])

# ---------------- per-topic, per-lab ----------------
TOPICS_BY_NUM={t["num"]:t for t in C.TOPICS}
for t in C.TOPICS:
    h1(f"Topic {t['code']} — {t['title']}  ({t['weighting']})")
    p(t["subtitle"])
    h3("Key concepts")
    bullets(t["concepts"])
    for a in [x for x in ACT if x["topic"]==t["num"]]:
        h2(f"Lab {a['num']} — {a['title']}")
        p("Maps to: " + a["objective"].rstrip(".") + ".")
        p(f"Simulated company: {a.get('company','')}.")
        p(f"Goal: {a['desc']}")
        h3("What you'll build")
        p(a["build"]+f"   (Tools: {a['services']}.)")
        h3("Step-by-step")
        st=[]
        for i,(instr,cmd) in enumerate(a["steps"],1):
            st.append((instr,cmd))
        steps(st)
        h3("Test it")
        p(a["test"])
        note(f"The lab folder labs/lab-{a['num']:02d}-* holds this lab's README and its synthetic "
             f"data set. All data is fabricated for training — never substitute real company, "
             f"market, financial or candidate data, and never record a credential in your evidence.")
        rule()

h1("Operating Reference — Beyond the Labs")
p("These cross-cutting topics are assessed throughout the course but do not each have a dedicated "
  "lab. Read this section alongside the labs so you can answer the knowledge questions and run a "
  "real Paperclip company safely afterwards.")
h3("Choosing the deployment mode")
bullets([
 "Loopback (the default) — trusted local only, the least exposed and the right choice for this course.",
 "`--bind lan` — reachable from your network; authentication becomes mandatory, not optional.",
 "`--bind tailnet` — reachable over a private mesh; again authentication is required.",
 "Hosted / container — an external PostgreSQL, a persistent volume for instance config and credentials, PAPERCLIP_TOOL_ACTION_SIGNING_SECRET for tool approvals, and an allowed-hostnames list.",
 "/api/health is the readiness probe at every one of these levels.",
])
h3("Budget layering in practice")
bullets([
 "Set the COMPANY cap before you hire anyone; set the AGENT cap below it; add a PROJECT cap where one project must not consume the company.",
 "Caps are enforced at CHECKOUT, not at billing — that is what makes unattended operation safe.",
 "Record a baseline (current spend, expected run frequency) before you rely on a cap.",
 "Treat it as a two-stage circuit breaker: warn, then stop. A cap you would be unhappy to actually pay is set too high.",
 "Cost is tracked per token by provider, model, agent and project — read the actual figure before adjusting any cap.",
])
h3("Routines and schedule safety")
bullets([
 "Create every routine PAUSED. A routine that is live before it has ever succeeded is unreviewed scheduled spend.",
 "State the trigger explicitly — a cron expression AND an IANA timezone (e.g. `30 16 * * *`, Asia/Singapore). An implicit timezone is a production incident waiting to happen.",
 "Prove it with exactly one bounded manual run, reviewed by a human, then leave it paused until you have read the generated issue, the run and the cost.",
 "Name the artifact the routine must produce, or the run is successful but unverifiable.",
])
h3("Governance, approvals and intervention")
bullets([
 "Approvals make human authority explicit: the agent proposes, the action HOLDS, a human decides with a recorded rationale. A close without a rationale is an unaudited decision.",
 "The activity log is durable — mutations, heartbeats, cost events and approvals. The audit loop closes when the whole operation reconstructs from the log alone.",
 "Use the least irreversible control first: inspect → pause → reassign → terminate. Terminate is the last rung and is not reversible.",
 "An unexplained gap in the activity log usually means work was done outside a run. Record it honestly — the gap is itself an audit finding.",
])
h3("Working safely with synthetic data")
bullets([
 "All six company data sets in this course are fabricated. The NorthPoint market data is not market data and must never inform a real trading decision.",
 "The TalentBridge candidate file deliberately records NO protected characteristics — no age, gender, race, religion, marital status or nationality. Keep it that way in any real hiring workflow.",
 "Keep credentials in the runtime or the Paperclip secret store with scoped injection at heartbeat time — never in prompts, notes or Git.",
])
rule()

h1("Course Preparation and Practice")
bullets([
 "First pass: complete every lab in order, reading each lab folder's README and its data/ set.",
 "Second pass: rebuild one company from scratch without the guide, until the control sequence — cap, hire, confine, assign, verify, audit — is automatic.",
 "Review the 'Test it' criterion for any lab you found hard; it states exactly what the assessor will look for.",
 "Practise writing acceptance criteria that name an artifact, its path and its required fields — this is the skill most learners under-practise.",
 "Sharpen your readiness with the Tertiary Infotech practice exam: https://exams.tertiaryinfotech.com",
 "Then apply it: pick ONE real internal workflow whose inputs and outputs are already observable, cap it low, and audit it before you scale.",
])

h1("Glossary")
gl=[
 ("Control plane","The layer that coordinates agents, goals, work, cost and governance. Paperclip is a control plane; it does not perform the reasoning itself."),
 ("Adapter / runtime","The agent that actually reasons and uses tools — Claude Code, Codex, Cursor, Gemini CLI, a bash process or an HTTP bot. 'If it can receive a heartbeat, it's hired.'"),
 ("Company","The boundary for one mission, its human members, AI employees, projects, issues, budget and activity history. One deployment holds many companies."),
 ("Mission","The measurable outcome that defines why a company exists — it needs a target, a metric and a boundary, or it cannot be verified."),
 ("CEO","The first hire and top of the org chart; owns goal alignment, decomposition and final synthesis, and may hire further agents under approval."),
 ("Org chart","The explicit reporting structure — who reports to whom, with what authority, budget and workspace."),
 ("Agent","A work-performing role defined by six fields: role, manager, adapter, instructions, heartbeat and budget."),
 ("Role instruction","A contract stating purpose, allowed inputs, output schema, exclusions and escalation path — not a personality."),
 ("Workspace","A dedicated local root for one role's files and evidence, isolated with git worktrees so every change is attributable."),
 ("Heartbeat","A bounded execution burst triggered by a timer, an assignment, an on-demand wake or a routine. Between heartbeats the agent is dormant."),
 ("Atomic checkout","The execution lock that stops two heartbeats double-working the same issue or racing past a budget ceiling."),
 ("Issue","A unit of work carrying full goal ancestry, so the agent sees why it exists and not only what to do."),
 ("Goal lineage","The chain company mission → project goal → parent issue → child issue that gives an agent its direction."),
 ("Acceptance criterion","A statement naming the required evidence — the artifact, its path and its fields. Never 'the work is done'."),
 ("Hand-off","Passing an artifact between agents. It is accepted only when the receiver can consume it without asking the producer a question."),
 ("Run","One agent execution instance, with a structured log, a cost entry and an observable result."),
 ("Routine","Recurring work triggered by cron, webhook or API. Create it paused, prove it once by hand, then let the schedule own it."),
 ("Budget layering","Company, project and agent caps. The innermost cap that binds fires first, and enforcement happens at checkout."),
 ("Approval","A governance gate: the agent proposes a hire, strategy or risky action; the action holds; a human decides with a recorded rationale."),
 ("Activity log","The durable record of mutations, heartbeats, cost events and approvals — the basis of the audit loop."),
 ("Intervention ladder","Inspect → pause → reassign → terminate. Always use the least irreversible control that resolves the situation."),
 ("Skill","A reusable agent capability imported into an org-wide library and attached to specific agents — capability without retraining."),
 ("Portability","Export/import of a whole company with secrets scrubbed and identifier collisions re-mapped."),
]
B.append(("dl",gl))

# ---------------- render Markdown ----------------
def _anchor(txt):
    return "".join(ch.lower() if ch.isalnum() else ("-" if ch in " -" else "") for ch in txt)

def render_md():
    out=[f"# {C.TITLE} — Learner Guide",""]
    out.append(f"**WSQ Course Code:** {C.COURSE_CODE}  |  **Conducted by:** {C.ORG} ({C.UEN.replace('UEN: ','UEN ')})  |  **Version {C.VERSION} · {C.VERSION_DATE}**")
    out.append("")
    # TOC (h1 + h2)
    out.append("## Contents"); out.append("")
    for kind,*rest in B:
        if kind=="h1": out.append(f"- [{rest[0]}](#{_anchor(rest[0])})")
        elif kind=="h2": out.append(f"  - [{rest[0]}](#{_anchor(rest[0])})")
    out.append("")
    for kind,*rest in B:
        if kind=="h1": out+=["",f"## {rest[0]}",""]
        elif kind=="h2": out+=["",f"### {rest[0]}",""]
        elif kind=="h3": out+=[f"**{rest[0]}**",""]
        elif kind=="p": out+=[rest[0],""]
        elif kind=="bullets": out+=[f"- {x}" for x in rest[0]]+[""]
        elif kind=="steps":
            for i,(instr,cmd) in enumerate(rest[0],1):
                out.append(f"{i}. {instr}")
                if cmd: out+=["",f"   ```bash",f"   {cmd}","   ```",""]
            out.append("")
        elif kind=="code": out+=["```bash",rest[0],"```",""]
        elif kind=="note": out+=[f"> **Note:** {rest[0]}",""]
        elif kind=="rule": out+=["---",""]
        elif kind=="dl":
            for term,defn in rest[0]: out.append(f"- **{term}** — {defn}")
            out.append("")
    return "\n".join(out)

MD_OUT=os.path.join(REPO,f"LG-{C.SHORT_TITLE}.md")
with open(MD_OUT,"w") as f: f.write(render_md())
print("Saved",MD_OUT)

# ---------------- render DOCX ----------------
BRAND=RGBColor(0x1F,0x6F,0xEB); DARK=RGBColor(0x11,0x18,0x27); GREY=RGBColor(0x55,0x5B,0x66)
INKCODE=RGBColor(0x0B,0x30,0x60)
doc=Document()
normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
prodoc.style_headings(doc)
prodoc.add_cover_page(doc,"LEARNER GUIDE",C.TITLE,C.VERSION.lstrip("v"),
                      org_logo=os.path.join(ASSETS,"tertiary-infotech-logo.png"),
                      course_logo=os.path.join(ASSETS,"paperclip-course-logo.png"),
                      course_code=C.COURSE_CODE)
prodoc.add_version_control(doc,[
 (C.VERSION.lstrip("v"),C.VERSION_DATE,
  "Initial release — Learner Guide for Manage AI Agents with Paperclip (TGS-2023036646): four topics, "
  "six hands-on labs, each building a different simulated one-person AI agent company on synthetic data.",
  C.TRAINER),
])
prodoc.add_toc(doc)

def code_para(text):
    for line in text.split("\n"):
        para=doc.add_paragraph(); prodoc._shade_para(para) if hasattr(prodoc,"_shade_para") else None
        r=para.add_run(line); r.font.name="Consolas"; r.font.size=Pt(8.5); r.font.color.rgb=INKCODE
        para.paragraph_format.space_after=Pt(0)


def _rich(para, text, size=11, color=None):
    """Write text into a paragraph, turning `backtick` spans into real monospace runs.
    Literal backticks were rendering as characters in the DOCX."""
    import re as _re
    for i, seg in enumerate(_re.split(r"`([^`]+)`", str(text))):
        if not seg:
            continue
        r = para.add_run(seg)
        r.font.size = Pt(size)
        if i % 2:                      # odd segments were inside backticks
            r.font.name = "Consolas"
            r.font.size = Pt(size - 1)
            r.font.color.rgb = INKCODE
        elif color is not None:
            r.font.color.rgb = color

for kind,*rest in B:
    if kind=="h1": doc.add_heading(rest[0],level=1)
    elif kind=="h2": doc.add_heading(rest[0],level=2)
    elif kind=="h3":
        para=doc.add_paragraph(); r=para.add_run(rest[0]); r.bold=True; r.font.size=Pt(11); r.font.color.rgb=BRAND
    elif kind=="p": _rich(doc.add_paragraph(), rest[0])
    elif kind=="bullets":
        for x in rest[0]: _rich(doc.add_paragraph(style="List Bullet"), x)
    elif kind=="steps":
        # Explicit numbering restarts at 1 for EVERY lab. Word's List Number style
        # continues across the whole document, which made Lab 2 start at step 10.
        for i,(instr,cmd) in enumerate(rest[0],1):
            para=doc.add_paragraph()
            para.paragraph_format.left_indent=Inches(0.32)
            para.paragraph_format.first_line_indent=Inches(-0.32)
            para.paragraph_format.space_after=Pt(4)
            r=para.add_run(f"{i}.  "); r.bold=True; r.font.color.rgb=BRAND
            _rich(para, instr)
            if cmd: code_para(cmd)
    elif kind=="code": code_para(rest[0])
    elif kind=="note":
        para=doc.add_paragraph(); r=para.add_run("Note: "); r.bold=True; r.font.color.rgb=BRAND
        _rich(para, rest[0], size=10)
    elif kind=="rule": doc.add_paragraph("")
    elif kind=="dl":
        for term,defn in rest[0]:
            para=doc.add_paragraph(style="List Bullet")
            r=para.add_run(term+" — "); r.bold=True; _rich(para, defn)

prodoc.add_page_numbers(doc)
prodoc.enable_update_fields(doc)
DOCX_OUT=os.path.join(REPO,"courseware",f"LG-{C.SHORT_TITLE}.docx")
doc.save(DOCX_OUT)
print("Saved",DOCX_OUT)
