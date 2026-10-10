---
lesson_id: e-change-management
slug: change-management
stage: E
level: 3
prerequisites: [e-config-management]
roles: []
map_refs: ["CISSP 7.9"]
test_date: 2026-10-10
description: "How to run change management — the change request, CAB review with written rationale, change paths, and the emergency procedure that keeps a spine. A free lesson in the security guidebook, serving CISSP objective 7.9."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Change management: approving the change before it ships


**Map ref:** serves **CISSP objective 7.9** — change management: reviewing, approving, and controlling changes to the trusted state.

---

## 1. Where this shows up

Most outages are caused by changes, and most unauthorized changes were made by authorized people skipping the process. Change management is the discipline that puts a decision — with a rationale, a risk assessment, and a backout plan — between "I want to change this" and the change itself. It shows up in the Friday-afternoon firewall edit that took down the VPN, in the "temporary" config tweak that became permanent, in the audit finding of production changes with no record — and in the CAB meeting that actually caught the bad change before it shipped. Operations leads, SOC managers, and GRC analysts live here. It is the taught pair of `e-config-management`: the baseline defines the trusted state, change management governs how the trusted state moves, and drift detection catches what moved without permission.

## 2. Before you start

- You have a baseline from `e-config-management` — change management is the process that updates it legitimately.
- You know the incident lifecycle from `c-incident-response` — emergency changes borrow its urgency without borrowing its improvisation.
- No tools. The work products are documents: reviewed change requests (approve/reject with rationale), a change-process design, and an emergency-change procedure. Primary spine: **NIST SP 800-128** (change control within configuration management, August 2011) and **SP 800-53 CM-3** (baseline change control).

## 3. How it works

Change management is risk management applied to the act of changing things. Four elements.

**The change request: the unit of decision.** Every change — patch, config edit, firewall rule, deployment — arrives as a **request** with the same fields: what changes, why (the business or security reason), the risk assessment (what breaks if this goes wrong, who depends on it), the implementation plan (steps, in order), the test plan (how we verify it worked), the **backout plan** (how we undo it, and the criteria for deciding to), and the schedule (when, with what maintenance window). The request is where the thinking happens; a change that can't fill these fields isn't ready, which is itself a useful verdict. SP 800-53's CM-3 (baseline change control) is this in control language: changes to the baseline are controlled, documented, and approved — the baseline from `e-config-management` doesn't move without a request.

**Review: approve, reject, or approve with conditions.** The reviewer's job is not to rubber-stamp — it's to ask the questions the requester didn't. The standard **change advisory board (CAB)** is the review body: stakeholders who can see cross-impacts (network, security, application owners) meeting on a cadence matched to the change rate. But the expert's understanding goes past the meeting: the CAB is a *function*, not necessarily a weekly gathering — small organizations do it as an async review with the right approvers; what matters is that someone with standing to say no actually reads the request. Every decision is recorded with **rationale**: approved (why the risk is acceptable), rejected (what was wrong — missing backout plan, untested, wrong window), or approved with conditions (ship it after the load test, or with the monitoring alert pre-staged). The rationale is the audit trail and the teaching record — next quarter's reviewer learns from this quarter's reasons.

**Change types and their paths.** Not every change deserves the full CAB. The working model: **standard changes** (pre-approved, low-risk, routine — monthly patching per the `e-patch-management` SLA, user provisioning per `e-iam`) follow a documented procedure without per-instance review; **normal changes** go through the CAB; **emergency changes** take the fast path (below). The classification is itself a decision recorded in the process design — and the failure mode is everything becoming "emergency" to skip review, which the metrics catch (emergency-change rate trending up is a process failure, not a sign of urgency).

**Emergency changes: speed with a spine.** When production is down or exploitation is active, the normal path is too slow — but "emergency" doesn't mean "undocumented." The emergency procedure pre-decides: who can declare it (named role), the minimum review (one qualified approver, reachable now — the CAB chair's phone number, not a meeting), the minimum documentation (the request fields filled *after* the change if necessary, but filled — retrospectively within 24 hours), and the mandatory follow-up (the emergency change gets a post-implementation review at the next CAB: was it really an emergency? did the backout plan exist?). The retrospective review is the control that keeps the emergency path honest — without it, the fast path becomes the default path.

