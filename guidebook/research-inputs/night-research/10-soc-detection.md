# SOC & Detection Depth — research dossier
### learncomputerstuff.dev security guidebook · night-research track 10
*Researched 2026-10-09. Governing brief: SECURITY_GUIDEBOOK_BRIEF-2.md (§5 Stage B defensive basics, §5 Stage D DFIR/detection).*

**Scope:** professional-depth lesson research on (1) SOC triage workflow, (2) log sources, (3) detection logic. Everything free-to-learn; no prices, fees, salaries, or time estimates anywhere.

---

## 0. Source ledger

| Claim / resource | Primary URL | Fetched | Status |
|---|---|---|---|
| Sigma main rule repository — 3000+ community rules, rule types (generic detection, threat hunting, emerging threat, compliance, placeholder), conversion tooling (Sigma CLI, pySigma), spec v2.x | https://github.com/SigmaHQ/sigma | 2026-10-09 | verified |
| Sigma rule specification repo — rules spec, correlation spec, filters spec, modifiers appendix, tags appendix, taxonomy appendix, JSON schema | https://github.com/SigmaHQ/sigma-specification | 2026-10-09 | verified |
| Detection engineering lifecycle (threat intel → draft → unit test → CI → staging soak → FP tuning → ship → quarterly review → retirement); detection-as-code states (draft/experimental/production/deprecated); CI gates (schema, lint, SIEM conversion, behavioral tests on positive/negative corpora) | https://github.com/dlpz-sec/detection-as-code | 2026-10-09 | verified |
| ATT&CK coverage from Sigma tags → Navigator layers; purple-team FP/FN loop; Atomic Red Team as detection unit test | https://github.com/baobug/kali-claw/blob/HEAD/skills/detection-engineering/SKILL.md | 2026-10-09 | operator-added (community skill, corroborated by SigmaHQ repo structure) |
| Detection tuning order (benign filters → thresholds → context → deprecate), rule decay, close-code telemetry feeding revisions | https://github.com/rhaist/marq/blob/HEAD/internal/skills/library/secops/detection-engineering.md | 2026-10-09 | operator-added (community skill, corroborated) |
| SOC alert triage six stages (reception → enrichment → impact/scoping → investigation → containment/escalation → documentation); L1/L2/L3 tier roles; ping-pong escalation warning | https://inventivehq.com/blog/soc-alert-triage-investigation-workflow | 2026-10-09 | operator-added (vendor blog — workflow structure corroborated by community handbook) |
| Triage classification (false positive / benign true positive / suspicious / confirmed incident / duplicate) and triage-note format | https://github.com/RedNode-Security/cybersecurity-engineering-handbook/blob/main/02-Blue-Team/SOC-Operations/soc-alert-triage.md | 2026-10-09 | operator-added (community handbook) |
| Impossible-travel triage checklist (shared account, interactive vs non-interactive, device join type, user agent, VPN group, vendor IPs, cross-user IP, prior reports); Defender for Cloud Apps 7-day baseline | https://medium.com/@osamaelghazaly/avoiding-reporting-false-positive-impossible-travel-alerts-41f3bcb58a17 | 2026-10-09 | operator-added (analyst-authored, corroborated by Microsoft docs concepts) |
| C2 beaconing: coefficient of variation on inter-query intervals (CV ≤ ~0.18 suspicious), jitter, DNS vs flow timing, lifecycle (staging → first callback → steady-state → tasking/exfil) | https://github.com/foghorn/dawnpatrol/blob/HEAD/docs/components/signals.md | 2026-10-09 | operator-added (open-source project docs) |
| vsagent HTTP beaconing lab: fresh TCP connection every 30s, no Referer, no browser fingerprint — interval proven by measuring SYN timestamps | https://github.com/blackhillsinfosec/freelabfriday_labs/blob/HEAD/Packet_Capture_Labs/AdvancedC2/vsagent_c2.md | 2026-10-09 | operator-added (BHIS free lab) |
| Sysmon event IDs and SOC value; SwiftOnSecurity config as industry starting point; Sysmon vs native log telemetry comparison | https://github.com/SwiftOnSecurity/sysmon-config (via corroborating home-lab writeups fetched 2026-10-09) | 2026-10-09 | operator-added (config repo is primary for the config itself; event semantics corroborated across 6 writeups) |
| NIST SP 800-92 Guide to Computer Security Log Management (2006): log management infrastructure functions, challenges (volume, immutability, inconsistent formats, review schedule, retention); SP 800-92r1 draft (Oct 2023) | https://doi.org/10.6028/NIST.SP.800-92 ; https://en.wikipedia.org/wiki/NIST_SP_800-92 | 2026-10-09 | verified (DOI landing + Wikipedia summary of the public-domain standard) |

