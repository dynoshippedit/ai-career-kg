# Content-depth audit 3 — Stage B batch, three new lenses (2026-10-10)

Auditor: subagent (depth-2 pass) · 2026-10-10 ~02:30 EDT. Dino's order: "go deeper on the lessons again." Two passes done (DEPTH-AUDIT-B.md, DEPTH-AUDIT-2-B.md — skimmed, not repeated). This pass applies three NEW lenses to all 21 Stage B lessons and edits where a lens genuinely fired.

Bar: brief SECURITY_GUIDEBOOK_BRIEF-2.md §5 (Stage B scope checklist), §6 (ten sections, in order), §7 (no hype, free-only, ≤3 resources, attack+detect+fix together).

## Lens-fire summary

| Lesson | L1 scope | L2 prereq chain | L3 exercises | Edits made |
|---|---|---|---|---|
| b-api-abuse | ✓ complete | B-AUTH dead ID (§2) | §9 walkthrough-redo escape hatch | B-AUTH→`b-authorization-scope`; §9 hatch removed |
| b-authorization-scope | ✓ complete (see note 1) | — (gate, no prereqs) | ✓ already explain/predict | none |
| b-bug-bounty | ✓ complete (see note 2) | **b-security-headers prereq delivered nothing** → removed | ✓ | prereq list fixed |
| b-business-logic | ✓ complete | b-sqli prereq is soft/sequencing (kept, noted) | ✓ (§5 fourth-assumption task is unaided, not a redo) | none |
| b-command-injection | ✓ complete | B-AUTH dead ID (§2); B-DEF dead pointer (§10) | ✓ | both fixed |
| b-csrf | ✓ complete | B-AUTH dead ID (§2); SOP assumed in §2 but taught only in §3; "B-VULN second wave: XSS" dead pointer (§10); B-DEF dead pointer (§10) | ✓ | B-AUTH fixed; §2 SOP reframed as taught-in-§3; §10 pointers fixed |
| b-deserialization | ✓ complete | B-AUTH dead ID (§2); §2 cited a-linux-cli, prereq list lacked it → added | ✓ | both fixed |
| b-graphql | ✓ complete | B-AUTH dead ID (§2) | ✓ | fixed |
| b-idor | ✓ complete | B-AUTH dead ID (§2); §10 had four dead pointers (B-VULN-02 nonexistent lesson, B-VULN-05, B-DEF, B-BOUNTY) | ✓ | B-AUTH fixed; §10 rewritten (see note 3) |
| b-jwt-oauth | ✓ complete | B-AUTH dead ID (§2) | ✓ | fixed |
| b-methodology | ✓ complete | §2 cited a-http-depth + a-linux-cli, prereq list lacked both → added | ✓ | prereq list fixed |
| b-practice-targets | ✓ complete | §2 cited a-tcpip-ports, prereq list lacked it → added; Docker image/container concepts assumed (gap note 4) | ✓ | prereq list fixed |
| b-race-conditions | ✓ complete | B-AUTH dead ID (§2) | ✓ | fixed |
| b-security-headers | **L1 gap: defensive basics untaught in Stage B** → taught (§3) | — | §8 Q5 was recall ("Name the attack class…") → rewritten | §3 defensive-basics block added; Q5 rewritten |
| b-session-auth | ✓ complete | §2 cited b-idor, prereq list lacked it → added | §8 Q5 was recall ("Name three abuses…") → rewritten | prereq list fixed; Q5 rewritten |
| b-sqli | ✓ complete | B-AUTH dead ID (§2); **a-git-github prereq delivered nothing** → removed; §2 assumed SQL literacy taught by a-reading-code, not listed → swapped in | §9 walkthrough-redo escape hatch | all fixed |
| b-ssrf | ✓ complete | B-AUTH dead ID (§2); "B-VULN second wave: XXE" dead pointer (§10); B-DEF dead pointer (§10) | ✓ | all fixed |
| b-ssti | ✓ complete | B-AUTH dead ID (§2) | ✓ | fixed |
| b-toolbench | ✓ complete (15/15 phases) | — | ✓ | none |
| b-xss | ✓ complete | §2 assumed JS literacy taught by a-reading-code, not listed → added; §4 attributed the no-`alert()` discipline to b-idor, which never states it → attribution fixed inline | ✓ | prereq + attribution fixed |
| b-xxe | ✓ complete | B-AUTH dead ID (§2) | ✓ | fixed |

