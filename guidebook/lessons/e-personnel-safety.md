# Personnel safety: protecting the people, not just the accounts

**ID:** `e-personnel-safety` · **Stage:** E (Expert) · **Level:** 3 (produce a travel-security briefing and a workplace-safety procedure set) · **Prerequisites:** none technical — this is the human-safety view; no command line in this lesson.

**Map ref:** serves **CISSP objective 7.15** — personnel safety and security concerns: travel security, workplace violence prevention, duress, and protective concepts.

---

## 1. Where this shows up

Security operations protect systems; this lesson protects the humans who run them. Personnel safety covers the risks to people as people: the engineer traveling to a high-crime region, the workplace-violence warning signs nobody reported, the duress situation no one rehearsed, the executive whose public profile makes them a target. It shows up in the travel briefing that kept a team out of trouble, in the incident report that began "we saw the signs and didn't act," and in the lone worker's check-in procedure that actually gets used. Security managers, executive-protection coordinators, and GRC analysts live here. Note the boundary with the Domain 1 personnel-security lesson: that one governs the employment lifecycle as policy — background checks, onboarding, termination. This lesson governs keeping people safe — travel, workplace violence, duress, and protection. HR policy decides who gets hired; this lesson decides how they come home.

## 2. Before you start

- No technical prerequisites. The work products are documents: a travel-security briefing, a workplace-violence prevention procedure, and a duress/check-in design.
- The mindset shift: the asset here is a person, and the "controls" are procedures, training, and communication — evaluated by whether people actually follow them, not by whether they're written.
- Primary spine: **OSHA's workplace-violence guidance** (osha.gov) and **CISA's insider-threat mitigation resources** (cisa.gov).

## 3. How it works

Three domains of personal safety, each with its own operating logic.

