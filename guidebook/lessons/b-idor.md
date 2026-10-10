# IDOR: Insecure Direct Object References

**ID:** `b-idor` · **Stage:** B (Practitioner) · **Level:** 3 (mechanism + live reproduction + fix verification) · **Prerequisites:** `a-http-depth` (HTTP in depth), B-AUTH (authorization discipline: you test only what you are allowed to touch, with accounts you own), an interception proxy or curl.

---

## 1. Where this shows up

IDOR is the single highest-yield vulnerability class for a beginning bounty hunter: it is common, it is usually simple to prove, and its impact writes itself ("one user reads another user's data"). It sits inside **OWASP Top 10:2025 A01 — Broken Access Control** and has an API twin, **BOLA** (Broken Object Level Authorization, API1:2023 in the OWASP API Security Top 10). The testing methodology cites it as **WSTG-ATHZ-04**. You will meet it in bug bounty programs, in penetration-test reports, in API security reviews, and — from the other side — in every access-log triage you ever do as a defender. The mechanism in this lesson is also the template for the whole Broken Access Control family: the server trusts a client-supplied identifier and never asks "is this yours?"

## 2. Before you start

- You can read HTTP requests and responses cold (`a-http-depth`).
- You have **two test accounts you own** on whatever target you practice against — the entire lesson is comparing what account A can see versus what account B can see. Never use someone else's account or data.
- Your scope is written down and the target authorizes your testing: your own local lab, a PortSwigger Academy lab, or a bounty program whose scope explicitly includes the asset. IDOR testing without authorization is not research; re-read B-AUTH if this sentence surprised you.
- Tooling: curl is enough for this lesson; an interception proxy (Burp Community) makes it faster later.

## 3. How it works

An **object** is anything the application stores per-user or per-tenant: invoices, orders, medical records, chat transcripts, files, API resources. A **direct object reference** is when the client names the object it wants with an identifier — `invoice?id=1043`, `/api/vehicle/8812/location`, a filename in a URL — and the server fetches it directly. The reference becomes **insecure** when the server uses that client-supplied identifier *without checking that the requesting identity is allowed to see that object*.

Walk the mechanism slowly, because the subtlety is where the bugs live. Authentication answers "who are you" — and in every IDOR the victim *is* authenticated. The server knows the request comes from alice. It takes `id=1043` from the query string, looks up invoice 1043, finds bob's invoice, and returns it with `200 OK`. No error, no anomaly, no failed check — because there was no check. The flaw is not the identifier scheme. Sequential IDs (`1042`, `1043`) make the flaw *easy to find*, but replacing them with unguessable UUIDs does not fix it — it only hides it. An attacker who obtains one UUID (from a shared link, a log, a referer header) walks straight through. **Obscurity of the identifier is not authorization.** The fix is always the same shape: on every object access, the server must verify ownership (or permission) *against the authenticated identity*, and deny by default.

Two directions of escalation ride on this one missing check. **Horizontal**: alice reads bob's data — same privilege level, different owner. This is the classic IDOR and the bounty bread-and-butter. **Vertical**: a low-privilege user reaches an object or function reserved for a higher role — e.g., changing `userId` to the administrator's ID on a profile endpoint that also returns admin-only fields. PortSwigger's framing is worth internalizing: IDOR is one example of the general class "the application uses user-supplied input to access objects directly," and the same missing-check shape produces both escalations.

Where do the identifiers hide? Everywhere the client gets a say: URL paths (`/users/9912`), query parameters (`?id=`), POST bodies (`{"orderId":…}`), headers, and API versions of all of these. The testing habit is mechanical: for every identifier your account legitimately touches, ask "what happens if I substitute an identifier belonging to my *other* account?" You need two accounts precisely so the answer is checkable without touching anyone else's data.

How defenders see it, so you can write it up properly: one session touching many sequential or foreign object IDs in the access logs — a spread of IDs no legitimate user browses. WAF signatures are nearly useless here (the requests are well-formed); detection is behavioral, per-session ID spread and rate. When you report, the evidence is the request/response pair: your session, the foreign ID, the other user's data returned with 200.

