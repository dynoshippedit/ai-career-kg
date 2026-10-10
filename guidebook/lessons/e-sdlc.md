---
lesson_id: e-sdlc
slug: sdlc
stage: E
level: 3
prerequisites: [e-risk-assessment]
roles: [appsec]
map_refs: ["CISSP 8.1", "CISSP 8.2", "CISSP 8.3", "CISSP 8.4", "CISSP 8.5"]
test_date: 2026-10-09
description: "Secure SDLC: threat modeling with STRIDE, security gates per phase, the SSDF practice groups, and metrics that measure effectiveness — with a gate review worked case. A free lesson in the security guidebook, serving CISSP objectives 8.1–8.5."
dateline: "Worked case authored and reviewed 2026-10-09 · no command line in this lesson"
---
# Secure SDLC: catching the vulnerability before it ships


**Map ref:** serves **CISSP objectives 8.1–8.5** at the governance level — security in the SDLC, development-ecosystem controls, effectiveness assessment, acquired software, secure coding as policy. (The hands-on techniques for 8.1–8.5 — STRIDE, SAST/DAST/IAST/SCA, code review — are taught in the Stage D AppSec track; this lesson is the program that deploys them.)

---

## 1. Where this shows up

Every vulnerability in Stage B was a decision somebody made under schedule pressure — and a secure SDLC is the organizational machinery for making those decisions differently. It shows up in the AppSec engineer's calendar (threat-model reviews, gate sign-offs), in the CISO's metrics (defect density trending down, or not), in procurement ("show us your SSDF practices" now appears in federal software acquisition), and in the post-incident review that asks why a SQL injection shipped in 2026. This lesson teaches the program, not the tools: where security activities attach to each development phase, what each gate demands, and how to prove the program works.

## 2. Before you start

- You can describe the major vulnerability classes and their fixes (Stage B) — the gates below exist to catch exactly those.
- You can write a risk statement with reasons (from `e-risk-assessment`) — gate decisions are risk decisions.
- No tools. The work products are a threat model and a gate-review record for a fictional system. The primary spine is **NIST SP 800-218 (SSDF v1.1, February 2022)**.

## 3. How it works

**The core idea.** A software development lifecycle already has phases — requirements, design, implementation, verification, release, maintenance — and security activities attach to each phase like stations on the line. The alternative is the industry default: build first, scan at the end, argue about the findings under release pressure. Shifting an activity left (earlier) makes its findings cheaper: a design flaw caught in threat modeling costs a whiteboard session; the same flaw caught in production costs an incident.

