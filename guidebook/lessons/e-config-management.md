---
lesson_id: e-config-management
slug: config-management
stage: E
level: 3
prerequisites: [a-linux-cli]
roles: []
map_refs: ["CISSP 7.3"]
test_date: 2026-10-10
description: "How to write a hardening baseline for a server role and operate drift detection against it — with a real local demo of the baseline-and-compare mechanism. A free lesson in the security guidebook, serving CISSP objective 7.3."
dateline: "Worked case authored and drift-demo run 2026-10-10 · local demo on fictional files, transcript in runs/e-config-management.log"
---
# Configuration management: baselines, hardening, and catching drift


**Map ref:** serves **CISSP objective 7.3** — configuration management: baselines, hardening, and controlling change to the trusted state.

---

## 1. Where this shows up

Every system ships in a default state optimized for working everywhere, which means optimized for security nowhere: unnecessary services running, default credentials set, verbose error messages on. Configuration management is the discipline that replaces defaults with decisions — a documented **baseline** (the approved secure state for a system role), **hardening** (the act of moving a system to that baseline), and **drift detection** (noticing when reality diverges from the document). It shows up in the breach that started with a debug interface left enabled, in the audit finding of forty-three "temporary" firewall rules, and in the 3 a.m. realization that nobody knows what the production config is *supposed* to be. System administrators, SOC engineers, and GRC analysts live here — and it is the daily-operations companion to `e-change-management`: a change that skips the change process is exactly the drift this lesson's checker finds.

## 2. Before you start

- You can read and change Linux configuration from `a-linux-cli` — the baseline is a set of decisions about those files and settings.
- The walkthrough runs a real drift-checker script locally against fictional demo files in `/tmp` — no system files are touched, no network, no special privileges. The transcript is in `runs/e-config-management.log`.
- Primary spine: **NIST SP 800-128** (Guide for Security-Focused Configuration Management of Information Systems, August 2011).

## 3. How it works

Configuration management answers a deceptively simple question: *what is this system supposed to look like?* Everything else is machinery for keeping the answer true.

**The baseline.** A baseline is the documented, approved secure configuration for a system **role** — not for an individual machine, but for "Linux web server," "Windows domain controller," "network switch." It lists every security-relevant setting and its required value: which services run, which are disabled, authentication settings, logging, file permissions, network posture. Two properties make it a baseline rather than a wish list: it is **versioned** (baseline v1.3, with a changelog — because the approved state changes and you must know what changed when), and it is **buildable** (a new system can be brought to the baseline mechanically, not by a senior admin's memory). SP 800-128 frames configuration management as the supporting discipline for the SP 800-53 configuration-management family: identify the configuration items, control changes to them, and account for their status. The baseline is the "identify" step made concrete.

**Hardening: getting to the baseline.** Hardening is the one-time (per system, then per change) work of moving a system from its default state to the baseline: remove or disable what's unneeded (every running service is attack surface and every default account is a credential to steal), configure what's left securely (authentication, logging, permissions), and verify. The industry's shared starting point is the **CIS Benchmarks** — community-developed, consensus-based secure-configuration guides for operating systems, applications, and cloud platforms, published as free PDF downloads by the Center for Internet Security. The expert move is not to apply a benchmark blindly: you take the benchmark, decide per recommendation (apply, adapt, or document an exception with rationale), and the result — benchmark plus your decisions — *is* your baseline. A benchmark applied without decisions is someone else's baseline; the exceptions document is where your organization's judgment lives.

**Drift: the baseline decays from the moment it's written.** Emergency fixes, troubleshooting changes, well-meaning admins, attackers — all move systems away from the baseline. **Drift detection** is the ongoing comparison of actual state against the documented baseline, and it closes the loop: without it, the baseline is a document and the systems are whatever they became. Detection ranges from the simple (hash the config files, compare to recorded hashes — the walkthrough below) to the continuous (agents reporting posture to a central console, cloud config rules evaluating every API change). The response to drift is a decision, not a reflex: investigate (was this an approved change that the baseline hasn't absorbed yet, or an unapproved one?), then either remediate the system back to baseline or update the baseline through the change process. Drift that turns out to be an approved-but-undocumented change is a change-management failure wearing a drift costume — which is why this lesson and `e-change-management` are taught as a pair.

