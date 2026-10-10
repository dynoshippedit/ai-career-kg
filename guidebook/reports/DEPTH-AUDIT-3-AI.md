# Content-depth audit, third pass — AI track (8 lessons)

Auditor: subagent 3e7cc7a5 · 2026-10-10. Dino's order: "go deeper on the lessons again."
Two passes already applied the jargon/why/detection/reading-guidance lenses (DEPTH-AUDIT-2.md,
AI track §508–594 — skimmed, not repeated). This pass uses three NEW lenses:

1. **Scope completeness** — §5 of SECURITY_GUIDEBOOK_BRIEF-2.md ("AI security track")
   extracted verbatim; every named sub-item checked as TAUGHT vs name-dropped.
2. **Prerequisite chain integrity** — every lesson's frontmatter `prerequisites` re-read;
   checked for (a) forward references, (b) orphan assumptions, (c) prereqs that don't
   deliver what they promise.
3. **Exercise quality** — §8 must need EXPLAINING/PREDICTING (recall rewritten);
   §5 success tests must be reader-verifiable (vague rewritten); §9 artifacts must
   evidence UNAIDED application (walkthrough-redos rewritten). Counts kept.

**Result: 4 of 8 lessons edited (7 edits). Lens 2 fired 4×, Lens 3 fired 3×,
Lens 1 fired 0× — the §5 scope is genuinely covered (evidence below).**
No level changes. No walkthrough steps added, no test servers started, no commits, no push.

## Lens 1: §5 scope checklist (verified per sub-item)

Extracted from brief §5 "AI security track" (site-run SECURITY_GUIDEBOOK_BRIEF-2.md):

| §5 sub-item | Lesson | Taught? |
|---|---|---|
| how LLM applications are built AND where they are attacked | ai-llm-architecture | Yes — tokens/embeddings/transformer/RAG/tools/agent loop built up in §3; six attack surfaces marked on the worked data-flow; each mapped to a Top 10:2026 entry in the walkthrough step 6 |
| OWASP LLM Top 10, LLM01–LLM10 | ai-prompt-injection (LLM01) + ai-llm-top10 (LLM02–10) | Yes — codes re-verified this session against the primary repo README (github.com/GenAI-Security-Project/GenAI-LLM-Top10, fetched 2026-10-10): LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Excessive Agency, LLM04 Supply Chain, LLM05 Data and Model Poisoning, LLM06 Unbounded Consumption, LLM07 Misinformation, LLM08 Hidden Context Exposure, LLM09 Vector and Embedding Weaknesses, LLM10 Improper Output Handling — match the lessons' edition note exactly; published 2026-08-04 (existing sources.csv rows 7/77/341 already ledger this; no new row needed) |
| attacks AND defenses in the build pipeline | ai-pipeline | Yes — five stages, each as attack→defense pair (poisoning→manifest, build tampering→provenance+hermetic, substitution→keyless signing, registry abuse→immutable tags/digest pins, compromised builder→adversarial CI gate); "each attack taught with its defense" holds per stage |
| threat modeling an AI system | ai-threat-modeling | Yes — data-flow mapping, five AI trust boundaries, STRIDE adapted per letter with AI meaning, ATLAS mapping, risk register with treatments; full Harborlight worked case |
| AI supply chain (model AND dataset provenance, signing) | ai-supply-chain | Yes — hashes/provenance/signatures taught as three mechanisms; model signing via Sigstore keyless; dataset provenance taught (§3 "training-data references", AIBOM dataset fields, worked handoff 2 records fine-tuning dataset hash+source, §6 "Forgetting the data"); dataset-manifest depth lives in ai-pipeline Stage 1, which this lesson's prereq chain reaches (cross-ref, not duplication) |
| governance (NIST AI RMF, Generative AI Profile, ISO/IEC 42001, EU AI Act) | ai-governance | Yes — RMF four functions with MEASURE/MANAGE rationale; GenAI Profile twelve categories; Act's five tiers + GPAI layer as concepts with Art. 43/65 definitions verified; 42001 as paid one-liner per brief |
| SEC598 subject area (automation for offense, defense AND cloud) | ai-sec-automation | Yes — offense: red-team AI agents + continuous emulation; defense: LLM-assisted detection engineering, SOAR playbooks, agentic investigation; cloud: IaC + policy-as-code + drift detection — each paired with defense and "what the defender detects" |
| SEC535 subject area (AI-enabled attack techniques) | ai-sec-automation | Yes — five concepts (recon at scale, phishing/deepfakes, web exploitation, patch diffing, AI malware), each with defense + concrete telemetry; taught as concepts, no attack tooling |
| Governing AI: AIGP + AAISM subject areas (AI law/policy, risk management, controls) | maps + lessons | Yes, via integration — the AIGP light map points domain II (laws/standards/frameworks) at ai-governance + e-cyber-law, domains I/IV at ai-governance; the AAISM map points domain 1 at ai-governance, domain 2 at e-risk-assessment + ai-threat-modeling, domain 3 at ai-llm-architecture + ai-pipeline + ai-supply-chain. The subject-area *content* (law/policy, risk management, controls) is taught in those lessons; the maps are the binding. No lesson-body change warranted (would duplicate the maps) |

