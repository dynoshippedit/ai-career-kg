# Data security controls: protecting data at rest, in transit, and in use

**ID:** `e-data-protection-controls` · **Stage:** E (Expert) · **Level:** 3 (select protective controls per data state, scope them to a requirement, and map them to compliance) · **Prerequisites:** `e-crypto-applied` (what the primitives do — this lesson is the selection view, not the primitives view); `e-asset-classification` (the tiers that set the protection level); local demo runs on your own machine.

**Map ref:** serves **CISSP objective 2.6** — data security controls and compliance: data states, scoping, standards selection, and protective methods.

---

## 1. Where this shows up

The primitives exist — encryption, hashing, access control — and the question is which to apply where. Data security controls are the selection discipline: given data in a particular state with a particular classification, which protective method, scoped to what, satisfying which requirement. It shows up in the "encrypt everything" mandate that nobody scoped, in the TLS-everywhere project that forgot the database backups, in the DLP alert queue nobody tunes, and in the breach where the data was encrypted at rest, in transit — and sitting in plaintext in application memory and logs.

## 2. Before you start

- You know what the primitives do from `e-crypto-applied` — symmetric and asymmetric encryption, hashing, signatures, PKI, and the misuses that defeat them. This lesson teaches *selection*: which control for which state, and why.
- You have classification tiers from `e-asset-classification` — the control selected depends on the tier; the lesson's worked case selects per tier per state.
- Primary spine: **NIST SP 800-111** (Guide to Storage Encryption Technologies for End User Devices, November 2007) — free; **NIST SP 800-53 Rev. 5** (SC-28, SC-8, SC-12) — free; **NIST CSF 2.0** (PR.DS) — free.

## 3. How it works

**Data has three states, and each state has different threats** — which CSF 2.0 encodes as PR.DS-01 (at rest), PR.DS-02 (in transit), PR.DS-10 (in use):

| State | Where | Threat | Control |
|---|---|---|---|
| At rest | Disk, database, backup tape | Stolen laptop, decommissioned drive | Encrypt stored data (SC-28) + access control — protects against *media* compromise, not the compromised app |
| In transit | Moving across a network | Interception, modification on the path | TLS (SC-8, internal and external) — the failure mode is partial coverage: TLS at the edge, plaintext between services |
| In use | Memory, application, screen | Compromised process, memory dump, plaintext in logs | Access enforcement, minimization, masking/tokenization — the state most programs under-protect |

**Selection, not collection.** The method per state is chosen against the classification tier and the threat: Public gets integrity protection; Confidential gets encryption in all three states; Restricted gets encryption plus need-to-know access, masking outside the vault, and no local copies. "Encrypt everything" is a slogan, not a selection.

**Scoping: the control has a boundary, and the boundary is the decision.** A control scoped to "the database" that doesn't cover the backups, the replicas, and the logs protects the database and nothing else. Under-scoping is the most common control failure — and the auditor's first question about any control is "what's in scope?"

**Standards selection: name the authority.** "We encrypt" is not a control description; "we encrypt data at rest with AES-256 via the platform's FIPS-validated module, keys in the KMS with annual rotation, per SC-28" is. Selecting the standard is a governance decision — it must be written down.

**Key management is the control behind the control.** SC-12's frame: keys are generated, distributed, stored, accessed, and destroyed per defined requirements — in an HSM/KMS (never in code), separated from the data, rotated on schedule and on compromise. The common failure is not weak algorithms — it is keys in the repository that never rotate.

**DLP: the detective control for the exfiltration path.** Data Loss Prevention monitors data in motion, in use, and at rest for policy violations — the control that catches what preventive controls miss. Taught honestly: DLP is a detection-and-response discipline, not a purchase. Its value comes from tuned policies built from the classification tiers, a staffed alert queue, and an exception process.

**Compliance mapping: the control must trace to the requirement.** Each selected control maps to the requirement it satisfies — regulation clause, contract term, framework subcategory (CSF 2.0 PR.DS gives the skeleton) — bidirectionally: requirement → control and control → requirement. The failure it prevents is the purchased-product fallacy: the tool exists, so the requirement is "met," without scoping, tuning, or evidence.

**The in-use gap deserves its own paragraph.** Every selection exercise should end with: "where is this data in plaintext, and who can see it?" Application memory, logs, caches, analytics pipelines — the in-use inventory is where the mature program spends its second year. Tokenization and masking are the characteristic controls: the application works with a token while the real value lives in the vault.

### Local demo: a data-state inventory script (run 2026-10-10)

**Setup.** A demo tree with four synthetic fixture files (invented values only). A small Python script walks the tree, matches content patterns, assigns data states by location heuristic, and prints the control each state calls for. The heuristics are labeled as heuristics — a real program would use the classification scheme and real discovery tooling. Real transcript:

```
root: /tmp/demo-d2/demo_tree
note: all findings are heuristics on SYNTHETIC fixture files

file: patient_export.csv
  content signals: looks-like-SSN
  state: at rest (on disk) -> control: encrypt (SC-28) + restrict access (MP-2/AC-3)
  state: in use (recently created/modified by a process) -> control: access enforcement (AC-3); minimize in memory

file: public_readme.md
  content signals: none
  state: at rest (on disk) -> control: encrypt (SC-28) + restrict access (MP-2/AC-3)
  state: in use (recently created/modified by a process) -> control: access enforcement (AC-3); minimize in memory

file: vault/backup_key.pem
  content signals: looks-like-private-key
  state: at rest (on disk) -> control: encrypt (SC-28) + restrict access (MP-2/AC-3)
  state: in use (recently created/modified by a process) -> control: access enforcement (AC-3); minimize in memory

file: shared/quarterly_notes.txt
  content signals: looks-like-password
  state: at rest (on disk) -> control: encrypt (SC-28) + restrict access (MP-2/AC-3)
  state: in transit (shared/copied across the network) -> control: TLS in transit (SC-8); DLP egress note
  state: in use (recently created/modified by a process) -> control: access enforcement (AC-3); minimize in memory
```

**Read the result honestly.** The script found the signals a real discovery tool would find — and its limits are the lesson: the "in use" heuristic is a teaching stand-in, not a detection; the suggestions are starting points, not selections (the demo doesn't know the classification tier); and the structural finding is that every file is in *multiple* states at once, so single-state controls always leave gaps.

Full transcript: `runs/e-data-protection-controls.log` (dated 2026-10-10; Python 3.12.3; script and fixtures synthetic, authored in-session).

### Worked example: Aster Diagnostics — control-selection matrix

**The company (fictional, continued).** For each tier, the protective method per data state, the scoping note, and the compliance mapping. Standards: NIST; algorithms and key management per SC-12 (AES-256, platform FIPS-validated modules, KMS-held keys, annual rotation, documented destruction).

| Tier | At rest (PR.DS-01) | In transit (PR.DS-02) | In use (PR.DS-10) | Scoping note | Maps to |
|---|---|---|---|---|---|
| Public | Integrity protection (signed releases, checksums) | TLS where available | Input validation; no special handling | Scope: public-facing systems only | Contractual integrity terms |
| Internal | Platform encryption + access control (AC-3) | TLS (SC-8) | Access enforcement; minimize retention in logs | Scope: company systems; excludes personal devices by policy | Internal policy |
| Confidential | Encrypted at rest (SC-28); keys in KMS, separated from data admins | TLS everywhere incl. service-to-service and replication (SC-8) | Access enforcement; masking in non-production; tokenization where feasible | Scope: LIMS, portal, warehouse, backups, replicas, logs — the copies from the lifecycle map | Breach-notification law; customer contracts |
| Restricted | Encrypted at rest; need-to-know access lists, quarterly review | TLS; no email attachments (secure transfer w/ logging) | Vault-held values; tokens outside the vault; memory hygiene; no local copies | Scope: R&D share, instrument PCs, key vault — enumerated, not described | Trade-secret protection; key-management policy |

**DLP policy sketch (tuned to the tiers):** monitor egress for Confidential and Restricted markers; block Restricted exfiltration outright, alert on Confidential; quarterly tuning review; staffed queue with 24-hour triage SLA. The policy is worthless without the last two items — stated in the document, not assumed.

**Design decisions recorded (fictional, authored in-session):**

1. **In-use gets the most new controls.** The gap analysis found at-rest and in-transit largely covered and in-use largely ungoverned. Selection follows the gap, not the slogan.
2. **The scope column enumerates.** "LIMS, portal, warehouse, backups, replicas, logs" — not "all systems."
3. **Key management is separated from data administration.** The database team does not hold the backup encryption keys.
4. **Non-production is masked.** Analytics and test environments work with masked or tokenized data — the in-use control that prevents the "it was only the dev database" breach.

## 4. Walkthrough

**Worked-case lesson — local demo run 2026-10-10.** The "run" is the inventory script above (real transcript in `runs/e-data-protection-controls.log`) plus the control-selection matrix, authored and self-reviewed in-session on 2026-10-10. Steps:

1. **Run the demo.** Build the fixture tree, run the script, read the output. Write down the script's limits.
2. **Inventory your states.** Where is sensitive data at rest (every copy — use the lifecycle map), in transit (including service-to-service and replication), in use (memory, logs, non-production).
3. **Select per tier per state.** Fill the matrix. The in-use column will be the hardest — that difficulty is the finding.
4. **Scope each control and name the standard.** Enumerate what's in: systems, flows, copies, people. Algorithm, module, key location, rotation, destruction.
5. **Sketch the DLP policy and map to requirements.** Which tiers monitored where, block vs alert, tuning cadence, who watches the queue, triage SLA — then each control traced to the requirement it satisfies, bidirectionally.

## 5. On your own

**Task:** Run the state inventory on a system you actually control — your laptop or homelab. Adapt the script (or do it by hand): list where your sensitive data rests, moves, and is used. Then answer the in-use question honestly: where is it in plaintext, and who can see it?

**Success test:** The inventory finds at least one in-use exposure you hadn't considered — plaintext in a log, an unmasked backup, a config file with a secret. Each finding gets a control decision (mask, tokenize, encrypt, delete) with a date.

## 6. Where it goes wrong

- **The single-state program.** Encrypted at rest, TLS in transit, plaintext in the logs and the analytics pipeline. Data lives in all three states; the program must cover all three.
- **Unscoped controls.** The encryption exists; the scope excludes the backups, the replicas, and the dev database. The breach path is always through the unscanned copy.
- **The purchased-product fallacy.** The DLP tool is bought, so the requirement is "met" — untuned, unwatched, unstaffed. A control without operation is a purchase order, not protection.
- **TLS at the edge only.** The front door is encrypted; service-to-service traffic and replication streams are plaintext "because it's the internal network." The internal network is not a security boundary.
- **"Encrypt everything" as strategy.** Uniform encryption without selection: effort spent where integrity was the need, gaps where in-use protection was the need. Selection follows tier, state, and threat — the matrix, not the slogan.

## 7. Read the source

Primary documents first:

- **NIST SP 800-111, Guide to Storage Encryption Technologies for End User Devices** (November 2007; nvlpubs.nist.gov, free) — *read* sections 3–4: the three solution types (full-disk, volume/virtual-disk, file/folder encryption), what each protects, and the selection guidance. Old but still the current revision; the solution-type framing transfers directly to the at-rest column.
- **NIST SP 800-53 Rev. 5** (September 2020; nvlpubs.nist.gov, free) — *read* SC-28 (protection of information at rest), SC-8 (transmission confidentiality and integrity), SC-12 (key establishment and management). These three are the at-rest, in-transit, and key-management controls in catalog language.
- **NIST CSF 2.0** (CSWP 29, February 26, 2024; nvlpubs.nist.gov, free) — *read* the Data Security category (PR.DS-01 data-at-rest, PR.DS-02 data-in-transit, PR.DS-10 data-in-use, PR.DS-11 backups): the three-state frame in framework language, and the compliance-mapping skeleton.

Then at most three free resources:

1. **OWASP Cryptographic Storage Cheat Sheet** (cheatsheetseries.owasp.org, free) — the practitioner checklist for the at-rest column: what to encrypt, how to store keys, the common mistakes.
2. **OWASP Transport Layer Protection Cheat Sheet** (cheatsheetseries.owasp.org, free) — the practitioner checklist for the in-transit column: TLS configuration, certificate handling, what to verify.

## 8. Check yourself

1. A company encrypts its database at rest and uses TLS for customer traffic, then suffers a breach via plaintext credentials in application logs. Name the data state that was unprotected, explain why neither existing control reached it, and select the control that would have (with its scope).
2. Distinguish this lesson from `e-crypto-applied` using a concrete decision: the team must protect patient data on laptops. What does each lesson contribute, and what goes wrong if only the primitives lesson is applied?
3. A compliance mapping claims "DLP requirement met" because the product is licensed. Lay out the four questions that test whether the control actually exists (tuning, staffing, scope, evidence) — and what the honest mapping says if any answer is no.
4. The scope of "encrypt backups" covers the production backup but not the dev database refreshed from it monthly. Explain the scoping failure, name the lifecycle concept it violates (the copies), and rewrite the scope line.
5. Predict the state of a data-protection program two years after its author leaves, with keys never rotated, DLP alerts unreviewed, and TLS added only at the edge: which failure is discovered first, by whom, and which single practice would have caught the most decay earliest?

## 9. Prove it

**Artifact:** your control-selection matrix — method per tier per data state, enumerated scope, named standard with key-management decisions, DLP sketch with staffing, bidirectional compliance mapping — plus the inventory-script transcript with its honestly stated limits.

**Honest claim:** "I can select data protections by state and scope them — which control protects which data in which state, what's covered, and which requirement each control satisfies."
**Can't claim yet:** "I can architect enterprise data protection at scale" — HSM operations and multi-region key management are their own engineering; this lesson taught the selection, where the judgment is formed.

## 10. Leads to

- `e-crypto-applied` — the primitives this lesson selects among; reread it as the "what the tools do" companion.
- `e-asset-classification` — the tiers the selection is made against; no tier, no selection.
- `e-data-lifecycle` — the copies the scoping must cover; the lifecycle map is the scope's source.
- `d-cloud-security` — the shared-responsibility view of the same controls in cloud infrastructure; reread for who operates what you selected.
- Map refs: **CISSP 2.6** (this lesson); also serves **CISSP 7.5** (resource and media protection — SC-28/MP controls in operations).
