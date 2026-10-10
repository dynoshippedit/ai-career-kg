---
lesson_id: e-facility-controls
slug: facility-controls
stage: E
level: 3
prerequisites: [e-facility-design]
roles: []
map_refs: ["CISSP 3.9"]
test_date: 2026-10-10
description: "Complete a five-family facility controls checklist — perimeter, access, environmental, power, fire — with findings, owners, and dates. A free lesson in the security guidebook, serving CISSP objective 3.9."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Site and facility controls: the checklist that holds


**Map ref:** serves **CISSP objective 3.9** — site and facility security controls: perimeter, access, environmental, power, and fire.

---

## 1. Where this shows up

Design says what the facility should do; controls are what it actually does at 2 a.m. on a Sunday. The fence, the badge reader, the UPS, the sprinkler head, the temperature sensor in the data closet — each is a control with a failure mode, a maintenance schedule, and a test procedure, and the difference between a facility that is secure and a facility that was *designed* secure is whether anyone checks. This lesson is the checklist discipline: the five control families walked in order, each control assessed as implemented, partial, or missing, with findings written the way an auditor — or the next incident — will read them. It shows up in the annual physical-security assessment, in the data-center audit where the assessor asks to see the UPS test logs, in the fire marshal's visit, and in the CISSP as the objective that turns the design principles of 3.8 into verifiable reality.

## 2. Before you start

- You have the design review (`e-facility-design`) — controls implement its findings; the checklist verifies the implementation.
- You know the control-selection discipline (`e-control-selection`) — each control here traces to a requirement, even if the requirement is "the fire code."
- No tools. The work product is a completed controls checklist: five families, status per control, findings with recommendations and owners.

## 3. How it works

**Perimeter controls.** The property line's job is to deter, delay, and detect — in that order. **Fencing and gates:** continuous (the `e-facility-design` rule — a perimeter is binary), with gates that fail secure (locked on power loss) and anti-tailgating measures where vehicles enter. **Vehicle barriers:** bollards, planters, or rated barriers at approaches where a vehicle is the threat — the standoff distance between the road and the building is a control with a measurement. **Lighting:** perimeter and parking illumination that supports natural surveillance — assessed at night, not on the plans, because lighting designs lie. **Signage:** territorial reinforcement with legal weight — "authorized personnel only" signs that make the trespasser's intent provable. **Intrusion detection:** fence sensors, gate alarms, camera coverage with *monitored* feeds — a camera nobody watches is a historian, not a control.

**Access controls.** Who gets in, to where, and what proves it. **Locks and keys:** the key inventory — every key accounted for, master keys minimized, rekeying on personnel changes. (The most common physical-security finding in existence: nobody knows how many keys exist.) **Electronic access control:** badge/card systems with zones matching the interior zoning from the design review — public, semi-private, private, restricted — each door's authorized population defined, not inherited. **Visitor management:** sign-in, escorts in restricted zones, badges that visibly differ from employee badges, logs retained. **Mantraps and turnstiles** where tailgating (following an authorized person through a secured door without badging in yourself) is the threat — a mantrap is a small room with two interlocking doors: the first must close before the second opens, so only one badged person passes at a time — the data closet's vestibule from the design review. **Fail states:** every electronic lock has a power-loss behavior — fail-secure (stays locked, for security areas) or fail-safe (unlocks, for life-safety egress) — and the choice per door is documented, not accidental. Fire code decides the egress doors; the security plan decides the rest, and the two must be reconciled in writing.

**Environmental controls.** The data closet's climate is a security control — heat kills servers as surely as attackers do. **Temperature and humidity:** monitored with alerting, not just HVAC with a thermostat nobody checks; the alert goes to someone who responds at 2 a.m. **Water:** leak detection under raised floors and near water sources; water sensors are cheap and flooding is forever. **Air quality:** dust filtration for equipment longevity; positive pressure in clean areas. The assessment question for each: monitored, alarmed, and responded — or merely installed.

**Power controls.** Power is the facility's most attacked utility that nobody attacks — it fails on its own often enough. **Utility feeds:** dual feeds from diverse paths where the design requires them; the single-feed facility has a single point of failure with a utility company's name on it. **UPS:** uninterruptible power supply sized for the load with tested runtime — the test logs are the control's evidence, and "we've never tested it" is a finding. **Generators:** fuel supply, automatic transfer switch, load testing under real load (not just a start test — generators that start but can't carry the load are decorative). **Power conditioning:** surge protection and line conditioning — dirty power degrades equipment slowly, which is why nobody notices until the failure cluster. The power chain is only as strong as its weakest transfer: utility → generator → UPS → distribution, each handoff tested.

