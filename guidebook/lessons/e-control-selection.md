# Selecting controls: from requirements to a defensible set

**ID:** `e-control-selection` · **Stage:** E (Expert) · **Level:** 3 (derive requirements from a scenario, select and tailor controls with written rationale, and defend the omissions) · **Prerequisites:** `e-risk-assessment` (risk responses become requirements), `e-secure-design` (the traceability habit); no command line in this lesson.

**Map ref:** serves **CISSP objective 3.3** — selecting security controls from system security requirements: derivation, catalog selection, tailoring, and traceability.

---

## 1. Where this shows up

Every security program eventually faces the same audit question: "Why *these* controls?" A firewall here, encryption there, logging everywhere — each control costs money, attention, and operational friction, and "best practice" is not an answer that survives scrutiny. Control selection is the discipline of deriving controls from requirements instead of from habit: the system's stakeholders state what must be protected and against what, those statements become testable security requirements, and each requirement earns its controls — selected from a catalog, tailored to context, and traced so the whole chain can be re-derived by someone who wasn't in the room. It shows up in the System Security Plan that actually means something, in the authorization decision where someone signs that the residual risk is acceptable, and in the post-incident review that asks "which requirement did we think this control satisfied?" The catalog most of the industry uses is NIST SP 800-53 — not as a checklist, but as a vocabulary.

## 2. Before you start

- You can run a risk assessment to decisions (`e-risk-assessment`) — risk responses are the raw material of requirements.
- You know the traceability habit from `e-secure-design`: every control answers "which requirement do you satisfy?"
- No tools. The work product is a control-selection package: requirements, selected controls with rationale, tailoring decisions, and the explicitly defended omissions.

## 3. How it works

**Requirements first.** A security requirement is a testable statement about what the system must do or must prevent: "The system shall authenticate every user before granting access to customer data," not "the system shall be secure." Requirements come from four sources: **stakeholder needs** (the business's actual obligations — contracts, regulations, customer commitments), **threat analysis** (what the threat model says will be attempted), **risk decisions** (the responses chosen in the risk assessment — mitigate, transfer, accept, avoid), and **design principles** (the `e-secure-design` review's numbered requirements). A requirement that can't be tested — "adequate logging" — is a wish; rewrite it until a tester could confirm or falsify it.

**The catalog.** NIST SP 800-53 Rev. 5 organizes controls into twenty families (Access Control, Audit and Accountability, Configuration Management, Identification and Authentication, Incident Response, System and Communications Protection, and fourteen more), each control with a number, a statement, and supplemental guidance. The catalog's value is coverage and shared language: when you select AC-2 (account management), everyone in the profession knows what you mean. The catalog's danger is completeness-as-virtue: applying all of it to a small system is how you get a security program that costs more than the system it protects. Selection is always requirement-driven and risk-proportionate.

**Baselines and tailoring.** SP 800-53 defines three baselines — low, moderate, high — as starting sets keyed to the system's impact level (from FIPS 199 categorization: what happens if confidentiality, integrity, or availability is lost). The baseline is a starting point, not an answer. **Tailoring** then adjusts it, and tailoring has a formal vocabulary: *scoping* (removing controls that don't apply — a control about wireless access on a system with no wireless), *parameterization* (filling in the assignment and selection statements — "review accounts every [assignment: organization-defined frequency]" becomes "every 90 days"), *supplementing* (adding controls or enhancements the baseline missed for your threats), and *compensating* (documenting an alternative when the prescribed control is infeasible). Every tailoring decision is written down with rationale — including the controls you *didn't* select, because the auditor will ask about those first.

**Traceability and the security plan.** The selection is recorded in a **traceability matrix**: requirement → control(s) → implementation → test/verification method. This matrix is the load-bearing structure of the System Security Plan: it lets a reviewer start from any stakeholder need and walk to the mechanism, or start from any mechanism and walk back to the need it serves. An untraced control is unjustified cost; an unimplemented requirement is an unkept promise. The matrix is also what makes the selection *maintainable* — when requirements change, you know exactly which controls to revisit.

**Control types and the coverage argument.** A defensible set covers the requirement from multiple angles: **preventive** (stop it), **detective** (see it), **corrective** (fix it), and the supporting **administrative/technical/physical** mix. The coverage argument for each requirement names which types are present and why the mix is sufficient — a requirement protected only by a preventive control with no detection is a requirement whose failure you will discover from the newspaper.

**The authorization shadow.** In formal environments this package supports an **authorization decision**: a designated official reviews the selection, the implementation evidence, and the residual risk, then signs. Even where no formal authorization exists, the discipline transfers: the selection package should be written as if someone with authority must sign it, because that forces the residual-risk statement to be honest.

### Worked example: Northwind Telehealth — control selection package

