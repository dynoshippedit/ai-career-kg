# Content-depth audit — Stage B (21 lessons)

Auditor: subagent ac08c7a7 · 2026-10-10
Scope: `guidebook/lessons/b-*.md` listed in the task. Each lesson read fully.
Standard: brief SECURITY_GUIDEBOOK_BRIEF-2.md §1 (L1 Recognize / L2 Operate / L3 Apply / L4 Extend), §6 (lesson spec), §7 (evidence / safety / voice).
Rule applied: PAD-FREE — never flagged for length alone; 1,200–2,500 words is a sanity check, not a target.
Verdicts: SOLID (deep enough at stated level) / DEEPEN (genuinely thin — specific missing substance named).

## Method

Every lesson was read end to end and checked for: (a) the ten §6 sections in order with real substance in
"How it works" and "Walkthrough"; (b) honest level badge vs delivered bar; (c) factual staleness
(dates, versions, renamed tools/URLs); (d) the safety frame (authorization, attack+detect+fix together,
local-only walkthroughs, honest "not run by us" markers).

## Verdicts

| lesson | words | level | verdict |
|---|---|---|---|
| b-api-abuse | 1958 | L3 | SOLID |
| b-authorization-scope | 2824 | L2 | SOLID |
| b-bug-bounty | 2448 | L3 | SOLID |
| b-business-logic | 2139 | L3 | SOLID |
| b-command-injection | 2097 | L3 | SOLID |
| b-csrf | 2475 | L3 | SOLID |
| b-deserialization | 1833 | L3 | SOLID |
| b-graphql | 1944 | L3 | SOLID |
| b-idor | 2112 | L3 | SOLID |
| b-jwt-oauth | 2290 | L3 | SOLID |
| b-methodology | 2984 | L2 | SOLID |
| b-practice-targets | 2329 | L2 | DEEPEN |
| b-race-conditions | 1850 | L3 | SOLID |
| b-security-headers | 2229 | L3 | SOLID |
| b-session-auth | 2291 | L3 | SOLID |
| b-sqli | 2385 | L3 | SOLID |
| b-ssrf | 2268 | L3 | SOLID |
| b-ssti | 1853 | L3 | SOLID |
| b-toolbench | 3355 | L2 | SOLID |
| b-xss | 2265 | L3 | SOLID |
| b-xxe | 1776 | L3 | SOLID |

## SOLID — why each stands

- **b-api-abuse / b-graphql / b-jwt-oauth / b-deserialization / b-ssti / b-xxe / b-command-injection / b-sqli / b-ssrf / b-xss / b-csrf / b-idor / b-race-conditions / b-business-logic / b-session-auth (L3, 15 lessons):** each teaches the mechanism from first principles, a worked example with the flaw's real-world "why it arises," a defender view, a walkthrough run for real on loopback with a transcript in `runs/`, attack+detect+fix together, and honest boundaries (e.g. b-ssti keeps engine-escalation lab-bounded; b-xxe states plainly what its toy parser does and doesn't do). None claims a higher level than delivered. Word counts 1776–2475; all complete at L3.
- **b-authorization-scope (L2, 2824) / b-methodology (L2, 2984):** no-command-line planning lessons; complete worked cases (RoE document, six-phase engagement plan), primary-source citations checked in-session. Deep for L2.
- **b-bug-bounty (L3, 2448):** report anatomy, triage lifecycle, failure modes — complete at its level; hands-on reporting is deliberately a dry run (safe by design).
- **b-toolbench (L3→L2, 3355):** fifteen phases each with question/tool/output-reading/blind-spot; nmap/Semgrep/Chromium re-run for real 2026-10-10, rest marked "not run by us" with reader procedures.
- **b-security-headers (L3, 2229):** six controls with what-each-buys + browser-enforcement re-runs 2026-10-10. Note: the HSTS/MIME/clickjacking browser re-runs from another worker are present in the copy read; no duplication was added.
- **b-xxe (L3, 1776, shortest):** thin-looking by count but complete by substance — the honest statement that `xml.etree` refuses external entities *is* the lesson's strength; the dangerous behavior is named, sourced (OWASP XML Security Cheat Sheet), and lab-bounded in PortSwigger's labs. Padding it would weaken it.
- **b-ssti (L3, 1853):** same honest-boundary structure; the escalation ladder stays lab-bounded per the brief's safety line.

## DEEPEN — the one lesson, with the specific gap

