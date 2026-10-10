# Stage B — Practitioner: Night Research
**Track 02 · Researched 2026-10-09 · Brief-governed: primary sources, free-only, no prices/fees/salaries/time estimates, original prose**

Stage B milestone (brief §5): a first valid finding submitted to a program that authorizes testing.

---

## 0. Source ledger

| # | Claim / resource | Primary URL (fetched 2026-10-09) | Status |
|---|---|---|---|
| S1 | OWASP WSTG: v4.2 stable (Dec 2020), v5.0 in development, 12 categories, `WSTG-<CAT>-<NN>` IDs | https://owasp.org/www-project-web-security-testing-guide/v42/ | verified |
| S2 | OWASP Top 10:2025 is the current edition (A01–A10) | https://owasp.org/Top10/2025/ | verified |
| S3 | NIST SP 800-115: Sept 2008, Final, supersedes SP 800-42; methods = testing/examination/interviewing; phases = planning/execution/post-execution | https://csrc.nist.gov/pubs/sp/800/115/final | verified (via CSRC search result body) |
| S4 | PTES: 7 phases (Pre-engagement, Intelligence Gathering, Threat Modeling, Vulnerability Analysis, Exploitation, Post Exploitation, Reporting) | http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines | unreachable (HTTP 403 on fetch; structure corroborated across multiple secondary sources) |
| S5 | PortSwigger Web Security Academy: free, interactive labs, Burp Community Edition works | https://portswigger.net/web-security | verified |
| S6 | DVWA: digininja/DVWA, `docker compose up -d`, serves on :4280 | https://github.com/digininja/DVWA | verified (via search result body) |
| S7 | Juice Shop: `bkimminich/juice-shop`, `docker run --rm -p 127.0.0.1:3000:3000`, :3000 | https://github.com/juice-shop/juice-shop (referenced; image name from project README) | operator-added (README text via mirrors; re-fetch at build) |
| S8 | WebGoat: `webgoat/webgoat`, `:8080/:9090`, TZ note for JWT lessons | https://github.com/WebGoat/WebGoat (org/repo named in project docs) | operator-added (README text via mirrors; re-fetch at build) |
| S9 | crAPI: OWASP/crAPI, `docker-compose -f deploy/docker/docker-compose.yml up`, :8888 + mailhog :8025 | https://github.com/OWASP/crAPI | verified (via search result body) |
| S10 | DVGA: `dolevf/dvga`, `docker run -t -p 5013:5013 -e WEB_HOST=0.0.0.0 dolevf/dvga`, :5013 | https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application | verified (via search result body; older mirrors say :5000 — re-verify) |
| S11 | HackerOne: program types (Private/Public/Time-bound), scope-first, report→triage→bounty→remediate→retest | https://www.HackerOne.com/blog/what-are-bug-bounties-and-how-do-they-work | verified |
| S12 | Bugcrowd researcher docs: anyone can sign up; private programs may need identity verification; valid = in-scope + reproducible; first reporter | https://docs.bugcrowd.com/researchers/onboarding/becoming-a-researcher/ | verified (via search result body) |
| S13 | Intigriti: program types Private/Application/Registered/Public; triage on all program types | https://www.intigriti.com/ | verified (via search result body) |
| S14 | OWASP Cheat Sheet Series: official site, 136 sheets in GitHub index (count grows) | https://cheatsheetseries.owasp.org | verified (via search result body) |
| S15 | Sigma: generic open signature format for log events ("YARA for logs") | https://sigmahq.io | operator-added (official site named in SigmaHQ docs; re-fetch at build) |
| S16 | 15-phase tool catalog + activation order + hard rules (owner's file) | site-run/Web-Security-Tool-Catalog.md | operator-added (Dino's file; authoritative for scope) |

---

## 1. Lesson B-AUTH — Authorization, scope, and the hard rules
**Level:** 2 (Operate: run every engagement inside written scope) → 3 when the reader has completed a scoped engagement without a violation.

