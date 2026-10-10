---
lesson_id: b-api-abuse
slug: api-abuse
stage: B
level: 3
prerequisites: [a-http-depth, b-idor]
roles: [pentester, appsec]
map_refs: []
test_date: 2026-10-10
description: "API abuse: broken object-level authorization, mass assignment and excessive data exposure behind the JSON — reproduced locally and fixed. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-10 · transcript in runs/b-api-abuse.log"
---
# API abuse: the flaws that live behind the JSON


**Map refs:** OWASP API Security Top 10:2023 (API1, API3, API4) · CWE-862, CWE-200, CWE-915

---

## 1. Where this shows up

Modern applications are APIs wearing a web page as a costume: the front end is JavaScript calling JSON endpoints, and the mobile app talks to the same endpoints directly. Testers who only click the UI miss the real attack surface — the endpoints themselves, including the ones the UI never calls. OWASP's **API Security Top 10:2023** exists because APIs fail in their own characteristic ways, and its #1 item — **API1:2023 Broken Object Level Authorization** — is the single most common API flaw in the wild. This lesson takes you to Level 3: you will find and prove four API abuse classes against a local demo, fix them, and verify the fixes.

## 2. Before you start

- You can read HTTP requests and responses cold (`a-http-depth`), including JSON bodies and status codes.
- You understand the IDOR lesson's core pattern — the server trusting client-supplied identifiers — because API1 is that pattern at API scale.
- Your target is written down and authorizes your testing: this lesson's local demo app, a PortSwigger API-testing lab, or a bounty program whose scope explicitly includes the API. API endpoints not referenced by the UI are still in scope only if the program says so — an undocumented endpoint is not an invitation. Re-read `b-authorization-scope` if this sentence surprised you.
- Tooling: curl and a JSON eye (python3 -m json.tool). No proxy required for this lesson's class, though you will want one later.

## 3. How it works

An API endpoint does three things the developer must get right: **decide who you are** (authentication), **decide whether you may touch this object** (authorization), and **decide what you may send and receive** (input/output shaping). The four flaws below are the four decisions skipped.

**Broken Object Level Authorization (BOLA, API1:2023).** `GET /api/users/2` while authenticated as user 1 returns user 2's record. The endpoint checks *that* you are logged in but never checks *whether this object is yours*. It is IDOR's bigger sibling: IDOR is usually taught on web pages, BOLA is the same flaw in the JSON layer, and it is #1 on the API Top 10 because APIs expose object references (IDs in paths) everywhere. **Why it arises:** the developer wrote one handler for "get user by id" and tested it with their own id. The deeper reason the check must be data-driven: the URL says *which* object, but only the database can say *whose* object it is — and the URL is attacker-controlled input. So the server must re-derive ownership from its own data on every request. The identifier in the path is a lookup key, never an authorization decision.

**Excessive data exposure (CWE-200).** `GET /api/users/me` returns the full database row — password hash, SSN, internal notes — because the handler serializes the ORM object directly instead of a shaped response. (ORM — object-relational mapping — the library that turns database rows into code objects; serializing it dumps every column.) The front end only displays the name, so nobody noticed the extra fields. **Why it arises:** frameworks make "return the object" a one-liner and "return the DTO" actual work. (A DTO — data transfer object — is an object shaped for exactly one response, carrying only the fields that response needs.) The attacker doesn't need to break in; the API hands over the data with a valid session.

**Mass assignment (CWE-915).** `POST /api/users {"name":"mallory","role":"admin"}` creates an admin, because the handler binds every JSON field to the model — including fields the client should never set. **Why it arises:** the same model class is used for the database and the request binding, and the developer never listed which fields are client-writable. Also called auto-binding.

**Missing rate limits (API4:2023 Unrestricted Resource Consumption).** No limit on requests per minute means credential stuffing, enumeration (`/api/users/1` … `/api/users/10000`), and algorithmic-complexity DoS all run at full speed. (Algorithmic-complexity DoS — requests crafted to trigger worst-case server work, like deeply nested filters that make the database crawl.) **Why it arises:** rate limiting is infrastructure the developer assumes "someone else" configured.

