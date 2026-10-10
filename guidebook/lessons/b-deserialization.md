---
lesson_id: b-deserialization
slug: deserialization
stage: B
level: 3
prerequisites: [a-python-security, a-http-depth]
roles: [pentester, appsec]
map_refs: []
test_date: 2026-10-10
description: "Insecure deserialization: when data builds the objects — untrusted-data deserialization reproduced locally, then fixed with integrity checks and safe formats. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-10 · transcript in runs/b-deserialization.log"
---
# Insecure deserialization: when data builds the objects


**Map refs:** CWE-502 (Deserialization of Untrusted Data) · PortSwigger Web Security Academy (Deserialization)

---

## 1. Where this shows up

Applications constantly convert objects to bytes and back — sessions in cookies, cached objects, messages between services, "remember me" tokens. **Serialization** is object→bytes; **deserialization** is bytes→object. The vulnerability is deserializing bytes the attacker controls with a format powerful enough to *execute code during reconstruction*. Python's `pickle`, Java's native serialization, PHP's `unserialize`, .NET's `BinaryFormatter` all have this property: the format can encode "call this function," and the parser obeys while reading. This lesson takes you to Level 3: you will make a local server execute your code at unpickle time, then replace the format and verify the fix.

## 2. Before you start

- You can read Python and run shell commands (`a-python-security`, `a-linux-cli`).
- You understand cookies carry client-controlled state (`a-http-depth`) — this lesson's session cookie is the attack vector.
- Your target is written down and authorizes your testing: this lesson's local demo, a PortSwigger Academy deserialization lab, or a bounty program whose scope explicitly includes the asset. The payload pattern here is *generic and powerful* — it belongs in labs and authorized scope, never in curiosity-driven testing. Re-read B-AUTH if this sentence surprised you.
- Tooling: Python 3 and curl. No proxy needed; the payloads are hand-built.

## 3. How it works

Serialization formats sit on a spectrum. **Data-only formats** (JSON, XML without entities) describe values: strings, numbers, lists. **Code-capable formats** (pickle, Java serialization, PHP serialize) describe *object graphs including behavior*: "create an instance of class X," "call function Y with these arguments." Deserializing untrusted bytes with a code-capable format hands the attacker a tiny programming language that runs during parsing.

The vulnerable shape (Python):

```python
session = request.cookies["session"]
data = pickle.loads(base64.b64decode(session))  # attacker controls these bytes
```

The attacker crafts bytes whose unpickling calls `os.system("...")` — via `__reduce__`, which tells pickle "to rebuild this object, call this callable with these arguments." The call happens *inside* `pickle.loads`, before the application ever looks at the result. Your "session cookie" just ran a shell command on the server.

**Why it arises in real code.** The developer needed state in a cookie and reached for the language's built-in serializer — one line, round-trips any object. They tested with their own session and never asked "what bytes could an attacker put here?" Frameworks have shipped this default (and the CVE) more than once.

**Gadget chains, at concept level.** Real exploitation rarely calls `os.system` directly. Libraries on the classpath (Java) or importable modules (Python/PHP) contain **gadgets**: classes whose methods, when invoked in the right sequence during deserialization, reach something dangerous. (The classpath — the list of places Java looks for classes — is every library the application ships with.) Attackers chain gadgets — `A` calls `B` calls `C` calls `Runtime.exec`. Finding chains is researcher work (the famous Java work is the "gadget chain" literature); *using* them is lab-bounded. What you must take from the concept: the danger isn't one bad class, it's the *format's* power combined with a rich standard library. This is why the fix is "don't deserialize untrusted data with code-capable formats," not "blocklist `os.system`." The parser is the trust boundary because the parser is a tiny interpreter: its instruction set *is* the attack surface. A data-only format's instruction set is "build values"; a code-capable format's instruction set includes "call functions." You cannot patch an instruction set with a blocklist — you change the interpreter.

