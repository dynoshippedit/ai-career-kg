---
lesson_id: b-ssti
slug: ssti
stage: B
level: 3
prerequisites: [a-http-depth, b-xss]
roles: [pentester, appsec]
map_refs: []
test_date: 2026-10-10
description: "Server-side template injection: when user input becomes the program — context-aware exploitation reproduced locally, then fixed. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-10 · transcript in runs/b-ssti.log"
---
# Server-side template injection: when your input becomes the program


**Map refs:** CWE-94 (Code Injection) · PortSwigger Web Security Academy (SSTI)

---

## 1. Where this shows up

Web applications build pages from **templates**: files mixing fixed HTML with placeholders the server fills in (`Hello, {{ name }}`). Template injection happens when attacker input stops being *data placed into* the template and becomes *part of the template itself* — and the template engine then executes it. The impact ladder runs from reading server-side values, to reading files, to full remote code execution, depending on the engine. This lesson takes you to Level 3: you will reproduce the injection against a local toy engine, understand why real engines are worse, and verify the fix.

## 2. Before you start

- You can read HTTP requests and responses cold (`a-http-depth`).
- You understand the XSS lesson's data-vs-code distinction — SSTI is that distinction failing on the *server* instead of in the browser.
- Your target is written down and authorizes your testing: this lesson's local toy engine, a PortSwigger Academy SSTI lab, or a bounty program whose scope explicitly includes the asset. Template engines are also *your own* code's risk — the fix section is written for builders too. Re-read B-AUTH if this sentence surprised you.
- Tooling: curl. A cheat sheet of engine-specific payloads is for the labs, not this lesson.

## 3. How it works

A template engine takes two inputs: the **template** (written by the developer, contains code-like directives) and the **data** (values to fill in). The engine's job is to keep them separate — data is inert, only the template's own directives execute.

The vulnerability is a confusion of the two. The classic shape:

```python
# VULNERABLE: user input concatenated into the template SOURCE
page = render("Hello, " + user_input + "!")
```

When `user_input` is `alice`, the template is `Hello, alice!` — harmless. When `user_input` is `{{7*7}}`, the template is `Hello, {{7*7}}!` — and the engine evaluates `7*7` and renders `Hello, 49!`. Your arithmetic executed on the server. That evaluation is the entire vulnerability: **the engine cannot tell your input apart from the developer's template**, because they were concatenated before rendering.

**Why it arises in real code.** Developers build strings: greeting pages, email subjects, PDF filenames, error messages. Anywhere a template is assembled from parts that include user input — especially "preview" features ("see how your message looks") — the input can reach the template source. The developer tested with `alice`, never with `{{7*7}}`.

**Why real engines are worse than the toy.** The walkthrough's toy evaluates arithmetic. Production engines (Twig, Jinja2, Freemarker, Velocity, ERB, Smarty) expose an object model: `{{7*7}}` proves evaluation, and then engine-specific payloads walk from arithmetic to attribute access (`().__class__`, `config.items()`) to file reads to command execution. (The object model — the set of server-side objects and attributes the template is allowed to reach: config values, request data, and, in the worst engines, the whole runtime.) The *detection* payload is always the arithmetic one — safe, unmistakable. The *escalation* payloads are engine-specific and taught at concept level here: know that the ladder exists, know it ends at RCE, and practice the escalation only in PortSwigger's labs, where the targets are built for it.

**The framework angle.** Modern frameworks (Django, Rails, Jinja2 autoescape) keep user data out of template *source* by design — you pass variables, never concatenated strings. (Autoescape — the engine HTML-escapes every variable by default, so `{{ name }}` can never become markup unless the developer opts out.) SSTI appears where developers bypass the framework: rendering user-supplied templates (CMS themes, "custom email templates"), using the low-level render-string API on concatenated input, or misconfiguring sandbox mode. Sandboxes are allow-lists around a dangerous engine; the history of SSTI is the history of sandbox escapes. The fix is architectural, not a better sandbox. The reason the framework design holds: a template is *compiled once* into code, and variable values are *bound later*, at render time — after compilation is finished. Values supplied after the compile step can never become instructions, because the compile step is already over. Concatenating input into the template source destroys that phase separation — and with it, the entire guarantee.

