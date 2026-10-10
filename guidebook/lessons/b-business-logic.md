---
lesson_id: b-business-logic
slug: business-logic
stage: B
level: 3
prerequisites: [b-idor, b-sqli, b-xss]
roles: [pentester, appsec]
map_refs: []
test_date: 2026-10-09
description: "Business-logic flaws: map the workflow, violate its assumptions — price tampering, coupon races and negative quantities, with server-side fixes and business-anomaly detection. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · local demo shop (price tamper, coupon race, negative quantity)"
---
# Business-logic flaws: when the code works and the rules don't


---

## 1. Where this shows up

Business-logic flaws are the highest-creativity class in bounty work: no injection, no misconfiguration, just the application's own rules failing when a user deviates from the expected path. They sit in **OWASP Top 10:2025 A06 — Insecure Design** and are tested per **WSTG-BUSL**. Scanners cannot find them — there is no malicious syntax to match — which is exactly why they pay: the entire signature layer is blind to a request that is perfectly well-formed and completely wrong.

## 2. Before you start

- You have finished the wave-1 lessons above; every one of them taught you to distrust one thing the client controls, and this lesson generalizes that into a method.
- **Authorization:** the walkthrough abuses a demo shop on your own loopback interface, plus PortSwigger's business-logic labs (permission granted by design). The discipline from the research holds: one tampered purchase proves the flaw — you never actually steal, never touch a real store's checkout, never replay against a production coupon system.
- Tooling: Python 3 (stdlib only), curl. Paper or a text file for the state-machine map — you will draw before you touch.

## 3. How it works

Every other class in this wave is about the application *mishandling input*. Business-logic flaws are about the application *doing exactly what it was coded to do*, where what it was coded to do is wrong. The vulnerability is not in a line of code but in an **assumption** nobody wrote down: users will use the browser UI (so client-side controls suffice), steps happen in order, numbers are positive, coupons apply once, the total on the receipt is the total the server computed.

The finding methodology is a discipline, not a trick. Run it in this order on every workflow you test:

**1. State-machine mapping.** Enumerate every state of the workflow and every transition between states, then draw it. Cart → checkout → payment → fulfillment, with the arrows labeled. The flaws live in the transitions the designers didn't draw: can checkout be reached without a cart? Can payment be revisited after fulfillment? Can the same state be entered twice?

**2. Workflow-step analysis.** For each step ask four questions: can it be *skipped*, *repeated*, *reordered*, or *revisited*? Repeat gives you coupon reuse and double-spend. Skip gives you checkout without payment. Reorder gives you confirmation before payment. Revisit gives you replaying a completed step against changed state.

**3. Trust-boundary review.** Mark every value the client supplies that the server *uses*: price, quantity, discount, currency, user ID, step index, the total itself. Each one is a candidate for tampering. The rule that kills the whole class: **the server re-derives every money value from its own data and never accepts a client-computed amount.** A price in a POST body is not a price; it is a suggestion from a stranger.

**4. Numeric edge fuzzing.** For every numeric field, try `-1`, `0`, `0.0001`, absurdly large values, and negative discounts. Watch the computed total. Applications that never considered a negative quantity will happily subtract it.

**5. Race/parallelism check.** Where two requests touch the same balance, coupon, or stock count, fire them concurrently. If the check ("is this coupon unused?") and the action ("mark it used") are two separate steps, the second request slips between them.

### Worked example: the demo shop

The shop has three items with server-side prices (mug 12.00, shirt 25.00, sticker 3.00), a cart, a coupon box, and a checkout that charges the total. Mapping the workflow surfaces three assumptions in the first pass: (a) the client sends the *price* with each add-to-cart request and the server trusts it; (b) the coupon `SAVE10` ("10 off, single use") is validated by checking a flag and then, separately, applying the discount; (c) quantity is a number the client chooses and the server multiplies.

Each assumption is a finding waiting for a request. Change the price parameter on add-to-cart: the server charges the tampered price — excessive trust in client-side controls, the canonical PortSwigger lab. Apply `SAVE10` in two sessions *before either checks out*: the coupon endpoint checks the single-use flag but only consumes the coupon at checkout, so both sessions see "unused" and both get the discount — a check-then-act race that sequential testing misses. Set quantity to `-1`: the line total goes negative and drags the order total down — the server never asked whether a quantity can be negative.

