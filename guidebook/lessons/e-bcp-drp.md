---
lesson_id: e-bcp-drp
slug: bcp-drp
stage: E
level: 3
prerequisites: [e-risk-assessment, c-incident-response]
roles: [grc-analyst]
map_refs: ["CISSP 1.7", "CISSP 7.10", "CISSP 7.11", "CISSP 7.12", "CISSP 7.13"]
test_date: 2026-10-09
description: "Business continuity and disaster recovery: the BIA, RTO/RPO as decisions, recovery strategy selection, and a tabletop exercise — worked end to end. A free lesson in the security guidebook, serving CISSP objectives 1.7, 7.10–7.13."
dateline: "Worked case authored and reviewed 2026-10-09 · no command line in this lesson"
---
# Business continuity and disaster recovery: deciding what survives the outage


**Map ref:** serves **CISSP objectives 1.7, 7.10, 7.11, 7.12, 7.13** — BIA and continuity requirements, recovery strategies, DR planning, DR testing, BC planning and exercises.

---

## 1. Where this shows up

Risk assessment asks "what could go wrong"; business continuity answers "when it does, what do we do Monday morning." It is the discipline behind every RTO/RPO pair in a vendor questionnaire, every tabletop exercise that found the backup nobody tested, and every outage postmortem that discovered the recovery plan assumed a data center that no longer exists. It shows up in GRC analyst work, in the operations reviews CISOs dread, and in the CISSP across two domains — because continuity is where risk management meets operations. This lesson produces the actual documents: a business impact analysis, a recovery strategy selection, a DR plan excerpt, and a tabletop exercise.

## 2. Before you start

- You can rate impact with reasons (from `e-risk-assessment`) — the BIA is impact analysis with operational teeth.
- You have read `c-incident-response` — continuity begins where incident response ends (the incident is contained; now the business must run).
- No tools. The work products are documents for a fictional company. Primary spine: **NIST SP 800-34 Rev. 1** (Contingency Planning Guide, May 2010 — old but still the current revision; the lesson notes where practice has moved on).

## 3. How it works

**The BIA comes first, always.** The **Business Impact Analysis** identifies what matters before anyone plans how to protect it. For each business process you determine: what breaks if it stops, how bad it gets over time, what it depends on, and how fast it must come back. Two decisions fall out of the BIA and everything else hangs on them:

- **RTO (Recovery Time Objective):** how long the process can be down. "The ordering system must be back within 4 hours" — a *decision*, made by the business, not by IT.
- **RPO (Recovery Point Objective):** how much data loss is tolerable. "We can lose at most 15 minutes of orders" — which dictates backup frequency, replication, and journaling.

