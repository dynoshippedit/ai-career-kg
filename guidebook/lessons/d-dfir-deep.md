---
lesson_id: d-dfir-deep
slug: dfir-deep
stage: D
level: 3
prerequisites: [c-incident-response, c-log-sources, a-linux-cli, d-malware-analysis, d-redteam-concepts, a-python-security]
roles: [soc-analyst, security-analyst, dfir]
map_refs: []
test_date: 2026-10-09
description: "DFIR deep: disk, memory and network forensics — the order of volatility, evidence handling, timeline construction from labeled data, and hypothesis-driven threat hunting. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · labeled synthetic evidence; tool runs on real images are reader-side in their own lab"
---
# DFIR deep: disk, memory, network forensics


**Map refs:** serves the Stage D DFIR specialist track; feeds detection engineering (`c-sigma-detection`).

---

## 1. Where this shows up

Triage ends with a decision: close it, or escalate it. Everything in this lesson is the escalation side — the work that begins when an alert becomes an incident and someone has to answer, with evidence, *what happened on this machine*. That someone might be an internal incident responder, a consultant called in after a breach, or a SOC analyst who pulled the thread far enough that the ticket became a case. The three questions are always the same: what did the attacker do, what did they touch, and how do we know. Forensics is the discipline of answering those questions without destroying the answers in the process.

The three evidence domains divide by where the traces live. **Disk forensics** reads what the filesystem remembers: files, metadata, logs, and the operating system's own record-keeping. **Memory forensics** reads what was true while the machine was running: processes, connections, injected code, credentials that never touch disk. **Network forensics** reads what moved between machines: packet captures, flow records, DNS logs. Each domain has tools, each has blind spots, and the professional read is knowing which domain answers the question in front of you — and what to do when the answer you need lives in a domain you haven't collected.

## 2. Before you start

- **Authorization and safety:** forensic analysis in this lesson is performed exclusively on labeled synthetic data you generate yourself, and on your own machine's own logs. Real forensic work happens on *copies* — you never analyze the original evidence, and you never run a suspect artifact on a machine you care about. The write-blocker concept below exists precisely because investigators learned this the expensive way.
- You know the incident lifecycle (`c-incident-response`): forensics is the investigation phase, and its output feeds containment, eradication, and the post-incident report.
- You can read logs and sort timelines (`c-log-sources`, `a-linux-cli`).
- You know what an implant looks like when you find one (`d-malware-analysis`) — forensics is how you find where it has been.
- You know the adversary's half of the artifacts: beaconing and the ATT&CK behavior language (`d-redteam-concepts`) — hunts are written in that language.
- You can write small Python scripts (`a-python-security`) — the walkthrough generates its labeled evidence with one.
- Tooling: a shell, `sort`, `awk`, `grep`, Python 3 — the walkthrough generates its labeled evidence with a Python script and builds timelines with coreutils.

## 3. How it works

### The order of volatility and why copies come first

Digital evidence decays in a known order, from most to least volatile: CPU registers and cache, RAM, network state, running processes, then disk, then backups and archives. You collect in that order because you can only lose what you never captured — reboot a machine and the memory evidence is gone forever, while the disk largely survives. This is why incident playbooks say *do not reboot the suspect machine* until memory is captured.

And the first rule of handling what you collect: **analyze the copy, never the original.** A forensic image is a bit-for-bit duplicate of the storage, hashed at acquisition time (SHA-256), with the hash recorded. The hash is what binds the analysis to the evidence: any later alteration changes the hash, so a verified hash proves the copy you examined is the copy that was collected. Every later claim — "this file existed at this time" — traces back to that hash, which is why the acquisition hash anchors the **chain of custody** (the documented, unbroken record of who handled each piece of evidence, when, and what they did). Hardware write blockers enforce the discipline physically: they sit between the analyst's machine and the evidence drive and refuse all write commands at the bus level. The concept survives even when you work on copies: the copy is sacred, the working analysis happens on a second copy, and anything that modifies the evidence modifies your credibility.

### Disk forensics: what the filesystem remembers