- **b-practice-targets (L2, 2329) — DEEPENED.** Its "How it works" quoted five README run-commands (verified quotes, honestly labeled), but every container run was "not run by us (no Docker on the build machine)" and the walkthrough was procedure-verification only. For the lesson every other hands-on lesson depends on, the reader still could not see a *confirmed* working bring-up done by the guidebook's own hand. **What was added (2026-10-10):**
  - Full Docker attempt, honestly logged: static Docker 28.5.2 binaries install and the daemon runs (`--storage-driver=vfs --iptables=false --bridge=none`, required because this VM's kernel rejects overlay mounts and iptables rule appends), but Docker Hub is unreachable from this network (registry TLS handshake timeouts; proxy-aware `crane` couldn't complete even a `hello-world` pull). Attempt log is in `runs/b-practice-targets.log` — the "not run by us" marker for the other four targets now stands on evidence, not assumption.
  - **DVGA run for real, natively from the project's own source** (github.com/dolevf/Damn-Vulnerable-GraphQL-Application): venv + pinned requirements (two logged substitutions — pinned gevent 22.10.2 won't build on Python 3.12 → gevent 26.9.0; pinned greenlet 2.0.1 conflicts → 3.5.6), `setup.py` built the database. With `WEB_HOST=127.0.0.1` the app listened on `127.0.0.1:5013` only and answered a real GraphQL introspection query (`__schema` → full type list, introspection enabled) and `{ systemHealth }`. Restarted with `WEB_HOST=0.0.0.0` (the README's setting) → `ss` showed `0.0.0.0:5013 LISTEN` on all interfaces. That `ss` pair is the lesson's key teaching moment demonstrated, not just described: the README's `-e WEB_HOST=0.0.0.0` plus `-p 5013:5013` is exactly what the lesson's loopback override protects against. Teardown verified by PID and `ss`/`pgrep`.
  - Lesson §4 walkthrough and dateline updated; the README commands themselves were additionally confirmed against the freshly cloned source (README line 122: `docker run -t -p 5013:5013 -e WEB_HOST=0.0.0.0 dolevf/dvga`; Dockerfile `EXPOSE 5013`; source default `WEB_HOST=127.0.0.1`, overridden by the README command — the mechanism behind the teaching point).

## Factual-freshness fixes (not deepenings)

- **b-security-headers §7:** the RFC 6797 (HSTS) entry was a "cited as primary lead — fetch at build time before linking" placeholder. Fetched the RFC text in-session 2026-10-10; entry now reads "verified 2026-10-10." Source row staged in `/tmp/sources-add-B.csv`.
- **b-business-logic §7:** the PortSwigger business-logic entry said "re-fetch at build time before linking." Fetched the topic page in-session 2026-10-10; updated to "verified 2026-10-10." Source row staged.
- **b-csrf §7:** the RFC 6265bis citation. Checked the draft's publication status in-session: still a draft (draft-ietf-httpbis-rfc6265bis), not yet an RFC — the lesson's wording ("draft-ietf-httpbis-rfc6265bis §5.6.7", "RFC 6265 has no §4.1.2.7") remains accurate; entry refreshed to "verified 2026-10-10."
- **b-xss §7:** MDN CSP guide URL path `developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP` — verified reachable in-session 2026-10-10 (MDN redirects to the current location); left as-is with refreshed date.
- No renamed tools, no dead URLs found in any of the 21 lessons.

## What was deliberately not added (anti-pad log)

- No engine-escalation content in b-ssti (lab-bounded by design — the lesson's own decision, aligned with brief §7).
- No external-entity-resolution demo in b-xxe (same reason; the honesty note is a feature).
- No multi-host race infrastructure in b-race-conditions (concept-level by design; the mechanism is the lesson).
- No gadget-chain payloads in b-deserialization (researcher work by the lesson's own claim).
- No credential-stuffing runs in b-session-auth (taught as concepts-with-defenses; running them is outside the lesson's authorization).
- No Docker-container *attacks* in b-practice-targets — it is a setup lesson; the deepening is verified bring-up, not exploits.
- Levels were not raised on any lesson; the badges already match the delivered bar.

## Follow-ups for the parent / coordinator

- b-practice-targets deepening is done: DVGA run for real (native); the other four targets' "not run by us" markers now carry the full Docker attempt log. If the coordinator ever gets a build machine with registry access, re-running the five documented Docker commands there and curl-verifying the ports would close the loop — the lesson is already structured to receive that evidence.
- Two deferred-link patterns exist elsewhere in the guidebook ("re-fetch at build time before linking") — the coordinator's single build pass should re-verify every linked URL before the site ships, since lessons are long-lived.
