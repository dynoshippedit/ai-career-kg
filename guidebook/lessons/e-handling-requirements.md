---
lesson_id: e-handling-requirements
slug: handling-requirements
stage: E
level: 3
prerequisites: [e-asset-classification]
roles: []
map_refs: ["CISSP 2.2"]
test_date: 2026-10-10
description: "Turn classification tiers into enforceable handling rules — labeling, storage, transmission, disposal — as a testable matrix. A free lesson in the security guidebook, serving CISSP objective 2.2."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Handling requirements: what each classification tier demands


**Map ref:** serves **CISSP objective 2.2** — information and asset handling requirements: the rules that turn a classification label into actual protection.

---

## 1. Where this shows up

A classification scheme says "this is Confidential." Handling requirements say what that *means* on Monday morning: how it is labeled, where it may be stored, how it may be sent, how it is destroyed — and what happens when someone does it wrong. This is the discipline behind every "do not forward" banner, every encrypted laptop mandate, every clean-desk finding, and every incident where the breach wasn't the hack but the spreadsheet emailed to a personal account.

## 2. Before you start

- You have a classification scheme with tiers, examples, and owners from `e-asset-classification` — this lesson is its enforcement arm. If your tiers have no impact-anchored definitions, fix that first; handling rules built on vague tiers are unenforceable.
- No tools. The work product is a handling matrix: tiers on one axis, handling dimensions on the other, a rule in every cell.
- Primary spine: **NIST SP 800-53 Rev. 5** (September 2020), the Media Protection family — MP-2 (media access), MP-3 (media marking), MP-4 (media storage), MP-5 (media transport), MP-6 (media sanitization), MP-7 (media use). Free.

## 3. How it works

**Handling is classification made operational.** The scheme from the last lesson is a set of labels; labels change nothing until each one implies rules a person can follow and an auditor can test. The standard structure is a matrix: one row per tier, one column per handling dimension, one rule per cell. The dimensions that matter:

**Labeling (marking).** The label must travel with the information: documents carry headers/footers with the tier, emails get classification banners, removable media gets a physical label. Two principles: the marking must be *visible enough to change behavior*, and it must be *applied at creation* — retroactive labeling of a decade of file shares is a project nobody finishes.

**Storage.** Where each tier may live, and under what protection. MP-4 (media storage) plus SC-28 (protection of information at rest) are the control homes: Confidential and Restricted live only on encrypted, access-controlled storage — no local copies on unmanaged laptops, no personal cloud drives, no USB sticks without written exception. The rule must name the *prohibited* locations, not just the approved ones, because the shadow copy is the threat: the Restricted file is safe on the encrypted share and exposed in the analyst's Downloads folder. Removable media gets its own line — allowed tiers, encryption requirement, registration — because a USB stick is storage that walks out of the building.

**Transmission.** How each tier may move. MP-5 (media transport) and SC-8 (transmission confidentiality and integrity) are the control homes: the rule names the approved channels per tier (corporate email with TLS, approved file-share links with expiry, no personal email, no consumer messaging apps for Confidential and above), and the encryption requirement (encrypted in transit, always, for the top two tiers — no exceptions for "it's just internal"). Physical transport gets a line too: couriers, registered mail, chain of custody for media leaving the building. The failure this prevents is the convenience bypass: the rule people break first is always the transmission rule, because sending is the action under time pressure.

**Disposal and destruction.** How each tier dies. MP-6 (media sanitization) and **NIST SP 800-88 Rev. 2** (September 2025) are the authorities: the matrix names the sanitization method per tier and media type — clear, purge, or destroy — and the verification the method requires. The key judgment, straight from 800-88: the method must match the *classification of the information*, not the convenience of the operator. Wiping a Restricted drive with a file-level overwrite and calling it done is the canonical failure; the matrix must say which method, applied how, verified by whom, with what record kept. Paper gets its own row — cross-cut shredding for Confidential and above, witnessed for Restricted — because the shredder next to the printer is where handling programs go to be embarrassed.

**Retention hooks.** The matrix points at the retention schedule (the fifth lesson) rather than duplicating it — but every storage rule carries the implication: data that should have been destroyed last year but sits on a backup tape is a handling failure with the retention schedule as the root cause.

**The matrix must be testable.** Every cell's rule needs a corresponding check: labeling by sampling documents; storage by scanning for tier markers on unapproved locations (this is where DLP earns its keep); transmission by reviewing egress logs and DLP blocks; disposal by the sanitization records. A rule with no check is a wish — auditors sample against the matrix, so the program must sample first.

