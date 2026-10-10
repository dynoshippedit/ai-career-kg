---
lesson_id: e-auth-systems
slug: auth-systems
stage: E
level: 3
prerequisites: [e-iam, a-http-depth]
roles: []
map_refs: ["CISSP 5.6"]
test_date: 2026-10-10
description: "Plan an MFA and passwordless rollout — phases, recovery, SSO migration, authenticator lifecycle — for a fictional company. A free lesson in the security guidebook, serving CISSP objective 5.6."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Implementing authentication systems: the rollout, not the theory


**Map ref:** serves **CISSP objective 5.6** — implementing authentication systems.

---

## 1. Where this shows up

`e-iam` taught you the strategy and lifecycle it serves; `b-session-auth` is the companion discipline — how authentication breaks, the failure mechanics this build is designed to prevent. This lesson is the build: choosing the mechanisms, sequencing the rollout, handling the humans, and operating the authenticators afterward. It shows up in the MFA rollout that stalls at 60 percent adoption, the passwordless pilot that dies on the help-desk queue, the SSO migration with three apps that "can't do SAML," and the biometric deployment that never answered where the templates live. IAM engineers and the security architects who sign off on the plan live here — and the difference between this lesson and its neighbors is the direction of the work: `b-session-auth` dissects failures, `e-iam` governs the lifecycle, this lesson ships the system.

## 2. Before you start

- You can distinguish authentication factors and schemes (`a-http-depth`) and you have the lifecycle frame — joiner, mover, leaver, and the assurance-level thinking (`e-iam`).
- This lesson reuses `e-iam`'s assurance idea (stronger proof where impersonation costs more) but asks the implementation question: *which mechanism, for which population, in which order, with what fallback.*
- No tools. The work product is an authentication implementation plan for a fictional company.

## 3. How it works

Implementation is sequencing. The technology choices are mostly settled — the industry has converged on a small set of mechanisms — so the work is deciding the order, the populations, the exceptions, and the recovery paths. A rollout that leads with the hardest population fails; a rollout with no recovery path fails at the first lost phone.

