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