Lens 1 fired nowhere. The agentic Top 10 stays out of scope per pass 2's gaps.md decision.

## Per-lesson table

| Lesson | Lenses fired | Missing §5 sub-items + what added | Broken prereq chains + fixes | Rewritten exercise sections |
|---|---|---|---|---|
| ai-prompt-injection | L2 | none | **(a) Circular forward reference.** §2 asserted "You understand the LLM application stack… (the `ai-llm-architecture` lesson)" with prereqs `[]` — but ai-llm-architecture lists ai-prompt-injection as ITS prereq, so the reference can't be fixed by adding a prereq (would cycle). Fixed the reference instead: §2 now says the stack is taught in §3 from scratch, no prior AI lesson assumed, and ai-llm-architecture is read next. | none — §8 all explain/predict; §5 success test concrete (before/after report + residual-risk statement); §9 is a new-app red-team report |
| ai-llm-architecture | — | none | Checked clean: prereq ai-prompt-injection delivers exactly what §2 claims (context-window mechanism §3; tool-permissions-in-code §3 defense 1). All stack terms taught in-lesson. | none — §8 Q1–Q5 all explain/trace/predict; §5 success test checkable (5 boundaries, 6 rows, specific impacts); §9 is a new app's diagram, not the walkthrough's |
| ai-llm-top10 | — | none | Checked clean: both prereqs deliver §2's claims (LLM01 not repeated; stack layers pointable). Inline glosses cover non-prereq terms (pickle, fine-tuning, typosquatting, inversion). | none — §8 all explain/apply (Q1/Q3/Q5's "name the entry" is one clause inside explain-and-fix questions); §5 requires three real incidents with primary sources; §9 is the incident-mapping write-up |
| ai-pipeline | L2 | none | **(c) Prereq without a stated promise.** `a-git-github` was in frontmatter but §2 never said what it delivers (the lesson leans on commit-hash identity and movable tags throughout §3–§4). Added §2 bullet: commits as content-addressed snapshots; tags move — which is why Stage 4 pins digests. Verified a-git-github teaches hash-of-contents identity and branch-as-pointer (it does not teach tags — the lesson defines "immutable tag" inline where used, so no gap). | none — §8 all apply/explain; §5 success test concrete (flags poison, 3 clean runs, one-paragraph complement-not-replacement statement); §9's new screening step is the unaided core |
| ai-supply-chain | L2, L3 | none | **(c) Same as ai-pipeline.** `a-git-github` in frontmatter, no §2 promise. Added §2 bullet: commit hash names exact bytes vs branch as movable pointer — why the lesson pins hashes and distrusts "latest." | **§8 Q5 was pure recall** (before/after quoted in full below). Rewritten as predict+explain. §5 §9: §5's "or the walkthrough's `model_dir`" gave walkthrough-redo equal billing — tightened to "a model artifact you did not build in the walkthrough — a real download if you have one; `model_dir` only as a last resort." The admission-policy script (new work) stays the artifact's core |
| ai-threat-modeling | L2, L3 | none | **(c) Prereq without a stated promise.** `e-risk-assessment` in frontmatter but §2 never mentioned it, though §3's register method ("likelihood and impact in words… the `e-risk-assessment` method") depends on it. Added §2 bullet: likelihood/impact in words, four treatments, owned residual risk. Verified e-risk-assessment teaches all of it (qualitative scales, mitigate/transfer/accept/avoid, owners, residual risk). | **§9 was a walkthrough redo.** It asked for the complete threat-model document for the Harborlight assistant — the §4 walkthrough's own case — while §5 asks for the Meridian pipeline. Rewritten so §9's artifact is the §5 product (Meridian pipeline threat model). Quote below |
| ai-sec-automation | — | none | Checked, no breaks: all three prereqs deliver §2's stated claims (stack/agent loop/RAG; 2026 risks; c-soc-triage's eight-stage workflow — verified in c-soc-triage §3). Two named pointers to non-prereq Stage C lessons ("the KEV discipline from `c-vuln-ecosystem`", "the incident-response lifecycle from `c-incident-response`") are cross-refs with named sources, not assumed knowledge — recorded, not fixed. | none — §8 all explain/judge/tradeoff (Q1/Q3's "name" clauses sit inside analysis questions); §5 success test stranger-checkable; §9 is a different chain's detection plan |
| ai-governance | — | none | Checked, no breaks: both prereqs deliver §2's claims (ai-llm-top10's risk vocabulary; e-risk-assessment's register format/scales/treatments — verified). §3's use of ai-llm-architecture §5 diagram and ai-prompt-injection's tool-approval rule arrives TRANSITIVELY via ai-llm-top10 (which requires both) — chain intact, recorded as transitive rather than fixed. | none — §8 all explain/rewrite; §5 success test stranger-checkable with a "best practices" fail clause; §9 is a different fictional deployment's memo+register |

## Rewritten exercises — before/after (worst one quoted in full)

**ai-supply-chain §8 Q5 (recall → predict/explain):**

Before:
> 5. A vendor says their model registry "signs all models." List the four verification checks from §3 and explain which one fails if the team never wrote the admission policy.

After:
> 5. A registry "signs all models," but no admission policy was ever written — deploys pull whatever the registry serves. An attacker publishes a backdoored model under a lookalike publisher identity and signs it properly with their own key. Predict which of the four §3 verification checks catches this, explain why the other three pass, and explain why the catching check is useless unless it runs in the deploy path.

Why this was the worst: it was the only pure-recall question across all 40 check-yourself items
in the track ("list the four checks"). The rewrite forces the reader to run the checks against
an attack (identity check catches the lookalike; byte-signature, chain-to-root, and Rekor-entry
checks pass silently) and to state the deploy-path rationale — the lesson's actual thesis.

**ai-threat-modeling §9 (walkthrough redo → unaided application):**

Before:
> **Artifact:** the complete threat-model document for the Harborlight assistant — data-flow diagram (photo/scan of the whiteboard is fine), trust-boundary statements, STRIDE table, ATLAS mappings, and the risk register with treatments, owners, and the self-review checklist signed off.

After:
> **Artifact:** the complete threat-model document for the Meridian pipeline from §5 — data-flow diagram (photo/scan of the whiteboard is fine), trust-boundary statements, STRIDE table, ATLAS mappings, and the risk register with treatments, owners, and the self-review checklist signed off.

The Harborlight assistant is the §4 walkthrough's own worked case — the old artifact asked the
reader to reproduce the walkthrough. The §5 task threat-models the Meridian support-model
pipeline (dataset → manifest → training → attestation → registry → gate → deploy), which the
walkthrough never models; the artifact now evidences unaided application to a new system.

**ai-supply-chain §5 (tightened, minor):** "Take any model artifact on your machine (a real
download, or the walkthrough's `model_dir`)" → "Take a model artifact you did not build in the
walkthrough — a real download if you have one; the walkthrough's `model_dir` only as a last
resort." The admission-policy script (exits non-zero unless hashes match + signature stub)
remains the unaided core.

## Prereq-chain notes for the coordinator (no frontmatter changed anywhere)

- No cross-stage frontmatter changes are needed. All four prereq fixes were §2 body
  additions in AI-track lessons; no other stage's files were touched.
- ai-prompt-injection's prereqs stay `[]` — the circular reference was fixed by rewriting
  the §2 claim, not by adding ai-llm-architecture (which would create a prereq cycle).
- ai-governance's transitive dependencies (ai-llm-architecture, ai-prompt-injection via
  ai-llm-top10) are intact; flagging in case the coordinator wants them listed explicitly —
  I did not add them (redundant with the transitive chain).
