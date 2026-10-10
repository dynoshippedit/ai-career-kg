---
lesson_id: e-incident-management
slug: incident-management
stage: E
level: 3
prerequisites: [c-incident-response]
roles: []
map_refs: ["CISSP 7.6"]
test_date: 2026-10-10
description: "How to build the incident-management structure around the response lifecycle — team roles, escalation criteria, communications planning, and improvement metrics. A free lesson in the security guidebook, serving CISSP objective 7.6."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Incident management: the team, the escalation, and the communications


**Map ref:** serves **CISSP objective 7.6** — managing incidents as an organizational discipline: team structure, escalation, communications, and improvement.

---

## 1. Where this shows up

The response lifecycle tells you *what* to do about an incident; incident management decides *who* does it, *who gets told*, and *how the organization gets better afterward*. It shows up in the incident where three teams all thought someone else owned containment, in the breach notification sent 40 days late because nobody owned the regulatory clock, in the executive who learned about the outage from a customer — and in the post-incident review that actually changed something. SOC managers, incident commanders, and GRC analysts live here. Note the split with `c-incident-response`: that lesson taught the lifecycle you execute — preparation through lessons-learned, hands on. This lesson teaches the organization you build around it: the team structure and roles, the escalation criteria that route the right incident to the right people, the communications plan that keeps every stakeholder correctly informed, and the metrics that prove the program improves.

## 2. Before you start

- You know the incident-response lifecycle from `c-incident-response` — preparation, detection, containment, eradication, recovery, lessons learned. This lesson staffs it.
- Incident management hands off to continuity; this lesson teaches the handoff from the incident side — the continuity half is `e-bcp-drp`'s subject.
- No tools. The work products are documents: a team charter with roles, an escalation matrix, a communications plan, and a metrics set. Primary spine: **NIST SP 800-61 Rev. 3** (Computer Security Incident Handling Guide, April 2025 — the current revision, restructured around CSF 2.0).

## 3. How it works

Incident management is the scaffolding; the lifecycle is the work. Four structures carry it.

**The team: roles, not heroes.** An incident response team needs defined roles because incidents don't wait for org charts. The standard structure: an **incident commander** (owns the incident — priorities, decisions, the buck stops here; does *not* do the technical work, because command requires the full picture — a commander who goes hands-on debugging loses the incident while winning the ticket), **operations** (containment, eradication, recovery — the hands), **communications** (internal updates, customer notices, regulatory filings — the voice), **liaison roles** (legal, HR, PR, executive sponsor — brought in by criteria, not by panic), and **scribe** (the log — every decision, timestamped; the role everyone skips and every post-incident review wishes existed). Two design rules. First, roles are *assigned per incident*, not per person — the on-call engineer can be incident commander for a SEV-3 and operations for a SEV-1. Second, every role has a named backup, because incidents don't respect vacations (the `e-bcp-drp` tabletop already taught this). The team is sized for the organization's actual incident rate — a three-person "team" for a company with weekly SEV-2s is a burnout plan. SP 800-61 Rev. 3 frames the team within the broader incident-management function: the lifecycle phases are what the team executes, and the guide's CSF 2.0 alignment means the program is measured against governance outcomes, not just response speed.

