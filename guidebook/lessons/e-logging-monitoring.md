---
lesson_id: e-logging-monitoring
slug: logging-monitoring
stage: E
level: 3
prerequisites: [c-log-sources, c-soc-triage]
roles: []
map_refs: ["CISSP 7.2"]
test_date: 2026-10-10
description: "How to design the logging and monitoring program — event taxonomy, retention schedule, log integrity, and the SOC workflow that turns logs into detections. A free lesson in the security guidebook, serving CISSP objective 7.2."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Logging and monitoring operations: deciding what gets watched, and by whom


**Map ref:** serves **CISSP objective 7.2** — logging and monitoring as an operations discipline: event selection, retention, and the monitoring program.

---

## 1. Where this shows up

Every detection the SOC ever makes rests on a decision somebody made months earlier: log this event, keep it this long, send it to the people watching. Logging and monitoring operations is the discipline of making those decisions deliberately — the event taxonomy (what's worth recording), the retention policy (how long each category lives, and where), and the monitoring program (who watches, how alerts get tuned, how coverage is measured). It shows up in the breach where the evidence aged out at 30 days, in the SOC drowning in unactionable alerts, and in the audit finding that nobody reviews the firewall logs anyone. SOC managers, detection engineers, and GRC analysts live here. Note the split with `c-log-sources`: that lesson taught you to parse a log line. This lesson teaches the organization's decisions about which log lines exist at all, how long they survive, and what the watch floor does with them.

## 2. Before you start

- You can read logs from `c-log-sources` — you know what an event record contains, which is the raw material this lesson budgets.
- You know the triage workflow from `c-soc-triage` — this lesson designs the staffing, tuning, and coverage around it.
- No tools. The work products are documents: a logging policy excerpt, a retention schedule, and a SOC workflow design. Primary spine: **NIST SP 800-92** (Guide to Computer Security Log Management, September 2006 — old, and the lesson is honest about what's changed since).

## 3. How it works

Logs are not exhaust; they are instrumentation you choose to install. The operations view has four decisions.

**What to log: the event taxonomy.** You cannot log everything — volume, cost, and noise forbid it — so you decide per category. SP 800-92's enduring contribution is the log-management lifecycle: **generation, transmission, storage, analysis, disposal**. Generation is the decision point: which events, from which sources, at what verbosity. The working taxonomy most programs converge on: **authentication events** (successes and failures — the highest signal-per-byte category in existence); **authorization decisions** (access granted/denied, privilege use); **system and service events** (starts, stops, crashes, configuration changes); **network security events** (firewall denies, IDS alerts, DNS queries at the boundary); **application events** (transactions, errors, admin actions); and **physical/environmental events** (badge access, power, temperature — the `e-physical-security` feed). Each category gets a required source list: authentication from the IdP and every server, DNS from the resolvers, and so on. The test of the taxonomy is coverage against the threats you care about: for each detection your program claims, name the log source that feeds it. A detection with no source is a wish.

**Integrity and time: the two properties that make logs evidence.** A log you can't trust is worse than no log — it invites confident wrong conclusions. Two controls carry the weight. **Time synchronization:** every source on NTP (or equivalent), because correlation across sources is meaningless if the clocks disagree by minutes; the policy names the time source, the allowed skew, and the alert when a host drifts. **Integrity protection:** logs transmitted over protected channels, stored where the generating system can't rewrite them (append-only forwarding to a central collector), with access restricted to the SOC and auditors. If an attacker who compromises a server can edit that server's local logs, the local logs are the attacker's alibi — centralize first, then analyze.

**Retention: how long each category lives, and where.** Retention is a three-way negotiation between investigation needs, legal obligations, and storage cost. The standard structure is **tiers**: hot (online, searchable, ~30–90 days for high-volume categories), warm (online but slower, ~1 year), cold (archived, retrievable within days, multi-year for the categories law or policy requires). The schedule is per-category, not per-system: authentication logs might be hot 90 days / warm 1 year / cold 7 years (employment and legal actions run long), while debug-level application logs are hot 14 days and then gone. Two rules: retention periods are written with their justification (legal citation, investigation window, or explicit risk acceptance), and **disposal is a procedure, not an accident** — when the retention period ends, deletion follows the documented process, and litigation hold suspends it (the `e-investigation-forensics` link: your retention schedule is the evidence base, and the hold is what freezes it).

**The monitoring program: who watches and how it improves.** Logs nobody watches are archaeology. The program has three parts. **The SOC workflow:** tiered analysis — Tier 1 triages against playbooks (the `c-soc-triage` workflow), Tier 2 investigates the ambiguous, Tier 3 hunts and engineers detections — with defined handoffs, escalation criteria, and staffing for the hours you claim to cover (a "24/7 SOC" with one analyst on nights is a slogan). **Alert tuning as a process, not an event:** every alert has an owner, a false-positive rate that's measured, and a tuning loop — triage findings feed back to detection engineering, which adjusts thresholds, adds context, or retires the rule. An alert nobody tunes becomes either ignored (alert fatigue) or a pager that cries wolf; both are tuning failures. **Coverage measurement:** the program tracks what fraction of the event taxonomy is actually collected, what fraction of alerts have current tuning reviews, and mean time to detect/triage — the metrics that tell you whether monitoring is operating or merely installed. SP 800-92's age shows here: it predates the SIEM-to-XDR evolution and cloud-native log pipelines, but the lifecycle (generate → transmit → store → analyze → dispose) still describes every pipeline, whatever the vendor calls the boxes.

### Worked example: Beacon Logistics — the logging program

**The company (fictional, continued from `e-bcp-drp`).** Beacon Logistics, 120 staff, regional freight. The dispatch system is the crown jewel (4-hour RTO from the BIA). Today: each server keeps local logs, retention is "until the disk fills," and one analyst watches a SIEM nobody tuned since installation.

**The event taxonomy (excerpt).** Authentication (IdP, VPN, all servers — success and failure); dispatch-application transactions and admin actions; firewall denies and IDS alerts at both sites; DNS queries from internal resolvers; badge-access events from the office system. Each maps to a detection: impossible-travel logins need IdP successes; data-exfiltration hypotheses need firewall denies plus DLP; the ransomware scenario from `e-bcp-drp` needs the dispatch app's admin-action log. Three claimed detections had no source — recorded as gaps, not coverage.

**The retention schedule (excerpt, fictional).**

| Category | Hot | Warm | Cold | Justification |
|---|---|---|---|---|
| Authentication | 90 days | 1 year | 7 years | employment/legal actions run long |
| Dispatch app transactions | 90 days | 1 year | 3 years | contract disputes; BIA-critical process |
| Firewall/IDS | 30 days | 1 year | — | high volume; investigation window is 1 year |
| DNS | 30 days | 6 months | — | threat-hunt window |
| Application debug | 14 days | — | — | troubleshooting only |

**Integrity and time.** All sources on the internal NTP pair; the SIEM alerts on >60s skew. Logs forward to the central collector over TLS; the collector is append-only for analysts (Tier 1 can read, only the platform team can administer — separation of duties from `e-secops-concepts`).

**The SOC workflow.** Two analysts cover business hours; nights and weekends go to a contracted MDR with a 15-minute SLA and a defined escalation path to Beacon's on-call. Tier 1 triages against five playbooks (phishing, impossible travel, malware alert, DLP, ransomware indicators); anything ambiguous escalates to the senior analyst (Tier 2), who also owns the tuning backlog. Every alert gets a quarterly tuning review: false-positive rate measured, thresholds adjusted or the rule retired with a written rationale. Coverage metric: percentage of taxonomy categories with verified collection — reviewed monthly, because collectors break silently.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the taxonomy, retention schedule, and SOC workflow above, authored and self-reviewed in-session on 2026-10-10 against SP 800-92's lifecycle. Transcript: `runs/e-logging-monitoring.log`.

1. **Inventory the sources.** For your fictional (or real) organization, list every log source by category: authentication, system, network security, application, physical. For each: where it lives now, whether it's centralized, its current retention. The "until the disk fills" entries are your first findings.
2. **Write the taxonomy.** Per category: required sources, verbosity, and the detection each source feeds. For every detection the program claims, name its source — unmapped detections become gaps with owners.
3. **Set the retention schedule.** Per category: hot/warm/cold tiers with periods and a written justification for each (legal, investigation window, or risk acceptance with owner and date). Then the disposal procedure and the litigation-hold suspension rule.
4. **Design integrity and time.** Name the time source, the skew threshold, and the alert. Describe the forwarding path and who can read vs. administer the collector — write the separation of duties explicitly.
5. **Design the watch floor.** Tiers, handoffs, escalation criteria, hours actually covered (name the night/weekend arrangement honestly). Five starter playbooks for Tier 1. The tuning loop: who owns each alert, how false-positive rate is measured, the quarterly review with retire-or-retune decisions.
6. **Define the coverage metrics.** Percentage of taxonomy with verified collection, alert tuning currency, mean time to detect and triage. Pick the review cadence and the owner who reads them — metrics nobody reads are decoration.

## 5. On your own

**Task:** For a system you control, check three things: the oldest entry in your authentication log (is retention what you think?), whether all your hosts agree on time within a minute, and whether any log you rely on lives only on the machine that generates it. Write the findings as a mini retention-and-integrity assessment.

**Success test:** You find at least one gap — a log that ages out faster than you assumed, a clock that's drifted, or a critical log with no central copy. If everything matches your assumptions, you didn't check; you recalled.

## 6. Where it goes wrong

- **"Until the disk fills."** The default retention policy of every unmanaged system — and the reason investigations die at day 31. Retention is a decision with a justification, not a side effect of disk size.
- **Logs nobody watches.** Collection without monitoring is archaeology with extra steps. If no human or tuned automation reads it, the budget spent collecting it bought nothing.
- **The unmapped detection.** The program claims to detect lateral movement; no log source records the authentication events that would show it. Map every detection to its source or stop claiming it.
- **Alert fatigue as a tuning failure.** A thousand daily alerts, all ignored — the SOC didn't fail at triage, it failed at tuning. Every alert needs an owner and a measured false-positive rate.
- **Clock skew.** Correlating events across sources with disagreeing clocks produces timelines that are fiction. Time sync is infrastructure, not a nice-to-have.
- **Local-only logs.** The compromised server's logs, editable by the compromise. Centralize over protected channels, restrict write access, and treat local logs as a convenience copy.
- **Retention without disposal.** Keeping everything forever "just in case" — until discovery, privacy law, or storage cost makes "everything" a liability. Disposal is part of the schedule, with litigation hold as the suspension.
- **Coverage decay.** Collectors break, sources get decommissioned, new systems ship without forwarding. The monthly coverage check exists because pipelines rot silently.

## 7. Read the source

Primary documents first:

- **NIST SP 800-92, Guide to Computer Security Log Management** (csrc.nist.gov, September 2006) — *read* the log-management lifecycle (generation, transmission, storage, analysis, disposal) and the log-source categories; *note* its age honestly — pre-SIEM-consolidation, pre-cloud, but the lifecycle still describes every pipeline.
- **NIST SP 800-53 Rev. 5, Audit and Accountability (AU) family** — the control catalog this program is audited against; AU-2 (auditable events) is the taxonomy in control language, AU-9/AU-10 the integrity requirements. Find it via the SP 800-53 publication page (csrc.nist.gov).

Then at most three free resources:

1. **CIS Critical Security Controls v8.1** (cisecurity.org) — free; the prioritized safeguard set — its audit-log-management guidance is the "what to do first" companion to 800-92's "how it all fits."
2. **NIST SP 800-94, Guide to Intrusion Detection and Prevention Systems** (csrc.nist.gov, February 2007) — free; the network-monitoring half of the program — what IDS/IPS sensors contribute to the collection.

## 8. Check yourself

1. A SOC claims to detect credential-stuffing against its VPN. The VPN logs only failures, retained 14 days, stored locally on the VPN appliance. Name the three distinct program failures (taxonomy, retention, integrity) and the fix for each.
2. Explain why "collect everything, figure it out later" fails as a logging strategy — what are the three constraints that force the taxonomy decision, and which one bites first?
3. Two servers disagree by eight minutes. An analyst builds an incident timeline from both. Explain, concretely, what goes wrong — and what the policy should have specified to prevent it.
4. Distinguish a test of activity from a test of effectiveness for monitoring: which of the coverage metrics validates that the SOC actually detects, and why is "alerts per day" the wrong metric?
5. Predict the state of a SIEM two years after installation with no tuning process: what do the alert queue, the rule set, and the analysts' behavior look like?

## 9. Prove it

**Artifact:** your event taxonomy (categories, sources, detection mapping with gaps), retention schedule (tiers, periods, justifications, disposal procedure, litigation-hold rule), integrity-and-time design, and SOC workflow (tiers, handoffs, coverage hours, tuning loop, metrics) — for the Beacon worked case in your own words, or better, for an environment you actually run.

**Honest claim:** "I can design the logging and monitoring program — decide what's worth recording, how long it lives, how it's protected, and how the watch floor turns it into detections that stay tuned."
**Can't claim yet:** "I can engineer detections at scale" — writing and tuning production detection logic across a large estate (the `c-sigma-detection` and `d-dfir-deep` hunting territory) is its own practice; this lesson taught the program that makes that work possible.

## 10. Leads to

- `c-log-sources` — the analyst's view of what this program produces; reread it as the consumer of your taxonomy.
- `c-soc-triage` — the Tier 1 workflow your staffing and playbooks serve.
- `e-investigation-forensics` — your retention schedule is the evidence base; the litigation hold freezes it.
- `e-secops-concepts` — separation of duties applied to log administration.
- Map refs: **CISSP 7.2** (this lesson); feeds **CISSP 7.1** (investigations) and **7.7** (detective measures).

---

*Worked case authored and self-reviewed 2026-10-10; all scenario data fictional. Sources fetched in-session — see `runs/e-logging-monitoring.log`.*
