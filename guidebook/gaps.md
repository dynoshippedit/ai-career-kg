# gaps.md — Phase 2 pilot

Everything below is unverified, unrun, or substituted, with what was tried. Nothing smoothed over.

## Brief §5 required-but-unwritten lessons — WRITTEN this session (2026-10-10)

- **8 lessons written, all walkthroughs run for real on loopback:** `a-crypto` (A, L2; OpenSSL 3.0.13 — avalanche, AES roundtrip, ECB/CBC block leak, RSA sign/verify + tamper fail, self-signed cert inspect, MD5 demo), `b-api-abuse` (BOLA, over-exposure, mass assignment, throttles; stdlib demo :8331/:8332), `b-ssti` (toy eval-engine :8333), `b-xxe` (xml.etree :8334/:8335 — taught honestly: expands internal entities, refuses external), `b-deserialization` (pickle :8336/:8337 — marker file proved code ran inside `pickle.loads`), `b-graphql` (real graphql-core 3.3.0 engine :8338/:8339 — introspection dump, ssn field gap, depth-6 → 17KB), `b-race-conditions` (two-thread coupon race :8340/:8341 — `uses_left` went to -1), `b-jwt-oauth` (hand-built tokens :8342/:8343 — alg=none, expired claims, real RS256→HS256 key confusion with OpenSSL RSA key, redirect_uri prefix bypass). Transcripts: `runs/<id>.log`. Every lesson: 10 sections, ≤3 free resources, Level 3 (a-crypto Level 2, names e-crypto-applied as finisher), §9 CAN/CANNOT claims, voice rules clean.
- **Honesty notes baked into the lessons:** the b-ssti first attempt failed (injected into variable not template source) — logged; b-jwt-oauth's first expired-token attempt 401'd (signed with wrong key) — corrected in the transcript; no step marked "not run by us" in any of the 8.
- **Integration:** frontmatter on all 8; 7 Stage B in pentester "Practitioner, full" + appsec "Vulnerability classes" paths (roles cross-validated); a-crypto on Stage A page; 16 new `verified` sources.csv rows (334 total); pages render (8/8 HTTP 200, 10 h2 each, 1,720–2,232 words); sitemap regenerated.

## Gap-closing sprint (2026-10-10) — RESOLVED this session

Environment track: installed what the build machine can actually carry, re-ran the "not run by us" steps for real. Evidence in `runs/*.log` re-run entries; lesson markers updated; pages rebuilt.

