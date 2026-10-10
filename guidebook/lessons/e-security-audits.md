# Security audits: independence, evidence, and the finding that holds up

**ID:** `e-security-audits` · **Stage:** E (Expert) · **Level:** 3 (write an audit plan for a control family and execute it to a defensible finding) · **Prerequisites:** `e-assessment-strategy` (the strategy this audit serves — audits are the independent half of it); no command line in this lesson.

**Map ref:** serves **CISSP objective 6.5** — conducting and facilitating security audits.

---

## 1. Where this shows up

Testing asks "can it be broken?"; audit asks "is the control operating as claimed, with evidence?" The difference is independence and evidence: the auditor doesn't work for the control owner, and every conclusion traces to artifacts a stranger could re-examine. It shows up in the external audit ("show me the change tickets for Q3"), in the internal audit plan's risk-based scoping, and in the finding that survives management's pushback because the evidence is unimpeachable. GRC analysts, internal auditors, and the security leaders who *facilitate* audits (as opposed to conducting them) live here — facilitation is half the lesson, because most readers will host auditors before they become one.

## 2. Before you start

- You have the assessment strategy (`e-assessment-strategy`) — the audit is the independent assurance half of that strategy, distinct from the testing half.
- You know control claims and evidence thinking from `e-control-testing` and `e-security-metrics` — audit is where evidence standards get strictest.
- No tools. The work products are an audit plan and one completed finding for a fictional company.

## 3. How it works

An **audit** is an independent, evidence-based examination of whether controls operate as intended. Three words carry the weight: **independent** (the auditor is not the control owner — self-review is not audit), **evidence-based** (conclusions rest on artifacts, not assertions), and **criteria** (there is a stated standard the control is measured against — a policy, a regulation, a framework). Testing finds weaknesses; audit renders a verdict against criteria. Both matter; they are not the same.

**The standards: ISACA's ITAF.** The profession's framework is ISACA's **IT Audit Framework (ITAF), 5th Edition** — the comprehensive framework establishing standards for IT audit and assurance practitioners' roles and responsibilities, ethics, and expected professional behavior, plus guidance for planning, performing, and reporting engagements (the 5th edition integrates AI audit guidance). ITAF structures engagements the way this lesson does: plan against risk, perform with supervision and evidence discipline, report with conclusions and follow-up. The lesson teaches from ITAF's structure and from free overviews — the framework document itself is the auditor's primary, and where access requires steps, the lesson says so honestly.

**Types of audit.** **Internal audit** (your organization's auditors, reporting to the board or audit committee — independence via reporting line, not employment), **external audit** (an outside firm — independence via distance, paid by the company but reporting to the board), and **third-party/regulatory audit** (the regulator or customer auditor — independence via authority). The strategy lesson decides the mix; this lesson teaches how each is conducted and — equally — how each is *facilitated*: the auditee's job is evidence readiness, not persuasion.

**The audit plan.** For one control family, the plan states:

- **Objectives:** what the audit will conclude — written as verdicts to be rendered ("change management controls operated effectively for in-scope systems in Q3"), not topics to be explored.
- **Scope and criteria:** which systems, which period, measured against which policy/standard. The criteria are named explicitly — findings argue against criteria, not against the auditor's opinion.
- **Procedures:** the tests — inquiry (ask), observation (watch), inspection (read the artifact), reperformance (redo the control yourself). The plan mixes them deliberately: inquiry alone is hearsay; reperformance is the gold standard and the most expensive.
- **Evidence requests:** the artifacts, named in advance — the change tickets, the approval records, the access logs, the configuration exports. Advance requests are the facilitation half: the auditee gathers; the auditor verifies.
- **Sampling:** you cannot test every change ticket. The sampling approach states the population, the method (judgmental for the risky items — all emergency changes, all privileged changes — plus random or systematic for the rest), the sample size rationale, and what a sample failure means (one failed emergency change is a finding; one failed routine change may expand the sample).

**The finding write-up.** A finding has five parts, and the discipline is that each is separate: **criteria** (what should be), **condition** (what is — the observed fact), **cause** (why it happened — the control gap, not the person), **effect** (the risk — what the gap exposes), and **recommendation** (the fix, addressed to the control owner). Management responds; the auditor evaluates the response; disagreement is documented, not negotiated away. The finding that holds up is the one where each part is evidenced and the chain from criteria to recommendation has no gaps.

**Facilitating an audit** — the half most readers do first. The facilitator's job: evidence ready before the auditors arrive (the plan's evidence requests, gathered in advance), the right people available (control owners, not proxies), no coaching of answers (inquiry is evidence; rehearsed inquiry is theater), findings tracked to closure like any other remediation, and the audit treated as a control test of the program itself — the findings about *your* evidence discipline are the valuable ones.