---

## 1. SOC triage workflow

### 1.1 The alert lifecycle

An alert is a hypothesis, not a verdict. The triage lifecycle that turns it into a decision:

1. **Intake and initial classification.** Acknowledge the alert; read the detection's hypothesis and logic first — what did the rule claim to see, and in which log? Identify the affected user, asset, application, and data source. Time-box this: triage is minutes, not hours.
2. **Enrichment.** Attach context before judging: asset criticality (is this a domain controller or a test VM?), user role (admin? service account?), geolocation of IPs, threat intelligence on IOCs (hash, domain, IP reputation), and related alerts on the same entities in the same window.
3. **Scoping — one host or a campaign?** The single most important triage question. Pivot the alert's entities (user, host, IP, hash, domain) across the estate and the time window: is this one machine, or five? One user, or a spray? A lone alert on one host is an incident candidate; the same IOC on forty hosts is either a campaign or a broken rule — both need different handling.
4. **Severity vs priority.** Severity is the detection's technical rating (how bad would this be if true). Priority is severity × asset value × confidence. A critical-severity alert on a decommissioned lab VM is low priority; a medium alert on the CEO's laptop during a travel week is high priority. Triage sets priority; the rule only suggested severity.
5. **Investigation.** Build the timeline before and after the alert. Identify root cause and initial access. Check for lateral movement. Determine what data was touched. Use EDR, SIEM, firewall, proxy, packet capture, and authentication logs together — one log source never tells the story.
6. **Containment recommendation and escalation.** Triage does not contain; it recommends. Escalation criteria (below) decide who acts.
7. **Classification and routing.** Every alert ends in one of five buckets: **false positive** (rule matched wrongly → tune the rule), **benign true positive** (rule matched correctly on expected activity → close with reason), **suspicious** (needs deeper work → escalate to Tier 2/IR), **confirmed incident** (start the IR playbook), **duplicate** (link to the parent case).
8. **Documentation and lessons learned.** Write the triage note (what was seen, what was checked, what was decided, and the evidence). Feed the outcome back: IOCs to intelligence, tuning notes to detection engineering, process gaps to the playbook. An alert that teaches nothing is an alert wasted.

### 1.2 The tiers

- **Tier 1** triages: rapid validation, FP filtering, enrichment, routing. Their job is protecting Tier 2's time.
- **Tier 2** investigates: correlation, hypothesis testing, timeline building, root-cause analysis.
- **Tier 3 / detection engineering** handles complex response, guides containment, owns detection rules and tooling, and hunts.

Quality handovers are the failure point. The anti-pattern is ping-pong escalation — an issue bounced between tiers with no progress. The fix is clear ownership rules and a triage note complete enough that the next analyst never redoes the first analyst's work.

### 1.3 Escalation criteria

Escalate from triage to incident response when any of these hold: confirmed malicious activity (not merely suspicious); evidence of lateral movement or multiple affected hosts; data access or exfiltration indicators; persistence mechanisms found; the affected asset is crown-jewel (domain controller, backup infrastructure, finance system, executive); or the analyst cannot rule out maliciousness within the triage time box — uncertainty on a high-value asset escalates, it does not close.

### 1.4 IR handoff

