---
lesson_id: e-threat-modeling-concepts
slug: threat-modeling-concepts
stage: E
level: 3
prerequisites: [e-sdlc, ai-threat-modeling]
roles: []
map_refs: ["CISSP 1.10"]
test_date: 2026-10-10
description: "Survey STRIDE, PASTA, OCTAVE, and attack trees, and choose the right methodology per situation. A free lesson in the security guidebook, serving CISSP objective 1.10."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Threat modeling concepts and methodologies: choosing how to think about what can go wrong


**Map ref:** serves **CISSP objective 1.10** — threat modeling concepts and methodologies.

---

## 1. Where this shows up

Threat modeling is the design-time discipline of asking "what can go wrong" before the system exists to go wrong in. It shows up in the architecture review where someone sketches the data flows and asks where the trust boundaries are; in the SDLC gate that requires a threat model before code is written; in the risk register whose best entries came from a modeling session, not a scanner; and in the post-incident review that discovers the attack path was obvious on a whiteboard six months earlier. `e-sdlc` taught you to *do* STRIDE on a system; `ai-threat-modeling` taught the AI variant. This lesson teaches the *choice*: STRIDE, PASTA, OCTAVE, and attack trees are different instruments for different situations, and picking the wrong one is how organizations produce threat-model theater — documents that describe threats without changing decisions.

## 2. Before you start

- You have run a STRIDE session in `e-sdlc` — that is your reference implementation. This lesson compares it against the alternatives.
- You have seen AI-specific threat modeling in `ai-threat-modeling` — the methodology choice applies there too.
- Bring a system you know well (from `e-sdlc` or your own work) — the worked case asks you to choose methodologies for three situations, and a concrete system makes the choice real.
- The work product is a methodology-selection decision record: situation, chosen method, rationale, staffing, cadence, and what the output feeds.

## 3. How it works

**What threat modeling is — and is not.** Threat modeling is structured design-time reasoning about threats: what you are building, what can go wrong, what you will do about it, and whether you did a good job. It is not a vulnerability scan (which finds weaknesses in built things), not a risk assessment (which evaluates and prioritizes — threat modeling *feeds* it), and not a one-time document (it is revisited when the design changes). The output that matters is not the diagram — it is the *decisions the diagram forced*: the trust boundary that moved, the component that got a different authentication scheme, the threat that became a security requirement.

**STRIDE (Microsoft).** The developer's method, and your reference from `e-sdlc`. STRIDE is a mnemonic of six threat categories applied per component and per data flow, usually against a data-flow diagram: **S**poofing (using another's authentication information), **T**ampering (malicious modification of data, at rest or in transit), **R**epudiation (denying an action without proof otherwise), **I**nformation disclosure, **D**enial of service, **E**levation of privilege. Microsoft's own threat-modeling documentation (learn.microsoft.com — the primary source for this lesson, fetched in-session) frames STRIDE as a way to formulate pointed questions per component: how can an attacker change the authentication data, what happens if access to the database is denied. Strengths: concrete, teachable, fits the SDLC — developers can run it with a DFD. Limits: component-centric, so it finds trees reliably and can miss the forest — business-logic abuse and attacker-chained paths across components are not its native output. Best for: development teams modeling systems they are building, as a design gate.

**PASTA (Process for Attack Simulation and Threat Analysis).** The risk-centric method: seven stages running from business objectives through threat simulation to risk-ranked output. Stage 1 (Define Objectives) exists because threat models that start with the technology stack produce finding lists executives cannot prioritize — PASTA forces the business-impact framing first, and every subsequent stage inherits it. The middle stages (threat analysis, vulnerability and weakness analysis, attack modeling) correlate real threat intelligence against the actual attack surface (the sum of all points where an attacker can interact with the system) and simulate attack paths rather than categorizing theoretical threats. Strengths: attacker-perspective, risk-ranked output a risk register can consume directly, business-aligned. Limits: heavyweight — seven stages need skilled facilitators and real threat intel; overkill for a small team's feature design. Best for: organizations that need threat modeling to feed enterprise risk management, or high-stakes systems where the output must be prioritized by business impact.

**OCTAVE (Operationally Critical Threat, Asset, and Vulnerability Evaluation).** The organizational method, from Carnegie Mellon's Software Engineering Institute. OCTAVE is asset-centric and workshop-driven: cross-functional teams identify what matters (critical information assets), profile the threats to those assets, examine the infrastructure those assets depend on, and build a protection strategy. The SEI's "Introduction to the OCTAVE Approach" (August 2003 — fetched in-session) organizes it in three phases: build asset-based threat profiles (an organizational evaluation — what is important, what protects it now), identify infrastructure vulnerabilities (the technology evaluation — access paths and component weaknesses), and develop security strategy and plans (risks to critical assets, the protection strategy, mitigation plans). Strengths: non-technical stakeholders can participate — it runs on staff knowledge, not code; produces organization-wide strategy, not component findings. Limits: slow, workshop-heavy, and its technology evaluation is shallower than a developer-led method. Best for: standing up threat modeling as an organizational practice, or assessing an enterprise where the critical question is "what matters" rather than "how does this component fail."

