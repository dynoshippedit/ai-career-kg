---
lesson_id: a-http-depth
slug: http-depth
stage: A
level: 3
prerequisites: []
roles: [soc-analyst, security-analyst, pentester, appsec, cloud-security, iam-engineer, grc-analyst]
map_refs: []
test_date: 2026-10-09
description: "HTTP in depth: requests, responses, cookies, JWTs and TLS — explained byte by byte, with every walkthrough step run locally. A free lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · loopback only, nothing external touched"
---
# HTTP in depth


---

## 1. Where this shows up

Everything above this lesson assumes HTTP and almost nothing below it explains it. Web vulnerability work (Stage B) is the art of sending requests a developer did not expect and reading responses the developer did not intend — you cannot do that if the request line, the headers, and the status code are magic. Traffic analysis (Stage C) is reading packet captures full of HTTP. Incident response (Stage D) is reconstructing what an attacker did from web-server logs, which are HTTP in shorthand. Authentication, sessions, APIs, and the entire AI-application stack (system prompts travel inside HTTP POST bodies) all sit on this protocol. Learn it once, properly, and every later lesson gets shorter.

## 2. Before you start

- A Linux shell with `curl` and `python3` (verify: `curl --version`, `python3 --version`).
- You can read a little Python — the demo server in the walkthrough is ~60 lines.
- No account, no cloud, no browser needed. Everything runs on `127.0.0.1`.

## 3. How it works

HTTP is a **stateless request/response protocol**: the client sends a text message describing what it wants, the server sends a text message back, and then — as far as the protocol is concerned — they forget each other. Every "session," "login," and "shopping cart" you have ever used is a trick built on top of this amnesia. Understanding HTTP means understanding exactly what is in those two messages and what each piece is allowed to mean.

A request has three parts. The **request line**: a method, a target, and the protocol version, e.g. `POST /login HTTP/1.1`. The **headers**: `Name: value` lines carrying metadata — what kind of body this is, who is asking, what credentials they present. Then a blank line, then the optional **body**: the actual payload. A response mirrors it: a **status line** (`HTTP/1.1 200 OK`), headers, a blank line, a body.

The method is the verb and it carries a contract. **GET** retrieves; it must not change anything (safe) and repeating it must be harmless (idempotent). **POST** submits data for processing — the catch-all for "do something." **PUT** replaces the resource at the target, **DELETE** removes it, **PATCH** partially modifies. **HEAD** and **OPTIONS** ask questions about a resource without fetching it. The contract matters for security: a state-changing action reachable by GET can be triggered by a mere link or image load (this is the entire basis of CSRF, Stage B). Servers are allowed to refuse methods — the correct refusal is `405 Method Not Allowed`, ideally with an `Allow` header naming what is accepted.

Status codes are grouped by their first digit, and the group tells you the story before you read anything else. **2xx** — done, here is your answer. **3xx** — look elsewhere; the `Location` header says where. **4xx** — you asked wrong (400 bad request, 401 unauthenticated, 403 authenticated-but-forbidden, 404 not found). **5xx** — the server failed itself. Two distinctions carry security weight. First, **401 vs 403**: 401 means "I don't know who you are — authenticate" (it usually arrives with a `WWW-Authenticate` header); 403 means "I know who you are and the answer is no." Confusing them leaks information about what exists. Second, **404 vs 403 on a hidden resource**: a 403 confirms the thing exists, a 404 pretends it doesn't — which one a server returns is a deliberate information-disclosure decision.

Headers are where the real work happens. A few you must know cold:

- `Host` — names the server the client wants (one IP can serve many sites; without this the server cannot route).
- `Content-Type` / `Content-Length` — describe the body. `Content-Type: application/json` tells the server to parse the body as JSON; a mismatch between what the header claims and what the body contains is a classic parser-confusion bug.
- `Set-Cookie` (response) / `Cookie` (request) — the amnesia workaround. The server says `Set-Cookie: session=abc; HttpOnly; Path=/`, and the browser dutifully returns `Cookie: session=abc` on every later request. Attributes are the security policy: `HttpOnly` hides the cookie from JavaScript (blunts XSS theft), `Secure` restricts it to HTTPS, `SameSite` controls whether it is sent on cross-site requests (the CSRF defense).
- `Authorization` — carries credentials per request, e.g. `Bearer <token>`. Unlike cookies, nothing sends it automatically; the client code must attach it.
- `Location` — the redirect target for 3xx responses.
- `WWW-Authenticate` — accompanies 401, naming the acceptable auth schemes.

