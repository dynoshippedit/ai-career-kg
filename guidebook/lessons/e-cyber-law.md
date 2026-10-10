---
lesson_id: e-cyber-law
slug: cyber-law
stage: E
level: 3
prerequisites: [e-risk-assessment, e-governance]
roles: []
map_refs: ["CISSP 1.4"]
test_date: 2026-10-10
description: "Build an obligation-to-evidence compliance matrix from GDPR and related regimes. A free lesson in the security guidebook, serving CISSP objective 1.4."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Legal, regulatory, and compliance: mapping obligations to evidence


**Map ref:** serves **CISSP objective 1.4** — legal, regulatory, and compliance landscape.

---

## 1. Where this shows up

This is the compliance-program view of the law — not "what is a crime" (that is `b-authorization-scope`: the CFAA and the UK Computer Misuse Act as the authorization boundary) but "what the organization owes, to whom, and how it proves it." It shows up in the vendor questionnaire asking for your Article 30 records; in the 72-hour breach-notification clock that starts at *awareness*, not certainty; in the data-processing agreement your biggest customer sends you; in the decision about whether you need a data protection officer; and in the board question "what happens if we get this wrong" — where the answer is a number from Article 83, not a shrug. The security practitioner's job here is translation: turn legal obligations into controls, evidence, owners, and test cadences.

## 2. Before you start

- You can write a risk statement from `e-risk-assessment` — a legal obligation is a risk whose likelihood includes "the regulator notices" and whose impact is written in the statute.
- You have the governance machinery from `e-governance` — every obligation below needs an owner, and the charter is where ownership lives.
- Process literacy, not legal advice: the worked case shows how a practitioner maps obligations; interpretation in a dispute belongs to counsel.

## 3. How it works

**The method: obligation to evidence.** Every compliance program runs five steps: (1) identify which obligations apply (jurisdiction, sector, data types); (2) translate each into controls; (3) assign an owner; (4) define the evidence proving compliance; (5) test on a cadence. Steps 2 and 4 are the practitioner's core contribution — lawyers name the obligations; you build the machinery and the evidence. A control without evidence is an opinion; evidence without a test cadence is history.

**GDPR as the worked regime.** Regulation (EU) 2016/679 of 27 April 2016 — the General Data Protection Regulation, full text fetched in-session from EUR-Lex. The articles below were read directly; everything stated here is traceable to them:

- **Principles (Article 5):** personal data must be processed lawfully, fairly and transparently; collected for specified, explicit, legitimate purposes (purpose limitation); adequate, relevant, limited to what is necessary (data minimisation); accurate and kept up to date (accuracy); kept identifiable no longer than necessary (storage limitation); processed securely (integrity and confidentiality). Then the load-bearing second paragraph: the controller is responsible for *and must be able to demonstrate* compliance with all of this — **accountability**. Article 5(2) is the entire compliance-program industry in one sentence: it is not enough to comply; you must be able to prove it.
- **Lawful bases (Article 6):** processing is lawful only with at least one of six bases — consent, contract, legal obligation, vital interests, public task, legitimate interests. "We have consent" is the most abused sentence in privacy: Article 7 requires consent to be demonstrable, distinguishable, and as easy to withdraw as to give. If withdrawing consent is harder than giving it, you do not have consent.
- **Breach notification (Articles 33–34):** the controller notifies the supervisory authority *without undue delay and, where feasible, not later than 72 hours after becoming aware* of a personal data breach — unless unlikely to risk individuals' rights. The processor notifies the controller without undue delay. If the breach is likely high-risk to individuals, the controller communicates it to the data subjects directly, in clear language. Two practitioner notes: the clock starts at *awareness*, not certainty — "we're still investigating" does not pause it, though information may be provided in phases; and Article 33(5) requires documenting *every* breach with facts, effects, and remedial action, so the authority can verify compliance.
- **DPIA (Article 35):** a data protection impact assessment is required *before* processing likely to create high risk — including systematic large-scale evaluation (profiling), large-scale processing of special-category data, and large-scale systematic monitoring of public areas. The DPIA is the compliance analogue of threat modeling: done before the build, not after the incident.
- **DPO (Articles 37–38):** a data protection officer is mandatory for public authorities, for core activities involving large-scale systematic monitoring, and for large-scale processing of special categories of data. The DPO is designated for expert knowledge, receives no instructions on how to do the job, cannot be penalised for doing it, and reports to the highest management level. A DPO who reports to the marketing director is decoration.
- **Enforcement (Article 83):** two tiers of administrative fines — up to EUR 10 million or 2% of worldwide annual turnover (whichever is higher) for violations of controller/processor obligations including Articles 25–39; up to EUR 20 million or 4% for violations of the principles, data-subject rights, and third-country transfer rules. The fine is per-infringement and calibrated to gravity, cooperation, and mitigation — which is why the evidence in step 4 of the method is also fine mitigation.

