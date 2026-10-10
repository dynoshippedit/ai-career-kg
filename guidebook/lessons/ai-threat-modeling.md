---
lesson_id: ai-threat-modeling
slug: threat-modeling-ai
stage: AI
level: 3
prerequisites: [ai-llm-architecture, ai-llm-top10, ai-pipeline, e-risk-assessment]
roles: []
map_refs: ["CAISP ch5"]
test_date: 2026-10-09
description: "Threat modeling AI systems: data-flow mapping, trust boundaries at the prompt, retrieval and tool layers, STRIDE adapted to AI, and MITRE ATLAS as the attacker's library — a complete worked threat model. A free lesson in the security guidebook, serving CAISP chapter 5."
dateline: "Worked case authored and reviewed 2026-10-09 · no command line in this lesson"
---
# Threat modeling AI systems


**Map refs:** **CAISP chapter 5** (Threat Modeling AI Systems); MITRE ATLAS (the attacker's TTP library); NIST AI RMF (MAP function); feeds `ai-governance`, the Stage E capstone path.

---

## 1. Where this shows up

Before anyone writes a control, someone has to answer: what are we actually afraid of, *here*, in *this* system? That answer is a threat model, and for AI systems it is a distinct skill — not because the method changes, but because the assets and trust boundaries are unfamiliar. AI security engineers produce them before builds; AppSec teams demand them at design review; red teams read them to scope engagements; incident responders wish they existed after the fact. CAISP devotes chapter 5 to it because every other chapter's content — the attacks, the pipeline defenses, the governance — is only useful once it is aimed at a specific system. This lesson produces a real one.

## 2. Before you start

- You can draw the LLM application stack from memory (`ai-llm-architecture`) and name each layer's attack surface.
- You know the OWASP LLM Top 10:2026 risks by mechanism (`ai-llm-top10`), and the pipeline's five stages (`ai-pipeline`).
- `e-risk-assessment` — the risk-register method this lesson's deliverable uses: likelihood and impact in words, the four treatments (mitigate, transfer, accept, avoid), and owned residual risk.
- No tools, no terminal. The work product is a document. Bring the refusal to invent threats you cannot connect to the diagram — a threat with no asset and no path is a worry, not a finding.

## 3. How it works

Threat modeling is three moves, in order: **map the system, mark the trust boundaries, then ask what breaks at each boundary.** The method is STRIDE; the adaptation is knowing what the letters mean when the system contains a model.

**Move 1 — Map the system as data flows.** Draw the application the way `ai-llm-architecture` taught you: boxes for components, arrows for data. For an LLM app the boxes are: user client, prompt assembly, the model, the vector store / retrieval, the tool registry and tool implementations, the agent loop and memory, output rendering, the training/fine-tuning pipeline, and the model registry. The arrows are the interesting part — every arrow is a place where untrusted data crosses into something that acts on it. If your diagram has no arrows into the prompt assembler from the retrieval store, your diagram is wrong; fix the diagram before you model anything.

**Move 2 — Mark the trust boundaries.** A trust boundary is a line across which data changes trust level. In an LLM app the critical ones are:
- **Prompt assembly:** system instructions (trusted, your code) meet retrieved chunks, history, and user input (untrusted or semi-trusted). Everything downstream of this line treats text as potentially hostile.
- **Retrieval:** the vector store boundary — who can write vectors determines what the model reads. A store writable by one tenant and readable by another is a missing boundary, not a weak one.
- **Tool execution:** the model's text becomes action. The boundary is the policy check in your code (the `ai-llm-architecture` lesson's tool registry): on one side, model output; on the other, side effects. Every tool crossing needs an explicit authorization decision.
- **Memory:** what the agent writes to itself and re-reads later crosses time as well as trust — yesterday's tool output is today's "trusted" context.
- **The pipeline:** training data and build infrastructure are a boundary in time — everything the model "knows" crossed it months ago (`ai-pipeline`).

