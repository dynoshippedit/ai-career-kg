---
lesson_id: b-jwt-oauth
slug: jwt-oauth
stage: B
level: 3
prerequisites: [a-http-depth, a-crypto]
roles: []
map_refs: []
test_date: 2026-10-10
description: "JWT and OAuth flaws: trusting the token more than the verifier deserves — algorithm confusion, none-alg, and scope flaws reproduced locally, then fixed. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-10 · transcript in runs/b-jwt-oauth.log"
---
# JWT and OAuth flaws: trusting the token more than the verifier deserves


**Map refs:** CWE-287 (Improper Authentication) · CWE-347 (Improper Verification of Cryptographic Signature) · RFC 7519 (JWT) · RFC 6749 (OAuth 2.0)

---

## 1. Where this shows up

JSON Web Tokens carry identity between services: `header.payload.signature`, base64url-encoded, the signature proving the payload wasn't tampered with. OAuth 2.0 is the delegation protocol that hands those tokens out ("log in with Google," API authorization grants). Both fail in characteristic, testable ways — and the failures are almost never in the cryptography. They are in the *verifier*: the code that decides whether to trust a token, and the redirect validation that decides where OAuth codes go. This lesson takes you to Level 3: you will forge tokens three ways against a local verifier, bypass an OAuth redirect check, and verify the fixes. (`a-http-depth` taught the format; this lesson teaches the flaws.)

## 2. Before you start

