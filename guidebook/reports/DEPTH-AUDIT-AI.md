# Depth audit — AI track (8 lessons)

Auditor: subagent ac08c7a7 · 2026-10-10. Brief §1 (level bar), §5 (AI scope), §6 (lesson spec), §7 (evidence/safety/voice) read first. Pad-free rule honored: no lesson flagged for length; all eight sit at 2,299–2,600 words with complete ten-section structures and run walkthroughs.

## Per-lesson audit

| Lesson | Words | Level | Stage | Verdict |
|---|---|---|---|---|
| ai-governance | 2456 | L2 | AI | **SOLID** |
| ai-llm-architecture | 2442 | L3 | AI | **SOLID** |
| ai-llm-top10 | 2600 | L3 | AI | **SOLID** |
| ai-pipeline | 2299 | L3 | AI | **SOLID** |
| ai-prompt-injection | 2377 | L3 | AI | **DEEPENED** (stale cross-references) |
| ai-sec-automation | 2488 | L2 | AI | **SOLID** |
| ai-supply-chain | 2312 | L3 | AI | **SOLID** |
| ai-threat-modeling | 2457 | L3 | AI | **DEEPENED** (wrong 2026 codes) |

### SOLID rationale (the six)

- **ai-governance** — RMF four functions with honest caveats (voluntary; 1.0 revision announced), GenAI Profile's twelve categories used as an action list not trivia, EU AI Act tiers as concepts with the Digital Omnibus amendment noted and dated, ISO/IEC 42001 one-liner as required, plus a worked classification case feeding a six-row risk register with named owners. Walkthrough correctly shaped as authored work products per §6's no-command-line provision. Complete at L2.
- **ai-llm-architecture** — Tokens/embeddings/transformer built from mechanism, six-layer application stack with the trust boundary at each layer, the worked data-flow example counting six attack surfaces, and a deterministic harness walkthrough that re-derives the lesson's claims (prompt assembly with unmarked provenance, policy denial on the poisoned tool call). Meets L3: the reader can decompose an unfamiliar app.
- **ai-llm-top10** — All nine non-LLM01 entries with mechanism + defense each, grouped in data/system/agency families, edition discipline enforced (2026 codes named everywhere, the 2025→2026 renumbering called out with the LLM04:2025/LLM04:2026 trap as an explicit worked example), deterministic classification-drill walkthrough including a real LLM10 command-interpolation demo. L3 bar met.
- **ai-pipeline** — Five stages taught as attack/defense pairs, the LLM04 compromised-builder scenario handled as the lesson's thesis ("provenance proves which build; only testing proves which behavior"), red-team CI gate as the structural fix, honest limit stated (screening catches clumsy poisoning, not careful). Deterministic five-stage walkthrough run. L3 bar met.
- **ai-sec-automation** — SEC598/SEC535 taught strictly as concepts per §7's safety line: every attack concept (phishing/deepfakes, web exploitation, patch diffing, malware/evasion, recon) paired with defense *and* defender-detectable telemetry; no attack tooling named as a how-to; the worked detection plan is a genuine defensive work product with human-in-the-loop gates on every irreversible action; dwell figures labeled illustrative. L2 bar met; no level change needed.
- **ai-supply-chain** — Hashes vs provenance vs signatures taught as a strength ladder with the "hash of a poisoned model is a valid hash" honesty line; Sigstore keyless mechanics with the four verification checks; CycloneDX AIBOM for the incident-response use case; the pickle hazard *demonstrated locally on a labeled file* then the safe-format alternative — exactly the §7 containment standard. L3 bar met.

### DEEPENED (the two) — what was thin/stale and what changed

