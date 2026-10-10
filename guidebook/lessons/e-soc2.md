# SOC 2 and the Trust Services Criteria

**ID:** `e-soc2` · **Stage:** E (Expert) · **Level:** 3 (scope a SOC 2 engagement and read the resulting report like a customer would) · **Prerequisites:** `e-csf-20` (frameworks state outcomes; this is the examination that tests them); `e-iso27001` (control selection — the auditor will test whether your selections operate). No command line in this lesson.

**Map ref:** brief §5 "Governance frameworks"; GRC analyst path; feeds `e-security-audits`, `e-cyber-law`.

---

## 1. Where this shows up

A prospective enterprise customer sends your company a security questionnaire, and question 40 reads: "Provide your most recent SOC 2 Type II report." If you have one, the sales cycle shortens by months; if you don't, you answer 300 questions by hand. SOC 2 is the mechanism by which a service organization *proves* its controls to customers who will never visit its data centers: an independent CPA examines the controls against the AICPA's Trust Services Criteria and writes an attestation report. The GRC analyst lives on both sides of this — preparing the organization for the examination, and reading vendors' reports during procurement. This lesson teaches what the report is, what it is not, and how to scope the engagement.

## 2. Before you start

- You understand control selection (`e-iso27001`). SOC 2 tests whether selected controls are designed well and operate effectively — it does not select them for you.
- You can read a framework outcome (`e-csf-20`). The Trust Services Criteria play a similar role: criteria, not controls.
- No tools. The work product is a scoping memo: which criteria, which systems, Type I or Type II, and why — written as if to the CFO who approves the engagement. Bring the brief's honesty rule: an attestation report is evidence, not a guarantee.

## 3. How it works

**What SOC 2 is.** SOC 2 is an **examination engagement**: an independent Certified Public Accountant examines a service organization's system and its controls against the AICPA's **Trust Services Criteria**, and issues a report with an opinion. Three load-bearing distinctions:

1. **It is an attestation report, not a certificate.** There is no "SOC 2 certified." The deliverable is a report containing management's description of the system, the auditor's opinion, and (in Type II) test descriptions and results. Anyone selling "SOC 2 certification" is mislabeling the product.
2. **There is no pass/fail.** The opinion addresses whether controls were suitably designed (Type I) and operated effectively (Type II) to meet the criteria. A report can contain qualified opinions and described exceptions — and a careful reader learns more from the exceptions than from a clean opinion.
3. **It is performed by a CPA under attestation standards.** Not by an IT consultant, not by the vendor itself. The independence of the examiner is part of what the report is worth.

**The five Trust Services Criteria.** The criteria are the yardstick — control *objectives*, not a control list. The current edition is the **2017 Trust Services Criteria, with revised points of focus issued in 2022** (the full criteria document is available from the AICPA with a free account):

- **Security** — protection against unauthorized access. This is the mandatory one: every SOC 2 engagement includes the Security criterion (the "common criteria"). The other four are optional, selected by what the organization commits to.
- **Availability** — the system is available as committed (think SLAs).
- **Processing Integrity** — processing is complete, valid, accurate, timely, and authorized (think: the analytics outputs customers make decisions on).
- **Confidentiality** — confidential information is protected as committed (think NDAs, customer data handling commitments).
- **Privacy** — personal information is collected, used, retained, disclosed, and disposed of as committed (think privacy notices and data-subject commitments).

The scoping logic: Security always; each additional criterion is included when the organization makes *commitments* in that area — in contracts, SLAs, privacy notices. The criteria follow the promises.

**Type I vs Type II.** The oldest confusion in the field, stated once clearly:

- **Type I** reports on the fairness of management's system description and the **suitability of the control design** *as of a specified date*. It answers: "were the controls well-designed on that day?" It says nothing about whether they operated afterward.
- **Type II** adds the auditor's opinion on **operating effectiveness** *throughout a specified period*, with a description of the tests performed and their results. It answers: "did the controls actually work, for months, as tested?"

A Type I is a design review; a Type II is evidence of operation. Customers who understand the difference ask for Type II.

**Who asks for it and why.** Customers and business partners request SOC 2 reports to support *their* risk assessments of a service organization — vendor risk management, in the GRC vocabulary. The report is **restricted-use**: intended for the service organization's stakeholders who understand the system, not for the general public. (SOC 3 is the general-use sibling — a short seal-style report for public consumption, covering the same criteria.)

