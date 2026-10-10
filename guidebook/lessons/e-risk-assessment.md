---
lesson_id: e-risk-assessment
slug: risk-assessment
stage: E
level: 3
prerequisites: []
roles: [grc-analyst]
map_refs: ["CISSP 1.9"]
test_date: 2026-10-09
description: "Risk assessment as a worked case: scope, rate, respond and report, end to end — serving CISSP objective 1.9. A free lesson in the security guidebook."
dateline: "Worked case authored and reviewed 2026-10-09 · no command line in this lesson"
---
# Risk assessment as a worked case


**Map ref:** serves **CISSP objective 1.9** — risk management concepts end to end.

---

## 1. Where this shows up

Risk assessment is the decision-making engine of every security program: it is how an organization decides what to fix first, what to accept, and what to explain to its leadership. In the CISSP it anchors Domain 1 (Security and Risk Management, 16% of the exam) as objective 1.9. In practice it shows up in vendor security reviews ("show us your risk register"), in audit evidence, in board memos, and in every "should we buy this tool or fix that system" argument you will ever have. The security engineer who can assess risk clearly is the one whose recommendations get funded. This lesson produces a real one.

## 2. Before you start

- You can describe realistic threats and vulnerabilities for a web application (Stage C). You do not need exploits — you need judgment about what is plausible.
- No tools, no terminal. The work product is a document. Bring a skeptical mind and a refusal to invent numbers (more on that in §6).
- Primary method reference: **NIST SP 800-30 Rev. 1, Guide for Conducting Risk Assessments** (September 2012) — the assessment process in this lesson follows its structure: prepare, conduct, communicate and maintain.

## 3. How it works

A **risk** is the potential for a threat to exploit a vulnerability and cause harm. Three ingredients, kept rigorously separate: the **threat** (who or what acts — e.g., an external attacker, a malicious insider, a failure), the **vulnerability** (the weakness — e.g., unpatched VPN, no MFA), and the **impact** (what breaks — e.g., customer data exposed, operations halted). A threat without a vulnerability is noise; a vulnerability without a threat is a finding waiting for one; neither is a risk until both meet an impact.

The assessment process (SP 800-30 Rev. 1, paraphrased):

1. **Prepare** — define scope, pick your scales, gather system knowledge. A risk assessment without agreed scales is an argument, not an analysis.
2. **Conduct** — identify threats and vulnerabilities, determine **likelihood** (how probable is exploitation, given the threat and the weakness) and **impact** (how bad if it happens), combine them into a **risk level**, and decide responses.
3. **Communicate and maintain** — report to decision-makers, assign owners, and revisit. A risk register nobody reviews is a diary.

Likelihood and impact are rated on **qualitative scales** — words, not numbers. Typical likelihood: Rare, Unlikely, Possible, Likely, Almost Certain. Typical impact: Negligible, Minor, Moderate, Major, Catastrophic. The risk level comes from a **matrix** crossing the two: a Likely × Catastrophic risk is Critical; a Rare × Minor risk is Low. The matrix is a communication tool, not mathematics — multiplying ordinals is meaningless, and the lesson's hard rule is that you never present matrix arithmetic as a calculation. Words in, words out, judgment throughout.

For each risk above the organization's tolerance, choose a **response**: **mitigate** (add controls to reduce likelihood or impact), **transfer** (insurance, contracts — the risk moves, it does not vanish), **accept** (documented, owned, time-bound — "we accept this until Q3" with a named owner), or **avoid** (stop doing the risky thing). Then select **controls by type**: **preventive** (stop it — MFA, patching), **detective** (find it — logging, alerting), **corrective** (recover — backups, incident response). A risk with only preventive controls and no detection is a hope, not a plan.

### Worked example: Beacon Logistics shipment portal

**Scope and scales (prepare).** Beacon Logistics is a fictional regional freight company. In scope: its customer shipment-tracking web portal. Out of scope: vehicle telematics, the corporate email system. Scales as above; risk tolerance: anything rated High or Critical must have a response plan with an owner within one quarter.

**Assets:** (1) customer database — names, addresses, shipment contents (PII); (2) the tracking API; (3) the admin panel used by dispatch staff.

**Risk 1 — SQL injection in the tracking search → customer PII breach.** Threat: external attacker probing the portal (automated scanning of logistics sites is routine). Vulnerability: the tracking search concatenates input into a database query (found in a Stage B-style review). Likelihood: **Likely** — the endpoint is internet-facing and the flaw is directly testable. Impact: **Major** — bulk PII exposure triggers breach-notification obligations and customer loss. **Risk: High.** Response: **mitigate**. Controls: preventive — parameterized queries, deployed this sprint; detective — WAF alerting on SQL-probe patterns plus query-anomaly logging; corrective — incident runbook for a suspected breach. Owner: application lead. Residual risk after controls: **Low** (re-assess post-deploy).

