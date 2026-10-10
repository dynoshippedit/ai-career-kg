# Depth Audit — Stage C batch (worker C)

Date: 2026-10-10 · Worker: subagent ac08c7a7 · Scope: the 10 Stage C lessons.

Brief references: SECURITY_GUIDEBOOK_BRIEF-2.md §1 (level bar), §6 (lesson spec),
§7 (evidence/safety/voice). Pad-free rule applied throughout: word counts are a
sanity check only; verdicts are about substance, never length.

Verdict key: **SOLID** = deep enough at its stated level; **DEEPEN** = genuinely
thin, with the specific missing substance named. **STALE** = factual staleness
(dates, versions, renamed tools/URLs) flagged for correction.

| Lesson | Words | Level | Verdict |
|---|---|---|---|
| c-cvd | 2,298 | L3 | **SOLID** |
| c-cve-program | 2,080 | L3 | **SOLID** |
| c-cvss | 2,133 | L3 | **SOLID** |
| c-vuln-ecosystem | 2,297 | L3 | **SOLID** |
| c-incident-response | 2,386 | L3 | **SOLID** |
| c-log-sources | 2,134 | L3 | **SOLID** |
| c-soc-triage | 2,147 | L3 | **SOLID** |
| c-sigma-detection | 2,122 | L3 | **SOLID** |
| c-ai-tooling | 2,231 | L3 | **SOLID** (one logged, non-blocking gap — see below) |
| c-public-track-record | 2,037 | L3 | **SOLID** |

**Result: 10/10 SOLID. Zero DEEPEN lessons. No lesson was edited; no deepening
pass was warranted.** All ten sit inside the 1,200–2,500-word sanity band, every
one fills "How it works" and "Walkthrough" with substance per §6, and all ten
carry honest §9 honest-claims/can't-claim-yet pairs.

## Per-lesson notes (why SOLID)

- **c-cvd** — Six-phase model with the five named actor roles; CERT principles
  from memory-load-bearing use; good/bad worked cases (Heartbleed with the
  deployer-notification critique; the 2018 zero-day drops as the SandboxEscaper
  pattern). Runnable security.txt lab, full disclosure package as work product.
  Primary docs: CERT CVD guide, OpenSSF finder guide, RFC 9116.
- **c-cve-program** — Federation model (CNAs / Roots / CNA-LRs), the
  independently-fixable counting rule, request path with the fictional Harborlight
  worksheet, credits schema with `type: finder` enum spelled out. Worked example:
  a real CVE-2021-44228 record fetched from the CVE API, read field by field.
  The 555-CNA figure (552 + 3 CNA-LRs, "October 2026 check") matches the
  program's reported growth trajectory — 508 in April 2026, 543 (540 + 3) in the
  Q2 2026 program report — and the lesson itself says "re-check; the number
  moves." Not stale: dated and self-aware.
- **c-cvss** — v3.1 and v4.0 taught as *argument frameworks*, three FIRST
  official calibration cases reproduced by hand and against the reference
  implementation (all published scores matched, per the dateline). The
  E:U-collapses-7.7-to-5.2 disagreement analysis is exactly the L3 bar:
  explain *which judgment* each decimal rests on. Nomenclature CVSS-B/BT/BE/BTE
  taught as anti-deception discipline.
- **c-vuln-ecosystem** — CWE Top 25 (2025 edition, dated), CAPEC, KEV CSV, live
  EPSS API pulls, the 2026-04-15 NVD-enrichment change sourced via Commerce OIG
  report OIG-26-020-I with the honest "government-confirmed via OIG, not
  NIST-direct" sourcing distinction. Three-way ranking of three real CVEs with
  *defended* disagreement. This is the strongest "don't smooth a gap" example
  in the batch.
- **c-incident-response** — SP 800-61 Rev. 3 (final April 2025, CSF 2.0 Community
  Profile) with the Rev. 2-staleness warning; a full fictional IR report
  (timeline, ordered containment, rebuild-vs-clean decision, load-bearing
  Limitations section). Non-CLI walkthrough handled per §6's worked-case
  allowance, review checklist logged.
- **c-log-sources** — Event IDs with meaning (4624 types, 4688's command-line
  dependency, 1102 as anti-forensics), Sysmon IDs, beaconing-visible-under-TLS
  via flow timing, worked five-source intrusion correlation, runnable fictional
  logs with the spray→payoff delta, and the blind-spot column (no proxy / no
  EDR / no email gateway) that c-incident-response's Limitations section
  inherits. ATT&CK v19.2 Stealth/Defense-Impairment split matches the brief's
  correction.
