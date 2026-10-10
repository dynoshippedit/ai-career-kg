---
lesson_id: ai-sec-automation
slug: ai-sec-automation
stage: AI
level: 2
prerequisites: [ai-llm-architecture, ai-llm-top10, c-soc-triage]
roles: []
map_refs: []
test_date: 2026-10-10
description: "AI security automation concepts: the SEC598 and SEC535 subject areas as concepts — every attack concept paired with its defense and defender-detectable telemetry. A free lesson in the security guidebook."
dateline: "Walkthrough finalized 2026-10-10 · runs/ai-sec-automation.log"
---
# AI security automation: concepts


**Map refs:** GASAE (SEC598) and GOAA (SEC535) subject areas as concepts — the site's lighter GASAE/GOAA knowledge maps come later.

---

## 1. Where this shows up

You are a SOC analyst, a detection engineer, or the person on a purple team who has to answer "what changes when the attacker uses AI?" The SANS subject areas for this ground are SEC598 (automation for offense, defense, and cloud) and SEC535 (AI-enabled attack techniques) — but the job never asks you to recite a syllabus. It asks you to do one thing: read an attack chain, say where automation compresses the attacker's time, and build defenses that compress your own response loop in return. AI does not invent new attack steps. It makes the old steps faster, broader, and more personalized — and that asymmetry is what you must plan against. This lesson gives you the concept map, with every attack concept paired with its defense and the telemetry that exposes it.

## 2. Before you start

- `ai-llm-architecture` — the app stack, the agent loop, and RAG: the machinery both courses' subject areas run on.
- `ai-llm-top10` — the 2026 risks; the defenses in this lesson answer specific risks from that list, not attacks in general.
- `c-soc-triage` — how an alert becomes an investigation. Know the unaccelerated workflow to judge whether automation's acceleration is honest.
- No command line. The walkthrough is a worked detection plan — a defensive work product. Tools: a text editor and the §7 sources.

## 3. How it works

**Automation vs AI automation.** Deterministic automation: *if* this alert fires, *then* run these steps. AI automation adds a model in the loop — generating text, code, or decisions — often inside an agent that plans, calls tools, observes, and plans again. The deterministic part gives repeatability; the model gives adaptability; the agent gives speed. Each gain has a defensive cost, and this lesson prices those costs.

**The compression principle.** The SEC535 subject areas contain no step an attacker could not do by hand. What models change is speed (minutes instead of days), scale (thousands of personalized lures instead of dozens), and iteration (the tool reads its own error output and adjusts). A defender tuned for a manual attacker's dwell time defends last year's threat. Your counter-move (the SEC598 half): compress your own loop until the asymmetry closes.

### The SEC598 subject areas, as concepts

**LLM-assisted detection engineering.** An analyst describes the behavior in words; the model drafts the rule; tests ship with it. Made safe by *detection-as-code*: rules versioned, peer-reviewed, run in CI against known-good and known-bad events before production. What the defender detects: rule drift, CI failures, and coverage gaps. A rule that never fired on a known-bad event is hope, not coverage.

**SOAR playbooks.** Triggers fire actions — isolate the host, revoke the session, open the ticket — without a human typing each step. Made safe by treating playbooks as code with human-in-the-loop gates on irreversible actions. What the defender detects: execution logs, failed or overridden actions, time-to-containment per run.

**Agentic investigation assistants.** RAG over your logs and docs: the model retrieves evidence and summarizes it for the analyst — the `c-soc-triage` workflow, accelerated. Made safe by read-only tools, scoped retrieval, and the prompt-injection defenses from `ai-prompt-injection` (the assistant reads attacker-controlled data every shift). What the defender detects: anomalous tool calls, out-of-scope retrieval, hallucinated citations. Trust the summary exactly as far as you verify the evidence.

**Red-team AI agents and continuous emulation.** Software that runs attacker behaviors against your own environment on a schedule to prove detections fire. Made honest by purple teaming: every emulated behavior maps to a detection, and a miss becomes a backlog item with an owner and a date. What the defender detects: the schedule, the gaps found, time-to-detect per behavior. Emulation that never misses is stale.

**Cloud automation and infrastructure as code.** Infrastructure declared in code, deployed identically. Made safe by policy-as-code plus drift detection. What the defender detects: configuration diffs and the audit trail of who changed what.

### The SEC535 subject areas, as concepts — each paired with its defense

**AI-assisted reconnaissance at scale.** Models read public data — DNS, certificate logs, job postings, exposed APIs — and assemble the target picture faster than any human. Defense: exposure reduction plus monitoring the channels attackers poll. Telemetry: DNS query spikes, certificate transparency logs, unusual API patterns, firewall/WAF probe counts, honeypot and honeytoken touches.

**AI-crafted phishing and deepfakes (text, audio, video).** Models write personalized lures and synthesize trusted voices and faces. Defense in two layers — technical: phishing-resistant MFA, DMARC/DKIM/SPF, lookalike-domain monitoring; procedural: a verification workflow for sensitive requests (call back on a known number). Telemetry: email authentication results, MFA push-challenge anomalies (an unprompted push is an attack signal), and helpdesk "was this real?" reports.