A file is not just its contents. Every file carries metadata — creation, modification, access times — and the operating system keeps journals of what happened to files independently of the files themselves. The artifacts that matter most on Windows: the **MFT** (Master File Table — every file's record, including deleted ones whose records haven't been reused yet), the **USN journal** (a running log of file changes), **prefetch** (records of programs executed, with run counts and last-run times), **event logs** (authentication, service installs, the 1102 anti-forensics tell), **registry hives** (persistence locations — Run keys, services), **LNK files** (shortcuts that remember where a file lived and when it was opened), and **browser history**. The professional read is not "check each artifact" but "reconstruct the sequence": prefetch says the program ran at 02:14, the USN journal says a file was created at 02:15, the registry says a Run key appeared at 02:16 — that is a timeline, and timelines are what turn artifacts into a story.

### Memory forensics: what was true while it ran

Disk shows what persisted. Memory shows what *happened*. Processes, their network connections, injected code, credentials in cleartext — much of it never touches disk, by design (fileless techniques exist precisely to defeat disk forensics). The standard workflow, taught against the Volatility framework, runs in an order: **image info** (what profile/OS this dump is), **pslist** (every process — compare against what *should* be running; the process that doesn't belong is the lead), **netscan** (which process holds which connection — the process-to-network binding disk forensics can't give you), **malfind** (memory regions that are executable but not backed by a file on disk — the classic injected-code tell). Each step narrows the search: list everything, bind processes to network, then look for the thing hiding from the list. The worked example below follows exactly this narrowing.

### Network forensics: what moved

Packets are the one record neither endpoint fully controls. **Full packet capture** (PCAP) is the richest and the most expensive — it sees payloads, which is why retention is usually short and why it is also the most sensitive to handle. **Zeek logs** (formerly Bro) are the professional compromise: connection summaries, DNS logs, HTTP logs, file hashes seen on the wire — structured, queryable, and small enough to keep for months. **NetFlow/IPFIX** records are the coarsest: who talked to whom, when, how much — enough to see beaconing (the regular timing from `d-redteam-concepts`) and exfiltration (the volume spike) without any payload at all. The three nest: NetFlow finds the *interesting* conversation, Zeek describes it, PCAP proves it. The discipline from the log-sources lesson applies: DNS logs catch the DGA-shaped burst (DGA: domain generation algorithm — malware that invents new domain names on a schedule, so blocking one domain never works), firewall flows catch the beacon shape, and the absence of a log where you expect one is itself a finding (the 1102 problem, at network scale).

### Threat hunting: hypothesis before data

Alerting asks "did something bad happen?" Hunting asks "if the adversary did X, what would it look like in data source Y?" — and then goes looking. The hypothesis comes first, always: an untested hypothesis is a fishing expedition, and fishing expeditions produce false positives that burn the team's credibility. A hunt hypothesis has three parts: the **technique** (from ATT&CK — the behavior language from `d-redteam-concepts`), the **expected evidence** (what the technique must leave in which data source — it cannot *not* leave it), and the **scope** (which systems, which time window). You run the hypothesis against telemetry, document what you found *and what you didn't* — a negative result is a result, and it tells you where your visibility is blind. The hunts that find something become detections: the hypothesis, hardened with thresholds and tested against benign data, graduates into a Sigma rule (`c-sigma-detection`). That pipeline — hypothesis → hunt → detection — is the whole detection-engineering loop, and forensics is what you do when the loop fires.

**Worked mini-example: the hunt becomes a rule.** Take the worked example's beaconing hunt — technique T1071.001, expected evidence: an internal host opening HTTPS to a rare external domain about every 60 seconds. The Sigma draft it graduates into (the *shape* is taught fully in `c-sigma-detection`; this is the graduation step, not the whole course — treat the rule text below as an illustrative sketch):

```yaml
title: Possible C2 Beaconing - Regular HTTPS to Rare Domain
status: experimental
description: Flags hosts with highly regular outbound HTTPS to domains first seen in the last 7 days.
logsource:
    category: proxy
detection:
    selection:
        cs-method: 'CONNECT'
    timeframe: 1h
    condition: selection | count() by src_ip > 50
level: medium
```

