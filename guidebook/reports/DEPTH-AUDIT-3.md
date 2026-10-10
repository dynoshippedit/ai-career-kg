# DEPTH-AUDIT-3 — merged report (2026-10-10)

Third depth pass. Three new lenses, applied to all 110 lessons by six stage crews.
Per-stage detail: DEPTH-AUDIT-3-A/B/C/D/E/AI.md. This file merges findings, records
coordinator decisions, and lists new gaps.

## Lens 1 — Scope completeness (§5 sub-items taught, not mentioned)

Fired hardest in Stage A:
- **a-tcpip-ports**: 6 missing §5 sub-items added — IPv4/IPv6 addressing + subnetting
  (CIDR, RFC 1918 ranges), IPv6 address-type reading, DHCP DORA, routing, middleboxes
  (stateful/stateless firewalls, VPNs, forward/reverse proxies, VLANs). Four new §3
  subsections, new §4 step 9 (run), §6/§7 extended.
- **a-http-depth**: Basic/Bearer/OAuth 2.0 authorization-code/OIDC flows taught (were
  absent); TLS 1.3 handshake written step-by-step (6 messages). New §4 steps 11–12 (run).
- **a-linux-cli**: "memory" was entirely absent from §5's "processes and memory" —
  added §3 subsection (VSZ vs RSS, /proc/<pid>/status, maps, swap, OOM killer,
  core-dump credential leaks) + §4 step 10 (run).
- a-crypto, a-dns-depth, a-python-security, a-reading-code: no fire (all taught).

Stage B (1 fire): the §5 "Defensive basics" bullet (SOC triage workflow, SIEM-alert
reading, alert-prioritization logic) was taught nowhere a Stage B reader could reach —
five attack lessons pointed at a "B-DEF" that resolved to nothing. Taught as a new
~250-word "Defensive basics: the other side of the wire" subsection in
b-security-headers §3 (collect→enrich→decide→act; rule→entities→raw-event;
fidelity × impact); all five pointers now resolve to it; c-soc-triage cross-referenced
for depth.

Stage C (3 fires): c-public-track-record — "impact chain" untaught → added
primitive → capability → consequence → business impact, each link needing its own
evidence; c-vuln-ecosystem — CAPEC abstract → added concrete CWE-89 ↔ CAPEC-66 pair
(verified on capec.mitre.org) + honest scoping note (CAPEC doesn't rank; the queue is
CVSS+EPSS+KEV); c-ai-tooling — CVP primary URL fetched and verified in-session
(anthropic.com/news/cyber-verification-program), all tier facts primary-confirmed,
added "How the trust is enforced" (applicant verification, proof of controls,
mandatory data retention).