**Escalation: criteria, not vibes.** Escalation answers two questions: *when does this get bigger* (analyst → incident commander → executive → board), and *when does it cross organizational boundaries* (IT → legal → HR → law enforcement → regulators → customers). The criteria are written in advance as a **severity matrix**: SEV-1 through SEV-4 (or your scale) defined by impact — data types involved, systems affected, customer impact, regulatory triggers — each with response-time targets, who gets paged, and who can declare or downgrade. The declaration authority is named: "the SOC lead can declare SEV-1; the incident commander can downgrade to SEV-2" — because the `e-bcp-drp` lesson already showed what ambiguous authority costs. Escalation also covers the *lateral* moves people forget: when does HR join (insider suspected), when does legal join (before collection, per `e-investigation-forensics` — not after), when does the board get told (criteria, not the CEO's judgment at midnight). The matrix is reviewed after every SEV-1: did the right people join at the right time? If not, the criteria change.

**Communications: the plan before the crisis.** Every incident is also a communications event, and improvising the message mid-incident is how organizations say the wrong thing on the record. The **communications plan** specifies: *internal* (who gets status updates, on what cadence, through which channel — the war-room channel, the executive brief, the all-hands note); *customer* (notification criteria, pre-written templates for the common cases, who approves the words — legal reviews before send, always); *regulatory* (which breaches trigger which filings, the clocks — the plan lists the obligations, not the lawyer's phone number from memory); and *public* (who speaks — one voice, named in advance; everyone else refers inquiries to that voice). Two principles: **pre-write the templates** (the first customer notice is assembled from paragraphs written calmly, not drafted at 3 a.m.), and **separate the technical channel from the stakeholder channel** (the war room's raw speculation must never leak into the customer update — the scribe's log is internal, the comms lead's summary is external).

**Metrics and improvement: the program learns or it rots.** The post-incident review (blameless — the question is what the *system* allowed, not who failed) produces findings with owners and dates, the same discipline as `e-risk-assessment`. The program-level metrics: **MTTD** (mean time to detect), **MTTR** (mean time to respond/recover — define which), **escalation accuracy** (did the severity match the reality?), **recurrence** (same root cause twice is a program failure), and **exercise currency** (when did each playbook last get tested). SP 800-61 Rev. 3's CSF alignment matters here: the metrics should roll up to governance — "are we improving?" is a board question, and the incident program needs an answer with numbers. The review cadence is the control: metrics reviewed quarterly by the security lead, annually with executives. A metrics set nobody reviews is decoration.

### Worked example: Beacon Logistics — the incident-management structure

**The company (fictional, continued from `e-bcp-drp`).** Beacon survived the ransomware scenario in the continuity lesson — barely, and the post-incident review found the management gaps: nobody owned the regulatory clock, the customer notice went out 18 hours late, and the war room had no scribe. This lesson builds what was missing.

**The team charter (excerpt, fictional).** Incident commander: the SOC lead (backup: the infrastructure lead). Operations: SOC analysts plus on-call infrastructure. Communications: the operations manager (backup: the customer-success lead) — owns internal updates, customer templates, regulatory filings checklist. Liaisons: legal (outside counsel, paged for any SEV-1/2), HR (insider criteria), executive sponsor (the COO, briefed at SEV-1). Scribe: rotating analyst assignment, non-optional — the charter states it plainly: *no scribe, no SEV-1 declaration.*

**The escalation matrix (excerpt, fictional).**

| Severity | Criteria | Who joins | Response target |
|---|---|---|---|
| SEV-4 | single-user malware, contained | SOC analyst | 4 hours |
| SEV-3 | multi-system event, no customer data | + incident commander | 1 hour |
| SEV-2 | customer data potentially involved, or dispatch degraded | + legal, comms, COO briefed | 30 minutes |
| SEV-1 | confirmed breach of customer data, or dispatch down | full team, board notified within 24h | 15 minutes |

Declaration: SOC lead declares up; incident commander declares down. Lateral triggers written in: HR joins when an insider is suspected; counsel directs evidence handling from SEV-2 up (the `e-investigation-forensics` rule).

**The communications plan (excerpt, fictional).** Internal: war-room channel (technical, internal only), executive brief every 2 hours at SEV-1 (comms lead's summary, not the raw log). Customer: template library (three pre-written notices: "investigating," "confirmed with scope," "resolved"), legal review before any send, notification criteria tied to the severity matrix. Regulatory: the obligations checklist with clocks — filled from counsel's advice, not from memory. Public: the COO is the single voice; all inquiries route to comms.

**Metrics and the first review.** MTTD, MTTR (defined as declare-to-recover), escalation accuracy, recurrence, exercise currency — baselined this quarter, reviewed quarterly. The ransomware post-incident produced four findings with owners and dates, including this lesson's charter itself.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the team charter, escalation matrix, communications plan, and metrics set above, authored and self-reviewed in-session on 2026-10-10 against SP 800-61 Rev. 3's incident-management framing. Transcript: `runs/e-incident-management.log`.

1. **Charter the team.** For your fictional (or real) organization: incident commander, operations, communications, liaisons (legal, HR, executive), scribe — named roles with named backups. Write the two design rules into the charter: roles assigned per incident, and no SEV-1 without a scribe.
2. **Write the severity matrix.** Three to four levels, defined by impact (data, systems, customers, regulatory triggers) — each with response targets, who joins, and who can declare or downgrade. Then the lateral triggers: HR, legal, board — criteria, not judgment calls.
3. **Plan the communications.** Four audiences (internal, customer, regulatory, public), each with channel, cadence, owner, and approval. Pre-write one template per customer-notice case. Name the single public voice.
4. **Define the metrics.** MTTD, MTTR (define the endpoints), escalation accuracy, recurrence, exercise currency. Set the review cadence and name who reads them — quarterly with the security lead, annually with executives.
5. **Run the tabletop against your own structure.** Take the `e-bcp-drp` ransomware scenario (or your own): walk it through the charter. Who declares? Who joins when? Who tells the customers, with what words, on whose approval? Record every ambiguity as a finding with an owner and a date — the tabletop tests the management structure, not the technical response.
6. **Close the loop.** The tabletop's findings become charter revisions. Date the next exercise and name its owner — the structure decays like every other document.

## 5. On your own

**Task:** Write the severity matrix and communications plan for an organization you know (your employer, your homelab "company," a volunteer group). Then test it: pick a real past incident or outage and walk it through — who would have declared, who would have joined, who would have told whom?

**Success test:** The walkthrough surfaces at least two ambiguities (an unowned decision, a missing lateral trigger, a customer notice with no template). If your structure handles the past incident perfectly, pick a worse incident.

## 6. Where it goes wrong

- **No incident commander.** Three teams, three theories, no one owning the decision. The IC role exists so the incident has exactly one decider.
- **No scribe.** The post-incident review reconstructs decisions from memory and chat scrollback. The log is the cheapest role and the most skipped.
- **Escalation by vibes.** "This feels big" as the criterion — under-escalation until the damage is obvious to everyone, then over-escalation in panic. Written criteria, reviewed after every SEV-1.
- **Legal joins late.** Evidence collected before counsel directed the handling — the `e-investigation-forensics` failure, caused by a missing lateral trigger in the matrix.
- **The 3 a.m. press release.** Customer notice drafted mid-incident, unreviewed, saying the wrong thing on the record. Templates plus legal review exist to prevent exactly this.
- **War-room leakage.** Raw technical speculation reaching customers or the public. Separate the channels; the comms lead's summary is the only external voice.
- **Blameful reviews.** The post-incident that names who failed instead of what the system allowed — which guarantees the next incident's participants stay silent. Blameless is a design choice, not a kindness.
- **Metrics as decoration.** MTTD on a slide nobody discusses. The review cadence — quarterly with the lead, annually with executives — is the control that makes metrics matter.

## 7. Read the source

Primary documents first:

- **NIST SP 800-61 Rev. 3, Computer Security Incident Handling Guide** (csrc.nist.gov, April 2025) — *read* the incident-management framing and the lifecycle phases; *note* the CSF 2.0 restructuring — this is the current revision, and it treats incident response as part of risk management, not a standalone fire department.
- **FIRST CSIRT Services Framework, v2.1** (first.org) — *read* the service catalogue: what a CSIRT (computer security incident response team — the formal name for the team this lesson charters) offers beyond response (coordination, communications, analysis) — useful when chartering the team or scoping what's in-house vs. contracted.

Then at most three free resources:

1. **NIST SP 800-86, Guide to Integrating Forensic Techniques into Incident Response** (csrc.nist.gov, August 2006) — free; the forensic support the escalation matrix must trigger — read for the collection/examination/analysis/reporting phases your liaisons need to understand.

## 8. Check yourself

1. A SEV-2 is declared at 02:00; the matrix says legal joins at SEV-2, but nobody pages counsel until 09:00 — meanwhile IT images the suspect systems. Name the two failures (one in execution, one in the matrix's design) and explain what the imaging delay cost.
2. Explain why the scribe is a role rather than a task — what specifically breaks in the post-incident review when "everyone takes notes," and what does the charter's "no scribe, no SEV-1" rule buy?
3. Distinguish escalation from notification: which one moves people into the response, which one moves information out, and what goes wrong when the same person owns both without a plan?
4. A post-incident review concludes "the analyst should have escalated sooner." Using the blameless principle, rewrite the finding as a system failure — then name the matrix change that prevents recurrence.
5. Predict the communications of an organization with no plan, 24 hours into a confirmed customer-data breach: who speaks, what do they say, and which of the four audiences is served worst?

## 9. Prove it

**Artifact:** your team charter (roles, backups, the per-incident assignment rule), severity matrix (criteria, response targets, declaration authority, lateral triggers), communications plan (four audiences, templates, approvals, the single public voice), and metrics set (definitions, baselines, review cadence) — for the Beacon worked case in your own words, or better, for an organization you actually serve, tested against a real past incident.

**Honest claim:** "I can build the incident-management structure — staff the response with clear roles, route the right incident to the right people by written criteria, keep every stakeholder correctly informed, and make the program improve from its own history."
**Can't claim yet:** "I can command a major incident" — incident command under real pressure, with lives or livelihoods on the line, is earned in exercises and real events; this lesson taught the structure that makes command possible, not the command itself.

## 10. Leads to

- `c-incident-response` — the lifecycle this structure staffs; reread it as the "what the team executes" companion.
- `e-investigation-forensics` — the evidence handling the escalation matrix must trigger early.
- `e-bcp-drp` — the handoff: incident management contains and recovers; continuity runs the business through it.
- `e-board-communication` — the executive and board briefing this plan's metrics feed.
- Map refs: **CISSP 7.6** (this lesson); feeds **CISSP 7.1** (investigations) and **7.10–7.13** (continuity and recovery).

---

*Worked case authored and self-reviewed 2026-10-10; all scenario data fictional. Sources fetched in-session — see `runs/e-incident-management.log`.*