Lens 1 fired on 1/21 (b-security-headers — the defensive-basics gap). Lens 2 fired on 14/21. Lens 3 fired on 4/21.

## Lens 1 — Scope completeness (brief §5 Stage B checklist)

Checked every named sub-item against the lesson that owns it:

- **Authorization** (b-authorization-scope): written authorization ✓, RoE's ten elements ✓, CFAA ✓, Computer Misuse Act §§1–3 incl. recklessness ✓. Note 1: the task brief for this pass said "the five hard rules," but the governing brief (line 211) lists **six** hard rules and the lesson quotes all six verbatim — the lesson matches the brief; the task's "five" is a miscount. No change made.
- **Methodology** (b-methodology): WSTG v4.2's 12 categories + how to read it and use test cases as a checklist ✓, PTES seven stages ✓ (verified on primary page 2026-10-09), SP 800-115 planning/execution/post-execution + RoE framing + handling of findings ✓, and all six phases (scoping taught first and hardest; recon passive/active split with "a name found is not permission"; enumeration as scoped inventory; exploitation as defender-reproduceable proof; post-exploitation in business terms; reporting with root cause/repro/impact/remediation/scope proof) ✓.
- **Toolbench** (b-toolbench): all fifteen phases in activation order, each with its question, the free tool, how to read its output, and what it cannot tell you ✓ (spot-checked phases 1, 7, 12, 15).
- **Vuln frame** (all 16 classes): what the flaw is / why it arises in real code / how found in authorized testing / single minimal PoC on local target / remediation AND detection ✓ in every lesson (each carries a "How defenders see it" or equivalent defender section).
- **Practice targets** (b-practice-targets): one-command setup for DVWA, Juice Shop, WebGoat, crAPI, DVGA ✓, reset procedure for each ✓.
- **Defensive basics**: **GAP FOUND.** The §5 bullet requires teaching the SOC triage workflow, how to read a SIEM alert, and alert-prioritization logic. No Stage B lesson taught any of the three — five attack lessons pointed at "B-DEF (defensive basics)" in §10, but B-DEF resolved to nothing in Stage B (the deep treatment lives in Stage C's c-soc-triage, which a Stage B reader hasn't reached; the soc-analyst role path lists "B defensive basics" explicitly). Fixed by teaching it: new "Defensive basics: the other side of the wire" subsection in b-security-headers §3 (the guidebook's defensive anchor lesson — triage workflow as collect→enrich→decide→act; SIEM-alert reading as rule→entities→raw-event; prioritization as fidelity × impact), cross-referencing c-soc-triage for the deep version. The five B-DEF pointers now resolve to `b-security-headers` §3.
- **Bug bounty** (b-bug-bounty): how programs define scope/safe harbor ✓ (program anatomy section), reading disclosed reports to learn chains ✓ (four-pass reading method), writing up findings ✓ (five-part triage-ready anatomy + dry-run walkthrough). Note 2: platform-specific wording differences (HackerOne vs Bugcrowd vs Intigriti) are deliberately delegated to §7's primary docs with comparison tasks — the wording changes per program and inline teaching would go stale; the lesson teaches the *reading* via the scope-card exercise in §5. Judgment call, logged.

## Lens 2 — Prerequisite chain integrity

### (a) Forward references / missing foundations — fixed

1. **b-deserialization**: §2 said "You can read Python and run shell commands (`a-python-security`, `a-linux-cli`)" but prereqs were `[a-python-security, a-http-depth]`. Added `a-linux-cli`.
2. **b-practice-targets**: §2 said "you understand what 'bind to localhost' means (`a-tcpip-ports`)" but prereqs were `[a-linux-cli]`. Added `a-tcpip-ports`.
3. **b-xss**: §2 assumed JavaScript reading (`document.getElementById`, `innerHTML`, event handlers, `location.hash`) — taught by `a-reading-code`, which was not listed. Added `a-reading-code`; §2 now cites it.
4. **b-sqli**: §2 assumed SQL literacy ("what the `WHERE` clause does, what `--` means") — taught by `a-reading-code`, not listed. Swapped the non-delivering `a-git-github` (see c) for `a-reading-code`; §2 now cites it.
5. **b-session-auth**: §2 said "You understand the authentication/authorization split from `b-idor`" but `b-idor` was not a prerequisite (list was `[a-http-depth, b-csrf]`). Added `b-idor`.
6. **b-methodology**: §2 said "You can read HTTP traffic (`a-http-depth`) and operate a Linux system (`a-linux-cli`)" but prereqs were `[b-authorization-scope]` alone. Added both.
7. **b-csrf**: §2 claimed "You know the same-origin policy's shape" — SOP is taught nowhere in its prerequisites; it is taught in the lesson's own §3 ("Why the same-origin policy leaves this gap at all"). Reframed §2 to present SOP as taught-in-§3 rather than assumed prior knowledge.
8. **b-xss §4**: attributed the no-`alert()` proof-marker discipline to b-idor ("per the guidebook's own discipline (see `b-idor`)") — b-idor never states it; neither does the brief nor curriculum.md. Removed the false attribution and stated the discipline inline with its rationale (proof payloads stay inert by construction, so a copied proof can't become someone else's working attack).

### Dead cross-references — fixed (12 + 9)

- **"B-AUTH"** appeared in §2 of 12 lessons (b-api-abuse, b-command-injection, b-csrf, b-deserialization, b-graphql, b-idor, b-jwt-oauth, b-race-conditions, b-sqli, b-ssrf, b-ssti, b-xxe). No lesson with that ID exists — the actual lesson is `b-authorization-scope`. All 12 now read "re-read `b-authorization-scope`".
- **§10 dead pointers**: b-idor's `B-VULN-02` pointed at a nonexistent "Broken access control (general)" lesson — rewritten to name the three family members (function-level checks, role tampering, forced browsing) as applications of this lesson's template, with the missing dedicated lesson logged as a coordinator gap (note 3). `B-VULN-05`→`b-api-abuse`; `B-BOUNTY`→`b-bug-bounty` (b-idor, b-sqli); "B-VULN second wave: XSS"→`b-xss` (b-csrf); "B-VULN second wave: XXE"→`b-xxe` (b-ssrf); all five `B-DEF` pointers→`b-security-headers` §3.

### (c) Prerequisites that didn't deliver — fixed

- **b-sqli** listed `a-git-github`: the lesson never uses git or GitHub (only a github.com link in §7 resources). Removed.
- **b-bug-bounty** listed `b-security-headers`: zero mentions of headers/CSP/SameSite/HSTS anywhere in the lesson (grep-verified). Removed. The real gate — "find, reproduce, and fix at least one vulnerability class end to end" — is already covered by the remaining `b-idor` prereq.

### Kept as deliberate sequencing (not hidden, logged)

- **b-business-logic** `[b-idor, b-sqli, b-xss]`: b-sqli is not directly used by the lesson text, but §2 explicitly frames the trio as "the wave-1 lessons" whose distrust-the-client pattern this lesson generalizes. Kept as a wave gate; softness noted.
- **b-csrf** `[a-http-depth, b-idor]`: b-idor's contribution is the authenticated-identity intuition and the two-account testing discipline rather than a cited mechanism. Soft but genuine; kept.

## Lens 3 — Exercise quality

§8 audited across all 21: 19/21 were already explain/predict throughout. Two recall-leaning questions rewritten:

**b-security-headers §8 Q5** (worst one — pure recall: "Name the attack class…"):
- Before: "A session cookie is set with `Secure; HttpOnly` but no `SameSite` attribute. Name the attack class this leaves open and the header from `b-csrf`'s lesson that would have closed it."
- After: "A session cookie is set with `Secure; HttpOnly` but no `SameSite` attribute. An attacker hosts a page that auto-submits a cross-site POST to the site's email-change endpoint. Walk through what the browser attaches to that request and what the server does with it — then explain which cookie attribute would have stopped the request from arriving authenticated, and why `Secure` and `HttpOnly` don't help here."
- Why: the old version is answered by two memorized nouns (CSRF, SameSite); the new one forces the reader to run the mechanism (browser attaches cookie cross-site → server sees authenticated request) and reason about *why* the other two flags are irrelevant.

**b-session-auth §8 Q5** (recall: "Name three distinct abuses…"):
- Before: "A password-reset token never expires and is accepted multiple times. Name three distinct abuses this enables, and the three token properties that would prevent them."
- After: "A password-reset token never expires and stays valid after use. An attacker recovers a year-old reset email from a breached mailbox. Explain what they can do with it that they couldn't if the token expired after an hour — then explain what changes if the token is also single-use, and which of the two properties matters more against an attacker who intercepts the email in transit."
- Why: the old version is a list-recall; the new one makes the reader compare expiry vs single-use under two different attacker positions.

**§9 "Prove it" — walkthrough-redo escape hatches removed** (2):
- b-api-abuse §9: "(or the local-demo equivalents with exact requests)" deleted — artifact must now be the four one-page reports against targets not touched in the lesson.
- b-sqli §9: "(or the walkthrough evidence chain)" deleted — same requirement.
- b-business-logic §9 kept as-is deliberately: its "On your own" demands a *fourth* assumption the walkthrough didn't violate — unaided work, not a redo — and its artifact format (state-machine diagram + request sequence + impact + fix + detection) is stranger-verifiable.

§5 "On your own" success tests: all 21 already verifiable by the reader alone (concrete artifacts: scope cards, curl transcripts, one-page reports with named fields, negative-evidence requirements). No rewrites needed.

## Gaps for the coordinator (not fixed — structural, need Dino-level decisions)

1. **No dedicated "broken access control (general)" lesson.** The §5 Stage B checklist lists "broken access control" as a class alongside IDOR; b-idor teaches the IDOR template and claims it generalizes, but function-level checks, role tampering, and forced browsing have no dedicated lesson — b-idor's §10 previously pointed at a phantom "B-VULN-02". I rewrote the pointer to frame them as applications of the IDOR template. If Dino wants a real lesson, that's new-lesson work, not a §10 fix.
2. **Defensive basics depth.** I taught the Stage B foundation (triage workflow, SIEM-alert reading, fidelity × impact) in b-security-headers §3; the deep treatment is c-soc-triage (Stage C). If the soc-analyst path needs more at Stage B, that's a scope decision.
3. **Docker image/container concepts** (b-practice-targets §2: "you know what an image and a container are") are assumed with no guidebook prereq teaching them; the mitigation is the §7 link to Docker's official install docs. Flagged, not "fixed" — adding a Docker lesson is out of this pass's scope.
4. **b-race-conditions** assumes "threads at the level of two things happening at once" — taught inline ("two things happening at once") rather than by a prereq; judged sufficient, logged.
5. **Bug-bounty platform wording** (note 2 above): concepts taught, platform-specific safe-harbor wording delegated to §7 primary docs. If Dino wants inline platform comparisons, that needs in-session fetches of all three platforms' current policies.

## Source rows staged

`reports/sources-add-3-B.csv` — header only, zero data rows. No new external facts were added in this pass: the defensive-basics block is the guidebook's own framework synthesis (triage workflow, SIEM reading, fidelity × impact — no product claims, no statistics), and every other edit is an internal reference fix, prereq-list correction, or exercise rewrite. Nothing to verify against a primary source.

## Verification (2026-10-10)

- All 21 lessons: exactly 10 `## ` sections each (grep-checked); `lesson_id:` frontmatter line present in all 21; frontmatter structure otherwise untouched.
- Legacy dead IDs (`B-AUTH`, `B-VULN`, `B-DEF`, `B-BOUNTY`): zero remaining matches across the 21 files.
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`): zero hits in all edited files.
- Currency symbols: none added.
- Test servers: none started by this audit (all additions are §2/§3/§8/§9/§10 prose and reference fixes; no new walkthrough steps). `pgrep` shows no stray demo processes.
- Levels: none raised. No new resources (≤3/resource rule undisturbed), no commits, no push. build_site.py NOT run (per instructions); STATE.md, gaps.md, map.md, sources.csv untouched; no other stage's files touched.

## Decisions

- The defensive-basics gap was taught rather than cross-referenced away: c-soc-triage is Stage C, and the soc-analyst role path promises "B defensive basics" — a Stage B reader needs the foundation before Stage C. The block is compact (~250 words), sits in the guidebook's defensive anchor lesson, and points forward to c-soc-triage for depth.
- Prereq lists were corrected, not shuffled: every addition matches a citation already in the lesson's §2; every removal was grep-verified as genuinely unused. The two soft/sequencing prereqs were kept and logged rather than silently dropped.
- The "five hard rules" in this pass's task brief is a miscount — the governing brief lists six, the lesson teaches six verbatim. Flagged, not "fixed."