**Exceptions are part of the design.** There will be legitimate needs to break the matrix. The handling program needs an exception process — requested in writing, time-bounded, approved by the data owner, with compensating controls — or people will break the rules silently. An undocumented exception is indistinguishable from a violation.

### Worked example: Aster Diagnostics — handling matrix

**The company (fictional, continued).** Aster Diagnostics, 240 people; four tiers from the last lesson: Public, Internal, Confidential, Restricted. The matrix below is the enforcement arm of that scheme — authored in-session, every cell a rule someone can follow and an auditor can sample.

| Dimension | Public | Internal | Confidential | Restricted |
|---|---|---|---|---|
| **Labeling** | No marking required; integrity note where it matters | Footer or banner "Internal" on documents and emails | Header/footer "Confidential — do not distribute"; email banner; file metadata where supported | "Restricted" marking plus handling caveat (e.g., "Restricted — need-to-know"); cover sheet for printed copies |
| **Storage** | Any approved location | Company-managed storage only; access-controlled shares | Encrypted at rest (SC-28); no local copies on unmanaged devices; no personal cloud; removable media only if encrypted, registered, and owner-approved | Encrypted at rest; need-to-know access lists reviewed quarterly; no removable media without CISO exception; no local copies, period |
| **Transmission** | Any channel | Company email and approved collaboration tools | Approved channels only; encrypted in transit (SC-8); no personal email or consumer messaging; file-share links expire in 7 days | Approved channels only; encrypted in transit; no email attachments — secure file transfer with access logging; physical media by bonded courier with chain of custody |
| **Disposal** | Standard deletion / recycling | Standard deletion; media reused within the company after clear-level sanitization | SP 800-88 Rev. 2: purge for reusable media, destroy for media leaving the company; paper cross-cut shredded | Purge or destroy per 800-88r2; destruction witnessed and logged; paper cross-cut shredded under witness; cryptographic erase only for validated self-encrypting drives |
| **Retention hook** | Per schedule | Per schedule | Per schedule; legal-hold override documented | Per schedule; legal-hold override documented; early destruction prohibited without owner + legal sign-off |

**Design decisions recorded (fictional, authored in-session):**

1. **Email attachments banned for Restricted.** The transmission cell is the strictest because exfiltration investigations kept finding the same pattern: the attachment, not the hack. Secure file transfer with access logging replaces the attachment — the control is auditable, the email is not.
2. **"No local copies, period" for Restricted.** The storage cell names the prohibited location explicitly. The exception process exists for the traveling researcher — encrypted laptop, time-bounded, CISO-approved — because an absolute ban with no exception process produces silent violations.
3. **Disposal methods cite 800-88 Rev. 2 by name.** The matrix does not invent sanitization methods; it points at the standard and names clear/purge/destroy per tier and media type. The verification column (who verifies, what record) is part of the rule — an unverified wipe is not a sanitization.
4. **Every cell got a check.** Labeling: quarterly document sampling. Storage: DLP scans for tier markers on unapproved locations. Transmission: egress log review plus DLP blocks. Disposal: sanitization records reviewed before asset disposal sign-off. The auditor samples; the program must sample first.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" for this lesson is the handling matrix above, authored and self-reviewed in-session on 2026-10-10 against SP 800-53 Rev. 5's MP family. Transcript: `runs/e-handling-requirements.log` (records scope, per-cell rules, the testability check, and review notes).

1. **Take your tiers.** From `e-asset-classification`'s scheme — four tiers with definitions, examples, owners. If a tier lacks examples, stop: unenforceable rules follow.
2. **Fill the labeling column.** For each tier: what marking, where it appears, when it is applied (at creation). Be specific enough that two employees mark the same document the same way — if they wouldn't, the rule is vague.
3. **Fill the storage column.** Approved locations and, more importantly, prohibited ones per tier. Name the encryption and access-control requirements; handle removable media as its own line.
4. **Fill the transmission column.** Approved channels per tier, encryption requirement, physical-transport rule. Assume time pressure: the rule must survive the employee sending it at 11 PM before a deadline.
5. **Fill the disposal column.** Sanitization method per tier and media type, citing SP 800-88 Rev. 2's clear/purge/destroy — matched to the information's classification, not the operator's convenience. Name the verifier and the record.
6. **Add the check per cell.** Every rule gets its sampling method and frequency. Then the honesty pass: pick three cells and ask "could I actually test this?" — any "no" goes back for rewriting.
7. **Write the exception process.** Requested in writing, time-bounded, owner-approved, compensating controls named. One paragraph; it prevents more violations than any rule in the matrix.

## 5. On your own