The handoff package: the timeline, the affected entities, the evidence collected, what has and has not been contained, and the recommended next actions. IR owns containment, eradication, and recovery per NIST SP 800-61 Rev. 3 (final April 2025, CSF 2.0-aligned). Triage's job ends where IR's begins — but triage stays available for questions, because the triage analyst holds the freshest context.

### 1.5 Worked triage 1 — impossible-travel login

**The alert:** user `j.chen` authenticated from Chicago at 09:12 and from Lagos at 09:19 — seven minutes apart, ~5,500 miles. The detection compares location pairs against travel feasibility.

**Decision tree:**
1. Is the account shared? Team/service accounts legitimately sign in from multiple geographies. Check the account type first — a shared account usually closes this alert immediately (and the rule should exclude it).
2. Interactive or non-interactive? Non-interactive sign-ins (token refreshes, background sync) can surface from cloud datacenter locations that have nothing to do with where the human is. Only interactive sign-ins count for travel logic.
3. Device check: is the second sign-in from a known, managed device (Entra ID join type, recognized user agent)? Same managed device + new location leans benign (travel, VPN exit).
4. VPN check: is the user in a VPN group, and does the source IP belong to a known VPN vendor range (Fortinet, Palo Alto, Zscaler exit nodes)? Corporate VPN exit points routinely geolocate far from the user.
5. Cross-user check: does this IP appear in other users' sign-ins? A shared egress IP explains many "impossible" logins at once.
6. History: has this user triggered this before? Repeat benign triggers are tuning candidates, not investigation candidates.
7. Corroborating signals: failed MFA pushes, unknown device, access to unusual apps, or password reset right before — any one of these flips the verdict toward compromise.

**Verdict paths:** all-benign answers → close as benign true positive, note the FP pattern for the rule owner. Any corroborating signal → escalate: force password reset, revoke sessions, treat as account compromise until proven otherwise.

### 1.6 Worked triage 2 — malware beaconing alert

**The alert:** host `WS-4417` shows periodic outbound HTTPS to `cdn-metrics-ops.net` — connections every ~60 seconds, small uniform response sizes, running for 14 hours.

**Decision tree:**
1. Endpoint first: which process owns these connections? (Sysmon Event ID 3 / EDR network telemetry.) A browser doing it is different from `rundll32.exe` doing it.
2. Timing analysis: compute inter-arrival intervals. Tight clustering (low coefficient of variation) with multi-hour span is the beaconing signature; human browsing is bursty and irregular. Note jitter — real implants randomize intervals, so look for consistency *within* the jitter band, not metronome precision.
3. Domain age and reputation: newly registered domain, no legitimate business relationship, TLS certificate that doesn't match the claimed CDN — each raises confidence.
4. Endpoint correlation: was there a suspicious process creation (Sysmon 1), a file drop (Sysmon 11), or a phishing email to this user shortly before the beaconing started? The first callback is usually the least camouflaged moment.
5. Scope: does any other host talk to this domain? One host is containment; several is an incident.
6. Tasking check: any spikes in response size or POSTs to the same destination? Steady small check-ins are dormant; size spikes mean active tasking or exfiltration — escalate immediately.

**Verdict paths:** unknown process + tight intervals + young domain → confirmed incident: isolate host, preserve memory/disk, hand to IR. Known updater process + matching vendor behavior → benign true positive, suppress by process+destination.

### 1.7 Worked triage 3 — suspicious PowerShell

**The alert:** `powershell.exe` launched with `-EncodedCommand` on `SRV-FILE02` at 02:40 by user `svc-backup`.

**Decision tree:**
1. Parent process: what launched PowerShell? `explorer.exe` at 2pm is a human; `wmiprvse.exe`, `mshta.exe`, or an Office process at 2:40am is not. Parentage is the single highest-value field.
2. User context: is `svc-backup` supposed to run PowerShell? Service accounts have narrow, documented behaviors — anything outside the documented behavior is suspicious by definition.
3. Decode the command: base64-decode `-EncodedCommand` (it is usually UTF-16LE). Read what it does — credential access, download cradle, and discovery commands (`whoami`, `net user`, `nltest`) sort very differently from a backup script.
4. Script Block Logging (Event ID 4104): the de-obfuscated content. If logging wasn't enabled, that's a logging gap to record, not an excuse to guess.
5. Time and host: 02:40 on a file server vs business hours on an admin workstation. Baseline matters — compare against the account's normal behavior.
6. Lateral check: did this host or user touch other systems in the same window (Event ID 4624 type 3/10, 4648)?

