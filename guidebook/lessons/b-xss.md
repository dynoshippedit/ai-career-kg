# Cross-site scripting: when the browser can't tell your code from the attacker's

**ID:** `b-xss` · **Stage:** B (Practitioner) · **Level:** 3 (mechanism + live reproduction of all three types + fix verification) · **Prerequisites:** `a-http-depth` (requests, responses, cookies), Stage A JavaScript reading (you must read a DOM sink cold), B-AUTH (authorization discipline)

---

## 1. Where this shows up

Every application that renders user input in a page can carry XSS, which makes it the most common web vulnerability class you will meet in bounty programs and penetration tests. It sits in **OWASP Top 10:2025 A05 — Injection** and is tested per **WSTG-INPV-01/02**. The same mechanism — untrusted data crossing a trust boundary into an execution context — reappears in the AI track (prompt injection) and in every client-side bug you will ever triage, so learn it once and learn it properly.

## 2. Before you start

- You can read HTTP requests and responses cold (`a-http-depth`), including where a cookie travels.
- You can read basic JavaScript: `document.getElementById`, `innerHTML`, event handlers, `location.hash`.
- **Authorization:** everything in the walkthrough runs against a demo app on your own loopback interface, plus PortSwigger's hosted labs (permission granted by design). Never inject markup into a site you don't own or aren't scoped to test. A reflected-XSS probe is a request like any other — the law doesn't care that it was "just a test string."
- Tooling: Python 3 (stdlib only), curl. A browser with devtools for the reader-side steps.

## 3. How it works

Start from the one fact the whole class hangs on: **the browser cannot distinguish the site's own JavaScript from JavaScript an attacker smuggled into the page.** The same-origin policy walls off *other sites'* scripts from your site's data — but anything executing in your page's origin *is* your origin. It reads your cookies (the non-HttpOnly ones), calls your APIs with your credentials, and acts as you. XSS is the art of getting the victim's browser to run the attacker's script inside the victim's session.

So the vulnerability is never "JavaScript exists." It is always: **untrusted data crossed into an execution context without being neutralized.** The three types are three different routes across that boundary:

**Reflected XSS** — the malicious input arrives in the current HTTP request and is copied into the immediate response, unsanitized. The classic shape: `/search?q=<script>…</script>` and the response contains `<p>Results for <script>…</script></p>`. The attack needs a delivery mechanism — a crafted link the victim clicks, or a form the victim submits — because the payload doesn't persist. Found by: submit a unique string into every input, then search every response for where it reappears, and in *which context*.

**Stored XSS** — the input is persisted (database, file, message queue) and rendered unsanitized in *later* responses to *other* users. A comment field, a username, a support ticket. No crafted link needed: the victim just visits the page. This is the type that turns one injection into a worm, because every viewer is a new victim and every victim's actions run as them.

**DOM-based XSS** — the vulnerability lives in client-side JavaScript, not in any server response. The server returns perfectly innocent code like `el.innerHTML = location.hash.slice(1)`, and the *browser* does the dangerous thing when it processes attacker-controlled data (the URL fragment, `document.cookie`, `postMessage` data). Server-side scanning cannot see it; the payload never crosses the wire in a form the server inspects. You find it by reading the JavaScript.

### Contexts: where the data lands decides the payload

"Output encoding" is not one operation. The correct neutralization depends on the *context* — where in the document the data lands:

- **HTML body** (`<p>USER-DATA</p>`): encode `<`, `>`, `&`, quotes. `&lt;script&gt;` renders as text.
- **HTML attribute** (`<input value="USER-DATA">`): quote the attribute *and* encode; an unquoted attribute breaks out with a space.
- **JavaScript string** (`var name = "USER-DATA";`): encode for the JS context — HTML-encoding is *not enough* here, because the browser decodes HTML entities before the JS parser runs.
- **URL** (`<a href="USER-DATA">`): validate the scheme; `javascript:` URLs execute.

The canonical failure the walkthrough demonstrates: data lands in an HTML body context and the developer encoded *nothing*, so `<img src=x onerror=…>` becomes live markup. The subtler failure: the developer HTML-encoded data that lands inside a `<script>` block, and the attacker's payload survives because the JS parser sees through the encoding.

### Worked example: the search page

