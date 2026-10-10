---
lesson_id: d-redteam-concepts
slug: redteam-concepts
stage: D
level: 2
prerequisites: [a-http-depth, a-tcpip-ports, c-soc-triage, c-log-sources]
roles: [soc-analyst, security-analyst, pentester]
map_refs: []
test_date: 2026-10-09
description: "Red team operations concepts: ATT&CK as the behavior language (15 tactics, v19.2), C2 and evasion as concepts, what defenders see, and the purple-team loop — with beaconing statistics run locally. A free lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · synthetic data on loopback; emulation tooling is reader-side in their own lab"
---
# Red team operations: concepts


**Map refs:** **MITRE ATT&CK Enterprise v19.2** (tactic list verified 2026-10-09; 15 tactics — the April 2026 split of Defense Evasion into Stealth + Defense Impairment is taught, the stale 14-tactic list is not). Serves the Stage D red-team specialist track.

---

## 1. Where this shows up

A red team is hired to act like an adversary so the defenders can practice on something real. The job needs a shared language for "what the adversary did," and that language is MITRE ATT&CK. You will meet it in pentest reports, SOC detections, threat-intel write-ups, and every purple-team exercise. This lesson teaches the language and the concepts behind the operations — command and control, evasion, emulation, the purple-team loop — from the defender's side of the glass. The hands-on half (running emulations) happens in your own isolated lab with published tests, never here.

## 2. Before you start

- **Authorization:** nothing in this lesson touches a live system. The walkthrough runs on your own machine against synthetic data you generate. Running adversary-emulation tooling (Atomic Red Team, Caldera, Stratus) happens only in an isolated lab you own — lab VMs, host-only networking, snapshots taken first. Emulation tooling pointed at anything you don't own is not practice; it is an attack.
- You can read HTTP and TCP behavior cold (`a-http-depth`, `a-tcpip-ports`).
- You know what SOC triage and log sources look like (`c-soc-triage`, `c-log-sources`) — this lesson is the adversary's half of that picture.
- Tooling: Python 3 (stdlib only). A browser for the reader-side ATT&CK Navigator step.

## 3. How it works

### The behavior language: tactics, techniques, sub-techniques, procedures

ATT&CK answers one question: *what did the adversary do, in terms a defender can act on?* It is organized in four layers. A **tactic** is the adversary's goal — the "why" (e.g., steal credentials). A **technique** is how they achieve it — the "how" (e.g., OS credential dumping). A **sub-technique** is the specific variant (e.g., dumping from LSASS memory). A **procedure** is the concrete instance — the actual commands one intrusion used. The hierarchy matters because detections are written at the technique level (procedures change weekly; techniques persist for years), and because two intrusions that look nothing alike can share the same technique — which is exactly what makes the technique the right unit for detection.

The Enterprise matrix currently lists **15 tactics** (verified against attack.mitre.org 2026-10-09; ATT&CK releases biannually, so name the version when you cite it). In April 2026 the old Defense Evasion tactic was split in two, because hiding and breaking are different goals: **Stealth (TA0005)** — the adversary tries to hide and blend in; **Defense Impairment (TA0112)** — the adversary tries to break the security tooling itself so defenders can't see or trust what is happening. Any material still listing 14 tactics is stale — treat it as a signal about the material's age.

### Three jobs that get confused

A **penetration test** is a scoped, time-boxed assessment that finds as many vulnerabilities as possible and reports them — breadth first, usually announced. A **red team operation** is goal-directed: get the crown jewels (the domain admin hash, the customer database) the way a real adversary would — stealth first, often unannounced to the blue team. **Adversary emulation** is the middle discipline this lesson centers: you pick a known adversary's documented techniques and replay them, on purpose, to test whether your detections fire. Emulation is what makes red-teaming *scientific* — the same test, run the same way, should produce the same telemetry, and the gap between "should have fired" and "fired" is the finding.

### Command and control, as a concept

A compromised host needs a channel back to the operator: tasking in, results out. The channel must survive the network's normal filtering, so adversaries design C2 to look like traffic the network already allows. The core tension is *stealth versus reliability* — stealthier means less bandwidth and more fragility; more reliable means more visible. Every C2 design decision is a trade on this axis.

