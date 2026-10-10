---
lesson_id: e-physical-security
slug: physical-security
stage: E
level: 3
prerequisites: []
roles: []
map_refs: ["CISSP 7.14"]
test_date: 2026-10-10
description: "How to run physical security day to day — guards and post orders, the badge lifecycle, mantraps and doors, CCTV operation, and environmental controls. A free lesson in the security guidebook, serving CISSP objective 7.14."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Physical security in operation: running the building's defenses day to day


**Map ref:** serves **CISSP objective 7.14** — implementing and operating physical security: the day-to-day running of the controls.

---

## 1. Where this shows up

The badge reader, the guard, the camera, the mantrap — none of them work without the operation behind them: the guard's post orders, the badge lifecycle, the camera someone actually watches, the visitor log someone actually checks. Physical security implementation is the day-to-day running of those controls: guards and patrols, badging, mantraps and tailgating discipline, CCTV placement and monitoring, and the environmental controls (power, fire, water, climate) that keep the equipment — and the people — alive. It shows up in the tailgating incident the camera recorded and nobody watched, in the terminated employee whose badge worked for a month, and in the server room that flooded because the water sensor's alert went to an unmonitored mailbox. Facilities leads, SOC managers, and GRC analysts live here. Note the boundary with the Domain 3 design lessons: those design the facility — perimeter, zones, control selection. This lesson operates it — the people, the rosters, the procedures, and the daily discipline that make the designed controls actually work.

## 2. Before you start

- You understand the identity lifecycle from `e-iam` — the badge lifecycle in this lesson follows the same joiner-mover-leaver logic.
- You know the monitoring-program thinking from `e-logging-monitoring` — badge and camera events are log sources with the same integrity and review needs.
- No tools. The work products are documents: guard post orders, a badge-lifecycle procedure, a CCTV monitoring plan, and an environmental-controls checklist. Primary spine: **NIST SP 800-53 Rev. 5, Physical and Environmental Protection (PE) family**.

## 3. How it works

Designed controls decay without operation. Five operating areas.

**People: guards, and what they're actually for.** Guards deter, observe, and respond — in that order. The operation is the **post orders**: the written instructions per post (what to check, what to challenge, when to escalate, what never to do alone). Patrols are randomized within bounds — predictable patrols are a schedule the adversary can read. The common failure is the guard as furniture: posted, unbriefed, untested. The operation tests: the occasional tailgating attempt by a friendly auditor, the after-hours challenge, the alarm-response drill. A guard who has never been tested is a control with no verification — the `e-detective-preventive` discipline applied to humans.

**Badges: the identity lifecycle, physical edition.** Every badge is an identity, and the `e-iam` lifecycle applies exactly: **joiner** (badge issued with the minimum zones for the role — the need-to-know principle from `e-secops-concepts`, physical edition), **mover** (zone access changes with the role — the engineer who moves to sales loses the lab), **leaver** (badge disabled on departure, same day — the terminated employee whose badge worked for a month is the physical version of the orphaned account). Visitor badges: logged, escorted in sensitive zones, time-bounded, collected on exit. The badge *system* needs the same administration as any identity store: who can grant zones, the quarterly review of who holds what, the lost-badge procedure (disable first, investigate second). Tailgating — following an authorized person through — is the perennial defeat of badging; the operation's answers are mantraps or turnstiles at the sensitive boundary, a culture where challenging is expected (backed by management, or nobody challenges the stranger in the suit), and the camera covering the door.

**Entry controls: mantraps, and the doors between zones.** A **mantrap** (two interlocking doors — the second opens only when the first closes) enforces one-person-at-a-time entry to the most sensitive areas: the data center, the cash room, the lab. In operation: the mantrap's procedure covers the duress case (what the guard does when someone is forced through), the failure case (power loss — does it fail open for life safety or fail closed for security? decided in advance, per fire code and risk), and the piggybacking case. Between zones, doors are the control: locked by default, alarmed when propped, with the alarm going somewhere someone responds — a propped-door alert to an unmonitored mailbox is the physical version of the unmonitored log.

