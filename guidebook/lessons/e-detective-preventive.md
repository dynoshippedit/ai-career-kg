---
lesson_id: e-detective-preventive
slug: detective-preventive
stage: E
level: 3
prerequisites: [c-soc-triage, c-sigma-detection]
roles: []
map_refs: ["CISSP 7.7"]
test_date: 2026-10-10
description: "How to choose, place, and tune detective and preventive controls in operation — IDS/IPS, honeypots, DLP, and allow-listing. A free lesson in the security guidebook, serving CISSP objective 7.7."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Detective and preventive measures in operation: choosing, placing, and tuning controls


**Map ref:** serves **CISSP objective 7.7** — operating detective and preventive measures: what each control type does, where it goes, and how it stays effective.

---

## 1. Where this shows up

Controls are easy to buy and hard to operate. The difference between a control that protects and one that decorates is a series of unglamorous decisions: which type fits the risk, where it sits in the architecture, who tunes it, and what happens when it fires. This lesson is about those decisions — detective vs. preventive vs. deterrent vs. corrective controls *in operation*: IDS/IPS placement and tuning, honeypots that buy early warning, DLP that watches the exits, allow-listing that shrinks what can run. It shows up in the IPS that blocked the CFO's legitimate traffic for a week, in the honeypot nobody monitored, in the DLP rule with four thousand daily false positives — and in the SOC where every alert has an owner and a tuning history. SOC engineers, security architects, and detection engineers live here.

## 2. Before you start

- You know the triage end of the pipeline from `c-soc-triage` — every control here feeds that workflow.
- You have written detection logic in `c-sigma-detection` — this lesson decides where that logic runs and who keeps it honest.
- No tools. The work products are documents: a control-selection rationale, a placement map, and a tuning procedure. Primary spine: **NIST SP 800-94** (Guide to Intrusion Detection and Prevention Systems, February 2007).

## 3. How it works

Controls are classified by what they *do* when they meet an event — and the operations question is always which type fits, where, and at what cost.

**The control types, operationally.** **Preventive** controls block the event: firewalls, IPS in inline mode, allow-listing, authentication. **Detective** controls record and alert: IDS in passive mode, log monitoring, honeypots, file-integrity checks. **Deterrent** controls discourage: warning banners, visible cameras — they work on humans, not on malware. **Corrective** controls repair: backups restored, systems reimaged, failover. **Compensating** controls stand in where the ideal control can't go (the `e-secops-concepts` SoD matrix used these). The expert's first decision is type selection: preventive where the cost of the event exceeds the cost of the occasional false block (malware execution on a server), detective where blocking would break the business or the confidence is low (anomaly alerts on user behavior). The classic error is preventive-by-default everywhere — an IPS blocking inline on a poorly tuned signature set doesn't prevent attacks, it prevents business.

**IDS/IPS: placement is the decision, tuning is the job.** SP 800-94 — February 2007, and honest about its age: it covers network-based, host-based, wireless, and NBA (network behavior analysis) systems, written before the XDR/NDR rebranding — teaches that effectiveness is mostly placement and tuning, not product. **Placement:** network sensors where traffic *must* pass to reach what matters — at internet ingress/egress, between trust zones (the `e-secops-concepts` segmentation), watching the paths to the crown jewels, not "everywhere" (everywhere is unaffordable and unmonitorable). Host-based sensors where network visibility dies: encrypted traffic the network sensor can't read, the laptop off the corporate network. **Inline vs. passive** is the preventive/detective choice made physical: inline (IPS) can block but a failure or false positive breaks traffic; passive (IDS) can't break anything but also can't stop anything — the decision is per segment, based on what a false block costs there. **Tuning** is the ongoing job: baseline what normal looks like, suppress the known-benign, escalate the known-malicious, and review on a cadence — because networks change and untuned signatures are how you get the CFO's traffic blocked for a week. SP 800-94's management components (the console, the database, the sensors) map directly to operations staffing: someone owns the console, someone owns the rule set, someone answers the alerts.

