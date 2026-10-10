# Security policy, standards, procedures, and guidelines: the document hierarchy

**ID:** `e-policy-docs` · **Stage:** E (Expert) · **Level:** 3 (author a three-tier document set — policy, standard, procedure — for one control area, plus the guideline, with owners and review dates) · **Prerequisites:** `e-governance` (the charter that gives policy its authority). No command line in this lesson.

**Map ref:** serves **CISSP objective 1.6** — security policy, standards, procedures, and guidelines.

---

## 1. Where this shows up

Every organization runs on documents it may not have written down. The "policy" that lives in the CISO's head, the "standard" that is actually a Slack message from 2021, the "procedure" that one engineer knows and everyone else guesses at — this is how most security programs actually operate, and it is why they fail audits, fail handovers, and fail at 3 a.m. The document hierarchy is the fix: four tiers, each with a distinct job, written so that a stranger can reconstruct what the organization decided and why. It shows up in the audit that asks "show me the policy"; in the new hire who needs to know the rule without asking three people; in the incident where the responder follows the procedure instead of improvising; and in the exception request that turns silent non-compliance into a governed decision. This lesson teaches the hierarchy and makes you write it.

## 2. Before you start

- You have the governance charter from `e-governance` — policy authority, approval path, and the exception process. This lesson writes the documents that charter authorizes.
- Bring one control area you know well (encryption, access control, logging — anything with real technical content). The worked case uses encryption; yours can differ.
- The work product is a document set: one policy, one standard, one procedure, one guideline — each fitting its tier, none doing another tier's job.

## 3. How it works

**The four tiers.** Each tier answers a different question, at a different altitude, approved at a different level:

- **Policy — what and why.** Management's statement of intent: what the organization requires and why it matters. Short (a page or two), stable (changes rarely), approved at the top. A policy says "the organization protects information with encryption proportionate to its classification"; it does not name algorithms. Policies are few — an organization with forty "policies" has forty procedures wearing costumes.
- **Standard — how well, how much.** Mandatory requirements that implement the policy: the specific bar. "All data classified Confidential or above is encrypted with an approved algorithm" — the standard names the approved list, the key lengths, the minimums. Standards change when technology changes, and they are mandatory: deviation requires the exception process.
- **Procedure — who does what, in what order.** Step-by-step instructions for the people doing the work: request a certificate, generate the key, store it, rotate it. Procedures change often (tools change, teams change) and are owned close to the work. A procedure that nobody follows is not strict — it is fiction.
- **Guideline — what is recommended.** Advisory, not mandatory: recommended practice, preferred options, the "if you're unsure, do this" document. Guidelines inform judgment where the standard leaves room. The moment a guideline is treated as mandatory, it has become an unapproved standard — call it what it is or stop enforcing it.

**Traceability.** The tiers link downward: every standard traces to a policy ("this standard implements the Encryption Policy §2"); every procedure traces to a standard; guidelines reference the standards they elaborate. Traceability is what makes the set auditable — an auditor picks a procedure step and walks it up to the management intent, or picks a policy statement and walks it down to the evidence. A document that traces to nothing is an opinion with formatting.

**Ownership and lifecycle.** Every document has a named owner (a role, not "the security team"), an approval authority (matching the charter), a review date, and a version. Review cadence follows volatility: policies annually or on strategy change; standards on technology change; procedures whenever the work changes. The version history is evidence — "we have always done it this way" is not.

**The exception process.** The hierarchy's pressure valve, from `e-governance`: a documented path for deviating from a standard — requester, business justification, risk statement, approver, expiry date. Exceptions are how the organization learns: a recurring exception is a standard that needs rewriting, and the exception log is where that signal lives. No exception process means exceptions happen anyway, invisibly.

**Baselines.** A useful fifth concept, adjacent to standards: the **baseline** is the minimum secure configuration for a system type — the hardened image, the default settings. Baselines are standards applied to platforms; they are what `e-sdlc` and operations teams actually deploy. Know the term because auditors use it.