**Attack trees (Schneier).** The analyst's method: goal-oriented decomposition. Start with the attacker's goal ("read the patient database"), decompose into alternative paths (OR nodes) and required sub-steps (AND nodes), down to leaf actions. Bruce Schneier's "Attack Trees" paper (December 1999 — fetched in-session) is the founding treatment. Strengths: precise, composable, excellent for a single crown-jewel asset — you can annotate nodes with cost, difficulty, and probability, and the tree shows exactly which countermeasure prunes the most attack paths. The annotation is the economics: it prices the attacker's options, so the countermeasure decision becomes "which defense raises the attacker's price the most per dollar spent" — security spending is a bidding war against the attacker's budget. Limits: narrow by design — one goal per tree; building trees for every component of a large system does not scale, and the tree is only as complete as the analyst's imagination. Best for: focused analysis of the asset whose compromise is the nightmare scenario, or evaluating which of several countermeasures buys the most.

**The comparison.** No method dominates; the choice is situational:

| Dev team designing a new service | STRIDE — fits the SDLC, developers run it, DFD-native |
| Output must feed the risk register, prioritized by business impact | PASTA — risk-centric, business-framed from stage 1 |
| Standing up the practice; "what matters" unclear | OCTAVE — asset-centric, workshop-driven, non-technical participants welcome |
| One crown-jewel asset; which countermeasure buys most | Attack trees — goal-oriented, annotatable, shows pruning value |

Methods also combine: OCTAVE to find what matters, attack trees on the crown jewels, STRIDE in the SDLC for everything new, PASTA's risk framing to prioritize the combined output. The expert move is rarely one method — it is the portfolio.

**Staffing and cadence.** STRIDE needs developers plus one experienced facilitator. PASTA needs a skilled lead and threat-intel input. OCTAVE needs cross-functional workshops. Attack trees need one sharp analyst. Cadence: model at design time, revisit on material change, review annually minimum — a model older than the architecture is a historical document.

**What the output feeds.** Findings become security requirements (into `e-sdlc`), risks (into the register, with owners and dates), and test plans ("the model says this trust boundary is critical; test it"). A threat model whose output feeds nothing was theater.

### Worked example: Harbor Clinic — the methodology selection record (fictional)

**The situations (fictional).** Harbor Clinic (fictional, continued): patient portal in development, no organizational threat-modeling practice, an EHR database everyone agrees is the crown jewel, and a risk register that needs prioritizing.

**The record:**

1. **Patient portal (in development) → STRIDE.** The dev team models it in the SDLC, per data flow, at the design gate. Staffing: the team's senior developer facilitated by security, one session per major feature. Output feeds: security requirements for the build and the assessment plan. Rationale: the team builds it, so the team models it; STRIDE is the method developers can actually run. Revisit on design change.
2. **Standing up the practice → OCTAVE.** The clinic has never done organizational threat modeling; nobody agrees on what matters most. A cross-functional workshop (clinical ops, IT, management) runs OCTAVE's phase 1 to build asset-based threat profiles. Output feeds: the enterprise risk picture and the decision of *what* gets deep analysis. Rationale: the question is organizational ("what matters"), not technical — OCTAVE's workshops answer it.
3. **The EHR database → attack trees.** One asset, nightmare scenario: bulk patient-data exfiltration. An analyst builds the tree from the attacker's goal down, annotates nodes with difficulty, and evaluates three candidate countermeasures by how many paths each prunes. Output feeds: the countermeasure investment decision. Rationale: focused, quantitative comparison of defenses is exactly what trees are for.
4. **Prioritizing the combined output → PASTA's risk framing.** The findings from all three need one prioritized register. PASTA's business-impact-first framing (stage 1 objectives) ranks them by effect on the clinic's objectives, not by technical severity. Rationale: the risk committee funds by business impact — the output must speak that language.

**Why this record works:** each choice names the situation's actual question, matches the method's strength to it, staffs it realistically, and names the consumer. Any row missing the consumer field would be flagged in review — that is the theater check.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the selection record above, authored and self-reviewed in-session on 2026-10-10 against the four methodology sources. Transcript: `runs/e-threat-modeling-concepts.log` (records the per-situation rationale, the staffing, and the review checklist — no commands to transcribe).

1. **Name your situations.** Three to four from a system you know: something in development, something organizational, one crown jewel, one prioritization need. Real situations — the method choice is only as good as the situation description.
2. **Choose per situation.** STRIDE, PASTA, OCTAVE, or attack trees — or a combination. Write the choice and the one-sentence rationale tied to the method's verified strengths.
3. **Staff it.** Who runs it, who participates, what input they need (threat intel for PASTA, cross-functional workshops for OCTAVE, a sharp analyst for trees). An unstaffed method is a plan to not do it.
4. **Name the consumer.** What does each method's output feed — requirements, risk register, test plan, investment decision? No consumer, no method.
5. **Set the cadence.** Design-time, on change, annual review. Write the trigger that re-opens the model.
6. **Check for theater.** Re-read each row: did the method change a decision, or merely describe threats? If the latter, the row fails — pick the method whose output the situation can consume.