**Fire controls.** Fire is the facility threat with its own code, its own inspector, and no patience for security theater. **Detection:** smoke and heat detectors zoned and monitored, with the panel's signals reaching someone who dispatches — detection without response is a noisemaker. **Suppression:** sprinklers (wet, dry, pre-action — pre-action for data areas, so a single sprinkler-head failure doesn't flood the servers), and **clean-agent systems** for spaces where water is as destructive as fire. **Fire classes and extinguishers** (per FEMA's guidance): Class A (ordinary combustibles — wood, paper, cloth), Class B (flammable liquids), Class C (energized electrical equipment), Class D (combustible metals), Class K (cooking oils) — extinguishers matched to the fire classes actually present, inspected and charged, with staff who know that water on a Class C fire is a second emergency. **Egress and compartmentation:** fire doors that actually close (the propped-open fire door is the physical-security equivalent of the disabled control), evacuation routes posted and drilled, muster points (the designated assembly area everyone goes to after evacuating — where the headcount happens) defined. The fire marshal's findings outrank the security plan's preferences — life safety is the constraint everything else optimizes within.

**The checklist method.** Walk the facility with the design review in hand. For each control: **status** (implemented / partial / missing), **evidence** (seen, tested, or documented — "the guard told me" is not evidence), **finding** if anything less than implemented, with recommendation and owner. Test what can be tested: pull the alarmed door (does the alarm sound and does anyone respond?), check the UPS logs, look at the extinguisher inspection tags. The checklist is dated — controls decay, and a checklist without a date is a historical document.

### Worked example: Harborline hub — completed controls checklist (excerpt)

**The facility (fictional).** The Harborline distribution hub from `e-facility-design`, now built and occupied. The design review's five findings were dispositioned: parking relocated to the south face (done), service road gated (done), data closet given a mantrap vestibule (done), parking-lot cameras installed and monitored (done), backup-media safe (done). This checklist verifies the controls.

**Perimeter:** fencing continuous with the new gate (implemented — walked); vehicle bollards at truck entrance (implemented); parking-lot lighting assessed at night — two fixtures out on the south lot (PARTIAL — finding F-01: work order to facilities, 7-day SLA); signage posted at all entrances (implemented); gate alarms report to the monitoring desk (implemented — tested: alarm raised, desk acknowledged in 90 seconds).

**Access:** key inventory — 34 keys issued, 31 accounted for; 3 unaccounted (PARTIAL — finding F-02: rekey the affected cores within 30 days, owner: facilities manager); badge system zones match the design's four zones (implemented); visitor log retained 90 days, escort policy posted (implemented); data-closet mantrap — tested: tailgating attempt alarmed and logged (implemented); fail states documented per door — the warehouse personnel doors fail safe (egress), the data closet fails secure (implemented, reconciled with fire code in writing).

**Environmental:** data-closet temperature/humidity monitored with alerting to the on-call phone (implemented — tested: alert fired on a simulated threshold breach); water-leak sensor under the closet's cooling unit (implemented); HVAC maintenance contract with quarterly service (implemented — last service dated within the quarter).

**Power:** dual utility feeds from diverse paths (implemented — confirmed with the utility); UPS sized for the closet load — test logs show monthly self-tests passing, but no full-load runtime test in 14 months (PARTIAL — finding F-03: full-load test scheduled, owner: facilities manager); generator with automatic transfer — last load test 8 months ago, fuel topped (PARTIAL — finding F-04: annual load test scheduled before storm season); surge protection on the closet distribution panel (implemented).

**Fire:** detection zoned and monitored, panel signals reach the monitoring desk (implemented); pre-action sprinkler in the data closet (implemented — protects against single-head failure flooding); extinguishers: ABC units in offices and warehouse, Class C-appropriate coverage in the electrical room and data closet (implemented — inspection tags current); one warehouse extinguisher blocked by pallet storage (PARTIAL — finding F-05: relocate, owner: warehouse supervisor, immediate); fire doors — all closers functional, none propped (implemented — walked); evacuation routes posted, last drill 5 months ago (implemented).

**Findings register:** F-01 (lighting, 7-day), F-02 (key inventory, 30-day rekey), F-03 (UPS runtime test), F-04 (generator load test), F-05 (extinguisher access, immediate). Five findings, five owners, five dates. The pattern the checklist reveals: installation is good, *testing and maintenance* is where the gaps live — the classic facility-controls story.

## 4. Walkthrough

**Worked-case lesson — no command line.** The Harborline checklist above, authored and self-reviewed in-session on 2026-10-10. Transcript: `runs/e-facility-controls.log`.

1. **Take the design review as input.** The checklist verifies the design's implementation — start from its findings register and confirm each disposition, then assess the five families fresh.
2. **Walk the perimeter.** Fence continuity, gates, barriers, lighting (at night if you can), signage, intrusion detection. Test the gate alarm; time the response.
3. **Audit access.** Count the keys — the inventory is the finding generator. Verify zones match the design, test the mantrap/vestibule, document every door's fail state and its fire-code reconciliation.
4. **Check environmental and power.** Monitoring with alerting (test the alert), UPS and generator test logs (read them — dates matter), surge protection. "Installed" without test evidence is partial.
5. **Walk fire.** Extinguisher classes matched to the spaces, inspection tags current, access unblocked, fire doors closing, detection monitored. The fire marshal's last report is input — reconcile any open items.
6. **Write the findings register.** Each finding: ID, observation, control family, recommendation, owner, date. Date the checklist — it expires.

## 5. On your own

**Task:** Run the five-family checklist on a facility you can access — your office, a building you know. Write the findings register.

**Success test:** You produce at least three findings, and at least one is a maintenance/testing gap rather than a missing gadget (the UPS never tested, the extinguisher tag expired, the key nobody can account for). Each finding has an owner and a date — even if the owner is "whoever runs this building" and the date is "ask them."

## 6. Where it goes wrong

- **Installation without verification.** The controls were bought, installed, and never tested — the alarm that doesn't alarm, the UPS that never ran on battery, the camera pointed at a wall. The checklist tests; the purchase order doesn't.
- **The key inventory nobody keeps.** Keys multiply with every contractor, every rekey skipped, every departure unprocessed. The key audit is the cheapest assessment in physical security and the most skipped.
- **Fail states by accident.** Electronic locks whose power-loss behavior was never specified — discovered during the first outage, when the "secure" area stood open. Every door's fail state is a design decision, documented.
- **Fire doors propped open.** Convenience defeating compartmentation, daily, everywhere. The propped fire door is the physical twin of the disabled control — and the fire doesn't care about your workflow.
- **Extinguisher mismatch.** ABC units everywhere including the electrical room is fine; water-only coverage near energized equipment is a second emergency waiting. Match the class to the space.
- **Monitoring without response.** Alarms that report to an unstaffed desk, temperature alerts to an unmonitored inbox. Detection is half a control; the response half needs a name and a phone number.
- **The checklist as a one-time event.** Controls decay — batteries die, keys multiply, storage migrates in front of extinguishers. The checklist has a date because the facility has entropy.

## 7. Read the source

Primary documents first:

- **CISA: Physical Security** (cisa.gov) — *read* the protective-measures sections for the control families; the operational catalog this lesson's checklist implements.
- **FEMA: How to Use a Portable Fire Extinguisher** (fema.gov) — *read* the fire classes (A/B/C/D/K) and the before-you-fight checks; the free authority for the fire section.

Then at most three free resources:

1. **NIST SP 800-53 Rev. 5, PE family** (csrc.nist.gov) — free; the physical/environmental controls in catalog form — trace each checklist row to its control.
2. **FEMA: Risk Management** (fema.gov) — free; the hazard framing behind the environmental controls — why water sensors and flood history belong in a security checklist.
3. **LISC: CPTED 2-pager** (lisc.org) — free; reread after this lesson — the design strategies these controls enforce.

## 8. Check yourself

1. A data closet's electronic lock fails open on power loss. The facilities team calls this "fail-safe" and therefore correct. Explain the terminology error, who actually decides the correct fail state for this door, and what the reconciliation looks like.
2. A key audit finds 34 keys issued and 31 accounted for. Explain why the correct response is rekeying (not "find the keys"), what the 30-day window risks, and what process prevents recurrence.
3. A UPS has monthly self-tests passing but no full-load runtime test in 14 months. Explain what the self-test proves, what it doesn't, and what the full-load test would reveal — then name the incident that reveals it instead.
4. A warehouse stores pallets in front of a fire extinguisher. Analyze this in two control families (fire and maintenance/territoriality) and explain why the immediate fix is relocation, not a memo.
5. Predict the assessment outcome when a facility's last controls checklist is three years old: which three controls have most likely decayed, and what evidence the assessor asks for first.

## 9. Prove it

**Artifact:** your completed five-family checklist — status and evidence per control, the findings register (ID, observation, family, recommendation, owner, date) — for the Harborline hub in your own words, or for a facility you can walk.

**Honest claim:** "I can assess a facility's perimeter, access, environmental, power, and fire controls, test what can be tested, and write findings with owners and dates."
**Can't claim yet:** "I can commission the systems" — installing and commissioning access-control hardware, fire suppression, and generator plants is licensed trade work; this lesson taught assessment, not installation.

## 10. Leads to

- `e-facility-design` — the design review this checklist verifies; the two lessons are a pair — design then verify, every cycle.
- `e-bcp-drp` — power and fire findings become recovery-plan inputs: the generator that never load-tested is a DR assumption waiting to fail.
- `e-platform-security` — the data closet's environmental and power controls are the physical half of the platform survey.
- Map refs: **CISSP 3.9** (this lesson); feeds **CISSP 7.14** (physical security implementation) and **7.11** (disaster recovery).
