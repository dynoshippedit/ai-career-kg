---
lesson_id: c-incident-response
slug: incident-response
stage: C
level: 3
prerequisites: [c-soc-triage, c-log-sources]
roles: [soc-analyst, dfir]
map_refs: []
test_date: 2026-10-09
description: "Incident response basics: the NIST SP 800-61 Rev. 3 lifecycle and the full IR report — timeline, scope, ordered containment, honest limitations. A free lesson in the security guidebook."
dateline: "Worked case authored and reviewed 2026-10-09 · no command line in this lesson"
---
# Incident Response Basics


---

## 1. Where this shows up

Triage ends with "confirmed incident" — and then a different discipline takes over. Incident response is the structured work of containing, eradicating, and recovering from a security incident without making it worse: no wiping the evidence before it's preserved, no alerting the adversary before containment is ready, no declaring victory before the persistence is found. It is the core of the DFIR role path (`/r/dfir/`), the reason SOC triage exists, and the artifact — the IR report — is one of the most checkable pieces of evidence a practitioner can produce. This lesson teaches the lifecycle and makes you write the report.

## 2. Before you start

- You can triage an alert to a classification and write a handoff note (`c-soc-triage`) — IR *starts* from that handoff package.
- You can build a cross-source timeline (`c-log-sources`) — the report's evidence section is that timeline, written for an executive.
- Internalize the boundary: **triage recommends, IR acts.** The moment you touch a containment action (isolate a host, reset credentials, block an IOC — an indicator of compromise, an observable tied to the intrusion such as an IP, a domain, or a file hash), you are doing IR, with IR's obligations: preserve evidence first, coordinate, document everything.

## 3. How it works

The current spine is **NIST SP 800-61 Rev. 3** (final, April 2025) — and note what changed: it is now titled *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile*. (A Community Profile is a pre-built CSF profile for a shared use case — a baseline of outcomes NIST publishes so organizations can adopt it instead of building their own from scratch.) It supersedes Rev. 2 (2012) and restructures incident handling around the CSF 2.0 functions rather than the old four-phase playbook. Old summaries of 800-61 you find online describe Rev. 2 — treat them as stale. The lifecycle, in the shape you will actually use:

**Preparation.** Everything that makes the later phases possible, built *before* anything happens: the IR team and its contact tree, the playbooks for common incident types (a playbook is the written response plan for one incident type: who does what, in what order, with which tools), the tooling (EDR, log retention that actually covers the timeline you'll need), the communication plan (who talks to legal, to executives, to customers — and in what order), and practiced roles. An incident is the wrong time to discover you have no retention.

**Detection and analysis.** Triage's output becomes IR's input. The handoff package: the timeline, the affected entities, the evidence collected, what has and has not been contained, recommended next actions. Analysis here means scoping the incident fully *before* acting — the classic failure is containing the one known host while the adversary's second foothold watches.

**Containment.** Stop the bleeding without destroying the evidence. Short-term containment (isolate the host from the network — but *not* power off, which kills memory evidence) comes before long-term containment (block IOCs at the perimeter, rotate credentials). The ordering matters: preserve first, then contain, and contain *quietly* — tipping off the adversary before you're ready trades one incident for a faster-moving one. Attacker infrastructure gets neutralized quietly too: sinkholing their domains (pointing the DNS at a server you control, so infected hosts phone home to you instead of the attacker) and blocking their IPs at the perimeter cut the command channel without announcing that you know.

**Eradication.** Remove the cause: kill the persistence (the Run key — the Windows registry key whose entries launch at logon, a classic persistence spot — the rogue account, the web shell), patch the exploited flaw, remove the attacker's artifacts. Eradication without complete scoping is theater — this is where missed second footholds come back.

**Recovery.** Bring systems back into production carefully: rebuild from known-good media where the compromise was deep, restore from clean backups, monitor closely for re-infection. Recovery is a *decision*, not the absence of incident — someone signs off that the environment is clean, with evidence.

**Post-incident activity.** The lessons-learned review: what happened, what worked, what didn't, what changes (detection, logging, playbook, architecture). The report from this phase is the artifact below — and its recommendations are the only part of IR that prevents the *next* incident.

Two principles govern all of it. **Evidence before action:** every containment step that destroys data (reimaging, deleting logs) needs the evidence preserved first — memory capture, disk image, log export. **Communicate in the right order:** internal coordination before external notification; legal before public statements. The order is risk management, not politeness: public statements create legal and regulatory exposure, and uncoordinated notifications tip the adversary. Internal alignment first means every external message is consistent and counsel has seen it. The report you write is read by people who were not in the room; it must stand alone.

### Worked example: the WS-4417 intrusion — full IR report

*Scenario (fictional, labeled):* the intrusion assembled across the `c-log-sources` walkthrough — password spray from `203.0.113.99` against `DC-01`, `t.nguyen`'s account compromised at 03:19, encoded PowerShell on `WS-4417` at 03:21, DGA-shaped DNS burst (DGA — domain generation algorithm — is malware that generates hundreds of pseudo-random domain names and queries them until one resolves to the real command server, so defenders can't blocklist it in advance), beacon-shaped firewall flows, audit log cleared at 03:25. Triage escalated at 03:40. What follows is the report IR would write.

