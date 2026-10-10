---
lesson_id: e-iam
slug: iam
stage: E
level: 3
prerequisites: [a-http-depth, a-linux-cli, b-session-auth]
roles: [cloud-security, iam-engineer]
map_refs: ["CISSP 5.1", "CISSP 5.2", "CISSP 5.3", "CISSP 5.4", "CISSP 5.5"]
test_date: 2026-10-09
description: "Identity and access management: the joiner-mover-leaver lifecycle, assurance levels, federation, RBAC/ABAC, privileged access — with a full access review worked case. A free lesson in the security guidebook, serving CISSP objectives 5.1–5.5."
dateline: "Worked case authored and reviewed 2026-10-09 · no command line in this lesson"
---
# Identity and access management: who gets in, and to what


**Map ref:** serves **CISSP objectives 5.1–5.5** — access control, identification/authentication strategy, federated identity, authorization models, the provisioning lifecycle. (Objective 5.6, implementing authentication systems, is taught in `e-auth-systems`.)

---

## 1. Where this shows up

Every security incident is, at its core, an identity question: somebody (or something) did something, and the system decided — correctly or not — that they were allowed to. IAM is the discipline that makes those decisions deliberate: who exists in your systems, how they prove who they are, what they may touch, and how that access ends. It shows up in the joiner-mover-leaver tickets nobody wants to own, in the quarterly access reviews auditors demand, in the SSO rollout that finally kills the password spreadsheet, and in the breach report that begins "the attacker used a legitimate account." GRC analysts live here; so do IAM engineers, cloud architects, and every CISO explaining to a board why a departed employee still had VPN access.

## 2. Before you start

- You understand authentication schemes (Basic, Bearer, JWT structure, OAuth 2.0/OIDC flows) from `a-http-depth`, and users/groups/permissions from `a-linux-cli`.
- You have seen authentication fail in `b-session-auth` — this lesson is the organizational answer to those failures.
- No tools. The work products are documents: a lifecycle design and a completed access review. Bring the discipline of writing reasons, owners, and dates.

## 3. How it works

IAM answers three questions in order, and the order matters. **Identification** is the claim: "I am alice." **Authentication** is the proof: a password, a token, a biometric, a certificate — something the system can verify against the claim. **Authorization** is the decision: given that this really is alice, what may she do? Every access-control failure you have ever read about is one of these three done wrong: nobody checked the claim, the proof was weak or replayable, or the decision was never made and the default was allow.

**The lifecycle.** An identity is not created once; it moves through states, and each transition is where access goes wrong. The standard frame is **joiner–mover–leaver**:

- **Joiner:** a person (or service) arrives. Provisioning creates the identity and grants *initial* access. The failure mode is over-provisioning on day one — "give them what the last person in the role had," which quietly accumulates into standing privilege nobody reviews.
- **Mover:** the person changes role, team, or project. Access should change with them — new grants *and* revoked old ones. This is the transition organizations skip most often, and it is how a marketing analyst keeps production database read access for three years.
- **Leaver:** the person departs. Deprovisioning disables the identity and revokes everything. The failure mode is delay — the account lingers "just in case," and lingering accounts are the ones attackers rent.

The lifecycle applies to **non-human identities** too: service accounts, API keys, CI/CD runners (CI/CD: continuous integration / continuous deployment — the automated build-and-ship pipeline, whose identity can deploy to production), and now AI agents. These are harder because nobody "leaves" — they persist until someone audits them, which is why the worked case below includes them.

**Authentication strategy.** Not every population needs the same strength — uniform strong authentication everywhere is too expensive and frictionful to survive, uniform weak authentication leaves the high-impact accounts exposed, so the strength follows the impact. The working method (from NIST SP 800-63, the digital-identity guidelines) is to pick an **assurance level** per population based on the impact of impersonation: customers logging into a forum need less than administrators touching production, which needs less than the break-glass account (the emergency admin account used when normal authentication is unavailable — sealed credentials, every use reviewed) that can rebuild everything. Then choose mechanisms to match: passwords alone where impact is low; phishing-resistant MFA (FIDO2/WebAuthn security keys or platform authenticators) where impact is high; certificates or managed identities (cloud-platform identities assigned to a workload automatically — no stored credential to steal or rotate) for service accounts. Two rules that never bend: never invent your own authentication protocol, and never let a weaker path bypass a stronger one — the help-desk password reset that skips MFA *is* the authentication system, whatever the architecture diagram says.

