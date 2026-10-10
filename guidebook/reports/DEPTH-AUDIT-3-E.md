# Depth audit 3 — Stage E (55 lessons), three new lenses — 2026-10-10

Auditor: subagent (session d906337c) · 2026-10-10 ~01:45–03:30 EDT.
Scope: all 55 `e-*.md` lessons. DEPTH-AUDIT-2 (DEa/DEb) work was skimmed and not repeated — this pass uses three NEW lenses only.

**Lenses:** L1 = scope completeness (each lesson's map_refs objective(s) actually taught at managerial/architectural breadth; the §5 framework trio checklist). L2 = prerequisite chain integrity (read every lesson in each lesson's frontmatter prerequisites; forward references, orphan assumptions, prereqs that don't deliver). L3 = exercise quality (§8 no-recall rule, §5 reader-verifiable success tests, §9 unaided-application artifacts).

**Result: 24 of 55 lessons edited.** L1 fired on 1/55 (e-soc2). L2 fired on 15/55. L3 fired on 4/55 (§9 rewrites/sharpening). 5 more files got drive-by formatting fixes only (no lens fired). §8 and §5 were audited across all 55 and passed everywhere — details below.

## Lens 1 — scope completeness

Every lesson's named CISSP objective(s) were checked against the body. Verdicts: all 55 teach their objective's substance at managerial/architectural breadth (paraphrased, no outline text). Spot-checked multi-objective lessons: e-iam teaches 5.1–5.5 (lifecycle, assurance strategy, federation/IAL-AAL-FAL, RBAC/ABAC, privileged access); e-sdlc covers the guidebook's own 8.1–8.5 map phrases (SDLC phases, SSDF, effectiveness metrics, acquirer vocabulary, secure coding as policy); e-bcp-drp covers 1.7 + 7.10–7.13 (BIA, RTO/RPO, BC vs DR, strategies, plans, test ladder, backups). The §5 "worked work-products" checklist is complete: risk register (e-risk-assessment), BIA (e-bcp-drp), access review (e-iam), audit plan (e-security-audits), board memo (e-board-communication).

One genuine gap found: **no lesson taught the three governance frameworks' relationship.** e-csf-20 teaches what CSF 2.0 is; e-iso27001 teaches what 27001 is, one-lines the paid-standard rule, and relates to the CSF; e-soc2 teaches what SOC 2 is and relates to 27001's SoA. But nowhere did the guidebook say, in one place, what each IS, WHO needs it, and HOW the three relate to each other. **Added** a "The three frameworks side by side" paragraph to e-soc2 §3: CSF = voluntary outcomes language (no certification) for orgs wanting a shared risk vocabulary; 27001 = certifiable ISMS + Annex A catalog for orgs whose customers/regulators expect an audited ISMS; SOC 2 = CPA attestation report for service organizations whose customers demand third-party assurance. Relations: CSF Informative References map Subcategories to 27001 controls (one control selection serves both); the 27001 SoA's selected controls become the SOC 2 engagement's tested controls; one evidence base can serve all three, purposes stay distinct (CSF communicates, 27001 manages, SOC 2 attests). No new external claims — derived from the three lessons' existing content.

## Lens 2 — prerequisite chain integrity

Scripted check: extracted each lesson's §2 and flagged every backticked lesson reference not in its frontmatter `prerequisites`. 15 lessons had extras; each was read in context and fixed by **fixing the reference** (rewording assumed-prior-learning into companion pointers, adding inline micro-foundations where the concept was load-bearing). No frontmatter prereq lists were changed. Prereq *delivery* was also checked the other direction (does the prereq teach what the lesson expects — e.g., e-auth-systems expects JML + assurance levels from e-iam, TLS handshake from a-http-depth; e-security-concepts expects hash/MAC from e-crypto-applied; e-threat-modeling-concepts expects STRIDE from e-sdlc): all prereqs deliver. Orphan-assumption sweep (concepts used but taught nowhere): none found — ITAF, ZTMM, RACI, SP 800-160, CPLP, SoA, KEV, FIPS 199 are all defined at first use. e-secops-concepts §2 was already the honest pattern ("control-type vocabulary at least by reputation; e-detective-preventive (same batch) goes deep") and was left alone.

## Lens 3 — exercise quality

- **§8 "Check yourself": all 55 pass.** Every question demands explaining, arguing, distinguishing, designing, or predicting with mechanisms. No pure-recall questions found (closest was e-risk-assessment Q1, but it requires applying threat/vulnerability/risk discrimination to a new case — acceptable). No rewrites needed.
- **§5 "On your own": all 55 pass.** Every success test is verifiable by the reader alone: "find at least one X," "every finding gets a decision, owner, and date," "at least one measure's first data point surprises you." No vague tests found. No rewrites needed.
- **§9 "Prove it": 4 fixes.** Two lessons were pure redo-the-worked-case (rewritten to require a different organization). Two were "worked case in your own words" first-option (sharpened to new-system-first). The rest already point at new systems or say "or better, for a system you control" and passed.

## Per-lesson table

| Lesson | Lenses fired | Scope substance check + what was added / fixed |
|---|---|---|
| e-arch-vuln-assessment | L3 | L1: 3.5 taught (decompose, per-component classes, rating with blast radius + structural persistence, architectural recommendations). L2: prereqs deliver; complete-mediation is defined inline. L3: §9 sharpened — new-system-first; "Harborline in your own words" demoted to a changed-architecture option. |
| e-assessment-strategy | L2, L3 | L1: 6.1 taught (policy, coverage inventory, assessor classes, cadence/viewpoints, scoping rules). L2: §2 assumed risk literacy from e-risk-assessment (not a prereq) — reworded to companion pointer + §3 pointer. L3: §9 sharpened — new-estate-first. |
| e-asset-classification | — | L1: 2.1 taught (FIPS 199, SP 800-60, four-tier scheme, owners). L2/L3 strong. (Suspected mojibake in §1 proved to be a display artifact — file bytes are a clean em dash; no change.) |
| e-asset-provisioning | — | L1: 2.3 taught (CM-8, ID.AM, CMDB, inventory audit, deprovisioning). L2/L3 strong. |
| e-auth-systems | L2 | L1: 5.6 taught (MFA rollout, FIDO2/passkeys, biometrics FAR/FRR, SSO, authenticator lifecycle). L2: §1 presented b-session-auth as prior learning (not a prereq) — reworded to companion discipline; §10 already listed it as companion. L3 strong. |
| e-awareness-training | L2 | L1: 1.12 taught (CPLP, program design, simulation rules). L2: §2 assumed the e-policy-docs hierarchy — reworded to pointer + one-line hierarchy definition inline. L3 strong. |
| e-bcp-drp | — | L1: 1.7, 7.10–7.13 taught (BIA, RTO/RPO as business decisions, BC vs DR, strategies, plans, test ladder, backups with tested restores). L2/L3 strong. |
| e-board-communication | L3 | L1: brief §5 board-memo work-product; taught. L2: prereqs deliver. L3: **§9 rewritten** — the artifact was the Beacon worked-case memo itself (the only E lesson-pair case with no alternative); now requires a different organization with its own charter and register behind the memo, stranger-reconstructable from the appendix. |
| e-change-management | L2 | L1: 7.9 taught. L2: §2 assumed the incident lifecycle from c-incident-response — reworded to "this lesson needs only the idea that emergencies compress timelines." L3 strong. |
| e-config-management | — | L1: 7.3 taught (baseline, hardening, drift, SP 800-128). L2/L3 strong. |
| e-control-selection | — | L1: 3.3 taught (requirements, catalog, baselines/tailoring, traceability matrix, coverage argument). L2/L3 strong. |
| e-control-testing | — | L1: 6.2 taught. L2: prereqs deliver. L3 strong. |
| e-cryptanalysis | — | L1: 3.7 taught. L2/L3 strong. |
| e-crypto-applied | — | L1: 3.6 taught. L2/L3 strong. |
| e-csf-20 | — | L1: CSF what-it-is + who-needs-it taught; how-it-relates covered by the new e-soc2 paragraph (e-csf-20 §10 already points at both). L2/L3 strong. |
| e-cyber-law | — | L1: 1.4 taught (GDPR obligations as testable artifacts). L2/L3 strong. |
| e-data-lifecycle | — | L1: 2.4 taught. L2/L3 strong. |
| e-data-protection-controls | — | L1: 2.6 taught. L2/L3 strong. |
| e-detective-preventive | — | L1: 7.7 taught. L2/L3 strong. |
| e-ethics | — | L1: 1.1 taught (four canons, priority ordering). L2/L3 strong. |
| e-facility-controls | L2 | L1: 3.9 taught. L2: §2 assumed the e-control-selection discipline — reworded to companion pointer ("the selection discipline itself is e-control-selection's subject"). L3 strong. |
| e-facility-design | — | L1: 3.8 taught. L2/L3 strong. |
| e-governance | — | L1: 1.3 taught (governance vs management, GV function, roles/reporting, framework rationale). L2/L3 strong. |
| e-handling-requirements | — | L1: 2.2 taught. L2/L3 strong. |
| e-iam | L2 | L1: 5.1–5.5 taught (lifecycle, assurance strategy, federation/IAL-AAL-FAL, authorization models, privileged access). L2: §2 "Bring the habit from e-risk-assessment" — dropped the lesson pointer, kept the discipline. L3 strong. |
| e-incident-management | L2 | L1: 7.6 taught (team, severity matrix, comms plan, metrics). L2: §2 assumed the e-bcp-drp view — reworded: "this lesson teaches the handoff from the incident side." L3 strong. (The DEb-flagged "undeniable" is gone — DEa/coordinator fixed it.) |
| e-investigation-forensics | L2 | L1: 7.1 taught. L2: §2 "Bring the e-risk-assessment habit" — same fix as e-iam. L3 strong. |
| e-investigations | L2 | L1: 1.5 taught. L2: §2 assumed the reader's e-cyber-law matrix — reworded to "If you have built it, bring it; the clocks and triggers are taught here." L3 strong. |
| e-iso27001 | — | L1: 27001 what/who taught; paid-standard one-lined; relates-to-CSF taught. L2/L3 strong. |
| e-logging-monitoring | — | L1: 7.2 taught. L2/L3 strong. |
| e-media-protection | L2 | L1: 7.5 taught. L2: §2 presented chain-of-custody as seen in e-investigation-forensics — reworded to companion pointer; the concept is defined in this lesson's §3 (added by DEb). L3 strong. |
| e-network-architecture | L2 | L1: 4.1 taught. L2: §2 "Bring the habit from e-risk-assessment" — same fix. L3 strong. |
| e-network-components | — | L1: 4.2 taught. L2/L3 strong. |
| e-patch-management | L2 | L1: 7.8 taught. L2: §2 assumed change control from e-change-management — reworded to companion pointer; §3 keeps the patching-specific design. L3 strong. |
| e-personnel-safety | — | L1: 7.15 taught. L2: prereqs [] and no assumed concepts — clean. L3 strong. |
| e-personnel-security | (format) | L1: 1.8 taught. L2/L3 strong. Drive-by only: fixed three "`e-iam`**"-style stray bold markers in §10. |
| e-physical-security | L2 | L1: 7.14 taught. L2: §2 assumed e-iam's identity lifecycle and e-logging-monitoring's monitoring program (prereqs are []) — fixed with inline micro-foundations (joiner–mover–leaver defined in one line) + companion pointers. L3 strong. |
| e-platform-security | — | L1: 3.4 taught. L2/L3 strong. |
| e-policy-docs | (format) | L1: 1.6 taught. L2/L3 strong. Drive-by only: fixed three stray bold markers in §10. |
| e-retention-eol | — | L1: 2.5 taught. L2/L3 strong. |
| e-risk-assessment | — | L1: 1.9 taught. L2/L3 strong (§8 Q1 is applied discrimination, not recall). |
| e-sdlc | — | L1: 8.1–8.5 taught per the guidebook's own map phrases (threat modeling, gates, SSDF incl. acquirer vocabulary, effectiveness metrics, secure coding as policy). L2/L3 strong. |
| e-secops-concepts | — | L1: 7.4 taught. L2: §2's e-detective-preventive reference was already the honest companion pattern — left alone. L3 strong. |
| e-secure-channels | — | L1: 4.3 taught. L2/L3 strong. |
| e-secure-design | — | L1: 3.1 taught. L2/L3 strong. |
| e-security-audits | L2 | L1: 6.5 taught. L2: §2 assumed control-claim/evidence thinking from e-control-testing + e-security-metrics — reworded: audits demand the strictest standard; the vocabulary is used in those lessons. L3 strong. |
| e-security-concepts | (format) | L1: 1.2 taught. L2/L3 strong. Drive-by only: fixed three stray bold markers in §10, including the "e-csf-20 — e-governance" muddle → now "CSF 2.0 — e-csf-20". |
| e-security-metrics | — | L1: 6.3 taught (SP 800-55 Vol. 1/2). L2/L3 strong. |
| e-security-models | — | L1: 3.2 taught (BLP, Biba, Brewer-Nash, selection). L2/L3 strong. |
| e-security-program | L3 | L1: brief §5 security-program work-product; taught. L2: prereqs deliver. L3: **§9 rewritten** — the artifact was the Beacon worked-case charter itself; now requires a different organization, stranger-distinguishable from the worked case. |
| e-soc2 | L1 | L1 gap closed: added the three-frameworks side-by-side paragraph (what each IS, WHO needs it, HOW they relate) to §3. L2/L3 strong. |
| e-supply-chain-risk | (format) | L1: 1.11 taught. L2/L3 strong. Drive-by only: fixed two stray bold markers in §10. |
| e-system-lifecycle | — | L1: 3.10 taught. L2/L3 strong. |
| e-test-analysis-reporting | L2 | L1: 6.4 taught. L2: §2 assumed e-control-testing's method matrix — the one genuinely load-bearing forward reference: added the inline micro-foundation (scanner = unverified, pentest = point-in-time, audit = sampled) + pointer to e-control-testing for the full matrix. L3 strong. |
| e-threat-modeling-concepts | (format) | L1: 1.10 taught (STRIDE, attack trees, PASTA, OCTAVE, methodology selection). L2/L3 strong. Drive-by only: fixed one stray bold marker in §10. |

## Worst exercise rewrites (before/after)

**e-board-communication §9.** Before: "**Artifact:** the one-page board memo for Beacon Logistics — five sections plus appendix, placeholders labeled, acronym sweep logged, director test passed and recorded." — this asked the reader to re-produce the §3 worked example (Beacon's memo). After: the artifact must be the memo "for an organization that is NOT Beacon Logistics: your employer, a company you know, or a fictional organization of your own invention with its own program charter and risk register behind the memo," with the test that "a stranger reading it should be able to reconstruct your charter's measurement plan and your register's risk decisions from the appendix alone."

**e-security-program §9.** Before: "**Artifact:** the complete program charter for Beacon Logistics — mission, scope, RACI, risk appetite statement, measurement plan (3 KPIs + 3 KRIs, each sourced/defined/targeted), and review cadence — with the self-review checklist signed off." After: the charter "for an organization that is NOT Beacon Logistics," with the test that "a stranger should be able to tell your program's strategy, accountabilities, and measures apart from the worked case's."

**e-test-analysis-reporting §2 (Lens 2, load-bearing fix).** Before: "You have the method matrix (`e-control-testing`) — every finding below arrives with the method that produced it, which bounds what the finding means." After: "Every finding below arrives with the method that produced it, which bounds what the finding means: a scanner finding is unverified until triaged, a pentest finding is point-in-time evidence, an audit finding is sampled evidence — the full method matrix is `e-control-testing`'s subject." This was the only forward reference where the assumed concept does real work in the lesson (interpreting findings), so the concept is now taught inline.

## Sources

`sources-add-3-E.csv` is header-only: no new external factual claims were introduced. The e-soc2 paragraph is synthesized from the three framework lessons' existing content; all other additions are reference rewordings, inline micro-foundations of already-taught concepts, or exercise rewrites. Checked against `guidebook/sources.csv` — nothing to add. No walkthrough steps were added or changed, so no runs were needed (all edited content is prose in §2/§3/§9/§10; no new commands).

## Verification (2026-10-10)

- All 24 edited lessons: exactly ten `^## ` sections each; all 10 frontmatter keys present.
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`) and currency (`$<digit>`): zero hits across all e-*.md (the pre-existing "undeniable" in e-incident-management flagged by DEb is gone — fixed by DEa or the coordinator).
- No full `build_site.py` run per task orders; edited files validated individually.
- pgrep: clean — no test servers were started (no runnable walkthrough steps were added), no stray processes.
- Untouched: build_site.py, STATE.md, gaps.md, map.md, sources.csv, runs/, all other stages' files and frontmatter. Nothing committed, nothing pushed.

## Not closed / for the coordinator

1. **Prereq-list changes considered but NOT made** (per the no-frontmatter-shuffle rule) — candidate additions if the coordinator wants the lists to match the §2 pointers: e-test-analysis-reporting ← e-control-testing (strongest case; mitigated by the new inline micro-foundation), e-assessment-strategy ← e-risk-assessment, e-incident-management ← e-bcp-drp, e-awareness-training ← e-policy-docs, e-auth-systems ← b-session-auth, e-security-audits ← e-control-testing and/or e-security-metrics, e-investigations ← e-cyber-law, e-facility-controls ← e-control-selection, e-patch-management ← e-change-management, e-change-management ← c-incident-response, e-media-protection ← e-investigation-forensics, e-physical-security ← e-iam and/or e-logging-monitoring (prereqs currently []). All 12 are now honest as written; these are optional list additions, not integrity fixes.
2. **Cross-stage note:** two Lens-2 fixes touch lessons in other stages only as named pointers (b-session-auth, c-incident-response, c-soc-triage, etc.) — no other stages' bodies or frontmatter were touched.
3. **e-secops-concepts §2** is the model for how same-stage forward pointers should read; worth adopting as the house pattern.
4. The §1 mojibake in e-asset-classification was a tool-display artifact (file bytes were always a clean em dash) — no fix needed.