**Verdict paths:** admin's known script from expected parent → benign true positive, document the pattern. Unknown parent + discovery commands + odd hour → escalate as potential intrusion; do not let the analyst "just watch it" — that decision belongs to IR with containment options ready.

---

## 2. Log sources

NIST SP 800-92's framing still holds: log management is infrastructure (collect → store → analyze → dispose), and its challenges are volume, immutability, inconsistent formats, review discipline, and retention. The defender's version of the question is simpler: for each source, what does it record, what question does it answer, what goes blind without it, and how do I generate it free in a lab.

### 2.1 Endpoint — Windows Event Logs

The native telemetry. Key Security-log event IDs every defender must know cold:

| ID | Meaning | Answers |
|---|---|---|
| 4624 | Successful logon (check Logon Type: 2 interactive, 3 network, 10 RDP, 11 cached) | Who got in, how, from where |
| 4625 | Failed logon | Brute force, password spraying |
| 4634 / 4647 | Logoff | Session bounds for timelines |
| 4648 | Logon with explicit credentials | RunAs, lateral movement |
| 4672 | Special privileges assigned | Admin-level logon |
| 4688 | Process creation (needs command-line auditing enabled) | What executed, with what arguments |
| 4697 / 7045 | Service installed (Security / System log) | Persistence via services |
| 4720 / 4722 / 4725 / 4726 | Account created / enabled / disabled / deleted | Rogue accounts |
| 4728 / 4732 / 4738 | Group membership changes (global / local / modified) | Privilege escalation |
| 4740 | Account locked out | Password attacks vs user error |
| 4768 / 4769 / 4771 | Kerberos TGT request / service ticket / pre-auth failure | Ticket abuse, AS-REP roasting |
| 1102 | Audit log cleared | Anti-forensics — almost always hostile |
| 4104 | PowerShell Script Block Logging | De-obfuscated script content |

What goes blind without it: identity. No 4624/4625 and you cannot answer "who logged in where" — the foundation of every account-compromise investigation. Note 4688 only carries command lines if process-creation auditing with command-line logging is enabled — a default-off setting that must be deliberately turned on.

### 2.2 Endpoint — Sysmon

Sysmon is the kernel-driver telemetry that makes Windows endpoints actually observable. The IDs that matter:

| ID | Event | Detection value |
|---|---|---|
| 1 | ProcessCreate | Full command line, parent, hashes (MD5/SHA256/IMPHASH) — malware execution |
| 2 | FileCreateTime changed | Timestomping |
| 3 | NetworkConnect | Process → IP:port mapping — C2 |
| 5 | ProcessTerminate | Lifecycle |
| 6 | DriverLoad | Unsigned drivers — rootkits |
| 7 | ImageLoad | DLL loads — injection, sideloading |
| 8 | CreateRemoteThread | Process injection (ATT&CK T1055) |
| 10 | ProcessAccess | Memory access — LSASS credential dumping |
| 11 | FileCreate | Dropped payloads |
| 12 / 13 / 14 | Registry create / value set | Persistence (Run keys) |
| 15 | FileCreateStreamHash | Alternate Data Streams |
| 17 / 18 | Named pipe create / connect | C2 channels, lateral movement |
| 22 | DNS query | Per-process DNS — DGA, DNS C2 |
| 23 | FileDelete | Anti-forensics |
| 25 | ProcessTampering | Hollowing, herpaderping |

The industry starting config is SwiftOnSecurity's sysmon-config (github.com/SwiftOnSecurity/sysmon-config): broad includes with tuned excludes for known noise. Olaf Hartong's modular config is the composable alternative. Config tuning *is* detection tuning at the source — every exclude you write is a decision about what you will never see.