**Cross-border transfers (Chapter V, Articles 44–49).** Personal data leaving the EEA needs a Chapter V basis — an adequacy decision, appropriate safeguards (such as standard contractual clauses), or a derogation. The practitioner translation: every vendor, subprocess, and cloud region outside the EEA is a transfer that needs a named basis and evidence. "Our cloud provider handles it" is not a basis.

**Beyond GDPR: the landscape in brief.** A compliance program maps more than one regime — same method, different obligations:

- **Sectoral and national privacy law:** health, financial, children's, and breach-notification statutes each carry their own clocks and thresholds. Record each regime's trigger, timeline, and evidence separately — one "breach procedure" assuming a single 72-hour rule misses the shorter ones.
- **Intellectual property:** trade secrets (protected by access controls and need-to-know — `e-iam` is IP protection in practice), copyright, licensing. The practitioner's contribution is technical: show who accessed the secret, when, under what authorization.
- **Import/export controls:** cryptography is subject to export regulation in many jurisdictions — the product decision "which cipher suite ships where" has a legal dimension. Know that the dimension exists; counsel navigates it.
- **Cybercrime law:** what counts as unauthorized access and what must be preserved for law enforcement — `b-authorization-scope` (the crime view) and `e-investigations` (the investigation view). This lesson's rule: the compliance program must not destroy what an investigation needs.