### Worked example: Beacon Logistics — three change requests, reviewed

**The company (fictional, continued from `e-bcp-drp` and `e-config-management`).** Beacon's dispatch system runs on the hardened baseline from `e-config-management`. The CAB meets weekly; the security lead chairs. Three requests arrive.

**CR-2026-118: Firewall rule for the new carrier integration — APPROVED WITH CONDITIONS (fictional).** Request: open the dispatch app's API port to the carrier's IP range. Risk assessment: adequate (single range, documented business need). Test plan: present. Backout: rule removal, 5 minutes. *Review finding:* the carrier's range is a /16 — far broader than needed. *Decision:* approved on condition the rule is scoped to the carrier's documented /28, with a 90-day review (the range may change; the review catches it). Rationale recorded: the business need is real, the blast radius was not — the condition fixes the radius.

**CR-2026-119: "Temporary" SSH password auth for weekend troubleshooting — REJECTED (fictional).** Request: enable password SSH on the dispatch servers for the weekend, revert Monday. *Review finding:* this is the exact change the `e-config-management` drift scenario caught last month — the "temporary" change that becomes permanent. The requester can't name what's broken about key-based access; the underlying need (troubleshooting from home) is real but the VPN path already exists. *Decision:* rejected. Rationale recorded: the risk (credential-auth exposure on the crown-jewel system) exceeds the convenience, the need has an existing solution, and "temporary" has a documented history of permanence. The requester is directed to the VPN runbook — the review teaches, not just blocks.

**CR-2026-120: Emergency — patch the KEV-listed VPN flaw — APPROVED VIA EMERGENCY PATH (fictional).** Friday 16:00: the `e-patch-management` emergency runbook triggers — KEV-listed CVE on the VPN concentrator. Declaration by the security lead per the runbook. Minimum review: the infrastructure lead approves by phone (named in the procedure). Minimum testing: the runbook's canary-plus-smoke, executed. Deployed 18:40, verified by scanner re-check. Documentation completed retrospectively by Monday 10:00. Post-implementation review at Wednesday's CAB: was the emergency path justified? Yes — KEV-listed, internet-facing, active exploitation reported. The review records one improvement: the carrier-notification template (from `e-incident-management`'s comms plan) didn't cover emergency maintenance — added.

**The process design (what Beacon wrote down).** Change types and paths (standard/normal/emergency with classification criteria), the CAB charter (members, cadence, quorum, the async path for small weeks), the request template (the seven fields), the decision record (approve/reject/conditions with rationale — published where requesters can learn from it), the emergency procedure (declaration, minimum review, retrospective documentation deadline, mandatory post-implementation review), and the metrics: change success rate, emergency-change rate, unauthorized-change rate (from the drift checker — the `e-config-management` feed).

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the three reviewed change requests and the process design above, authored and self-reviewed in-session on 2026-10-10 against SP 800-128's change-control framing and SP 800-53 CM-3. Transcript: `runs/e-change-management.log`.

1. **Write the request template.** The seven fields: what, why, risk, implementation plan, test plan, backout plan, schedule. If a field can't be filled, the change isn't ready — write that rule into the template.
2. **Design the paths.** Standard (pre-approved procedures), normal (CAB review), emergency (fast path) — with the classification criteria that route each change. Define the emergency rate metric that catches path abuse.
3. **Charter the CAB.** Members (who sees cross-impacts), cadence, quorum, the async alternative. The function matters more than the meeting.
4. **Review three requests.** Write one of each verdict: approve, reject, approve-with-conditions — each with the rationale recorded. Plant the flaws deliberately: the oversized firewall scope, the "temporary" auth change, the missing backout plan. The review must catch what you planted; if it doesn't, the review criteria are weak.
5. **Write the emergency procedure.** Declaration authority, minimum review, minimum testing, retrospective documentation deadline, mandatory post-implementation review. Then the honesty test: would this procedure have caught last month's "emergency" that wasn't?
6. **Define the metrics.** Change success rate, emergency-change rate, unauthorized-change rate (fed by drift detection). Name who reads them and what trend triggers a process review.

## 5. On your own

**Task:** Take the last three changes you made to a system you run (a config edit, an update, a firewall rule). Write each up as a change request with the seven fields — honestly, including the ones you skipped. Then review them as the CAB: what verdict would each get?

**Success test:** At least one of your past changes gets rejected or conditioned — the missing backout plan is the usual verdict. If all three pass cleanly, you're reviewing your own work too kindly; hand one to someone else.

## 6. Where it goes wrong

- **The rubber stamp.** The CAB that approves everything in eleven minutes. A review with no rejections is a review that didn't happen — the chair's job is to ask the unasked question.
- **"Temporary" as a change type.** The permanent temporary change. Every temporary change gets an expiry and an owner, or it's rejected.
- **Everything is emergency.** The fast path becomes the default path. The emergency-rate metric and the mandatory post-implementation review exist to catch exactly this.
- **No backout plan.** The change that can't be undone, discovered mid-incident. Backout is a field on the template, not an afterthought — and the rollback criteria are decided before the change ships.
- **Undocumented approval.** The hallway "yeah, go ahead." Approvals live in the decision record with rationale, or they didn't happen.
- **Change without test.** Skipping verification because the change is "small." Small changes cause large outages; the test plan scales to the risk, it doesn't vanish for it.
- **The CAB as bottleneck.** Review so slow that teams route around it. The async path, the standard-change pre-approvals, and a cadence matched to the change rate keep the process from becoming the problem it solves.
- **ITIL as the only answer.** ITIL 4's change enablement is the commercial reference — and a paid framework, so this lesson teaches the function from free sources (one line, per the brief's rule). The function is what matters; the framework is one packaging.

