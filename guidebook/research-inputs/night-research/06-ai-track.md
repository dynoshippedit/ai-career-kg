# 06 — AI Security Track: lesson research map

Track spine: CAISP's seven chapters (Practical DevSecOps — verified at the issuer via its official training partner's course outline; never merged with CertNexus CAIP, which the site already lists separately):
1. Introduction to AI Security
2. Understanding and Attacking Large Language Models
3. LLM Top 10 Vulnerabilities
4. AI Attacks and Defenses Using DevOps
5. Threat Modeling AI Systems
6. Supply Chain Attacks in AI
7. Emerging Threats, Governance, and Compliance in AI

Prerequisite for the track as a whole: basic Linux commands; scripting familiarity helps but is not required (per CAISP's own stated prerequisites). Lesson-level prerequisites name the earlier stages that feed each lesson.

Safety line (per brief §7): teach attack concepts + what defenders see + detection + defenses together. No working exploits for real products, no phishing kits, no evasion tooling. Hands-on work only against local models/apps the reader runs (Ollama, local RAG) and established open-source red-team tooling.

---

## A. Securing AI systems (CAISP spine)

### ai-01 — How LLM applications are built (CAISP ch. 1–2) · Level 2
What the lesson teaches: tokens and tokenization; embeddings; what a transformer does at mechanism level (attention as weighted lookup, no more); the LLM application stack — system prompt, user input, retrieval (RAG), tool/function calling, agents (plan → act → observe loops with memory).
- **Primary sources:** OWASP GenAI Security Project (genai.owasp.org) — project documentation; MITRE ATLAS (atlas.mitre.org) — tactic/technique structure.
- **Free resources (≤3):** OWASP GenAI Security Project docs; Hugging Face "LLM Course" (free, covers tokenization/embeddings/transformers); the tokenizer playground in any open-weight model's repo docs.
- **Lab target:** local only — run an open-weight model with Ollama; build a minimal RAG pipeline locally (LangChain or LlamaIndex + Chroma, own documents only); inspect what lands in the prompt.
- **Proof artifact:** a diagram of the reader's own local RAG app's data flow (user → retriever → prompt assembly → model → output), with each trust boundary marked.
- **Prerequisites:** Stage A (Python, HTTP, networking). Feeds: ai-02, ai-03.

### ai-02 — Prompt injection, the #1 risk (CAISP ch. 3 · LLM01:2025) · Level 3
What the lesson teaches: direct injection (jailbreaking) vs indirect injection (via retrieved content); why instructions and data cannot be reliably separated in a transformer context window; ATLAS technique AML.T0051; defenses — input/output handling, least privilege for tools, human-in-the-loop for destructive actions; what detection looks like (anomalous tool calls, instruction-override patterns in logs).
- **Primary sources:** OWASP LLM Top 10 2025, LLM01:2025 (genai.owasp.org); MITRE ATLAS AML.T0051 (atlas.mitre.org).
- **Free resources (≤3):** OWASP LLM01:2025 page; MITRE ATLAS AML.T0051 technique page; promptfoo docs (red-team plugin reference).
- **Lab target:** local only — attack the reader's own Ollama chatbot with promptfoo's prompt-injection plugins; then harden it (separate trusted instructions from untrusted data, constrain tools) and re-run to show the delta.
- **Proof artifact:** before/after red-team report on the reader's own app — successful injections, mitigations applied, residual risk stated.
- **Prerequisites:** ai-01; Stage B (injection mindset, web vuln classes). Feeds: ai-03, ai-04.

### ai-03a — Data risks: disclosure, poisoning, vector weaknesses (CAISP ch. 3 · LLM02/LLM04/LLM08:2025) · Level 3
What the lesson teaches: LLM02 Sensitive Information Disclosure (training-data memorization, context leakage across users); LLM04 Data and Model Poisoning (poisoned fine-tuning data, backdoored behavior); LLM08 Vector and Embedding Weaknesses (RAG store as attack surface, tenant isolation, indirect injection via poisoned chunks). Detection and fixes for each.
- **Primary sources:** OWASP LLM Top 10 2025, LLM02/LLM04/LLM08 (genai.owasp.org); MITRE ATLAS Exfiltration and ML Attack Staging tactics (atlas.mitre.org).
- **Free resources (≤3):** OWASP LLM02/LLM04/LLM08 pages; MITRE ATLAS technique pages for the mapped techniques; Chroma/embedding-store access-control docs.
- **Lab target:** local only — plant a canary secret in the reader's own local RAG corpus, demonstrate extraction; poison one chunk and show retrieval manipulation; then fix with tenant namespacing and chunk signing/hashing.
- **Proof artifact:** lab write-up with extraction evidence and the implemented controls.
- **Prerequisites:** ai-01, ai-02. Feeds: ai-05, ai-06.

### ai-03b — System risks: supply chain, output handling, prompt leakage (CAISP ch. 3 · LLM03/LLM05/LLM07:2025) · Level 3
What the lesson teaches: LLM03 Supply Chain (unverified model weights, malicious pickles, compromised hubs); LLM05 Improper Output Handling (LLM output as untrusted input — treat like any user input before it hits SQL, shell, DOM, or tool calls); LLM07 System Prompt Leakage (new in 2025 — prompts are extractable, never hold secrets). Detection and fixes.
- **Primary sources:** OWASP LLM Top 10 2025, LLM03/LLM05/LLM07 (genai.owasp.org); CycloneDX specification (cyclonedx.org).
- **Free resources (≤3):** OWASP LLM03/LLM05/LLM07 pages; Hugging Face model-card and commit-hash documentation; Sigstore docs (docs.sigstore.dev).
- **Lab target:** local only — verify a model download by pinned commit hash; demonstrate a pickle-deserialization hazard in a sandbox with a deliberately crafted local file (concept demo, reader's own machine); run garak's probe set against the local model and triage the findings.
- **Proof artifact:** garak scan report on the reader's local model with triaged findings and applied mitigations.
- **Prerequisites:** ai-01, ai-02. Feeds: ai-06.

### ai-03c — Agency risks: excessive agency, misinformation, unbounded consumption (CAISP ch. 3 · LLM06/LLM09/LLM10:2025) · Level 2
What the lesson teaches: LLM06 Excessive Agency (agents with write/delete/execute and no confirmation — the 2025 agentic risk); LLM09 Misinformation (ungrounded output in high-stakes decisions); LLM10 Unbounded Consumption (token/cost exhaustion, no rate limits). Defenses: least-privilege tooling, human approval gates, grounding requirements, rate limits and timeouts, cost monitoring.
- **Primary sources:** OWASP LLM Top 10 2025, LLM06/LLM09/LLM10 (genai.owasp.org).
- **Free resources (≤3):** OWASP LLM06/LLM09/LLM10 pages; OWASP GenAI Agentic AI guidance (genai.owasp.org); AgentDojo research environment docs (agent injection benchmark).
- **Lab target:** local only — give the reader's local agent a destructive tool, demonstrate an unwanted action in a sandbox, then add approval gates and per-task credential scoping; load-test token limits.
- **Proof artifact:** agent permission matrix (tool × allowed/confirm/denied) for the reader's own agent, with the reasoning written down.
- **Prerequisites:** ai-01. Feeds: ai-05.

### ai-04 — Attacks and defenses in the pipeline (CAISP ch. 4) · Level 3
What the lesson teaches: DevSecOps for AI — securing the training/fine-tuning pipeline, model registries, and deployment; adversarial testing as a CI gate (red-team findings become regression tests); SBOM generation at build; signing and attestation before deploy.
- **Primary sources:** SLSA specification (slsa.dev); Sigstore documentation (docs.sigstore.dev); OWASP GenAI Security Project CI/CD guidance.
- **Free resources (≤3):** SLSA docs; Sigstore/cosign docs; promptfoo CI integration docs.
- **Lab target:** local only — GitHub Actions workflow on the reader's own repo: build a container serving the local model, generate a CycloneDX SBOM, run promptfoo red-team as a build gate that fails on new findings, sign with keyless cosign.
- **Proof artifact:** the working pipeline (config files + a passing/failing run log) and the signed SBOM.
- **Prerequisites:** ai-02, ai-03a/b; Stage B (methodology, evidence discipline). Feeds: ai-06.

### ai-05 — Threat modeling AI systems (CAISP ch. 5) · Level 3
What the lesson teaches: STRIDE applied to AI components (spoofing of agents, tampering with training data/RAG, repudiation of model actions, information disclosure via the model, denial of service via consumption, elevation via excessive agency); ATLAS as the attacker's TTP library mapped onto the model; building an AI threat library and risk register.
- **Primary sources:** MITRE ATLAS (atlas.mitre.org) — tactics, techniques, case studies; NIST AI RMF MAP function (nist.gov).
- **Free resources (≤3):** MITRE ATLAS Navigator; OWASP Threat Modeling guidance; Microsoft Threat Modeling Tool (free download).
- **Worked case (no CLI):** threat model of the reader's ai-01 RAG chatbot — data-flow diagram, STRIDE-per-element, ATLAS-mapped threats, risk register with treatments. This is the lesson's real work product.
- **Proof artifact:** the completed threat model document — diagram, threat table, risk register.
- **Prerequisites:** ai-01 through ai-03c; Stage E governance thinking helps (not required). Feeds: ai-07, ai-cap.

### ai-06 — AI supply chain (CAISP ch. 6) · Level 3
What the lesson teaches: model provenance (pinned commits, verified publishers); weight-format hazards (pickle deserialization); dataset integrity; AIBOM — CycloneDX with model components (hashes, source URLs, framework, dataset references); signing with Sigstore keyless (Fulcio/Rekor); SLSA provenance for builds; OpenSSF model signing.
- **Primary sources:** CycloneDX specification (cyclonedx.org); Sigstore docs (docs.sigstore.dev); SLSA spec (slsa.dev).
- **Free resources (≤3):** CycloneDX spec; Sigstore docs; OpenSSF model-signing project docs.
- **Lab target:** local only — generate a CycloneDX AIBOM for the reader's local model directory (hashes, source, framework), sign it keyless with cosign, verify the signature and transparency-log entry; write a policy that refuses unsigned models.
- **Proof artifact:** signed AIBOM + verification transcript + the admission policy.
- **Prerequisites:** ai-03b, ai-04. Feeds: ai-cap.

### ai-07 — Governance I: NIST AI RMF and the Generative AI Profile (CAISP ch. 7) · Level 2
What the lesson teaches: AI RMF 1.0 (NIST AI 100-1, Jan 2023) — the four functions GOVERN (culture, roles, accountability), MAP (context, intended use, risks), MEASURE (test, benchmark, monitor), MANAGE (prioritize, treat, respond); the Generative AI Profile (NIST AI 600-1, Jul 2024) and its twelve GenAI risk categories (including information security/prompt injection, data privacy, IP, information integrity); voluntary, outcome-based — what good looks like, not a compliance obligation.
- **Primary sources:** NIST AI Risk Management Framework 1.0 (n
...[truncated 9031 chars]