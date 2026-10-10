# The Security Guidebook
### From absolute novice to employable security expert — a free learning and recognition pathway
*Companion to learncomputerstuff.dev — manuscript assembled 2026-10-09*

## Thesis

This guide takes you from zero to a working security professional — someone with a CVE credited in their name, a public track record, and a clear run at Anthropic's Cyber Verification Program. It is also a **recognition pathway, not just a learning path**: every stage shows you how to produce public, verifiable proof of skill — lab completions, bounty track records, disclosure history, CVE credits, certifications. That proof is what gets you hired without a degree. Employers don't hire certificates; they hire evidence. This guide builds your evidence at every step.

Everything here is free. Every stage, every exam's content, every skill — learnable with free resources and free tools. Where a certification or commercial tool exists, this guide covers what free material teaches its content, what knowledge it requires, and who it's actually for. No prices, no paid courses, no paid tools — the free path is the complete path.

## How to use this guide

- **Stages A→E are sequential.** Each stage's milestone is the gate to the next. Don't skip: Stage B assumes Stage A's mechanics, Stage C assumes Stage B's proof discipline.
- **The AI security certification track runs alongside Stages D–E.** It has its own prerequisite ladder — start it when you qualify, not before.
- **The career ladder section maps every stage to real work roles** (NICE framework) and tells you exactly what you can and cannot put on your CV.
- **Authorized targets only, always.** Labs, CTFs, and in-scope bounty targets. The ethics rules in the appendix are non-negotiable.

---

# STAGE A — FOUNDATIONS

*Goal: understand how computers, networks, and the web actually work. No vocabulary without mechanics.*

## Objectives

By the end of Stage A you can: administer a Linux system from the CLI; explain the TCP/IP stack, DNS resolution, and the TLS handshake; dissect any HTTP request and response; write Python tooling from scratch; tell hashing, encryption, and signatures apart and name the classic misuses; trace data flow through JavaScript and SQL.

## Lessons