A search page takes `?q=` and renders `<h2>Results for: {q}</h2>` with no processing. Request `/search?q=hello` → the response contains `Results for: hello`. Request `/search?q=<b>hi</b>` → the response contains a real bold element: the input was reflected as *markup*, not text. The context is HTML body, so the fix is HTML-encoding on output: the response should contain `Results for: &lt;b&gt;hi&lt;/b&gt;`, which renders as inert text. One fact to carry forward: **the reflection is the finding's location; the missing encoding is the finding's cause.** Your report names both.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-xss.log`. Clean environment: stock Python 3.12, curl 8.5.0, loopback only, 2026-10-09. The demo app (`xss-demo.py`, stdlib only) exposes three routes: `/search?q=` (reflected), `/guestbook` (stored notes), `/dom` (a page whose script writes `location.hash` into the DOM). Proof markers are benign DOM writes — no `alert()` anywhere, per the guidebook's own discipline (see `b-idor`). Actual script *execution* happens only in a browser; the curl-visible steps prove the injection reaches the page unneutralized, and steps 4 and 6 re-ran 2026-10-10 in headless Chromium (see below) — the reader confirms execution in a PortSwigger lab too.

**Step 1 — start the demo.** Run `python3 xss-demo.py 18091 &`; it binds 127.0.0.1:18091 and logs to stdout.

**Step 2 — reflected: prove the echo.** `curl -s "http://127.0.0.1:18091/search?q=UNIQUE-STRING-42"`. The response contains `<h2>Results for: UNIQUE-STRING-42</h2>`. Unique string in, unique string out, no transformation: this is the reflection point.

**Step 3 — reflected: prove it's markup, not text.** `curl -s "http://127.0.0.1:18091/search?q=<b>BOLD-PROBE</b>"`. The response contains a literal `<b>BOLD-PROBE</b>` element. The input crossed into an HTML-body context and became live markup. In a browser this renders bold; with an event-handler payload it would execute. This is the vulnerability, confirmed.

**Step 4 — reflected: the benign execution marker.** `curl -s "http://127.0.0.1:18091/search?q=<img%20src=x%20onerror=%27document.getElementById(%22v%22).textContent=%22EXEC-REFLECTED%22%27>"`. The response contains the `onerror` handler verbatim, unencoded. **Re-ran 2026-10-10 — now RUN BY US:** headless Chromium via Playwright; the marker fired for real (`#v` text became `EXEC-REFLECTED`). See `runs/b-xss.log` re-run entry. The reader does this exact step in PortSwigger's reflected-XSS lab, where the marker firing is the solve condition. What we proved by curl: the payload reaches the page byte-identical and unneutralized — the only remaining step is a browser parsing it, which is what browsers do.

**Step 5 — stored: plant the note.** `curl -s -X POST -d "note=STORED-PROBE-<b>bold</b>" http://127.0.0.1:18091/guestbook`. Then `curl -s http://127.0.0.1:18091/guestbook` — the note renders with live `<b>` markup. Now fetch it a second time, from a *fresh* curl with no cookies: same result. The payload persists server-side and executes for every viewer. That persistence is what makes stored XSS the highest-impact type.