Most C2 is **beaconing**: the implant initiates outbound connections on a schedule (inbound is blocked by NAT and firewalls; outbound web traffic is allowed). A beacon has three observable properties: **periodicity** (roughly regular check-ins, often with jitter — randomized timing added specifically to defeat naive interval detection), **asymmetry** (small regular outbound requests, occasional larger inbound tasking or outbound exfiltration bursts), and **mimicry** (ordinary protocols, increasingly ordinary destinations). Beaconing detection is a *statistics* problem, not a signature problem: no single connection looks wrong; the pattern across time does.

The channel space, at concept level (ATT&CK technique IDs so you can look each up): **T1071** Application Layer Protocol — C2 inside HTTP/HTTPS, DNS, mail, the protocols the firewall already permits; **T1090** Proxy — relays between implant and operator, including multi-hop chains; **T1572** Protocol Tunneling — one protocol wrapped inside another; **T1573** Encrypted Channel — TLS defeats payload inspection, so defenders work on metadata; **T1102** Web Service — legitimate cloud storage or messaging as the medium, nearly unblockable by destination; **T1105** Ingress Tool Transfer — follow-on tooling downloaded over the channel; **T1568** Dynamic Resolution — fast-flux DNS (rapidly rotating the DNS answers so the domain resolves to new IPs constantly) and DGAs (domain generation algorithms: malware that invents new domain names on a schedule) — so the destination moves faster than blocklists. **Domain fronting** (T1090.004) is worth knowing as *history*: it abused CDN routing so traffic appeared to go to a reputable domain; the major CDNs closed the SNI/Host mismatch in 2018 and killed it. The lesson is the arms race — techniques die when platforms change — not a recipe.

### Evasion, as a concept

Every defensive control makes an assumption, and every evasion technique breaks one specific assumption. Signature matching assumes known bytes — **obfuscation (T1027)** breaks it. Process reputation assumes the binary's name tells you what it does — **living-off-the-land binaries (T1218)** and **masquerading (T1036)** break it. Forensic timelines assume timestamps are honest — **timestomping (T1070.006)** breaks it. Behavioral monitoring assumes code runs in its own process — **process injection (T1055)** breaks it. Monitoring assumes the sensors are intact — **defense impairment (T1562)** attacks the sensors themselves. The professional mental model: *for each evasion technique, name the defensive assumption it defeats.* That is what makes the technique understandable — and detectable, because the broken assumption leaves its own trace (the deobfuscation moment, the cross-process thread, the cleared log whose absence is evidence).

### What defenders see

C2 and evasion are detected through telemetry, never through the adversary's cooperation. Network: NetFlow/IPFIX and proxy logs show beaconing as regular intervals with low byte variance; DNS logs show DGA shapes (high NXDOMAIN rates, encoded-looking labels); TLS metadata shows JA3/JA4 fingerprints that don't match the claimed application. **JA3** (and its newer successor **JA4**) fingerprints the TLS *handshake*: it hashes the Client Hello's cipher list, extensions, and elliptic-curve parameters, identifying which software made the connection even though everything after the handshake is encrypted. Malware using a nonstandard TLS library stands out against a baseline of browser fingerprints — that mismatch is the signal. Endpoint: Sysmon Event ID 3 (network connection) matters less than *which process* opened it — a signed binary opening persistent HTTPS sessions from a temp path is the signal; Event ID 8 (remote thread creation) and Event ID 10 (cross-process memory access) are the injection tells; Event ID 1102 (log cleared) is itself the alert. Free tooling exists for exactly this: **RITA** runs beacon analysis over Zeek logs; **Sigma** rules encode the detections portably; a tuned Sysmon config is the telemetry foundation.

### The purple-team loop