**CCTV: placement, monitoring, retention.** Cameras **deter** (visible, signed) and **detect** (recorded, reviewed) — but only as operated. **Placement** covers the entries, the mantrap, the sensitive zones, and the paths between them — not "everywhere" (unaffordable to monitor) but the chokepoints, overlapping so one camera's blind spot is another's view. **Monitoring** is the decision: live watch of the critical feeds during risk hours, recorded-everything with defined review (post-incident pull, random sampling — the tuning loop from `e-logging-monitoring`, physical edition). **Retention** follows the same schedule logic as logs: long enough for incident discovery (the fraud found in month three needs month-one footage), with the integrity protection (write-once or access-controlled storage — footage the suspect can delete is the attacker's alibi, same as logs). The failure is always the same shape: cameras installed, nobody watches, footage overwritten in 72 hours, the incident discovered on day five.

**Environmental: the building as a life-support system.** The PE family's unglamorous half: **power** (UPS for ride-through, generator for extended outage, tested under load — the untested generator is the physical version of the untested backup), **fire** (detection, suppression matched to the space — clean-agent for the data center, not sprinklers over the racks — drills, the marshaled assembly point), **water** (sensors under the raised floor and near plumbing, with alerts to a monitored destination), **climate** (temperature and humidity monitoring with thresholds and alerting — the slow killer of equipment). Each has the same operating pattern: the control, the monitoring, the alert destination that someone watches, the test cadence. The environmental checklist is reviewed with the seasons and after every incident — the flood teaches what the checklist missed.

### Worked example: Kestrel Components — the physical-security operations review

**The company (fictional, continued from `e-media-protection`).** Kestrel Components, 90 staff, precision manufacturing: HQ with engineering, a lab with prototype hardware, and the server room holding the design files (the crown jewels from the media-protection lesson).

**The review (excerpt, fictional — findings with decisions).**

1. **Guards.** One guard, nights and weekends, no post orders — "walk around." *Decision:* post orders written (perimeter check, lab-door verification, alarm response, the never-alone rule for the lab); patrol times randomized; quarterly tailgating test by a friendly auditor. Owner named, first test dated.
2. **Badges.** Joiner/mover/leaver exists on paper; leaver deactivation averages 11 days (the month-long badge from §1, measured). *Decision:* deactivation same-day, tied to the HR termination checklist (the `e-iam` leaver SLA, physical edition); quarterly zone-access review by managers; visitor log moved from paper to the badge system with escort rules for the lab.
3. **Mantrap and doors.** The lab has a mantrap — installed, never procedurally defined. *Decision:* procedure written (duress, power-failure behavior — fail-secure on the lab side with manual life-safety override, decided with the fire marshal — piggybacking response); the server-room door gets a prop alarm routed to the guard's radio, not to email.
4. **CCTV.** Twelve cameras, recorded locally, 72-hour overwrite, nobody reviews. *Decision:* placement rationalized to entries, mantrap, lab, server room, and the paths between (two cameras repositioned for overlap); retention extended to 90 days on access-controlled storage; weekly 15-minute random-sample review by the guard supervisor; post-incident pull procedure written.
5. **Environmental.** Server room: UPS present, generator never tested under load; no water sensor; temperature alerting to an unmonitored distribution list. *Decision:* generator load test quarterly (owner, date); water sensor installed under the cooling unit with alerting to the monitored SOC channel; temperature alerts re-routed to the on-call phone. Fire: clean-agent suppression verified in date; drill scheduled.

**The operations calendar (fictional).** Daily: guard patrols, badge exception review. Weekly: CCTV sample review. Monthly: visitor-log audit, environmental threshold check. Quarterly: zone-access review, generator load test, tailgating test. Annually: fire drill, full procedure review. Every item with an owner — the calendar is the operation made visible.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the operations review, findings with decisions, and the operations calendar above, authored and self-reviewed in-session on 2026-10-10 against the SP 800-53 PE family's control areas. Transcript: `runs/e-physical-security.log`.

1. **Map the zones.** For your fictional (or real) facility: public, controlled, sensitive — draw the boundaries and name what lives in each. The zone you can't draw is the zone with no controls.
2. **Review the people.** Guards: post orders exist? Patrols randomized? Tested? Write the findings. If there's no guard, write who performs the function (reception, the on-call) — the function doesn't vanish because the role does.
3. **Audit the badge lifecycle.** Sample ten badges: joiner (minimum zones?), mover (role changed — zones changed?), leaver (deactivation time?). Visitor procedure: logged, escorted, time-bounded, collected. Every gap gets a decision with an owner and a date.
4. **Walk the doors.** Mantrap procedure (duress, power failure, piggybacking) — written or not? Prop alarms — where do they go, and does anyone respond? Fail-open vs. fail-closed decided per door, in advance.
5. **Review the cameras.** Placement against the chokepoints, monitoring (live vs. recorded, who reviews, how often), retention (long enough for discovery, integrity-protected). The footage-overwritten-before-discovery finding is the classic — check your retention against a realistic discovery window.
6. **Check the environment.** Power (UPS, generator — tested under load?), fire (suppression matched to the space, drill dated?), water (sensors, alert destination monitored?), climate (thresholds, alerting). Build the operations calendar with owners.

## 5. On your own

**Task:** Walk your own building (office, home office, makerspace) as the reviewer: the entries, the locks, the cameras (or their absence), the fire and power situation. Write the findings with decisions — including the ones that are "accept the risk," with the owner (you) and the date named.

**Success test:** Your review finds the tailgating-equivalent (the door everyone props, the code everyone knows) and the unmonitored alert (the sensor that pages nobody). If your building is perfect, you reviewed the design, not the operation — go at 2 a.m. (figuratively) and review what's actually running.

## 6. Where it goes wrong

- **The guard as furniture.** Posted, unbriefed, untested. Post orders, randomized patrols, and friendly-auditor tests are the operation.
- **The month-long badge.** Leaver deactivation measured in weeks. Same-day deactivation, tied to the HR checklist — the physical orphaned account.
- **Tailgating culture.** Nobody challenges the stranger. The mantrap enforces at the sensitive boundary; management backing enforces everywhere else.
- **The unmonitored camera.** Installed, recording, overwritten in 72 hours, never reviewed. Placement, monitoring, retention — all three, or it's decoration.
- **Prop alarms to nowhere.** The alert destination nobody watches. Every alarm names its responder — the physical version of the unmonitored log.
- **Fail-open by surprise.** Power loss, and the mantrap opens — decided by physics, not by policy. Fail-open vs. fail-closed is decided per door in advance, with life safety and the fire marshal in the decision.
- **The untested generator.** Present, never run under load. Environmental controls are tested on cadence like everything else — the flood and the outage teach what the checklist missed.
- **Design without operation.** The Domain 3 lesson's perfect zones, with no rosters, no reviews, no calendar. Design is the starting line; the operations calendar is the race.

## 7. Read the source

Primary documents first:

- **NIST SP 800-53 Rev. 5, Physical and Environmental Protection (PE) family** (csrc.nist.gov) — *read* as the control catalog this operation is audited against: PE-2/PE-3 (physical access authorizations and enforcement — the badge lifecycle), PE-6 (monitoring physical access), PE-9/PE-10/PE-11 (power, emergency shutoff, emergency power), PE-13 (fire protection).
- Note: **ASIS International** publishes the physical-security profession's standards and guidelines — they are paid publications, so this lesson teaches the function from free sources (one line, per the brief's rule).