Because the protocol forgets, **sessions are a server-side fiction maintained with client-side tokens**. Two designs dominate. The **opaque session cookie**: the cookie is a random string, meaningless by itself; the server looks it up in a store. Steal the string and you are the user (session hijacking) — which is why the cookie attributes and TLS matter. The **JWT**: the token carries its own claims — three base64url segments separated by dots, `header.payload.signature`. The header names the algorithm (`HS256`), the payload carries claims (`sub` for subject, `iat`/`exp` for issued-at/expiry), and the signature is a MAC or digital signature over the first two segments. The critical insight: **a JWT is signed, not encrypted** — anyone can read the payload; the signature only proves it was issued by someone holding the key. And a signature that is never verified is decoration. Servers that accept `alg=none`, or that verify an HMAC with the public RSA key, have turned their session mechanism into a suggestion box (Stage B covers the attacks; this lesson covers the structure that makes them possible).

Below HTTP sits **TLS**, and the layering is the point. HTTP does not know or care whether its bytes are encrypted; TLS wraps the entire HTTP conversation — request line, headers, body, everything — in an encrypted tunnel negotiated before the first HTTP byte flows. The handshake (TLS 1.3, RFC 8446) establishes the protocol version, the cipher, the server's identity via its certificate, and the session keys, in roughly one round trip. What TLS protects: everything above TCP. What it does not protect: the fact that you talked to the server at all (IP addresses and timing are visible), and anything the endpoints themselves mishandle. "HTTPS" is just HTTP inside that tunnel — which is why a plain-HTTP request to a TLS port fails with silence, as the walkthrough shows.

Finally, versions. **HTTP/1.1** (text messages, one request at a time per connection, keep-alive), **HTTP/2** (multiplexed binary frames over one TCP connection), **HTTP/3** (same idea over QUIC/UDP). RFC 9110 defines the **semantics** — methods, status codes, fields — shared by all three; the version changes the transport syntax, not the meaning. When a lesson says "send a GET," the semantics are identical whether the bytes are HTTP/1.1 text or HTTP/3 frames.

### Worked example: one login, end to end

Run the demo server from the walkthrough (`python3 server.py`, port 8321) and follow a single login the way the protocol sees it. The client sends:

```
POST /login HTTP/1.1
Host: 127.0.0.1:8321
Content-Type: application/json
Content-Length: 38

{"user":"alice","pass":"wonderland"}
```

The server checks the credentials and answers:

```
HTTP/1.1 200 OK
Content-Type: application/json
Set-Cookie: session=alice-sess-abc; HttpOnly; Path=/
Content-Length: ...

{"token":"<header>.<payload>.<signature>"}
```

Two session mechanisms are issued at once: an opaque cookie and a JWT. Decode the JWT (base64url-decode each segment — the walkthrough does this in Python): the header says `{"alg":"HS256","typ":"JWT"}`, the payload says `{"sub":"alice","iat":...,"exp":...}`. Recompute the HMAC-SHA256 over `header.payload` with the server's secret and compare — it matches, so the token is genuine. Now flip one character of the payload and recompute: the signature no longer matches, and any server that actually verifies will reject it. That is the whole of JWT security in one motion: **readable by all, trustworthy only if verified, worthless if not**. Reproduce every step of this against your own running server before moving on — the walkthrough below is that reproduction.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/a-http-depth.log`. Clean environment: stock Python 3.12, curl 8.5.0, OpenSSL, loopback only, 2026-10-09.

