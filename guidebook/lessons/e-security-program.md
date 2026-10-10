---
lesson_id: e-security-program
slug: security-program
stage: E
level: 3
prerequisites: [e-risk-assessment, e-sdlc, c-incident-response]
roles: [grc-analyst]
map_refs: []
test_date: 2026-10-09
description: "Running a security program: strategy in the Govern loop, the metrics that matter vs vanity metrics (KPI vs KRI), risk-based prioritization, and the program charter as the worked artifact. A free lesson in the security guidebook."
dateline: "Worked case authored and reviewed 2026-10-09 · no command line in this lesson"
---
# Running a security program


**Map ref:** brief §5 "Running a security program"; **CISSP Domain 1** (Security and Risk Management) at program level; NIST CSF 2.0; NIST SP 800-55; feeds `e-board-communication`, the Stage E capstone path.

---

## 1. Where this shows up

Someone has to own security as a whole — not the vulnerabilities, the tools, or the incidents, but the *program*: the direction, the resources, the proof it works. That someone is the security program lead (a candidate role for the site's Stop 1 list — no role page created), and the GRC analyst is usually their right hand. The job shows up in every organization large enough to have one person whose title contains "security": setting strategy, deciding what gets funded, knowing whether the controls work, and answering for the result. The brief puts this lesson in Stage E deliberately — it is the work everything else in the guidebook feeds.

## 2. Before you start

- You can build a risk register (`e-risk-assessment`) — the program's prioritization engine.
- You understand SDLC gates (`e-sdlc`) and incident response (`c-incident-response`) — two capabilities the program must operate, not just admire.
- No tools, no terminal. The work product is a document: the program charter. Bring the hard rule from the brief: no invented numbers — every figure traces to a named source.

## 3. How it works

A security program is a loop, not a project. NIST CSF 2.0 §5 describes the mechanism as a **bidirectional flow**: executives set priorities and communicate expectations about risk appetite, accountability, and resources; managers build Target Profiles and action plans; practitioners implement, measure operational risk, and report back up. The program is that loop running continuously. Everything in this lesson hangs off it.

**Strategy.** Strategy lives in Govern — the CSF function at the center of the wheel. In plain terms, the strategy answers four questions, and the charter records the answers:
1. **What are we protecting, and why does it matter?** (The mission, in business terms — customer data, service availability, the things a breach would actually break.)
2. **What is our risk appetite?** What level of risk leadership will accept, stated plainly enough that a manager can use it to decide. "We accept no unpatched internet-facing criticals beyond 14 days" is a strategy; "we take security seriously" is a poster.
3. **Who is accountable for what?** Named roles, not teams — the charter's RACI names people. Accountability that points at a department points at no one.
4. **How do we know it's working?** The measurement plan (below). A strategy without measurement is a wish.

**Metrics: the ones that matter vs. the vanity kind.** Two primary sources anchor this, and the lesson keeps them separate:
- NIST SP 800-55 (Measurement Guide for Information Security; Volumes 1 and 2, final December 2024) gives the *method*: develop, select, prioritize, and validate measures — quantitative and qualitative — with attention to documentation, reporting, data quality, and uncertainty. Then run measurement as a program: defined roles, a communication plan, managed data. Measurement is itself a program inside the program.
- CSF 2.0 §5 names the two metric *families* leadership needs: **KPIs (key performance indicators)** — how well the program's activities are performing (control coverage, patch latency, training completion, backup-test success); and **KRIs (key risk indicators)** — the level of exposure itself (risks above tolerance, unpatched internet-facing systems, mean time to detect). The distinction is the whole point: KPIs measure the *program's work*; KRIs measure the *risk's size*. A program can have excellent KPIs and terrible KRIs — busy but exposed — and reporting only KPIs is how leadership learns the program is fine two weeks before the incident.

Vanity metrics are the failure mode: numbers that move without meaning anything. "Attacks blocked" (blocked attacks are noise, and counting them rewards being attacked); raw vulnerability counts with no severity or exposure context; training completion as a proxy for behavior change; a single "security score" that averages away the actual risks. The test for any metric: *what decision does this number change?* If the answer is "none," it doesn't belong in the program — it belongs in a dashboard nobody reads, or nowhere.

**Risk-based prioritization.** The register (`e-risk-assessment`) is the input; the action plan is the output. Prioritization is mechanical once the register is honest: risks above tolerance get responses with owners and dates; responses become actions; actions get sequenced by risk reduction per effort. The charter records the prioritization *rule* (e.g., "High and Critical risks get funded responses within one quarter; Medium risks get scheduled responses; Low risks are monitored"), not just this quarter's list — because the list changes and the rule must survive the change.

**The program charter.** The charter is the program's constitution: the document that says what the program is, who runs it, what authority it has, and how it proves its worth. It is the worked artifact of this lesson, and the worked example below is its skeleton with flesh on.

### Worked example: program charter for Beacon Logistics

Beacon Logistics (the fictional freight company from `e-risk-assessment`): customer shipment-tracking portal, PII in the customer database, no dedicated security staff yet — the charter is written for the incoming program lead.

**1. Mission.** Protect customer data and shipment operations so the business can promise both in contracts. One paragraph, business language, no jargon.

**2. Scope.** In scope: the customer portal, the customer database, the admin panel, the cloud accounts that host them, and the third parties with access to customer data. Out of scope (stated explicitly): vehicle telematics, corporate email — with the note that scope is reviewed annually, because unstated scope is where incidents come from.

**3. Roles and accountability (RACI, abridged).**

| Activity | Program lead | IT lead | Founders |
|---|---|---|---|
| Risk register maintenance | A (owns) | R (provides) | I (informed) |
| Patch SLA for internet-facing | A | R (executes) | I |
| Incident declaration | R (declares) | R (responds) | A (accountable) |
| Board reporting | R (authors) | C (data) | I (receives) |
| Risk acceptance decisions | R (recommends) | C | A (decides) |

**4. Risk strategy.** Appetite statement: "Beacon accepts no High or Critical risk without a funded response plan within one quarter; Medium risks get scheduled responses within two quarters; Low risks are monitored." Tolerance: the register's defined scales (from `e-risk-assessment`), reviewed with the register quarterly.

**5. Measurement plan.** Three KPIs (program work): patch latency for internet-facing systems — source: vulnerability scans, definition: days from disclosure to deployed fix, target ≤14 days; backup restore-test success — source: quarterly test log, definition: successful restore of the customer database to a scratch environment; access-review completion — source: review records, definition: % of privileged accounts reviewed quarterly. Three KRIs (exposure): risks above tolerance — source: risk register, definition: count of High/Critical risks without a funded response; unpatched internet-facing criticals — source: scans, definition: count older than 14 days; mean time to detect — source: incident log, definition: hours from first indicator to declared incident. Every metric names its source, its definition, and its target — SP 800-55's documentation discipline, applied.

**6. Review cadence.** Register reviewed monthly by the program lead, quarterly with founders; charter reviewed annually; metrics reported quarterly (the board memo in `e-board-communication` is the reporting vehicle).

## 4. Walkthrough

No command line in this lesson — the walkthrough is the charter, and the transcript is the authoring log with the self-review checklist: `runs/e-security-program.log`.

1. **Write the mission** in one paragraph of business language. Test: a non-technical founder nods instead of asking what a word means.
2. **Scope the program**: in-scope systems, explicitly out-of-scope systems, and the review trigger. Test: every system holding customer data from the `e-risk-assessment` example appears in scope.
3. **Build the RACI** for at least six activities (register maintenance, patching, incident declaration, board reporting, risk acceptance, vendor review). Test: every row has exactly one A; no activity's A is a department.
4. **Write the risk appetite statement** in the worked example's form — thresholds, timeframes, no posters.
5. **Define the measurement plan**: three KPIs and three KRIs, each with source, definition, and target. Test: apply the "what decision does this change?" test to each — cut any metric that fails it, and log the cut.
6. **Set the review cadence** and name the reporting vehicle.
7. **Self-review** against the checklist in the log: mission in business language; scope explicit both ways; RACI with single accountability; appetite with thresholds and timeframes; every metric sourced, defined, targeted, and decision-linked; no invented numbers anywhere (placeholders labeled where real data doesn't exist yet); review cadence named.

## 5. On your own

Take the Harborlight Books assistant threat model from `ai-threat-modeling` and write the measurement plan a program lead would need for it: three KPIs and three KRIs specific to that AI system (not generic security metrics — what does "patch latency" mean for a model? what is the AI equivalent of "unpatched internet-facing criticals"?). Each metric needs source, definition, target, and the decision it changes.

**Success test:** a reader who knows the Harborlight system can point at where each metric's data comes from, and at least one of your KRIs measures model-specific exposure (data leakage, excessive agency, pipeline integrity) rather than generic IT hygiene.

## 6. Where it goes wrong

- **Activity reported as risk.** "We blocked 10,000 attacks" is the canonical vanity metric — it measures being attacked, not being safe. Every metric in the charter must survive the decision test.
- **KPIs without KRIs.** The program looks industrious while exposure grows. The charter requires both families, reported together, every time.
- **Metrics nobody owns.** A metric with no owner and no review date is a number that will be wrong within a quarter and nobody will notice. SP 800-55's program discipline — roles, communication, data management — exists because of this failure.
- **The charter as a wish list.** A charter that promises outcomes without authority ("the program will ensure...") instead of defining authority ("the program lead may...") is a document that will be ignored at the first conflict. Authority is the charter's real content.
- **Invented numbers.** A metric nobody measured teaches leadership to trust numbers that aren't real — and then to distrust the real ones. Placeholders are labeled; sources are named; the lesson's hard rule holds.

## 7. Read the source

- **NIST Cybersecurity Framework 2.0** (nist.gov/cyberframework; the document is NIST CSWP 29) — §5 (the bidirectional executive/manager/practitioner flow, KPI/KRI families, enterprise-risk integration) and §3 (Profiles and Tiers — the strategy's working method). Read §5 first; it is this lesson's spine. (NIST CSF page fetched 2026-10-09.)
- **NIST SP 800-55, Measurement Guide for Information Security** (Volumes 1 and 2, final December 2024) — v1: developing, selecting, prioritizing, and validating measures, with data quality and uncertainty; v2: running measurement as a program. Read the release page for scope, then v1's measure-development chapters. (Release page fetched 2026-10-09.)
- **NIST SP 800-30 Rev. 1** — the risk assessment method the register (and therefore the prioritization rule) is built on. You read it in `e-risk-assessment`; re-read §3's communicate-and-maintain step with program eyes.

Free resources for going deeper (≤3): the CSF 2.0 document; the SP 800-55 volumes; SP 800-30 Rev. 1.

## 8. Check yourself

1. Your KPIs are all green and your KRIs are getting worse. Explain how that is possible, and what you tell the board — in two sentences a director would understand.
2. A founder asks you to add "number of attacks blocked" to the charter's measurement plan. Apply the decision test from §3 and write the one-paragraph reply refusing it.
3. Your RACI has "IT department" as Accountable for patching. What breaks, and how do you fix the row?
4. The charter promises "the program will ensure no breaches occur." Rewrite that line as an authority statement, and explain why the original version guarantees the charter will be ignored.
5. A risk sits at Medium for three quarters with no scheduled response. Which part of the charter failed — the appetite statement, the prioritization rule, or the review cadence? Explain how you can tell.

## 9. Prove it

**Artifact:** the complete program charter for Beacon Logistics — mission, scope, RACI, risk appetite statement, measurement plan (3 KPIs + 3 KRIs, each sourced/defined/targeted), and review cadence — with the self-review checklist signed off.

**You can claim:** "I can design a security program's governing document — strategy, accountability, risk-based prioritization, and a measurement plan that distinguishes program activity from actual exposure — and defend every metric in it."

**You cannot claim:** executive experience; authority to accept risk on a real company's behalf; or that the charter alone makes anything secure — the charter authorizes and directs the work, it is not the work.

## 10. Leads to

- `e-board-communication` — the charter's reporting vehicle: the board memo this lesson's measurement plan feeds.
- `e-risk-assessment` — the register method this program runs on.
- The Stage E capstone path: a full program plan for a real (authorized) small organization — profile, register, measurement plan, and board pack — as the level-4 artifact.
- **Map refs:** brief §5 "Running a security program" (served directly); **CISSP Domain 1** (program level); NIST CSF 2.0; NIST SP 800-55.