**Threat modeling: design-phase reasoning.** Before code exists, you model what you are building and ask what can go wrong. The working method (STRIDE, from the Stage D track): draw the **data-flow diagram** — processes, data stores, data flows, trust boundaries — then walk each element asking six questions: **S**poofing (can someone pretend to be someone else here?), **T**ampering (can data be modified in transit or at rest?), **R**epudiation (can someone deny doing it — is there logging?), **I**nformation disclosure (does data cross a boundary it shouldn't?), **D**enial of service (can this be exhausted?), **E**levation of privilege (can a low-privilege actor reach a high-privilege function?). Each "yes" becomes a threat with a mitigation recorded *in the design* — not in a ticket filed later. The artifact is the model plus the decision log; a threat model nobody recorded is a conversation, not a control.

**Gates per phase.** A **gate** is a checkpoint with entry criteria: the phase's work cannot proceed until the security activity is done and its findings dispositioned. The standard attachment points:

- **Requirements:** security requirements written alongside functional ones (authentication, authorization, data classification, compliance obligations). *Gate:* requirements reviewed for completeness — "the system shall…" includes the security shalls.
- **Design:** threat model completed; security architecture reviewed (this is where `E-D3-01`'s principles get applied). *Gate:* threat-model sign-off with mitigations assigned.
- **Implementation:** secure-coding standards in force, IDE/editor checks, pre-commit secret scanning, peer review with a security checklist. *Gate:* no known-bad patterns merged (the checklist is the gate, not a person).
- **Verification:** SAST on every build, DAST against a staging environment, SCA for dependency vulnerabilities, targeted penetration testing for high-risk changes. *Gate:* findings triaged by severity with SLAs; release-blocking severities defined in advance, not negotiated at release time.
- **Release:** final review — all gate findings dispositioned, SBOM generated, signing in place. *Gate:* the release checklist, signed.
- **Maintenance:** vulnerability monitoring (new CVEs in your dependencies), incident response readiness, decommissioning plan. *Gate (ongoing):* SLA compliance on patching, reviewed periodically.

**The SSDF frame** (NIST SP 800-218 v1.1) organizes the same idea into four practice groups — **Prepare** the organization (define roles, train, set tooling), **Protect** the software (source control, signing, artifact integrity), **Produce** well-secured software (the phase activities above), **Respond** to vulnerabilities (intake, triage, remediation, root-cause analysis). It matters beyond theory: it is the vocabulary acquirers now use to ask producers what they do, so your gate program should be describable in SSDF terms.

**Measuring effectiveness.** A gate program that cannot show it works is process theater. The honest metrics: defect density by phase of introduction vs phase of detection (are you catching things earlier over time?), gate pass/fail rates with reasons, mean time to remediate by severity, and recurrence — the same vulnerability class reappearing means the *standard* failed, not the developer. "Number of scans run" is activity, not effectiveness; never report it as the latter.

### Worked example: Northwind Traders ordering API — threat model and the gate that would have caught it

**The system (fictional).** Northwind Traders is rebuilding its ordering API: a public REST API, a web frontend, a PostgreSQL database, a background worker for fulfillment, and a third-party payment processor. Trust boundaries: internet ↔ API, API ↔ database, API ↔ payment processor.

**Threat model (STRIDE walk, excerpt).** Data flows: customer → API (orders, payment tokens), API → database (order records, PII), API → payment processor (tokens). Findings recorded in the design:

1. *Tampering — order total:* the frontend sends the order total; the API trusts it. **Threat:** price tampering (the exact class from `b-business-logic`). **Mitigation (design):** the API recomputes totals server-side from the product catalog; the frontend total is display-only. Assigned: backend lead, due before implementation gate.
2. *Information disclosure — order history:* `GET /orders/{id}` takes an order ID. **Threat:** IDOR across customers (`b-idor`). **Mitigation (design):** every order access checks ownership against the authenticated identity; added to the implementation checklist as a mandatory pattern.
3. *Elevation — admin endpoints:* `/admin/*` shares the API process. **Threat:** a customer token reaching admin functions. **Mitigation (design):** separate authorization middleware for the admin path, tested by an explicit negative test case in verification.
4. *Repudiation — payment disputes:* **Threat:** "I never placed that order." **Mitigation (design):** append-only order event log with actor, timestamp, and source IP; defined in requirements as a compliance need.

**The gate review (verification phase).** The SAST run flags a concatenated SQL query in the new admin search endpoint — the exact pattern from `b-sqli`. Gate decision: **release-blocking** (severity defined in advance: injection-class findings block). The finding goes back to implementation; the fix (parameterized query) is verified by re-scan plus the negative test case; the root-cause note records that the implementation checklist's "no string-built queries" item was skipped for admin code — so the *checklist enforcement* gets fixed, not just the query. The release proceeds one day late with the evidence attached.

**What the program proved:** the threat model caught two design flaws before code existed (price tampering, IDOR); the verification gate caught the one that slipped through (SQLi in admin search); the root-cause step fixed the process gap. Total: three findings, zero shipped. That is what a gate is for — and the record of it is what you show an acquirer asking about your SSDF practices.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" for this lesson is the threat model and gate review above, authored and self-reviewed in-session on 2026-10-09 against SP 800-218's practice groups. Transcript: `runs/e-sdlc.log` (records the system scope, the STRIDE walk, gate criteria, and review notes).

1. **Scope the system.** One paragraph: components, data flows, trust boundaries. Draw the data-flow diagram (boxes and arrows on paper is fine — photograph it). If you cannot draw the trust boundaries, you are not ready to threat-model; go back until you can.
2. **Walk STRIDE.** For each diagram element, ask the six questions. Record every "yes" as a threat with a *design-phase* mitigation and an owner. Aim for 6–10 threats; fewer means you walked too fast.
3. **Write the gate criteria.** For each SDLC phase, one paragraph: the security activity, its entry criteria, who signs off, and which finding severities block. Define "release-blocking" now, in calm — never at release time.
4. **Run the gate review.** Take one finding (use the SQLi-in-admin-search scenario, or invent one from your Stage B knowledge) and disposition it: severity, fix, verification evidence, root-cause note, process fix. The root-cause note is the step everyone skips — it is also the step that makes the program improve instead of repeat.
5. **Map to SSDF.** Label each of your activities with its SSDF practice group (Prepare/Protect/Produce/Respond). Anything unmapped is either unnecessary or a gap — decide which, in writing.
6. **Write the effectiveness sketch.** Three metrics you would track for this program over a year, with definitions and data sources. If any metric is "number of scans," replace it — that is activity, not effectiveness.

## 5. On your own

**Task:** Threat-model a real system you have built or maintain (a side project, a lab app, your homelab's exposed services). Produce the data-flow diagram, the STRIDE findings with design mitigations, and the gate criteria you would impose if you were releasing it to strangers.

**Success test:** Your model contains at least one finding that surprises you — a trust boundary you had not consciously drawn, or a repudiation gap in your logging. If the model only confirms what you already knew, your diagram was too coarse; redraw it with more elements and walk it again.

## 6. Where it goes wrong

- **Threat modeling after code.** A threat model written to bless an existing design finds nothing — the design is already load-bearing. It belongs before implementation, when change is cheap.
- **Gates negotiated at release time.** "This SQLi is release-blocking, but the launch is Thursday" — if severity definitions are not fixed in advance, every gate becomes a negotiation the schedule wins. Define blocking severities in calm.
- **Checklist without enforcement.** The secure-coding checklist exists; nobody checks it; admin code is exempt "because it's internal." The Northwind root cause is the archetype — fix the enforcement, not just the finding.
- **Scanning as the program.** SAST/DAST/SCA are verification *activities*, not a secure SDLC. A program that scans at the end and threat-models never is just waterfall with dashboards.
- **Metrics of activity.** "We ran 400 scans" tells you nothing about whether software got safer. Track detection-phase shift, remediation time, and recurrence — or admit you are not measuring effectiveness.
- **Third-party code as someone else's problem.** Dependencies and acquired components carry your risk (Log4Shell taught this at scale). SCA and acquisition review (`E-D1-11`'s territory) are gates too — an SBOM nobody reads is inventory, not control.
- **The maintenance cliff.** Gates end at release; vulnerabilities do not. Without the Respond practices (intake, triage, SLA, root cause), the program covers birth and abandons life.

## 7. Read the source

Primary documents first:

- **NIST SP 800-218 v1.1, Secure Software Development Framework** (csrc.nist.gov, February 2022) — *read* the four practice groups and their tasks; *use* it as the vocabulary for describing any gate program. Short, free, authoritative.
- **OWASP SAMM** (owaspsamm.org) — *skim* the five business functions; *read* the Design and Implementation practices. The maturity-model view: where your program is vs where it needs to be.
- **NIST SP 800-64 Rev. 2, Security Considerations in the System Development Life Cycle** (csrc.nist.gov) — *skim* the phase-by-phase security considerations; the government companion to the same idea.

Then at most three free resources:

1. **OWASP Threat Modeling Cheat Sheet** (cheatsheetseries.owasp.org) — free; the practitioner process for running the STRIDE walk this lesson describes.
2. **CISA Secure by Design guidance** (cisa.gov) — free; the policy direction your gate program aligns with — leadership reads this.
3. **OWASP DevSecOps Guideline** (owasp.org) — free; how the gates fit into CI/CD pipelines in practice.

## 8. Check yourself

1. Explain why a threat model must happen before implementation — what specifically becomes more expensive with each phase you delay it, using the price-tampering finding as your example.
2. A SAST scan at release time finds an injection flaw; the launch is in two days. Explain why "we'll fix it in a patch next week" is a gate-design failure rather than a reasonable tradeoff — and what should have been decided in advance.
3. Distinguish a metric of activity from a metric of effectiveness using two examples from this lesson — then explain which one a CISO should put in a board report and why.
4. Your threat model finds that order totals are trusted from the client. Explain why adding a WAF rule is the wrong mitigation *at the design phase* — what does the design-phase mitigation look like, and why is it structurally stronger?
5. Predict what happens to a gate program over two years if root-cause analysis is skipped at every gate review: which vulnerability class reappears first, and what does the recurrence prove about the program?

## 9. Prove it

**Artifact:** your threat model (data-flow diagram, STRIDE findings with design mitigations and owners) plus a gate-review record (finding, severity, fix, verification evidence, root-cause note, process fix) — for the Northwind worked case in your own words, or better, for a system you actually build or maintain.

**Honest claim:** "I can threat-model a system before it is built and run gate reviews that change what ships — I can attach the right security activity to each SDLC phase and prove the program works."
**Can't claim yet:** "I can run an AppSec tooling program" — operating SAST/DAST/SCA at scale (tuning, pipeline integration, false-positive management) is the Stage D AppSec track's hands-on work; this lesson taught the program that directs it.

## 10. Leads to

- **D-AppSec track** — the hands-on techniques this program deploys: STRIDE facilitation, SAST/DAST/IAST/SCA operation, code review.
- **E-D3-01 — Secure design principles** — the design-phase companion: principles applied at the threat-model table.
- **E-D1-11 — Supply chain risk management** — the acquisition gate: third-party software under the same discipline.
- `b-business-logic`, `b-sqli`, `b-idor` — the vulnerability classes your gates exist to catch; reread them as gate-test cases.
- Map refs: **CISSP 8.1, 8.2, 8.3, 8.4, 8.5** (this lesson, governance level); feeds **CISSP 3.10** (system lifecycle).