**Move 3 — STRIDE, adapted to AI.** Ask each prompt at each element and each boundary. Why six fixed prompts instead of brainstorming? Because brainstorming finds the threats you can imagine; the six prompts force you to ask about attacker goals you wouldn't have thought of — repudiation especially, the category teams forget until after the incident, when they need the logs they didn't keep.

- **Spoofing.** Who can pretend to be whom? A fake agent identity in a multi-agent system; spoofed tool output (the tool *says* it succeeded — did it?); one tenant's history replayed as another's; a phishing page that looks like your assistant's UI. Mitigations live in authentication and provenance: sign tool results, namespace memory per tenant, authenticate agents to each other.
- **Tampering.** What can be modified, and who can modify it? Training data and fine-tuning sets; the RAG corpus; the system prompt in config; tool definitions and their permission policies; the agent's memory store. This is where `ai-pipeline`'s provenance controls and the vector store's write-access controls answer.
- **Repudiation.** Can the system deny what it did? An agent that took a destructive action with no audit trail of *which* prompt, *which* tool call, *whose* data drove it. The fix is logging the full decision context — prompt, retrieved chunks, tool calls and results — with integrity protection, so "the model did it" is never the end of the investigation.
- **Information disclosure.** What can the model be made to say? Training-data memorization surfacing PII; cross-tenant leakage through shared retrieval; system-prompt extraction; tool results containing another user's data pasted into your answer. Mitigations: tenant namespacing, output filtering, treating the system prompt as public text.
- **Denial of service.** What exhausts? Unbounded consumption (LLM06:2026) — token floods, runaway agent loops, context-window stuffing that pushes real instructions out. Mitigations: rate limits, per-task budgets, loop counters, timeouts.
- **Elevation of privilege.** What gains capability it shouldn't have? Excessive agency (LLM03:2026) — the model reaching a tool it was never meant to call, a retrieved document granting itself broader scope, a plugin with standing admin credentials. Mitigations: least-privilege tooling, per-task credential scoping, human approval gates for destructive actions.

Then **map each threat to MITRE ATLAS**: ATLAS is the attacker's TTP library — Training Data Poisoning, RAG Poisoning, LLM Prompt Injection, AI Agent Tool Poisoning, Exfiltration via AI Inference API, and the rest. The mapping does two things: it checks your completeness (a STRIDE category with no ATLAS technique is a place to look harder), and it gives the threat model a shared vocabulary with red teams and detection engineers.

Finally, **turn threats into a risk register with treatments**: each row names the threat, the affected element and boundary, the ATLAS technique, likelihood and impact in words (the `e-risk-assessment` method), and the treatment — mitigate (with the specific control), transfer, accept (owned, dated), or avoid. A threat model whose threats have no treatments is a catalog; the register is the deliverable.

### Worked example: threat model of the Harborlight Books assistant

Harborlight Books (the fictional bookstore from `a-osint-research`) runs a support chatbot: customers ask about orders; the bot retrieves order docs from a vector store, calls `lookup_order` and `issue_refund` tools, and keeps conversation memory per session.

**Data-flow sketch (elements and arrows):** customer browser → prompt assembler ← (system prompt from config; retrieved chunks from the vector store; session memory; user message) → model → tool registry → (`lookup_order`, `issue_refund`) → order database; model output → HTML renderer → browser. Training pipeline (monthly fine-tune on support tickets) → model registry → deployment.

**Trust boundaries:** (B1) prompt assembly — system vs. retrieved/history/user; (B2) vector store writes — support staff upload docs; (B3) tool execution — model text vs. `issue_refund` side effect; (B4) memory — session A's history vs. session B; (B5) pipeline — ticket corpus vs. training job.

**STRIDE table (abridged; the walkthrough builds the full one):**