**Honeypots: cheap early warning, if anyone watches.** A honeypot is a system with no production purpose — so *any* interaction with it is suspicious by definition. That property is what makes them valuable: no tuning for false positives, because legitimate users never touch them. The Honeynet Project (honeynet.org, the long-running open research organization) maintains the tools and the knowledge base — including ICS/SCADA honeypots for industrial environments. The operations decisions: **fidelity** (low-interaction emulations are cheap and safe; high-interaction real systems yield richer attacker behavior but must be contained so they can't become launch pads), **placement** (inside the network to catch lateral movement, in the DMZ to catch external probing — never where they can be mistaken for production), and **monitoring** (a honeypot nobody watches is a liability, not a control — its alerts go to the SOC with high priority because the false-positive rate is near zero). The failure mode is always the same: deployed with enthusiasm, abandoned within months.

**DLP and allow-listing: watching the exits and shrinking the executable.** **Data loss prevention** monitors data in motion (and at rest, and in use) against policies — the `e-media-protection` USB ban needs DLP to mean anything. Placed at the natural chokepoints: email egress, web upload, endpoint agents on machines that handle the crown-jewel data. The tuning burden is the highest of any control here — DLP policies generate false positives by design (people do legitimate things that look like exfiltration), so deployment starts in monitor-only mode, tunes, and only then blocks. **Allow-listing** (application control) inverts the endpoint model: instead of blocking known-bad, only known-good may execute. It's the strongest preventive control on servers with stable software sets — and the most operationally demanding, because every legitimate change needs the list updated (which is why it pairs with `e-change-management`: the change process feeds the allow list).

**The selection discipline.** For each risk, the worked case below asks four questions: which type (prevent/detect/deter/correct)? where does it sit (which chokepoint, which segment)? who tunes it and on what cadence? what does it cost when it's wrong (false block vs. missed event)? A control with no tuning owner is a future incident — write the owner into the selection document, not into someone's memory.

### Worked example: Meridian Analytics — control selection for the SOC

**The company (fictional, continued from `e-iam`).** Meridian, 180 people, one IdP, cloud account, production database, CI/CD, VPN. The SOC is two analysts plus the contracted MDR nights/weekends (from `e-logging-monitoring`'s Beacon design — Meridian adopts the same model). The crown jewels: the customer database and the CI/CD pipeline that deploys to production.

**The selection (excerpt, fictional).**

| Risk | Control | Type | Placement | Tuning owner / cadence |
|---|---|---|---|---|
| External intrusion | IDS/IPS | passive at ingress (detect), inline at egress (prevent C2) | internet boundary, both sites | detection engineer, monthly rule review |
| Lateral movement | honeypot (low-interaction) | detective | inside each trust zone, non-production addresses | SOC analyst, alerts high-priority (near-zero FP) |
| Data exfiltration | DLP | detect-then-block | email egress, web upload, endpoints with customer data | DLP admin, monitor-only 30 days before blocking |
| Malware on servers | allow-listing | preventive | production servers (stable software set) | change process feeds the list; review per change |
| Compromised credentials | IdP anomaly detection | detective | identity layer | SOC, weekly FP review |

**Placement decisions with reasons.** The IPS goes inline only at egress (blocking command-and-control is worth the false-block risk; blocking inbound on a poorly tuned set once took down the customer portal — recorded as the lesson that set the policy). The honeypot sits inside the production zone at addresses that were never assigned — any touch is lateral movement or scanning, no legitimate explanation exists. DLP starts monitor-only: the first month's findings tune out the finance team's legitimate bulk transfers before any block goes live.

**The tuning procedure.** Every control has an owner, a review cadence, and a measured false-positive rate. Quarterly, each owner answers: what fired, what was real, what changed in the environment, what retires. The honeypot's review is the shortest — near-zero false positives means its alerts stay high-priority, which is the whole point. The DLP review is the longest — and the one that prevents the four-thousand-false-positive death spiral.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the control selection, placement map, and tuning procedure above, authored and self-reviewed in-session on 2026-10-10 against SP 800-94's IDS/IPS guidance and the Honeynet Project's deployment knowledge. Transcript: `runs/e-detective-preventive.log`.

1. **List the risks.** For your fictional (or real) organization: the five risks that would hurt most (intrusion, lateral movement, exfiltration, malware, credential compromise — adapt to your estate).
2. **Select the type per risk.** Prevent, detect, deter, or correct — with the cost-of-being-wrong reasoning written down. Preventive where the event costs more than the false block; detective where confidence is low or blocking breaks the business.
3. **Place each control.** Name the chokepoint or segment and the reason. For IDS/IPS: inline or passive, per segment, with the false-block cost stated. For honeypots: fidelity, placement, containment.
4. **Name the tuning owner and cadence.** Every control gets an owner and a review rhythm. No owner, no control — write that rule into the document.
5. **Stage the DLP (or any high-FP control).** Monitor-only first, with a defined tuning period and promotion criteria before blocking. Write the promotion decision as a change (the `e-change-management` link).
6. **Define the quarterly review.** What each owner reports (fired, real, environmental changes, retirements). The review that retires a control is as valuable as the one that tunes it.

## 5. On your own

**Task:** Pick one preventive and one detective control on a system you run (your firewall rules and your auth logs count). For each: what type is it really, where does it sit, who tunes it (you — on what cadence?), and what's the measured false-positive rate? If you can't state the FP rate, that's the finding.

**Success test:** You produce the tuning history — or its absence — for both controls, and you name one control that's been firing unactioned. Unactioned firing is the control telling you it's misconfigured; the success is hearing it.

## 6. Where it goes wrong

- **Preventive by default.** The IPS blocking inline on untuned signatures — preventing business, not attacks. Type selection is a decision with a cost-of-being-wrong analysis, not a posture.
- **Placement by hope.** Sensors where traffic doesn't flow to anything valuable; honeypots in the DMZ nobody routes alerts from. Placement follows the crown jewels and the chokepoints.
- **The unmonitored honeypot.** Deployed with enthusiasm, abandoned in months — now a liability that could host attacker activity. Monitoring is part of the deployment, not a later phase.
- **High-interaction without containment.** A real system as a honeypot, reachable and exploitable, with no isolation. Fidelity without containment is arming the attacker.
- **DLP straight to block.** Policies enabled in blocking mode on day one — four thousand false positives, the business revolts, DLP gets disabled entirely. Monitor, tune, then block.
- **Allow-listing without a change feed.** The list goes stale with the first emergency patch; then it's bypassed "temporarily" forever. The change process feeds the list or the list dies.
- **Tuning as nobody's job.** The console has an owner, the rule set doesn't. Every control's tuning owner is named in the selection document.
- **Controls that share a fate.** The IDS, the firewall, and the SIEM all on the same unpatched management host. Layer independence (from `e-secops-concepts`) applies to the controls themselves.

## 7. Read the source

Primary documents first:

- **NIST SP 800-94, Guide to Intrusion Detection and Prevention Systems** (csrc.nist.gov, February 2007) — *read* the IDS/IPS types (network, host, wireless, NBA) and the management considerations; *note* its age honestly — pre-XDR/NDR, but placement and tuning are still the job.
- **NIST SP 800-53 Rev. 5, System and Information Integrity (SI) family** — SI-4 (information system monitoring) is the control-language home of this lesson. Find it via the SP 800-53 publication page (csrc.nist.gov).

Then at most three free resources:

1. **The Honeynet Project** (honeynet.org) — free; the open research organization's tools and deployment knowledge — start here before placing any honeypot, and note their ICS/SCADA work if you have industrial systems.

## 8. Check yourself

1. An IPS is deployed inline at the internet ingress with the vendor's default signature set. Within a week it blocks legitimate customer traffic twice and misses an actual intrusion. Using the type-selection and tuning discipline, explain the three decisions that were skipped and the order you'd fix them.
2. Explain why a honeypot's alerts can be high-priority by default while a DLP's cannot — what property of the honeypot makes its false-positive rate near zero, and what breaks that property?
3. A server's allow-list hasn't been updated in six months; admins routinely bypass it "temporarily" for patches. Name the two process failures (one in change management, one in tuning ownership) and the single integration that fixes both.
4. Distinguish inline from passive deployment as a risk decision: what does each choice cost when it's wrong, and why is the decision per segment rather than per product?
5. Predict the alert queue of a SOC two years after deploying five new detective controls with no tuning owners: which control's alerts get ignored first, and which failure mode from §6 does the honeypot exhibit?

## 9. Prove it

**Artifact:** your control-selection rationale (risk → type → placement → tuning owner/cadence, with cost-of-being-wrong per control), the placement map, and the tuning procedure (review cadence, FP measurement, retire criteria) — for the Meridian worked case in your own words, or better, for an estate you actually defend.

**Honest claim:** "I can choose the right control type for a risk, put it where it matters, and keep it effective — selection, placement, and the tuning discipline that prevents controls from decaying into decoration."
**Can't claim yet:** "I can engineer detections" — writing the detection logic itself (Sigma rules, behavioral analytics) is `c-sigma-detection` and `d-dfir-deep` territory; this lesson taught the operational decisions around the controls, not the logic inside them.

## 10. Leads to

- `c-sigma-detection` — the detection logic this lesson puts into operation and keeps tuned.
- `c-soc-triage` — the workflow these controls feed; tuning quality is triage quality.
- `e-secops-concepts` — layer independence and the principles behind type selection.
- `e-change-management` — the change feed that keeps allow-listing alive.
- Map refs: **CISSP 7.7** (this lesson); feeds **CISSP 7.2** (monitoring) and **7.4** (operations concepts).

---

*Worked case authored and self-reviewed 2026-10-10; all scenario data fictional. Sources fetched in-session — see `runs/e-detective-preventive.log`.*
