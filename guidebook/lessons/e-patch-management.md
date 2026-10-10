---
lesson_id: e-patch-management
slug: patch-management
stage: E
level: 3
prerequisites: [c-vuln-ecosystem, c-cvss]
roles: []
map_refs: ["CISSP 7.8"]
test_date: 2026-10-10
description: "How to run the patching operation — KEV-driven prioritization, severity-to-timeline SLAs, the exception register, and the emergency-patching runbook. A free lesson in the security guidebook, serving CISSP objective 7.8."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Patch and vulnerability management operations: from CVE to deployed fix


**Map ref:** serves **CISSP objective 7.8** — patch and vulnerability management as an operations discipline: timelines, exceptions, and the emergency path.

---

## 1. Where this shows up

Vulnerabilities are found constantly; patches exist for most of them; breaches still happen through unpatched systems years later. The gap between "patch available" and "patch deployed" is an operations problem — prioritization (which of this month's hundred patches goes first), scheduling (when can production be touched), exceptions (what can't be patched and why), and the emergency path (what happens when the exploited-in-the-wild patch lands on a Friday). It shows up in the ransomware that entered through a two-year-old flaw, in the "we'll patch it in the next window" that never came, and in the change board that treats every patch as equally urgent — which means none is. Vulnerability managers, SOC leads, and system owners live here.

## 2. Before you start

- You know the vulnerability inputs from `c-vuln-ecosystem` — CVE records, the KEV catalog, EPSS — and severity from `c-cvss`. This lesson turns those inputs into an operation.
- Routine patching flows through change control; emergency patching has its own path — the change-control discipline is `e-change-management`'s subject (same stage); this lesson teaches the patching-specific design.
- No tools. The work products are documents: a patching SLA policy, an exception register, and an emergency-patching runbook. Primary spine: **CISA's Known Exploited Vulnerabilities (KEV) catalog** and **NIST SP 800-40 Rev. 4** (Guide to Enterprise Patch Management Planning, April 2022).

## 3. How it works

Patching fails as an operation for predictable reasons: everything is "critical," nothing is scheduled, exceptions are verbal, and emergencies improvise. The operation fixes each.