**The system (fictional).** Northwind Telehealth is a 60-person startup: a patient portal (web), a clinician scheduling app, a video-visit service (third-party), and a PostgreSQL database holding appointment records and visit notes. Impact categorization: moderate for confidentiality (health-adjacent personal data under contractual obligations), moderate for integrity (scheduling errors strand patients), low for availability (outages are painful, not life-threatening). Baseline starting point: moderate.

**Requirements (derived, testable, numbered):**

- SR-1: The system shall authenticate every user (patient, clinician, administrator) before granting access to any appointment or visit data.
- SR-2: Appointment and visit data shall be encrypted in transit and at rest, with keys managed under a documented lifecycle.
- SR-3: Every access to visit notes shall be logged with user identity, timestamp, and action; logs shall be protected from modification.
- SR-4: Administrative access to production data shall require two-person approval for changes.
- SR-5: The third-party video service shall not receive patient data beyond the minimum needed for the visit, and its access shall be reviewable.

**Selection with rationale (excerpt):**

| Req | Control (SP 800-53) | Tailoring | Rationale |
|---|---|---|---|
| SR-1 | IA-2 (identification and authentication) | Parameterized: phishing-resistant MFA for clinicians/admins; password + TOTP minimum for patients (from `e-iam`'s assurance logic) | Directly implements the requirement; strength keyed to impersonation impact per population |
| SR-1 | AC-2 (account management) | Parameterized: automated deprovisioning within 24h of HR termination event | Authentication is meaningless for accounts that should not exist — the joiner-mover-leaver complement |
| SR-2 | SC-12 (cryptographic key establishment and management) | Parameterized: platform-managed keys, annual rotation, documented compromise procedure (from `e-crypto-applied`'s lifecycle) | Encryption without key management is obfuscation with extra steps |
| SR-2 | SC-28 (protection of information at rest) | As written | The at-rest half of the requirement; implementation: platform disk encryption |
| SR-3 | AU-2 (audit events), AU-9 (protection of audit information) | Supplemented: AU-9 enhanced — append-only log store | The requirement has two halves (capture + protect); AU-2 alone leaves logs editable by the people being logged |
| SR-4 | AC-5 (separation of duties) | Parameterized: approver ≠ executor, enforced in the change tool | The `e-secure-design` R3 pattern; prevents unilateral production data changes |
| SR-5 | CA-7-adjacent continuous monitoring; PS/contractual control via vendor review | Compensating: no direct technical control over the third party's internals, so monitoring + contractual audit right + data minimization at the integration boundary | Honest about the boundary: you cannot control their system, only your exposure to it |

**Tailoring decisions (written down):** *Scoped out:* SC-7 boundary protection enhancements for a dedicated network security stack — the system runs on a managed platform whose boundary controls are inherited (documented as inherited, not absent). *Scoped out:* PE family beyond the office basics — no owned data center. *Supplemented:* AU-9 enhancement for append-only logs — the moderate baseline's audit protection was judged insufficient against an administrator-threat model.

**Defended omissions (the part most selections skip):** *SI-4 (system monitoring) full deployment deferred:* the team judged that AU-2/AU-6 (audit review) plus the platform's native alerting covers the detection requirement for year one; full SI-4 is scheduled for the next review cycle with an owner and date — a deferral, not an abandonment. *CP-4 (contingency plan testing):* tabletop only in year one; the honest statement is that recovery is untested beyond the tabletop, and the residual risk is accepted by the CTO in writing.

**Coverage check:** SR-3 has detective (AU-2/AU-6) plus protective (AU-9) — covered. SR-1 has preventive (IA-2) plus lifecycle (AC-2) — covered. The package's weakest point is named, not hidden: availability requirements have only the platform's native redundancy (inherited controls), so a platform-region failure is the largest unmitigated risk — stated in the residual-risk paragraph the authorization would sign.

## 4. Walkthrough

**Worked-case lesson — no command line.** The Northwind package above, authored and self-reviewed in-session on 2026-10-10. Transcript: `runs/e-control-selection.log`.

1. **Categorize the impact.** For a fictional (or your own) system, state the confidentiality/integrity/availability impact (low/moderate/high) with one sentence of justification each. This sets the baseline starting point — and forces you to say what the system is *for*.
2. **Write testable requirements.** Five to eight, each falsifiable by a tester. Ban the words "adequate," "appropriate," and "secure" — replace each with something measurable.
3. **Select from the catalog.** For each requirement, name the SP 800-53 control(s), the tailoring (scoping, parameterization, supplementing, compensating), and the rationale in one paragraph. If you cannot write the rationale, you have not selected — you have guessed.
4. **Write the defended omissions.** List every baseline control you scoped out or deferred, with the reason and — for deferrals — the owner and date. An omission without a reason is a finding waiting for an auditor.
5. **Check coverage.** For each requirement, name the control types present (preventive/detective/corrective) and identify the requirement with the thinnest coverage. That requirement gets the residual-risk paragraph.
6. **Close out.** One page: requirements, selection, tailoring, omissions, coverage, residual risk. Written as if someone must sign it — because the discipline is the point even when the signature is informal.

## 5. On your own

**Task:** Build a control-selection package for a system you control (home lab counts): categorize impact, write five testable requirements, select and tailor controls with rationale, and write the defended omissions.

**Success test:** Your package contains at least one scoped-out baseline control with a written reason, at least one parameterized assignment with a specific value, and at least one deferral with an owner and a date. The residual-risk paragraph names the single largest unmitigated risk honestly — if everything is "covered," you did not look hard enough.

## 6. Where it goes wrong

- **Catalog as checklist.** Selecting controls because they exist, not because a requirement needs them. The symptom: a selection nobody can defend and everybody resents — security theater with a control number on it.
- **Inherited controls, forgotten.** "The platform handles it" without naming the control, the service, and the evidence. Inherited is a legitimate tailoring outcome; undocumented is an omission.
- **Untestable requirements.** "The system shall adequately protect data" traces to everything and verifies nothing. If the tester can't falsify it, the requirement is decoration.
- **The missing detective half.** Preventive controls selected, detection assumed. Every requirement needs someone to notice when the preventive control fails — coverage is a mix, not a single layer.
- **Deferrals without owners.** "We'll do SI-4 next year" with no name and no date is abandonment with better PR. `e-risk-assessment`'s rule transfers: acceptance without an owner and a date is abandonment.
- **Tailoring by comfort.** Scoping out the controls that are hard to implement and keeping the easy ones, then calling the result "risk-based." The scoping rationale must cite the requirement and the threat, not the effort.
- **The unsigned residual risk.** A package that never states what remains exposed is a package that pretends selection equals safety. Residual risk named and accepted is the honest end state; residual risk unmentioned is the incident report's opening paragraph.

## 7. Read the source

Primary documents first:

- **NIST SP 800-53 Rev. 5, Security and Privacy Controls** (csrc.nist.gov) — *read* the introduction (baselines, tailoring vocabulary) and two families end to end (AC and AU are the best-taught); *use* the rest as the catalog during selection.
- **NIST SP 800-160 Vol. 1 Rev. 1** (csrc.nist.gov) — *read* the requirements-engineering sections: how stakeholder needs become system security requirements. The "why" behind this lesson's first step.

Then at most three free resources:

1. **OWASP ASVS (Application Security Verification Standard)** (owasp.org) — free; a requirements catalog at application level — use it to practice writing testable requirements before touching 800-53.
2. **MITRE ATT&CK** (attack.mitre.org) — free; the threat-informed side of selection: check that your controls cover the techniques your threat model actually predicts.
3. **CISA physical security resources** (cisa.gov) — free; for the PE-family selections most software teams scope out — read before you scope, so the omission is defended.

## 8. Check yourself

1. A team selects AC-2 with the assignment "review accounts periodically." Explain the two defects (one in the requirement it traces to, one in the tailoring) and rewrite both correctly.
2. A startup applies the full moderate baseline to a five-person internal tool. Name the failure mode, explain what it costs beyond money, and describe the requirement-driven alternative.
3. A selection covers a logging requirement with AU-2 (audit events) only. Using the coverage argument, explain what is missing, which control supplies it, and what incident reveals the gap.
4. A team writes "inherited from the cloud provider" for six controls. List the three things that must be documented for each for the inheritance to be legitimate rather than an omission.
5. Predict the audit outcome for a package with no defended-omissions section: which question does the auditor ask first, and what does the team's inability to answer reveal about the selection process?

## 9. Prove it

**Artifact:** your control-selection package — impact categorization with justification, five-plus testable requirements, the selection table (control, tailoring, rationale), defended omissions with owners and dates, the coverage check, and the residual-risk paragraph — for the Northwind case in your own words, or for a system you control.

**Honest claim:** "I can derive testable security requirements, select and tailor controls from the catalog with written rationale, defend the omissions, and state the residual risk."
**Can't claim yet:** "I can lead a formal authorization" — the authorizing-official role carries organizational authority and accountability this lesson doesn't confer; it taught the package such a decision is made from.

## 10. Leads to

- `e-secure-design` — the traceability matrix habit this lesson extends; reread its R1–R6 as a mini-selection.
- `e-risk-assessment` — risk responses are requirement sources; the deferral rule (owner + date) is shared.
- `e-assessment-strategy` — assessment, test, and audit strategy: the verification column of the trace becomes the assessment plan.
- `d-cloud-security` — inherited controls done right: what "the platform handles" must document.
- Map refs: **CISSP 3.3** (this lesson); feeds **CISSP 6.1** (assessment strategy from the trace).
