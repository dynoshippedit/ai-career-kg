---
lesson_id: e-security-metrics
slug: security-metrics
stage: E
level: 3
prerequisites: [c-soc-triage, c-log-sources, e-security-program]
roles: []
map_refs: ["CISSP 6.3"]
test_date: 2026-10-10
description: "Specify a SOC measurement program: KPI/KRI definitions, sources, collection, and cadence for a fictional insurer. A free lesson in the security guidebook, serving CISSP objective 6.3."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Security metrics: measuring the program without lying to yourself


**Map ref:** serves **CISSP objective 6.3** — collecting security process data.

---

## 1. Where this shows up

Every security program eventually faces the question "how are we doing?" — from the board, the auditor, or its own leadership. The honest answer is a measurement program: defined metrics, collected the same way every time, reviewed on a cadence, driving decisions. The dishonest answer is a dashboard of whatever was easy to count. It shows up in the quarterly business review where "we closed 500 tickets" meets "so what?", in the auditor's request for evidence that the process works (not just that it exists), and in the SOC that can't tell whether it's getting better. This is the measurement-program view: the machinery under the board metrics your `e-security-program` lesson teaches.

## 2. Before you start

- You know where SOC data comes from (`c-soc-triage`, `c-log-sources`) — this lesson turns that data into measures.
- You have seen the board-metrics view (`e-security-program`) — this lesson builds the program that produces numbers worth putting in front of a board.
- No tools. The work product is a metrics specification for a fictional SOC.

## 3. How it works

A **measure** is a number collected by a defined method; a **metric** is a measure interpreted against a target or trend to support a decision. The distinction matters: "47 open critical vulnerabilities" is a measure; "open criticals trending down 20% quarter over quarter against a target of under 30" is a metric. Programs drown in measures and starve for metrics — this lesson builds the latter.

**The primary: NIST SP 800-55, in its current form.** Note the edition carefully, because the old one is dead: SP 800-55 Rev. 1 (2008) was withdrawn on December 4, 2024, superseded in its entirety by **SP 800-55 Vol. 1** (*Measurement Guide for Information Security: Volume 1 — Identifying and Selecting Measures*) and **Vol. 2** (*Volume 2 — Developing an Information Security Measurement Program*), both December 2024. Vol. 1 is the measure-selection guide; Vol. 2 is the program-development guide — how to build the collection, analysis, and reporting machinery. Cite the volumes, not the withdrawn revision. The research spec's "SP 800-55" means these.

**What makes a measure worth collecting.** Vol. 1's selection logic, applied: a good measure is *relevant* (it informs a decision someone actually makes), *measurable* (the data exists and the collection method is repeatable), *actionable* (movement in the number triggers a known response), and *resistant to gaming* (the easiest way to improve the number isn't to cheat it). "Mean time to remediate critical vulnerabilities" passes: relevant to the patch program owner, measurable from scan and ticket data, actionable (rising MTTR triggers resourcing), hard to game without visible cheating. "Number of firewall rules" fails: nobody decides anything from it, and deleting rules to improve it is arson.

**KPI vs KRI.** **Key performance indicators** measure how well the program executes (patch cadence, training completion, backup verification success rate). **Key risk indicators** measure exposure (open critical vulnerabilities older than 30 days, privileged accounts without MFA, unencrypted sensitive data stores found by scans). The program needs both: KPIs without KRIs show a busy program that may still be exposed; KRIs without KPIs show risk nobody is working. The worked case below keeps them in separate sections so the review conversation stays honest — "we're performing well and still exposed" is a possible, important outcome.