**Primary sources:** the brief §7 (owner's rules, authoritative for this site); each bounty program's own policy page (HackerOne/Bugcrowd/Intigriti program pages, S11–S13).

**Free resources (≤3):** PortSwigger Academy "Essential Skills" (authorized-lab discipline); HackerOne Hacktivity disclosed reports (see how scope is written); the site's own authorization notice (brief §7).

**Lab target:** none — this is a reading + writing lesson. Exercise: take three real public program policies and extract (a) in-scope assets, (b) out-of-scope, (c) forbidden test types, (d) safe-harbor wording, into a one-page scope card.

**Proof artifact:** a filled scope card for a chosen program + a signed (written) personal rules list: the six hard rules verbatim.

**Prerequisites:** Stage A complete.

**The six hard rules (lesson material, brief §7, owner's wording):**
1. A name found in recon is a candidate, never permission. Recheck scope before probing, crawling, or sending a request.
2. A scanner match on a known issue is not a new CVE.
3. A bearer token is not a JWT until the format is identified.
4. Never use a credential you find.
5. Secret scanners run with verification off.
6. Automated findings are confirmed by hand.

**Why this lesson is first:** every later lesson assumes the reader can state what they are allowed to touch. A finding obtained outside authorization is not a finding — it is a liability, and the site cannot publish it.

---

## 2. Lesson B-METH — Methodology: WSTG, PTES, NIST SP 800-115
**Level:** 2 (follow the methodology on a prepared target); the lesson names B-VULN lessons as the path to 3.

### OWASP WSTG (Web Security Testing Guide)
- **What it is:** the community testing methodology for web applications. Current stable release **v4.2 (December 2020)**; **v5.0 in active development** (not the baseline — report against v4.2 IDs).
- **Structure:** 12 test categories (information gathering; configuration and deployment management; identity management; authentication; authorization; session management; input validation; error handling; weak cryptography; business logic; client-side; API testing). Each test has a stable ID `WSTG-<CATEGORY>-<NN>` (e.g. `WSTG-ATHZ-02`); versioned form `WSTG-v42-ATHZ-02`.
- **When to use it:** as the test-by-test checklist for any web application assessment, and as the citation in findings (finding → test ID → Top 10 category).
- **Companion:** OWASP ASVS (verification requirements, three levels) — WSTG tests whether ASVS requirements hold.
- **Primary:** S1. Free resource: the guide itself (free, online).

### PTES (Penetration Testing Execution Standard)
- **What it is:** the engagement-lifecycle standard. Seven phases: Pre-engagement Interactions → Intelligence Gathering → Threat Modeling → Vulnerability Analysis → Exploitation → Post Exploitation → Reporting.
- **When to use it:** to structure a whole engagement (especially the parts WSTG doesn't cover: scoping, threat modeling, post-exploitation, reporting). PTES Technical Guidelines page returned HTTP 403 on fetch — structure corroborated across sources; mark the guidelines URL `unreachable` in the site ledger and cite the phase list from corroboration.
- **Primary:** S4 (unreachable; phases corroborated).

### NIST SP 800-115 (Technical Guide to Information Security Testing and Assessment)
- **What it is:** NIST's assessment guide, **September 2008, Final**, supersedes SP 800-42. Three assessment methods: **testing** (exercising objects under specified conditions), **examination** (checking/inspecting/reviewing), **interviewing** (discussions to clarify or locate evidence). Three project phases: **planning, execution, post-execution**.
- **When to use it:** the methodology-framing citation — it is the document that says assessment is not only technical testing, and it is the right reference when an engagement must verify compliance with policy, not just find bugs.
- **Primary:** S3.

**How the three fit (lesson teaching point):** PTES frames the engagement, WSTG fills the web-testing middle with test cases, 800-115 reminds you that examination and interviews are assessment too. A Stage B web finding typically cites WSTG test ID + OWASP Top 10:2025 category.

**Free resources (≤3):** WSTG v4.2 itself (S1); NIST SP 800-115 PDF (S3); PortSwigger Academy (S5) as the hands-on companion.

**Lab target:** pick a DVWA module; map the tests you ran to WSTG IDs and one PTES phase each.

**Proof artifact:** a one-page methodology sheet: engagement phases (PTES), test IDs used (WSTG), and which 800-115 method each test was.

**Prerequisites:** B-AUTH, Stage A.

---

## 3. The toolbench — 15 phases in activation order (S16)

Each phase: the question it answers, and what it **cannot** tell you. Paid-layer table ignored per brief. sqlmap, Nikto, Nessus, Hydra, and a second fuzzer stay off this path — not banned by category; they do not answer the first question, which is whether one signed-in user can read another user's object.

| # | Phase (tools) | Question it answers | What it cannot tell you |
|---|---|---|---|
| 1 | Scope and records — Obsidian/Markdown notes, Git | What is allowed, what is excluded, which accounts you own, what you already tried | Whether scope changed since you wrote it — recheck; it cannot authorize anything for you |
| 2 | Interception proxy — Burp Community (one primary proxy), Caido, mitmproxy | What did this request send, and what changed when you replayed one field | What the server-side check is; it cannot find logic flaws — it only shows traffic |
| 3 | Session isolation — Firefox profiles, Multi-Account Containers, PwnFox | Which identity sent this request | Whether the token actually belongs to that identity — confirm the cookie/token value, never trust the tab label |
| 4 | Authorization comparison — Autorize, AuthMatrix, Burp Comparer | Did account A receive account B's object | What the authorization *means* — output still needs a manual read |
| 5 | Asset discovery — subfinder, dnsx, httpx, amass, Shodan/Censys | Which names resolve, and which are live web apps | Permission — results are candidates only; nothing here is in scope by itself |
| 6 | Crawling and history — katana, gau, waybackurls, DevTools | Which paths the app or the archive already exposed | Current scope — recheck each path against scope before touching it |
| 7 | Content and parameters — ffuf, SecLists, Arjun | Is this one missing path or parameter real | Whether it is vulnerable; one hypothesis, one host, at a rate the program allows |
| 8 | Data handling — jq, yq, ripgrep, anew, unfurl | What is in this output, deduped, with the field you care about kept | What the data means — it structures, never interprets |
| 9 | API contracts — Bruno or Postman, oasdiff, Schemathesis | What does the spec say, what changed, what fails on a local install | Business permissions — specs do not know authorization rules |
| 10 | Tokens and callbacks — JWT Editor or jwt_tool, CyberChef, Burp Collaborator or interactsh | Is this token a JWT, what does this value decode to, did a permitted callback fire | A bearer token is not a JWT until the format is identified; a fired callback is a signal, not a vulnerability |
| 11 | Source analysis — VS Code, Git, Semgrep, CodeQL | Where is the permission check, and does this change remove it | Runtime exploitability — static findings still need a live proof; CodeQL on private repos carries licensing conditions (teach the condition, not the price) |
| 12 | Dependencies and secrets — Trivy, Gitleaks, TruffleHog with verification disabled | Is a dependency already vulnerable, or is a secret present | Whether the secret works — verification stays off by rule; never use a found credential; a match is not a new CVE by itself |
| 13 | Local environment — Docker/Compose, a debugger, a local test database | Can you pin the version, reset dummy data, and watch the check run | Production behavior — local is a model, and models differ |
| 14 | Reproduction — curl, Playwright, the project's own tests | Can someone else rerun it, and does the fix block the forbidden call while legitimate access still works | Absence of other flaws — a reproduced fix is one closed hole, not a clean bill |
| 15 | Evidence — Flameshot, Markdown, Dradis | Can you show the request, the other user's dummy data, and the timeline | Validity — evidence presents the finding; the finding still has to be real |

**Activation order (lesson teaching point):** 1) browser profiles + Burp Community + notes + screenshots; 2) Git, Docker, VS Code, curl once a product and disclosure policy are chosen; 3) Autorize/AuthMatrix once the two-account comparison works by hand; 4) Semgrep/CodeQL when one source file raises a specific question; 5) Playwright or the project's tests to replay the finding and check the fix. A paid proxy only enters when unsaved projects start costing findings — and the guidebook teaches the free path throughout, so this stays a footnote.