### Worked example: the invoice demo

A minimal shop app (stdlib Python, local only — the walkthrough runs it). Two users, alice and bob, each with two invoices: alice owns 1041–1042, bob owns 1043–1044. Login issues a bearer token; `GET /invoices` lists your own; `GET /invoice?id=N` fetches one by ID.

As alice, list your invoices — 1041, 1042, correct. Now change the parameter: `GET /invoice?id=1043`. The server responds `200 OK` with `{"owner":"bob","item":"Monitor","total":"249.99"}`. That response *is* the vulnerability: an authenticated user asked for another tenant's object by changing one digit, and the server complied. Confirm the ownership independently — log in as bob and see 1043 in his list — so the report states a fact, not an inference.

The fix, in the same app: before serving, compare the invoice's owner against the authenticated user and return `403` on mismatch. Re-test three cases: alice→1043 now gets `403`; alice→1042 still gets `200` (legitimate access unbroken — a fix that breaks the app is not a fix); alice→9999 gets `404`. Note the 403-vs-404 decision from `a-http-depth`: here 403 is chosen deliberately to distinguish "exists but not yours" from "does not exist" — either is defensible, but it must be a *decision*, recorded, because it leaks existence either way.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-idor.log`. Clean environment: stock Python 3.12, curl 8.5.0, loopback only, 2026-10-09. The demo app stands in for the PortSwigger/DVWA/crAPI targets the reader uses (no Docker on this machine — see gaps).

1. **Start the vulnerable app.** Save the `app.py` from this lesson's companion (two users, four invoices, bearer-token auth, `GET /invoice?id=` with no ownership check) and run it on port 8322. Confirm it answers.
2. **Establish the baseline as alice.** Log in (`POST /login`, alice's credentials), capture the token, `GET /invoices` — record that alice owns 1041 and 1042. This is your control: what legitimate access looks like.
3. **Substitute the identifier.** `GET /invoice?id=1043` with alice's token. Observe `200 OK` returning bob's invoice. Write down, verbatim, the request and the response — this pair is the finding.
4. **Confirm ownership independently.** Log in as bob, `GET /invoices` — 1043 and 1044 are his. The finding is now a fact: cross-tenant read, no guessing involved.
5. **Check the unauthenticated case.** Same request with no token: `401`. Note that authentication works fine — this was never an authentication bug. Say it out loud: the app knew exactly who was asking and answered anyway.
6. **Apply the fix.** Patch the `/invoice` handler: deny by default unless `invoice.owner == authenticated_user`. Restart the app.
7. **Verify the fix — three cases.** alice→1043: `403` (blocked). alice→1042: `200` (her own data still works). alice→9999: `404` (missing objects still 404, not 403 — the error handling did not regress).
8. **Write the mini-report.** One page: title, severity reasoning, reproduction steps (exact requests), impact (what an attacker gains: any authenticated user reads any invoice), remediation (server-side ownership check, deny by default), evidence (the request/response pair from step 3).

No step above is marked "not run by us" — the vulnerable behavior, the fix, and all three verification cases ran locally and the transcript records the real output.

## 5. On your own

**Task:** Pick one authorized target you have not touched in this lesson — a PortSwigger Academy access-control lab, DVWA at low difficulty, or crAPI's BOLA challenges. Using two accounts you own, find and document one IDOR-class issue (it may be the lab's intended vulnerability). Then, for the same endpoint, determine whether the application also fails the *write* direction: can account A modify or delete account B's object, not just read it?

**Success test:** A one-page report in the anatomy from walkthrough step 8, with request/response evidence for the read case and a clear yes/no (with evidence) for the write case. If your report cannot distinguish "the object exists but is protected" from "the object does not exist," say so — that ambiguity is itself a finding about error handling.

## 6. Where it goes wrong

