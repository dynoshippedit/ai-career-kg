---
lesson_id: b-race-conditions
slug: race-conditions
stage: B
level: 3
prerequisites: [a-http-depth, b-business-logic]
roles: [pentester, appsec]
map_refs: []
test_date: 2026-10-10
description: "Race conditions: when check-then-act isn't atomic — TOCTOU flaws reproduced locally with parallel requests, then fixed with atomic operations. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-10 · transcript in runs/b-race-conditions.log"
---
# Race conditions: when "check, then act" isn't atomic


**Map refs:** CWE-367 (Time-of-check Time-of-use) · PortSwigger Web Security Academy (Race conditions)

---

## 1. Where this shows up

Most web code runs as **check, then act**: check the coupon is unused, then apply the discount; check the balance covers the transfer, then move the money; check the username is free, then create the account. Between the check and the act there is a gap — database writes, payment calls, network round-trips — and in that gap, a second request can pass the *same* check. Both requests then act. The single-use coupon is redeemed twice; the balance goes negative; the "unique" username exists twice. This lesson generalizes the `b-business-logic` coupon race into the full class, and takes you to Level 3: you will win the race locally, then close it.

## 2. Before you start

- You can read HTTP requests and responses cold (`a-http-depth`).
- You have done `b-business-logic` — its coupon race is this lesson's worked example, extended to the general check-then-act pattern.
- You understand threads at the level of "two things happening at once" — the walkthrough uses two threads; the concept is concurrent requests, however they arrive.
- Your target is written down and authorizes your testing: this lesson's local demo, a PortSwigger Academy race-conditions lab, or a bounty program whose scope explicitly includes the asset. Race testing sends *bursts* of requests — confirm the program tolerates burst traffic before you start, and keep every burst small and local-first. Re-read `b-authorization-scope` if this sentence surprised you.
- Tooling: Python 3 (threads) and curl. No proxy needed.

## 3. How it works

The vulnerable shape, in pseudocode:

```
if coupon.uses_left > 0:      # CHECK
    ...slow work here...       # the window: DB write, payment call
    coupon.uses_left -= 1      # ACT
    apply_discount()
```

