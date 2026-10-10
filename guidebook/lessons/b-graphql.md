---
lesson_id: b-graphql
slug: graphql
stage: B
level: 3
prerequisites: [a-http-depth, b-api-abuse]
roles: []
map_refs: []
test_date: 2026-10-10
description: "GraphQL abuse: the query language that trusts the querier — introspection, BOLA on queries, and resource exhaustion reproduced locally, then locked down. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-10 · transcript in runs/b-graphql.log"
---
# GraphQL abuse: the query language that trusts the querier


**Map refs:** CWE-862 (Missing Authorization) · CWE-770 (Allocation of Resources Without Limits) · GraphQL spec (introspection)

---

## 1. Where this shows up

GraphQL replaces REST's fixed endpoints with a single endpoint that answers *whatever shape the client asks for*: the client writes the query, the server resolves it. That flexibility is the feature — and the attack surface. Everything in `b-api-abuse` (BOLA, over-exposure, mass assignment, missing throttles) exists identically in GraphQL, and GraphQL adds three of its own: **introspection** (the API documents itself to attackers), **nested-query DoS** (the client controls the work factor), and **field-level authorization gaps** (one resolver without a check leaks one field to everyone). This lesson takes you to Level 3 on the GraphQL-specific three, against a real GraphQL server running locally.

## 2. Before you start

- You can read HTTP requests and responses cold (`a-http-depth`), including JSON bodies.
- You have done `b-api-abuse` — the four base classes are assumed; this lesson covers only what GraphQL *adds*.
- Your target is written down and authorizes your testing: this lesson's local GraphQL server (graphql-core, real engine), a PortSwigger API/GraphQL lab, or a bounty program whose scope explicitly includes the API. Introspection is *enabled by default* in most frameworks — probing it on an authorized target is normal testing. Re-read B-AUTH if this sentence surprised you.
- Tooling: curl or any HTTP client that posts JSON. No special GraphQL client needed.

## 3. How it works

A GraphQL server exposes one endpoint (usually `/graphql`). You POST `{"query": "{ user(id: 1) { name } }"}` and get back exactly the shape you asked for. Three consequences:

**Introspection: the schema asks to be read.** By default, a GraphQL server answers `__schema` queries — a complete dump of every type, field, argument, and mutation it supports, including the ones the UI never calls. Attackers use it the way you would use API documentation: to find the interesting fields. **Why it arises:** introspection is on by default in development and nobody turns it off in production. The fix is one configuration flag — which tells you how often it is forgotten.

**Nested-query DoS: the client sets the price.** `{ user { posts { comments { author { posts { comments { text } } } } } } }` — each level fans out (5 posts × 5 comments × 5 authors × ...). The client wrote a short string; the server does exponential work. REST endpoints have fixed cost; GraphQL queries have *client-chosen* cost. **Why it arises:** resolvers are written per-field with no global view of what a nested query costs. Defenses: query depth limits, query cost analysis (assign each field a cost, reject over budget), pagination caps, timeouts.