### A1. Linux internals
Filesystem layout and what each top-level directory holds; permissions (octal and symbolic) and what breaks when they're loose; processes (ps, top, kill, signals); users, groups, and sudo; SSH with key-based auth; reading system logs; services and package management.
- **Free resources:** [OverTheWire: Bandit](https://overthewire.org/wargames/bandit) — learn Linux through progressive SSH security challenges; [Linux Journey](https://linuxjourney.com); *The Linux Command Line* by William Shotts (free PDF at linuxcommand.org).
- **Free tools:** Ubuntu/Debian in VirtualBox, or WSL2 on Windows; OpenSSH.
- **Labs:** (1) Complete Bandit levels 0–15 minimum, one command learned per level, in notes. (2) Permission lab: create users/groups/files, predict `ls -l` output, break something with 777, fix it, write the security consequence in one paragraph. (3) SSH hardening: fresh VM, key-only auth, no root login, verify from a second machine.
- **Recognition:** Bandit completion is public proof of CLI fluency; keep per-level notes on GitHub — your first public artifact.

### A2. Networking (TCP/IP, DNS, TLS)
The TCP/IP stack and what each layer does; the DNS resolution chain from stub resolver to authoritative server; the TLS handshake step by step (ClientHello → certificate validation → key exchange → encrypted session); reading packet captures; subnetting by hand.
- **Free resources:** [Professor Messer Network+ N10-009](https://www.professormesser.com) (free video series, current version); [Practical Networking](https://www.youtube.com/@PracticalNetworking) (free deep-dives); *Computer Networking: A Top-Down Approach* — Kurose & Ross (free companion site with Wireshark labs); Cisco Networking Academy / Packet Tracer (free).
- **Free tools:** Wireshark, tcpdump, dig, nmap (own machines and authorized targets only).
- **Labs:** (1) Capture your own traffic; isolate a DNS query/response, a TCP three-way handshake, and a TLS handshake with display filters; annotate each. (2) `dig +trace` a domain and explain every hop. (3) Subnet 10.0.0.0/16 by hand, verify with a calculator, build it in Packet Tracer.
- **Recognition:** annotated packet captures on GitHub demonstrate you read the wire, not just the textbook.

### A3. HTTP, deeply
Every part of a request/response: methods, status codes, headers; cookies and sessions — how state is maintained and where it leaks; JWT structure (header/payload/signature) and the `alg:none` and weak-secret failure modes; OAuth2/OIDC flows; what TLS protects and what it doesn't.
- **Free resources:** [PortSwigger Web Security Academy](https://portswigger.net/web-security) (free; starts at HTTP fundamentals — open your account here, it becomes the Stage B backbone); [MDN Web Docs — HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP).
- **Free tools:** curl (learn it deeply — the single most important HTTP tool), browser DevTools Network tab, jwt.io (decode only — never paste real secrets), OpenSSL CLI, httpbin.org (free request/response echo service).
- **Labs:** (1) Full login flow against httpbin.org with curl alone — GET, POST, redirects, cookies; explain every header in a write-up. (2) Decode sample JWTs at jwt.io by hand; explain why `alg=none` is catastrophic. (3) `openssl s_client` to real sites: read the chain, name the TLS version and cipher, state what a passive observer sees.
- **Recognition:** your curl write-ups and header-by-header explanations are portfolio pieces — this is the HTTP fluency employers test for.

### A4. Python for security tooling
HTTP requests and response parsing; basic sockets; parsing JSON/HTML/logs; argparse CLI tools; reading and modifying other people's security scripts.
- **Free resources:** [Python for Everybody](https://www.py4e.com); [Automate the Boring Stuff with Python](https://automatetheboringstuff.com) (full book free); the `requests` library docs.
- **Free tools:** Python 3, VS Code, pip + virtualenv.
- **Labs:** (1) Build a TCP connect port scanner from scratch with `socket` — no nmap import — then compare against nmap on your own VM and explain the differences. (2) Log parser: ingest an Apache/Nginx access log, output top IPs and status codes, flag probable scanning. (3) Python session client: log into a test app, hold the cookie, fetch a protected page, handle one error gracefully.
- **Recognition:** original tooling on GitHub — written from scratch, explained line by line — is the strongest Stage A proof there is.

### A5. Cryptography
Hashing vs symmetric encryption vs asymmetric encryption vs signatures — the correct use case for each; PKI and certificate chains; classic misuses (MD5/SHA1 for passwords, ECB mode, hardcoded keys, custom crypto); the rule: never roll your own crypto.
- **Free resources:** [CryptoHack](https://cryptohack.org) (free, gamified — scope to Introduction/General/Symmetric; the advanced RSA/ECC categories are Stage D material); Dan Boneh's *Cryptography I* (free audit); Latacora's "Cryptographic Right Answers" (free, current algorithm guidance).
- **Free tools:** OpenSSL CLI, Python hashlib/hmac, CyberChef (browser-based, runs locally).
- **Labs:** (1) Hash one password with MD5, SHA-256, and bcrypt; time a brute-force against the MD5 version — write why the timings end the argument. (2) The ECB penguin: encrypt a bitmap in ECB mode and see what leaks. (3) Verify a real site's certificate chain to its root with OpenSSL; explain what a privately installed CA enables.
- **Recognition:** CryptoHack progress is publicly verifiable; the misuse-ranking write-up shows judgment, not just knowledge.

### A6. Reading code
JavaScript: trace data flow from user input to a sink (DOM, fetch, eval). SQL: read queries and spot where injection could occur. Enough Python/PHP to follow a vulnerability in a lab app. Browser DevTools Sources tab: breakpoints and call stacks.
- **Free resources:** [javascript.info](https://javascript.info) (Data types + Advanced functions sections); [SQLBolt](https://sqlbolt.com) (interactive, in-browser); PortSwigger Academy (its labs increasingly require reading provided source).
- **Free tools:** DevTools, VS Code, ripgrep.
- **Labs:** (1) Trace user input → `innerHTML` sink on paper; mark the sink; name the vulnerability class. (2) Translate five increasingly complex SQL queries into plain English; circle every user-input entry point. (3) Breakpoint a button handler in DevTools; document the call stack in three sentences.
- **Recognition:** data-flow tracing write-ups show the exact skill AppSec employers screen for.

## Milestone check — Stage A exit

**Explain the full packet-to-render path of a login submission**, narrated in order: DNS resolution → TCP handshake → TLS handshake → HTTP POST → server session creation → Set-Cookie → authenticated requests → HTML/JS rendering — naming at each step what is encrypted, what is visible on the wire, and where the trust boundaries sit. Delivered as a written walkthrough or recorded narration, not multiple choice.

**Exit checklist:** Bandit 0–15+ with notes · annotated Wireshark capture (DNS, TCP, TLS) · curl-only login replay documented header by header · port scanner + log parser written from scratch · CryptoHack Introduction complete · misuse-ranking scenario answered · data-flow tracing exercise complete · packet-to-render walkthrough delivered.

## CV — Stage A

- **Can claim:** lab completions by name ("Completed OverTheWire Bandit; Wireshark packet-analysis labs"); concrete skills ("Linux CLI administration; TCP/IP and DNS fundamentals; Python scripting"); original tooling with links.
- **Cannot claim:** any professional security title; penetration testing ability; "cybersecurity experience"; vulnerability research; any certification not earned. Claiming "cybersecurity knowledge" here is the exact resume inflation this guide teaches you to avoid.
- **Unlocks:** Stage B. **Recognition so far:** public lab completions + original code on GitHub — proof of work without a degree, and it's only the beginning.

---
# STAGE B — PRACTITIONER

*Goal: find real vulnerabilities in authorized targets, prove them reproducibly, report them.*

## Objectives

By the end of Stage B you can: run the full 15-phase tool catalog in order; test to a methodology (not vibes); exploit the core web vulnerability classes manually; prove each finding with a reproducible PoC; write a professional report; operate inside scope without exception.

## Lessons

### B1. The tool catalog — 15 phases in activation order

A tool is activated only when it answers a specific research question, stays inside documented scope, and produces evidence you can explain without the tool. One primary proxy. Containers are convenient, not required.

1. **Scope and records** — a written record of what's allowed, what's excluded, which accounts you own, what you already tried. The most skipped phase and the one that prevents legal trouble. *Free: Obsidian or Markdown notes + Git (private storage only for confidential notes).* Lab: extract a HackerOne program's scope into a one-page scope sheet — the header of every later notebook.
2. **Interception proxy** — see exactly what the browser sent; modify and replay one field at a time. The foundation of all web testing. *Free (pick one primary): [Burp Suite Community](https://portswigger.net/burp/communitydownload) — Repeater teaches HTTP better than any textbook; [OWASP ZAP](https://www.zaproxy.org) — fully open source; [mitmproxy](https://mitmproxy.org) — scriptable in Python; [Caido Basic](https://caido.io) — free tier, modern alternative.* Lab: intercept a PortSwigger Academy login, send it to Repeater, change one field, document the request/response pair.
3. **Session isolation** — certainty about *which identity* sent a request. Authorization bugs are found by comparing two accounts; this phase makes the comparison trustworthy. *Free: separate browser profiles (one per test identity — enough; containers are a convenience, not a requirement); Firefox Multi-Account Containers; PwnFox.* Rule: confirm the cookie in the proxy, not the tab label. Lab: two accounts on Juice Shop in separate profiles; capture one authenticated request each; confirm in the proxy which cookie belongs to whom.
4. **Authorization comparison** — "did account A receive account B's object?" *Free: Burp's Autorize extension, AuthMatrix, Comparer.* Correction: automated tools still require manual interpretation — a flagged difference is a candidate, not a finding. Lab: do the comparison by hand on Juice Shop first, then through Autorize; compare what the tool caught, missed, and false-flagged.
5. **Asset discovery** — which names exist and which are live web apps. Everything here is a *candidate* — a name from recon is not permission to test it. *Free: subfinder, amass, dnsx, httpx (all ProjectDiscovery/OWASP); Shodan free queries.* Lab: on an explicitly scoped target, run subfinder → dnsx → httpx; produce a deduped live-app list; recheck every entry against the scope sheet.
6. **Crawling and history** — which paths the app or the public archive already exposed. *Free: katana, gau, waybackurls, browser DevTools.* Lab: crawl local Juice Shop with katana; pull archived URLs; diff; check each against scope.
7. **Content and parameter discovery** — "is this missing path or parameter real?" Brute-forcing is the noisiest phase; restraint is the skill. *Free: ffuf, SecLists (start with common.txt, not the 10-million-entry lists), Arjun.* Lab: ffuf against local DVWA at an explicit low rate; document the rate, the why, and what a real program's policy would allow.
8. **Data handling** — turn tool output into answers: dedupe, filter, keep the field that matters. *Free: jq, yq, ripgrep, anew, unfurl.* Lab: reshape httpx JSON into a clean target list with jq; pipe through anew twice; show the second run added zero lines.
9. **API contracts** — what the API *says* it does (spec), what changed between versions, what fails locally. *Free: Bruno (open source) or Postman (free tier); oasdiff (diffs OpenAPI specs); Schemathesis (generates tests from schemas).* Correction: oasdiff compares specifications, Schemathesis generates tests — **neither knows business authorization rules**; "user A must not see user B's object" stays manual (Phase 4). Lab: run OWASP crAPI locally; replay an authenticated request as a second user; diff two spec versions with oasdiff and state what the diff can and can't tell you.
10. **Tokens and callbacks** — identify what a token *is*, decode what it carries, confirm out-of-band callbacks (SSRF/blind-injection proof). *Free: JWT Editor / jwt_tool, CyberChef, interactsh (self-hostable; the free Burp Collaborator equivalent — Collaborator itself needs the commercial Burp edition).* Correction: a bearer token is **not** a JWT until the format is identified — opaque tokens are common. Lab: classify three `Authorization` headers (opaque vs JWT vs other) with structural evidence; decode the JWTs; fire one interactsh callback in a lab.
11. **Source analysis** — find where the permission check lives in code. Reading code beats guessing endpoints. *Free: VS Code, Git (`git log -S` / `git blame`), Semgrep (open source, 2,800+ community rules), CodeQL (free for public repos — private-repo use has licensing conditions, stated plainly).* Lab: clone a small open-source web app; flag one candidate with Semgrep; read the code by hand; deliver the verdict with file and line numbers.
12. **Dependencies and secrets** — "is a dependency already vulnerable, or is a secret in the repo?" — and nothing more. *Free: Trivy, Gitleaks, TruffleHog with verification **disabled**.* Hard rules: never validate a found credential by using it; a Trivy hit on a known CVE in a dependency is **not** a new CVE. Lab: triage one Trivy HIGH on a local lab image (reachable or not?); run Gitleaks on a test repo with a planted fake secret; document without using it.
13. **Local environment** — pin the exact version, reset dummy data at will, watch the check run. *Free: Docker/Compose (convenient, not required), language debuggers, local SQLite/Postgres.* Lab: stand up Juice Shop pinned; create two dummy users; reset the DB to a known state. This becomes the Phase 14 range.
14. **Reproduction** — prove someone else can rerun the finding; prove the fix blocks the forbidden call while legitimate access still works. *Free: curl (the minimal proof), Playwright (scripted browser flows), the project's own test suite (strongest fix validation).* Lab: write the Phase 4 IDOR as a curl one-liner *and* a Playwright script; write the fix's regression test (arrange two users; act: B requests A's object; assert 403/404 for B, 200 for A).
15. **Evidence** — the package: the request, the other user's dummy data, the timeline. *Free: Flameshot (annotated screenshots), Markdown reports, Dradis Community Edition (findings library, report templates).* Lab: assemble the full evidence package for the Phase 14 IDOR — scope sheet, annotated request/response, reproduction scripts, timeline, impact, remediation. **This package is the Stage B portfolio artifact.**

### B2. Methodology
Three standards, three jobs — they compose, they don't compete.
- **[OWASP Web Security Testing Guide (WSTG)](https://owasp.org/www-project-web-security-testing-guide/)** — *what to test, test by test.* 12 categories (information gathering; configuration; identity management; authentication; authorization; session management; input validation; error handling; weak cryptography; business logic; client-side; API testing), each with numbered cases (e.g., WSTG-SESS-05 is the CSRF test). Use during testing as the coverage checklist; professional reports cite these IDs. Companion: OWASP ASVS (requirements at three assurance levels — WSTG tests whether they're met).
- **[PTES](https://www.pentest-standard.org)** — *how to run the engagement.* 7 phases: pre-engagement → intel gathering → threat modeling → vulnerability analysis → exploitation → post-exploitation → reporting. Separates vulnerability *analysis* from *exploitation* — a flagged condition is not proof until deliberately, controllably exploited. Layer current tech guidance on top of its baseline.
- **[NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final)** — *the methodology framing.* The vendor-neutral citation for why testing is structured the way it is — use in reports and write-ups.
- **When to use which:** PTES structures the engagement (before/during); WSTG drives the technical testing (during); SP 800-115 justifies the methodology (in reporting).

### B3. The web hacking chain
Each class: how it works → how to find it → how to prove it. *Primary range: [PortSwigger Web Security Academy](https://portswigger.net/web-security) — free, the single best hands-on resource; its topic list is the curriculum.* Lab counts below are "at least" floors, verified October 9, 2026 (SQLi 18, access control 13, XSS 30, SSRF 7, command injection 5, JWT 8, XXE 9, deserialization 10, race conditions 6, CSRF 14); PortSwigger adds labs over time, so re-count at build time.
- **Broken access control & IDOR** — the app checks authentication but not authorization on an object reference (`/api/orders/1024` → change the ID → another user's data). Horizontal, vertical, forced browsing, method override, workflow bypass. Find: proxy everything with two accounts; replay each ID-carrying request as the other user. Prove: Repeater — victim object with attacker session returns 200 + victim data; negative control (no session → 403/401). Highest-ROI beginner topic — most first bounties are IDORs. *PortSwigger: 13+ access-control labs. Self-hosted: Juice Shop ("View/Manipulate Basket", "Forged Feedback").*
- **SQL injection** — input concatenated into queries. UNION-based, error-based, blind (boolean/time), second-order, out-of-band. Find: single quote in every input; confirm with `AND 1=1` vs `AND 1=2`. Prove: manual UNION sequence (column count → text columns → information_schema → target table), every request/response recorded. sqlmap is legitimate *here* — pointed at a confirmed injection in a lab to learn its workflow — but the manual proof is the skill. *PortSwigger: 18+ labs. Self-hosted: DVWA (Low/Medium/High/Impossible), Juice Shop "Login Bender".*
- **OS command injection** — input reaches a shell (`shell_exec("ping " . $_GET['ip'])`). Inject `;`, `|`, `&&`, backticks, `$()`. Blind variants need time delays or out-of-band confirmation. *PortSwigger: 5+ labs. Self-hosted: DVWA command injection module, bWAPP.*
- **API abuse** — modern apps are API-first. [OWASP API Security Top 10](https://owasp.org/API-Security/): broken object-level authorization (IDOR at API scale — the #1 real API bug), broken authentication, mass assignment (`"role":"admin"` accepted), broken function-level authorization, unrestricted consumption, misconfiguration. Find: build an endpoint × role matrix (admin, user A, user B, unauthenticated) per endpoint; test method tampering, rate limits, verbose errors. *PortSwigger: API testing + GraphQL labs. Self-hosted: [OWASP crAPI](https://github.com/OWASP/crAPI) (compose up → :8888), VAmPI, DVGA for GraphQL.*
- **SSRF** — the server fetches an attacker-influenced URL. Point it internal: `http://169.254.169.254/` (cloud metadata — the highest-impact variant), `http://localhost/admin`. Find: URL previews, import-from-URL, avatar-by-URL, webhook testers — submit a callback URL first to prove server-side fetch. Prove: metadata/internal content in response, or callback log. Discipline: read-only proof of the metadata endpoint; never exfiltrate real credentials. *PortSwigger: 7+ labs (incl. cloud metadata chain).*
- **XSS** — attacker JS in the victim's origin: reflected, stored, DOM-based (source → sink tracing: `location.hash` → `innerHTML`). Contexts (HTML, attribute, JS, URL) need different breakouts. Prove: `alert(document.domain)` in labs; professionally, a payload demonstrating impact without harm (same-origin fetch showing session riding — never exfiltrate unless scope explicitly permits). *PortSwigger: 30+ labs — the largest topic. Self-hosted: DVWA reflected/stored modules, Juice Shop, Google's XSS Game.*
- **CSRF** — cross-site requests ride the victim's cookies. Find: state-changing requests; remove the token — does it still work? Is it validated, session-tied, or static? GET-based actions? Prove: minimal auto-submitting HTML PoC in two browsers; show the state change. *PortSwigger: 12+ labs. Self-hosted: DVWA CSRF module.*
- **Business logic flaws** — the code works; the *workflow* is abusable. Negative quantities, coupon stacking, workflow skipping, client-side price trust, race conditions on limited offers. No scanner finds these — they require understanding what the app is *for*, which is why they're among the most rewarding bounty classes. Find: draw the intended workflow; attack the model (quantity = -1? replay step 2? two simultaneous redemptions?). Prove: the deviation + business impact in business terms ("attacker purchases goods at negative cost"). *PortSwigger: 11+ labs. Self-hosted: Juice Shop ("Payback Time", "Manipulate Basket", "Christmas Special").*
- **SSTI** — input embedded in server templates (Twig, Jinja2, Freemarker). Fingerprint: `{{7*7}}` → `49`. Escalate via engine introspection (labs only). *PortSwigger: 7+ labs.*
- **XXE** — XML parsers resolving external entities: file disclosure (`file:///etc/passwd`), SSRF, billion-laughs DoS. Fix: disable DTDs/external entities. *PortSwigger: 9+ labs. Self-hosted: WebGoat, bWAPP.*
- **Insecure deserialization** — attacker bytes → objects (Java `readObject`, PHP `unserialize`, Python `pickle`). Spot the blobs: base64 `rO0` (Java), `O:` (PHP), `gASV` (pickle). Stage B teaches recognition; deep exploitation is Stage D. *PortSwigger: 10+ labs.*
- **JWT attacks** — `alg:none`, RS256→HS256 confusion, weak HMAC secrets, `kid` injection, `jku`/`x5u` SSRF. Always verify the token is actually a JWT first. Prove: forged `{"sub":"administrator"}` token accepted. *PortSwigger: 8+ labs. Self-hosted: Juice Shop JWT challenges; jwt_tool after manual learning.*
- **OAuth/OIDC flaws** — unvalidated `redirect_uri` (code/token theft), missing `state` (login CSRF), replayed codes. Prove: code delivered to attacker-controlled redirect URI, or victim logged in as attacker. *PortSwigger: 6+ labs.*
- **Race conditions** — check-then-act non-atomically: parallel requests redeem the same coupon. Prove: sequential baseline vs parallel burst outcomes. *PortSwigger: 6+ labs.*
- **Supporting classes** — file upload (unrestricted → webshell; DVWA module), path traversal (`../../etc/passwd`; DVWA file inclusion), NoSQL injection (`{"$gt":""}`).

### B4. Practice labs — the free range
- **Browser-based:** [PortSwigger Web Security Academy](https://portswigger.net/web-security) (the backbone), [Google Gruyere](https://google-gruyere.appspot.com) (absolute beginners), [XSS Game](https://xss-game.appspot.com), [Hacker101](https://www.hacker101.com).
- **Self-hosted (Docker):** `vulnerables/web-dvwa` (DVWA) · `bkimminich/juice-shop` (Juice Shop — the most realistic) · `webgoat/webgoat` (guided) · `raesene/bwapp` (100+ vulns) · OWASP crAPI (API Top 10) · DVGA (GraphQL) · [VulnHub](https://www.vulnhub.com) VMs (Kioptrix, DC series for full chains).
- **Guided platforms:** [TryHackMe](https://tryhackme.com) and [HackTheBox](https://www.hackthebox.com) free tiers; [CTFtime](https://ctftime.org) for time-boxed authorized practice.

### B5. Defensive basics
SOC triage workflow: alert → context → scope → contain → document. Reading SIEM alerts: what fired, why, what the log actually says vs what the rule assumed. Alert logic: true positive, false positive, benign true positive — and how each gets handled differently.
- **Free resources:** [LetsDefend](https://letsdefend.io) (free tier — SOC simulations), [CyberDefenders](https://cyberdefenders.org) (free tier — blue-team challenges), SANS DFIR posters (free cheat sheets).

### B6. Bounty mechanics
**HackerOne** (largest): public programs (open, competitive) and private programs (invite-only, better signal). Report lifecycle: submit → triage → validation → bounty/severity decision → fix → disclosure (Hacktivity — a public learning goldmine). Reputation (signal + impact) gates private invites. **Bugcrowd:** P1–P5 priority scale via the Vulnerability Rating Taxonomy; crowd analysts triage first. **Intigriti:** EU focus, strict scope enforcement, smaller researcher pool — less duplication racing. Also: YesWeHack, OpenBugBounty (non-paid disclosure — good practice ground).
- **The policy page is your authorization.** Read scope, out-of-scope, forbidden test types (no DoS, no social engineering, no aggressive scanning), and the safe-harbor clause. Scope is sacred — out-of-scope testing risks bans and legal exposure.
- **Realistic expectations:** first bugs typically take weeks to months; duplicates are common on public programs; the long-term goal is private invites, earned via reputation, not volume.
- **Learn from disclosed write-ups (free, highest-ROI study):** [HackerOne Hacktivity](https://hackerone.com/hacktivity), [PentesterLand writeup archive](https://pentester.land/writeups), Bugcrowd disclosures, researcher blogs. Method: read a writeup → reproduce the *class* (not the target) in a lab → add the technique to your methodology checklist.

## Milestone check — Stage B exit

**First valid submitted finding** on an authorized target — a report with reproducible steps, request/response evidence, impact, and remediation, accepted by a program or lab reviewer. Plus: the Phase 15 evidence package for one finding, portfolio-ready.

## CV — Stage B

- **Can claim:** bug bounty platform profile with accepted findings (link it); PortSwigger Academy progress; methodology literacy (OWASP WSTG, PTES); reproducible PoC reports; scope and authorization discipline.
- **Cannot claim:** CVE credits; "penetration tester" as a job title unless employed as one; CVSS scoring authority; consulting experience; exploit development.
- **Unlocks:** Stage C. **Recognition so far:** a public bounty profile with accepted findings + a portfolio evidence package — verifiable proof you find real bugs in real systems, no degree required.

---
# STAGE C — PROFESSIONAL

*Goal: coordinated disclosure done right; a CVE with your name on it; the hireable line.*

## Objectives

By the end of Stage C you can: run a coordinated disclosure from finding to publication; request a CVE ID through the right CNA; score vulnerabilities in CVSS v3.1 and v4.0 with worked examples; classify with CWE and prioritize with the KEV catalog; write a public write-up worth reading. This is the stage that makes you employable.

## Lessons

### C1. Coordinated vulnerability disclosure, end to end
The pipeline: **finding → validation → vendor contact → acknowledgment → patch window → CVE request → publication.**
- **Vendor contact:** the project's security policy or `/.well-known/security.txt` first — it names the right channel and the expected timeline. Never test-first-and-ask-later.
- **The patch window:** Google Project Zero's published policy is the industry's best-known model — **90+30**: 90 days for patch development, plus 30 days of patch-adoption time before technical details publish if the bug is fixed in the window (immediate release if unpatched at day 90); a 7-day deadline for vulnerabilities exploited in the wild. The embargo protects users, not vendors — honor it exactly.
- **Real cases to study:**
  - *Good — Log4Shell (CVE-2021-44228), Dec 2021:* privately reported to Apache on Nov 24; CVE reserved Nov 25; a PoC leaked early on Dec 9; Apache shipped 2.15.0 on Dec 10. Textbook coordination — and the lesson is why the embargo exists: even good process can be broken by a leak.
  - *Good but criticized — Heartbleed (CVE-2014-0160), Apr 2014:* privately reported, patched in 6 days — coordination working. But only a tiny circle got early warning while everyone else scrambled, and the branded launch site looked like marketing. Lesson: coordination means *broad* notification, not just your friends.
  - *Bad — SandboxEscaper's Windows zero-days, 2018:* full PoCs dropped on Twitter with no vendor notice, out of frustration with a bounty program. Exploits were found in the wild before patches. Lesson: uncoordinated disclosure burns users, hands attackers working code, and attaches your name to the incident instead of the finding. Full-disclosure drops are a career-ending move on the professional track.
- **Free resources:** the [OpenSSF guide to coordinated disclosure](https://github.com/ossf/oss-vulnerability-guide); CERT/CC vulnerability reporting guidance.
- **Lab:** reconstruct the Log4Shell disclosure timeline from public sources (report → CVE reservation → leak → patch → CISA directive); write what each party did right or wrong.
- **Recognition:** a clean disclosure history — vendors who will vouch that you handled it right — is professional reputation you can't buy.

### C2. The CVE program
- **What it is:** the common dictionary of public vulnerabilities. [MITRE](https://www.cve.org) operates the program (under contract with CISA); the canonical `CVE-YYYY-NNNNN` identifier lets every scanner, database, and team talk about the same flaw. The program passed 300,000 CVE Records in 2025 (cve.org metrics).
- **The CNA hierarchy (federated, not centralized):** Top-Level Roots (MITRE, CISA; ENISA for Europe) → Roots (Red Hat, Google, JPCERT/CC...) → **CNAs** — **555 participating organizations as of October 9, 2026** (552 CNAs + 3 CNAs of Last Resort), across **43** countries (cve.org/ProgramOrganization/CNAs — the figure moves, date it when citing): software vendors (for their own products), open-source ecosystems (Linux kernel, curl, Python; GitHub for GitHub-hosted projects), bug bounty platforms (HackerOne is a CNA), research organizations, coordinating bodies (CERT/CC). **CNA of Last Resort** (MITRE primarily) covers products no other CNA's scope reaches. **ADP** (Authorized Data Publisher, e.g., CISA) enriches records but doesn't assign IDs.
- **How a researcher requests a CVE ID:** (1) qualify the finding — exploitable code with negative impact on confidentiality, integrity, or availability; independently fixable; one codebase; check for duplicates first. A framework SQLi qualifies; one company's misconfigured bucket does not. (2) Contact the vendor in good faith via their security policy. (3) Find the right CNA — vendor if they're one, ecosystem CNA for open source, research CNA or bounty platform, CNA-LR as last resort (partner list at cve.org). (4) Fallback: the CVE web form. (5) Receive the ID — not public yet. (6) Coordinate disclosure timing. (7) Publication; NVD ingests it. **Anyone can request a CVE — no credential or professional status required. What matters is the finding.**
- **The record (CVE JSON 5.x):** `cveMetadata` (ID, assigning CNA, state: PUBLISHED / RESERVED / REJECTED); `containers.cna` — title, English description, `affected[]` (products, version ranges), `problemTypes[]` (CWE IDs), `references[]`, `metrics[]` (CVSS), and `credits[]` — **the `finder` entry is where your name goes**. `containers.adp[]` carries enrichment like KEV status.
- **[NVD](https://nvd.nist.gov)** (NIST) enriches published records with CVSS scores, CWE mapping, and CPE product identifiers — where most scanners and employers actually consume CVE data. **Current policy (announced 2026-04-15, confirmed via DoC OIG report OIG-26-020-I): NVD only enriches vulnerabilities meeting new prioritization criteria** (CISA KEV with 1-business-day target, federal software, EO 14028 critical software) and no longer assigns a score to every vulnerability; the rest go to **"Not Scheduled"**; pre-2026-03-01 unenriched CVEs were reclassified the same way. Enrichment requests go to nvd@nist.gov.
- **Lab:** look up CVE-2021-44228 on cve.org and nvd.nist.gov; compare CNA data vs NVD enrichment. Read one raw CVE JSON record; find the finder credit, the affected range, the metrics block. Fill a mock CNA `affected` + `descriptions` block for one of your Stage B lab findings.

### C3. CVSS v3.1 and v4.0
- **What it is:** the [FIRST.org](https://www.first.org/cvss/) standard — the severity language employers, vendors, and scanners use to prioritize. The vector string is mandatory alongside the score; a score without a vector is unverifiable.
- **Severity bands (both versions):** None 0.0 · Low 0.1–3.9 · Medium 4.0–6.9 · High 7.0–8.9 · Critical 9.0–10.0.
- **v3.1 metric groups:** Base Exploitability (Attack Vector, Attack Complexity, Privileges Required, User Interaction, Scope — whether impact escapes the vulnerable component); Base Impact (Confidentiality, Integrity, Availability); Temporal (exploit maturity, remediation level, report confidence); Environmental (your context retunes the score).
- **v4.0 changes:** Attack Complexity splits out **Attack Requirements** (prerequisites like a MITM position); User Interaction becomes three-valued (None / Active / Passive); Scope becomes explicit **Vulnerable-system vs Subsequent-system** impact (subsequent systems include human safety); Temporal becomes **Threat** (Exploit Maturity — active exploitation raises, unreported lowers); new **Supplemental** metrics (Safety, Automatable, Recovery — never change the score, add prioritization context). Scores are labeled by input: CVSS-B (base), -BT, -BE, -BTE.
- **Worked examples (from FIRST's official CVSS v4.0 Examples, doc v1.8 — verified 2026-10-09; FIRST revises this document, so re-check before citing. Vectors below are complete — FIRST's license requires publishing score + vector together):**
  - *CVE-2022-41741 (NGINX mp4 memory corruption):* v3.1 `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` → **7.0**; v4.0 `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` → **7.3**. The "high complexity" becomes low complexity with attack requirements present — same band, cleaner reasoning.
  - *CVE-2020-3549 (Cisco FMC/FTD MITM):* v3.1 `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` → **8.1**; v4.0 base `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` → **7.7**; v4.0 Base+Threat → **5.2** (append `/E:U` — Exploit Maturity Unreported). Two lessons at once: refined metrics shift base slightly, and Threat metrics move it a full band (High → Medium) when no exploit code is known. Scores are meant to move with threat intelligence.
  - *CVE-2023-3089 (OpenShift FIPS):* v3.1 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` → **7.5**; v4.0 base `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N` → **8.3** — v4.0 scores it *higher*, capturing confidentiality impact on high-assurance systems better.
  - *CVE-2021-44228 (Log4Shell):* v3.1 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` → **10.0**; v4.0 `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:A` → **9.3 (Base+Threat)**. The famous 10.0 does *not* survive the v4.0 revision: FIRST's updated analysis constrains all impact to the vulnerable system (subsequent systems: none — hardware/firmware/software on one box count as a single system). Even the canonical worst case moves between versions.
  - *CVE-2013-6014 (Juniper Proxy ARP DoS) — the sharpest band disagreement:* v3.1 `AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:H` → **9.3 (Critical)**; v4.0 `AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:H/SI:N/SA:H` → **6.4 (Medium)**. The v3.1 Scope-Changed multiplier drove it to Critical; v4.0's explicit subsequent-system accounting (low impact on the vulnerable system, high on subsequent systems) compresses it to Medium. The mechanism to remember: v3.1 scope-inflated scores are exactly where severity *bands* move between versions.
- **Common mistakes:** scoring your deployment instead of the vulnerability (your firewall belongs in Environmental); UI:N on anything needing a victim click; Scope Changed on reflected XSS affecting only the victim's own session; publishing a score with no vector.
- **Free tools:** the [NVD CVSS calculators](https://nvd.nist.gov/vuln-metrics/cvss) (v3.1 and v4.0); FIRST's free self-paced CVSS v4.0 course.
- **Lab:** score five real CVEs in both versions with the NVD calculator; write up every disagreement and which metric caused it. Re-score one CVE you disagree with, justifying each metric in writing.
- **Recognition:** CVSS fluency is table stakes in professional reports; scoring write-ups in your portfolio prove you speak the industry's severity language.

### C4. CWE, CAPEC, and the CISA KEV catalog
- **[CWE](https://cwe.mitre.org) (Common Weakness Enumeration):** the taxonomy of weakness *kinds*. The annual **CWE Top 25** (2025 edition, ranked by CVE prevalence × severity; KEV counts = CVEs on CISA's exploited list). Web-relevant entries marked (W) — a Stage B graduate should be able to define, find, and fix every one of them: #1 CWE-79 XSS (W, 7 KEV) · #2 CWE-89 SQL injection (W, 4 KEV) · #3 CWE-352 CSRF (W) · #4 CWE-862 missing authorization (W, up from #9 — the check was never written; IDOR hunting ground) · #5 CWE-787 out-of-bounds write (12 KEV) · #6 CWE-22 path traversal (W, 10 KEV) · #7 CWE-416 use-after-free (14 KEV — highest KEV count on the list) · #8 CWE-125 out-of-bounds read (3 KEV) · #9 CWE-78 OS command injection (W, 20 KEV — the most KEV-exploited weakness overall) · #10 CWE-94 code injection (W, 7 KEV — SSTI, eval) · #11 CWE-120 classic buffer overflow (new entry) · #12 CWE-434 unrestricted file upload (W, 4 KEV) · #13 CWE-476 null-pointer dereference (up from #21) · #14 CWE-121 stack-based buffer overflow (new, 4 KEV) · #15 CWE-502 deserialization (W, 11 KEV — gadget chains) · #16 CWE-122 heap-based buffer overflow (new, 6 KEV) · #17 CWE-863 incorrect authorization (W, 4 KEV — the check exists but is wrong; your Stage B authorization-comparison phase lives here) · #18 CWE-20 improper input validation (W, 2 KEV — the root cause behind half the list) · #19 CWE-284 improper access control (W, new, 1 KEV) · #20 CWE-200 sensitive information exposure (W, 1 KEV) · #21 CWE-306 missing authentication for critical function (W, 11 KEV, up from #25) · #22 CWE-918 SSRF (W) · #23 CWE-77 command injection (W, 2 KEV) · #24 CWE-639 authorization bypass through user-controlled key (W, up from #30 — the formal name for IDOR) · #25 CWE-770 allocation of resources without limits (W — rate-limit/DoS class). **17 of the 25 are web-application weaknesses.** Movers vs 2024: the access-control family is climbing (862, 306, 639) — that's where the action is.
- **[CAPEC](https://capec.mitre.org):** attack patterns — the *how* to CWE's *what*. Each pattern links to its CWE root causes.
- **[CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog):** vulnerabilities *known to be exploited in the wild* — free, machine-readable, with public nominations. **Current federal rule: BOD 26-04** "Prioritizing Security Updates Based on Risk" (issued June 10, 2026, replacing BOD 22-01, referenced on the KEV catalog page) — remediation deadlines are now set by a four-factor risk model: public exposure × KEV status × automatability × technical impact. A flaw hitting all four gets **3 days plus mandatory forensic triage**; weaker combinations get up to two weeks. Private-sector teams increasingly borrow this model. Why employers screen on it: a KEV entry means *proven attacker interest*, not theoretical severity. A CVSS 9.8 nobody exploits vs a CVSS 7.5 in active ransomware campaigns — KEV answers which to patch first. Note what's instructive: XSS (#1 overall) has only 7 KEV entries — attackers exploit what's weaponizable at scale, not just what's common. The interview-ready rule: KEV first, then CVSS plus exploit maturity.
- **Lab:** map your five favorite Stage B vuln classes to CWE IDs from memory, then check. Pull the KEV JSON; pick three entries and read their NVD pages — what made each exploitable at scale? Trace one CVE → CWE → CAPEC → KEV status in one paragraph.

### C5. The public track record — write-ups that teach
The quality bar (distilled from Google Project Zero's blog and PortSwigger Research — both free to study):
1. **Reproducible** — exact steps, versions, environment; request/response pairs beat prose.
2. **Root cause, not symptom** — "user input flows unsanitized from `search.php:42` into a concatenated query," with the code path shown.
3. **Honest impact** — state what you *proved*, not what you imagine. "Arbitrary file read as the web user" beats "potential full server compromise" you never demonstrated. CVSS inflation destroys credibility.
4. **Remediation advice** — the fix at the code level. This separates a report from a complaint.
5. **Full timeline** — discovery → report → vendor response → patch → publication.
6. **Teaches something** — a new technique, a defense bypass, a pattern others can hunt. This is what gets shared and cited.
7. **Maintainer-first tone** — no grandstanding, no shaming vendors before the embargo lifts.
- **Study:** Google Project Zero blog archive, PortSwigger Research, HackerOne Hacktivity disclosed reports, the PentesterLand write-up archive.
- **Lab:** write one Stage B lab exploit to this standard — title, summary, affected versions, repro steps, PoC, proven impact, root cause with code reference, remediation, references. If it wouldn't survive a vendor's triage queue, rewrite until it would.
- **Recognition:** public write-ups are permanent, searchable proof of how you think. One excellent write-up outweighs ten vague ones, and hiring managers read them.

### C6. CVP Defense Access — the individual milestone
[Anthropic's Cyber Verification Program](https://www.anthropic.com/news/cyber-verification-program) (announced October 6, 2026) has three tiers. **Defense Access** covers defensive work — SOC and incident-response tasks, malware reverse-engineering, vulnerability analysis and validation — and qualifying examples explicitly include **individual researchers with a track record of reported vulnerabilities**, alongside company security teams, critical infrastructure operators of any size, smaller firms, open-source maintainers, universities, and government bodies. Applications are answered within days. That's the currency: not a certificate, but proof you've found and disclosed real flaws — exactly what Stage C builds. Red Team and Specialized tiers are organization-only (Stage E).
- **Supporting signal:** Anthropic's own testing showed Defense Access completing defensive security tasks that standard access blocks — the tiering is mechanically real. Project Glasswing partners verified 129,000+ vulnerabilities in one quarter.
- **Lab:** map your Stage C portfolio (CVEs, disclosures, write-ups) against the Defense Access qualifier; write the one-paragraph summary you'd put in the application.

## Milestone check — Stage C exit

**A CVE credited in your name.** A public CVE record with you in the `credits[]` finder field, earned through coordinated disclosure — validated, scored, classified, published. Plus: one publication-grade write-up.

**Exit checklist:** explain CVD end-to-end with Log4Shell/Heartbleed/SandboxEscaper lessons · walk a CVE request path (which CNA, what the record needs, pre-publication state) · read a raw CVE JSON 5.x record and point to finder credit, affected range, metrics · score 5 real CVEs in v3.1 and v4.0, explaining disagreements · map 10 web vuln classes to CWE IDs; explain KEV-over-CVSS prioritization · one write-up meeting the quality bar.

## CV — Stage C

- **Can claim:** CVE IDs credited by name — list each (`CVE-YYYY-NNNNN` with a one-line description); coordinated disclosure history with vendors; public write-ups; CVSS scoring competence (v3.1 + v4.0); CWE classification fluency.
- **Cannot claim:** security leadership or program ownership; CISSP-level breadth; specialist depth in any D track; management experience.
- **Unlocks:** Stage D — and CVP Defense Access eligibility. **Recognition so far:** a CVE with your name on it is the single strongest hireability signal in this industry that doesn't require anyone's permission to earn — no degree, no employer, no gatekeeper. This is the line where "aspiring" becomes "professional."

---
# STAGE D — SPECIALIST

*Goal: deep, employable expertise in one direction. Pick a track, go deep.*

## Objectives

Stage D is where breadth becomes depth. You've proven you can find and disclose vulnerabilities; now you master one domain the way professionals do. Pick the track that fits how you think — each is a complete career direction with free resources all the way down.

## Track 1 — Red team operations

**What it is:** authorized adversary emulation — operating like a real threat actor against an organization, with defined objectives, rules of engagement, and a debrief that improves the defenders. A pentest asks "what vulnerabilities exist"; a red team asks "can you detect and stop me achieving this objective."

**Core knowledge:**
- **[MITRE ATT&CK](https://attack.mitre.org)** — the shared language. Tactics (the "why," **15 tactics as of v19.2, April 2026** — Defense Evasion split into **Stealth** and **Defense Impairment**; any source listing 14 is stale), Techniques (the "how," e.g., T1059), sub-techniques, procedures, plus Groups, Software, Mitigations, Detections. Map every engagement action to technique IDs; the free ATT&CK Navigator builds coverage heatmaps.
- **Adversary emulation** — plan from threat intel: pick an actor profile, replicate their TTPs in order, stay inside the rules of engagement. *Free practice: [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) — small ATT&CK-mapped tests that validate detections.*
- **C2 infrastructure concepts** — listeners, redirectors, malleable profiles, OPSEC (infrastructure separation, burnable domains, jitter/sleep). *Free to learn: Sliver, Mythic, Havoc, Covenant; the open-source C2 Matrix comparison.*
- **Evasion concepts** — AMSI bypass, ETW tampering, living-off-the-land binaries ([LOLBAS](https://lolbas-project.github.io)), obfuscation. The mindset shift from pentesting: not just access, but *undetected* access.
- **Purple teaming** — red and blue collaborating: run an Atomic test, check the detection, tune, re-run. "Red teamer who can talk to blue" is the hireable profile.
- **Active Directory** — the center of gravity for enterprise work: Kerberos attacks (Kerberoasting, AS-REP roasting, ticket attacks), lateral movement, [BloodHound Community Edition](https://github.com/SpecterOps/BloodHound) (free) for attack-path mapping.
- **Free labs:** TryHackMe red-team paths (free tier), DetectionLab (free — builds a logging lab with Sysmon), ATT&CK Navigator.
- **Certifications (what they validate, free prep path):** CRTO (Zero-Point Security) — practical red-team operator exam, Cobalt-Strike-based, AD-focused; OSCP (OffSec PEN-200) — the HR filter, 24-hour practical + report; OSEP (PEN-300) — advanced pentesting/evasion; PNPT (TCM Security) — practical with a live debrief simulating consulting. *Free prep for all: HackTheBox/TryHackMe machines, ATT&CK-mapped practice, published exam-topic outlines.*
- **Recognition:** CTF rankings, published emulation plans, purple-team detection write-ups — operators are hired on demonstrated tradecraft.

## Track 2 — DFIR (Digital Forensics & Incident Response)

**What it is:** what happened, how, when, and what's the blast radius. Forensics (evidence collection and analysis) plus incident response (containing and eradicating the threat). Among the highest-demand defensive specializations.

**Core knowledge:**
- **IR lifecycle — [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) (April 2025, a CSF 2.0 Community Profile; Rev. 2 withdrawn April 3, 2025):** organized around the CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond, Recover) with incident response sitting at Detect → Respond → Recover. Know it cold — and know its predecessor's four phases (Preparation → Detection & Analysis → Containment, Eradication & Recovery → Post-Incident Activity) too, because every IR interview still references them.
- **Forensic artifacts:** *Disk* — MFT, registry hives (SAM/SECURITY/SYSTEM/SOFTWARE, NTUSER.DAT), event logs, prefetch, Shimcache/Amcache, USN journal, browser artifacts, LNK files. *Memory* — process lists, injected code, credentials in memory; analysis with [Volatility 3](https://www.volatilityfoundation.org) (free). *Network* — full packet capture, Zeek logs, DNS logs. *Cloud* — CloudTrail / Activity Log (API history is cloud forensics).
- **Threat hunting — the hypothesis method:** form a hypothesis ("APT29 uses scheduled tasks for persistence — do we see anomalous schtasks?"), identify data sources, test, document. ATT&CK for hypothesis generation.
- **Detection engineering:** [Sigma](https://github.com/SigmaHQ/sigma) (write once, convert to Splunk/Elastic/Sentinel queries) and [YARA](https://virustotal.github.io/yara/) (file/malware pattern matching). Lab: write a Sigma rule for a technique you ran in Atomic Red Team — the purple-team loop.
- **Timeline analysis:** super-timelines (Plaso/log2timeline) correlating host + network + identity into one narrative.
- **Free tools:** [Eric Zimmerman's tools](https://ericzimmerman.github.io) (Windows forensics gold standard), [Velociraptor](https://www.velocidex.com) (endpoint visibility at scale), [REMnux](https://remnux.org), SIFT Workstation, Security Onion + Zeek, SANS DFIR posters.
- **Free labs:** [CyberDefenders](https://cyberdefenders.org) (free tier — forensic challenges), [LetsDefend](https://letsdefend.io) (free tier — SOC simulations).
- **Certifications (what they validate, free prep path):** BTL1/BTL2 (Security Blue Team) — practical blue-team exams with strong community reputation; GIAC GCFE/GCFA/GNFA — the DFIR gold standards; eCIR (INE) — practical IR. *Free prep: CyberDefenders challenges, Zimmerman's tool docs, NIST SP 800-61.*
- **Recognition:** published Sigma/YARA rules with real detections, CTF forensics write-ups, challenge completions — artifact work is publicly verifiable and scarce.

## Track 3 — Application Security (AppSec)

**What it is:** making software secure by design and by verification — finding vulnerabilities in code before attackers find them in production, and building the processes that prevent recurrence. For people who like code and systems thinking.

**Core knowledge:**
- **Threat modeling:** STRIDE (Microsoft), PASTA (risk-centric), attack trees; [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon) (free). STRIDE for design reviews, PASTA for risk-driven programs.
- **Testing types:** SAST (source analysis — early, scalable, false positives), DAST (running app — real findings, late), IAST (agent inside the app), SCA (vulnerable dependencies — the Log4Shell lesson), manual code review (the highest-value skill — tools assist, humans find logic flaws).
- **Secure SDLC:** where gates go — requirements (abuse cases), design (threat modeling), implementation (secure coding standards, pre-commit hooks), verification (SAST/DAST in CI), release (signing, SBOMs), response (vuln SLAs). [OWASP SAMM](https://owaspsamm.org) (free) for program maturity.
- **Code review technique:** trust boundaries, input-to-sink tracing, auth/authz at every layer, the "boring" bugs (IDOR, mass assignment, logic). [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/) (free).
- **Standards:** [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) (the requirements bible, free), OWASP Top 10 / API Top 10, [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) (free).
- **Free tools:** [Semgrep](https://semgrep.dev) (open source, OWASP rulesets — write custom rules), [CodeQL](https://codeql.github.com) (free for public repos; private-repo use has licensing conditions), Bearer, Bandit (Python), gosec (Go), Brakeman (Ruby), OWASP Dependency-Check.
- **Free labs:** WebGoat, Juice Shop (test your tooling against them), PortSwigger Academy (validates what scanners find).
- **Certifications (what they validate, free prep path):** GWAPT (GIAC) — AppSec pentest standard; OSWE (OffSec WEB-300) — white-box web exploitation, the technical hiring manager's favorite; CSSLP (ISC2) — management-leaning secure software. *Free prep: Semgrep custom rules, OWASP materials, code-review practice on open source.*
- **Recognition:** published Semgrep rules, CVEs found through code review, AppSec write-ups — every company shipping software needs this, and people who can actually read code are thin on the ground.

## Track 4 — Exploit development & reverse engineering

**What it is:** the deep end — software at the machine level: how binaries work, how memory corruption becomes code execution, how to analyze software with no source. The hardest track, the scarcest skill set.

**Core knowledge (learn in order — each mitigation exists because the previous technique worked):**
- **Binary basics:** ELF/PE/Mach-O formats, stack vs heap, calling conventions, x86-64 assembly reading (ARM increasingly relevant).
- **Debuggers:** x64dbg and WinDbg (Windows, free), GDB with GEF/Pwndbg (Linux, free) — breakpoints, stepping, memory inspection, patching.
- **Static analysis:** [Ghidra](https://ghidra-sre.org) (NSA, free and open source) — disassembly, decompilation, scripting; find interesting functions via imports, strings, crypto constants.
- **The progression:** classic stack buffer overflow (no mitigations) → stack canaries → DEP/NX → ROP chains → ASLR → info leaks → heap exploitation (use-after-free) → format strings → type confusion.
- **Fuzzing:** [AFL++](https://aflplus.plus) (free) — coverage-guided fuzzing, the primary real-world native-code discovery method.
- **Free resources:** [pwn.college](https://pwn.college) (ASU — the best free binary exploitation curriculum on the internet; start here), Exploit Education VMs, Nightmare (free course).
- **Certifications (what they validate, free prep path):** OSED (OffSec EXP-301) — Windows user-mode exploit dev, the practitioner standard; OSEE (EXP-401) — advanced Windows exploitation, tiny holder population; GXPN (GIAC) — alternative. *Free prep: pwn.college to completion, CTF pwn challenges.*
- **Recognition:** in exploit dev, demonstrated ability outweighs every cert — CTF rankings, published exploits, CVEs from binary targets. This track feeds directly back into Stage C: binary CVEs are high-value.

## Track 5 — Malware analysis

**What it is:** determining what malicious software does, how it does it, and how to detect and stop it — without becoming a victim. RE techniques in service of the defensive mission.

**Core knowledge:**
- **Static analysis (no execution):** hashes (MD5/SHA256, imphash), strings, PE headers (sections, imports, entropy — high entropy means packed), packer detection (Detect It Easy, free), [YARA](https://virustotal.github.io/yara/) classification, Mandiant [CAPA](https://github.com/mandiant/capa) (free — identifies capabilities in binaries), FLOSS (free — deobfuscates strings).
- **Dynamic analysis (controlled execution):** Process Monitor (Sysinternals, free), Wireshark for C2 traffic, RegShot for registry diffs. Behavioral indicators: persistence (Run keys, scheduled tasks, services), process injection, C2 beaconing, anti-analysis tricks (VM detection, sleep timers).
- **Sandboxing:** [CAPE Sandbox](https://github.com/kevoreilly/CAPEv2) (free, open source — the maintained Cuckoo fork), [Any.Run](https://any.run) (free community tier — interactive), Triage (free tier). Rule: never detonate on bare metal — isolated VM, host-only networking, fake services (REMnux provides these).
- **The workflow:** triage (hash lookup on VirusTotal/MalwareBazaar — free) → static → dynamic → behavioral summary → IOC extraction (hashes, IPs, domains, mutexes, YARA rule) → report. IOCs feed detection engineering.
- **Safety and legality:** isolated VMs, snapshots before detonation, no uploading sensitive samples to public sandboxes (use local CAPE for those), never redistribute live malware.
- **Free tools:** [FLARE VM](https://github.com/mandiant/flare-vm) (Windows analysis distro), [REMnux](https://remnux.org) (Linux analysis distro), CAPA, FLOSS.
- **Certifications (what they validate, free prep path):** GREM (GIAC) — the malware analysis gold standard. *Stronger than certs early: published sample analyses, YARA rules with wild detections, [FLARE-On](https://flare-on.com) (Mandiant's free annual RE challenge) — the single best credential-builder in this track, and it's free.*
- **Recognition:** published dissections of real samples and FLARE-On completions are the malware analyst's public portfolio.

## Track 6 — Cloud security

**What it is:** securing cloud infrastructure — where the fastest-growing share of real breaches happens, and where misconfiguration (not zero-days) is the dominant cause.

**Core knowledge:**
- **Shared responsibility:** the provider secures *the cloud*; you secure *in the cloud* (your data, IAM, configurations). Every cloud breach postmortem starts here.
- **IAM fundamentals:** AWS — users/roles/policies (Effect/Action/Resource/Condition), permission boundaries, cross-account roles, STS temporary credentials, root lockdown + MFA. Azure — Entra ID, RBAC, managed identities, Conditional Access, PIM. Core discipline: least privilege, and reading a policy to determine *effective* permissions.
- **The common misconfigurations checklist:** public storage buckets; 0.0.0.0/0 security groups on sensitive ports; `*` IAM actions/resources; exposed access keys; unencrypted storage; disabled logging; public snapshots; SSRF-to-metadata-service (169.254.169.254 — the classic cloud attack primitive).
- **Cloud attack paths:** SSRF → instance metadata → temporary credentials → IAM privilege escalation. *Free practice tools: Pacu, CloudFox (authorized testing only).*
- **Defense:** guardrails (AWS Organizations SCPs, Azure Policy), detective controls (GuardDuty, Security Hub, Defender for Cloud), logging (CloudTrail, VPC Flow Logs), CSPM scanning in CI.
- **Free resources:** [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) (free hardening checklists), [Prowler](https://github.com/prowler-cloud/prowler) (open-source cloud security assessment), [ScoutSuite](https://github.com/nccgroup/ScoutSuite) (multi-cloud auditing), [flaws.cloud](https://flaws.cloud) (free AWS security challenges), cloud free tiers for building a vulnerable-by-design lab you then audit.
- **Certifications (what they validate, free prep path):** AWS Certified Security – Specialty — the most recognized cloud security cert; Microsoft SC-series (verify the current exam code on learn.microsoft.com — codes churn); CCSK (CSA) — vendor-neutral cloud security theory. *Free prep: CIS Benchmarks, Prowler/ScoutSuite practice, flaws.cloud.*
- **Recognition:** remediated Prowler/ScoutSuite findings in a public lab, cloud security write-ups — the largest hiring volume of any specialist track, and the proof is hands-on.

## Milestone check — Stage D exit

Deep, employable specialization: the NICE work role your track maps to, practiced for real — plus one public proof artifact (a tool built, a talk given, published detections, challenge completions, or a certification earned).

## CV — Stage D

- **Can claim:** the NICE work role the track maps to, once genuinely practiced; specialization evidence — tool, talk, published rules, challenge completions, certification earned.
- **Cannot claim:** organizational security ownership; governance or audit authority; breadth outside the chosen track.
- **Unlocks:** Stage E. **Recognition so far:** specialist proof is public by nature — code, rules, analyses, rankings. At this point your GitHub and your name in the community carry more weight than any degree.

---
# STAGE E — EXPERT

*Goal: the person organizations hire to own security.*

## Objectives

Stage E is breadth plus ownership. The CISSP's eight domains are the industry's agreed map of what a security leader must command; governance frameworks are the language organizations buy; and leadership is the skill that turns knowledge into programs. The CISSP mindset shift: a technician asks what tool fixes the problem — a leader asks what risk exists, who owns it, what law or policy applies, what control reduces it, what evidence proves it, and how the organization keeps operating.

## Lessons

### E1. The eight CISSP domains
The [ISC2 CISSP exam outline](https://www.isc2.org/certifications/cissp) is the controlling document — study from it, not third-party weight tables. Format: computerized adaptive testing, 100–150 items, 700/1000 to pass. The experience gate is real: 5 years cumulative paid experience across 2+ domains (a degree can waive one year); without it you hold Associate of ISC2 status until the experience is earned. That gate is knowledge-plus-time, not money — and this guide teaches the knowledge free.

- **Domain 1 — Security and Risk Management (16%, the heaviest):** governance principles; risk management (qualitative vs quantitative — ALE = SLE × ARO; FAIR for financial quantification); risk treatment (accept, avoid, transfer, mitigate); residual risk; control types (preventive, detective, corrective, deterrent, compensating); BIA driving RTO/RPO; BCP/DRP; legal/regulatory/compliance; professional ethics; personnel security; third-party risk. *Why it matters:* these concepts resurface in nearly every other domain, and risk language is how security gets budget. *Free: [NIST SP 800-39](https://csrc.nist.gov/pubs/sp/800/39/final), [NIST SP 800-30](https://csrc.nist.gov/pubs/sp/800/30/r1/final), FAIR Institute intro materials.* Lab: qualitative risk assessment on a lab network; draft a one-page security policy.
- **Domain 2 — Asset Security (10%):** classification schemes and why classification without handling procedures is theater; ownership (data owner vs custodian vs user); the data lifecycle (create → use → share → archive → destroy) and which controls attach at each phase; retention; privacy principles (purpose limitation, data minimization); data remanence and secure destruction. *Why it matters:* every breach post-mortem asks "what data was where and who owned it." *Free: [NIST SP 800-60](https://csrc.nist.gov/pubs/sp/800/60/v2/final), OWASP data classification cheat sheet.* Lab: classify a lab environment's assets; demonstrate secure deletion vs simple delete.
- **Domain 3 — Security Architecture and Engineering (13%, the heaviest technical domain):** security models (Bell-LaPadula, Biba, Clark-Wilson, Brewer-Nash) as integrity/confidentiality rules; evaluation criteria (Common Criteria); crypto systems and key management; defense in depth vs security through obscurity; secure defaults, fail securely, least privilege, separation of duties, complete mediation; physical and emanation security. *Why it matters:* architects decide what is even possible to defend later — misunderstood trust models are where the unfixable vulnerabilities live. *Free: [NIST SP 800-27](https://csrc.nist.gov/pubs/sp/800/27/r1/final), the Common Criteria portal.* Lab: map Bell-LaPadula/Biba to a real permission scheme; evaluate crypto choices against current NIST guidance.
- **Domain 4 — Communication and Network Security (13%):** secure architecture (segmentation, DMZ, zero trust — never trust, always verify, assume breach); transmission media; network attacks (DoS/DDoS, spoofing, MITM, DNS) and countermeasures; secure channels (VPNs, TLS, WPA3 wireless). *Why it matters:* network design determines incident blast radius — most "advanced" breaches are mundane lateral movement through flat networks. *Free: Practical Networking (YouTube), Professor Messer Security+ networking sections.* Lab: design a segmented network (VLANs, firewall rules, DMZ); demonstrate ARP spoofing and its countermeasure in a lab.
- **Domain 5 — Identity and Access Management (13%):** authentication factors and why phishing-resistant MFA (FIDO2/WebAuthn) is the single highest-ROI control; authorization models (DAC, MAC, RBAC, ABAC) and when each fits; Kerberos ticket flow; SSO/SAML/OAuth2/OIDC at the protocol level; the joiner-mover-leaver lifecycle and orphaned accounts; privileged access management. *Why it matters:* identity is the primary perimeter — credential theft and privilege misuse dominate breach reports. *Free: [NIST SP 800-63](https://pages.nist.gov/800-63-3/) (Digital Identity Guidelines), the OAuth2/OIDC core specs.* Lab: stand up Keycloak (free) with OIDC; configure RBAC vs ABAC; audit a lab for orphaned accounts.
- **Domain 6 — Security Assessment and Testing (12%):** scan vs pentest vs audit — which question each answers (breadth/automated, depth/adversarial/time-boxed, compliance-against-a-standard); test coverage vs depth; false positives/negatives; security metrics from test data; the audit lifecycle; log review; misuse/abuse case testing. *Why it matters:* this domain legitimizes everything from Stages B–D inside an organizational frame — leaders must scope assessments correctly or they buy the wrong test. *Free: OWASP WSTG, PTES, [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final).* Lab: scope three assessments (scan, pentest, audit) for one target; justify which answers which stakeholder question.
- **Domain 7 — Security Operations (13%):** the IR lifecycle ([NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final), April 2025 — CSF 2.0 profile; Rev. 2's classic four-phase lifecycle still shows up in interviews); chain of custody and evidence admissibility; SOC tiers and alert tuning; logging and monitoring; change and configuration management; redundancy and backup tied to RTO/RPO; DR/BC operations; physical and personnel security. *Why it matters:* operations is where security succeeds or fails daily — the best architecture is worthless with no monitoring and no practiced response. *Free: NIST SP 800-61, SANS DFIR posters.* Lab: tabletop incident exercise; build a logging pipeline (Wazuh or ELK, free) and write two detection rules.
- **Domain 8 — Software Development Security (10%):** shifting left — threat modeling and security requirements before code; SAST/DAST/IAST/SCA and what each catches; OWASP Top 10 and ASVS as requirements sources; database controls (parameterization, least-privilege accounts, encryption); secure defaults; supply-chain integrity (SBOMs, signing). *Why it matters:* the cheapest vulnerability is the one never written. *Free: OWASP Top 10 and ASVS, [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final).* Lab: STRIDE-threat-model a small app; run Semgrep against a codebase and triage.

### E2. Governance frameworks
- **[NIST CSF 2.0](https://www.nist.gov/cyberframework)** (free): the voluntary, outcome-based framework for managing cyber risk. Six Functions — Govern (new in 2.0: strategy, policy, roles, supply-chain risk), Identify, Protect, Detect, Respond, Recover — over 22 categories. The common real-world failure is over-investment in Protect relative to Detect and Respond. Lab: build a current-vs-target profile for a fictional company; defend the three priority gaps.
- **ISO/IEC 27001:2022:** the international standard for an Information Security Management System — running security as a repeatable business process. Clauses 4–10 plus Annex A: 93 controls in 4 themes (Organizational, People, Physical, Technological). Certification is organizational (two-stage accredited audit, Statement of Applicability as the central document). Note: the standard's official text is published by ISO and isn't freely available — but everything about what it requires is freely documented. Lab: draft a Statement of Applicability excerpt with risk justifications.
- **SOC 2:** an AICPA attestation (not a certification) for service organizations — a licensed CPA firm audits your controls. Five Trust Services Criteria (Security mandatory, plus Availability, Processing Integrity, Confidentiality, Privacy); Type I (design, point in time) vs Type II (operating effectiveness, 6–12 months — what enterprise buyers want). Key distinction: ISO 27001 = international certification of your management system; SOC 2 = US-centric attestation of your controls. Lab: map the five criteria to a sample SaaS architecture.

### E3. Leading security programs
- **Strategy:** present budgets as risk reduction, not tool purchases. Security as an embedded engineering capability, not an imposed checkpoint. Reward reporting mistakes and near-misses — culture is a control.
- **Board-grade metrics:** MTTD/MTTR; patch compliance and % of criticals past SLA; MFA coverage; incident volume and cost; exposure reduction trend; RTO/RPO accuracy from tested recovery; third-party risk coverage. Leading indicators, not raw blocked-attack counts.
- **Board communication:** business language. Per cycle: the risk objective, the exposure trend, the action taken, the measured change, the decision or investment needed next. The board allocates capital against risk — translate accordingly.
- **Free resources:** FAIR Institute materials, NIST CSF Organizational Profiles, CISA's Cybersecurity Performance Goals (free baseline checklist).
- **Lab:** write a one-page board report for a fictional quarter — exposure trend, two metrics, one investment ask framed as risk reduction.

### E4. CVP Red Team and Specialized tiers — the organizational horizon
Anthropic's Cyber Verification Program reserves its upper tiers for organizations: **Red Team Access** (authorized penetration testing and red teaming — in-house red teams, government teams, professional pentest firms) and **Specialized Access** (the fewest restrictions, for verified organizations authorized to test safety-critical systems — power grids, telecom, flight operations, interbank payments — vetted with government involvement). Individuals can't hold these tiers — and that's the point of the whole guide: **the tiers open through employment.** You join or found a qualifying organization; its enrollment carries your access. Stages C through E made you someone such an organization hires. This is the promise, fulfilled literally.
- **Lab:** write a one-page justification for which tier a fictional employer (hospital SOC vs pentest firm vs grid operator) should apply for, and what controls it must demonstrate.

## Milestone check — Stage E exit

Map all eight CISSP domains to a real organization's program (one page per domain, no gaps) · build and defend a NIST CSF 2.0 current-vs-target profile · draft a Statement of Applicability excerpt · explain Type I vs Type II SOC 2 to a founder · deliver the one-page board report · complete the CVP tier justification exercise.

## CV — Stage E

- **Can claim:** CISSP — only after passing *and* meeting the experience requirement (Associate of ISC2 otherwise — claim it honestly); NIST CSF 2.0 program experience; ISO 27001 implementation/audit participation (never "certified" as an individual — certification belongs to organizations); SOC 2 readiness/audit support; CVP Defense Access enrollment; AI governance credentials where earned.
- **Cannot claim:** "ISO 27001 certified" as an individual; CVP Red Team/Specialized as an individual (organization-only); CISSP without the experience met; management experience from study alone. The standard holds at every stage: claim nothing you haven't earned.
- **Unlocks:** organizational security ownership — CISO-track roles, security architecture leadership, and the CVP organizational tiers through employment. **Recognition, complete:** CISSP + specialization + CVE history + public write-ups + CVP standing. Every item verifiable, none requiring a degree. This is what the recognition pathway was building toward from Stage A.

---
# AI SECURITY CERTIFICATION TRACK

*Runs alongside Stages D–E. Each cert below is covered the way this guide covers everything: what free material teaches its domains, what knowledge it requires, who it's actually for. Start each when you qualify — not before.*

## The prerequisite ladder (easiest gate first)

### 1. AIGP — AI Governance Professional (IAPP)
- **What it is:** the policy-side AI credential — AI governance, law, risk frameworks. Knowledge exam, no labs.
- **Gate:** none. No prerequisites, no technical background assumed.
- **Domains (IAPP Body of Knowledge, free download):** foundations of AI governance (AI/ML concepts, responsible-AI principles, roles, accountability); AI laws, standards, and frameworks (EU AI Act, privacy law overlap, OECD principles, NIST AI RMF, ISO standards); governing AI development (data governance, impact assessments, model testing, documentation); governing AI deployment and use (vendor assessment, deployment risks, monitoring, incident management).
- **Exam:** 100 multiple-choice/scenario questions, about 2.75 hours, scaled pass mark; Pearson VUE test centers or online proctoring.
- **Who it's for:** privacy officers, legal/compliance, risk managers, AI governance leads. Skip it if you want hands-on skill — it won't teach you to attack or defend anything. Pairs with CAISP for both sides.
- **Free prep:** the IAPP Body of Knowledge and exam blueprint are free downloads — build the whole study plan around them; EU AI Act text; NIST AI RMF (free).
- **Recognition:** a governance credential with zero gate — the fastest verifiable AI-governance signal for policy-minded learners.

### 2. CAISP — Certified AI Security Professional (Practical DevSecOps)
- **What it is:** practitioner-grade, hands-on AI security — attack and defend LLMs and AI pipelines. The technical counterpart to AIGP.
- **Gate:** no credential gate. Requires basic Linux CLI comfort; scripting familiarity (Python/Go/Ruby) helps. The practical exam assumes you can live in a terminal — Stage A and B graduates qualify.
- **Syllabus (7 chapters):** AI security foundations (AI/ML concepts, LLM architecture); LLM attack methodologies via the MITRE ATLAS matrix; the OWASP LLM Top 10 **(2026 edition — released 2026-09-30, codes renumbered from 2025; always name the edition when citing)** (prompt injection, training data poisoning, model theft, supply-chain attacks, excessive agency); AI DevOps security (securing AI pipelines, poisoned pipelines, dependency confusion); AI threat modeling (STRIDE for AI systems); AI supply chain security (SBOMs/MLBOMs, model signing with Cosign, SLSA); AI governance and compliance (EU AI Act, NIST AI RMF, ISO/IEC 42001).
- **Exam:** practical and online — hands-on challenges against live scenarios (about 6 hours) plus a professional written report (24 hours to submit). No multiple choice; it can't be faked with memorization. Lifetime validity — no renewal.
- **Follow-on:** CAASE (Certified Agentic AI Security Expert) — agentic AI security, for later.
- **Who it's for:** AI security engineers, LLM security engineers, AI red teamers, AppSec engineers, DevSecOps for AI pipelines. Skip it until you can live in a Linux terminal — do the foundations first.
- **Free prep:** the [OWASP LLM Top 10 (2026 edition)](https://genai.owasp.org) documentation and the [MITRE ATLAS](https://atlas.mitre.org) matrix — both free, both heavily tested. PortSwigger's web LLM attack labs (free) for prompt injection practice.
- **Recognition:** a practical exam with lifetime validity — proof you can attack and defend AI systems, verifiable without renewal.

### 3. SEC535 → GIAC GOAA — Offensive AI (SANS)
- **What it is:** offensive AI — how attackers use AI across the kill chain, taught so testers and defenders can match it.
- **Gate:** practitioner experience. Requires solid cybersecurity fundamentals and enterprise security familiarity; the course assumes you can already pentest — if you can't do recon and exploitation without AI, the AI layer won't save you. (Lab note: the course environment needs Intel virtualization — check your hardware against the course requirements.)
- **Syllabus (3 sections, 14 labs + CTF capstone):** offensive AI foundations (RAG, GenAI, LLMs, vector databases, AI agents); building pentesting GPTs; automating offensive workflows; AI-augmented OSINT and network recon (vuln prioritization, adaptive scanning); AI web exploitation (AI-augmented SQLi, brute-forcers, command injection); AI social engineering (AI phishing, audio and visual deepfakes, vishing); AI-assisted patch diffing; AI-written malware and security-control evasion (AMSI bypasses, obfuscation).
- **Exam (GOAA):** 56 questions, 2 hours, 67% to pass.
- **Who it's for:** pentesters, red team operators, security consultants, SOC/IR personnel. Skip until Stage B skills are solid.
- **Free prep:** MITRE ATLAS (offensive techniques), PortSwigger Academy (the underlying web exploitation the AI augments), open-source OSINT tooling docs.
- **Recognition:** the attack-minded AI credential — proves you understand the adversary's AI tooling, not just the theory.

### 4. SEC598 → GIAC GASAE — AI and Security Automation (SANS)
- **What it is:** AI plus security automation across red, blue, and purple teams. The automation engineer's AI credential.
- **Gate:** working security background — SOC analysis, detection engineering, security engineering, or incident response — plus scripting comfort (Python/PowerShell) and cloud/SOAR familiarity. Not an intro course.
- **Syllabus (6 sections, 25 labs + full-day capstone in a hybrid cloud lab):** GenAI/LLM foundations and security automation concepts (policy-as-code, automation triggers, detection-as-code); automation engineering (PowerShell for offense and defense, Terraform IaC, automated firing ranges, Python/Jupyter for SOC enrichment, SOAR playbooks, agentic AI); cloud automation and AI security services (Azure and AWS); red team automation and offensive AI agents (adversary emulation, ATT&CK, emulation-as-code); defensive automation and AI-augmented response (modular IR playbooks, LLM-assisted detection-as-code, triage tooling); capstone exercise.
- **Exam (GASAE):** GIAC CyberLive format — hands-on lab challenges; 82 questions, 3 hours, 70% to pass.
- **Who it's for:** SOC analysts, detection engineers, automation engineers, IR analysts, red/blue/purple operators, cloud security engineers. Skip unless you're already operating in a SOC or security-engineering role.
- **Free prep:** SOAR platform community editions, Terraform/Ansible docs, Sigma detection-as-code practice, the course's published exam objectives.
- **Recognition:** you leave with playbooks, IaC templates, and detection pipelines — artifacts that demonstrate automation skill directly.

### 5. AAISM — Advanced in AI Security Management (ISACA)
- **What it is:** the management-track AI security credential — governing AI risk at the program level, not hands-on hacking.
- **Gate — hard:** an active CISSP or CISM is required to register; ISACA verifies, with no test-first path and no experience substitute. If the underlying CISSP/CISM lapses, AAISM goes with it. ISACA also recommends experience assessing or maintaining AI systems.
- **Domains (ISACA exam content outline, free):** AI governance and program management (31%) — stakeholders, frameworks, regulatory requirements, policies, asset and data lifecycle, program development, business continuity and IR; AI risk management (31%) — risk assessment, thresholds, treatment, threat and vulnerability management, vendor and supply chain; AI technologies and controls (38%) — security architecture, model lifecycle, data management controls, privacy/ethical/trust/safety controls, security controls and monitoring.
- **Exam:** 90 scenario-based questions, 150 minutes, scaled pass mark; PSI test centers or remote proctoring.
- **Who it's for:** CISOs, security managers, GRC leaders, AI security/risk managers. If you don't hold CISSP/CISM, this cert doesn't exist for you yet — earn one first, and take CAISP or AIGP in the meantime for actual AI knowledge.
- **Free prep:** ISACA's published exam content outline; NIST AI RMF; ISO/IEC 42001 overview materials; your CISSP Domain 1 knowledge does heavy lifting here.
- **Recognition:** the AI-governance credential for people who already lead security functions — meaningful precisely because of its gate.

### Wider SANS AI family (reference)
- **SEC545 → GAIPS:** securing LLM applications (prompt injection, data leakage, model abuse) — for AI engineers and AppSec teams.
- **SEC573 → GPYC:** Python for security automation — for engineers who want to code.
- **SEC595 → GMLE:** data science and ML for security — for engineers moving into ML-driven detection.
- **SEC536 → GAIPT:** penetration testing AI systems — for pentesters working with AI-enabled targets.
- Each follows the same pattern: practitioner gate, hands-on exam, free prep via published objectives and open-source tooling.

### Positioning rules
- AIGP and CAISP are reachable from the core track — AIGP for the policy-minded, CAISP for the technical; they pair well.
- SEC535/SEC598 need practitioner experience first — never entry points.
- AAISM is downstream of CISSP/CISM entirely — not a standalone goal for anyone without those.
- No cert is automatically worth pursuing: match the cert to the role you want, prepare free, and let the knowledge — not the logo — do the work.

---
# CAREER LADDER

*How the stages map to real work, real titles, and honest CV lines.*

## The NICE framework map

The [NICE Cybersecurity Workforce Framework](https://niccs.cisa.gov/tools/nice-framework) (NIST SP 800-181 Rev. 1) defines security work by function, not job title — 7 categories, each with specialty areas and work roles. This guide's stages map onto it:

| Stage | Primary NICE categories | Representative work roles |
|---|---|---|
| **A — Foundations** | Operate & Maintain | System Administrator, Network Operations Specialist, Technical Support Specialist — the entry roles the foundations feed (Stage A itself is pre-role preparation) |
| **B — Practitioner** | Protect & Defend; Securely Provision (Test & Evaluation) | Vulnerability Assessment Analyst, Cyber Defense Analyst, Test and Evaluation Specialist |
| **C — Professional** | Protect & Defend (mature); Securely Provision (Risk Management) | Vulnerability Assessment Analyst (independent practice), Security Control Assessor |
| **D — Specialist** | Track-dependent | Red team → Exploitation Analyst (Analyze), Cyber Operator (Collect & Operate); DFIR → Cyber Defense Forensics Analyst (Investigate), Cyber Defense Incident Responder (Protect & Defend); AppSec → Secure Software Assessor, Information Systems Security Developer (Securely Provision); Threat intel → Threat/Warning Analyst, All-Source Analyst (Analyze) |
| **E — Expert** | Oversee & Govern; Securely Provision (Systems Architecture) | Information Systems Security Manager, Cyber Policy and Strategy Planner, Executive Cyber Leadership, Security Architect |

Note: NICE has no standalone "Penetration Tester" role — offensive testing maps across Vulnerability Assessment Analyst, Exploitation Analyst, and Test and Evaluation Specialist depending on context. This guide says so explicitly rather than inventing a mapping.

The 7 categories for reference: Securely Provision (design and build secure systems) · Operate & Maintain (support and administer) · Oversee & Govern (lead and manage) · Protect & Defend (identify and mitigate threats) · Analyze (evaluate security information) · Collect & Operate (denial, deception, collection) · Investigate (cyber events, crimes, digital evidence).

## The hireable narrative

- **Stage C is the employable-professional line.** A CVE with your name on it plus a disclosure history is what makes a hiring manager take the interview. Everything before it is preparation; everything after it is leverage.
- **CVP Defense Access is the individual milestone.** Anthropic's Cyber Verification Program admits individual researchers with a track record of reported vulnerabilities to its Defense tier — your Stage C evidence is the application.
- **Red Team and Specialized tiers open through organizational sponsorship.** They're organization-only by design. The guide's promise is literal: become someone such an organization hires (Stages C–E), and the tiers open through employment.
- **No degree required at any point.** Every stage's recognition artifacts — lab completions, bounty profiles, CVE records, write-ups, challenge completions, certifications — are public and verifiable without any institution's permission. That's the recognition pathway: proof, not pedigree.

## CV honesty rules (all stages)

1. Claim only what you've done — link the evidence.
2. "Cannot claim yet" lists are not modesty; they're what make the claimed items believable.
3. A certification abbreviation without the underlying work is a liability in an interview, not an asset.
4. One verifiable CVE beats a page of adjectives.

---

# APPENDIX

## Ethics and scope — hard rules (non-negotiable, everywhere in this guide)

1. **Written authorization first.** No testing outside explicitly documented scope — scope sheet before any packet beyond normal browsing.
2. **Recon ≠ permission.** A name from recon is a candidate, not authorization. Recheck scope before probing, crawling, or sending a request.
3. **A scanner match on a known issue is not a new CVE.** Scanner output is a lead; it still needs manual validation, and a known CVE ID is someone else's finding.
4. **No credential use, ever.** Found secrets are evidence of exposure, not invitations. Secret-scanner verification stays disabled.
5. **Automated tools produce false positives** — confirm by hand before reporting. Authorization tooling especially: a human reads the output.
6. **A bearer token is not a JWT** until the format is identified — opaque tokens are common; assuming JWT structure leads to false conclusions.
7. **Rate and noise discipline** — one hypothesis, one host, a rate the program allows. The noisiest phases get explicit rate notes in every lab.
8. **Confidential notes stay out of public repos.** Scope sheets, credentials owned, client data — private storage only.

## Free lab index

- **Linux/CLI:** [OverTheWire Bandit](https://overthewire.org/wargames/bandit)
- **Networking:** Wireshark + the Kurose & Ross companion labs; Cisco Packet Tracer
- **HTTP:** [PortSwigger Web Security Academy](https://portswigger.net/web-security) — the backbone from A3 through B3
- **Python:** your own scripts, from scratch
- **Crypto:** [CryptoHack](https://cryptohack.org)
- **Web hacking:** PortSwigger Academy · DVWA (`docker run -p 80:80 vulnerables/web-dvwa`) · [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) (`docker run -p 3000:3000 bkimminich/juice-shop`) · WebGoat · bWAPP · [OWASP crAPI](https://github.com/OWASP/crAPI) (APIs) · DVGA (GraphQL) · [Google Gruyere](https://google-gruyere.appspot.com) (beginners) · [XSS Game](https://xss-game.appspot.com) · [Hacker101](https://www.hacker101.com)
- **CTF/practice platforms:** [TryHackMe](https://tryhackme.com) and [HackTheBox](https://www.hackthebox.com) (free tiers) · [VulnHub](https://www.vulnhub.com) (downloadable VMs) · [CTFtime](https://ctftime.org)
- **Blue team:** [LetsDefend](https://letsdefend.io) (free tier) · [CyberDefenders](https://cyberdefenders.org) (free tier)
- **Binary/RE:** [pwn.college](https://pwn.college) · [Ghidra](https://ghidra-sre.org)
- **Malware:** [FLARE VM](https://github.com/mandiant/flare-vm) · [REMnux](https://remnux.org) · [Any.Run](https://any.run) (community tier) · [FLARE-On](https://flare-on.com) (free annual challenge)
- **Cloud:** [flaws.cloud](https://flaws.cloud) · [Prowler](https://github.com/prowler-cloud/prowler) · [ScoutSuite](https://github.com/nccgroup/ScoutSuite)
- **Red team:** [MITRE ATT&CK](https://attack.mitre.org) + Navigator · [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) · [BloodHound CE](https://github.com/SpecterOps/BloodHound) · [LOLBAS](https://lolbas-project.github.io)
- **Detection:** [Sigma](https://github.com/SigmaHQ/sigma) · [YARA](https://virustotal.github.io/yara/) · [Velociraptor](https://www.velocidex.com)
- **AppSec:** [Semgrep](https://semgrep.dev) (open source) · [CodeQL](https://codeql.github.com) (public repos) · [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon) · [OWASP SAMM](https://owaspsamm.org) · [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- **AI security:** [OWASP LLM Top 10 (2026 edition)](https://genai.owasp.org) · [MITRE ATLAS](https://atlas.mitre.org) · IAPP AIGP Body of Knowledge (free) · ISACA AAISM exam outline (free) · [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- **Disclosure & scoring:** [cve.org](https://www.cve.org) · [NVD](https://nvd.nist.gov) + CVSS calculators · [FIRST.org CVSS docs](https://www.first.org/cvss/) · [CWE](https://cwe.mitre.org) · [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [OpenSSF disclosure guide](https://github.com/ossf/oss-vulnerability-guide)
- **Governance:** [NIST CSF 2.0](https://www.nist.gov/cyberframework) · [NIST SP 800-series](https://csrc.nist.gov/pubs/sp) (800-30, 800-39, 800-53, 800-61, 800-63, 800-115, 800-218 — all free) · [NICE Framework](https://niccs.cisa.gov/tools/nice-framework) · [CISA CPGs](https://www.cisa.gov/cross-sector-cybersecurity-performance-goals)

---

*Manuscript assembled 2026-10-09 from eight research tracks. Sources are summarized and linked throughout — no substantial text copied. Gaps and unverified items are listed in the assembler's handoff report.*
