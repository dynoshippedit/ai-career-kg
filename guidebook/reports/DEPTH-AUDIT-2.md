# Content-depth audit, second pass — all 110 lessons (2026-10-10)

Dino's order: "try again" — the first pass (105 solid / 5 deepened) was too lenient.
Six stage crews applied five sharper lenses to every lesson:

1. **Unpacked jargon** — terms used but never defined (brief §1: "Define each term where it is first needed, by what it does")
2. **Missing "why"** — design rationale: why is it built this way, what breaks if you remove it
3. **Detection gaps** — concrete defender-side signals (log lines, alerts, telemetry), not "check the logs"
4. **Worked-example gaps** — concrete worked examples in "How it works" where abstract-only
5. **"Read the source" quality** — §7 must say HOW to read the primary docs (which sections, what order, what to skip)

**Result: 110/110 lessons edited.** Lens fire totals: L1 ~99/110, L2 ~74/110, L3 ~58/110 (attack/detection-applicable), L4 1/110, L5 7/110. No levels changed. No padding — where a lens didn't fire, crews recorded why. ~37 new source rows staged, 30 merged (7 URL dupes skipped); sources.csv now 375 rows.

Per-stage detail follows (merged from the six crew reports, kept alongside).

---


======================================================================
# Stage A
======================================================================

# Depth audit 2 — Stage A (stricter pass, five lenses)

Auditor: subagent session 7480edce · 2026-10-10.
Scope: the 10 Stage A lessons in `guidebook/lessons/a-*.md`.
Method: every lesson re-read end to end. All five lenses applied to every lesson (unlike pass 1, which judged overall solidity). Additions are surgical: one-liner definitions where terms are first needed, 1–2 sentence design-rationale inserts in §3, concrete defender signals, one new worked walkthrough step (run, transcript appended). No level changes (levels were already honest). No padding: lens 4 (worked examples) fired zero times — every lesson already had one.

Lens key: **L1** unpacked jargon · **L2** missing "why" · **L3** detection gaps · **L4** worked-example gaps · **L5** "read the source" quality.

## Per-lesson verdicts