- **c-soc-triage** — Eight-stage pipeline (intake → lessons learned), the
  five classification buckets, escalation criteria including uncertainty-as-
  routing-input, impossible-travel and beaconing decision trees with two
  worked branches each, runnable fictional event set with real CV statistics.
  Severity-vs-priority distinction done concretely.
- **c-sigma-detection** — Rule anatomy field-by-field against the Sigma spec
  (modifiers, condition, tags as detection map), the measured tuning loop
  (v1 FP=1 → v2 FP=0, TP unchanged, on labeled corpora), detection-as-code
  discipline, and the procedure-vs-technique coverage honesty. On-your-own
  requires an aggregation condition the walkthrough deliberately withholds.
- **c-public-track-record** — Mechanism-first anatomy (root cause / mechanism /
  confirmation / honest impact / fix+verification / dead ends), one finding in
  two formats (research write-up vs one-page bounty report), Project Zero bar
  taught from structure, the pwn.college no-solutions rule honored by name.
- **c-ai-tooling** — The brief §3 correction internalized as the lesson's spine:
  "access to tooling — never a credential, a milestone, or a CV line" appears in
  §1, §6, §9, and the closing line. Tiers dated 2026-10-06 on every statement.
  **Spot-check 2026-10-10:** the tier facts, eligibility, review times,
  CyScenarioBench numbers (0/50, 4/50, 34/50), and Glasswing figures (129,000 /
  33,000+ critical-high / 5,500 Anthropic scanning) all match secondary coverage
  of the Oct 6 announcement — no factual correction needed.

## Logged gap (not a deepen trigger)

- **c-ai-tooling §7** states plainly: the Anthropic announcement URL was not
  fetched in-session (the guessed path 404'd); tier details come from 6+
  secondary outlets dated 2026-10-06–08 plus one secondary page that read the
  announcement directly. This is a logged gap per §7's honesty standard, not a
  depth failure. The lesson explicitly instructs "re-fetch the primary before
  publishing." I did not close it: no verified primary URL surfaced in-session,
  and per the brief's sourcing rule, secondary search snippets cannot supply a
  primary row. Candidate for the coordinator's pre-publish re-fetch pass.

## Staleness sweep (whole batch)

Checked: CVSS v4.0 group names (Base/Threat/Environmental/Supplemental — Threat
replaced Temporal ✓); CVE Record Format 5.2.0 ✓; CNA scale (see c-cve-program
note ✓); NVD policy change date 2026-04-15 ✓; SP 800-61 Rev. 3 April 2025 ✓;
OWASP LLM Top 10 2026 edition (amendment — the Stage C batch doesn't teach the
LLM Top 10 directly; no cross-reference needed) ✓; CVE-2022-41741 vectors used
only as scoring specimens, not factual claims about the vulns ✓. **No stale
facts found.**

## Phase 2 (deepening)

Not triggered — no DEEPEN verdicts. No files touched, no frontmatter changes,
no new factual claims added to any lesson, so **/tmp/sources-add-C.csv** carries
zero new rows (header-only file written for the merge).

## Phase 3 (verification)

Vacuous: zero edited lessons. Recorded for the record — nothing to grep,
nothing to build.

## Counts

- Lessons audited: 10
- SOLID: 10 · DEEPEN: 0 · STALE findings: 0
- Lessons edited: 0 · new factual claims: 0 · sources-add-C.csv rows: 0
- Banned voice words in new copy: none (no new copy) · currency symbols: none
- Test servers started: none (no walkthroughs needed re-running) · pgrep: clean

## Decisions

- Held the pad-free rule strictly: all ten lessons were already substantive at
  L3, so all ten stand as written. Depth without new content added was not
  needed anywhere.
- Did not attempt to close the c-ai-tooling primary-URL gap with a secondary
  URL — that would have traded one logged gap for a fabricated row.
- Left the walkthrough transcripts (runs/*.log) untouched; re-running them
  was not required to judge depth.

## Questions for the parent/coordinator

- None that block this batch. Optional follow-up: the c-ai-tooling primary-URL
  re-fetch at publish time, as the lesson itself requests.
