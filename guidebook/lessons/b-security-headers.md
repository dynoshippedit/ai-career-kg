# Security headers and browser defenses: telling the browser what "safe" means

**ID:** `b-security-headers` · **Stage:** B (Practitioner) · **Level:** 3 (mechanism + local verification of every header with curl + correct scoping of what each buys) · **Prerequisites:** `a-http-depth` (headers, cookies), `b-xss` (CSP as defense in depth), `b-csrf` (SameSite), `b-session-auth` (cookie flags)

---

## 1. Where this shows up

Security headers are the cheapest defense-in-depth in web security: a handful of response headers that change how the browser treats your pages — blocking inline scripts, upgrading connections to HTTPS, refusing to be framed. They sit in **OWASP Top 10:2025 A02 — Security Misconfiguration** (their absence is the finding) and are the fix layer behind `b-xss`, `b-csrf`, and `b-session-auth`. Every AppSec review and every hardening checklist grades them, and verifying them is a pure curl exercise — no lab account needed.

## 2. Before you start

- You can read response headers with `curl -I` / `curl -D` (`a-http-depth`).
- You know what CSP, SameSite, and cookie flags are for from the lessons above — this lesson makes them deployable.
- **Authorization:** the walkthrough runs a demo server on your own loopback interface. Header verification against any other target follows the same rule as every other lesson: your machines, your labs, or written scope. Reading headers is a request like any other.
- Tooling: Python 3 (stdlib only, plus its `ssl` module for the HTTPS check), curl, openssl (for the self-signed certificate).

## 3. How it works

A response header is the server giving the browser instructions about the page it just sent. Most headers are informational; the security headers change browser *behavior*. Each one answers one question the browser would otherwise answer unsafely by default. Learn them as six independent controls, because that is how they deploy and how they fail:

**Content-Security-Policy (CSP)** — the allow-list for what the page may load and run. `Content-Security-Policy: default-src 'self'` tells the browser: scripts, styles, images — everything — must come from our own origin. Inline `<script>` blocks and inline event handlers (`onerror=`, `onload=`) are blocked unless explicitly allowed. The strict form uses a per-response **nonce** (a random value the server generates, puts in the header *and* in each legitimate `<script nonce="…">` tag) or a **hash** of each legitimate script. The attacker's injected script doesn't know the nonce, so the browser refuses to run it. What it buys: it shrinks XSS from "full compromise" to "defaced markup" — the injection still happened, but the script doesn't execute. What it doesn't: it is not a substitute for output encoding (`'unsafe-inline'` in the policy re-opens the hole), and it only constrains *loading and execution*, not data theft via already-allowed channels. Violations can be reported back via `report-uri` / `report-to` — the telemetry from `b-xss`'s walkthrough.

**Strict-Transport-Security (HSTS)** — `Strict-Transport-Security: max-age=31536000; includeSubDomains` tells the browser: for the next year, *only* talk to this host over HTTPS, and upgrade any `http://` URL automatically — no click-through past certificate warnings. What it buys: it kills SSL-stripping (the attacker downgrading the victim to plaintext HTTP), because the browser refuses to speak HTTP at all. What it doesn't: it only takes effect *after the first HTTPS visit* (the bootstrap problem — solved by HSTS preload lists, which browsers ship), and it is meaningless on a site that doesn't serve HTTPS.

**X-Frame-Options / frame-ancestors** — `X-Frame-Options: DENY` (legacy) or `Content-Security-Policy: frame-ancestors 'self'` (current) tells the browser which origins may embed this page in a frame. What it buys: it defeats **clickjacking** — the attack where a transparent iframe of your "delete account" page sits under the attacker's "win a prize" button and the victim's click lands on your page. `frame-ancestors` supersedes `X-Frame-Options`; send the CSP directive on modern deployments.

**X-Content-Type-Options: nosniff** — tells the browser not to second-guess the `Content-Type`. Without it, a browser receiving `Content-Type: text/plain` containing `<script>` may "sniff" it as HTML and execute it — turning a file upload or an API response into stored XSS. One header, one behavior change, whole class of MIME-confusion bugs closed.

**Referrer-Policy** — controls how much of the URL the browser sends in the `Referer` header when navigating away. `Referrer-Policy: strict-origin-when-cross-origin` (the modern default in most browsers) sends the full URL same-origin but only the origin cross-origin. Why it matters: password-reset tokens, session ids, or search terms in query strings leak through Referer to third parties — the policy decides how much leaks.