Request A checks: `uses_left` is 1, proceeds. Before A acts, request B checks: `uses_left` is *still* 1 (A hasn't decremented yet), proceeds. Both act. The coupon was single-use; it has now been used twice, and `uses_left` reads -1 — the arithmetic itself testifies.

**Why it arises in real code.** The developer tested sequentially: redeem, redeem again, second one correctly rejected. Sequential testing can *never* find a race — the flaw exists only in the interleaving. And the window is invisible in code review unless you're looking for it: the check and the act are each correct; only their *non-atomicity* is wrong. (Atomic means indivisible: the operation completes entirely or not at all, with no observable intermediate state — no other request can catch it half-done.) The wider the window between them (a payment-gateway call, an email send), the easier the race is to win.

**The general class.** Anywhere state is read, then written based on the read:
- **Balances and transfers:** check-then-debit across two requests → negative balances, duplicated payouts.
- **Unique constraints:** check-username-free then insert → duplicates (the database's UNIQUE constraint is the atomic fix).
- **Limited inventory / ticket sales:** check-stock then decrement → overselling.
- **Password-reset / token consumption:** check-valid then consume → token reuse.
- **File uploads:** check-extension then save → the TOCTOU the CWE is named for (time-of-check vs time-of-use on the filesystem).

**Why single-request testing misses it.** Scanners send one request at a time. So do humans clicking through the UI. Races require *concurrency*: two requests in flight simultaneously, timed to land inside the window. That is also why races are flaky — sometimes you win, sometimes you don't — and why the finding must include the *mechanism* (the check/act gap you identified in code or behavior), not just "it worked once."

**How defenders see it.** The arithmetic testifies: `uses_left = -1`, negative balances, duplicate usernames, two redemptions one millisecond apart in the logs. An invariant is a condition the application promises is always true — `uses_left` never goes negative, usernames are unique. The race breaks the promise, and the broken promise is the evidence:

```
2026-10-10T01:15:44.112Z redeem coupon=SAVE10 session=A result=200 uses_left=0
2026-10-10T01:15:44.112Z redeem coupon=SAVE10 session=B result=200 uses_left=-1
```

Same millisecond, same coupon, two sessions — and the counter at -1. Detection rule shapes: alert on invariant violations the application should never produce (negative counters, duplicate "unique" values); alert on near-simultaneous duplicate actions from one principal. In code review: any read-then-write on shared state without atomicity — the fix shapes below are what you look for.

### Worked example: the coupon race, generalized

A coupon endpoint (stdlib Python, local only — the walkthrough runs it): `POST /redeem {"coupon": "SAVE10"}` checks `uses_left > 0`, sleeps 0.3s (standing in for the slow work — DB write, payment call), then decrements and applies the discount.

- Sequential: redeem → 200; redeem again → 409 "already used." Correct — and this is exactly what the developer tested.
- Race: two threads redeem *concurrently* → **both 200**, `uses_left` reads **-1**, redemptions = 2. The single-use coupon was used twice. The -1 is the proof: no legitimate sequence of operations produces it.

The fix, in the same app: the check and the act happen **under one lock** (in production: a database transaction with row locking, or an atomic compare-and-set / single UPDATE with a WHERE clause on the expected state — compare-and-set writes the new value only if the current value is still what you expect; if another request changed it first, your write fails instead of clobbering). Re-run the race: one 200, one 409, `uses_left` = 0. Then the general rule: **make check-and-act atomic** — the database, not application code, is the arbiter of shared state. Why the database: it is the one process every request passes through — the only place with a total order on operations. Ten app servers can disagree about what happened first; the database serializes them into a single sequence. Atomicity has to live where the order is decided.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-race-conditions.log`. Clean environment: stock Python 3.12, loopback only, 2026-10-10. The 0.3s sleep stands in for real slow work (labeled in the companion); the race mechanism is identical.

1. **Start the app.** Save the `app.py` from this lesson's companion and run it on port 8340. Confirm the baseline: `GET /state` → `uses_left: 1`.
2. **Prove sequential correctness.** Redeem once → 200 with the discount. Redeem again → 409 "already used." Write down: the developer's test suite passes. This is why the flaw shipped.
3. **Win the race.** Restart the app (fresh single-use coupon), then fire two concurrent redeems via the companion's threading snippet → **both 200**. `GET /state` → `uses_left: -1`, `redemptions: 2`. The -1 is your finding — quote it verbatim in your notes.
4. **Say the mechanism out loud.** Both threads passed the check before either acted, because the 0.3s window sits between them. The flaw is the *gap*, not the check and not the act.
5. **Apply the fix.** Restart with `FIXED=1` on port 8341: check+act under a single lock.
6. **Verify the fix.** Same two-thread race → one 200, one 409; `uses_left` = 0. Then the sequential test still passes (redeem → 200, redeem → 409). A fix that breaks legitimate redemption is not a fix.
7. **Read the defender view.** The companion logs each redemption with a timestamp. Find your two same-millisecond redemptions. Write the detection rule: alert on invariant violations (negative `uses_left`, duplicate redemptions of single-use coupons) — the arithmetic testifying, as section 3 says.

No step above is marked "not run by us" — the sequential baseline, the race win, and the fix verification all ran locally. Multi-host races (the window spanning servers) are the production variant; the mechanism and fix are identical.

## 5. On your own

**Task:** Pick one authorized target you have not touched in this lesson — a PortSwigger Academy race-conditions lab (start with "Limit overrun race conditions"). First *find the check-then-act gap*: read the lab's behavior the way section 3 teaches — what is checked, what is acted, and what slow work sits between them. Then race it with a small burst (the Academy's Turbo Intruder or a 2-thread script — keep it minimal), and confirm the invariant violation.

**Success test:** A one-page report: the check/act/window identified (with the evidence for each), the race result (exact responses, the invariant violation quoted), the fix stated as the atomicity rule for that stack, and the defender detection (which log, which invariant). If the race doesn't win in 5 attempts, document the attempts and the window analysis — a characterized race surface is a result; flakiness is data.

## 6. Where it goes wrong

- **Testing sequentially and declaring it safe.** The developer's test passed. Yours must be concurrent — the flaw exists only in the interleaving.
- **"It worked once" as the finding.** Races are flaky by nature. The finding is the *mechanism* (check/act/window) plus the invariant violation, not a single lucky run. Show the -1.
- **Fixing with a sleep or a retry.** Adding delays narrows the window; it doesn't close it. Attackers widen windows (slowloris-style) faster than you narrow them. Atomicity or nothing.
- **Locking in application code across hosts.** A Python lock fixes one process; production runs N processes behind a load balancer. The atomicity must live in the shared state: the database (transactions, row locks, conditional writes), not the app tier.
- **Forgetting the *read* side.** Some races are check-check-act: *two* checks race (username-free checked twice). Audit every read of shared state, not just the writes.
- **Burst-testing outside authorized scope.** Race testing is, by definition, abnormal traffic. Confirm burst tolerance in the scope *before* the first burst — this class has its own authorization footnote.

## 7. Read the source

Primary documents first:

- **PortSwigger Web Security Academy — Race conditions** (portswigger.net/web-security/race-conditions — verified 2026-10-10): the canonical treatment — limit overruns, multi-endpoint races, single-endpoint races. *Read* fully, then do the labs.
- **CWE-367** (cwe.mitre.org/data/definitions/367.html — verified 2026-10-10): Time-of-check Time-of-use Race Condition. *Skim*; cite the ID.

Then at most three free resources:

1. **PortSwigger race-condition labs** (portswigger.net/web-security — free): the lab set this lesson's method was built for, hosted and authorized.
2. **`b-business-logic`** (this guidebook): the coupon race as a business-logic finding — this lesson is its generalization to the concurrency class.
3. **Your database's locking docs** (postgresql.org or dev.mysql.com — free): `SELECT ... FOR UPDATE`, transactions, and conditional writes — the production fix, from the primary source.

## 8. Check yourself

1. Explain why the developer's sequential test (redeem → 200, redeem → 409) passed while the vulnerability was present, and what test would have caught it.
2. `uses_left` reads -1 after your test. Explain why no legitimate sequence of operations produces this value, and why it is stronger evidence than "both requests returned 200."
3. A developer "fixes" the race by adding a 2-second delay before the check. Explain why this doesn't work, and state the correct fix.
4. The app runs on 4 servers behind a load balancer. Explain why the Python-lock fix from the walkthrough is insufficient here, and where the atomicity must live.
5. Explain the difference between a check-then-act race and a check-check-act race, with an example of each.

## 9. Prove it

**Artifact:** the one-page report from "On your own": check/act/window, the race result with the invariant violation quoted, the atomicity fix for that stack, defender detection — plus your local-demo notes (sequential baseline, the -1, the fixed-build verification).

**This lesson takes you to Level 3 (Apply).** You can honestly claim: you can identify check-then-act gaps, win races with concurrent requests on authorized targets, and verify atomicity fixes. You cannot yet claim: production concurrency review — multi-host atomicity design (distributed locks, transaction isolation levels — the rules for how much of other transactions' unfinished work your transaction may see) is the operational layer this lesson points at but doesn't teach.

## 10. Leads to

- `b-business-logic` (re-read) — the coupon race as a business-logic finding; compare the *logic* flaw with the *concurrency* flaw in the same feature.
- `b-api-abuse` — API4:2023 (unrestricted resource consumption) is the rate-limit cousin; races are what throttles *don't* fix.
- `e-sdlc` — where the "test concurrently" requirement belongs in a development process.
- Map refs: **CWE-367** · **PortSwigger Race conditions**.
