# Assessment strategy: deciding what gets tested, by whom, and how often

**ID:** `e-assessment-strategy` · **Stage:** E (Expert) · **Level:** 3 (write an annual assessment strategy that covers the estate without gaps or waste) · **Prerequisites:** `b-methodology` (what an engagement looks like from the inside — this lesson plans the year's worth of them); no command line in this lesson.

**Map ref:** serves **CISSP objective 6.1** — designing assessment, test, and audit strategies.

---

## 1. Where this shows up

`b-methodology` taught you how one engagement runs. This lesson decides the portfolio: which systems get tested this year, by whom (internal team, external firm, or the vendor's own auditors), how often, to what depth, and under what rules. It shows up in the annual security plan ("we're doing two pentests and a red team this year — why those, and why not the ERP?"), in the audit committee's coverage question, and in the incident where the breached system turns out to be the one nobody ever scoped. GRC analysts and security leaders own this document — it is the strategy that the year's testing executes.

## 2. Before you start

- You know the engagement lifecycle from `b-methodology` — scoping, rules of engagement, reporting. This lesson writes the scoping decisions for twelve months at once.
- You have seen risk thinking (`e-risk-assessment`) — the strategy allocates testing where risk justifies it, not where it is convenient.
- No tools. The work product is an annual assessment strategy document for a fictional company.

## 3. How it works

An assessment strategy answers four questions, in order: **what** is assessed (the inventory of assessable things), **who** assesses it (internal, external, or third-party), **how often and how deep** (cadence and rigor), and **under what rules** (scoping, authorization, handling of findings). Get the order wrong and you get the common failure: a technically excellent pentest of the wrong system.

**The assessment policy comes first.** NIST SP 800-115 (§6.1) frames it plainly: the organization needs a written assessment policy before any individual assessment is planned. The policy states the purpose of testing, the authority to test, the requirement for written authorization, and the handling rules for what testers find and touch. Everything in the strategy traces to this policy; an assessment program without one is a collection of vendor contracts.

**What: the coverage inventory.** List everything that *can* be assessed: external attack surface, internal networks, cloud accounts, web applications, APIs, wireless, physical premises, people (social engineering, within legal and policy bounds), and the security processes themselves (is the SOC actually detecting?). Then prioritize (SP 800-115 §6.2): by risk (crown jewels and internet-facing first), by change (new systems and major changes get tested at launch, not at the next annual cycle), and by obligation (regulators and customers demand certain tests on certain schedules — the strategy names each obligation and the test that satisfies it). The prioritization is written with reasons, because next year's budget fight will ask why the ERP wasn't tested.

**Who: internal, external, third-party.** The three assessor classes have different strengths, and the strategy uses each where it fits:

- **Internal** (your own team): cheap, continuous, deep context — ideal for vulnerability scanning cadence, configuration review, and retesting. Weakness: familiarity blindness, and no independence for the findings the board needs to trust.
- **External** (a hired firm): independence, fresh eyes, specialized depth (a web-app firm for the app, a red team for the adversary simulation). Weakness: cost, and they test what you scope — garbage scope in, garbage findings out.
- **Third-party** (someone else's assessment you rely on): the SaaS vendor's SOC 2 report, the cloud provider's certifications. Not testing you perform — evidence you collect and evaluate. The strategy names which vendor attestations are accepted, what they cover, and where they don't reach (the vendor's SOC 2 does not test *your* configuration of their service).

**How often and how deep: cadence and viewpoints.** SP 800-115's testing viewpoints (§2.4) shape the schedule: **external** (from the internet, as the attacker starts) versus **internal** (from inside, as the attacker continues after the phishing email); **overt** (the defenders know — tests the controls) versus **covert** (the defenders don't — tests the detection). A mature year includes all four combinations across the estate, not just the annual external pentest. Cadence follows risk and change: continuous scanning for the known, periodic deep tests for the complex, event-driven tests for launches and incidents. The strategy also schedules the *retest* — findings without retesting are findings without closure.

**Under what rules: scoping discipline.** Every assessment in the strategy carries its scoping rules: written authorization naming the targets and the window, the rules of engagement (what techniques are allowed — the strategy distinguishes scanning from exploitation from social engineering, and each needs its own approval), the handling of findings (severity, reporting timeline, who sees the report), and the constraints (production hours, fragile systems, data-handling rules for anything the testers touch). Scoping is where the strategy prevents the two classic failures: the test that broke production because nobody said "not during month-end close," and the test that found nothing because the scope excluded the interesting systems.

**Technique selection** (SP 800-115 §6.3) is the strategy's method menu: which techniques apply to which targets — review techniques, discovery and scanning, validation techniques — matched to the target and the question. The companion lesson `e-control-testing` teaches the menu; this lesson decides who orders what, when.

### Worked example: Alderpoint Mutual — annual assessment strategy (fictional)

**The company (fictional).** Alderpoint Mutual: regional insurer, 600 employees, customer portal, policy admin system, a cloud data warehouse, two offices, 40-person IT.

**The strategy document (excerpts).**

*Coverage and prioritization.* Tier 1 (test deeply, test often): customer portal and its APIs (internet-facing, holds customer PII — external pentest annually, vulnerability scanning monthly, code review per release). Tier 2: internal network and identity infrastructure (internal pentest annually, covert once every two years to test the SOC). Tier 3: cloud data warehouse configuration (assessed quarterly by the internal team against benchmarks — misconfiguration is the risk, not novel vulnerabilities). Tier 4: physical and social engineering (annual, tightly scoped, legal review first). The policy admin system — Tier 1 by data, Tier 2 by exposure — gets the internal deep test because the external firm can't reach it meaningfully; the reasoning is written down.

*Who does what.* Internal team: monthly vuln scans, quarterly config reviews, retesting of all remediated highs within 30 days. External firm A (web-app specialist): annual portal pentest, overt. External firm B (red team): biennial covert exercise, scoped to exclude the claims call center during business hours. Third-party: the cloud provider's attestations accepted for the hypervisor layer only — our configuration is ours to test (the shared-responsibility line, written).

*Cadence.* Monthly: scans. Quarterly: config reviews, cloud posture review. Per-release: portal security review. Annually: external pentest, internal pentest, wireless assessment, tabletop of the IR plan. Biennially: covert red team. Event-driven: any internet-facing launch, any acquisition, any significant incident.

*Scoping rules.* Every engagement: written authorization with named targets, window, and technique approvals; production testing restricted to maintenance windows for anything beyond scanning; findings reported within 5 business days of engagement end, criticals within 24 hours; retest scheduled at remediation, not "next year." The strategy names who approves scope (CISO) and who can halt a test (any system owner, no justification required mid-incident).

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the strategy document above, authored and self-reviewed in-session on 2026-10-10 against SP 800-115 §6. Transcript: `runs/e-assessment-strategy.log`.

1. **Write the assessment policy first.** Purpose, authority, authorization requirement, findings handling — one page. No policy, no program.
2. **Inventory the assessable estate.** Every system, surface, and process — including the ones nobody wants tested (that's usually where the risk is).
3. **Prioritize with reasons.** Tiers by risk, change, and obligation. Each tier's placement gets a sentence of justification a budget-holder could challenge.
4. **Assign the assessor class per tier.** Internal, external, or third-party — with the reason (independence, depth, cost, continuity) and the known weakness of the choice.
5. **Set cadence and viewpoints.** Continuous, periodic, and event-driven; external and internal; overt and covert. The year should include all four viewpoint combinations somewhere.
6. **Write the scoping rules once.** Authorization, technique approvals, production constraints, findings timelines, halt authority — the template every engagement inherits.
7. **Schedule the retests.** Every finding class gets a retest commitment. The strategy that doesn't schedule retesting is a findings-generation program.

## 5. On your own

**Task:** Write the assessment strategy for an estate you know — your homelab (treat each service as a tier), your employer's (from memory), or a fictional company. Policy, inventory, tiers with reasons, assessor assignments, cadence, scoping rules.

**Success test:** A skeptic can point at any system and you can say when it was last tested, by whom, to what depth, when it's next, and why that cadence — and you can name one system whose tier assignment you argued with yourself about, with the reasoning that won.

## 6. Where it goes wrong

- **The annual pentest as the whole program.** One external test, once a year, of the same scope — while the estate changes monthly. The strategy must include the continuous and the event-driven, not just the annual.
- **Testing the convenient.** The portal gets tested because the firm knows web apps; the identity infrastructure doesn't because it's harder to scope. Risk decides, not convenience.
- **Scope as a shield.** The interesting systems excluded "because they're fragile" — then never tested any other way. Fragile systems get careful testing, not no testing.
- **No retest commitment.** Findings reported, remediations claimed, never verified. The retest is scheduled in the strategy, not negotiated after.
- **Third-party evidence accepted blindly.** The vendor's SOC 2 filed without reading what it covers. Your configuration of their service is your test to run.
- **Covert testing without legal cover.** Testing the SOC's detection without written authorization and legal review is an HR incident waiting to happen.
- **Technique creep.** The engagement approved for scanning quietly becomes exploitation because the tester "found something interesting." Technique approvals are per-engagement and explicit.
- **Findings without owners.** The report lands, nobody owns remediation, the same findings return next year. The strategy names the remediation ownership rule.

## 7. Read the source

Primary documents first:

- **NIST SP 800-115, Technical Guide to Information Security Testing and Assessment** (csrc.nist.gov) — *read* §6 (Security Assessment Planning: policy, prioritizing and scheduling, selecting techniques — this lesson's spine); *read* §2.4 (testing viewpoints: external/internal, overt/covert); *skim* §3–§5 as the technique catalog the strategy selects from.

Then at most three free resources:

1. **OWASP Web Security Testing Guide — the testing framework section** (owasp.org) — free; the strategy view for web applications: phases, techniques, and how to scope them.
2. **CISA: Cyber Assessments** (cisa.gov/resources-tools/resources/cyber-assessments) — free; what a risk and vulnerability assessment covers and what the customer receives — calibrate your strategy's depth expectations against it.
3. Your guidebook's own `b-methodology` — the engagement lifecycle this strategy plans a year of; reread its scoping section as the template your scoping rules generalize.

## 8. Check yourself

1. A company runs one annual external pentest of its web portal. Name three distinct coverage gaps this leaves (think: viewpoints, cadence, estate) and the strategy element that closes each.
2. The identity infrastructure is excluded from testing "because it's fragile and critical." Explain why this is backwards, and design the careful-test alternative.
3. Compare internal, external, and third-party assessment for the cloud data warehouse's configuration: which class fits, what does each miss, and where does the shared-responsibility line fall?
4. A covert red-team exercise is proposed. List the authorizations and constraints the strategy must require before it runs — and what goes wrong without each.
5. Findings from last year's pentest were "remediated" but never retested. Explain how the strategy prevents this, and who owns the failure when it happens anyway.

## 9. Prove it

**Artifact:** your annual assessment strategy — policy, coverage inventory with tiered prioritization and written reasons, assessor-class assignments, cadence (continuous, periodic, event-driven) across all four testing viewpoints, scoping-rule template, and retest commitments — for the Alderpoint worked case in your own words or an estate you know.

**Honest claim:** "I can design a year's assessment program — I can say what gets tested, by whom, how often, how deep, under what rules, and why each choice, and I can defend the coverage against a skeptic."
**Can't claim yet:** "I can execute these assessments" — performing the tests is the practitioners' work (`b-methodology`, `e-control-testing`); this lesson taught the strategy that directs it.

## 10. Leads to

- `e-control-testing` — the technique menu this strategy orders from: what each method proves and what it can't.
- `e-security-audits` — the audit half of the strategy: assurance with independence.
- `e-security-metrics` — measuring whether the strategy is working: coverage, findings, retest rates.
- `b-methodology` — the engagement this strategy plans; reread its scoping as your template.
- Map refs: **CISSP 6.1** (this lesson); feeds **CISSP 6.2** (methods), **6.5** (audits), and **1.9** (risk assessment — the prioritization input).

---

*Sources fetched 2026-10-10: NIST SP 800-115 (csrc.nist.gov); OWASP Web Security Testing Guide framework section; CISA assessment resources. Full ledger in the batch manifest.*