**Risk 2 — credential stuffing against customer logins → account takeover.** Threat: credential-stuffing botnets using breached password lists. Vulnerability: no rate limiting or MFA on the customer login. Likelihood: **Almost Certain** over a year — this traffic hits every login form on the internet. Impact: **Moderate** — individual accounts compromised, shipment data viewed, support load; bulk impact limited per account. **Risk: High.** Response: **mitigate**. Controls: preventive — rate limiting, breached-password screening, optional MFA for customers; detective — impossible-travel and burst-login alerting. Owner: platform lead. Residual: **Medium** (accepted until MFA adoption is measured — documented, owned, dated).

**Risk 3 — ransomware via unpatched edge VPN → operations halt.** Threat: ransomware affiliates targeting edge devices. Vulnerability: VPN concentrator two firmware versions behind, internet-facing. Likelihood: **Possible** — exploited edge devices are a known initial-access vector (CISA KEV lists several). Impact: **Catastrophic** — dispatch and tracking down, contractual penalties, recovery measured in days. **Risk: Critical.** Response: **mitigate** urgently + **transfer** partially. Controls: preventive — emergency patching window, network segmentation of the VPN segment; detective — EDR on reachable hosts, VPN log alerting; corrective — tested offline backups, documented recovery runbook. Owner: infrastructure lead, executive sponsor. Residual: **Medium** after patching.

**Risk 4 — insider bulk export of the customer database.** Threat: a departing sales employee. Vulnerability: no export alerting; broad read access for the sales role. Likelihood: **Unlikely** — no indicators, small team. Impact: **Major** — full customer list to a competitor. **Risk: Medium.** Response: **mitigate**. Controls: preventive — least-privilege review of the sales role; detective — bulk-export alerting on the customer table; corrective — access revocation runbook for departures. Owner: security lead. Residual: **Low**.

**Monitoring plan (maintain):** quarterly register review; the WAF/EDR alerts from Risks 1–3 feed a monthly metrics check; any new internet-facing endpoint triggers a mini-assessment before launch. The register is a living document — "maintain" is the step everyone skips and the step that makes the rest matter.

**One-page risk report (communicate).** Addressed to Beacon's operations director: *We assessed the shipment portal against four scenarios. One risk is Critical (unpatched edge VPN — patching window proposed for this month, needs your approval), two are High (SQL injection in tracking search — fix in progress; credential stuffing — rate limiting deployed, MFA rollout planned), one is Medium (insider export — alerting added). Residual risk after planned controls is Medium or lower across the board. Decisions needed from you: approve the emergency maintenance window; accept the Medium residual on credential stuffing until MFA adoption is measured (owner and review date attached).* Every claim traces to the register; every risk has an owner; nothing is "handled" without evidence.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" for this lesson is the assessment itself, authored and reviewed in-session on 2026-10-09 against SP 800-30 Rev. 1's process. Transcript: `runs/e-risk-assessment.log` (records scope, scales, and review notes — there are no commands to transcribe).

1. **Prepare.** Write one paragraph of scope (what is in, what is out) and fix your likelihood/impact scales and risk tolerance *before* identifying any risk. If you catch yourself adjusting a scale to make a pet risk look bigger, you have found the reason this step comes first.
2. **Inventory assets.** List the assets in scope and what makes each one matter (data, availability, trust). Three to six assets is plenty.
3. **Identify threat × vulnerability pairs.** For each asset, name 2–4 realistic pairs. Each pair gets one row. If you cannot name the vulnerability concretely, you have a worry, not a risk — either sharpen it or drop it.
4. **Rate likelihood and impact — with reasons.** Every rating gets one sentence of justification citing evidence (exposure, KEV membership, past incidents, control state). "Likely because internet-facing and directly testable" is a reason; "Likely because it feels likely" is not.
5. **Read the matrix, then decide responses.** Anything at or above tolerance gets mitigate/transfer/avoid with controls by type (preventive, detective, corrective), an owner, and a date. Anything below tolerance gets documented acceptance with an owner and a review date — or it will be forgotten.
6. **Write the one-page report.** Audience: a busy executive. Risks in plain language, decisions needed, owners, residual risk. If it needs a second page, cut — the register holds the detail.

## 5. On your own

**Task:** Risk-assess a system you actually run — your home lab network, your personal VPS, or the lab environment from Stage B. Scope it in one paragraph, identify at least four threat × vulnerability pairs, rate and justify each, assign responses with owners (you) and dates, and write the one-page report addressed to yourself as the executive.

**Success test:** A stranger reading your register can trace every risk rating back to a stated reason, every response to an owner and date, and your one-page report contains at least one explicit decision ("approve," "accept until," "fund") rather than a summary. If all your risks came out Low, your scope was too narrow or your honesty too generous — redo it.