### Worked example: Alderpoint Mutual — audit plan for the change-management control family (fictional, continued)

**Objectives.** Render verdicts on whether change-management controls operated effectively for the customer portal and policy admin system during 2026-Q3, against the company's change-management policy v2.1 (criteria).

**Procedures and evidence.** (1) Inspection: all 14 emergency changes in Q3 — approval records, testing evidence, post-implementation review. (Sampling: 100% of emergency changes — judgmental, risk-based.) (2) Inspection + reperformance: random sample of 25 routine changes from the 312 in the population — verify approval, testing, and implementation match the ticket; reperform the approval workflow for 5. (3) Inquiry + observation: attend one change-advisory-board meeting; interview the release manager on the emergency-change process. (4) Data analysis: compare the deployment log against the ticket system — every production deployment should have a ticket (the completeness check).

**Evidence requests (issued in advance).** Q3 change tickets export, CAB meeting minutes, the emergency-change log, production deployment logs, the change policy v2.1, the approver roster with delegation records.

**One completed finding (fictional).**

- **Criteria:** Policy v2.1 §4.2 — emergency changes require post-implementation review within 5 business days.
- **Condition:** 6 of 14 emergency changes lack post-implementation review records; 3 more were reviewed after 15+ days. (Evidence: emergency-change log vs review records, inspected 2026-10-08.)
- **Cause:** The emergency process has no review-scheduling step — the ticket closes at implementation, and nothing reopens it for review.
- **Effect:** Unreviewed emergency changes bypass the control that catches unauthorized or faulty urgent work; the highest-risk change class has the weakest oversight.
- **Recommendation:** Add a system-enforced review task on emergency-ticket closure (owner: release manager, due 2026-11-30); retroactively review the 6 missing (owner: change manager, due 2026-10-31).
- **Management response:** Accepted. (Documented; the auditor does not implement the fix — independence.)

**Facilitation notes.** Evidence delivered two days before fieldwork; the release manager (control owner) attended all inquiry sessions; one finding was initially disputed ("the reviews happened verbally") — resolved by criteria: the policy requires *records*, and none exist. The dispute and its resolution are in the workpapers.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the audit plan and completed finding above, authored and self-reviewed in-session on 2026-10-10 against ITAF's engagement structure. Transcript: `runs/e-security-audits.log`.

1. **Pick the control family.** One family — change management, access control, backup operations. Narrow enough to audit deeply in the exercise.
2. **Write the objectives as verdicts.** "Render a verdict on whether X operated effectively for Y during Z against criteria C." If the objective can't be written as a verdict, it's a research topic, not an audit.
3. **Name the criteria.** The policy, standard, or regulation — versioned. Every finding will argue against these.
4. **Design the procedures.** Mix inquiry, observation, inspection, reperformance. Put the expensive procedures (reperformance) where the risk is (emergency changes, privileged actions).
5. **Issue the evidence requests.** In advance, named artifacts. This is the facilitation rehearsal.
6. **Set the sampling.** Population, method, size rationale, and the rule for what a failure triggers (finding vs expanded sample).
7. **Write one finding completely.** All five parts, each evidenced, the chain unbroken. Then write the facilitation note: how the dispute (there should be one — plant it if you must) was resolved by criteria.

## 5. On your own

**Task:** Audit one control family on a system you run — your backup procedure, your change process for the homelab, your access reviews. Write the plan, issue yourself the evidence requests, sample, and write one finding in the five-part format.

**Success test:** Your finding's condition is an observed fact (not an impression), the cause names the control gap (not a person), and you can point to the evidence artifact for each part. If you can't produce the artifact, the finding isn't ready.