None of these requests looks malicious. There is no `<script>`, no `' OR 1=1`, no `../`. A WAF sees a well-formed POST and waves it through. That is the entire point of the class, and the entire reason the defender's detection has to be *business* telemetry — reconciliation, not signatures.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-business-logic.log`. Clean environment: stock Python 3.12, curl 8.5.0, loopback only, 2026-10-09. The demo shop (`logic-demo.py`, stdlib only) implements the cart/coupon/checkout workflow above on 127.0.0.1:18093. No real money, no real store, nothing external.

**Step 1 — start the demo and map the workflow.** Run `python3 logic-demo.py 18093 &`. Before touching it, draw the state machine from the lesson's worked example: browse → add → coupon → checkout → receipt. Write the three assumptions down (client price trusted; coupon check-then-apply; quantity unvalidated). The map comes before the requests — that ordering *is* the methodology.

**Step 2 — baseline: a honest purchase.** `curl -s -c jar -X POST -d "item=mug&price=12.00&qty=1" http://127.0.0.1:18093/cart/add` then `curl -s -b jar -X POST http://127.0.0.1:18093/cart/checkout`. Receipt shows `total=12.00`. This is the control: the workflow behaving as designed.

**Step 3 — violate assumption (a): tamper the price.** `curl -s -c jar2 -X POST -d "item=mug&price=0.01&qty=1" http://127.0.0.1:18093/cart/add` then checkout with `-b jar2`. Receipt: `total=0.01`. The server charged the client-supplied price. One tampered purchase proves it; the finding is complete.

**Step 4 — violate assumption (b): the coupon race.** The coupon endpoint *checks* the single-use flag but only *consumes* the coupon at checkout — a check-then-act gap. Two sessions, interleaved: session A adds a shirt and applies `SAVE10` → `discount=10.00` (no checkout yet); session B adds a shirt and applies the same `SAVE10` → `discount=10.00` again, because the flag still reads unused; then both check out → two receipts at `total=15.00`. The single-use coupon paid out twice. The methodology's race check (step 5 of "How it works") is what finds this: sequential testing would have missed it, because a lone second order *is* correctly rejected once the first checks out.

**Step 5 — violate assumption (c): negative quantity.** `curl -s -c jar4 -X POST -d "item=sticker&price=3.00&qty=-1" …/cart/add`, checkout. Receipt: `total=-3.00`. The shop owes *you* three dollars. The server multiplied without asking whether quantities can be negative.