**Federation.** When your users need access to someone else's system (a SaaS app, a partner portal), you have two bad options and one good one: give the third party passwords (bad), maintain separate accounts everywhere (worse), or **federate** — your identity provider asserts "this is alice, authenticated at this level" and the third party trusts the assertion. SAML (Security Assertion Markup Language) and OIDC (OpenID Connect) are the protocols that carry these assertions. SP 800-63's three assurance components, for the §7 reading: IAL (identity assurance level — how well the identity was proofed), AAL (authenticator assurance level — how strong the authentication is), FAL (federation assurance level — how strong the assertion is). The security judgment is in the trust decision: which attributes you release, how long assertions live, and what happens when the provider is compromised — because federation concentrates risk in the identity provider, which is exactly why attackers target it.

**Authorization models.** Once identity is established, the access decision needs a model:

- **Discretionary (DAC):** the resource owner decides ("I shared the doc with you"). Simple, familiar, and ungovernable at scale — every shared drive is a DAC system, and every "who has access to this folder?" mystery is DAC's bill coming due.
- **Mandatory (MAC):** the system enforces labels (clearances, classifications). Strong, rigid, rare outside government and high-assurance environments.
- **Role-based (RBAC):** permissions attach to roles, users attach to roles. The enterprise workhorse. Its failure mode is **role explosion** — thousands of roles that nobody can distinguish, which is just DAC with extra steps — and **privilege creep**, the slow accumulation the mover transition feeds.
- **Attribute-based (ABAC):** decisions evaluate attributes of the subject, resource, action, and environment ("allow if subject.department == resource.owner_department AND time < 18:00"). Expressive and precise; its failure mode is policy complexity nobody can audit by reading.

In practice you will see RBAC for the coarse structure with ABAC-style conditions bolted on (cloud IAM policies are this hybrid). The model matters less than the review: whatever you choose, someone must periodically ask "should this still be true?" — which is the access review.

**Privileged access.** A small set of accounts can do outsized damage: domain admins, cloud root/owner roles, database superusers, the CI/CD identity that deploys to production. These get special handling: **just-in-time elevation** (privilege granted for a bounded task, then removed, instead of standing admin rights), **separation of duties** (no single person can both request and approve their own elevation), and **session recording** for the sessions that matter. Standing privilege is the enemy — every account with permanent admin rights is an account an attacker only needs to borrow once.

### Worked example: Meridian Analytics — lifecycle design and access review

**The company (fictional).** Meridian Analytics, 180 people. One identity provider (SSO for 40 SaaS apps), an AWS-style cloud account, a production database, a CI/CD system, and a VPN. Today: IT provisions accounts from a spreadsheet, nobody owns the mover transition, and deprovisioning happens "when someone remembers."

**Part 1 — the lifecycle design.** The HR system becomes the **authoritative source**: a hire record triggers provisioning, a transfer triggers a mover review, a termination triggers deprovisioning within 24 hours — automatic for SSO and VPN, ticketed with an SLA for the rest. Role definitions are written down (twelve roles, each listing exactly which systems and permission levels it grants — no "same as the last person"). Service accounts get owners, documented purpose, and 90-day credential rotation; any service account without an owner is disabled. Break-glass accounts exist for the IdP and the cloud root, sealed credentials in a safe, every use triggers an alert and a mandatory review.

