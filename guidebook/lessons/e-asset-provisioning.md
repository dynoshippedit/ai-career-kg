---
lesson_id: e-asset-provisioning
slug: asset-provisioning
stage: E
level: 3
prerequisites: [e-asset-classification]
roles: []
map_refs: ["CISSP 2.3"]
test_date: 2026-10-10
description: "Design a provisioning workflow with ownership assignment and run an inventory audit that reconciles against the CMDB. A free lesson in the security guidebook, serving CISSP objective 2.3."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Secure provisioning: ownership, inventory, and the CMDB


**Map ref:** serves **CISSP objective 2.3** — secure provisioning of information and assets: ownership assignment, inventory, and asset management across the asset's life in the organization.

---

## 1. Where this shows up

Every asset the organization owns was acquired, configured, assigned, and — eventually — retired by some process, or by no process at all. Provisioning is the discipline that makes it a process: the workflow that brings an asset into the environment securely, records it, assigns it an owner, and keeps that record true until the asset leaves. It shows up in the laptop that arrives with a standard image instead of a factory install, in the cloud account nobody can say who created, in the audit finding "47 devices on the network are not in the inventory," and in the decommissioned server still holding customer data because nobody owned its retirement.

## 2. Before you start

- You have the classification scheme from `e-asset-classification` — provisioning records each asset's tier and owner at birth. Without the scheme, the inventory is a list without meaning.
- No tools. The work products are documents: a provisioning workflow and a completed inventory audit with reconciled findings.
- Primary spine: **NIST CSF 2.0** (CSWP 29, February 26, 2024), the Identify function's Asset Management category (ID.AM) — free; and **NIST SP 800-53 Rev. 5** (September 2020), CM-8 (system component inventory) — free.

## 3. How it works

**Provisioning is birth with paperwork.** An asset enters the organization through one of a few gates — purchase, cloud creation, employee onboarding (BYOD or issued device), software deployment, data acquisition — and each gate needs the same workflow: request, approval, secure configuration, recording, owner assignment, deployment, verification. The security content of each step:

- **Request and approval.** Who may ask for an asset, and who approves. Unapproved assets are shadow IT by definition, and shadow IT is inventory's permanent enemy.
- **Secure configuration.** The asset is built to a known-good baseline before it touches production: hardened image, patched, encrypted storage, logging enabled, default credentials replaced.
- **Recording.** The asset enters the inventory with its identity: what it is, where it is, what it holds, its classification tier, its owner, its expected lifespan. CM-8's requirements are the checklist: the inventory must accurately reflect the system, include all components, avoid duplicate accounting, be at the granularity needed for tracking, and carry the accountability information the organization defines. "The spreadsheet" fails most of these; the lesson's position is that the inventory must be a system of record, not a file.
- **Owner assignment.** Every asset gets exactly one owner — the person accountable for its protection decisions — at provisioning time, not later. The classification lesson assigned owners to *information types*; provisioning assigns owners to *assets*. The two meet in the record: this laptop (asset) holds Confidential patient data (type) owned by the CMO, while the laptop itself is owned by its assigned user under IT's custodianship.
- **Verification.** Someone confirms the asset matches its record: right configuration, right owner, right location, logging working. Unverified provisioning is how the inventory and reality diverge on day one.

**The inventory is a living record, not a list.** CSF 2.0's ID.AM says what "living" means: ID.AM-01/02 (inventories of hardware, software, services, and systems are *maintained* — present tense, ongoing), ID.AM-03 (network communication and data flows represented), ID.AM-04 (supplier services inventoried), ID.AM-05 (assets prioritized by classification, criticality, resources, and mission impact), ID.AM-07 (inventories of data and metadata for designated data types), ID.AM-08 (everything managed throughout its lifecycle). Note ID.AM-05: the inventory is *prioritized*, not flat — classification flows into the inventory and tells the organization which assets matter most. And ID.AM-08 closes the loop: the inventory follows the asset from provisioning to decommissioning.

**The CMDB is the inventory grown up.** A Configuration Management Database records not just assets but their relationships: this application runs on these servers, depends on this database, holds this data. The CMDB is what turns "which systems hold Restricted assay data?" from a week-long investigation into a query. Its failure modes are well known: stale (nobody updates it on change — the number-one CMDB killer) and disconnected (the cloud inventory and the on-prem inventory never meet). The discipline that keeps it alive is the same as the inventory's: updates driven by the change process, audited by reconciliation.

**The inventory audit is the reconciliation.** Periodically — and always before an audit or a major change — the organization reconciles the record against reality: network discovery vs. the CMDB, purchase records vs. deployed assets, assigned owners vs. the HR roster (departed owners are orphaned assets), data-flow diagrams vs. actual traffic. Every discrepancy is a finding with a decision, an owner, and a date — the same discipline as the access review in `e-iam`. The audit is also where shadow IT surfaces: the discovered asset with no record is either provisioned properly now or removed.

