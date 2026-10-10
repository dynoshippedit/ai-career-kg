# Content-depth audit: Stage D + Stage E (first half) — DEa batch

Auditor: subagent (session a04bfe8c) · 2026-10-10 ~02:00–03:00 EDT
Scope: the 34 lessons listed in the dispatch brief (d-* × 6, e-* × 28).
Method: every lesson file read in full; word count, level, stage, section count checked by script; load-bearing factual claims spot-verified in-session against primary sources (CSRC/NIST/CSRC DOI records via search + page reads). Bar: brief §1 (L1–L4), §6 ("If you can't fill 'How it works' and 'Walkthrough' with substance, that is a gap. Log it. Don't pad."), §7 (voice/evidence/safety).

## Summary

- **SOLID: 34 of 34.** Every lesson is deep at its stated level. Word counts run 2,111–2,768 (see table). All have exactly 10 `##` sections, working frontmatter, a run-or-worked-case walkthrough with honest limits, "Prove it" artifacts, and honest-claim statements.
- **DEEPEN for thinness: 0.** The pad-free rule holds — none of these are thin at their level.
- **Genuine corrections applied (Phase 2, not padding):** 4 small factual/formatting fixes across 6 lesson files (listed below).
- **Cross-cutting flag for the coordinator (NOT changed):** legacy lesson-ID scheme in "Leads to" sections (E-GOV-01, E-D7-10, E-D2-06, E-D3-01, E-AI-01, C-CVD-01, B-BTY-01, D-DFIR, C-IR, E-LEAD, E-GOV-AI, E-D1-08, E-D7-03) appears in both this batch's lessons and other workers' lessons (e-risk-assessment, e-sdlc, e-security-concepts). Needs a coordinator decision on normalizing to the `e-`/`c-`/`b-`/`ai-` slug scheme — do not edit per-lesson until decided.

## Verdict table