The translation discipline is the lesson: the hypothesis's *expected evidence* becomes the `logsource` plus `selection`; the *scope* becomes the timeframe; the *threshold* (50/hour, tuned against benign proxy data until the SOC stops drowning) is what separates a detection from a guess. A rule without the hunt behind it is YAML-shaped guessing — which is why the pipeline runs hunt first, rule second, and why the rule carries the hunt's technique ID in its references when you write the real one.

### Worked example: the narrowing, end to end

A fictional workstation, WS-4417 — the same machine the incident-response lesson's worked case investigated. The alert said beaconing; forensics answers what happened.

**Disk:** prefetch shows `updater-svc.exe` ran 214 times with a last run at 02:14 — a "service" with a userland name and a 2 AM schedule. The USN journal shows `C:\Users\j.chen\AppData\Roaming\updater-svc.exe` created at 02:11. A Run key points at it. Three artifacts, one sequence: dropped at 02:11, first ran at 02:14, persisted via the registry.

**Memory:** pslist shows `updater-svc.exe` as PID 4412 with a parent of `explorer.exe` — services don't spawn from Explorer. Netscan binds PID 4412 to a connection to an external IP on port 443, every 60 seconds. Malfind flags an executable region in that process not backed by any file — injected code. The process is lying about what it is, and memory proves it.

**Network:** Zeek's connection log shows the 60-second rhythm from this host going back nine days — the beaconing the SOC lesson's decision tree escalated. DNS logs show no DGA burst (the C2 used a single domain — a finding about the *adversary's* tradecraft, not just ours). NetFlow shows 4.2 MB outbound in the last hour against a 60-second baseline — the exfiltration window, and the clock for scoping what left.

Each domain confirmed the others and added what the others couldn't see. That is the professional standard: no single artifact carries the conclusion; the conclusion is the point where independent domains agree.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/d-dfir-deep.log`. Clean environment: stock Python 3.12 and coreutils, 2026-10-09. All evidence below is synthetic and labeled — generated for this exercise, describing a fictional intrusion on a fictional host. No real system was analyzed.

The walkthrough builds the core forensic skill — timeline construction — from three labeled evidence files: a synthetic auth log, a synthetic web-access log, and a synthetic "artifact list" standing in for disk findings. Steps: (1) generate the labeled evidence; (2) normalize all three to a common timeline format (timestamp, source, event); (3) merge and sort into a single super-timeline; (4) read the timeline as a sequence and write the three-sentence story it tells; (5) extract IOCs (IPs, usernames, file paths) into a findings list; (6) hash the evidence files and record the hashes as the chain-of-custody anchor; (7) write the findings memo — what happened, what was touched, how we know, and the honest limits (what the labeled data cannot prove).

## 5. On your own

Build the same pipeline against a second labeled evidence set you generate yourself — different attack shape (this time make it a credential-spray followed by a data-staging event, not a beacon). Produce the merged timeline, the IOC list, and the findings memo. Success test (alone — no stranger needed): put the timeline away and read only your memo. Write down, from the memo alone: the attacker's sequence, the compromised account, and the staging/exfiltration window. Then open the timeline and check each of the three against cited timeline lines — every claim in the memo must carry its line reference, and any claim without one fails the test. Three claims, three citations, zero uncited assertions. Then, in your own lab: install SIFT Workstation or Autopsy, load a published training image (HTB Sherlocks — Hack The Box's DFIR challenge series, realistic incident scenarios for practice — or a SANS challenge), and build a real timeline with a real tool — the walkthrough taught you what the tool is *for*.

## 6. Where it goes wrong

