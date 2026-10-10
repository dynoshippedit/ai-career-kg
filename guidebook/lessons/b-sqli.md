# SQL injection: when your input becomes the query

**ID:** `b-sqli` · **Stage:** B (Practitioner) · **Level:** 3 (mechanism + live reproduction in three families + fix verification) · **Prerequisites:** `a-http-depth` (HTTP in depth), `a-git-github` (the evidence pipeline), B-AUTH (authorization discipline: you test only what you are allowed to touch), enough SQL to read a `SELECT` statement.

**Map refs:** OWASP Top 10:2025 A05 Injection · WSTG-INPV-05 · CWE-89

---

## 1. Where this shows up

SQL injection is the oldest injection class on the web and still one of the most damaging: it sits inside **OWASP Top 10:2025 A05 — Injection** and carries its own weakness ID, **CWE-89**. You will meet it in bug bounty programs (database access is high-impact by definition), in penetration-test reports, in code reviews where a query is built by concatenation, and — from the other side — in WAF alert queues and database slow-query logs. The lesson's real subject is bigger than SQL: the pattern "user input stops being data and becomes code" repeats in every injection class after this one, and SQLi is where you learn to see it.

## 2. Before you start

- You can read HTTP requests and responses cold (`a-http-depth`), including how query parameters travel.
- You can read a simple SQL `SELECT` — what the `WHERE` clause does, what `--` means as a comment.
- Your target is written down and authorizes your testing: your own local lab (this lesson's demo app), a PortSwigger Academy SQLi lab, DVWA's SQL Injection module, or a bounty program whose scope explicitly includes the asset. SQLi testing outside authorization is not research; re-read B-AUTH if this sentence surprised you.
- Tooling: curl is enough. An interception proxy (Burp Community) makes parameter tampering faster later.

## 3. How it works

A web application talks to its database by sending SQL strings. The dangerous pattern looks like this, in any language:

```
query = "SELECT * FROM products WHERE category = '" + user_input + "'"
```

The developer intended `user_input` to be **data** — a category name. But the database receives one flat string and parses the whole thing as **code**. If `user_input` is `Gifts`, the query is what the developer meant. If `user_input` is `Gifts' OR 1=1--`, the database sees:

```sql
SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1
```

The `--` comments out the rest of the line, and `OR 1=1` is always true, so the `WHERE` clause now matches every row. The input stopped being data and became code. That sentence is the entire vulnerability class. Everything else is elaboration: where the input enters, what the database does with the injected code, and what channel carries the answer back to you.

**Why it arises in real code.** String concatenation in query construction — the line above. It also arises in less obvious sinks where bind variables cannot be used: `ORDER BY` clauses, table and column names, `LIKE` patterns. And it arises in **second-order** form: input stored safely (parameterized `INSERT`), then later concatenated into a different query by a developer who wrongly treated stored data as trusted. First-order is "input becomes code now"; second-order is "input becomes code later."

**The three families — how each is found.** The finding technique depends on what the application shows you:

- **In-band (union / error-based).** The query's results or the database's errors come back in the response. Detection probe: a single quote `'`, then boolean pairs (`' OR 1=1--` vs `' OR 1=2--`) watching for response differences. UNION attacks require matching the original query's column count (`ORDER BY n` to find it, incrementing until the error) and compatible types; `NULL` placeholders fill columns you don't care about.
- **Blind.** No output in the response. Two channels: **boolean-based** — inject a true/false condition and infer one bit per request from a response difference (a row appears or doesn't); and **time-based** — inject a delay function (`SLEEP()` in MySQL, `pg_sleep()` in PostgreSQL, `WAITFOR DELAY` in MSSQL) and measure response latency. Slower, but fully exploitable: extract data one bit at a time.
- **Out-of-band (OAST).** The injected query triggers a DNS or HTTP interaction to infrastructure you control (e.g., Burp Collaborator). Powerful where blind is impractical; data can be exfiltrated inside the DNS lookup itself. DBMS-specific functions required.

Database differences matter at exploitation time, not at finding time. The comment syntax (`--` with trailing space in MySQL, `#` also works there), the delay function, whether stacked queries (`; second statement`) are allowed — these are fingerprinting details. Fingerprint first: which delay function works reveals the DBMS.

**How defenders see it.** In WAF logs, SQLi rules live in the ModSecurity CRS 942xxx family (`REQUEST-942-APPLICATION-ATTACK-SQLI.conf`; rule 942100 is the libinjection-based headline detector): matched rule IDs, the offending argument, anomaly scores. In database logs, repeated multi-second `SLEEP`/`pg_sleep`/`WAITFOR` queries from one client in the slow-query log are the signature of time-based blind probing; `information_schema` enumeration in the general query log is the signature of someone mapping the database. In application logs: repeated 500s from malformed quotes during the probing phase.

### Worked example: the catalog demo

A minimal catalog app (stdlib Python + sqlite3, local only — the walkthrough runs it). `GET /products?category=Gifts` builds the query by concatenation and returns matching products as JSON. Two tables: `products` (name, category, price) and `secrets` (owner, api_key) — the second table exists so the UNION step has something to reach for.

Baseline: `category=Gifts` returns the two gift products. Probe: `category=Gifts'` — the app returns `500` with a database error. That error is already information: the input reached the query parser. Boolean pair: `Gifts' OR 1=1-- ` returns all four products; `Gifts' OR 1=2-- ` returns only the two gifts. The difference proves the injected condition is evaluated. Column count: `Gifts' ORDER BY 1-- ` works, `ORDER BY 2-- ` works, `ORDER BY 3-- ` errors — two columns. UNION: `Gifts' UNION SELECT owner, api_key FROM secrets-- ` returns the secrets rows alongside the products. Each step is one fact, and the finding is the chain.

The fix, in the same app: replace concatenation with a parameterized query — the query string becomes a hard-coded constant and the category travels as a bound parameter. Re-run all four probes: quote returns zero rows (or a clean 400, no error text), both boolean conditions return identical results, the UNION returns identical results. The injected code is now inert data. Then the defense-in-depth notes: where bind variables can't go (table names, `ORDER BY` direction), allow-list validation maps input to a fixed set of legal values; escaping is strongly discouraged (database-specific, fragile); and the application DB account gets only the rights it needs — never DBA.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-sqli.log`. Clean environment: stock Python 3.12 (sqlite3 stdlib), curl 8.5.0, loopback only, 2026-10-09. The demo app stands in for the PortSwigger/DVWA/Juice Shop targets the reader uses (no Docker on this machine — see gaps).

1. **Start the vulnerable app.** Save the `app.py` from this lesson's companion (catalog with `products` and `secrets` tables, `/products?category=` built by concatenation) and run it on port 8323. Confirm the baseline: `curl 'localhost:8323/products?category=Gifts'` returns the two gift products as JSON.
2. **Probe with a quote.** `category=Gifts'` — observe the `500` and the database error text in the response. Write down what the error tells you: the input reached the SQL parser. (In production this error text would itself be a finding — information disclosure — but here it's the lab's way of confirming the sink.)
3. **Boolean pair.** `category=Gifts' OR 1=1--%20` vs `category=Gifts' OR 1=2--%20` (the `%20` is the trailing space `--` needs). Record the row counts: all four products vs two. The difference is the proof that your injected SQL is evaluated.
4. **Find the column count.** `category=Gifts' ORDER BY 1--%20` (works), `ORDER BY 2--%20` (works), `ORDER BY 3--%20` (500). Two columns. This is the mechanical step UNION attacks require.
5. **UNION extraction.** `category=Gifts' UNION SELECT owner, api_key FROM secrets--%20` — observe the secrets rows in the response. Read, don't dump: one row is enough to prove cross-table read. Stop here; you have a confirmed finding.
6. **Time-based blind.** The app registers a `sleeps(n)` SQL function (SQLite has no built-in delay; the registration is labeled in the companion). `category=x' AND sleeps(3)--%20` — measure the response time (~3s) versus `sleeps(0)` (~instant). This is the blind channel: one bit per request, no output needed.
7. **Apply the fix.** Patch the handler to use a parameterized query (`?` placeholder, category as a bound value). Restart the app.
8. **Verify the fix — four cases.** Re-run steps 2–5: quote returns no error (clean empty result or 400); both boolean conditions return identical results; the UNION returns identical results. Legitimate `category=Gifts` still returns its two products (a fix that breaks the app is not a fix).
9. **Read the defender view.** Open the app's request log: find your quote probe (500), the `UNION` and `information_schema`-shaped requests, and the repeated multi-second `sleeps` calls. Write down what rule you would write: alert on repeated 500s from quote characters in parameters, and on slow-query patterns from a single client.

No step above is marked "not run by us" — in-band, boolean-blind, time-blind, the UNION extraction, the fix, and all four verification cases ran locally.

## 5. On your own

**Task:** Pick one authorized target you have not touched in this lesson — a PortSwigger Academy SQLi lab (the "WHERE clause" retrieval lab is the closest match), DVWA's SQL Injection module, or Juice Shop's "Login Admin" challenge. Find the injection point using only the quote probe and the boolean pair (no scanner). Then determine which family it is: does the response carry query results (in-band), only a true/false difference (blind), or neither (OAST territory — stop and document why)?

**Success test:** A one-page report: the vulnerable parameter, the boolean-pair evidence (exact requests and the response difference), the family determination with reasoning, the fix (parameterized query or allow-list, stated as code-level remediation), and the defender detection (which log, which pattern). If you cannot determine the family with the quote and boolean pair alone, say so and name what you would try next — that honesty is the finding's boundary.

## 6. Where it goes wrong

- **Only testing the `WHERE` clause.** Injection lives in `ORDER BY`, `UPDATE` values, table names, JSON/XML-parsed input — everywhere a query is assembled. One tested parameter is not a tested application.
- **`OR 1=1` in a write query.** PortSwigger's warning is worth internalizing: if your injected condition reaches an `UPDATE` or `DELETE`, you can destroy data. On authorized targets, prefer read-only proofs (`UNION SELECT`, version strings) and know which queries your input feeds.
- **Escaping as the fix.** Database-specific, fragile, bypassable — OWASP strongly discourages it. Parameterize; allow-list where parameters can't reach.
- **"The ORM handles it."** ORMs parameterize normal queries, but raw-query methods (`.raw()`, string-built `where` clauses, HQL/JPQL concatenation) reintroduce injection. Audit every raw path — the ORM is a tool, not a guarantee.
- **Stored procedures as magic.** Only as safe as their implementation: dynamic SQL inside the procedure (`EXEC`, `sp_executesql` with concatenation) reintroduces the flaw. Audit the procedure body.
- **Second-order blindness.** The stored value looks safe because the `INSERT` was parameterized — then it gets concatenated into a later query. Treat stored data as untrusted at every query boundary.
- **Scanner match = confirmed finding.** A scanner's SQLi match is a candidate. Confirm by hand with the boolean pair before reporting — automated findings are confirmed by hand is a hard rule.

## 7. Read the source

Primary documents first:

- **PortSwigger Web Security Academy — SQL injection** (portswigger.net/web-security/sql-injection) — *read* fully; it is the canonical treatment (detection probes, UNION technique, blind families, second-order, prevention). *Skim* the lab list; *do* the labs after this lesson.
- **OWASP SQL Injection Prevention Cheat Sheet** (cheatsheetseries.owasp.org) — *read* the four defense options in order; *note* that escaping is "STRONGLY DISCOURAGED" and *read* the least-privilege section. This is the fix side, stated as checkpoints.
- **CWE-89** (cwe.mitre.org/data/definitions/89.html) — *skim* the weakness definition and its relationships; cite the ID in findings.

Then at most three free resources:

1. **PortSwigger Academy — SQL injection labs** (portswigger.net/web-security) — free, hosted, authorized; 18+ labs across every family in this lesson.
2. **OWASP Juice Shop** (owasp.org/www-project-juice-shop) — free; run locally via Docker: "Login Admin" (bypass), "User Credentials" (UNION retrieval), "Database Schema" (enumeration).
3. **DVWA — SQL Injection modules** (github.com/digininja/DVWA) — free; run locally via Docker: the Low→High difficulty ladder shows the naive filters, and Impossible shows the parameterized fix.

## 8. Check yourself

1. Explain, in terms of code versus data, why a parameterized query defeats SQL injection even when the attacker controls the entire parameter value.
2. An endpoint returns identical responses for `' OR 1=1--` and `' OR 1=2--`, but the first takes 50ms and the second takes 5 seconds when you inject a delay function into the true branch only. Explain which family this is and what the timing difference proves.
3. Predict what a defender sees in the database slow-query log during a time-based blind attack, and explain why that pattern is more useful than a WAF signature for this family.
4. A developer fixes an `ORDER BY` injection by escaping quotes in the sort parameter. Explain why this fails and give the two correct options for that sink.
5. You find that input is stored via a parameterized `INSERT` but later rendered into a report query built by concatenation. Explain why the application is still vulnerable and what the developer's mistake was.

## 9. Prove it

**Artifact:** the one-page report from "On your own" (or the walkthrough evidence chain): vulnerable parameter, boolean-pair requests and the response difference, family determination, code-level remediation, defender detection.

**Honest claim:** "I can find SQL injection with manual probes, determine which family it belongs to, demonstrate it with a minimal read-only proof, and verify the parameterized fix."
**Can't claim yet:** "I can exploit blind SQLi at scale" — boolean-extraction tooling and OAST exfiltration are practiced in the PortSwigger labs, not claimed from this lesson.

## 10. Leads to

- `b-command-injection` — the same input-becomes-code pattern one layer down, in the operating system.
- `b-xss` (second wave) — input-becomes-code in the victim's browser; compare the three injection contexts.
- B-DEF (defensive basics) — sit on the other side: write the WAF/slow-query detection for your own attack traffic.
- B-BOUNTY (bug bounty mechanics) — this lesson's report format is the dry run for a real submission.
- Map refs: **OWASP Top 10:2025 A05**, **WSTG-INPV-05**, **CWE-89**.