## 6. Where it goes wrong

- **Invented statistics.** "There is a 73% chance of breach" — no, there is not. Likelihood scales are qualitative for a reason: nobody has the data for real probabilities, and fabricated precision destroys credibility. This is a hard rule: every number in a risk assessment must be sourced or it does not appear.
- **Confusing the ingredients.** Listing vulnerabilities as risks ("unpatched server" is not a risk — it is a vulnerability waiting for a threat and an impact). The threat × vulnerability × impact discipline exists to stop this.
- **Treating the matrix as math.** High × Medium is not a computation; the matrix is a structured conversation. Two assessors who disagree by one cell should talk, not average.
- **Acceptance without an owner and a date.** "Accepted risk" with no name and no review date is not acceptance — it is abandonment with paperwork.
- **Controls of one type.** All-preventive plans fail silently; all-detective plans watch the disaster in high definition. Every significant risk wants all three types.
- **One-and-done.** The assessment that is never maintained decays from the day it is written — new endpoints, new threats, drifted controls. "Maintain" is a process step, not a aspiration.
- **Risk theater for compliance.** An assessment written to satisfy an auditor, with every risk rated Low and no decisions requested, teaches the organization that risk assessment is fiction. Write the honest version; note where it differs from what anyone wanted to hear.

## 7. Read the source

Primary documents first:

- **NIST SP 800-30 Rev. 1, Guide for Conducting Risk Assessments** (csrc.nist.gov, September 2012) — *read* Chapter 3 (the assessment process: prepare, conduct, communicate/maintain) and the risk-level matrix construction; *skim* the appendices (threat/vulnerability tables are useful references); *skip* the federal-tier framing on first pass — the method ports to any organization.
- **NIST SP 800-39, Managing Information Security Risk** (csrc.nist.gov) — *skim* the three-tier model (organization, mission/business process, information system); *read* the risk-response section. It is the parent document SP 800-30 amplifies.
- **NIST Cybersecurity Framework 2.0, Govern function** (nvlpubs.nist.gov) — *skim* GV.OC and GV.RM; risk assessment lives inside governance, and this is where the board-level conversation connects.

Then at most three free resources:

1. **NIST CSF 2.0** (free PDF, nist.gov) — the full framework; the worked case's "communicate" step maps to its Govern function.
2. **CISA Known Exploited Vulnerabilities catalog** (cisa.gov/known-exploited-vulnerabilities-catalog) — free; evidence for likelihood ratings ("this vulnerability class is being exploited in the wild right now").
3. **OWASP Risk Rating Methodology** (owasp.org) — free; an alternative likelihood/impact factor breakdown, useful when SP 800-30's scales feel too coarse.

## 8. Check yourself

1. Explain the difference between a threat, a vulnerability, and a risk — then classify "an unpatched internet-facing VPN" and say what is missing before it becomes a risk statement.
2. Two assessors rate the same scenario "Possible × Major" and "Likely × Moderate." Explain why the correct resolution is a conversation about evidence, not averaging the cells — and what evidence would settle it.
3. A risk is rated Medium and the response chosen is "accept." Name the three things that must be recorded for that acceptance to be real rather than abandonment.
4. For the credential-stuffing risk in the worked case, explain why the plan includes detective controls in addition to preventive ones — what failure mode does detection cover that prevention does not?
5. Predict what happens to the Beacon register over two years if the "maintain" step is skipped: which entries decay first, and what kind of incident is most likely to reveal the decay?

## 9. Prove it

**Artifact:** your risk register (scope paragraph, scales, threat × vulnerability rows with justified ratings, responses with owners and dates, monitoring plan) plus the one-page executive report — for the worked case (reproduced in your own words) or, better, for the "On your own" system.

**Honest claim:** "I can conduct a qualitative risk assessment end to end — scope, rate with reasons, assign responses with owners, and report decisions to leadership."
**Can't claim yet:** "I can quantify risk in financial terms" — quantitative analysis (ALE, Monte Carlo) is a separate discipline this lesson deliberately did not teach; nothing here converts to currency.

## 10. Leads to

- **E-GOV-01 — NIST Cybersecurity Framework 2.0** — the risk assessment feeds the Govern function and the Current-vs-Target profile.
- **E-D1-11 — Supply chain risk management** — the same method applied to vendors (SP 800-161).
- **E-LEAD — Running a security program** — the board memo: risk communication as a leadership skill.
- **E-D1-07 — Business continuity (BIA)** — impact analysis is the sibling discipline; the two share scales and stakeholders.
- Map refs: **CISSP 1.9** (this lesson); feeds **CISSP 1.3** (governance) and **1.7** (BIA) downstream.