**How defenders see it.** Template syntax in input logs is the tripwire: `{{`, `{%`, `${`, `#{`, `<%=` appearing in request parameters — especially in fields that get reflected into rendered pages. In the access log, the probe is visible once you decode it:

```
203.0.113.44 - - [10/Oct/2026:01:18:22 +0000] "GET /?name=%7B%7B7*7%7D%7D HTTP/1.1" 200 14
```

URL-decoded, that parameter is `{{7*7}}` — the arithmetic probe. Nobody's real name looks like that. A WAF rule on these is a tripwire, not a fix (encoding and engine variations bypass naive patterns). In code review: string concatenation into any `render`/`render_template_string`/equivalent call, user-controlled template names, "preview" features. Server-side: unexpected child processes or file reads from the web worker are the escalation signal.

### Worked example: the greeting demo

A toy template engine (stdlib Python, local only — the walkthrough runs it): `{{ expression }}` in the template source is evaluated. The vulnerable endpoint concatenates the `name` parameter into the template source; the fixed endpoint treats input as data.

Baseline: `?name=alice` → `Hello, alice!`. Probe: `?name={{7*7}}` → `Hello, 49!`. The `49` in the response *is* the vulnerability: your input was compiled and executed by the server's template engine. The fixed endpoint (`/fixed`) renders the same input inert: `Hello, {{7*7}}!` — data, not code.