**Cookie flags** (`Secure`, `HttpOnly`, `SameSite`) — set on the `Set-Cookie` itself, from `b-session-auth`: `Secure` = never send over plaintext HTTP; `HttpOnly` = invisible to JavaScript (XSS can't `document.cookie` it); `SameSite=Lax` = don't send on cross-site POSTs (the CSRF baseline from `b-csrf`). Not headers in the strict sense, but they are verified the same way — by reading `Set-Cookie` — and they belong in every header audit.

### The verification habit

Every header in this lesson is verified the same way: `curl -s -D - -o /dev/null <url>` and read what the server actually sent. Not what the framework's documentation promises, not what the config file says — what arrives on the wire. Header audits are diffed against a baseline: the expected set for the page type. A missing CSP on an HTML page is a finding; a missing CSP on a JSON API is usually fine (no execution context — though `nosniff` still matters there).

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-security-headers.log`. Clean environment: stock Python 3.12, curl 8.5.0, openssl, loopback only, 2026-10-09. The demo (`headers-demo.py`, stdlib only) serves a small page on 127.0.0.1:18098 (HTTP) and, with a self-signed certificate, on 127.0.0.1:18099 (HTTPS).

**Step 1 — start the bare demo.** Run `python3 headers-demo.py 18098 &`. `curl -s -D - -o /dev/null http://127.0.0.1:18098/` — the response carries no security headers at all. This is the baseline most default configurations ship: the absence *is* the finding.

**Step 2 — add the header set.** Restart with `SECURED=1`. `curl -s -D - -o /dev/null http://127.0.0.1:18098/` now shows: `Content-Security-Policy: default-src 'self'; frame-ancestors 'self'`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and (legacy, belt-and-braces) `X-Frame-Options: DENY`. Read each one and state what it buys, from section 3 above, before moving on.

**Step 3 — CSP blocks the `b-xss` payload.** The secured page reflects `?q=` HTML-encoded (encoding is still the fix), but also carries the CSP. Request `/?q=<img src=x onerror=alert(1)>`: the response shows the payload HTML-encoded *and* the CSP header present. Two independent layers: even if the encoding regressed, `default-src 'self'` with no `'unsafe-inline'` would stop the inline handler from executing. **Re-ran 2026-10-10 — now RUN BY US:** headless Chromium via Playwright; an unencoded inline-handler payload served with `default-src 'self'` did NOT execute (`window.__fired` stayed false) and the console logged the CSP violation. The reader confirms the block in a browser's devtools console. See `runs/b-security-headers.log` re-run entry.

**Step 4 — clickjacking defense.** The secured page sends `frame-ancestors 'self'`. An attacker's framing page (`/attacker`, served by the same demo for illustration) contains `<iframe src="http://127.0.0.1:18098/">`. The header is verified present on the framed response; per the CSP specification the browser refuses to render it cross-origin. **Re-ran 2026-10-10 — now RUN BY US:** headless Chromium via Playwright; a cross-origin framing page was refused (`frame-ancestors 'self'` violation in the console, subframe never committed). Note: same-origin framing is correctly *allowed* by `frame-ancestors 'self'` — the refusal manifests cross-origin, which is the actual clickjacking threat model. See `runs/b-security-headers.log` re-run entry.

**Step 5 — MIME sniffing.** The bare demo serves `/download?name=x` as `Content-Type: text/plain` with body `<script>/*looks like html*/</script>`. On the secured build the same route sends `X-Content-Type-Options: nosniff`: the browser is instructed not to reinterpret it as HTML. Verified by header presence on both builds; the behavior change is per the WHATWG fetch specification.

**Step 6 — HSTS over real HTTPS.** Generate a self-signed certificate (`openssl req -x509 -newkey rsa:2048 -keyout /tmp/hkey.pem -out /tmp/hcert.pem -days 1 -nodes -subj "/CN=127.0.0.1"`), start the demo with `TLS=1` on 127.0.0.1:18099, and `curl -sk -D - -o /dev/null https://127.0.0.1:18099/` — the response carries `Strict-Transport-Security: max-age=31536000; includeSubDomains`. Note the honest boundary, stated on the page: HSTS was verified as *sent*; its *enforcement* (the browser refusing future HTTP) is browser behavior, and the bootstrap caveat (first visit) plus preload are taught as concepts, not demonstrated.

**Step 7 — cookie flags.** `curl -s -D - -o /dev/null -X POST -d "user=alice&pass=x" http://127.0.0.1:18098/login | grep -i "^set-cookie"` → `sid=<hex>; HttpOnly; SameSite=Lax; Path=/` (and `Secure` on the HTTPS build). Same verification habit as the headers: read the wire.

**Step 8 — the audit as a script.** The transcript ends with a ten-line header-audit script: fetch the URL, assert the expected header set per content type, exit nonzero on any missing header. This is the artifact pattern from section 9 — the check that runs in CI, not in a human's memory.

**Step 9 — stop the demo.** `pkill -f headers-demo.py`; verify no demo processes remain and nothing listens on 18098/18099.

## 5. On your own

Run the audit script from step 8 against three real sites you use (read-only `curl` — you are only reading their headers, which is what every browser does on every visit; stay within the authorization rules for anything beyond that). For each missing header, write one sentence on what attack it would mitigate *for that specific site*. **Success test:** your report distinguishes "missing CSP on an HTML page" (finding) from "missing CSP on a JSON API" (usually fine) and says why.

## 6. Where it goes wrong

- **CSP with `'unsafe-inline'`.** The single most common CSP failure: the policy allows inline scripts, which re-opens exactly the hole it was meant to close. If your CSP contains `'unsafe-inline'`, you have a compliance checkbox, not a defense. Nonces or hashes are the way out.
- **HSTS without HTTPS everywhere.** Sending HSTS over a plaintext redirect chain, or with a `max-age` of minutes, provides theater. It must be served over HTTPS, with a long max-age, `includeSubDomains`, and preload submission to cover first visits.
- **X-Frame-Options instead of frame-ancestors.** The legacy header is still honored, but `frame-ancestors` is the standard and supersedes it. Sending both with conflicting values is a misconfiguration — pick the CSP directive as canonical.
- **Headers on the wrong content type.** CSP on a JSON API response is harmless but pointless; `nosniff` on that same API is load-bearing. Audit per content type, not per domain.
- **`Referrer-Policy` ignored.** The default in modern browsers is already sane (`strict-origin-when-cross-origin`), which tempts teams to skip it — until a legacy integration or an explicit `unsafe-url` somewhere leaks tokens. Set it explicitly; defaults change.
- **Cookie flags forgotten on subdomains.** `Secure` without `__Host-` prefix discipline, or a session cookie set without `SameSite` on an API the SPA calls cross-site, re-opens the CSRF and theft vectors from `b-csrf` and `b-session-auth`. The flags are part of the header audit, not a separate concern.

## 7. Read the source

Primary documents — read in this order:

1. **OWASP Secure Headers Project** (owasp.org/www-project-secure-headers/): the header catalog — what each header does, with configuration guidance. Read the header reference fully. *Verified in-session 2026-10-09.*
2. **MDN — Content Security Policy guide** (developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP): directives, nonces, hashes, the `unsafe-inline` warnings. Read the XSS-defense and nonce sections; skim the rest. *Verified in-session 2026-10-09.*
3. **RFC 6797 — HTTP Strict Transport Security** (rfc-editor.org/rfc/rfc6797): the HSTS mechanism — max-age, includeSubDomains, preload semantics. Read §6–§8; skim the rest. *Cited as primary lead — fetch at build time before linking.*

Free resources for going deeper (≤3): **MDN HTTP headers reference** (per-header semantics, browser support tables); **the OWASP Secure Headers validator** (the project's own checking tool — run it against your labs); **Google's CSP evaluator** (paste a policy, get the bypasses — teaches you to read policies adversarially).

## 8. Check yourself

1. A page sends `Content-Security-Policy: default-src 'self' 'unsafe-inline'`. An attacker achieves stored XSS on it. Explain precisely what the policy still blocks and what it fails to block — and the minimal policy change that fixes it.
2. Why does HSTS do nothing against an attacker who intercepts the victim's *very first* visit to the site? Name the mechanism that addresses this and where it lives.
3. A JSON API sends no CSP but does send `X-Content-Type-Options: nosniff`. Is the missing CSP a finding? Is the `nosniff` load-bearing? Justify both answers from the execution-context argument.
4. `frame-ancestors 'self'` and `X-Frame-Options: ALLOW-FROM https://partner.example` are both present with different meanings. Which wins in a modern browser, and why is the combination a misconfiguration?
5. A session cookie is set with `Secure; HttpOnly` but no `SameSite` attribute. Name the attack class this leaves open and the header from `b-csrf`'s lesson that would have closed it.

## 9. Prove it

**Artifact:** a header-audit report for three targets (your lab apps, then — within the rules — sites you use): the full response-header set per page type, each missing header named with the attack it would mitigate *for that page*, and the audit script itself, committed, so the check is repeatable. Re-run it after hardening and show the diff.

**After this lesson you can honestly claim:** you can audit any site's browser-defense posture with curl, explain what each header buys and where each fails, and deploy the set correctly. **You cannot yet claim:** your CSP survives adversarial review against bypass techniques (nonce leakage, JSONP endpoints, overly broad allow-lists) — that is AppSec-track work, built on this foundation.

## 10. Leads to

Next: the second-wave lessons (authentication flaws, SSTI, JWT/OAuth — each assumes the header layer from this lesson is in place). Map refs: **OWASP Top 10:2025 A02 — Security Misconfiguration**; WSTG-CONF (configuration testing); CWE-693 (protection mechanism failure); closes the loop on `b-xss` (CSP), `b-csrf` (SameSite/frame-ancestors), and `b-session-auth` (cookie flags).
