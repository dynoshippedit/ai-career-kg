# Stage A — Foundations: research
### Night research track 01 · 2026-10-09 · brief-governed
**Stage milestone:** explain, packet by packet, what happens between pressing "log in" and the page rendering. **Claim after this stage:** nothing yet.

Verification key: **verified** = fetched today (2026-10-09) · **lead** = from PROGRAM_MAP.md or well-known, to re-verify at build time. All summaries below are original prose, not copied text.

---

## A1. Operating systems and Linux (Linux first, Windows second)

Topics: processes, memory, filesystems, permissions, users, services, logs, packages, SSH, the shell.

**Primary sources** (projects' own docs — the lesson's "Read the source"):
- `man` pages on the reader's own machine (`man ls`, `man ssh`, `man chmod`) — the canonical reference for every command taught. No fetch needed; it ships with the OS.
- OpenSSH manual pages / openssh.com — for the SSH hardening lesson (key-based auth, `sshd_config`).

**Free resources (max 3):**
1. **OverTheWire: Bandit** — https://overthewire.org/wargames/bandit/ — **verified**. SSH-based wargame aimed at absolute beginners; each level teaches commands by requiring them. What it's for: hands-on shell fluency from day one; the lesson's walkthrough target. (Site grants permission by design.)
2. **Linux Journey** — now hosted on LabEx (linuxjourney.com redirects) — **verified** free and open-source, 200+ community updates as of 2026. What it's for: structured reading on filesystem layout, permissions, processes, users — the concepts Bandit exercises.
3. **The reader's own VM + man pages** — Ubuntu/Debian in VirtualBox/UTM, or WSL2 on Windows. What it's for: the lab bench; every lesson's commands run here first.

**Lab target:** local VM (reader owns it) + Bandit over SSH (authorized by the game).
**Proof artifact:** per-level Bandit notes published (one command learned per level) — the reader's first public artifact; plus a hardened SSH config on their VM with key-only auth, documented.
**Windows-second note:** PowerShell/Microsoft Learn free tier is the Windows path — **lead**, verify at build time. Keep Windows to: what differs (registry vs files, services, Event Viewer, AD concepts preview).

## A2. Networking at packet level

Topics: TCP/IP, IPv4 and IPv6, subnetting, DNS, DHCP, routing, firewalls, VPNs, proxies, VLANs.

**Primary sources (fetched today, rfc-editor.org):**
- **RFC 9293 — TCP (Aug 2022, obsoletes 793).** Read: §2.2 Key TCP Concepts (reliable in-order byte stream, ports as multiplexers); §3.1 Header Format (the header diagram — ports, sequence/acknowledgment numbers, flags); §3.4 Sequence Numbers; §3.5 Establishing a Connection (three-way handshake); §3.6 Closing. Skim: §3.7 segmentation/MSS, §3.8 retransmission/congestion (concepts only). Skip: §3.9–3.10 (implementer API/event processing), appendices.
- **RFC 1034 — DNS concepts** (companion to 1035; concepts of name space, zones, resolvers vs name servers). **RFC 1035 — DNS implementation.** Read: §2.1 Overview; §3.2–3.3 RR definitions and standard RRs (A, AAAA, CNAME, MX, NS, PTR, SOA, TXT); §4.1 message format (header/question/answer sections — this is what the Wireshark lab dissects); §4.2 transport (UDP normally, TCP fallback). Skip: §5 master files, §6–7 server/resolver implementation, §8 mail.
- Also worth one lesson pointing at: **RFC 791 (IPv4)** and **RFC 8200 (IPv6)** headers — **leads**, fetch at build time; the lesson needs the header diagrams, not the full texts.

**Free resources (max 3):**
1. **Professor Messer — Network+ video series** — https://www.professormesser.com/ — **verified** (homepage shows free video training for Network+; current series N10-009 per earlier research). What it's for: structured TCP/IP, DNS, DHCP, subnetting walkthrough in plain language.
2. **Wireshark** (wireshark.org) + `tcpdump`/`dig` on the reader's machine — **lead** (well-known project; re-verify download page at build). What it's for: the packet labs — capture own traffic, follow a TCP stream, dissect DNS and the TLS handshake.
3. **Kurose & Ross companion site** (gaia.cs.umass.edu/kurose_ross) — **lead**, with the brief's correction carried: the textbook is commercial; the authors' lectures, slides, and Wireshark labs are free. What it's for: the Wireshark lab exercises.