## 6. Where it goes wrong

- **Self-review called audit.** The control owner "audits" their own control. Independence is structural — reporting line, not good intentions.
- **Criteria never named.** Findings argued against the auditor's opinion instead of a stated standard. Management disputes the opinion; they can't dispute the criteria they signed.
- **Inquiry as the only procedure.** "The manager said the reviews happen." Without inspection or reperformance, the audit is a transcription service.
- **Sampling without rationale.** "We looked at a few." A few of what, chosen how, meaning what? The sample is the audit's evidentiary foundation — vague sampling voids the verdict.
- **Findings negotiated away.** The draft finding softened until it says nothing, because the relationship mattered more than the verdict. Disagreement is documented; the finding stands on its evidence.
- **The auditee who performs.** Facilitation curdled into obstruction: evidence dribbled out, proxies sent to interviews, answers rehearsed. The auditor notes it — and the note becomes a finding about the control environment.
- **No follow-up.** The report issued, the findings tracked nowhere. ITAF's reporting standards include follow-up — a finding without tracked remediation is a suggestion.
- **Auditor implements the fix.** Helpful, and fatal to independence. The auditor recommends; the owner implements; the auditor verifies.

## 7. Read the source

Primary documents first:

- **ISACA ITAF, 5th Edition** (isaca.org — free download via account checkout) — *read* the engagement structure: planning, performing, reporting; the standard the profession audits against. Note the edition's AI audit guidance as the current frontier.
- **NIST SP 800-115** (csrc.nist.gov) — *reread* as the technical complement: ITAF governs the engagement; 800-115 describes the techniques the procedures may call on.

Then at most three free resources:

1. **ISACA Now: ITAF 5th edition overview** (isaca.org, blog) — free; what changed in the 5th edition and why it matters for audit planning.
2. **NIST SP 800-53, control families** (csrc.nist.gov) — free; the control catalog your audit plans select families from — the criteria source.
3. Your guidebook's own `e-assessment-strategy` — where the audit sits in the year's assurance; `e-test-analysis-reporting` — the findings pipeline your audit findings join.

## 8. Check yourself

1. The change manager "audits" the change process and reports full compliance. Name the independence failure precisely — and the structural fix (not "try harder to be objective").
2. An audit tests 3 of 300 change tickets, chosen undescribed. Explain what the sampling must state for the verdict to mean anything — population, method, size rationale, failure rule.
3. A finding's condition is documented but its criteria section is empty. Explain why management can legitimately dispute this finding — and what the criteria section would have to contain.
4. During fieldwork, the auditee sends a junior proxy to every interview and delivers evidence in dribbles. As the facilitator's counterpart, what do you do — and what does the workpaper note say?
5. Six emergency changes lack post-implementation reviews. Argue whether this is one finding or six — and what the cause section must establish either way.

## 9. Prove it

**Artifact:** your audit plan (objectives as verdicts, scope, named criteria, procedures mixing all four evidence types, advance evidence requests, sampling with rationale and failure rules) plus one completed five-part finding with management response and the facilitation note — for the Alderpoint worked case in your own words or a control family you actually audited.

**Honest claim:** "I can plan and conduct an audit of a control family — I can set objectives as verdicts, gather evidence to a standard, sample with rationale, write findings that hold up against pushback, and facilitate an audit without compromising it."
**Can't claim yet:** "I am a qualified auditor" — professional audit practice (ITAF in full, professional standards, audit program management) is its own discipline; this lesson taught the engagement as the reader will first meet it.

## 10. Leads to

- `e-assessment-strategy` — the strategy this audit serves; `e-test-analysis-reporting` — where audit findings join the remediation pipeline.
- `e-security-metrics` — audit coverage and finding-closure as program measures; `e-control-testing` — the technical procedures audits call on.
- Map refs: **CISSP 6.5** (this lesson); feeds **CISSP 6.1** (strategy) and **6.4** (reporting); the facilitation half serves **CISSP 1.3** (governance).

---

*Sources fetched 2026-10-10: ISACA ITAF 5th edition (isaca.org); NIST SP 800-115; NIST SP 800-53 (csrc.nist.gov). Full ledger in the batch manifest.*
