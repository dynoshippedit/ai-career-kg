---
lesson_id: e-security-concepts
slug: security-concepts
stage: E
level: 2
prerequisites: [a-http-depth, e-crypto-applied]
roles: []
map_refs: ["CISSP 1.2"]
test_date: 2026-10-10
description: "Map a system's assets onto confidentiality, integrity, availability and the AAA properties, and name the trade-offs. A free lesson in the security guidebook, serving CISSP objective 1.2."
dateline: "Local demo run 2026-10-10 (transcript in runs/e-security-concepts.log) · worked case authored and reviewed 2026-10-10"
---
# Core security concepts: the CIA triad and the properties around it


**Map ref:** serves **CISSP objective 1.2** — core security concepts: confidentiality, integrity, availability, and related properties.

---

## 1. Where this shows up

Every security conversation you will ever have is secretly a conversation about three properties: is the data secret from the wrong people, is it unaltered by the wrong people, and is it there when the right people need it. A breach notification is a confidentiality failure. A defaced website or a tampered firmware update is an integrity failure. Ransomware is an availability failure wearing an extortion costume. Architects argue about these three properties without naming them; auditors test them; incident responders classify by them. This lesson gives you the precise vocabulary — the CIA triad plus the properties that orbit it (authentication, authorization, accountability, non-repudiation) — and the two structural ideas that organize them in real systems: defense in depth and zero trust.

## 2. Before you start

- You have watched authentication and sessions fail in `a-http-depth` — those were confidentiality and integrity failures; this lesson names the properties.
- You know what a hash function and a MAC do from `e-crypto-applied` — the §4 demo leans on both concepts without re-teaching them.
- Python 3 with the standard library is enough for the demo. No packages, no network.

## 3. How it works

**The triad.** The three properties, in the IETF's Internet Security Glossary (RFC 4949, August 2007 — the primary source for this lesson's definitions, fetched in-session):

- **Confidentiality:** information is not disclosed to unauthorized parties. The mechanism family is access control plus encryption. Note what it does *not* promise: encrypted data can still be deleted, corrupted, or withheld — confidentiality says nothing about the other two properties.
- **Integrity:** information has not been altered or destroyed in an unauthorized manner — and, in the fuller treatment, that it is authentic in origin. The mechanism family is hashes, MACs, and digital signatures. Integrity detects change; it does not prevent it.
- **Availability:** information and systems are accessible and usable when needed by authorized parties. The mechanism family is redundancy, capacity planning, backups, and denial-of-service resistance. Availability is the property organizations underinvest in until the first outage, then overinvest in until the first breach.

Each property fails independently, which is the triad's real lesson. A system can be perfectly confidential and completely unavailable (encrypted backups with the only key copy in the burning building). It can be available and integer-violated (the website is up; it is serving the attacker's content). Any control you meet in this career protects at least one of the three — ask which, and you will immediately see what it does not protect.

**The surrounding properties.** Four more complete the working vocabulary:

- **Identification** — the claim ("I am alice"). **Authentication** — the proof of the claim (password, token, key). **Authorization** — the decision about what the authenticated party may do. **Accountability** (sometimes rendered as auditing) — the record tying actions to identities. Together: IAAA, usually shortened to AAA with identification folded in. The ordering is load-bearing: every access-control failure is one of these done wrong or in the wrong order — authorizing before authenticating, or skipping accountability so no one can reconstruct what happened.
- **Non-repudiation:** the property that a party cannot later deny an action — provided by digital signatures over the action plus trustworthy time. Distinct from authentication: authentication proves who you are *now*; non-repudiation proves to a *third party, later*, that you did the thing. A login log gives you authentication; a signed contract gives you non-repudiation.
- **Privacy:** often listed alongside the triad — the individual's control over their personal information. It leans on confidentiality (as a mechanism) but adds consent, purpose limitation, and data-subject rights, which is why `e-cyber-law` treats it as a legal discipline, not just a property.

**Defense in depth.** No single control is trustworthy, so protection is layered: if one control fails, another still stands. The classic image is concentric — perimeter, network, host, application, data — but the principle is about *independence of failure*, not geometry. Five firewalls in a row are not depth; they share a failure mode (one rule mistake, one vendor bug). Depth means the layers fail differently: a WAF plus input validation plus parameterized queries is depth against injection, because the three fail for unrelated reasons. The failure mode of depth is complacency — "we have seven layers" said about seven copies of the same assumption.