**How defenders see it.** API abuse is *visible* in logs, which is the good news: BOLA probing looks like one authenticated principal touching many object IDs (especially sequential IDs). (A principal — the identity a request acts as: the user or service account the server believes is asking.) Excessive-data exposure is found in code review (ORM object → response) and in response-size anomalies; mass assignment shows up as unexpected fields in request bodies; missing rate limits show up as the absence of 429s under load. Detection rule shapes: alert on one principal accessing N distinct object IDs in M minutes; alert on 200-responses whose bodies contain `password_hash`-shaped fields; schema-validate request bodies and log rejected fields.

Concretely, BOLA probing in an access log looks like this — one session, sequential IDs, all 200:

```
10.0.4.21 - alice [10/Oct/2026:01:12:03 +0000] "GET /api/users/1 HTTP/1.1" 200 412
10.0.4.21 - alice [10/Oct/2026:01:12:04 +0000] "GET /api/users/2 HTTP/1.1" 200 408
10.0.4.21 - alice [10/Oct/2026:01:12:05 +0000] "GET /api/users/3 HTTP/1.1" 200 415
```

No legitimate user pages through the user table one ID per second. The ID spread *is* the signal.

### Worked example: the Harborlight users API

A minimal JSON API (stdlib Python, local only — the walkthrough runs it). Four endpoints, four flaws, each proven with curl:

- `GET /api/users/2` as user 1 → **200 with user 2's full record** (BOLA — no per-object check).
- `GET /api/users/me` → **200 with password hash, SSN, internal notes** (excessive data exposure — full ORM row serialized).
- `POST /api/users {"name":"mallory","role":"admin"}` → **201 with `"role":"admin"`** (mass assignment — the field was bound straight to the model).
- Ten rapid `POST /api/users` → **ten 201s, zero 429s** (no rate limiting — enumeration and stuffing run unthrottled).

