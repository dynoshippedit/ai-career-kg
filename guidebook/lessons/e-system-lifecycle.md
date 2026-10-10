---
lesson_id: e-system-lifecycle
slug: system-lifecycle
stage: E
level: 3
prerequisites: [e-secure-design, e-sdlc]
roles: []
map_refs: ["CISSP 3.10"]
test_date: 2026-10-10
description: "Write a gate-review template with security deliverables per phase, complete one gate review to a go/no-go decision, and plan secure disposal. A free lesson in the security guidebook, serving CISSP objective 3.10."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# The information system lifecycle: security at every gate


**Map ref:** serves **CISSP objective 3.10** — the information system lifecycle: security integration across phases, gate reviews, and secure disposal.

---

## 1. Where this shows up

Systems are not born secure and do not stay secure by inertia — they pass through phases, and each phase transition is a moment when security can be required, verified, or quietly dropped. The information system lifecycle is the discipline of attaching security deliverables to those transitions: requirements before design, architecture review before build, testing before deployment, monitoring during operations, sanitization at disposal. It shows up in the gate review that stops a system from deploying without its authorization package, in the decommissioning checklist that ensures the retired server's disks don't become someone else's data breach, in NIST SP 800-160's treatment of security as a systems-engineering concern across the whole life cycle, and in the CISSP as the objective that connects every other Domain 3 topic into a timeline. Most security failures are lifecycle failures with a technical symptom: the vulnerability that was a missing requirement, the breach that was a skipped gate, the data exposure that was a disposal nobody owned.

## 2. Before you start

- You can derive security requirements (`e-secure-design`) — requirements are the lifecycle's first deliverable.
- You know the SDLC's security activities (`e-sdlc`) — this lesson places them in the full system lifecycle, which is wider than software development.
- No tools. The work products are a gate-review template (security deliverables per phase) and one completed gate review with a go/no-go decision.

## 3. How it works

**The phases.** Systems engineering (ISO/IEC/IEEE 15288, NIST SP 800-160) describes the life cycle in phases that every system traverses, whatever the development methodology:

