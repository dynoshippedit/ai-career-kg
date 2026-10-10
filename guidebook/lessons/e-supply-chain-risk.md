---
lesson_id: e-supply-chain-risk
slug: supply-chain-risk
stage: E
level: 3
prerequisites: [e-risk-assessment, ai-supply-chain]
roles: []
map_refs: ["CISSP 1.11"]
test_date: 2026-10-10
description: "Complete a vendor risk assessment ending in a residual-risk decision with owner and date. A free lesson in the security guidebook, serving CISSP objective 1.11."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Supply chain risk management: trusting what you didn't build


**Map ref:** serves **CISSP objective 1.11** — supply chain risk management.

---

## 1. Where this shows up

Modern systems are mostly other people's code, running on other people's infrastructure, maintained by people you will never meet. The application you deploy pulls hundreds of open-source packages; the SaaS you buy processes your customers' data on hardware you will never see; the vendor you onboarded last quarter has its own vendors, who have theirs. Supply chain risk management (C-SCRM) is the discipline of treating that dependency web as an attack surface: the compromise that matters may not be of *your* systems at all, but of a supplier whose access, code, or outage becomes yours. It shows up in the vendor security questionnaire, in the SBOM you requested and nobody read, in the acquisition where "we'll review their security later" became never, and in the incident whose root cause was a library three layers down the dependency tree. This lesson teaches the assessment: how to evaluate a supplier before you depend on them, and how to stay honest about the residual risk after.

## 2. Before you start

- You can run a risk assessment from `e-risk-assessment` — a vendor assessment is that method with the threat actor replaced by "the supplier's security posture" and the asset replaced by "everything they can touch."
- You have the AI supply-chain material from `ai-supply-chain` — models and training data are suppliers too, and this lesson's method applies to them.
- Bring a real or realistic acquisition: a SaaS product, a library, a managed-service contract. The worked case assesses a SaaS purchase; yours can differ.
- The work product is a vendor risk assessment ending in a decision: accept (with owner and date), mitigate, or walk away.

## 3. How it works

**The problem, stated plainly.** Every supplier relationship extends your trust boundary to an organization you do not control. The supplier's vulnerabilities become your vulnerabilities (their breach exposes your data), their outages become your outages (their downtime is your downtime), and their suppliers — the *fourth parties* — become risks you cannot even see. NIST SP 800-161 Rev. 1, *Cybersecurity Supply Chain Risk Management Practices for Systems and Organizations* (May 2022 — the primary source for this lesson, fetched in-session; note on currency: the revision was withdrawn from its old nvlpubs URL in November 2024 and the same Rev. 1 is the current edition on csrc.nist.gov) treats C-SCRM as enterprise risk management, not procurement paperwork: supply chain risk is managed across three levels — enterprise, mission/business process, and operational — with acquisition as one of the critical success factors.

**What you are assessing.** A supplier assessment examines the risk factors of *depending on this supplier for this purpose*:

- **Access:** what the supplier can touch — data, systems, network. A billing platform holding customer records is a different risk than a survey tool holding anonymous responses. Scope to the access, not the marketing.
- **Criticality:** what breaks if the supplier fails — compromised, breached, or simply gone? The dependency that halts dispatch (for Copperline Freight) or exposes patient data (for Harbor Clinic) gets the deep assessment; the office snack-delivery app does not. Criticality sets the assessment's depth.
- **Security posture evidence:** what the supplier can *show*, not claim — independent attestations (SOC 2 Type II reports, ISO 27001 certificates), penetration-test summaries, vulnerability-disclosure programs, incident history. A questionnaire answered by the vendor's sales team is a claim; an auditor's report is evidence. The difference is authorship and liability: the questionnaire is self-graded by the party that benefits from a good score; the auditor's report is produced by an independent party whose professional standing depends on its accuracy. Both have uses; never confuse them.
- **Fourth parties:** who the supplier depends on — their cloud provider, their subprocessors (a subprocessor is a vendor's vendor — a third party the supplier uses to handle your data), their own vendors. You will not get the full graph; you assess whether the supplier *manages* it (their subprocessor list, their notification obligations to you).
- **Concentration and exit:** what happens if you must leave — data export formats, contract termination terms, migration cost. An assessment that ignores exit has assessed only the honeymoon.
- **Provenance and integrity:** for software — where the code came from, how it was built, whether you can verify it. The SBOM's job (below).

**The SBOM.** A Software Bill of Materials is the ingredient list for software: components, versions, suppliers, relationships. CISA's SBOM resources (fetched for this lesson) describe the use: you cannot assess what you cannot enumerate. The honest practitioner's position: an SBOM you never read is compliance theater; an SBOM fed into vulnerability monitoring (which components have known CVEs, which suppliers have incidents) is an assessment input. Request the SBOM in the contract, define the format, and name who reads it and on what cadence — otherwise it arrives as a PDF nobody opens.

**Mitigations, in the contract.** Assessment without contractual teeth is advice the supplier can ignore. The mitigations that matter are written into the agreement: minimum security requirements (referenced, not reinvented — point at the frameworks), the right to assess/audit, breach-notification obligations *to you* with timelines, subprocessor-change notification, data-return and deletion on termination, and the SBOM delivery clause. Legal drafts it; security specifies what it must contain — which is why `e-cyber-law`'s obligation-to-evidence method and this lesson are siblings.

**The residual-risk decision.** No supplier is risk-free; the assessment ends in a decision with the same discipline as `e-risk-assessment`: accept the residual risk (named owner, review date), mitigate further (named actions, dates), or decline the acquisition. "Approved with concerns" without an owner and a date is abandonment wearing a signature. High-criticality suppliers get reassessment on a cadence and on trigger events (breach, acquisition, major architecture change) — the assessment is a living file, not a snapshot.

**C-SCRM as a program.** Beyond single assessments, SP 800-161's program view: supply chain risk belongs in the enterprise risk register, the acquisition process includes C-SCRM by default (not as an exception path), information about supplier risk is shared internally, and the workforce is trained on supply chain risk. The single assessment teaches the judgment; the program makes it repeatable.

**The AI angle.** Per the ISC2 exam guidance's Domain 1 mapping, AI supply-chain and third-party risk is in scope: training datasets, pre-trained models, and model weights are supply-chain components with provenance, integrity, and fourth-party questions of their own. Your `ai-supply-chain` lesson goes deep; this lesson's method — access, criticality, evidence, fourth parties, exit, provenance — applies to a model vendor unchanged.

### Worked example: Harbor Clinic — SaaS billing platform assessment (fictional)

**The acquisition (fictional).** Harbor Clinic (fictional, continued) is buying a cloud billing platform: it will hold patient names, contact details, and payment tokens; it integrates with the EHR (electronic health record — the clinic's patient-record system) via API; the vendor is a 40-person SaaS company, SOC 2 Type II attested, hosted on a major cloud provider.

**Risk factors identified:**

1. **Access (high):** the platform holds patient contact data and payment tokens, and its API integration can read appointment records. A breach of the vendor is a breach of the clinic's patients — notification obligations (`e-cyber-law`) trigger regardless of whose infrastructure failed.
2. **Criticality (high):** billing halts without it; no manual fallback exists beyond paper invoices. Outage equals revenue stop.
3. **Posture evidence (medium):** SOC 2 Type II report provided (read it — the auditor's exceptions section, not the marketing summary); no published vulnerability-disclosure program; incident history: one 2024 incident disclosed, handled adequately per the report.
4. **Fourth parties (medium):** hosted on a major cloud provider (subprocessor listed); payment processing via a PCI-assessed processor (assessed against PCI DSS, the payment-card industry's security standard; evidence requested, not yet received); the vendor's own subprocessor list exists but change-notification is not contractual.
5. **Exit (high risk):** data export is CSV-only, no API bulk export; contract auto-renews with 90-day termination notice; no contractual data-deletion attestation. Leaving would be painful — which is exactly when you negotiate exit, before signing.
6. **Provenance (low for SaaS, noted):** SBOM not applicable to the service directly, but requested for the vendor's client-side integration library.

**Mitigations (contractual and operational):**

- Minimum requirements clause referencing the clinic's standard; right-to-assess annually.
- Breach notification to the clinic within 48 hours of the vendor's awareness (tighter than the clinic's own regulatory clock, preserving response time).
- Subprocessor-change notification 30 days in advance, with the clinic's right to object.
- Data return in a documented format and deletion attestation on termination; export API evaluated before signing.
- The API integration scoped to least privilege (billing data only — not the full appointment record); integration credentials rotated on the clinic's schedule.
- Vendor reassessment annually and on trigger events.

**Residual-risk decision:** *conditionally accept* — owner: the clinic's operations director; review date: 12 months or on trigger. Accepted risks named explicitly: the vendor's small security team (mitigated by the attestation and the notification clause), the CSV-only export (mitigated by a quarterly export test proving the data is actually retrievable). Declined alternative: a larger vendor with stronger posture but no healthcare references — the assessment judged domain fit as the greater risk reducer. Every accepted risk has the owner and the date. That is the difference between a decision and a hope.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the assessment above, authored and self-reviewed in-session on 2026-10-10 against NIST SP 800-161 Rev. 1's structure. Transcript: `runs/e-supply-chain-risk.log` (records the risk factors, the mitigations, the decision, and the review checklist — no commands to transcribe).

1. **Scope the acquisition.** What the supplier will touch (data, systems, network) and what breaks if they fail. Write the criticality first — it sets the assessment's depth. Low-criticality acquisitions get the light version; say so explicitly.
2. **Gather posture evidence.** Request the attestations, the pen-test summary, the incident history, the subprocessor list. Read the auditor's exceptions, not the sales deck. Record what was requested but not received — gaps are findings.
3. **Assess the six factors.** Access, criticality, posture evidence, fourth parties, exit, provenance. One paragraph each, with a rating and a reason. Ratings without reasons are opinions.
4. **Write the mitigations.** Contractual (clauses) and operational (integration scoping, monitoring). Name who negotiates each clause — security specifies, legal drafts.
5. **Decide.** Accept (owner, date), mitigate further (actions, dates), or decline. Name the accepted residual risks explicitly — the decision document lists what you are living with.
6. **File and schedule.** The assessment is a living file: reassessment cadence and trigger events recorded. Put the review date in the calendar.

## 5. On your own

**Task:** Assess a real acquisition — a SaaS product you use, an open-source library you depend on, or a vendor your organization is considering. Run all six factors, request at least one piece of evidence you have never asked for (the SOC 2 report, the SBOM, the subprocessor list), and end in a decision with owner and date.

**Success test:** Your assessment contains at least one requested-but-not-received evidence item (recorded as a gap, not ignored), at least one contractual mitigation, and an explicit exit analysis. If every factor rated "low," the acquisition was too trivial to teach on — pick a bigger one.

## 6. Where it goes wrong

- **Questionnaire theater.** The vendor's self-attestation filed as an assessment. Questionnaires have a place (scoping, low-criticality); they are not evidence. The tell: the vendor file contains only the self-attested questionnaire — no independent evidence requested or received.
- **Assessing the vendor, not the access.** A thorough review of a vendor's corporate security that never asks what *this* deployment can touch. Scope to the access.
- **Fourth-party blindness.** The assessment stops at the vendor's front door. Their subprocessors, their cloud, their libraries — the risk graph continues past the contract signature.
- **The unread SBOM.** Requested, delivered, never opened. An SBOM needs a reader, a format, and a cadence — or it is theater.
- **No exit analysis.** The assessment covers the honeymoon. Negotiate exit before signing, when you still have leverage.
- **"We'll review later."** The acquisition closes, the assessment never happens. C-SCRM in the acquisition process by default — `e-governance`'s rule: the process must not depend on someone remembering.
- **Approved with concerns.** The decision document lists worries with no owner and no date. Concerns without ownership are abandonment with a signature.
- **Snapshot assessments.** Assessed once at purchase, never again. Breaches, acquisitions, and architecture changes are trigger events — record them in advance. The tell: the vendor file's last update predates the vendor's acquisition — the trigger event happened, the file didn't notice.

## 7. Read the source

Primary documents first:

- **NIST SP 800-161 Rev. 1, Cybersecurity Supply Chain Risk Management Practices for Systems and Organizations** (May 2022; csrc.nist.gov) — *read* the enterprise-risk framing and the acquisition guidance; *note* the publication's relocation honestly (withdrawn from the old nvlpubs URL November 2024; same Rev. 1 current on csrc). The C-SCRM canon.

Then at most three free resources:

1. **CISA ICT Supply Chain Risk Management** (cisa.gov) — free; the operational companion — tasks, resources, and the ICT SCRM task-force material for putting the SP 800-161 practices to work.
2. **CISA SBOM resources** (cisa.gov) — free; what an SBOM is, minimum elements, and how to consume one — the provenance input to your assessments.

## 8. Check yourself

1. A vendor provides a completed security questionnaire and a SOC 2 Type II report with two auditor exceptions. Explain which is evidence and which is a claim — and what you do about the exceptions.
2. A SaaS purchase holds customer personal data and integrates via API with read access to the full customer database. Scope the assessment: what access question must be answered before any other factor, and what mitigation follows from it?
3. Distinguish fourth-party risk from vendor risk using a concrete chain: your vendor's cloud provider suffers an outage. Which of your assessment's mitigations fires, and which gap does the incident reveal if none does?
4. A vendor's contract auto-renews with 90-day termination, CSV-only export, and no deletion attestation. Name the exit risks and the three contractual mitigations you negotiate before signing.
5. Predict the state of a vendor file three years after purchase with no reassessment cadence: which factor decays fastest, and what trigger event the file should have named in advance?

## 9. Prove it

**Artifact:** your vendor risk assessment (scope and criticality, the six factors with ratings and reasons, evidence requested and received, contractual and operational mitigations, the residual-risk decision with owner and date, reassessment cadence and triggers) — for the Harbor Clinic case in your own words, or better, for a real acquisition.

**Honest claim:** "I can assess a supplier before depending on them — access, criticality, evidence, fourth parties, exit, provenance — negotiate the mitigations into the relationship, and drive the residual risk to a decision with an owner and a date."
**Can't claim yet:** "I can run an enterprise C-SCRM program" — multi-tier supplier governance, continuous monitoring at scale, and sector-wide information sharing are their own practice; this lesson taught the assessment, which is where the judgment is formed.

## 10. Leads to

- **ai-supply-chain — `ai-supply-chain`** — the AI variant: models, datasets, and weights as supply-chain components.
- `e-cyber-law` — the contractual sibling: obligations to evidence, and what the clauses must contain.
- `e-governance` — the program home: C-SCRM in the acquisition process by default.
- Map refs: **CISSP 1.11** (this lesson); feeds **CISSP 8.4** (security of acquired software).