---

**INCIDENT REPORT — IR-2026-1047** (fictional training scenario)

**Executive summary.** On 2026-10-09 at 03:40, SOC triage escalated a confirmed account compromise. An external actor password-sprayed six accounts, compromised one (`t.nguyen`), executed encoded PowerShell on workstation `WS-4417`, established periodic outbound communications consistent with command-and-control, and cleared the local audit log. Containment completed 06:15; no evidence of lateral movement beyond the single host or of data exfiltration was found *within the sources available* — that qualifier is load-bearing (see Limitations).

**Timeline (all times UTC).**

| Time | Event | Source |
|---|---|---|
| 03:01–03:18 | 18 failed logons (4625), six users, one source IP `203.0.113.99` | DC-01 Security log |
| 03:19 | Successful logon (4624, type 3) for `t.nguyen` from `203.0.113.99` | DC-01 Security log |
| 03:21 | PowerShell `-EncodedCommand` (4688); de-obfuscated content (4104) | WS-4417 |
| 03:21–03:33 | 12 queries to nonsense domains (DGA shape) | DNS log |
| 03:20–03:32 | 12 uniform 210-byte outbound flows to `203.0.113.200` (beacon shape) | Firewall |
| 03:25 | Audit log cleared (1102) | WS-4417 |
| 03:40 | Triage escalates: confirmed incident | SOC ticket |
| 04:05 | Memory capture + disk image of `WS-4417` preserved | IR action |
| 04:20 | Host isolated from network (not powered off); `t.nguyen` credentials rotated, sessions revoked | IR action |
| 05:00 | Attacker IP blocked at perimeter; DGA domains sinkholed | IR action |
| 06:15 | Full-enterprise sweep for IOCs: no other hosts affected | EDR + SIEM |

**Scope.** One user account, one workstation. The IOC sweep (hash of the dropped payload, the 12 domains, the beacon IP) across the fleet found no other matches.

**Root cause.** Password spray succeeded against an account with no MFA and no lockout-effective throttling — the same weakness class as `b-session-auth`. Initial access was credential-based, not exploit-based.

**Containment.** Short-term: host isolated, credentials rotated, sessions revoked (04:20). Long-term: perimeter blocks, sinkhole (05:00). Evidence preserved *before* containment actions that could destroy it.

**Eradication.** Rogue scheduled task removed, payload hash blocked, `t.nguyen`'s account re-secured with MFA enrolled. Attack chain broken at every link observed.

**Recovery.** `WS-4417` rebuilt from known-good image (not cleaned in place — the 1102 made in-place trust impossible); returned to service 2026-10-10 after 24h enhanced monitoring with no recurrence.

**Limitations — what we cannot claim.** No proxy logs existed, so web activity is unknown. No EDR process tree, so in-memory-only activity before 03:21 is unknown. The 1102 means the local timeline after 03:25 is incomplete. "No evidence of exfiltration" is not "evidence of no exfiltration" — say which one you have.

