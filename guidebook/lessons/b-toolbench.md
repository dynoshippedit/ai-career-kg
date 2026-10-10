---
lesson_id: b-toolbench
slug: toolbench
stage: B
level: 2
prerequisites: [b-authorization-scope, b-methodology, a-http-depth, a-linux-cli]
roles: [pentester]
map_refs: []
test_date: 2026-10-10
description: "The toolbench: fifteen tool phases in activation order — for each, the one question it answers, the free tool that answers it, and what it cannot tell you. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · loopback only; nmap/Semgrep/Chromium steps re-ran 2026-10-10; remaining tools marked not run by us with reader procedures"
---
# The toolbench: fifteen phases, one question each


**Map refs:** the fifteen tool phases in activation order (owner's tool catalog); feeds every `b-…` vulnerability lesson.

---

## 1. Where this shows up

Every engagement in the methodology lesson runs on tools, and every tool in this lesson exists to answer exactly one question. Beginners collect tools; professionals collect answers. The difference shows up in the report: "I ran a scan and it found nothing" is a tool report, while "I asked which names resolve, got four candidates, and confirmed two are in scope" is an answer report. This lesson teaches the bench the way the field's working catalog organizes it — fifteen phases in activation order, each gated by the authorization lesson — so that when a later lesson says "phase 4," you know exactly which question you are answering and which tool answers it. The catalog this lesson follows is the owner's own `Web-Security-Tool-Catalog.md`: use its table and its activation order; its "Paid layer" table is ignored throughout the guidebook because the guidebook teaches the free path.

## 2. Before you start

- `b-authorization-scope` is complete — every tool below is gated by written scope. A tool does not authorize anything for you.
- `b-methodology` is complete — you know which PTES phase each tool phase serves.
- You can read HTTP and operate a Linux shell. You do not need any of these tools installed yet: the lesson teaches them as answers to questions, never as an install list. Install a tool when it answers a question you actually have.

## 3. How it works

The organizing idea: **each phase answers one question, and the tool is the instrument for that question.** Learn the question first; the tool's flags are documentation you read when you need them. For each phase: the question, the free tool that answers it, how to read its output, and what it cannot tell you — because every tool has a blind spot, and the blind spot is where false findings are born.

**Phase 1 — Scope and records.** *Question: what is allowed, what is excluded, which accounts do I own, and what have I already tried?* Tools: Markdown notes (Obsidian or any editor) and Git. Read the output as the engagement's memory: the scope card, the account list, the dated log of attempts. What it cannot tell you: whether scope changed since you wrote it — recheck the policy before each session. And a records rule that is also a safety rule: keep confidential notes (real customer data, real credentials) out of public repos. Your notes are an artifact; treat them like one.

**Phase 2 — Interception proxy.** *Question: what did this request send, and what changed when I replayed one field?* Tools: Burp Community (one primary proxy — pick one and learn it deeply), Caido, mitmproxy. Read the output as the ground truth of client-server conversation: the raw request, the raw response, the diff between two replays that differ in one field. What it cannot tell you: what the server-side check is. The proxy shows traffic; it cannot find logic flaws — a request that looks innocent in the proxy can still violate a business rule, and a request that looks suspicious can be perfectly authorized.

**Phase 3 — Session isolation.** *Question: which identity sent this request?* Tools: Firefox profiles, Multi-Account Containers, PwnFox. Read the output as identity discipline: this tab is tester01, that tab is tester02, and you know because you confirmed the cookie or token value — never the tab label. What it cannot tell you: whether the token actually belongs to that identity. Confirm the credential value; a labeled tab is a claim, not evidence. Profiles are enough; you do not need exotic tooling for the discipline that matters.

**Phase 4 — Authorization comparison.** *Question: did account A receive account B's object?* Tools: Autorize, AuthMatrix, Burp Comparer. Read the output as a candidate list: these requests returned different statuses or bodies across the two identities. What it cannot tell you: what the authorization *means*. The output still needs a manual read — a 200 for both accounts can be correct (a public resource) or a finding (a private one); only you, knowing the application's intent, can tell. Run the two-account comparison by hand first (the `b-idor` walkthrough); automate it after the manual version works.

**Phase 5 — Asset discovery.** *Question: which names resolve, and which of those are live web apps?* Tools: subfinder, dnsx, httpx, amass; Shodan or Censys for internet-wide data. Read the output as candidates: these names exist, these respond on web ports. What it cannot tell you: permission. Every result is a candidate only — hard rule 1 in tool form. Nothing in a discovery list is in scope by itself; each name goes through the scope check before you touch it.

**Phase 6 — Crawling and history.** *Question: which paths did the app or the archive already expose?* Tools: katana, gau, waybackurls, browser DevTools. Read the output as a map of what is already known: endpoints the crawler found, URLs the archives recorded. What it cannot tell you: current scope. Recheck each path against scope before touching it — an archived admin URL from 2019 is still a candidate, not permission.

**Phase 7 — Content and parameters.** *Question: is this one missing path or parameter real?* Tools: ffuf, SecLists wordlists, Arjun. Read the output as a single hypothesis tested: this path exists (200, and the body differs from the not-found baseline) or it does not. What it cannot tell you: whether it is vulnerable. Fuzzing finds *existence*; vulnerability is a separate question answered by later phases. Discipline: one hypothesis, one host, at a rate the program allows. A fuzzing run is the easiest way to accidentally exceed scope or rate limits — the RoE's rate cap applies here first.

**Phase 8 — Data handling.** *Question: what is in this output, deduped, with the field I care about kept?* Tools: jq, yq, ripgrep, anew, unfurl. Read the output as structured evidence: the fields you need, the duplicates removed, the noise stripped. What it cannot tell you: what the data *means*. These tools structure; they never interpret. `jq` extracting every `account_id` from a response is not a finding — it is the material a finding is built from.

**Phase 9 — API contracts.** *Question: what does the spec say, what changed, and what fails on a local install?* Tools: Bruno or Postman, oasdiff, Schemathesis. Read the output as the contract's promises versus reality: the spec says these endpoints exist; the diff says these changed; the local install says these actually fail. What it cannot tell you: business permissions. Specs do not know authorization rules — an endpoint can match its OpenAPI contract perfectly and still serve one user's data to another.

**Phase 10 — Tokens and callbacks.** *Question: is this token a JWT, what does this value decode to, did a permitted callback fire?* Tools: JWT Editor or jwt_tool, CyberChef, Burp Collaborator or interactsh. Read the output as identification: the token's format (hard rule 3 — a bearer token is not a JWT until the format is identified), the decoded claims, the callback log. What it cannot tell you: that a fired callback is a vulnerability. An out-of-band ping proves the server *can* reach you; whether that reachability is a flaw depends on what was reachable and why. And callbacks go only to infrastructure you own, inside scope — a collaborator ping to an out-of-scope host is still touching it.

**Phase 11 — Source analysis.** *Question: where is the permission check, and does this change remove it?* Tools: VS Code, Git, Semgrep, CodeQL. Read the output as code facts: the check lives here, this diff touches it. What it cannot tell you: runtime exploitability. Static findings still need a live proof on an authorized target — a missing check in code you cannot reach is a code-review note, not a vulnerability report. One licensing note, stated without prices: CodeQL on private repositories carries conditions — read them before you rely on it in a workflow.

**Phase 12 — Dependencies and secrets.** *Question: is a dependency already vulnerable, or is a secret present?* Tools: Trivy, Gitleaks, TruffleHog. Read the output as leads: this dependency has a known CVE; this string looks like a secret. What it cannot tell you: whether the secret *works* — because verification stays off (hard rule 5) and you never use a found credential (hard rule 4). A secret's presence is reported as exposure; its validity is never your experiment to run. And a dependency match is not a new CVE by itself (hard rule 2): it becomes a finding only when you confirm reachability on the authorized target, by hand (hard rule 6).

**Phase 13 — Local environment.** *Question: can I pin the version, reset dummy data, and watch the check run?* Tools: Docker or Compose, a debugger, a local test database. Read the output as control: the exact version running, the data reset to a known state, the check observed in the act. What it cannot tell you: production behavior. Local is a model, and models differ — a fix verified locally is verified against the model, which is why the report says where it was tested.

**Phase 14 — Reproduction.** *Question: can someone else rerun it, and does the fix block the forbidden call while legitimate access still works?* Tools: curl, Playwright, the project's own tests. Read the output as the defender's experience: the exact commands, the before/after behavior, the legitimate flow still passing. What it cannot tell you: the absence of other flaws. A reproduced fix is one closed hole, not a clean bill of health — say which hole, and no more.

**Phase 15 — Evidence.** *Question: can I show the request, the other user's dummy data, and the timeline?* Tools: Flameshot, Markdown, Dradis. Read the output as the report's exhibits: the request/response pair, the timestamps, the narrative order. What it cannot tell you: validity. Evidence presents the finding; the finding still has to be real. Beautiful screenshots of an unconfirmed scanner match are still unconfirmed.

**Activation order** — the order you actually turn these on, from the catalog:

1. Browser profiles, Burp Community, notes, screenshots. (Phases 1, 2, 3, 15 — the minimum viable engagement.)
2. Git, Docker, VS Code, curl — once a product and a disclosure policy are chosen. (Phases 1, 11, 13, 14.)
3. Autorize or AuthMatrix — after the two-account comparison works by hand. (Phase 4.)
4. Semgrep or CodeQL — when one source file raises a specific question. (Phase 11.)
5. Playwright or the project's tests — to replay the finding and check the fix. (Phase 14.)
6. A paid proxy — only when unsaved projects start costing findings. The guidebook teaches the free path throughout; this stays a footnote.

**What stays off this path, and why.** sqlmap, Nikto, Nessus, Hydra, and a second fuzzer are not banned by category — they are simply not on this path. The reason is the path's first question: *can one signed-in user read another user's object?* None of those tools answers that question first. sqlmap automates a question you have not asked yet; Nikto and Nessus enumerate known issues (hard rule 2 territory); Hydra attacks credentials (outside the authorization discipline entirely); a second fuzzer duplicates phase 7 without new questions. When a later lesson's question genuinely needs one of them, the lesson will say so. Until then, the bench stays lean: every tool present earns its place by answering a question you have.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-toolbench.log`. Clean environment: curl 8.5.0, jq 1.7, ripgrep 14.1.0, ss (iproute2 6.1.0), git 2.43.0, Python 3.12.3; loopback only; fictional Harborlight Books scope; 2026-10-09. Tools not installed here are marked **not run by us** with the exact reader procedure.

1. **Phase 1 — records.** Write engagement notes (scope in/out, accounts owned, dated log) and commit them to a local git repo. Observed: `d1b8fee engagement notes: scope + accounts`. The commit history is the records trail.
2. **Phases 2/14 — read what the wire says.** Start a local demo server on 127.0.0.1:8471; `curl -sI` the endpoint. Observed: `HTTP/1.0 200 OK`, `Server: SimpleHTTP/0.6 Python/3.12.3`, `Content-type: application/json`, `Content-Length: 48`. Headers read cold, the way every later lesson starts.
3. **Phase 8 — structure the data.** Pipe the curl body through `jq '{user, points}'`. Observed: `{"user": "tester01", "points": 1250}`. The fields you care about, kept; the rest, dropped.
4. **Phase 8 — search the output.** Against a labeled fake access log: `rg -c " 200"` → `2`; `rg "account_id=1043"` surfaced the cross-account line. This is the shape of log triage you will do for real in Stage C.
5. **Phases 5/7 — sanity-check the target.** `ss -tlnp` showed `127.0.0.1:8471 LISTEN` on the expected python3 process. Before any testing: the thing listening is the thing you meant to test, bound to loopback.
6. **Phase 10 — decode, don't guess.** Percent-decoded `account_id%3D1043%26tier%3Dgold` → `account_id=1043&tier=gold` with Python's urllib. Values are identified by decoding, never by squinting (hard rule 3's spirit applied to every encoded value).
7. **Not run by us — the rest of the bench.** ffuf, subfinder/dnsx/httpx/amass, katana/gau/waybackurls, Burp Community/Caido/mitmproxy, Autorize/AuthMatrix, JWT Editor/jwt_tool, CodeQL, Trivy/Gitleaks, Docker, Flameshot/Dradis: not installed on this machine or need the reader's own lab. (Update 2026-10-10: nmap 7.94SVN, Semgrep 1.180.0, and Playwright headless Chromium were installed and ran for real — see the re-run entry in `runs/b-toolbench.log`.) The transcript gives the exact reader procedure for each — the install, the first command, and what to read in the output. Kill the demo server and verify it is gone (transcript records a self-match correction on the kill command, logged honestly).

## 5. On your own

**Task:** Against one local target from `b-practice-targets` (DVWA at low difficulty is the natural first bench), build a toolbench log: for each phase you actually use, one answered research question, the exact command, and the evidence it produced. Minimum: phases 1, 2, 7, 8, 14 — scope notes, one intercepted request, one existence hypothesis tested, one structured extraction, one reproducible curl command.

**Success test:** A toolbench log where every entry is shaped "question → command → evidence → what it can't tell me," and at least one entry where the tool's answer was *negative* (the path does not exist; the parameter is not reflected) — recorded as useful negative evidence, not as a failed step. If every entry is a positive, you stopped asking questions too early.

## 6. Where it goes wrong

- **Install-list thinking.** Twenty tools installed, none learned. The activation order exists to prevent this: each tool arrives answering a question you already have.
- **Scanner match as finding.** Phase 7 and 12 outputs are candidates (hard rules 2 and 6). The tool proposes; you confirm by hand, on the authorized target, with a reproduceable proof.
- **Tool output as understanding.** "The scanner says it's vulnerable" is not a mechanism. If you cannot explain *why* the output means what you claim, you do not have a finding — you have a printout.
- **Wrong-phase tools.** Running ffuf before reading the application, or Semgrep before you have a question about a specific file. The phases are ordered because each one's output feeds the next one's question.
- **Paid-tool envy.** Believing the free proxy is the reason findings are missed. Findings are missed for want of methodology and authorization discipline, not for want of a paid scanner. The paid tier enters only when unsaved projects cost findings.
- **Notes in public.** Engagement notes with real hostnames, real credentials, or real customer data pushed to a public repo. Phase 1's records rule: confidential notes stay out of public repos, always.
- **Trusting the tab.** Testing "as tester02" in a tab that is actually still tester01's session. Phase 3's discipline: confirm the cookie or token value, never the tab label.
- **Forgetting the rate.** A fuzzing run at default speed against a target whose RoE caps you at 10 requests/second. The RoE's numbers apply to automation first, because automation is what exceeds them.

## 7. Read the source

Primary documents first — the tool projects themselves (all fetched in-session, 2026-10-09):

- **nmap.org** — *read* the front page's "what it does" and the documentation index; nmap is phase 5's deep instrument (service/version detection), and its docs are the honest treatment of what a scan can and cannot prove.
- **ffuf** (github.com/ffuf/ffuf) — *read* the README's usage and examples; the project's own words on recursion, filtering, and rate control are phase 7's operating manual.
- **jq manual** (jqlang.github.io/jq/manual) — *read* the tutorial section; *use* it as the reference every time phase 8 needs a new filter. This is the one tool document worth reading end to end early.
- **ProjectDiscovery katana** (github.com/projectdiscovery/katana) — *skim* the README for crawl modes; phase 6's instrument, and the README is explicit about scope-respecting options.
- **OWASP Amass** (github.com/owasp-amass/amass) — *skim* the README's enumeration techniques; phase 5's other deep instrument. Note its passive emphasis — the design respects hard rule 1 structurally.
- **Trivy** (github.com/aquasecurity/trivy) and **Gitleaks** (github.com/gitleaks/gitleaks) — *read* each README's "what it finds" section; phase 12's pair, and both are explicit that a match is a lead (Gitleaks' verification-off posture matches hard rule 5 by design).

Then at most three free resources:

1. **The owner's tool catalog** (`Web-Security-Tool-Catalog.md` — the table and activation order this lesson follows) — free; the one-page version of this lesson to keep open during engagements.
2. **PortSwigger Web Security Academy** (portswigger.net/web-security) — free; every phase gets its practice target here, each lab its own authorized scope.
3. **OWASP Cheat Sheet Series** (cheatsheetseries.owasp.org) — free; the fix side of every finding your bench produces.

## 8. Check yourself

1. Your proxy shows a request returning another user's data with `200 OK`, and Autorize flags the same request as "different response across users." Explain what the tool has established, what it has *not* established, and the one manual step that turns the flag into a finding.
2. ffuf reports a `200` on `/admin-backup`. Explain why this is an existence result rather than a vulnerability, and name the two phases whose questions must be answered before it becomes a finding.
3. Gitleaks flags a string that looks like an AWS key in a repository you are authorized to test. Explain exactly what hard rules 4 and 5 require you to do and not do, and what your report may honestly claim about the finding.
4. Explain why sqlmap is not on this path even though SQL injection is one of the first vulnerability classes taught — and describe the situation in which reaching for it would be methodologically sound.
5. You have two browser tabs open, one per test account, and your IDOR test "works" — account A's tab sees account B's data. Explain the phase-3 error that could make this entire result invalid, and how you check.

## 9. Prove it

**Artifact:** the toolbench log from "On your own": one answered research question per phase used (minimum phases 1, 2, 7, 8, 14), each with the exact command, the evidence produced, and the "what it can't tell me" line. The log is the artifact because the log *is* the bench in use.

**Honest claim:** "I can operate each bench phase's tool to answer its question on a prepared target, read the output correctly, and state what the output cannot tell me."
**Can't claim yet:** "I can find vulnerabilities end to end" — chaining the phases across a full finding, from scope to report, is what the vulnerability lessons plus `b-methodology` build toward.

## 10. Leads to

- **`b-practice-targets`** — the local targets where the full bench gets its workout: DVWA, Juice Shop, WebGoat, crAPI, DVGA, each on its own localhost port.
- **The `b-sqli`, `b-xss`, `b-…` vulnerability lessons** — each one names the bench phases it uses; re-read this lesson's phase table before each one.
- **`b-methodology`** (back-link) — the engagement frame the bench executes; **`b-authorization-scope`** (back-link) — the gate every phase operates inside.
- Map refs: fifteen tool phases in activation order (owner's catalog); feeds **CISSP 5.4** (via the authorization lessons, Stage E).