**Deprovisioning closes the loop.** Provisioning's mirror: when an asset leaves service, data is sanitized per the handling matrix (SP 800-88 Rev. 2), the CMDB record is marked retired with history retained, credentials are revoked, and the owner is released. The asset that skips deprovisioning becomes the ghost server: unpatched, unmonitored, still holding data.

### Worked example: Aster Diagnostics — provisioning workflow and inventory audit

**The company (fictional, continued).** Aster Diagnostics, 240 people. Today: laptops are imaged by IT from a checklist (good), cloud resources are created by any engineer with console access (bad — no approval, no record), and the "inventory" is a spreadsheet last reconciled fourteen months ago.

**The provisioning workflow (all asset classes, one gate each).**

1. **Request.** Ticket in the ITSM system: what, why, which project, requested owner. Cloud resources: requested through the same ticket — the console's "create" button is not a request process.
2. **Approval.** Manager approval for standard items; security review for anything holding Confidential or above, anything internet-facing, anything processing patient data. Approval records the classification tier the asset will hold.
3. **Secure build.** Laptops: standard hardened image (encrypted disk, EDR, logging). Servers/cloud: baseline template from the hardened catalog — no hand-built production systems. Credentials: no defaults; secrets in the vault from birth.
4. **Record.** CMDB entry created *before* deployment: asset ID, type, location, owner, classification tier of data it will hold, expected lifespan, related assets (which system it belongs to, which data flows through it).
5. **Deploy and verify.** Asset goes live; a second person (or automated check) verifies configuration matches baseline, logging is flowing, and the CMDB record is accurate. Verification is a checklist item, not a hope.
6. **Change-driven updates.** Every subsequent change (move, reimage, repurpose, owner change) updates the CMDB record as part of the change ticket — the change process feeds the inventory, which is the only sustainable way to keep it current.
7. **Deprovision.** Retirement ticket: data sanitized per the handling matrix, CMDB record marked retired (not deleted — the history matters for forensics and audits), credentials revoked, owner released.