**The measure specification.** Every measure gets the same six fields: **definition** (exactly what is counted, with the formula), **data source** (the system of record — the scanner, the ticketing system, the training platform — never "an analyst's spreadsheet" if a system exists), **collection method** (automated query, sampled review, attestation — and who runs it), **cadence** (daily, weekly, monthly, quarterly — matched to how fast the number can meaningfully move), **target or threshold** (the number that triggers action, with the action named), and **owner** (the person who explains the number when it's red). A measure missing any field is a dashboard decoration.

**Collection discipline.** Automate what can be automated (scanner APIs, ticket queries, log counts); sample what can't (manual control tests, configuration reviews — with the sampling method stated, because a convenience sample is a bias); attest sparingly (self-attestation is the weakest collection method and gets the shortest leash). Every collection method is documented so the number is reproducible — the next analyst, or the auditor, gets the same number from the same method. And the program states its own limits: what isn't measured, and why — the unmeasured backup-restore test is the classic gap.

**Review cadence and the anti-gaming rule.** Metrics are reviewed on their cadence by their owners, with trends, not snapshots — a single month's number is noise; six months is a story. The review asks three questions: is the number moving toward the target, do we believe the number (spot-check the collection), and is the target still right. And the program watches for gaming: when "training completion" hits 100% because the module auto-plays, the measure is broken, not the workforce — fix the collection, not the people.

### Worked example: Alderpoint Mutual — SOC metrics specification (fictional, continued)

**KPI set (excerpt).**

| Measure | Definition | Source / method | Cadence | Target → action |
|---|---|---|---|---|
| Critical vuln MTTR | Mean days from scan detection to verified remediation, criticals | Scanner + ticketing, automated query | Weekly | >30 days → program review with IT owners |
| Backup verification rate | % of backup jobs with successful test restore per schedule | Backup system logs, automated | Monthly | <100% → immediate investigation (a backup never tested is a hope) |
| Training completion | % of workforce completing annual security training | Training platform, automated | Quarterly | <95% at deadline → manager escalation |
| Phishing report rate | % of simulated phishes reported vs clicked | Simulation platform + mailbox, automated | Per campaign | Click rate rising 2 campaigns → targeted retraining |

**KRI set (excerpt).**

| Measure | Definition | Source / method | Cadence | Threshold → action |
|---|---|---|---|---|
| Aged criticals | Critical vulns open >30 days | Scanner, automated | Weekly | >10 → CISO briefing |
| Un-MFA'd privileged accounts | Privileged accounts without phishing-resistant MFA | IdP + PAM inventory, automated | Weekly | >0 → immediate remediation ticket |
| Unencrypted sensitive stores | Data stores with customer PII lacking encryption at rest | Discovery scan, quarterly sample | Quarterly | Any → risk acceptance or remediation in 30 days |
| Mean analyst triage time | Mean minutes from alert to triage decision | SIEM + ticketing, automated | Monthly | Trend review — rising means capacity or tuning problem |

**Program notes.** Collection is automated except the quarterly discovery sample (documented sampling method: stratified by data classification tier). Every measure has a named owner. The quarterly metrics review includes a gaming check: the analyst spot-checks two automated numbers by recomputing them by hand. Unmeasured and stated: mean time to *detect* (the SIEM migration in progress makes the number unreliable until Q3 — honest gap, dated).

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the metrics specification above, authored and self-reviewed in-session on 2026-10-10 against SP 800-55 Vols. 1–2. Transcript: `runs/e-security-metrics.log`.

1. **Name the decisions first.** List the decisions the program's leadership actually makes (resource allocation, risk acceptance, escalation). Every measure must serve one — or be cut.
2. **Draft the KPI/KRI sets.** Performance and risk, separate sections. Aim for ten to fifteen total; more is a dashboard, not a program.
3. **Write the six-field specification per measure.** Definition, source, method, cadence, target→action, owner. The target→action field is the one everyone skips — a metric without a triggered action is a hobby.
4. **Design the collection.** Automate, sample, or attest — with the method documented for reproducibility. Name what's unmeasured and why.
5. **Set the review cadence.** Who reviews, how often, the three questions (trend, belief, target). Include the gaming spot-check.
6. **Include the spec's required measures.** Backup verification and training completion appear in the worked case because the research spec requires them — check your program against the same bar: does it cover the unglamorous operational measures, not just the exciting ones?

## 5. On your own

**Task:** Specify five measures for something you operate — your backup scheme, your homelab patching, your personal phishing defenses. Full six-field spec per measure, one KPI-flavored, one KRI-flavored minimum. Collect the first data point by hand.

**Success test:** You can state the target→action for each ("if this number is X, I will do Y"), and at least one measure's first data point surprises you — the program's first job is telling you what you didn't know.

## 6. Where it goes wrong

- **Vanity metrics.** "Attacks blocked: 4,000,000" — the firewall counting internet background noise. Impressive, meaningless, unmoving.
- **Measures without targets.** The number is collected, reviewed, and admired. Nobody knows what value would trigger action, so nothing ever does.
- **Gaming the collection.** Training auto-plays, tickets closed without remediation, scanners excluded from the scope that would fail. The program must spot-check its own numbers.
- **The unmeasured critical.** Backup restores never tested, detection time never measured — the gaps cluster exactly where measurement is hardest, which is where it matters most.
- **Snapshot reviews.** "This month: 12." Twelve what, versus what, trending where? A number without history is a rumor.
- **Attestation as the default.** "The system owner confirms compliance quarterly." Self-reported, unverified, and the first thing an auditor discounts.
- **Metric sprawl.** Sixty measures, none owned, none reviewed. Fifteen owned measures beat sixty ornaments.
- **Citing the withdrawn revision.** SP 800-55 Rev. 1 is superseded — the program's methodology cites Vols. 1–2 (December 2024). Standards hygiene is part of measurement hygiene.

## 7. Read the source

Primary documents first:

- **NIST SP 800-55 Vol. 1, Measurement Guide for Information Security: Volume 1 — Identifying and Selecting Measures** (csrc.nist.gov, December 2024) — *read* for measure selection: what makes a measure worth collecting.
- **NIST SP 800-55 Vol. 2, Measurement Guide for Information Security: Volume 2 — Developing an Information Security Measurement Program** (csrc.nist.gov, December 2024) — *read* for program development: collection, analysis, reporting, and review. Note: these two volumes supersede the withdrawn Rev. 1 in its entirety — say so when you cite them.

Then at most three free resources:

1. **CIS Critical Security Controls** (cisecurity.org/controls) — free; the control set with example safeguards — a starting set of measurable controls to select from, not to adopt wholesale.
2. **NIST Cybersecurity Framework (CSF) 2.0** (nist.gov/cyberframework) — free; the Govern function and its measurement expectations — where your metrics plug into the framework the governance lessons use.
3. Your guidebook's own `e-security-program` — the board-metrics view this program feeds; `c-soc-triage` and `c-log-sources` — the data sources your measures draw on.

## 8. Check yourself

1. "We blocked 4 million attacks this quarter" is presented as the program's headline metric. Explain the three distinct failures (relevance, actionability, gaming-resistance) and propose the replacement measure.
2. A measure has a definition, source, and cadence but no target and no owner. Explain what breaks at the first red month — and why the target→action field is the load-bearing one.
3. Training completion hits 100% two weeks after launch. Argue the two hypotheses (genuine completion vs auto-play gaming) and design the spot-check that distinguishes them.
4. Compare a KPI and a KRI for the vulnerability program: what decision does each serve, and what does "performing well but still exposed" look like in the numbers?
5. The program doesn't measure mean time to detect because "the SIEM migration makes it unreliable." Evaluate this as a gap statement: what's honest about it, and what must be true for it to stay honest?

## 9. Prove it

**Artifact:** your metrics specification — KPI and KRI sets with the six-field spec per measure (definition, source, method, cadence, target→action, owner), the collection design with sampling methods, the review cadence with the gaming check, and the stated unmeasured gaps — for the Alderpoint worked case in your own words or a program you run, with at least one measure's first real data point collected.

**Honest claim:** "I can build a security measurement program — I can define measures worth collecting, specify their collection so they're reproducible, set targets that trigger action, and review them without fooling myself."
**Can't claim yet:** "I can present these to a board" — the board-level communication is `e-security-program`'s territory; this lesson built the program that earns the right to present.

## 10. Leads to

- `e-security-program` — the board-metrics view this program feeds; `e-assessment-strategy` and `e-control-testing` — the testing whose effectiveness these metrics measure.
- `c-soc-triage`, `c-log-sources` — the data sources; `e-test-analysis-reporting` — the findings pipeline whose aging becomes a KRI.
- Map refs: **CISSP 6.3** (this lesson); feeds **CISSP 6.1** (strategy), **6.2** (methods), and **1.3** (governance — metrics as governance evidence).

---

*Sources fetched 2026-10-10: NIST SP 800-55 Vol. 1 and Vol. 2 (csrc.nist.gov, Dec 2024); CIS Critical Security Controls (cisecurity.org/controls); NIST CSF 2.0 (nist.gov/cyberframework). Full ledger in the batch manifest.*
