---
lesson_id: c-log-sources
slug: log-sources
stage: C
level: 3
prerequisites: [a-linux-cli, a-tcpip-ports]
roles: [soc-analyst, security-analyst, dfir]
map_refs: []
test_date: 2026-10-09
description: "Log sources that matter: endpoint, network, identity, email, cloud — what each sees, what goes blind without it, and cross-source correlation. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · fictional sample logs parsed with CLI tools"
---
# Log Sources That Matter


---

## 1. Where this shows up

Triage told you *what to decide*; this lesson tells you *where to look*. Every investigation is a question aimed at a log source: "who logged in where" goes to identity logs, "what did the process do" goes to endpoint telemetry, "where did the bytes go" goes to the wire. Pick the wrong source and you stare at the right question with no data. This is the daily vocabulary of the SOC analyst and DFIR paths (`/r/soc-analyst/`, `/r/dfir/`), and it is what makes the difference between an analyst who queries and one who *knows where the answer lives*.

## 2. Before you start

- You parse text with the command line without thinking about it (`a-linux-cli`): `grep`, `awk`, `sort`, `uniq -c`.
- You know what a TCP connection looks like (`a-tcpip-ports`): 5-tuple, ports, what encryption hides and what it doesn't.
- Accept the premise you will use for the rest of your career: **one log source never tells the story.** Every conclusion in this lesson is cross-source.
- Vocabulary you will meet here: **telemetry** is the stream of events and measurements a system emits about its own operation — the raw material every detection and investigation is built from. A **SIEM** (security information and event management) is the platform that ingests logs from many sources so you can search and correlate them in one place — Wazuh, Splunk, and Microsoft Sentinel are examples.

## 3. How it works

NIST SP 800-92's framing still holds: log management is infrastructure — collect, store, analyze, dispose — and its hard problems are volume, immutability, inconsistent formats, review discipline, and retention. The defender's version is simpler. For each source: what it records, what question it answers, what goes blind without it.

**Endpoint — Windows Security log.** The native identity telemetry. The event IDs you must know cold: **4624** successful logon (check the Logon Type — 2 interactive, 3 network, 10 RDP, 11 cached), **4625** failed logon (brute force, spray), **4648** explicit-credential logon (RunAs, lateral movement), **4672** special privileges assigned (admin-level logon), **4688** process creation — but only with command lines if process-creation auditing is deliberately enabled (default off: Microsoft ships the "Include command line" policy as Not Configured, because logging every process launch on every machine costs real volume and performance — and the command lines land in the log in plain text, readable by anyone who can read the log. Windows makes the admin opt in.) **4720/4728/4732** account and group changes (rogue accounts, privilege escalation), **4768/4769/4771** Kerberos ticket traffic (ticket abuse), **1102** audit log cleared — anti-forensics, almost always hostile, **4104** PowerShell Script Block Logging — the de-obfuscated script content. Blind without it: identity. No 4624/4625 and "who logged in where" is unanswerable.