- **Concept and requirements:** the system's purpose, stakeholders, and constraints are defined. The security deliverable: the **security requirements baseline** — stakeholder needs translated into testable security requirements (`e-secure-design`'s R1–Rn), the threat model, and the impact categorization that sets the control baseline (`e-control-selection`).
- **Design and architecture:** requirements become architecture. Deliverables: the **architecture review** against the design principles, the **control selection package** with its traceability matrix, and the platform/facility decisions that constrain everything after.
- **Implementation and integration:** the system is built and assembled. Deliverables: **secure implementation evidence** — code review and testing results (`e-sdlc`), configuration baselines, and the as-built documentation showing what was actually built versus what was designed (the drift between them is a finding source).
- **Verification and deployment:** the system is proven and released. Deliverables: **security assessment results** (the architecture assessment from `e-arch-vuln-assessment`, penetration testing where warranted), **remediation of findings** or documented risk acceptances with owners and dates, and the **authorization decision** — someone with authority signs that the residual risk is acceptable. Deployment without authorization is the gate this whole lifecycle exists to enforce.
- **Operations and maintenance:** the system runs. Deliverables: **continuous monitoring** (logging, vulnerability management, configuration change control), **periodic reassessment** (the assessment re-runs when the architecture changes), and **incident response readiness**. Security decays in operations — the lifecycle's job here is to make decay visible.
- **Disposal and transition:** the system retires. Deliverables: the **disposition plan** — data migration or archival, **media sanitization** per NIST SP 800-88 (clear, purge, or destroy, matched to the data's classification), decommissioning of identities and credentials, contract termination, and confirmation that no residual data, access, or dependency remains. Disposal is the most skipped phase and the source of the most embarrassing breaches: the retired server sold with customer data, the cloud account nobody closed still running (and billing) with production credentials.

**Gates and their teeth.** A **gate review** sits at each phase transition: a defined set of entry criteria (the deliverables the phase must produce), a reviewer independent of the builders, and a **go / no-go / go-with-conditions** decision recorded with rationale. The gate's power is entirely in its teeth: a gate that cannot say no is a milestone with a fancier name. Go-with-conditions is the honest middle — deployment allowed with named conditions, owners, and dates, which is risk acceptance made explicit rather than implicit. The gate review for deployment is the lifecycle's load-bearing moment: it is where "we'll fix it in production" meets someone authorized to refuse.

**Security across methodologies.** Agile, DevOps, and waterfall all have lifecycles — the phases compress but don't disappear. In continuous delivery, the gate review becomes the pipeline's policy checks plus periodic human reviews; in agile, the security requirements live in the backlog with acceptance criteria. The lifecycle discipline is methodology-agnostic: whatever your process calls its phases, each transition needs its security deliverable and its decision. "We're agile so we don't do gates" is how you get continuous deployment of continuous vulnerabilities.

**Disposal done right.** The disposal phase deserves its weight here because it is where the lifecycle most often ends in practice — abandoned, not completed. The disposition plan covers: **data** (migrate, archive with retention, or destroy — per the retention schedule from the data lifecycle); **media** (sanitize per SP 800-88: *clear* (overwrite), *purge* (firmware-level or degauss), *destroy* (shred, incinerate) — the method matched to the classification and the media type; an SSD needs purge or destroy, not a clear designed for spinning disks); **identities and access** (deprovision every account, key, certificate, and integration the system owned — the joiner-mover-leaver lesson applied to the system itself); **dependencies** (notify and migrate every downstream consumer); and **confirmation** (evidence that each step happened — sanitization certificates, account-deletion logs). The decommissioned system gets a final review: nothing left running, nothing left accessible, nothing left billable.

### Worked example: Northwind Telehealth — gate-review template and a completed review

**The template (fictional, reusable).** Columns: phase gate, entry criteria (security deliverables required), reviewer, possible decisions.

| Gate | Entry criteria (security) | Reviewer | Decisions |
|---|---|---|---|
| G1: Requirements | Security requirements baseline; threat model; impact categorization; control baseline selected | Security architect (independent of product team) | Go / No-go (requirements untestable or uncategorized) |
| G2: Architecture | Architecture review (principles, pass/fail); control selection with traceability; platform + facility surveys | Security architect + infrastructure lead | Go / No-go / Go-with-conditions |
| G3: Implementation | Code review and test results; as-built documentation; configuration baselines | AppSec lead | Go / No-go (critical findings open) |
| G4: Deployment | Assessment results; remediation or risk acceptances (owner + date); authorization package | Authorizing official | Go / No-go / Go-with-conditions |
| G5: Operations (periodic) | Monitoring evidence; vuln-management metrics; change log; reassessment trigger check | Security operations lead | Continue / Remediate / Re-authorize |
| G6: Disposal | Disposition plan; sanitization evidence; identity deprovisioning log; dependency migration confirmations | Security architect + operations lead | Close / Re-open (residual items) |

**The completed review: G4 deployment gate for Northwind's patient portal (fictional).** Entry criteria presented: the architecture assessment (from `e-arch-vuln-assessment`'s method — 4 findings, 3 remediated), penetration test summary (2 highs remediated, 1 moderate accepted), the control selection package (`e-control-selection`'s Northwind work — trace complete), and the authorization package with residual risk stated.

Findings at the gate: (1) the third-party video service's audit right — contracted but the vendor's evidence not yet received (the SR-5 compensating control's weak point, honestly carried forward); (2) one moderate pen-test finding accepted by the CTO with a 90-day remediation date and an owner; (3) logging coverage verified in staging but the production log-forwarding rule not yet confirmed.

**Decision: GO WITH CONDITIONS.** Conditions: (a) vendor audit evidence received within 60 days, owner: vendor manager, else the video integration is re-scoped to minimum-data mode; (b) the accepted moderate remediated by its 90-day date; (c) production log forwarding confirmed within 7 days of deployment, owner: platform lead. Rationale recorded: the residual risks are bounded, owned, and dated; none permits silent data exposure. The no-go alternative was considered — delaying launch 60 days for the vendor evidence — and rejected in writing because the conditions contain the risk without the delay. That written rejection is the gate's honesty: the decision, the alternative, and why.

## 4. Walkthrough

**Worked-case lesson — no command line.** The Northwind template and G4 review above, authored and self-reviewed in-session on 2026-10-10. Transcript: `runs/e-system-lifecycle.log`.

1. **Write the template.** Six gates (or your methodology's equivalents), each with entry criteria (the security deliverables), a named reviewer independent of the builders, and the decision options. If a gate's reviewer is the team that built the phase, rewrite it — independence is the gate's teeth.
2. **Pick one gate and complete it.** Use a fictional system or a real one approaching a transition. Assemble the entry criteria honestly — missing deliverables are findings, not embarrassments.
3. **Record the findings at the gate.** Each: the observation, the deliverable it blocks or conditions, the owner, the date. Risk acceptances need the acceptor's name — "the team accepts" is not acceptance.
4. **Make the decision.** Go, no-go, or go-with-conditions — with the rationale and the considered alternative written down. A go-with-conditions decision lists every condition with owner and date; a condition without both is a wish.
5. **Write the disposal plan for something.** Pick a retired or retiring system (an old laptop, a decommissioned service, a closed account) and write its disposition: data, media sanitization method per SP 800-88, identities deprovisioned, dependencies migrated, confirmation evidence. The exercise usually finds something still running.
6. **Close out.** File the template (reusable) and the completed review (dated). The template is the artifact; the completed review is the proof the template has teeth.

## 5. On your own

**Task:** (a) Complete a gate review for a real transition — a project you're about to deploy, migrate, or retire. (b) Write a disposal plan for one retired system or device you own, and execute the sanitization step.

**Success test:** Your gate review contains at least one go-with-conditions item with owner and date — a clean go on the first real review means the entry criteria were too soft. Your disposal plan's execution finds at least one identity, credential, or dependency you forgot the system had.

## 6. Where it goes wrong

- **Gates without teeth.** Reviews that cannot say no — the schedule overrules the findings, every gate is a go, and the template becomes ceremony. A gate's value is measured in no-gos issued, not reviews held.
- **The skipped disposal.** Systems retired by abandonment: accounts live, data rests, bills accrue. Disposal is a phase with deliverables, not the absence of operations — plan it or inherit its breaches.
- **Sanitization mismatch.** Overwriting an SSD with a clear procedure designed for spinning disks, then selling it. Match the SP 800-88 method to the media and the classification — purge or destroy for flash media holding sensitive data.
- **Authorization as a signature.** The authorizing official signs without reading the package, or the package is written to be signed rather than to inform. Authorization is a decision about residual risk; a signature without the reading is a ritual.
- **"Agile means no gates."** The methodology changed; the phase transitions didn't. Pipeline policy checks plus periodic human review *are* the gates — name them, or the transitions happen without security present.
- **As-built drift.** The deployed system differs from the reviewed architecture, and nobody updated the assessment. The G4 review gates the system as *built*, not as designed — verify, don't assume.
- **Conditions without follow-through.** Go-with-conditions where the conditions evaporate after deployment — no tracking, no owner follow-up, the 90-day date passing silently. Conditions are findings with a later due date; they need the same register.

## 7. Read the source

Primary documents first:

- **NIST SP 800-160 Vol. 1 Rev. 1, Engineering Trustworthy Secure Systems** (csrc.nist.gov) — *read* the life-cycle processes and the security integration across phases; the primary source for this lesson's structure.
- **NIST SP 800-88 Rev. 1, Guidelines for Media Sanitization** (csrc.nist.gov) — *read* the clear/purge/destroy decision factors and the media-type guidance; *skim* the method details. The disposal phase's authority.

Then at most three free resources:

1. **SEBoK: System Life Cycle Process Models** (sebokwiki.org) — free; the systems-engineering view of life-cycle models (iterative, incremental) — the methodology-agnostic framing.
2. **NIST SP 800-53 Rev. 5** (csrc.nist.gov) — free; the SR (supply chain) and SI families for the disposal and operations gates — trace the gate criteria to controls.
3. **OWASP ASVS** (owasp.org) — free; the verification levels as G3/G4 entry criteria for the application components — what "tested" must mean.

## 8. Check yourself

1. A team deploys after a "gate review" in which the builders presented to themselves and approved unanimously. Name the two structural defects and describe the minimum change that gives the gate teeth.
2. A decommissioned file server is sold after a single overwrite pass. The drives are SSDs holding patient-adjacent data. Name the sanitization error (method vs media), the correct method per SP 800-88's framework, and the evidence the disposal review should have demanded.
3. A go-with-conditions deployment lists three conditions with no owners. Explain why each condition is currently a wish, what the register must add, and what happens at the due date if nothing was tracked.
4. An agile team argues gates don't apply to continuous delivery. Describe the pipeline-native equivalent of G3 and G4 — what automated checks and what human reviews, and where each lives.
5. Predict the incident that reveals disposal was skipped: which artifact survives (data, identity, or dependency), who discovers it, and what the disposition plan would have caught.

## 9. Prove it

**Artifact:** your gate-review template (six gates with entry criteria, reviewers, decisions) plus one completed gate review (findings, decision with rationale and considered alternative, conditions with owners and dates) — for the Northwind case in your own words, or for a real transition — and a disposal plan for one retired system with the sanitization step executed.

**Honest claim:** "I can define security gates across the system lifecycle, run a gate review to a recorded go/no-go decision, and plan and execute secure disposal."
**Can't claim yet:** "I can run a systems-engineering program" — SP 800-160's full process suite (stakeholder coordination, assurance cases, trade studies) is a program discipline; this lesson taught its lifecycle-gate core.

## 10. Leads to

- `e-sdlc` — the development lifecycle's security activities as the implementation phase's deliverables; reread it as G3's entry criteria.
- `e-secure-design`, `e-control-selection` — G1/G2's entry criteria, already written if you did those lessons' artifacts.
- `e-bcp-drp` — the operations gate's continuity evidence; disposal and recovery are the lifecycle's two ends.
- Map refs: **CISSP 3.10** (this lesson); feeds **CISSP 8.1** (security in the SDLC) and **2.4** (data lifecycle).