**Step 6 — the fix, all three.** Restart with `FIXED=1`: prices are looked up server-side by item id (the client's price field is ignored), the coupon is consumed atomically in the same operation that validates it (second use → `already used`), quantity is coerced to an integer ≥ 1. Re-run steps 3–5: tampered price → charged 12.00; second `SAVE10` → rejected; qty=-1 → rejected with `invalid quantity`. The receipt totals reconcile with the server's own price table in every case.

**Step 7 — defender: read the order log.** The vulnerable run's order log shows the three abuses as *business* anomalies, not attack signatures: `total=0.01` on a 12.00 item, `coupon SAVE10 used 2 times`, `total=-3.00`. Detection here is reconciliation rules: alert on any order with total ≤ 0, any coupon used more times than its limit, any line total that doesn't equal quantity × server price. Write these as the detection half of your report — the developer fixes the code, the defender watches the ledger.

**Step 8 — stop the demo.** `pkill -f logic-demo.py`; verify with `pgrep -f "logic-demo.py"` (excluding the shell's own match) that nothing remains.

## 5. On your own

Take the fixed demo shop and find a *fourth* assumption the walkthrough didn't violate. Candidates the methodology suggests: the currency parameter (is there one? what happens if you add it?), revisiting checkout twice for the same cart (double-charge or double-fulfillment?), applying the coupon *after* checkout. **Success test:** you can state the assumption in one sentence, demonstrate the violation with one request sequence, and name the server-side rule that would stop it.

## 6. Where it goes wrong

- **Testing the UI instead of the workflow.** The browser enforces order, positivity, and single-use — the server must too. Every logic test worth running bypasses the UI and talks to the endpoints directly. If your "test" is clicking buttons, you tested the theater, not the play.
- **Stopping at the first abuse.** Workflows have multiple assumptions; the methodology's five steps exist because one tampered price doesn't imply the coupon is safe. Map first, then violate *each* assumption.
- **Calling it "low severity" because there's no RCE.** A price-tampering flaw that lets anyone buy inventory at a cent is a direct financial loss. Severity follows business impact — argue it in money, units, or accounts affected, not in exploit sophistication.
- **Fixing the client.** Disabling the price field in JavaScript, hiding the coupon box after use, setting `min="1"` on the quantity input — none of these is a fix. The client is the attacker's machine. Every rule must be enforced server-side.
- **Race-condition hand-waving.** "We check the coupon flag" is not a fix if check and consume are separate operations. Atomicity — one indivisible validate-and-consume — is the fix; rate limiting only narrows the window.
- **WAF as detection.** There is nothing to signature-match. Teams that rely on WAF logs for logic flaws will find them in the chargeback reports instead. Detection is reconciliation: totals, counts, state transitions.

## 7. Read the source

Primary documents — read in this order:

1. **PortSwigger Web Security Academy — Business logic vulnerabilities** (portswigger.net/web-security/logic-flaws): definition, the flaw families, prevention practices. Read fully, then work the labs (11+ labs: excessive trust in client-side controls, low-level logic flaws, inconsistent handling of exceptional input, weak isolation on dual-use endpoints, insufficient workflow validation, flawed state machines). *Verified in-session 2026-10-10.*
2. **OWASP Top 10:2025 — A06 Insecure Design** (owasp.org/Top10/2025/): what "insecure design" means as a category and why logic flaws live there rather than under Injection. *Verified in-session 2026-10-09.*
3. **WSTG business-logic testing** (owasp.org/www-project-web-security-testing-guide/ — WSTG-BUSL): the test-case checklist form of this lesson's methodology. Skim the test IDs; use as a checklist on your next workflow.

Free resources for going deeper (≤3): **PortSwigger business-logic labs** (the hands-on companion); **Juice Shop logic challenges** ("Payback Time" negative-quantity, "Christmas Special" — gamified, free); **disclosed HackerOne logic-flaw reports** (read for how impact is argued in money terms — study the reasoning, never the payload).

## 8. Check yourself

1. A checkout accepts `{"item": "mug", "price": 12.00, "qty": 2}`. The developer fixes price tampering by removing the price field from the HTML form. Why is the vulnerability still present, and what is the correct fix?
2. A coupon is validated (`if not used: apply_discount(); mark_used()`). Two requests arrive simultaneously and both get the discount. Explain the interleaving, then name the fix that makes the violation impossible rather than merely unlikely.
3. Why can't a WAF or signature-based IDS detect a negative-quantity order? What *can* detect it, and where does that detection live?
4. Draw the state machine for "apply coupon → checkout → receipt" and mark three transitions the designer probably didn't draw. For each, name the abuse.
5. A bug-bounty report says "I bought a $25 shirt for $0.01 by editing the price parameter." What three facts must the report establish for the triager to reproduce it, and what is the honest severity argument?

## 9. Prove it

**Artifact:** a workflow-abuse write-up against a lab target (PortSwigger business-logic lab or the local demo): the intended flow as a state-machine diagram, the abused flow as a request sequence, the financial or logical impact stated concretely, and the server-side rule that stops it — plus the defender's reconciliation rule that would catch it in the logs.

**After this lesson you can honestly claim:** you can systematically map a web workflow, violate each of its assumptions with minimal proof-of-concept requests, and specify server-side fixes plus business-anomaly detection. **You cannot yet claim:** your methodology covers concurrency attacks at scale — race conditions get their own second-wave lesson — or that you can assess workflows you can't see, like multi-service checkout pipelines.

## 10. Leads to

Next: `b-session-auth` (the other half of "who are you and what may you do" — authentication and session flaws), then `b-security-headers` (the browser-defense layer that shrinks every class's blast radius). Map refs: **OWASP Top 10:2025 A06 — Insecure Design**; WSTG-BUSL; CWE-840/CWE-841; feeds Stage C disclosure write-ups (a logic flaw is only a finding once it's written up).
