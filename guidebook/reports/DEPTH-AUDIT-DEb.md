# Depth Audit — DEb (Stage E, second half of 27)

Auditor: subagent session 905e4917 · 2026-10-10. All 27 lessons read in full.
Method: read each lesson end-to-end against the brief §1 level bar and §6 lesson spec;
checked version/date/tool claims against current primary sources where staleness was plausible.
Pad-free rule applied: no verdicts for length alone.

## Verdicts

SOLID (26) — deep enough at stated level, no genuine thinness:

| lesson | words | lvl | note |
|---|---|---|---|
| e-iso27001 | 2164 | 3 | ISMS/Clauses 4–10/93-control Annex A/SoA; paid-doc rule honored; complete |
| e-logging-monitoring | 2463 | 3 | 800-92 lifecycle, integrity/time, retention tiers, SOC workflow; honest about 800-92 age |
| e-media-protection | 2396 | 3 | 800-88 Rev. 2 Clear/Purge/Destroy, CE preconditions, custody; Rev. 2 claims verified |
| e-network-architecture | 2520 | 3 | 800-207 tenets, zone map, DMZ, NAC, vendor access, monitoring points |
| e-network-components | 2290 | 3 | 800-41r1 ruleset review, 800-94 placement, 800-153 wireless, NAC failure mode |
| e-patch-management | 2346 | 3 | KEV-first prioritization, SLA policy, exception register, emergency runbook; BOD 26-04 verified |
| e-personnel-safety | 2284 | 3 | OSHA workplace-violence program, OSAC travel briefings, duress, lone-worker check-in |
| e-personnel-security | 2404 | 3 | 800-53 PS family, departure checklists with owners/timing, SoD, travel security |
| e-physical-security | 2403 | 3 | PE family, post orders, badge lifecycle, mantrap, CCTV ops, environmental; FEMA 403 honestly logged |
| e-platform-security | 2524 | 3 | TPM/measured boot/attestation, UEFI Secure Boot, CET, virtualization boundary, survey method |
| e-policy-docs | 2318 | 3 | four-tier hierarchy, traceability both ways, exception process; strong worked set |
| e-retention-eol | 2475 | 3 | SI-12 schedule with computable triggers, legal hold, decommissioning workflow; Rev. 2 cited |
| e-risk-assessment | 2346 | 3 | 800-30 prep/conduct/communicate, qualitative scales with anti-math rule, worked register |
| e-sdlc | 2377 | 3 | STRIDE, per-phase gates, SSDF 800-218 groups, effectiveness metrics |
| e-secops-concepts | 2469 | 3 | need-to-know/least privilege/SoD/defense-in-depth + ZTMM v2.0 gap assessment; ZTMM v2.0 verified current |
| e-secure-channels | 2245 | 3 | per-flow channel selection, TLS 1.3 termination, VPN types, SSH, E2E messaging |
| e-secure-design | 2540 | 3 | Saltzer & Schroeder applied per principle, requirement→control trace, platform survey |
| e-security-audits | 2169 | 3 | ITAF 5th ed structure, plan, sampling, five-part finding, facilitation; ITAF 5th verified (2026 release) |
| e-security-concepts | 2501 | 2 | CIA/AAA/non-repudiation, property tensions, real local hash demo run; L2 honest |
| e-security-metrics | 2199 | 3 | 800-55 Vols 1–2 (Dec 2024), measure spec six fields, KPI/KRI, anti-gaming |
| e-security-models | 2370 | 2 | BLP/Biba/Clark-Wilson/Brewer-Nash with selection rationales; real BLP script run; L2 honest |
| e-security-program | 2232 | 3 | CSF 2.0 §5 loop, charter, KPI/KRI families, appetite with thresholds |
| e-soc2 | 2060 | 3 | examination engagement, five TSC, Type I vs II, SOC family, scoping memo |
| e-supply-chain-risk | 2498 | 3 | 800-161, six assessment factors, SBOM, contractual mitigations, residual decision |
| e-test-analysis-reporting | 2377 | 3 | triage dispositions, severity-vs-risk, two-layer report, tracking; real demo run |
| e-threat-modeling-concepts | 2488 | 3 | STRIDE/PASTA/OCTAVE/attack trees selection record; OCTAVE Aug-2003 date verified at SEI |

DEEPEN (0) — no lesson was genuinely thin. Every lesson fills §3 (mechanism from first
principles with defined terms) and §4 (walkthrough producing real work products, or
locally-run demos with transcripts) with substance specific to its level. Per the
pad-free rule, the shorter-but-complete lessons (e-soc2 2060, e-iso27001 2164,
e-security-audits 2169) were left alone.

## Factual-staleness pass (the one fix)

- **e-system-lifecycle §7 cited "NIST SP 800-88 Rev. 1".** Stale: Rev. 2 final published
  2025-09-26 and Rev. 1 withdrawn that day (confirmed in-session at the primary source,
  csrc.nist.gov/pubs/sp/800/88/r2/final — date published Sept 2025, supersedes Rev. 1,
  document history 09/26/25 Final). Corrected in place to Rev. 2; §3's
  Clear/Purge/Destroy content needed no change (definitions survive Rev. 2).
- Verified and accurate, no change needed: 800-88 Rev. 2 claims in e-media-protection
  and e-retention-eol; ITAF 5th edition (ISACA store + March-2026 release coverage,
  previous edition 2020) in e-security-audits; BOD 26-04 "Prioritizing Security Updates
  Based on Risk" issued 2026-06-10, superseding/revoking BOD 22-01 (and 19-02), in
  e-patch-management; OCTAVE "Introduction to the OCTAVE Approach" August 2003 at
  sei.cmu.edu in e-threat-modeling-concepts; NISTIR 7316 (Hu/Ferraiolo/Kuhn, 2006-09-29)
  in e-secops-concepts; CISA ZTMM v2.0 as current edition in e-secops-concepts,
  e-network-architecture, e-network-components.

## Deepening performed

None — one staleness correction only (e-system-lifecycle §7, above). No frontmatter
level changes, no new walkthrough steps, no new resources. Source row staged in
/tmp/sources-add-DEb.csv (1 row: 800-88 Rev. 2 claim, status verified).

## Cross-batch link note (for coordinator)

Many lessons reference sibling-batch lessons that may or may not exist yet:
e-iam (×9), e-governance (×6), e-awareness-training (×3), e-investigations /
e-investigation-forensics (×4), e-crypto-applied (×6), e-arch-vuln-assessment (×2),
e-control-testing (×3), e-csf-20 (×5), e-cyber-law (×5), e-board-communication (×3),
e-bcp-drp (×5), e-data-lifecycle (×3), e-handling-requirements (×1),
e-detective-preventive (×5), e-change-management (×2), e-config-management (×1),
e-asset-provisioning (×2), e-facility-controls (×1), ai-threat-modeling (×2),
ai-supply-chain (×2), e-control-selection (×4), d-appsec / D-AppSec track (×3).
The internal-link check should run after all batches land.

## Phase 3 verification

- All 27 files: exactly 10 `^## ` sections (checked via grep before/after edit).
- Frontmatter intact: `^lesson_id:` present in all 27 after edit.
- Banned voice words: none of "guaranteed", "job-ready", "undeniable" in the edited lesson
  (or any of the 27 — they were written to the voice rule).
- Currency symbols: none added by the correction (the correction adds no prices).
- Test servers: none started (no walkthroughs needed running; audit-only). pgrep checked.
- Untouched: build_site.py, STATE.md, gaps.md, map.md, sources.csv, runs/, other reports.