1. **Start the lab server.** Save the `server.py` from this lesson's companion (a ~60-line stdlib HTTP server with `/`, `/login`, `/echo`, `/old`, `/new`, `/private`, `/admin` routes) and run `python3 server.py`. Confirm `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8321/` returns `200`.
2. **Read a raw response.** `curl -s -i http://127.0.0.1:8321/` — identify the status line, each header, the blank line, the body. Note the `Server` and `Date` headers: the server volunteers information; real servers volunteer more (version strings are reconnaissance).
3. **Follow a redirect.** `curl -s -i http://127.0.0.1:8321/old` returns `301` with `Location: /new`. Predict, then verify with `curl -s http://127.0.0.1:8321/new`. *Teaching point:* the client decides whether to follow — `curl` without `-L` does not. Redirects are client behavior, not protocol magic.
4. **Map the status codes.** Request `/nope` (404), `/admin` (403), `/private` (401 + `WWW-Authenticate`). Say out loud which of 401/403/404 you got and why each is the correct code for that situation.
5. **Provoke a 405.** `curl -s -i -X PUT http://127.0.0.1:8321/` — read the `Allow` header. Then try `DELETE` and `PATCH`: same result. *Teaching point:* method handling is per-route server logic; "the API supports PUT" is a claim you test, not a fact you assume.
6. **Log in and capture both session mechanisms.** `curl -s -i -X POST http://127.0.0.1:8321/login -H 'Content-Type: application/json' -d '{"user":"alice","pass":"wonderland"}'` — find the `Set-Cookie` header and the JWT in the JSON body. Then repeat with a wrong password: `401`.
7. **Dissect the JWT.** Split the token on `.`, base64url-decode the first two segments, read the claims (`sub`, `iat`, `exp`). Recompute the HMAC-SHA256 signature with the lab secret and confirm it matches; tamper with one payload character and confirm the signature check now fails. (The lab secret is printed in the transcript for reproducibility; on a real system the secret is the entire security of the scheme.)
8. **Echo and Content-Type.** `curl -s -X POST http://127.0.0.1:8321/echo -H 'Content-Type: text/plain' -d 'hello body'` — the body round-trips. Now send JSON with `Content-Type: text/plain` and consider: the server echoes bytes, but a real app would *parse* by the header — header/body mismatch is where parser differentials live.
9. **Add TLS.** Generate a throwaway self-signed certificate (`openssl req -x509 -newkey rsa:2048 -nodes -subj "/CN=127.0.0.1"`), wrap the server with Python's `ssl` module on port 8443. Observe the negotiated parameters with `openssl s_client -connect 127.0.0.1:8443` (TLS 1.3, `TLS_AES_256_GCM_SHA384` in our run). Fetch with `curl -sk https://127.0.0.1:8443/` — `-k` skips certificate verification, which is why the self-signed cert is accepted; on the real internet `-k` is how you volunteer for interception.
10. **Prove the layering.** `curl --max-time 5 http://127.0.0.1:8443/` — plain HTTP against the TLS port fails (000, handshake failed). The TLS handshake happens *before* any HTTP byte; there is no graceful "please speak TLS" fallback.

No step above is marked "not run by us" — every command ran against the local lab server and the transcript records the real output.

## 5. On your own

**Task:** Extend the lab server with a `/profile` endpoint that returns a JSON greeting for the logged-in user. It must read the JWT from the `Authorization: Bearer <token>` header, verify the signature and the `exp` claim, and reject bad tokens. Then, with curl only: (a) show a valid login reaching `/profile` successfully, (b) show a tampered token being rejected, (c) show an expired token being rejected (hint: mint one with `exp` in the past), (d) show the missing-header case.

**Success test:** Four request/response pairs, each with the correct status code (200 / 401 / 401 / 401) and a response body that does not leak *why* the token failed beyond what 401 already says. If your error messages distinguish "bad signature" from "expired" from "missing," you have built a username-enumeration-style oracle for tokens — fix it.

## 6. Where it goes wrong

- **Trusting the client.** Every header, cookie, method, and body byte is attacker-controlled. The server that treats `Cookie: role=admin` as authoritative has no authorization — it has a suggestion box. (Stage B makes a career of this.)
- **Cookies without attributes.** A session cookie missing `HttpOnly` is stealable by any XSS; missing `Secure` travels over HTTP; missing `SameSite` rides along on cross-site requests. The attributes are not hygiene — they are the session's armor.
- **JWTs accepted without verification.** `alg=none` accepted, signature unchecked, `exp` ignored, or the key confused (verifying an HMAC with a public RSA key). A bearer token is not a JWT until you have identified the format *and* validated it per RFC 7519 §7.2.
- **Information in status codes and errors.** 403-vs-404 choices, verbose 500 stack traces, `Server` banners with version numbers — each is a free answer to a reconnaissance question.
- **Method confusion.** State-changing GETs (CSRF bait), or routes that enforce authorization on POST but forget the same path answers to PUT/DELETE.
- **HTTP where HTTPS belongs.** Credentials, cookies, or tokens over plain HTTP are readable by anyone on the path. HSTS and redirect-to-HTTPS exist because one stray `http://` link is enough.

