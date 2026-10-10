---
lesson_id: e-personnel-security
slug: personnel-security
stage: E
level: 3
prerequisites: [e-iam]
roles: []
map_refs: ["CISSP 1.8"]
test_date: 2026-10-10
description: "Run the human side of hiring, transfer, departure, and travel security with owners and timing. A free lesson in the security guidebook, serving CISSP objective 1.8."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Personnel security: the human side of the employment lifecycle


**Map ref:** serves **CISSP objective 1.8** — personnel security across hiring, employment, and departure.

---

## 1. Where this shows up

`e-iam` taught the technical lifecycle: provision, review, deprovision. This lesson teaches the human side of the same transitions — who decides what, who tells whom, and in what order, when a person joins, moves, travels, or leaves. It shows up in the background check calibrated to the role's trust level; in the NDA signed on day one and the acceptable-use acknowledgment that makes enforcement possible; in the termination where IT learns about the departure from the farewell email; in the shared admin password that was never rotated after three departures; and in the traveling executive whose laptop crosses a border carrying the company's crown jewels. Personnel security is the discipline of making the human transitions as deliberate as the technical ones — because every technical control in `e-iam` depends on a human process firing first.

## 2. Before you start

- You know the technical transitions from `e-iam` — joiner, mover, leaver, with SLAs. This lesson assigns the *human* owners and timing: HR, the manager, security, IT.
- Bring the insider-threat material referenced in §7 — the departure procedures here are insider-threat prevention in practice.
- The work products are documents: a termination checklist with owners and timing per action, an access-revocation runbook, and a travel-security briefing.

## 3. How it works

**The lifecycle, from the human side.** NIST SP 800-53 Rev. 5's Personnel Security (PS) family — the control catalog for this domain, verified on the csrc.nist.gov publication page — organizes the same ground this lesson walks: screening, termination, transfer, sanctions, agreements. The frame:

- **Hiring — screening proportionate to trust.** The background check matches the role's access: a help-desk hire and a domain administrator are not screened identically, because their blast radii (the damage if that account is compromised) differ. Screening is role-based, documented, and completed *before* privileged access is granted — the check that finishes after the admin credentials are issued is theater. New hires sign the NDA/nondisclosure agreement and acknowledge the acceptable-use policy (the policy stating what employees may and may not do with company systems — the document that makes enforcement possible) on day one — not because the signature prevents misconduct, but because enforcement without a signed acknowledgment is uphill.
- **Employment — the ongoing relationship.** Least privilege and separation of duties (your `e-iam` lesson) are personnel-security controls with human owners: the manager who approves access, the security team that reviews it. The disciplinary process is graduated and documented — verbal, written, suspension, termination — because an undocumented disciplinary history cannot support a termination decision. Ongoing awareness (`e-awareness-training`) keeps the acceptable-use acknowledgment alive past day one.
- **Transfer — the mover's human half.** When someone changes roles, the manager owns confirming which access dies with the old role — the technical mover checklist in `e-iam` needs a human trigger, and the trigger is the transfer conversation. Moves into higher-trust roles re-trigger screening: the check that cleared a support analyst does not clear a database administrator, because the original screening assessed a different blast radius — the new role's access was never part of that decision.
- **Departure — the highest-risk transition.** Departures come in flavors with different timing: voluntary resignation (notice period, orderly handover), involuntary termination (immediate revocation, no notice-period access — the timing difference is motive: a person just fired for cause has both the reason and, until revocation, the means; the window between knowledge of termination and loss of access is the danger window), layoffs (volume — the process must scale), and contractor end-of-engagement (the end date must exist in a system, not in someone's head — `e-iam`'s orphaned-contractor finding was a personnel-security failure first). The termination checklist covers: access revocation timing per system, asset return (hardware, tokens, documents), knowledge transfer, the exit interview, and post-departure monitoring for privileged roles.

**The insider threat lens.** CISA's insider threat mitigation guidance (fetched for this lesson) frames the problem: trusted insiders with legitimate access are the vector — theft of intellectual property, sabotage, fraud, espionage. The personnel-security controls are the mitigations: screening at hire, least privilege during employment, immediate revocation at involuntary departure, and attention to the behavioral precursors (disgruntlement, policy violations, unexplained affluence — observed and reported through a defined channel, not gossiped about). The point is structural, not accusatory: the controls protect the organization *and* the employee, because a clean process leaves no ambiguity about who did what.

**NDAs and agreements.** The nondisclosure agreement, the acceptable-use acknowledgment, the non-compete where used — these are HR-owned documents with security consequences. The practitioner's interest is narrow and practical: are they signed before access is granted, are they acknowledged (not just distributed), and do they cover the data the person will actually touch? An NDA signed six months after the admin credentials is evidence of a process failure, not protection.