**Baselines for the moving parts.** The 2011 vintage of SP 800-128 shows in its assumptions — it was written for servers you could name. The concepts transfer: for cloud, the baseline is the approved configuration of the account/landing zone expressed as policy (the drift checker becomes the config rule evaluating continuously); for containers, the baseline is the approved image definition (drift is a running container that differs from its image); for network devices, it's the approved device template. What doesn't transfer is the *method* of checking — which is why the lesson teaches the principle (documented approved state, mechanical comparison, decided response) rather than one tool.

### Worked example: Beacon Logistics — hardening baseline for the dispatch app server

**The company (fictional, continued from `e-bcp-drp`).** Beacon's dispatch system is the BIA's crown jewel. The server role: "Linux application server, dispatch role." Today: built from a generic image, configured by whoever deployed it, no two alike.

**The baseline (excerpt, fictional — decisions shown, not just values).**

| Setting | Baseline value | Source / rationale |
|---|---|---|
| SSH root login | `no` | CIS Benchmark; no break-glass need — console access exists |
| SSH password auth | `no` | keys only; the help-desk reset path must not bypass this |
| Unneeded services (telnet, ftp, rpc) | disabled | attack surface; nothing in the role needs them |
| Audit logging | enabled, forwarded to collector | `e-logging-monitoring` taxonomy requires it |
| File integrity baseline | recorded at build | drift detection input |
| Local firewall | deny-by-default, app ports only | documented port list in the baseline appendix |

**Exceptions (the judgment document):** one — the dispatch app requires an older TLS setting for a carrier integration; exception EX-2026-014, owner named, review date set, compensating control (the integration is on an isolated segment). An exception without an owner and a review date is just a hole.

**The drift scenario.** A month after hardening, the night-shift admin enables password SSH "temporarily" to troubleshoot from home, then forgets to revert. The weekly drift check flags `sshd_config` as diverged. Investigation finds no change record — unapproved change. Response: revert to baseline, and the admin's troubleshooting need becomes a proper change request for a VPN-based path (the `e-change-management` loop). The baseline didn't prevent the change; it made the change *visible*, which is what baselines are for.

## 4. Walkthrough

**Local demo — actually run.** The walkthrough implements the lesson's core mechanism: a documented baseline (recorded hashes of the role's config files) plus a compare step that reports drift. It runs against fictional demo files in `/tmp/baseline-demo/` — never real system files. **Run 2026-10-10; full transcript in `runs/e-config-management.log`.**

1. **Create the fictional role files.** Three demo config files stand in for the server role's governed settings (`sshd_config`, `sysctl.conf`, `sudoers.demo`) — each labeled fictional in its header. In production these would be the real files; the mechanism is identical.
2. **Record the baseline.** `python3 drift_demo.py init` writes each file and records its SHA-256 in `baseline.json`. The baseline file is the document — in production, versioned and change-controlled, not sitting in `/tmp`.
3. **Verify the clean state.** `python3 drift_demo.py check` compares current hashes to the baseline: `OK: no drift`. This is the weekly check passing.
4. **Introduce unauthorized drift.** Append `PermitRootLogin yes` to the demo `sshd_config` — the night-shift admin's "temporary" change, with no change record.
5. **Run the check again.** `python3 drift_demo.py check` reports `DRIFT DETECTED: sshd_config differs from baseline` and exits nonzero. The change is now visible.
6. **Decide, don't just revert.** The walkthrough's decision step: investigate (no change record → unapproved), revert the file, and route the underlying need through change management. The checker found the symptom; the process treats the cause.

**What the demo doesn't do (honest limits):** it checks file hashes, not semantic settings — a real checker parses values (is `PermitRootLogin` actually `no`?) and covers packages, services, and permissions. It has no central reporting, no scheduling, no baseline versioning. Those are the production gaps the artifact below must address in design, even though the demo doesn't implement them.

## 5. On your own

**Task:** Write a hardening baseline for a role you actually run — your homelab server, your VPS, your laptop's SSH config. Pick ten settings, record each with value and rationale (apply/adapt/exception), then check your real system against it and record the drift you find.