The fix, in the same app: per-object authorization check (`uid == current_user` or an ownership lookup) returning 403; a shaped DTO on `/me` (id + name only); an allow-list of writable fields on create (role forced server-side); a simple per-endpoint rate limit (5/minute → 429). Re-test all four: 403, DTO, role dropped, 429s. Then the general rule: **authorize every object, shape every response, allow-list every input, throttle every endpoint** — four sentences that prevent four vulnerability classes.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-api-abuse.log`. Clean environment: stock Python 3.12, curl 8.5.0, loopback only, 2026-10-10. The demo app stands in for the PortSwigger API labs the reader uses (no Docker on this machine — see gaps).

1. **Start the app.** Save the `app.py` from this lesson's companion and run it on port 8331. Confirm the baseline: `curl -s localhost:8331/api/users/me` returns user 1's record. You are "logged in" as user 1 for the whole exercise.
2. **Prove BOLA.** `curl -s localhost:8331/api/users/2` — observe user 2's full record returned with HTTP 200. You asked for another user's object and the server complied without checking ownership. Write down the request/response pair — this is the finding.
3. **Prove excessive data exposure.** Look at the `/me` response from step 1: `password_hash`, `ssn`, `internal_notes`. The front end displays only the name. List every field the UI doesn't need — each one is data the API should never have sent.
4. **Prove mass assignment.** `curl -s -X POST localhost:8331/api/users -d '{"name":"mallory","role":"admin"}'` — observe `"role":"admin"` in the 201 response. Then `GET /api/users/3` to confirm the role persisted. The client chose its own privilege level.
5. **Prove missing rate limits.** Ten rapid POSTs in a loop — observe ten `201` responses and zero `429`s. On a real target this is the green light for enumeration and credential stuffing; here it is the missing control, demonstrated.
6. **Apply the fix.** Restart with `FIXED=1` on port 8332: per-object check, DTO response, writable-field allow-list, 5/minute rate limit.
7. **Verify the fix — four cases.** `/api/users/2` → 403; `/me` → id+name only; the `role` field → dropped (forced `user`); the 6th rapid POST → 429. A fix that breaks legitimate use is not a fix — confirm `/me` still works for user 1.

No step above is marked "not run by us" — all four flaws and all four fixes ran locally. The demo's "authentication" is a hardcoded user (labeled in the companion); real session handling is `b-session-auth`'s subject.

## 5. On your own

**Task:** Pick one authorized target you have not touched in this lesson — a PortSwigger API-testing lab (the "exploiting a mass assignment vulnerability" lab is the closest match for one class; the API testing topic covers the rest). Enumerate the API surface first: map every endpoint, method, and parameter from normal UI traffic plus the API documentation if the lab provides it. Then test each of the four classes in order: BOLA (swap IDs), excessive data (diff the response against what the UI shows), mass assignment (add a privileged field), rate limits (burst and watch for 429).

**Success test:** A one-page report per class tested: the endpoint, the exact requests, the evidence (response excerpts), the fix stated as the general rule it violates (authorize/shape/allow-list/throttle), and the defender detection (which log, which pattern). If a class is *not* vulnerable, document the control you found — a characterized defense is a result.

## 6. Where it goes wrong

- **"The UI doesn't show it, so it's safe."** Undocumented and UI-unreferenced endpoints are the attacker's favorite targets. Enumerate the API, not the UI.
- **Testing BOLA with your own ID only.** The flaw is in the *other* IDs. Always test cross-object access with two principals.
- **Fixing mass assignment with a denylist.** Blocking `role` while leaving `is_admin`, `permissions[]`, or nested objects bindable is the same flaw wearing a hat. Allow-list writable fields.
- **Rate limiting by IP only.** Behind NATs and proxies, one IP is many users — and attackers rotate IPs. Limit by principal + endpoint, and treat the absence of 429s as the finding.
- **Calling the DTO "the fix" for BOLA.** Shaping the response doesn't stop the unauthorized *access* — it only hides fields. BOLA needs the authorization check; the DTO is a separate fix for a separate flaw.
- **Assuming GraphQL/REST differences matter here.** They don't for these four classes — BOLA, over-exposure, mass assignment, and missing throttles exist identically in both. (`b-graphql` covers what GraphQL adds on top.)

## 7. Read the source

Primary documents first:

- **OWASP API Security Top 10:2023** (owasp.org/API-Security — verified 2026-10-10): the canonical list — API1 BOLA, API3 BOPLA, API4 resource consumption. *Read* the risk descriptions for API1–API4; *skim* the rest.
- **PortSwigger Web Security Academy — API testing** (portswigger.net/web-security/api-testing — verified 2026-10-10): how the flaws are found in practice. *Read* fully, then do the labs.
- **CWE-862** (cwe.mitre.org/data/definitions/862.html — verified 2026-10-09): Missing Authorization — the weakness behind BOLA. *Skim*; cite the ID.

Then at most three free resources:

1. **PortSwigger API testing labs** (portswigger.net/web-security — free): mass assignment, BOLA, and excessive-data labs, hosted and authorized.
2. **OWASP API Security Top 10 details** (owasp.org/API-Security — free): prevention cheat-sheet mappings per risk.
3. **`b-graphql`** (this guidebook): what GraphQL adds on top of these four classes — introspection, nested-query DoS, field-level authorization.

## 8. Check yourself

1. Explain why BOLA is the API version of IDOR, and why APIs make it *more* common than classic web apps do.
2. A `GET /api/users/me` returns 40 fields; the UI displays 6. Explain the flaw, who it hurts even though "only the user sees their own data," and the fix.
3. You POST `{"name":"x","role":"admin"}` and get 201 with admin. The developer "fixes" it by rejecting requests containing the string `role`. Explain two ways this fix fails and state the correct fix.
4. An API returns 200 to 1,000 rapid login attempts with no 429. Name the missing control, the two attacks it enables, and where you would implement it.
5. Explain the difference between fixing BOLA and fixing excessive data exposure — why one fix does not cover the other.

## 9. Prove it

**Artifact:** the four one-page reports from "On your own" — each against a target you had not touched in this lesson: endpoint, evidence, the general rule violated, the fix, the defender detection.

**This lesson takes you to Level 3 (Apply).** You can honestly claim: you can enumerate an API surface, find and prove BOLA, excessive data exposure, mass assignment, and missing rate limits on an authorized target, and verify each fix. You cannot yet claim: production API security review — real APIs add versioning, gateway policies, and business-logic flows (`b-business-logic`) that this lesson's four classes don't cover.

## 10. Leads to

- `b-graphql` — the same four classes plus what GraphQL adds: introspection, nested-query DoS, field-level authorization.
- `b-business-logic` — API6:2023 (sensitive business flows) lives here: the flaw isn't the endpoint, it's the *flow*.
- `b-session-auth` — the authentication half that BOLA assumes is already done.
- Map refs: **OWASP API Security Top 10:2023 (API1, API3, API4)** · **CWE-862** · **CWE-200** · **CWE-915**.
