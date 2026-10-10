# Content-depth audit 2 — Stage B batch, sharper lenses (2026-10-10)

Auditor: subagent (depth-2 pass) · 2026-10-10. Dino's order: "try again" — the first pass (DEPTH-AUDIT.md Stage B: 20 SOLID / 1 deepened) was too lenient. This pass applied the five sharper lenses to all 21 Stage B lessons and edited every lesson where a lens genuinely fired.

Bar: brief SECURITY_GUIDEBOOK_BRIEF-2.md §1 (no term the reader can't unpack; define each term where first needed, by what it does), §6 (ten sections, in order), §7 (no hype words, free-only, ≤3 resources, attack+detect+fix together).

## Lens-fire summary

| Lesson | L1 jargon | L2 why | L3 detection | L4 worked-ex | L5 §7 | Notes |
|---|---|---|---|---|---|---|
| b-api-abuse | ORM, DTO, principal, algorithmic-complexity DoS | why authz must be data-driven (URL is a lookup key, never a decision) | concrete BOLA access-log lines | — | — | |
| b-authorization-scope | VDP | — | N/A (gating lesson, no attack) | — | — | |
| b-bug-bounty | CFAA, kudos points | why first-reporter-wins (novelty = new risk information) | N/A (process lesson) | — | — | |
| b-business-logic | fuzzing, dual-use endpoints | why the map comes first (can't violate an unnamed assumption) | — (already concrete: reconciliation rules) | — | — | dual-use def moved to the resource that names it |
| b-command-injection | metacharacter (by-function), sink | why no-shell argv defeats injection (no parse phase exists) | — (already concrete: Sysmon E1, parent-child) | — | — | |
| b-csrf | constant-time comparison, HMAC, method override | why the SOP is asymmetric (reading blocked, sending allowed) | concrete rejected-CSRF application-log line | — | — | |
| b-deserialization | classpath, SAST, HMAC | why the parser's instruction set is the attack surface | concrete cookie-size-anomaly log | — | — | |
| b-graphql | resolver, principal, persisted queries | — (rationale covered) | concrete `__schema` query-log line | — | — | |
| b-idor | tenant, bearer token | why the check belongs at the data-access layer | concrete IDOR-probing access-log lines | — | — | |
| b-jwt-oauth | base64url, JOSE, JWKS, PKCE, IdP, BCP | why the code flow exists (browser is an untrusted channel) | concrete decoded `alg=none` header | — | — | |
| b-methodology | certificate transparency logs | — | N/A (planning lesson) | — | — | |
| b-practice-targets | ephemeral, network namespace | why the app must bind 0.0.0.0 *inside* the container | N/A (setup lesson) | — | — | |
| b-race-conditions | atomic, invariant, compare-and-set, isolation levels | why the DB is the arbiter (only place with a total order) | concrete same-millisecond redemption log | — | — | |
| b-security-headers | MIME, execution context, `__Host-` prefix | why browsers sniff (compat history) | concrete CSP violation-report JSON | — | — | |
| b-session-auth | TOTP, breach-password screening, entropy | why possession beats knowledge as a factor | concrete auth-log excerpt (fixation + 20×401) | — | — | |
| b-sqli | sink, WAF, bind variable | why prepared statements win at the protocol level (parse once, never re-parse) | — (already concrete: CRS 942xxx, slow-query) | — | — | |
| b-ssrf | link-local, IAM, canonicalized, OAST | why IMDSv2's PUT requirement stops simple SSRF | concrete egress-log lines to 169.254.169.254 | — | — | |
| b-ssti | object model, autoescape | why the compile/render phase split is the guarantee | concrete URL-decoded probe log line | — | — | |
| b-toolbench | wordlist, interactsh, recursion, kudos | why manual runs precede automation (calibration before amplification) | N/A (tools lesson) | — | — | kudos def already present in b-bug-bounty; not duplicated |
| b-xss | execution context, trust boundary, sink | why `textContent` is safe (no HTML parser invoked) | — (already concrete: log patterns + CSP report) | — | — | |
| b-xxe | SAML, DTD, DOCTYPE, canary file | why external entities were a default (trusted-document design) | concrete DOCTYPE request-body excerpt | — | — | |

Lens 1 fired on 21/21. Lens 2 fired on 19/21 (b-graphql, b-methodology: rationale already complete — recorded, not padded). Lens 3 fired on 12/15 applicable lessons (b-sqli, b-command-injection, b-xss, b-business-logic already carried concrete defender signals; the three N/A lessons are non-attack lessons). Lens 4 fired on 0/21 — every lesson's §3 already carries its own worked mechanism example (verified, not assumed). Lens 5 fired on 0/21 — every §7 already gives read-order guidance ("read §4; note…; skim…").

## What was added, per lesson (exact)

- **b-api-abuse** (§3): by-function definitions for ORM, DTO (data transfer object), principal, algorithmic-complexity DoS; a "why it arises"-level rationale that the URL is a lookup key and ownership must be re-derived from the database on every request; a three-line access-log excerpt showing BOLA probing (one session, sequential IDs, all 200) with the "ID spread is the signal" reading.
- **b-authorization-scope** (§6): VDP defined where first needed (standing-offer structure, safe harbor, no payout).
- **b-bug-bounty** (§3): CFAA expanded at first use; the first-reporter-wins rationale (novelty = new risk information); (§7) kudos points defined.
- **b-business-logic** (§3): the map-first rationale (can't violate an unnamed assumption); fuzzing defined by function; (§7) dual-use endpoints defined in the resource that names the term.
- **b-command-injection** (§3): metacharacter defined by what it does; the no-shell/argv rationale (no parsing phase exists — the shell was the parser); (§6) sink defined.
- **b-csrf** (§3): HMAC, constant-time comparison, method override defined by function; the SOP-asymmetry rationale (reading blocked for confidentiality, sending allowed for the web's machinery — CSRF lives in that gap); a rejected-CSRF application-log line (event logged, token value never logged).
- **b-deserialization** (§3): classpath, SAST, HMAC defined by function; the parser-as-interpreter rationale (instruction set = attack surface; you change the interpreter, not the blocklist); a cookie-size-anomaly log (48/48/312 bytes).
- **b-graphql** (§3): resolver and principal defined by function; a query-log line showing the `__schema` tripwire; (§9) persisted queries defined.
- **b-idor** (§3): tenant and bearer token defined by function (bearer token cites RFC 6750); the data-access-layer rationale (one choke point can't be forgotten); a three-line access-log excerpt of IDOR probing with the spread-is-the-signal reading.
- **b-jwt-oauth** (§2): base64url defined (RFC 4648 §5); (§3) JWKS defined (RFC 7517), the code-flow rationale (browser is an untrusted channel — code is worthless without the client secret); the decoded `{"alg": "none"}` header as the defender's one-line signal; (§7) JOSE and BCP (BCP 225) defined; (§9) PKCE and IdP defined.
- **b-methodology** (§4): certificate transparency logs defined by function (RFC 6962).
- **b-practice-targets** (§3): ephemeral and network namespace defined; the container-bind rationale (container localhost ≠ host localhost — the app listens on all interfaces of its private network; `-p` decides which host interfaces may knock).
- **b-race-conditions** (§3): atomic, invariant defined by function; the same-millisecond redemption log with the -1; compare-and-set defined; the database-as-arbiter rationale (only place with a total order); (§9) isolation levels defined.
- **b-security-headers** (§3): MIME defined; the sniffing-compat-history rationale; a CSP violation-report JSON naming document-uri/violated-directive/blocked-uri; execution context defined in the verification habit; (§6) `__Host-` prefix defined (Secure + host-only + Path=/, per the cookie draft §5.7).
- **b-session-auth** (§3): TOTP expanded and defined (RFC 6238, 30-second step); breach-password screening defined (NIST SP 800-63B); the possession-vs-knowledge rationale; (§4) a concrete auth-log excerpt (20×401s + the fixation line) and entropy defined.
- **b-sqli** (§1): WAF expanded; (§3) bind variable defined; the prepared-statement protocol rationale (query and values travel separately; values are never parsed); (§4) sink defined.
- **b-ssrf** (§3): link-local and IAM defined; the IMDSv2 PUT rationale (simplest fetchers only do GETs — the method requirement is the barrier); canonicalized defined; a two-line egress log to 169.254.169.254; (§5) OAST expanded.
- **b-ssti** (§3): object model and autoescape defined; the compile/render phase-split rationale; a URL-decoded `{{7*7}}` access-log line.
- **b-toolbench** (§3): phase-4 manual-before-automation rationale (calibration before amplification); wordlist and interactsh defined; (§7) recursion defined.
- **b-xss** (§1): trust boundary defined; (§3) execution context defined; the `textContent` rationale (no HTML parser invoked); (§4) sink defined.
- **b-xxe** (§1): SAML expanded; (§3) the trusted-document-design rationale for external-entity defaults; DTD defined; a DOCTYPE request-body excerpt; the DOCTYPE defined in the worked example; (§6) canary file defined.

## Source rows staged

`reports/sources-add-2-B.csv` — 10 rows, all status=verified, all fetched in-session 2026-10-10: RFC 6238 (TOTP), RFC 7636 (PKCE), RFC 7517 (JWKS), RFC 4648 §5 (base64url), RFC 6750 (bearer token), RFC 6962 (certificate transparency), RFC 8725 (BCP 225), draft-ietf-httpbis-rfc6265bis-22 §5.7 (`__Host-` rules; expires 4 June 2026), AWS IMDSv2 docs (PUT-issued session token), SP 800-63B-4 landing page (July 2025 edition confirmed). Purely definitional one-liners (ORM, sink, principal, etc.) carry no rows — they are standard vocabulary explained by function, not external factual claims. The parent merges this file into sources.csv.

## Verification (2026-10-10)

- All 21 lessons: exactly 10 `## ` sections each (grep-checked); `lesson_id:` frontmatter line present in all 21; frontmatter structure untouched.
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`): zero hits in new copy — and zero across all 21 files (they were already clean).
- Currency symbols: no `$<digit>` added (only pre-existing awk-style references, none new).
- `python3 guidebook/build_site.py` from ~/workspace/learncomputerstuff: completed with zero errors.
- Test servers: none started by this audit (no new walkthrough steps were added — all additions are §3/§6/§7/§9 prose and illustrative log examples; per the ratified substitution policy, illustrative examples are marked as examples, not run transcripts). `pgrep` shows no stray demo processes.
- Levels: none raised. No new walkthrough steps, no new resources (≤3/resource rule undisturbed), no commits, no push. build_site.py, STATE.md, gaps.md, map.md untouched; no other stage's files touched.

## Decisions

- Illustrative log lines are presented as teaching examples ("looks like this"), not as run transcripts — they teach the defender's reading of telemetry, and the walkthroughs' real transcripts in runs/ are untouched.
- Lens 2 and lens 3 were recorded as no-fire where the lesson already carried the rationale or the concrete signal — padding a strong lesson to make a lens fire would have weakened it.
- b-graphql got no lens-2 addition: its design rationale (spec assumes trusted context; resolvers lack a global cost view) is already the lesson's spine.
- No factual claim was added without an in-session primary-source fetch where a standard backs it; the CSV above is the evidence.

## What this pass did not do

- No re-verdict of the first pass's SOLID calls — different lenses, as ordered.
- The two cross-batch link notes from the first pass (legacy lesson-ID scheme in "Leads to"; deferred "re-fetch at build time" links) are coordinator-owned and were not touched.
