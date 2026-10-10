# Content-depth audit, second pass — AI track (8 lessons)

Auditor: subagent 2183e7d7 · 2026-10-10. Dino's order after the first pass (105 solid / 5 deepened): "try again" — the first pass was too lenient. This pass applied five sharper lenses to every one of the 8 AI lessons, deliberately different from the first audit's verdicts. Brief §1 (the bar: "explain each mechanism from first principles, with no term they can't unpack"; "Define each term where it is first needed, by what it does"), §5 (AI scope), §6 (ten sections), §7 (evidence/safety/voice) re-read first.

Result: **lenses fired on all 8 lessons; all 8 deepened.** No padding — every addition is a definition, a design rationale, a concrete detection signal, or a fixed §7.

## Per-lesson: which lenses fired, what was added

### ai-governance (L2) — lenses 1, 2
- **L1:** defined "conformity assessment" where the high-risk tier uses it (Art. 43: provider's documented internal control or independent notified-body assessment, before market placement); defined "systemic risk" where the GPAI layer uses it (Art. 65: GPAI models whose high-impact capabilities could significantly affect the EU market or public health, safety, security, or fundamental rights). Both verified against the EUR-Lex primary text in-session.
- **L2:** added the design rationale for MEASURE vs MANAGE as separate RMF functions — a treatment decision without evidence is a guess; MANAGE assigns, only MEASURE tells you the control works; ties directly to the lesson's own §6 "governance without MEASURE" failure mode.
- L3 N/A (governance lesson teaches no attacks). L4 already has a worked example (Meridian classification). L5 §7 already carries read-order guidance.

### ai-llm-architecture (L3) — lenses 1, 2
- **L1:** expanded RAG on first use (Retrieval-Augmented Generation); defined "chunk" (a short passage a document was split into for retrieval).
- **L2:** added *why next-token prediction instead of answering directly* — no labeled-answer dataset exists at internet scale, but every document is a labeled dataset for "what word comes next"; self-supervised objective, verified against HF's own glossary. Added *why RAG exists* — three problems scale doesn't solve (frozen knowledge + retraining cost; private/fresh data can't enter a shared training set; cited retrieval is checkable, model memory is not), verified against the RAG paper's own stated motivations (Lewis et al., 2020).
- L3 N/A (mechanism-mapping lesson; detection lives in the sibling lessons it feeds). L4 already has the worked data-flow example. L5 §7 already has read/skim/skip guidance.

### ai-llm-top10 (L3) — lenses 1, 2, 3, 4
- **L1:** defined "fine-tuning" (LLM05), "held-out" (LLM05), "typosquatting" (LLM04), "inversion" (LLM09 — with the verified 92% figure from Morris et al., 2023).
- **L2:** added *why the retrieval filter must run before the similarity search, not after* (post-search filtering still admits other tenants' chunks into the computation — scores/timing leak; one filter bug is a full bypass); added *why the Stage B fix works for LLM10* (downstream systems can't tell who authored the text; trust lives in the context, not the author).
- **L3:** five concrete detection signals added where the lesson was generic — LLM02: plant canary strings, probe the model, a canary in the output proves exposure (verified: Carlini et al., "Secret Sharer", 2019); LLM03: alert on tool calls outside the task's declared tool set + approval-gate overrides; LLM07: check each cited source against the retrieved set — a citation to a never-retrieved document is the fabrication signature; LLM08: extraction-phrasing alerts weighted toward new accounts (pattern, not one curious user); LLM09: the retrieval-log line where chunk tenant ≠ requester tenant.
- **L4:** LLM07 was the one abstract-only risk section — added a one-paragraph concrete shape (the support bot quoting a nonexistent policy section and help-article number; the citation is the tell). All other risks already had concrete sketches or the incidents worked example.
- L5 §7 already has read/skim/skip guidance.

### ai-pipeline (L3) — lenses 1, 2, 5
- **L1:** defined "CI/CD" (the automated build-test-release machinery) and "digest" (the artifact's hash used as its version name — content-addressed, unrepointable) where first used.
- **L2:** added *why hermetic builds deny network* — a compromised dependency without a network path cannot exfiltrate or fetch a second stage; the blast radius ends at the container wall.
- **L3:** already concrete per stage (manifest names the file; attestation rejected with reason; gate logs the trigger) — no addition warranted, recorded as checked.
- **L5:** real defect fixed — §7's "free resources" was a duplicate list of the three primary docs with no purposes. Replaced with three *distinct* free resources, each with what it is for: GitHub artifact attestations docs (the concrete Stage 2–4 implementation, verified in-session), in-toto (the layout/link provenance vocabulary, verified in-session), OpenSSF Scorecard (upstream hygiene checks before trusting artifacts, verified in-session). (First choice, the CNCF supply-chain whitepaper PDF, returned HTTP 503 three times — not retried per fetch-failure discipline; Scorecard substituted and verified.)

### ai-prompt-injection (L3) — lenses 1, 2, 3
- **L1:** defined "red-teaming" (§1, where "red team" first appears), expanded RAG (§2), defined "instruction hierarchy" (§3 — conflicts resolve by privilege, verified: Wallace et al., 2024).
- **L2:** added *why no marking scheme fixes the provenance problem* — the model sees token IDs, not spans; any delimiter is itself text an attacker can forge; a text-completion interface has no out-of-band channel. Architectural, not a missing feature.
- **L3:** sharpened the detection paragraph with the concrete signal shape: `tool=refund_order session=4821 instruction_source=retrieved_doc`, and the rule it encodes — "destructive tool whose instruction source is not the user."
- L4 already has the poisoned-knowledge-base worked example. L5 §7 already has read/skim/skip guidance.

### ai-sec-automation (L2) — lenses 1, 2, 3
- **L1 (heaviest fire):** defined dwell time, SOAR (Security Orchestration, Automation and Response), purple teaming, EDR (Endpoint Detection and Response), IdP, SPF/DKIM/DMARC (email-authentication standards), honeytoken, ASN, NetFlow, step-up authentication, Sigma (standard detection-rule format, cross-ref to `c-sigma-detection`), virtual patching, and certificate-transparency logs — each where first needed, each by what it does.
- **L2:** added *why behavioral EDR over signatures* for AI-generated malware — signatures match known code; AI-generated malware is new code every time, so only behavior catches it.
- **L3:** sharpened the two generic telemetries found — "certificate transparency logs" → CT-log alerts on new certificates for lookalike domains; "outbound patterns that look scheduled rather than human" → outbound connections at fixed intervals to domains first seen this week. The rest (MFA push anomalies, impossible-travel/ASN-change rules, process-tree anomalies, patch-lag metrics) was already concrete — recorded as checked.
- L4 already has the worked detection plan. L5 §7 already has read/skip guidance.

### ai-supply-chain (L3) — lenses 1, 2, 3
- **L1:** defined OIDC (OpenID Connect — the login protocol letting GitHub/Google vouch for identity), "model card", and "predicate" (the statement inside an attestation about what was built).
- **L2:** added *why keyless wins* — a stolen long-lived key signs forgeries silently and indefinitely; a short-lived certificate expires in minutes and every signing is Rekor-visible, so theft buys almost nothing and is itself observable.
- **L3:** added the concrete provenance-monitoring signal — a Rekor monitor alert for a signing event on your artifact name from an unexpected identity: a signature that verifies but shouldn't exist.
- L4: the pickle demo is the lesson's worked example — left alone per the task's explicit instruction. L5 §7 already has read/skim/skip guidance.

### ai-threat-modeling (L3) — lenses 2, 3
- **L1:** checked — STRIDE letters, trust boundary, ATLAS technique, asset/path are all defined in-lesson; "provenance" arrives via prerequisite `ai-pipeline`. No addition warranted, recorded as checked.
- **L2:** added *why six fixed prompts instead of brainstorming* — brainstorming finds threats you can imagine; the prompts force attacker goals you wouldn't think of, repudiation especially (the category forgotten until the logs you didn't keep are needed).
- **L3:** added "What the defender sees, per threat" — a concrete signal for each STRIDE-table row (T1 chunk-hash drift alert naming the document; T2 tenant-mismatch retrieval line; T3 approval-gate override alert; T4 provenance-labeled poisoned summary; T5 CI gate logging the trigger prompt; T6 extraction-phrasing alerts) — with the instruction that each register treatment carries its signal in the same row.
- L4 already has the Harborlight worked threat model. L5 §7 already has read/skim/skip guidance.

## Sources staged

`guidebook/reports/sources-add-2-AI.csv` — 9 rows, all status=verified, all fetched in-session 2026-10-10 (parent merges into sources.csv):
1. RAG paper, arxiv.org/abs/2005.11401 (why-retrieval rationale)
2. Instruction Hierarchy, arxiv.org/abs/2404.13208v1 (instruction-hierarchy definition)
3. Embedding inversion, arxiv.org/abs/2310.06816 (92% recovery figure)
4. Secret Sharer, ar5iv.labs.arxiv.org/html/1802.08232 (canary methodology)
5. EU AI Act, eur-lex.europa.eu/eli/reg/2024/1689/oj (Art. 43 conformity assessment; Art. 65 systemic-risk definition; Art. 55 obligations)
6. HF Transformers glossary, huggingface.co/docs/transformers/v4.49.0/en/glossary (self-supervised next-token objective; finetuning)
7. GitHub artifact attestations docs (Sigstore provenance; attestations must be verified)
8. in-toto, github.com/in-toto/in-toto (layout/link provenance framework)
9. OpenSSF Scorecard, github.com/ossf/scorecard (0–10 security-health checks)

Acronym expansions (SOAR, EDR, IdP, DMARC/DKIM/SPF, ASN, CI/CD, OIDC, CT, RAG) are treated as definitional glosses — defined by what they do per the §1 bar — and were sanity-checked against the fetched primary docs where those docs cover them (GitHub attestations doc confirms OIDC/Sigstore usage; HF glossary confirms the ML terms). No new walkthrough steps were added, so no new run transcripts were required; no test servers were started at any point.

## Verification (Phase 3)

- `python3 guidebook/build_site.py` from ~/workspace/learncomputerstuff: completed with zero errors.
- All 8 edited lessons: exactly ten `^## ` sections each; `^lesson_id:` frontmatter present in all 8 (structure untouched).
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`): zero hits in new copy.
- Currency symbols: no `$<digit>` in new copy.
- `pgrep` for test servers / stray processes: clean (none were started).
- Levels: none changed — additions are definitions, rationales, and detection signals, not new capability claims.
- NOT committed, NOT pushed, per orders. build_site.py, STATE.md, gaps.md, map.md untouched. No other stage's files touched.

## Couldn't close / follow-ups

- The CNCF Software Supply Chain Best Practices whitepaper PDF (github.com/cncf/tag-security …/CNCF_SSCP_v1.pdf) returned HTTP 503 on three attempts; per fetch-failure discipline it was not retried and was replaced by the verified OpenSSF Scorecard resource. If the coordinator wants the CNCF whitepaper in §7, it needs a re-fetch at build time.
- ai-sec-automation §7 still cites the paid SEC598/SEC535 courses' public pages (sans.org/sec598, sans.org/sec535) as primary leads with read/skip guidance — unchanged from the first audit; the brief's §3 correction (SEC598→GASAE, SEC535→GOAA) is the anchor and the lesson uses it correctly.
- The first audit's follow-up stands: OWASP's separate Top 10 for Agentic Applications (2026) is outside §5 scope — a gaps.md decision for the coordinator, not this pass.