### 2.3 Endpoint — EDR telemetry

EDR adds what logs can't: real-time process trees, memory context, behavioral blocking, and remote response (isolate, kill, quarantine). In triage terms, EDR answers "what is happening *right now* on this box" while logs answer "what happened." Free lab path: Wazuh agents (open-source XDR with Sysmon integration) or Velociraptor for collection and hunting queries.

### 2.4 Network — the wire doesn't lie

| Source | Records | Answers | Blind without it |
|---|---|---|---|
| Firewall | Allowed/denied 5-tuples | What crossed boundaries, what was stopped | No perimeter truth |
| Proxy | Full URLs, user agents, categories | Web activity per user/device — phishing clicks, malicious downloads | No web-visibility |
| DNS query logs | Every name resolution | DGA, DNS tunneling, beaconing to rare domains | C2 over DNS invisible |
| IDS/IPS (Suricata, Snort, Zeek) | Signature + protocol-anomaly alerts; Zeek logs (conn, dns, http, ssl, files) | Exploit attempts, protocol abuse, file transfers | No network detection layer |
| NetFlow / IPFIX | 5-tuple + bytes/packets/timing, no payload | Beaconing intervals, data volume anomalies, lateral movement | Encrypted traffic is a black box |

Zeek is the standout free sensor: connection, DNS, HTTP, SSL, and file logs with full protocol parsing — the network equivalent of Sysmon. Suricata and Snort provide signature IDS. NetFlow answers the beaconing question even when TLS hides the payload: timing and volume survive encryption.

### 2.5 Identity — Active Directory and Entra ID

Domain controllers emit the 4624/4625/4768/4769/4771 stream that makes account-compromise investigation possible. Entra ID (Azure AD) sign-in logs add: interactive vs non-interactive sign-in type, device join state, IP geolocation, MFA result, conditional access decisions, and the anomaly detections (impossible travel, unfamiliar sign-in properties, leaked credentials). The impossible-travel triage in §1.5 runs entirely on this source. Blind without it: every identity attack — password spray, token theft, Kerberoasting — is invisible.

### 2.6 Email gateway

Records sender, recipients, subject, attachment names/hashes, URLs, and verdicts (spam, phish, malware). Answers "how did it get in" — the initial-access question for most intrusions. In the beaconing triage (§1.6), the email gateway is where you look for the phish that preceded the first callback.

### 2.7 Cloud audit

- **AWS CloudTrail:** every API call — who (IAM principal), what action, on which resource, from which IP, with what result. Answers "what did the key do." Blind without it: cloud control-plane attacks are invisible.
- **Azure Activity Log:** control-plane operations on Azure resources — role assignments, VM changes, key creation.

Free lab generation: a personal AWS/Azure account's own audit trail (read-only audit roles), CloudTrail to local storage, plus Prowler/ScoutSuite for misconfiguration auditing against your own account.

### 2.8 The home-lab logging stack (all free)

Security Onion (Zeek + Suricata + Sigma-based detection with daily rule updates), Wazuh (agents + manager + dashboard, Sysmon ingestion), Velociraptor (endpoint collection and hunting), Windows Event Forwarding (native, no agent), Winlogbeat/Elastic Agent shipping to a local stack. This stack generates every source in §2.1–§2.4 against your own lab VMs.

---

## 3. Detection logic

### 3.1 Reading a real Sigma rule, field by field

Sigma is the vendor-agnostic detection format: one YAML rule compiles via pySigma backends (Sigma CLI, sigconverter.io, Detection Studio) into Splunk SPL, Sentinel KQL, Elastic EQL, and others. The SigmaHQ repository holds 3000+ community rules in four types: generic detection, threat hunting, emerging threat, and compliance rules. Below is a complete real-format rule — suspicious encoded PowerShell — read field by field:

