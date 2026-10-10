---
lesson_id: c-soc-triage
slug: soc-triage
stage: C
level: 3
prerequisites: [a-linux-cli, b-session-auth]
roles: [soc-analyst, security-analyst]
map_refs: []
test_date: 2026-10-09
description: "SOC triage: from alert to decision — the eight-stage pipeline, impossible-travel and beaconing decision trees, and the five classification buckets. A free lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · labeled fictional event set; decision trees executed locally"
---
# SOC Triage: From Alert to Decision


---

## 1. Where this shows up

Every alert a security operations center produces lands on a human who has minutes — not hours — to decide what it means. That decision is triage: turning a detection's hypothesis into a classification and a routing action. It is the daily work of the SOC analyst role (`/r/soc-analyst/`), the skill every detection engineer writes rules *for*, and the discipline that stands between a 3 AM page and a real incident. Get triage wrong and two things happen: real attacks sit in a queue, and analysts burn out on noise. This lesson teaches the decision flow, not the tools — the flow survives every SIEM change. (A SIEM — security information and event management — is the platform that ingests logs from many sources so you can search and correlate them in one place; the triage discipline is the same whatever vendor's console you're staring at.)

## 2. Before you start

- You can read a log line cold and count things with the command line (`a-linux-cli`).
- You know the attacker's session-abuse shapes (`b-session-auth`): fixation, predictable tokens, brute force and credential stuffing as concepts, and the honest limit that a stolen post-login cookie bypasses MFA. The defensive-signal *reading* of those attacks — impossible travel, the spray shape — is taught here, in the decision trees below, not there.
- Mindset shift from Stage B: you are no longer proving a finding. You are *disproving* an alert — innocent until the evidence says otherwise. The alert is a hypothesis, not a verdict.

## 3. How it works

Triage is a pipeline with eight stages. Memorize the shape, because under time pressure you will fall back to whatever shape you trained:

1. **Intake.** Acknowledge the alert. Read the detection's hypothesis *first* — what did the rule claim to see, and in which log? Identify the user, the asset, the application, the data source. Time-box this: triage is minutes.
2. **Enrichment.** Attach context before judging: asset criticality (domain controller or test VM?), user role (admin? service account?), IP geolocation, threat intel (curated records of known-malicious IPs, domains, and file hashes — from feeds or commercial sources — that let you attach a verdict to an observable) on the IOCs (indicators of compromise — the observables tied to the intrusion), and — most valuable — other alerts on the same entities in the same window.
3. **Scoping.** The single most important triage question: *one host or a campaign?* Pivot the alert's entities (user, host, IP, hash, domain) across the estate and the time window. One host with a suspicious IOC is an incident candidate; the same IOC on forty hosts is either a campaign or a broken rule — different handling either way.
4. **Severity vs. priority.** Severity is the detection's technical rating (how bad *if true*). Priority is severity × asset value × confidence. A critical alert on a decommissioned lab VM is low priority; a medium alert on the CFO's laptop is high priority. Triage sets priority; the rule only suggested severity.
5. **Investigation.** Build the timeline around the alert. Find root cause and initial access. Check for lateral movement. Determine what data was touched. One log source never tells the story — correlate endpoint, identity, and network together.
6. **Containment recommendation and escalation.** Triage does not contain; it *recommends*. The split is deliberate: containment needs full scoping, carries evidence-destruction and legal risk, and requires authority the triage analyst doesn't hold. Triage runs in minutes; IR acts with coordination. Recommending instead of acting keeps the fast decision from becoming the irreversible one. Escalation criteria decide who acts (below).
7. **Classification and routing.** Every alert ends in one of five buckets: **false positive** (rule matched wrongly → tune the rule), **benign true positive** (rule matched correctly on expected activity → close with reason), **suspicious** (needs deeper work → Tier 2, the more experienced analysts who take the cases Tier 1 can't close), **confirmed incident** (start the IR playbook), **duplicate** (link to the parent case).
8. **Documentation and lessons learned.** Write the triage note: what was seen, what was checked, what was decided, the evidence. Feed the outcome back — IOCs to intel, tuning notes to detection engineering, process gaps to the playbook. An alert that teaches nothing is an alert wasted.

**Escalate** from triage to incident response when any of these hold: confirmed malicious activity (not merely suspicious); lateral movement or multiple affected hosts; data access or exfiltration indicators; persistence found; a crown-jewel asset (domain controller, backups, finance, executive); or you cannot rule out maliciousness within the triage time box — uncertainty on a high-value asset escalates, it does not close. The rule is asymmetric cost: a missed compromise on a domain controller costs more than a hundred wasted escalations. Uncertainty is a routing input — "I can't rule it out" — not a verdict.

### Worked example: the impossible-travel decision tree

The alert: `j.chen` signed in from Chicago at 09:12 and from Lagos at 09:19 — seven minutes apart, roughly 9,600 km. The detection compares location pairs against travel feasibility. Your decision tree, in order:

1. **Shared account?** Team or service accounts legitimately sign in from multiple geographies. Check account type first — a shared account usually closes this alert immediately (and the rule should exclude it).
2. **Interactive or non-interactive?** Non-interactive sign-ins (token refreshes, background sync) surface from cloud datacenter locations that have nothing to do with where the human is. Only interactive sign-ins count for travel logic.
3. **Device check.** Is the second sign-in from a known, managed device? Same managed device plus a new location leans benign (travel, new VPN exit).
4. **VPN check.** Is the user in a VPN group, and is the source IP a known VPN vendor exit range? Corporate VPN exits routinely geolocate far from the user.
5. **Cross-user check.** Does this IP appear in other users' sign-ins? A shared egress IP explains many "impossible" logins at once.
6. **History.** Has this user triggered this before? Repeat benign triggers are tuning candidates, not investigation candidates.
7. **Corroborating signals.** Failed MFA pushes, unknown device, unusual apps, a password reset right before — any one flips the verdict toward compromise. Concretely: in the sign-in log, look for repeated MFA challenges the user denied or ignored right after the travel-violating sign-in — a burst of "MFA denied" results is the attacker trying to push through.

All-benign answers → close as benign true positive, note the pattern for the rule owner. Any corroborating signal → escalate: force password reset, revoke sessions, treat as compromise until proven otherwise.

The same tree shape applies to the beaconing alert (host `WS-4417`, HTTPS every ~60 seconds to a young domain for 14 hours): which process owns the connections? How tight are the intervals (low coefficient of variation = beaconing signature; humans are bursty)? Domain age and reputation? Was there a phishing email before the first callback? One host or several? Steady small check-ins are dormant; size spikes mean tasking or exfiltration — escalate immediately.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/c-soc-triage.log`. Clean environment: stock Python 3.12.3, loopback only, 2026-10-09. The event set is **fictional and labeled as such** — invented sign-ins and flows designed to exercise each branch of the decision trees.

1. **Read the event set.** Open `/tmp/guidebook/c-stage/triage_events.jsonl`: five sign-in events across three users, two network-flow summaries. Note the `# FICTIONAL` header — every value invented.
2. **Pair the sign-ins per user.** The script groups by user and sorts by time — this is the scoping step: one timeline per identity.
3. **Run the impossible-travel tree on `j.chen`.** Chicago → Lagos, 7 minutes, ~9,607 km: physically impossible. Interactive? Yes. Known device on the second sign-in? No. VPN exit? No. Verdict: **ESCALATE** — cannot rule out compromise. This is the case the alert exists for.
4. **Run it on `m.okafor`.** Austin → Frankfurt, 38 minutes, ~8,528 km: also impossible on its face. But the second sign-in is from a known VPN exit range. Verdict: **CLOSE (benign true positive)** — and note the tuning feedback: the rule should check VPN exits before alerting.
5. **Run it on `svc-backup`.** Ashburn → Singapore, non-interactive both times. Verdict: **CLOSE** — travel logic never applied; the rule firing on a service account is itself a tuning note.
6. **Run the beaconing check on `WS-4417`.** Six connections, mean interval 60 s, coefficient of variation 0.03 — tight clustering over a multi-hour span. Verdict: **ESCALATE (beaconing suspected)**. Then run the enrichment stage on it: the DNS log shows `WS-4417` also bursting queries for nonsense domains (the DGA shape) — one host, two independent suspicious signals. (`c-log-sources` teaches the DNS source behind this pivot; you don't need it to run the tree.)
7. **Run it on `WS-4420`.** Mean interval 1,800 s, CV 0.84 — bursty, irregular, large byte counts mixed with tiny ones: an updater, not a beacon. Verdict: **CLOSE (benign true positive)**.
8. **Write the triage notes.** For each of the five cases, one note in the format: *what was seen / what was checked / what was decided / evidence*. The escalated `j.chen` note ends with the containment *recommendation* (password reset, session revoke) — you recommend, IR acts.

No step above is marked "not run by us" — the trees, the classifications, and all five verdicts ran against the labeled fictional set and the transcript records the real output.

## 5. On your own

**Task:** Extend the event set with two new cases of your own invention: one alert that should escalate and one that should close, each exercising a *different* branch of the trees than the walkthrough used (e.g., a shared-account close, a size-spike escalation). Add them to the JSONL, re-run the script, and write triage notes for both.

**Success test:** Your two new cases classify correctly, and each triage note names the exact tree branch that decided it. If you cannot say which branch decided it, the note is incomplete — rewrite it.

## 6. Where it goes wrong

- **Treating the alert as the verdict.** The rule said "impossible travel" — the analyst's job is to check whether it was. Analysts who forward alerts instead of triaging them are expensive routers.
- **Skipping scoping.** Triaging one host while four others beacon to the same domain turns an incident into five separate "suspicious" tickets. Pivot *before* you classify.
- **Confusing severity with priority.** A critical-severity rule firing on a lab VM is not a 3 AM page. Priority needs asset value and confidence; the rule cannot know either.
- **Ping-pong escalation.** An issue bounced between tiers with no progress and no new evidence. The fix is ownership rules and a triage note complete enough that the next analyst never redoes your work.
- **Closing on uncertainty.** "Probably fine" is not a classification. If you cannot rule out maliciousness on a valuable asset within the time box, it escalates — uncertainty is a routing input, not a verdict.
- **Alert fatigue as a personal failing.** Fatigue is a *detection* problem (noisy rules), not an analyst problem. The professional response is tuning feedback with close-code data, not trying harder to care about the 200th false positive.

## 7. Read the source

Primary documents first:

- **NIST SP 800-61 Rev. 3** (csrc.nist.gov/pubs/sp/800/61/r3/final) — *read* the incident-response lifecycle framing; *note* it is now a CSF 2.0 Community Profile (April 2025), not the old four-phase playbook — the structure changed and the old summaries are stale.
- **NIST SP 800-92, Guide to Computer Security Log Management** (2006, via doi.org/10.6028/NIST.SP.800-92) — *read* the log-management infrastructure functions and challenges (volume, immutability, inconsistent formats, retention); *note* the r1 draft status before citing anything newer.
- **MITRE ATT&CK Enterprise tactics** (attack.mitre.org/tactics/enterprise/) — *read* the 15 tactics; *note* v19.2 split Defense Evasion into **Stealth** (hide actions) and **Defense Impairment** (break the defenders' tooling) — any 14-tactic list you find is stale.

Then at most three free resources:

1. **MITRE, *11 Strategies of a World-Class Cybersecurity Operations Center*** (mitre.org — free download, 20-page summary plus the full book) — the SOC operator's field manual. Read the 20-page summary first; then strategy 5 (prioritize incident response) and strategy 7 (select and collect the right data), which are this lesson's enrichment and scoping in the wild. Skip the staffing and structure chapters until you manage a SOC.
2. **Wazuh** (wazuh.com) — free, open-source XDR: agents, manager, dashboard. The lab where you practice this lesson against real telemetry from your own VMs.
3. **Security Onion** (securityonion.net) — free network security monitoring distro (Zeek + Suricata + Sigma-based detection). The lab where the network half of triage lives.

## 8. Check yourself

1. An alert fires: impossible travel for a service account, both sign-ins non-interactive. Walk the decision tree and explain which branch closes it — and what tuning feedback you would send the rule owner.
2. Explain the difference between severity and priority, and construct a case where a *critical*-severity alert is *low* priority and a *medium*-severity alert is *high* priority.
3. You find the same suspicious domain in DNS logs on one host. Before classifying, what is the single most important question to answer, and what two different handlings follow from its two answers?
4. A host beacons every 60 seconds with CV 0.03 for 14 hours, then the response sizes spike tenfold for three minutes. Explain what changed in your assessment and what you recommend now.
5. Your triage note says "looks fine, closed." Explain what is missing from this note and why the next analyst — or an auditor — cannot use it.

## 9. Prove it

**Artifact:** the two invented cases from §5 — the event JSON, the decision-tree branch that decided each, and the triage notes in *seen / checked / decided / evidence* format — presented as the handoff you would give a Tier 2 analyst. The five walkthrough notes were the practice set; the two invented cases are the proof: they must exercise branches the walkthrough didn't use, and a stranger must be able to see which branch decided each without asking you.

**Honest claim:** "I can take a SOC alert, apply a decision tree, classify it into the five buckets, and write a triage note another analyst can act on without redoing my work."
**Can't claim yet:** "I can run incident response" — containment, eradication, and recovery belong to IR (`c-incident-response`); triage recommends, it does not act.

## 10. Leads to

- `c-log-sources` — the telemetry each triage branch reaches for: know what every source sees before you pivot into it.
- `c-sigma-detection` — the other side of the alert: how the rule that paged you was written, and how your close codes tune it.
- `c-incident-response` — where the escalated cases go: the IR lifecycle that starts where triage ends.
- Map refs: **Stage C · Professional**; NICE **Protection and Defense** work roles; the `/r/soc-analyst/` path.
