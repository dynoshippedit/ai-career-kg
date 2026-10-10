---
lesson_id: e-csf-20
slug: csf-20
stage: E
level: 3
prerequisites: [e-risk-assessment, e-governance]
roles: [grc-analyst]
map_refs: []
test_date: 2026-10-10
description: "NIST Cybersecurity Framework 2.0: outcomes not actions — the 6 Functions, 22 Categories, Current-vs-Target profiles, and Tiers, with a worked gap assessment. A free lesson in the security guidebook."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# NIST Cybersecurity Framework 2.0


**Map ref:** brief §5 "Governance frameworks"; GRC analyst path; feeds `e-iso27001`, `e-soc2`, `e-security-program`.

---

## 1. Where this shows up

Every security program eventually faces the same meeting: leadership asks "how secure are we, and what should we do next?" and the answer has to be structured, comparable, and honest. The NIST Cybersecurity Framework is the most widely used structure for that answer in the United States — it is the language in which gap assessments, roadmaps, and program charters get written. The GRC analyst lives inside it: scoping assessments against it, writing the Current and Target Profiles, and turning the gap between them into a funded plan. This lesson teaches the framework as a working tool, not a poster.

## 2. Before you start

- You can write a risk in the standard form — asset, threat, vulnerability, impact, likelihood (`e-risk-assessment`). The profiles below are risk statements wearing a framework's clothes.
- You understand who owns security decisions (`e-governance`). A Target Profile is a decision document; someone has to sign it.
- No tools. The work product is a document set: a Current-vs-Target profile sketch and a prioritized action plan. Bring the hard rule from the brief: no invented numbers — every maturity claim traces to named evidence.

## 3. How it works

**What it is.** The NIST Cybersecurity Framework (CSF) 2.0 is a voluntary framework for managing cybersecurity risk, published by NIST as CSWP 29 on February 26, 2024. "Voluntary" matters: nobody certifies you against it, and no regulator grades you with it — organizations adopt it because it gives risk conversations a shared structure. The framework states **outcomes** (what good looks like), not **actions** (how to get there). That distinction is the whole philosophy: two organizations can achieve the same outcome with completely different controls, and the CSF treats both as valid. It is a language for describing a program, not a checklist for building one.

**The three parts.** CSF 2.0 has three components that work together:

1. **The CSF Core** — the taxonomy itself: Functions, Categories, Subcategories. This is the vocabulary.
2. **Organizational Profiles** — a way to describe where you are and where you want to be, in the Core's vocabulary. The gap between them is your action plan.
3. **Tiers** — a way to characterize how rigorous your risk management practices are, as a communication aid.

**The Core: 6 Functions, 22 Categories, 106 Subcategories.** The hierarchy runs Function → Category → Subcategory, each level a more specific outcome. The six Functions, with **Govern** new in 2.0 and sitting at the center of the wheel:

- **Govern (GV)** — the organization's cybersecurity risk management strategy, expectations, and policy are established, communicated, and monitored. Governance is a function now, not an assumption — the framework's way of saying strategy is a first-class outcome. Why at the center: a strategy failure cascades into every other function — unfunded Identify, unstaffed Detect, untested Recover — so the framework puts the thing that breaks everything else where you can't skip it.
- **Identify (ID)** — understand what you have and what threatens it.
- **Protect (PR)** — safeguards to manage risk to systems and data.
- **Detect (DE)** — find cybersecurity events in time.
- **Respond (RS)** — act on detected events.
- **Recover (RC)** — restore capabilities impaired by an event.