**The SOC family, kept straight.** The AICPA's testimony before the ERISA Advisory Council — the primary source for this section — lays the suite out plainly: **SOC 1** reports on controls relevant to user entities' *internal control over financial reporting* (the auditors' world); **SOC 2** reports on controls against the Trust Services Criteria (the security/availability/integrity/confidentiality/privacy world); **SOC for Cybersecurity** examines an *entity's own* cybersecurity risk management program. SOC 1 answers the CFO's auditor; SOC 2 answers the customer's CISO; confusing the two is the classic procurement error.

## 4. Walkthrough

No CLI by design — the walkthrough is the worked case, authored and self-reviewed 2026-10-10 against the primary sources (AICPA's Trust Services Criteria resource page and the AICPA's 2022 testimony, both fetched in-session). The fictional company is **Meridian Analytics** (180-person SaaS analytics firm). Every fact about Meridian is invented and labeled.

**Step 1 — Inventory the commitments.** Before choosing criteria, list what Meridian has *promised*, because criteria follow commitments:

| Commitment (fictional, labeled) | Source | Implicates |
|---|---|---|
| "99.9% monthly uptime" | Enterprise MSA §7 (fictional) | Availability |
| "Customer data encrypted at rest and in transit; access logged" | Security exhibit to the MSA (fictional) | Security, Confidentiality |
| "Analytics outputs validated against source on every run" | Product documentation (fictional) | Processing Integrity |
| "We process end-user personal data per our privacy notice; deletion on request within 30 days" | Privacy notice v3 (fictional) | Privacy, Confidentiality |

**Step 2 — Scope the criteria.** Security: mandatory, in scope. Availability: in scope — the 99.9% SLA is a written commitment. Processing Integrity: in scope — customers make decisions on the outputs. Confidentiality: in scope — the security exhibit promises it. Privacy: in scope — personal data plus a deletion commitment. All five: this is a full-scope engagement, and the memo says why each one earned its place.

**Step 3 — Define the system boundary.** In scope: the SaaS production platform, the data pipeline, corporate identity systems. Out of scope: the marketing website (no customer data); sub-processors are *carved out* with the complementary-subservice-organization-controls language — Meridian's report will state what it relies on its cloud provider for, explicitly. Boundary owner: CTO.

**Step 4 — Choose Type I vs Type II.** Meridian has never been examined. The memo recommends: Type I now (design review — finds the design gaps cheaply), Type II covering the following twelve months (the report customers actually want). Rationale stated plainly: a Type II over a period when controls were still being built would produce a report full of exceptions — honest but commercially useless. Sequence the work, don't fake the evidence.

**Step 5 — Draft the evidence list per criterion.** For each in-scope criterion, name the controls (from the `e-iso27001` SoA) and the evidence the auditor will ask for: Security → IdP policy exports, MFA enrollment reports, access-review records; Availability → uptime measurements vs the SLA, incident records; Processing Integrity → validation job logs, reconciliation reports; Confidentiality → encryption configs, NDA register; Privacy → deletion request log with 30-day evidence, data inventory. Every row names where the artifact lives.

**Step 6 — Self-review.** Checklist, all true before this ships: every criterion traces to a written commitment (no criterion included "to look thorough"); the boundary is explicit including carve-outs; the Type I→Type II sequencing is argued, not assumed; the words "certified" and "pass" appear nowhere; the memo states what the report will *not* prove (it is not a penetration test, not a guarantee).

## 5. On your own

Write the one-page "description of the system" outline the auditor will examine — the narrative of what Meridian's system is, its boundaries, and its commitments. Success test: a reader can draw the system boundary from your description alone, and every commitment in it appears in the scoping memo's criteria table. Then pick one criterion and write three control→evidence pairs an auditor could actually test.

## 6. Where it goes wrong

- **"SOC 2 certified."** The most common mislabel in the industry. There is an examination, an opinion, and a report. There is no certificate. Using the word in your own materials is a finding about you.
- **Type I sold as ongoing assurance.** A point-in-time design opinion waved at a customer asking "are your controls working?" It answers a different question than the one asked — say which question your report answers.
- **Scoping by ambition instead of commitment.** Including Privacy with no privacy commitments, or excluding Availability while the SLA promises 99.9%. Criteria follow promises; audit the promises first.
- **The clean-opinion reflex.** Treating exceptions in a Type II report as failures to hide. Exceptions with root causes and remediation are what a mature program looks like — the report a customer trusts is the honest one, not the blank one.
- **SOC 1 vs SOC 2 confusion.** Handing a customer's CISO your SOC 1 (financial-reporting controls) when they asked about security. The testimony this lesson is built on exists partly because this error is endemic — know which report answers which question.

## 7. Read the source

1. **AICPA: 2017 Trust Services Criteria (With Revised Points of Focus — 2022)** — *read* the resource page for what the criteria are, who publishes them, and the edition currency; the full criteria document needs a free AICPA account. This is the yardstick everything in the lesson is measured against.
2. **AICPA testimony before the ERISA Advisory Council (July 18, 2022)** — *read* the SOC suite section: SOC 1 vs SOC 2 vs SOC for Cybersecurity, Type I vs Type II, who uses each report and why. An AICPA officer explaining the suite in plain language, on the public record.

## 8. Check yourself

1. Meridian's largest customer asks for "your SOC 2 certification." Draft the two-sentence correction you send back — accurate, not condescending — and name what you send instead.
2. The scoping memo includes Privacy because of the 30-day deletion commitment. Meridian's counsel now says the privacy notice never actually promised deletion timelines. What changes in the scope, and what does this reveal about the criteria-follow-commitments rule?
3. A vendor hands you a Type I report dated fourteen months ago. List everything it does and does not tell you about their controls *today*.
4. Meridian carves out its cloud sub-processor with complementary-controls language. A customer asks: "so who is responsible if the cloud provider is breached?" Give the answer the report's boundary language supports.
5. Two vendors: one with a clean Type II, one with a Type II containing three described exceptions with remediation. Which report do you trust more, and what specifically do you read next in each?

## 9. Prove it

The artifact: a SOC 2 scoping memo for a fictional service organization — commitments inventory, criteria selection with rationale per criterion, system boundary with carve-outs, Type I/II sequencing decision, and a per-criterion evidence list naming where each artifact lives. Written for the CFO who approves the engagement: business language, no jargon unexplained.

After this lesson you can honestly claim: you can scope a SOC 2 engagement and read a SOC 2 report the way a customer does — criteria against commitments, exceptions as information. You cannot yet claim: examination experience, auditor judgment, or that any fictional memo describes a real engagement.

## 10. Leads to

- `e-security-audits` — audit method: how the examiner tests what your memo scoped.
- `e-cyber-law` — the MSAs, DPAs, and privacy notices whose commitments drive the criteria.
- `e-board-communication` — reporting the examination plan and its results upward.
- GRC analyst path: this lesson is the vendor-risk reading skill the path's checkpoints assume.
