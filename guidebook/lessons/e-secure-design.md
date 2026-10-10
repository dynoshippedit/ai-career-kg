---
lesson_id: e-secure-design
slug: secure-design
stage: E
level: 3
prerequisites: [e-risk-assessment, d-appsec]
roles: []
map_refs: ["CISSP 3.1"]
test_date: 2026-10-10
description: "Apply the eight Saltzer and Schroeder design principles in an architecture review, trace requirements to controls, and survey platform capabilities for a deployment decision. A free lesson in the security guidebook, serving CISSP objectives 3.1, 3.3 and 3.4."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Secure design principles: engineering judgment before controls


**Map ref:** serves **CISSP objective 3.1** — design principles for engineering trustworthy systems: Saltzer and Schroeder's principles applied as reviewable requirements. (Control selection and platform capabilities are taught in `e-control-selection` and `e-platform-security`.)

---

## 1. Where this shows up

Controls are the end of an argument, not the beginning. A firewall rule, an encryption setting, a key rotation schedule — each answers a design question asked much earlier. Secure design principles are the questions asked on time: before the code is written, before the platform is chosen, before requirements harden into something expensive to change. They show up in architecture reviews that kill a bad design in week two instead of discovering it in the incident report; in NIST SP 800-160's treatment of trustworthiness as an engineered property; and in the platform decision where a host with measured boot changes what you can promise. Saltzer and Schroeder's 1975 paper gave the eight principles that have survived every technology cycle since.

## 2. Before you start

- You can run a risk assessment to a decision (`e-risk-assessment`) — this lesson converts decisions into design requirements.
- You know threat modeling (`d-appsec`) — principles are what you appeal to when a threat has no pre-canned control.
- No tools. The work products are the architecture review, the requirement-to-control trace, and the platform survey. Write reasons, owners, and dates.

## 3. How it works

**The Saltzer and Schroeder principles (1975).** From "The Protection of Information in Computer Systems" — eight compressed lessons about how systems actually fail:

- **Economy of mechanism.** Keep the security design small enough to analyze. Every extra component in the trusted path is another place for a flaw to hide — prefer a tiny, well-understood reference monitor (the single component that mediates every access decision — one place to get right) over a sprawling policy engine.
- **Fail-safe defaults.** Base access decisions on permission, not exclusion: deny by default. Blacklists fail because you cannot enumerate every bad thing; whitelists fail into outages, and outages get noticed.
- **Complete mediation.** Every access to every object is checked, with no cached shortcuts or "internal" exceptions. The "no cached shortcuts" clause matters because a cached decision was made under old context — by a different component, for a different request — and can be stale or poisoned; the check must be evaluated at the moment of access. The check must sit on the path the attacker actually travels — the unauthenticated internal endpoint is the classic violation.
- **Open design.** Security must not depend on the secrecy of the design. A mechanism that survives public scrutiny has *been* scrutinized; obscurity is a hope, not a control.
- **Separation of privilege.** Require more than one key to unlock where it matters: dual control on key ceremonies, distinct approver and executor. This bounds the blast radius of one compromised credential.
- **Least privilege.** Every subject gets the minimum authority it needs, for the minimum time. Unused privilege is unmonitored attack surface — the principle behind just-in-time elevation in `e-iam`.
- **Least common mechanism.** Minimize mechanism shared by mutually distrusting parties. A shared cache, a shared admin console, one schema for all tenants: single points of compromise.
- **Psychological acceptability.** Mechanisms must be easy enough that users route around them less than they use them. Security that fights the user loses to the user.

(OWASP's Security by Design principles restate this lineage for application architects — minimize attack surface, secure defaults, least privilege, defense in depth, fail securely, don't trust services, separation of duties, avoid security by obscurity, keep security simple, fix issues correctly.)