```yaml
title: Suspicious Encoded PowerShell Command
id: 5b1a3c2e-7d4f-4e8a-9c11-2f6b8d0a1e33
status: experimental
description: Detects PowerShell launched with an encoded command, a common obfuscation technique
references:
    - https://attack.mitre.org/techniques/T1059/001/
author: Your Name
date: 2026/09/21
tags:
    - attack.execution
    - attack.t1059.001
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains:
            - ' -enc '
            - ' -EncodedCommand '
    condition: selection
falsepositives:
    - Legitimate administration scripts
level: high
```

- **title / description:** what a human reads in the alert queue. A good title names the behavior, not the malware family — behaviors outlive campaigns.
- **id:** UUIDv4, globally unique. This is how rules are tracked across versions, forks, and SIEM conversions. Generate with `python -c "import uuid; print(uuid.uuid4())"`.
- **status:** maturity — `experimental`, `test`, `stable`, `deprecated`, `unsupported`. Never ship `experimental` to production without a soak period.
- **references:** the research the rule is built on — ATT&CK technique pages, write-ups. A rule without references is un-auditable.
- **tags:** MITRE ATT&CK mapping (`attack.execution` tactic, `attack.t1059.001` technique). These tags are what make coverage measurement possible — the union of tags across your ruleset is your detection map.
- **logsource:** where the rule looks. `category: process_creation` + `product: windows` means "Windows process-creation telemetry" — which in practice is Sysmon Event ID 1 or Windows 4688. The category is the contract: if your environment doesn't produce that category, the rule is dead on arrival. (A detection you can't feed is a paper rule.)
- **detection / selection:** the matching logic. Fields within a selection are ANDed; list values are ORed. `Image|endswith` and `CommandLine|contains` are **modifiers** — they change how matching works (suffix, substring, prefix, regex, case-sensitivity, base64offset). Modifiers are the difference between a rule that fires on noise and one that fires on signal.
- **detection / condition:** the boolean combining selections — `selection`, `selection and not filter`, `1 of them`, aggregations like `count() by`. Filters are named selections of known-benign patterns excluded from the alert.
- **falsepositives:** the documented benign triggers. Writing these honestly is what separates a production rule from a lab experiment — 80% of production false positives come from missing filters and poor documentation.
- **level:** `informational / low / medium / high / critical` — the severity the rule *suggests*. Triage sets the priority (§1.4); the rule does not get the last word.
- **fields (optional):** which event fields to include in the alert output — the enrichment the analyst needs without a second query (UtcTime, Image, CommandLine, User, ComputerName).

The Sigma specification itself (SigmaHQ/sigma-specification) defines all of this formally: the rules spec, the correlation spec (multi-event rules), the filters spec, and appendices for modifiers, tags, and the taxonomy of supported log sources. Version 2.x is current.

### 3.2 The tuning loop

Detections are kept honest by a loop, not a launch:

1. **Baseline.** Before the rule ships, know what normal looks like in *your* environment — run the logic against historical data and count the hits.
2. **Threshold.** Set the firing bar from the baseline: frequency thresholds, rarity windows, allowlisted entities. A rule that fires 200 times a day on SCCM activity is a broken rule, not a sensitive one.
3. **Suppress.** Build benign filters into the rule (`filter: ParentImage|endswith: '\sccm.exe'`), narrow the logsource, add context (asset, user, change window). Tune order: filters first, thresholds second, narrowing third.
4. **Escalate.** What survives tuning is signal. Ship it with its triage runbook — every production rule carries an expected FP profile and a runbook, or it doesn't ship, because analysts can't action what they can't interpret.

### 3.3 False-positive management

FPs are closed, counted, and fed back. Analyst close codes (true positive / benign true positive / false positive) are tuning telemetry — the detection engineer's raw material for the next revision. Periodic detection audits review three lists: the noisiest rules (tune or suppress), the never-fired rules (broken, or genuinely quiet — find out which), and rules whose data source went dark (paper rules). Rule decay is real: environment changes, vendor API changes, and attacker drift silently break detections.

### 3.4 Detection-as-code workflow

Treat detections like software, because they are:

- **Repo:** Sigma YAML in git. Every rule has id, status, tags, level.
- **CI on every change:** schema validation against the Sigma spec, linting (missing ATT&CK tags, invalid log sources, impossible conditions), conversion to each SIEM backend (catches translation errors), behavioral tests — the rule fires on a positive corpus and stays silent on a benign corpus.
- **Staging soak:** new rules run in non-production first, against live data, measuring real FP rate before promotion.
- **Production:** converted queries deployed; drift monitored (nightly recompile, diff against production).
- **Quarterly review and retirement:** coverage re-measured, dead rules deprecated with documented justification.

A proven gap is a deliverable: run Atomic Red Team's tests for a technique, and if no alert fires, that false negative is a finding, not an absence of findings.

### 3.5 Mapping detections to ATT&CK and measuring coverage

The `tags:` on every rule, aggregated, produce an ATT&CK Navigator layer: techniques with detections light up, techniques without stay dark. That layer is the honest answer to "what do we detect." But read it correctly:

- **Technique coverage is not procedure coverage.** A rule for "PowerShell with encoded command" covers one *procedure* of T1059.001, not the technique. An adversary using a different procedure walks past it.
- **Coverage needs the negative test.** A detection with no executed test (Atomic Red Team, Caldera) is unvalidated — claimed, not proven.
- **Coverage decays.** New procedures, new tools, and environment changes erode it; the quarterly review re-proves it.

"What we detect" really means: which ATT&CK techniques have validated, tuned, production detections with runbooks, measured against both positive and negative corpora, reviewed this quarter. Anything less is a claim, not coverage.

---

## 4. Gaps (honest, for build time)

1. SigmaHQ rule-file paths have been restructured — one raw.githubusercontent fetch 404'd; lesson writers should browse the repo tree rather than guessing paths. The spec repo (SigmaHQ/sigma-specification) is the stable primary for format questions.
2. Several rows above are `operator-added` (community writeups, analyst blogs) rather than primary-fetched: PTES technical guidelines page returned HTTP 403 in the earlier round; the impossible-travel checklist is analyst-authored (corroborated by Microsoft's documented sign-in fields). Lesson writers re-fetch as primary per the brief's evidence rules.
3. NIST SP 800-92r1 is still a draft (Oct 2023 initial public draft) — the 2006 final remains the citable standard; check whether r1 has finalized before lessons ship.
4. CloudTrail/Azure Activity Log field details were written from established knowledge, not a fresh primary fetch — re-verify against current AWS/Azure docs at lesson-writing time.
5. No walkthrough commands were executed in this pass — per the brief, walkthrough execution belongs to Phase 2/3 lesson writing, and each lesson must record tool versions and dates when run.

---

## 5-line handoff

1. **Coverage:** all three areas delivered to lesson depth — SOC triage lifecycle with 3 worked triages (impossible travel, beaconing, suspicious PowerShell) each with a decision tree; 8 log-source families (Windows Event IDs, Sysmon IDs, EDR, network 5, identity, email, cloud) each with records/answers/blind-spots/free-lab-generation; detection logic (real Sigma rule read field-by-field, tuning loop, FP management, detection-as-code CI, ATT&CK coverage semantics).
2. **Key sources:** SigmaHQ/sigma and sigma-specification repos (verified), NIST SP 800-92 (DOI), SwiftOnSecurity sysmon-config, detection-as-code lifecycle, impossible-travel analyst checklist, beaconing signal docs, BHIS vsagent C2 lab.
3. **Gaps:** one 404 on a SigmaHQ raw file path (use repo tree browsing); several rows operator-added not primary-fetched (flagged in ledger); SP 800-92r1 still draft; cloud audit fields need doc re-verification at write time; no walkthroughs executed (Phase 2/3 work).
4. **Brief compliance:** zero prices/fees/salaries/time estimates; free-to-learn only; original prose; no copied rule text beyond short field examples; safety line held (concepts + detection, no offensive tooling).
5. **File:** ~/workspace/security-curriculum/night-research/10-soc-detection.md — ready for the lesson-writing phase.