**Endpoint — Sysmon.** The kernel-driver telemetry that makes Windows actually observable. The IDs that matter: **1** ProcessCreate (full command line, parent, hashes), **3** NetworkConnect (process → IP:port — C2 attribution, where C2, command-and-control, is the attacker's remote server that the malware phones home to for instructions), **8** CreateRemoteThread (process injection), **10** ProcessAccess (LSASS access — credential dumping), **11** FileCreate (dropped payloads), **12/13** registry (Run-key persistence), **22** DNS query (per-process DNS — DGA, DNS C2), **23** FileDelete (anti-forensics). The industry starting config is SwiftOnSecurity's sysmon-config — broad includes, tuned excludes. Every exclude you write is a decision about what you will never see; config tuning *is* detection tuning at the source.

**Endpoint — EDR.** Adds what logs can't: live process trees, memory context, behavioral blocking, remote response (isolate, kill, quarantine). In triage terms, EDR answers "what is happening *right now* on this box" while logs answer "what happened." Free lab: Wazuh agents or Velociraptor.

**Network — firewall, proxy, DNS, IDS, flow.** The firewall records allowed/denied 5-tuples — the five values that identify one connection (source IP, source port, destination IP, destination port, protocol) — (what crossed boundaries). The proxy records full URLs per user (phishing clicks, downloads). DNS query logs record every name resolution (DGA, DNS tunneling, beaconing to rare domains). Suricata/Snort/Zeek give signature and protocol-anomaly detection — Zeek's conn/dns/http/ssl/files logs are the network equivalent of Sysmon. NetFlow/IPFIX records 5-tuple plus bytes, packets, and timing with no payload — and that is enough: **timing and volume survive encryption**, so beaconing intervals and exfil sizes are visible even when TLS hides everything else. Encryption hides the *content* of the conversation, not the *envelope*: packet sizes and send times are visible to anything on the path. Malware that checks in every 60 seconds can't hide its schedule — the rhythm is the signal. Blind without the wire: encrypted traffic is a black box and lateral movement is invisible.

**Identity — AD and Entra ID.** Domain controllers emit the 4624/4625/4768 stream; Entra ID sign-in logs add interactive vs. non-interactive type, device join state, IP geolocation, MFA result, conditional-access decisions, and anomaly detections. The impossible-travel triage runs entirely on this source. Blind without it: every identity attack is invisible.

**Email gateway.** Sender, recipients, subject, attachment hashes, URLs, verdicts. Answers "how did it get in" — the initial-access question for most intrusions.

**Cloud audit.** AWS CloudTrail records every API call — who (IAM principal), what action, on which resource, from which IP, with what result. Azure Activity Log covers control-plane operations. Blind without it: cloud control-plane attacks are invisible. Free lab: your own account's audit trail plus Prowler/ScoutSuite against your own account.

### Worked example: one intrusion, five sources

At 03:01, an external IP fails logons against six users on `DC-01` — eighteen 4625s in eighteen minutes (identity source). At 03:19, `t.nguyen` succeeds from that same IP (identity + the spray's payoff). At 03:21, `WS-4417` logs 4688: PowerShell with `-EncodedCommand`, and 4104 shows the de-obfuscated content (endpoint source). The DNS log shows `WS-4417` bursting queries for twelve nonsense domains (network source: DGA-shaped). The firewall shows twelve small, uniform outbound flows to one rare IP (network source: beacon-shaped). At 03:25, event 1102: the audit log is cleared on `WS-4417` (endpoint source: anti-forensics). No single source proves the intrusion. Together they are a timeline: spray → compromise → execution → C2 → cover-up. That is the whole lesson in one paragraph.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/c-log-sources.log`. Clean environment: stock Python 3.12.3 plus coreutils (`awk`, `grep`, `sort`), 2026-10-09. The logs are **fictional samples generated locally for teaching** — 62 security events, 42 DNS queries, 37 firewall flows, all invented values. They stand in for the Windows Event Logs, DNS logs, and firewall exports you would pull from a real environment or a home lab (Wazuh, Security Onion).

1. **Take the census.** `awk -F, 'NR>1{print $3}' security_events.csv | sort | uniq -c | sort -rn` — count events by ID. You see 41× 4624, 18× 4625, and single 4688/4104/1102s. The census is always step one: know what the source *saw* before you ask what it *means*.
2. **Find the spray.** Count 4625s by source IP: all 18 come from one IP, `203.0.113.99`. Eighteen failures, six users, eighteen minutes — that is the password-spray shape, not user error (user error clusters on one account).
3. **Check for the payoff.** List sprayed users, then check for any 4624 from the attacker IP: `t.nguyen` succeeded at 03:19. A spray with no success is reconnaissance; a spray *with* success is a compromise. Write both lists down — the delta between them is the incident.
4. **Read the endpoint tells.** The 4688 shows PowerShell `-EncodedCommand` under `t.nguyen` on `WS-4417`; 4104 gives the de-obfuscated content. Note the dependency: 4688 is only this useful because command-line auditing was enabled — on a default build, this field is empty and the lesson is "turn it on."
5. **Pivot to DNS.** Count queries per host: `WS-4417` asked for twelve distinct nonsense domains (`xq1000zv9q.example` …) while the clean host asked for one intranet name thirty times. Twelve rare domains from one host in minutes is the DGA shape.
6. **Pivot to the firewall.** Filter small flows: twelve uniform 210-byte outbound flows from `10.0.4.77` to one rare IP. Small, uniform, periodic — the beacon shape from the triage lesson, confirmed at a second source.
7. **Note the anti-forensics.** `grep ",1102,"` — the audit log was cleared at 03:25. 1102 is almost never benign; it also tells you the timeline *after* 03:25 is incomplete, which bounds what you can claim.
8. **Write the source map.** One page: for each of the five sources, what it contributed, what question it answered, and what would have been blind without it. Then add the blind-spot column: this environment had no proxy (no URLs), no EDR (no process tree), no email gateway (no initial-access vector) — name what you *couldn't* see.

No step above is marked "not run by us" — the census, the spray detection, the payoff check, the pivots, and the blind-spot analysis all ran against the labeled fictional samples.

## 5. On your own

**Task:** Add a Sysmon-style `sysmon.csv` sample of your own invention (20+ events: process creates with parents, two network connects, one registry Run-key write) describing a *different* intrusion story than the walkthrough's. Then answer, using only your new file plus the walkthrough's logs: which process is the initial execution, what is its parent (and why the parent matters), and which event is the persistence mechanism.

**Success test:** A one-page source map for your story naming the initial-access, execution, and persistence events by ID, plus one blind spot your invented sources leave (something you *cannot* answer from the logs you made).

## 6. Where it goes wrong

- **Treating absence as evidence.** "No 4625s" can mean no spray — or no log forwarding. Before concluding anything from a quiet source, verify the source is *healthy* (recent events, expected volume).
- **Logon Type blindness.** 4624 type 3 (network) from an external IP is lateral movement or spray-payoff; 4624 type 2 (interactive) at 3 AM is a human at a keyboard. Same ID, different meaning — read the fields, not just the ID.
- **Trusting the hostname.** DHCP reassignment and spoofing mean "WS-4417" is a label, not an identity. Correlate host with IP and time before you isolate the wrong machine.
- **Ignoring clock skew.** A timeline built from sources with unsynchronized clocks puts effect before cause. NTP health is an investigation prerequisite, not trivia.
- **Over-reading the DGA shape.** Twelve rare domains can also be a misconfigured app or a CDN's domain sharding. The shape is a hypothesis; the process behind it (from Sysmon 1/22) is the verdict.
- **Keeping logs you can't parse.** A source with no documented schema, no time format, and no retention policy is a write-only archive. If you can't query it under pressure, you don't have it.

## 7. Read the source

Primary documents first:

- **NIST SP 800-92, Guide to Computer Security Log Management** (doi.org/10.6028/NIST.SP.800-92) — *read* the infrastructure functions and the five challenges (volume, immutability, formats, review, retention); *note* the 2006 date and check the r1 draft status before citing anything newer.
- **MITRE ATT&CK Enterprise tactics** (attack.mitre.org/tactics/enterprise/) — *read* the 15 tactics; *note* v19.2 split Defense Evasion into **Stealth** (TA0005) and **Defense Impairment** (TA0112) — stale 14-tactic lists mislead. On first pass, read the tactic pages as a map and skip the hundreds of technique pages — come back to a technique page when a rule or alert names one.
- **SwiftOnSecurity sysmon-config** (github.com/SwiftOnSecurity/sysmon-config) — *read* the config itself as the industry's starting answer to "what should an endpoint record"; *study* how excludes are written, because each one is a visibility decision.

Then at most three free resources:

1. **Wazuh** (wazuh.com) — free XDR (extended detection and response: the product category that bundles endpoint, network, and identity telemetry into one console): agents plus manager plus dashboard; generates the endpoint and identity telemetry in this lesson against your own lab VMs.
2. **Security Onion** (securityonion.net) — free NSM distro: Zeek and Suricata sensors generating the network telemetry in this lesson.
3. **Velociraptor** (docs.velociraptor.app) — free endpoint collection and hunting; the tool for asking a fleet "which of you has seen this" during scoping.

## 8. Check yourself

1. Eighteen 4625s from one IP against six users, then one 4624 for one of those users from the same IP. Explain why the 4624 changes the incident classification — and what the eighteen 4625s alone would have been.
2. A 4688 event shows `powershell.exe` launched but the command-line field is empty. Explain what configuration is missing, why it defaults off, and what investigation question becomes unanswerable without it.
3. Name the two network sources that can reveal beaconing even when all traffic is TLS-encrypted, and explain *why* encryption doesn't hide what each of them sees.
4. Event 1102 appears on a host mid-timeline. Explain what it tells you about the attacker's behavior *and* what it tells you about the limits of your own timeline.
5. Your SIEM has no proxy logs and no EDR. An analyst asks "which user clicked the phishing link?" Explain why this question is unanswerable from your sources, which source would answer it, and how you would work around the gap today.

## 9. Prove it

**Artifact:** the source map from walkthrough step 8 plus your invented Sysmon story: per source, what it contributed, what it answered, and the blind-spot column naming what you couldn't see.

**Honest claim:** "Given a set of log sources, I can select the right source for each investigation question, parse it with CLI tools, correlate across sources into a timeline, and state what remains blind."
**Can't claim yet:** "I can design a logging architecture" — collection engineering, retention policy, and pipeline reliability are the detection-engineering discipline (`c-sigma-detection` and the D track).

## 10. Leads to

- `c-sigma-detection` — turn what the logs show into rules that fire on it: the detection side of every pattern in this lesson.
- `c-incident-response` — where correlated timelines go: the IR report is built from exactly this kind of cross-source work.
- `b-session-auth`, `b-command-injection`, `b-xss` — the attack lessons whose telemetry you just learned to read; revisit each "how defenders see it" section with source names attached.
- Map refs: **Stage C · Professional**; NICE **Protection and Defense**; the `/r/soc-analyst/` and `/r/dfir/` paths.