- ai-sec-automation's KEV (c-vuln-ecosystem) and IR-lifecycle (c-incident-response)
  pointers are named cross-refs to Stage C lessons the reader has already passed; no action.

## Orphan assumptions found: none

Every concept used-but-not-defined was traced: either defined inline (SLSA, hermetic,
in-toto, predicate, dwell time, SOAR/EDR/IdP/ASN/NetFlow/CT-log glosses), taught by a
(direct or transitive) prerequisite, or named with its source lesson (KEV, IR lifecycle,
pickle→ai-supply-chain). Nothing is assumed from nowhere.

## Sources staged

`sources-add-3-AI.csv` — not created. No new external factual claims were added in this
pass (all edits are §2 prereq-promise bullets referencing already-taught lessons, and
exercise rewrites). The one in-session verification — OWASP LLM Top 10:2026 codes/titles
against the primary repo README (2026-10-10) — re-confirms existing sources.csv rows
7, 77, 341; no new row warranted.

## Verification

- All 8 lessons: exactly ten `^## ` sections; `lesson_id:` present in all 8; frontmatter
  values untouched (prerequisites lists byte-identical before/after).
- Banned voice words (guaranteed, job-ready, undeniable): zero hits across all 8 files.
- Currency: no `$<digit>` in new or existing copy.
- `build_site.py` NOT run per orders (validate-own-files only).
- pgrep: one transient PID matched during the check, gone on re-query — no test servers
  were started by this pass (no walkthrough steps added; all edits are §2/§5/§8/§9 prose).
- NOT committed, NOT pushed. build_site.py, STATE.md, gaps.md, map.md, sources.csv,
  runs/ untouched. No other stage's files touched.

## Gaps not closed (coordinator-owned)

- OWASP's separate Top 10 for Agentic Applications (2026) remains outside §5 scope per
  pass 2's gaps.md decision.
- ai-sec-automation §7's paid-course primary leads (sans.org/sec598, /sec535) stand per
  pass 2; the brief's SEC598→GASAE / SEC535→GOAA correction is the anchor and the
  lesson uses it.
