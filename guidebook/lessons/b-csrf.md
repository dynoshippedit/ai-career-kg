---
lesson_id: b-csrf
slug: csrf
stage: B
level: 3
prerequisites: [a-http-depth, b-idor]
roles: [pentester, appsec]
map_refs: []
test_date: 2026-10-10
description: "CSRF: when the victim's browser does the attacker's work — token defense, SameSite, and the no-state-changing-GET rule. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · local demo app; browser-click sub-step re-ran 2026-10-10 (headless Chromium)"
---
# CSRF: when the victim's browser does the attacker's work


**Map refs:** OWASP Top 10:2025 A01 · WSTG-SESS-05 · CWE-352

---

## 1. Where this shows up

Cross-site request forgery is the attack where the victim's own browser issues the malicious request — authenticated, cookie-attached, indistinguishable from legitimate traffic. It sits in **OWASP Top 10:2025 A01** and carries **CWE-352**. You will meet it in every cookie-sessioned application with state-changing actions: email changes, password changes, transfers, privilege grants. It is also the lesson that teaches the single most repeated rule in web security: **no state changes via GET — ever.** From the defender's side, it is nearly invisible to signature WAFs (the forged request is syntactically identical to a real one), which is why the fix is design, not detection.

## 2. Before you start

- You can read HTTP requests and responses cold (`a-http-depth`), and you know what the browser attaches automatically: cookies, including session cookies, on every request to the cookie's domain.
- You know the same-origin policy's shape: one site's script can't *read* another site's responses — but it can *cause* the browser to *send* requests there. That asymmetry is this entire lesson.
- Your target is written down and authorizes your testing: your own local lab (this lesson's demo app), a PortSwigger Academy CSRF lab, DVWA's CSRF module, or a bounty program whose scope explicitly includes the asset. The "attacker's page" in this lesson is a local HTML file you open in your own browser against your own lab — never hosted against someone else's site. Re-read B-AUTH if this sentence surprised you.
- Tooling: curl plus a browser with two profiles (or containers) so you can hold a victim session and an attacker page apart.

## 3. How it works

Three conditions must hold — PortSwigger's framing, worth memorizing:

1. **A relevant action.** Something the attacker wants done: change an email, change a password, transfer funds.
2. **Cookie-based session handling.** The application identifies the user *solely* by the session cookie. No other proof travels with the request.
3. **No unpredictable request parameters.** Every parameter the action needs is guessable — no per-request secret.

When all three hold, the attack is one HTML page on the attacker's site:

```html
<form action="https://vulnerable-site/email/change" method="POST">
  <input type="hidden" name="email" value="attacker@evil.example">
</form>
<script>document.forms[0].submit();</script>
```

The victim visits the page (a link, an embedded comment, any lure). The browser submits the form to the vulnerable site — and **automatically attaches the victim's session cookie**, because that's what browsers do with cookies. The vulnerable site sees a well-formed, authenticated request to change the email, and complies. It cannot distinguish this from the victim doing it deliberately, because nothing in the request proves intent — the cookie proves *identity*, and identity is all the site asked for.

**The state-changing-GET lesson.** If the action also works via GET (`/email/change?email=attacker@evil.example`), the attack needs no form at all — a single `<img src="...">` tag fires it, and the exploit becomes a URL that can be fed directly to victims. This is why the rule is absolute: GET requests must never change state. A GET that changes state collapses the attacker's work to one line and removes every defense that depends on request shape.

**The token defense — generation, binding, verification.** The synchronizer token pattern breaks condition 3 by adding a per-request secret the attacker's page cannot know:

- **Generation:** cryptographically random, unique per session at minimum (per-request tokens are stronger but break back-button flows — know the tradeoff). Never derive it from the user ID or email alone.
- **Binding:** the token must be tied to the authenticated session. The naive double-submit pattern (cookie value == request value, no session binding) falls to cookie injection from a sibling subdomain or a network position on plaintext HTTP. The signed variant HMACs session data into the token so a planted cookie can't forge it.
- **Verification:** constant-time comparison of the request-supplied token against the session-bound value; **reject on missing *or* mismatched**; never accept the cookie value as the proof — cookies are auto-sent, and that's the whole vulnerability.
- **Transmission:** hidden form field or custom header — never the URL (leaks via history, logs, Referer).

**SameSite: the browser's own checkpoint.** `Strict` — cookie never sent cross-site (strongest; breaks legitimate cross-site flows like SSO callbacks). `Lax` — sent on top-level GET navigations, not on POSTs or subrequests; the browser default since 2021. `None` — sent cross-site, requires `Secure`. The lesson point: **SameSite=Lax is a baseline, not a complete defense** — GET-based state changes and Lax-bypass techniques (top-level GET with side effects, method override) still get through. Set `Lax` minimum on session cookies, `Strict` where flows allow, and keep the token as the real defense.

**Where the other patterns fail.** Custom headers (`X-CSRF-Token` via JavaScript) are strong for AJAX APIs — cross-site pages can't set custom headers on simple requests — but fail if the API also accepts form-encoded requests without the header, or if CORS is misconfigured. Referer/Origin validation is cheap defense-in-depth but fails when browsers strip Referer (privacy settings, HTTPS→HTTP downgrade) — it must fail *closed* and never stand alone. Fetch Metadata headers (`Sec-Fetch-Site`) let the server reject `cross-site` values on state-changing endpoints — modern and strong where supported, a layer rather than the only one. And the strongest per-action control for high-value operations is user interaction: re-authentication or OTP.

**How defenders see it.** Barely, at the signature layer: the forged request is syntactically identical to a legitimate one, so CSRF is nearly invisible to WAFs. Detection is application-layer: log state-changing requests with missing/invalid tokens (log the *event*, never the token value), Referer/Origin mismatches on POST endpoints, and GET requests hitting state-changing endpoints. This is why the lesson teaches CSRF as a design flaw, not a payload problem.

### Worked example: the profile demo

A minimal profile app (stdlib Python, local only — the walkthrough runs it). Login at `POST /login` sets a session cookie; `POST /change-email` with `email=<addr>` changes the account email — no token, no Origin check. A second endpoint, `GET /change-email-get?email=<addr>`, does the same thing via GET, deliberately, so the lesson can demonstrate the rule.

Baseline: log in as the victim, `POST /change-email` with the cookie — email changes. The server-side proof: `curl -X POST -b victim-cookie /change-email -d email=attacker@evil.example` with *no token and no Origin header* succeeds. If a bare cross-site-shaped request succeeds, the attacker's auto-submit form would too — the form adds nothing the server checks. Then the attacker's page (a local HTML file): open it in the browser while logged in, watch the email change — the browser attached the cookie, the server complied. Then the GET variant: loading `<img src="http://127.0.0.1:8327/change-email-get?email=attacker@evil.example">` changes the email with no form at all.

The fix, in the same app: per-session synchronizer tokens (cryptographically random, stored server-side in the session), validated with constant-time comparison, rejecting missing *or* mismatched; the GET variant removed entirely (state changes require POST + token); session cookie set with `SameSite=Lax`. Re-test: the bare cross-site-shaped POST → `403`; the attacker's form → `403` (no valid token); the legitimate in-app form (which carries the token) → `200`. Defense in depth noted: Origin check and `Sec-Fetch-Site` validation as additional layers, step-up auth for the password-change equivalent.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-csrf.log`. Clean environment: stock Python 3.12, curl 8.5.0, loopback only, 2026-10-09. The demo app stands in for the PortSwigger/DVWA targets the reader uses (no Docker on this machine — see gaps).

1. **Start the vulnerable app.** Save the `app.py` from this lesson's companion (login, cookie sessions, `POST /change-email` with no token, `GET /change-email-get` deliberately) and run it on port 8327. Log in as the victim (`POST /login`, user `victim`); capture the session cookie.
2. **Baseline.** `curl -b <cookie> -d 'email=victim@example.com' localhost:8327/change-email` — email changes. This is the control: what legitimate use looks like.
3. **Server-side proof of CSRF.** `curl -X POST -b <cookie> -d 'email=attacker@evil.example' localhost:8327/change-email` with no token, no Referer, no Origin — observe `200` and the changed email. Write it down: the server accepted a request shaped exactly like a forged one. This is the finding, proven without a browser.
4. **The attacker's page.** Save the companion's `evil.html` (auto-submitting form targeting the local app), open it in a browser logged in as the victim — observe the email change to the attacker's address. The browser attached the cookie; the server couldn't tell the difference. (Local file, local app, your own accounts — this is the authorized shape of the exercise. **Update 2026-10-10: now RUN BY US** — headless Chromium via Playwright installed; the attacker's auto-submit page was opened in a victim-logged-in browser context and the email changed from `victim@example.com` to `attacker@evil.example` for real. See `runs/b-csrf.log` re-run entry.)
5. **The state-changing GET.** `curl 'localhost:8327/change-email-get?email=attacker2@evil.example'` — no cookie needed beyond the session, no form, one URL. Write down why this is worse: the exploit is a link, and every GET-based defense assumption collapses.
6. **Apply the fix.** Patch the app: per-session random tokens issued at login, required on every state-changing POST, constant-time compare, reject missing/mismatched; delete the GET variant; `SameSite=Lax` on the session cookie. Restart, log in again (new session, new token).
7. **Verify the fix — four cases.** Bare forged-shaped POST (no token) → `403`; wrong token → `403`; missing token → `403`; legitimate in-app form (fetch the form, extract the token, submit) → `200` and the email changes. Confirm the `Set-Cookie` header carries `SameSite=Lax`.
8. **Read the defender view.** Open the app's security log: find your token-less POSTs (logged as rejected CSRF events — event logged, token value never logged) and the GET-variant hits. Write the detection rule: alert on state-changing endpoints receiving requests with missing/invalid tokens, and on any GET to a state-changing path.

No step above is marked "not run by us" — the server-side proof, the browser page (re-ran 2026-10-10 with headless Chromium; the forged POST fired from the attacker's page for real), the GET variant, the fix, and all four verification cases ran locally.

## 5. On your own

**Task:** Pick one authorized target you have not touched in this lesson — a PortSwigger Academy CSRF lab (the "no defenses" email-change lab is the closest match), or DVWA's CSRF module. First, determine server-side whether the endpoint is vulnerable: replay the state-changing request with curl, stripped of any token/Referer/Origin, and see if it succeeds. Then build the minimal HTML proof (form or single URL) and confirm it in your browser against your own lab account. Then check the GET question: does the action work via GET?

**Success test:** A one-page report: the vulnerable action, the three-condition analysis (relevant action / cookie sessions / no unpredictable parameter), the server-side proof (exact requests), the HTML proof result, the GET finding, the fix (token pattern + SameSite + no-GET, stated as code-level remediation), and the defender detection (which log, which events). If the lab has a token defense, characterize it instead: per-session or per-request, bound to the session or naive double-submit — and say which bypass you'd try first.

## 6. Where it goes wrong

- **State changes via GET.** The single most repeated rule in this lesson. Every GET-based action is a one-line exploit; fix by requiring POST + token, not by hiding the URL.
- **Checking the cookie as the proof.** Comparing the request's token against the *cookie* value instead of the *session* value — cookies are auto-sent, so this "validates" the attacker's request. The token must be verified against server-side session state (or a session-bound HMAC).
- **Rejecting only mismatches.** Accepting a *missing* token ("no token, no check") reopens everything. Reject on missing *or* mismatched.
- **Token in the URL.** Leaks via history, logs, Referer — the token becomes the vulnerability. Hidden field or custom header.
- **SameSite as the only defense.** Lax is the baseline; GET-based actions and bypass techniques get through. The token is the defense; SameSite is the seatbelt.
- **XSS anywhere on the site.** Cross-site scripting defeats every CSRF mitigation — the attacker's script reads the token from the page. CSRF defense assumes XSS is handled; note the dependency in your report.
- **Forgetting the login CSRF case.** The login form itself needs a token — otherwise an attacker can log the victim into the *attacker's* account and harvest what the victim does there.

## 7. Read the source

Primary documents first:

- **PortSwigger Web Security Academy — CSRF** (portswigger.net/web-security/csrf) — *read* fully; the canonical treatment (three conditions, the email-change example, token/SameSite/Referer defenses and their bypass labs). *Do* the labs after this lesson.
- **OWASP CSRF Prevention Cheat Sheet** (cheatsheetseries.owasp.org) — *read* the token patterns (synchronizer, signed double-submit) and the defense-in-depth section; *note* the warning that naive double-submit is bypassable via cookie injection, and that XSS defeats all CSRF mitigations.
- **draft-ietf-httpbis-rfc6265bis §5.6.7** (ietf.org — the SameSite attribute; RFC 6265 has no §4.1.2.7) — *skim* the cookie attribute semantics; cite it when you set the attribute.

Then at most three free resources:

1. **PortSwigger Academy — CSRF labs** (portswigger.net/web-security) — free, hosted, authorized; no-defense plus token-validation, SameSite, and Referer bypass labs.
2. **DVWA — CSRF module** (github.com/digininja/DVWA) — free; run locally via Docker: the Low→High ladder, and Impossible shows the token implementation.
3. **MDN — SameSite cookies** (developer.mozilla.org) — free; the browser-behavior reference for Strict/Lax/None.

## 8. Check yourself

1. Explain why the attacker's auto-submit form succeeds even though the same-origin policy stops the attacker's site from *reading* the victim's responses.
2. A state-changing action works via both POST and GET. Explain why the GET variant is worse for the defender, and state the rule that fixes it.
3. A developer validates the CSRF token by comparing the form field against the `csrf_token` cookie. Explain why this check passes for the attacker's forged request.
4. Predict what a defender sees in application logs during a CSRF token-bypass attempt, and explain why a WAF signature is a poor detector for CSRF in general.
5. The application sets `SameSite=Lax` on its session cookie and declares CSRF solved. Explain two attack shapes that still work, and what must be added.

## 9. Prove it

**Artifact:** the one-page report from "On your own": the vulnerable action, three-condition analysis, server-side proof, HTML proof, GET finding, code-level fix, defender detection.

**Honest claim:** "I can determine server-side whether a cookie-sessioned action is CSRF-vulnerable, demonstrate it with a minimal proof, and verify the synchronizer-token fix."
**Can't claim yet:** "I can bypass CSRF defenses" — token-validation bypasses, SameSite bypasses, and Referer tricks are the PortSwigger bypass labs, not claimed from this lesson.

## 10. Leads to

- B-VULN second wave: XSS — the class that defeats every mitigation in this lesson; understand the dependency.
- `b-ssrf` — compare: in CSRF the *browser* makes the forged request, in SSRF the *server* does. Which trust relationship does each abuse?
- B-DEF (defensive basics) — sit on the other side: write the application-layer alert for your own attack traffic.
- Map refs: **OWASP Top 10:2025 A01**, **WSTG-SESS-05**, **CWE-352**.