- You can read HTTP requests and responses cold (`a-http-depth`), including Authorization headers.
- You know what a digital signature proves — and what defeats it (`a-crypto`'s misuse pairs: unverified signatures, wrong keys).
- You can hand-decode base64url and HMAC-sign a string in Python (the walkthrough does it step by step; no JWT library needed — building tokens by hand is the lesson).
- Your target is written down and authorizes your testing: this lesson's local verifier, a PortSwigger Academy JWT/OAuth lab, or a bounty program whose scope explicitly includes the asset. Token forgery is *authentication bypass* — the highest-sensitivity class. It belongs in labs and authorized scope, never in curiosity-driven testing. Re-read B-AUTH if this sentence surprised you.
- Tooling: Python 3, curl, OpenSSL (for the RSA keypair the key-confusion demo needs).

## 3. How it works

A JWT is three parts: `header.payload.signature`. The header names the algorithm (`{"alg":"HS256"}`); the payload carries claims (`sub`, `role`, `exp`, `aud`, `iss`); the signature is computed over `header.payload` with the server's key. Verification *should* mean: parse the header, look up the expected algorithm (server-side, never from the token), verify the signature with the right key, then check every claim the security decision depends on (`exp`, `aud`, `iss`).

Every flaw below is the verifier skipping a step:

**`alg=none`: the signature that isn't.** The attacker sets the header to `{"alg":"none"}` and drops the signature. A verifier that *trusts the token's own `alg` claim* skips verification entirely — and accepts a fully attacker-written payload. **Why it arises:** the verification code switches on the token-supplied algorithm instead of an allow-list the server controls. (Some libraries historically supported `none` for "unsecured" use cases; the bug is accepting it where security was intended.)

**Key confusion (RS256→HS256): the public key as a password.** The server verifies RS256 (RSA) tokens with its RSA *public* key — which is public by design. The attacker crafts a token with `alg: HS256`, signs it with HMAC using *the RSA public key bytes as the HMAC secret* (downloadable from the server's JWKS endpoint), and the confused verifier — using one key variable for both algorithms — checks the HMAC against the public key and accepts. **Why it arises:** one code path, one key variable, two algorithms with different key semantics. The fix is architectural: never let the token choose the algorithm; bind each key to exactly one algorithm.

**`exp`/`aud`/`iss` ignored: the claims nobody reads.** A verifier that checks the signature but never checks expiry accepts a stolen token forever; one that skips `aud` accepts tokens minted for a *different* service; one that skips `iss` accepts tokens from a different issuer. **Why it arises:** the JWT library verifies the signature and returns the payload; the *application* never validates the claims. Signature validity and token *acceptability* are two different checks.

**OAuth `redirect_uri` games: where the code goes.** In the authorization-code flow, the client tells the authorization server where to send the code (`redirect_uri`). If the server validates it with a *prefix match* (`startswith("https://trusted-app.example")`), the attacker registers `https://trusted-app.example.evil.example/` — a different domain that passes the prefix check — and the authorization code (which becomes an access token) goes to the attacker. Related games: unregistered `redirect_uri` parameters, `state` not validated (CSRF on the login flow), and `scope` escalation where the token request asks for more than the user granted. **Why it arises:** string matching instead of exact allow-list comparison, and optional parameters treated as decorative.

**How defenders see it.** `alg=none` in Authorization headers is a near-certain attack signal — legitimate clients never send it. Algorithm *changes* for one principal (RS256 yesterday, HS256 today) is the key-confusion tripwire. Expired-token reuse shows up as `exp` far in the past on otherwise valid signatures. OAuth abuse shows up in `redirect_uri` values: unexpected domains, subdomains of trusted names, and authorization codes redeemed from unexpected IPs. Detection rule shapes: alert on `alg:none` tokens; alert on algorithm flips per issuer; alert on `redirect_uri` values not in the exact allow-list.

### Worked example: the Harborlight verifier

A login/admin app (stdlib Python, local only — the walkthrough runs it) with a deliberately buggy verifier:

- Baseline: `/login?user=alice` → a real HS256 token; `/admin` with it → 401 (valid token, but `role: user` — the verifier works for the honest case).
- **`alg=none`:** hand-build `{"alg":"none"}` + `{"role":"admin"}` + empty signature → `/admin` → **200, "admin panel."** The verifier trusted the token's own algorithm claim and skipped verification.
- **Expired token:** a correctly-signed token with `exp` two hours in the past → **200.** The signature checked out; nobody read the expiry.
- **Key confusion:** fetch the server's *public* RSA key from `/pubkey`, HMAC-sign an admin payload with the public-key bytes as the secret, set `alg: HS256` → **200.** The verifier used its RSA public key as an HMAC secret — the classic confusion, reproduced for real.
- **OAuth `redirect_uri`:** `/oauth-check?redirect_uri=https://trusted-app.example.evil.example/steal` → **"redirect allowed: True."** The prefix match approved an attacker domain.

The fix, in the same app: strict algorithm allow-list (`HS256` only, server-chosen), signature verified with the *correct* key, `exp`/`aud`/`iss` all checked, `redirect_uri` compared by exact match against the allow-list. Re-test: `alg=none` → 401, key confusion → 401, expired → 401, bypass domain → False, legitimate callback → True, legitimate login → 403 (valid token, not admin — correct). Then the general rule: **the server chooses the algorithm, the key, and the acceptable claims — the token chooses none of them.**

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-jwt-oauth.log`. Clean environment: stock Python 3.12, OpenSSL 3.0.13 (RSA keygen), loopback only, 2026-10-10. Tokens are built by hand (base64url + HMAC) — no JWT library, because the construction *is* the lesson.

1. **Start the app.** Save the `app.py` from this lesson's companion and run it on port 8342. Confirm the baseline: log in as alice, call `/admin` with the token → 401 (role=user). The verifier works for honest tokens.
2. **Decode a token by hand.** Split the login token on `.`, base64url-decode the header and payload, read the claims. Say out loud which claims the security decision *should* depend on.
3. **Forge `alg=none`.** Build the header `{"alg":"none","typ":"JWT"}`, the payload with `"role":"admin"`, empty signature → `/admin` → 200. Write down the request/response pair — this is the finding.
4. **Forge the expired token.** Sign (with the confused key, as this verifier expects) a payload with `exp` two hours in the past → 200. The signature verified; the expiry was never read. (The walkthrough log records a correction: the first attempt signed with the wrong key and 401'd — the signature must match what *this* verifier checks, which is itself part of the finding.)
5. **Run the key confusion for real.** `GET /pubkey` → the RSA public key (it's public — that's the point). HMAC-sign your admin payload with those exact bytes, set `alg: HS256` → `/admin` → 200. Write down, in one sentence, whose key you used and why the verifier accepted it.
6. **Bypass the redirect check.** `/oauth-check?redirect_uri=https://trusted-app.example.evil.example/steal` → True. Explain why the prefix matched and what the attacker's domain actually is.
7. **Apply the fix.** Restart with `FIXED=1` on port 8343: allow-listed alg, correct key, exp/aud/iss enforced, exact-match redirect allow-list.
8. **Verify the fix — six cases.** `alg=none` → 401; key confusion → 401; expired → 401; bypass domain → False; legitimate callback → True; legitimate login → 403 (valid, not admin). A fix that breaks legitimate logins is not a fix.
9. **Read the defender view.** The companion logs Authorization headers. Find your `alg=none` token in the log. Write the detection rules: alert on `alg:none`; alert on algorithm flips per issuer; alert on `redirect_uri` values outside the exact allow-list.

No step above is marked "not run by us" — all three forgeries, the redirect bypass, and all six fix verifications ran locally. (`kid` path traversal and `jku`/`x5u` header injection are named in section 6 as the next rungs; they are concept-level here, lab-bounded in PortSwigger's JWT labs.)

## 5. On your own

**Task:** Pick one authorized target you have not touched in this lesson — a PortSwigger Academy JWT lab (start with "JWT authentication bypass via unverified signature," then the `none` and key-confusion labs in order). For each lab: (1) decode the provided token by hand first — never skip the reading step; (2) apply exactly one forgery class per attempt; (3) record which claim the verifier failed to enforce.

**Success test:** A one-page report per lab: the token decoded (header + claims quoted), the forgery class applied, the exact request/response proving it, the verifier-side root cause (which check was missing), the fix stated as the general rule it violates, and the defender detection (which log, which pattern). If a lab's verifier resists your forgery, document the check that stopped you — a characterized defense is a result.

## 6. Where it goes wrong

- **"The library handles it."** Libraries verify signatures; *applications* validate claims. The most common JWT bug is the gap between those two sentences. Read your library's docs for what it does *not* check.
- **Trusting the token's `alg`.** The algorithm is a server-side decision. Any code path that reads `alg` from the token to choose the verification method is the vulnerability.
- **One key variable for two algorithms.** RS256 and HS256 keys must live in separate variables with separate code paths — or better, separate verification functions that each accept exactly one algorithm.
- **Checking expiry "later."** `exp` is checked at verification time or not at all. "We'll check it in the handler" means the handler that forgets.
- **`kid` and `jku`/`x5u` headers.** The key-ID header that becomes a path traversal (`kid: ../../dev/null` → null key → empty HMAC secret) and the URL headers that let the attacker supply the verification key — the next two rungs. Know they exist; practice them in the labs.
- **OAuth `state` left unvalidated.** Without `state`, the login flow is CSRF-able: the attacker completes *their* OAuth flow in *your* browser. Always bind and validate `state`.
- **Scope as a suggestion.** If the token endpoint grants whatever scope is requested, the authorization step is theater. Validate granted scopes server-side against what the user actually approved.

## 7. Read the source

Primary documents first:

- **RFC 7519** (rfc-editor.org/rfc/rfc7519.txt — verified 2026-10-10): JSON Web Token — the claims registry (`exp`, `aud`, `iss`, `sub`) and the JOSE header. *Read* §4 (claims); *note* what the RFC says the *application* must validate.
- **RFC 6749** (rfc-editor.org/rfc/rfc6749.txt — verified 2026-10-09): OAuth 2.0 — the authorization-code flow and `redirect_uri` handling. *Read* §4.1 (code flow); *note* §4.1.2's exact-match language.
- **PortSwigger Web Security Academy — JWT attacks** (portswigger.net/web-security/jwt — verified 2026-10-10): the canonical flaw catalog — unverified signature, `none`, key confusion, `kid`/`jku`. *Read* fully, then do the labs in order.

Then at most three free resources:

1. **PortSwigger JWT + OAuth labs** (portswigger.net/web-security — free): the ordered lab set this lesson's method mirrors, hosted and authorized.
2. **RFC 8725 (JWT BCP)** (rfc-editor.org — free): the best-practices RFC — the fix list in standards language. *Skim* after the labs.
3. **`a-crypto`** (this guidebook): signatures — what they prove, and the misuse pairs this lesson weaponizes.

## 8. Check yourself

1. Explain why `alg=none` works only against verifiers that read the algorithm *from the token*, and what the server-side allow-list looks like.
2. The server publishes its RSA public key at `/pubkey`. Explain step by step how you turn that into an accepted admin token, and which line of the verifier is the bug.
3. A token has a valid signature but `exp` is yesterday. Explain the two checks (signature validity vs token acceptability) and which one failed to happen.
4. `redirect_uri=https://trusted-app.example.evil.example/` passes a prefix check for `https://trusted-app.example`. Explain why, state the correct check, and explain what the attacker does with the authorization code.
5. Explain why hand-building tokens (base64url + HMAC, no library) is the right way to *learn* this class, even though production code must use a vetted library.

## 9. Prove it

**Artifact:** the one-page reports from "On your own" (one per lab): token decoded, forgery class, exact proof, root cause, the general rule violated, defender detection — plus your local-demo notes (the three forgeries, the redirect bypass, the six fixed-build cases).

**This lesson takes you to Level 3 (Apply).** You can honestly claim: you can decode JWTs by hand, forge `alg=none`, expired-claim, and key-confusion tokens against vulnerable verifiers on authorized targets, bypass prefix-match redirect validation, and verify the complete fix. You cannot yet claim: OAuth/OIDC implementation review — `kid`/`jku` exploitation, PKCE analysis, and multi-IdP trust design are the deeper layer this lesson points at.

## 10. Leads to

- `a-crypto` (re-read the signature misuse pairs) — now that you've seen what "unverified signature" buys an attacker.
- `b-session-auth` — sessions done right: what should have been in that cookie instead of a confused JWT.
- `b-api-abuse` — where forged tokens get *used*: BOLA with an admin token is the combination that ends engagements.
- Map refs: **CWE-287** · **CWE-347** · **RFC 7519** · **RFC 6749** · **PortSwigger JWT/OAuth**.