**Lessons learned / recommendations.** (1) Enforce MFA on all accounts — kills this entire attack class. (2) Alert on spray shape — the detection rule this incident now justifies (concretely: multiple 4625s from one IP across three or more users inside a short window; the count, the IP, and the user spread are the three fields the rule keys on; `c-sigma-detection` teaches the rule format for writing it). (3) Enable command-line auditing on all endpoints (the 4688 was luck). (4) Deploy proxy logging — the initial-access vector question was unanswerable. (5) Forward logs off-host in real time so a future 1102 can't blind the timeline.

---

That report is the lesson's artifact and its proof of understanding in one: timeline from evidence, scope honestly bounded, actions ordered correctly, limitations stated, recommendations that prevent recurrence.

## 4. Walkthrough

**Run by us** — transcript: `runs/c-incident-response.log`. There is no command line in this lesson by design (brief §6: for non-CLI topics the walkthrough is the worked case producing the real work product). What "ran" here is the authoring-and-review pass, logged with scope, method, and review notes, 2026-10-09.

1. **Fix the scenario.** The fictional WS-4417 intrusion from `c-log-sources` — labeled fictional, every timestamp and value invented. State the scenario's boundaries up front: single host, credential initial access, no real systems involved.
2. **Assemble the evidence pack.** Collect the timeline rows from the log-sources walkthrough (the 4625 spray, the 4624 payoff, 4688/4104, DNS burst, firewall flows, 1102). An IR report with no evidence pack is fiction; check each row has a source.
3. **Scope before acting (on paper).** Write the scoping questions first: which accounts? which hosts? (IOC sweep results: one and one.) lateral movement? (none found.) data touched? (unknown — no proxy/EDR.) Do not write a single containment action until scoping is drafted — this ordering is the discipline.
4. **Draft containment in the right order.** Evidence preservation (memory, disk, log export) *before* isolation; isolation *before* credential rotation alerts anyone; quiet actions before noisy ones. Read your draft and check: does any step destroy evidence a later step needs? Fix it if so.
5. **Draft eradication and recovery.** Name the persistence removed, the flaw fixed, the rebuild-vs-clean decision (1102 → rebuild, with the reason stated). Recovery gets a sign-off line: who declares clean, on what evidence.
6. **Write the Limitations section.** List every blind spot from the source map: no proxy, no EDR, post-1102 timeline incomplete. Convert "no evidence of X" claims into their honest form.
7. **Write recommendations that prevent recurrence.** Each recommendation must trace to a specific failure in the timeline (MFA → spray succeeded; spray-shape alert → 18 failures unnoticed; command-line auditing → 4688 luck; proxy logging → unanswerable vector; off-host forwarding → 1102 blindness). A recommendation that doesn't trace to the incident is generic advice, not lessons learned.
8. **Self-review against the checklist.** The log records the review: ☐ every timeline row sourced; ☐ scope stated before actions; ☐ evidence preserved before destructive steps; ☐ limitations honest; ☐ recommendations traceable; ☐ no prices, no hype, no claim beyond the evidence. All boxes checked 2026-10-09.

## 5. On your own

**Task:** Take the beaconing triage case from `c-soc-triage` (host `WS-4417`, 60-second intervals to a young domain — invent the three events *after* the triage escalation: what the memory capture found, whether lateral movement occurred, one surprise) and write the full IR report: executive summary, timeline, scope, root cause, containment, eradication, recovery, limitations, recommendations.

**Success test:** A reader who wasn't in the room can reconstruct what happened, what was done, and what remains unknown — from your report alone. If any section requires asking you a follow-up question, it's incomplete.

## 6. Where it goes wrong

- **Containing before scoping.** Isolating the one known host while the second foothold watches is the classic failure. Scope first — the adversary's patience exceeds your urgency.
- **Powering off the box.** Kills memory evidence (running processes, network connections, encryption keys). Isolate from the network; keep it running until memory is captured.
- **Tipping off the adversary.** Loud containment (mass password resets, public blocks) before you're ready trades a contained incident for a faster-moving one. Quiet first, then broad.
- **Cleaning instead of rebuilding.** "We removed the malware" on a host whose audit log was cleared is trust without evidence. Deep compromise → rebuild from known-good.
- **Declaring victory at containment.** Containment stops the bleeding; eradication removes the cause; recovery returns to production. Skipping to "we blocked the IP" leaves the persistence in place.
- **The report nobody writes.** No post-incident review means the next incident re-learns everything. The recommendations section is the only part of IR that compounds.

