---
lesson_id: e-media-protection
slug: media-protection
stage: E
level: 3
prerequisites: [e-security-program]
roles: []
map_refs: ["CISSP 7.5"]
test_date: 2026-10-10
description: "How to protect the physical object — media inventory and labeling, custody in storage and transport, and sanitization per NIST SP 800-88. A free lesson in the security guidebook, serving CISSP objective 7.5."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Media protection: handling the physical object


**Map ref:** serves **CISSP objective 7.5** — protecting resources and media in operation: handling, storage, transport, and sanitization.

---

## 1. Where this shows up

Data has a body. It lives on drives, tapes, USB sticks, printed pages, and the backup media in the off-site cage — and every one of those objects can be lost, stolen, sold, or thrown away with the data still on it. Media protection is the operational discipline for the physical object: how media is labeled, who may handle it, how it's stored and transported, and how it's sanitized when its job is done. It shows up in the decommissioned server sold with customer data on the disks, in the backup tape that fell off a truck, and in the audit finding that nobody knows where the archived drives are. Operations leads, GRC analysts, and anyone running a data center or a records room live here. Note the boundary with the data lifecycle: retention schedules govern data's *life* — how long information is kept. This lesson governs the physical *object's* handling — labeling, custody, transport, and destruction. The retention schedule says "keep seven years"; media protection says "here's the labeled, locked, inventoried drive it lives on, and here's how it's destroyed in year eight."

## 2. Before you start

- You understand that handling rules derive from classification — the retention schedule says how long; this lesson says how.
- You have seen the chain-of-custody discipline in `e-investigation-forensics` — media protection applies the same custody thinking to everyday operations, not just investigations.
- No tools. The work products are documents: a media-handling procedure, a labeling scheme, a sanitization decision table, and a transport log. Primary spine: **NIST SP 800-88 Rev. 2** (Guidelines for Media Sanitization, September 2025 — Rev. 1 withdrawn September 26, 2025).

## 3. How it works

Media protection has four movements: know what you have, label it, control its custody, and sanitize it at the end.

**Inventory and labeling: you can't protect what you can't find.** The program starts with a **media inventory** — every piece of removable or portable media the organization owns, recorded with type, capacity, owner, classification of the data it holds, and location. Then **labeling**: the classification travels *on the object* — a sticker, tag, or marking stating the handling tier (e.g., CONFIDENTIAL — do not remove from the facility without authorization). Labels are the cheapest control in the discipline and the most skipped: an unlabeled drive is handled as unimportant by everyone who touches it, including the person who throws it away. The labeling scheme must be simple enough that people actually apply it — three or four tiers, visually distinct, with the handling rule printed on the label itself.

**Custody: storage and transport.** Media at rest lives in **controlled storage**: locked containers or rooms, with access limited to authorized handlers and logged. The control scales with the classification — the backup tapes for the crown-jewel system don't sit on an open shelf. Media in motion is the higher-risk state: **transport procedures** specify approved carriers or couriers, tamper-evident packaging, and a handoff log (who gave it to whom, when — the chain-of-custody discipline from `e-investigation-forensics`, applied to routine operations; chain of custody means an unbroken written record of who held the item at every moment, so any gap is visible). The classic failures are all transport failures: the tape on the passenger seat, the unencrypted USB in checked luggage, the "I'll bring the drive home and wipe it there." The procedure's answer is boring on purpose: only approved transport, only logged handoffs, no exceptions for convenience.

**Sanitization: Clear, Purge, Destroy.** When media is repurposed or retired, the data on it must be rendered unrecoverable to a level matching the information's sensitivity. SP 800-88 Rev. 2 defines three sanitization actions, and the definitions are worth quoting in paraphrase because the whole decision table hangs on them: **Clear** applies logical techniques to all user-addressable storage locations — rewriting with new values, or a factory reset where rewriting isn't supported — protecting against simple, non-invasive recovery. **Purge** applies physical or logical techniques (including firmware-level commands) that render recovery infeasible even with state-of-the-art laboratory techniques. **Destroy** renders recovery infeasible through physical destruction — disassemble, incinerate, shred, melt. The decision rule from 800-88: *think in terms of information confidentiality first, then apply considerations based on media type.* The order matters: the data's sensitivity sets how strong the sanitization must be, while the media's physics sets which techniques are possible — deciding technique first lets the feasible drive out the necessary. (The degaussed SSD is the classic result.) A hard drive leaving the organization after holding customer data gets Purged or Destroyed; the same drive moving between two equally-trusted systems inside the organization might be Cleared. And the honest edge the document states plainly: **disposal without sanitization is only acceptable when disclosure would have no impact** — no mission impact, no asset damage, no financial loss, no harm to individuals. Everything else gets sanitized, and the sanitization is **verified** — 800-88 dedicates a section to verifying equipment, personnel competence, and results, because an unverified wipe is a hope.