**Separation of duties, human edition.** SoD is usually taught as a technical control (no single account can both create and approve a payment). The personnel version: no single *person* controls a critical process end to end — the person who can grant access cannot approve their own access; the person who processes terminations is not the terminated person's manager acting alone. Collusion resistance comes from the human arrangement, not the permission bit.

**Travel security.** High-risk travel is a personnel-security event: the briefing happens *before* departure, not after the incident. The elements: travel with minimal data (a loaner device or a wiped profile — the crown jewels do not cross borders on a daily driver), assume the device and the network are monitored, know the local reporting procedure, and debrief on return (device inspected, credentials rotated). The briefing is documented — the traveler acknowledged it — because the post-incident question will be "were they briefed," and the answer needs evidence.

### Worked example: Copperline Freight — privileged departure runbook (fictional)

**The situation (fictional).** Copperline Freight (fictional, continued from `e-governance`): a systems administrator with domain-admin rights resigns voluntarily, giving two weeks' notice. The risk: two weeks of privileged access by someone with no future stake, plus everything they know walking out the door.

**The termination checklist — owners and timing.** (Abridged; the full version is the artifact.)

| When | Action | Owner |
|---|---|---|
| Notice received (day 0) | Record the departure in the HR system with the last working day — the system date drives everything downstream | HR |
| Day 0 | Risk-rate the departure: privileged access plus voluntary resignation equals elevated handling — privileged accounts move to monitored status, no new privileged grants | Security lead |
| Day 0 | Inventory the person's access: every system, every shared credential they know, every physical token | IT, from the `e-iam` role definitions |
| Days 1–10 | Knowledge transfer: document the undocumented — runbooks, passwords in the vault (rotated, not shared), vendor contacts. The manager verifies completeness, not the departing employee's word alone | Manager |
| Day 10 | Rotate every shared credential the person knew — admin passwords, service accounts, Wi-Fi PSKs (pre-shared keys — the shared Wi-Fi passwords), safe combinations. Shared secrets are compromised by departure by definition | IT |
| Last day, morning | Exit interview: asset return checklist (laptop, tokens, badges, documents), NDA reminder in writing, forwarding-address confirmation for post-employment obligations | HR |
| Last day, COB (close of business) | Revoke all access per the `e-iam` leaver SLA; disable, do not delete, the accounts (preservation for the administrative track — see `e-investigations`) | IT |
| Day +1 | Verify: attempt login as the departed identity (should fail), confirm shared-credential rotation completed, confirm the HR system shows the termination | Security lead |
| Day +30 | Post-departure review for privileged roles: check for anomalous access in the final two weeks, confirm no lingering API keys or personal-device access | Security lead |

**The involuntary variant.** Same checklist, compressed: revocation *before* the termination meeting, the meeting with HR and security present, escort from the building, asset collection at the meeting — not "please mail the laptop." The timing difference is the whole difference: voluntary gets order, involuntary gets immediacy. Both get the shared-credential rotation — the step organizations skip most, because rotating shared secrets is tedious and nobody owned it. The checklist fixes that by naming IT and dating it.

**Travel-security briefing — one high-risk trip (fictional, abridged).** The CFO travels to a country with aggressive commercial-espionage reporting. Briefing (documented, acknowledged): travel on a loaner laptop with only the trip's data; no customer database access from the hotel network — use the approved remote-access path; assume device inspection at the border (power off, encrypted, no sensitive data at rest beyond the trip); report any device tampering, coercion, or "IT support" approaches immediately to the security lead; on return, the device goes to IT for inspection before reconnecting, and the travel credentials are rotated. The debrief is scheduled before departure — a briefing without a scheduled debrief is a suggestion.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the checklist, runbook, and briefing above, authored and self-reviewed in-session on 2026-10-10 against the SP 800-53 PS family and CISA's insider-threat guidance. Transcript: `runs/e-personnel-security.log` (records the timing decisions, the owner assignments, and the review checklist — no commands to transcribe).

1. **Pick the departure.** Voluntary privileged resignation (the worked case), involuntary termination, or contractor end — each has different timing. Write which one and why the timing differs.
2. **Build the checklist.** Every action gets three fields: what, owner, when. No action without an owner; no owner without a when. The `e-iam` leaver SLA gives you the technical timing — this checklist adds the human timing around it.
3. **Write the runbook.** The checklist in execution order, with the decision points: voluntary versus involuntary, privileged versus standard, the shared-credential rotation nobody wants to do. The runbook is what gets followed at 4 p.m. on a Friday — write it for that reader.
4. **Handle the shared secrets.** List every shared credential the departing person knew, and the rotation plan with a date. This step is the audit's favorite finding — do it properly here.
5. **Write the travel briefing.** One trip, one traveler, one risk profile: the pre-departure briefing, the in-travel rules, the scheduled debrief. Document the acknowledgment.
6. **Verify after.** The day-after verification (login attempt fails, rotation confirmed, HR system updated) is part of the runbook, not a nice-to-have. A checklist without verification is a wish list.