## 7. Read the source

Primary documents first:

- **NIST SP 800-61 Rev. 3** (csrc.nist.gov/pubs/sp/800/61/r3/final) — *read* fully; it is the lifecycle spine of this lesson. *Note* the April 2025 date, the CSF 2.0 Community Profile structure, and that it supersedes Rev. 2 (2012) — older summaries are stale.
- **NIST SP 800-92** (doi.org/10.6028/NIST.SP.800-92) — *re-read* the retention and review sections with IR eyes: your timeline is only as long as your retention.
- **CERT Guide to Coordinated Vulnerability Disclosure** (certcc.github.io/CERT-Guide-to-CVD/) — *read* the communication principles; *note* IR's external-notification obligations rhyme with CVD's (coordinate before you announce).

Then at most three free resources:

1. **SANS, *Dynamic Incident Response*** (sans.org/engage/dynamic-incident-response — free, CC BY 4.0, no purchase or login) — the modern practitioner book arguing incidents don't follow the linear script. Read the "Verify, triage, and scope" chapter first — it is this lesson's scoping discipline from the field; skip the domain chapters (ransomware, cloud, OT) until you specialize. The free DAIR model poster is the two-page summary.
2. **Velociraptor** (docs.velociraptor.app) — free; the evidence-preservation and collection tool: memory capture, disk triage, fleet-wide IOC sweeps like the one in the worked example. Read the Quickstart to stand it up, then the Artifact Reference (the pre-built collection queries — that is what the IOC sweep runs on); skip the VQL Reference on first pass — it is a language manual, not a lesson.
3. **The `c-log-sources` blind-spot column** — re-read your own source map: every blind spot you named there is a limitation pre-written for your first real IR report.

## 8. Check yourself

1. Triage hands you a confirmed incident on one host. Before any containment action, name the three scoping questions you must answer — and explain what goes wrong if you contain first and scope second.
2. Explain why "isolate from the network but do not power off" is the correct first containment step, naming the specific evidence each choice preserves or destroys.
3. Your report says "no evidence of data exfiltration." Explain the honest reformulation of this claim given no proxy logs and no EDR — and why the distinction matters to the executives reading it.
4. The audit log was cleared (1102) mid-incident. Explain how this changes both your eradication decision (clean vs. rebuild) and what your timeline can claim.
5. A recommendation says "improve monitoring." Explain why this fails the traceability test — and rewrite it so it traces to a specific failure in the WS-4417 timeline.

## 9. Prove it

**Artifact:** the §5 report — the beaconing case with your three invented post-escalation events, written to the full structure: executive summary, sourced timeline, scope, root cause, ordered containment/eradication/recovery, honest limitations, traceable recommendations. Not the walkthrough's WS-4417 report — that one was the worked example. This one must be yours: a stranger reading it should not be able to tell which parts came from the lesson.

**Honest claim:** "I can take a triage escalation, scope it, order containment without destroying evidence, and write the IR report that stands alone."
**Can't claim yet:** "I can lead incident response" — leading means legal coordination, executive communication under pressure, and adversary-aware operations across a real enterprise (`d-dfir-deep` track).

## 10. Leads to

- `c-soc-triage` — the loop closes: your recommendations become the detection rules and logging improvements the next triage shift relies on.
- `c-sigma-detection` — recommendation (2) in the worked example is a rule waiting to be written; detection engineering is where IR lessons compound.
- **d-dfir-deep track** — disk, memory, and network forensics: the deep evidence work this lesson's timeline assumes.
- Map refs: **Stage C · Professional**; **NIST SP 800-61 Rev. 3**; NICE **Protection and Defense** and **Investigation**; the `/r/dfir/` and `/r/soc-analyst/` paths.
