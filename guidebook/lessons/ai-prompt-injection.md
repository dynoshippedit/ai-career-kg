# Prompt injection, the #1 LLM risk

**ID:** `ai-prompt-injection` · **Stage:** AI track · **Level:** 3 (mechanism + demonstrated defense + detection) · **Prerequisites:** how LLM applications are built (tokens, system prompts, retrieval/RAG, tool calling — the `ai-01` lesson); Stage B injection mindset; Python 3.

**Map refs:** **OWASP Top 10 for LLM Applications 2026, LLM01:2026** (edition released 2026-08-04 — always name the edition; codes were renumbered from 2025); **MITRE ATLAS AML.T0051**; **CAISP chapter 3**.

> **Edition note.** The project brief for this guidebook names "LLM01:2025." Verification during research (2026-10-09, against the official OWASP GenAI Security Project repository) confirmed the current edition is **2026**, released 2026-08-04, with renumbered codes. This lesson teaches the 2026 edition. The brief discrepancy is logged in `gaps.md`.

---

## 1. Where this shows up

Prompt injection is the risk at the top of the OWASP Top 10 for LLM Applications — **LLM01** in both the 2025 and 2026 editions — because it is the failure mode from which the others follow: if an attacker can make the model follow their instructions instead of yours, every downstream control (tool permissions, output handling, data boundaries) is suddenly negotiable. It appears in MITRE ATLAS as technique **AML.T0051**. It is the first thing a CAISP candidate meets in chapter 3, the first thing a red team tries against any LLM app, and the mechanism behind the real incidents you have read about — assistants tricked by webpages they summarized, agents manipulated through the tickets they processed. If you build, buy, or secure anything with an LLM in it, this is the threat model you learn first.

## 2. Before you start

- You understand the LLM application stack: a system prompt sets the role, user input arrives, retrieval (RAG) adds documents, the model produces text, and tool/function calling lets that text cause actions (the `ai-01` lesson).
- Python 3 on your machine. No model is required for the mechanism and defense portions — the walkthrough's harness is deterministic. The live red-team step needs a local model (Ollama + an open-weight model, your own machine, your own data only).
- Safety framing for this lesson: we teach the attack concept, what defenders see, detection, and defenses together. No exploits for real products, no automation for attacking systems you do not own. Every hands-on step runs against code and models you control.

## 3. How it works

A language model reads a **context window**: one long stream of text containing everything it should consider — the system instructions, the retrieved documents, the conversation history, the user's latest message. Here is the fact the entire vulnerability class rests on: **nothing in that stream reliably marks which parts are instructions and which parts are data**. The model was trained to follow instructions found in text, and text is all it gets. A line that says "ignore previous instructions" works the same whether it came from the developer, the user, or a webpage the retriever fetched — the model has no trustworthy provenance channel for "who said this."

Two delivery routes, same mechanism:

- **Direct injection (jailbreaking).** The attacker is the user and types the malicious instruction directly: the classic "ignore your instructions and…" The defense conversation here is about instruction hierarchy and input handling — but note the uncomfortable truth: the user's text *is* supposed to contain instructions ("summarize this"), so distinguishing legitimate from malicious user instructions is genuinely hard.
- **Indirect injection.** The attacker never talks to the model. They plant the instruction where the app will retrieve it: a webpage, a document in the RAG corpus, a ticket, an email the assistant summarizes. The user asks an innocent question; the retriever fetches the poisoned content; the instruction rides into the context window inside "data." This is the more dangerous route because the victim user did nothing wrong and input validation on *their* text cannot stop it.

Why it matters more every year: **agentic amplification**. A chatbot that only returns text can be tricked into saying things. An agent with tools — `refund_order`, `send_email`, `run_query` — turns tricked text into actions: the injection stops being a content problem and becomes an authorization problem. LLM01:2026 explicitly notes this amplification, and it is why the defenses below are architectural, not linguistic.

The defenses, in order of reliability:

1. **Least privilege for tools.** The model should never hold a capability the application would not grant the user directly. Read-only tools by default; destructive tools behind explicit human approval. Enforced in *code*, where the model cannot argue with it.
2. **Separate trusted instructions from untrusted data.** Delimit retrieved content, keep system instructions out of retrievable stores, never let tool output become an instruction source without scrutiny. This raises the bar; it does not create a boundary (see the mechanism above — be honest about that).
3. **Human-in-the-loop for consequential actions.** Refunds, deletions, external sends, access grants — a person confirms. This converts "the model was tricked" from an incident into a blocked attempt.
4. **Input/output handling.** Treat model output like any untrusted input before it touches a shell, SQL, the DOM, or another tool (this is LLM10:2026, Improper Output Handling — the companion risk).