**The inventory audit (one quarter's run, fictional).** Method: automated network discovery plus cloud-account enumeration, reconciled against the CMDB; purchase records sampled against deployed assets; owner list checked against the HR roster.

Findings (fictional, labeled):

1. **Shadow cloud:** 23 cloud instances with no CMDB record, created directly in the console over six months. *Decision: 17 claimed by project owners and provisioned retroactively through the workflow (recorded, owners assigned, baselines verified); 6 with no claimant shut down after data review.*
2. **Stale ownership:** 31 assets owned by departed employees. *Decision: ownership transferred to current team leads within two weeks; HR-feed trigger added so departures reassign asset ownership automatically.*
3. **Ghost server:** a decommissioned lab server still powered on, still on the network, holding Confidential patient data from 2024 — it never got a retirement ticket. *Decision: data sanitized per 800-88r2, server decommissioned properly, CMDB history retained; retirement-ticket requirement added to the decommissioning checklist.*
4. **Duplicate accounting:** 14 laptops recorded in both the CMDB and the old spreadsheet, with conflicting owners. *Decision: spreadsheet retired as a system of record; CMDB declared authoritative; duplicates merged with the verified owner.*
5. **Unverified builds:** 9 servers deployed in the last quarter with no verification record. *Decision: verified retroactively (2 needed remediation); verification checklist made a merge-gate — no record, no production.*

**Audit close-out:** every finding has a decision, an owner, and a date. The next audit is scheduled (quarterly discovery reconciliation; annual full audit). The CMDB is declared the authoritative inventory — one system of record, which is the finding that fixes findings 1 and 4 structurally.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" for this lesson is the provisioning workflow and inventory audit above, authored and self-reviewed in-session on 2026-10-10 against CSF 2.0 ID.AM and SP 800-53 CM-8. Transcript: `runs/e-asset-provisioning.log` (records scope, workflow design decisions, audit findings, and review notes).

1. **Map the gates.** For your fictional (or real lab) organization, list every way an asset enters: purchase, cloud creation, onboarding, software install, data acquisition. For each gate, answer: is there a request process, an approval, a secure build, a record, an owner, a verification? The gates with no process are your shadow-IT surface.
2. **Write the workflow.** Seven steps as above, adapted to your scale. The non-negotiables: approval records the classification tier; the CMDB record is created before deployment; verification is a checklist item; changes update the record.
3. **Define the record.** What fields the inventory carries per asset (identity, location, owner, tier, lifespan, relationships). CM-8's test: accurate, complete, no duplicates, right granularity, accountability information present.
4. **Run the audit.** Reconcile discovery against the record, purchases against deployments, owners against the roster. Drive each discrepancy to a decision with an owner and a date.
5. **Close the loop.** Deprovisioning workflow: sanitize, mark retired (never delete the history), revoke, release. Then schedule the next audit and declare the authoritative system of record.

## 5. On your own

**Task:** Run an inventory audit on systems you actually control — your homelab, your VPS fleet, your cloud account. Reconcile what you can discover (running instances, installed machines, registered domains) against what you have recorded (notes, docs, memory). Then write the provisioning checklist you will follow for the next asset you create.

**Success test:** The audit finds at least one asset you forgot you had, or one record that is wrong about an asset's purpose or owner. Every discrepancy gets a decision (record it properly or decommission it) with a date.

## 6. Where it goes wrong

- **The spreadsheet of record.** A file that one person updates, nobody audits, and fourteen months of drift turns into fiction. The inventory must be a system with change-driven updates, not a document.
- **Cloud exceptionalism.** "The CMDB is for physical stuff." Cloud assets are assets — ID.AM-02 says software, services, and systems, with no on-prem qualifier. The console's create button is the largest ungoverned provisioning gate in most organizations.
- **Ownerless assets.** Everything has an owner on paper; the paper names someone who left two years ago. Ownership must be re-validated against the roster, and departures must trigger reassignment.
- **The ghost fleet.** Retired-in-name-only assets: powered on, unpatched, holding data. Deprovisioning is a workflow with a ticket, not an intention.
- **Duplicate accounting.** The same asset in two systems with two owners — CM-8 names this explicitly as a failure. One authoritative system of record; everything else is a view.

## 7. Read the source

Primary documents first:

- **NIST CSF 2.0** (CSWP 29, February 26, 2024; nvlpubs.nist.gov, free) — *read* the Identify function's Asset Management category (ID.AM-01 through ID.AM-08): the maintained inventories, the prioritization by classification (ID.AM-05), the lifecycle management (ID.AM-08). This is the inventory program in framework language.
- **NIST SP 800-53 Rev. 5** (September 2020; nvlpubs.nist.gov, free) — *read* CM-8 (system component inventory): the accuracy, completeness, no-duplicate-accounting, and review requirements. The worked case's record definition is CM-8 operationalized.
- **NIST SP 800-88 Rev. 2** (September 2025; nvlpubs.nist.gov, free) — *skim* for the deprovisioning step: the sanitization methods the retirement ticket invokes.

Then at most three free resources:

1. **SANS Data Inventory Management Policy template** (sans.org, free) — a starting skeleton for the written inventory policy; fill it with your record definition, don't file it blank.
2. **SANS Information Security Policy Templates** (sans.org, free library) — the broader set for the provisioning workflow's policy home.

## 8. Check yourself

1. An engineer creates 23 cloud instances directly in the console over six months; none are in the CMDB. Name the workflow gate that failed, explain why "we'll record them later" structurally guarantees recurrence, and describe the fix that addresses the gate rather than the instances.
2. A decommissioned server is found still powered on and holding Confidential data. Explain why this is a provisioning-process failure rather than a one-off mistake, naming the missing workflow step and the record-keeping rule it violates.
3. Distinguish the data owner from the asset owner using the laptop-holding-patient-data example: who decides the data's classification, who is accountable for the laptop's protection, and where do the two records meet?
4. The CMDB has forty fields per asset and nobody trusts it. Explain the failure (over-detail), what it costs (false confidence), and the minimal field set that restores trust.
5. Predict the state of an inventory program two years after its author leaves, with change tickets no longer updating the CMDB and no audit ever scheduled: which ID.AM subcategory fails first, what discovers the failure, and which single practice would have prevented the drift?

## 9. Prove it

**Artifact:** your provisioning workflow (the gates, the seven steps, the record definition, the deprovisioning close-out) plus a completed inventory audit — for the Aster worked case in your own words, or better, for systems you actually control.

**Honest claim:** "I can bring assets into an environment securely and keep the inventory honest — the provisioning workflow, ownership assignment, and the audit that reconciles the record against reality."
**Can't claim yet:** "I can run enterprise IT asset management" — procurement integration and software-license compliance are their own operations; this lesson taught the security core they rest on.

## 10. Leads to

- `e-asset-classification` — the tiers and owners the provisioning record carries; the inventory without the scheme is a list without meaning.
- `e-handling-requirements` — the handling matrix the deprovisioning step invokes; retirement without sanitization is abandonment.
- `e-data-lifecycle` — the asset's data gets its own lifecycle; the two records (asset, data) meet at decommissioning.
- `e-iam` — the HR-feed pattern for ownership reassignment; the same authoritative-source discipline applied to assets.
- Map refs: **CISSP 2.3** (this lesson); feeds **CISSP 2.4** (destruction at retirement), **2.5** (end-of-life), **7.5** (resource protection).