- **Checking on the list page but not the direct fetch.** The app filters `/invoices` to your own but serves `/invoice?id=` to anyone. Every object access needs the check, not just the convenient ones.
- **Client-side "protection."** Hiding the ID in JavaScript, disabling the button, or removing the link — the endpoint still answers direct requests. If the server doesn't enforce it, it isn't enforced.
- **Unguessable IDs as the fix.** UUIDs, hashes, "random" filenames: they slow discovery, they are not authorization. One leaked link reopens everything.
- **Checking identity but not ownership.** "Is the user logged in?" is not "is this the user's object?" — the vulnerable app in this lesson passed the first check perfectly.
- **IDOR in writes.** Testers check reads and stop. The same missing check on update/delete endpoints turns data exposure into data destruction.
- **Mass assignment / over-posting.** The API silently accepts extra fields (`{"role":"admin"}`) — the object-reference flaw's cousin, same root cause: the server trusts the client's description of what should happen.
- **Fixing with 404-for-everything.** Returning 404 for "not yours" avoids confirming existence but complicates legitimate debugging and can still be distinguished by timing — pick deliberately, document the choice.

## 7. Read the source

Primary documents first:

- **PortSwigger Web Security Academy — IDOR** (portswigger.net/web-security/access-control/idor) — *read* fully; it is short and it is the canonical explanation (direct DB references, static-file references, horizontal vs vertical escalation).
- **OWASP Top 10:2025 — A01 Broken Access Control** (owasp.org/Top10/2025) — *read* the A01 entry; *note* that the 2025 edition folds SSRF into A01 — the category is "the server does something for you that it shouldn't," and IDOR is its most common shape.
- **OWASP WSTG — WSTG-ATHZ-04** (owasp.org/www-project-web-security-testing-guide) — *read* the test procedure; this is the checklist form of the walkthrough above. *Skip* the other ATHZ tests until the next lesson.

Then at most three free resources:

1. **PortSwigger Academy — Access Control labs** (portswigger.net/web-security) — free, hosted, authorized; the IDOR labs are the hands-on companion to this lesson.
2. **OWASP Cheat Sheet Series — Access Control** (cheatsheetseries.owasp.org) — free; the fix side: deny-by-default, centralized authorization.
3. **OWASP crAPI** (github.com/OWASP/crAPI) — free; run locally via Docker and work the vehicle/order BOLA challenges (`GET /identity/api/v2/vehicle/{id}/location` with two users) — IDOR's API twin.

## 8. Check yourself

1. Explain why replacing sequential invoice IDs with unguessable UUIDs does not fix an IDOR, and name the one change that does.
2. An endpoint returns `200` with another user's data when you substitute their ID, but returns `401` when you drop your token. Explain why this is an authorization failure and not an authentication failure.
3. Predict the server behavior you would expect, as a defender, in the access logs of an application under active IDOR probing — and explain why a WAF signature is a poor detector for it.
4. You find that `GET /invoice?id=` is protected but `PUT /invoice?id=` with a JSON body is not. Explain the impact difference between the read and write variants, and which one you would report as higher severity.
5. A developer proposes fixing the lesson's demo by removing the `id` parameter and only serving "the current invoice." Explain why this is not a fix for any application with more than one object per user.

## 9. Prove it

**Artifact:** the one-page mini-report from walkthrough step 8 (or the "On your own" report against a real lab target): title, severity with reasoning, exact reproduction requests, impact stated concretely, remediation, and the request/response evidence pair.

**Honest claim:** "I can demonstrate, with evidence, that one authenticated user can access another's object through a client-supplied identifier, and I can verify the server-side fix."
**Can't claim yet:** "I can find authorization flaws in general" — function-level bypasses, privilege escalation, and API authorization are the next lessons.

## 10. Leads to

- **B-VULN-02 — Broken access control (general)** — IDOR as one member of the family: missing function-level checks, role tampering, forced browsing.
- **B-VULN-05 — API abuse / BOLA** — the same flaw through API-shaped endpoints (API1:2023).
- **B-DEF — Defensive basics** — sit on the other side: given your own attack traffic, write the detection (per-session ID spread).
- **B-BOUNTY — Bug bounty mechanics** — this lesson's report format is the dry run for a real submission.
- Map refs: **OWASP Top 10:2025 A01**, **WSTG-ATHZ-04**, **CISSP 5.4** (authorization mechanisms and models, via Stage E).