| lesson_id | words | level | verdict | notes |
|---|---|---|---|---|
| d-appsec | 2427 | 3 | SOLID | STRIDE worked case + 4 scanner families + SDLC gates + code review; real Semgrep 1.180.0 run compared against teaching sketch; honest "cannot yet claim" |
| d-cloud-security | 2361 | 3 | SOLID | Shared-responsibility line, IAM escalation via Cloudsplaining (real run), 5 misconfigs, Prowler/ScoutSuite reader-side with exact commands |
| d-dfir-deep | 2529 | 3 | SOLID | Volatility-order collection, disk/memory/network tiers, hunting hypothesis discipline; timeline built from labeled synthetic data (real run) |
| d-exploit-concepts | 2111 | 3 | SOLID | Flaw-to-control chain, 4+2 mitigation survey (ASLR + checksec run live); exploitation strictly reader-side on pwn.college per safety line |
| d-malware-analysis | 2420 | 3 | SOLID | Triage workflow, real YARA run with false-positive demo (tighten/loosen/retune); detonation reader-side in isolated lab |
| d-redteam-concepts | 2573 | 2 | SOLID | L2 stated honestly; ATT&CK v19.2 15-tactic split taught (14-tactic lists flagged stale); beaconing statistics run locally; emulation reader-side |
| e-arch-vuln-assessment | 2517 | 3 | SOLID | 7 findings with blast-radius + structural-persistence modifiers; foundation-first priority logic |
| e-assessment-strategy | 2167 | 3 | SOLID | SP 800-115 §6 spine; internal/external/third-party assessor classes; 4 testing viewpoints; retest commitments |
| e-asset-classification | 2463 | 3 | SOLID | FIPS 199 triple + high-water mark + aggregation adjustment (SP 800-60); 4-tier scheme with owners and handling hooks |
| e-asset-provisioning | 2460 | 3 | SOLID | CSF 2.0 ID.AM-01..08; CM-8 record definition; inventory audit with 5 findings incl. ghost server |
| e-auth-systems | 2379 | 3 | SOLID | SP 800-63-4 (verified July 2025 final); MFA phasing; passwordless/FIDO2; biometrics FAR/FRR/template decision; SSO long tail; authenticator lifecycle |
| e-awareness-training | 2318 | 3 | SOLID | SP 800-50 Rev. 1 (verified Sept 2024); CPLP framing; behavior-not-completion metrics; phishing-sim ROE |
| e-bcp-drp | 2600 | 3 | SOLID | BIA → RTO/RPO decisions → strategy per process → plan excerpt → tabletop with injects; SP 800-34 Rev. 1 age flagged honestly |
| e-board-communication | 2115 | 3 | SOLID | One-page memo as artifact; CSF 2.0 §5 translation rule; director test; labeled placeholders, no invented numbers |
| e-change-management | 2295 | 3 | SOLID | 3 reviewed change requests (approve/reject/conditions) with rationale; emergency path with spine; SP 800-128/CM-3 |
| e-config-management | 2297 | 3 | SOLID | Real drift-demo run (baseline + tamper + detect); CIS Benchmark apply/adapt/exception; 2011-vintage SP 800-128 translated for cloud/container |
| e-control-selection | 2512 | 3 | SOLID | Testable requirements → 800-53 selection + tailoring vocabulary → traceability matrix → defended omissions |
| e-control-testing | 2246 | 3 | SOLID | SP 800-115 §§3–5 method catalog; what-each-method-proves discipline; cheap-before-expensive sequencing |
| e-cryptanalysis | 2480 | 3 | SOLID | 3 real demos (brute-force table, birthday bound P(collision)=0.3935 at 2^32, Caesar break); differential/linear as concepts; side channels; per-method defense |
| e-crypto-applied | 2157 | 3 | SOLID | Real OpenSSL runs: avalanche, ECB-vs-CBC (the persuasive demo), sign/verify, cert path validation, TLS 1.3 handshake on loopback |
| e-csf-20 | 2322 | 3 | SOLID | CSWP 29 Feb 2024; 6 Functions / 22 Categories / 106 Subcategories; Current-vs-Target profiles; Tiers as communication aid; "no CSF certification" stated |
| e-cyber-law | 2497 | 3 | SOLID | GDPR Arts 5,6,7,33–35,37,38,83 + Ch.V read from EUR-Lex; EU AI Act 2024/1689 verified; obligation-to-evidence matrix |
| e-data-lifecycle | 2460 | 3 | SOLID | SP 800-88 Rev. 2 (verified final 26 Sept 2025) Clear/Purge/Destroy + Rev. 2 folklore corrections; local deletion-vs-overwrite demo run |
| e-data-protection-controls | 2450 | 3 | SOLID | Per-tier-per-state selection matrix (PR.DS-01/02/10); scoping discipline; in-use gap paragraph; DLP as staffed discipline |
| e-detective-preventive | 2425 | 3 | SOLID | IDS/IPS placement + tuning (SP 800-94 age flagged); honeypot fidelity/placement/monitoring; DLP monitor-only-first; allow-listing |
| e-ethics | 2509 | 2 | SOLID | L2 honest; ISC2 four canons in priority order; two argued dilemmas with named decisions and costs; ACM comparison |
| e-facility-controls | 2460 | 3 | SOLID | 5-family checklist with F-01..F-05 findings, owners, dates; maintenance/testing as the gap pattern |
| e-facility-design | 2532 | 3 | SOLID | CPTED four per space; layered defense deter/delay/detect; 6 site-selection factors; design-phase cost advantage |
| e-governance | 2518 | 3 | SOLID | Govern (GV) function; reporting-line analysis; risk appetite; framework rationale (CSF 2.0 vs ISO 27001 vs SOC 2); charter |
| e-handling-requirements | 2448 | 3 | SOLID | Full tier×dimension handling matrix (labeling/storage/transmission/disposal); every cell testable; exception process |
| e-iam | 2768 | 3 | SOLID | Joiner-mover-leaver + service accounts; assurance per population; federation; RBAC/ABAC; privileged access; access review with 6 findings. **FIXED:** duplicate `cloud-security` in roles frontmatter; corrected 5.6 map-ref parenthetical (see below) |
| e-incident-management | 2430 | 3 | SOLID | SP 800-61 Rev. 3 (verified final 3 April 2025); team charter; severity matrix; comms plan; improvement metrics |
| e-investigation-forensics | 2508 | 3 | SOLID | SP 800-86 four phases; RFC 3227 volatility order; chain of custody; counsel/law-enforcement decisions; NIJ first-responder guidance |
| e-investigations | 2500 | 3 | SOLID | Admin/criminal/civil/regulatory decision tree; type-stacking + sequencing; highest-standard evidence rule; 3 scenarios |