**The AI angle.** Regulation (EU) 2024/1689 of 13 June 2024 — the EU Artificial Intelligence Act, fetched in-session from EUR-Lex — lays down harmonised rules for AI systems across the internal market, with common rules for high-risk AI systems and explicit complementarity with data protection law. For the compliance program, the AI Act is a new column in the same matrix: if the organization deploys AI systems, the mapping gains obligations (risk management, documentation, human oversight — per the Act's structure) with the same five steps. Cross-reference: `ai-governance`.

### Worked example: Bluefin Retail — the compliance-mapping matrix (fictional)

**The company (fictional).** Bluefin Retail: US-based e-commerce, 180 staff, selling to EU customers. Holds names, addresses, payment tokens, purchase history, and a loyalty-program analytics pipeline. No DPO, no Article 30 records, breach procedure written for a single US state law.

**The matrix (abridged — the full version is the artifact).** Columns: obligation, legal basis, owner, control, evidence, test cadence.

1. **Lawful basis for marketing (Art 6):** email marketing currently runs on pre-ticked consent. *Control:* move to affirmative opt-in meeting Article 7 (demonstrable, withdrawable in one click). *Owner:* marketing lead. *Evidence:* consent records with timestamp and wording version. *Cadence:* quarterly sampling.
2. **Records of processing (Art 30):** none exist. *Control:* build the register — purposes, categories, recipients, retention, security measures. *Owner:* privacy lead (to hire). *Evidence:* the register itself, version-controlled. *Cadence:* reviewed on every new processing activity.
3. **Breach notification (Art 33/34):** current procedure assumes a single US timeline. *Control:* rewrite the runbook with the 72-hour authority clock, the processor-to-controller notification clause in vendor contracts, and the high-risk communication templates. *Owner:* security lead. *Evidence:* tabletop exercise records, notification log. *Cadence:* annual tabletop.
4. **DPIA for loyalty analytics (Art 35):** large-scale profiling for marketing. *Control:* conduct the DPIA before the next model retrain — necessity, proportionality, risks, mitigations. *Owner:* data science lead with privacy lead. *Evidence:* the DPIA document and its review record. *Cadence:* revisit on material change.
5. **DPO decision (Art 37):** core activities include large-scale systematic monitoring (behavioral analytics). *Control:* designate a DPO with direct reporting to the CEO and no conflicting duties. *Owner:* CEO. *Evidence:* designation letter, reporting line in the org chart. *Cadence:* annual independence check.
6. **US processing of EU data (Chapter V):** customer data processed in US cloud regions. *Control:* name the transfer basis per flow (clauses, derogations) and record it in the Article 30 register. *Owner:* privacy lead. *Evidence:* executed clauses, transfer impact notes. *Cadence:* annual re-verification.
7. **Fine exposure (Art 83):** board briefing. *Control:* one-page brief — the two tiers, what moves a fine up (no cooperation, no mitigation evidence) and down. *Owner:* General Counsel. *Evidence:* the brief and the board minutes. *Cadence:* annual.

**What the matrix does:** it turns "GDPR applies to us" into 7 owned, evidenced, tested work items. The board can read it. An auditor can test it. That is the compliance program.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the Bluefin matrix above, authored and self-reviewed in-session on 2026-10-10 against the GDPR articles read from EUR-Lex. Transcript: `runs/e-cyber-law.log` (records the matrix rows, the article-to-row traceability, and the review checklist — no commands to transcribe).

1. **List your regimes.** For your fictional (or real) organization: which jurisdictions, which sectors, which data types. Each combination is a potential row. Do not assume one regime — the map starts by enumerating.
2. **Extract the obligations.** For each regime, list the concrete obligations with article/section numbers — not "do privacy" but "Art 33: notify within 72 hours of awareness." Numbered obligations are testable; vibes are not.
3. **Translate to controls.** For each obligation, write the control in one sentence. If you cannot state it, the obligation is not yet understood — go back to the text.
4. **Assign owners and evidence.** Every row gets a named owner and a named evidence artifact. "The team" is not an owner; "we comply" is not evidence.
5. **Set the test cadence.** How often is each row verified, and by whom. Rows without a cadence decay — the matrix is a living document with review dates, per `e-governance`.
6. **Brief the board.** One page: regimes, top three exposures, owners. If the board cannot understand the exposure, the mapping failed its primary job.

## 5. On your own

**Task:** Build the matrix for an organization you know (your employer, your side project's user base, or a fictional company). Minimum eight rows across at least two regimes — GDPR plus one more (a breach-notification statute, a sectoral rule, or the AI Act if AI systems are in play).

**Success test:** Every row has a numbered obligation, a named owner, a named evidence artifact, and a test cadence. At least one row changed something real — a procedure rewritten, a missing record created. If the matrix describes only things already done, it is a description, not a program.

## 6. Where it goes wrong

- **The lawyer-only program.** Obligations identified, no controls built, no evidence defined. The law named the target; nobody built the machinery.
- **"We have consent."** Pre-ticked boxes, bundled terms, withdrawal harder than opt-in — Article 7 fails all three, and the lawful basis evaporates under examination.
- **The awareness fallacy.** The 72-hour clock starts at awareness, not certainty. Teams that wait until "we're sure" breach Article 33 while investigating the breach.
- **One clock for all regimes.** A breach procedure written for one jurisdiction's timeline, silently missing the shorter ones. Map each regime's trigger and timeline separately.
- **The decorative DPO.** Designated, then given conflicting duties or buried in the org chart. Articles 37–38 describe independence in operational terms — reporting line, no instructions, no penalty.
- **Transfer blindness.** Data flows to vendors and regions nobody mapped; Chapter V needs a named basis per flow, and "the cloud handles it" is not one.
- **Evidence as afterthought.** Controls built, nothing recorded. Article 5(2) requires *demonstrable* compliance — the evidence column is not paperwork, it is the compliance itself.
- **The matrix as a monument.** Built once, never reviewed, describing an organization that has since changed. Review dates are load-bearing — `e-governance`'s rule.

## 7. Read the source

Primary documents first:

- **Regulation (EU) 2016/679 — General Data Protection Regulation** (eur-lex.europa.eu) — *read* Articles 5, 6, 7, 33, 34, 35, 37, 38, 83 and Chapter V (Articles 44–49). The regulation is the obligation; everything else is commentary.

Then at most three free resources:

1. **NIST Privacy Framework v1.0** (nist.gov) — free; the outcomes-based privacy-risk framework — use it to structure the controls column of your matrix (Identify, Govern, Control, Communicate, Protect).
2. **Regulation (EU) 2024/1689 — EU Artificial Intelligence Act** (eur-lex.europa.eu) — free; the AI column of the matrix — read the scope and the high-risk provisions before your organization deploys AI systems affecting people.

## 8. Check yourself

1. Your breach procedure says "notify the authority within 72 hours of confirming the breach." Identify the two errors in that sentence against Article 33, and rewrite it correctly.
2. A marketing team claims consent via a pre-ticked checkbox with withdrawal by mailed letter. Walk Article 7's three conditions and state which fail — and what the lawful-basis consequence is.
3. Explain why the Article 30 register and the Chapter V transfer record are the same document in practice: what breaks when an organization keeps them separately, or keeps neither?
4. A company designates its General Counsel's junior associate as DPO, reporting to the VP of Marketing, alongside a full marketing-ops workload. Name every Article 37–38 problem in that arrangement.
5. Predict the state of a compliance matrix two years after its author leaves, with no review cadence ever set: which rows decay first, and what event reveals the decay?

## 9. Prove it

**Artifact:** your obligation-to-evidence matrix (regimes, numbered obligations, controls, named owners, named evidence artifacts, test cadences) — for the Bluefin worked case in your own words, or better, for a real organization — plus the one-page board brief.

**Honest claim:** "I can take a regulatory regime, extract its testable obligations, and build the program that satisfies them — controls, owners, evidence, cadences — and brief the exposure to a board."
**Can't claim yet:** "I can give legal advice on regulatory interpretation" — obligation *mapping* is the practitioner's work; obligation *interpretation* in a dispute belongs to counsel. This lesson taught the machinery, not the lawyering.

## 10. Leads to

- `e-investigations` — when obligations become incidents: the investigation types the breach clock triggers.
- `e-policy-docs` — the policy tier that carries the controls column into the organization.
- **ai-governance — `ai-governance`** — the AI Act column of the matrix, in depth.
- Map refs: **CISSP 1.4** (this lesson); feeds **CISSP 1.5** (investigations) and **2.6** (data protection controls).