**ai-threat-modeling** — factually wrong 2026 codes in three places, in an L3 lesson whose job is precise citation:
- §3 STRIDE "Denial of service": Unbounded Consumption cited as **LLM10:2026** → corrected to **LLM06:2026**.
- §3 STRIDE "Elevation of privilege": Excessive Agency cited as **LLM06:2026** → corrected to **LLM03:2026**.
- §5 "On your own": the Meridian pipeline's compromised-builder scenario cited as "the **LLM03** scenario" → corrected to **LLM04** (matches `ai-pipeline`'s own correct statement that LLM04:2026 added the compromised-build-pipeline scenario).
- Verification done in-session: fetched the primary 2026 final directory listing (GitHub, 2026-10-10) — file names confirm LLM03=ExcessiveAgency, LLM06=UnboundedConsumption, LLM10=ImproperOutputHandling. Source rows staged in `/tmp/sources-add-AI.csv`.
- Additionally verified (defensive check, no change needed): every ATLAS technique name used in the lesson is real, confirmed against the primary `ATLAS.yaml` (mitre-atlas/atlas-data, 452,399 bytes, fetched 2026-10-10): AML.T0020 Poison Training Data, AML.T0053 AI Agent Tool Invocation, AML.T0056 Extract LLM System Prompt, AML.T0057 LLM Data Leakage, AML.T0070 RAG Poisoning, AML.T0080 AI Agent Context Poisoning, AML.T0110 AI Agent Tool Poisoning. The lesson's technique-name-only references were *not* fabricated. Row staged in `/tmp/sources-add-AI.csv`.
- No level change; lesson remains L3. Nothing padded — the substance was already there; the citations were wrong.

**ai-prompt-injection** — five stale internal lesson IDs from an older naming scheme, including in the "Leads to" section (dead cross-references readers would chase):
- §2: `(the `ai-01` lesson)` → `(the `ai-llm-architecture` lesson)`.
- §10: `ai-03a/03b/03c` (three rows) → `ai-llm-top10` (the three Top-10 risk families are sections of the single top10 lesson, which is why the old a/b/c split dissolved); `ai-04` → `ai-pipeline`; `ai-05` → `ai-threat-modeling`.
- Spot-checked the edition claim in §6 ("LLM07 in 2025; LLM08 Hidden Context Exposure in 2026") against secondary sources: **correct** — LLM07:2025 was System Prompt Leakage. No change.
- AML.T0051 citation verified against primary ATLAS.yaml (name: "LLM Prompt Injection"; sub-techniques .000 Direct, .001 Indirect, .002 Triggered) — the lesson's claim holds. Row staged in `/tmp/sources-add-AI.csv`.
- No level change; remains L3.

## Staleness watch (verified, no action)

- OWASP LLM Top 10:2026 final listing confirms the code ordering every AI lesson teaches; the edition note in each lesson is accurate.
- EU AI Act amendment status (Digital Omnibus through Aug 2026) and NIST AI RMF 1.0 revision announcement (Apr 2026) in `ai-governance` are ledger-backed (sources.csv, verified 2026-10-09); both are flagged as moving and dated, which is the honest treatment.
- SEC598/SEC535 titles in `ai-sec-automation` were not re-verified in this session (the brief's §3 correction — SEC598→GASAE, SEC535→GOAA — is the anchor, and the lesson uses it correctly). If a coordinator re-checks paid-course titles, flag it.

## Follow-up recommended (not mine to act on)

- OWASP has published a separate **Top 10 for Agentic Applications — 2026** (ASI01–ASI10, via genai.owasp.org). It is outside the §5 scope (which names only the LLM Top 10:2026) and the lessons are correct at their stated scope — but a coordinator may want a gaps.md entry on whether the AI track should reference it.

## Verification (edited files only)

- `ai-threat-modeling.md`: exactly 10 `^## ` sections; frontmatter intact (`lesson_id:` present); no banned voice words; no currency symbols in new copy; no test servers started by this audit (none were running — nothing in the deepening required a run).
- `ai-prompt-injection.md`: same checks pass.

NEVER committed, NEVER pushed, build_site.py untouched.