## 5. On your own

**Task:** Write the termination checklist and runbook for a departure in an organization you know — or your own hypothetical departure from a privileged role you hold (your homelab's admin, your cloud account's root). Include the shared-credential rotation with dates, and the travel briefing for one trip you actually take.

**Success test:** Every action has an owner and a when; the shared-credential rotation is dated, not aspirational; the involuntary variant exists and differs in timing; and the verification step is in the runbook. If the checklist would work identically for a voluntary and an involuntary departure, the timing analysis is missing.

## 6. Where it goes wrong

- **IT learns from the farewell email.** HR never told IT; the accounts linger. The HR-system date must drive deprovisioning — the process failure is upstream of the technical one. The tell: the HR system shows last-day Friday; the identity-provider log shows the account authenticating Monday.
- **The trusted exception.** "She's been here ten years, she doesn't need the checklist." Tenure is not a control. The checklist applies to everyone or it applies to no one.
- **Shared secrets never rotated.** Three departures, one admin password. Rotation after every privileged departure is the rule — tedious, non-negotiable, and the most common audit finding in this domain. The tell: the admin password's last-changed date predates three departures.
- **Screening as a one-time event.** The check at hire never re-fires on transfer to higher-trust roles. Trust levels change; screening must follow.
- **The skipped exit interview.** No asset-return checklist, no NDA reminder, no documentation. The interview is evidence as well as process.
- **Contractors outside the process.** No end date in any system, no checklist, no return of assets — the orphaned account in `e-iam` started as a personnel-security gap.
- **Travel without briefing.** The executive's daily driver crosses the border with the customer database. The briefing is cheap; the incident is not.
- **Delete instead of disable.** Accounts deleted on departure, destroying the evidence the administrative track might need — `e-investigations`' preservation rule applies here.

## 7. Read the source

Primary documents first:

- **NIST SP 800-53 Rev. 5, Personnel Security (PS) family** (csrc.nist.gov) — *read* the PS controls (screening, termination, transfer, agreements) as the control-language version of this lesson's checklist.

Then at most three free resources:

1. **CISA Insider Threat Mitigation** (cisa.gov) — free; the insider-threat frame this lesson's departure procedures implement — pathways, indicators, and the mitigation program structure.

## 8. Check yourself

1. A domain administrator resigns voluntarily with two weeks' notice; another is terminated for cause effective immediately. For each, state the access-revocation timing and explain why they differ — then name the step both cases share that organizations skip most often.
2. Explain why the HR-system departure date — not the manager's email, not IT's ticket — must drive deprovisioning, using the orphaned-contractor failure as the mechanism.
3. A company screens at hire but never on transfer to higher-trust roles. Describe the resulting exposure with a concrete role pair, and state the control that closes it.
4. Distinguish the personnel-security view of separation of duties from the technical view: give an example where the permission bits are correct and the human arrangement still fails.
5. Predict the findings of an audit of termination practices at a company with no checklist: rank the three most likely findings by how often they occur in practice, and state the evidence each one cites.

## 9. Prove it

**Artifact:** your termination checklist (what, owner, when per action), the access-revocation runbook (voluntary and involuntary variants, shared-credential rotation dated), and the travel-security briefing with acknowledgment — for the Copperline worked case in your own words, or better, for a real organization.

**Honest claim:** "I can run the human side of the employment lifecycle's security transitions — screening, transfer, departure, travel — with named owners, timing, and verification, and I can explain how each step prevents the insider-threat failure it targets."
**Can't claim yet:** "I can adjudicate employment-law questions" — background-check law, termination procedure, and non-compete enforceability vary by jurisdiction and belong to counsel and HR; this lesson taught the security process, not the employment law.

## 10. Leads to

- `e-iam` — the technical lifecycle this lesson's human process drives: the checklist triggers the provisioning system.
- `e-awareness-training` — the ongoing employment control: keeping the day-one acknowledgments alive.
- `e-investigations` — the administrative track: when a departure becomes an investigation.
- Map refs: **CISSP 1.8** (this lesson); feeds **CISSP 5.5** (provisioning lifecycle) and **7.15** (personnel safety and security).