RTO without RPO is half a plan (the system is up but yesterday's data is gone); RPO without RTO is the other half (no data lost, but nothing runs for a week). Both are business decisions with technical consequences — and both must be *achievable*: an RTO of 4 hours with backups restored by hand from tape is fiction, and the BIA process is where that fiction gets exposed.

**Continuity vs recovery.** **Business continuity (BC)** keeps the *business* running during the disruption — manual workarounds, alternate sites, rerouted phones. **Disaster recovery (DR)** brings the *systems* back — failover, restore, rebuild. BC is the bridge; DR is the repair. Plans that only do DR answer "how do we restore the servers" while the business bleeds for the 48 hours the restore takes.

**Recovery strategies** are chosen per system, matched to its RTO/RPO:

- **Backups** (with tested restores — an untested backup is a hope): cheap, slow; fits long RTO/RPO.
- **Alternate sites** — *cold* (space, no equipment), *warm* (equipment, no live data), *hot* (live, ready): increasing cost, decreasing recovery time. The strategy must match the RTO honestly — a 4-hour RTO cannot rest on a cold site three states away.
- **Cloud failover / replication:** the modern hot site, but with its own dependencies (the failover region, the replication lag, the runbook for declaring the failover — *who decides, and on what evidence*).
- **Resilience options:** high availability, geographic distribution, degraded-mode operation (the ordering system takes phone orders while the site is down — a BC measure, not a DR one).

**The plans.** SP 800-34's structure: the **Business Continuity Plan** (keep operating), the **Disaster Recovery Plan** (restore systems), plus supporting plans (incident response — your `c-incident-response` lesson — occupant emergency, communications). A DR plan excerpt contains: activation criteria and authority (who declares a disaster — this decision made *during* the outage is how hours get lost), roles and contact trees, communications plan (who tells customers, in what words, through which channel), system recovery procedures in order (dependencies first — restore the database before the app that reads it), and the return-to-normal plan (failback is a second migration, planned with the same care).

**Testing: the plan is a hypothesis.** Untested plans fail in predictable ways — contact trees with departed employees, recovery steps for decommissioned systems, RTOs nobody validated. The test ladder, cheapest first:

1. **Checklist review** (read the plan; does it still describe reality?)
2. **Tabletop exercise** (walk a scenario around a table; find the decisions nobody made)
3. **Simulation** (execute recovery steps without failing over)
4. **Full failover test** (actually cut over — the only test that validates the RTO)

Most organizations live at levels 1–2; the lesson's position is that level 2 done honestly beats level 4 done as theater. A tabletop that surfaces "nobody knows who declares the failover" has paid for itself.

### Worked example: Beacon Logistics — BIA, strategy, plan excerpt, tabletop

**The company (fictional, continued from `e-risk-assessment`).** Beacon Logistics: regional freight, 120 staff. The outage: a ransomware event encrypts the primary data center on a Tuesday at 03:00. Incident response contains it by 09:00 (`c-incident-response`'s territory). Now continuity takes over.

**BIA (three critical processes).**

| Process | Impact if down | Dependencies | RTO | RPO |
|---|---|---|---|---|
| Dispatch operations (assigning loads to drivers) | After 4h: missed pickups, contract penalties; after 24h: customer losses | Dispatch app, driver phones/SMS, customer shipment data (≤15 min old) | 4 hours | 15 minutes |
| Customer shipment tracking portal | Reputational; support queue floods within hours; no safety impact | Web portal, tracking database | 8 hours | 1 hour |
| Billing and invoicing | No immediate operational impact; cash-flow impact after ~2 weeks | Billing system, last month's data | 72 hours | 24 hours |

Note what the BIA *decided*: dispatch is the business — 4-hour RTO drives strategy. Billing can wait three days; spending hot-site money on billing would be misallocated resilience.

**Recovery strategy selection.** Dispatch (RTO 4h, RPO 15min): warm standby in a second region with continuous replication (15-min lag verified, not assumed) + documented manual-dispatch workaround (phones, paper manifests — the BC bridge for the first hours). Tracking portal (8h/1h): rebuild from nightly backups plus hourly database replication; acceptable degradation — a static "we're recovering" page with phone numbers (BC measure). Billing (72h/24h): nightly backups, restore to any available compute. *Trade-off recorded:* the warm standby costs the most and protects the process the BIA ranked first — resilience spending follows the BIA, not anxiety.

**DR plan excerpt — dispatch system.** *Activation:* the operations director declares a disaster when dispatch is down >1 hour with no ETA, on the incident commander's recommendation — authority named in advance, not improvised. *Order of operations:* 1) declare and notify (customer comms template attached — pre-written words, not drafted mid-crisis); 2) shift to manual dispatch (BC bridge — phones/paper, driver call tree); 3) fail over to the warm site (runbook: promote replica, repoint DNS, verify with the dispatch smoke test); 4) validate data currency (replication lag check — the 15-minute RPO verified, not assumed); 5) failback plan drafted before failover completes (the return trip is a migration). *Roles:* named individuals with backups for each role — the plan lists people, not titles.

**Tabletop exercise (the test).** Scenario: the ransomware hits during the driver's shift change, and the warm-site failover engineer is on vacation. Injects: (1) the replica lag is 45 minutes, not 15 — do you fail over with 30 minutes of dispatch data missing, or wait? (2) a major customer demands a status call in 20 minutes — who speaks, with what words? (3) the DNS repoint propagates slowly — half the drivers see the old site. *Findings recorded:* the failover authority was ambiguous between two managers (fixed: single named authority); the customer comms template didn't cover partial data loss (fixed: template updated); nobody had tested the manual-dispatch paper forms in two years (fixed: quarterly drill added). The exercise found three real gaps in ninety minutes — which is the point.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" for this lesson is the BIA, strategy selection, plan excerpt, and tabletop above, authored and self-reviewed in-session on 2026-10-09 against SP 800-34's structure. Transcript: `runs/e-bcp-drp.log` (records scope, BIA decisions, strategy rationale, and review notes).

1. **Pick the processes.** Three to five business processes for your fictional (or real lab) organization. For each: what breaks over time if it stops — hour 1, hour 4, day 3. The time dimension is the analysis; "it's critical" without a timeline is not a BIA.
2. **Set RTO/RPO as decisions.** Each pair gets a one-sentence business justification. Then the achievability check: describe, concretely, how the RTO would be met with current capabilities. Any RTO that requires capabilities you don't have is fiction — either change the strategy or change the objective, in writing.
3. **Select strategies.** Per process, matched to its RTO/RPO, with the trade-off recorded. Resilience spending must trace to BIA ranking — if your most expensive protection guards your least critical process, say so and fix it.
4. **Write the plan excerpt.** Activation authority (named person), role list (named people with backups), communications (pre-written templates), ordered recovery steps (dependencies first), failback plan. If any role says "the IT team" instead of a name, it is not a plan.
5. **Run the tabletop.** One scenario, three injects, 90 minutes. Record findings as decisions with owners and dates — the same discipline as `e-risk-assessment`. You should find at least two genuine gaps; a tabletop that finds nothing was too kind.
6. **Schedule the next test.** The plan decays from the day it is written (staff leave, systems change). Date the next review and name its owner.

## 5. On your own

**Task:** Write a BIA and recovery plan for a system you actually run — your homelab, your VPS hosting a side project, your backup scheme. Set real RTO/RPO, select strategies you can actually execute, and then *test the restore* — the one step fictional exercises skip.

**Success test:** You attempt a real restore (or failover) and it either works within your stated RTO — or it doesn't, and you have found the gap the tabletop would have found. An untested restore procedure is the most common finding in this discipline; do not let your own plan carry it.

## 6. Where it goes wrong

- **The untested backup.** The most common DR finding in existence. Backups complete nightly; nobody has restored in two years; the restore needs a tape drive that was decommissioned. Test restores are the cheapest validation in the discipline — their absence is negligence, not bad luck.
- **RTO as wish.** "Four hours" chosen because it sounds responsible, with no capability behind it. The achievability check in the walkthrough exists to kill these — an RTO is a claim about your systems, and claims need evidence.
- **DR without BC.** The servers restore in 48 hours; the business needed to operate during those 48 hours. The manual workaround (phones, paper, degraded mode) is unglamorous and is usually what actually saves the quarter.
- **Ambiguous authority.** Nobody named to declare the disaster, so the declaration happens three hours late while managers conference. Authority named in advance, with a backup, is a one-line fix with outsized returns.
- **Failback forgotten.** The failover succeeds; the return to primary is improvised six weeks later and causes a second outage. Failback is a migration — plan it before you fail over.
- **The plan describes a dead company.** Contact trees with departed staff, recovery steps for decommissioned systems, vendors under old contracts. Plans decay; the review date is load-bearing.
- **Testing as theater.** The tabletop where every inject is answered with "we'd handle it" and no finding is recorded. A test with no findings tested nothing — inject harder until something breaks, because the outage will.
- **SP 800-34's age.** Rev. 1 is from May 2010 — still the current revision, but written before cloud-native architectures. Its structure (BIA → strategy → plan → test) endures; its technology assumptions don't. Apply the structure, modernize the mechanisms, and say so when you cite it.

## 7. Read the source

Primary documents first:

- **NIST SP 800-34 Rev. 1, Contingency Planning Guide** (csrc.nist.gov, May 2010) — *read* the contingency planning process and plan structure; *note* its age honestly (see §6). The structure is the standard; the examples are dated.
- **ISO 22301 (business continuity management)** — paid standard; one line per the brief's rule. Teach from free equivalents: the BCI's free good-practice summaries and vendor-neutral BC planning guides.
- **NIST SP 800-53, Contingency Planning family (CP)** (csrc.nist.gov) — *skim* as the control catalog: CP-2 (the plan), CP-4 (testing), CP-9 (backups) map directly to this lesson's sections.

Then at most three free resources:

1. **CISA: business continuity planning resources** (cisa.gov) — free; tabletop exercise packages and planning templates.
2. **NIST CSF 2.0, Recover function (RC)** (nvlpubs.nist.gov) — free; where continuity lives in the framework your governance lessons use.
3. **SANS: disaster recovery plan template** (sans.org, free policy templates) — free; a starting skeleton for the plan excerpt — fill it, don't file it.

## 8. Check yourself

1. Explain why the BIA must precede strategy selection — what goes wrong, concretely, when an organization buys the warm standby before doing the BIA? Use the billing-vs-dispatch example.
2. A DR plan restores all systems within the RTO but the business still loses a week of revenue. Name the missing half of the discipline and the specific artifact that would have covered it.
3. During a tabletop, the replica lag is 45 minutes against a 15-minute RPO. Lay out the decision: who decides, what the options are, and what information the decider needs in the next ten minutes.
4. Distinguish a test of activity from a test of effectiveness for DR: which rung of the test ladder validates the RTO, and why do honest level-2 tabletops beat theatrical level-4 failovers?
5. Predict the state of a DR plan three years after its author leaves, with no review date ever set: which section decays first, and what kind of incident reveals the decay?

## 9. Prove it

**Artifact:** your BIA (processes, time-phased impacts, dependencies, RTO/RPO with justifications and achievability checks), strategy selection with trade-offs, DR plan excerpt (named authority, named roles, comms templates, ordered steps, failback), and tabletop findings with decisions/owners/dates — for the Beacon worked case in your own words, or better, for a system you actually run, with a real restore test.

**Honest claim:** "I can determine what a business needs to survive an outage and build the plan to deliver it — BIA, strategy, tested procedures, and the exercises that keep them honest."
**Can't claim yet:** "I can run enterprise BC/DR at scale" — multi-site programs, regulatory continuity obligations, and crisis management at organizational scale are their own practice; this lesson taught the method on one system, which is where the judgment is formed.

## 10. Leads to

- **E-GOV-01 — NIST CSF 2.0** — continuity lives in the Recover function; the BIA feeds the Current-vs-Target profile.
- **E-D7-10 — Recovery strategies** — the deep companion: strategy selection as its own discipline.
- `e-risk-assessment` — the BIA's sibling: impact analysis feeding risk decisions; `c-incident-response` — the handoff point where IR ends and continuity begins.
- Map refs: **CISSP 1.7, 7.10, 7.11, 7.12, 7.13** (this lesson).