**AI-assisted web exploitation.** The model drafts injection payloads and iterates against error messages — the Stage B flaw classes with a faster assistant at the keyboard. Defense: parameterized queries, server-side validation, patching; the WAF is a speed bump, never the fix. Telemetry: WAF blocks, application error-rate spikes, request-rate anomalies on specific endpoints, failed-auth bursts.

**AI-assisted patch diffing.** Models compare pre- and post-patch binaries to find silently fixed bugs, shrinking the window between patch release and exploitability. Defense: patch quickly, prioritize by known exploitation (the KEV discipline from `c-vuln-ecosystem`), virtual-patch at the WAF where the real patch cannot ship. Telemetry: patch-lag metrics per asset class, and threat-intel showing which patches are being diffed — the window is measured, not assumed.

**AI-assisted malware, evasion, and agentic malware.** Models generate or rewrite malicious code that adapts in the environment. Defense: behavioral EDR over signatures, application allow-listing, memory-protection telemetry, least privilege. Telemetry: process-tree anomalies, unsigned DLL loads, security-service tamper events, and outbound patterns that look scheduled rather than human.

### The worked example: one automated minute, both vocabularies

A model drafts a spear-phishing lure for a finance employee (SEC535: AI-crafted phishing). The stolen session is replayed by an automated script (automated credential use). A second agent enumerates internal shares and moves laterally to a file server (automated lateral movement). At the telemetry the vocabularies meet: the gateway logs the auth result, the identity provider logs the impossible sign-in, the EDR logs the enumeration's process tree. No new steps — compressed steps. The walkthrough turns that into a plan.

## 4. Walkthrough

**No command line by design** — transcript: `runs/ai-sec-automation.log`. The walkthrough is the detection plan below, authored 2026-10-10 and validated by a script (Python 3.12.3) asserting every chain step names defender logs, detection, and response, and every attack concept carries a defense and telemetry. Reproduce the shape for your own chain.

**Scenario:** Meridian Analytics (fictional) — AI-assisted phishing → credential theft → automated lateral movement. Dwell figures are illustrative estimates, not measurements; they show where automation moves the asymmetry.

| # | Chain step (attacker concept, no instructions) | Defender logs | Detection that fires | Response | Illustrative dwell: manual → AI-automated |
|---|---|---|---|---|---|
| 1 | AI-drafted spear phishing to finance staff | Email gateway (SPF/DKIM/DMARC results, URL rewrites); lookalike-domain watch | Phishing-resistant MFA enrollment check; auth-failure + push-anomaly rule; helpdesk "is this real?" reports | Block sender domain; revoke sessions for clickers; force re-enrollment where needed | Hours to craft 50 lures → minutes to craft 5,000 |
| 2 | Credential theft and session replay | IdP sign-in logs (device, IP, ASN, session token); MFA challenge log | Impossible-travel / new-device / ASN-change rules; a push challenge nobody asked for | Revoke refresh tokens; step-up to phishing-resistant MFA; contain the account | Minutes–hours of manual replay → seconds of scripted replay |
| 3 | Automated internal enumeration (shares, users, services) | EDR process trees; SMB/RDP session logs; DNS queries to internal names | Lateral-movement Sigma rules (new-service creation, credential-dump patterns, mass SMB reads); honeytoken touches | Isolate host via playbook gate; snapshot memory for DFIR; block outbound C2-pattern traffic | Hours–days of careful manual probing → minutes of agent-driven probing |
| 4 | Automated lateral movement to the file server | NetFlow; authentication event logs; file-access audit logs | Anomalous admin-share access; first-seen service creation on the target; impossible-time file access | Isolate both hosts; rotate affected credentials; invoke the incident-response lifecycle from `c-incident-response` | Days of dwell before discovery → detection must fire in minutes or the plan has failed |

**What automation changes about dwell time.** The attacker's dwell compresses at *every* step, and the compression compounds: step 1's scale feeds step 2's speed feeds step 3's breadth. The only honest counter is compressing the detection→response loop to match — which is why SEC598 exists. Manual triage of 5,000 lures is impossible, so the plan requires enrichment automation (the gateway verdict arrives with the alert), detection-as-code (lateral-movement rules versioned and tested, not ad hoc queries), and playbook containment (isolation behind a human gate, firing in minutes). Wherever a link stays manual, the dwell column says "discovered weeks later."

**Self-review checklist** (in the log): concrete logs at every step (no "monitor the network"); detection logic families named; irreversible-action gates in every response; every attack concept paired with defense and telemetry; dwell figures labeled illustrative; no attack tooling named as a how-to.

## 5. On your own

**Task:** Pick a different AI-automated chain — AI-assisted recon → patch diffing → AI-assisted web exploitation, or deepfake vishing → helpdesk password reset → VPN access. Write its detection plan in the walkthrough's shape: numbered steps, attacker concept (no instructions), defender logs, the detection that fires, the response with its human-in-the-loop gate, and the manual-vs-automated dwell column with figures labeled illustrative.