**Cryptographic erase and the modern footnote.** For encrypted media, destroying the keys can render the data unrecoverable — **cryptographic erase (CE)**. SP 800-88 treats CE carefully: it works only when the encryption was actually protecting the data (proper algorithms, keys never exposed, the full media encrypted including spare areas), and the document gives explicit "do not use CE" cases. The operations lesson: CE is a legitimate Purge-equivalent *when its preconditions are verified*, not a shortcut for drives you merely assume were encrypted. The procedure records the verification — key destruction witnessed, encryption scope confirmed — or it doesn't claim CE.

**Roles: sanitization is nobody's hobby.** SP 800-88 names the roles because the failures are always ownership failures: the system owner decides the sanitization level, the security officer verifies the method, property management controls the physical media, and users follow the handling rules. The procedure names names — "the IT asset manager" is a role; "Priya N." is an owner.

### Worked example: Kestrel Components — media-protection procedures

**The company (fictional).** Kestrel Components, 90 staff, precision manufacturing. Design files (the crown jewels) live on engineering workstations, a file server, nightly backup tapes, and a growing pile of retired drives in the storage room — the pile nobody owns.

**The inventory and labeling.** Every medium gets an asset tag and an entry: type, owner, data classification, location. Labels: three tiers — INTERNAL (green), CONFIDENTIAL (yellow, handling rule printed: "no removal from facility without manager approval"), RESTRICTED (red: "no removal, no copying, transport by bonded courier only" — a bonded courier is a carrier backed by a surety bond, insurance that pays if the shipment is lost or stolen, so the carrier has skin in the game). The retired-drive pile gets inventoried first — twelve drives, three still containing design data, none labeled. Finding one, recorded: the pile existed because no procedure assigned ownership of retired media.

**Custody procedures.** Backup tapes: locked safe in the server room, sign-out log, only the backup operator and the IT lead have the combination. Transport to the off-site cage: bonded courier, tamper-evident bags, handoff log signed at both ends — monthly rotation, never in personal vehicles. USB sticks: banned for RESTRICTED data entirely (the procedure says so in one line, and the DLP — Data Loss Prevention, software that watches for sensitive data leaving endpoints or the network — rule enforces it — the `e-detective-preventive` companion).

**The sanitization decision table (excerpt, fictional — per 800-88).**

| Media | Situation | Decision | Verification |
|---|---|---|---|
| HDD, engineering workstation | redeploy inside engineering | Purge (firmware command) | full read-back verify, logged |
| HDD, file server | leaves the organization (donation) | Destroy (shred) | certificate of destruction, witnessed |
| Backup tapes, expired retention | retention ended, no hold | Destroy (degauss — a strong magnetic field that scrambles magnetic media; HDDs and tapes only, useless on SSDs — + shred) | witnessed, log entry |
| SSD, laptop | employee departure | Purge; CE only if encryption preconditions verified | verification recorded or CE not claimed |
| Paper, RESTRICTED | retention ended | Destroy (cross-cut shred) | witnessed batch log |

**The transport log (excerpt, fictional):** tape set KT-2026-10-03: sealed 2026-10-03 16:40 by backup operator D. Reyes, bag seal #88412; courier pickup 17:05, signed; cage receipt 2026-10-04 09:12, seal intact, signed by cage attendant. Three lines that would have answered every question about the tape that "fell off a truck."

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the inventory scheme, custody procedures, sanitization decision table, and transport log above, authored and self-reviewed in-session on 2026-10-10 against SP 800-88 Rev. 2's decision framework. Transcript: `runs/e-media-protection.log`.

1. **Inventory the media.** For your fictional (or real) organization, list every medium: drives, tapes, USB sticks, optical, paper archives, the retired pile nobody owns. Columns: type, owner, classification, location. The unowned pile is always the first finding.
2. **Design the labeling scheme.** Three or four tiers, visually distinct, handling rule on the label. Then the honesty check: would anyone actually apply these? If the scheme needs training to understand, simplify it.
3. **Write the custody procedures.** Storage (what's locked, who has access, what's logged) and transport (approved methods, packaging, handoff log). Include the one-line bans — the prohibitions that need no nuance.
4. **Build the sanitization decision table.** Per media type and situation: Clear, Purge, or Destroy, with the 800-88 rationale (confidentiality first, media type second). Add the verification column — method, witness, record. No row without verification.
5. **Handle cryptographic erase honestly.** If you claim CE anywhere, write the preconditions you'd verify (encryption scope, key custody, algorithm) and who verifies them. If you can't verify, the decision is Purge or Destroy, not CE.
6. **Name the roles.** System owner, security verifier, property custodian, users — named people, not titles. The retired-media pile gets an owner in this step.