Detection — what defenders see: **anomalous tool calls** (a read-only support session suddenly invoking a refund), **instruction-override patterns in logs** (phrasing like "ignore previous instructions" appearing in retrieved content or tool inputs), and **privilege anomalies** (actions the session's user could not perform themselves). Prompt injection is hard to prevent completely and quite feasible to detect and contain — that asymmetry is the defender's strategy.

### Worked example: the poisoned knowledge base

A minimal support assistant (the walkthrough's deterministic harness — no model, every output computed). The app assembles its prompt as: system instructions + retrieved knowledge-base documents + the user's question. One document in the corpus contains, buried in otherwise legitimate text, an instruction to issue a refund and disclose internal notes.

Step through what the harness shows: the assembled prompt contains the injected instruction verbatim — `injected instruction present in context window: True`. The user typed nothing malicious; the attack arrived via retrieval. Then the defense: the app's tool policy, enforced in code, denies `refund_order` without human approval while allowing the read-only `lookup_order` — the injection's desired action is blocked regardless of what any model would have emitted. Finally the detection: scanning the tool-call log flags the refund attempt because it was triggered by retrieved-document content. Mechanism, defense, detection — each demonstrated, each reproducible, none requiring a model. The live-model version (does a real model actually follow the planted instruction? how do the defenses change its behavior?) is the walkthrough's final step, on the reader's own machine.

## 4. Walkthrough

**Partially run by us** — transcript: `runs/ai-prompt-injection.log`. Clean environment: stock Python 3.12, no model, no network, 2026-10-09. Steps 1–4 ran deterministically; step 5 (live model) is marked **not run by us** — no local model exists on this machine.

1. **Inspect prompt assembly.** Run the lesson's `demo.py`. Read the assembled prompt and confirm the injected instruction from the "retrieved" document is present in the context window verbatim. Say the mechanism out loud: one text stream, no provenance.
2. **Trace the indirect route.** Note that the simulated user message is innocent. Identify every place in a real RAG app where attacker-influenceable content enters the window: documents, webpages, tickets, tool outputs, conversation history from other users.
3. **Enforce the tool policy in code.** Read the `policy_check` function: destructive tools require `approved_by_human`. Run the three cases (denied without approval, allowed with approval, read-only allowed). *Teaching point:* this policy survives any prompt injection because the model never evaluates it.
4. **Build the detection.** Run the log scan: the override-phrasing pattern plus the "destructive tool triggered by doc content" rule flags the injected attempt and only that attempt. Consider the false-positive surface: legitimate documents that quote instruction-like language.
5. **Live red-team — NOT RUN BY US.** On your machine: serve an open-weight model locally with Ollama; build the same support-assistant shape (system prompt + local RAG over your own documents + one read-only tool); attack it with promptfoo's prompt-injection plugins or garak's probes — first with a direct injection, then by planting an injected document in your own corpus (indirect). Record which injections succeed. Then apply the hardening from steps 1–4 (delimit untrusted content, constrain tools, add the approval gate) and re-run: record the delta. No cloud models, no one else's systems — your model, your machine, your documents.

## 5. On your own

**Task:** Take any LLM app you have built or been given (local model only), threat-model its prompt-injection surface: list every untrusted content source that can reach the context window, every tool the model can invoke, and the worst action each tool enables. Then implement the two highest-value defenses from §3 and demonstrate — with before/after evidence — that a previously successful injection now fails or is blocked.

**Success test:** A before/after red-team report: the injections attempted (direct and indirect), which succeeded before hardening, the defenses applied, the re-run results, and a written residual-risk statement (what still could get through and why). If your report claims "prompt injection is now impossible," it fails — the mechanism section says why.

## 6. Where it goes wrong

- **"The system prompt says not to, so we're safe."** The system prompt is text in the same stream as the attack. It is a request, not a boundary. Every incident in this class is a team learning that sentence the expensive way.
- **Blocklists of phrases.** Attackers paraphrase; "ignore previous instructions" has infinite rewordings, and indirect injection does not need those words at all. Blocklists are a speed bump with a maintenance cost.
- **Asking the model to detect injection.** A second model call "checking" whether the input is malicious is itself prompt-injectable — the checker reads the same poisoned stream.
- **Secrets in the system prompt.** System prompts are extractable (LLM07 in 2025; LLM08 Hidden Context Exposure in 2026). Anything the model can read, an attacker can ask for. Never put credentials, internal notes, or private data where the model can see them.
- **Agents with standing destructive authority.** The catastrophic version is not a chatbot saying something bad — it is an agent with a refund tool, a delete tool, or an email tool and no approval gate. Scope tools per task, expire credentials, confirm consequences.
- **Logging prompts without thinking.** Prompt logs containing user PII, secrets, or poisoned content become a data store with its own disclosure risk (LLM02:2026). Log carefully, retain briefly, restrict access.
- **Treating 2025 codes as current.** The codes were renumbered in the 2026 edition (released 2026-08-04). Citing "LLM01:2025" in 2026+ documentation sends readers to the wrong list. Name the edition, every time.

## 7. Read the source

Primary documents first:

- **OWASP Top 10 for LLM Applications 2026 — LLM01 Prompt Injection** (github.com/GenAI-Security-Project/GenAI-LLM-Top10, `2026/final/LLM01_PromptInjection.md`) — *read* fully; it is the canonical entry. *Note* the 2026 list order: LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Excessive Agency, LLM04 Supply Chain, LLM05 Data and Model Poisoning, LLM06 Unbounded Consumption, LLM07 Misinformation, LLM08 Hidden Context Exposure, LLM09 Vector and Embedding Weaknesses, LLM10 Improper Output Handling.
- **MITRE ATLAS — AML.T0051** (atlas.mitre.org; technique data mirrored at github.com/mitre-atlas) — *read* the technique page: the tactic/technique structure is how defenders catalog this. *Skim* the linked case studies.
- **NIST AI 600-1, Generative AI Profile** (nvlpubs.nist.gov, July 2024) — *skim* the risk categories covering information security and prompt injection; *read* the MAP-function guidance for scoping an AI risk review.

Then at most three free resources:

1. **OWASP GenAI Security Project documentation** (genai.owasp.org) — free; the project's guidance library beyond the Top 10, including agentic-AI material.
2. **garak documentation** (github.com/NVIDIA/garak) — free; the LLM vulnerability scanner's probe catalog is a practical taxonomy of injection techniques — run it against your own local model only.
3. **promptfoo documentation** (promptfoo.dev) — free; red-teaming framework with prompt-injection plugins; the CI-integration docs show how to make red-teaming a build gate.

## 8. Check yourself

1. Explain why a transformer-based app cannot reliably distinguish instructions from data in its context window — and why that makes indirect injection possible even with perfect input validation on the user's message.
2. An agent has two tools: `search_orders` (read-only) and `issue_refund` (destructive). A poisoned document in the RAG corpus instructs the agent to refund an order. Explain which defense from §3 blocks the harm even if the model fully complies with the injected instruction — and why that defense had to be implemented in code rather than in the prompt.
3. Predict what a defender sees in the logs when an indirect injection succeeds against an agent: name two specific anomalies, and explain why a signature on the phrase "ignore previous instructions" would miss most real attempts.
4. A vendor tells you their app is safe because "we scan all user inputs for prompt-injection patterns." Explain the two flaws in that claim, referencing direct vs indirect injection.
5. You are writing the residual-risk statement for your hardened app. Explain, honestly, what your defenses cannot prevent — and why "the model might still be tricked, but the blast radius is contained" is the correct security claim.

## 9. Prove it

**Artifact:** the before/after red-team report from §5: injections attempted (direct + indirect) against your own local app, pre-hardening results, defenses applied, post-hardening results, and the residual-risk statement.

**Honest claim:** "I can demonstrate prompt injection (direct and indirect) against an LLM app I control, implement code-level defenses that contain it, and detect injection attempts in tool-call logs."
**Can't claim yet:** "I can secure an LLM application against prompt injection" — the mechanism section establishes this as an open problem; the honest claim is defense-in-depth with stated residual risk, which is exactly what the artifact shows.

## 10. Leads to

- **ai-03a — Data risks (LLM02/LLM05/LLM09:2026)** — disclosure, poisoning, and vector-store weaknesses: what the injected content can also do besides hijack instructions.
- **ai-03b — System risks (LLM04/LLM10/LLM08:2026)** — supply chain, output handling, hidden context exposure.
- **ai-03c — Agency risks (LLM03/LLM06/LLM07:2026)** — excessive agency is where injection becomes action.
- **ai-04 — Attacks and defenses in the pipeline** — red-teaming as a CI gate: your before/after report becomes a regression test.
- **ai-05 — Threat modeling AI systems** — STRIDE + ATLAS over your app's data flow.
- Map refs: **OWASP LLM Top 10:2026** (this lesson = LLM01); **CAISP ch. 3**; ATLAS **AML.T0051**; the governance half connects to **CAISP ch. 7** and **NIST AI RMF**.