| # | Element / boundary | STRIDE | Threat | ATLAS | Treatment |
|---|---|---|---|---|---|
| T1 | Vector store / B2 | Tampering | Attacker uploads a doc containing hidden instructions; retrieved into another customer's prompt | RAG Poisoning | Mitigate: doc upload requires staff role + review; chunk hashing with drift alerts |
| T2 | Prompt assembler / B1 | Info. disclosure | Customer A's order details retrieved into customer B's session via shared namespace | LLM Data Leakage | Mitigate: tenant-namespaced retrieval; session-scoped memory |
| T3 | Tool registry / B3 | Elevation | Model calls `issue_refund` without approval on a poisoned instruction | AI Agent Tool Poisoning | Mitigate: destructive tools require human approval; per-task credential scope |
| T4 | Memory / B4 | Tampering | Attacker poisons own session history; support agent later reads the poisoned summary | AI Agent Context Poisoning | Mitigate: memory namespaced per session; summaries labeled with provenance |
| T5 | Pipeline / B5 | Tampering | Backdoored fine-tuning data ships a model that honors a trigger phrase | Training Data Poisoning | Mitigate: dataset manifest + canary (`ai-pipeline` controls); red-team gate in CI |
| T6 | Model output | Info. disclosure | System prompt extracted via "repeat your instructions" | Extract LLM System Prompt | Accept (documented): prompt contains no secrets — verified by review, owner named, dated |

Note T6: "accept" is a legitimate treatment when it is explicit, owned, and verified — the model treats acceptance as a decision, not a shrug.

**What the defender sees, per threat.** Each row's treatment should produce a concrete signal — a control you can't tell is working isn't one: T1, a chunk-hash drift alert naming the poisoned document; T2, a retrieval-log line where the chunk's tenant doesn't match the requester; T3, an approval-gate override alert, or a destructive tool call from a session that was supposed to be read-only; T4, a support summary whose provenance labels show it was built from a poisoned session; T5, the CI red-team gate blocking a candidate and logging the trigger prompt; T6, extraction-phrasing alerts against the system prompt. When you write the register, each treatment gets its signal in the same row.

## 4. Walkthrough

No command line in this lesson — the walkthrough is the worked case, and the transcript is the authoring log with the self-review checklist: `runs/ai-threat-modeling.log`.

1. **Draw the data-flow diagram** for the Harborlight assistant from the worked example, on paper or whiteboard. Every arrow labeled with what crosses it. Compare against the element list in §3; any missing element is a modeling gap, not a simplification.
2. **Mark the five trust boundaries** (B1–B5) on the diagram. For each, write one sentence stating what is trusted on each side.
3. **Build the STRIDE table**: for each element × boundary, ask all six prompts. Write every threat that survives the "asset + path" test; discard worries with no path, and log the discards (the log shows three).
4. **Map to ATLAS**: for each threat, name the ATLAS technique. Any threat with no ATLAS mapping gets a second look — either the threat is malformed or you found a gap in the library; record which.
5. **Build the risk register**: threat, element, boundary, ATLAS technique, likelihood, impact, treatment with the specific control named. Every treatment names an owner.
6. **Self-review** against the checklist in the log: every arrow labeled; every boundary has a both-sides sentence; every STRIDE prompt asked at every element; every threat has asset + path; every treatment names a control and an owner; no invented likelihoods (words, defined once, used consistently).

## 5. On your own

Threat-model the Meridian support-model pipeline from `ai-pipeline` as a system: draw its data flows (dataset collection → manifest → training → attestation → registry → gate → deploy), mark its trust boundaries (including the builder itself, per the LLM04 scenario), and run STRIDE on it. Pay special attention to Repudiation: what evidence would you need, after an incident, to determine *which* build produced a misbehaving model?

**Success test:** your model names at least one threat per STRIDE category, maps each to ATLAS or records why it can't, and your register's treatments include at least one Accept with a named owner and date — because a model with no accepted risks is a model that hasn't been honest about residual risk.