**Structure reference.** NIST SP 800-53 Rev. 5 organizes its controls into 20 families — Access Control, Awareness and Training, Audit and Accountability, Configuration Management, Contingency Planning, Identification and Authentication, Incident Response, Maintenance, Media Protection, Physical and Environmental Protection, Planning, Program Management, Personnel Security, PII Processing and Transparency, Risk Assessment, System and Services Acquisition, System and Communications Protection, System and Information Integrity, Supply Chain Risk Management, and Assessment/Authorization/Monitoring (family list verified on the csrc.nist.gov publication page, fetched in-session). The families are the catalog your standards point at: a standard does not reinvent access control — it selects from the catalog and sets the bar.

### Worked example: Harbor Clinic — the encryption document set (fictional)

**The control area (fictional).** Harbor Clinic (fictional, continued from `e-security-concepts`): 60 staff, patient portal, lab results. The set covers encryption of patient data.

**Policy — Information Protection Policy (one page, abridged).** *Purpose:* patient information is protected proportionate to its sensitivity, per the clinic's duty of care and its legal obligations. *Scope:* all workforce members, all systems handling patient data. *Statements:* (1) information is classified on creation; (2) protection measures follow classification; (3) encryption is required for patient data in transit and at rest; (4) the CISO owns the supporting standards; (5) exceptions follow the documented exception process. *Approved by:* the risk committee. *Review:* annually. Note what it does not contain: no algorithms, no key lengths, no steps. That restraint is the tier discipline.

**Standard — Encryption Standard (abridged).** *Implements:* Information Protection Policy §3. *Requirements:* (1) patient data in transit uses TLS 1.2 or later with an approved cipher suite list (maintained in the appendix); (2) patient data at rest uses an approved algorithm per the current `e-crypto-applied` baseline — the standard references the baseline document rather than embedding algorithm names, so the standard survives algorithm deprecation; (3) keys are generated, stored, and rotated per the Key Management Standard; (4) no ECB mode, no hard-coded keys, no keys in source repositories; (5) new systems are verified against this standard before production. *Deviation:* exception process only. *Review:* on baseline change or annually.

**Procedure — Requesting and rotating a data-encryption key (abridged).** *Implements:* Encryption Standard §3. Steps: (1) requester files a key request ticket with system name and data classification; (2) the key custodian generates the key in the approved key store (never on a workstation); (3) the custodian records the key ID, purpose, and rotation date in the key inventory; (4) the requester configures the application to reference the key ID — the key value is never copied into config files; (5) rotation occurs automatically at the interval in the Key Management Standard, or immediately on suspected compromise or staff departure with key access; (6) retired keys are archived per the retention schedule, then destroyed. Each step names the role that performs it. *Review:* whenever the key store or ticketing tool changes.

**Guideline — Choosing encryption options (abridged).** *Advisory.* When the standard offers a choice (e.g., between approved algorithms for a new system), prefer the option with the longest support lifetime and the simplest operational profile; for data with retention beyond five years, prefer algorithms with the widest independent review. If unsure, ask the CISO — the guideline names the escalation, because "use your judgment" without a backstop is abandonment.

**Traceability check:** procedure §5 (rotation on staff departure) traces to standard §3 (key management), which traces to policy §3 (encryption required). An auditor can walk it in either direction. That is the whole point.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the document set above, authored and self-reviewed in-session on 2026-10-10 against the four-tier model and the SP 800-53 family structure. Transcript: `runs/e-policy-docs.log` (records the tier discipline per document, the traceability check, and the review checklist — no commands to transcribe).

1. **Pick the control area.** One area you know technically — encryption, logging, access reviews, backup. Narrow beats comprehensive: one area done in four tiers teaches the discipline; five areas done shallowly teaches nothing.
2. **Write the policy first.** One page: purpose, scope, the what-and-why statements, owner, approver, review date. Then delete every technical detail that crept in — algorithms, ports, tool names. If it is longer than two pages, it is not a policy.
3. **Write the standard.** Mandatory requirements implementing the policy, with the traceability line ("implements Policy §N"). Reference external baselines (like `e-crypto-applied`) instead of embedding volatile details. Name the exception path.
4. **Write the procedure.** Steps, in order, with the role per step. Hand it to an imaginary new hire: can they execute it without asking anyone? If not, it is not a procedure yet.
5. **Write the guideline.** Advisory recommendations for the judgment calls the standard leaves open. Mark it advisory explicitly — and mean it.
6. **Run the traceability check.** Pick a procedure step, walk it up to the policy. Pick a policy statement, walk it down to the procedure. Every link must exist. Then date the next review for each document.

