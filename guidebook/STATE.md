# STATE.md — security guidebook build

**Last updated:** 2026-10-10 · **Phase:** Content-depth audit + deepening (all 110 lessons)

## Depth audit — 2026-10-10 (integrated)

Dino's order: review every lesson, add more only where genuinely warranted. Six stage crews audited all 110 lessons against brief §1/§6/§7 with a pad-free rule (never flag for length alone; "If you can't fill 'How it works' and 'Walkthrough' with substance, that is a gap. Log it. Don't pad.").

**Verdict: 105 SOLID, 5 DEEPENED.** Per-lesson tables in `reports/DEPTH-AUDIT.md` (merged from the six crew files, kept alongside).

Deepened in place:
- `a-linux-cli` — added the brief §5-mandated package-management and services/daemons sections the lesson was missing (read-only commands run, transcript in `runs/a-linux-cli.log`); level stays L3.
- `a-windows-concepts` — added PowerShell execution policy (the first thing that bites a beginner; policy list, scope precedence, "not a security boundary" per Microsoft's own doc); replaced a duplicated §7 URL with the registry-value-types reference; level stays L2.
- `b-practice-targets` — DVGA run for real from source (DB built; `ss` pair proving the README's 0.0.0.0 bind vs loopback). Docker Hub unreachable from the build network (logged in gaps.md with evidence).
- `ai-threat-modeling` — corrected three factually wrong OWASP LLM Top 10:2026 codes (Unbounded Consumption = LLM06, Excessive Agency = LLM03, build-pipeline scenario = LLM04); every ATLAS technique name used verified real against primary `ATLAS.yaml`.
- `ai-prompt-injection` — fixed five stale internal lesson IDs (dead cross-references); AML.T0051 citation verified against ATLAS.yaml.

Factual-freshness fixes (one-liners, all verified in-session): RFC 6797 fetched (killed a "fetch at build time" placeholder in b-security-headers); PortSwigger logic-flaws page fetched (b-business-logic); rfc6265bis confirmed still a draft (b-csrf); MDN CSP guide verified (b-xss); `e-system-lifecycle` §7 corrected from SP 800-88 Rev. 1 (withdrawn 2025-09-26) to Rev. 2; `e-iam` duplicate role entry removed + wrong 5.6 map-ref fixed; malformed backtick markdown fixed in 4 E lessons; `e-facility-design` citation corrected to (fema.gov).

**Coordinator-wide normalization:** legacy lesson-ID scheme in "Leads to" sections (E-GOV-01, E-D7-10, E-D2-06, E-D3-01, E-AI-01, C-CVD-01, B-BTY-01, D-DFIR, C-IR, E-LEAD, E-GOV-AI, E-D1-08, E-D7-03, E-D1-11, E-D1-07, E-AI-SC, E-AI-TM, ai-01/03a/b/c/04/05) mapped to current slugs across 16 lessons; the self-referential E-D7-10 line in e-bcp-drp removed. Zero residual legacy IDs.

**Sources:** 11 new `verified` ledger rows (sources.csv 334 → 345, 341 verified). Note: two crews' `/tmp` staging files were wiped by their VMs before the merge; 15 rows reconstructed from the lesson diffs and audit files, every URL re-fetched in-session by the coordinator (one row uses the raw.githubusercontent.com URL after github.com blob returned 503); DEa's 4 verification-only rows skipped as duplicates of existing rows.

**Verification gate:** build clean (zero errors); all 110 lessons exactly 10 `##` sections + intact frontmatter; 5,039 internal links, 0 broken; all 110 lesson pages carry the level badge (the 12 pages without are maps/stages/paths, by design); no banned voice words or currency symbols in new copy; zero stray test servers.

Nothing committed, nothing pushed — parent's lane.

**Last updated:** 2026-10-10 · **Phase:** Frontmatter refactor — lessons as data (brief §4)

## Frontmatter refactor (2026-10-10)

Brief §4 requires lessons stored as data with fields for stage, level, prerequisites, roles, map references, sources and test date, with paths/maps/stages/counts generated from those fields.

**Done:**
- All 110 lesson files carry YAML frontmatter: `lesson_id, slug, stage, level, prerequisites, roles, map_refs, test_date, description, dateline`. The old `**ID:**` meta line was removed (redundant); the prose `**Map refs:**` line stays as body content.
- `build_site.py` refactored: `load_registry()` reads + validates every frontmatter block (hard build error on any inconsistency); the LESSONS table is deleted; LINKMAP/TOTAL derive from the registry; CISSP_DOMAINS and CAISP_CHAPTERS are prose-only (objective/chapter → lessons inverted from `map_refs` at build); PATHS/STAGES keep editorial ordering but every id is validated against frontmatter.
- Every lesson page renders a visible level badge ("Level 3 · Apply — do it unaided on an unfamiliar authorized target…") and prerequisites as links.
- 9 new crew lessons integrated: `a-crypto` (A, L2, CISSP 3.6), `b-api-abuse`, `b-ssti`, `b-xxe`, `b-deserialization`, `b-graphql`, `b-race-conditions`, `b-jwt-oauth` (B, L3), `ai-sec-automation` (AI, L2, walkthrough being finalized). Path placement (done 2026-10-10, same session): the 7 Stage B lessons carry `roles: [pentester, appsec]` and are listed in the pentester path's "Practitioner, full" group and the appsec path's "Vulnerability classes, from the fix side" group (build cross-validates roles↔paths, zero errors). `a-crypto` keeps `roles: []` — it lives on the Stage A page; no path claims. Index lede + meta now name the "Stage B second wave"; sitemap regenerated with all 8 URLs.

**Verification gate:** 130 pages build with zero errors; 4,988 internal links, 0 broken; all 110 lesson pages show the level badge + prerequisites row; zero regressions vs pre-refactor snapshot (only intended additions: stage-a +crypto, stage-b +api-abuse/ssti/xxe/deserialization/graphql/race-conditions/jwt-oauth, map-cissp 3.6 +crypto).

**Data contract:** frontmatter is canonical. New lessons must ship with frontmatter or the build fails loudly. `map.md` is a frozen research artifact.


**Last updated:** 2026-10-10 · **Phase:** Governance-framework lessons (integrated, uncommitted)

## Governance-framework lessons — 2026-10-10 (integrated)

Dino's order: whole permissions, keep going until production-ready. The three E-GOV lessons from the 05b dossier — the last "Still to come" on the GRC path — written to the full 10-part spec, original prose, no prices/fees/salaries/currency symbols anywhere.

- `lessons/e-csf-20.md` (2,306 words) — NIST CSF 2.0: outcomes-not-actions philosophy; Core/Profiles/Tiers; the 6 Functions with Govern new at the center; the 22 Categories transcribed from the document's own Table 1 (verified in-session against the downloaded CSWP 29 PDF — the first from-memory draft had only 20 and mislabeled PR.AA; corrected, logged in runs/e-csf-20.log); Current-vs-Target profiles and the gap→action-plan method; Tiers 1–4 (Partial/Risk Informed/Repeatable/Adaptive) as a communication aid; "no such thing as CSF certified." Walkthrough: worked gap assessment for fictional Meridian Analytics (6 categories fully worked, 16 as the reader's task) + prioritized action plan + tier rationale, self-reviewed (`runs/e-csf-20.log`).
- `lessons/e-iso27001.md` (2,142 words) — ISO/IEC 27001: one line that the standard is a paid document (no prices, verified zero currency symbols); ISMS concept; Clauses 4–10 vs the 93-control Annex A catalog in four themes (organizational/people/physical/technological — from ISO's free Help Centre page); risk assessment as the selection engine; the Statement of Applicability as the load-bearing artifact; voluntary certification via accredited bodies. Walkthrough: theme-level readiness checklist + SoA sketch with risk-tied justifications incl. one honest exclusion and one scoped partial (`runs/e-iso27001.log`).
- `lessons/e-soc2.md` (2,042 words) — SOC 2 and the Trust Services Criteria: examination engagement by a CPA (attestation report, not a certificate; no pass/fail); five criteria with Security mandatory; criteria follow commitments; Type I (design at a point in time) vs Type II (operating effectiveness over a period); restricted-use report; SOC 1 vs SOC 2 vs SOC for Cybersecurity per the AICPA's 2022 testimony. Walkthrough: scoping memo for Meridian Analytics — commitments inventory → criteria → boundary with carve-outs → Type I→II sequencing → per-criterion evidence list (`runs/e-soc2.log`).

Sources: 7 new `verified` ledger rows fetched in-session 2026-10-10 (NIST CSF hub; CSF Quick-Start Guides page; CSWP 29 PDF downloaded 1,518,858 bytes; ISO 27001:2022 standard page — Edition 3 confirmed current; ISO Help Centre ISMS overview; AICPA TSC 2017+2022 resource page; AICPA Blanco-Best testimony PDF on dol.gov). sources.csv: 305 → 312 rows (308 verified). Edition currency re-confirmed: CSF 2.0 still current (2-year anniversary Feb 2026, no newer edition); ISO/IEC 27001:2022 Edition 3 still current; TSC 2017 with revised points of focus 2022 still current.

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` — 3 LESSONS rows (`e-csf-20`→`csf-20`, `e-iso27001`→`iso27001`, `e-soc2`→`soc2`); reading order extended; GRC path "Still to come" note replaced with a real "Governance frameworks" group; `numword()` fixed for 100+ (was IndexError at 101 lessons — now "one hundred one"). Pages: `g/csf-20/`, `g/iso27001/`, `g/soc2/` + rebuilt `g/index.html`, `g/stage-e/`, `g/path/grc-analyst/`. Sitemap: 209 → 212 URLs (hand-maintained). Marker check: 6/6 URLs 200 with H1 — ALL PASS. Price scan clean on new pages. Hygiene: test http.server killed in the same command; zero remain.

Remaining gaps: AICPA SOC 2 overview page fetch timed out (lesson ships with 2 verified resources; re-check at build); CIS Benchmarks ledger row (403); man-pages row (no URL by definition); Docker/AI-model/Windows walkthrough steps (honestly labeled).

**Last updated:** 2026-10-10 · **Phase:** CISSP coverage wave (integrated, uncommitted)

## CISSP coverage wave — 2026-10-10 (integrated)

Dino's order: whole permissions, keep going until production-ready. All 45 remaining CISSP objectives written as Stage E lessons in five parallel batches (D1: 10, D2: 6, D3: 9, D4/5/6: 9, D7: 11). The map page now shows **62 of 62** objectives covered — zero "No lesson yet."

**New lessons** (all 1,800–2,500 words, exact ten-section sequence, ≤3 free resources, no currency symbols, no outline text reproduced):
- D1: `e-ethics` (1.1), `e-security-concepts` (1.2), `e-governance` (1.3), `e-cyber-law` (1.4), `e-investigations` (1.5), `e-policy-docs` (1.6), `e-personnel-security` (1.8), `e-threat-modeling-concepts` (1.10), `e-supply-chain-risk` (1.11), `e-awareness-training` (1.12)
- D2: `e-asset-classification` (2.1), `e-handling-requirements` (2.2), `e-asset-provisioning` (2.3), `e-data-lifecycle` (2.4), `e-retention-eol` (2.5), `e-data-protection-controls` (2.6)
- D3: `e-secure-design` (3.1), `e-security-models` (3.2), `e-control-selection` (3.3), `e-platform-security` (3.4), `e-arch-vuln-assessment` (3.5), `e-cryptanalysis` (3.7), `e-facility-design` (3.8), `e-facility-controls` (3.9), `e-system-lifecycle` (3.10)
- D4/5/6: `e-network-architecture` (4.1), `e-network-components` (4.2), `e-secure-channels` (4.3), `e-auth-systems` (5.6), `e-assessment-strategy` (6.1), `e-control-testing` (6.2), `e-security-metrics` (6.3), `e-test-analysis-reporting` (6.4), `e-security-audits` (6.5)
- D7: `e-investigation-forensics` (7.1), `e-logging-monitoring` (7.2), `e-config-management` (7.3), `e-secops-concepts` (7.4), `e-media-protection` (7.5), `e-incident-management` (7.6), `e-detective-preventive` (7.7), `e-patch-management` (7.8), `e-change-management` (7.9), `e-physical-security` (7.14), `e-personnel-safety` (7.15)

**Walkthroughs:** worked-case pattern (fictional companies, labeled) authored + self-reviewed in-session; real local demos where they fit — BLP rules engine (3.2), brute-force/birthday/frequency-analysis math (3.7), config drift checker (7.3), findings-triage scorer (6.4), data-state inventory (2.6), sanitization overwrite demo (2.4), hashing demo (1.2). Every step RUN with transcript in `runs/` or honestly marked. No Docker/Windows/AI-model steps — labeled per the ratified substitution policy.

**Sources:** 91 new `verified` ledger rows (sources.csv 214 → 305), every URL fetched in-session 2026-10-10 with char counts. Batch manifests in `manifests/batch-{d1,d2,d3,d456,d7}.json`.

**Corrections applied (all verified in-session, not smoothed):**
- SP 800-88 Rev. 1 withdrawn 2025-09-26 (NIST's own CSRC page) → Rev. 2 current; `e-media-protection` updated from Rev. 1 to Rev. 2.
- SP 800-63-4 (July 2025) supersedes 800-63-3; `e-iam` §7 updated to the 4th revision.
- SP 800-55 Rev. 1 withdrawn 2024-12-04 → Vols. 1+2 current (already right in `e-security-program`).
- SP 800-50 (2003) withdrawn Sept 2024 → Rev. 1 (Sept 2024) current.
- NISTIR 7316 is "Assessment of Access Control Systems," not an ABAC paper — `e-iam` §7 corrected.
- CISA BOD 22-01 revoked 2026-06-10 → BOD 26-04.
- `e-secure-design`'s Map ref narrowed to 3.1 (it claimed 3.1/3.3/3.4; the dedicated 3.3/3.4 lessons stand).
- 18 spec-code "Leads to" refs (E-Dxx) rewritten as real backticked lesson ids across D1/D3 batches.
- `e-crypto-applied`'s Map-ref 3.7 gap note now points to `e-cryptanalysis` (conflict resolved).

**Integration** (working tree only — NOT committed, NOT pushed): `build_site.py` — 45 LESSONS rows, CISSP_DOMAINS all 45 gaps filled, Stage E stage page lists all 52 Stage E lessons in domain order, GRC path gained Asset-security + Assessment-and-testing sections ("Still to come" now only the governance-framework lessons), index lede + meta mention the CISSP coverage wave. Pages: 45 new `g/<slug>/` + rebuilt `g/index.html`, `g/stage-e/`, `g/map-cissp/`, `g/path/grc-analyst/`. Sitemap: 164 → 209 URLs (45 new lesson URLs, lastmod 2026-10-10; hand-maintained — no sitemap builder exists in build_site.py). Marker check: 12/12 URLs 200 — ALL PASS (`runs/site-integration.log` pattern; pgrep self-match noted, zero http.servers remain). Price scan clean on new pages. `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held (no commit, no push per task).

**Remaining gaps (not this wave):** governance-framework lessons (NIST CSF 2.0, ISO/IEC 27001, SOC 2 — research specified E-GOV-01/02/03, never written); CIS Benchmarks ledger row (403); man-pages row (no URL by definition); Docker/AI-model/Windows walkthrough steps (honestly labeled).

## Gap-closing sprint, environment track — 2026-10-10 (integrated)

Dino's order: close the gaps first. Installed what the build machine can actually carry and re-ran the "not run by us" walkthrough steps for real; updated lessons + run logs + pages honestly. Nothing committed, nothing pushed — working tree only, HEAD still 17f437a.

**Installed and ran for real (loopback only):**
- nmap 7.94SVN — `nmap -sT -p 18499 127.0.0.1` → `18499/tcp open` against a local demo listener (`runs/b-toolbench.log`).
- tcpdump 4.99.4 — full loopback capture: SYN / SYN-ACK / ACK / data / FIN, 10 packets (`runs/a-tcpip-ports.log`). a-tcpip-ports step 8 marker closed; step 5 (UDP) stays unrun — sandbox blocks UDP loopback.
- dig (DiG 9.18.39, already present) — A, CNAME, TXT, NS, NXDOMAIN re-ran with real dig `+tcp -p 53535 @127.0.0.1` (`runs/a-dns-depth.log`). DNSSEC step stays unrun.
- Playwright headless Chromium — b-xss steps 4/6 markers fired for real (`EXEC-REFLECTED`, `EXEC-DOM`; fixed build inert); b-csrf step 4 (attacker's page changed the victim email for real); b-security-headers steps 3 (CSP blocked an unencoded inline handler, violation in console) and 4 (cross-origin frame refused per `frame-ancestors 'self'`) — all observed browser behavior, not header presence. `runs/b-xss.log`, `runs/b-csrf.log`, `runs/b-security-headers.log`.
- Semgrep 1.180.0 — the earlier "dead shim" report is superseded; engine matched a local rule for real (`runs/b-toolbench.log`).

Install notes: `apt-get update` hangs on this machine's mirrors (zero-CPU stall), so nmap/tcpdump came as .debs via curl from archive.ubuntu.com + dpkg (full dep chain resolved by hand); Playwright via pip (`--break-system-packages`); Semgrep in a clean venv (system pip refused on a typing_extensions RECORD conflict). This container has no `tcpdump` user, so captures need `-Z root`.

**Confirmed-unavailable (verified once, logged):** Docker (`command -v docker` empty — daemon install out of scope); local AI model (no ollama, no GPU, no weights); Windows (no Windows on the bench); sshd (no binary; long dep chain, out of scope). Still not installed: ffuf, subfinder/dnsx/httpx/amass, katana/gau/waybackurls, Burp/Caido/mitmproxy, Autorize/AuthMatrix, JWT Editor/jwt_tool, CodeQL, Trivy/Gitleaks, Flameshot/Dradis.

**Integration:** six lessons' "not run by us" markers updated (`b-toolbench`, `a-tcpip-ports`, `a-dns-depth`, `b-xss`, `b-csrf`, `b-security-headers`); six pages rebuilt (`g/toolbench/`, `g/tcpip-ports/`, `g/dns-depth/`, `g/xss/`, `g/csrf/`, `g/security-headers/`); `gaps.md` gained a resolved list with evidence. Hygiene: all demo servers killed by explicit PID; `pgrep -fa "http.server" | grep -v "pgrep -fa"` confirms zero remain; all lab ports free. Standing rule held — no commit, no push.

Open decisions carried (not resolved): (1) OWASP LLM Top 10 2026-vs-2025 edition question (brief still says 2025; guidebook teaches the verified 2026 edition); (2) walkthrough substitution policy (local-demo / not-run steps vs Docker/model machine).

## Bug bounty + stage pages — 2026-10-09 (integrated)

Dino's order: keep building. One final Stage B lesson plus the five stage pages (brief §4: a new page type — the novice-to-expert backbone). Original prose throughout, no prices/fees/salaries anywhere.

- `lessons/b-bug-bounty.md` (2,410 words) — Bug bounty mechanics: program anatomy (scope, RoE, safe harbor), program types (public/private/time-bound/VDP), the report lifecycle (submit → triage → reward → remediate → retest), the three validity gates, impact-writing as the paid-vs-informative difference, reading disclosed reports as the textbook. Worked example: the five-part triage-ready report anatomy built on the b-idor finding. Walkthrough: all 8 steps ran (`runs/b-bug-bounty.log`) — full dry-run report drafted against the fictional Harborlight Books IDOR (title, summary, reproduction steps, impact, remediation), self-scored 10/10 against the anatomy, duplicate-check habits, fictional scope re-read signed off. No real submission, no live target (by design). Level 3, labeled honestly.

**Stage pages** (generated from data, not hand prose — STAGES table in build_site.py, lesson doors filtered from the LESSONS table in reading order): `/g/stage-a/` (9 lessons; milestone: the login-to-render path packet by packet; claim: nothing yet — the brief's own reasoning), `/g/stage-b/` (14 lessons; milestone: first valid finding submitted to an authorized program), `/g/stage-c/` (10 lessons; milestone: coordinated disclosure completed + CVE record crediting the reader), `/g/stage-d/` (6 lessons; milestone: a capstone body of work in one track — the brief names no single Stage D artifact, the page says so), `/g/stage-e/` (7 lessons; milestone: managerial/architectural breadth; claims block states the CISSP 5-year/Associate-of-ISC2 rule as the issuer's rule). Each page: eyebrow, goal lede, "The milestone", "The lessons" (numbered doors in reading order), "What you can honestly claim", "What comes next" (stage chain A→B→C→D→E→AI track).

Sources: 6 new `operator-added` ledger rows (HackerOne explainer, Bugcrowd researcher docs, Hacktivity, Hacker101, Intigriti, PortSwigger Academy — from night research, not re-fetched this session; re-fetch at publish). No new `verified` rows this batch (no pages fetched).

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended — 1 LESSONS row (`b-bug-bounty`), STAGES table (key/slug/title/lede/milestone/claims/next/ordered lesson ids) + `build_stage_pages()` following the `build_index()` pattern + STAGEMAP; every lesson page's "Keep going" note now links back to its stage page (AI track lessons have no stage page — no link, by design); `/g/index.html` gained a "Stages" section; reading order extended with Bug bounty mechanics; index now lists 53 lessons ("Fifty-three lessons"). Pages: `g/bug-bounty/` + `g/stage-a/`…`g/stage-e/` + rebuilt `g/index.html` (+ all lesson pages rebuilt for the Keep-going link). Sitemap: 147 → 153 URLs (`lastmod 2026-10-09`). Marker check: 8/8 URLs 200 — ALL PASS (`runs/site-integration.log`; the one 3/4 was the known false-FAIL class — "not run by us" legitimately absent since the walkthrough fully ran — corrected on recheck). Price scan clean. `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held, HEAD still 17f437a. Hygiene: marker-check http.server killed by explicit PID (the `$SRV` shell-variable kill missed again — same trap as earlier batches); pgrep confirms zero remain.

Open decisions carried (not resolved): (1) OWASP LLM Top 10 2026-vs-2025 edition question (brief still says 2025; guidebook teaches the verified 2026 edition); (2) walkthrough substitution policy (local-demo / not-run steps vs Docker/model machine).

## Final wave: Stage D wave 2 + Stage C remainder — 2026-10-09 (integrated)

Dino's order: keep building. Four lessons written to the full 10-part spec, original prose, no prices/fees/salaries anywhere. Safety line held throughout: concepts + defender telemetry + detection only for the offensive-adjacent lessons; no working exploits, no malware, no evasion tooling.

- `lessons/d-dfir-deep.md` (2,510 words) — DFIR deep: order of volatility, copies-first evidence handling, disk artifacts (MFT/USN/prefetch/registry), the Volatility workflow (imageinfo→pslist→netscan→malfind), network evidence tiers (PCAP/Zeek/NetFlow), hypothesis-driven threat hunting. Walkthrough: all 7 steps ran (`runs/d-dfir-deep.log`) — labeled synthetic evidence (21-line merged super-timeline, UTC-normalized), IOC extraction, chain-of-custody hashes, findings memo. One honest correction logged (first normalizer dropped the sudo line and truncated disk lines; fixed, re-ran 21/21).
- `lessons/d-exploit-concepts.md` (2,077 words) — Exploit dev + RE concepts: flaw-to-control via the return address, the mitigation landscape (NX/DEP, ASLR/PIE, canaries, RELRO, FORTIFY, CFI) with what each breaks, disassembly vs decompilation workflow. Walkthrough: all 6 steps ran (`runs/d-exploit-concepts.log`) — ASLR demo (addresses change every run; frozen under `setarch -R`), readelf checksec-style survey of 7 system binaries (all four mitigations on everywhere), deliberately unhardened build (all four off). Training targets only; pwn.college's no-solutions rule stated. Demo binaries deleted after.
- `lessons/c-public-track-record.md` (2,006 words) — Building a public track record: the recognition pathway's keystone — root-cause-first write-ups, the Project Zero bar, one finding in two formats (research write-up + one-page bounty report), honest impact discipline. Walkthrough: no CLI by design — worked write-up of the b-sqli lab finding through the 7-step self-review checklist (`runs/c-public-track-record.log`).
- `lessons/c-ai-tooling.md` (2,195 words) — AI tooling professionals use: Anthropic's CVP as the dated worked example — three tiers (Defense: orgs + qualifying individual researchers, days; Red Team: org-only, weeks, ransomware still blocked; Specialized: org-only safety-critical, US-government review), Glasswing numbers (129,000+ verified vulns Apr–Jul 2026), CyScenarioBench 0/4/34-of-50 with the vendor-eval caveat. Brief §3 correction as the spine: access to tooling, NEVER a credential/milestone/CV line. Walkthrough: no CLI by design — dated evidence-map worksheet against the guidebook's fictional track record (`runs/c-ai-tooling.log`). Every CVP statement dated 2026-10-06 or 2026-10-09.

Sources: 1 new `verified` ledger row fetched in-session (CellCog CVP page, which read Anthropic's 2026-10-06 announcement; 6+ outlets consistent) + 15 `operator-added` (Anthropic announcement URL — guessed path 404'd, gap logged; SP 800-86; Volatility 3; SIFT; Autopsy; Eric Zimmerman tools; pwn.college; how2heap; OST2; Ghidra; exploit.education; ROP Emporium; Project Zero blog; Kettle HTTP/2 — exact article URL not fetched, row says so; Anthropic Help Center cyber safeguards).

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended (4 LESSONS rows; LINKMAP auto-extends; index now lists 52 lessons; lede + reading order extended: Stage D wave 2 Exploit concepts → DFIR deep; Stage C remainder Vulnerability ecosystem → Public track record → AI tooling). Pages: `g/dfir-deep/`, `g/exploit-concepts/`, `g/public-track-record/`, `g/ai-tooling/` + rebuilt `g/index.html`. Sitemap: 143 → 147 URLs (`lastmod 2026-10-09`). Cross-links wired via LINKMAP (dfir-deep after incident-response; exploit-concepts after redteam-concepts; public-track-record after vuln-ecosystem; ai-tooling after ai-governance). Marker check: 4/4 new pages + `/g/` (Fifty-two lessons) + `/sitemap.xml` — ALL PASS (`runs/site-integration.log`; dfir-deep's first FAIL was the wrong-marker class — "not run by us" legitimately absent since the walkthrough fully ran — corrected on recheck). Price scan clean. `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held, HEAD still 17f437a. Hygiene: both marker-check http.servers killed by explicit PID in the same command; pgrep confirms zero remain.

Open decisions carried (not resolved): (1) OWASP LLM Top 10 2026-vs-2025 edition question (brief still says 2025; guidebook teaches the verified 2026 edition); (2) walkthrough substitution policy (local-demo / not-run steps vs Docker/model machine).

## AI track completion + program leadership — 2026-10-09 (integrated)

Dino's order: keep building. Four lessons written to the full 10-part spec, original prose, no prices/fees/salaries anywhere:

- `lessons/ai-pipeline.md` (2,267 words) — AI attacks and defenses in the build pipeline (CAISP ch.4): training-data poisoning, build provenance, registry hygiene, the compromised-builder LLM04 scenario, and the red-team CI gate — each attack paired with its defense. Walkthrough: all 6 steps ran (`runs/ai-pipeline.log`) — deterministic harness (dataset manifest → tamper caught/named/filed → forged provenance rejected → red-team gate 12/12 clean, backdoored model caught on the trigger prompt, promotion blocked, regression test logged). Python 3.12, no network, no model.
- `lessons/ai-threat-modeling.md` (2,416 words) — Threat modeling AI systems (CAISP ch.5): data-flow mapping, five trust boundaries (prompt/retrieval/tool/memory/pipeline), STRIDE adapted to AI, ATLAS as the TTP library, risk register with owned treatments. Walkthrough: no CLI by design — full Harborlight Books threat model authored + self-review checklist (`runs/ai-threat-modeling.log`).
- `lessons/e-security-program.md` (2,206 words) — Running a security program: the Govern bidirectional loop, KPI vs KRI (CSF 2.0 §5), SP 800-55 measurement method, vanity-metric discipline, risk-based prioritization, the program charter as worked artifact (Beacon Logistics). Walkthrough: no CLI by design (`runs/e-security-program.log`).
- `lessons/e-board-communication.md` (2,088 words) — Board-level communication: the one-page memo (protect/stand/risks/changed/decisions + appendix), what to report vs leave out, the director test, the ninety-second incident briefing. Walkthrough: no CLI by design (`runs/e-board-communication.log`).

**Correction applied before publish (not smoothed):** the new `ai-pipeline` draft cited wrong 2026 codes (LLM03/LLM04 for Supply Chain / Data+Model Poisoning) and the guidebook carried a wrong release date (2026-09-30). Fetched the official GenAI repo `2026/` directory in-session: final mapping is **LLM04:2026 Supply Chain**, **LLM05:2026 Data and Model Poisoning**, **released August 4, 2026**. Fixed in `ai-pipeline.md` (10 occurrences), the date in 6 files (zero stale occurrences remain), map.md, sources.csv (row upgraded to verified), gaps.md. The earlier AI lessons already had the right codes — confirmed against the same page.

Sources: 5 new `verified` ledger rows fetched in-session (SLSA spec; SP 800-55 release page; NIST CSF 2.0 page; MITRE ATLAS matrix; OWASP LLM Top 10:2026 final list + release date) + 1 `operator-added` (SP 800-55 volumes unread — release page only).

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended (4 LESSONS rows; LINKMAP auto-extends; index now lists 48 lessons; reading order extended: AI track … → AI pipeline → AI threat modeling; Risk assessment → … → BCP/DR → Security program → Board communication). Pages: `g/ai-pipeline/`, `g/threat-modeling-ai/`, `g/security-program/`, `g/board-communication/` + rebuilt `g/index.html` + rebuilt `g/prompt-injection/`, `g/llm-top10/`, `g/supply-chain/` (date corrections). Sitemap: 139 → 143 URLs (`lastmod 2026-10-09`). Cross-links wired via LINKMAP. Marker check: 4/4 new pages + `/g/` + `/sitemap.xml` — ALL PASS (`runs/site-integration.log`; one false FAIL from a wrong "not run by us" marker on ai-pipeline, corrected on recheck — same class as osint-research). Price scan clean. `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held, HEAD still 17f437a. Hygiene: marker-check http.server killed by explicit PID after the shell-variable kill missed a 4th time; pgrep confirms zero remain.

Open decisions carried (not resolved): (1) OWASP LLM Top 10 2026-vs-2025 edition question (brief still says 2025; guidebook teaches the verified 2026 edition); (2) walkthrough substitution policy (local-demo / not-run steps vs Docker/model machine).

## Stage A remainder wave — 2026-10-09 (integrated)

Dino's order: keep building. Four Stage A remainder lessons written to the full 10-part spec, original prose, no prices/fees/salaries anywhere:

- `lessons/a-python-security.md` (2,020 words) — Python for security tooling: read/change/write small scripts — urllib requests, JSON parsing, sockets, argparse, files. The read-first discipline (imports → entry point → outward) as the lesson's core skill. Walkthrough: all 7 steps ran (`runs/a-python-security.log`) — Python 3.12.3, local stdlib HTTP server on 127.0.0.1:8471, fetch/parse/URLError-branch/socket roundtrip/`--save` edit, server killed by PID. Stdlib only, nothing external touched.
- `lessons/a-reading-code.md` (2,079 words) — Reading code through a vulnerability: source→path→sink tracing in JavaScript (form input, fetch, innerHTML) and SQL (clause reading order, concatenation vs placeholders). Walkthrough: all 6 steps ran (`runs/a-reading-code.log`) — labeled teaching snippets; benign vs `' OR '1'='1` input traced through both builders; hostile query printed, never executed against a database.
- `lessons/a-windows-concepts.md` (2,235 words) — Windows concepts: registry hives, value types, services, event logs, PowerShell objects, NTFS/UAC, the Linux→Windows translation table. **Level 2, labeled honestly** — no Windows on the build bench, so all five hands-on steps are **not run by us** with exact reader procedures; nothing invented. What was verified in-session: Microsoft "Registry Hives" + "Get-WinEvent" references fetched 2026-10-09 (`runs/a-windows-concepts.log`).
- `lessons/a-osint-research.md` (2,249 words) — OSINT and research discipline: passive vs active (the bright line), what "public" means vs exposed, the standard sources, re-derivable documentation, the ethics stated plainly. Walkthrough: all 6 steps ran (`runs/a-osint-research.log`) — fictional `harborlight-books.example` dossier as local files only; 9 findings table; zero packets left the machine; no real target touched.

Sources: 5 new `verified` ledger rows fetched in-session (docs.python.org/3/tutorial; javascript.info; sqlbolt.com; Microsoft Registry Hives; Microsoft Get-WinEvent — all 2026-10-09) + 7 `operator-added` (py4e; Automate the Boring Stuff; SQLite lang ref; MS Learn registry training module; WSTG info-gathering; OSINT Framework; Bellingcat toolkit).

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended (4 LESSONS rows; LINKMAP auto-extends; index now lists 44 lessons; lede + meta description mention the remainder wave; reading order extended: Linux CLI → Windows concepts → Git & GitHub → HTTP in depth → Python for security → Reading code → OSINT & research discipline → Authorization & scope). Pages: `g/python-security/`, `g/reading-code/`, `g/windows-concepts/`, `g/osint-research/` + rebuilt `g/index.html`. Sitemap: 135 → 139 URLs (`lastmod 2026-10-09`). Cross-links wired via LINKMAP (python→reading-code→b-sqli/b-xss/b-command-injection; windows→c-log-sources/d-malware-analysis; osint→b-authorization-scope/b-methodology). Marker check: 6/6 PASS (`runs/site-integration.log`; first osint-research FAIL was a wrong marker — "not run by us" legitimately absent since that walkthrough fully ran — corrected on recheck). Price scan clean. `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held, HEAD still 17f437a. Hygiene: `kill $SRV` missed a third time (shell-variable trap); orphan PID 11631 killed by explicit PID; pgrep confirms zero http.servers remain, port 8499 closed.

Open decisions carried (not resolved): (1) OWASP LLM Top 10 2026-vs-2025 edition question; (2) walkthrough substitution policy (local-demo / not-run steps vs Docker/model machine).

## Stage C disclosure wave — 2026-10-09 (integrated)

Dino's order: keep building. Four Stage C disclosure lessons written to the full 10-part spec, original prose, no prices/fees/salaries anywhere:

- `lessons/c-cvd.md` (2,279 words) — Coordinated vulnerability disclosure: CERT CVD roles/phases/principles, security.txt contact-finding, the report, the timeline, Heartbleed (good, imperfect) vs 2018 zero-day drops (bad) as worked cases. Walkthrough: worked case + runnable local security.txt lab (`runs/c-cvd.log`) — RFC 9116 required-fields validation, lookup order demonstrated.
- `lessons/c-cve-program.md` (2,047 words) — The CVE Program: 555 CNAs, CNA/Root/TLR structure, qualification rule (independently fixable), the five-step request path, Record Format 5.2.0, credits[] schema (finder/reporter/…/other — type optional). Walkthrough: real CVE-2021-44228 record fetched via CVE API (`runs/c-cve-program.log`) — assigner apache, credits entry for Chen Zhaojun, affected block, 53 references; fictional request worksheet + credits JSON drafted. No real request submitted (by design).
- `lessons/c-cvss.md` (2,102 words) — CVSS v3.1 (Base/Temporal/Environmental) and v4.0 (Base/Threat/Environmental/Supplemental) scored by hand: three FIRST official calibration cases with published vectors, metric-level disagreement analysis (AT:P split; E:U collapsing 7.7→5.2; split VC/VI/VA impact model), nomenclature discipline. Walkthrough: fully ran (`runs/c-cvss.log`) — local v3.1 equation implementation reproduced all 3 published scores; FIRST's reference v4.0 implementation (run verbatim) reproduced all 5 published scores. Two corrections logged honestly (Roundup decimal bug; abandoned Python v4.0 port).
- `lessons/c-vuln-ecosystem.md` (2,263 words) — CWE Top 25:2025, CAPEC, CISA KEV, EPSS, and the 2026 NVD change: NIST enriches only prioritized CVEs since 2026-04-15 — government-confirmed via Commerce OIG report OIG-26-020-I (PDF fetched in-session), described as OIG-confirmed not NIST-direct. Walkthrough: fully ran (`runs/c-vuln-ecosystem.log`) — live EPSS for 3 CVEs, KEV CSV membership, three-method ranking comparison (CVSS-only vs EPSS-only vs KEV-first disagree on 2nd/3rd place).

Sources: 14 new `verified` ledger rows fetched in-session (CERT CVD guide; OpenSSF finder guide; cve.org CNAs + CVE Services; cve-schema credits[]; FIRST v4.0 spec + examples + reference calculator; EPSS page + API; CWE Top 25; CISA KEV CSV; OIG-26-020-I PDF; CVE-2021-44228 record — all 2026-10-09) + 6 `operator-added` (RFC 9116, OpenSSF maintainer guide, OWASP disclosure cheat sheet, RedHat CVE-HOWTO, Project Zero policy, CAPEC).

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended (4 LESSONS rows; LINKMAP auto-extends; index now lists 40 lessons; reading order extended incident-response → cvd → cve-program → cvss → vuln-ecosystem). Pages: `g/cvd/`, `g/cve-program/`, `g/cvss/`, `g/vuln-ecosystem/` + rebuilt `g/index.html`. Sitemap: 131 → 135 URLs (`lastmod 2026-10-09`). Cross-links wired via LINKMAP (disclosure chain + back-link to b-methodology's reporting phase). Marker check: 4/4 new pages + `/g/` + `/sitemap.xml` — ALL PASS (`runs/site-integration.log`). Price scan clean. `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held, HEAD still 17f437a. Hygiene: marker-check http.server killed in the same command; verified zero remain.

Open decisions carried (not resolved): (1) OWASP LLM Top 10 2026-vs-2025 edition question; (2) walkthrough substitution policy (local-demo / not-run steps vs Docker/model machine).

## Stage B mechanics wave — 2026-10-09 (integrated)

Dino's order: keep building. Four Stage B mechanics lessons written to the full 10-part spec, original prose, no prices/fees/salaries anywhere. Safety line held throughout: local/owned/permissioned targets only; every hands-on lesson opens inside the authorization the first lesson establishes.

- `lessons/b-authorization-scope.md` (2,787 words) — Authorization, scope, and the hard rules: the gating lesson. Written authorization, the ten-element RoE, CFAA (18 U.S.C. § 1030) and the Computer Misuse Act 1990 in plain terms (both statute pages fetched in-session; "not legal advice" stated), the six hard rules quoted verbatim from the brief. Walkthrough: no CLI by design — RoE document for fictional Harborlight Books + five-scenario scope-violation triage + six-rules-from-memory check, self-reviewed (`runs/b-authorization-scope.log`). Level 2, labeled honestly.
- `lessons/b-methodology.md` (2,949 words) — Engagement methodology: WSTG v4.2 (12 categories, ID format), PTES seven phases, NIST SP 800-115 (three methods, three phases) — how the three fit, then the six phases scoping→reporting each defined by what it produces. Walkthrough: no CLI by design — six-document fictional engagement plan (threat model, recon plan, enumeration inventory, proof template, impact paragraph, report outline), self-reviewed (`runs/b-methodology.log`). Primary verification in-session: PTES page now fetches (resolves the old 403 gap); WSTG-ATHZ-04 confirmed as the IDOR test; SP 800-115 PDF fetched (544,047 bytes) and phase/method structure confirmed.
- `lessons/b-toolbench.md` (3,289 words) — The toolbench: the catalog's fifteen phases in activation order — for each, the ONE question it answers, the free tool, how to read its output, what it cannot tell you; the six-step activation order; why sqlmap/Nikto/Nessus/Hydra/second-fuzzer stay off this path. Walkthrough: ran (`runs/b-toolbench.log`) — curl header read, jq extraction, ripgrep triage, ss target sanity, git records, urllib decode on loopback; the rest marked **not run by us** with exact reader procedures. Level 2, labeled honestly.
- `lessons/b-practice-targets.md` (2,304 words) — Practice targets: DVWA, Juice Shop, WebGoat, crAPI, DVGA — one-command setups quoted from the canonical READMEs fetched in-session today (ports :4280, :3000, :8080/:9090, :8888/:8025, :5013 all confirmed); the DVGA loopback-bind correction (README binds all interfaces — lesson teaches the override and the two-bind distinction); reset procedures; run-only-while-practicing discipline. Walkthrough: procedure verification, container runs **not run by us** (no Docker on this machine) (`runs/b-practice-targets.log`). Level 2.

Corrections applied this session (with primary evidence, not smoothed): `b-idor`'s `WSTG-ATHZ-02` → `WSTG-ATHZ-04` in lesson + map.md + rebuilt page (both v4.2 test pages fetched in-session); PTES 403 gap resolved; DVGA :5013 confirmed; build_site.py's hardcoded "twenty-four" in the "Keep going" note replaced with computed `numword(len(LESSONS))` (was drifting against the 32-lesson index) — all pages rebuilt.

Sources: 23 new `verified` ledger rows fetched in-session (WSTG v4.2 + ATHZ-04 + ATHZ-02 pages; PTES guidelines; SP 800-115 landing + full PDF; 18 U.S.C. § 1030; Computer Misuse Act 1990; Bugcrowd researcher docs; HackerOne bounty explainer; DVWA/Juice Shop/WebGoat/crAPI/DVGA READMEs; PortSwigger Academy; nmap.org; ffuf/amass/katana/trivy/gitleaks READMEs; jq manual — all 2026-10-09).

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended (4 LESSONS rows; LINKMAP auto-extends; index now lists 36 lessons; lede mentions the mechanics wave; reading order inserts Authorization & scope → Methodology → Toolbench → Practice targets between HTTP in depth and IDOR). Pages: `g/authorization-scope/`, `g/methodology/`, `g/toolbench/`, `g/practice-targets/` + rebuilt `g/index.html`. Sitemap: 127 → 131 URLs (`lastmod 2026-10-09`). Cross-links wired via LINKMAP (authorization↔methodology↔toolbench↔practice-targets chain + back-links to vuln lessons). Marker check: 7/7 PASS (`runs/site-integration.log`; first attempt's grep-without-`-E` false counts and two missed `kill $SRV`s corrected and logged; final pgrep "STILL RUNNING" was a self-match). Price scan clean. `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held, HEAD still 17f437a. Hygiene: zero http.servers remain (verified, port closed).

Open decisions carried (not resolved): (1) OWASP LLM Top 10 2026-vs-2025 edition question; (2) walkthrough substitution policy (local-demo / not-run steps vs Docker/model machine).

## Stage D specialist wave 1 — 2026-10-09 (integrated)

Dino's order: keep building. Four Stage D lessons written to the full 10-part spec, original prose, no prices/fees/salaries anywhere. Safety line held throughout: concepts + defender telemetry + detection + fixes + established labs only; no working malware, exploit code, C2/phishing kits, or original evasion tooling.

- `lessons/d-redteam-concepts.md` (2,542 words) — ATT&CK as the behavior language (v19.2, 15 tactics — Stealth TA0005 + Defense Impairment TA0112 split taught, stale 14-tactic lists flagged), pentest vs red team vs adversary emulation, C2/beaconing concepts + defender view, evasion as broken defensive assumptions, the purple-team loop. Walkthrough: all ran (`runs/d-redteam-concepts.log`) — tactic mapper (8 observations → 9/15 tactics covered, 6 blind), beaconing statistics (beacon CV 0.060 vs human 0.558), valid Navigator layer JSON (5 techniques); Atomic Red Team is reader-side in their own lab (**not run by us**).
- `lessons/d-malware-analysis.md` (2,392 words) — static vs dynamic and their blind spots, the triage workflow (hash → file ID → strings → imports → entropy), packing concepts, dynamic-analysis streams, behavioral IOCs, YARA rule craft with false-positive discipline. Walkthrough: all ran (`runs/d-malware-analysis.log`) — synthetic benign training files only; SHA-256/file/strings; entropy (random.bin 7.91 vs text.bin 4.44); **real YARA via yara-python**: tight rule matched only the family sample, deliberately loosened rule false-positived on benign.txt (the lesson's core warning, demonstrated), tuned rule (`2 of` + filesize guard) clean; detonation is reader-side in the isolated lab (**not run by us**).
- `lessons/d-cloud-security.md` (2,340 words) — shared-responsibility line (AWS: security *of* vs *in* the cloud), IAM policies read as code, the five classic misconfigurations, Prowler vs ScoutSuite (benchmark checks vs point-in-time picture), cloud logging as the control plane's memory. Walkthrough: all ran (`runs/d-cloud-security.log`) — three policies analyzed with **real Cloudsplaining 0.9.1**: demo-correct 0 escalation findings, demo-overbroad flagged `CreateEC2WithExistingIP` via `iam:PassRole`+`ec2:RunInstances`, demo-broken flagged `CreateAccessKey`/`CreateLoginProfile`/more; two honest corrections logged (output dirs must exist; scan input must be account-authorization-details shape). Live-account scanning is reader-side (**not run by us**).
- `lessons/d-appsec.md` (2,353 words) — STRIDE threat modeling (six prompts + responses), SAST/DAST/IAST/SCA families and what each is blind to (no family sees business logic), SDLC gate integration, code-review technique. Walkthrough: ran (`runs/d-appsec.log`) — STRIDE on the upload flow (worked case); teaching-sketch SAST found all 3 pattern findings (secret :2, SQL-concat :6, weak hash :10) and demonstrably missed the client-controlled discount flaw; diff review with 4 developer-actionable findings; real Semgrep **not run by us** (engine binary non-functional in this sandbox — logged honestly), ZAP/Dependency-Check reader-side. Two sketch corrections logged (paren typo; /tmp vs ~/tmp-guidebook path mix).

Sources: 10 new `verified` ledger rows fetched in-session (ATT&CK Enterprise tactics; Atomic Red Team; YARA 4.4.0 stable docs; REMnux; FLARE VM; Prowler; ScoutSuite; OWASP Threat Modeling cheat sheet; AWS Shared Responsibility; Semgrep quickstart — all 2026-10-09) + 10 `operator-added` (ATT&CK C2 tactic page, LOLBAS, ATT&CK Navigator, RITA, Sysmon docs, Cloudsplaining repo, OWASP ASVS, Stratus Red Team, MalwareBazaar, CIS Benchmarks).

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended (4 LESSONS rows; LINKMAP auto-extends; index now lists 32 lessons; lede 28→32; reading order extended with "Stage D wave 1: Red team concepts → Malware analysis → Cloud security → AppSec"). Pages: `g/redteam-concepts/`, `g/malware-analysis/`, `g/cloud-security/`, `g/appsec/` + rebuilt `g/index.html`. Sitemap: 4 new URLs (`lastmod 2026-10-09`). Cross-links wired via LINKMAP (Stage D lessons link back to Stage B/C prerequisites). Marker check: 4/4 new pages + `/g/` (32 doors) + `/sitemap.xml` — ALL PASS (`runs/site-integration.log`). Price scan clean. `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held, HEAD still 17f437a. Hygiene: marker-check http.server killed by explicit PID after the shell-variable kill missed it; pgrep confirms zero remain.

## AI security track wave — 2026-10-09 (integrated)

Dino's order: keep building. Four AI track lessons written to the full 10-part spec, original prose, no prices/fees/salaries anywhere:

- `lessons/ai-llm-architecture.md` (2,419 words) — How LLM applications are built and where they are attacked: tokens, embeddings, attention-as-weighted-lookup, the six-layer app stack (system prompt, RAG, history/memory, user input, tools, agent loop), output handling; eight-surface attack map. Walkthrough: all 6 steps ran (`runs/ai-llm-architecture.log`) — toy tokenizer, fake-embedding retrieval (poisoned chunk retrieved on similarity, not authorization), prompt assembly (injected instruction present, no provenance), tool registry with code-level policy, scripted agent loop (refund blocked, lookup allowed), attack-surface report.
- `lessons/ai-llm-top10.md` (2,572 words) — The OWASP LLM Top 10:2026 beyond prompt injection: nine risks in data/system/agency families, mechanism + defense each; worked classification of three incident sketches. Walkthrough: all 5 steps ran (`runs/ai-llm-top10.log`) — list, two classification drills, LLM10 output-handling demo (vulnerable shell-interpolation builder drops the marker, fixed argv builder does not). **Correction logged, not smoothed:** first LLM10 run used output containing an apostrophe, which broke shell quoting so the marker never appeared; re-ran quote-free and the demo is honest.
- `lessons/ai-supply-chain.md` (2,279 words) — Provenance discipline: hashes (content identity), SLSA provenance (origin), Sigstore keyless signing (Fulcio/Rekor, four verification checks), CycloneDX AIBOM, the pickle-deserialization hazard, what a poisoned upstream looks like to a defender. Walkthrough: steps 1–5 ran (`runs/ai-supply-chain.log`) — build, hash, tamper-caught (named file, nonzero exit), AIBOM, labeled local pickle demo (code ran at load; hazard files deleted), admission-policy sketch. Step 6 (live cosign/Rekor) marked **not run by us** (needs network + OIDC identity).
- `lessons/ai-governance.md` (2,436 words) — Governing AI: NIST AI RMF 1.0 four functions (voluntary; revision announced April 2026 — noted), GenAI Profile AI 600-1 (twelve risk categories; reader sent to the profile's table), EU AI Act tiers as concepts (unacceptable/high-risk/limited/minimal + GPAI; Digital Omnibus amendments noted), ISO/IEC 42001 as paid in one line per the brief. CAISP kept separate from CertNexus CAIP throughout. Walkthrough: no CLI by design — Meridian Analytics risk register (6 risks, RMF-mapped, owned) + classification memo, self-reviewed (`runs/ai-governance.log`). Level 2, labeled honestly.

CAISP map refs served: ch. 1–2 (ai-llm-architecture), ch. 3 (ai-llm-top10; LLM01 stays in ai-prompt-injection), ch. 6 (ai-supply-chain), ch. 7 (ai-governance). Ch. 4 (pipeline) and ch. 5 (threat modeling) remain as logged future lessons.

Edition rule held: every Top 10 citation names **OWASP LLM Top 10:2026** (released 2026-08-04, renumbered codes — list verified in-session against the official GenAI repo `2026/final/`); visible edition notes carried on the prompt-injection and top-10 pages.

Sources: 5 new `verified` ledger rows fetched in-session (OWASP 2026 final dir; NIST AI RMF page; CycloneDX spec overview; Sigstore docs; EU AI Act summary — all 2026-10-09) + 10 `operator-added` (Appendix B, SLSA, model-transparency, AI 600-1 PDF, ATLAS, HF LLM Course, genai.owasp.org, garak, AI RMF Playbook, IAPP).

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended (4 LESSONS rows; index now lists 28 lessons; lede 24→28; reading order extended with the AI track chain prompt-injection → llm-architecture → llm-top10 → supply-chain → ai-governance). Pages: `g/llm-architecture/`, `g/llm-top10/`, `g/supply-chain/`, `g/ai-governance/` + rebuilt `g/index.html`. Sitemap: 119 → 123 URLs (`lastmod 2026-10-09`). Cross-links wired via LINKMAP. Marker check: 4/4 new pages + `/g/` + `/sitemap.xml` — ALL PASS on recheck (`runs/site-integration.log`; first attempt showed 000s — slow test-server bind, corrected and noted; orphan killed, zero http.servers remain). Price scan clean. `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held, HEAD still 17f437a.

## Stage E CISSP-domain wave — 2026-10-09 (integrated)

Dino's order: keep building. Four Stage E lessons written to the full 10-part spec, original prose, no prices/fees/salaries anywhere:

- `lessons/e-iam.md` (2,711 words) — Identity and access management: identification/authentication/authorization order, joiner-mover-leaver lifecycle, assurance levels, federation, RBAC/ABAC/DAC/MAC, privileged access. Worked case: Meridian Analytics lifecycle design + quarterly access review (6 findings, each with decision/owner/date). Walkthrough: no CLI by design — authoring + self-review logged (`runs/e-iam.log`).
- `lessons/e-crypto-applied.md` (2,133 words) — Applied cryptography: hash/symmetric/asymmetric guarantees, ECB-vs-CBC modes, PKI path validation, SP 800-57 key lifecycle, TLS 1.3 as the composed system. Walkthrough: all 6 steps ran (`runs/e-crypto-applied.log`) — SHA-256 avalanche, AES-256-CBC roundtrip + wrong-password failure, ECB/CBC block-leak demo (4 identical blocks → 4 identical ECB blocks, observed via `od`; `xxd` absent, logged), RSA sign/verify + tamper failure, self-signed cert inspection, local TLS 1.3 handshake (`TLS_AES_256_GCM_SHA384`). pgrep self-match false positive logged, not smoothed.
- `lessons/e-sdlc.md` (2,340 words) — Secure SDLC: threat modeling (STRIDE), gates per phase, SSDF v1.1 practice groups, effectiveness vs activity metrics. Worked case: Northwind Traders threat model (4 findings) + verification-gate review (SAST SQLi → release-blocking → root-cause process fix). Walkthrough: no CLI by design (`runs/e-sdlc.log`).
- `lessons/e-bcp-drp.md` (2,564 words) — BCP/DR: BIA with RTO/RPO as decisions, continuity vs recovery, strategy selection, DR plan excerpt, tabletop exercise. Worked case: Beacon Logistics BIA (3 processes) + warm-standby strategy + plan excerpt (named authority/roles) + 90-min tabletop (3 injects, 3 findings). SP 800-34 Rev. 1's 2010 age noted honestly in-lesson. Walkthrough: no CLI by design (`runs/e-bcp-drp.log`).

CISSP map refs served: 5.1–5.5 (e-iam), 3.6 (e-crypto-applied), 8.1–8.5 governance level (e-sdlc), 1.7/7.10/7.11/7.12/7.13 (e-bcp-drp). Objectives referenced by number with paraphrase only; no exam questions or outline text reproduced.

Sources: 4 new `verified` ledger rows (RFC 5280; SP 800-57 Pt.1 Rev.5; SP 800-218 SSDF v1.1; SP 800-34 Rev.1 — all fetched 2026-10-09) + 8 `operator-added` (SP 800-63, NISTIR 7316, 3 OWASP cheat sheets, OWASP SAMM, FIDO Alliance, CISA BC resources).

Also resolved this session: b-sqli/b-command-injection A03→A05 correction verified live in lessons + built pages; map.md rows 13–14 corrected; gaps.md entry marked resolved.

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended (4 LESSONS rows; index now lists 24 lessons; reading order extended incident-response → iam → crypto-applied → sdlc → bcp-drp; lede 20→24). Pages: `g/iam/`, `g/crypto-applied/`, `g/sdlc/`, `g/bcp-drp/` + rebuilt `g/index.html`. Sitemap: 115 → 119 URLs (`lastmod 2026-10-09`). Cross-links wired via LINKMAP (backticked lesson ids resolve). Marker check: 4/4 new pages + `/g/` + `/sitemap.xml` — ALL PASS (`runs/site-integration.log`; one false FAIL from a case-sensitive marker, corrected on recheck; pgrep self-match false positives logged, not smoothed). `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held. Hygiene: marker-check http.servers killed in the same command that started them; verified zero remain (port closed).

## Done

- Working folder created at `~/workspace/security-curriculum/security-guidebook/`: `lessons/`, `runs/`, `reports/`, plus this file, `map.md`, `sources.csv`, `gaps.md`.
- All 4 Phase 2 pilot lessons written to the full 10-part spec (brief §6), original prose, no prices/fees/salaries/time estimates anywhere:
  - `lessons/a-http-depth.md` — HTTP in depth (Stage A, level 3)
  - `lessons/b-idor.md` — IDOR (Stage B, level 3)
  - `lessons/e-risk-assessment.md` — Risk assessment as a worked case, serves CISSP 1.9 (Stage E, level 3)
  - `lessons/ai-prompt-injection.md` — Prompt injection, serves the CAISP map (AI track, level 3)
- Walkthroughs executed in a clean local environment (stock Python 3.12, curl 8.5.0, loopback only); transcripts saved:
  - `runs/a-http-depth.log` — all 10 steps ran (HTTP server, JWT dissection, TLS 1.3 handshake, layering proof)
  - `runs/b-idor.log` — all 8 steps ran (vulnerable → finding reproduced → fix → 3 verification cases)
  - `runs/e-risk-assessment.log` — worked case authored/reviewed (no CLI by design)
  - `runs/ai-prompt-injection.log` — steps 1–4 ran (deterministic harness); step 5 (live model) marked **not run by us**
- Primary sources fetched in-session and ledgered in `sources.csv` (7 URLs, all verified 2026-10-09).
- Brief discrepancy found and handled: brief-2 names OWASP LLM01:2025; verification proved the **2026 edition** (released 2026-08-04, renumbered codes) is current. The AI lesson teaches the 2026 edition, names edition+date on every citation, and the discrepancy is logged in `gaps.md`.

## Stage A foundation batch — 2026-10-09

Dino's order: keep building. Four Stage A lessons written to the full 10-part spec, original prose, no prices/fees/salaries anywhere:

- `lessons/a-dns-depth.md` (2,409 words) — DNS: resolution chain, message format, record types, TTL/caching, DNSSEC concept. Walkthrough: all 9 steps ran (`runs/a-dns-depth.log`) — toy authoritative server + stdlib DNS client on 127.0.0.1:53535, TCP form (sandbox blocks UDP; lesson says so). Step 9 (DNSSEC chain) marked **not run by us**.
- `lessons/a-tcpip-ports.md` (2,146 words) — handshake/teardown, `ss` states, what a port is, privileged ports, NAT. Walkthrough: 6 of 8 steps ran (`runs/a-tcpip-ports.log`) — ESTABLISHED/LISTEN/EADDRINUSE/PermissionDenied-as-nobody/TIME-WAIT all observed. UDP datagrams + packet capture marked **not run by us**.
- `lessons/a-linux-cli.md` (2,285 words) — files, permissions bitmask, users/setuid, processes/signals, logs, pipes, SSH keys. Walkthrough: all 7 steps ran (`runs/a-linux-cli.log`); shell ran as root — flagged in-lesson at every affected step; no sshd on the machine (noted).
- `lessons/a-git-github.md` (2,071 words) — snapshots vs diffs, staging, branching/merging, remotes, undo ladder, secrets rule. Walkthrough: 6 of 7 steps ran (`runs/a-git-github.log`) — local bare repo as the remote; GitHub fork/PR steps marked **not run by us** (no auth here).

Sources: 9 new `verified` ledger rows (RFC 1035, RFC 9293, OpenSSH manual, git-scm docs, Pro Git book, Bandit, Linux Journey, Practical Networking, Cloudflare DNS guide — all fetched 2026-10-09) + 4 `operator-added` (RFC 1034/791/8200/4033-4035 leads, local man pages).

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended (4 LESSONS rows; LINKMAP auto-extends; index page now lists 8 lessons with the A→B reading order; "keep going" note updated). Pages: `g/dns-depth/`, `g/tcpip-ports/`, `g/linux-cli/`, `g/git-github/` + rebuilt `g/index.html`. Sitemap: 4 new URLs (`lastmod 2026-10-09`). Cross-links wired dns → tcpip → linux-cli → git-github → http-depth → idor. Marker check: 8/8 URLs 200, all markers — ALL PASS (`runs/site-integration.log`). `git status`: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held.

## Stage B web-vulnerability wave — 2026-10-09

Dino's order: keep building. Four Stage B lessons written to the full 10-part spec, original prose, no prices/fees/salaries anywhere:

- `lessons/b-sqli.md` (2,368 words) — SQL injection: code-vs-data, three families (in-band/boolean-blind/time-blind), UNION technique, parameterized queries. Walkthrough: all 9 steps ran (`runs/b-sqli.log`) — quote probe → 500, boolean pair difference, ORDER BY column count, UNION cross-table read, time-blind via labeled `sleeps()` SQL function (4.0s vs instant), fix + 4 verification cases, defender log read.
- `lessons/b-command-injection.md` (2,078 words) — OS command injection: metacharacter classes, blind time-delay channel, allow-list > blocklist, no-shell APIs. Walkthrough: all 7 steps ran (`runs/b-command-injection.log`) — `; echo PROBE-XYZ` in-band, `&& whoami` read-only impact, `sleep 5` blind channel (5.0s), fix + 4 verification cases, spawn-log defender view.
- `lessons/b-ssrf.md` (2,182 words) — SSRF: server-fetches-attacker-URL, loopback trust, cloud metadata angle, denylist-bypass checkpoints, allow-list + canonicalized validation + egress controls. Walkthrough: 7 steps ran (`runs/b-ssrf.log`) — loopback admin fetched, metadata simulation role-name read, denylist bypass demonstrated at validator layer (urllib normalizes alternates; lesson says so), fix + 4 verification cases, fetch-log defender view.
- `lessons/b-csrf.md` (2,399 words) — CSRF: three preconditions, synchronizer tokens (gen/bind/verify), SameSite semantics, no-state-changing-GET. Walkthrough: 8 steps ran (`runs/b-csrf.log`) — server-side forged-shape proof, attacker's page (browser-click sub-step **not run by us**, request shape verified), GET variant, fix + 4 verification cases (403/403/403/200), SameSite=Lax observed, security-log defender view.

Sources: 6 new `verified` ledger rows (4 PortSwigger topic pages + 2 OWASP cheat sheets, all fetched 2026-10-09) + 10 `operator-added` (CWE-89/78/918/352, DVWA, Juice Shop, 2 cheat sheets, MDN SameSite, RFC 6265 §4.1.2.7).

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended (4 LESSONS rows; LINKMAP auto-extends; index now lists 12 lessons; reading order extended idor → sqli → command-injection → ssrf → csrf; "keep going" note 8→12). Pages: `g/sqli/`, `g/command-injection/`, `g/ssrf/`, `g/csrf/` + rebuilt `g/index.html`. Sitemap: 103 → 107 URLs (`lastmod 2026-10-09`). Cross-links wired (sqli→command-injection→ssrf→csrf chain). Marker check: 6/6 pages 200, all markers — ALL PASS (`runs/site-integration.log`). `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held.

## Stage B web-vulnerability wave, continued — 2026-10-09

Dino's order: keep building. Four more Stage B lessons written to the full 10-part spec, original prose, no prices/fees/salaries anywhere:

- `lessons/b-xss.md` (2,163 words) — Cross-site scripting: reflected/stored/DOM, trust-boundary mechanism, context-aware output encoding, CSP as defense in depth. Walkthrough: all 10 steps ran (`runs/b-xss.log`) — reflection/storage/DOM-sink proven by curl against a local demo; browser-*execution* sub-steps marked **not run by us** (no headless browser); fixed build verified (encoding + CSP header `default-src 'self'`).
- `lessons/b-business-logic.md` (2,107 words) — Business-logic flaws: the five-step methodology (state-machine map → step analysis → trust-boundary review → numeric fuzzing → race check). Walkthrough: all 8 steps ran (`runs/b-business-logic.log`) — price tamper (12.00→0.01), single-use coupon double-payout via check-then-act race (two interleaved sessions, both 15.00), negative quantity (total=-3.00); fixed build (server-side prices, atomic coupon consume, qty≥1) + order-log anomaly detection.
- `lessons/b-session-auth.md` (2,277 words) — Broken authentication and session management: token predictability, session fixation, missing rate limits, MFA as structural fix. Walkthrough: all 9 steps ran (`runs/b-session-auth.log`) — sequential sids, fixation chain proven end to end (planted id survives login AND reuses into the victim's dashboard), 20× 401 with no brakes; fixed build (32-hex rotated sids, 429 + Retry-After after 5 attempts, `HttpOnly; SameSite=Lax` cookies). MFA enrollment marked **not run by us** (reader-side, own accounts).
- `lessons/b-security-headers.md` (2,162 words) — Security headers: CSP, HSTS, frame-ancestors, nosniff, Referrer-Policy, cookie flags — what each buys and where each fails, verified header-by-header with curl. Walkthrough: all 9 steps ran (`runs/b-security-headers.log`) — bare vs secured header sets, CSP+encoding double layer, clickjacking header, MIME-sniffing contrast, HSTS over self-signed TLS (verified *sent*; enforcement is browser behavior), cookie flags on HTTP and HTTPS, plus a committable audit script. Browser-*rendering* sub-steps marked **not run by us**.

Walkthrough corrections applied honestly in the logs (not smoothed over): the coupon demo's sequential replay was correctly rejected, so step 4 was re-run as the interleaved race it was meant to be; the auth demo's first fixation pass used a planted id unknown server-side, so the demo was corrected to honor client-supplied ids (the classic model) and the chain re-proven; `curl -I` vs GET for the CSP header noted. Cleanup: every demo server killed by PID and verified gone (one `kill $SRV` raced a background start; killed by explicit PID after — noted in logs).

Sources: 5 new `verified` ledger rows (PortSwigger XSS page, PortSwigger Authentication page, OWASP Secure Headers Project, MDN CSP guide, OWASP Top 10:2025 category list — all fetched 2026-10-09) + 5 `operator-added` (PortSwigger logic-flaws page from night research; OWASP XSS/Auth cheat-sheet slugs unverified; RFC 6797 HSTS; CWE-79/840/287/384/693).

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended (4 LESSONS rows; LINKMAP auto-extends; index now lists 16 lessons; reading order extended csrf → xss → business-logic → session-auth → security-headers; lede 12→16). Pages: `g/xss/`, `g/business-logic/`, `g/session-auth/`, `g/security-headers/` + rebuilt `g/index.html`. Sitemap: 107 → 111 URLs (`lastmod 2026-10-09`). Cross-links wired via LINKMAP (backticked lesson ids). Marker check: 6/6 pages 200, all markers — ALL PASS (`runs/site-integration.log`). `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held.

## Stage C detection/operations wave — 2026-10-09

Dino's order: keep building. Four Stage C defender lessons written to the full 10-part spec, original prose, no prices/fees/salaries anywhere:

- `lessons/c-soc-triage.md` (2,117 words) — SOC triage: the eight-stage alert-to-decision pipeline, impossible-travel and beaconing decision trees, five classification buckets, severity vs priority, escalation criteria. Walkthrough: all 8 steps ran (`runs/c-soc-triage.log`) — labeled fictional event set; j.chen Chicago→Lagos ESCALATEd, m.okafor VPN-exit closed benign, svc-backup non-interactive closed, WS-4417 beaconing (CV 0.03) escalated, WS-4420 updater closed.
- `lessons/c-log-sources.md` (2,098 words) — Log sources: Windows event IDs, Sysmon IDs, EDR, network five (firewall/proxy/DNS/IDS/flow), identity, email, cloud audit — records/answers/blind-without for each. Walkthrough: all 8 steps ran (`runs/c-log-sources.log`) — fictional 62-event sample parsed with awk/grep/sort: 18×4625 spray from one IP → t.nguyen 4624 payoff, DGA-shaped DNS burst, beacon-shaped firewall flows, 1102 anti-forensics; blind-spot column names proxy/EDR/email gaps.
- `lessons/c-sigma-detection.md` (2,090 words) — Sigma: rule anatomy field-by-field against the spec, modifiers, the tuning loop (filters→thresholds→narrowing), detection-as-code CI, honest ATT&CK coverage semantics (procedure ≠ technique). Walkthrough: all 8 steps ran (`runs/c-sigma-detection.log`) — rule YAML schema-validated, evaluated against labeled corpora (2 TP, 1 FP on benign updater), tuned filter → FP 1→0 with TP unchanged; first filter attempt missed and was corrected honestly in the transcript; no SIEM backend conversion (teaching harness, lesson says so).
- `lessons/c-incident-response.md` (2,354 words) — IR basics on the NIST SP 800-61 Rev. 3 spine (final April 2025, CSF 2.0 Community Profile — fetched in-session; old Rev. 2 summaries flagged stale): preparation through post-incident, evidence-before-action, the full fictional WS-4417 IR report (timeline, scope, ordered containment, honest limitations, traceable recommendations). Walkthrough: no CLI by design — worked-case authoring + self-review checklist logged (`runs/c-incident-response.log`).

Sources: 3 new `verified` ledger rows fetched in-session (SigmaHQ/sigma-specification; NIST SP 800-61 Rev. 3; MITRE ATT&CK Enterprise tactics — 15 tactics, Stealth + Defense Impairment split confirmed) + 9 `operator-added` (SigmaHQ/sigma repo, SP 800-92, sysmon-config, Wazuh, Security Onion, Velociraptor, Atomic Red Team, ATT&CK Navigator, CERT CVD guide).

Integration (working tree only — NOT committed, NOT pushed): `build_site.py` extended (4 LESSONS rows; index now lists 20 lessons; reading order extended security-headers → soc-triage → log-sources → sigma-detection → incident-response; lede 16→20). Pages: `g/soc-triage/`, `g/log-sources/`, `g/sigma-detection/`, `g/incident-response/` + rebuilt `g/index.html`. Sitemap: 111 → 115 URLs (`lastmod 2026-10-09`). Cross-links wired via LINKMAP. Marker check: 4/4 new pages 200 (incident-response 4/5 markers — "not run by us" legitimately absent: no unrun steps in a worked-case lesson), `/g/` and `/sitemap.xml` pass — appended to `runs/site-integration.log`. `git status` in repo: `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held. Hygiene: killed two leftover http.server test processes from earlier batches' marker checks + this batch's own; verified zero remain.

## Next

1. **STOP 1 per brief §8** (pilot report) was delivered; Dino ordered continued building — this batch is the first Phase 3 output.
2. Phase 3: lesson batches (Stage A remainder, Stage B vuln wave, Stage C, Stage D tracks, Stage E objectives, AI track remainder) — one fresh session per batch per the run plan.
3. Re-verify open gaps at build time (see `gaps.md`): PortSwigger slugs, RFC 8446/6749, ATLAS AML.T0051 page, NIST AI 600-1, SP 800-39.
4. Run the Docker-based walkthroughs (DVWA/Juice Shop/crAPI/DVGA) on a machine with Docker, or mark permanently substituted.

## Decisions needed (from Dino)

1. **Integration is built (working tree only).** The 4 pilot lessons are now real site pages under `/g/` in the repo working tree (see "Site integration" below) — nothing committed, nothing pushed, per the standing rule. Say the word for a commit, and separately for any push/deploy.
2. **Brief correction:** confirm the guidebook should keep teaching OWASP LLM Top 10 **2026** (not the brief's 2025 reference) going forward, and whether brief-2 §5 should be amended. The prompt-injection page carries a visible edition note flagging this.
3. **Walkthrough substitution policy:** no Docker on this machine — confirm the local-demo-app substitution (clearly labeled in-lesson) is acceptable for pilot, with Docker-based verification deferred to a machine that has it.

## Site integration — 2026-10-09 (pilot lessons → real site pages)

### Phase 0 — repo orientation (read-only)
- Site repo: `~/workspace/learncomputerstuff/` = `dynoshippedit/ai-career-kg` @ 17f437a, cloned 2026-10-09 (public, no auth for read).
- Architecture: **static HTML, pages committed**. No server-side generator in the repo. `data/catalog.json` (889 rows) is the source of truth for the directory/roles/credentials pages; `builder/index.html` is a *client-side* page tool (the old stack builder is retired — the page is now a "moved" notice). Pages are authored as full `index.html` files sharing one inline CSS block (design tokens: paper/claret, wayfinding voice for nav, ledger voice for facts).
- URL scheme: single-letter section dirs — `/c/` credentials, `/f/` career families, `/r/` roles, `/x/` directory explorer, plus `/method/`, `/path/`, `/start/`, `/builder/`. Sitemap lists every page, all `lastmod 2026-07-28`.
- Template studied: `r/ai-security-engineer/index.html` (head: title/description/canonical/og/JSON-LD BreadcrumbList; body: skip link, header.site brand+nav, crumbs, main, footer.site 3-col).

### What was built (working tree only — NOT committed, NOT pushed)
- **URL scheme: `/g/<slug>/`** ("g" = guide — fits the single-letter section convention; no collision). Slugs drop the stage prefix: `a-http-depth`→`http-depth`, `b-idor`→`idor`, `e-risk-assessment`→`risk-assessment`, `ai-prompt-injection`→`prompt-injection`. Plus `/g/` index as the guidebook entry page.
- **Builder script:** `build_site.py` (this folder) — converts `lessons/*.md` → `<repo>/g/<slug>/index.html` + `<repo>/g/index.html`. Extracts the site's CSS verbatim from the homepage so tokens never drift. Handles the constructs lessons use: `##`/`###`, fenced code→`<pre>`, `>`→`.note` div, `-`/`1.` lists, inline code/bold/italic, bare-domain linkification, cross-links any backticked lesson id in LINKMAP (map.md dependency graph). Re-run for future batches.
- **Pages:** `g/http-depth/`, `g/idor/`, `g/risk-assessment/`, `g/prompt-injection/`, `g/` — each with canonical URL, og tags, JSON-LD breadcrumbs, all 10 lesson sections, a `.ledger` meta table (stage/level/prereqs/map refs), per-page dateline (walkthrough run date), preserved "not run by us" / edition-note honesty.
- **Wiring:** homepage gained one section ("Learn it, don't just browse it" with a door to `/g/`) between "Pick a direction" and "Browse everything" — matches existing patterns, no redesign. `sitemap.xml` gained the 5 `/g/` URLs (`lastmod 2026-10-09`).
- **Verification:** served locally (`python3 -m http.server`), 7/7 URLs returned 200 with all content markers — log: `runs/site-integration.log` (ALL PASS). Price scan clean. No headless browser on this machine — no screenshot taken.
- **git status:** `M index.html`, `M sitemap.xml`, `?? g/` — standing rule held.

### Integration pattern (future batches — mechanical)
1. Write lesson to the 10-part spec in `lessons/<id>.md`; run walkthrough, save `runs/<id>.log`.
2. Add one row to `build_site.py` LESSONS (id, slug, stage label, dateline note, meta description); add id→URL to LINKMAP.
3. Run `build_site.py` → pages land in `<repo>/g/<slug>/`.
4. New entry points (stage/role pages) go in the script's `build_index()` doors; cross-links resolve via LINKMAP automatically.
5. Add new URLs to `sitemap.xml` (`lastmod` = build date); re-run the http.server marker check; extend the marker list.

## Final structural batch — role paths + knowledge maps (2026-10-09)

**The brief's four page types are now complete: lessons (53), stage pages (5), role paths (8), knowledge maps (2).**

### What was built (working tree only — NOT committed, NOT pushed)
- `build_site.py` extended: `PATHS` table (8 roles: ordered lesson groups with stage labels, 3–4 checkpoints each, one level-4 capstone naming the public artifact) + `build_paths()` → `/g/path/<role>/`; `build_path_index()` → `/g/paths/`; `CISSP_DOMAINS` (62 objectives 1.1–8.5, guidebook's own paraphrases, lesson ids or gap) + `CAISP_CHAPTERS` (7 chapters) + `build_maps()` → `/g/map-cissp/`, `/g/map-caisp/`. `build_index()` gained Role paths + Knowledge maps sections.
- 11 new pages, all verified 200 with content markers (log: runs/site-integration.log — ALL PASS). Test http.server killed by explicit PID; pgrep confirms zero remain.
- CISSP map: **17 of 62 objectives have a lesson** (plain count, computed from data): 1.7, 1.9 (e-bcp-drp, e-risk-assessment); 3.6 (e-crypto-applied); 5.1–5.5 (e-iam); 7.10–7.13 (e-bcp-drp); 8.1–8.5 (e-sdlc + d-appsec). The other 45 are rendered as "No lesson yet — logged as a gap." Issuer's rule stated once (5 years in ≥2 domains, one year waivable, else Associate of ISC2). AI treated as woven context, not separate objectives, per the night-research determination.
- CAISP map: **7 of 7 chapters have a lesson**. One line keeps CAISP separate from CertNexus CAIP (never merged). Edition note carries the open 2026-vs-2025 decision.
- Existing-page edits (the ONLY edits to existing pages, per brief §8 Phase 4): one `<li>` added to "Where this route continues" in each of the 8 `/r/<role>/` pages, linking to its `/g/path/<role>/` page. Diff stays visible in the working tree for Dino's review. `git status`: `M index.html`, `M sitemap.xml`, `M r/<8>/index.html`, `?? g/`.

### Decisions made
- Path sequences corrected against the live role pages per brief §5: dfir routes THROUGH the completed SOC-analyst path first (role page: "essentially always entered from a SOC or security analyst role"); cloud-security gets a "cloud fluency first" block (role page: cloud/DevOps first) — marked as a lesson gap since no cloud-services lesson exists; appsec front-loads code fluency (role page: "read and write code well before the security layer means anything").
- e-crypto-applied's claim that objective 3.7 "is taught in the Stage A cryptography lesson" is false — no such lesson exists; 3.7 counted as a gap and the conflict logged in gaps.md.
- OWASP LLM Top 10 release-date conflict inside our own files: pilot handoff says 2026-09-30, ai-llm-top10.md says 2026-08-04. Map page says "2026 edition" with no date; conflict logged in gaps.md.
- Brief's candidate-role list corrected: `/r/ai-security-engineer/` EXISTS on the site (two role pages link it as a continuation). Candidate roles logged in gaps.md: red team operator, exploit developer, malware analyst, security program lead.

### Carried open decisions (not resolved)
1. OWASP LLM Top 10 2026-vs-2025 edition question.
2. Walkthrough substitution policy (local-demo / not-run steps vs Docker/model machine).

## 2026-10-09 — Gap-closing sprint, web-verification track (subagent)

**Ledger:** 214 rows → **208 verified**, 2 unreachable (Hacktivity script-rendered; MS Learn registry module retired), 4 operator-added (2× MITRE ATLAS cookie-walled — needs live browser; CIS Benchmarks 403 Cloudflare; man-pages row has no URL by definition). Started the sprint at 97 verified / 99 operator-added per the task brief; row count grew as cited-but-unrowed sources got verified rows.

**Critical fix:** RFC 6265 has no §4.1.2.7 — SameSite is draft-ietf-httpbis-rfc6265bis §5.6.7 (138,768-char draft fetched, HTTP 200). Corrected in `lessons/b-csrf.md` + rebuilt `/g/csrf/index.html`.

**LLM Top 10 2026 date — resolved:** 2026-08-04 is canonical (official GenAI repo README: "Current release: 2026 — published August 4, 2026"; corroborated by OWASP legacy repo + 2 derivatives). The 2026-09-30 was already purged from lessons/pages; no fix needed.

**Verified this session (selection):** 7 RFCs; 7 PortSwigger topics; 8 OWASP cheat sheets (real slugs from repo file list); 11 CWEs; Anthropic CVP announcement at its real URL (anthropic.com/news/cyber-verification-program, tier details from Anthropic's own page); 4 bounty-platform docs; NIST AI 600-1 PDF (12 risk categories confirmed) + SP 800-39 PDF; OWASP LLM Appendix B (diagram PNG); 5 DFIR + 6 exploit leads; CAPEC catalog + CAPEC-1; CISA KEV at the hyphenated URL (unhyphenated 404s); OWASP Agentic Top 10 page (was 403, now loads); AICPA TSC primary page; SANS SEC598 + SEC535 (both full syllabus text); ~60 bulk rows (ATT&CK, SAMM, SLSA, ASVS, WSTG, CISSP outline, Kettle HTTP/2 research at portswigger.net/research/http2, etc.).

**Corrections still needed in lesson files:** (1) CISA KEV unhyphenated URL → hyphenated; (2) Kettle HTTP/2 bare portswigger.net → /research/http2; (3) MS Learn registry module → registry-hives docs. None applied — flagged for the parent.

**CSV hygiene:** file rewritten with proper quoting mid-sprint (backup sources.csv.bak-20261009); schema intact.

**Open decisions carried:** (1) OWASP LLM Top 10 2026-vs-2025 edition question (brief still says 2025); (2) walkthrough substitution policy. **Standing rule held:** nothing committed or pushed; site rebuilt in working tree only.

## ai-sec-automation — 2026-10-10 (written, unintegrated)

Dino's order: whole permissions, keep going. One AI-track lesson written to the full 10-part spec, original prose, zero currency symbols.

- `lessons/ai-sec-automation.md` (2,498 words, exactly 10 `##` sections) — SEC598 subject areas (automation for offense, defense, and cloud: LLM-assisted detection engineering, SOAR playbooks, agentic investigation assistants, red-team AI agents + continuous emulation, cloud IaC) and SEC535 subject areas (AI-enabled attack techniques: recon at scale, AI-crafted phishing + deepfakes, AI-assisted web exploitation, patch diffing, AI-assisted malware/evasion + agentic malware) taught as concepts. Every attack concept paired with its defense and defender-detectable telemetry; the compression principle (AI compresses speed/scale/iteration, not steps) as the through-line. "Paid" line in §7 once, teach-from-free-material only. ≤3 free resources (MITRE ATLAS, SigmaHQ sigma, CISA MFA). Walkthrough: worked detection plan for AI-assisted phishing → credential theft → automated lateral movement as the defensive work product — defender logs, firing detections, responses with human-in-the-loop gates, illustrative manual-vs-automated dwell column. Validation script (Python 3.12.3) rendered the plan as data and asserted every step names logs + detection + response and every attack concept carries defense + telemetry — all checks passed. Transcript + self-review in `runs/ai-sec-automation.log`. Level 2 stated honestly in the ID line; what finishes the job (paid courses + authorized-lab work) named.

Sources: 3 new `verified` ledger rows (SEC598 + SEC535 pages re-fetched in-session 2026-10-10 — GASAE/GOAA pairings confirmed from the pages' own "prepares you for" statements; CISA Require MFA re-verified 2026-10-10). GIAC pages not cited (guessed giac.org URL 404'd; sibling ledger rows 318–319 carry the GIAC objective statements). ATLAS still cookie-walled (pre-existing gap).

NOT integrated: build_site.py untouched, no build run, no commit, no push — integration is a separate agent's job per the task. Deliverables: lesson file, run log, 3 sources.csv rows. LESSONS-tuple fields for the integrator: lid=`ai-sec-automation`, slug=`ai-sec-automation`, stage=AI track, Level 2, description "AI security automation as concepts: the SEC598 and SEC535 subject areas with every attack technique paired to its defense and defender telemetry, and a detection plan for an AI-automated attack chain."

## Brief-compliance integration — 2026-10-10 (integrator)

**ai-sec-automation integrated:** Lesson picked up by the frontmatter-driven builder (106 lessons in registry); page built at /g/sec-automation/ (slug `sec-automation`, lesson_id `ai-sec-automation`). GASAE map links resolve. Note: Child A's STATE entry named slug `ai-sec-automation` but the file's frontmatter says `sec-automation` — page builds and links work; slug choice is editorial.

**CISSP AI notes integrated:** `CISSP_AI_NOTES` dict added to build_site.py; all 8 domains now carry an AI-note line linking AI-track lessons. Verdict (from ISC2's "Exam Guidance for Artificial Intelligence," Sept 1, 2026): exam content, not commentary. The "AI in the outline" header note updated to cite the document.

**Four light maps built:** LIGHT_MAPS data + build code in build_site.py; pages at /g/map-aigp/ (4/4), /g/map-gasae/ (10/10), /g/map-goaa/ (7/10, 3 honest gaps), /g/map-aaism/ (3/3). Four doors added to g/index.html Knowledge maps grid. Sitemap: 4 URLs added (223 total, valid XML).

**Verification:** All 6 map/lesson pages have exactly one h1; 214 internal links checked, 0 broken. Build runs clean.

**sources.csv:** 315 rows, 311 verified. Repaired a malformed row (Child B's Exam Guidance row had unquoted commas shifting columns); re-added 2 GIAC rows lost in the repair from the handoff data. One pre-existing exception: man-pages row (local, operator-added).

**Directory:** 35 rows added to data/catalog.json (889 → 924) — done in a prior unit, schema unchanged.

**Not committed, not pushed** (parent's lane).