Stage D (2 fires): d-malware-analysis — "sandboxing" was scope-named but never taught
(only "sandbox evasion" mentioned) → added "Sandboxing: dynamic analysis, automated"
§3 subsection; d-dfir-deep — "writing detections in Sigma" named but never exercised
→ added worked mini-example (beaconing hunt T1071.001 → Sigma draft, marked sketch;
field list grounded in c-sigma-detection's spec).

Stage E (1 fire): nowhere did the guidebook teach the three governance frameworks'
relationship → added "three frameworks side by side" to e-soc2 §3 (CSF communicates,
27001 manages, SOC 2 attests; Informative References map CSF↔27001; the 27001 SoA's
controls become SOC 2's tested controls).

AI track (0 fires): all §5 sub-items genuinely taught; OWASP 2026 codes re-verified
against the primary repo README (LLM01–LLM10, published 2026-08-04).

## Lens 2 — Prerequisite chain integrity

Stage A (4 fixes): **broke a cycle** a-linux-cli → a-tcpip-ports → a-dns-depth →
a-linux-cli (removed a-tcpip-ports from cli's prereqs; cli now root); removed Stage B
b-sqli from a-reading-code prereqs (chain inversion → "Leads to"); removed
b-authorization-scope from a-osint-research (rule now taught up front in §2); added
a-linux-cli to a-http-depth prereqs (shell fluency was assumed). All prereqs now
Stage-A-only, acyclic.

Stage B (14 lessons): 12 dead "B-AUTH" references → b-authorization-scope; 9 dead §10
pointers (B-VULN-05→b-api-abuse, B-BOUNTY→b-bug-bounty, second-wave→b-xss/b-xxe,
B-DEF→b-security-headers §3) fixed; b-idor's B-VULN-02 phantom pointer rewritten as
template-application guidance. Prereq lists corrected: added a-linux-cli
(b-deserialization), a-tcpip-ports (b-practice-targets), a-reading-code (b-xss, b-sqli),
b-idor (b-session-auth), a-http-depth+a-linux-cli (b-methodology); removed a-git-github
(b-sqli) and b-security-headers (b-bug-bounty), both grep-verified unused.

Stage C (6 breaks): c-soc-triage §2 overstated b-session-auth's content → corrected to
what it delivers; §4's c-log-sources reference (sibling, not prereq) → enrichment moved
in-lesson; c-log-sources §2 overstated a-tcpip-ports → corrected; c-sigma-detection
assumed YAML taught nowhere → 5-line primer added in-lesson; c-incident-response's
sibling rule reference → stated fully in-lesson; c-cve-program named KEV early →
one-line gloss. Removed ai-governance from c-ai-tooling prereqs (transitive closure
pulled Stage E; zero ai-governance concepts used) — ratified below.

Stage D: **biggest find** — d-exploit-concepts §2 claimed "read C and follow a pointer
(a-reading-code)" — false; a-reading-code teaches JS/SQL and NO lesson teaches C
(full-text verified). Fixed both ways: §2 corrected to what a-reading-code delivers,
§3 gained "The C you need" foundation (pointer/buffer/strcpy-without-measuring,
concept level). Added a-python-security to d-redteam-concepts, d-dfir-deep, d-appsec,
d-malware-analysis (walkthroughs script Python); added d-redteam-concepts to d-dfir-deep
(used in §3+§10); removed d-redteam-concepts from d-exploit-concepts prereqs (only in
§10 "Leads to" — ratified below); added b-authorization-scope to d-exploit-concepts
(§2 invokes its safety concept).

Stage E (15 lessons): all fixed by fixing the reference — assumed-prior-learning
reworded into companion pointers with inline micro-foundations where load-bearing
(strongest: e-test-analysis-reporting assumed e-control-testing's method matrix; the
method-bounds concept now taught inline). No frontmatter lists changed; reverse
verification (prereqs deliver what dependents expect) passed; orphan sweep clean
(ITAF, ZTMM, RACI, SP 800-160, CPLP, SoA all defined at first use).

AI track (4 fixes): ai-prompt-injection §2 had a circular forward reference
(ai-llm-architecture knowledge asserted with prereqs []; architecture requires
prompt-injection) → §2 now teaches the stack from scratch in §3; ai-pipeline,
ai-supply-chain, ai-threat-modeling §2s now state what their frontmatter prereqs
deliver (git-hash identity, hash-vs-branch, likelihood/impact vocabulary).

## Lens 3 — Exercise quality

Recall questions rewritten as explain/predict (worst cases):
- a-dns-depth Q1: "List every server involved in resolving shop.example.com, in
  order" → 4ms-answer vs cold-cache predict/explain.
- a-http-depth Q1, a-python-security Q2, a-reading-code Q1+Q3, a-osint-research Q4,
  a-windows-concepts Q2, b-security-headers Q5 ("Name the attack class…"),
  b-session-auth Q5 ("Name three abuses…"), c-cvd Q5, c-cve-program Q2,
  c-vuln-ecosystem Q2, c-ai-tooling Q2/Q3, d-exploit-concepts Q1 (thesis-sentence
  recall → prediction from a weaker primitive), ai-supply-chain Q5 ("List the four
  verification checks" → predict/explain against a lookalike-publisher attack).
  Stage E: zero recall questions found (all 55 already explain/argue/predict).

Vague success tests made reader-verifiable (14 in Stage A incl. a-linux-cli §5(a) → a
concrete `sudo -u nobody` denial test; c-public-track-record's peer-dependent test →
line-number checklist + redacted-title test; c-ai-tooling → 3-item Defense Access fit
checklist; d-appsec §5 → all six STRIDE letters; d-cloud-security/d-redteam-concepts/
d-malware-analysis "second reader" tests → alone-verifiable versions).

"Prove it" artifacts closed the walkthrough-redo loopholes: b-api-abuse, b-sqli,
c-cvss (→ the §5 KEV CVE as "the test set"), c-incident-response (removed "or the
walkthrough report"), c-sigma-detection, c-soc-triage/c-log-sources (invented
cases/stories required), d-appsec (diff review on the reader's own commit/PR),
d-malware-analysis (reader-crafted sample + own YARA rule), ai-threat-modeling (the
§5 Meridian pipeline, not the walkthrough's case), e-board-communication and
e-security-program (a *different* organization, stranger-verifiable), a-crypto/
a-tcpip-ports/a-http-depth §9s rebuilt around unaided application.

## Coordinator decisions (ratified)

1. d-redteam-concepts removed from d-exploit-concepts prereqs — ratified: a §10
   "Leads to" pointer is a forward reference, not a prerequisite.
2. ai-governance removed from c-ai-tooling prereqs — ratified: zero concepts used;
   the transitive closure dragged in Stage E.
3. Broken-access-control "gap" (B worker) — closed as already decided: b-idor §10
   documents the consolidation ("no separate lesson: missing function-level checks,
   role tampering, and forced browsing are the same missing-check shape as IDOR").
4. Block-assumption convention — recorded as standing: Stage D/E lessons may assume
   their stage's block knowledge with explicit "Stage X cold" wording (d-appsec,
   e-sdlc precedent) rather than listing every lesson.
5. No-C-anywhere — the inline minimal-C foundation in d-exploit-concepts stands;
   teaching C earlier (e.g. in a-reading-code) is a Stage A scope decision for Dino.
6. E worker's 12 optional prereq-list additions — logged, not applied (lessons fixed
   via inline foundations instead).
7. C worker's optional Stage A/B follow-ups (spray-shape/impossible-travel in
   b-session-auth; 5-tuple/encryption in a-tcpip-ports) — logged as optional.

## New gaps (added to gaps.md)

- DoT/DoH has no home: a-dns-depth prescribes it as the fix; no lesson teaches it.
- Docker image/container concepts assumed in b-practice-targets (mitigated by §7
  link to Docker's official docs).
- Defensive-basics depth at Stage B: minimal foundation now in b-security-headers §3;
  deep treatment is c-soc-triage — scope call if the soc-analyst path needs more.
- Bounty platform safe-harbor wording delegated to §7 primary docs; inline platform
  comparisons need fresh in-session fetches.

## Counts

- Lessons edited: A 9/10, B 14/21, C 10/10, D 6/6, E 24/55, AI 4/8.
- sources.csv: 375 → 388 rows (13 new verified rows + CVP row merged with re-fetch
  detail); new dedicated `chars_fetched` column (empty for legacy rows — their
  embedded counts stay in claim text, no data lost).
- New run-log appends: a-tcpip-ports, a-linux-cli, a-http-depth (4 new walkthrough
  steps, all run on loopback 2026-10-10).