**Level:** 2 per phase (operate the tool on a prepared target); 3 when chained across a full finding.

**Free resources (≤3):** the catalog itself (S16, owner's file); PortSwigger Academy (S5); OWASP Cheat Sheet Series (S14) for the fix side.

**Lab target:** DVWA (S6) for phases 2–4, 7, 10; Juice Shop (S7) for 9–10; crAPI (S9) for 9.

**Proof artifact:** a toolbench log: one answered research question per phase, with the command and the evidence it produced.

**Prerequisites:** B-AUTH, B-METH, Stage A (HTTP in depth, Linux CLI).

---

## 4. Web vulnerability classes — wave 1

Each lesson follows the brief §6 spec. Mechanism in original prose; detection = what defenders see; fix = the correct remediation. Lab targets: PortSwigger Academy (S5) + the local apps (S6–S10). Level 3 target for all nine.

### B-VULN-01 — IDOR (Insecure Direct Object Reference)
- **Mechanism:** the server uses a client-supplied identifier (in URL, body, or header) to fetch an object and never checks that the requesting identity owns it. Change `invoiceId=1042` to `1043` and the server returns another tenant's record with 200 OK. The flaw is a missing authorization check on the object, not a broken identifier scheme — unguessable IDs are obfuscation, not a fix.
- **Primary references:** PortSwigger Academy → Access Control → IDOR (`portswigger.net/web-security/access-control/idor` — topic confirmed, re-verify exact slug at build); OWASP Top 10:2025 A01 Broken Access Control (S2); WSTG-ATHZ-02.
- **How defenders detect it:** access logs showing one session touching many sequential or foreign object IDs; WAF rules cannot reliably distinguish legitimate from illegitimate ID use — detection is behavioral (rate + spread of ID access per session).
- **Fix:** server-side ownership check on every object access (deny by default); indirect reference maps where appropriate; tests that assert cross-tenant access returns 403/404.
- **Free resources:** PortSwigger access-control labs; OWASP Access Control Cheat Sheet (S14); crAPI (S9) vehicle/order BOLA challenges.
- **Lab target:** PortSwigger IDOR labs + crAPI (`GET /identity/api/v2/vehicle/{id}/location` with two users).
- **Proof artifact:** request/response pair showing user A's session receiving user B's object, with the fix re-tested.
- **Prerequisites:** B-AUTH, B-METH, toolbench phases 2–4.

### B-VULN-02 — Broken access control (general)
- **Mechanism:** the application's authorization model fails to enforce what an authenticated user may do: missing function-level checks (unlinked admin endpoints reachable by URL), privilege escalation via parameter tampering (`role=user` → `role=admin`), forced browsing, insecure direct object references as a subclass. The common root: the client is trusted to stay within its lane.
- **Primary references:** PortSwigger Academy → Access Control (S5); OWASP Top 10:2025 A01 (S2 — now absorbs SSRF); WSTG-ATHZ (authorization testing).
- **How defenders detect it:** 403/404 probing followed by 200s on privileged paths; role-parameter anomalies in logs; impossible-role sessions.
- **Fix:** deny-by-default authorization on every endpoint and every object; server-side role checks, never client-side; centralized authorization logic, not per-endpoint ad hoc checks.
- **Free resources:** PortSwigger access-control labs (13 across apprentice/practitioner per community trackers — write as "13+" at build); OWASP Authorization Cheat Sheet (S14); DVWA (S6) low/medium/high levels.
- **Lab target:** PortSwigger access-control labs + DVWA.
- **Proof artifact:** matrix of (role × endpoint × object) with expected vs actual status codes.
- **Prerequisites:** B-VULN-01.

### B-VULN-03 — SQL injection
- **Mechanism:** untrusted input is concatenated into a database query and the database parses it as code. `’ OR ’1’=’1` changes the query's logic; stacked queries or UNION SELECT exfiltrate data. Variants: in-band (UNION/error-based), blind boolean, blind time-based, out-of-band. The flaw is query construction, not input "badness."
- **Primary references:** PortSwigger Academy → SQL Injection (S5); OWASP Top 10:2025 A05 Injection (S2); WSTG-INPV-05; OWASP SQL Injection Prevention Cheat Sheet (S14).
- **How defenders detect it:** WAF/IDS signatures on SQL keywords and tautologies; database logs showing anomalous query shapes; error-based probes are the noisiest.
- **Fix:** parameterized queries (prepared statements) everywhere; least-privilege DB accounts; no dynamic SQL from string concatenation; output is not the fix — construction is.
- **Free resources:** PortSwigger SQLi labs (18 per community trackers — "18+" at build); OWASP SQL Injection Prevention Cheat Sheet; DVWA SQLi modules (S6).
- **Lab target:** PortSwigger SQLi labs + DVWA (low → impossible, noting what each level's defense does).
- **Proof artifact:** extracted database version string via UNION technique on a lab target, with the parameterized-query fix demonstrated.
- **Prerequisites:** B-AUTH, B-METH, Stage A SQL reading.

### B-VULN-04 — OS command injection
- **Mechanism:** untrusted input reaches a shell command. The application builds `ping <input>` and the input `8.8.8.8; whoami` runs a second command. Blind variants exfiltrate via time delays or out-of-band callbacks. The flaw is shell invocation with unsanitized input.
- **Primary references:** PortSwigger Academy → OS Command Injection (S5); OWASP Top 10:2025 A05 (S2); WSTG-INPV-12; OWASP OS Command Injection Defense Cheat Sheet (S14).
- **How defenders detect it:** EDR/command-line logging showing shell metacharacters in web-process command lines; egress to collaborator-style domains from server processes.
- **Fix:** avoid shell invocation entirely (exec with argument arrays); strict allowlist validation; least-privilege service accounts so a breakout buys little.
- **Free resources:** PortSwigger command-injection labs; OWASP cheat sheet; DVWA command injection module (S6).
- **Lab target:** PortSwigger labs + DVWA.
- **Proof artifact:** `whoami` output via injection on the lab target, then the fixed code path showing the argument-array call.
- **Prerequisites:** B-VULN-03 (injection mindset), Stage A Linux CLI.

### B-VULN-05 — API abuse
- **Mechanism:** APIs expose the application's real attack surface: BOLA (API1:2023 — the API twin of IDOR), broken function-level authorization (API5), mass assignment / over-posting via BOPLA (API3), unrestricted resource consumption (API4), unsafe consumption of APIs (API10). Mobile and SPA front ends are just API clients — everything the UI hides, the API still serves.
- **Primary references:** OWASP API Security Top 10:2023 (API1–API10; primary project page — fetch at build, URL from brief §11 lead); PortSwigger Academy → API Testing (S5); OWASP REST Security Cheat Sheet (S14).
- **How defenders detect it:** API gateway logs showing cross-tenant object access, method-not-allowed probing, mass-assignment field anomalies; schema violations at the gateway.
- **Fix:** object-level and function-level authorization on every endpoint; explicit allowlisted response/request schemas (no silent field acceptance); rate limiting per identity; full API inventory (shadow/zombie APIs are the classic miss).
- **Free resources:** OWASP API Security Top 10 project docs; PortSwigger API testing labs; crAPI (S9) — purpose-built for this lesson.
- **Lab target:** crAPI (full API Top 10 coverage) + PortSwigger API labs.
- **Proof artifact:** BOLA reproduction across two crAPI users with captured tokens, mapped to API1:2023.
- **Prerequisites:** B-VULN-01, B-VULN-02, toolbench phase 9.

### B-VULN-06 — SSRF (Server-Side Request Forgery)
- **Mechanism:** the server fetches a URL the client supplied. `?url=http://169.254.169.254/latest/meta-data/` makes the server request its own cloud metadata. The attacker never touches the internal network directly — the server does it for them. Note the 2025 reframing: SSRF is folded into OWASP A01:2025 Broken Access Control.
- **Primary references:** PortSwigger Academy → SSRF (S5); OWASP Top 10:2025 A01 (S2); WSTG-INPV-19; OWASP SSRF Prevention Cheat Sheet (S14).
- **How defenders detect it:** egress logs showing server-initiated requests to internal/metadata addresses; DNS logs for internal names resolved by server processes.
- **Fix:** allowlist of fetchable destinations; no user-controlled URLs in server-side fetches; metadata service protections (IMDSv2); egress filtering.
- **Free resources:** PortSwigger SSRF labs; OWASP cheat sheet; Juice Shop SSRF challenges (S7).
- **Lab target:** PortSwigger SSRF labs + Juice Shop.
- **Proof artifact:** metadata-service response retrieved through the lab app's fetch feature, with the allowlist fix verified.
- **Prerequisites:** B-VULN-03, Stage A networking (what 169.254.169.254 is).

### B-VULN-07 — XSS (Cross-Site Scripting)
- **Mechanism:** attacker input is reflected into a page (reflected), persisted in storage and served later (stored), or executed via client-side DOM manipulation (DOM-based) without proper output encoding. `<svg onload=...>` breaks out of its context and runs in the victim's session. The flaw is context-unaware output handling.
- **Primary references:** PortSwigger Academy → XSS (S5; the largest topic — 30 labs per community trackers, "30+" at build); OWASP Top 10:2025 A05 (S2); WSTG-INPV-01/02; OWASP XSS Prevention Cheat Sheet (S14).
- **How defenders detect it:** CSP violation reports; WAF signatures on script contexts; reflected-XSS probes are noisy, stored XSS shows up in content reviews.
- **Fix:** context-aware output encoding; strict Content Security Policy; modern frameworks' auto-escaping (and knowing where it stops — e.g. `innerHTML`, `dangerouslySetInnerHTML`).
- **Free resources:** PortSwigger XSS labs; OWASP XSS Prevention Cheat Sheet; DVWA XSS modules (S6).
- **Lab target:** PortSwigger XSS labs + DVWA (reflected/stored/DOM).
- **Proof artifact:** alert-free proof of execution (use a benign marker like `document.domain` exfil to your own collaborator) on the lab target, with the encoding fix shown.
- **Prerequisites:** B-AUTH, B-METH, Stage A JavaScript reading.

### B-VULN-08 — CSRF (Cross-Site Request Forgery)
- **Mechanism:** the browser automatically attaches cookies to cross-site requests, so a malicious page can make the victim's browser issue a state-changing request the victim never intended. The flaw is the application's inability to distinguish a request the user made from one made *as* the user.
- **Primary references:** PortSwigger Academy → CSRF (S5); WSTG-SESS-05 (session management testing covers CSRF); OWASP CSRF Prevention Cheat Sheet (S14).
- **How defenders detect it:** hard to detect server-side — the request is indistinguishable from legitimate traffic; anti-CSRF token validation failures in logs are the signal that *attempts* occurred.
- **Fix:** anti-CSRF tokens (synchronizer pattern); SameSite cookie attribute; checking Origin/Referer as defense-in-depth; requiring re-authentication for sensitive actions.
- **Free resources:** PortSwigger CSRF labs; OWASP cheat sheet; DVWA CSRF module (S6).
- **Lab target:** PortSwigger CSRF labs + DVWA.
- **Proof artifact:** a self-contained HTML proof-of-concept that changes the lab victim's email, then the token-protected version that rejects it.
- **Prerequisites:** B-VULN-07 (browser security model), Stage A cookies/sessions.

### B-VULN-09 — Business-logic flaws
- **Mechanism:** the application does exactly what it was coded to do, and what it was coded to do is wrong: negative quantities, price in the POST body, workflow steps skippable by URL, coupon reuse, race-to-checkout. No injection, no misconfiguration — the logic itself is the vulnerability. Scanners cannot find these; only a human who understands the intended workflow can.
- **Primary references:** PortSwigger Academy → Business Logic Vulnerabilities (S5); OWASP Top 10:2025 A06 Insecure Design (S2); WSTG-BUSL (business logic testing); OWASP Business Logic Security Cheat Sheet (S14).
- **How defenders detect it:** transaction anomaly monitoring (impossible quantities, out-of-order workflow states); these are found in logs only if the business defines what "wrong" looks like.
- **Fix:** server-side enforcement of every business rule; state machines for workflows; price/quantity recalculated server-side; abuse-case testing during design.
- **Free resources:** PortSwigger business-logic labs; OWASP cheat sheet; Juice Shop logic challenges (S7).
- **Lab target:** PortSwigger business-logic labs + Juice Shop.
- **Proof artifact:** a workflow-abuse write-up: intended flow, abused flow, financial/logic impact, server-side rule that stops it.
- **Prerequisites:** all wave-1 lessons above (this is the synthesis lesson).

---

## 5. Web vulnerability classes — wave 2

### B-VULN-10 — Authentication flaws
- **Mechanism:** failures in proving identity: credential stuffing/brute force without rate limiting, weak lockout, password reset token flaws, session fixation, "remember me" token issues, MFA bypass via logic, username enumeration via response differences. Distinct from authorization (B-VULN-02): this is *who are you*, not *what may you do*.
- **Primary references:** PortSwigger Academy → Authentication (S5); OWASP Top 10:2025 A07 Authentication Failures (S2); WSTG-ATHN; OWASP Authentication Cheat Sheet + Forgot Password Cheat Sheet (S14).
- **How defenders detect it:** authentication logs — burst login attempts, reset-token request anomalies, enumeration patterns (timing/response deltas).
- **Fix:** rate limiting + lockout + monitoring on auth endpoints; unguessable reset tokens with expiry, single-use; session rotation on login; MFA; generic auth-failure responses.
- **Free resources:** PortSwigger auth labs (14 per community trackers); OWASP cheat sheets; DVWA brute-force module (S6).
- **Lab target:** PortSwigger authentication labs + DVWA.
- **Proof artifact:** username-enumeration evidence (response delta) on the lab target, then the fixed generic-response behavior.
- **Prerequisites:** B-VULN-02, B-VULN-08.

### B-VULN-11 — SSTI (Server-Side Template Injection)
- **Mechanism:** user input is embedded in a server-side template and the template engine evaluates it: `{{7*7}}` rendering `49` proves evaluation; escalating to `{{config}}` or engine-specific payloads yields code execution. The flaw is concatenating input into templates instead of passing it as data.
- **Primary references:** PortSwigger Academy → Server-Side Template Injection (S5); OWASP Top 10:2025 A05 (S2); WSTG-INPV (input validation); template-engine documentation as primary (identify the engine first).
- **How defenders detect it:** template-syntax probes in input logs; engine error messages; code-execution follow-on is an EDR matter.
- **Fix:** never build templates from user input — pass input as variables; logic-less templates; sandboxing is not a fix.
- **Free resources:** PortSwigger SSTI labs; engine docs (Jinja2, Twig, Freemarker — read the primary); Juice Shop SSTI-adjacent challenges (S7).
- **Lab target:** PortSwigger SSTI labs.
- **Proof artifact:** `{{7*7}}→49` detection plus one impact escalation on the lab target, with the variable-passing fix.
- **Prerequisites:** B-VULN-03, B-VULN-04.

### B-VULN-12 — XXE (XML External Entity injection)
- **Mechanism:** the XML parser processes external entities: `<!ENTITY xxe SYSTEM "file:///etc/passwd">` makes the parser read server files or issue SSRF requests. Billion-laughs variants DoS the parser. The flaw is a parser configured with entity expansion enabled.
- **Primary references:** PortSwigger Academy → XXE Injection (S5); OWASP Top 10:2025 A05 (S2); WSTG-INPV-07; OWASP XXE Prevention Cheat Sheet (S14).
- **How defenders detect it:** parser error logs; egress from XML-processing services to internal addresses (XXE-as-SSRF).
- **Fix:** disable DTDs/external entities in the parser configuration (per-language cheat-sheet snippet); prefer JSON where XML is not needed; XSD validation is not a fix.
- **Free resources:** PortSwigger XXE labs; OWASP cheat sheet; WebGoat XXE lessons (S8).
- **Lab target:** PortSwigger XXE labs + WebGoat.
- **Proof artifact:** `/etc/passwd` (lab container) exfiltrated via XXE, then the hardened parser config rejecting the payload.
- **Prerequisites:** B-VULN-06 (SSRF mindset helps), Stage A XML basics.

### B-VULN-13 — Insecure deserialization
- **Mechanism:** the application deserializes attacker-controlled data with a format that can instantiate arbitrary objects (Java `readObject`, Python `pickle`, PHP `unserialize`, Node `node-serialize`). A crafted payload executes code during deserialization — before any application logic runs. The flaw is trusting a byte stream.
- **Primary references:** PortSwigger Academy → Insecure Deserialization (S5); OWASP Top 10:2025 A08 Software or Data Integrity Failures (S2); WSTG-INPV-08; OWASP Deserialization Cheat Sheet (S14).
- **How defenders detect it:** deserialization gadget signatures are unreliable; detection focuses on the code-execution aftermath (EDR) and on integrity monitoring of serialized stores.
- **Fix:** do not deserialize untrusted data — use data-only formats (JSON) with integrity checks (signatures); allowlisted classes where deserialization is unavoidable.
- **Free resources:** PortSwigger deserialization labs; OWASP cheat sheet; WebGoat deserialization lessons (S8).
- **Lab target:** PortSwigger labs + WebGoat.
- **Proof artifact:** code execution via a gadget chain on the lab target (documented, lab-only), with the JSON+signature replacement.
- **Prerequisites:** B-VULN-03, Stage A reading code (Java/Python/PHP as encountered).

### B-VULN-14 — JWT and OAuth flaws
- **Mechanism (JWT):** JSON Web Tokens are signed, not encrypted, by default — and many implementations accept `alg=none`, accept attacker-supplied HMAC keys (confusing RS256→HS256), or skip signature verification. A bearer token is not a JWT until the format is identified (hard rule 3).
- **Mechanism (OAuth):** authorization-code flows break via redirect_uri manipulation, code leakage through referer/history, PKCE omission on public clients, and open redirectors chained into the flow.
- **Primary references:** PortSwigger Academy → JWT Attacks and OAuth Authentication (S5); RFC 7519 (JWT), RFC 6749 (OAuth 2.0) — primary standards, read the security-considerations sections; OWASP JWT Cheat Sheet (S14).
- **How defenders detect it:** `alg=none` or unexpected-alg tokens in auth logs; redirect_uri anomalies; token-reuse across clients.
- **Fix:** strict allowlist of algorithms; verify signatures with the correct key, every time; short expiries; PKCE for public clients; exact-match redirect URIs.
- **Free resources:** PortSwigger JWT + OAuth labs; RFC 7519 §security considerations; jwt.io (decode/inspect only — never paste real tokens).
- **Lab target:** PortSwigger JWT/OAuth labs; jwt_tool or Burp's JWT Editor on lab tokens.
- **Proof artifact:** forged `alg=none` token accepted by the lab app, then the strict-verification fix rejecting it.
- **Prerequisites:** B-VULN-10, Stage A (JWT structure, OAuth2/OIDC flows).

### B-VULN-15 — GraphQL abuse
- **Mechanism:** GraphQL endpoints expose a typed schema (introspection) that documents every query the API supports — including hidden ones. Abuse patterns: introspection-enabled-in-production, batching/aliases for brute force and DoS, field duplication, nested-query depth bombs, authorization checked per-query but not per-field (BOLA through GraphQL).
- **Primary references:** PortSwigger Academy → GraphQL API Vulnerabilities (S5); OWASP API Security Top 10:2023 (S2-adjacent); GraphQL spec (introspection section — primary).
- **How defenders detect it:** introspection queries in API logs; query-depth/complexity anomalies; batched alias patterns.
- **Fix:** disable introspection in production; query depth/complexity limits; per-field authorization; rate limiting that accounts for batching.
- **Free resources:** PortSwigger GraphQL labs; DVGA (S10) — purpose-built; GraphQL spec introspection docs.
- **Lab target:** DVGA (`dolevf/dvga`, :5013 — re-verify port at build) + PortSwigger GraphQL labs.
- **Proof artifact:** introspection dump of the DVGA schema plus one field-level authorization bypass, with introspection disabled and depth-limited after the fix.
- **Prerequisites:** B-VULN-05, B-VULN-01.

### B-VULN-16 — Race conditions
- **Mechanism:** the application checks a condition and acts on it as two separate steps (check-then-act), and a second request slips between them: double-spending a coupon, withdrawing the same balance twice, winning a race to claim a username. Single-threaded reasoning fails against concurrent requests.
- **Primary references:** PortSwigger Academy → Race Conditions (S5); OWASP Top 10:2025 A06/A10 (design + exceptional conditions, S2); WSTG-BUSL (business logic testing).
- **How defenders detect it:** near-simultaneous duplicate transactions from one identity; balance/coupon integrity alerts; these are found by reconciliation, not by request inspection.
- **Fix:** atomic operations (database transactions, compare-and-swap); pessimistic locking on contested resources; idempotency keys; rate limiting helps but is not the fix.
- **Free resources:** PortSwigger race-condition labs (single-packet attack technique); Juice Shop race-adjacent challenges (S7).
- **Lab target:** PortSwigger race-condition labs (Burp Repeater single-packet / Turbo Intruder on lab targets).
- **Proof artifact:** double-redemption of a lab coupon via parallel requests, with the transactional fix preventing the second.
- **Prerequisites:** B-VULN-09, toolbench phase 2 (proxy) + 14 (replay).

---

## 6. Lesson B-LAB — Setting up practice targets locally
**Level:** 2 (Operate: stand up and reset every target below).

| Target | What it is | Run command (verified 2026-10-09) | Serves |
|---|---|---|---|
| DVWA | PHP/MariaDB classic, difficulty levels low→impossible | `git clone https://github.com/digininja/DVWA && cd DVWA && docker compose up -d` → http://localhost:4280 (S6) | B-VULN-01–04, 07–08, 10 |
| OWASP Juice Shop | Modern Node.js app, gamified challenges, score board | `docker run --rm -p 127.0.0.1:3000:3000 bkimminich/juice-shop` → http://localhost:3000 (S7) | B-VULN-05–07, 09, 11, 16 |
| OWASP WebGoat | Java lessons app + WebWolf attacker mailbox | `docker run -it -p 127.0.0.1:8080:8080 -p 127.0.0.1:9090:9090 webgoat/webgoat` (set `-e TZ=` to match host for JWT lessons) (S8) | B-VULN-03, 07, 12–13 |
| OWASP crAPI | Full vulnerable API (car-shop), mailhog included | `curl -o docker-compose.yml https://raw.githubusercontent.com/OWASP/crAPI/main/deploy/docker/docker-compose.yml && docker-compose -f docker-compose.yml --compatibility up -d` → http://localhost:8888, mail http://localhost:8025 (S9) | B-VULN-01, 05 |
| DVGA | Vulnerable GraphQL service | `docker pull dolevf/dvga && docker run -t -p 5013:5013 -e WEB_HOST=0.0.0.0 dolevf/dvga` → http://localhost:5013 (S10; older mirrors say :5000 — re-verify at build) | B-VULN-15 |
| PortSwigger labs | Hosted, authorized, resettable per lab | Account at portswigger.net; every lab is its own ephemeral target (S5) | all B-VULN lessons |

**Safety rules for this lesson (brief §7):** bind everything to localhost/127.0.0.1; never expose a vulnerable app to a network; DVWA/WebGoat warn they make the machine vulnerable while running — run them only while practicing, then `docker compose down`. During research, never scan or probe any live system.

**Free resources (≤3):** each project's README (S6–S10); Docker's official install docs; PortSwigger Academy (S5).

**Proof artifact:** all five local targets running simultaneously on distinct localhost ports, screenshotted, with a one-line "what this target is for" each.

**Prerequisites:** Stage A (Linux CLI, Docker basics).

---

## 7. Lesson B-DEF — Defensive basics: SOC triage, reading SIEM alerts, alert logic
**Level:** 2 (Operate: triage a queue, read an alert, explain what fired and why).

- **SOC triage, the workflow:** an alert arrives with a severity, an entity (user/host), and a detection name. Triage answers three questions in order: (1) is this a true positive — does the underlying event exist in the raw logs; (2) is it malicious or benign-but-weird — business context decides; (3) what is the blast radius — one host or many, one user or a service account. Escalate with the evidence attached, not with a feeling. Close false positives with the reason recorded — the record is what tunes the detection later.
- **Reading a SIEM alert:** every alert is a detection rule that matched events. Read it bottom-up: the matched events first (timestamps, source, user, process, network 5-tuple), then the rule logic (what condition fired), then the entity timeline (what else that user/host did that day). An alert without its raw events is a rumor.
- **Alert logic (Sigma):** detections are written as rules, and the shareable open format is Sigma — "YARA for logs": a YAML rule describing log events, convertible to SIEM query languages (S15). A Stage B reader should be able to read a Sigma rule and say what log evidence would satisfy it, and write one for an attack they just performed (e.g. "many 403s then a 200 on /admin" from B-VULN-02).
- **The defender's view of Stage B attacks:** for each B-VULN lesson, the lesson already names what defenders see — this lesson teaches the student to sit on the other side: given the attacker's request log, write the detection.
- **Primary sources:** Sigma format documentation (sigmahq.io, S15 — re-fetch at build); NIST SP 800-92 (Guide to Computer Security Log Management — lead, fetch at build); the site's own B-VULN lessons as attack ground truth.
- **Free resources (≤3):** SigmaHQ rule repository (read rules for attacks you know); LetsDefend/Botconf-style free SOC walkthroughs are leads — verify at build; Elastic's free detection-rules repo (lead, verify at build).
- **Lab target:** your own B-LAB targets — attack them, keep the access logs, then triage your own attacks as alerts.
- **Proof artifact:** three Sigma-style rules written for three attacks from B-VULN (one auth, one injection, one access-control), each with the log evidence that would fire it and one known false positive.
- **Prerequisites:** B-VULN-01–09 (you cannot detect what you cannot do).

---

## 8. Lesson B-BOUNTY — Bug bounty mechanics
**Level:** 2 → 3 when the reader's first report is accepted as valid (not necessarily paid).

- **How programs work:** an organization defines scope (assets in/out), rules of engagement (forbidden test types — typically DoS, social engineering, physical), and severity-tied rewards. Researchers test within scope, submit a report with reproduction steps and impact, the report goes through triage (platform or in-house), valid findings are rewarded, the company remediates and retests. Reports may be disclosed publicly afterwards (HackerOne Hacktivity). Program types: **public** (anyone), **private** (invite-only), **time-bound** (short sprints); plus **VDPs** (vulnerability disclosure programs — structured reporting without bounties, still legal safe harbor). (S11)
- **The three platforms:**
  - **HackerOne** — program types Private/Public/Time-bound; scope-first discipline; report → triage → bounty → remediation → retest; reputation/leaderboards as researcher currency alongside money. (S11, fetched)
  - **Bugcrowd** — anyone can sign up as a researcher; private programs may require identity verification; a valid bug is in-scope and reproducible by triage; first reporter wins; status flow Triaged → Unresolved → rewarded; kudos points feed leaderboards. (S12)
  - **Intigriti** — program visibility tiers Private/Application/Registered/Public; triage on all program types — every report is validated as in-scope, unique, and well-written before reaching the customer. (S13)
- **Reading disclosed reports:** HackerOne Hacktivity and platform disclosure pages are the textbook. Read for: how the researcher scoped, the reproduction steps' precision, how impact was argued (this is what separates paid from closed-as-informative), and what the fix was.
- **Writing the report:** the anatomy — title (vulnerability + location), severity with reasoning, prerequisites, step-by-step reproduction (exact requests), impact (what an attacker gains, concretely), remediation suggestion, supporting evidence (requests/responses, screenshots). Write for the triager: if they cannot reproduce it from your steps alone, it is not done.
- **Beginner discipline:** start on VDPs and wide-scope public programs; IDOR and access-control classes (B-VULN-01/02) are the highest-yield first hunts; never touch out-of-scope assets; duplicates are the tuition — read disclosed reports in your target area first.
- **Primary sources:** S11, S12, S13 (platform docs, fetched 2026-10-09).
- **Free resources (≤3):** HackerOne Hacker101 (free training, named on hackerone.com); disclosed reports on Hacktivity; Intigriti/Bugcrowd researcher docs.
- **Lab target:** none new — the report is written against a B-LAB target as a dry run, then submitted to a real program only inside its scope.
- **Proof artifact:** a complete dry-run report against a local target in the anatomy above, peer-reviewed against two disclosed reports.
- **Prerequisites:** B-AUTH, B-METH, B-VULN-01–09, B-DEF (triage thinking makes better reports).

---

## 9. Gap log

1. **PTES Technical Guidelines URL** returned HTTP 403 on fetch (S4). Phase list corroborated across multiple secondary sources; mark the guidelines URL `unreachable` in the site ledger and re-try from a different network at build time.
2. **PortSwigger per-topic URLs** (e.g. `/web-security/access-control/idor`): topic existence confirmed via the Academy index and community lab trackers; exact slugs not individually fetched — verify each at build time before linking.
3. **PortSwigger lab counts** ("18", "30", etc. from community trackers): the Academy grows; the site must write counts as "18+" style or pull from data, never as fixed numbers.
4. **DVGA port**: current docs say :5013, older mirrors say :5000 — re-verify at build time.
5. **Juice Shop / WebGoat install commands**: verified via README mirrors, not the canonical repos directly — re-fetch `github.com/juice-shop/juice-shop` and `github.com/WebGoat/WebGoat` at build time.
6. **SigmaHQ official repo**: official site sigmahq.io confirmed via docs; canonical `github.com/SigmaHQ/sigma` not directly fetched — verify at build.
7. **NIST SP 800-92** (log management, for B-DEF depth): not fetched this pass — fetch at build time.
8. **OWASP API Security Top 10 project page**: categories confirmed via multiple sources; primary project URL not directly fetched — fetch at build time.
9. **RFC 7519 / 6749** (for B-VULN-14 "Read the source"): named as primary leads; fetch at lesson-writing time.
10. **No live-system verification performed**: per brief §7, no scanning/probing during research — all lab commands are from project documentation, marked to be run by the lesson author at build time.