## 7. Read the source

Primary documents first — read with a purpose, skip without guilt:

- **RFC 9110, HTTP Semantics** (rfc-editor.org/rfc/rfc9110) — *read* §9 (methods) and §15 (status codes); *skim* the field registry sections; *skip* the ABNF grammar on first pass. This is the shared meaning of all HTTP versions.
- **RFC 6265, HTTP State Management Mechanism** (rfc-editor.org/rfc/rfc6265) — *read* §4 (Set-Cookie semantics, the attributes); *skim* §5 (user-agent processing); *skip* the date-parsing algorithm unless you implement cookies.
- **RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3** (rfc-editor.org/rfc/rfc8446) — *read* the handshake overview (§2); *skip* the cryptographic details — know what the handshake achieves, not the math.
- **RFC 7519, JSON Web Token** (rfc-editor.org/rfc/rfc7519) — *read* §3–4 (structure and claims) and §7.2 (validation); *skim* §11 (security considerations); *skip* the JWE appendices until you need encryption.

Then at most three free resources:

1. **MDN Web Docs — HTTP** (developer.mozilla.org) — the best free guided tour; read the "Messages," "Methods," and "Status codes" articles after the RFCs to consolidate.
2. **PortSwigger Web Security Academy** (portswigger.net/web-security) — free; the request-smuggling and auth labs in Stage B will assume everything in this lesson.
3. **curl documentation** (`curl --help`, curl.se/docs) — free; the tool you will use for the next hundred lessons deserves an hour of manual reading.

## 8. Check yourself

1. Explain why HTTP is called stateless, and name the two mechanisms from this lesson that applications layer on top to fake state. Which one requires server-side storage?
2. A server returns `403` for `/admin` when you request it unauthenticated, and `404` for `/admin_backup` under the same conditions. Predict what an attacker learns from each response, and explain which behavior you would choose for a sensitive path and why.
3. You intercept a JWT and can read `{"sub":"admin"}` in the payload. Explain, precisely, why you still cannot forge an admin token — and name the single server-side mistake that would let you.
4. `curl -k https://example.com` succeeds where `curl https://example.com` fails with a certificate error. Explain what `-k` disabled, what attack it re-enables, and why the walkthrough used it anyway.
5. A form's "delete account" button issues `GET /account/delete`. Explain the vulnerability class this enables (you will meet it by name in Stage B) and the one-line method-level fix.

## 9. Prove it

**Artifact:** a lab notebook (Markdown) containing: the full login exchange from the worked example (request + response with headers), the decoded JWT header and payload with the signature verification shown, the TLS negotiation line from step 9, and your answers to the four "On your own" probes with their status codes.

**Honest claim:** "I can read any HTTP request/response and explain every line, mint and verify a JWT by hand, and describe what TLS does and does not protect."
**Can't claim yet:** "I can find or exploit HTTP-level vulnerabilities" — that is Stage B, and this lesson deliberately built no vulnerable app.

## 10. Leads to

- **Stage B web vulnerability lessons** (B-VULN-01 through B-VULN-16) — every one of them is "send an unexpected HTTP message, read the response." IDOR (`b-idor`) is the immediate next step.
- **Stage B defensive basics** (B-DEF) — reading web logs and writing detections assumes you can parse what you just learned to produce.
- **Stage D DFIR track** — reconstructing attacks from access logs is this lesson applied to someone else's traffic.
- Map refs: this lesson is pre-map foundations; the authorization half of it feeds **CISSP 5.4** (authorization mechanisms) via Stage B, and the TLS half feeds **CISSP 4.3** (secure communication channels) via Stage E.