Purple teaming is the loop that turns emulation into defense: select techniques → execute them in the lab (Atomic Red Team's published atomic tests, mapped to technique IDs) → measure (detected? blocked? alerted? how fast?) → report the gaps → fix the detection → re-run. Detection coverage is a living assessment, not a scoreboard. The loop only works if the execution is reproducible — the same atomic test, the same way, every time — which is why published emulation tests beat improvised ones.

### Worked example: naming the intrusion

Read this fictional incident the way an analyst does, and watch the story become a detection plan:

> A phishing email delivered a macro document. The macro launched PowerShell with an encoded command. PowerShell reached out to a cloud-storage URL every 60 seconds. A second-stage payload was downloaded, injected into explorer.exe, and began querying the domain controller. Event logs on the host were cleared.

In ATT&CK terms: Phishing T1566 → Execution via T1059.001 (PowerShell) → Obfuscation T1027.010 (encoded command) → C2 T1071.001 (web protocols) with T1102 (web service) → Ingress Tool Transfer T1105 → Process Injection T1055 → Discovery T1018 (remote system discovery) → Indicator Removal T1070.001 (log clearing, Event ID 1102). Each mapping is a detection assignment: 4104 script-block logging for the encoded command, proxy beacon analytics for the 60-second callback, Sysmon 8/10 for the injection, 1102 alerting for the log clearing. The story is the same; the language turns it into work items. That is what ATT&CK is for.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/d-redteam-concepts.log`. Clean environment: stock Python 3.12, loopback only, 2026-10-09. Everything below runs against synthetic data generated on the spot.

**Step 1 — Environment.** Confirm the interpreter and date:
```
python3 --version
date -u +%Y-%m-%d
```

**Step 2 — Map observations to tactics.** Write `tactic_mapper.py`: a keyword table mapping 8 fictional telemetry observations to ATT&CK tactics, printing a coverage table of which tactics the (fictional) sensor stack sees and which are blind:
```
python3 tactic_mapper.py
```
Expected: a table with 8 observations mapped (e.g., "powershell -enc" → Execution + Stealth; "hourly POST to rare domain" → Command and Control), plus a blind-tactic list — the start of a detection-gap memo.

**Step 3 — See beaconing statistically.** Write `beacon_stats.py`: generate two synthetic inter-arrival series — a beacon at 60s ±10% jitter, and human browsing (random 20–600s) — then compute mean, standard deviation, and coefficient of variation (stddev/mean) for each:
```
python3 beacon_stats.py
```
Expected: the beacon's CV near 0.1 (regular), the human's CV near 1.0 (irregular). The number *is* the detection concept: regularity, not content.

**Step 4 — Build a Navigator layer.** Write `layer.json`: an ATT&CK Navigator layer (v4.5 format) annotating 5 techniques from the worked example with scores and comments naming the data source that would detect each. Validate it parses:
```
python3 -c "import json; d=json.load(open('layer.json')); print('valid JSON,', len(d['techniques']), 'techniques')"
```
Expected: `valid JSON, 5 techniques`. Importing it into the ATT&CK Navigator (your browser, mitre-attack.github.io/attack-navigator) is reader-side — **not run by us** here.

**Step 5 — Emulation tooling (reader-side).** Atomic Red Team (github.com/redcanaryco/atomic-red-team — public, MIT-licensed, verified 2026-10-09) publishes small YAML-defined tests mapped to technique IDs. In your isolated lab: pick three *discovery*-family atomics (T1082 system information, T1018 remote discovery, T1033 system owner), run each, and record which of your defenses logged it. Running these here is **not run by us** — this machine is not an isolated lab, and emulation tooling never runs on shared infrastructure.

**Step 6 — Close the loop on paper.** Take the blind-tactic list from step 2 and write one paragraph per blind tactic: what telemetry would close it, and which existing log source from `c-log-sources` provides it. This is the purple-team memo in miniature.

## 5. On your own

Take the worked example's intrusion and extend it: add three more adversary actions (one persistence, one credential-access, one exfiltration), map each to its ATT&CK technique ID, and write the detection assignment for each as in the example. Success test: a second reader can take your mapping, look at the technique's ATT&CK detection section, and confirm your assignment names a real data source — no hand-waving.

## 6. Where it goes wrong

- **Tactic-name drift.** The 14-tactic list is everywhere in older material. If your source says "Defense Evasion" as a single tactic, it predates April 2026 — update your mental model, don't argue with the page.
- **Technique vs procedure confusion.** A detection written against one procedure ("alert on this exact PowerShell one-liner") dies with the procedure. Detections belong at the technique level; procedures belong in hunt notes.
- **Beaconing false positives.** Software updaters, NTP (Network Time Protocol — the service that keeps clocks in sync, which phones home on a schedule), and keepalives all beacon. Regularity alone is a candidate, not a verdict — the walkthrough's CV number needs the context of *which process* and *which destination* before it becomes a finding.
- **Emulation without a lab.** Running atomic tests on a production-adjacent machine "because it's just a test" is how people get fired or charged. The lab boundary is the whole discipline.
- **Coverage theater.** A Navigator layer with every technique colored green and no re-run dates is a painting, not an assessment. Coverage expires the day the environment changes.

## 7. Read the source

Primary, in this order:
1. **MITRE ATT&CK Enterprise tactics** (attack.mitre.org/tactics/enterprise/) — read the 15 tactic definitions first; they are the table of contents. Then read the **Command and Control tactic page** end to end, techniques then the detection/mitigation notes.
2. **Atomic Red Team repository** (github.com/redcanaryco/atomic-red-team) — read the README's philosophy section, then open one atomic's YAML to see how a test maps to a technique ID. Skip the execution-engine setup docs until you are in the lab.
3. **ATT&CK Navigator** (mitre-attack.github.io/attack-navigator) — open it, load the layer file from the walkthrough, and read how scores and comments render.

Free resources for going deeper (at most three):
- **RITA** (Real Intelligence Threat Analytics) — beacon analysis over Zeek logs; the free tool that implements the walkthrough's step 3 at production scale. *For: turning the statistics concept into real detections.*
- **LOLBAS** (lolbas-project.github.io) — the defender's catalog of living-off-the-land binaries, each with legitimate vs abusive uses. *For: the T1218 reference you will actually query.*
- **MITRE Caldera** (github.com/mitre/caldera) — agent-based planned adversary emulation for the isolated lab, when atomic tests stop being enough. *For: the next step after Atomic Red Team.*

## 8. Check yourself

1. An intrusion uses DNS queries to exfiltrate data. Which tactic is the goal, which technique family is the channel, and why is this harder to detect than the same exfiltration over HTTPS to a new domain?
2. A colleague proposes detecting T1059.001 by alerting on any PowerShell execution. Explain, using the technique/procedure distinction, why this rule will fail in both directions.
3. The walkthrough's beacon had 10% jitter and CV ≈ 0.1. An adversary switches to 50% jitter. Does the CV rise or fall, and what does the defender lose and keep?
4. Your Navigator layer shows green across Execution but red across Stealth. A manager asks "are we covered?" — what is the honest answer, and what single sentence explains why green-on-Execution is not enough?
5. Two vendors both claim "ATT&CK coverage." One maps product features to tactics, the other to techniques with named data sources. Which claim can you verify, and how?

## 9. Prove it

**Artifact:** the Navigator layer file from the walkthrough plus a one-page detection-gap memo: the blind tactics, the telemetry that would close each, and the log source that provides it — written so a SOC lead could hand it to an engineer.

**You can honestly claim:** you can name adversary behavior in ATT&CK terms, map observations to tactics and techniques, describe what telemetry each technique should produce, and explain the purple-team loop. **You cannot yet claim:** you can run emulations or write production detections — those need the isolated-lab work (Atomic Red Team, your own Sysmon/Sigma stack), which this lesson points at but does not perform.

## 10. Leads to

- `d-malware-analysis` — the payload side: what the implant *is*, statically and dynamically.
- `c-sigma-detection` — writing the detections this lesson assigns (you already know Sigma; now you know what to aim it at).
- Stage E governance — the ROE and authorization half of red teaming, taught as policy.
- Map: ATT&CK Enterprise v19.2 tactic list (verified 2026-10-09); the Stage D red-team track continues with reader-side Atomic Red Team work in the isolated lab.