**Lab target:** reader's own machine — capture their own traffic only (browsing they do themselves); `dig`/`nslookup` against public resolvers (reading, not attacking); subnetting worked on paper then checked with `ipcalc`.
**Proof artifact:** annotated packet capture — a DNS resolution chain plus TCP three-way handshake from the reader's own page load, narrated field by field.

## A3. HTTP in depth

Topics: methods, status codes, headers, cookies and sessions, Basic, Bearer, JWT, OAuth 2.0 and OIDC, the TLS handshake.

**Primary sources (fetched today, rfc-editor.org):**
- **RFC 9110 — HTTP Semantics (June 2022, STD 97).** Read: §3 Terminology and Core Concepts (resources, representations, messages); §5 Fields (field names, lines, values); §9 Methods (9.2 safe/idempotent, 9.3 GET/POST/PUT/DELETE definitions); §11 HTTP Authentication (11.1–11.4 schemes/challenge-response, 11.6 WWW-Authenticate/Authorization); §15 Status Codes (15.1 class overview, then the codes that matter: 200, 201, 204, 301/302/307/308, 400, 401, 403, 404, 405, 500, 502, 503); §17 Security Considerations (17.9 sensitive info in URIs, 17.16 auth considerations). Skim: §7 routing/proxies, §8 representation metadata, §13 conditional requests. Skip: §12 content negotiation (deep), §16–18 registries/IANA, Appendix A ABNF (reference only).
- **RFC 6265 — Cookies (2011).** Read: §3 Overview + §3.1 examples; §4.1 Set-Cookie syntax and attributes; §5.2.1–5.2.6 the attributes (Expires, Max-Age, Domain, Path, Secure, HttpOnly); §8 Security Considerations (8.2 ambient authority, 8.3 clear text, 8.4 session identifiers — why cookie theft matters). Skip: §5.1 parsing algorithms (reference), §6, §9.
- **RFC 8446 — TLS 1.3 (Aug 2018).** Read: §1 Introduction (the three goals: authentication, confidentiality, integrity); §1.2 major differences from TLS 1.2 (why 1.3 removed renegotiation/static RSA); §2 Protocol Overview — the handshake message diagram (ClientHello → ServerHello → {EncryptedExtensions} → {Certificate} → {CertificateVerify} → {Finished}); §4.1.2/4.1.3 ClientHello/ServerHello (what gets negotiated); §4.4 authentication messages (what Certificate, CertificateVerify, Finished each prove). Skim: §5 record protocol, §7.1 key schedule (conceptual), Appendix E security properties. Skip: §3 presentation language, §4.2 extensions in full (reference), §6 alerts, §8–9, appendices A–D.
- **RFC 7519 — JWT (May 2015).** Read: §3 Overview + §3.1 example JWT (the three dot-separated parts); §4.1 registered claims (iss, sub, aud, exp, nbf, iat, jti — what each asserts); §7.2 validating a JWT (the checklist a validator must run — this is the security lesson); §11.1 trust decisions. Skim: §5 JOSE header, §6 unsecured JWTs. Skip: §8–10, appendices.
- **RFC 6749 — OAuth 2.0 (Oct 2012).** Read: §1.1 roles (resource owner, client, resource server, authorization server); §1.2 protocol flow (the redirect dance); §1.3 grant types (know all four exist; study §4.1 authorization code grant in full); §1.4/1.5 access vs refresh tokens; §10 security considerations (10.3 access tokens, 10.12 CSRF/`state`). Skip: §2 client registration, §4.2 implicit (deprecated in practice — lesson notes the OAuth 2.1 / Security BCP direction), §4.3/4.4 legacy grants, §8, §11, Appendix A.
- **RFC 9116 — security.txt (Apr 2022, Informational).** Read: §2.5 field definitions (Contact, Expires, Policy, Acknowledgments, Canonical); §3 location (`/.well-known/security.txt`); §5.5 no implied permission for testing — direct tie-in to the brief's hard rules. Skip: §4 ABNF, §6 IANA.
- **OpenID Connect Core 1.0** (openid.net/specs) — **lead**, fetch at build time; the lesson needs the ID-token-on-top-of-OAuth-2.0 concept, not the full spec.