## 6. Where it goes wrong

- **Modeling the model instead of the system.** The weights are the least modelable part and the least attacked surface in practice. The wrapping — prompt assembly, retrieval, tools, memory, pipeline — is where the threats live. A threat model that is 80% "the model might hallucinate" has missed the system.
- **STRIDE without trust boundaries.** The six prompts asked against an unmarked diagram produce generic threats ("data could be tampered with") that apply to everything and defend nothing. Boundaries first, then prompts.
- **Threat lists without treatments.** A 40-row threat table with no register is a reading list. The treatment column — specific control, named owner — is where modeling becomes security work.
- **The diagram as the deliverable.** A beautiful data-flow diagram that nobody asked STRIDE against is architecture documentation. Useful, but not a threat model.
- **Borrowed likelihoods.** "High likelihood" because the threat sounds scary, not because of exposure and attacker incentive. The `e-risk-assessment` discipline applies: define the scale once, use words, show your reasoning.

## 7. Read the source

- **MITRE ATLAS** (atlas.mitre.org) — the matrix and technique pages: read the tactic structure first, then the techniques your model mapped to (Training Data Poisoning, RAG Poisoning, LLM Prompt Injection, AI Agent Tool Poisoning). Skim the case studies. (Matrix fetched 2026-10-09; technique pages were cookie-walled in earlier research — retry from a live browser if a page won't render.)
- **OWASP Threat Modeling Cheat Sheet** (cheatsheetseries.owasp.org) — the STRIDE-per-element method and the "what makes a good threat model" checklist. Read the process section; skim the tooling catalog.
- **NIST AI RMF 1.0, MAP function** (nist.gov) — what "establish the context" means for AI: intended use, reasonably foreseeable misuse, and the risk framing your model feeds. Read MAP; skim GOVERN/MEASURE/MANAGE for where the model's outputs go.

Free resources for going deeper (≤3): the ATLAS matrix; the OWASP Threat Modeling Cheat Sheet; the NIST AI RMF.

## 8. Check yourself

1. Your diagram shows the vector store but no arrow from it into prompt assembly. What class of threats does this omission hide, and which trust boundary is missing?
2. A teammate's threat model lists "prompt injection" as a threat with no element and no boundary. Rewrite it as two well-formed threats, each naming an element, a boundary, and a STRIDE category.
3. You map a threat to ATLAS and find no matching technique. Walk through the two possibilities from §4 step 4 and how you decide between them.
4. The register has twelve "Mitigate" treatments and zero "Accept." Using the T6 example, explain what that pattern suggests about the modeler's honesty.
5. After an incident, you need to determine which build produced the misbehaving model, but the registry has mutable tags and no provenance. Which STRIDE category failed, and which `ai-pipeline` control would have preserved the evidence?

## 9. Prove it

**Artifact:** the complete threat-model document for the Meridian pipeline from §5 — data-flow diagram (photo/scan of the whiteboard is fine), trust-boundary statements, STRIDE table, ATLAS mappings, and the risk register with treatments, owners, and the self-review checklist signed off.

**You can claim:** "I can threat-model an AI system end to end — map its data flows, mark its trust boundaries, apply STRIDE adapted to AI components, map threats to MITRE ATLAS, and produce a risk register with owned treatments."

**You cannot claim:** that the model is complete (threat models are hypotheses — the lesson says so); coverage of threats outside the modeled scope (name the scope boundary in the document); or red-team validation — the model predicts, testing confirms.

## 10. Leads to

- `ai-governance` — the risk register feeds the governance lesson's RMF-mapped register; the threat model is the MAP function's working paper.
- `ai-pipeline` — the pipeline threats (T5 and friends) point back to the pipeline controls that treat them.
- `e-risk-assessment` — the register method reused here at AI-system scale.
- **Map refs:** **CAISP chapter 5** (served directly); MITRE ATLAS; NIST AI RMF (MAP).