| Lesson | Lenses fired | What was added (specific) |
|---|---|---|
| a-crypto | L1, L2, L3, L4 | L1: salt defined by function (random data mixed into each password → identical passwords hash differently); IV defined (random starting value so identical plaintexts encrypt differently); authenticated encryption defined (proves ciphertext wasn't tampered with); malleable defined; PBKDF2 defined in §4 step 3 (password-based key derivation, thousands of hash iterations, slowness deliberate). L2: why you sign the *hash* not the data (signing is slow; digest commits to exact content). L3: Certificate Transparency logs as the one log-side signal for PKI misuse (unrequested cert for your domain = mis-issuance/attacker minting). L4: **new §4 step 8 — salt demonstration, RUN** (same password, two salts → two digests; transcript appended to `runs/a-crypto.log`). Dateline updated. |
| a-dns-depth | L1, L2, L3 | L1: DoT/DoH defined (query encrypted inside TLS/HTTPS to the resolver); zone transfer defined (secondary copying a zone's full record set — the operation that always needs TCP); label entropy defined (how random the labels look — DGA/tunneled data is high-entropy gibberish); SPF and DKIM defined at the TXT record-type line. L2: why the stub doesn't walk the tree (load, not capability — roots would drown; the recursor centralizes walking and caching). L3: **concrete BIND query-log line** for DGA detection (`client @0x… ip#port (name): query: name IN A …`), format verified in-session against ISC's BIND 9 ARM — staged source row. |
| a-git-github | L1, L2, L3 | L1: CI defined (automated checks that run on the pull request before merge); Git LFS defined (big files outside the object database, pointer in the repo). L2: **why git uses content-addressed snapshots** (identity-by-content → any two copies of a hash hold the same bytes; corruption/tampering detected on read; the no-trusted-central-server design that makes every clone a verifiable backup). L3: defender's secret check on inherited repos — `git log --all -S 'BEGIN RSA PRIVATE KEY'` plus secret scanners (verification off) and GitHub's own secret-scanning alerts; rotation first, deletion second. |
| a-http-depth | L1, L2, L3 | L1: base64url (URL-safe alphabet, why it exists); MAC (keyed checksum proving integrity + key-holder authorship); bearer token (proves you hold it, not who you are); oracle (yes/no answering machine — §5); parser differential (two systems disagreeing on the same bytes — §4 step 8); multiplexed; QUIC; cipher. L2: **why HTTP is stateless** (any server handles any request — no per-client memory → trivial load balancing, crash loses nothing); **why TLS needs a handshake** (can't just encrypt: must agree algorithms, authenticate server first, solve key distribution — task's own example); **why SameSite exists** (browsers attach cookies automatically — the exact thing CSRF exploits); **opaque-cookie vs JWT tradeoff** (revocability vs statelessness — why logout is hard with JWTs). L3: **concrete Apache access-log line** as the defender's view + the three concrete signals (401 bursts = credential stuffing; 404 sweeps = enumeration; 500 after strange input = read the error). |
| a-linux-cli | L1, L2, L3, L5 | L1: ring buffer (fixed-size log, oldest overwritten); init system (first process, PID 1); challenge-response mechanism (random challenge only the private key can answer); PPA (Ubuntu's per-developer package archives); maintainer scripts (preinst/postinst, run as root during install). L2: why umask default-denies (never world-readable by accident — relax deliberately); why root bypasses permission checks (checks protect users from each other, not root from the machine — hence root is the most dangerous account to operate as). L3: **concrete `/var/log/auth.log` lines** — failed-password and accepted-publickey shapes, and the spray-vs-brute-force distinction (many usernames vs one username). L5: added the reading tip that `sshd_config` documents every option in inline comments — read the file top to bottom once. |
| a-osint-research | L1, L2, L3 | L1: SPF (published list of authorized senders — anti-spoofing); Shodan (search engine indexing internet-connected devices and banners); chronolocation/geolocation/source-evaluation unpacked in the Bellingcat §7 entry. L2: **why "a name found is not permission"** (authorization is defined by permission, not difficulty — an unlocked door is still a door you weren't invited through). L3: defender's view of recon in web logs (`GET /robots.txt` → requests for exactly the disallowed paths → 404 run = someone weaponizing your robots.txt) and CT-log monitoring as the defender's mirror of subdomain enumeration. |
| a-python-security | L1, L2, L3 | L1: REPL (read-eval-print loop); the `if __name__ == "__main__"` guard explained as the entry-point idiom (runs only when executed directly, not on import). L2: why `sys.exit(1)` (nonzero exit = how scripts report failure to their callers). L3: defender's first greps on an unknown/suspicious script (`eval(`, `exec(`, `base64`, `os.system`, `subprocess`, hardcoded IPs — obfuscated blob + network calls = the malicious-script shape). L5 checked: §7 already names chapters and read/skim/skip for Tutorial, stdlib, and both books — no fire. |
| a-reading-code | L1, L2, L3 | L1: DOM (browser's live representation of the page); bundler (packages many source files into the browser's few — why production code looks nothing like the snippet); ORM (translates objects↔rows; SQL still generated underneath); middleware (request→handler shared plumbing); UNION (glues two queries' results — the smuggling keyword). L2: **why placeholders are airtight** (database parses once with `?` as holes, then binds values — no second parse for the attacker to influence). L3: **concrete SQLi probe in access logs** (`GET /search?q=%27%20OR%20%271%27%3D%271`) — the `'`, `UNION`, `--` token set is exactly what WAF rules alert on. |
| a-tcpip-ports | L1, L2, L3 | L1: pseudo-header (virtual, checksum-only, never transmitted); banner-grabbing (read the service's self-identifying greeting); RST injection spelled out. L2: **SYN flood as handshake-statefulness weaponized** (one SYN forces server-side state — the attack the design enables); why UDP skips the handshake (three extra packets would triple a one-question cost); why NAT exists (IPv4 exhaustion — whole network shares one public address). L3: scan signature from the target's side (SYN-RECV pile-up, SYNs marching across sequential ports, many SYNs / few ESTABLISHED — the ratio IDS alerts are built on). |
| a-windows-concepts | L1, L2, L3 | L1: hive (top-level key backed by a file on disk); cmdlet (pronounced "command-let"); `$_` (current object in the pipe); **logon types** 2/3/10 (the field turning a 4624 from noise into signal — codes verified in-session against Microsoft's logon-types reference, staged source row); Group Policy (centrally-pushed settings outranking local ones); SID (in check question 1). L2: why the registry is centralized (one API, crash-safe writes, per-key permissions — price: one corrupt database kills the machine, hence no casual undo); why execution policy exists (stops *accidents*, not *adversaries* — the reason Microsoft is honest it isn't a boundary). L3: brute-force vs spray read on 4625s (one username hammered vs many usernames — the username spread is the whole distinction). |

## Counts

- Lessons audited: 10 · lessons edited: 10 (lens 1 fired on 10/10 — the highest-value lens, as predicted).
- Lens fire counts: L1 10/10 · L2 9/10 (not a-python-security in any substantial way — it was already why-complete) · L3 10/10 · L4 1/10 (a-crypto salt step only) · L5 1/10 (a-linux-cli sshd_config tip only).
- New walkthrough steps run: 1 (a-crypto §4 step 8; transcript appended to `runs/a-crypto.log`, scratch dir deleted).
- Source rows staged: `reports/sources-add-2-A.csv`, 2 rows, both status=verified, both fetched in-session 2026-10-10. NOT merged into `sources.csv` (parent merges).
- Levels: unchanged on all 10 (additions are definitions/rationale/signals at the lessons' existing levels — no level raised).
- Frontmatter: untouched on all 10.

## Verification

- All 10 lessons: exactly ten `^## ` sections; `lesson_id:` frontmatter line present in all 10.
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`): zero hits in all 10 files.
- Currency: no `$<digit>` in new copy (only pre-existing awk `$7` field reference in a-linux-cli §4).
- `python3 guidebook/build_site.py` from `~/workspace/learncomputerstuff`: completed with zero errors; level badge renders (spot-checked `g/crypto/index.html` — "Level 2 · Operate").
- pgrep: no stray test servers (no server.js, no python http servers; earlier transient self-match confirmed as the pgrep command line itself).
- No commits, no pushes. Untouched: build_site.py, STATE.md, gaps.md, map.md, sources.csv, runs/ (except the a-crypto.log append), other stages' files.

## Gaps / things I did not close

- **a-http-depth §10 still cites legacy IDs** (`B-VULN-01` through `B-VULN-16`, `B-DEF`) that don't match the `b-*` slug scheme. Left untouched per the coordinator flag from the DEa batch (normalize centrally; per-lesson edits would race other workers). Same class of issue as the E-GOV-01 etc. flag.
- **a-osint-research and a-reading-code §7 still carry "lead, verify at build time" resource rows** (OSINT Framework, Bellingcat, Tracelabs, SQLite ref). Flagged by pass 1 for the build-time verifier; not a depth gap — left for the pre-publish re-fetch pass, per pass 1's decision.
- **Two intentional worked-example non-duplications**: a-dns-depth's end-to-end resolution walk and a-crypto's OpenSSL runs were left alone per the task's do-not-duplicate rule; a-crypto's new salt step extends, not duplicates.
- Definitions of standard terms (salt, IV, MAC, DOM, ORM, etc.) were written from established technical knowledge and grounded in each lesson's existing primary sources (RFCs, vendor docs); per the task, only the two *new factual claims that required verification* (BIND log format, logon-type codes) got fetched source rows.

## Decisions I made

- Lens 1 (unpack terms) fired on every lesson — mostly one-liner parentheticals/clauses placed exactly where each term is first needed, per the brief's "define each term where it is first needed, by what it does."
- Lens 5 fired almost nowhere: pass 1's deepening had already given a-linux-cli and a-windows-concepts strong read-guidance §7s, and most Stage A §7s already name sections and read/skim/skip. I did not manufacture guidance where the existing text was already good.
- No new resources added to any §7 (≤3 rule preserved); no new §10 entries except where a cross-reference already existed.


======================================================================
# Stage B
======================================================================

# Content-depth audit 2 — Stage B batch, sharper lenses (2026-10-10)

Auditor: subagent (depth-2 pass) · 2026-10-10. Dino's order: "try again" — the first pass (DEPTH-AUDIT.md Stage B: 20 SOLID / 1 deepened) was too lenient. This pass applied the five sharper lenses to all 21 Stage B lessons and edited every lesson where a lens genuinely fired.

Bar: brief SECURITY_GUIDEBOOK_BRIEF-2.md §1 (no term the reader can't unpack; define each term where first needed, by what it does), §6 (ten sections, in order), §7 (no hype words, free-only, ≤3 resources, attack+detect+fix together).

## Lens-fire summary

| Lesson | L1 jargon | L2 why | L3 detection | L4 worked-ex | L5 §7 | Notes |
|---|---|---|---|---|---|---|
| b-api-abuse | ORM, DTO, principal, algorithmic-complexity DoS | why authz must be data-driven (URL is a lookup key, never a decision) | concrete BOLA access-log lines | — | — | |
| b-authorization-scope | VDP | — | N/A (gating lesson, no attack) | — | — | |
| b-bug-bounty | CFAA, kudos points | why first-reporter-wins (novelty = new risk information) | N/A (process lesson) | — | — | |
| b-business-logic | fuzzing, dual-use endpoints | why the map comes first (can't violate an unnamed assumption) | — (already concrete: reconciliation rules) | — | — | dual-use def moved to the resource that names it |
| b-command-injection | metacharacter (by-function), sink | why no-shell argv defeats injection (no parse phase exists) | — (already concrete: Sysmon E1, parent-child) | — | — | |
| b-csrf | constant-time comparison, HMAC, method override | why the SOP is asymmetric (reading blocked, sending allowed) | concrete rejected-CSRF application-log line | — | — | |
| b-deserialization | classpath, SAST, HMAC | why the parser's instruction set is the attack surface | concrete cookie-size-anomaly log | — | — | |
| b-graphql | resolver, principal, persisted queries | — (rationale covered) | concrete `__schema` query-log line | — | — | |
| b-idor | tenant, bearer token | why the check belongs at the data-access layer | concrete IDOR-probing access-log lines | — | — | |
| b-jwt-oauth | base64url, JOSE, JWKS, PKCE, IdP, BCP | why the code flow exists (browser is an untrusted channel) | concrete decoded `alg=none` header | — | — | |
| b-methodology | certificate transparency logs | — | N/A (planning lesson) | — | — | |
| b-practice-targets | ephemeral, network namespace | why the app must bind 0.0.0.0 *inside* the container | N/A (setup lesson) | — | — | |
| b-race-conditions | atomic, invariant, compare-and-set, isolation levels | why the DB is the arbiter (only place with a total order) | concrete same-millisecond redemption log | — | — | |
| b-security-headers | MIME, execution context, `__Host-` prefix | why browsers sniff (compat history) | concrete CSP violation-report JSON | — | — | |
| b-session-auth | TOTP, breach-password screening, entropy | why possession beats knowledge as a factor | concrete auth-log excerpt (fixation + 20×401) | — | — | |
| b-sqli | sink, WAF, bind variable | why prepared statements win at the protocol level (parse once, never re-parse) | — (already concrete: CRS 942xxx, slow-query) | — | — | |
| b-ssrf | link-local, IAM, canonicalized, OAST | why IMDSv2's PUT requirement stops simple SSRF | concrete egress-log lines to 169.254.169.254 | — | — | |
| b-ssti | object model, autoescape | why the compile/render phase split is the guarantee | concrete URL-decoded probe log line | — | — | |
| b-toolbench | wordlist, interactsh, recursion, kudos | why manual runs precede automation (calibration before amplification) | N/A (tools lesson) | — | — | kudos def already present in b-bug-bounty; not duplicated |
| b-xss | execution context, trust boundary, sink | why `textContent` is safe (no HTML parser invoked) | — (already concrete: log patterns + CSP report) | — | — | |
| b-xxe | SAML, DTD, DOCTYPE, canary file | why external entities were a default (trusted-document design) | concrete DOCTYPE request-body excerpt | — | — | |

Lens 1 fired on 21/21. Lens 2 fired on 19/21 (b-graphql, b-methodology: rationale already complete — recorded, not padded). Lens 3 fired on 12/15 applicable lessons (b-sqli, b-command-injection, b-xss, b-business-logic already carried concrete defender signals; the three N/A lessons are non-attack lessons). Lens 4 fired on 0/21 — every lesson's §3 already carries its own worked mechanism example (verified, not assumed). Lens 5 fired on 0/21 — every §7 already gives read-order guidance ("read §4; note…; skim…").

## What was added, per lesson (exact)

- **b-api-abuse** (§3): by-function definitions for ORM, DTO (data transfer object), principal, algorithmic-complexity DoS; a "why it arises"-level rationale that the URL is a lookup key and ownership must be re-derived from the database on every request; a three-line access-log excerpt showing BOLA probing (one session, sequential IDs, all 200) with the "ID spread is the signal" reading.
- **b-authorization-scope** (§6): VDP defined where first needed (standing-offer structure, safe harbor, no payout).
- **b-bug-bounty** (§3): CFAA expanded at first use; the first-reporter-wins rationale (novelty = new risk information); (§7) kudos points defined.
- **b-business-logic** (§3): the map-first rationale (can't violate an unnamed assumption); fuzzing defined by function; (§7) dual-use endpoints defined in the resource that names the term.
- **b-command-injection** (§3): metacharacter defined by what it does; the no-shell/argv rationale (no parsing phase exists — the shell was the parser); (§6) sink defined.
- **b-csrf** (§3): HMAC, constant-time comparison, method override defined by function; the SOP-asymmetry rationale (reading blocked for confidentiality, sending allowed for the web's machinery — CSRF lives in that gap); a rejected-CSRF application-log line (event logged, token value never logged).
- **b-deserialization** (§3): classpath, SAST, HMAC defined by function; the parser-as-interpreter rationale (instruction set = attack surface; you change the interpreter, not the blocklist); a cookie-size-anomaly log (48/48/312 bytes).
- **b-graphql** (§3): resolver and principal defined by function; a query-log line showing the `__schema` tripwire; (§9) persisted queries defined.
- **b-idor** (§3): tenant and bearer token defined by function (bearer token cites RFC 6750); the data-access-layer rationale (one choke point can't be forgotten); a three-line access-log excerpt of IDOR probing with the spread-is-the-signal reading.
- **b-jwt-oauth** (§2): base64url defined (RFC 4648 §5); (§3) JWKS defined (RFC 7517), the code-flow rationale (browser is an untrusted channel — code is worthless without the client secret); the decoded `{"alg": "none"}` header as the defender's one-line signal; (§7) JOSE and BCP (BCP 225) defined; (§9) PKCE and IdP defined.
- **b-methodology** (§4): certificate transparency logs defined by function (RFC 6962).
- **b-practice-targets** (§3): ephemeral and network namespace defined; the container-bind rationale (container localhost ≠ host localhost — the app listens on all interfaces of its private network; `-p` decides which host interfaces may knock).
- **b-race-conditions** (§3): atomic, invariant defined by function; the same-millisecond redemption log with the -1; compare-and-set defined; the database-as-arbiter rationale (only place with a total order); (§9) isolation levels defined.
- **b-security-headers** (§3): MIME defined; the sniffing-compat-history rationale; a CSP violation-report JSON naming document-uri/violated-directive/blocked-uri; execution context defined in the verification habit; (§6) `__Host-` prefix defined (Secure + host-only + Path=/, per the cookie draft §5.7).
- **b-session-auth** (§3): TOTP expanded and defined (RFC 6238, 30-second step); breach-password screening defined (NIST SP 800-63B); the possession-vs-knowledge rationale; (§4) a concrete auth-log excerpt (20×401s + the fixation line) and entropy defined.
- **b-sqli** (§1): WAF expanded; (§3) bind variable defined; the prepared-statement protocol rationale (query and values travel separately; values are never parsed); (§4) sink defined.
- **b-ssrf** (§3): link-local and IAM defined; the IMDSv2 PUT rationale (simplest fetchers only do GETs — the method requirement is the barrier); canonicalized defined; a two-line egress log to 169.254.169.254; (§5) OAST expanded.
- **b-ssti** (§3): object model and autoescape defined; the compile/render phase-split rationale; a URL-decoded `{{7*7}}` access-log line.
- **b-toolbench** (§3): phase-4 manual-before-automation rationale (calibration before amplification); wordlist and interactsh defined; (§7) recursion defined.
- **b-xss** (§1): trust boundary defined; (§3) execution context defined; the `textContent` rationale (no HTML parser invoked); (§4) sink defined.
- **b-xxe** (§1): SAML expanded; (§3) the trusted-document-design rationale for external-entity defaults; DTD defined; a DOCTYPE request-body excerpt; the DOCTYPE defined in the worked example; (§6) canary file defined.

## Source rows staged

`reports/sources-add-2-B.csv` — 10 rows, all status=verified, all fetched in-session 2026-10-10: RFC 6238 (TOTP), RFC 7636 (PKCE), RFC 7517 (JWKS), RFC 4648 §5 (base64url), RFC 6750 (bearer token), RFC 6962 (certificate transparency), RFC 8725 (BCP 225), draft-ietf-httpbis-rfc6265bis-22 §5.7 (`__Host-` rules; expires 4 June 2026), AWS IMDSv2 docs (PUT-issued session token), SP 800-63B-4 landing page (July 2025 edition confirmed). Purely definitional one-liners (ORM, sink, principal, etc.) carry no rows — they are standard vocabulary explained by function, not external factual claims. The parent merges this file into sources.csv.

## Verification (2026-10-10)

- All 21 lessons: exactly 10 `## ` sections each (grep-checked); `lesson_id:` frontmatter line present in all 21; frontmatter structure untouched.
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`): zero hits in new copy — and zero across all 21 files (they were already clean).
- Currency symbols: no `$<digit>` added (only pre-existing awk-style references, none new).
- `python3 guidebook/build_site.py` from ~/workspace/learncomputerstuff: completed with zero errors.
- Test servers: none started by this audit (no new walkthrough steps were added — all additions are §3/§6/§7/§9 prose and illustrative log examples; per the ratified substitution policy, illustrative examples are marked as examples, not run transcripts). `pgrep` shows no stray demo processes.
- Levels: none raised. No new walkthrough steps, no new resources (≤3/resource rule undisturbed), no commits, no push. build_site.py, STATE.md, gaps.md, map.md untouched; no other stage's files touched.

## Decisions

- Illustrative log lines are presented as teaching examples ("looks like this"), not as run transcripts — they teach the defender's reading of telemetry, and the walkthroughs' real transcripts in runs/ are untouched.
- Lens 2 and lens 3 were recorded as no-fire where the lesson already carried the rationale or the concrete signal — padding a strong lesson to make a lens fire would have weakened it.
- b-graphql got no lens-2 addition: its design rationale (spec assumes trusted context; resolvers lack a global cost view) is already the lesson's spine.
- No factual claim was added without an in-session primary-source fetch where a standard backs it; the CSV above is the evidence.

## What this pass did not do

- No re-verdict of the first pass's SOLID calls — different lenses, as ordered.
- The two cross-batch link notes from the first pass (legacy lesson-ID scheme in "Leads to"; deferred "re-fetch at build time" links) are coordinator-owned and were not touched.


======================================================================
# Stage C
======================================================================

# Depth audit 2 — Stage C batch (stricter lenses)

Auditor: subagent 2e7885c9 · 2026-10-10 ~01:20–02:00 EDT.
Standard: brief §1 (the bar: "explain each mechanism from first principles, with no term
they can't unpack"; "Define each term where it is first needed, by what it does"),
§6 (ten ## sections in order), §7 (free-only, ≤3 resources, no hype).
Method: all 10 lessons re-read end to end against the FIVE new lenses. The first pass
(DEPTH-AUDIT.md, 10/10 SOLID) used different lenses and was deliberately not re-run.

Verdict: **all 10 lessons deepened.** Lenses fired 38 times total. No level changes
(levels were honest and stay). No lesson needed padding; every addition below is a
lens finding with a specific location.

## Per-lesson lens table

| Lesson | Lens 1 (jargon) | Lens 2 (why) | Lens 3 (detection) | Lens 4 (worked ex.) | Lens 5 (§7 quality) |
|---|---|---|---|---|---|
| c-cvd | embargo, adoption wait, zero-day | embargo trade + deadline rationale | — | already had | already guided |
| c-cve-program | BCP 47 | independently-fixable rule; private-first reservation | — | already had | skip-guidance added |
| c-cvss | MacroVector/equivalence class; Modified Base metrics | exploitability/impact split; why v4.0 dropped equations | — | already had (left alone) | reading-order strengthened |
| c-vuln-ecosystem | Binding Operational Directive; CPE | why the CNA record became the default | — | already had (left alone) | EPSS reading order; OIG skip guidance |
| c-incident-response | Community Profile; IOC; sinkhole; DGA; playbook; Run key | why comms order is risk management | spray-shape alert made concrete | already had | filler §7 item REPLACED (SANS Dynamic Incident Response, verified free CC BY 4.0); Velociraptor guidance |
| c-log-sources | telemetry; SIEM; C2; 5-tuple; XDR | why timing/volume survive encryption; why 4688 command lines default off | already concrete | already had | ATT&CK skip guidance |
| c-soc-triage | SIEM; threat intel; IOC; Tier 2 | why triage recommends-not-acts; why uncertainty escalates | MFA-denied burst as the concrete corroborating signal | already had | filler §7 item REPLACED (MITRE 11 Strategies, verified free) |
| c-sigma-detection | backend; pySigma; soak period | why a shared format exists; why tuning order is filters→thresholds→narrowing | — (the whole lesson is detection) | **NEW §4 step 9: real `sigma convert` run on loopback** | filler §7 item REPLACED (Sigma CLI, verified) |
| c-ai-tooling | red teaming vs pentesting; malware RE | why Red Team Access is orgs-only; why real-time blocks persist at Red Team | — | already had | already guided |
| c-public-track-record | primitive; triager; 0-day | why the 90-day deadline exists (embargo mechanism) | — | already had | already guided |

## What was added, per lesson (specific)

- **c-cvd** (§3): "Why the embargo exists — and whose interests it serves" paragraph
  (three-way trade: vendor time / deployer patch-ready / finder-and-user cost; deadline
  converts "trust us" into commitment). By-function definitions: **embargo**, **adoption
  wait** (the extra month after the patch before details publish), **zero-day**.
- **c-cve-program** (§3): "Why the rule is 'independently fixable'" (one ID per fixable
  unit — keeps the catalog aligned with the work of fixing); "private-first ordering is
  load-bearing" (a public reservation for an unpatched flaw is a pointer attackers can
  read). **BCP 47** defined (language tags `en`/`en-US`). (§7): skip-guidance on the
  cve.org Services page (skip API reference) and the schema repo (skip ADP on first pass).
- **c-cvss** (§3): equivalence class defined by function (grouping lets 15M+ vectors
  share 101 scores); "Why v4.0 abandoned the equations" (v3.x algebra vs expert ranking,
  per FIRST FAQ §3.17 — math serves judgment instead of overriding it); "Why the split"
  (exploitability = the flaw, vendor knows best; impact = the consequence, consumer
  knows best; one blended number would force the consumer to accept the vendor's
  judgment about their own losses); Modified Base metrics one-liner. (§7): read the
  Examples doc *before* the Specification; skim MacroVector math and run the reference
  implementation; skip version-history appendices; v3.1 Temporal/Environmental skip note.
- **c-vuln-ecosystem** (§3): **BOD** defined (mandatory CISA order to federal civilian
  agencies); **CPE** defined (NIST structured product naming); "Why the CNA record
  became the default" (OIG: 60,000/year projected, tenfold decade growth, NIST "no
  sustainable processes" — the default is what scales, not the best analysis). (§7):
  EPSS reading order (Why EPSS? → Using EPSS → How It Works; skip Research); OIG
  reading guidance (Report Highlights → Finding 2; skip appendices).
- **c-incident-response** (§3): **Community Profile**, **IOC**, **playbook**, **sinkhole**,
  **DGA**, **Run key** all defined by function; "the order is risk management, not
  politeness" (legal/regulatory exposure, tipping the adversary). Worked example:
  recommendation (2) now names the concrete spray-shape signal (multiple 4625s, one IP,
  ≥3 users, short window). (§7): filler item 1 ("SANS IR-related reading via free
  summaries") **replaced** with SANS *Dynamic Incident Response* (sans.org, verified
  free CC BY 4.0, no login) + read-first guidance; Velociraptor guidance added
  (Quickstart → Artifact Reference; skip VQL Reference on first pass).
- **c-log-sources** (§2/§3): **telemetry**, **SIEM**, **C2**, **5-tuple**, **XDR** defined
  by function where first needed. "Encryption hides the content, not the envelope"
  (packet sizes/send times visible — the rhythm is the signal). 4688: why command lines
  default off (Microsoft ships it Not Configured — every-process logging costs volume;
  lines land in plain text readable by anyone with log access). (§7): ATT&CK — read
  tactic pages as a map, skip technique pages on first pass.
- **c-soc-triage** (§1/§3): **SIEM**, **threat intel**, **IOC**, **Tier 2** defined by
  function. "The split is deliberate" (triage recommends; containment needs scoping,
  carries evidence/legal risk, needs authority). "The rule is asymmetric cost" (a missed
  compromise on a DC costs more than a hundred wasted escalations). Worked example
  step 7: the concrete corroborating signal (burst of "MFA denied" results after the
  travel-violating sign-in). (§7): filler item 1 ("references in sources.csv")
  **replaced** with MITRE *11 Strategies of a World-Class SOC* (mitre.org, verified free
  download, 20-page summary + full book) + read-first guidance.
- **c-sigma-detection** (§3): **backend**, **pySigma**, **soak period** defined;
  "Why a shared format exists at all" (every SIEM its own language — logic once,
  translation mechanical); "The order is load-bearing" (filters remove known-benign;
  thresholds trade TPs; narrowing is blindness wearing a tuning costume). (§4): **new
  step 9 — real backend conversion run on loopback** (sigma-cli 3.1.0, pySigma 1.5.1,
  pysigma-backend-splunk 2.1.0, pysigma-pipeline-sysmon 2.0.0, Python 3.12.3,
  2026-10-10): `sigma convert -t splunk -p sysmon encoded_ps_rule.yml` →
  `EventID=1 Image="*\\powershell.exe" CommandLine IN ("* -enc *", "* -EncodedCommand *")`
  (exit 0; transcript appended to `runs/c-sigma-detection.log`). The harness still
  stands in for corpus evaluation — the lesson says so. (§7): filler item 2
  ("references in sources.csv") **replaced** with Sigma CLI (github.com/SigmaHQ/sigma-cli,
  verified) + Usage reading guidance.
- **c-ai-tooling** (§3): red teaming vs pentesting distinguished (adversary emulation
  vs bounded assessment); malware RE defined (analysis, not reuse); why Red Team
  Access is organizations-only (accountability — a legal entity with contracts and
  someone to answer for misuse; authorization runs through organizations anyway);
  why real-time blocks persist at Red Team (those actions have no legitimate testing
  use case at any trust level — trust changes *which* work is allowed, not *whether*
  physics matters).
- **c-public-track-record** (§3): **primitive** defined (the basic capability the
  exploit is built from); **triager** defined; the 90-day deadline explained as the
  embargo mechanism (without a date, "responsible" becomes indefinite delay). (§6):
  **0-day** defined (a claim about the vendor's state, not the finding's severity).

## Lens-1 inventory (the highest-value lens, per the brief)

Terms the lessons USED but never DEFINED, now defined by function where first needed:
embargo, adoption wait, zero-day/0-day, BCP 47, MacroVector/equivalence class, Modified
Base metrics, Binding Operational Directive, CPE, CSF 2.0 Community Profile, IOC,
playbook, sinkhole, DGA, Run key, telemetry, SIEM, C2, 5-tuple, XDR, threat intel,
Tier 2, backend, pySigma, soak period, red teaming (vs pentesting), malware reverse
engineering, primitive, triager. That is 28 unpacked terms across 10 lessons.

## Sources staged

`guidebook/reports/sources-add-2-C.csv` — 12 rows, all status=verified, all fetched
in-session 2026-10-10 (in the repo, not /tmp; parent merges into sources.csv):
FIRST CVSS v4.0 FAQ (expert ranking/equivalency sets); MicrosoftDocs command-line
process auditing (default Not Configured; plain-text note); NIST NVD CPE page;
RFC Editor BCP 47; Commerce OIG OIG-26-020-I PDF (60,000/year, tenfold, "no
sustainable processes"); NIST CSF page (profiles); SANS Dynamic Incident Response
(free CC BY 4.0); MITRE 11 Strategies (free download); SigmaHQ sigma-cli README;
SigmaHQ sigma-specification README; FIRST EPSS page (section structure); Velociraptor
docs (section structure). Existing sources.csv checked first — no duplicates
(the OIG report row existed but not the fetched-PDF volume figures; the sigma-cli
and DAIR/11-Strategies URLs are new).

## Verification results

- All 10 lessons: exactly ten `^## ` sections; `^lesson_id:` present in each;
  frontmatter values untouched (no level changes).
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`): zero hits across all
  10 files. No currency symbols in new copy (the one `$[0-9]` hit is pre-existing
  `$3` awk field references in c-log-sources §4).
- Resource counts: replacements only — every lesson still ≤3 free resources in §7;
  the three §7 filler rows ("references in sources.csv" / "SANS IR-related reading
  via free summaries") are gone, replaced with verified free primaries.
- Runs: `runs/c-sigma-detection.log` appended with the real sigma-cli conversion
  (tool versions + 2026-10-10 UTC date + the honest proxy-workaround note). No new
  walkthrough steps were added to any other lesson, so no other runs were needed.
- `python3 guidebook/build_site.py` from ~/workspace/learncomputerstuff: completed,
  "done", exit 0, zero errors.
- pgrep clean; /tmp test artifacts (sigma venv, rule file, corpora) removed.
- Nothing committed, nothing pushed. build_site.py, STATE.md, gaps.md, map.md,
  sources.csv untouched. No other stage's files touched.

## Word counts

2359 / 2460 / 2228 / 2414 / 2681 / 2363 / 2153 / 2439 / 2380 / 2516 (c-incident-response
and c-vuln-ecosystem sit slightly above the 2,500-word sanity band; the band is
explicitly not a target and every word above it is a lens finding, not padding).

## What I couldn't close

1. **c-ai-tooling §7 item 1 (CVP primary URL gap)** — still open from pass 1. The
   announcement URL was not fetched this session either; the lesson's honest "gap,
   stated plainly" note stands. The tier facts were not re-verified (no new factual
   claims added to this lesson, so no re-verification was triggered). Candidate for
   the coordinator's pre-publish re-fetch pass, as pass 1 recommended.
2. **BOD one-liner row** — c-vuln-ecosystem's "Binding Operational Directive is a
   mandatory CISA order to federal civilian agencies" gloss rests on the lesson's
   existing BOD-26-04 context (ledger-backed by the DEb batch: BOD 26-04 issuance
   and KEV-remediation content verified). The cisa.gov BOD page returned HTTP 403 to
   the text fetcher, so no new primary row was staged for the gloss itself; I did
   not invent one. If the parent wants a dedicated row, the BOD 26-04 directive text
   needs a fetch that clears the bot wall.
3. **Community Profile definition sourcing** — the one-liner's substance follows
   NIST CSWP 29's glossary (quoted via a search snippet, not fetched in-session);
   the staged row cites nist.gov/cyberframework (fetched: confirms CSF 2.0 Profiles
   exist as templates/resources). The staged claim is limited to what was fetched.
4. **Lens 3 on c-cvd / c-cve-program / c-cvss / c-public-track-record** — genuinely
   not applicable (disclosure mechanics, record formats, scoring math, and writing
   are not detection lessons; forcing "concrete signals" into them would be padding).
   Lens 4 on c-cvss and c-vuln-ecosystem — did not fire per the task's explicit
   instruction to leave the hand-scoring and three-way ranking alone; both already
   carry full worked examples.


======================================================================
# Stage D + E first half
======================================================================

# Depth audit, second pass (stricter) — Stage D + E first half (DEa), 2026-10-10

Auditor: subagent session 9bf3530c. All 34 lessons re-read in full against the five sharper lenses
from the dispatch brief. The first audit (DEPTH-AUDIT.md, "Stage D + E (a)") found 34/34 SOLID with
only 4 small corrections; this pass applies DIFFERENT lenses and does not re-run those verdicts.

Lens key: **L1** unpacked jargon · **L2** missing "why" · **L3** detection gaps ·
**L4** worked-example gaps · **L5** "read the source" quality.
A lens is listed only where it fired and produced an addition. L4 fired on none —
every lesson already carries its worked case or demo (per the task, existing worked
examples were not duplicated).

## Per-lesson table

| Lesson | Lenses fired | What was added (specific) |
|---|---|---|
| d-appsec | L1, L2, L5 | L1: "abuse cases" (misuse scenarios written as requirements), "trust boundary" (defined by function), "pre-commit hooks", "security champions". L2: why STRIDE has six categories — each threatens a different security property, making enumeration systematic not brainstorm. L5: ASVS skip guidance (skip requirement text on first pass; open the catalog when writing requirements). |
| d-cloud-security | L1, L2, L3, L5 | L1: "posture" (core term of the lesson, never defined), management plane vs data plane, "origin access identity". L2: why the shared-responsibility line sits where it does — provider owns what it can see/change; cannot patch your guest OS without violating the isolation it promises. L3: concrete trail-kill event names worth memorizing — `StopLogging`, `DeleteTrail`, `PutEventSelectors` (the quiet one) — as the alert set (verified against AWS API Reference + Stratus technique map). L5: skip guidance on the AWS shared-responsibility page (compliance-artifact links first pass). |
| d-dfir-deep | L1, L2 | L1: "DGA" (domain generation algorithm), "chain of custody" (d-dfir is a prerequisite of e-investigation-forensics — the lesson depends on the term, so a cross-ref was not enough), "HTB Sherlocks". L2: why the acquisition hash anchors chain of custody — alteration changes the hash, so a verified hash proves the analyzed copy is the collected copy. L3/L5: already strong (§6 failure modes concrete; §7 has read+skip guidance). |
| d-exploit-concepts | L1, L2, L3 | L1: "belt progression", "GEF/pwndbg" (gdb plugins), "cross-references". L2: why static-first before dynamic — static gives the whole map cheaply; dynamic only shows executed paths, so you confirm rather than explore. L3: new paragraph "What the defender sees when a mitigation fires" — tripped canary logs `*** stack smashing detected ***` (verified locally 2026-10-10, transcript `runs/dea-canary-abort.log`, exit 134/SIGABRT), NX violation dies as segfault at a non-executable address; either is an active-exploitation-or-bug signal for the timeline treatment. |
| d-malware-analysis | L1, L2 | L1: "PDB paths" (compiler's Program Database — build-machine path), "mutex" (named lock; distinctive malware mutex names become detection strings), "INetSim" (fake-internet server for the lab). L2: why entropy is a 0–8 scale — a byte has 256 values, log₂(256)=8, so max entropy = encrypted/compressed-looking data. |
| d-redteam-concepts | L1, L5 | L1: "JA3/JA4" (handshake fingerprinting — hashes the Client Hello's cipher list/extensions/parameters; verified against the salesforce/ja3 repo), "DGA", "fast-flux" (rapidly rotating DNS answers), "NTP". L5: skip guidance for the ATT&CK C2 page (mitigations appendix on first pass; return when writing detections). L2/L3: already strong (stealth-vs-reliability, technique-vs-procedure, §3 "What defenders see" is concrete telemetry). |
| e-arch-vuln-assessment | L1 | L1: "confused deputy" (privileged program tricked into misusing its own authority — with a webhook example), "complete mediation" (every access to every object checked every time — the lesson depends on the concept via the service-to-service finding). L2/L3/L5: already strong (structural-persistence rationale, §6 observable failures, §7 read/skim guidance). |
| e-assessment-strategy | L1 | L1: "crown jewels" (systems whose loss ends the business), "audit committee" (board subcommittee overseeing audit and risk). L2/L3/L5: already strong (policy-first rationale, §6 observable failures like "same findings return next year", excellent §7). |
| e-asset-classification | L1, L2 | L1: "remanence" (used undefined in §10), "breach-notification" (the legal requirement; bigger collection = bigger notification and fine). L2: why name the role not the person as owner — people leave, roles persist, the scheme must survive both. |
| e-asset-provisioning | L1, L2 | L1: "ITSM" (IT service management — the ticketing/workflow system), "merge-gate" (check that blocks deployment until it passes). L2: why the CMDB record is created *before* deployment — anything existing even briefly unrecorded can be forgotten, which is the inventory's whole failure mode. |
| e-auth-systems | L1, L3, L5 | L1: "TOTP", "SIM-swap" (attacker moves the victim's number to their SIM; codes follow the number), "SAML"/"OIDC" (expansions), "IdP" (introduced at first use), "relying party", "break-glass". L3: concrete observable for the "passwordless declared, fallback forgotten" failure — authentication logs showing the fallback path used by a passkey-enrolled account; one event is an anomaly, a pattern is exploitation. L5: skip guidance for SP 800-63B federation message formats on first pass. |
| e-awareness-training | L1, L5 | L1: "business email compromise" (BEC), "whaling" (phishing aimed at executives), "acceptable-use policy". L5: strengthened §7 to verified structure — read the CPLP life-cycle framing first, then the metrics/evaluation-methods guidance (backs the lesson's effectiveness-vs-activity split), skim federal-workforce detail. (An earlier draft claimed "templates and role-mapping appendices" — unverified; replaced after fetching the CSRC page.) |
| e-bcp-drp | L1 | L1: "runbook" (step-by-step written procedure), "injects" (pre-planned exercise events that force decisions), "incident commander" (the one person owning the incident's decisions), "smoke test" (quickest check the system basically works). L2/L3/L5: already strong (BIA-first rationale is the brief's own example; §6 concrete; §7 read/skim/age-honesty). L4: excluded by task (BIA worked case left alone). |
| e-board-communication | L1, L2, L3 | L1: "KPI"/"KRI" (effort vs exposure — the lesson depends on the distinction for the anti-single-score argument), "maturity model" (staged capability scale), "residual risk" (risk remaining after controls — the memo's core "accept" decision). L2: why the CSF 2.0 translation rule exists — the board holds risk-acceptance authority and can only accept what it understands in its own terms; an un-understood risk is a risk nobody accepted. L3: observable symptom of failed board communication — a board that never asks a follow-up question; questions mean the memo landed. |
| e-change-management | L1 | L1: "maintenance window" (scheduled period when changes are allowed), "KEV" (CISA's Known Exploited Vulnerabilities catalog), "canary" (deploy to a small subset first), "quorum" (minimum attendance for a valid decision). L2/L3: already strong (emergency-path retrospective rationale; §6 observable signals like "a review with no rejections didn't happen"). |
| e-config-management | L1 | L1: "status accounting" (recording/reporting each configuration item's current state), "landing zone" (pre-configured cloud environment new workloads deploy into), "EDR" (endpoint detection and response) — added as a new baseline-table row (audit-logging row preserved). L2/L3/L5: already strong. |
| e-control-selection | L1 | L1: "control" — the brief's own lens-1 example: the lesson used "control" as core vocabulary without ever saying what one is (a safeguard — administrative, technical, or physical measure implementing a requirement); "residual risk" (risk remaining after controls — the authorization-signing concept). L2/L3/L5: already strong. |
| e-control-testing | L1 | L1: "backport" (security fix applied to an older version without changing the version number — why version banners lie). This lesson already defines "control" properly. L2/L3/L5: already strong (cheap-before-expensive rationale; "what a pass proves and doesn't prove" throughout). |
| e-cryptanalysis | L1, L2 | L1: "rounds" (one iteration of the cipher's core transformation — AES-128 runs 10), "blinding/masking" (randomizing the computation so measurements don't correlate with the secret), "MAC" (message authentication code — keyed checksum), "work factor" (the slow hash's tunable cost parameter). L2: why the birthday bound is a square root — collisions come from pairs; 2^32 inputs make ~2^63 pairs, so the work halves the defender's margin. L4: excluded by task (demos left alone). |
| e-crypto-applied | L1 | L1: "IV" (initialization vector), "MAC", "trust store" (OS/browser's built-in root-CA list), "salt" (random data per password hash), "key schedule" (handshake key-derivation steps), "ephemeral" (fresh per connection, discarded after — with the forward-secrecy consequence). L2/L3/L5: already strong (ECB demo is the why; §6 misuses concrete; §7 has read/skim/skip). |
| e-csf-20 | L1, L2 | L1: "risk committee" (board subcommittee overseeing risk). L2: why Govern sits at the center — a strategy failure cascades into every other function (unfunded Identify, unstaffed Detect, untested Recover), so the framework puts what breaks everything else where it can't be skipped. |
| e-cyber-law | L1 | L1: "controller" vs "processor" (the distinction the entire GDPR section hinges on — defined at first use), "supervisory authority" (the country's data-protection regulator), "data subject" (the person the data is about), "adequacy decision" (EU ruling a country protects data well enough), "derogation" (specific legal exception allowing a transfer), "special-category data" (sensitive data with extra protections). L2/L3/L5: already strong. |
| e-data-lifecycle | L1, L2 | L1: "wear-leveling" (SSD controller spreading writes — moves data into host-invisible cells), "overprovisioning" (hidden spare capacity the overwrite can't reach), "slack space" (unused tail of the last allocated block), "legal hold" (order to preserve data — suspends all destruction). L2: why the legal hold gates destruction — deleting under a hold is spoliation, punished independently of the underlying case. |
| e-data-protection-controls | L1, L2 | L1: "HSM" (tamper-resistant key-holding device), "KMS" (cloud key store), "FIPS-validated" (passed NIST's testing program), "tokenization" (random tokens mapping back only inside a vault), "masking" (`****-1234`), "memory hygiene" (clearing sensitive values from memory promptly). L2: why in-use is the hardest state — data must be decrypted to be processed, so plaintext in memory is unavoidable and protection is about shrinking reach, not eliminating it. |
| e-detective-preventive | L1 | L1: "control" (same brief-example gap as e-control-selection — defined at §3 opening), "XDR"/"NDR" (rebranding terms), "MDR" (managed detection and response — outsourced SOC), "CI/CD" (the build-and-ship pipeline). L2/L3/L5: already strong (cost-of-being-wrong type selection; §6 concrete; §7 read + age-honesty). |
| e-ethics | L1 | L1: "due diligence" (the buyer-side investigation before a deal — moved into the §1 dilemma setup where it's used), "attestation" (formal statement you stand behind as true), "whistleblowing" (reporting outside the chain when the chain is the problem). L2/L3/L5: already strong. |
| e-facility-controls | L1 | L1: "tailgating" (following an authorized person through a secured door), "mantrap" (two interlocking doors — first closes before second opens), "muster point" (designated post-evacuation assembly area for headcount). L2/L3/L5: already strong (life-safety-constraint rationale; §6 concrete; §7 read guidance). |
| e-facility-design | L1 | L1: "data residency" (legal requirement data stay inside a jurisdiction — a wrong-country site disqualifies the facility). L2/L3/L5: already strong (design-cheap/retrofit-ruinous; §6 concrete; §7 read guidance). |
| e-governance | L1 | L1: "tone at the top" (leadership's visible ethical commitment — what gets rewarded/punished), "ISMS" (information security management system). L2/L3/L5: already strong (reporting-line rationale; §6 "name the last risk decision" test; §7 read guidance). |
| e-handling-requirements | L1 | L1: "DLP" (used undefined — data loss prevention tooling watching for sensitive data leaving approved channels), "chain of custody" (same concept as the digital-evidence one, applied to physical media), "legal hold" (order to preserve — suspends the retention schedule; cross-consistent with e-data-lifecycle). |
| e-iam | L1, L2, L3 | L1: "CI/CD runners", "managed identities" (cloud-assigned workload identities — no stored credential), "SAML"/"OIDC" (expansions), "break-glass account", "IAL/AAL/FAL" (identity/authenticator/federation assurance levels — placed at the federation paragraph where §7's reading lands). L2: why assurance levels exist at all — uniform strong is too frictionful to survive, uniform weak leaves high-impact accounts exposed, so strength follows impact. L3: detective control for the standing-privilege finding — alert on privileged actions with no change ticket and no named task behind them. |
| e-incident-management | L1, L2 | L1: "CSIRT" (computer security incident response team — the formal name for the chartered team). L2: why the incident commander does *not* do technical work — command requires the full picture; a commander debugging loses the incident while winning the ticket. |
| e-investigation-forensics | L1 | L1: "admissibility" (allowed as evidence in a legal proceeding — stricter than "technically convincing"), "privilege" (attorney-client privilege), "spoliation" (destroying evidence you had a duty to preserve — courts punish it independently, assuming the destroyed evidence would have hurt you). L2/L3/L5: already strong. |
| e-investigations | L1 | L1: "work-product doctrine" (shields litigation-prepared materials from handover), "discoverable" (the other side can legally demand to see them). L2/L3/L5: already strong (type-stacking/interference rationale; §6 concrete; §7 read guidance). |

## Lens summary

- **L1 (unpacked jargon) fired on all 34 lessons** — as expected for the governance-heavy E track. Most additions are one-sentence or parenthetical by-function definitions at first use. Two lessons had the brief's exact example gap (a lesson using "control" without defining it: e-control-selection, e-detective-preventive — both now fixed).
- **L2 (missing "why") fired on 14 lessons** — only where the rationale was genuinely illuminating (STRIDE's six, the shared-responsibility line's position, static-first, Govern at the center, assurance levels, in-use hardness, the birthday square root, entropy's 0–8, the board translation rule, the IC's hands-off role, record-before-deployment, role-not-person ownership, legal-hold gating, chain-of-custody hashes).
- **L3 (detection gaps) fired on 5 lessons** — only where a concrete signal was missing: d-cloud-security (CloudTrail `StopLogging`/`DeleteTrail`/`PutEventSelectors` alert set), d-exploit-concepts (`*** stack smashing detected ***` as the active-exploitation signal, verified locally), e-auth-systems (passkey-enrolled account using the password fallback), e-board-communication (the silent board as the failed-communication signal), e-iam (privileged actions with no ticket). Most lessons already had concrete observable failure modes.
- **L4 fired on 0 lessons** — no abstract-without-example §3 sections found; duplicating existing worked cases was explicitly out of scope.
- **L5 (read-the-source quality) fired on 5 lessons** — d-appsec (ASVS skip), d-cloud-security (shared-responsibility page skip), d-redteam-concepts (ATT&CK mitigations-appendix skip), e-auth-systems (800-63B federation formats skip), e-awareness-training (strengthened to verified structure: CPLP life-cycle first, then metrics/evaluation guidance). e-board-communication's §7 was already adequate — no change. Most E lessons already had read/skim/skip guidance.

## Sources staged

`guidebook/reports/sources-add-2-DEa.csv` — 4 rows, all status=verified, all fetched or
executed in-session 2026-10-10:
1. AWS CloudTrail API Reference — StopLogging/DeleteTrail/PutEventSelectors actions.
2. salesforce/ja3 repo — JA3 definition (hashes Client Hello fields; 2017; JA4 successor).
3. NIST SP 800-50 Rev. 1 CSRC page — life-cycle CPLP guidance; metrics/evaluation methods.
4. Local execution — glibc canary abort message + exit 134 (transcript `guidebook/runs/dea-canary-abort.log`).

No other new factual claims were introduced: all other additions are functional
definitions, design rationales, or observables derived from the lessons' own content.
Checked against `guidebook/sources.csv` — no duplicates.

## Deliberately not added (anti-pad log)

- No worked examples duplicated (L4 never fired; e-cryptanalysis demos, e-config-management drift demo, e-bcp-drp BIA explicitly left alone per task).
- No level changes on any lesson — all additions are one-liners/paragraphs at the lesson's existing level.
- One self-caught correction: the first draft of e-awareness-training's §7 claimed "templates and role-mapping appendices" in SP 800-50 Rev. 1 — unverified; replaced with guidance grounded in the fetched CSRC page before finalizing.
- One content-preservation fix: an e-config-management edit initially replaced the audit-logging baseline row with the new EDR row — caught and corrected; both rows now present.

## Verification (pending — runs at the end)

- `python3 guidebook/build_site.py` from ~/workspace/learncomputerstuff: zero errors.
- Every edited lesson: exactly 10 `## ` sections; `lesson_id:` frontmatter present.
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`) and currency symbols in new copy: none.
- pgrep clean (no test servers started — only a local gcc crash demo; binary and sources in /tmp, transcript in guidebook/runs/).
- No commits, no pushes. build_site.py, STATE.md, gaps.md, map.md untouched.


======================================================================
# Stage E second half
======================================================================

# Depth audit 2 — Stage E second half (DEb), stricter lenses — 2026-10-10

Auditor: subagent (session 15d3327a) · 2026-10-10 ~01:20–02:30 EDT.
Scope: the 27 `e-*` lessons listed in the dispatch brief.
Method: every lesson re-read end to end against the FIVE lenses (not the first pass's pad-free verdicts). Every lens applied to every lesson. Additions are term definitions by function (lens 1), design-rationale sentences (lens 2), concrete observable failure signals (lens 3), and one §7 reading-guidance improvement (lens 5). Worked examples already present were left alone (lens 4 did not fire — every lesson has one; e-risk-assessment's register and e-test-analysis-reporting's two-layer report untouched per instructions).

Result: **all 27 lessons edited. Lens 1 fired on 27/27. Lens 2 on 23/27. Lens 3 on 27/27. Lens 4 on 0/27. Lens 5 on 1/27** (most §7 sections already carry read/skim/skip guidance; only e-soc2's was list-like).

## Per-lesson table

| Lesson | Lenses fired | What was added (specific) |
|---|---|---|
| e-iso27001 | 1, 2, 3 | L1: Plan-Do-Check-Act defined (plan/do/check/act cycle). L2: why SoA exclusions need justification as careful as inclusions — an unjustified exclusion is indistinguishable from an unnoticed gap. L3: scope-games tell — the production platform excluded while office Wi-Fi is included, read the scope statement. |
| e-logging-monitoring | 1, 2, 3 | L1: SIEM, MDR, SLA defined on first use. L2: why the 800-92 lifecycle is phased — each phase has a different owner and failure mode (generation misses events, transmission tampers, storage ages out, analysis unread, disposal liability). L3: tuning-loop observables — 1,000 unacknowledged alerts, or a rule with zero true positives in 90 days. |
| e-media-protection | 1, 2, 3 | L1: bonded courier (surety bond = carrier skin in the game), chain of custody, degauss (magnetic-only, HDD/tape, useless on SSD), DLP. L2: why confidentiality-before-media-type ordering — the data sets required strength, the physics sets feasible technique; technique-first yields the degaussed SSD. L3: sanitization-theater tell — disposal register with empty verification column, destruction certificate with no witness. |
| e-network-architecture | 1, 2, 3 | L1: east-west vs north-south, 802.1X, jump host/bastion, VPN concentrator, historian server, SPAN, SIEM (pointer). L2: why the management network is its own zone (administer-the-firewalls = own-every-zone); why per-session grants (trust decays; a once-evaluated grant is a standing opportunity). L3: VLAN-costume tell — inter-VLAN ACL empty or ending in permit-any; read the router config, not the diagram. |
| e-network-components | 1, 2, 3 | L1: any-any, in-band, HA pair, RADIUS (by function), SPAN, NAT, SNMP community strings, SSID. L2: why default deny fails safe (blocklists fail open; attackers specialize in the unnamed); why specific-before-general (first-match semantics — a general rule above silently swallows the specific below). L3: ruleset review output as a list — no-owner rules, zero-hit rules in 12 months, any-any allows. |
| e-patch-management | 1, 2, 3 | L1: EPSS, SLA, canary deploy, smoke test, BIA, tabletop, host IDS. L2: why KEV outranks CVSS (evidence of attack beats a model of severity — attackers don't read scores); why exceptions transfer risk to compensating controls (the register records the transfer). L3: "everything is critical" observable — KEV item from March behind forty routine items; "deployment assumed" tell — ticket says deployed, scanner still lists the CVE. |
| e-personnel-safety | 1, 2, 3 | L1: express kidnapping, de-escalation, advance work. L2: why check-in escalation is tiered (+2/+4h) — travelers miss check-ins innocently; immediate escalation would be cried-wolf into uselessness. L3: duress recall test — ask three people the phrase a month after rollout. |
| e-personnel-security | 1, 2, 3 | L1: blast radius, acceptable-use policy, PSK, COB. L2: why involuntary termination gets immediacy (motive + means window); why transfers re-trigger screening (original screening assessed a different blast radius). L3: HR-says-Friday/IdP-log-shows-Monday tell; admin password last-changed predating three departures. |
| e-physical-security | 1, 2, 3 | L1: CCTV, UPS, clean-agent suppression, fail-secure vs fail-safe, piggybacking. L2: why the mantrap's two-door design is the mechanism — a single door can't distinguish one person from two; the interlock creates the contained, identifiable moment. L3: deactivation-aging report — badges active past holder's last day, days counted, monthly. |
| e-platform-security | 1, 2, 3 | L1: vTPM, BOM, key ceremonies. L2: why attestation quotes are signed — without the signature an attacker simply sends fake measurements; the verifier must know the quote came from a real TPM. L3: never-attested tell — ask for the last attestation verification record; if the log doesn't exist, measurements were recorded and never checked. |
| e-policy-docs | 1, 2, 3 | L1: CISO, duty of care, cipher suite, ECB mode. L2: why traceability runs both directions — down proves the policy is implemented (not shelfware), up proves the procedure is authorized (not rogue). L3: forty-page-policy audit tell — review date three years old, names a decommissioned tool. |
| e-retention-eol | 1, 2, 3 | L1: spoliation, CMDB, LIMS, HRIS. L2: why longest-period-wins — the schedule must satisfy every obligation at once; one law's timeline can violate another's. L3: EOSL-denial query (EOSL past, status still production — run quarterly); backup-amnesia tell (destruction record for production copy, none for backups). |
| e-risk-assessment | 1, 2, 3 | L1: residual risk (defined before the worked register), WAF, EDR, ALE. L2: why likelihood and impact are separated — different controls reduce each (preventive cuts likelihood, containment/recovery cuts impact), so the split tells you which kind of control to buy; also drives response choice (transfer/accept vs mitigate). L3: invented-statistics tell — a percentage likelihood with no cited source. (Register/worked case untouched.) |
| e-sdlc | 1, 2, 3 | L1: SAST, DAST, SCA (by function), SBOM, waterfall. L2: why gates sit at phase boundaries instead of one end review — a single end-review concentrates findings where fixes cost most and schedule pressure is highest, so findings get negotiated away; per-phase gates force decisions when change is cheap. L3: gate-negotiated tell — release-blocking severity marked "accepted" with no new mitigation; checklist-without-enforcement tell — same finding class in three consecutive gate reviews. |
| e-secops-concepts | 1, 2, 3 | L1: break-glass account. L2: why SoD demands collusion — one person can quietly skip a process; two must agree to conspire, which is rarer, harder to coordinate, leaves twice the evidence. L3: unused-privilege report (standing admin, last privileged action 90+ days ago); shared-fate tell — one credential administering all three layers. |
| e-secure-channels | 1, 2, 3 | L1: idempotent, mutual TLS, split tunneling, safety numbers, footgun. L2: why 0-RTT is restricted to idempotent requests (captured 0-RTT can be replayed; server can't distinguish replay from original); why agent forwarding is dangerous (delegation — the bastion borrows your keys for the session). L3: cert-expiry tell — dashboard shows <30 days with no renewal ticket (outage already scheduled); downgrade tell — endpoint still negotiates the old TLS version with no deprecation ticket. |
| e-secure-design | 1, 2, 3 | L1: reference monitor, OIDC (in worked example), call graph, telematics, tailor. L2: why complete mediation bans cached shortcuts — a cached decision was made under old context by a different component; the check must be evaluated at the moment of access. L3: wall-art test (no principle in last quarter's review minutes); shopping-list tell (trace-matrix controls with empty requirement rows). |
| e-security-audits | 1, 2, 3 | L1: assurance (operational definition — the auditor's product, per the brief's bar), workpapers, fieldwork, systematic sampling. L2: why audits sample instead of testing everything — the canonical rationale: exhaustive testing costs more than the assurance is worth; audit aims for reasonable assurance, so expensive procedures go 100% on risky items while routine items get the random sample. L3: no-follow-up tell (last year's findings still "open", no remediation date); sampling tell (workpapers' sampling section blank or "selected a few"). |
| e-security-concepts | 1, 2, 3 | L1: avalanche property, RTO/RPO, shadow IT, WAF, MFA. L2: why authentication precedes authorization — authorization is a decision about an identity; without authentication you don't know whose permissions to evaluate. L3: authn/authz-confusion case (service account with valid login acting outside its role); usability-denial tell (sanctioned encrypted-USB fleet gathering dust while personal sticks are everywhere). |
| e-security-metrics | 1, 2, 3 | L1: IdP, PAM, SIEM. L2: why self-attestation is the weakest collection method — reporter and measured are the same party; the number measures willingness to report well, not compliance. L3: gaming tell (measure improves while risk doesn't — training 100%, phishing clicks climbing); metric-sprawl tell (review meeting where nobody can name any measure's owner). |
| e-security-models | 1, 3 | L1: covert channels, compartments, mandatory access control, state-machine discipline. L3: deploy-the-model tell — every file labeled, but the operation-level rule check met with silence. (Lens 2 quiet — the dual-structure rationales were already stated.) |
| e-security-program | 1, 2, 3 | L1: RACI (full expansion), Target Profiles. L2: why the program is a loop not a project — threats/tech/business change continuously; a project ends, and the day it ends the program starts decaying. L3: unowned-metric tell (red number, no one in the room to explain it); wish-list charter observable (verbs "ensure"/"guarantee" instead of "may"/"decides"); invented-numbers tell (round target, no named source). |
| e-soc2 | 1, 2, 3, 5 | L1: carve-out / complementary-subservice-organization-controls, MSA, DPA. L2: why Security is the mandatory criterion (availability of a system anyone can alter isn't the availability committed to); why no pass/fail (the report informs the reader's risk decision — the customer decides whether exceptions matter). L3: Type-I-sold-as-assurance tell (Type I, fourteen months old); scoping-by-ambition tell (ask which commitment the criterion traces to — silence is the finding). L5: §7 reading order sharpened (criteria page orients before the document; testimony's SOC-suite section is the plain-language map first). |
| e-supply-chain-risk | 1, 2, 3 | L1: subprocessor, PCI-assessed (PCI DSS), EHR. L2: why a questionnaire is a claim and an auditor's report is evidence — authorship and liability: self-graded by the beneficiary vs produced by an independent party whose standing depends on accuracy. L3: questionnaire-theater tell (file contains only self-attestation); snapshot-assessment tell (file's last update predates the vendor's acquisition). |
| e-system-lifecycle | 1, 2, 3 | L1: degauss (magnetic-only), ASVS, SR-5 identified as the supply-chain control from the selection package (no invented control text). L2: why the authorization decision needs authority — residual-risk acceptance is a business decision; only someone empowered to own consequences can meaningfully sign. L3: authorization-as-signature tell (signed same day as issued, or boilerplate rationale across systems); conditions-without-follow-through tell (gate register shows conditions past due, no closure evidence). |
| e-test-analysis-reporting | 1, 2, 3 | L1: banner, backported fix, honeypot, KEV. L2: why triage precedes scoring — scoring an unverified finding launders the tool's error into a decision (a false positive scored "critical" becomes top priority by arithmetic). L3: remediation-without-verification tell ("closed" findings, empty verification columns — or the next rescan); risk-acceptance-as-rug tell (accepted rows, blank owner/expiry). (Two-layer report untouched.) |
| e-threat-modeling-concepts | 1, 2, 3 | L1: attack surface. L2: why attack-tree nodes are annotated — the annotation is the economics: it prices the attacker's options, so the countermeasure decision is "which defense raises the attacker's price most per dollar spent." L3: never-revisited tell (model older than the last architecture change); STRIDE-as-checklist tell (six categories ticked, no attacker goal, no chained path). |

## Lens 4 note

Every lesson already carries a concrete worked example (worked case, selection record, register, survey, or run demo). No lens-4 additions were warranted — adding one would have duplicated, not deepened. e-risk-assessment's register and e-test-analysis-reporting's two-layer report were left byte-identical per instructions.

## Lens 5 note

§7 "Read the source" sections were written to the §6 spec (read/skim/skip per item) across the batch; only e-soc2's was list-like and got sharpened. No other lens-5 changes.

## Sources

`sources-add-2-DEb.csv` is header-only: no new external factual claims were introduced. All additions are (a) definitions of standard industry terms by what they do, (b) design-rationale sentences derived from the lesson's own stated mechanisms, and (c) concrete observable signals for failures the lessons already name. No §7 citations were added or changed (except e-soc2's reading-order wording, same sources). No walkthrough steps were added anywhere, so no runs were needed.

## Verification (2026-10-10)

- All 27 edited lessons: exactly ten `^## ` sections each; `^lesson_id:` present in all 27.
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`): zero hits in the 27 edited files. One pre-existing hit in `e-incident-management.md` (DEa batch, line 84 — "under-escalation until it's undeniable") — not my file, not touched; flagged for the coordinator.
- Currency: no `$<digit>` in any of the 27 files.
- `python3 guidebook/build_site.py` from `~/workspace/learncomputerstuff`: completed, exit 0, "done" — zero errors.
- pgrep: clean (one transient PID during the scan, gone on recheck; no test servers were started by this audit — no walkthrough steps were added).
- Untouched: build_site.py, STATE.md, gaps.md, map.md, sources.csv, runs/, all other stages' files. Nothing committed, nothing pushed.

## Not closed / for the coordinator

1. Pre-existing "undeniable" in `e-incident-management.md` line 84 (voice-rule scan) — DEa batch's file; needs their one-word fix.
2. The legacy lesson-ID scheme in "Leads to" sections (flagged by the DEa audit) still stands — coordinator decision pending; not touched per orders.
3. One judgment call to record: in `e-system-lifecycle` the worked example references "the SR-5 compensating control" — I identified it as the supply-chain control from the selection package without inventing SP 800-53 control text. If the coordinator wants the exact SR-5 requirement named, that's a primary-source fetch.


======================================================================
# AI track
======================================================================

# Content-depth audit, second pass — AI track (8 lessons)

Auditor: subagent 2183e7d7 · 2026-10-10. Dino's order after the first pass (105 solid / 5 deepened): "try again" — the first pass was too lenient. This pass applied five sharper lenses to every one of the 8 AI lessons, deliberately different from the first audit's verdicts. Brief §1 (the bar: "explain each mechanism from first principles, with no term they can't unpack"; "Define each term where it is first needed, by what it does"), §5 (AI scope), §6 (ten sections), §7 (evidence/safety/voice) re-read first.

Result: **lenses fired on all 8 lessons; all 8 deepened.** No padding — every addition is a definition, a design rationale, a concrete detection signal, or a fixed §7.

## Per-lesson: which lenses fired, what was added

### ai-governance (L2) — lenses 1, 2
- **L1:** defined "conformity assessment" where the high-risk tier uses it (Art. 43: provider's documented internal control or independent notified-body assessment, before market placement); defined "systemic risk" where the GPAI layer uses it (Art. 65: GPAI models whose high-impact capabilities could significantly affect the EU market or public health, safety, security, or fundamental rights). Both verified against the EUR-Lex primary text in-session.
- **L2:** added the design rationale for MEASURE vs MANAGE as separate RMF functions — a treatment decision without evidence is a guess; MANAGE assigns, only MEASURE tells you the control works; ties directly to the lesson's own §6 "governance without MEASURE" failure mode.
- L3 N/A (governance lesson teaches no attacks). L4 already has a worked example (Meridian classification). L5 §7 already carries read-order guidance.

### ai-llm-architecture (L3) — lenses 1, 2
- **L1:** expanded RAG on first use (Retrieval-Augmented Generation); defined "chunk" (a short passage a document was split into for retrieval).
- **L2:** added *why next-token prediction instead of answering directly* — no labeled-answer dataset exists at internet scale, but every document is a labeled dataset for "what word comes next"; self-supervised objective, verified against HF's own glossary. Added *why RAG exists* — three problems scale doesn't solve (frozen knowledge + retraining cost; private/fresh data can't enter a shared training set; cited retrieval is checkable, model memory is not), verified against the RAG paper's own stated motivations (Lewis et al., 2020).
- L3 N/A (mechanism-mapping lesson; detection lives in the sibling lessons it feeds). L4 already has the worked data-flow example. L5 §7 already has read/skim/skip guidance.

### ai-llm-top10 (L3) — lenses 1, 2, 3, 4
- **L1:** defined "fine-tuning" (LLM05), "held-out" (LLM05), "typosquatting" (LLM04), "inversion" (LLM09 — with the verified 92% figure from Morris et al., 2023).
- **L2:** added *why the retrieval filter must run before the similarity search, not after* (post-search filtering still admits other tenants' chunks into the computation — scores/timing leak; one filter bug is a full bypass); added *why the Stage B fix works for LLM10* (downstream systems can't tell who authored the text; trust lives in the context, not the author).
- **L3:** five concrete detection signals added where the lesson was generic — LLM02: plant canary strings, probe the model, a canary in the output proves exposure (verified: Carlini et al., "Secret Sharer", 2019); LLM03: alert on tool calls outside the task's declared tool set + approval-gate overrides; LLM07: check each cited source against the retrieved set — a citation to a never-retrieved document is the fabrication signature; LLM08: extraction-phrasing alerts weighted toward new accounts (pattern, not one curious user); LLM09: the retrieval-log line where chunk tenant ≠ requester tenant.
- **L4:** LLM07 was the one abstract-only risk section — added a one-paragraph concrete shape (the support bot quoting a nonexistent policy section and help-article number; the citation is the tell). All other risks already had concrete sketches or the incidents worked example.
- L5 §7 already has read/skim/skip guidance.

### ai-pipeline (L3) — lenses 1, 2, 5
- **L1:** defined "CI/CD" (the automated build-test-release machinery) and "digest" (the artifact's hash used as its version name — content-addressed, unrepointable) where first used.
- **L2:** added *why hermetic builds deny network* — a compromised dependency without a network path cannot exfiltrate or fetch a second stage; the blast radius ends at the container wall.
- **L3:** already concrete per stage (manifest names the file; attestation rejected with reason; gate logs the trigger) — no addition warranted, recorded as checked.
- **L5:** real defect fixed — §7's "free resources" was a duplicate list of the three primary docs with no purposes. Replaced with three *distinct* free resources, each with what it is for: GitHub artifact attestations docs (the concrete Stage 2–4 implementation, verified in-session), in-toto (the layout/link provenance vocabulary, verified in-session), OpenSSF Scorecard (upstream hygiene checks before trusting artifacts, verified in-session). (First choice, the CNCF supply-chain whitepaper PDF, returned HTTP 503 three times — not retried per fetch-failure discipline; Scorecard substituted and verified.)

### ai-prompt-injection (L3) — lenses 1, 2, 3
- **L1:** defined "red-teaming" (§1, where "red team" first appears), expanded RAG (§2), defined "instruction hierarchy" (§3 — conflicts resolve by privilege, verified: Wallace et al., 2024).
- **L2:** added *why no marking scheme fixes the provenance problem* — the model sees token IDs, not spans; any delimiter is itself text an attacker can forge; a text-completion interface has no out-of-band channel. Architectural, not a missing feature.
- **L3:** sharpened the detection paragraph with the concrete signal shape: `tool=refund_order session=4821 instruction_source=retrieved_doc`, and the rule it encodes — "destructive tool whose instruction source is not the user."
- L4 already has the poisoned-knowledge-base worked example. L5 §7 already has read/skim/skip guidance.

### ai-sec-automation (L2) — lenses 1, 2, 3
- **L1 (heaviest fire):** defined dwell time, SOAR (Security Orchestration, Automation and Response), purple teaming, EDR (Endpoint Detection and Response), IdP, SPF/DKIM/DMARC (email-authentication standards), honeytoken, ASN, NetFlow, step-up authentication, Sigma (standard detection-rule format, cross-ref to `c-sigma-detection`), virtual patching, and certificate-transparency logs — each where first needed, each by what it does.
- **L2:** added *why behavioral EDR over signatures* for AI-generated malware — signatures match known code; AI-generated malware is new code every time, so only behavior catches it.
- **L3:** sharpened the two generic telemetries found — "certificate transparency logs" → CT-log alerts on new certificates for lookalike domains; "outbound patterns that look scheduled rather than human" → outbound connections at fixed intervals to domains first seen this week. The rest (MFA push anomalies, impossible-travel/ASN-change rules, process-tree anomalies, patch-lag metrics) was already concrete — recorded as checked.
- L4 already has the worked detection plan. L5 §7 already has read/skip guidance.

### ai-supply-chain (L3) — lenses 1, 2, 3
- **L1:** defined OIDC (OpenID Connect — the login protocol letting GitHub/Google vouch for identity), "model card", and "predicate" (the statement inside an attestation about what was built).
- **L2:** added *why keyless wins* — a stolen long-lived key signs forgeries silently and indefinitely; a short-lived certificate expires in minutes and every signing is Rekor-visible, so theft buys almost nothing and is itself observable.
- **L3:** added the concrete provenance-monitoring signal — a Rekor monitor alert for a signing event on your artifact name from an unexpected identity: a signature that verifies but shouldn't exist.
- L4: the pickle demo is the lesson's worked example — left alone per the task's explicit instruction. L5 §7 already has read/skim/skip guidance.

### ai-threat-modeling (L3) — lenses 2, 3
- **L1:** checked — STRIDE letters, trust boundary, ATLAS technique, asset/path are all defined in-lesson; "provenance" arrives via prerequisite `ai-pipeline`. No addition warranted, recorded as checked.
- **L2:** added *why six fixed prompts instead of brainstorming* — brainstorming finds threats you can imagine; the prompts force attacker goals you wouldn't think of, repudiation especially (the category forgotten until the logs you didn't keep are needed).
- **L3:** added "What the defender sees, per threat" — a concrete signal for each STRIDE-table row (T1 chunk-hash drift alert naming the document; T2 tenant-mismatch retrieval line; T3 approval-gate override alert; T4 provenance-labeled poisoned summary; T5 CI gate logging the trigger prompt; T6 extraction-phrasing alerts) — with the instruction that each register treatment carries its signal in the same row.
- L4 already has the Harborlight worked threat model. L5 §7 already has read/skim/skip guidance.

## Sources staged

`guidebook/reports/sources-add-2-AI.csv` — 9 rows, all status=verified, all fetched in-session 2026-10-10 (parent merges into sources.csv):
1. RAG paper, arxiv.org/abs/2005.11401 (why-retrieval rationale)
2. Instruction Hierarchy, arxiv.org/abs/2404.13208v1 (instruction-hierarchy definition)
3. Embedding inversion, arxiv.org/abs/2310.06816 (92% recovery figure)
4. Secret Sharer, ar5iv.labs.arxiv.org/html/1802.08232 (canary methodology)
5. EU AI Act, eur-lex.europa.eu/eli/reg/2024/1689/oj (Art. 43 conformity assessment; Art. 65 systemic-risk definition; Art. 55 obligations)
6. HF Transformers glossary, huggingface.co/docs/transformers/v4.49.0/en/glossary (self-supervised next-token objective; finetuning)
7. GitHub artifact attestations docs (Sigstore provenance; attestations must be verified)
8. in-toto, github.com/in-toto/in-toto (layout/link provenance framework)
9. OpenSSF Scorecard, github.com/ossf/scorecard (0–10 security-health checks)

Acronym expansions (SOAR, EDR, IdP, DMARC/DKIM/SPF, ASN, CI/CD, OIDC, CT, RAG) are treated as definitional glosses — defined by what they do per the §1 bar — and were sanity-checked against the fetched primary docs where those docs cover them (GitHub attestations doc confirms OIDC/Sigstore usage; HF glossary confirms the ML terms). No new walkthrough steps were added, so no new run transcripts were required; no test servers were started at any point.

## Verification (Phase 3)

- `python3 guidebook/build_site.py` from ~/workspace/learncomputerstuff: completed with zero errors.
- All 8 edited lessons: exactly ten `^## ` sections each; `^lesson_id:` frontmatter present in all 8 (structure untouched).
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`): zero hits in new copy.
- Currency symbols: no `$<digit>` in new copy.
- `pgrep` for test servers / stray processes: clean (none were started).
- Levels: none changed — additions are definitions, rationales, and detection signals, not new capability claims.
- NOT committed, NOT pushed, per orders. build_site.py, STATE.md, gaps.md, map.md untouched. No other stage's files touched.

## Couldn't close / follow-ups

- The CNCF Software Supply Chain Best Practices whitepaper PDF (github.com/cncf/tag-security …/CNCF_SSCP_v1.pdf) returned HTTP 503 on three attempts; per fetch-failure discipline it was not retried and was replaced by the verified OpenSSF Scorecard resource. If the coordinator wants the CNCF whitepaper in §7, it needs a re-fetch at build time.
- ai-sec-automation §7 still cites the paid SEC598/SEC535 courses' public pages (sans.org/sec598, sans.org/sec535) as primary leads with read/skip guidance — unchanged from the first audit; the brief's §3 correction (SEC598→GASAE, SEC535→GOAA) is the anchor and the lesson uses it correctly.
- The first audit's follow-up stands: OWASP's separate Top 10 for Agentic Applications (2026) is outside §5 scope — a gaps.md decision for the coordinator, not this pass.
