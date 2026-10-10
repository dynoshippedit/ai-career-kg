---
lesson_id: e-awareness-training
slug: awareness-training
stage: E
level: 3
prerequisites: [c-soc-triage]
roles: []
map_refs: ["CISSP 1.12"]
test_date: 2026-10-10
description: "Design a one-year security learning program measured by behavior change. A free lesson in the security guidebook, serving CISSP objective 1.12."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Security awareness, education, and training: building the learning program


**Map ref:** serves **CISSP objective 1.12** — security awareness, education, and training programs.

---

## 1. Where this shows up

Every control in this guidebook assumes a human who knows what to do. The phishing email that the finance officer reports instead of clicking — or does not. The developer who recognizes a secret in a code review because training made it salient. The new hire who knows the acceptable-use policy because onboarding taught it, not because it was emailed as a PDF. Security awareness, education, and training is the program that builds those humans — and it is where most organizations run an annual checkbox video, measure completions, and declare victory while the click rate never moves. This lesson teaches the program as NIST now frames it: not a training course but a learning program, designed around audiences, measured by behavior change, and owned like any other security control.

## 2. Before you start

- No technical prerequisites beyond Stage D. This lesson is program design: audiences, objectives, delivery, measurement.
- Bring `c-soc-triage`'s human-factor material — fatigue, inattention, and workaround culture are the problems the program exists to reduce.
- Bring your `e-policy-docs` hierarchy — the program is how policy becomes known; a policy nobody has been taught is shelfware with extra steps.
- The work product is a one-year program plan for a fictional company, with the rules of engagement for phishing simulation and the metrics that prove effectiveness.

## 3. How it works

**The rename that matters.** NIST SP 800-50 Rev. 1, *Building a Cybersecurity and Privacy Learning Program* (September 2024 — the primary source for this lesson, fetched in-session; it supersedes both the 2003 SP 800-50 and the 1998 SP 800-16) deliberately retired the old awareness/training/education three-tier split. The reason, stated in the publication itself: research with federal training managers showed the three terms meant different things to different people and caused confusion when describing what the program is for. The replacement term is **CPLP — Cybersecurity and Privacy Learning Program** — applied generically: whatever your organization calls its program, the goal is providing learning opportunities at every career stage, not sorting activities into three buckets. The lesson for practitioners: stop arguing about whether something is "awareness" or "training" and start asking whether it changes behavior.

**Program design, end to end.** A learning program is designed like any security control — with a purpose, an audience, and a measurement:

1. **Needs assessment.** What do the humans actually get wrong? Phishing-report rates, policy-violation patterns, incident root causes involving human action, audit findings about untrained roles. The program targets the observed failures, not a generic curriculum.
2. **Audience segmentation.** One size fits none: all-staff foundations (phishing, passwords, reporting), privileged users (the access they hold and the targeting they attract), developers (secure coding, secrets handling — coordinate with `e-sdlc`), executives (their risk decisions and their attractiveness as targets), and new hires (onboarding that actually teaches the policy). Each segment gets objectives appropriate to its risk.
3. **Learning objectives.** Stated as behaviors, not topics: "report suspected phishing within 15 minutes" beats "understand phishing." Objectives are testable; topics are not.
4. **Delivery.** Varied by audience and attention budget: short modules, simulated phishing, tabletop participation, onboarding sessions, just-in-time nudges. The annual hour-long video is the minimum viable program, not the model.
5. **Reinforcement.** Learning decays. The program repeats, varies, and reinforces — the phishing simulation is monthly, not annual; the policy reminder arrives when the behavior matters.
6. **Measurement of effectiveness.** The program measures behavior change, not completions. Completion rate is an activity metric — it proves the video played. Report rate, click rate *trend*, time-to-report, and policy-violation recurrence are effectiveness metrics — they prove humans changed. An honest program reports both and optimizes for the second.

**Phishing simulation: the rules of engagement.** Simulated phishing is the program's most powerful and most dangerous tool — powerful because it measures real behavior, dangerous because it can destroy trust. The rules, written before the first simulation runs:

- **Purpose is learning, not punishment.** Results go to the program, not to performance reviews — the moment a simulation feeds HR discipline, reporting dies and the metric becomes fear compliance.
- **No shaming.** No public leaderboards of clickers, no "gotcha" emails from the CEO. Embarrassment teaches avoidance of the program, not of phishing.
- **Immediate, kind feedback.** The click lands on a teaching moment — what the tell was, what to do next time — not a reprimand.
- **Report-rate over click-rate.** The metric that matters is how many people *report* the phish, because reporting is the behavior that saves the organization. A program that drives clicks down by terrifying people has optimized the wrong thing.
- **Vary and escalate honestly.** Templates evolve with the real threat landscape; difficulty ramps. But the simulation never impersonates a real person in a way that damages trust (no fake messages "from the CEO" that then require the CEO to explain), and the program's existence is not secret — people know simulations happen; they do not know when.
- **Exclude with care.** Excluding executives "because they're busy" teaches the organization that security is for other people. Include everyone; tailor difficulty.

**Roles and ownership.** The program has a named owner (often the CISO's organization, sometimes a dedicated awareness lead), content owners per audience segment, and executive sponsorship — visible, not nominal. The CISO who has never taken the training is the program's credibility problem. Funding follows the measurement: effectiveness metrics justify the budget; completion metrics justify only the checkbox.

**The governance home.** The program lives under the governance charter (`e-governance`): policy requires it, the risk committee sees its metrics, and the annual review asks whether behavior changed. A learning program outside governance is a marketing campaign.

### Worked example: Copperline Freight — one-year program plan (fictional)

**The organization (fictional).** Copperline Freight (fictional, continued from `e-governance`): 240 staff across three sites — dispatchers, drivers, warehouse, finance, IT, executives. Current state: one annual video, 94% completion, phishing click rate unmeasured, no reporting button in the email client.

**The plan (abridged — the full version is the artifact):**

- **Needs assessment findings:** two 2025 incidents involved credential phishing of dispatchers; the finance team wires funds on email instruction; drivers use personal devices for dispatch messaging. The program targets these three behaviors first.
- **Audience segments and objectives:**
  - *All staff (240):* report suspected phishing via the new report button within 15 minutes; never act on financial instruction by email alone (verify by voice). Quarterly short modules plus monthly simulations.
  - *Dispatchers and finance (45):* targeted deep-dives — business-email-compromise patterns, voice-verification procedure for payment changes. The highest-risk segment gets the most attention.
  - *IT and privileged users (18):* admin-targeting awareness, secrets handling, the reporting expectations for their elevated risk. Coordinated with `e-iam`'s privileged-access work.
  - *Executives (8):* whaling and impersonation briefing, their role in incident communications, visible participation in the program (credibility).
  - *New hires:* day-one security onboarding — acceptable use, reporting, phishing basics — before system access, not after.
- **Topic calendar (quarters):** Q1 — phishing recognition and the report button (launch); Q2 — business email compromise and payment verification; Q3 — passwords, MFA, and device hygiene; Q4 — holiday-season social engineering and the annual review. Monthly phishing simulations throughout, difficulty ramping, templates drawn from the real threats the SOC sees (`c-soc-triage` feeds the template library).
- **Phishing simulation rules of engagement:** purpose is learning; results never feed performance reviews; no public shaming; immediate teaching-moment feedback on click; report-rate is the headline metric; executives included; program existence announced, timing not.
- **Effectiveness metrics:** phishing report rate (target: rising trend), click rate (target: falling trend — secondary), median time-to-report, training completion (activity — reported, not optimized), policy-violation recurrence for the three targeted behaviors, and new-hire onboarding completion before access grant. Reported quarterly to the risk committee.
- **Ownership:** program owner — the security awareness lead (new role, reporting to the CISO); content owners per segment; executive sponsor — the CEO, who takes the training publicly in Q1.

**Why this plan works:** it starts from observed failures, segments by risk, states objectives as behaviors, measures effectiveness rather than activity, and puts the program under governance. The 94%-completion video is replaced, not supplemented — the plan says so explicitly, because "both" means the checkbox survives and the behavior never changes.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the program plan above, authored and self-reviewed in-session on 2026-10-10 against NIST SP 800-50 Rev. 1's CPLP framing. Transcript: `runs/e-awareness-training.log` (records the needs assessment, the segments, the simulation rules, the metrics, and the review checklist — no commands to transcribe).

1. **Assess needs.** List the organization's actual human-factor failures: phishing incidents, policy violations, audit findings, the behaviors behind recent incidents. Three concrete failures minimum — the program targets these, not a generic curriculum.
2. **Segment the audience.** All-staff, high-risk roles, privileged users, developers, executives, new hires. For each: what they must *do* differently, stated as behavior.
3. **Build the calendar.** Four quarters of topics tied to the needs assessment, with delivery methods per segment. Monthly phishing simulations with ramping difficulty.
4. **Write the simulation rules.** Purpose, no-punishment, no-shaming, feedback, report-rate as headline metric, executive inclusion, announcement policy. Written before the first simulation — retroactive rules are damage control.
5. **Define the metrics.** Effectiveness (report rate, time-to-report, behavior recurrence) separated from activity (completion). Targets as trends, not absolutes — the program improves behavior; it does not achieve a number.
6. **Assign ownership and governance.** Named owner, content owners, executive sponsor, quarterly reporting to the risk committee. Then schedule the annual program review.

## 5. On your own

**Task:** Write the one-year plan for an organization you know — your employer, your lab treated as an org, or a fictional company. Minimum: needs assessment with three real failures, four audience segments with behavioral objectives, the quarterly calendar, the simulation rules of engagement, and the metrics split (effectiveness vs activity).

**Success test:** Your plan replaces at least one checkbox activity with a behavioral intervention (not "in addition to" — replacement); your metrics include report-rate or an equivalent behavior metric as the headline; and the simulation rules are written before any simulation runs. If the plan could be executed without changing anyone's behavior, it is a calendar, not a program.

## 6. Where it goes wrong

- **The annual checkbox video.** One hour, once a year, completion measured, behavior unmeasured. The minimum viable program treated as the model.
- **Completion as victory.** 94% completion reported as success while the click rate never moves. Activity metrics optimizing the wrong thing.
- **Shaming the clickers.** Public leaderboards, "gotcha" emails, HR referrals. Trust in the program dies; reporting dies with it; the metric becomes fear compliance.
- **Punishment pipelines.** Simulation results feeding performance reviews. The program becomes surveillance, and humans route around surveillance.
- **One size fits all.** The same module for dispatchers, developers, and executives. Nobody's actual risk addressed; everybody's time wasted.
- **The excluded executive.** "Too busy" for the simulation. The organization learns that security is for other people — from the top.
- **Secret simulations.** People discover they were tested without ever being told a program exists. The betrayal response poisons every future security message.
- **No governance home.** The program runs outside the charter, unmeasured by the risk committee, unfunded past the video license. `e-governance`'s rule: what is not governed is not sustained.

## 7. Read the source

Primary documents first:

- **NIST SP 800-50 Rev. 1, Building a Cybersecurity and Privacy Learning Program** (September 2024; csrc.nist.gov) — *read* the CPLP framing and the program-design guidance; *note* the deliberate retirement of the awareness/training/education split and why. Free.

Then at most three free resources:

1. **CISA Cybersecurity Awareness Month resources** (cisa.gov) — free; campaign materials and themes — use as content inputs for your quarterly calendar, not as the program itself.

## 8. Check yourself

1. A program reports 96% training completion and has never measured phishing report rate. Explain which metric is activity and which is effectiveness — and what the program must change to measure the second.
2. A CISO proposes feeding phishing-simulation click results into annual performance reviews "to drive accountability." Argue against it from the rules of engagement: what breaks, and what metric should be the headline instead?
3. Explain the SP 800-50 Rev. 1 rename: why did NIST retire the awareness/training/education split, and what does the CPLP framing change about how you design the program?
4. An organization excludes executives from phishing simulation "because they're busy." Name the two distinct failures (credibility and risk) and the rule that prevents both.
5. Predict the state of a learning program two years after its owner leaves, with no governance home and no metrics beyond completion: what does the quarterly report to the risk committee look like, and what does it conceal?

## 9. Prove it

**Artifact:** your one-year program plan (needs assessment, audience segments with behavioral objectives, quarterly topic calendar, phishing-simulation rules of engagement, effectiveness-vs-activity metrics, ownership and governance) — for the Copperline worked case in your own words, or better, for a real organization.

**Honest claim:** "I can design a security learning program around observed human-factor failures — segmented, behavioral, measured by effectiveness — including phishing simulation with rules of engagement that build trust instead of destroying it."
**Can't claim yet:** "I can change an organization's security culture" — culture change is a multi-year leadership outcome; this lesson taught the program design that makes it possible, which is where the practitioner's leverage is.

## 10. Leads to

- `e-governance` — the program's home: charter, risk-committee reporting, annual review.
- `e-policy-docs` — the program's curriculum source: policy is what the program teaches.
- **C-SOC — `c-soc-triage`** — the template library: real phishing the SOC sees becomes the simulation content.
- Map refs: **CISSP 1.12** (this lesson); feeds **CISSP 7.15** (personnel security) and **1.3** (governance).