**Success test:** A stranger can answer from your plan: what logs each step needs, which detection fires, where human gates sit, and where dwell time compresses. Any step whose defense is empty or says "best practices" fails — name the control and the telemetry.

## 6. Where it goes wrong

- **A tooling shopping list.** The SEC535 subject areas describe concepts adversaries use; your job is the defense and the telemetry, not the kit. Anyone who reads this lesson as a how-to has misread it — §9 tests that you can tell the difference.
- **Automation without gates.** The playbook that isolates hosts on any "suspicious process" alert will isolate the wrong host at 3 a.m. Irreversible actions sit behind human approval; the gate is part of the automation, not an obstacle.
- **LLM-hallucinated detections.** A model-drafted rule that never fired on a known-bad event is not coverage. Detection-as-code means the tests are the proof — versioned, peer-reviewed, run in CI.
- **Detection confused with prevention.** Email filters detect phishing; phishing-resistant MFA defeats stolen credentials. Know which layer each control lives in, or you will celebrate a detector for doing a preventer's job badly.
- **No verification workflow for voice and video.** The deepfake defense is procedural, not technical: a callback on a known number, an out-of-band confirmation. No workflow means the vishing call works regardless of tooling.
- **Stale emulations, false confidence.** Red-team AI agents that always pass are testing last year's behaviors. Rotate emulations against current techniques or the purple-team loop is theater.
- **Over-trust in agent summaries.** An investigation assistant that hallucinates a citation puts fiction in your incident report. Verify the retrieved evidence before quoting the summary.
- **Forgetting the asymmetry.** A plan that assumes manual dwell time is already beaten. The §4 dwell column is the discipline: name the compression, then the counter-compression.

## 7. Read the source

Both SEC598 and SEC535 are paid SANS courses — this lesson teaches their subject areas from free material only.

- **SEC598: AI and Security Automation for Red, Blue, and Purple Teams** (sans.org/sec598) — *read* "What You'll Learn" and the syllabus section headings (the automation subject areas); *skip* instructor bios and marketing.
- **SEC535: Offensive AI — Attack Tools and Techniques** (sans.org/sec535) — *read* "What You'll Learn" and the syllabus section headings (the AI-enabled attack subject areas); *skip* the same marketing.

Then at most three free resources:

1. **MITRE ATLAS** (atlas.mitre.org) — free; the adversary-tactics knowledge base for AI attacks. Use it as the behavior vocabulary for the SEC535 concepts: look up each concept's technique, read the data sources it lists, and turn those into your detection plan's log column.
2. **SigmaHQ sigma rule repository** (github.com/SigmaHQ/sigma) — free; community detection rules written as code. Use it as detection-as-code in practice: read how a rule declares its log source, detection logic, and false-positive notes — the shape your §5 detection column should imitate.
3. **CISA "Require Multifactor Authentication"** (cisa.gov) — free; MFA methods ranked from most to least secure, phishing-resistant first. Use it as the credential-theft defense that answers the AI-phishing concept: why automated credential replay fails against security keys.

## 8. Check yourself

1. Walk through the §4 chain and name the telemetry at each step. Explain which telemetry survives automation's speed-up (process trees, auth logs) and which degrades (human report volume, manual review queues).
2. An organization runs red-team AI agents weekly with no detection mapping. Explain the two things that go wrong and what the purple-team loop from §3 adds to fix each.
3. A SOAR playbook auto-isolates any host with a "suspicious process" alert. Name the §6 failure mode and the gate that fixes it — then explain what you lose by adding that gate.
4. Your LLM-drafted lateral-movement rule fires on 2% of all logins. Using detection-as-code practice: coverage or noise — and what must the CI tests contain for the answer to be trustworthy?
5. An executive gets a voice call from "the CEO" authorizing an urgent wire transfer. Give the defender's two-layer answer (technical control + verification workflow), name what you log, and explain which layer fails first if the workflow is missing.

## 9. Prove it

**Artifact:** your §5 detection plan — numbered steps in the walkthrough's shape, every attack concept paired with defense and telemetry, irreversible actions behind named human gates, dwell figures labeled illustrative.

**Honest claim:** "I can name the SEC598/SEC535 subject areas as concepts, pair each attack concept with its defense and telemetry, and write a detection plan for an AI-automated chain."
**Can't claim yet:** "I can build or run AI security automation or adversary tooling" — that is authorized-lab and paid-course work. This lesson is the concept map that work assumes; the map is not the territory.

## 10. Leads to

- `c-sigma-detection` — write the rules the detection column names, as versioned, tested code.
- `d-redteam-concepts` — the ATT&CK behavior language your emulation mapping and purple-team loop are expressed in.
- `ai-threat-modeling` — turn the lens around: threat-model the AI system itself, with its own trust boundaries.
- `e-incident-management` — the lifecycle your automated containment feeds; automation accelerates the loop, it does not replace it.
- Map refs: GASAE and GOAA subject areas as concepts — the site's lighter GASAE/GOAA knowledge maps come later; CAISP ch. 2 context arrives via `ai-llm-top10`.