**Task:** Write the handling matrix for the system you classified in `e-asset-classification`'s exercise. Then *test three cells for real*: sample five documents for correct labeling, check one storage location for tier violations, and review your own last month of file transfers against the transmission column.

**Success test:** The self-test finds at least one violation — a mislabeled document, a file in the wrong location, a transfer through an unapproved channel. Every violation gets a fix or a documented exception with owner and date.

## 6. Where it goes wrong

- **The unmarked share.** Ten years of files with no labels, and the rule applies "going forward." The program must at least label the top tier's known locations, or the matrix protects only new data while the old data is the breach.
- **The convenience bypass.** Transmission rules die first under time pressure. If the approved channel is meaningfully harder than the forbidden one, the rule is fiction — fix the channel, not the people.
- **Sanitization theater.** The file-level overwrite on an SSD, the degaussed SSD, the recycled drive with a signed form and no verification. The method must match the media and the classification.
- **The uncheckable rule.** "Handle with appropriate care" in a cell. If the auditor cannot sample it, it is not a rule — rewrite until it is testable.
- **Paper exceptionalism.** The program covers digital media meticulously and forgets the printer, the shred bin, the whiteboard photo. Non-digital media is media; MP-6 says so explicitly.
- **Exception by silence.** No exception process, so exceptions happen without records. The program then cannot distinguish governance from violation — and neither can the auditor.

## 7. Read the source

Primary documents first:

- **NIST SP 800-53 Rev. 5** (September 2020; nvlpubs.nist.gov, free) — *read* the Media Protection family: MP-2 (media access), MP-3 (media marking), MP-4 (media storage), MP-5 (media transport), MP-6 (media sanitization), MP-7 (media use). The matrix's columns are these controls in plain language.
- **NIST SP 800-88 Rev. 2, Guidelines for Media Sanitization** (September 2025; nvlpubs.nist.gov, free) — *read* section 3 (clear, purge, destroy) for the disposal column; *note* the FAQ's point that Rev. 2 defers media-specific techniques to IEEE 2883 and organizational policy.

Then at most three free resources:

1. **NIST SP 800-88 Rev. 2 FAQ** (July 2026; csrc.nist.gov, free) — the Rev. 1 vs Rev. 2 differences and the decision-flow framing; useful when someone asks "why did the disposal rule change."
2. **SANS Information Security Policy Templates** (sans.org, free library) — media-protection and handling policy skeletons; fill with your matrix, don't file blank.

## 8. Check yourself

1. An employee emails a Confidential spreadsheet from a personal account at 11 PM to meet a deadline. Name the two matrix cells violated, explain why the transmission rule is the one people break first, and describe the fix that addresses the cause rather than punishing the employee.
2. A "sanitized" SSD is resold after a single file-level overwrite pass. Using SP 800-88 Rev. 2's definitions, explain why this fails on two independent grounds (method-vs-media and verification) — and what the matrix should have required instead.
3. Distinguish a handling rule from a handling wish: rewrite "Restricted data must be handled with appropriate care during transmission" as a testable rule, and name the check an auditor would run against it.
4. The exception process doesn't exist, and a researcher takes Restricted data to a conference on an encrypted laptop. Explain why the program cannot distinguish this from a violation, and what the one-paragraph exception process changes.
5. Predict the state of a handling program two years after its author leaves, with the matrix unchanged, DLP never tuned, and no cell ever sampled: which column decays first, what incident reveals the decay, and which single practice would have caught it earliest?

## 9. Prove it

**Artifact:** your handling matrix — tiers by labeling, storage, transmission, and disposal rules, each cell testable, each tier's disposal method citing SP 800-88 Rev. 2, plus the exception process — for the Aster worked case in your own words, or better, for a system you actually run, with three cells self-tested.

**Honest claim:** "I can turn a classification scheme into enforceable handling rules — what each tier demands for labeling, storage, transmission, and disposal, and how each rule is checked."
**Can't claim yet:** "I can operate enterprise DLP" — tuning detection and managing false positives across a fleet are operational disciplines; this lesson taught the rules the operations enforce.

## 10. Leads to

- `e-asset-classification` — the scheme this matrix enforces; reread it as the "what the labels mean" companion.
- `e-data-lifecycle` — disposal is one lifecycle stage; the lifecycle map shows where handling hands off to retention and destruction.
- `e-retention-eol` — the retention schedule the matrix's retention hooks point to.
- `e-data-protection-controls` — the technical controls (encryption per state, DLP) that implement the matrix's storage and transmission columns.
- Map refs: **CISSP 2.2** (this lesson); feeds **CISSP 2.4** (destruction), **2.6** (protective controls), **7.5** (media protection).