## 5. On your own

**Task:** Inventory your own media — old drives, USB sticks, backup disks, printed sensitive documents. For each: what's on it, where it is, what sanitization it needs. Then sanitize one item you've been meaning to deal with, using the decision table logic, and record what you did.

**Success test:** Your inventory includes at least one item whose contents you can't fully account for — that's the finding. Your sanitization record names the method and how you verified it. "I threw it away" without a method is the failure this lesson exists to prevent.

## 6. Where it goes wrong

- **The unowned pile.** Retired media with no owner and no procedure — the most common finding, and the source of most "sold with data on it" stories. Ownership is the first control.
- **Unlabeled media.** Handled as unimportant by everyone, including whoever disposes of it. The label carries the classification to the point of disposal.
- **Transport by convenience.** The passenger seat, the checked luggage, the personal vehicle. Transport is the highest-risk state; the procedure's boring answer is the protection.
- **Sanitization theater.** The "wipe" nobody verified, the degauss applied to a drive degaussing can't touch (modern high-density media), the CE claimed on an unencrypted drive. Verification is part of the method, not an optional extra — the tell is the paperwork: a disposal register with methods recorded but the verification column empty, or a certificate of destruction with no witness named.
- **Clear where Purge was needed.** Logical overwrite on media leaving the organization. The decision table exists so the choice is made by classification and media type, not by whoever has the screwdriver.
- **Disposal without decision.** Thrown away because "it's just an old drive." 800-88's bar for skipping sanitization — no impact of any kind from disclosure — is deliberately almost unreachable.
- **The hold ignored.** Media destroyed on schedule while a litigation hold was active. The retention schedule's disposal step and the legal hold must check each other — the `e-investigation-forensics` link again.

## 7. Read the source

Primary documents first:

- **NIST SP 800-88 Rev. 2, Guidelines for Media Sanitization** (csrc.nist.gov / nvlpubs.nist.gov, September 2025 — supersedes Rev. 1) — *read* the decision-flow (categorization, reuse, sanitization decision, verification, documentation) and the Clear/Purge/Destroy definitions; *skim* the media-specific technique tables.
- **NIST SP 800-53 Rev. 5, Media Protection (MP) family** — the control catalog: MP-6 (media sanitization) is this lesson in control language. Find it via the SP 800-53 publication page (csrc.nist.gov).

Then at most three free resources:

1. **NIST SP 800-111, Guide to Storage Encryption Technologies for End User Devices** (csrc.nist.gov, November 2007) — free; the encryption preconditions that make cryptographic erase an honest claim — read before you ever write "CE" in a decision table.

## 8. Check yourself

1. A company donates 40 decommissioned desktops after running a software "wipe" on each drive. Using the 800-88 decision rule (confidentiality first, media type second), explain what's wrong with this procedure — and what the verification column would have required.
2. Explain why an unlabeled drive is a handling failure even if it's stored in a locked room — whose decision does the label change, and at which lifecycle point does that matter most?
3. A laptop's SSD held customer data; IT claims cryptographic erase. Name the three preconditions 800-88 requires before CE is an honest claim, and the consequence if any one can't be verified.
4. Distinguish media protection from the data lifecycle: the retention schedule says "destroy after seven years" — what decisions does this lesson's procedure still have to make at year seven?
5. Predict the transport log of an organization with no procedure, six months after the backup rotation starts: what do the entries look like, and which entry is missing when a tape goes unaccounted for?

## 9. Prove it

**Artifact:** your media inventory (with the unowned pile found and assigned), labeling scheme, custody procedures (storage and transport with the handoff log), sanitization decision table (Clear/Purge/Destroy per media and situation, with verification per row), and named roles — for the Kestrel worked case in your own words, or better, for media you actually own.

**Honest claim:** "I can protect the physical object — inventory and label media, control its storage and transport, and decide and verify its sanitization by the book."
**Can't claim yet:** "I can run a certified destruction program" — witnessed destruction at regulatory scale, with the chain of evidence a regulator or court demands across thousands of assets, is its own operation; this lesson taught the procedure design, which is where the judgment lives.

## 10. Leads to

- `e-investigation-forensics` — chain of custody applied to investigations; the litigation hold that suspends your disposal schedule.
- `e-detective-preventive` — DLP and endpoint controls that enforce the handling rules (the USB ban needs a control behind it).
- `e-security-program` — where the handling rules get their authority and their audit.
- Map refs: **CISSP 7.5** (this lesson); feeds **CISSP 2.x** (data security) and **7.1** (investigations).

---

*Worked case authored and self-reviewed 2026-10-10; all scenario data fictional. Sources fetched in-session — see `runs/e-media-protection.log`.*