## 5. On your own

**Task:** Build the selection record for a real system or organization you know. Minimum three situations, at least two different methodologies, every row with rationale, staffing, consumer, and cadence.

**Success test:** At least one row uses a method you have never run (OCTAVE or PASTA for most readers) — with honest staffing ("facilitator to be trained" is acceptable; pretending you can facilitate PASTA cold is not). Every row names a consumer that exists — if the risk register does not exist yet, that is a finding, not a consumer.

## 6. Where it goes wrong

- **Modeling after build.** The threat model written to satisfy the gate, describing the system as built. Design-time or it is documentation.
- **The threat list with no diagram.** Findings enumerated without a model of the system — no data flows, no trust boundaries. The diagram is the analysis; the list is the exhaust.
- **STRIDE as checklist.** Six categories ticked per component with no attacker thinking. STRIDE structures the questions; it does not ask them for you. The tell: six categories ticked per component, but no attacker goal and no chained path named.
- **No attacker perspective.** Models that enumerate what *could* break without asking what an attacker *wants*. PASTA's simulation stages and attack trees exist to force this — use them.
- **The wrong instrument.** OCTAVE workshops for a feature design (months for what STRIDE does in an afternoon); attack trees for an entire enterprise (a forest nobody reads). Match the method to the question.
- **Never revisited.** The model describes last year's architecture. Tie the review trigger to the design-change process, not the calendar alone. The tell: the model's date is older than the last architecture change.
- **Theater output.** A threat model that feeds nothing — no requirements, no risks, no tests. The consumer field in the selection record is the prevention.
- **Confusing threat modeling with risk assessment.** Related, sequential, different: modeling finds what can go wrong; assessment evaluates and prioritizes. The model feeds the assessment (`e-risk-assessment`); it does not replace it.

## 7. Read the source

Primary documents first:

- **Microsoft Threat Modeling documentation** (learn.microsoft.com) — *read* the STRIDE categories and the per-component questioning method. The reference implementation for the developer's method.

Then at most three free resources:

1. **OWASP Threat Modeling Cheat Sheet** (cheatsheetseries.owasp.org) — free; the practitioner survey — process steps, method mentions (STRIDE, PASTA, OCTAVE), and cloud adaptations. Your selection-record template.
2. **Bruce Schneier, "Attack Trees"** (schneier.com, December 1999) — free; the founding paper — read the construction method and the annotation idea (cost, probability per node).
3. **SEI, "Introduction to the OCTAVE Approach"** (sei.cmu.edu, August 2003) — free; the three phases and the asset-based threat-profile concept — the organizational method's source.

## 8. Check yourself

1. A dev team models a new payment service with attack trees, producing one tree per microservice — fourteen trees nobody reads. Name the methodology error, the method that fits, and why the trees failed here.
2. Explain why STRIDE applied per component can miss a business-logic attack chain — and which method's structure (PASTA's or attack trees') catches it, and how.
3. An organization has never done threat modeling and cannot agree on its critical assets. Argue for OCTAVE over STRIDE for the first engagement — then state what STRIDE is for once OCTAVE has answered the "what matters" question.
4. A threat model's findings are filed and never referenced again. Using the consumer-field rule, diagnose the failure and name the minimum fix.
5. Predict the output of a PASTA engagement run without threat-intel input and without business stakeholders: which stages degrade, and what does the final "risk-ranked" output actually rank?

## 9. Prove it

**Artifact:** your methodology-selection record (situations, chosen methods, rationales, staffing, consumers, cadences) — for the Harbor Clinic case in your own words, or better, for a real system — plus one worked fragment in the chosen method for one situation (a STRIDE per-component pass, or an attack tree for the crown jewel).

**Honest claim:** "I can look at a threat-modeling situation, choose the methodology whose strengths match the question, staff it, set its cadence, and ensure its output feeds a real decision."
**Can't claim yet:** "I can facilitate PASTA or OCTAVE engagements" — facilitation at organizational scale is a practiced skill; this lesson taught the selection judgment. Run one with a mentor before claiming it.

## 10. Leads to

- **D-APPSEC — `e-sdlc`** — the hands-on companion: STRIDE in the development workflow, this lesson's reference implementation.
- **ai-threat-modeling — `ai-threat-modeling`** — the AI variant: methodology choice applied to AI systems.
- `e-risk-assessment`** — the consumer: threat-model output becomes risk-register entries.
- Map refs: **CISSP 1.10** (this lesson); feeds **CISSP 8.1** (security in the SDLC).
