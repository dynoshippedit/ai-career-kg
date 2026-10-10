---
lesson_id: ai-governance
slug: ai-governance
stage: AI
level: 2
prerequisites: [ai-llm-top10, e-risk-assessment]
roles: [grc-analyst]
map_refs: ["CAISP ch7"]
test_date: 2026-10-09
description: "Governing AI: the NIST AI RMF functions, the Generative AI Profile, EU AI Act risk tiers as concepts, and ISO/IEC 42001 noted as paid — applied to a full risk register. A free lesson in the security guidebook, serving CAISP chapter 7."
dateline: "Worked case authored and reviewed 2026-10-09 · no command line in this lesson"
---
# Governing AI


**Map refs:** **CAISP chapter 7** (Emerging Threats, Governance, and Compliance in AI); NIST AI RMF 1.0; NIST AI 600-1 Generative AI Profile; EU AI Act (risk tiers as concepts). *Not* CertNexus CAIP — a separate credential the site lists separately; never merged.

---

## 1. Where this shows up

Someone has to answer "is this safe to ship, and who says so?" — that someone is you if you work GRC, security leadership, or AI security engineering at any organization large enough to have a risk committee. The answer has three vocabularies: the voluntary framework that structures the thinking (NIST's AI RMF), the law that compels parts of it (the EU AI Act), and the management-system standard auditors ask about (ISO/IEC 42001). CAISP closes its curriculum here for the same reason: chapters 1–6 teach you the attacks, chapter 7 teaches you the system that keeps an organization from shipping them. This lesson gives you all three vocabularies and makes you apply them to one fictional deployment, because governance you cannot apply is trivia.

## 2. Before you start

- `ai-llm-top10` — governance without the risk vocabulary is box-ticking; you have the vocabulary.
- `e-risk-assessment` — the risk register format, likelihood/impact scales, and treatment options transfer directly.
- No command line in this lesson. The walkthrough is a worked case producing the real work products: an AI risk register and a classification memo. The tools are a text editor and the primary sources in §7.

## 3. How it works

Governance is the system by which an organization decides what AI it builds, what risks it accepts, and who is accountable when it goes wrong. Three instruments, three different kinds of authority.

**NIST AI RMF 1.0 — the voluntary framework.** Released January 26, 2023, the AI Risk Management Framework is voluntary, outcome-based guidance — it describes what good looks like, not what the law requires. Four functions, each with categories of suggested actions:

- **GOVERN** — the culture and accountability layer: who owns AI risk, what policies exist, how decisions are documented. Without this, the other three are theater — risks get measured by nobody and managed by nobody.
- **MAP** — establish context before you assess: what the system is for, who uses it, who it affects, what could go wrong. The threat model from `ai-llm-architecture` §5 *is* a MAP activity.
- **MEASURE** — test, benchmark, and monitor: red-teaming results, evaluation scores, incident counts, cost metrics. Your `ai-prompt-injection` before/after report is MEASURE evidence.
- **MANAGE** — prioritize the measured risks, assign treatments and owners, respond to incidents, and feed lessons back into GOVERN.

Why the framework keeps MEASURE and MANAGE as separate functions: a treatment decision made without evidence is a guess. MANAGE prioritizes and assigns; only MEASURE tells you whether the control you assigned actually works. That separation is why §6 lists "governance without MEASURE" as a failure mode — a risk register row with no evidence source is fiction, not management.

Two honest notes from the primary source itself: the framework is *voluntary* (a team can do everything right and still have no legal obligation to — and a team can ignore it entirely until a regulator or a lawsuit arrives), and as of April 2026 NIST has announced the 1.0 version is being revised under the White House AI Action Plan — so cite the version you used and expect the structure to evolve.

**NIST AI 600-1 — the Generative AI Profile.** Released July 26, 2024, this profile applies the RMF to generative AI specifically: twelve GenAI risk categories with suggested MAP/MEASURE/MANAGE actions for each. The categories include information security (prompt injection lives here), data privacy, intellectual property, and information integrity — read the profile's risk table for the full twelve rather than trusting anyone's summary, including this lesson's. The profile's value is its *actions*: for each risk, concrete things to do under each RMF function, which turns "we follow the RMF" from a slogan into an auditable work plan.

**The EU AI Act — the law.** Regulation (EU) 2024/1689 takes the opposite approach from the RMF: mandatory, tiered by risk, with obligations that bite. The tiers, as concepts:

- **Unacceptable risk — prohibited.** Social scoring, manipulative techniques, untargeted facial-recognition scraping, real-time remote biometric identification for law enforcement (with narrow exceptions), and similar practices are banned outright.
- **High-risk — regulated.** Listed use cases (employment screening, education access, law enforcement, critical infrastructure, and others): providers must run a risk management system, govern their data, keep technical documentation, log operations, enable human oversight, and pass conformity assessment — the Act's term (Article 43) for demonstrating the system meets the requirements, either by the provider's own documented internal control or by assessment from an independent notified body, before the system can be placed on the market.
- **Limited risk — transparency obligations.** If a person is interacting with AI, they must be told. Chatbots and deepfakes live here.
- **Minimal risk — unregulated.** Most consumer AI; no obligations beyond existing law.
- **General-purpose AI models** get their own layer: documentation, copyright compliance, and training-data summaries for all GPAI providers; evaluations, incident reporting, and cybersecurity protections for models with systemic risk — the Act's term (Article 65) for GPAI models whose high-impact capabilities could significantly affect the EU market or public health, safety, security, or fundamental rights.

One honest note: the Act is *being amended* — the summary maintained by the Future of Life Institute notes updates adopted through the Digital Omnibus on AI as of August 2026. Teach the tiers as the stable concept; cite the current text for anything operational, and date your citation.

**ISO/IEC 42001 — the paid standard.** This is the AI management-system standard: the certifiable "we run AI responsibly" framework auditors ask about. It is a paid document — this guidebook teaches from free equivalents instead (the RMF functions above cover the same conceptual ground: governance, risk assessment, controls, continual improvement). One line, as the brief requires; no more.

**How the three fit together.** The RMF tells you *how to think*; the Act tells you *what you must do* (in the EU, for covered systems); 42001 tells an auditor *how to check* that you have a system at all. A support chatbot deployed by an EU company: the Act says which tier it is in and what that demands; the RMF organizates the work of meeting those demands; the 42001-shaped management system is what the auditor examines. Confusing the three — treating voluntary guidance as law, or a certificate as security — is the characteristic governance failure.

### Worked example: classifying the Meridian support assistant

Meridian Analytics (fictional) is deploying the support assistant from `ai-llm-architecture`: RAG over order data, two tools (`lookup_order` read-only, `issue_refund` behind human approval), EU customers. Classify it:

- **EU AI Act tier:** not prohibited, not a listed high-risk use case — but it *is* a chatbot interacting with people, so the **limited-risk transparency obligation** applies: users must know they are talking to AI. (If Meridian later adds CV-screening to the same assistant, that component becomes high-risk — tiers attach to *use cases*, not to companies.)
- **RMF mapping:** GOVERN — name the owner (the support-ops lead) and the policy (the tool-approval rule from `ai-prompt-injection`); MAP — the data-flow diagram and attack-surface table from `ai-llm-architecture`; MEASURE — the red-team report, the retrieval-isolation test, the cost monitoring; MANAGE — the risk register below, with owners and dates.
- **GenAI Profile:** information-security risk → the injection defenses; data-privacy risk → tenant isolation on the order data; IP risk → the training-data summary for the fine-tuned model.

The walkthrough turns this sketch into the full register.

## 4. Walkthrough

**No command line by design** — transcript: `runs/ai-governance.log`. The walkthrough is the authored work product below, written 2026-10-09 and self-reviewed against the checklist in the log. Reproduce it for your own fictional deployment by following the same shape.

**The Meridian AI risk register (6 risks):**

| # | Risk | RMF function | GenAI Profile category | EU Act relevance | Treatment | Owner |
|---|---|---|---|---|---|---|
| R-1 | Indirect prompt injection via RAG corpus → unauthorized refund | MANAGE (respond); MAP (threat model) | Information security | Transparency: disclose AI interaction | Approval gate on `issue_refund` (in code); corpus write-access control; detection on tool-call anomalies | AppSec lead |
| R-2 | Cross-tenant order disclosure via shared vector store | MAP; MEASURE (isolation test) | Data privacy | High-risk if extended to employment/credit use | Per-tenant namespaces, filter before search; quarterly isolation test | Data platform lead |
| R-3 | System prompt extraction discloses internal escalation numbers | MAP | Information security | — | Minimal system prompt; no secrets in context; extraction-pattern monitoring | AppSec lead |
| R-4 | Agent loop cost spike (unbounded consumption) | MEASURE; MANAGE | (operational; RMF MANAGE) | — | Per-session token caps; iteration bound; cost alerts | SRE lead |
| R-5 | Model weights from unverified publisher (supply chain) | GOVERN (procurement policy); MAP | Information security | GPAI systemic-risk duties if applicable | Pin commit hash; verify signature; admission policy in deploy pipeline | ML platform lead |
| R-6 | Ungrounded answers in refund disputes (misinformation) | MEASURE (grounding eval); MANAGE | Information integrity | — | Cite-sources requirement; human review of contested refunds | Support-ops lead |

**The classification memo (one page, the companion product):** states the Act tier (limited-risk; transparency obligation), the basis (chatbot interacting with EU persons; not a listed high-risk use case), the RMF coverage claim (which functions are evidenced and where the evidence lives), the 42001 note (management-system evidence organized RMF-first; certification is a separate, paid decision), and the residual risks (R-1 and R-2 can be contained, not eliminated — the honest statement from `ai-prompt-injection` §9, now at program level).

**Self-review checklist** (in the log): every risk names a concrete mechanism from the track's lessons (no generic "data breach" rows); every treatment is a control that exists in an earlier lesson; every owner is a named role; the Act tier cites the current text with a date; the 42001 line says "paid" once.

## 5. On your own

**Task:** Pick a different fictional AI deployment (a hiring-screening assistant, a medical triage chatbot, a code-review agent with repo write access). Write its classification memo and risk register in the walkthrough's shape: Act tier with reasoning, RMF function mapping, six risks minimum, each with mechanism, treatment from this track's lessons, and a named owner.

**Success test:** A stranger can read your memo and answer: what tier, why, what are the top three risks, who owns each, and what evidence would show the controls work. If your register's "treatment" column says "follow best practices" anywhere, it fails — name the control.

## 6. Where it goes wrong

- **Voluntary vs mandatory confusion.** "We follow the NIST RMF" does not satisfy the EU AI Act, and Act compliance does not mean the RMF's MEASURE function is done. Say which instrument each claim belongs to.
- **The certificate as security.** An ISO/IEC 42001 certificate (or any management-system certificate) attests that a *system exists*, not that the system works. Auditors check the system; attackers check the implementation. Both matter; neither substitutes for the other.
- **"Minimal risk, so no work."** Minimal-risk systems still sit inside an organization that needs GOVERN and MAP. The Act's lightest tier is not an exemption from thinking.
- **Tiers attached to companies.** Tiers attach to *use cases and deployments*. One company runs minimal-risk, limited-risk, and high-risk systems simultaneously; classify each deployment, not the logo.
- **Static governance.** The Act is being amended, the RMF is being revised, the Top 10 was re-issued in 2026. A governance memo without dates is a memo about a world that no longer exists. Date every classification.
- **Governance without MEASURE.** A risk register nobody tests is fiction. Every risk in the register needs its evidence: the red-team report, the isolation test, the cost dashboard. If the evidence does not exist, the register says "not yet evidenced" — the honest cell.

## 7. Read the source

Primary documents first:

- **NIST AI Risk Management Framework 1.0** (nvlpubs.nist.gov, NIST AI 100-1, January 2023; overview at nist.gov/itl/ai-risk-management-framework) — *read* the four functions and their categories; *note* the April 2026 revision announcement and cite your version.
- **NIST AI 600-1, Generative AI Profile** (nvlpubs.nist.gov, July 2024) — *read* the twelve risk categories and their suggested actions; this is the document that turns the RMF into an AI work plan.
- **EU AI Act — full text and explorer** (artificialintelligenceact.eu) — *read* the risk-tier summary and the prohibited/high-risk lists; *use* the explorer for anything operational. *Note* the Digital Omnibus amendments (current as of August 2026) and date your reading.

Then at most three free resources:

1. **NIST AI RMF Playbook** (airc.nist.gov) — free; suggested actions per function — the implementation companion to the framework.
2. **OWASP GenAI Security Project — AI governance guidance** (genai.owasp.org) — free; maps the Top 10 risks onto governance controls.
3. **IAPP AI Governance resources** (iapp.org) — free articles; the professional community's view of how the Act is actually being implemented.

## 8. Check yourself

1. A company says "we are NIST AI RMF aligned, so we are EU AI Act compliant." Explain the two category errors in that sentence and what each instrument actually provides.
2. Meridian adds resume screening to its support assistant. Explain what changes in its EU AI Act classification, which RMF function owns the re-assessment, and which two risks from the register gain new urgency.
3. Explain why the GenAI Profile's twelve risk categories are more *actionable* than the RMF's four functions alone — and why neither replaces a threat model of the specific system.
4. A vendor shows you their ISO/IEC 42001 certificate as proof their chatbot "cannot leak data." Explain what the certificate actually attests, which lesson's mechanism defeats the claim, and the question you ask next.
5. Your risk register lists "prompt injection" with treatment "input validation." Using this track's lessons, explain why that treatment is insufficient and rewrite the row with the defense stack the track actually teaches.

## 9. Prove it

**Artifact:** the classification memo and risk register from §5 for your chosen fictional deployment — Act tier with dated reasoning, RMF-mapped risks with mechanisms, treatments, and named owners.

**Honest claim:** "I can classify an AI deployment under the EU AI Act's risk tiers, map its risks to the NIST AI RMF functions and the GenAI Profile categories, and write a risk register with owned treatments."
**Can't claim yet:** "I run an AI governance program" — that is organizational work over time (GOVERN lived, not written); this lesson is the literacy and the work products it starts with.

## 10. Leads to

- **Stage E governance lessons** — `e-risk-assessment` (the method applied here), `e-sdlc` (where AI security gates join the SDLC), `e-bcp-drp` (when the AI system is the thing that fails).
- **`ai-supply-chain`** — re-read with governance eyes: provenance records are the evidence auditors ask for first.
- **CAISP ch. 7 map** — this lesson plus the track's earlier chapters complete the CAISP spine; the emerging-threats half of chapter 7 is ongoing reading (the field moves — date everything).
- Map refs: **CAISP ch. 7**; NIST AI RMF 1.0; NIST AI 600-1; EU AI Act (concept tiers); ISO/IEC 42001 (paid — one line, as required).