**Field-level authorization: one resolver, one missing check.** `ssn` resolves for any caller because its resolver never asks "may *this* principal see *this* field?" Object-level authz (`b-api-abuse`'s BOLA) is not enough: the user object is legitimately readable, but the *field* isn't. **Why it arises:** authorization is checked at the query root ("is this user logged in?") and assumed to cover everything beneath it. Every sensitive field needs its own check, in its own resolver.

**How defenders see it.** `__schema` / `__type` in request bodies is the introspection tripwire — legitimate clients almost never send these in production. Nested-query abuse shows up as requests with extreme brace depth and response-time outliers on `/graphql`. Field-level gaps are found in code review (resolvers without authz checks) and in testing (request every sensitive field as a low-privilege principal). Detection rule shapes: alert on introspection queries in production traffic; alert on `/graphql` requests over N levels deep or over M ms.

### Worked example: the Harborlight GraphQL demo

A real GraphQL server (graphql-core 3.3.0, local only — the walkthrough runs it): `Query.user(id:)`, `User.posts`, `Post.comments`, `Comment.author` — each level fans out 5x, and `User.ssn` has no authorization check.

- Baseline: `{ user(id: 1) { name } }` → `{"name": "alice"}`. The engine is real.
- Introspection: `{ __schema { types { name } } }` → the full type list (`Query`, `User`, `Post`, `Comment` — plus every field, on request). The API documented itself to you.
- Field-level gap: `{ user(id: 1) { name ssn } }` → `{"name": "alice", "ssn": "000-00-0001"}`. No check in the resolver; the sensitive field came back to an unprivileged query.
- Nested DoS: the 6-level nesting query → **17,143 response chars in 0.02s** from a 90-char query. The work factor is yours to choose; the server's bill grows exponentially with depth.

The fix, in the same server: introspection disabled (400 on `__schema`), per-field authorization on `ssn` (null + "forbidden"), query depth limit of 4 (400 on the deep query). Re-test all three, plus a legitimate query to confirm the API still works. Then the general rule: **introspection off in production, cost/depth limits on every query, authorization in every sensitive resolver** — three lines that close the three GraphQL-specific classes.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-graphql.log`. Clean environment: graphql-core 3.3.0, stock Python 3.12, loopback only, 2026-10-10. A real GraphQL engine, not a simulation.

1. **Start the server.** Save the `app.py` from this lesson's companion (`pip install graphql-core` first) and run it on port 8338. Confirm the baseline: POST `{"query": "{ user(id: 1) { name } }"}` to `/graphql` → `{"name": "alice"}`.
2. **Dump the schema via introspection.** POST `{ __schema { types { name } } }` → the type list. Then go one deeper: `{ __type(name: "User") { fields { name } } }` → every field on User, including `ssn`. Write down what an attacker learns from these two queries alone.
3. **Prove the field-level gap.** POST `{ user(id: 1) { name ssn } }` → the SSN returns. You are an unprivileged querier; the resolver never asked. This is the finding — quote the exact query and response.
4. **Prove the nesting multiplier.** POST the 6-level nesting query from the companion → note the response size vs the query size. Compute the ratio. Then *think*, don't run: what would depth 10 do at 5x fanout? (The math is the lesson; the server is grateful you didn't.)
5. **Apply the fix.** Restart with `FIXED=1` on port 8339: introspection disabled, `ssn` resolver checks authorization, depth limit 4.
6. **Verify the fix — four cases.** Introspection → 400; `ssn` → null + forbidden error; the deep query → 400 depth-exceeded; a legitimate `{ user(id: 1) { name email } }` → 200 with data. A fix that breaks the API is not a fix.
7. **Read the defender view.** The companion logs query strings. Find your `__schema` probe and your deep query. Write the two detection rules: alert on introspection strings in production traffic; alert on queries over the depth limit — and note that the depth rule only works if the *limit* exists server-side.

No step above is marked "not run by us" — introspection, the field gap, the nesting multiplier, and all four fix verifications ran against the real engine locally.

## 5. On your own

**Task:** Pick one authorized target you have not touched in this lesson — a public GraphQL API in a bounty program's scope, or a PortSwigger lab covering GraphQL. In order: (1) send the introspection query — record whether it answers and what you learn; (2) request every field on the principal object type as the lowest-privilege principal you have, diffing against what the UI shows; (3) construct a nested query two levels deeper than the UI ever goes and measure the response-time delta (do *not* run an actual DoS — measure, then stop).

**Success test:** A one-page report: introspection status (on/off, evidence), the field-level test matrix (field × principal → allowed/denied, with the gaps named), the nesting measurement (depth vs response time, no DoS performed), the three fixes stated for that stack, and the defender detection (which log, which patterns). If introspection is off, document how you confirmed it — a characterized defense is a result.

## 6. Where it goes wrong

- **"It's just like REST."** The four base classes transfer; the three GraphQL-specific ones don't exist in REST. Test for all seven.
- **Disabling introspection and declaring victory.** Introspection-off hides the schema; it doesn't fix the field-level gaps or the nesting cost. It is obscurity, not authorization.
- **Depth limits alone.** A depth-4 query can still be expensive if each level fans out 1000x (pagination without caps). Depth limits + cost analysis + pagination caps, together.
- **Measuring DoS by actually DoSing.** On an authorized target, measure the *scaling* (depth vs time on small increments) and report the projection. Running the full exponential query is the impact, not the test — and outside scope it is an attack.
- **Forgetting mutations.** Introspection dumps mutations too. Every mutation is an endpoint — test each one with the `b-api-abuse` four classes.
- **Assuming the framework handles authz.** Frameworks provide the *hook* (directives, middleware); the checks are still yours to write, per field, per resolver.

## 7. Read the source

Primary documents first:

- **GraphQL spec — Introspection** (spec.graphql.org — verified 2026-10-10): what `__schema` is *supposed* to do, which is why it's on by default. *Read* the introspection section; *note* the spec assumes a trusted context.
- **PortSwigger Web Security Academy — API testing** (portswigger.net/web-security/api-testing — verified 2026-10-10): the GraphQL-relevant methodology. *Read* the GraphQL sections.
- **CWE-862 / CWE-770** (cwe.mitre.org — verified 2026-10-09/10): Missing Authorization and Uncontrolled Resource Consumption. *Skim*; cite the IDs.

Then at most three free resources:

1. **graphql-core docs** (graphql-core-3.readthedocs.io — free): the engine from this lesson's walkthrough — read the execution model to understand what a nested query costs.
2. **`b-api-abuse`** (this guidebook): the four base classes, unchanged in GraphQL — BOLA, over-exposure, mass assignment, throttles.
3. **OWASP API Security Top 10:2023** (owasp.org/API-Security — free): API4 (resource consumption) and API1 (BOLA) are the GraphQL-relevant entries.

## 8. Check yourself

1. Explain why GraphQL introspection is enabled by default, what an attacker learns from `__schema`, and why disabling it is obscurity rather than a fix.
2. A 90-character query produces a 17KB response in 0.02s. Explain the fanout mechanism, and why REST endpoints don't have this property.
3. The `ssn` field returns data to any caller while the `user` object itself is legitimately readable. Explain why object-level authorization doesn't cover this, and where the check belongs.
4. A team sets a query depth limit of 10 and declares the DoS class fixed. Explain two ways expensive queries still get through, and state the complete defense.
5. Explain why every GraphQL mutation must be tested with the four `b-api-abuse` classes, even though this lesson focused on queries.

## 9. Prove it

**Artifact:** the one-page report from "On your own": introspection status, the field×principal matrix, the nesting measurement (no DoS performed), the three fixes for that stack, defender detection — plus your local-demo notes (the three proofs and four fix verifications).

**This lesson takes you to Level 3 (Apply).** You can honestly claim: you can probe GraphQL introspection, test field-level authorization, measure nested-query cost scaling, and verify the three fixes — on authorized targets, without performing denial of service. You cannot yet claim: production GraphQL security review — persisted queries, cost-analysis tuning, and gateway policy design are the operational layer this lesson doesn't cover.

## 10. Leads to

- `b-api-abuse` (re-read) — the four base classes that apply unchanged; GraphQL is the *added* surface, not a replacement.
- `b-race-conditions` — the next class where the client's freedom of action is the vulnerability.
- `c-vuln-ecosystem` — where GraphQL's `__schema` habit meets the attacker's reconnaissance workflow.
- Map refs: **CWE-862** · **CWE-770** · **GraphQL spec (introspection)**.