## 5. On your own

**Task:** Write the four-tier set for a control area in a system you actually run — your backup scheme, your homelab's access control, your password-manager usage. Real area, real steps, your name as owner.

**Success test:** The policy fits on one page with no technical details; the standard contains a requirement you can test (pass/fail); the procedure is executable by a stranger; the guideline is honestly advisory. And the traceability check passes in both directions — if it does not, the set is four documents, not a hierarchy.

## 6. Where it goes wrong

- **The forty-page policy.** Policies that contain standards, procedures, and guidelines in one document — unapprovable, unreadable, unmaintained. Tier discipline is the fix.
- **Procedures wearing policy costumes.** "Policies" that name tools and ports — they cannot be approved at the top (leadership cannot evaluate them) and they rot on every tool change.
- **Guidelines enforced as standards.** The advisory document treated as mandatory without going through approval. Either approve it as a standard or stop enforcing it.
- **No owner, no review date.** Documents that belong to "the team" and are reviewed "as needed" — which means never. Ownership and dates are load-bearing.
- **The missing exception process.** Deviations happen invisibly, the standard describes a fictional organization, and the audit finds the gap. The exception log is also the signal for rewriting bad standards.
- **Shelfware.** The set is written for the audit, filed, and never used. Test: ask three engineers where the procedure lives. Silence is the diagnosis.
- **Traceability theater.** "Implements Policy §2" written on a standard that contradicts §2. The check is substantive — read both directions.
- **Baselines confused with standards.** The hardened image treated as the requirement, so every platform exception becomes a standards violation. Baselines implement standards; they are not the standards.

## 7. Read the source

Primary documents first:

- **NIST SP 800-53 Rev. 5, Security and Privacy Controls** (csrc.nist.gov) — *read* the family structure (20 families) as the catalog your standards select from; *skim* one family's controls to see the control/enhancement pattern your standards mirror.

Then at most three free resources:

1. **SANS Information Security Policy Templates** (sans.org) — free; the template set — use as skeletons for tier discipline (policy vs standard vs procedure), not as finished documents. Fill them; do not file them.
2. **NIST CSF 2.0, Govern function (GV.OC)** (nvlpubs.nist.gov) — free; where policy lives in the framework — the organizational-context outcomes your policy tier answers to.

## 8. Check yourself

1. A "policy" document names specific cipher suites, key lengths, and the ticketing tool for key requests. Identify every tier violation, and state what belongs in which tier.
2. Explain traceability as an audit mechanism: walk a procedure step up to management intent, and a policy statement down to evidence — and state what breaks when a link is missing.
3. A team treats an advisory guideline as mandatory and disciplines an engineer for deviating. Name the governance failure and the two legitimate resolutions.
4. Distinguish a standard from a baseline using a concrete example: which changes when the organization switches key-management tools, and which does not?
5. Predict the state of a document set three years after its owner leaves, with no review dates ever set: which tier rots first, and what event reveals the rot?

## 9. Prove it

**Artifact:** your four-tier document set (policy, standard, procedure, guideline) for one control area — for the Harbor Clinic encryption case in your own words, or better, for a real system you run — with the traceability check documented and review dates set.

**Honest claim:** "I can write the document hierarchy for a control area — policy through guideline — with tier discipline, traceability in both directions, named owners, and review dates."
**Can't claim yet:** "I can run an organization's full policy program" — a complete policy library across all control families, with approval workflows and exception governance at scale, is its own practice; this lesson taught the discipline on one control area, which is where the judgment is formed.

## 10. Leads to

- `e-governance`** — the charter that authorizes policy: approval, ownership, exceptions.
- `e-awareness-training`** — the program that teaches the documents: policy is only real when people know it.
- `e-crypto-applied`** — the technical baseline the encryption standard references.
- Map refs: **CISSP 1.6** (this lesson); feeds **CISSP 1.3** (governance) and **7.3** (configuration management).
