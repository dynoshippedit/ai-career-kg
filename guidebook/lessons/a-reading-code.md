---
lesson_id: a-reading-code
slug: reading-code
stage: A
level: 3
prerequisites: [a-http-depth, a-python-security]
roles: [pentester, appsec]
map_refs: []
test_date: 2026-10-09
description: "Reading code through a vulnerability: tracing untrusted input from a JavaScript form to a SQL query — source, path, sink — with the injection located by reading. A free lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · labeled teaching snippets, local string-trace only, nothing executed against a database · third depth pass 2026-10-10 (prereq chain fixed: b-sqli removed — the lesson teaches the injection mechanism itself and leads to b-sqli; check-yourself Q1/Q3 rewritten to explain/predict)"
---
# Reading code through a vulnerability


**Map refs:** Stage A foundation; the reading half of `a-python-security`; direct prerequisite for every Stage B web-vulnerability lesson.

---

## 1. Where this shows up

Every vulnerability you will ever find is a story about input: where it enters, what touches it, and where it lands. Source code is where that story is written down — and the ability to *read* it, following one value from the browser to the database, is what separates "ran a scanner" from "understood the flaw." Scanners flag candidates; readers confirm them. In bug bounty work, the disclosed reports worth studying all read like code traces: "the `user` parameter flows from the route handler into this query builder unescaped." This lesson teaches exactly that move, in the two languages web vulnerabilities live in: enough JavaScript to follow client-side behavior, and enough SQL to see how a query is built and where user input enters it. You are not learning to write applications. You are learning to *interrogate* them.

## 2. Before you start

- The read-first discipline from `a-python-security`: imports first, entry point second, outward into functions.
- Enough HTTP to know what a form submission becomes on the wire (`a-http-depth`).
- A text editor and Python 3 (for the SQL half — SQLite ships with Python, no database to install).
- The two snippet files from the walkthrough are yours to keep: a 20-line login form (`login.html`) and a query builder (`querybuilder.py`).

## 3. How it works

Code reading is not code writing done slowly. Writing asks "what should this do"; reading asks "what does this *actually* do to my input." The technique is always the same, in any language: **find where untrusted input enters, then follow it** — through assignments, function calls, string operations — until it reaches something that *acts* on it (a query, a shell, a page render). That endpoint is the sink; the entry is the source; everything between is the path. A vulnerability is a path from source to sink with no adequate check in between. Hold that frame and unfamiliar code stops being a wall of text and becomes a map with a route highlighted.

**Enough JavaScript to follow a form.** You need surprisingly little. `document.getElementById("user").value` reads what the user typed — that is a *source*, and the walkthrough's snippet labels it (A). (`document` is the DOM — the Document Object Model, the browser's live representation of the page, the thing JavaScript reads and writes.) `addEventListener("submit", ...)` runs code when the form submits; `e.preventDefault()` stops the browser's default submission so the script can take over. `fetch("/api/login", {method: "POST", body: JSON.stringify({user, pw})})` sends the values to the server — a *trust boundary crossed* (C). `await` pauses until the response arrives; `document.body.innerHTML = ...` writes server data into the page — a potential *sink* (E). That is the whole vocabulary the walkthrough needs: read input, handle an event, send it, render the answer. When you read real client code later, you will meet frameworks and bundlers (tools that package many source files into the few files the browser loads — which is why production client code looks nothing like this snippet), but the question never changes: where does input enter, and where does it go?

**The client is not a security boundary.** The walkthrough's form does zero validation before sending (D) — and that is *fine*, because client-side validation is user experience, not security. Anything the browser sends can be re-sent by curl with different values. This is the single most important thing JavaScript reading teaches you: the client is the attacker's machine. Every check that matters must also exist on the server. When you read client code and find the "validation," your next question is always "and where is it enforced server-side?"

**Enough SQL to read a query.** A query has clauses, and you read them in execution order, not written order: `FROM users` (which table), `WHERE name = 'alice' AND pw = 's3cret'` (which rows — the filter), `SELECT *` (which columns, evaluated last). The `WHERE` clause is where input lands and therefore where you look. In the walkthrough's vulnerable builder, the query is assembled by *string concatenation*: `"SELECT ... '" + user + "' ..."`. The quotes are part of the query's *syntax*, and the input is dropped between them — so input containing a quote character doesn't stay data; it becomes *structure*. That is the entire mechanism of SQL injection, visible in one line: code and data share a channel, and the boundary between them is a quote character the attacker controls. (An attacker who controls the quote can append `UNION SELECT ...` — `UNION` glues two queries' results together, so it smuggles a second query's output into the first — and read other tables through your query.)