**MFA rollout planning.** Multi-factor authentication combines independent factors — something you know, have, or are — so that one compromised factor is not enough. **TOTP** (time-based one-time password — the six-digit codes from authenticator apps, changing every 30 seconds) is the common second factor; SMS codes are the weak form, for the reason below. The rollout plan phases by population: administrators and privileged users first (highest impersonation impact, smallest population, most tolerance for friction), then the general workforce, then customers or partners last. Each phase needs: the enrollment window and mechanism (in-person, self-service with verification), the help-desk procedure for the inevitable lockouts (which must itself resist social engineering — the help desk *is* an authentication path, per `e-iam`'s weaker-path principle), the exception process (documented, time-bounded, owned — not a permanent bypass list), and the success metric (enrollment percentage, authentication success rate, help-desk ticket volume). The plan also names what MFA does not cover: service accounts, legacy protocols, and the break-glass accounts — each gets its own compensating control, written down.

**Passwordless: FIDO2/WebAuthn and passkeys.** The phishing-resistant answer. FIDO2/WebAuthn replaces the shared secret with public-key cryptography: the private key never leaves the user's device (or hardware security key), the server holds only the public key, and the authentication ceremony binds the response to the site's origin — a phishing page on the wrong domain gets nothing usable. Passkeys are the synced, user-friendly form: the same cryptography, with the credential backed up across the user's devices or held on a hardware key. The implementation decisions: which populations get passkeys versus hardware security keys (executives and admins get the keys — no sync, no cloud dependency), the account-recovery flow when all devices are lost (this is the hard part — pre-registered recovery, verified out-of-band, never "answer your security questions"), attestation policy (whether to require proof the key is genuine hardware), and the relying-party implementation checklist from the FIDO Alliance and the OWASP Authentication Cheat Sheet. Passwordless does not mean factorless — it means the factors are cryptographic possession plus user verification (PIN or biometric unlocking the key), and the plan says so explicitly so nobody treats it as magic.

**Biometrics: implementation considerations.** Biometrics are identification convenience, not secrets — you cannot revoke your face. The implementation treats them accordingly:

- **FAR/FRR:** the false accept rate (impostor admitted) and false reject rate (legitimate user denied) trade against each other at the match threshold. The plan sets the threshold per use case — a phone unlock tolerates higher FAR than a data-center turnstile — and states both rates, because "biometric authentication" without numbers is a vibe, not a control.
- **Template protection:** the stored template must not be reversible to the biometric. Templates are encrypted, ideally held in hardware-backed secure storage on the device (never a central database of raw biometrics if avoidable), and the plan answers the breach question in advance: what happens to enrolled users if the template store is stolen.
- **Liveness and presentation-attack detection:** the sensor must resist photos, molds, and replays — the plan names the required assurance (the vendor's claim is not evidence; independent testing is).
- **Fallback and consent:** every biometric path has a non-biometric fallback (the weaker-path audit from `e-iam` applies — the fallback must not be weaker than the policy allows), enrollment is consented and revocable, and the legal/privacy handling of biometric data is documented before deployment, not after a complaint.

**SSO implementation.** Single sign-on concentrates authentication at the identity provider (IdP — the system that verifies identities and vouches for them to other systems) — one strong authentication, asserted to every application via SAML (Security Assertion Markup Language) or OIDC (OpenID Connect), the two protocols that carry these trust assertions. The implementation work is the application inventory and the long tail: which apps support modern SSO (migrate first, they're easy), which need a gateway or proxy in front (legacy apps that can't speak SAML), and which genuinely cannot (the two apps from `e-iam`'s worked case — migrate or document the risk acceptance with owner and date). Session management across the federation: idle and absolute timeouts set at the IdP, single logout behavior tested (logging out of the IdP should kill the app sessions that matter), and the IdP itself hardened as the highest-value target in the estate — phishing-resistant MFA for all IdP admins, break-glass procedure, its own monitoring. The relying party (the application that relies on the IdP's assertion — the "RP" in the FIDO checklists) is where the implementation checklist applies: it must verify the assertion's signature, audience, and freshness, not just accept the redirect.

**The authenticator lifecycle.** Every authenticator — password, key, token, biometric enrollment, certificate — is issued, used, replaced, and revoked. The implementation plan covers: issuance (identity proofing at enrollment — the strength of issuance bounds the strength of everything after, per NIST SP 800-63-4), active management (expiry, rotation for shared/standing credentials, re-verification triggers), loss and compromise (revocation SLAs: minutes for privileged, hours for standard — the stolen laptop's session must die on a timeline, not a hope), and deprovisioning (the leaver transition from `e-iam`, now with the concrete per-authenticator steps). SP 800-63-4 (Digital Identity Guidelines, July 2025, superseding the 3rd revision) is the primary: it defines the technical requirements across identity proofing, enrollment, authenticators, management processes, authentication protocols, and federation — the plan traces each decision to it.

### Worked example: Meridian Analytics — authentication implementation plan (fictional, continued from `e-iam`)

**Populations and assurance.** Admins and break-glass-adjacent roles (highest impersonation impact — break-glass: the emergency admin accounts used when normal authentication is unavailable): hardware security keys + PIN, no SMS, no fallback weaker than the key. Workforce (180): passkeys as primary, authenticator-app TOTP as the enrolled backup — SMS explicitly excluded (SIM-swap risk, stated: an attacker convinces the phone carrier to move the victim's number to the attacker's SIM, and the codes follow the number). Customers (portal): passwords plus optional passkey upgrade, risk-based step-up for sensitive actions. Service accounts: certificates or managed identities, no passwords, 90-day rotation (from the `e-iam` review's finding 4).

**Phase plan.** Phase 0 (weeks 1–2): IdP hardening — phishing-resistant MFA for IdP admins, break-glass tested, monitoring on. Phase 1 (weeks 3–6): 14 admins to security keys; help-desk lockout procedure drilled; exception process published. Phase 2 (weeks 7–12): workforce passkey enrollment, department by department, with floor-walking support the first week per department. Phase 3 (quarter 2): SSO migration of the 40 SaaS apps — 34 straightforward, 4 via gateway, 2 documented exceptions with owners and dates. Phase 4: customer portal passkey option; legacy protocol (IMAP basic auth) disabled with the one integration that needs it given a dated migration path.

**Recovery and fallback.** Lost-key procedure: in-person or video-verified re-enrollment, 24-hour delay for privileged roles (the delay is the control — it gives the real owner time to report the theft). Help-desk resets require two independent verifications and are logged to the SIEM with an alert on privileged resets. No security questions anywhere.

**Biometrics decision.** Deferred for workforce authentication — the template-storage and fallback questions couldn't be answered to the plan's standard; phone-unlock biometrics remain a device-local convenience, not an enterprise authenticator. Documented as a decision with a revisit date, not a silent omission.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the implementation plan above, authored and self-reviewed in-session on 2026-10-10 against SP 800-63-4 and the FIDO Alliance guidance. Transcript: `runs/e-auth-systems.log`.

1. **Segment the populations.** List every population that authenticates (don't forget service accounts, vendors, break-glass) and assign the impersonation impact per population — this drives every mechanism choice.
2. **Choose mechanisms per population.** Passwordless where the impact justifies the operational cost; MFA everywhere else; legacy protocols named and dated for removal. Write the rejected alternative and why for each choice.
3. **Sequence the phases.** Hardest/highest-impact first, with the help-desk and exception machinery built *before* the first user enrolls. A rollout without support sequencing is a ticket avalanche.
4. **Design recovery before enrollment.** Lost, stolen, and replaced authenticators — the procedure, the verification, the SLA, the logging. Test it on paper with the adversarial question: how would I social-engineer this?
5. **Plan the SSO long tail.** App inventory, migration order, gateway candidates, documented exceptions with owners and dates.
6. **Write the authenticator lifecycle.** Issuance, rotation, revocation SLAs, deprovisioning steps — per authenticator type.
7. **Decide biometrics explicitly.** Deploy with FAR/FRR, template protection, liveness, fallback, and consent answered — or defer in writing with a revisit date.

## 5. On your own

**Task:** Write the authentication plan for a real scope you control — your homelab, your family's devices, or your team's tooling. Populations, mechanisms, phases, recovery, and the authenticator lifecycle.

**Success test:** Your plan includes the recovery procedure attacked on paper (you find at least one social-engineering hole and fix it), every legacy protocol has a removal date or a documented exception, and the help-desk/self-recovery path is not weaker than the front door.

## 6. Where it goes wrong

- **The help-desk bypass.** Phishing-resistant MFA on the front door, password reset over the phone with a date of birth. The reset path *is* the authentication system.
- **SMS as the second factor.** SIM-swap turns it into a notification service for the attacker. Excluded by decision, not by hope.
- **The stalled rollout.** Phase 1 completes, phase 2 never starts, and the company runs two authentication systems forever — doubling the attack surface and the support load.
- **No recovery plan.** The first lost security key becomes an emergency, then a precedent, then a policy written by panic.
- **Biometrics as secrets.** A central database of fingerprints treated like a password vault. Breach it and the users cannot rotate their hands.
- **The SSO long tail ignored.** Thirty-eight apps migrated, two left on shared passwords "temporarily" — permanently. The exceptions need owners and dates.
- **Break-glass without a drill.** The sealed credentials exist; nobody has tested the envelope, the alert, or the review. The first real use is the test.
- **Passwordless declared, fallback forgotten.** The passkey rollout with a password fallback "for compatibility" — the attacker uses the fallback, not the passkey. The observable signal: authentication logs showing the fallback path used by an account enrolled in passkeys. One such event is an anomaly worth investigating; a pattern of them is the fallback being exploited.

## 7. Read the source

Primary documents first:

- **NIST SP 800-63-4, Digital Identity Guidelines** (csrc.nist.gov, July 2025 — supersedes SP 800-63-3) — *read* the authenticator and lifecycle requirements; this is the document every mechanism choice traces to. Note the edition: the 4th revision keeps the IAL/AAL/FAL model while updating the requirements — cite the current one.
- **NIST SP 800-63B (Authentication and Lifecycle Management)** as the component volume — *read* the authenticator types and their requirements; *skip* the federation protocol message formats on first pass — come back when you implement the SSO phase, not while planning it.

Then at most three free resources:

1. **FIDO Alliance: passkeys and WebAuthn explainers** (fidoalliance.org) — free; what phishing-resistant authentication looks like to deploy: the ceremony, attestation, and the recovery problem stated honestly.
2. **OWASP Authentication Cheat Sheet** (cheatsheetseries.owasp.org) — free; the practitioner checklist — session management, credential storage, MFA implementation notes.
3. **CISA: Require Multifactor Authentication** (cisa.gov/audiences/small-and-medium-businesses/secure-your-business/require-multifactor-authentication) — free; ranks MFA methods from security key down to SMS, and states the prioritization this lesson's phasing follows: strongest available, admins first.

## 8. Check yourself

1. A company rolls out security keys to admins but keeps phone-based help-desk resets requiring only an employee ID. Explain the weaker-path failure and design the reset procedure that doesn't nullify the keys.
2. Compare passkeys and hardware security keys for the executive population: what does the key provide that the passkey doesn't, and what operational cost does it impose?
3. A biometric vendor quotes "99.9% accuracy." Explain why that number is meaningless without FAR and FRR stated separately — and what threshold decision the deployer must make.
4. The SSO migration stalls with three legacy apps that can't speak SAML. Lay out the three options (gateway, exception, replacement) and what each costs in risk versus effort.
5. Predict the state of an MFA rollout one year after phase 1, if no phase 2 was ever scheduled and exceptions never expire. Which population is unprotected, and what does the attacker target?

## 9. Prove it

**Artifact:** your authentication implementation plan — populations with impersonation impact, mechanism per population with rejected alternatives, phased rollout with support sequencing, recovery procedures attacked on paper, SSO migration with the long tail dispositioned, authenticator lifecycle with revocation SLAs, and the biometrics decision (deployed with numbers or deferred in writing) — for the Meridian worked case in your own words or a real scope you control.

**Honest claim:** "I can plan and defend an authentication rollout — I can choose the mechanism per population, sequence the phases, design the recovery paths, and operate the authenticator lifecycle."
**Can't claim yet:** "I can build the identity provider or the FIDO2 integration" — protocol implementation and IdP engineering are their own disciplines; this lesson taught the implementation decisions around them, not the code.

## 10. Leads to

- `e-iam` — the strategy and lifecycle this lesson implements; reread its weaker-path findings as this plan's threat model.
- `b-session-auth` — the failure mechanics this plan is designed to prevent; the recovery procedure's adversary.
- `a-http-depth` — the protocol layer (OAuth/OIDC flows, token handling) under the SSO implementation.
- Map refs: **CISSP 5.6** (this lesson); feeds **CISSP 5.2** (authentication strategy) and **5.5** (the provisioning lifecycle's authenticator steps).

---

*Sources fetched 2026-10-10: NIST SP 800-63-4 (csrc.nist.gov, July 2025); FIDO Alliance passkeys explainers; OWASP Authentication Cheat Sheet; CISA Require Multifactor Authentication. Full ledger in the batch manifest.*