**Success test:** You find at least two divergences between your real system and the baseline you just wrote — including one you can't explain on sight. If your system matches perfectly, your baseline describes what is, not what should be; rewrite it from a CIS Benchmark instead of from memory.

## 6. Where it goes wrong

- **The undocumented build.** Every server hand-configured, no two alike. There is no baseline to drift from — the first step isn't a checker, it's writing down what one good system looks like.
- **Benchmark as baseline.** Applying CIS Benchmarks verbatim with no decisions and no exceptions document. The benchmark is the starting point; your decisions are the baseline.
- **Exceptions without owners.** The TLS exception with no review date becomes permanent. Every exception names an owner and a review date, or it's a hole with paperwork.
- **Drift detection without response.** The checker emails weekly; nobody reads it. Detection without a decided response (investigate → remediate or absorb via change) is monitoring theater.
- **The emergency change that never comes back.** "Temporary" changes are the most permanent kind. The drift check exists largely to catch these — and the change process must have an emergency path, or people will route around it (see `e-change-management`).
- **Checking hashes, thinking settings.** A file can match its hash and still be wrong if the baseline recorded a bad value. Baseline quality matters as much as check frequency — review what the baseline *says*, not just whether systems match it.
- **Baseline for the dead.** The baseline describes v2 of the app; production runs v3. Baselines decay too — version them, changelog them, review them on the same cadence as the systems they govern.

## 7. Read the source

Primary documents first:

- **NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems** (csrc.nist.gov, August 2011) — *read* the configuration-management process (identify, control, status-account) and the baseline concept; *note* the server-centric assumptions and translate the method to cloud/container/network yourself.
- **NIST SP 800-70 Rev. 4, National Checklist Program for IT Products** (csrc.nist.gov, February 2018) — *read* as the federal checklist repository: what a security configuration checklist contains and how it's structured.

Then at most three free resources:

1. **CIS Benchmarks** (cisecurity.org) — free PDF downloads; the consensus starting point for any server/application baseline. Pick your role's benchmark and practice the apply/adapt/exception decision per recommendation.
2. **NIST SP 800-53 Rev. 5, Configuration Management (CM) family** — the control catalog: CM-2 (baseline), CM-3 (change control), CM-6 (settings). Find it via the SP 800-53 publication page (csrc.nist.gov).

## 8. Check yourself

1. A drift checker reports `sshd_config` diverged; investigation finds an approved emergency change from last night that was never folded into the baseline. Is this a drift-detection success or a change-management failure? Explain what each process should do next.
2. Explain why "apply the CIS Benchmark verbatim" is not a baseline — what document is missing, and what goes wrong the first time an application needs a nonstandard setting?
3. A file's hash matches the baseline, but the setting it contains is insecure. Name the two distinct failures (one in baseline quality, one in checker design) and the review that catches each.
4. Distinguish hardening from drift detection: which one answers "what should this look like," which answers "does it still," and what breaks if you operate the second without the first?
5. Predict the state of a baseline document three years after its author leaves, with no versioning and no review cadence: which section rots first, and what incident reveals it?

## 9. Prove it

**Artifact:** your hardening baseline for a server role (settings with values, per-setting source/rationale, the exceptions document with owners and review dates), plus the drift-detection design (what's checked, how often, the investigate→remediate-or-absorb response) — for the Beacon worked case in your own words, or better, for a role you actually run, with the drift checker's output against your real system.

**Honest claim:** "I can define what a system role should look like, get it there, and notice when it leaves — I can write the baseline, make the apply/adapt/exception decisions, and operate the check that catches drift."
**Can't claim yet:** "I can run enterprise configuration management at scale" — fleet-wide enforcement, continuous compliance pipelines, and baseline governance across hundreds of roles are their own practice; this lesson taught the method on one role, which is where the judgment is formed.

## 10. Leads to

- `e-change-management` — the process that turns drift into either remediation or an updated baseline; taught as this lesson's pair.
- `e-logging-monitoring` — the baseline requires the logging the monitoring program consumes.
- `a-linux-cli` — the settings-level companion: what each baseline line actually does on the machine.
- Map refs: **CISSP 7.3** (this lesson); feeds **CISSP 7.9** (change management).

---

*Baseline authored and drift demo run 2026-10-10; all scenario data fictional. Sources fetched in-session — see `runs/e-config-management.log`.*