**How defenders see it.** In code review: `pickle.loads`, `yaml.load` (not `safe_load`), `unserialize(`, `ObjectInputStream.readObject`, `BinaryFormatter.Deserialize` on anything reachable from the network. (Alerting on these in code search is a SAST-shaped finding — SAST is static application security testing: analyzing code without running it.) In logs and traffic: over-long opaque blobs in cookies/parameters (base64 pickles have a recognizable shape — they often start with `gASV`), especially ones that change between requests without the application visibly using them. Detection rule shapes: alert on `pickle.loads`/`readObject` in code search; alert on base64 blobs over N bytes in session cookies that the application never legitimately rotates. In the cookie-length log the walkthrough keeps, the attack stands out as a size anomaly:

```
session cookie len=48   user=alice   (legitimate)
session cookie len=48   user=alice   (legitimate)
session cookie len=312  user=alice   (the pickle — 6x the legitimate size band)
```

Legitimate sessions don't change size. The blob that does is the one to inspect.

### Worked example: the session-cookie demo

A login/dashboard app (stdlib Python, local only — the walkthrough runs it). `/login?user=alice` sets a `session` cookie containing a base64 pickled dict; `/dashboard` unpickles it.

Baseline: login → cookie decodes to `{'user': 'alice'}` → dashboard says "welcome, alice." Probe: craft a pickle whose `__reduce__` calls `os.system("touch /tmp/deserwalk/PWNED-marker")` — a *benign marker file*, labeled, local-only — and send it as the session cookie. Result: the marker file **exists** afterward. Your code ran inside `pickle.loads`, on the "server." (The app then 400s because the return value wasn't a dict — the execution already happened during unpickling, which is the point: the damage precedes any application logic.)

The fix, in the same app: sessions become **JSON + HMAC** — data-only format, tamper-evident signature with a server-side key. (HMAC — a keyed hash computed with a secret only the server knows; it makes tampering detectable because the attacker can't recompute a valid signature.) Re-test: legitimate cookie → 200; flipped `user` field with the old signature → 403; a pickle blob sent to the fixed endpoint → 400 without any unpickling. Then the general rule: **deserialize untrusted input only with data-only formats, and sign what must not change** — and where a code-capable format is unavoidable, integrity-check (HMAC) *before* deserializing, never after.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-deserialization.log`. Clean environment: stock Python 3.12, loopback only, 2026-10-10. The payload writes a benign marker file in /tmp, labeled in the companion — the standard teaching proof, nothing more.

1. **Start the app.** Save the `app.py` from this lesson's companion and run it on port 8336. Confirm the baseline: log in as alice, decode the cookie (`base64 -d`), observe the pickle bytes; visit `/dashboard` with the cookie → "welcome, alice."
2. **Build the benign-evil pickle.** In Python: a class whose `__reduce__` returns `(os.system, ("touch /tmp/deserwalk/PWNED-marker",))`; `pickle.dumps` it, base64 it. Read your payload before sending it — you should be able to say exactly what it will do.
3. **Prove code execution at unpickle time.** Send the payload as the session cookie → observe the marker file's existence with `ls -la`. The file existing *is* the vulnerability: your code ran inside the server's `pickle.loads`. Note the app's 400 afterward and explain why it doesn't matter (execution preceded application logic).
4. **Apply the fix.** Restart with `FIXED=1` on port 8337: JSON session + HMAC-SHA256 signature, server-side key.
5. **Verify the fix — three cases.** Legitimate login → 200 "welcome, alice"; tampered `user` field (old signature) → 403; a pickle blob → 400 with no unpickling attempted. A fix that breaks legitimate sessions is not a fix — confirm login still works.
6. **Read the defender view.** The companion logs cookie lengths. Find your oversized pickle cookie in the log. Write the detection rule: alert on session cookies matching the base64-pickle shape or exceeding the legitimate size band — and write the code-review rule next to it: `pickle.loads` on network-reachable input is a finding on sight.

No step above is marked "not run by us" — the execution proof and all three fix verifications ran locally. Gadget-chain construction beyond `__reduce__` is concept-level here and lab-bounded in PortSwigger's labs.

## 5. On your own

**Task:** Pick one authorized target you have not touched in this lesson — a PortSwigger Academy deserialization lab (start with "Modifying serialized objects" — the no-code-execution variant — before the RCE labs). First *identify the format*: base64-decode the cookie/object and look for format markers (pickle's `gAS`, Java's `rO0`, PHP's `O:8:`). Then follow the lab: modify a value without breaking the signature scheme it documents, escalate only as the lab instructs.

**Success test:** A one-page report: the format identified (with the marker bytes quoted), the exact modification or payload, the evidence it worked, the fix for that stack (data-only format + signature, or integrity-before-deserialization), and the defender detection (code pattern + traffic shape). If the lab's object is signed, document how the signature scheme works before attempting anything — understanding the scheme is the result.

## 6. Where it goes wrong

- **"We base64 it, so it's safe."** Encoding is not encryption and not integrity. Base64 just changes the alphabet; the attacker speaks it fluently.
- **"We check the signature after unpickling."** The code runs *during* unpickling. Verify-then-parse is the only order; parse-then-verify is the vulnerability wearing a seatbelt it put on after the crash.
- **Blocklisting dangerous classes.** Gadget chains route around blocklists — the vulnerable surface is the *format's* power, not one callable. Change the format.
- **"It's an internal service."** Internal services receive attacker-influenced data constantly (caches, queues, cookies forwarded between services). "Internal" is not a trust boundary for deserialization.
- **Running the payload outside authorized scope.** This lesson's payload pattern is generic and powerful. It belongs in the local demo and authorized labs — the safety line from the brief applies in full.
- **Forgetting `yaml.load`.** PyYAML's `load` (vs `safe_load`) is the same vulnerability in a config file. Grep your own projects after this lesson.

## 7. Read the source

Primary documents first:

- **PortSwigger Web Security Academy — Insecure deserialization** (portswigger.net/web-security/deserialization — verified 2026-10-10): the canonical treatment — PHP/Java/Python/.NET specifics, gadget concepts, labs. *Read* fully, then do the labs in order.
- **OWASP Deserialization Cheat Sheet** (cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html — verified 2026-10-10): the fix catalog per language. *Read* your stack's section.
- **CWE-502** (cwe.mitre.org/data/definitions/502.html — verified 2026-10-10): Deserialization of Untrusted Data. *Skim*; cite the ID.

Then at most three free resources:

1. **PortSwigger deserialization labs** (portswigger.net/web-security — free): from modified objects through documented RCE, hosted and authorized.
2. **Python `pickle` docs warning** (docs.python.org — free): the standard library itself says never to unpickle untrusted data — read the warning as a primary source on the format's power.
3. **`b-session-auth`** (this guidebook): session design done right — what should have been in that cookie instead.

## 8. Check yourself

1. Explain why the marker file existing proves the vulnerability, even though the app returned 400 afterward — at which exact moment did your code run?
2. A developer "fixes" pickle deserialization by verifying an HMAC *after* `pickle.loads` returns. Explain why the order is wrong and state the correct order.
3. Explain the difference between a data-only format (JSON) and a code-capable format (pickle) in terms of what the *parser* is allowed to do.
4. You see `gASVEwAAAAAAAAB` at the start of a base64 session cookie. Name the format, explain what the prefix tells you, and state your next step on an authorized target.
5. Explain what a gadget chain is and why blocklisting `os.system` does not fix a deserialization vulnerability.

## 9. Prove it

**Artifact:** the one-page report from "On your own": format identified with marker bytes, the modification/payload, evidence, the per-stack fix, defender detection — plus your local-demo notes (the marker-file proof and the three fixed-build cases).

**This lesson takes you to Level 3 (Apply).** You can honestly claim: you can identify serialization formats in the wild, prove code execution via deserialization on an authorized target with a benign marker, and verify the data-only-format fix. You cannot yet claim: gadget-chain research — finding new chains in libraries is researcher work, and using known chains outside labs and authorized scope violates the safety line.

## 10. Leads to

- `b-session-auth` — what belongs in a session cookie instead of a pickled object.
- `b-ssti` — the same "untrusted input reaches a powerful interpreter" shape, one layer up (template engines).
- `d-malware-analysis` — from the defender's side: what serialized payloads look like in the wild.
- Map refs: **CWE-502** · **PortSwigger Deserialization** · **OWASP Deserialization Cheat Sheet**.