- **nmap — RESOLVED.** Installed 7.94SVN (apt-get update hangs on this machine's mirrors, so .debs were fetched via curl from archive.ubuntu.com and installed with dpkg: nmap-common, liblinear4, liblua5.4-0, libpcap0.8t64, libssh2-1t64, libibverbs1, libnl-route-3-200, libnl-3-200). `nmap -sT -p 18499 127.0.0.1` → `18499/tcp open` against a local demo listener. `runs/b-toolbench.log`.
- **tcpdump — RESOLVED.** Installed 4.99.4 (same .deb route). `tcpdump -Z root -i lo -n 'tcp port 18445'` captured the full loopback exchange: SYN / SYN-ACK / ACK / data / FIN — 10 packets. (Container has no `tcpdump` user, hence `-Z root`.) `runs/a-tcpip-ports.log`. The a-tcpip-ports step 8 "not run by us" marker is closed; step 5 (UDP) stays unrun — sandbox still blocks UDP loopback.
- **dig — RESOLVED.** DiG 9.18.39 was already on the machine (dnsutils never needed). All DNS-lesson query steps re-ran with real dig `+tcp -p 53535 @127.0.0.1` against the toy authoritative server: A, CNAME, TXT, NS, NXDOMAIN. `runs/a-dns-depth.log`. Step 9 (DNSSEC chain) stays unrun — needs a validating resolver + signed zone.
- **Headless browser — RESOLVED.** Playwright + Chromium (headless shell 1243) installed; JS execution verified. Re-ran for real: b-xss steps 4 (reflected marker `EXEC-REFLECTED` fired) and 6 (DOM sink `EXEC-DOM` fired), plus the fixed build (no execution); b-csrf step 4 (attacker's auto-submit page changed the victim email `victim@example.com` → `attacker@evil.example` in a logged-in browser context); b-security-headers step 3 (CSP `default-src 'self'` blocked an unencoded inline handler — violation in the console) and step 4 (cross-origin frame refused per `frame-ancestors 'self'`). `runs/b-xss.log`, `runs/b-csrf.log`, `runs/b-security-headers.log`.
- **Semgrep engine — RESOLVED.** The earlier "dead shim" report is superseded: system pip refused (typing_extensions RECORD conflict with the Debian-shipped copy), but a clean venv install runs 1.180.0 fine — a local rule matched `subprocess.call(..., shell=True)` for real. `runs/b-toolbench.log`.
- **Docker — confirmed-unavailable** (`command -v docker` empty 2026-10-10; daemon install not attempted — out of scope). **Local AI model — confirmed-unavailable** (no ollama binary, no GPU, no weights; multi-GB download not attempted). **Windows — confirmed-unavailable** (no Windows on the build bench). **sshd — confirmed-unavailable** (no sshd binary; openssh-server has a long dep chain and was not pursued per scope).

Still not installed / not run by us: ffuf, subfinder/dnsx/httpx/amass, katana/gau/waybackurls, Burp Community/Caido/mitmproxy, Autorize/AuthMatrix, JWT Editor/jwt_tool, CodeQL, Trivy/Gitleaks, Flameshot/Dradis.

## Brief discrepancy (handled, needs Dino's confirmation)

- **Brief-2 §5 names OWASP LLM01:2025; the current edition is 2026.** Verified 2026-10-09 against the official OWASP GenAI Security Project repo (`2026/final/` lists LLM01–LLM10; edition released 2026-08-04; codes renumbered from 2025). The `ai-prompt-injection` lesson teaches the 2026 edition and names edition+date on every citation. **Decision needed:** confirm the guidebook keeps teaching 2026 going forward and whether brief-2 should be amended.

## Walkthrough substitutions and unrun steps

- **No Docker on this machine** (`docker` not installed). The DVWA / Juice Shop / WebGoat / crAPI / DVGA targets named in the research could not be run here. The `b-idor` walkthrough used a labeled local stdlib demo app instead (mechanism-identical; named in lesson and transcript). **Tried:** checked for docker binary — absent. **Next:** run the Docker-based targets on a machine with Docker, or confirm the substitution policy with Dino.
- **AI lesson step 5 (live red-team against a real model) — not run by us.** No Ollama, no model weights, no GPU workload on this machine. Steps 1–4 ran deterministically. The lesson gives the reader the exact procedure (Ollama + promptfoo/garak, own machine, own data). **Tried:** checked for ollama binary — absent; installing a model was out of scope for a pilot run. **Next:** run once on a machine with a local model before calling the AI track complete.
- **PortSwigger lab slugs:** `/web-security/access-control/idor` verified live this session. Other per-topic slugs (SQLi, auth, etc.) were pattern-confirmed in night research, not individually fetched — verify each at build time before linking.

## Cited but not fetched this session (operator-added rows in sources.csv)

These are named as primary leads in the lessons; each needs an in-session fetch at build time: RFC 8446 (TLS 1.3), RFC 6749 (OAuth 2.0), MITRE ATLAS AML.T0051 technique page (atlas.mitre.org was cookie-walled during research — use a live browser), NIST AI 600-1 Generative AI Profile, NIST SP 800-39. The lessons' "Read the source" guidance (read/skim/skip) is written; the ledger rows must be upgraded from `operator-added` to `verified` before publish.

## Carried from night-research error sweep (not re-tried this session)

- PTES Technical Guidelines URL returns HTTP 403 (two attempts) — retry from a live browser at build time.
- OWASP Agentic AI Top 10 page returned 403 — extension project, non-blocking for the pilot.
- SANS course pages (SEC598→GASAE, SEC535→GOAA) are script-rendered — verify from a live browser at build time.
- ISO 27001 certification lifecycle — paywalled; the guidebook covers it through free resources only.
- Trust Services Criteria edition — secondary-corroborated (2017 with 2022 revised points of focus); AICPA primary page not confirmed.
- ATT&CK v19.2 (2026-04-28) split Defense Evasion into Stealth + Defense Impairment (15 tactics) — any future lesson text using the 14-tactic list is stale; the pilot lessons do not reference ATT&CK tactics.
- CVE CNA count (555) and NVD enrichment policy — not referenced by the pilot lessons; relevant at Stage C build time.

## Blocked / pending decisions

- **Repo integration:** site repo now at `~/workspace/learncomputerstuff/` (cloned 2026-10-09, public, read-only). Generator/template integration and any commit/push await Dino's explicit say-so (standing rule).
- **Phase 3 batches** await Dino's STOP 1 go-ahead per brief §8.

## Stage A foundation batch gaps (2026-10-09)

Sandbox limits hit during this batch's walkthroughs (all marked "not run by us" in-lesson at the step):
- **UDP loopback blocked** (`PermissionError` on sendto). The DNS walkthrough used the TCP form of DNS (RFC 1035 §4.2) on 127.0.0.1:53535 — message format identical, transport differs; the lesson says so. The TCP lesson's UDP datagram step is not-run with the exact reader commands given.
- **No tcpdump/Wireshark** — the packet-capture step (tcpip-ports step 8) is not-run; reader exercise with the exact filter given.
- **No dig/host/nslookup** — the DNS lesson ships its own stdlib client (`dnsq.py`, in the transcript notes); arguably better pedagogy, but `dig` fluency is left to the reader.
- **No sshd** — `/etc/ssh/sshd_config` absent; the lesson's server-side hardening reads as a reader exercise.
- **No GitHub auth** (`gh` not logged in) — fork/PR steps not-run; exact reader procedure given.
- **Walkthrough ran as root** (container) — permission-denial demos adapted honestly: `chmod 000` cat still succeeding as root is flagged in-lesson; the privileged-port bind was demonstrated by dropping to `nobody` via setpriv.
- **DNSSEC chain verification not run** — needs a validating resolver + signed zone; reader exercise (`dig +dnssec`).
- Carried from pilot (still open): no Docker (DVWA/Juice Shop/crAPI/DVGA walkthroughs), no local AI model (prompt-injection step 5), PortSwigger per-topic slugs beyond `/idor` pattern-confirmed not fetched, RFC 8446/6749 + ATLAS AML.T0051 + NIST AI 600-1 + SP 800-39 cited-as-leads.

Judgment calls (logged, not smoothed):
- Prose-before-lab words: 957–1163 across the four lessons vs the brief's 1,200 sanity floor. "How it works" + "Walkthrough" are substantive in all four (worked examples, real transcripts); nothing padded to hit the number. Two genuine additions made during review (NAT in tcpip-ports; git history as investigation tool in git-github).
- Lesson order for this batch (dns → tcpip → linux-cli → git-github) follows the batch tasking; the CLI lesson notes it is the true foundation and is readable first.
- Cloudflare Learning Center is vendor content — used as a guided explainer, never as the primary source (RFCs hold that role); ledger says so.

## Stage B web-vuln wave (2026-10-09) — sqli, command-injection, ssrf, csrf

Walkthrough deviations (all labeled in-lesson at the step):
- **No Docker** (carried): DVWA SQL Injection / Command Injection / CSRF modules and Juice Shop injection challenges named as reader lab targets; walkthroughs used labeled local stdlib demo apps. CWE IDs (89/78/918/352) cited from the CWE database — marked `operator-added` (not fetched this session; verify at build).
- **OWASP cheat-sheet URLs beyond the two fetched**: Command Injection Defense and SSRF Prevention cheat sheets cited as bare domains in lessons; full URLs in ledger as `operator-added` — fetch at build before linking directly.
- **MDN SameSite page**: cited as a free resource in b-csrf; ledger row `operator-added` — fetch at build.
- **RFC 6265 §4.1.2.7** (SameSite): cited in b-csrf read-the-source; ledger `operator-added` (RFC 6265 was fetched in the pilot session for cookies — re-fetch the specific section at build).
- **b-csrf walkthrough step 4 (browser click)**: **RESOLVED 2026-10-10** — headless Chromium via Playwright; the attacker's auto-submit page was opened in a victim-logged-in browser context and the email changed for real. See the gap-closing sprint section above and `runs/b-csrf.log`.
- **b-ssrf walkthrough step 4 (denylist bypass)**: demonstrated at the validator layer in Python, not over the network — Python's urllib normalizes some alternate IP forms (decimal-octet, 127.1, hex); the transcript shows the string-check-vs-resolution gap explicitly and notes curl/Java/browsers follow the alternates. Real cloud metadata endpoints untouched (labeled loopback simulation).
- **b-sqli time-blind**: SQLite has no built-in delay function; the demo registers a labeled `sleeps()` SQL function — the channel (latency as signal) is identical; the lesson says so.
- PortSwigger per-topic lab slugs (`/sql-injection`, `/os-command-injection`, `/ssrf`, `/csrf`) — the four topic pages were fetched this session; individual lab slugs not enumerated — verify each at build time before deep-linking labs.

## Stage B web-vuln wave, continued (2026-10-09) — xss, business-logic, session-auth, security-headers

Walkthrough deviations (all labeled in-lesson at the step):
- **No Docker** (carried): PortSwigger XSS / business-logic / authentication labs and Juice Shop logic challenges named as reader lab targets; walkthroughs used labeled local stdlib demo apps on loopback.
- **b-xss steps 4/6 (browser execution)**: **RESOLVED 2026-10-10** — headless Chromium via Playwright; both markers (`EXEC-REFLECTED`, `EXEC-DOM`) fired for real, and the fixed build showed no execution. See the gap-closing sprint section above and `runs/b-xss.log`.
- **b-business-logic step 4 (coupon)**: the first transcript pass showed a sequential second-order replay correctly rejected ("already used") — the real flaw is the check-then-act race, re-run as two interleaved sessions (both got the discount). Lesson text describes the interleaved version; the addendum in `runs/b-business-logic.log` records the correction.
- **b-session-auth steps 4/6 (fixation + rate limit)**: the first demo build ignored planted sids unknown server-side (fixation didn't reproduce); demo corrected to the classic model (server honors client-supplied sid) and the full chain re-proven (planted id survives login AND accesses the victim's dashboard). Rate-limit first pass tripped early (successful logins counted toward the window); re-run on a fresh server: 5x 401 → 429 + `Retry-After: 60`. Both corrections logged in `runs/b-session-auth.log`.
- **b-session-auth step 7 (MFA enrollment)**: no real authenticator enrollment — **not run by us**; the lesson documents the enrollment contract and assigns it as the reader's own-accounts task.
- **b-security-headers steps 3/4 (browser enforcement)**: **RESOLVED 2026-10-10** — headless Chromium via Playwright; the CSP block (inline handler, violation in console) and the cross-origin frame refusal (`frame-ancestors 'self'`) were observed as real browser behavior. HSTS enforcement stays as-verified-sent (the honest boundary stands). See the gap-closing sprint section above and `runs/b-security-headers.log`.
- **OWASP cheat-sheet slugs (XSS Prevention, Authentication)**: both guessed URL forms 404'd — ledger rows `operator-added`; correct slugs must be confirmed at build time before linking.
- **RFC 6797 (HSTS)**: cited as primary lead, not fetched — ledger `operator-added`; fetch at build.
- **CWE IDs (79/840/287/384/693)**: from night research, not fetched this session — `operator-added`.
- **Fictional dollar figures in b-business-logic** ("$25 shirt", "$0.01", "total=-3.00"): these are the vulnerability's own worked-example amounts in a lesson about price tampering, not prices of real products/services/fees — reviewed and kept. No real-world prices, fees, or salaries appear anywhere in the batch.

## Correction applied (prior batch, resolved 2026-10-09)

- **b-sqli cited "OWASP Top 10:2025 A03" for Injection — RESOLVED.** Verified 2026-10-09 at owasp.org/Top10/2025/: A03:2025 is **Software Supply Chain Failures**; Injection is **A05:2025**. Fix applied: `lessons/b-sqli.md`, `lessons/b-command-injection.md`, map.md rows 13–14, and rebuilt pages `g/sqli/`, `g/command-injection/` all cite A05. No stale A03 references remain.

## Stage C detection/operations wave (2026-10-09) — soc-triage, log-sources, sigma-detection, incident-response

Walkthrough deviations and substitutions (all labeled in-lesson):
- **c-soc-triage**: event set is **fictional and labeled** (invented sign-ins/flows in triage_events.jsonl). No real SIEM on the build machine. Both decision trees (impossible-travel, beaconing CV) executed locally; all 5 cases classified as designed (j.chen ESCALATE / m.okafor VPN-exit close / svc-backup non-interactive close / WS-4417 beaconing ESCALATE / WS-4420 updater close).
- **c-log-sources**: logs are **fictional samples generated locally** (62 security events, 42 DNS queries, 37 firewall flows; seed 7, all values invented). No real Windows Event Logs, Sysmon, EDR, or proxy on this machine. Parsed with real CLI tools (awk/grep/sort); spray (18x4625 -> t.nguyen 4624), DGA burst, beacon flows, and 1102 all detected. Blind-spot column names what's missing (proxy, EDR, email gateway).
- **c-sigma-detection**: evaluator is a **teaching harness**, not a SIEM backend — applies the rule's selection logic directly; no Sigma CLI/pySigma conversion run here (lesson says so). Corpora are tiny (2 positive + 3 benign events) vs production hundreds — lesson states this as the honest limitation. First tuning-filter attempt missed (filter string absent from corpus); corpus corrected and re-run; correction logged in transcript, not smoothed.
- **c-incident-response**: no CLI by design (brief §6) — walkthrough is the worked-case authoring + self-review pass, logged in runs/c-incident-response.log. Scenario is **fictional and labeled**, built from the log-sources evidence pack. SP 800-61 Rev. 3 structure used (fetched in-session).
- **Verified in-session (new `verified` rows):** Sigma specification repo (SigmaHQ/sigma-specification, spec 2.x); NIST SP 800-61 Rev. 3 final (April 2025, CSF 2.0 Community Profile); MITRE ATT&CK Enterprise tactics page — **15 tactics**, TA0005 Stealth + TA0112 Defense Impairment split confirmed (v19.2). Lessons use the 15-tactic list; no 14-tactic references.
- **Operator-added (verify at build):** SigmaHQ/sigma repo, NIST SP 800-92 (DOI), SwiftOnSecurity sysmon-config, Wazuh, Security Onion, Velociraptor, Atomic Red Team, ATT&CK Navigator, CERT CVD guide.
- **Hygiene note:** two leftover `python3 -m http.server` test processes (ports 8471/8472) from earlier batches' marker checks were found still running this session and killed by PID, plus this batch's own server — verified zero remain afterward. Future batches: kill the marker-check server in the same command that starts it.
- Carried from prior batches (still open): no Docker; no local AI model; PortSwigger per-topic lab slugs need individual verification; the two Dino decisions (OWASP LLM 2026-vs-2025; walkthrough substitution policy). (b-sqli A03→A05 correction resolved 2026-10-09.)

## Stage E CISSP-domain wave (2026-10-09) — e-iam, e-crypto-applied, e-sdlc, e-bcp-drp

Walkthrough deviations and substitutions (all labeled in-lesson):
- **e-crypto-applied**: all 6 steps ran locally (OpenSSL 3.0.13, loopback only). Corrections logged in transcript, not smoothed: `xxd` absent on this machine — used `od -A d -t x1` for the ECB/CBC block dumps (same information); `pgrep -f "openssl s_server"` self-matched (PIDs 6168/6170 were the pgrep itself) — `ps` confirmed no s_server remained. Fixed key/IV used for the ECB/CBC determinism demo (labeled in transcript); wrong-password decrypt failure and tampered-signature failure both observed for real.
- **e-iam / e-sdlc / e-bcp-drp**: no CLI by design (brief §6) — worked-case authoring + self-review checklists logged in runs/e-iam.log, runs/e-sdlc.log, runs/e-bcp-drp.log. All scenario elements labeled fictional.
- **Operator-added (verify at build):** NIST SP 800-63, NISTIR 7316, OWASP Authentication/Cryptographic Storage/Threat Modeling cheat sheets, OWASP SAMM, FIDO Alliance, CISA BC resources. RFC 8446 (TLS 1.3) cited in e-crypto-applied §7 as a primary lead — needs in-session fetch at build time.
- **SP 800-34 Rev. 1 age noted in-lesson** (§6): May 2010, still the current revision; structure endures, technology assumptions dated — lesson says so explicitly.
- Carried from prior batches (still open): no Docker; no local AI model; PortSwigger per-topic lab slugs need individual verification; the two Dino decisions (OWASP LLM 2026-vs-2025; walkthrough substitution policy).

## AI security track wave (2026-10-09)

- **ai-supply-chain step 6 (live keyless signing) — not run by us.** Needs network + an OIDC identity (GitHub Actions or email) for Sigstore's public Rekor log; neither exists on this machine. The lesson gives the exact cosign procedure. The local hash/AIBOM/policy harness (steps 1–5) ran.
- **MITRE ATLAS still not fetched in-session.** atlas.mitre.org was cookie-walled during night research; not retried this session. ATLAS citations in `ai-llm-architecture`/`ai-llm-top10` are `operator-added` — verify from a live browser at build time.
- **NIST AI 600-1 PDF not fetched.** The GenAI Profile's twelve risk categories are described from the NIST overview page (verified) and night research, not from the PDF itself. The lesson tells the reader to read the profile's risk table rather than trusting the summary — same discipline applies at build time: fetch the PDF and confirm the category list.
- **OWASP Appendix B (LLM app architecture + threat modeling) not fetched.** Cited as the canonical architecture reference; `operator-added`. Fetch at build.
- **SLSA spec, OpenSSF model-transparency, HF LLM Course, genai.owasp.org, garak docs, NIST AI RMF Playbook, IAPP resources** — all `operator-added`; fetch at build time.
- **EU AI Act dates.** The tier concepts are verified via the FLI summary (updated 2026-08-31 for Digital Omnibus amendments). Operational details (application dates per tier) were deliberately left out of the lesson — anyone building on this must read the current Act text, which the lesson says.
- **ISO/IEC 42001 taught from free equivalents** per the brief (one line, paid standard noted). No gap — this is the brief's prescribed handling.
- **Walkthrough correction (logged, not smoothed):** the `ai-llm-top10` LLM10 demo's first run used model output containing an apostrophe, which broke shell quoting so the marker never appeared; re-ran with quote-free output — vulnerable builder shows the marker, fixed builder does not. Noted in `runs/ai-llm-top10.log`.
- **Marker-check correction (logged):** first AI-track marker check showed 000s — the test http.server was slow to bind; recheck on a fresh port passed 6/6. Noted in `runs/site-integration.log`. One orphan http.server from the first attempt was killed; zero remain.
- **CAISP chapters 4 (pipeline/DevOps) and 5 (threat modeling AI systems)** have no dedicated lessons yet — logged as future lessons. The track's reading order does not depend on them.

## Stage D specialist wave 1 gaps (2026-10-09)

- **Semgrep engine non-functional in this sandbox.** `pip install semgrep` (1.180.0) installed the Python shim but `pysemgrep` exits silently with no output — the OCaml engine binary never runs here. **Tried:** chmod +x, `python -m semgrep`, verbose flags, a real scan against a test file — all silent. The `d-appsec` walkthrough uses a labeled 30-line teaching sketch for the *triage* practice instead, and the lesson sends the reader to real Semgrep with exact commands. **Next:** run the real-Semgrep comparison step on a machine where the engine works.
- **Reader-side lab/account steps (by design, not run here):** ATT&CK Navigator import (layer JSON validated locally), Atomic Red Team atomics, FLARE VM / REMnux lab build, Prowler / ScoutSuite scans, ZAP + Dependency-Check — all require the reader's own isolated lab or own cloud account. Each lesson gives the exact procedure and marks the step **not run by us**.
- **Cloudsplaining input shape (resolved, logged):** `scan -i` expects an IAM *account authorization details* file, not bare policies — first attempt failed honestly in the log; corrected with a minimal fixture. Lesson text describes the corrected procedure.
- **YARA docs version note:** the stable docs line fetched is v4.4.0 (night research referenced 4.5.0). Lesson names the docs line used; rule syntax shown is version-stable.
- **Operator-added rows needing in-session fetch at build time:** ATT&CK C2 tactic page, LOLBAS, ATT&CK Navigator, RITA, Sysmon/Sysinternals docs, Cloudsplaining repo, OWASP ASVS, Stratus Red Team, MalwareBazaar, CIS Benchmarks (name the edition at audit time).
- **pgrep self-match / slow-bind notes:** the marker-check http.server needed an explicit kill by PID after the shell's `$SRV` kill missed it (logged in site-integration.log); zero http.servers remain — verified with pgrep.

## Stage B mechanics wave gaps (2026-10-09)

### Resolved this session
- **PTES Technical Guidelines URL — RESOLVED.** The page returned HTTP 403 during night research; it fetched cleanly in-session on 2026-10-09 (HTTP 200, 561,643 chars) and all seven phase names were confirmed on the primary page. The old `unreachable` gap entry is superseded — the `b-methodology` lesson cites the phases from the standard with the check date.
- **DVGA port — RESOLVED.** Current README (fetched 2026-10-09) says `:5013`; older mirrors saying `:5000` are stale. The `b-practice-targets` lesson teaches `:5013` and names the discrepancy.
- **WSTG IDOR test ID — CORRECTED.** The `b-idor` lesson and map.md cited `WSTG-ATHZ-02` for the IDOR test. Verified against the primary v4.2 pages in-session: IDOR is `WSTG-ATHZ-04`; `-02` is "Testing for Bypassing Authorization Schema." Corrected in `lessons/b-idor.md`, `map.md`, and the rebuilt `/g/idor/` page. The `b-methodology` lesson teaches the "verify the ID on the page, not from memory" discipline using this as the example.
- **build_site.py "Keep going" count drift — FIXED.** Lesson pages hardcoded "twenty-four" while the index listed 32. Now computed as `numword(len(LESSONS))`; all pages rebuilt.

### Open / carried
- **No Docker on this machine** (verified: `command -v docker` → missing). All five practice-target container runs are marked **not run by us**; the setup commands are verified quotes from the canonical READMEs fetched in-session. Reader runs them on their own machine. (Carried from earlier batches' substitution-policy question.)
- **Toolbench tools not installed here** (ffuf, subfinder/dnsx/httpx/amass, katana/gau/waybackurls, Burp/Caido/mitmproxy, Autorize/AuthMatrix, JWT Editor/jwt_tool, CodeQL, Trivy/Gitleaks, Flameshot/Dradis): marked **not run by us** with exact reader procedures in `runs/b-toolbench.log`. **Update 2026-10-10:** nmap 7.94SVN, Semgrep 1.180.0, and Playwright headless Chromium were installed and ran for real (see the gap-closing sprint section). Ran locally: curl, jq, ripgrep, ss, git, python urllib, nmap, semgrep, playwright.
- **HackerOne Hacktivity page** (HackerOne.com/hacktivity) returned only 1,794 chars — script-rendered shell. Cited as a reader-side resource; not a verified ledger row.
- **OWASP cheat-sheet project URL** https://owasp.org/www-project-cheat-sheets/ returns 404 — the canonical index is https://cheatsheetseries.owasp.org (already a verified row from an earlier batch). Lessons link the cheatsheetseries domain.
- **Legal content (CFAA / Computer Misuse Act):** taught at concept level from the primary statute pages (both fetched in-session); the lessons state explicitly this is not legal advice and the landscape moves. Not a gap — this is the prescribed handling.
- **Walkthrough hygiene corrections (logged, not smoothed):** (1) `pkill -f "http.server 8471"` matched the killing shell's own command line and SIGTERM'd the exec session — server verified gone afterward via non-self-matching pgrep; (2) first marker check used `grep` without `-E` (false low counts) and `kill $SRV` missed twice — rechecked with a proper script, 7/7 PASS, orphan killed by explicit PID; (3) a final "STILL RUNNING" was pgrep matching its own command line. All in `runs/site-integration.log`.
- **Word-count sanity:** `b-toolbench` (3,289), `b-methodology` (2,949), `b-authorization-scope` (2,787) exceed the brief's 2,500-word sanity ceiling; `b-practice-targets` (2,304) is inside. Judgment call: the toolbench lesson covers fifteen phases (~220 words each) and the methodology lesson covers three standards plus six phases — the substance fills the space, no padding added. Logged per the brief's "sanity check, never a target" rule.
- **Carried open decisions (not resolved):** (1) OWASP LLM Top 10 2026-vs-2025 edition question; (2) walkthrough substitution policy (local-demo / not-run steps vs Docker/model machine).

## Stage C disclosure wave gaps (2026-10-09)

- **Walkthrough corrections (logged, not smoothed):**
  1. `c-cvss` v3.1 scorer: first implementation rounded to 5 decimal places; the spec's Roundup means the smallest number to ONE decimal place ≥ input. Fixed; all 3 calibration vectors then matched published scores exactly.
  2. `c-cvss` v4.0: a from-scratch Python port of the MacroVector/interpolation scoring produced scores 0.2–0.5 off published values. Abandoned in favor of running FIRST's own reference implementation (cvss-v4-calculator, BSD-2-Clause) verbatim under node — all 5 published scores reproduced exactly. The abandoned port is not shipped.
  3. `c-cvd` lesson file was truncated mid-§7 during writing (sections 8–10 missing); detected by the section-count check, appended, re-verified at 10 sections.
- **cve.org is a JS SPA** — curl returns only the 880-byte app shell. The CNA directory (555 CNAs confirmed) and CVE Services pages (Record Format 5.2.0, researcher credit) were read via rendered page fetch in-session; the transcript notes the method. Re-verify the same way at build time.
- **NVD policy sourcing:** the April 15, 2026 prioritized-enrichment change is government-confirmed via Commerce OIG report OIG-26-020-I (PDF fetched in-session, 6.7 MB; report states NIST "will only enrich vulnerabilities that meet its new criteria"). No NIST-direct announcement page was found — the lesson describes the policy as government-confirmed via OIG, not NIST-direct. The three prioritized categories (KEV / federal-government software / EO 14028 critical software) are per consistent multi-outlet reporting of Booth's VulnCon26 announcement.
- **CVE-2021-44228 credits entry** has no `type` field (valid per schema — type is optional). The lesson uses this to teach asking for `type: finder` explicitly during coordination.
- **No real CVE request submitted** (by design): the `c-cve-program` walkthrough's worksheet is fictional and stays fictional. The program's forms are for real disclosures only.
- **Heartbleed/SandboxEscaper timelines** are reconstructed from public reporting (secondary sources per night research); the lesson presents them as worked-case reconstructions, not primary-verified timelines.
- **Operator-added rows needing in-session fetch at build time:** RFC 9116, OpenSSF maintainer guide, OWASP disclosure cheat sheet, RedHat CVE-HOWTO, Project Zero disclosure policy page, CAPEC.
- **Carried open decisions (not resolved):** (1) OWASP LLM Top 10 2026-vs-2025 edition question; (2) walkthrough substitution policy.

## Stage A remainder wave gaps (2026-10-09)

- **a-windows-concepts: no Windows on the build bench.** All five hands-on steps marked **not run by us** with exact reader procedures; the lesson is Level 2 (reader's own VM reaches 3). What WAS verified in-session: Microsoft "Registry Hives" and "Get-WinEvent" reference pages fetched 2026-10-09 (hive definitions, supporting-file table, cmdlet syntax sets, FilterHashtable pattern, 4624/4625 IDs). No PowerShell output was invented. The Microsoft Learn training module (registry tour) is a lead — verify at build time.
- **a-osint-research: fictional target only, by design.** Walkthrough ran fully against local teaching artifacts (`/tmp/osintwalk/harborlight/`) — fictional `harborlight-books.example`, zero packets left the machine, no real target touched. The lesson's "not run by us" marker is legitimately ABSENT (first marker-check FAIL was a wrong marker, corrected on recheck — logged in runs/site-integration.log). OSINT Framework, Bellingcat toolkit, TraceLabs are operator-added leads — verify at build time.
- **a-reading-code: hostile input executed as string construction only.** The `' OR '1'='1` trace printed the built query; it was never executed against a database. The lesson states this. SQLite lang.html is a lead.
- **a-python-security: stdlib only.** The walkthrough deliberately avoids pip/requests — noted in-lesson as the dependency discipline. py4e.com and automatetheboringstuff.com are operator-added (verified in night research, not re-fetched this session).
- **Carried open decisions (not resolved):** (1) OWASP LLM Top 10 2026-vs-2025 edition question; (2) walkthrough substitution policy (local-demo / not-run steps vs Docker/model machine).

## Correction applied this batch (resolved 2026-10-09) — OWASP LLM Top 10:2026 codes + release date

- **Wrong codes in the new `ai-pipeline` lesson (caught before publish).** The draft cited "LLM04 (Data and Model Poisoning)" and "LLM03 (Supply Chain)". Fetching the official GenAI repo's `2026/` directory in-session proved the final 2026 mapping is **LLM04:2026 Supply Chain** and **LLM05:2026 Data and Model Poisoning** (the compromised-build-pipeline scenario lives in LLM04, not LLM03 — the July PR that added it used the pre-renumbering draft codes). All 10 occurrences in `lessons/ai-pipeline.md` corrected; map.md row updated. The earlier lessons (`ai-llm-top10`, `ai-supply-chain`) already carried the correct final mapping — verified against the same page.
- **Wrong release date across the guidebook (caught before publish).** Night research had recorded "released 2026-09-30"; the project's own repo states **Release date: August 4, 2026** (`2026/` directory, canonical source). Corrected in `ai-llm-top10.md`, `ai-prompt-injection.md`, `ai-supply-chain.md`, `gaps.md`, `STATE.md`, `sources.csv` (6 files, zero remaining occurrences of the old date).
- ATLAS technique pages (beyond the matrix) remain cookie-wall-sensitive — matrix verified in-session; individual technique pages retry from a live browser if needed before publish.
- SP 800-55 volumes themselves not read (only the NIST release page, verified) — the lesson's metrics guidance beyond the release-page summary needs the volumes fetched before publish.
- No Docker / no local model on this machine (carried): `ai-pipeline` walkthrough used the deterministic local harness (fully ran); worked-case lessons have no CLI by design.

## Final wave: Stage D wave 2 + Stage C remainder (2026-10-09)

- **Anthropic CVP announcement primary URL not fetched.** Guessed path `anthropic.com/cyber-verification-program` returned 404; tier details in `c-ai-tooling` are consistent across 6+ outlets dated 2026-10-06–08 plus the CellCog page (fetched in-session, which read the announcement directly). Lesson states this plainly and dates every claim. **Next:** fetch the exact announcement URL at publish time and upgrade the sources.csv row from `operator-added` to `verified`.
- **CyScenarioBench figures are Anthropic's own** (0/50, 4/50, 34/50) — independent validation flagged absent in coverage; lesson states this. Do not repeat the numbers without the caveat.
- **pwn.college re-verification:** night research verified it live 2026-10-09 (ASU-run, free); not re-fetched this session. Re-confirm live before publish.
- **DFIR lesson primary leads** (NIST SP 800-86, Volatility 3 docs, SIFT docs, Autopsy, Eric Zimmerman tools) and **exploit lesson leads** (how2heap, OST2, Ghidra, exploit.education, ROP Emporium) are `operator-added` — fetch each at build time before publish.
- **Kettle HTTP/2 exact article URL** not fetched — row cites portswigger.net with the gap noted.
- **dfir-deep marker-check false FAIL** (same class as osint-research, incident-response): "not run by us" legitimately absent — the walkthrough fully ran (7/7 steps). Corrected on recheck; logged in runs/site-integration.log.

## Bug bounty + stage pages batch (2026-10-09)

- **Bug-bounty platform docs are `operator-added`, not re-fetched this session.** The lesson's claims rest on night-research rows S11–S13 (fetched 2026-10-09 in that session: HackerOne program-types explainer, Bugcrowd researcher docs, Intigriti). Re-fetch each platform's current researcher docs at publish time and upgrade the sources.csv rows to `verified` — program policies change.
- **No real submission anywhere in the lesson** (by design): the walkthrough is a dry-run report against a fictional finding. The lesson says plainly that the first real submission happens after it, on a real program.
- **bug-bounty marker-check false FAIL** (same class as dfir-deep/osint-research/ai-pipeline/incident-response): "not run by us" legitimately absent — the walkthrough fully ran (8/8 steps, worked case). Corrected on recheck; logged in runs/site-integration.log.
- **Stage pages are generated from data** (STAGES table in build_site.py + map.md/LESSONS), not hand-authored prose — no walkthrough applies; noted in the handoff. Stage D milestone wording: the brief names no single Stage D artifact, so the page says the milestone is a capstone body of work in one track and labels that as the guidebook's reading of the brief.
- **Stage E claims block** states the CISSP experience rule (5 years / Associate of ISC2) per the brief's correction — the brief requires it once on the CISSP map page; the stage page states it as the issuer's rule and the map page will carry it too when built.
- **Carried open decisions (not resolved):** (1) OWASP LLM Top 10 2026-vs-2025 edition question; (2) walkthrough substitution policy (local-demo / not-run steps vs Docker/model machine).

## Role paths + knowledge maps batch (2026-10-09)

### Candidate roles (brief §5: do NOT create role pages — listed here)
- **Red team operator:** A → B → C → D red team; adversary emulation (ATT&CK, Atomic Red Team), C2 concepts taught defensively with detection, purple teaming; proof is emulation plans and reports. NICE has no direct work role for it (offensive roles moved to the DCWF).
- **Exploit developer:** A → B → D exploit dev/RE; binary analysis, debugger fluency, modern mitigations; proof is original research and tooling; no NICE work role.
- **Malware analyst:** A → B defensive → D malware analysis; static/dynamic analysis, sandboxing, behavioral indicators; proof is published analyses; partially covered by NICE Investigation/Protection-and-Defense forensics roles.
- **Security program lead:** A → E + Oversight-and-Governance; CISSP domains, NIST CSF 2.0, metrics, board communication; maps to NICE OG roles (Executive Cybersecurity Leadership, Cybersecurity Management).
- **Correction vs the brief:** the brief listed "AI security engineer" as a role the site doesn't have — it does: `/r/ai-security-engineer/` exists and two role pages link it as a continuation. Not a candidate.

### CISSP objectives with no lesson — RESOLVED 2026-10-10 (45/45 now have lessons)

All 45 remaining objectives were written as Stage E lessons in the CISSP coverage wave (2026-10-10), five parallel batches. The map page now shows **62 of 62** objectives covered, zero "No lesson yet."

| Objective | Lesson |
|---|---|
| 1.1 | `e-ethics` — Professional ethics in security work |
| 1.2 | `e-security-concepts` — Core security concepts: CIA and related properties |
| 1.3 | `e-governance` — Security governance: aligning security with business strategy |
| 1.4 | `e-cyber-law` — Legal, regulatory, and compliance landscape |
| 1.5 | `e-investigations` — Investigation types and their requirements |
| 1.6 | `e-policy-docs` — Security policy, standards, procedures, and guidelines |
| 1.8 | `e-personnel-security` — Personnel security across hiring, employment, departure |
| 1.10 | `e-threat-modeling-concepts` — Threat modeling concepts and methodologies |
| 1.11 | `e-supply-chain-risk` — Supply chain risk management |
| 1.12 | `e-awareness-training` — Security awareness, education, and training programs |
| 2.1 | `e-asset-classification` — Identifying and classifying information and assets |
| 2.2 | `e-handling-requirements` — Information and asset handling requirements |
| 2.3 | `e-asset-provisioning` — Secure provisioning: ownership, inventory, asset management |
| 2.4 | `e-data-lifecycle` — The data lifecycle: roles, retention, remanence, destruction |
| 2.5 | `e-retention-eol` — Asset retention and end-of-life/support |
| 2.6 | `e-data-protection-controls` — Data security controls and compliance |
| 3.1 | `e-secure-design` — Secure design principles for engineering |
| 3.2 | `e-security-models` — Formal security models (BLP/Biba/Clark-Wilson/Brewer-Nash) |
| 3.3 | `e-control-selection` — Selecting controls from system security requirements |
| 3.4 | `e-platform-security` — Platform security capabilities |
| 3.5 | `e-arch-vuln-assessment` — Assessing vulnerabilities across architecture types |
| 3.7 | `e-cryptanalysis` — Cryptanalytic attack methods (resolves the e-crypto-applied gap note) |
| 3.8 | `e-facility-design` — Site and facility design principles |
| 3.9 | `e-facility-controls` — Site and facility security controls |
| 3.10 | `e-system-lifecycle` — The information system lifecycle |
| 4.1 | `e-network-architecture` — Secure network architecture design |
| 4.2 | `e-network-components` — Securing network components |
| 4.3 | `e-secure-channels` — Secure communication channels |
| 5.6 | `e-auth-systems` — Implementing authentication systems |
| 6.1 | `e-assessment-strategy` — Designing assessment, test, and audit strategies |
| 6.2 | `e-control-testing` — Security control testing methods |
| 6.3 | `e-security-metrics` — Collecting security process data |
| 6.4 | `e-test-analysis-reporting` — Analyzing test output and reporting |
| 6.5 | `e-security-audits` — Conducting and facilitating security audits |
| 7.1 | `e-investigation-forensics` — Investigations: evidence, techniques, forensics |
| 7.2 | `e-logging-monitoring` — Logging and monitoring operations |
| 7.3 | `e-config-management` — Configuration management |
| 7.4 | `e-secops-concepts` — Foundational security operations concepts |
| 7.5 | `e-media-protection` — Resource and media protection |
| 7.6 | `e-incident-management` — Incident management |
| 7.7 | `e-detective-preventive` — Operating detective and preventive measures |
| 7.8 | `e-patch-management` — Patch and vulnerability management operations |
| 7.9 | `e-change-management` — Change management |
| 7.14 | `e-physical-security` — Physical security implementation |
| 7.15 | `e-personnel-safety` — Personnel safety and security concerns |

**Factual corrections applied during this wave (verified in-session 2026-10-10):**
- SP 800-88 Rev. 1 withdrawn 2025-09-26 \u2192 Rev. 2 (Sept 2025) is current. `e-media-protection` (written against Rev. 1) updated to Rev. 2; withdrawal date verified against NIST\u2019s own CSRC page.
- SP 800-63-4 (July 2025) supersedes 800-63-3. `e-iam` \u00a77 updated to the 4th revision; `e-auth-systems` teaches it.
- SP 800-55 Rev. 1 withdrawn 2024-12-04 \u2192 Vols. 1+2 (Dec 2024) current (already correct in `e-security-program`; new `e-security-metrics` teaches the withdrawal).
- SP 800-50 (2003) withdrawn Sept 2024 \u2192 Rev. 1 (Sept 2024) current; `e-awareness-training` teaches Rev. 1.
- NISTIR 7316 is "Assessment of Access Control Systems," not an ABAC paper \u2014 `e-iam` \u00a77 description corrected.
- CISA BOD 22-01 revoked 2026-06-10, superseded by BOD 26-04 \u2014 taught in `e-patch-management`.
- CSF 2.0 has no ID.AM-06 (numbering jumps 05\u219207) \u2014 stated in `e-asset-classification`.

**Lesson gaps the paths surface \u2014 remaining:** ~~the governance-framework lessons (NIST CSF 2.0, ISO/IEC 27001, SOC 2) still have no lessons~~ — **RESOLVED 2026-10-10:** `e-csf-20`, `e-iso27001`, `e-soc2` written, built, and wired into the GRC path ("Governance frameworks" group replaces the "Still to come" note).
- **Internal conflict (RESOLVED 2026-10-10):** `e-crypto-applied`'s Map-ref line said objective 3.7 had no lesson. The new `e-cryptanalysis` lesson serves 3.7, and `e-crypto-applied`'s Map-ref now points to it.

### Lesson gaps the paths surface
- **Cloud fluency block:** the cloud-security path needs a "core cloud services" lesson (compute/storage/networking/IAM of one major cloud, learned in the reader's own account) before `d-cloud-security`. None exists — the path page says so and logs it here.
- **Governance-framework lessons (RESOLVED 2026-10-10):** `e-csf-20` (NIST CSF 2.0), `e-iso27001` (paid-document one-liner honored; taught from ISO free pages), `e-soc2` (Trust Services Criteria) — all written from the E-GOV-01/02/03 specs, every factual claim re-verified in-session. One remaining fetch gap: the AICPA's own SOC 2 overview page (aicpa-cima.com topic page) timed out on the in-session fetch and was not retried — the lesson ships with two verified resources; re-check at build time.
- **Stage A cryptography lesson:** referenced by `e-crypto-applied`'s map ref (see conflict above); not in the lesson set. Needed by the IAM path's cryptography step (currently filled by `e-crypto-applied`, which is Stage E depth).

### OWASP LLM Top 10 release-date conflict (our own files)
- The pilot handoff says the 2026 edition was released 2026-09-30; `ai-llm-top10.md`'s Map-ref line says 2026-08-04. The CAISP map page says "2026 edition" with no date. **Next:** re-verify the edition release date against the official OWASP GenAI Security Project repo at publish time and fix the lesson file.

### Carried open decisions (not resolved)
1. OWASP LLM Top 10 2026-vs-2025 edition question.
2. Walkthrough substitution policy (local-demo / not-run steps vs Docker/model machine).

## Gap-closing sprint 2026-10-09 (web-verification track)

**Ledger state:** 214 rows total → **208 verified**, 2 unreachable, 4 operator-added (was 97 verified / 99 operator-added at sprint start per the task brief; the row count grew as new verified rows were added for cited-but-unrowed sources).

**Critical correction applied:** RFC 6265 has NO §4.1.2.7 (it ends at §4.1.2.6 HttpOnly). SameSite is normatively defined in **draft-ietf-httpbis-rfc6265bis §5.6.7**. Fixed in `lessons/b-csrf.md` and rebuilt `/g/csrf/index.html` via build_site.py. sources.csv row corrected to the bis draft (138,768 chars, HTTP 200).

**LLM Top 10 2026 date verdict:** **2026-08-04 is canonical** — confirmed against the official repo README (github.com/GenAI-Security-Project/GenAI-LLM-Top10: "**Current release: 2026 — published August 4, 2026**"), corroborated by the OWASP legacy repo and two independent derivatives. The 2026-09-30 in the pilot handoff was wrong; zero occurrences remain in lessons/pages (already purged). No lesson-file fix needed.

**Every URL tried this session (all fetched 2026-10-09):**

*RFCs (rfc-editor.org .txt, all HTTP 200):* 8446 (337,736 chars), 6749 (163,498), 6797 (103,554), 9116 (45,129), 1034 (126,103), 791 (94,892), 4033 (52,445). SameSite: draft-ietf-httpbis-rfc6265bis-22.txt (138,768 chars, §5.6.7 confirmed).

*PortSwigger (all HTTP 200):* /web-security/sql-injection, /os-command-injection (45,944), /ssrf (49,834), /csrf (48,664), /cross-site-scripting (60,884), /authentication (43,707), /web-security/logic-flaws (41,510). Lab slugs not enumerated — lessons link topic pages, not individual labs.

*OWASP cheat sheets (all HTTP 200, real slugs from the GitHub repo file list):* Cross_Site_Scripting_Prevention (117,207), Authentication (135,420), OS_Command_Injection_Defense (89,372), Server_Side_Request_Forgery_Prevention (115,663), Access_Control (59,198), Vulnerability_Disclosure (101,356), Threat_Modeling (88,587), Cryptographic_Storage (93,638). The guessed forms for XSS/Auth were wrong; lessons cite the bare domain so no lesson URL fixes needed.

*CWE (all HTTP 200, IDs+names confirmed):* 79, 89, 78, 918, 352, 840, 287, 384, 693, 862, 787.

*Anthropic CVP:* real URL is **https://www.anthropic.com/news/cyber-verification-program** ("Expanding the Cyber Verification Program", 2026-10-06). Tier details verified from Anthropic's own page: Defense Access (SOC/IR, malware RE, vuln validation; individuals eligible; days), Red Team Access (adds authorized pentesting; org-only; weeks; blocks remain on physical-harm/mass-disruption), Specialized Access (fewest blocks; safety-critical; US-gov review; Glasswing members transition). CyScenarioBench: 46/50 blocked Defense, 34/50 completed Red Team.

*Bounty docs (all HTTP 200):* HackerOne bounties blog (309,640), Bugcrowd researcher onboarding (112,240), Hacker101 (314,493), Intigriti researchers (628,479). Hacktivity → **unreachable** (script-rendered shell, 1,794 chars).

*NIST:* AI 600-1 PDF (1,174,643 bytes; **12 numbered risk categories confirmed from PDF text**, CBRN through Value Chain); SP 800-39 PDF (1,228,127 bytes, "Managing Information Security Risk" confirmed).

*OWASP LLM Appendix B:* MD stub (424 chars) + the Threat Model 2026 diagram PNG (1,421,618 bytes, HTTP 200). Verified.

*DFIR (all HTTP 200):* SP 800-86 landing (45,371), Volatility Foundation (249,179), SANS SIFT (381,193), Autopsy (46,309), Eric Zimmerman tools (31,761).

*Exploit (all HTTP 200):* pwn.college (21,751), how2heap (412,228), OST2/ost2.fyi = OpenSecurityTraining2 (2,080,003), Ghidra GitHub (360,033), exploit.education (16,384), ROP Emporium (8,350).

*CAPEC:* catalog + CAPEC-1 pattern page ("Accessing Functionality Not Properly Constrained by ACLs", 45,266 chars). Verified.

*CISA KEV:* **https://www.cisa.gov/known-exploited-vulnerabilities-catalog** (hyphenated; the unhyphenated form 404s) — 285,443 chars, HTTP 200. Lesson files using the old URL need the hyphenated form.

*NVD enrichment policy:* bonus attempt — NVD vuln page and dashboard carry no April 2026 policy text. OIG confirmation (OIG-26-020-I) stands as the sourcing.

*OWASP Agentic AI Top 10:* page now loads (was 403) — https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ (ASI01–ASI10; risk list in the PDF). Verified.

*AICPA TSC:* primary page live — 2017 Trust Services Criteria (With Revised Points of Focus — 2022), full doc needs free account. Verified.

*SANS:* SEC598 (https://www.sans.org/sec598, full syllabus text) and SEC535 (https://www.sans.org/sec535, full syllabus text) both load. Verified.

*Bulk verifications (all HTTP 200):* OWASP Top 10:2025, DVWA, Juice Shop, MDN Set-Cookie, SP 800-92 (DOI→PDF 1.7MB), sysmon-config, Wazuh, Security Onion, Velociraptor, Atomic Red Team, ATT&CK Navigator, CERT CVD guide, OWASP SAMM, FIDO Alliance, SLSA, OpenSSF model-transparency, HF LLM course, genai.owasp.org hub, garak, NIST AI RMF Playbook, IAPP, ATT&CK TA0011, LOLBAS, RITA, Sysmon docs, Cloudsplaining, OWASP ASVS, Stratus Red Team, MalwareBazaar, OSSF oss-vulnerability-guide, CVE-HOWTO, Project Zero disclosure policy, py4e, SQLite docs, OSINT Framework, Bellingcat toolkit, opensecuritytraining.info, Project Zero blog, Anthropic Help Center, Practical DevSecOps (CAISP), OWASP WSTG, ISC2 CISSP exam outline (effective 2024-04-15; 8 domains 16/10/13/13/13/12/13/10), James Kettle "HTTP/2: The Sequel is Always Worse" (**https://portswigger.net/research/http2** — the row's bare portswigger.net URL was corrected), SP 800-63 (URL corrected to /pubs/ form), NISTIR 7316, Sigma repo, Automate the Boring Stuff, CISA homepage.

**Unreachable (2):** HackerOne Hacktivity (script-rendered); MS Learn "Examine the Windows registry" module (retired — redirects to generic training browse; row 160 registry-hives docs stand as the replacement).

**Still operator-added (4) and why:**
- MITRE ATLAS rows (2): cookie-walled; needs live-browser verification (subagent has no live browser). Technique IDs (AML.T0051 etc.) corroborated by multiple secondary sources but not primary-fetched.
- CIS Benchmarks: 403 Cloudflare block on 2026-10-09.
- man pages row: ships with the OS, no URL possible by definition.

**Lesson-file corrections needed from this sprint:**
1. `b-csrf.md` — DONE (RFC 6265 §4.1.2.7 → draft-ietf-httpbis-rfc6265bis §5.6.7; site rebuilt).
2. Any lesson citing the CISA KEV catalog at the unhyphenated URL → use https://www.cisa.gov/known-exploited-vulnerabilities-catalog.
3. Any lesson citing James Kettle's HTTP/2 research at bare portswigger.net → use https://portswigger.net/research/http2.
4. Any lesson citing the MS Learn registry module → replace with the registry-hives docs (https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-hives).

**CSV hygiene note:** mid-sprint the file's unquoted comma-containing claims broke naive rsplit parsing; the whole file was rewritten with proper CSV quoting (backup at sources.csv.bak-20261009). Schema intact: claim/resource, primary URL, fetch date, status.

## Gap-closing sprint, environment track + follow-ups (2026-10-10)

**Environment (all installed for real on this machine, all loopback-only):**
- nmap 7.94SVN (8 .debs hand-fetched from archive.ubuntu.com; apt mirrors hang) — `nmap -sT -p 18499 127.0.0.1` → open. `runs/b-toolbench.log`. Lesson/page `g/toolbench/` updated.
- tcpdump 4.99.4 — full loopback SYN/SYN-ACK/ACK/data/FIN capture, 10 packets (`-Z root` required; container has no tcpdump user). `runs/a-tcpip-ports.log`. `g/tcpip-ports/` step 8 marker closed.
- dig 9.18.39 — all DNS query steps re-ran real (`+tcp -p 53535 @127.0.0.1`): A, CNAME, TXT, NS, NXDOMAIN. `runs/a-dns-depth.log`. `g/dns-depth/` updated.
- Playwright headless Chromium 1243 — JS execution verified. Re-ran for real: b-xss steps 4/6 (reflected + DOM markers fired; fixed build silent), b-csrf step 4 (attacker's auto-submit page changed the victim's email for real), b-security-headers steps 3/4 (CSP blocked the inline handler with a console violation; cross-origin frame refused with `chrome-error://chromewebdata/`, and same-origin framing correctly allowed). All six pages rebuilt; markers verified in HTML.
- Semgrep 1.180.0 — clean venv install works (system pip had a typing_extensions RECORD conflict). The old "dead shim" gap entry is superseded: **step 5 of `d-appsec` re-ran with the real engine** 2026-10-10 (local 4-rule file; 4 findings incl. a taint-tracked flow the teaching sketch can't see; both sketch and engine miss the business-logic flaw — the lesson's core point now proven against the real tool). `runs/d-appsec.log`, `g/appsec/` updated.
- Docker / local AI model / Windows / sshd — confirmed unavailable on this machine (single verification each; no multi-GB downloads attempted). Markers stay honest.
- Hygiene: zero stray processes after each re-run (explicit-PID kills; verified with non-self-matching pgrep). One VM recycle mid-sprint wiped /tmp; all re-runs redone with evidence under `.gap-sprint/` (persistent).

**Lesson-file corrections from the web sprint — all DONE (2026-10-10):**
1. b-csrf RFC 6265 §4.1.2.7 → draft-ietf-httpbis-rfc6265bis §5.6.7 (done by web crew).
2. CISA KEV URL → hyphenated form (fixed in `lessons/c-vuln-ecosystem.md`, page rebuilt).
3. Kettle HTTP/2 → `portswigger.net/research/http2` (added in `lessons/c-public-track-record.md`, page rebuilt).
4. Retired MS Learn registry module → registry-hives docs (fixed in `lessons/a-windows-concepts.md`, page rebuilt).

**Still open (not closable from here):** 2 ATLAS rows (cookie-walled — live-browser check delegated 2026-10-10), CIS Benchmarks (403 Cloudflare), man pages (no URL by definition), Docker/AI-model/Windows/sshd walkthrough steps (honestly labeled), the two Dino decisions (LLM edition; substitution policy), 45 CISSP objectives without lessons (future lesson work, not verification gaps).

## Decisions ratified by Dino (2026-10-09, whole-permission order)

1. **OWASP LLM Top 10 edition: 2026.** The guidebook teaches the verified current edition (released 2026-08-04, codes renumbered). Brief-2 §5's "2025" is amended by this decision. No lesson changes needed — lessons already teach 2026.
2. **Walkthrough substitution policy: ACCEPTED.** Clearly labeled local-demo/deterministic substitutions and "not run by us" markers stand as the guidebook's honesty policy. Production-ready = every step is either run-with-transcript or honestly marked, not Docker-on-this-box. Docker/model/Windows/sshd steps remain marked and re-runnable by the reader.

## Brief-compliance wave — directory additions (2026-10-10)

Brief §8 Phase 4: 35 directory-worthy resources added to data/catalog.json (889 → 924 rows; `count` field updated; schema unchanged; no existing rows touched). All 35 come from `verified` sources.csv rows not already in the catalog: OWASP Cheat Sheet Series, PortSwigger Web Security Academy, MITRE ATLAS, ATT&CK Navigator, CWE, CAPEC, CISA KEV catalog, FIRST CVSS v4.0 spec, EPSS, Wazuh, Security Onion, Velociraptor, YARA docs, Ghidra, pwn.college, Nmap, Semgrep, SLSA, Sigstore, CycloneDX, CERT CVD Guide, CVE Program CNA directory, RFC 8446, RFC 9110, REMnux, OpenSSH manuals, PTES Technical Guidelines, CISA, MalwareBazaar, Hacker101, Intigriti researcher resources, LOLBAS, Project Zero blog, Python docs, CIS Critical Security Controls v8.1. Verification dates filled from the ledger (v field). Five duplicate URLs found during dedup were pre-existing catalog rows (LangChain, SnowPro, MLOps Zoomcamp, WCAG) — left untouched.

## Light knowledge maps: AIGP / GASAE / GOAA / AAISM — 2026-10-10 (research done, integration pending)

All four outlines were fetched from the issuer in-session on 2026-10-10 and ledgered as `verified` (8 new rows; sources.csv now 324 rows). Domain-level only, per brief §4. Domain titles are the issuers' words; outcome statements paraphrased; no exam questions or outline text reproduced.

- **AIGP (IAPP):** BoK v2.1, effective 2026-02-02 (supersedes 2.0.1) — 4 domains, all map to lessons (4/4).
- **GASAE (GIAC):** "Exam Certification Objectives & Outcome Statements" — 10 objectives, all map to lessons (10/10). GASAE maps use the `ai-sec-automation` lesson, which is being written in parallel by another agent; the integrator must check it exists in LESSONS before building (it was absent from build_site.py at research time).
- **GOAA (GIAC):** "Exam Certification Objectives & Outcome Statements" — 10 objectives; 7/10 map to lessons. Three with no lesson, logged honestly: "Audio, Image, and Video Deepfakes" (no deepfake lesson exists in the guidebook), "Creating Phishing Emails with AI" and "Social Engineering Fundamentals" (no social-engineering lesson; the guidebook's safety line excludes phishing tooling — do not close these by writing how-to content). "Creating Malicious Software with AI" maps to `d-malware-analysis` (analysis/detection, not authoring); "Bypassing Defensive Controls" maps to `d-exploit-concepts` (concepts + the mitigation landscape) — the map's notes must keep this framing visible.
- **AAISM (ISACA):** exam content outline — 3 job practice domains, all map to lessons (3/3). Prerequisite CONFIRMED at isaca.org: active CISM or CISSP required (press release, in-session). ISACA's other AI credentials CONFIRMED as separate at isaca.org: AAIA (Advanced in AI Audit, launched May 2025) and AAIR (Advanced in AI Risk) — three credentials, not one. The AAISM map must carry the prerequisite note and must not imply AAISM is ISACA's only AI credential.
- SANS pairings verified in-session at sans.org: SEC598 → GASAE (5 course sections → 10 objectives), SEC535 → GOAA (3 sections → 10 objectives). Courses are paid; the maps teach the subject areas from free lessons. Nothing paywalled blocked the research — every outline was read in full at the primary source.

## Frontmatter refactor (2026-10-10)

Brief §4 data contract implemented: all 107 lessons carry YAML frontmatter (stage, level, prerequisites, roles, map_refs, test_date); the builder generates the registry, link map, counts, path membership validation, stage listings, and knowledge-map references from it. Verification gate passed (128 pages, 4,936 internal links 0 broken, zero regressions).

Open from this work:
- 6 new crew lessons (`a-crypto`, `b-api-abuse`, `b-ssti`, `b-xxe`, `b-deserialization`, `ai-sec-automation`) have `roles: []` — not yet placed in role paths.
- `ai-sec-automation` has no runs log yet; its dateline says the walkthrough is being finalized. Test date to be confirmed.
- Sitemap is still hand-maintained (no builder).
- `map.md` frozen as a research artifact; frontmatter is now canonical.

## Brief-compliance wave (2026-10-10)

**AI-track SEC598/SEC535 lesson** (`ai-sec-automation`): SANS SEC598 + SEC535 re-verified in-session 2026-10-10 (GASAE/GOAA pairings confirmed from the pages' own statements). Lesson teaches both subject areas as concepts paired with defenses and defender telemetry; SANS courses named as paid in one line; walkthrough = worked detection plan for an AI-automated attack chain.

**CISSP AI-note verdict: exam content, not commentary.** The per-domain AI notes live in ISC2's "Exam Guidance for Artificial Intelligence" (Sept 1, 2026), which maps AI topics across 50+ exam domains / 200 subtasks woven into all eight CISSP domains via the normal 3-year refresh cycle. The CISSP certification page itself carries only a banner, not per-domain notes (brief §3's premise corrected). All eight domains now carry an AI-note line on /g/map-cissp/ linking AI-track lessons.

**Four light knowledge maps** (brief §4): /g/map-aigp/ (4/4), /g/map-gasae/ (10/10), /g/map-goaa/ (7/10 — deepfakes, AI phishing email, social-engineering fundamentals honestly unmapped; safety line excludes phishing/malware how-tos), /g/map-aaism/ (3/3; AAISM needs active CISM or CISSP; AAIA/AAIR named as separate ISACA credentials). All outlines verified in-session at the primary issuers 2026-10-10.

**Directory**: 35 rows added to data/catalog.json (889 → 924), all from verified ledger rows, schema unchanged, no existing rows touched.

## Frontmatter refactor (2026-10-10)

Brief §4 data contract implemented: all 109 lessons carry YAML frontmatter (stage, level, prerequisites, roles, map_refs, test_date, description, dateline); the builder generates the registry, link map, counts, path membership validation, stage listings, and knowledge-map references from it. The 320-line LESSONS hand table is deleted; CISSP_DOMAINS and CAISP_CHAPTERS are prose-only (mapping inverted from frontmatter at build). Verification gate passed (131 pages, 5,013 internal links 0 broken, zero regressions vs pre-refactor).

Open from this work:
- 9 new crew lessons (`a-crypto`, `b-api-abuse`, `b-ssti`, `b-xxe`, `b-deserialization`, `b-graphql`, `b-race-conditions`, `b-jwt-oauth`, `ai-sec-automation`) have `roles: []` — not yet placed in role paths.
- `ai-sec-automation` has no runs log yet; its dateline says the walkthrough is being finalized. Test date to be confirmed.
- Sitemap is still hand-maintained (no builder).
- `map.md` frozen as a research artifact; frontmatter is now canonical.