**Zero trust.** The architectural answer to the perimeter's collapse: never trust, always verify. The formulation from NIST SP 800-207: no implicit trust based on network location; every access decision evaluates identity, device health, and context, continuously. Note what zero trust is not: it is not a product, and it is not the absence of trust — it is trust made explicit, narrow, and re-evaluated. Its relationship to the triad: zero trust is mostly a confidentiality-and-integrity architecture (verify the subject, verify the channel), and it *costs* availability thinking — every verification step is a new dependency that can fail closed. A zero-trust design that never considered what happens when the policy engine is unreachable has traded one availability problem for another.

**Security versus usability.** The triad's properties are in permanent tension with the humans they serve, and the tension is not a bug to fix but a constraint to design within. Confidentiality mechanisms that users cannot operate get bypassed (the encrypted USB drive left unused because mounting it takes six steps). Authentication strength beyond the user's tolerance produces password reuse and shadow IT — the security property is technically satisfied and practically void. The expert move is not to maximize any property but to find the *minimum effective* control the humans will actually sustain, and then layer depth around the residual risk. A control users bypass is not a control.

**The properties as design tensions.** Pairs of properties pull against each other, and naming the pull is the design work: confidentiality versus availability (encrypt everything, lose the keys, lose the data — key management is where this tension lives); integrity versus availability (signed updates that cannot be rolled back quickly; integrity checks that slow recovery); confidentiality versus accountability (end-to-end encryption blinds the audit log — the tension behind every "lawful access" debate). There is no universal resolution; there is only the resolution appropriate to the asset, stated with reasons.

### Local demo: integrity is a property you can watch (run 2026-10-10)

The transcript below is real — Python 3.12.3, standard library only, run in-session. Full transcript: `runs/e-security-concepts.log`.

```
message: transfer 1000 credits to account 4821
sha256 : af330fc48c17a8dd7a1fc86adf50bf2b322354d3640fcc6c15a924f8c9f2bf63
tampered: transfer 9000 credits to account 4821
sha256 : 34527aba747836546eac698342b7433db7cd7fecd33a1c9c3c38c2e73acbf493
digests equal: False
```

One changed digit — `1` to `9` — and the digest is unrecognizably different. That is the avalanche property doing integrity's detection work: any alteration, however small, is *detectable* by comparing against a trusted digest. Two honest limitations, stated now because the demo invites overclaiming: a bare hash proves nothing about *origin* — an attacker who can alter the message can recompute the hash, which is why authenticity needs a MAC or signature (your `e-crypto-applied` lesson); and detection is not prevention — integrity tells you the message changed, not how to stop it changing.

### Worked example: Harbor Clinic patient portal — the property map (fictional)

Harbor Clinic (fictional), 60 staff, is buying a patient portal: appointment booking, lab results, messaging with clinicians. The property map is the triad plus AAA applied per asset:

- **Lab results (confidentiality-critical):** encrypted in transit and at rest; access restricted to the patient and their care team (authorization); every view logged (accountability). The named tension: confidentiality versus availability — if the encryption keys are lost, results are unrecoverable, so key backup and recovery is a first-class requirement, not an afterthought.
- **Appointment records (integrity-critical):** bookings are signed by the issuing service; double-booking and silent modification are the integrity threats. Availability matters too — a down portal means phone bookings, the degraded mode.
- **The portal itself (availability-critical):** patients checking results before a procedure cannot wait. Redundancy and a tested restore (see `e-bcp-drp`).
- **Authentication:** phishing-resistant MFA for clinicians (high-impact impersonation), simpler MFA for patients (usability tension named and accepted, with depth — anomaly detection — around the residual risk).
- **Non-repudiation:** patient consent forms are digitally signed with trusted timestamps — needed later, by third parties, which authentication alone cannot provide.

Every row names the property, the mechanism, and the tension accepted. That last column is what separates a property map from a compliance checklist.

## 4. Walkthrough

**Demo lesson — one local run plus a worked case.** The "run" is the hashing demo above (executed 2026-10-10, transcript in `runs/e-security-concepts.log`) and the Harbor Clinic property map, authored and self-reviewed in-session. Steps:

1. **Run the demo yourself.** Save the script from the log, run it with `python3`, change a different character, and confirm the digest changes completely. Then break it honestly: recompute the tampered message's hash yourself and note that a bare hash would now "verify" — write one sentence on why this means hashes detect but do not authenticate.
2. **Pick a system you run.** Your homelab, your VPS, your password manager — anything with data you care about.
3. **List its assets.** Three to five: the data, the credentials, the service itself.
4. **Assign properties.** For each asset, name which of confidentiality, integrity, availability matters most, and which of identification/authentication/authorization/accountability/non-repudiation applies. If an asset needs all three of the triad equally, you have not thought about it hard enough — rank them.
5. **Name the tensions.** For each asset, write the property pair in tension (confidentiality vs availability is the classic) and the resolution you chose, with a reason. This column is the lesson's actual deliverable.
6. **Check for depth.** For your highest-ranked property per asset, list two controls that fail independently. If both fail the same way, you have one control wearing a costume.

