---
lesson_id: e-asset-classification
slug: asset-classification
stage: E
level: 3
prerequisites: [e-risk-assessment]
roles: [grc-analyst]
map_refs: ["CISSP 2.1"]
test_date: 2026-10-10
description: "Build a four-tier classification scheme — tiers, examples, handling hooks, owners — anchored in impact per FIPS 199 and NIST SP 800-60. A free lesson in the security guidebook, serving CISSP objective 2.1."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Classifying information and assets: the scheme everything else hangs on


**Map ref:** serves **CISSP objective 2.1** — identifying and classifying information and assets: deciding what an organization has, what it is worth protecting, and how sensitive each thing is.

---

## 1. Where this shows up

Every security program eventually faces the question "protect what, from whom, how much?" — and every answer that skips classification is either uniform (everything gets the maximum, which nobody can afford) or arbitrary (protection follows whoever shouted loudest). Classification is the discipline that makes the answer deliberate: an inventory of information and assets, each assigned a tier that encodes how bad it would be if its confidentiality, integrity, or availability were compromised. It shows up in the data-classification policy auditors ask for first, in the "is this Restricted or just Internal?" argument between engineering and legal, in the cloud migration where nobody can say which buckets hold customer data, and in the breach notification analysis that starts by asking what classification the exposed records carried.

## 2. Before you start

- You can rate impact with reasons from `e-risk-assessment` — classification is impact rating applied to information, with organizational teeth.
- No tools. The work product is a document: a classification scheme with four tiers, examples, handling hooks, and named owners. Bring the habit of writing reasons, owners, and dates.
- Primary spine: **NIST SP 800-60 Vol. 1 Rev. 1** (Guide for Mapping Types of Information and Information Systems to Security Categories, August 2008) and **FIPS 199** (Standards for Security Categorization, February 2004). Both are free.

## 3. How it works

**Classification answers one question: what is the impact if this goes wrong?** Not "is this secret?" — impact. The federal government's formulation, which the industry's schemes all descend from, is FIPS 199: for each of three security objectives — **confidentiality** (no unauthorized disclosure), **integrity** (no unauthorized modification), **availability** (accessible when needed) — assign a potential impact of **low, moderate, or high**. A system's security category is then the triple {(confidentiality, impact), (integrity, impact), (availability, impact)}, and the overall level is the highest of the three — the high-water mark.

Three ideas in that paragraph do most of the work:

**Impact is per objective, not per thing.** A patient-results database is high confidentiality impact (disclosure harms people and triggers breach law) and high availability impact (clinicians need it during care), but its integrity impact is a separate judgment — and a public marketing site is low confidentiality, low integrity, moderate availability. Rating the thing once, on one axis, is how organizations end up encrypting the lunch menu and leaving the backup tapes in an unlocked closet.

**The high-water mark forces honesty.** The overall category is the *highest* impact across the three objectives, not the average: a system that is low confidentiality but high availability still needs high-availability controls. Averaging would let a low score cancel a high one — the mistake the formula exists to prevent.

**Aggregation changes the answer.** SP 800-60's process explicitly adjusts the provisional levels for special factors — and aggregation is the most important one: a database of one thousand records at moderate confidentiality becomes high when it holds ten million, because the impact of a breach scales with the count. The classification of a collection is not the classification of a sample. Cloud storage, data lakes, and backups are where this bites: each object looks moderate, the bucket is high.

**The commercial four-tier scheme.** Outside the federal system, organizations typically use labeled tiers. The common shape — Public, Internal, Confidential, Restricted — compresses the same impact logic into labels people will actually use. The tiers must be:

- **Ordered and few.** Four is the sweet spot: fewer and the top tier becomes a dumping ground; more and nobody can keep them straight. Each tier needs a one-sentence definition anchored in impact, not "sensitive stuff."
- **Exemplified.** Every tier carries concrete examples from the organization's own data — abstract definitions drift, examples don't.
- **Owned.** Every information type has a **data owner** — the business person accountable for classification decisions — distinct from the **custodian** (IT, who implements controls) and the **steward** (who tends data quality). Classification without an owner is a suggestion.
- **Connected to handling.** A tier that implies no handling rule is decoration. Each tier must hook to handling requirements — labeling, storage, transmission, disposal — which is the next lesson's entire subject. Write the scheme and the handling matrix together, or the scheme will never be used.

**Classification vs. categorization.** The vocabulary matters: in the NIST frame, you *classify information types* and *categorize systems* — the system's category derives from the information it holds (adjusted for its use and connectivity). In commercial speech the two words blur, but the direction is what matters: the data's sensitivity drives the system's protection level, not the other way around. A hardened server holding Public data is wasted hardening; a default-configured server holding Restricted data is the finding.

