# Content-depth audit, third pass — Stage D (6 lessons), three new lenses — 2026-10-10

Auditor: subagent (depth-2 pass) · 2026-10-10 ~01:45–03:00 EDT.
Scope: `d-redteam-concepts`, `d-dfir-deep`, `d-appsec`, `d-exploit-concepts`, `d-malware-analysis`, `d-cloud-security`.
Method: every lesson re-read end to end against three NEW lenses (scope completeness vs the §5 checklist; prerequisite-chain integrity against every lesson named in each frontmatter `prerequisites` list; exercise quality). DEPTH-AUDIT-2's jargon/why/detection/reading-guidance work was skimmed and NOT repeated.

**Result: all 6 lessons edited. Lens 1 fired on 2/6, Lens 2 on 6/6, Lens 3 on 6/6.** No level changes. No walkthrough steps added or re-run (all additions are §2/§3/§5/§8/§9 prose and one illustrative worked sketch). No commits, no pushes.

---

## Per-lesson table

| Lesson | Lenses fired | Missing §5 sub-items + what was added | Broken prereq chains + fixes | Exercise rewrites |
|---|---|---|---|---|
| d-redteam-concepts | 2, 3 | None — ATT&CK model (15 tactics, v19.2 split taught), adversary emulation, C2 + evasion at concept level, purple teaming, Atomic-Red-Team-in-lab hands-on all genuinely taught. | (a) Python scripting used in §4 (tactic_mapper.py, beacon_stats.py) but no prereq taught it → added `a-python-security` to frontmatter. (b) `d-malware-analysis` claims "why the implant exists: persistence, C2, collection" from this lesson — C2 was taught, Persistence/Collection/Exfiltration were only tactic-list names → added a "Why the channel exists" paragraph to §3 naming the three goal-tactics as the implant's ends. | §5: "second reader" test → alone-verifiable (quote the ATT&CK Detection-section line per mapping). §9: artifact re-centered on the §5 extended intrusion + a *different* fictional estate (not walkthrough repackaging). |
| d-dfir-deep | 1, 2, 3 | "Writing detections in Sigma" was named but never taught — the lesson pointed at `c-sigma-detection` without exercising the translation. Added a worked mini-example to §3 (beaconing hunt T1071.001 → Sigma draft, marked illustrative sketch; field list grounded in c-sigma-detection's own spec). YARA side genuinely covered via prereq `d-malware-analysis`. 800-61 lifecycle genuinely covered via prereq `c-incident-response` (verified: teaches SP 800-61 Rev. 3, April 2025). Disk/memory/network forensics, threat hunting: taught. | (a) §3 uses `d-redteam-concepts` twice (beaconing "the regular timing from d-redteam-concepts"; ATT&CK "the behavior language from d-redteam-concepts") + §10 — but it was not a prerequisite → added to frontmatter. (b) §4 uses Python (gen_evidence.py confirmed in runs/d-dfir-deep.log) with no prereq → added `a-python-security`; also fixed the stale §2 tooling line (claimed shell-only, walkthrough uses Python 3.12). | §5: "stranger" test → alone-verifiable (memo-away check; every claim must carry a timeline-line citation). §9: artifact re-centered on the §5 own-evidence case (their generated set, their attack shape). |
| d-appsec | 2, 3 | None — STRIDE (with property mapping), SAST/DAST/IAST/SCA each with Sees/Blind-to, secure-SDLC integration, code-review technique all taught. (`e-sdlc` also teaches STRIDE — different angle, program vs tooling; not duplication.) | (a) §4 builds sketch_sast.py — Python used, no prereq → added `a-python-security`. (b) §2's "Stage B vulnerability classes cold" has no Stage B prereq — checked: this is the guidebook's standing block-assumption convention (`e-sdlc` §2 does the same: "major vulnerability classes and their fixes (Stage B)"); knowledge is taught in Stage B, so not an orphan; left as-is, flagged for coordinator standardization (see Gaps). | §5: success test extended to all six STRIDE letters (was S,T,I,E — R/D empty was a silent pass). §9: diff review must be on the reader's own recent commit/PR, not the walkthrough's review.diff. |
| d-exploit-concepts | 2, 3 | None — flaw→instruction-pointer taught at binary level; ASLR/DEP/canaries (+RELRO/FORTIFY/CFI) taught with per-mitigation "what it stops / doesn't stop"; hands-on sent to pwn.college with the no-solutions rule. | (a) **§2 claimed "You can read C and follow a pointer (`a-reading-code`)" — false.** `a-reading-code` teaches JavaScript + SQL reading; a full-text search confirmed NO lesson in the guidebook teaches C (no strcpy/malloc/#include matches anywhere). Fixed both ways: §2 now states what a-reading-code actually delivers (systematic unfamiliar-code reading), and §3 gained "The C you need" foundation (pointer / buffer / strcpy-copy-without-measuring, concept level, no exploit code). (b) `d-redteam-concepts` was a prerequisite but is never used or mapped — appears only in §10 "Leads to" → removed from frontmatter (judgment call, see Gaps). (c) §2's safety line told readers to "re-read `b-authorization-scope`" without it being a prereq → added (the lesson's safety concept). | §8 Q1 was pure recall of the lesson's thesis sentence → rewritten as prediction (local-variable-only overwrite: what can/can't the attacker do, what second flaw reaches the instruction pointer). §5: shopping-list test — most-hardened list must be strictly longer, every item names the forcing mitigation. |
| d-malware-analysis | 1, 2, 3 | **"Sandboxing" was named in the §5 scope but never taught** — the lesson mentioned "sandbox evasion" twice but never the sandbox concept. Added "Sandboxing: dynamic analysis, automated" to §3 (automated detonation → behavioral report; triage-speed vs manual lab; evasion still applies; absent-behavior is only as trustworthy as the detonation). Static/dynamic, behavioral indicators, REMnux/FLARE VM lab, analysis-not-authoring: taught. | (a) §4 writes entropy.py / scan*.py — Python used, no prereq → added `a-python-security`. (b) `c-log-sources` was a prerequisite but unmapped in §2 → added the mapping line (dynamic analysis produces exactly those streams). `d-redteam-concepts` dependency verified genuine (C2 concepts + now the goal-tactics paragraph). | §9: triage sheet must be on a sample the reader crafts themselves (not the walkthrough's invoice-reminder.exe) + YARA rule for their invented family with positive/negative logs. |
| d-cloud-security | 3 | None — shared-responsibility line (with why-it-sits-there), cloud IAM (least privilege, evaluation logic, escalation paths), five classic misconfigurations each with happen/find/detect, Prowler + ScoutSuite reader-side against the reader's own account: all taught. | All three prereqs verified genuine: `b-ssrf` teaches the IMDS/metadata angle the lesson depends on ("why instance metadata matters" — confirmed in b-ssrf §3); `e-risk-assessment` teaches the risk/finding write-up format (threat×vuln→impact, responses, controls, one-page report — confirmed); `a-tcpip-ports` for firewall rules. No Python scripting in §4 (JSON + CLI only) → no prereq change. Cleanest chain of the six. | §5: "second reader" → alone-verifiable (saved Cloudsplaining output + no-unexplained-terms chain check). §9: added a fourth policy the reader writes for a real role (CI deploy / auditor / backup), scanned before/after. |

---

## Lens 2 detail: the prereq-chain findings

**Verified genuine (read the prereq, confirmed it delivers):**
- `c-incident-response` → d-dfir-deep: teaches NIST SP 800-61 **Rev. 3** (April 2025, CSF 2.0 Community Profile), full lifecycle with the evidence-before-action discipline. The scope's "IR lifecycle per NIST SP 800-61 current revision" is satisfied through this prereq.
- `e-sdlc` → d-appsec: teaches the secure-SDLC shape (phases, per-phase gates, SSDF) that §2 claims.
- `d-malware-analysis` → d-exploit-concepts ("binary structure basics — sections, imports, entropy": PE sections, IAT, entropy 0–8 — confirmed in §3) and → d-dfir-deep ("what an implant looks like": capability sketch injection+C2 — confirmed).
- `b-ssrf` → d-cloud-security: the IMDSv2/PUT-token mechanics §2 depends on — confirmed in b-ssrf §3.
- `e-risk-assessment` → d-cloud-security: finding write-up format (risk register rows, responses, controls by type, one-page report) — confirmed in §3.
- `c-sigma-detection` (cross-ref, not prereq) → d-dfir-deep/d-redteam-concepts/d-malware-analysis: teaches Sigma rule writing end to end (walkthrough writes and saves a rule with all spec fields) — confirmed; the new §3 sketch's field list is grounded in it.

**Fixed:**
1. Python scripting used-but-unlisted in four walkthroughs → `a-python-security` added to d-redteam-concepts, d-dfir-deep, d-appsec, d-malware-analysis (d-exploit-concepts already had it; d-cloud-security needs none). Convention check: `b-deserialization` already lists it for the same reason — this matches existing practice.
2. d-dfir-deep §3's two `d-redteam-concepts` references (beaconing, ATT&CK behavior language) → added to its frontmatter.
3. d-exploit-concepts' false "read C / follow a pointer (a-reading-code)" claim → §2 corrected to what a-reading-code actually teaches; missing C foundation added to §3 ("The C you need": pointer, buffer, strcpy-without-measuring). **No lesson in the guidebook teaches C** — this was an orphan assumption, now closed in-lesson.
4. d-exploit-concepts' unused `d-redteam-concepts` prereq → removed (it appears nowhere in §2–§9; §10 already leads to it, which is the honest relationship).
5. d-exploit-concepts' "re-read b-authorization-scope" pointer → `b-authorization-scope` added to frontmatter (the safety concept the lesson invokes).
6. d-malware-analysis' unmapped `c-log-sources` prereq → §2 mapping line added.

**Noted, not changed:**
- d-appsec's "Stage B vulnerability classes cold" (no individual b-* prereqs): matches `e-sdlc`'s standing block-assumption convention; knowledge exists in Stage B. Coordinator should standardize whether Stage D lessons carry block assumptions or explicit b-* prereqs.
- d-exploit-concepts prereq removal (finding 4 above) is a judgment call — flagged for coordinator ratification in case the map intends a soft dependency.

No other-stage frontmatter was touched. No other-stage bodies were touched (all fixes landed in my six lessons).

---

## Lens 3 detail: exercise rewrites

Counts kept: §8 still 5 questions each; §5 and §9 one block each. Every §8 set re-judged: all questions across the six lessons now require explaining/predicting/applying — the single recall question found (d-exploit-concepts Q1) was rewritten.

**Worst before/after — d-exploit-concepts §8 Q1** (the only recall question in the batch):

Before:
> 1. In the flaw-to-control chain, what exactly does overwriting the return address buy the attacker — and why is "control of the instruction pointer" the sentence everything else hangs on?

After:
> 1. A program has a stack overflow that overwrites a *local variable* but stops short of the return address. Explain what the attacker can do with this primitive and what they cannot — then name the second flaw (or second step) they would need to reach control of the instruction pointer, and why.

Why it was the worst: the before-question is answered by quoting §3's thesis sentence verbatim ("control of the instruction pointer becomes arbitrary code execution") — zero transfer required. The after-question forces the reader to apply the stack-layout model to a *weaker* primitive than the lesson's example, reason about its limits, and compose it with a second flaw — prediction, not retrieval.

**Other rewrites (all "second reader / stranger" tests replaced with alone-verifiable ones):**
- d-redteam-concepts §5: was "a second reader can take your mapping…"; now each mapping must quote the ATT&CK Detection-section line naming the data source — checkable alone against the primary source.
- d-dfir-deep §5: was "a stranger reading only your memo…"; now the memo-away self-check with mandatory timeline-line citations per claim (three claims, three citations).
- d-cloud-security §5: was "a second reader can follow your three steps…"; now saved Cloudsplaining output (zero findings) plus a no-unexplained-terms chain check.
- d-dfir-deep §9, d-redteam-concepts §9, d-appsec §9, d-malware-analysis §9, d-cloud-security §9: artifacts re-centered on reader-generated material (their §5 extension, their own commit, their invented sample, their own policy) instead of repackaging walkthrough outputs.
- d-appsec §5: success test now demands all six STRIDE letters (R and D can no longer come up empty silently).
- d-exploit-concepts §5: shopping-list comparison — most-hardened list strictly longer, every item names its forcing mitigation.

**§8 sets judged solid, unchanged:** d-redteam-concepts (all five explain/predict — Q3's jitter→CV prediction is the strongest in the batch), d-dfir-deep, d-appsec, d-malware-analysis, d-cloud-security.

---

## Sources staged

`guidebook/reports/sources-add-3-D.csv` — **header-only, zero rows.** Deliberate: every addition is (a) a definition/rationale derived from the lesson's own content, (b) the Sigma sketch grounded in `c-sigma-detection`'s own spec field list, (c) standard CS vocabulary (pointer/buffer/strcpy semantics, sandbox concept), or (d) prereq/exercise restructuring. No new external factual claims were introduced, so per the DEb precedent no rows were staged. `sources.csv` untouched.

## Verification

- All 6 lessons: exactly ten `^## ` sections each; `lesson_id:` and `prerequisites:` present in all 6; frontmatter structure otherwise untouched.
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`): zero hits across all 6 files.
- Currency: no `$<digit>` in any of the 6 files.
- Levels: unchanged on all 6 (additions are paragraphs/definitions/exercise rewrites at existing levels).
- No walkthrough steps added or modified → no runs needed; `pgrep` clean (one transient PID, gone on recheck; no test servers started).
- `build_site.py` NOT run per task instructions (validate own files only — done above).
- Nothing committed, nothing pushed. Untouched: build_site.py, STATE.md, gaps.md, map.md, sources.csv, runs/, all other stages' files.

## Gaps / for the coordinator

1. **Prereq-list judgment call:** removed `d-redteam-concepts` from d-exploit-concepts prerequisites (unused — appears only in §10 Leads to). Ratify or revert.
2. **Block-assumption convention:** d-appsec (and `e-sdlc`) assume "Stage B" as a block with no individual b-* prereqs. Standardize guidebook-wide: block assumptions vs explicit b-* lists.
3. **No lesson teaches C.** The d-exploit-concepts fix teaches the minimal C inline. If the curriculum wants C literacy earlier (e.g., in `a-reading-code`), that's a Stage A scope decision, not this pass's.
4. `sources-add-3-D.csv` is header-only by design (no new external claims) — merge is a no-op, kept for the paper trail.