The 22 Categories (short labels from the framework's own table):

| Function | Categories |
|---|---|
| Govern | Organizational Context (GV.OC) · Risk Management Strategy (GV.RM) · Roles, Responsibilities, and Authorities (GV.RR) · Policy (GV.PO) · Oversight (GV.OV) · Cybersecurity Supply Chain Risk Management (GV.SC) |
| Identify | Asset Management (ID.AM) · Risk Assessment (ID.RA) · Improvement (ID.IM) |
| Protect | Identity Management, Authentication, and Access Control (PR.AA) · Awareness and Training (PR.AT) · Data Security (PR.DS) · Platform Security (PR.PS) · Technology Infrastructure Resilience (PR.IR) |
| Detect | Continuous Monitoring (DE.CM) · Adverse Event Analysis (DE.AE) |
| Respond | Incident Management (RS.MA) · Incident Analysis (RS.AN) · Incident Response Reporting and Communication (RS.CO) · Incident Mitigation (RS.MI) |
| Recover | Incident Recovery Plan Execution (RC.RP) · Incident Recovery Communication (RC.CO) |

Each Category divides into Subcategories — 106 in total — each stating one specific outcome (for example, under Organizational Context: the organizational mission is understood and informs cybersecurity risk management). Around the Core sit two supporting layers: **Informative References**, which map each Subcategory to controls in other standards (this is how the CSF talks to ISO 27001 and SP 800-53 without duplicating them), and **Implementation Examples**, which illustrate — not prescribe — how an outcome might be achieved.

**Profiles: Current vs Target.** An Organizational Profile is a selection of Core outcomes that matter to *this* organization, with a statement of where it stands on each. The method: build the **Current Profile** (where we are, evidenced), build the **Target Profile** (where we need to be, decided), and the gap between them becomes the action plan — prioritized by risk, cost, and impact. Community Profiles extend the idea to groups with shared priorities (a sector, a supply chain). The profile is the framework's unit of work: everything else is vocabulary for writing profiles well.

**Tiers: Partial, Risk Informed, Repeatable, Adaptive.** The four Tiers (Tier 1 Partial through Tier 4 Adaptive) describe the rigor of an organization's risk management practices — how aware, organized, and adaptive its approach is. They are a **communication aid**, not a grade. The failure mode is treating Tier 4 as the goal everywhere: a Tier 2 practice can be the right, risk-informed answer for a low-criticality outcome, and saying so honestly is better governance than inflating every Tier.

**What it is not.** There is no such thing as "CSF certified." Any vendor or assessor selling CSF certification is selling something NIST does not offer. And the Core is not a control catalog — if you need prescriptive controls, the Informative References point you to the standards that have them.

## 4. Walkthrough

No CLI by design — the walkthrough is the worked case, authored and self-reviewed 2026-10-10 against the primary document (CSWP 29, fetched in-session; category table verified against the document's own Table 1). The fictional company is **Meridian Analytics**, a 180-person SaaS analytics firm used across this guidebook's governance lessons. Every fact about Meridian below is invented and labeled.

**Step 1 — Frame the engagement.** Meridian's leadership wants a gap assessment: "tell us where we stand and what to do first." Scope: the production SaaS platform and the corporate IT that supports it. Out of scope: the office physical plant (covered under a separate facilities review). Timebox: two weeks. Decision-maker for the Target Profile: the CTO, with the board's risk committee (the board subcommittee that oversees risk) informed.

**Step 2 — Draft the Current Profile (representative slice).** For each Function, assess one Category honestly against named evidence. Six rows worked in full; the remaining sixteen Categories get the same treatment in the reader's own pass (see "On your own").

| # | Category | Current state (evidenced) | Target | Gap → action |
|---|---|---|---|---|
| 1 | GV.OC Organizational Context | Partial: mission statement exists; no written statement of which data types matter most. Evidence: company wiki, 2026-03. | Risk-informed: data classification scheme (`e-asset-classification`) published and referenced in the security policy. | Action A1: draft classification scheme; owner: GRC analyst; due Q1. |
| 2 | ID.AM Asset Management | Risk-informed: CMDB covers production; ~15% of SaaS-tool accounts unowned. Evidence: CMDB export 2026-09, IAM review. | Repeatable: quarterly access reviews with named owners for every asset class. | Action A2: assign owners to orphaned accounts; owner: IAM lead; due Q1. |
| 3 | PR.AA Identity Mgmt, Auth, Access Control | Repeatable: SSO + MFA enforced for staff; service accounts exempt with documented exceptions. Evidence: IdP policy export. | Repeatable (hold): close the service-account exceptions or accept the risk in writing. | Action A3: CTO risk-acceptance memo or remediation plan; due Q1. |
| 4 | DE.CM Continuous Monitoring | Partial: central logging exists; no alerting on authentication anomalies. Evidence: SIEM config review. | Risk-informed: alerting on impossible-travel + brute-force patterns (the `c-soc-triage` patterns). | Action A4: deploy two detections; owner: detection engineer; due Q2. |
| 5 | RS.MA Incident Management | Risk-informed: IR plan exists (SP 800-61 structure); never table-topped. Evidence: plan doc v1.2, 2025-11. | Repeatable: annual tabletop with findings tracked. | Action A5: run tabletop; owner: IR lead; due Q2. |
| 6 | RC.RP Incident Recovery Plan Execution | Partial: backups run nightly; restore never tested end-to-end. Evidence: backup job logs. | Risk-informed: tested restore meeting the RPO in `e-bcp-drp` terms. | Action A6: full restore test; owner: platform lead; due Q2. |

**Step 3 — Characterize Tiers (honestly).** Meridian's risk management practices: risk-informed (Tier 2) overall — risks are discussed and inform decisions, but the approach is not yet organization-wide and repeatable. Two Categories (PR.AA, RS.MA) show repeatable practices; the rest are Tier 1–2. The assessment says so plainly instead of averaging upward.

**Step 4 — Prioritize the action plan.** Order by risk reduction per effort: A4 (detection gap on the authentication path — highest), A2 (unowned accounts), A1 (classification unlocks everything downstream), A3 (decision, not work — cheapest), A5, A6. Each action names an owner and a due quarter. Nothing in the plan requires a tool Meridian doesn't have.

**Step 5 — Self-review.** Checklist, all true before this ships: every Current claim cites named evidence (not "we think"); every Target is a decision someone signed, not a wish; no Category claims a Tier above its evidence; the plan's order is argued from risk, not from ease; the words "certified" and "compliant" appear nowhere.

## 5. On your own

Complete the Current Profile for the remaining sixteen Categories of Meridian Analytics, using the same four columns (current + evidence, target, gap → action). Success test: a reviewer who has never met you can trace any row from its Current claim to the named evidence, and can tell which Target decisions are signed and which are still open. Then write the one-paragraph Tier rationale you would put in front of the CTO — and notice how hard it is to be honest about Tier 1s.

## 6. Where it goes wrong

- **The checklist fallacy.** Treating 106 Subcategories as 106 boxes to tick. The framework states outcomes; two organizations can satisfy the same Subcategory with entirely different controls. If your assessment reads like an audit of a fixed control list, you are using the wrong tool — use the Informative References to find the control catalog you actually need.
- **Tier inflation.** Rating everything Tier 3 because Tier 2 feels embarrassing. Tiers describe rigor, and rigor should follow risk: a Tier 2 practice guarding a low-criticality outcome is good governance, honestly stated.
- **"CSF certified."** There is no such certification. If a vendor claims it, that claim itself is a finding about the vendor.
- **Shelfware profiles.** A Current Profile built from interviews with no evidence, or a Target Profile nobody signed. The profile is a decision document; an unsigned target is a wish list.
- **Govern as decoration.** Adding GV rows to the spreadsheet while strategy is still decided by whoever shouts loudest. Govern is at the center of the wheel because the framework considers strategy load-bearing — if GV.OC and GV.RM are Tier 1, say so and fix them first.

## 7. Read the source

Primary documents first — read in this order, then the free resources:

1. **CSF 2.0 itself (CSWP 29, Feb 26 2024)** — read §§1–3 (the framework's own explanation of Core, Profiles, Tiers), skim the appendices. Free PDF from NIST.
2. **NIST's CSF 2.0 Quick-Start Guides page** — *start here if the PDF feels heavy*: the Organizational Profiles guide and the Tiers guide are the fastest on-ramps to the method this lesson teaches. Free.
3. **NIST SP 800-30 Rev. 1, Guide for Conducting Risk Assessments** — *read* for the risk assessment method that sits behind every honest Current Profile; the CSF tells you what outcomes to describe, SP 800-30 tells you how to assess the risk. Free.

## 8. Check yourself

1. The CSF states outcomes, not actions. Explain what breaks — concretely, in an assessment — if an assessor treats a Subcategory as a prescriptive control requirement.
2. Meridian's DE.CM row says "Partial" with evidence "SIEM config review." A manager asks you to rate it "Risk-informed" because "we have a SIEM." What do you say, and what evidence would change your answer?
3. Why does the framework put Govern at the center instead of treating governance as one row among many? Give the mechanism: what fails downstream when GV.RM is Tier 1?
4. An Informative Reference maps a Subcategory to an ISO 27001 control. Does satisfying the ISO control automatically satisfy the Subcategory? Explain the direction of the mapping.
5. Two organizations both claim Tier 3 for RS.MA. One ran a tabletop last quarter with tracked findings; the other has a plan document dated three years ago. What does the Tier claim actually tell you, and what question do you ask next?

## 9. Prove it

The artifact: a Current-vs-Target profile sketch (all 22 Categories, evidence per row) plus a prioritized action plan with named owners, for a fictional organization you define. Publish it as a document a stranger can follow — every Current claim traceable to named (fictional, labeled) evidence, every Target a signed decision.

After this lesson you can honestly claim: you can scope a CSF 2.0 gap assessment, write Current and Target Profiles, and turn the gap into a risk-ordered plan. You cannot yet claim: any certification (none exists), or that a profile you wrote describes a real organization — the first real one happens on a real engagement.

## 10. Leads to

- `e-iso27001` — the certifiable management system organizations pair with the CSF's outcomes language.
- `e-soc2` — the attestation report customers ask for, and how its criteria differ from a framework.
- `e-security-program` — the Govern loop running continuously: strategy, metrics, and the charter.
- GRC analyst path: this lesson is the assessment method the path's checkpoints assume.