**What counts as an asset.** Information is the asset class this objective cares about most, but the inventory behind the scheme covers the containers too: systems, devices, media, software, services, credentials. You cannot protect what you have not inventoried — which is why provisioning and inventory (the third lesson) and the scheme are built together.

### Worked example: Aster Diagnostics — four-tier classification scheme

**The company (fictional).** Aster Diagnostics: 240 people, clinical lab plus a SaaS portal where patients view results. Data lives in a LIMS (lab information management system), a patient portal, a data warehouse, email, file shares, and laptops. Today: no classification; everything is treated the same, which in practice means the minimum.

**The scheme (four tiers, impact-anchored).**

| Tier | Definition (impact if confidentiality is breached) | Aster examples | Owner (role) |
|---|---|---|---|
| **Public** | Disclosure causes no harm; integrity matters more than secrecy | Marketing site, published test catalog, job postings | Marketing lead |
| **Internal** | Disclosure causes embarrassment or minor competitive harm; not regulated | Internal memos, org charts, non-sensitive operational metrics | COO |
| **Confidential** | Disclosure causes material harm: regulatory breach-notification duties, significant competitive damage, or harm to individuals | Patient lab results, employee PII (HR records), customer contracts | Chief Medical Officer (patient data); HR director (employee data) |
| **Restricted** | Disclosure causes severe harm: loss of the business's core advantage, large-scale regulatory action, or danger to individuals | Assay R&D trade secrets (proprietary test algorithms), master cryptographic keys, de-identified research datasets whose re-identification is feasible | CTO (R&D); CISO (keys) |

**Design decisions recorded (fictional, authored in-session):**

1. **Patient data is Confidential, not Restricted.** The impact analysis: disclosure triggers breach-notification law and harms individuals — squarely Confidential. Reserving Restricted for the smaller set (trade secrets, keys) keeps the top tier small enough to actually protect. A Restricted tier containing half the company's data is a tier nobody can enforce.
2. **De-identified research data is Restricted, not Internal.** Re-identification risk was the deciding factor: the dataset plus the lab's other holdings could re-identify subjects, so the *aggregate* impact is high even though each record looks anonymous. This is the aggregation adjustment from SP 800-60, applied commercially.
3. **Every type has one owner.** Dual-owned types from the first draft were split: the CMO owns the clinical content, the CTO owns the platform. The auditor's question — "who decided?" — must have one answer.
4. **The scheme hooks to handling.** Each tier row points at the handling matrix (next lesson). The scheme was not approved until the matrix existed — unhooked tiers are decoration.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" for this lesson is the classification scheme above, authored and self-reviewed in-session on 2026-10-10 against SP 800-60 Rev. 1's process. Transcript: `runs/e-asset-classification.log` (records scope, tier decisions, ownership assignments, and the review checklist — there are no commands to transcribe).