**From principles to requirements to controls.** The disciplined flow (NIST SP 800-160, *Engineering Trustworthy Secure Systems*): derive **system security requirements** from stakeholder needs, threats, and the principles; select **controls** from a catalog — NIST SP 800-53 is the reference — that satisfy those requirements; **tailor** (adjust the selected controls — add, remove, or scope them — to fit the system's risk and context) for context; record the chain in a **traceability matrix** so every control answers "which requirement do you satisfy?" An unmapped control is cost without justification; an unimplemented requirement is a promise the architecture quietly broke. Selection is never "apply the whole catalog" — it is risk-proportionate, which is why this lesson takes `e-risk-assessment` decisions as input.

**Platform security capabilities.** The platform is the foundation the architecture stands on:

- **Memory protection:** non-executable memory, address-space layout randomization, control-flow enforcement (e.g., Intel CET's shadow stack) — raising memory-corruption exploitation from reliable technique to research project.
- **Hardware roots of trust:** a TPM provides measured boot (boot-component hashes in platform configuration registers), sealed storage (keys usable only when measurements match), and remote attestation. Everything else's evidence chains back to it.
- **Secure boot (UEFI):** firmware verifies each boot stage's signature before handing it control, so a compromised bootloader cannot persist below the OS's notice.
- **Virtualization isolation:** the hypervisor as a smaller trust boundary than a general-purpose OS; confidential-computing extensions encrypt guest memory against a compromised host.
- **Encryption capabilities:** hardware AES acceleration, TPM or platform-keystore key storage, full-disk encryption — encryption you can deploy because the platform makes it cheap and the keys have somewhere to live.

The deployment decision is where these capabilities become architecture: two "equivalent" hosts are not equivalent if one offers a TPM, measured boot, and memory encryption and the other offers none.

### Worked example: Harborline Logistics — architecture review with traceability

**The system (fictional).** Harborline Logistics runs a fleet-management platform: vehicle telematics gateways (telematics: the systems reporting vehicle location and status over cellular; cellular IoT) report to an ingestion API; a dispatch web app assigns routes; a billing service invoices customers; the database tier is proposed to move from cloud to colocation.

**Principle-by-principle review (pass/fail with rationale):**

1. **Economy of mechanism — FAIL.** Authorization lives in three places: the API gateway, a per-service middleware library, and ad-hoc checks in the dispatch app. *Fix:* one authorization service on the request path. *Requirement R1:* "All access decisions are made by a single authorization component."
2. **Fail-safe defaults — PASS (with note).** The gateway denies by default; routes open explicitly. *Note:* a debug endpoint sits in staging's default route table — a hygiene item, not a design flaw.
3. **Complete mediation — FAIL.** The billing service reads telematics data straight from the database, bypassing the API's authorization checks. *Requirement R2:* "Every data access traverses the authorization component; no service holds database credentials."
4. **Open design — PASS.** Standard OIDC (OpenID Connect — the authentication protocol that lets users log in via an identity provider), AES-GCM via the platform crypto library, no custom protocols. The architecture is shared with customer auditors.
5. **Separation of privilege — FAIL.** The on-call engineer can both approve and execute production database changes. *Requirement R3:* "Production data changes require a distinct approver and executor."
6. **Least privilege — PARTIAL.** Services run as non-root with scoped roles (pass); but the gateway agent runs as root and the ingestion API's database account holds write access it never uses (fail). *Requirement R4:* "Service identities hold only the permissions their call graph (the set of functions and APIs the service actually invokes) requires; reviewed quarterly."
7. **Least common mechanism — FAIL.** All tenants share one database schema with application-level tenant filtering — one bug from cross-tenant disclosure. *Fix:* database-enforced row security, a real boundary below the application.
8. **Psychological acceptability — FAIL.** Production deploys need a 14-step manual runbook, so engineers batch changes and deploy at midnight, tired. *Fix:* a one-command pipeline with approvals *in* it, not around it.

**Requirement → control trace (excerpt):**

| Req | Requirement (paraphrase) | Control (SP 800-53) | Implementation |
|---|---|---|---|
| R1 | Single authorization component | AC-3 (access enforcement) | Central authz service; gateway + services call it; middleware checks removed |
| R2 | No bypass of authorization | AC-3, AC-6 (least privilege) | Services lose DB credentials; data access via API only |
| R3 | Two-person production changes | AC-5 (separation of duties) | Change tooling enforces distinct approver/executor |
| R4 | Least-privilege service identities | AC-6 | Scoped roles; quarterly review owned by platform team |
| R5 | Boot integrity of telematics gateways | SI-7 (software/firmware integrity) | Measured boot with TPM; attestation before fleet enrollment |
| R6 | Tenant isolation for dispatch data | AC-4 (information flow enforcement) | Database-enforced row security per tenant |

**Platform capability survey (the deployment decision).** Comparing the current cloud hosts against the colocation quote on five capabilities — measured boot/TPM, UEFI Secure Boot, memory encryption, hardware key storage, virtualization isolation — both offerings check out, *provided* the TPM attestation flow (R5's implementation) is built before migration. A capability you cannot confirm in writing does not exist for decision purposes; without the attestation flow, the fleet's boot integrity story silently degrades on move day.

## 4. Walkthrough

**Worked-case lesson — no command line.** The Harborline review above, authored and self-reviewed in-session on 2026-10-10. Transcript: `runs/e-secure-design.log`.

1. **Describe the system in one paragraph.** Fictional is fine — name the components, the data flows, and the trust boundaries. If you cannot draw the trust boundaries, that is your first finding.
2. **Apply each of the eight principles.** Write PASS, FAIL, or PARTIAL with a one-paragraph rationale citing a specific mechanism. A principle with no evidence either way is a FAIL.
3. **Convert each FAIL into a requirement.** Phrase it as a testable statement: "Every X must Y." Number them (R1, R2, …). These are the security requirements the architecture must satisfy.
4. **Trace each requirement to a control.** Use SP 800-53 as the catalog: name the control family and number, then write the concrete implementation. If no catalog control fits, write the implementation anyway and note the gap honestly — the trace matters more than the catalog.
5. **Survey the platform.** List the deployment options under consideration; for each, check the five capabilities (memory protection, hardware root of trust, secure boot, virtualization isolation, encryption/key storage). A capability you cannot confirm in writing does not exist for decision purposes.
6. **Close out.** Summarize: principle score, requirement count, control trace completeness, and the deployment recommendation with its conditions. File it as the artifact an auditor — or your future self — can re-derive.

## 5. On your own

**Task:** Review a system you actually control against all eight principles. Write pass/fail rationale per principle, derive numbered requirements from the failures, and trace each to an SP 800-53 control with a concrete implementation.

**Success test:** You find at least two FAILs, one a complete-mediation bypass (there is almost always one). Every requirement has a traced control naming an implementation, not a product category. Your platform survey names one capability your host lacks and what that costs you in design options.

## 6. Where it goes wrong

- **Principles as wall art.** The eight principles in a slide deck, referenced in zero design decisions. Principles exist only in review minutes — a design never challenged against them was never reviewed. The test: ask for last quarter's design-review minutes — if no principle appears in them, the principles are wall art.
- **The control shopping list.** Controls selected because they are in the catalog or the last audit mentioned them, with no requirement behind them. Untraced controls are how you get an expensive SIEM and an unpatched VPN. The tell: the trace matrix has controls with empty requirement rows — cost without justification.
- **Complete mediation's quiet exceptions.** The internal endpoint, the batch job, the "temporary" direct database access still there three years later. Every exception is a second, unreviewed architecture.
- **Fail-open defaults inherited from the framework.** ORMs, web frameworks, and cloud consoles ship permissive and expect you to lock down. Review the *actual* default configuration, not the documented one.
- **Psychological acceptability treated as soft.** It is about humans: the secure path must be the easy path, or the organization builds an insecure path around it and calls it productivity.
- **Platform capabilities assumed.** "The cloud handles that" without naming the service, the setting, and who verified it. Attestation nobody checks is theater; a TPM whose measurements nobody reads is a chip.
- **Least common mechanism in multi-tenant systems.** Shared everything with application-level tenant filtering is the most common architecture and the most commonly breached data-layer pattern — always ask what enforces the boundary *below* the application.

## 7. Read the source

Primary documents first:

- **Saltzer, J. H. & Schroeder, M. D., "The Protection of Information in Computer Systems"** (cs.virginia.edu, 1975; the full paper is freely hosted) — *read* the eight principles in the authors' own words; *skim* the Multics-era examples. This is the primary source for half the lesson — everything else is commentary.
- **NIST SP 800-160 Vol. 1 Rev. 1, Engineering Trustworthy Secure Systems** (csrc.nist.gov) — *read* the systems security engineering framework and the requirements-to-architecture flow; *skim* the process appendix. This is the document that turns principles into engineering method.
- **NIST SP 800-53 Rev. 5, Security and Privacy Controls** (csrc.nist.gov) — *skim* as the control catalog; *read* the AC family closely when building your first trace. It is a catalog, not a to-do list — selection is always requirement-driven.

Then at most three free resources:

1. **OWASP Security by Design Principles** (wiki.owasp.org) — free; the ten application-focused principles with the "why" behind each, a good second voice after Saltzer and Schroeder.
2. **Microsoft Learn: Trusted Platform Module (TPM) fundamentals** (learn.microsoft.com) — free; what a TPM actually provides (measured boot, sealed storage, attestation) without vendor mystique.
3. **Intel: A Technical Look at Control-Flow Enforcement Technology (CET)** (intel.com) — free; how hardware memory-protection capabilities work under the hood.

## 8. Check yourself

1. A team fixes a complete-mediation failure by adding authorization checks to the internal endpoint. Explain why this is still a FAIL under economy of mechanism — and what the single-check design looks like.
2. An architect argues that open design is reckless: "publishing our security architecture helps attackers." Refute this using the principle's actual claim — what does open design say security may *not* depend on, and what may it still keep secret?
3. A database holds three tenants' data with application-level tenant filtering, defended as least privilege ("the app's account can only run filtered queries"). Say which principle is actually violated and why that defense aims at the wrong one.
4. Trace one row: "Production database credentials must never exist on application hosts." Give the testable requirement, the SP 800-53 control, and the implementation — then say what breaks if the implementation is "config file with tight permissions."
5. Predict the failure sequence when a deployment pipeline's "secure" process has 14 manual steps: which principle is violated, what behavior it produces, and what the incident that exposes it looks like.

## 9. Prove it

**Artifact:** your architecture review — system description, eight principles with pass/fail rationale, numbered requirements, the requirement-to-control trace, and the platform survey with deployment recommendation — for the Harborline case in your own words, or for a system you control.

**Honest claim:** "I can review an architecture against the eight design principles, turn failures into testable requirements, trace each to a control, and judge a platform's capabilities for a deployment decision."
**Can't claim yet:** "I can execute a systems security engineering program" — SP 800-160 is a full lifecycle discipline; this lesson taught its design-review core.

## 10. Leads to

- `e-security-models` — formal security models: the mathematical form of complete mediation and least privilege.
- `e-system-lifecycle` — the information system lifecycle: where this lesson's requirements and gates live across phases.
- `e-risk-assessment` — the risk decisions that become this lesson's requirements; reread its response options as requirement sources.
- `e-crypto-applied` — platform encryption meets key lifecycle: the TPM holds the keys this lesson's R5 needs managed.
- Map refs: **CISSP 3.1** (this lesson); feeds **CISSP 3.3, 3.4** (`e-control-selection`, `e-platform-security`) and **CISSP 8.1** (security in the SDLC).
