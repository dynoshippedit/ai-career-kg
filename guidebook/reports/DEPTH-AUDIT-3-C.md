# Depth audit 3 — Stage C batch (three new lenses)

Auditor: subagent 857d7d0d · 2026-10-10 ~02:00–03:30 EDT.
Standard: brief §1 (first-principles mechanism), §5 (the Stage C checklist), §6 (ten ## sections in order), §7 (free-only, ≤3 resources, no hype).
Method: all 10 lessons re-read end to end against the THREE new lenses. Pass 2 (DEPTH-AUDIT-2-C.md — 28 jargon terms unpacked, why-paragraphs, §7 filler replacements, one real sigma-cli run) was deliberately not repeated; its additions were treated as settled ground and verified intact. Every prerequisite lesson named in a frontmatter `prerequisites` list was read or grep-audited for what it actually teaches.

Verdict: **all 10 lessons deepened.** Lenses fired 20 times total. No level changes (levels stay honest). No padding — every addition is a lens finding with a specific location.

## Per-lesson lens table

| Lesson | Lens 1 (scope completeness) | Lens 2 (prereq chain) | Lens 3 (exercises) |
|---|---|---|---|
| c-cvd | — (§5 CVD bullet complete) | — (b-methodology delivers) | Q1, Q5 rewritten |
| c-cve-program | — (§5 CVE bullet complete) | KEV forward-ref gloss added | Q2 rewritten; §5 success test sharpened |
| c-cvss | — (§5 CVSS bullet complete) | — (c-cve-program delivers; EPSS/KEV pointers labeled) | §9 rewritten (walkthrough-redo closed) |
| c-incident-response | n/a (not in §5 checklist) | Sigma forward-ref fixed | §9 rewritten (the "or" removed) |
| c-log-sources | n/a | a-tcpip-ports overpromise fixed | §9 rewritten (invented story required) |
| c-public-track-record | **impact chain taught** (was the §5 gap) | b-sqli ref made non-blocking | §5 success test rewritten (peer removed) |
| c-sigma-detection | n/a | **YAML primer added** (orphan assumption) | §9 rewritten (spray rule specified) |
| c-soc-triage | n/a | 2 fixes (b-session-auth overpromise; log-sources forward ref) | §9 rewritten (invented cases are the proof) |
| c-vuln-ecosystem | **CAPEC concretized** (CWE-89↔CAPEC-66); "used together" scoped honestly | — (c-cvss, c-cve-program deliver) | Q2 rewritten |
| c-ai-tooling | **CVP primary fetched** — gap closed; "How the trust is enforced" added | **ai-governance dropped from prereqs** (Stage E graph bug) | Q2, Q3 rewritten; §5 fit-check checklist |

## Lens 1 — scope completeness (against the §5 checklist)

Checked every named sub-item of each §5 bullet; the finding is *taught*, not name-dropped.

- **CVD (c-cvd): complete, no firing.** security.txt-first contact order taught with fallbacks and documentation discipline; private reporting (OpenSSF report structure); timeline negotiation (30–90 day range, Project Zero 90-day clock, adoption wait); responsible publication (advisory draft, deployer-facing); good case (Heartbleed) and bad case (2018 zero-day drops) both worked; OpenSSF finder guide and CERT/CC guide both in §7 with read/skip guidance.
- **CVE (c-cve-program): complete, no firing.** What a CVE is, what a CNA does (incl. Roots, CNA-LR, 555 count as of Oct 2026), the five-step request path, Record Format 5.2.0 structure, credits field with `type: finder`, the independently-fixable bar.
- **NVD (c-vuln-ecosystem): complete, no firing.** What NVD adds (NIST score, CWE, CPE mappings); the 2026-04-15 prioritized-only change with OIG government confirmation and the honest "no NIST-direct announcement page" sourcing note; the three-place sourcing order (CNA record → NVD enrichment → ADP/community); the "Not Scheduled means not analyzed" rule.
- **CVSS (c-cvss): complete, no firing.** v3.1 and v4.0 metric groups taught by hand (equations run locally, MacroVectors run via FIRST's reference implementation); three real CVEs scored in both versions against FIRST's official examples; disagreement mechanisms named (AT split, Threat group, VC/VI/VA impact model); Threat-replaces-Temporal and Supplemental both covered.
- **CWE/CAPEC/KEV/EPSS (c-vuln-ecosystem): fired once.** CWE, KEV, EPSS were taught with concrete uses; CAPEC was abstract ("catalog-level treatment here; the lesson sends you to capec.mitre.org"). **Added:** the concrete pair — **CWE-89** (Improper Neutralization of Special Elements used in an SQL Command) as the weakness, **CAPEC-66** (SQL Injection, Standard abstraction — verified on capec.mitre.org 2026-10-10, sources-add-3-C.csv) as the attack pattern, reading as one sentence (*CWE-89 in the search endpoint, attacked via CAPEC-66's quote-injection flow*), plus the honest scoping note that CAPEC doesn't rank the queue — the prioritization trio is CVSS+EPSS+KEV, while CWE/CAPEC are the taxonomy that makes the queue legible (Top 25 for systemic fixes, CAPEC patterns for detection mapping).
- **Track record (c-public-track-record): fired once.** Root cause, remediation, and honest limits were taught; **impact chain** — named in the §5 bullet — was not taught as a structure. **Added** item 5 to the anatomy list: *primitive → capability → consequence → business impact*, each link needing its own evidence, "the classic failure is proving link one and claiming link four"; the worked example now claims link two and marks three/four untested. (List renumbered 1–7; walkthrough self-review checklist updated to ask "impact honest — and chained, with unproven links marked?")
- **AI tooling (c-ai-tooling): fired twice.** (a) The §5 bullet's open item is closed: the CVP announcement primary URL (anthropic.com/news/cyber-verification-program) was fetched in-session 2026-10-10 — all tier facts primary-confirmed (three tiers, Defense admitting individual researchers with reported-vulnerability records, Red Team orgs-only, Specialized with US-government review, CyScenarioBench 0/50 → 46-blocked-4/50 → 34/50 = 67.6% no-safeguards equivalence, Glasswing 129,000 / 5,500 / 33,000+ with fivefold-undercount caveat, the unblocked-task list). §7 item 1's "gap, stated plainly" note replaced with the verified-primary entry; dateline and footer updated. (b) **Added** "How the trust is enforced" (§3): applicant verification + proof of tier security controls + mandatory data retention for misuse monitoring until Enterprise Frontier Safeguards ship — the accountability mechanism behind the orgs-only Red Team gate, and the "verified *and* watched" distinction from a credential.

## Lens 2 — prerequisite chain integrity

Every lesson in each frontmatter `prerequisites` list was checked for (a) forward references, (b) orphan assumptions, (c) prereqs that don't deliver. Six breaks found, all fixed in the dependent lesson (no prereq-list shuffling except the one genuine graph bug, documented below).

1. **c-soc-triage §2 ← b-session-auth: prereq didn't deliver what was promised.** The bullet claimed b-session-auth teaches "password spray, session theft, impossible travel as a signal." Grep-audit of b-session-auth: it teaches fixation, predictable tokens, brute force vs credential stuffing as concepts, and the honest limit that a stolen post-login cookie bypasses MFA — it does *not* teach password spray as an attack shape, session theft, or impossible travel as a defensive signal. **Fix:** rewrote the bullet to claim only what b-session-auth delivers, and to state that the defensive-signal reading (impossible travel, the spray shape) is taught in the triage decision trees themselves.
2. **c-soc-triage §4 ← c-log-sources: forward reference outside the prereq list.** Walkthrough step 6 said "this is the same host that appears in the log-sources lesson's DGA burst" — but c-log-sources is not a prerequisite (its own prereqs are a-linux-cli + a-tcpip-ports; the stage order has triage first). **Fix:** the enrichment stage now pulls the DNS burst explicitly inside the triage event set, with c-log-sources demoted to a labeled pointer ("teaches the DNS source behind this pivot; you don't need it to run the tree").
3. **c-log-sources §2 ← a-tcpip-ports: prereq overpromised.** The bullet claimed a-tcpip-ports teaches "5-tuple, ports, what encryption hides and what it doesn't." Audit: it teaches the socket pair (four numbers), ports, handshake states — no 5-tuple term, nothing on encryption visibility (content vs envelope). **Fix:** bullet now claims the socket pair/ports/handshake and states that the 5-tuple's fifth field and the encryption distinction are this lesson's own additions.
4. **c-sigma-detection §2: orphan assumption.** "You can read YAML without fear" — YAML is taught nowhere in the guidebook and by no prerequisite. **Fix:** the missing foundation added in-lesson — a five-line YAML primer (key: value, indentation-is-nesting, `- ` lists, `|` modifiers) that the walkthrough's field-by-field validation then checks.
5. **c-incident-response §3 ← c-sigma-detection: forward reference.** Recommendation (2) referenced "the c-sigma-detection 'on your own' rule" — c-sigma-detection is a sibling (prereqs: c-log-sources, c-soc-triage), not a prerequisite. **Fix:** the recommendation now states the spray-shape rule fully in-lesson (multiple 4625s, one IP, ≥3 users, short window) with c-sigma-detection as a labeled pointer for the rule format.
6. **c-cve-program §3 → c-vuln-ecosystem: forward reference to a later lesson.** The KEV catalog was named twice ("scanners, advisories, the KEV catalog...") before it is taught — c-vuln-ecosystem comes *after* c-cve-program (its prereqs include c-cve-program). **Fix:** one-line gloss at first mention (CISA's list of CVEs with confirmed active exploitation — the catalog c-vuln-ecosystem teaches in full). The §5 "pick any CVE from the KEV catalog (see c-vuln-ecosystem)" pointer was already labeled; it now lands on a reader who isn't lost.
7. **c-ai-tooling prereqs: genuine graph bug — ai-governance removed.** ai-governance's own prereqs are [ai-llm-top10, e-risk-assessment] — a **Stage E** lesson inside a Stage C lesson's transitive closure. Audit of c-ai-tooling: no ai-governance concept is used anywhere in §§1–9 (its §2 bullets use only c-public-track-record and c-cvd). The prereq promised governance foundation the lesson never consumes, and silently forced Stage E into Stage C. **Fix:** prereqs are now [c-public-track-record, c-cvd]; ai-governance stays as the §10 "Leads to" pointer ("governing the systems, not just wielding the tooling"), which is all the lesson ever needed from it. This is the one prereq-list change in the batch, and it removes a false dependency rather than hiding a missing one.

Chains verified clean (prereq delivers what the dependent claims): c-cvd ← b-methodology (PTES reporting phase, "prove findings reproduceably", report outline — confirmed); c-cve-program ← c-cvd; c-cvss ← c-cve-program (EPSS/KEV mentions are labeled forward pointers, not assumptions); c-incident-response ← c-soc-triage + c-log-sources; c-vuln-ecosystem ← c-cvss + c-cve-program; c-public-track-record ← c-cvd + c-cve-program + c-vuln-ecosystem + b-methodology (the b-sqli worked-example reference is self-contained — the finding is restated inline; §4 step 1 now says "re-read the b-sqli run log *if you did that lesson* — otherwise use the facts as restated in section 3"); c-sigma-detection ← c-log-sources + c-soc-triage; c-soc-triage ← a-linux-cli (grep/awk/sort/uniq -c confirmed) + b-session-auth (per fix 1); c-log-sources ← a-linux-cli + a-tcpip-ports (per fix 3).

## Lens 3 — exercise quality

Standard: §8 questions must need EXPLAINING/PREDICTING (never recall); §5 success tests verifiable by the reader alone; §9 artifacts must evidence UNAIDED application (never the walkthrough set). Rewrites below; the worst rewritten item per lesson is quoted before/after.

- **c-cvd** — Q1 and Q5 were recall (recite the contact order; name the day-14 step). Q5 was the worst:
  - Before: "Your disclosure timeline hits day 14 of vendor silence. Name the exact next step from this lesson's walkthrough — and what you must not do."
  - After: "Your disclosure timeline hits day 14 of vendor silence, and a colleague urges you to publish the proof of concept "to light a fire under them." Using the CERT principles from this lesson, explain the two harms that publication would cause, what the walkthrough prescribes instead, and why the prescribed step preserves your leverage better than the PoC would."
  - Q1 rebuilt as a conflict case (bouncing security.txt vs a different SECURITY.md address — which first, what changes in documentation when the first method fails, why the order exists).
- **c-cve-program** — Q2 was walk-the-taught-path recall. Worst was Q2:
  - Before: "You found a flaw in a small vendor's product. The vendor has no security contact and is not a CNA. Walk the request path: what do you try, in what order, and where does MITRE as CNA of Last Resort enter?"
  - After: adds a second researcher about to request through a different CNA; the reader must explain the two failure modes (duplicate IDs; public reservation before coordination) and lay out the path that avoids both. §5 success test sharpened from "would survive a CNA's first read" to the six named fields (product+versions, vuln type, independently-fixable argument, proven impact, dated timeline, contact) — any missing, the worksheet fails.
- **c-cvss** — §8 was already explain-grade; the worst item was §9, which asked for the walkthrough's own calibration vectors (redo-the-walkthrough artifact):
  - Before: "your three hand-scored calibration vectors with metric-by-metric justifications, the run output showing they match the published scores, and the disagreement analysis for CVE-2020-3549."
  - After: the §5 KEV CVE — both versions' vectors with justifications, FIRST calculator confirmation, and the disagreement paragraph taking a position on which version argues more honestly for *that* vulnerability. "The walkthrough's three calibration cases were the training set; this CVE is the test set."
- **c-vuln-ecosystem** — Q2 was list-the-three-places recall. Worst was Q2:
  - Before: "You open an NVD page and see no NIST CVSS score, no CWE, and a "Not Scheduled" label. List the three places you look next, in order, and what each can give you."
  - After: the manager reads "Not Scheduled" as "NIST says it's not serious" — the reader must explain the two errors in that reading first, then walk the ordered fallback with what each source gives that NVD didn't.
- **c-incident-response** — §8 was explain-grade; worst was §9's "the full IR report from the walkthrough (**or** your 'on your own' report)" — the "or" let the reader submit the worked example:
  - Before: "the full IR report from the walkthrough (or your "on your own" report): executive summary, sourced timeline, scope, root cause, ordered containment/eradication/recovery, honest limitations, traceable recommendations."
  - After: the §5 report only — the beaconing case with the reader's three invented post-escalation events. "Not the walkthrough's WS-4417 report — that one was the worked example. This one must be yours: a stranger reading it should not be able to tell which parts came from the lesson."
- **c-log-sources** — worst was §9 ("the source map from walkthrough step 8 plus your invented Sysmon story" — ambiguous which story carries the proof):
  - After: the source map for *the invented Sysmon story* (not the walkthrough's), with initial-access/execution/persistence events cited by ID and a blind-spot column naming what the invented sources genuinely cannot answer. "The walkthrough's map was the template; this one is unaided."
- **c-public-track-record** — worst was the §5 success test, which required a peer (not verifiable by the reader alone):
  - Before: "a peer who has never seen your lab can read the write-up and state the root cause, the confirmation, and the fix — and can point at the exact lines that prove each."
  - After: for each of the seven checklist items, write the line number(s) satisfying it (every item needs ≥1 line number; no line covers >2 items); then redact the title and read only the first paragraph — it must state the root cause with no exploitation detail, or the opening fails the bar.
- **c-sigma-detection** — §8 was explain-grade; worst was §9 (ambiguous which rule — the reader could submit the walkthrough's encoded-PowerShell rule):
  - After: "the §5 password-spray rule bundle — the Sigma YAML (valid against the spec, ATT&CK-tagged), both corpora, the before/after tuning numbers, and the three-line runbook — committed as a detection-as-code bundle. Not the walkthrough's encoded-PowerShell rule: the walkthrough taught the loop; the spray rule proves you can run it on a behavior you weren't handed."
- **c-soc-triage** — worst was §9 (the five walkthrough notes as the artifact):
  - After: the two invented §5 cases — event JSON, the deciding decision-tree branch, triage notes in seen/checked/decided/evidence format — "presented as the handoff you would give a Tier 2 analyst. The five walkthrough notes were the practice set; the two invented cases are the proof: they must exercise branches the walkthrough didn't use, and a stranger must be able to see which branch decided each without asking you."
- **c-ai-tooling** — Q2 was name-the-tiers recall; Q3 was "explain the two caveats" recall of taught caveats. Q3 was the worst:
  - Before: "Anthropic's CyScenarioBench numbers are 0/50, 4/50, 34/50 across the settings. Explain the two caveats a professional attaches before repeating these numbers."
  - After: "A vendor announces its own benchmark showing its access tiers "behave as designed" (0/50, 4/50, 34/50 on CyScenarioBench). Explain what these numbers *can* legitimately tell you about the tier design, what they *cannot* tell you about the model's real-world defensive value, and the one independent check you would want before citing them as evidence the program works."
  - Q2 rebuilt as the three-mistakes peer case (eligibility error, category error about what tiers sort, authorization error). §5 success test converted to the three-item Defense Access fit checklist (vendor-confirmed item; dated timelines; no practice counted as reported) — failing item names next quarter's work.

Counts kept: every §8 still ~5 questions; every lesson keeps §5/§8/§9.

## Sources staged

`guidebook/reports/sources-add-3-C.csv` — 2 rows, both status=verified, both fetched in-session 2026-10-10 (in the repo; parent merges into sources.csv; sources.csv untouched):
1. Anthropic CVP announcement primary (anthropic.com/news/cyber-verification-program) — tier table, eligibility, CyScenarioBench numbers, Glasswing figures, unblocked-task list, data-retention requirement, applicant verification. Closes the open gap from passes 1 and 2.
2. CAPEC-66 primary page (capec.mitre.org/data/definitions/66.html, CAPEC v3.9) — SQL Injection pattern definition, used for the CWE-89↔CAPEC-66 pair.
Existing sources.csv checked — no duplicates (the OIG/EPSS/CVSS-FAQ rows from pass 2 stand; these two URLs are new).

## Verification results

- All 10 lessons: exactly ten `^## ` sections; `^lesson_id:` present in each; frontmatter values intact (only changes: c-ai-tooling `prerequisites` minus ai-governance, c-ai-tooling `dateline` noting the 2026-10-10 primary fetch). No level changes.
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`): zero hits across all 10 files. No currency symbols in new copy.
- Resource counts: no §7 additions — both new facts cite pages already in the lessons' §7 (CVP announcement, CAPEC); every lesson still ≤3 free resources.
- No new walkthrough steps added to any lesson, so no new runs were needed (brief §6: the new worked content is authored analysis, and the two fetched primaries are reads, not executions). `runs/` untouched.
- `pgrep -f "server\.js"`: 0 — clean. No test servers were started by this pass (no CLI work added).
- build_site.py NOT run per task instructions (validate own files only — done above).
- Nothing committed, nothing pushed. build_site.py, STATE.md, gaps.md, map.md, sources.csv untouched. No other stage's files touched (the six prereq lessons were read/grepped only — the fixes went into the Stage C lessons, except the one documented c-ai-tooling frontmatter change).

## Word counts

2636 / 2503 / 2326 / 2447 / 2719 / 2426 / 2317 / 2544 / 2474 / 2671 (c-incident-response and c-vuln-ecosystem remain slightly above the 2,500-word sanity band from pass 2; the band is not a target and the words above it are lens findings — the CAPEC pair, the impact chain, the trust-enforcement section — not padding).

## What I couldn't close / open items for the parent

1. **c-ai-tooling prereq removal (ai-governance).** Done and documented above, but it changes the dependency graph — flagging explicitly in case the coordinator wants the AI-track lead to confirm the intent. The §10 pointer keeps the thematic link.
2. **b-session-auth as a prereq of c-soc-triage.** I fixed the *reference* (the §2 bullet now claims only what b-session-auth delivers). If the coordinator would rather the *foundation* be added — i.e., password spray as an attack shape and impossible-travel-as-signal taught in b-session-auth itself — that's the Stage B batch's call; my fix keeps Stage C honest either way.
3. **a-tcpip-ports and the 5-tuple/encryption wording.** Same pattern: fixed the reference in c-log-sources. If Stage A wants the lesson to actually teach the 5-tuple term and the encryption-envelope distinction, the c-log-sources bullet can be re-tightened — currently it honestly says "this lesson adds what that lesson doesn't teach."
4. **CAPEC-63 vs CAPEC-66.** The lesson uses CAPEC-66 (SQL Injection) as the concrete pair; CAPEC-63 (XSS) would pair with CWE-79 equally well, but one concrete pair was enough — the §7 pointer covers the rest of the catalog.