**Free resources (max 3):**
1. **MDN — HTTP documentation** — https://developer.mozilla.org/en-US/docs/Web/HTTP — **verified** live today (guides from "Overview of HTTP" through auth, caching, CORS, plus the full header/method/status reference). What it's for: the readable companion to RFC 9110 — start here, then read the RFC sections.
2. **PortSwigger Web Security Academy** — https://portswigger.net/web-security — **verified** 100% free today (their words), interactive labs, Burp Community Edition free. What it's for: HTTP basics taught through labs; also the bridge into Stage B.
3. **RFCs above, read in the order listed** — what they're for: the primary-source habit; the lesson's "Read the source" section points at exact sections per above.

**Lab target:** `curl` against a local server (`python3 -m http.server`) the reader runs; browser devtools Network panel on sites they visit (passive reading); PortSwigger labs (permission granted); jwt.io-style decode done locally with Python (no token pasted anywhere third-party).
**Proof artifact:** full request/response dissection of a login against the local server — every header explained in the reader's own words; a JWT decoded with each claim explained and the validation checklist from RFC 7519 §7.2 applied.

## A4. Python for security tooling

Topics: language basics through writing tools — requests, sockets, argparse, parsing output, file handling, regex.

**Primary sources:**
- **docs.python.org/3/tutorial/** — the language's own tutorial — **lead** (well-known; re-verify URL at build). The primary reference for every construct taught.

**Free resources (max 3):**
1. **Python for Everybody (py4e.com)** — **verified** free today (site: free materials, lectures, book, autograded assignments; CC-licensed). What it's for: programming from zero — the on-ramp for readers who have never coded.
2. **Automate the Boring Stuff with Python (automatetheboringstuff.com)** — **verified** free to read today under Creative Commons (3rd edition). What it's for: practical scripting with security-direct chapters — regex (ch. 9), files (ch. 10), web scraping (ch. 13), SQLite (ch. 16). This is the bridge from "can code" to "codes tools."
3. **Python docs tutorial** (above) — what it's for: the reference habit; the lesson teaches reading stdlib docs, not just tutorials.

**Lab target:** local interpreter only; scripts run against the reader's local lab targets (their VM, local HTTP server).
**Proof artifact:** a small tool in a repo with a README — e.g., a port scanner, a log parser, or an HTTP request replayer — written from scratch, no copied code.

## A5. Reading code: JavaScript and SQL

Topics: enough JS to follow a web app's client logic; enough SQL to read queries and understand what a query does.

**Primary sources:**
- **ECMAScript specification** (tc39.es/ecma262) — **lead**; the lesson references it as "the spec exists, here's how to read one section," not as reading material.
- **SQLite documentation** (sqlite.org/lang.html) — **lead**; the SQL dialect the labs use.

**Free resources (max 3):**
1. **javascript.info — The Modern JavaScript Tutorial** — https://javascript.info/ — **verified** live today (fundamentals through advanced, regex included). What it's for: JS from scratch; the lesson scopes to Part 1 (language) + fetch/DOM basics.
2. **SQLBolt** — https://sqlbolt.com/ — **verified** live today (interactive in-browser lessons with exercises). What it's for: SQL queries through joins — exactly the reading level Stage B's SQLi lesson needs.
3. *(Third slot intentionally empty — two strong resources beat three padded ones. Gap logged below.)*

**Lab target:** local files only — read the source of the reader's own Python tools; read Juice Shop/DVWA source locally (read-only preview of Stage B targets).
**Proof artifact:** annotated walkthrough of a JS login form (what each function does, where the request goes) + a SQL query explained clause by clause + spot-the-bug in a provided snippet.

## A6. Cryptography

Topics: hashing, symmetric and asymmetric encryption, signatures, PKI, and what breaks when each is misused. (Conceptual + hands-on-breaking; no math proofs.)

**Primary sources:**
- **RFC 8446 §7.1** (key schedule/HKDF concept) and **RFC 7519 §3** (signed vs encrypted JWT) — already fetched; reused here as the "where crypto meets the web" bridge.
- **RFC 5280** (PKI/X.509) — **lead**, fetch at build time; the lesson needs the certificate-chain concept, not the ASN.1.

**Free resources (max 3):**
1. **CryptoHack** — https://cryptohack.org/ — **verified** live and active today (2025 CTF challenges listed, recent solves streaming). What it's for: learn-by-breaking — Introduction, General, and Modular Arithmetic categories at Stage A; RSA/ECC categories explicitly deferred to Stage D.
2. **Dan Boneh — Cryptography I (Coursera, audit track)** — **lead** (well-known free-to-audit; re-verify availability at build). What it's for: the rigorous conceptual spine (one-time pad, block ciphers, MACs) for readers who want depth.
3. **OpenSSL CLI + CyberChef on the reader's machine** — CyberChef (gchq.github.io/CyberChef) **lead** (well-known; re-verify URL at build). What it's for: hands-on — hash a file, verify a signature, watch ECB vs CBC on an image.

**Lab target:** CryptoHack (authorized by design); local OpenSSL/CyberChef on the reader's own files.
**Proof artifact:** CryptoHack intro-category completions + a one-page explainer of one classic misuse (e.g., ECB mode, unsalted hashes, or `alg:none`) written for a non-technical reader.

---

## Prerequisite ordering (the lesson DAG)

1. **A1 Linux/shell first.** Everything else runs in a terminal. Bandit can start on day one.
2. **A2 Networking second.** Packets, DNS, TCP — the substrate TLS and HTTP sit on.
3. **A6 Cryptography third.** Hashing/encryption/signatures/PKI must precede the TLS handshake lesson.
4. **A3 HTTP fourth.** Requires A2 (TCP/DNS) + A6 (TLS/crypto). The Stage A milestone (packet-to-render login narration) is assessed here.
5. **A4 Python fifth** — needs A1 (shell); uses HTTP via `requests`, so it lands best alongside or just after A3. May run in parallel with A3 once A1 is done.
6. **A5 Reading code sixth** — needs A3 context to read web code meaningfully. Order within: JavaScript, then SQL (SQL reading is the direct prerequisite for Stage B's SQL injection lesson).

**Stage A exit gate:** the reader narrates, packet by packet with captures to point at, the full path of a login submit — DNS, TCP handshake, TLS handshake, HTTP request/response, cookie set, page render — naming every protocol and field from the RFCs above. Assessed as narration, not multiple choice.

---

## Gaps (honest log)

1. **OIDC:** OpenID Connect Core 1.0 not fetched — lead for build time (openid.net/specs). Lesson needs only the ID-token concept.
2. **OAuth Security BCP:** the current best-practice doc (successor guidance to RFC 6749 §4.2 implicit grant) not verified — lead for build time.
3. **IPv6 hands-on:** verified resources lean IPv4; need an IPv6-specific lab exercise at build time (e.g., capture own IPv6 traffic, `ping6`/`dig AAAA`).
4. **Windows-as-second-OS:** no verified free Windows lab path yet (Microsoft Learn free tier is the candidate) — lead.
5. **Kurose & Ross:** companion-site free labs/slides not fetched — lead, with the brief's commercial-textbook correction carried into the lesson copy.
6. **Dan Boneh Crypto I:** current free-audit availability not verified today — lead.
7. **CyberChef URL:** not fetched today — lead (well-known, low risk).
8. **A5 third resource:** deliberately left empty rather than padding; if the lesson author finds a strong third free resource (e.g., a guided code-reading exercise), it goes in the directory, not the lesson.
9. **Walkthrough execution:** per the brief, lesson walkthroughs get executed at build time (Phase 2+). This research verified sources and targets; no commands were run in this pass.

---

## Handoff (5 lines)

1. **Coverage:** all six Stage A areas researched — each with fetched primary sources (8 RFCs: 9110, 6265, 8446, 9293, 1034/1035, 7519, 6749, 9116, with read/skim/skip section guidance), ≤3 free resources each (10 verified live today), lab targets the reader owns, and proof artifacts.
2. **Key primary sources:** RFC 9110 (HTTP), RFC 8446 (TLS 1.3 handshake §2/§4), RFC 9293 (TCP), RFC 1035 (DNS), RFC 6265 (cookies), RFC 7519 (JWT), RFC 6749 (OAuth 2.0), RFC 9116 (security.txt §5.5 ethics tie-in).
3. **Ordering:** A1 shell → A2 networking → A6 crypto → A3 HTTP (milestone here) → A4 Python (parallel-able with A3) → A5 code reading (JS then SQL).
4. **Gaps:** OIDC spec, OAuth Security BCP, IPv6 lab, Windows free path, Kurose companion labs, Boneh audit availability, CyberChef URL — all logged as leads for build time; A5 third resource slot deliberately empty.
5. **Brief compliance:** no prices/fees/salaries/time estimates anywhere; free-to-learn only; all summaries original; PROGRAM_MAP.md resource names treated as leads and verified or marked as such.