## 7. Read the source

Primary documents first:

- **NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems** (csrc.nist.gov, August 2011) — *read* for change control as part of configuration management: changes to the baseline are identified, evaluated, approved, and documented.
- **NIST SP 800-53 Rev. 5, CM-3 (Baseline Change Control)** — the control-language version: control changes to the baseline, document, approve, audit. Find it via the SP 800-53 publication page (csrc.nist.gov).

Then at most three free resources:

1. **SANS Information Security Policy Templates** (sans.org) — free; the change-management policy template is the starting skeleton — fill it with your process, don't file it as-is.

## 8. Check yourself

1. A CAB approves forty changes in a twelve-minute meeting with no rejections and no conditions. Name the two distinct failures (one in review quality, one in change classification) and the metric that would have surfaced each.
2. Explain why the emergency change procedure requires retrospective documentation and a post-implementation review — what specific abuse does each prevent, and what happens to the fast path without them?
3. A "temporary" firewall rule from 2023 is found still active. Using the change-type model, explain which path it should have taken, what the expiry mechanism would have done, and whose metric catches it now.
4. Distinguish the CAB as a function from the CAB as a meeting: what does the async review preserve, what does it lose, and when is the meeting the right form?
5. Predict the emergency-change rate of an organization whose normal path takes three weeks: what does the rate look like after a year, and what does the post-implementation review conclude about the process?

## 9. Prove it

**Artifact:** your change-process design (types, paths, classification criteria), CAB charter, the request template, three reviewed requests (approve / reject / approve-with-conditions, each with rationale), the emergency procedure, and the metrics set — for the Beacon worked case in your own words, or better, for changes you actually make, with your last three real changes written up and reviewed.

**Honest claim:** "I can run change management — put a real decision with rationale between intent and implementation, review requests honestly, and keep the emergency path fast without letting it become the default."
**Can't claim yet:** "I can transform an organization's change culture" — the politics of getting engineers to actually use the process, at scale, is organizational work beyond the process design; this lesson taught the design that makes the culture change possible.

## 10. Leads to

- `e-config-management` — the baseline this process moves; the drift checker catches what moved without a request. Read as the pair.
- `e-patch-management` — routine patching flows through the standard-change path; emergency patching through the fast path.
- `e-iam` — provisioning changes follow the same request discipline (the joiner/mover/leaver tickets are changes too).
- Map refs: **CISSP 7.9** (this lesson); feeds **CISSP 7.3** (configuration management).

---

*Worked case authored and self-reviewed 2026-10-10; all scenario data fictional. Sources fetched in-session — see `runs/e-change-management.log`. Note: ITIL 4 (change enablement) is a paid framework — one line per the brief's rule; this lesson teaches the function from free sources.*