- **Analyzing the original.** Opening the suspect drive read-write, booting the suspect machine "to take a look," running the sample on the analyst workstation. Every one of these modifies the evidence and ends the investigation's credibility. Copies first, always.
- **No hash, no chain.** An image without a recorded acquisition hash is a story, not evidence. Hash at acquisition, re-verify before analysis, and record both.
- **Timeline timezone errors.** UTC vs local vs the attacker's timezone — a timeline built in mixed timezones convicts the wrong sequence. Normalize everything to UTC at ingest and say so.
- **Single-artifact conclusions.** Prefetch says the program ran; it does not say it was malicious. The conclusion lives where independent domains agree — the worked example's standard.
- **Confirmation bias.** Deciding it is ransomware in the first hour and then only collecting ransomware evidence. The hypothesis discipline from threat hunting applies to investigations too: write down what would *disprove* your theory and go look for it.
- **Destroying evidence by investigating.** The classic: the responder logs into the compromised machine with the domain admin account to "check something" — creating new logons, new artifacts, new confusion, and handing the attacker fresh credentials. Read-only, from copies, or not at all.

## 7. Read the source

Read the primary material in this order — each entry says what to read and what to skip:

1. **NIST SP 800-86, Guide to Integrating Forensic Techniques into Incident Response** (csrc.nist.gov) — read chapters 1–3 for the forensic process model and the collection/handling discipline; skim the tool catalog (it ages, the process doesn't). This is the process spine this lesson follows.
2. **Volatility 3 documentation** (volatilityfoundation.org) — read the plugin workflow pages (imageinfo → pslist → netscan → malfind); skip API internals until you write plugins. The command sequence is the memory-forensics lesson in miniature.
3. **SANS SIFT Workstation documentation** (sans.org/tools/sift-workstation) — read the tool list and what each tool answers; this is your lab shopping list, organized by evidence domain.

Then at most three free resources, each genuinely free: **Autopsy** (free, open-source disk forensics — your first real tool), **Eric Zimmerman's tools** (free Windows artifact parsers — the MFT/USN/prefetch readers), **Wireshark** (free — the network domain's microscope, from `a-tcpip-ports` onward).

## 8. Check yourself

Answer in your own words — no peeking at section 3:

1. A responder reboots the suspect workstation "to see if the alert clears" before anyone captures memory. Name the two things destroyed and explain, using the order of volatility, why disk imaging afterward cannot recover them.
2. Prefetch shows `invoice-tool.exe` ran 40 times. Explain why this is *not* by itself evidence of malice, and name two other artifacts whose agreement would change your assessment.
3. In the Volatility workflow, what question does `netscan` answer that `pslist` cannot — and why does that make it the step that catches the liar process?
4. Zeek logs show a host beaconing every 60 seconds to one domain; NetFlow shows 4.2 MB outbound in the last hour against that baseline. Explain which of the three network evidence tiers (PCAP / Zeek / NetFlow) found each fact, and what PCAP would add that the other two cannot.
5. Write a one-paragraph hunt hypothesis for credential dumping (ATT&CK T1003): the technique, the expected evidence in a specific data source, and the scope. Then state what a negative result would tell you.

## 9. Prove it

**Artifact:** the merged super-timeline, the IOC list, and the findings memo for your §5 case — the evidence set *you* generated, the attack shape *you* chose — committed to your evidence repo with the acquisition hashes recorded. The walkthrough's beacon case stays in the log; the artifact proves you can build the timeline on evidence the lesson didn't hand you.

**Honest claim:** "I can take labeled multi-source evidence, normalize it to UTC, build a merged timeline, and write a findings memo where every claim points at timeline lines." **What you cannot claim:** court-ready forensic expertise, tool certifications, or that you can attribute an intrusion to an actor — timeline construction is the foundation skill, not the profession. The profession adds real tools on real images (your lab), chain-of-custody procedure, and report writing under review.

## 10. Leads to

- `d-malware-analysis` — the sample the timeline points at: what it does, statically and dynamically.
- `c-sigma-detection` — the hunt that found something becomes the rule that fires next time.
- `c-incident-response` — the findings memo becomes the investigation section of the IR report.
- `d-redteam-concepts` — read the adversary's side of the artifacts: what each of your findings looked like from the operator's seat, and which of them they tried to prevent.

---

*Walkthrough transcript: `runs/d-dfir-deep.log` · Evidence in this lesson is synthetic and labeled unless a step says otherwise.*