Then at most three free resources:

1. **CISA: Physical Security** (cisa.gov, topic page) — free; the federal operational view — assessments, planning considerations, and protective-measures guidance for facilities.

## 8. Check yourself

1. A terminated employee's badge works for 23 days; during that time the ex-employee enters the lab twice. Using the badge-lifecycle model, name the two failures (one in the leaver process, one in monitoring) and the `e-iam` concept each mirrors.
2. Explain why a mantrap's power-failure behavior must be decided in advance — who has to be in the decision, and what goes wrong when physics decides instead of policy?
3. A facility has 40 cameras, 72-hour retention, and no review procedure. An intrusion is discovered on day six. Name the three operations failures (placement is not one of them) and the realistic discovery window the retention should have covered.
4. Distinguish the Domain 3 design view from this lesson's operations view using the mantrap: what does each view produce, and which one fails when the mantrap has no duress procedure?
5. Predict the guard operation one year after post orders are written but never tested: what do the patrols, the tailgating rate, and the alarm responses look like?

## 9. Prove it

**Artifact:** your physical-security operations review (zones mapped, findings with decisions/owners/dates across guards, badges, entry controls, CCTV, environmental), plus the operations calendar — for the Kestrel worked case in your own words, or better, for a facility you actually use, walked as the reviewer.

**Honest claim:** "I can run the physical-security operation — staff and test the human controls, administer the badge lifecycle, place and monitor cameras, and keep the environmental controls tested — and I can review a facility and drive every finding to a decision."
**Can't claim yet:** "I can design a facility's physical security" — the Domain 3 design work (perimeter engineering, zone architecture, control selection against threats) is its own discipline; this lesson taught the daily operation of whatever was designed.

## 10. Leads to

- `e-iam` — the badge lifecycle is the identity lifecycle, physical edition; leaver SLAs apply to both.
- `e-logging-monitoring` — badge and camera events as log sources: integrity, retention, review.
- `e-detective-preventive` — the guard as a detective control: post orders as tuning, friendly-auditor tests as verification.
- `e-personnel-safety` — the same building, the people's safety view: duress, workplace violence, evacuation.
- Map refs: **CISSP 7.14** (this lesson); feeds **CISSP 3.8/3.9** (the design companion) and **7.15** (personnel safety).

---

*Worked case authored and self-reviewed 2026-10-10; all scenario data fictional. Sources fetched in-session — see `runs/e-physical-security.log`. Factual note: the FEMA site-security guidance page was unreachable in-session (HTTP 403 via two routes) and is logged as an unverified lead, not cited.*