## 5. On your own

**Task:** Write the property map for a system you actually administer (or your own workstation, treated as a system). Include: the asset list, the ranked properties per asset, the mechanisms in place, the tensions named with resolutions, and the depth check from step 6.

**Success test:** Your map contains at least one tension you resolved *against* maximum security (usability won, with compensating depth) — if every tension resolved toward more control, you designed for imaginary users. And at least one depth pair where you can articulate why the two controls fail differently.

## 6. Where it goes wrong

- **The triad as a slogan.** "We do CIA" said about a firewall and an antivirus license. The triad is an analysis tool — apply it per asset, or it is decoration.
- **Authentication confused with authorization.** Proving who you are is not permission to act. Systems that check identity and skip the authorization decision fail open by design.
- **Accountability skipped.** No logs, or logs nobody can tie to identities — then the incident review reconstructs nothing, and the same failure recurs.
- **Encryption without key management.** Confidentiality purchased, availability forfeited the day the key is lost. The key lifecycle is part of the property, not an accessory.
- **Integrity without authenticity.** Checksums and bare hashes that an attacker can recompute. Detection that the attacker controls is theater.
- **Availability without integrity.** The restore works; it restores last month's corrupted data. RTO met, RPO meaningless — `e-bcp-drp`'s territory, but the property confusion starts here.
- **Depth as duplication.** Seven layers sharing one failure mode. Ask of every layer: "if this one fails, what *different* thing catches it?"
- **Zero trust as a purchase.** A product bought, implicit trust relocated to the vendor's policy engine, availability never re-examined.
- **Usability denial.** Controls users bypass are not controls. The expert designs for the humans present, not the humans deserved.

## 7. Read the source

Primary documents first:

- **RFC 4949, Internet Security Glossary, Version 2** (IETF, August 2007; obsoletes RFC 2828) — *read* the definitions of confidentiality, integrity, availability, authentication, authorization, accountability, and non-repudiation. The working vocabulary of the field, from the body that standardizes the internet's protocols.
- **NIST CSRC Glossary** (csrc.nist.gov) — *use* as the cross-check: compare its definitions against RFC 4949's and note where they differ. Definitions drift between authorities; knowing that is part of expertise.

Then at most three free resources:

1. **NIST SP 800-12 Rev. 1, An Introduction to Information Security** (csrc.nist.gov) — free; the triad and the surrounding concepts taught as a coherent introduction — the best single free text if the RFC's glossary style is too terse.
2. **NIST SP 800-207, Zero Trust Architecture** (csrc.nist.gov) — free; the primary treatment of zero trust referenced in §3 — read the tenets before repeating the slogan.

## 8. Check yourself

1. A hospital encrypts all patient backups and stores the only decryption key on a USB drive in the server room. Name the two properties in tension, which one fails, and the mechanism that resolves the tension without weakening either.
2. Explain why a SHA-256 digest of a message gives integrity but not authenticity — and what minimal addition converts it. (Your §4 demo is the evidence.)
3. Distinguish authentication from non-repudiation using a concrete scenario: why is a login log insufficient to prove to a third party, a year later, that a specific user approved a specific transaction?
4. A vendor sells "zero trust in a box." Using the SP 800-207 tenets, name two questions that expose whether the product delivers the architecture — and the availability question the buyer must ask.
5. Predict the failure of a backup scheme that optimizes purely for availability (fastest restore, tested weekly) with no integrity property: describe the incident that reveals the gap, and which property the postmortem says was missing.

## 9. Prove it

**Artifact:** your property map (assets, ranked properties, mechanisms, named tensions with resolutions, depth check) — for the Harbor Clinic case in your own words, or better, for a system you actually run, plus your one-sentence "hashes detect but do not authenticate" note on the demo output.

**Honest claim:** "I can take a real system, map its assets onto confidentiality, integrity, availability and the AAA properties, name the tensions between properties, and check that my controls fail independently."
**Can't claim yet:** "I can architect a zero-trust enterprise" — this lesson taught the tenets and the trade-offs; designing the policy engine, the device inventory, and the failure modes at organizational scale is its own engineering discipline.

## 10. Leads to

- `e-risk-assessment`** — properties become impact: the triad is what risk analysis measures damage against.
- `e-crypto-applied`** — the mechanisms behind the properties: hashes, MACs, signatures, key management.
- **e-csf-20 — `e-governance`** — the properties as business language: what the board is actually buying.
- Map refs: **CISSP 1.2** (this lesson); feeds **CISSP 2.6** (data states and protective methods) and **3.1** (secure design principles).