## Factual verification (done in-session, primary sources)

All verified via NIST/CSRC records — no stale claims found:
- **SP 800-63-4** final **July 2025**, supersedes 800-63-3 (withdrawn Aug 1, 2025); IAL/AAL/FAL assurance levels carried forward (§3.3.1). Lesson claims correct.
- **SP 800-88 Rev. 2** final **Sept 26, 2025**, supersedes Rev. 1. Lesson claims correct (incl. July 2026 FAQ planning note on the CSRC page).
- **SP 800-61 Rev. 3** final **April 3, 2025**, supersedes Rev. 2, CSF 2.0-aligned. Lesson claims correct.
- **SP 800-50 Rev. 1** released **Sept 12, 2024**. Lesson claims correct.

## Corrections applied in Phase 2 (genuine bugs, not padding)

1. **e-iam.md frontmatter:** `roles: [cloud-security, cloud-security, iam-engineer]` → `roles: [cloud-security, iam-engineer]` (duplicate value would double-count the lesson in the cloud-security path).
2. **e-iam.md §"Map ref":** "(Objective 5.6, implementing authentication systems, is taught hands-on in Stage A and Stage D.)" → "(Objective 5.6, implementing authentication systems, is taught in `e-auth-systems`.)" — the old parenthetical was factually wrong and contradicted this batch's own e-auth-systems lesson.
3. **Malformed markdown (mixed backtick/bold) in "Leads to" bullets** — fixed to clean `` `slug` `` form in: e-awareness-training (1), e-cyber-law (2), e-governance (1), e-investigations (2).
4. **e-facility-design.md §7:** "FEMA: How to Use a Portable Fire Extinguisher (fema.gov via wsu.edu)" → "(fema.gov)" — normalized to match e-facility-controls' citation of the same source.

No source-ledger rows added: none of the corrections introduce new factual claims (fix #2 cites a lesson that exists in this batch; the rest are formatting/dupe removals). The four verification rows above are staged in `/tmp/sources-add-DEa.csv` for the merge-owner's convenience.

## Cross-cutting finding for the coordinator (flagged, not changed)

- **Legacy lesson-ID scheme in "Leads to"** (E-GOV-01, E-D7-10, E-D2-06, E-D3-01, E-AI-01, E-D1-08, E-D7-03, C-CVD-01, C-IR, B-BTY-01, D-DFIR, E-LEAD, E-GOV-AI) appears in this batch AND in other workers' lessons (e-risk-assessment, e-sdlc, e-security-concepts). Normalize centrally; per-lesson edits would race with other workers.
- **Spot-checked sibling references resolve:** `e-sdlc`, `e-secure-design`, `e-data-protection-controls`, `e-governance`, `e-media-protection`, `e-secops-concepts`, `e-security-program`, `e-policy-docs`, `e-logging-monitoring`, `e-risk-assessment`, `e-board-communication`, `e-personnel-security` all exist as files (55 `e-` lessons in the dir). `e-security-audits`, `e-security-metrics`, `e-test-analysis-reporting` (referenced by e-assessment-strategy/e-control-testing) also exist.
- **e-bcp-drp §10 "E-GOV-01 — NIST CSF 2.0" + "E-D7-10 — Recovery strategies"**: second one has no clear slug counterpart — covered by the coordinator flag.