**Travel security: the briefing before the boarding pass.** Every trip to an elevated-risk location gets a **security briefing** built from authoritative sources — the State Department's OSAC (the Overseas Security Advisory Council, a State Department Diplomatic Security Service public-private partnership providing country security reports and a Traveler Toolkit for U.S. organizations operating abroad) country reporting, plus the organization's own risk picture. The briefing covers: the threat picture (crime, civil unrest, terrorism — what actually threatens travelers there, not generic anxiety); **communications** (check-in schedule, who the traveler calls and when, the escalation if a check-in is missed); **movement** (approved transport, routes, the no-go areas, the "don't" list — unmarked taxis, displaying valuables, predictable routines); **lodging and meeting** security (hotel selection criteria, room practices, meeting-venue vetting); and the **emergency plan** (embassy/consulate contacts, the organization's 24-hour number, medical evacuation arrangement, the rally point). Two rules: the briefing is *before* travel, in writing, acknowledged — and the traveler's family or emergency contact gets the communications plan too, because the missed check-in escalates to people who need to know what "missed" means.

**Workplace violence: prevention as a program.** OSHA defines workplace violence broadly — any act or threat of physical violence, harassment, intimidation, or other threatening behavior at the work site, ranging from threats and verbal abuse to assault and homicide — and publishes prevention guidance built on a clear-eyed premise: in most workplaces where risk factors can be identified, the risk can be prevented or minimized. The program elements, from OSHA's guidance: a **zero-tolerance policy** covering workers, clients, visitors, and contractors; **worksite assessment** (the risk factors OSHA names — exchanging money with the public, working alone or in isolated areas, late-night hours, high-crime locations, volatile contacts — assessed per site, not assumed uniform); **engineering and administrative controls** (the physical measures from `e-physical-security` — lighting, access control, visibility — plus staffing and procedural ones); **training** (recognizing warning signs, de-escalation, how to report, how to react); and **reporting and investigation** — every claim investigated and remedied promptly, with the reporting channel trusted enough to use. The honest note from the source: OSHA states there are currently no specific OSHA standards for workplace violence — the guidance is the program, and the enforcement backdrop is general. The management insight: the program lives or dies on the reporting channel. Warning signs get reported only where reporters trust the response — which means the first few reports must be handled visibly well, or there won't be more.

**Duress, check-in, and protective concepts.** Some situations need a covert signal: the **duress code** — a pre-agreed word or phrase, ordinary in context, that tells the listener "I'm under coercion, send help, don't acknowledge this." The design rules: it must be usable under stress (simple, rehearsed), deniable (sounds normal to the coercer), and tied to a response (the listener knows exactly what to do — who they call, what they don't say). The **lone-worker check-in** is the routine version: scheduled contacts, the missed-check-in escalation with named responders and timelines. **Executive protection** concepts scale the same thinking: profile management (what's public about the principal), route and venue planning, the advance work before the visit. The common thread: these are *rehearsed* procedures, not documents. A duress code never practiced is a phrase, not a control — the drill is the implementation.

### Worked example: Kestrel Components — travel briefing and safety procedures

**The company (fictional, continued from `e-media-protection` and `e-physical-security`).** Kestrel's field engineer, Amara D., travels to commission equipment at a customer site in a region with elevated street crime and periodic civil unrest. Separately, the HQ office manager has received two aggressive confrontations from a terminated contractor at the reception desk.

**The travel-security briefing (excerpt, fictional).** *Threat picture:* street crime (theft, express kidnapping in the metro area per OSAC country reporting), unrest concentrated in the capital's central district — the customer site is outside it. *Communications:* check-in twice daily with the operations manager (08:00 and 20:00 local); missed check-in escalates at +2 hours to the security lead, at +4 to the 24-hour response number and the travel-risk provider. *Movement:* pre-arranged car service only (no street taxis), hotel-to-site route vetted, no-go areas mapped, valuables policy (no visible laptop bag branding). *Lodging:* hotel from the approved list (controlled access, room above ground floor, below the top floors). *Emergency plan:* consulate contacts, the medical-evacuation membership number, the rally point (the hotel, then the consulate), and the duress phrase — ordinary in context ("I'll send the revised drawings tonight"), meaning: *I'm under coercion; start the response; don't acknowledge.* Amara acknowledges the briefing in writing; the emergency contact (her partner) gets the communications plan and the escalation meaning of a missed check-in.

**The workplace-violence procedure (excerpt, fictional).** *Policy:* zero tolerance, posted, covering employees, visitors, contractors — signed acknowledgment for all staff. *Assessment:* reception identified as the highest-risk point (public contact, the recent confrontations); the late-shift warehouse as second (isolated, night hours). *Controls:* reception gets the physical measures (the `e-physical-security` review — controlled entry, duress alarm at the desk routed to the guard's radio, not email); warehouse late shift moves to paired staffing. *Training:* all staff — warning signs, de-escalation basics, the reporting channel, what happens after a report. *Reporting:* reports go to the office manager and the security lead jointly; every report investigated within 48 hours; outcomes communicated back to the reporter (the trust loop). The two confrontations are logged as the procedure's first cases — investigated, the contractor trespassed from the premises, reception briefed on the outcome.

**The check-in design (lone worker, fictional).** Field engineers on customer sites: check-in on arrival, midday, and departure; missed check-in +1 hour → supervisor calls; +2 hours → security lead dispatches the local contact. The schedule lives in the shared calendar, not in anyone's head.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the travel briefing, workplace-violence procedure, and check-in design above, authored and self-reviewed in-session on 2026-10-10 against OSHA's prevention-program elements and OSAC's briefing resources. Transcript: `runs/e-personnel-safety.log`.

1. **Write the travel briefing.** For a fictional (or real) trip: threat picture from OSAC country reporting, communications plan with escalation timelines, movement rules, lodging criteria, emergency plan with contacts. The traveler acknowledges in writing; the emergency contact gets the comms plan.
2. **Design the duress signal.** A phrase ordinary in context, deniable, rehearsed — tied to a listener response (who they call, what they don't say). Write the response procedure, not just the phrase.
3. **Assess the workplace.** Per site: OSHA's risk factors (public contact, isolation, hours, location, volatile contacts). Name the highest-risk point and the honest reason — the recent incident is data, use it.
4. **Write the prevention procedure.** Zero-tolerance policy, controls (engineering and administrative), training content, reporting channel with the 48-hour investigation commitment and the trust loop (outcomes communicated back).
5. **Design the lone-worker check-in.** Schedule, missed-check-in escalation with named responders and timelines, where the schedule lives. Then the honesty test: who actually notices a missed check-in at 22:00?
6. **Rehearse one thing.** The duress phrase, the check-in escalation, or the de-escalation response — picked, scheduled, done. The drill date is part of the artifact.

## 5. On your own

**Task:** Write the travel-security briefing for a trip you're actually taking (or took recently) — threat picture, comms plan, emergency contacts. Then assess your own workplace against OSHA's risk factors and write the one procedure it's missing.

**Success test:** The briefing names a specific threat you hadn't considered before writing it (that's the OSAC reporting earning its keep), and the workplace assessment finds the unmonitored reporting gap — the channel people don't trust or don't know. If your workplace needs nothing, assess a friend's (with permission).

## 6. Where it goes wrong

- **The unbriefed traveler.** Sent with a plane ticket and good luck. The briefing is before travel, in writing, acknowledged — the cost is an hour, the alternative is improvisation under threat.
- **The emergency contact who knows nothing.** The missed check-in escalates to someone who doesn't know what "missed" means or who to call. The comms plan goes to the family too.
- **Warning signs, unreported.** The concerning behavior everyone saw and nobody reported — because the channel wasn't trusted or wasn't known. The first reports must be handled visibly well.
- **The policy nobody signed.** Zero tolerance, unposted, unacknowledged. The policy's existence matters less than its communication — signed, posted, trained.
- **Duress as a phrase.** The code word nobody rehearsed, tied to no response. Rehearsal is the implementation; the drill date is part of the artifact.
- **The 22:00 check-in.** The escalation that names a responder who doesn't watch the channel at night. The honesty test in the walkthrough exists for this — name who actually notices.
- **Protection as secrecy.** The executive's itinerary shared widely "for coordination." Need-to-know (from `e-secops-concepts`) applies to people's movements too.
- **The HR-only view.** Treating the aggressive confrontation as purely an HR matter with no security procedure. The Domain 1 lesson handles the employment side; this lesson handles the safety side — both run.

## 7. Read the source

Primary documents first:

- **OSHA: Workplace Violence — Overview** (osha.gov) — *read* the overview page: the definition, who's at risk, the risk factors, and the prevention-program elements (policy, assessment, controls, training). Note honestly: OSHA states there are currently no specific standards for workplace violence — the guidance is the program.
- **CISA: Insider Threat Mitigation** (cisa.gov) — *read* as the companion: the pathway from concerning behavior to action — reporting, assessment, and intervention resources. Free.

Then at most three free resources:

1. **OSAC — Overseas Security Advisory Council** (osac.gov) — free; the State Department Diplomatic Security Service's public-private partnership: country security reports and the Traveler Toolkit — the authoritative input to every travel briefing.

## 8. Check yourself

1. An engineer travels to an elevated-risk region with no briefing; the check-in arrangement is "text me when you land." Name the three distinct failures (briefing, communications design, emergency planning) and what each would have specified.
2. Explain why the reporting channel is the load-bearing element of a workplace-violence program — what happens to reporting after the first two reports are handled badly, and what does "handled visibly well" require?
3. Design a duress phrase for a field engineer and its listener response: what are the three design rules (usable, deniable, tied to response), and what breaks if the phrase is never rehearsed?
4. Distinguish this lesson from the Domain 1 personnel-security lesson using the terminated contractor's confrontations: which lesson handles the termination procedure, which handles the reception-desk safety, and why do both run?
5. Predict the lone-worker check-in one year after it's designed but never tested: what does a missed 22:00 check-in actually trigger, and which walkthrough step would have caught it?

## 9. Prove it

**Artifact:** your travel-security briefing (threat picture, comms with escalation, movement, lodging, emergency plan — acknowledged in writing), workplace-violence prevention procedure (policy, assessment, controls, training, reporting with the trust loop), duress design with listener response, and the lone-worker check-in with the honesty test answered — for the Kestrel worked case in your own words, or better, for travel and a workplace you actually know.

**Honest claim:** "I can protect the people — brief travel so the risks are named and the comms work, build the workplace-violence program around a trusted reporting channel, and design duress and check-in procedures that function under stress."
**Can't claim yet:** "I can run executive protection" — close protection as a discipline (advance work, protective details, protective intelligence) is its own profession; this lesson taught the concepts and the procedures an organization can operate itself.

## 10. Leads to

- `e-physical-security` — the same building, the controls view: the duress alarm, the controlled entry, and the guard the safety procedures rely on.
- `e-secops-concepts` — need-to-know applied to people's movements and itineraries.
- `e-incident-management` — the missed check-in escalates into the incident structure; the workplace-violence report can become the incident.
- Map refs: **CISSP 7.15** (this lesson); feeds **CISSP 1.8** (personnel security) and **7.14** (physical security operations).

---

*Worked case authored and self-reviewed 2026-10-10; all scenario data fictional. Sources fetched in-session — see `runs/e-personnel-safety.log`.*