**Part 2 — the access review (one quarter's run).** Scope: all 180 human identities plus 34 service accounts, against the twelve role definitions. Reviewers: each manager reviews their direct reports; the security lead reviews all privileged access; service-account owners review their own.

Findings (fictional, labeled):

1. **Orphaned leaver:** a contractor's SSO account active 47 days post-departure — the spreadsheet had no departure date. *Decision: disable immediately; fix the HR feed to carry contractor end dates.*
2. **Mover accumulation:** a support engineer moved to sales eight months ago retains production database read. *Decision: revoke; add a mover checklist item ("revoke prior-team access") to the transfer ticket template.*
3. **Role explosion symptom:** three "analyst" roles with indistinguishable permissions. *Decision: merge into one; document the one legitimate exception (finance analysts need the billing export).*
4. **Ownerless service accounts:** 6 of 34 have no owner; 2 have credentials older than a year. *Decision: disable 4 (no recent use), assign owners and rotate the remaining 2 within a week.*
5. **Standing privilege:** 11 people hold permanent production admin; the on-call rotation needs 4. *Decision: move 7 to just-in-time elevation; keep 4 standing with session recording. The detective control for the 4: alert on privileged actions with no change ticket and no named task behind them — the admin session nobody can explain.*
6. **Federation gap:** two SaaS apps still use shared passwords instead of SSO. *Decision: migrate both to SSO this quarter or document a risk acceptance with owner and date (per `e-risk-assessment`'s rule — acceptance without an owner and a date is abandonment).*

**Review close-out:** every finding has a decision, an owner, and a date. The next review is scheduled (quarterly for privileged access, semi-annually for standard). The review itself is the artifact an auditor asks for — and, more importantly, it is the mechanism that keeps the lifecycle honest.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" for this lesson is the lifecycle design and access review above, authored and self-reviewed in-session on 2026-10-09. Transcript: `runs/e-iam.log` (records scope, design decisions, and the review checklist — there are no commands to transcribe).

1. **Draw the current state.** For a fictional (or your own lab) organization, list every identity store: the IdP, the cloud account, the database, CI/CD, VPN, SaaS apps. For each, answer: who provisions, who deprovisions, what triggers each, and how long deprovisioning takes. The gaps you find in this inventory are the findings before you have even started reviewing.
2. **Write the role definitions.** Twelve or fewer roles. Each names the systems and the exact permission level. If two roles end up identical, merge them — you have found your first role-explosion symptom.
3. **Design the three transitions.** Joiner (what the HR record triggers, what is automatic vs ticketed), mover (the checklist that revokes old access), leaver (the 24-hour rule and its SLA per system). Name the authoritative source. If it is a spreadsheet, say so honestly and note the failure mode.
4. **Run the review.** Take a roster (fictional is fine — invent 20 identities across your roles, including one leaver, one mover, and two service accounts) and review each against the role definitions. Record every deviation as a finding with a decision, an owner, and a date. You should find the planted problems; if you find none, your roster was too clean.
5. **Handle privileged access separately.** List every identity with admin-level rights. For each, decide: standing (with justification and session recording) or just-in-time. Anyone whose justification is "they might need it someday" moves to just-in-time.
6. **Close out.** Schedule the next review, file the decisions, and write the one-paragraph summary you would give an auditor: scope, findings count, decisions, next date.

## 5. On your own

**Task:** Run an access review on a system you actually control — your home lab, your VPS, your GitHub organization, or your cloud account's IAM. Inventory every identity (human and non-human), compare each against what the role should grant, and produce the findings list with decisions, owners (you), and dates.

**Success test:** Your findings include at least one non-human identity and at least one access grant you cannot justify on sight — if everything looks perfect, you did not look hard enough. Every finding has a decision, an owner, and a date; standing privileged access is either justified in writing or converted to just-in-time.

## 6. Where it goes wrong

- **The spreadsheet of truth.** Provisioning driven by memory, chat messages, or "same as the last person" produces access nobody can reconstruct. The authoritative source must be a system of record (HR), not a person.
- **The skipped mover.** Joiner and leaver get process; mover gets forgotten. Privilege creep is almost entirely a mover problem — audit the transitions, not just the endpoints.
- **Role explosion.** A thousand roles nobody can distinguish is DAC wearing a costume. If you cannot explain a role's purpose in one sentence, it should not exist.
- **The weaker path.** MFA on the front door, password-only reset via help desk, SSO everywhere except the two apps with shared passwords. Attackers use the weakest path, not the documented one — inventory *all* paths.
- **Non-human identity sprawl.** Service accounts created for a migration in 2021, API keys in a former employee's notes, CI/CD tokens with production deploy rights. These never "leave," so they only shrink under review.
- **Review theater.** The quarterly review where every manager clicks "approve all" in eleven minutes. A review with no findings is a review that did not happen — sample-check two approvals per cycle by asking the reviewer to justify one grant aloud.
- **Federation as single point of failure.** Concentrating trust in the IdP is correct architecture and a prime target. The IdP gets the strongest authentication, the tightest break-glass procedure, and its own monitoring — compromise of the IdP is compromise of everything downstream.

## 7. Read the source

Primary documents first:

- **NIST SP 800-63-4 (Digital Identity Guidelines)** (csrc.nist.gov, final July 2025 — supersedes 800-63-3) — *read* the assurance-level concept (IAL/AAL/FAL, carried forward from the 3rd revision) and the authenticator guidance; *skim* 800-63A-4/B-4/C-4 for the enrollment/authentication/federation split. This is the document the industry's authentication strategy is written against — cite the 4th revision, not the 3rd.
- **NISTIR 7316, Assessment of Access Control Systems** (csrc.nist.gov) — free; how access-control authorization structures are assessed — *read* for the assessment lens on the models above.
- **NIST SP 800-53, Access Control family (AC)** (csrc.nist.gov) — *skim* as the control catalog IAM programs are audited against; *read* AC-2 (account management) and AC-5/AC-6 (separation of duties, least privilege) closely — they are the lifecycle in control language.

Then at most three free resources:

1. **OWASP Authentication Cheat Sheet** (cheatsheetseries.owasp.org) — free; the practitioner checklist for implementing what 800-63 specifies.
2. **CISA Identity and Access Management guidance** (cisa.gov) — free; the operational view: what to prioritize first.
3. **FIDO Alliance: passkeys and WebAuthn explainers** (fidoalliance.org) — free; what phishing-resistant authentication actually looks like to deploy.

## 8. Check yourself

1. A company provisions from the HR system, reviews access quarterly, and still finds a departed contractor's account active 47 days later. Name the two distinct failures (one in the lifecycle design, one in the review) and the fix for each.
2. Explain why "give them what the last person in the role had" is an anti-pattern — what does it produce over three years, and which transition (joiner, mover, leaver) feeds it most?
3. A SaaS app offers SSO but the team keeps using its built-in shared admin password "for emergencies." Explain, using the weaker-path principle, why this nullifies the SSO investment — and what the break-glass alternative should be.
4. Compare RBAC and ABAC for a hospital records system: which failure mode (role explosion vs policy complexity) is more likely there, and what review mechanism catches it?
5. Predict the state of a company's service accounts two years after an IAM program launches with human identities fully governed but service accounts explicitly out of scope. Which finding appears first, and who discovers it?

## 9. Prove it

**Artifact:** your lifecycle design (authoritative source, the three transitions with SLAs, role definitions) plus a completed access review (roster, findings with decisions/owners/dates, privileged-access disposition, close-out summary) — for the Meridian worked case reproduced in your own words, or better, for a system you actually control.

**Honest claim:** "I can design an identity lifecycle and run an access review that produces decisions — I can say who should have access to what, find where reality diverges, and drive each divergence to a decision with an owner and a date."
**Can't claim yet:** "I can architect a federated enterprise identity deployment" — protocol-level federation design (SAML/OIDC integration, IdP hardening at scale) is its own engineering discipline; this lesson taught the decisions around it, not the implementation.

## 10. Leads to

- **e-personnel-security — Personnel security across the employment lifecycle** — the HR side of joiner-mover-leaver: background checks, onboarding security, termination procedure.
- **e-secops-concepts — Operational disciplines** — privileged-access management as a daily operation: just-in-time elevation, session recording, SoD enforcement.
- **e-csf-20 — NIST CSF 2.0** — IAM sits in the Protect function (PR.AC); the access review is evidence for the Govern function.
- `b-session-auth` — the technical failures this lesson's processes exist to prevent; reread it as the "what happens without this" companion.
- Map refs: **CISSP 5.1, 5.2, 5.3, 5.4, 5.5** (this lesson); feeds **CISSP 1.8** (personnel security) and **7.4/7.9** (operations).
