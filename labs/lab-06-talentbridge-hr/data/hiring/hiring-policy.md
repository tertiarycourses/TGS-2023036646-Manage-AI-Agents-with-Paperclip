# Fair Hiring Policy (TalentBridge People Ops)

> **SYNTHETIC TRAINING DATA.** TalentBridge People Ops is a fictional company invented for the WSQ
> course *Manage AI Agents with Paperclip* (TGS-2023036646). This policy is a training artifact.
> It is written in the spirit of the Singapore Tripartite Guidelines on Fair Employment Practices
> but it is **not** legal advice and must not be used as a real workplace policy.

**Version:** v1.0 · 28 August 2026
**Applies to:** every human and every AI agent participating in a TalentBridge hiring process

---

## 1. Purpose

TalentBridge's mission is:

> Fill each open role within 30 days with a fair, documented and auditable process from sourcing
> through to day-one onboarding.

Note the order of the adjectives. **Fair** comes before **fast**. A role filled in 20 days through
an undocumented process has failed this mission, not exceeded it.

This policy exists because agents now perform part of the process. An agent will do exactly what
its instructions permit, at speed and at volume — which makes an unstated fairness rule far more
dangerous here than it would be with a human reviewer who might pause and ask.

## 2. Principles

1. **Merit only.** Candidates are assessed on skills, experience and demonstrated ability relevant
   to the role — nothing else.
2. **One published rubric.** Every candidate for a role is assessed against the same published
   rubric, `interview-rubric.md`, using the same scale.
3. **Traceable reasons.** Every decision records a reason that traces to a rubric criterion.
4. **Documented decisions.** Shortlisting, progression and rejection are all recorded with the
   evidence they rest on.
5. **Human accountability.** An agent may analyse, score and recommend. A human decides, and the
   rationale is recorded in the approval.
6. **Data minimisation.** The process collects only what the rubric needs. What is never collected
   cannot be misused.

## 3. Prohibited grounds

No decision, score, shortlist, comment, ranking or brief may rely on, or infer:

- Age or date of birth
- Gender or gender identity
- Race, ethnicity, colour or national origin
- Religion or religious practice
- Marital or family status, pregnancy, or caregiving responsibilities
- Nationality or citizenship — with the single lawful exception of confirming legal entitlement to
  work in Singapore, which is a yes/no eligibility check made once, recorded once, and never used
  as a scoring criterion
- Disability or health status, except to arrange a reasonable accommodation at the candidate's
  own request

**Inference is prohibited, not merely collection.** Deducing a protected characteristic from a
name, a photograph, a graduation year, a career gap or a school is the same breach as asking for
it directly. A career break is not a scoring input.

## 4. Rules for AI agents

An agent operating in a TalentBridge hiring process must:

| Rule | Meaning in practice |
|---|---|
| Use only supplied data | `candidates.csv`, `interview-rubric.md` and this policy. Nothing else. |
| Never enrich a candidate record | No searching for, guessing at or reconstructing any additional detail about a person. |
| Never request a protected characteristic | If a task appears to need one, stop and escalate. It is a defective task. |
| Cite the rubric | Every reason names the criterion it comes from. |
| State limitations | What the data could not establish is part of the deliverable. |
| Never decide | Produce a recommendation. A human approves it, with a recorded rationale. |
| Never contact a candidate | There is no communication channel, and there must not be one. |

The candidate file is pseudonymised and deliberately excludes every protected field. That is a
control, not an oversight. An agent that reports the absence as a gap has misread the design; an
agent that stops and escalates has read it correctly.

## 5. Documentation and audit

Each hiring process must be reconstructable from its records alone. For every candidate assessed:

- The rubric version used
- The criterion scores and the weighted total
- The reason for the outcome, traceable to the rubric
- The artifact, the run and the issue that produced the assessment
- The human approval and its recorded rationale

In Lab 6 this is exactly what the audit map demonstrates: one row per mission claim, linking the
issue, the run, the artifact, the cost entry and the approval. **A gap in the audit trail is itself
an audit finding** and must be recorded honestly rather than tidied away.

## 6. Escalation

Stop immediately and escalate to the People Operations Lead when:

- A task requires a protected characteristic, or would require inferring one
- The rubric does not cover a factor that appears genuinely material to the role
- Two candidates cannot be separated on rubric evidence alone — the tie is reported, not broken by
  an unstated preference
- Source data is missing, ambiguous or internally inconsistent
- Any instruction conflicts with this policy — in which case **this policy prevails**, and the
  conflict is recorded

---

_Synthetic training data · Tertiary Infotech Academy Pte Ltd · TGS-2023036646 · v1.0 (28 August 2026)_