The fix, stated generally: **never build template source from user input.** Pass input as variables to a fixed template; if users must customize appearance, give them a logic-less template language (Mustache-style: variables and sections only, no expressions) or a strict allow-list of fields. Then re-test: the arithmetic probe renders inert.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-ssti.log`. Clean environment: stock Python 3.12, curl 8.5.0, loopback only, 2026-10-10. The toy engine (`eval` on `{{ }}`) stands in for real engines — deliberately the worst practice, labeled as such, so the mechanism is unmistakable. Real engine payloads are PortSwigger-lab material (no Docker on this machine — see gaps).

1. **Start the app.** Save the `app.py` from this lesson's companion and run it on port 8333. Confirm the baseline: `curl -s "localhost:8333/?name=alice"` → `Hello, alice!`.
2. **Prove evaluation.** `curl -s "localhost:8333/?name=%7B%7B7*7%7D%7D"` → `Hello, 49!`. The arithmetic executed server-side. Write down the request/response pair — this is the finding. (The `%7B%7B` is URL-encoded `{{`; the lesson names the encoding so the reader isn't mystified.)
3. **Understand what you just proved.** You proved *evaluation*, not RCE. On a real engine, this is the detection payload — the safe, unmistakable signal. Say out loud what the next rung would be (attribute access toward the object model) without running it here; the escalation ladder is lab material.
4. **Verify the fix.** `curl -s "localhost:8333/fixed?name=%7B%7B7*7%7D%7D"` → `Hello, {{7*7}}!`. Same input, inert output: the fixed endpoint never lets input reach the template source.
5. **Read the defender view.** The companion logs each request's raw `name` value. Find your `{{7*7}}` probe in the log. Write the detection rule: alert on template delimiters (`{{`, `{%`, `${`, `#{`, `<%=`) in input parameters — and write next to it, in the same note, why it is a tripwire and not a fix.

No step above is marked "not run by us" — the evaluation proof and the fix verification ran locally. Engine-specific escalation payloads are PortSwigger-lab material by design (concepts taught here, hands-on there).

## 5. On your own

**Task:** Pick one authorized target you have not touched in this lesson — a PortSwigger Academy SSTI lab (start with "Basic server-side template injection"). First *fingerprint the engine*: the Academy's methodology is to try the arithmetic probes for each engine family (`{{7*7}}`, `${7*7}`, `<%= 7*7 %>`, `#{7*7}`) and see which evaluates. Then follow that engine's documented path exactly one rung: from evaluation to reading a server-side value (e.g., an object attribute the lab exposes). Stop there — the lab's own questions tell you when you've proved the class.

**Success test:** A one-page report: the fingerprinting probes tried and which evaluated (engine identified), the exact request proving evaluation, the server-side value read, the fix stated architecturally (input never reaches template source), and the defender detection (which log, which delimiters). If no probe evaluates, document the negative result and what it tells you about the template handling.

## 6. Where it goes wrong

- **"We escape the input, so we're safe."** Output-escaping protects the *browser* (XSS). SSTI happens *before* output, on the server, during template compilation. Different layer, different fix.
- **Blacklisting `{{`.** Engines have multiple syntaxes (`${}`, `#{`, `<%= %>`, `*{}`), and string-concatenation tricks can smuggle delimiters past naive filters. The fix is architectural (no input in template source), not a filter.
- **Trusting the sandbox.** Sandbox escapes are a genre, not an accident. If your security depends on the sandbox holding, you have already lost — treat sandboxed evaluation of untrusted input as vulnerable by design.
- **"Preview" features.** "See how your template looks" is the most common real-world SSTI shape: the feature *requires* rendering user input as a template. Redesign the feature (fixed templates + variable pickers) instead of securing the unsecurable.
- **Confusing SSTI with XSS.** `{{7*7}}` rendering as `49` in *your browser's* view-source is SSTI only if the *server* evaluated it. Check where the evaluation happened before naming the class.
- **Running escalation payloads outside labs.** The RCE rungs are real. They belong in PortSwigger's labs and authorized scope — never in curiosity-driven testing.

## 7. Read the source

Primary documents first:

- **PortSwigger Web Security Academy — Server-side template injection** (portswigger.net/web-security/server-side-template-injection — verified 2026-10-10): the canonical treatment — detection methodology, engine fingerprinting, the escalation ladder. *Read* fully, then do the labs.
- **CWE-94** (cwe.mitre.org/data/definitions/94.html — verified 2026-10-10): Improper Control of Generation of Code ("Code Injection") — the weakness family SSTI belongs to. *Skim*; cite the ID.

Then at most three free resources:

1. **PortSwigger SSTI labs** (portswigger.net/web-security — free): engine-specific labs from detection through documented exploitation, hosted and authorized.
2. **PortSwigger's SSTI decision tree** (in the Academy topic above — free): which probe for which engine; print it and keep it next to you in labs.
3. **`b-xss`** (this guidebook): the data-vs-code distinction on the client side — the same confusion, one layer down the stack.

## 8. Check yourself

1. Explain the difference between `render("Hello, " + name + "!")` and `render("Hello, {{name}}!", name=name)` — which one is vulnerable and why, in terms of template *source* vs *data*.
2. Your probe `{{7*7}}` returns `49`. Explain what you have proved and what you have *not* proved, and why the distinction matters for the report's impact section.
3. A developer "fixes" SSTI by stripping the substring `{{` from input. Explain two bypasses (different engine syntax; smuggled delimiters) and state the architectural fix.
4. Explain why a sandbox around template evaluation is not a sufficient fix, using the history of sandbox escapes as your evidence.
5. You see `${7*7}` evaluate but `{{7*7}}` render inert. Name what you've learned (engine family hint) and your next probe.

## 9. Prove it

**Artifact:** the one-page report from "On your own": fingerprinting probes, the evaluation proof, the server-side value read, the architectural fix, the defender detection.

**This lesson takes you to Level 3 (Apply).** You can honestly claim: you can detect SSTI with the arithmetic probe, fingerprint the engine family, prove server-side evaluation on an authorized target, and state the architectural fix. You cannot yet claim: exploit development against template engines — the escalation ladder past detection is lab-bounded practice, and real-engine RCE is out of scope for this lesson by design.

## 10. Leads to

- `b-xxe` — the same "server processes attacker-shaped input" shape through XML parsers.
- `b-deserialization` — untrusted input reaching a dangerous interpreter, one layer deeper (object construction).
- `b-xss` (re-read) — the data-vs-code confusion on the client side; compare which layer each class executes in.
- Map refs: **CWE-94** · **PortSwigger SSTI** (detection methodology + labs).