**Step 6 — DOM: read the sink.** `curl -s http://127.0.0.1:18091/dom` and read the served script: `var el = document.getElementById('out'); el.innerHTML = decodeURIComponent(location.hash.slice(1));`. The server never sees the fragment (fragments aren't sent to servers); no server-side filter could catch this. The sink is `innerHTML` — an execution context. `textContent` would have been safe. **Re-ran 2026-10-10 — now RUN BY US:** headless Chromium via Playwright; the fragment payload executed through the `innerHTML` sink (`#out` text became `EXEC-DOM`). The reader confirms in PortSwigger's DOM-XSS lab. See `runs/b-xss.log` re-run entry.

**Step 7 — the fix, all three types.** Restart the demo with `FIXED=1`: `/search` now HTML-encodes output, `/guestbook` encodes on render, `/dom` uses `textContent`. Re-run steps 2–5: the `<b>` probe returns as `&lt;b&gt;` inert text; the `onerror` payload returns encoded and harmless. The search page additionally sends `Content-Security-Policy: default-src 'self'` (the header lesson is `b-security-headers`; here it is defense in depth — even the unencoded payload couldn't load an external script).

**Step 8 — defender: watch the probes land.** Read the demo's access log: the reflection probes appear as ordinary GETs with long, markup-bearing query strings — noisy and signature-friendly (`<script`, `onerror=`, `javascript:`). The stored-XSS plant is a single quiet POST; its *detonation* is invisible in request logs and only visible in a CSP violation report or a content review. That asymmetry is the defender's lesson: reflected probes are WAF-fodder; stored payloads are found by CSP reports and by reviewing rendered content, not by request signatures.

**Step 9 — CSP violation report (simulated).** The fixed app exposes `/csp-report`. `curl -s -X POST -H 'Content-Type: application/csp-report' -d '{"csp-report":{"blocked-uri":"inline","violated-directive":"script-src"}}' http://127.0.0.1:18091/csp-report` → `204`. In production these reports are the highest-fidelity XSS-attempt telemetry you own: they come from the victim's browser, naming exactly what the policy blocked.

**Step 10 — stop the demo.** `pkill -f xss-demo.py`; verify with `pgrep -f xss-demo.py` returning nothing.

## 5. On your own

Extend the demo (or your PortSwigger lab target): find one reflection point the walkthrough didn't cover — an attribute context (`?q=` inside `<input value="…">`), a JavaScript-string context, or a `javascript:` URL context — and for each, state the context, the minimal probe that proves live markup, and the correct encoding for that context. **Success test:** your probe renders inert text after the fix, and you can explain *why* HTML-encoding alone fails in the JS-string context.

## 6. Where it goes wrong

- **Encoding for the wrong context.** HTML-encoding data that lands in a `<script>` block or an event handler is the classic incomplete fix — the browser decodes entities before the JS parser runs, so the payload survives. Encode for the context the data *lands in*, not the context it came from.
- **Blacklist filtering.** Stripping `<script>` while allowing `<img onerror>`, `<svg onload>`, `<body onload>`, or `javascript:` URLs is a bypass waiting to happen. Encoding on output beats filtering on input, every time.
- **"It needs a click, so it's low severity."** Reflected XSS needs user interaction, yes — but the crafted link can be one click inside a phishing email, and stored XSS needs none. Severity follows impact on the *application's* data, not the payload's elegance.
- **CSP as the only fix.** CSP is mitigation, not remediation: it reduces what an injected script can do, but misconfigured policies (`unsafe-inline`, overly broad `script-src`) are bypassable, and the underlying injection is still a vulnerability. Fix the encoding; keep the CSP as depth.
- **DOM XSS blind spot.** Scanners and server logs are nearly blind to DOM-based XSS. If your methodology is "proxy and grep responses," you will miss the entire class — reading client-side JavaScript is the only reliable detection.
- **Framework false confidence.** Modern frameworks auto-escape in templates — until you use `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, or template injection into scripts. Audit the escape hatches, not the framework's marketing.

## 7. Read the source

Primary documents — read in this order, skipping as marked:

1. **PortSwigger Web Security Academy — Cross-site scripting** (portswigger.net/web-security/cross-site-scripting): the topic page — types, contexts, prevention checklist. Read fully; then work the reflected/stored/DOM labs (the largest Academy topic — dozens of labs, free).
2. **MDN — Content Security Policy guide** (developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP): directives, nonces, hashes, `unsafe-inline` warnings. Read the "how CSP protects against XSS" and nonce sections; skim the rest.
3. **OWASP XSS Prevention Cheat Sheet** (cheatsheetseries.owasp.org): the output-encoding rules per context. *Slug unverified at build — confirm the exact cheat-sheet URL before linking; the rule content is corroborated by the PortSwigger and MDN pages above.*

Free resources for going deeper (≤3): **PortSwigger XSS labs** (the hands-on companion — reflected, stored, DOM, filter bypasses); **MDN CSP reference** (directive-by-directive semantics); **the `b-security-headers` lesson** (this guidebook — CSP as deployed defense).

## 8. Check yourself

1. A search page reflects your input inside a `<script>var q = "INPUT";</script>` block. You HTML-encode the input. Why can an attacker still execute JavaScript, and what encoding is actually required?
2. Explain why a stored XSS in a comment field is more severe than a reflected XSS in a search field, even when both execute the same payload.
3. A developer "fixes" reflected XSS by stripping the literal string `<script` from input. Give two payloads that bypass this, and explain what each relies on.
4. Why is DOM-based XSS invisible to a proxy that only inspects HTTP requests and responses?
5. A page sets `Content-Security-Policy: script-src 'self'` and still gets exploited via XSS. Name two ways the underlying injection could still execute script, and explain what the policy did and didn't buy.

## 9. Prove it

**Artifact:** a three-part write-up — one reflected, one stored, one DOM-based finding — each with the reflection/sink location, the context, the benign proof marker, and the fix (encoding + context named), produced against a lab target (PortSwigger labs or your local demo). Include the CSP report (or its absence) as part of the evidence.

**After this lesson you can honestly claim:** you can find and prove all three XSS types on an authorized target, name the output context, and apply the correct encoding plus a CSP. **You cannot yet claim:** your fixes survive a determined bypass review — that needs the header-hardening in `b-security-headers` and the methodology discipline of `b-business-logic`'s trust-boundary review applied to every rendering path.

## 10. Leads to

Next: `b-business-logic` (the methodology lesson — XSS taught you contexts; now learn to map whole workflows), then `b-security-headers` (deploying CSP, HSTS and cookie flags as the browser-defense layer). Map refs: **OWASP Top 10:2025 A05 — Injection**; WSTG-INPV-01/02; CWE-79; feeds `ai-prompt-injection` (same trust-boundary shape, new substrate).