**Prioritization: severity is not urgency.** A CVSS 9.8 on a system nobody can reach is less urgent than a CVSS 7.5 being exploited in the wild against your exact stack. The working prioritization, and the one this lesson's SLA is built on: **KEV membership first** — CISA's KEV catalog lists CVEs known to be exploited in the wild; anything in the catalog affecting your estate jumps the queue regardless of its CVSS. Then **exploitability and exposure** (is there a public exploit? is the system internet-facing? — the EPSS (Exploit Prediction Scoring System: an estimated probability the vulnerability will be exploited in the wild) and reachability inputs from `c-vuln-ecosystem`), then **severity** (CVSS as the tiebreaker), then **asset criticality** (the BIA's — Business Impact Analysis: the study ranking which processes matter most — crown jewels from `e-bcp-drp` go first within a tier). The federal reference point: CISA's binding operational directives have required federal agencies to remediate KEV-listed vulnerabilities on the catalog's timelines — BOD 22-01 (November 2021) established the model, and **BOD 26-04 "Prioritizing Security Updates Based on Risk" (2026) now supersedes it**, consolidating federal vulnerability-remediation guidance. The lesson's position: you are probably not a federal agency, but the KEV catalog is free and the prioritization logic — exploited-in-the-wild outranks theoretical severity — applies to everyone. The rationale is evidential: CVSS models how bad a flaw *could* be; KEV membership reports that someone is exploiting it *right now*. Evidence of attack beats a model of severity, because attackers don't read scores.

**The SLA policy: severity to timeline, in writing.** The SLA (service-level agreement — here, the organization's written commitment that each priority tier is remediated within a stated time) maps each priority tier to a remediation deadline, counted from the trigger (patch release or KEV listing, whichever the policy names): KEV-listed on in-scope systems gets the shortest clock; critical-exploitable next; high severity on a defined cadence; medium/low in the regular cycle. The deadlines are the organization's own decisions — the policy states them plainly, with the trigger event defined, because "promptly" is not a timeline and auditors will ask what it meant. SP 800-40 Rev. 4 (April 2022) is the planning guide underneath: it frames enterprise patch management as a program — inventory, prioritization, testing, deployment, verification — and insists on the unglamorous parts (knowing what you have to patch is step zero; the asset inventory is the patch program's foundation).

**Testing and deployment: the pipeline, not the event.** Patches break things — which is why "just patch faster" isn't an operation. The program defines **testing tiers** matched to risk: automated regression for routine patches, staged rollout (canary → subset → fleet) for broad ones, full pre-production validation for the patches that touch the crown jewels. **Maintenance windows** are scheduled and published — the business knows when systems will be touched, and the patch team knows when it may touch them. Deployment is **verified**, not assumed: the scanner re-checks, the asset shows the patch level, the exceptions are the only gaps — because "we pushed it" without verification is how the two-year-old flaw survives.

**Exceptions: the register, not the rumor.** Some systems can't be patched on schedule — the legacy control system, the medical device, the vendor-supported appliance where patching voids support. The operation doesn't pretend otherwise; it **registers** each exception: the system, the unpatched vulnerability, the reason, the compensating controls (segmentation, monitoring, the `e-detective-preventive` controls watching it harder), the owner, and the review date. Declining a patch doesn't delete the risk — it transfers it to the compensating controls, and the register is where that transfer is recorded and reviewed. The rule from `e-risk-assessment`, repeated here because it's violated here most: an exception without an owner and a review date is abandonment. The register is reviewed on cadence; exceptions that outlive their justification get re-decided, not renewed by inertia.

**Emergency patching: the runbook for the bad Friday.** When a KEV-listed vulnerability hits your stack — or active exploitation is reported against you — the routine cadence is too slow. The **emergency runbook** pre-decides: who can declare an emergency patch (named role), who approves the skipped testing (and what testing is *never* skipped — the runbook lists the minimum validation even in emergency), the communications (who gets told the system is going down *now*), and the rollback criteria (what observed breakage triggers revert, decided before the patch goes in). The runbook is exercised — a tabletop (a discussion-based exercise: the team walks through the scenario without touching production), at least annually — because the first emergency is the wrong time to discover the declaration authority is ambiguous (the `e-bcp-drp` lesson again).

### Worked example: Northgate Retail — the patching SLA policy

**The company (fictional).** Northgate Retail, 300 staff, 40 stores, e-commerce platform, POS terminals, warehouse systems. Today: patches applied "when the vendor's tech visits" for POS, "when someone has time" for servers. The KEV catalog is checked never.

**The SLA policy (excerpt, fictional — the company's own decisions).**

| Tier | Trigger | Timeline | Scope notes |
|---|---|---|---|
| Emergency | KEV-listed CVE affecting in-scope systems, or active exploitation reported | 24 hours to deploy or mitigate | testing reduced to the runbook minimum, never zero |
| Critical | CVSS ≥ 9.0 with public exploit, or internet-facing high | 7 days | staged rollout; crown jewels first |
| High | CVSS 7.0–8.9 | 30 days | regular maintenance windows |
| Routine | medium/low, no exploit | 90 days / next cycle | bundled with scheduled maintenance |

*Timelines are Northgate's decisions, not CISA's — the policy says so explicitly, with the rationale (POS terminals can't be touched during trading hours; the e-commerce platform can).*

**Testing and windows.** POS: vendor-managed, patched in the overnight window, verified by the morning health check. E-commerce: canary → 10% → full, with automated rollback on error-rate thresholds. Warehouse: monthly window, announced two weeks ahead.

**The exception register (excerpt, fictional).** Two entries: the warehouse management server (2008 OS, vendor out of business) — unpatchable, compensating controls: isolated VLAN, no internet, host IDS (an intrusion-detection agent running on the host itself), quarterly review, owner named; one POS terminal model awaiting vendor firmware — 90-day exception with the vendor ticket referenced. Everything else: no exception, no excuse.

**The emergency runbook (excerpt, fictional).** Declaration: the security lead (backup: the infrastructure lead). Minimum testing even in emergency: the canary deploy (rolling the patch to a tiny fraction of systems first and watching for breakage before the fleet) plus the smoke test (a quick check that the system's core functions still work) — listed, non-waivable. Communications: store managers notified before POS touches; e-commerce status page updated. Rollback: error-rate or transaction-failure thresholds, decided in the runbook, executed by the deployer without needing new approval. Exercised annually via tabletop — last year's exercise found the store-notification list was two years stale (fixed: quarterly refresh, owner named).

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the SLA policy, exception register, and emergency runbook above, authored and self-reviewed in-session on 2026-10-10 against SP 800-40 Rev. 4's program structure and the KEV catalog's prioritization model. Transcript: `runs/e-patch-management.log`.

1. **Inventory the patchable estate.** For your fictional (or real) organization: systems, owners, patch sources, current patch levels. The systems with no owner and the ones with no patch source are findings before you write a word of policy.
2. **Define the priority tiers.** KEV membership first, then exploitability/exposure, then severity, then asset criticality. Write the trigger event for each tier's clock (patch release? KEV listing? both?) — the clock's start is the part policies forget.
3. **Set the timelines as decisions.** Per tier: the deadline, the scope notes, the rationale. If a timeline can't be met with current staffing and windows, change the timeline or the resourcing — in writing.
4. **Design testing and windows.** Per system class: testing tier, rollout stages, maintenance windows, verification method. The verification step ("scanner re-checks, asset shows the patch level") is non-optional.
5. **Open the exception register.** Every unpatchable-or-delayed system gets a row: vulnerability, reason, compensating controls, owner, review date. No verbal exceptions survive this step.
6. **Write the emergency runbook.** Declaration authority, non-waivable minimum testing, communications, rollback criteria. Then exercise it — tabletop, annually at least — and record what the exercise found.

## 5. On your own

**Task:** Check the KEV catalog for any CVE affecting software you run. For each hit: is it patched in your environment? If not, write the exception-register row (or the patch plan with a date). Then check one system's actual patch level against what you believed it was.

**Success test:** You find at least one gap between believed and actual patch state — the inventory is always worse than memory says. Every unpatched KEV hit gets either a patch date or a register row with compensating controls. "I'll get to it" is neither.

## 6. Where it goes wrong

- **Everything is critical.** No prioritization — the hundred-patch month gets the same urgency as the quiet one, which means the exploited one waits behind the theoretical ones. The observable: the patch queue where a KEV item from March still sits behind forty routine items, all labeled the same priority. KEV-first is the tiebreaker that matters.
- **"Promptly."** The policy with no timelines. Deadlines are decisions; without them there's nothing to miss and nothing to escalate.
- **Patching without inventory.** The program that doesn't know what it has to patch. Step zero is the asset list — the two-year-old flaw lives on the forgotten system.
- **Testing theater or testing absence.** Either patches ship untested (and break things, teaching everyone to fear patching) or testing is so heavy nothing ships. Tiered testing matched to risk is the middle.
- **Deployment assumed.** "We pushed it" with no verification. The scanner re-check is part of the operation, not an audit afterthought — the tell: the change ticket says "deployed" but the scanner still lists the CVE on that asset. The re-scan is the independent witness.
- **Verbal exceptions.** "We can't patch that one" with no register, no compensating controls, no review date. The register turns folklore into decisions.
- **The untested runbook.** Emergency authority ambiguous, rollback criteria undecided, notification list stale — discovered during the actual emergency. Exercise it annually.
- **POS-hours patching.** Touching systems when the business can't tolerate it, because the windows were never negotiated. Maintenance windows are agreements, published in advance.

## 7. Read the source

Primary documents first:

- **NIST SP 800-40 Rev. 4, Guide to Enterprise Patch Management Planning** (csrc.nist.gov, April 2022) — *read* the program structure (inventory through verification); the unglamorous parts are the point.
- **CISA Known Exploited Vulnerabilities (KEV) catalog** (cisa.gov) — *use* it, don't just read about it: check your estate against it. Note the catalog's structure (CVE, vendor, product, required action, due date) — the due dates are the federal timelines; your SLA sets your own.

Then at most three free resources:

1. **CISA BOD 26-04, Prioritizing Security Updates Based on Risk** (cisa.gov, 2026) — free; the current federal model — it supersedes BOD 22-01 (revoked June 2026) and consolidates vulnerability-remediation guidance. Read for the prioritization logic, which applies beyond federal agencies.

## 8. Check yourself

1. A KEV-listed CVE with CVSS 7.5 affects your internet-facing VPN; a non-KEV CVE with CVSS 9.8 affects an isolated lab system. Using the prioritization order, explain which gets patched first and why — then explain what the SLA's trigger-event definition has to say for the clock to start correctly.
2. Explain why "we pushed the patch" is not a completed operation — what are the two verification steps, and which failure ("the two-year-old flaw") does each prevent?
3. A warehouse system can't be patched (vendor defunct). Design the exception-register row: what are the required fields, and what specifically makes the compensating controls adequate rather than decorative?
4. Distinguish routine patching from emergency patching as process designs: what does the emergency runbook pre-decide that the routine process decides per patch, and what testing is never skipped even in emergency?
5. Predict the exception register of an organization with only verbal exceptions, three years on: what do the entries look like, who owns them, and which incident reveals the register's absence?

## 9. Prove it

**Artifact:** your patching SLA policy (tiers, triggers, timelines with rationales), exception register (rows with compensating controls, owners, review dates), and emergency runbook (declaration, minimum testing, communications, rollback criteria) — for the Northgate worked case in your own words, or better, for an estate you actually run, with the KEV check against your own systems.

**Honest claim:** "I can run the patching operation — prioritize by exploited-in-the-wild over theoretical severity, set and meet timelines, register the exceptions honestly, and handle the emergency without improvising."
**Can't claim yet:** "I can secure unpatchable systems" — the compensating controls around legacy systems reduce risk; they don't eliminate it. The register is honest about that, and so is this claim.

## 10. Leads to

- `c-vuln-ecosystem` — the KEV/EPSS/CVE inputs this operation consumes; reread it as the feed, not the decision.
- `e-change-management` — routine patching flows through change control; the emergency path is its defined exception.
- `e-config-management` — patching changes the baseline; the drift checker should confirm the new state.
- Map refs: **CISSP 7.8** (this lesson); feeds **CISSP 7.9** (change management).

---

*Worked case authored and self-reviewed 2026-10-10; all scenario data fictional. Sources fetched in-session — see `runs/e-patch-management.log`. Factual note: BOD 22-01 was revoked June 2026 and superseded by BOD 26-04 — verified in-session against cisa.gov; the research spec's BOD 22-01 reference is corrected here.*