**Placeholders keep the boundary.** The safe builder returns `("SELECT ... WHERE name = ? AND pw = ?", (user, pw))` — the query text and the values travel *separately* to the database, which never confuses them. The mechanism that makes this airtight: the database *parses* the query text once, with the `?` marks as holes, and *then* plugs the values in. Because parsing is already finished, a value can never be reinterpreted as syntax — there is no second parse for the attacker to influence. Note what the walkthrough proved: with hostile input `' OR '1'='1`, the vulnerable builder produced `WHERE name = '' OR '1'='1' AND pw = 'x'` (the input rewrote the logic), while the safe builder kept the hostile string as a single inert value. Two builders, same input, different universes — and the difference is visible in the source before anything runs.

**Reading order for unfamiliar code.** Imports (capabilities) → entry point (where execution starts) → the request path (follow one input end to end) → the sinks (queries, renders, shell calls — read each one's inputs). Annotate as you go: mark every source with "input enters here," every sink with "this acts on it," and draw the path between. The walkthrough's (A)–(G) labels are training wheels for exactly this habit.

### Worked example: the full trace

The walkthrough's two files are one application split across the trust boundary. Follow `user` from keystroke to database:

1. **(A)** `document.getElementById("user").value` — the value leaves the input field and enters JavaScript. Source identified.
2. **(D)** `JSON.stringify({user, pw})` — packaged into the request body. No validation, no encoding — the client adds nothing.
3. **(C)** `fetch("/api/login", ...)` — crosses the network to the server. Trust boundary one.
4. **(F)** `"... name = '" + user + "' ..."` — the server concatenates the value into SQL text. Trust boundary two, and the fatal one: the value is now *part of the command*.
5. With benign input the query filters correctly; with `' OR '1'='1` the query's *logic* changes — proven by the transcript, not asserted.

Three hops, zero checks. Every web vulnerability you will study in Stage B is this shape with different syntax at (F): a shell command, an HTML page, a file path, a server-side request. Learn the shape once.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/a-reading-code.log`. Clean environment: Python 3.12.3, scratch dir `/tmp/codewalk`, 2026-10-09. Both snippets are labeled teaching files, fictional throughout.

1. **Inventory the files.** `ls -la` — two files, `login.html` (891 bytes) and `querybuilder.py` (566 bytes). Small enough to read whole; that is the point.
2. **Read the JavaScript entry point.** `grep -n "getElementById\|fetch\|JSON.stringify" login.html` — five lines locate every input source and the network crossing. Read those lines first, then the ten lines around them.
3. **Trace the benign input.** `python3 querybuilder.py alice s3cret` → `SELECT * FROM users WHERE name = 'alice' AND pw = 's3cret'`. Say aloud which characters came from the query template and which came from input.
4. **Trace the hostile input.** `python3 querybuilder.py "' OR '1'='1" x` → `WHERE name = '' OR '1'='1' AND pw = 'x'`. Point at the exact character where input stopped being data and became structure (the first `'`). This is the vulnerability, located by reading.
5. **Read the safe builder.** Same hostile input through `build_query_safe` → the query keeps its `?` placeholders and the hostile string travels as a tuple value. The fix is visible in the source: separation of code and data.
6. **Count the trust boundaries.** DOM → network → SQL string: three hops, zero checks. Write that sentence down — it is the report format in miniature.

## 5. On your own

**Task:** Take this fictional snippet (a search feature) and produce a written trace:

```python
def search(q):
    sql = "SELECT title, body FROM articles WHERE title LIKE '%" + q + "%'"
    return db.execute(sql)
```

(a) Mark the source, the sink, and the path between them. (b) Give one benign input and show the query it builds. (c) Give one hostile input (a single quote plus SQL syntax) and show the query it builds — then state in one sentence what the query now *does* that the author didn't intend. (d) Rewrite the function with placeholders.

**Success test:** Your trace names the exact character where input becomes structure; your hostile input is syntactically valid SQL, not hand-waving; your rewrite keeps the `LIKE '%...%'` behavior (hint: the `%` wildcards belong in the *value*, not the query text).

**Hints:** The `%` signs are part of the intended pattern match — concatenate them onto the value in Python, not into the SQL string.

## 6. Where it goes wrong

- **Reading the client and stopping.** Finding "no validation in the JS" is not a vulnerability — it's normal. The flaw, if any, is server-side. Client reading tells you what the server *expects*; it never tells you what the server *enforces*.
- **Assuming frameworks protect you.** ORMs (Object-Relational Mappers — libraries that translate between program objects and database rows so developers write less raw SQL; SQL is still generated underneath), templating engines, and frameworks have safe defaults *until you bypass them* — raw queries, `innerHTML`, string-built commands. When reading framework code, look for the escape hatches; that's where the bugs live.
- **Trusting comments.** Comments describe intent; code describes behavior. When they disagree, the code is the truth and the comment is the bug report.
- **Skimming the boring parts.** Input handling lives in validation helpers, middleware (code that runs between receiving a request and your handler — auth checks, parsing, logging, shared plumbing), and utility functions — the unglamorous code nobody reads. Read it anyway; that's where the missing check is.
- **Confusing "I see the bug" with "I proved it."** Reading locates the candidate; the walkthrough's query-printing *proves* the mechanism. In Stage B, the proof is a reproduction against a running target — reading gets you to the right ten lines, execution confirms them.
- **What the probe looks like in the logs.** This lesson's injection is visible in web access logs as URL-encoded quotes in parameters — `GET /search?q=%27%20OR%20%271%27%3D%271` — a burst of requests carrying `'`, `UNION`, or `--` in the query string is someone probing for SQLi. That token set is exactly what WAF rules alert on; learn to spot it and you can read an attacker's progress from the logs.

## 7. Read the source

Primary documents first:

- **The snippets themselves** — re-read them after the lesson; you will see more the second time. That improvement *is* the skill developing.
- **SQLite language reference** (sqlite.org/lang.html — lead, verify at build time) — the SQL dialect the labs use. *Read* the `SELECT` page's clause list; *skim* the expression syntax.

Then at most three free resources:

1. **javascript.info — The Modern JavaScript Tutorial** (javascript.info — verified 2026-10-09) — *read* Part 1 (the language) through functions; *skim* the Browser/DOM part for `getElementById`, events, and `fetch`. You need the reading vocabulary, not the writing fluency.
2. **SQLBolt** (sqlbolt.com — verified 2026-10-09) — interactive in-browser SQL lessons through joins. *Do* the exercises through lesson 6 — exactly the reading level Stage B's SQLi lesson assumes.
3. **PortSwigger Web Security Academy** (portswigger.net/web-security — verified 2026-10-09) — the lab environment where this lesson's traces become live reproductions in `b-sqli` and friends. Read-only source study now; hands-on there.

## 8. Check yourself

1. An attacker submits `admin'-- ` as the username to the walkthrough's vulnerable builder. Mark the exact character where the input stops being data and becomes structure, and explain what the database now *does* with the rest of the query that the author didn't intend.
2. The login form validates nothing client-side. Explain why that is *not* the vulnerability, and where the vulnerability actually is.
3. Your teammate says "the ORM handles it, we don't need to review the queries" — and you find `db.execute("SELECT * FROM users ORDER BY " + sort_param)` in the codebase. Explain why the ORM's protection doesn't cover this line, and name one other ORM escape hatch you'd grep for when reading unfamiliar code.
4. Trace `q = "x' UNION SELECT password FROM users -- "` through the On-your-own `search()` function. What does the final query do?
5. You find `element.innerHTML = location.hash.slice(1)` in client code. Mark source, sink, and path — and state what you'd check server-side (if anything).

## 9. Prove it

**Artifact:** A published code trace: take one open-source web application (Juice Shop's source is local and readable — `b-practice-targets` shows the setup), pick one request handler, and write up the full source→sink trace for one user-controlled parameter: the entry point, every function it passes through, the sink it reaches, and your verdict (safe / unsafe / needs-runtime-proof) with reasons. 300–500 words, file and line references.

**Honest claim:** "I can trace untrusted input through source I didn't write and say where it becomes dangerous — demonstrated on a published trace of a real handler."

**You cannot yet claim:** finding vulnerabilities in unfamiliar production code unaided — that needs the Stage B vulnerability classes (`b-sqli` onward) plus runtime confirmation. This lesson is the reading half; Stage B is the proving half.

## 10. Leads to

- `b-sqli` — the vulnerability class this lesson traced, now with live reproduction and the full attacker/defender frame.
- `b-xss` — the same source→sink shape with an HTML sink instead of a SQL one.
- `b-command-injection` — the same shape with a shell sink.
- `b-business-logic` — where reading alone isn't enough: the flaw is in the workflow, not the syntax.