1. **Inventory the information types.** For your fictional (or real lab) organization, list every distinct type of information: customer data, employee data, financials, IP, logs, backups, credentials. Ten to twenty types is the right order of magnitude; fewer and you have missed the containers (backups, logs), more and you are listing fields instead of types.
2. **Rate impact per objective.** For each type, assign low/moderate/high for confidentiality, integrity, and availability, with a one-sentence reason each. The reasons are the work — a rating without a reason is a guess, and the review in step 5 exists to interrogate the guesses.
3. **Apply the adjustments.** Aggregation (does the collection's impact exceed any sample's?), legal/regulatory overlay (does a law set a floor?), and special factors (re-identification, key material, safety impact). Record each adjustment and why.
4. **Compress into tiers.** Group the rated types into four labeled tiers with impact-anchored definitions and organization-specific examples. If a tier holds more than half your types, split it or redefine it — the dumping-ground test.
5. **Assign one owner per type.** Name the role, not the person. Resolve every dual-ownership dispute now; the scheme is not finished while any type has two owners or none.
6. **Hook every tier to handling.** Write the one-line handling implication per tier (the full matrix is the next lesson's artifact). A tier with no handling hook goes back to step 4.

## 5. On your own

**Task:** Classify the information in a system you actually run — your homelab, your VPS, your personal cloud storage. Inventory the types (including backups and logs — the containers people forget), rate confidentiality/integrity/availability impact with reasons, compress into tiers, and name the owner of each type (you, wearing different hats, counts — write the hats down).

**Success test:** Your scheme has at least one type whose tier surprised you on first rating (the aggregation adjustment usually produces one), every type has exactly one owner, and each tier has a handling hook you could implement.

## 6. Where it goes wrong

- **The dumping-ground top tier.** Everything "important" becomes Restricted, and Restricted becomes unenforceable. The top tier must be small — if it is not, the definitions are wrong.
- **Secrecy as the only axis.** Classifying on confidentiality alone and forgetting integrity and availability. The modified lab result and the unreachable patient portal are both failures the scheme should have priced.
- **The sample-vs-collection error.** Rating one record instead of the database. Aggregation is the most common under-classification in practice, and it is exactly what breach-notification math punishes.
- **Orphan types.** Information with no owner — usually the logs, the backups, the shared drive nobody admits to creating. The inventory step exists to surface them; the ownership step exists to adopt them.
- **The unhooked scheme.** A beautiful four-tier policy that changes no handling rule. Classification that does not drive handling, provisioning, and retention is a document, not a control — the matrix in the next lesson is the enforcement.
- **Tier names without definitions.** "Confidential" meaning one thing to legal and another to engineering. The one-sentence impact definition per tier is load-bearing; the examples are the calibration. And schemes decay: data changes sensitivity over time, so the scheme needs a review trigger — the inventory audit in the provisioning lesson is one.

## 7. Read the source

Primary documents first:

- **NIST SP 800-60 Vol. 1 Rev. 1, Guide for Mapping Types of Information and Information Systems to Security Categories** (August 2008; nvlpubs.nist.gov, free) — *read* sections 3–4: the categorization process, provisional impact levels, and the adjustment factors (aggregation especially). This is the method the worked case follows.
- **FIPS Publication 199, Standards for Security Categorization of Federal Information and Information Systems** (February 2004; csrc.nist.gov, free) — *read* the whole thing; it is short. The {(confidentiality, impact), (integrity, impact), (availability, impact)} triple and the high-water-mark rule originate here.
- **NIST SP 800-53 Rev. 5** (September 2020; nvlpubs.nist.gov, free) — *skim* as the control catalog that consumes categorizations; *read* RA-2 (security categorization) to see where the scheme plugs into a control program.

Then at most three free resources:

1. **SANS Information Security Policy Templates** (sans.org, free library) — includes a data inventory management policy template; a starting skeleton for the written scheme — fill it with your own impact ratings, don't file it blank.
2. **NIST SP 800-60 Vol. 2 Rev. 1** (August 2008; nvlpubs.nist.gov, free) — the appendices: provisional impact levels for common information types, with rationale. *Use* as calibration for your own ratings, not as a substitute for them.

## 8. Check yourself

1. A database holds ten million customer records, each individually rated moderate confidentiality impact. Explain, using the aggregation adjustment, why the collection is rated high — and what changes downstream (handling, retention, breach math) when it is.
2. A de-identified research dataset is classified Internal because "no record identifies anyone." Lay out the re-identification argument that moves it to Restricted, and name the information the argument depends on.
3. Two executives both claim ownership of the patient portal's data. Explain why the scheme cannot be finished until this is resolved, and propose the split that gives the auditor one answer per data type.
4. Distinguish classifying information from categorizing a system, using the hardened-server-holding-Public-data example: what is wasted, what is missing, and which direction does the protection decision flow?
5. Predict the state of a four-tier scheme three years after its author leaves, with the top tier holding sixty percent of the company's data types and no review ever scheduled. Which failure modes from §6 are present, and which single fix addresses the most of them?

## 9. Prove it

**Artifact:** your classification scheme — the information-type inventory, per-objective impact ratings with reasons, the four tiers with impact-anchored definitions and organization-specific examples, one named owner per type, and the handling hook per tier — for the Aster worked case reproduced in your own words, or better, for a system you actually run.

**Honest claim:** "I can identify an organization's information assets and classify them by impact — I can say what each type is worth protecting, why, and who decided."
**Can't claim yet:** "I can run an enterprise data-governance program" — stewardship councils and automated discovery are their own practice; this lesson taught the scheme, where the judgment is formed.

## 10. Leads to

- `e-handling-requirements` — the handling matrix this scheme hooks to; classification without handling is decoration.
- `e-asset-provisioning` — ownership and inventory as an operating process: the scheme's owners and types become the CMDB's records.
- `e-data-lifecycle` — each classified type gets a lifecycle: retention, remanence, destruction.
- `e-risk-assessment` — the impact-rating method this lesson applies; reread it as the "how to rate honestly" companion.
- Map refs: **CISSP 2.1** (this lesson); feeds **CISSP 2.2** (handling), **2.3** (provisioning), **2.4** (lifecycle roles).
