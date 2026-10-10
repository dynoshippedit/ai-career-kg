# Content-depth audit — all 110 lessons (2026-10-10)

Dino's order: review every lesson, add more only where genuinely warranted. Six stage crews audited all 110 lessons against brief §1/§6/§7 with a pad-free rule: only genuine thinness flagged; never length alone.

---

# Stage A

# Content-depth audit — Stage A batch (worker A)

Batch: a-crypto, a-dns-depth, a-git-github, a-http-depth, a-linux-cli, a-osint-research, a-python-security, a-reading-code, a-tcpip-ports, a-windows-concepts
Auditor: depth-audit worker, 2026-10-10. Brief §1/§6/§7 read before auditing.

Pad-free rule applied: a lesson complete at its level is left alone even under 2,500 words.

## Phase 1 verdicts

| Lesson | Words | Level | Verdict | Notes |
|---|---|---|---|---|
| a-crypto | 2063 | L2 | **SOLID** | Four primitives + per-primitive misuse, full OpenSSL walkthrough run locally. Level honest. |
| a-dns-depth | 2452 | L3 | **SOLID** | Message format, record types, caching, DNSSEC, NXDOMAIN/SERVFAIL split; walkthrough re-ran with real dig 2026-10-10. |
| a-git-github | 2198 | L3 | **SOLID** | Snapshot model, staging, branches, remotes via local bare repo, undo ladder, history-as-investigation (`log -S`, blame). GitHub side honestly not-run. |
| a-http-depth | 2735 | L3 | **SOLID** | Over 2,500 words; deep. Methods, status codes, cookie attrs, JWT structure + verification, TLS layering, all run locally. |
| a-linux-cli | 2306 | L3 | **DEEPEN** | Strong, but brief §5's Linux scope list names *package management* and *services and daemons*; the lesson teaches neither and defers to "a later Stage A lesson" that does not exist in the lesson set. Installing tools is the first thing Stage B's toolbench assumes. Genuinely warranted: a package-management section (apt) + a compact services/daemons primer (systemctl). |
| a-osint-research | 2269 | L3 | **SOLID** | Passive/active line, public-vs-exposed discipline, documentation standard, fictional-target ethics frame all solid. Resources 1–3 marked "(lead, verify at build time)" — flagged for the build-time verifier, not a depth gap. |
| a-python-security | 2054 | L3 | **SOLID** | stdlib-only choice deliberate and justified; annotated fetcher, sockets, argparse, traceback reading. Complete at L3. |
| a-reading-code | 2112 | L3 | **SOLID** | Source→path→sink frame, JS vocabulary, SQL execution order, hostile-vs-safe builder proven by transcript. Complete at L3. |
| a-tcpip-ports | 2329 | L3 | **SOLID** | Handshake, states, ephemeral ports, RST-vs-silence scanning basis, TIME_WAIT, NAT, tcpdump re-run 2026-10-10 with real packet flags. |
| a-windows-concepts | 2277 | L2 | **DEEPEN** | Good translation table + honest not-run markers, but two genuine gaps: (1) §7 "Read the source" lists the *same* Registry Hives URL as both primary item 1 and primary item 3 ("reread") — a real duplication, not depth; (2) **PowerShell execution policy is entirely absent** — the first thing that bites a beginner running any script (including this lesson's own §5 on-your-own `Export-Csv` step and any `.ps1`), and the natural home for "signed vs bypass" security framing. Both are specific substance, not padding. |

## Cross-cutting notes (for the coordinator, not for deepening)

- **Cross-stage prerequisites in Stage A lessons:** `a-reading-code` lists `b-sqli` and `a-osint-research` lists `b-authorization-scope` as prerequisites. A Stage A reader cannot have done a Stage B lesson first; the map/coordinator should decide whether these mean "read the rule stated here" or are ordering errors. Left untouched.
- **Resource leads:** `a-osint-research` §7 items 1–3 and `a-reading-code`'s SQLite reference are marked "lead, verify at build time." For the build-time verifier to confirm; TraceLabs/Search Party activity in particular should be re-checked (program status changes are plausible).
- **No factual staleness found** in version/tool claims (OpenSSL 3.0.13, git 2.43.0, curl 8.5.0, iproute2 6.1.0, tcpdump 4.99.4, Python 3.12.3, OpenSSH 9.6, bash 5.2.21, Windows event IDs 4624/4625/4720/4726/4672/1102) — all carried with test dates from in-session runs; nothing renamed or withdrawn that I could see.
- **Banned voice/currency scan:** run in Phase 3 after edits.

## Phase 2 deepening targets (this worker)

1. **a-linux-cli** — DONE 2026-10-10. Added: §3 "Package management" subsection (apt/apt-get/apt-cache/dpkg, update-then-install order, `dpkg -S`/`dpkg -L` round trip, `apt-cache policy`, remove-vs-purge forensics angle — sourced to Debian AptCLI wiki, fetched in-session) and §3 "Services and daemons" primer (unit files, systemctl read-only vs state-changing, enabled-vs-running gap — start/stop honestly marked not-run on the build container). Walkthrough gained steps 8–9 (all read-only, run, transcript appended to `runs/a-linux-cli.log`); §6 gained two items (blind `apt install`/third-party repos; stop-vs-disable); §7 gained the Debian AptCLI primary doc; §8 gained one check question; §9 honest claim and §10 leads extended. Level stays L3 — the additions are operate-level fluency, not design judgment.
2. **a-windows-concepts** — DONE 2026-10-10. Added: §3 "PowerShell execution policy" paragraph (Restricted/RemoteSigned/AllSigned/Bypass, not-a-security-boundary per Microsoft's own doc, scopes with precedence, `Set-ExecutionPolicy -Scope CurrentUser`, Bypass-in-scheduled-tasks as a finding — sourced to MicrosoftDocs/PowerShell-Docs `about_Execution_Policies`, fetched in-session); §4 step 6 (exact reader procedure, not-run-by-us); §6 item (Bypass-as-fix anti-pattern); §8 question 6 (scheduled-task finding); §7 now cites the distinct registry-value-types reference instead of the duplicated Registry Hives URL; §7 also gained the about_Execution_Policies doc. Level stays L2.
   - One fetch failure: learn.microsoft.com's `about_execution_policies` page returned HTTP 403 to the text fetcher. Worked around via the same content in Microsoft's own PowerShell-Docs GitHub repo (found through web search, fetched in-session). Lesson links the repo path, not the denied URL.

## Phase 3 verification (2026-10-10)

- All 10 lessons: exactly ten `^## ` sections, one `^lesson_id:` frontmatter line each. Frontmatter structure untouched (values only: dateline extended on the two deepened lessons).
- Banned voice words: `guaranteed`, `job-ready`, `undeniable` — zero hits across all 10 files.
- Currency symbols: no `$<digit>` in new copy (only pre-existing awk field references like `$7`).
- Stray test servers: `pgrep` shows none (no demo listeners, no sleep jobs, no server.js).
- Source rows staged: `/tmp/sources-add-A.csv`, 4 rows, all status=verified. NOT merged into `guidebook/sources.csv` (another worker owns the merge).
- Runs log: deepening transcript appended to `guidebook/runs/a-linux-cli.log`. No new run file for a-windows-concepts (no Windows on the bench; steps marked not-run-by-us in-lesson per the walkthrough substitution policy).
- build_site.py NOT run; nothing committed or pushed, per orders.

---

# Stage B

# Content-depth audit — Stage B (21 lessons)

Auditor: subagent ac08c7a7 · 2026-10-10
Scope: `guidebook/lessons/b-*.md` listed in the task. Each lesson read fully.
Standard: brief SECURITY_GUIDEBOOK_BRIEF-2.md §1 (L1 Recognize / L2 Operate / L3 Apply / L4 Extend), §6 (lesson spec), §7 (evidence / safety / voice).
Rule applied: PAD-FREE — never flagged for length alone; 1,200–2,500 words is a sanity check, not a target.
Verdicts: SOLID (deep enough at stated level) / DEEPEN (genuinely thin — specific missing substance named).

## Method

Every lesson was read end to end and checked for: (a) the ten §6 sections in order with real substance in
"How it works" and "Walkthrough"; (b) honest level badge vs delivered bar; (c) factual staleness
(dates, versions, renamed tools/URLs); (d) the safety frame (authorization, attack+detect+fix together,
local-only walkthroughs, honest "not run by us" markers).

## Verdicts

| lesson | words | level | verdict |
|---|---|---|---|
| b-api-abuse | 1958 | L3 | SOLID |
| b-authorization-scope | 2824 | L2 | SOLID |
| b-bug-bounty | 2448 | L3 | SOLID |
| b-business-logic | 2139 | L3 | SOLID |
| b-command-injection | 2097 | L3 | SOLID |
| b-csrf | 2475 | L3 | SOLID |
| b-deserialization | 1833 | L3 | SOLID |
| b-graphql | 1944 | L3 | SOLID |
| b-idor | 2112 | L3 | SOLID |
| b-jwt-oauth | 2290 | L3 | SOLID |
| b-methodology | 2984 | L2 | SOLID |
| b-practice-targets | 2329 | L2 | DEEPEN |
| b-race-conditions | 1850 | L3 | SOLID |
| b-security-headers | 2229 | L3 | SOLID |
| b-session-auth | 2291 | L3 | SOLID |
| b-sqli | 2385 | L3 | SOLID |
| b-ssrf | 2268 | L3 | SOLID |
| b-ssti | 1853 | L3 | SOLID |
| b-toolbench | 3355 | L2 | SOLID |
| b-xss | 2265 | L3 | SOLID |
| b-xxe | 1776 | L3 | SOLID |

## SOLID — why each stands

- **b-api-abuse / b-graphql / b-jwt-oauth / b-deserialization / b-ssti / b-xxe / b-command-injection / b-sqli / b-ssrf / b-xss / b-csrf / b-idor / b-race-conditions / b-business-logic / b-session-auth (L3, 15 lessons):** each teaches the mechanism from first principles, a worked example with the flaw's real-world "why it arises," a defender view, a walkthrough run for real on loopback with a transcript in `runs/`, attack+detect+fix together, and honest boundaries (e.g. b-ssti keeps engine-escalation lab-bounded; b-xxe states plainly what its toy parser does and doesn't do). None claims a higher level than delivered. Word counts 1776–2475; all complete at L3.
- **b-authorization-scope (L2, 2824) / b-methodology (L2, 2984):** no-command-line planning lessons; complete worked cases (RoE document, six-phase engagement plan), primary-source citations checked in-session. Deep for L2.
- **b-bug-bounty (L3, 2448):** report anatomy, triage lifecycle, failure modes — complete at its level; hands-on reporting is deliberately a dry run (safe by design).
- **b-toolbench (L3→L2, 3355):** fifteen phases each with question/tool/output-reading/blind-spot; nmap/Semgrep/Chromium re-run for real 2026-10-10, rest marked "not run by us" with reader procedures.
- **b-security-headers (L3, 2229):** six controls with what-each-buys + browser-enforcement re-runs 2026-10-10. Note: the HSTS/MIME/clickjacking browser re-runs from another worker are present in the copy read; no duplication was added.
- **b-xxe (L3, 1776, shortest):** thin-looking by count but complete by substance — the honest statement that `xml.etree` refuses external entities *is* the lesson's strength; the dangerous behavior is named, sourced (OWASP XML Security Cheat Sheet), and lab-bounded in PortSwigger's labs. Padding it would weaken it.
- **b-ssti (L3, 1853):** same honest-boundary structure; the escalation ladder stays lab-bounded per the brief's safety line.

## DEEPEN — the one lesson, with the specific gap

- **b-practice-targets (L2, 2329) — DEEPENED.** Its "How it works" quoted five README run-commands (verified quotes, honestly labeled), but every container run was "not run by us (no Docker on the build machine)" and the walkthrough was procedure-verification only. For the lesson every other hands-on lesson depends on, the reader still could not see a *confirmed* working bring-up done by the guidebook's own hand. **What was added (2026-10-10):**
  - Full Docker attempt, honestly logged: static Docker 28.5.2 binaries install and the daemon runs (`--storage-driver=vfs --iptables=false --bridge=none`, required because this VM's kernel rejects overlay mounts and iptables rule appends), but Docker Hub is unreachable from this network (registry TLS handshake timeouts; proxy-aware `crane` couldn't complete even a `hello-world` pull). Attempt log is in `runs/b-practice-targets.log` — the "not run by us" marker for the other four targets now stands on evidence, not assumption.
  - **DVGA run for real, natively from the project's own source** (github.com/dolevf/Damn-Vulnerable-GraphQL-Application): venv + pinned requirements (two logged substitutions — pinned gevent 22.10.2 won't build on Python 3.12 → gevent 26.9.0; pinned greenlet 2.0.1 conflicts → 3.5.6), `setup.py` built the database. With `WEB_HOST=127.0.0.1` the app listened on `127.0.0.1:5013` only and answered a real GraphQL introspection query (`__schema` → full type list, introspection enabled) and `{ systemHealth }`. Restarted with `WEB_HOST=0.0.0.0` (the README's setting) → `ss` showed `0.0.0.0:5013 LISTEN` on all interfaces. That `ss` pair is the lesson's key teaching moment demonstrated, not just described: the README's `-e WEB_HOST=0.0.0.0` plus `-p 5013:5013` is exactly what the lesson's loopback override protects against. Teardown verified by PID and `ss`/`pgrep`.
  - Lesson §4 walkthrough and dateline updated; the README commands themselves were additionally confirmed against the freshly cloned source (README line 122: `docker run -t -p 5013:5013 -e WEB_HOST=0.0.0.0 dolevf/dvga`; Dockerfile `EXPOSE 5013`; source default `WEB_HOST=127.0.0.1`, overridden by the README command — the mechanism behind the teaching point).

## Factual-freshness fixes (not deepenings)

- **b-security-headers §7:** the RFC 6797 (HSTS) entry was a "cited as primary lead — fetch at build time before linking" placeholder. Fetched the RFC text in-session 2026-10-10; entry now reads "verified 2026-10-10." Source row staged in `/tmp/sources-add-B.csv`.
- **b-business-logic §7:** the PortSwigger business-logic entry said "re-fetch at build time before linking." Fetched the topic page in-session 2026-10-10; updated to "verified 2026-10-10." Source row staged.
- **b-csrf §7:** the RFC 6265bis citation. Checked the draft's publication status in-session: still a draft (draft-ietf-httpbis-rfc6265bis), not yet an RFC — the lesson's wording ("draft-ietf-httpbis-rfc6265bis §5.6.7", "RFC 6265 has no §4.1.2.7") remains accurate; entry refreshed to "verified 2026-10-10."
- **b-xss §7:** MDN CSP guide URL path `developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP` — verified reachable in-session 2026-10-10 (MDN redirects to the current location); left as-is with refreshed date.
- No renamed tools, no dead URLs found in any of the 21 lessons.

## What was deliberately not added (anti-pad log)

- No engine-escalation content in b-ssti (lab-bounded by design — the lesson's own decision, aligned with brief §7).
- No external-entity-resolution demo in b-xxe (same reason; the honesty note is a feature).
- No multi-host race infrastructure in b-race-conditions (concept-level by design; the mechanism is the lesson).
- No gadget-chain payloads in b-deserialization (researcher work by the lesson's own claim).
- No credential-stuffing runs in b-session-auth (taught as concepts-with-defenses; running them is outside the lesson's authorization).
- No Docker-container *attacks* in b-practice-targets — it is a setup lesson; the deepening is verified bring-up, not exploits.
- Levels were not raised on any lesson; the badges already match the delivered bar.

## Follow-ups for the parent / coordinator

- b-practice-targets deepening is done: DVGA run for real (native); the other four targets' "not run by us" markers now carry the full Docker attempt log. If the coordinator ever gets a build machine with registry access, re-running the five documented Docker commands there and curl-verifying the ports would close the loop — the lesson is already structured to receive that evidence.
- Two deferred-link patterns exist elsewhere in the guidebook ("re-fetch at build time before linking") — the coordinator's single build pass should re-verify every linked URL before the site ships, since lessons are long-lived.

---

# Stage C

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

---

# Stage D + E (a)

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

---

# Stage E (b)

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

---

# AI track

# Depth audit — AI track (8 lessons)

Auditor: subagent ac08c7a7 · 2026-10-10. Brief §1 (level bar), §5 (AI scope), §6 (lesson spec), §7 (evidence/safety/voice) read first. Pad-free rule honored: no lesson flagged for length; all eight sit at 2,299–2,600 words with complete ten-section structures and run walkthroughs.

## Per-lesson audit

| Lesson | Words | Level | Stage | Verdict |
|---|---|---|---|---|
| ai-governance | 2456 | L2 | AI | **SOLID** |
| ai-llm-architecture | 2442 | L3 | AI | **SOLID** |
| ai-llm-top10 | 2600 | L3 | AI | **SOLID** |
| ai-pipeline | 2299 | L3 | AI | **SOLID** |
| ai-prompt-injection | 2377 | L3 | AI | **DEEPENED** (stale cross-references) |
| ai-sec-automation | 2488 | L2 | AI | **SOLID** |
| ai-supply-chain | 2312 | L3 | AI | **SOLID** |
| ai-threat-modeling | 2457 | L3 | AI | **DEEPENED** (wrong 2026 codes) |

### SOLID rationale (the six)

- **ai-governance** — RMF four functions with honest caveats (voluntary; 1.0 revision announced), GenAI Profile's twelve categories used as an action list not trivia, EU AI Act tiers as concepts with the Digital Omnibus amendment noted and dated, ISO/IEC 42001 one-liner as required, plus a worked classification case feeding a six-row risk register with named owners. Walkthrough correctly shaped as authored work products per §6's no-command-line provision. Complete at L2.
- **ai-llm-architecture** — Tokens/embeddings/transformer built from mechanism, six-layer application stack with the trust boundary at each layer, the worked data-flow example counting six attack surfaces, and a deterministic harness walkthrough that re-derives the lesson's claims (prompt assembly with unmarked provenance, policy denial on the poisoned tool call). Meets L3: the reader can decompose an unfamiliar app.
- **ai-llm-top10** — All nine non-LLM01 entries with mechanism + defense each, grouped in data/system/agency families, edition discipline enforced (2026 codes named everywhere, the 2025→2026 renumbering called out with the LLM04:2025/LLM04:2026 trap as an explicit worked example), deterministic classification-drill walkthrough including a real LLM10 command-interpolation demo. L3 bar met.
- **ai-pipeline** — Five stages taught as attack/defense pairs, the LLM04 compromised-builder scenario handled as the lesson's thesis ("provenance proves which build; only testing proves which behavior"), red-team CI gate as the structural fix, honest limit stated (screening catches clumsy poisoning, not careful). Deterministic five-stage walkthrough run. L3 bar met.
- **ai-sec-automation** — SEC598/SEC535 taught strictly as concepts per §7's safety line: every attack concept (phishing/deepfakes, web exploitation, patch diffing, malware/evasion, recon) paired with defense *and* defender-detectable telemetry; no attack tooling named as a how-to; the worked detection plan is a genuine defensive work product with human-in-the-loop gates on every irreversible action; dwell figures labeled illustrative. L2 bar met; no level change needed.
- **ai-supply-chain** — Hashes vs provenance vs signatures taught as a strength ladder with the "hash of a poisoned model is a valid hash" honesty line; Sigstore keyless mechanics with the four verification checks; CycloneDX AIBOM for the incident-response use case; the pickle hazard *demonstrated locally on a labeled file* then the safe-format alternative — exactly the §7 containment standard. L3 bar met.

### DEEPENED (the two) — what was thin/stale and what changed

**ai-threat-modeling** — factually wrong 2026 codes in three places, in an L3 lesson whose job is precise citation:
- §3 STRIDE "Denial of service": Unbounded Consumption cited as **LLM10:2026** → corrected to **LLM06:2026**.
- §3 STRIDE "Elevation of privilege": Excessive Agency cited as **LLM06:2026** → corrected to **LLM03:2026**.
- §5 "On your own": the Meridian pipeline's compromised-builder scenario cited as "the **LLM03** scenario" → corrected to **LLM04** (matches `ai-pipeline`'s own correct statement that LLM04:2026 added the compromised-build-pipeline scenario).
- Verification done in-session: fetched the primary 2026 final directory listing (GitHub, 2026-10-10) — file names confirm LLM03=ExcessiveAgency, LLM06=UnboundedConsumption, LLM10=ImproperOutputHandling. Source rows staged in `/tmp/sources-add-AI.csv`.
- Additionally verified (defensive check, no change needed): every ATLAS technique name used in the lesson is real, confirmed against the primary `ATLAS.yaml` (mitre-atlas/atlas-data, 452,399 bytes, fetched 2026-10-10): AML.T0020 Poison Training Data, AML.T0053 AI Agent Tool Invocation, AML.T0056 Extract LLM System Prompt, AML.T0057 LLM Data Leakage, AML.T0070 RAG Poisoning, AML.T0080 AI Agent Context Poisoning, AML.T0110 AI Agent Tool Poisoning. The lesson's technique-name-only references were *not* fabricated. Row staged in `/tmp/sources-add-AI.csv`.
- No level change; lesson remains L3. Nothing padded — the substance was already there; the citations were wrong.

**ai-prompt-injection** — five stale internal lesson IDs from an older naming scheme, including in the "Leads to" section (dead cross-references readers would chase):
- §2: `(the `ai-01` lesson)` → `(the `ai-llm-architecture` lesson)`.
- §10: `ai-03a/03b/03c` (three rows) → `ai-llm-top10` (the three Top-10 risk families are sections of the single top10 lesson, which is why the old a/b/c split dissolved); `ai-04` → `ai-pipeline`; `ai-05` → `ai-threat-modeling`.
- Spot-checked the edition claim in §6 ("LLM07 in 2025; LLM08 Hidden Context Exposure in 2026") against secondary sources: **correct** — LLM07:2025 was System Prompt Leakage. No change.
- AML.T0051 citation verified against primary ATLAS.yaml (name: "LLM Prompt Injection"; sub-techniques .000 Direct, .001 Indirect, .002 Triggered) — the lesson's claim holds. Row staged in `/tmp/sources-add-AI.csv`.
- No level change; remains L3.

## Staleness watch (verified, no action)

- OWASP LLM Top 10:2026 final listing confirms the code ordering every AI lesson teaches; the edition note in each lesson is accurate.
- EU AI Act amendment status (Digital Omnibus through Aug 2026) and NIST AI RMF 1.0 revision announcement (Apr 2026) in `ai-governance` are ledger-backed (sources.csv, verified 2026-10-09); both are flagged as moving and dated, which is the honest treatment.
- SEC598/SEC535 titles in `ai-sec-automation` were not re-verified in this session (the brief's §3 correction — SEC598→GASAE, SEC535→GOAA — is the anchor, and the lesson uses it correctly). If a coordinator re-checks paid-course titles, flag it.

## Follow-up recommended (not mine to act on)

- OWASP has published a separate **Top 10 for Agentic Applications — 2026** (ASI01–ASI10, via genai.owasp.org). It is outside the §5 scope (which names only the LLM Top 10:2026) and the lessons are correct at their stated scope — but a coordinator may want a gaps.md entry on whether the AI track should reference it.

## Verification (edited files only)

- `ai-threat-modeling.md`: exactly 10 `^## ` sections; frontmatter intact (`lesson_id:` present); no banned voice words; no currency symbols in new copy; no test servers started by this audit (none were running — nothing in the deepening required a run).
- `ai-prompt-injection.md`: same checks pass.

NEVER committed, NEVER pushed, build_site.py untouched.
