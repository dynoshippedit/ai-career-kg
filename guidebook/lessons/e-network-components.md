---
lesson_id: e-network-components
slug: network-components
stage: E
level: 3
prerequisites: [e-network-architecture, a-tcpip-ports]
roles: []
map_refs: ["CISSP 4.2"]
test_date: 2026-10-10
description: "Harden firewalls, IDS/IPS, switches, wireless, and NAC with placement rationale for a fictional manufacturer. A free lesson in the security guidebook, serving CISSP objective 4.2."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Network components: hardening everything the architecture trusts


**Map ref:** serves **CISSP objective 4.2** — securing network components.

---

## 1. Where this shows up

The architecture lesson drew the boundaries; this lesson hardens the devices that enforce them. A firewall with an any-any rule, an IDS sensor watching the wrong interface, a switch with default credentials, a wireless network that hands the keys to the parking lot — each is a component failure that voids the architecture. It shows up in hardening reviews ("show me the firewall ruleset review from last quarter"), in wireless assessments, and in every incident where the sensor that should have seen the attack was misconfigured, unpatched, or never deployed. Network security engineers and the SOC analysts who depend on their feeds live here.

## 2. Before you start

- You have a zone map (yours or Harborlight's from `e-network-architecture`) — every placement decision below references it.
- You understand what firewall rules match (`a-tcpip-ports`).
- No tools. The work product is a component-hardening review document.

## 3. How it works

Every network component falls into one of three jobs: **enforce** (decide what passes), **detect** (see what passed), or **transport** (carry traffic faithfully). Hardening means making each do its job and nothing else — disabling what is unnecessary, authenticating what is administrative, and logging what is security-relevant. The principle from the architecture lesson carries over: the component is only as trustworthy as its own configuration, and the management plane is the highest-value target on the device.

**Firewalls: the enforcement points.** A firewall's job is the boundary table made real: default deny, explicit allows, stateful tracking of connections so return traffic is recognized rather than re-permitted. Default deny is the fail-safe posture: unknown traffic is blocked, so the attacker's novelty works against them. A blocklist fails open — anything you forgot to name is allowed, and attackers specialize in the unnamed. The review discipline (per NIST SP 800-41 Rev. 1, Guidelines on Firewalls and Firewall Policy): the ruleset is reviewed against the policy it claims to implement — every rule traceable to a business need, ordered so the specific precedes the general (firewalls match top-down and stop at the first match — a general rule above silently swallows the specific rule below), with no shadowing (a broad rule above that makes a narrow rule below dead), no any-any allows (a rule permitting any source to any destination on any port — the widest possible opening) except named and justified, and logging on the denies so the firewall is also a sensor. The review's output is a list, not a feeling: rules with no owner, rules with zero hits in twelve months, any-any allows — each a finding. The management interface lives in the management zone, reachable only from admin workstations over encrypted, authenticated channels — a firewall whose admin page is reachable from the user LAN is a firewall waiting to be reconfigured by someone else. Rule changes go through the change process (`e-security-audits` will audit exactly this): request, approval, implementation, verification.

**IDS/IPS: the detection layer.** An IDS sees and alerts; an IPS sees and blocks — the same sensor, different courage. NIST SP 800-94 (Guide to Intrusion Detection and Prevention Systems) frames the placement question, and placement is the whole game: a sensor outside the edge firewall sees the internet's background noise; a sensor inside sees what got through; a sensor on a SPAN feed (a switch port configured to copy traffic to the sensor) at a trust boundary sees exactly the crossing traffic the boundary table governs. The worked case places sensors where the architecture lesson's monitoring points went — the detection goal per sensor named in advance, because a sensor without a stated detection goal produces alerts nobody triaged. Signatures catch the known; anomaly detection catches the deviation — the OT boundary's tiny allow-list makes anomaly detection practical there (any unexpected flow *is* the alert), while the internet edge needs signatures to survive the noise. The IPS decision — block or alert-only — is risk, not technology: block where the false-positive cost is low (known-malicious indicators), alert where blocking breaks the business (the plant floor).

**Routers and switches: the transport, hardened.** These devices are computers with a forwarding job, and they get the server-hardening treatment: unused ports administratively disabled, unused services off (no telnet, no HTTP admin, no discovery protocols leaking topology beyond need), strong authentication on every administrative path, configuration backups tested by restore, and firmware patched on a schedule — a switch running five-year-old firmware is a firewall with extra steps and fewer logs. Separation matters: management traffic on the management VLAN/zone, never in-band (riding the same network path as user traffic) with user data; control-plane protections so the device's own CPU cannot be drowned by data-plane floods.

**Wireless: the boundary you cannot see.** Wireless extends a trust zone into the parking lot, so it gets its own policy (per NIST SP 800-153, Guidelines for Securing Wireless Local Area Networks): strong authentication for corporate SSIDs (the network names devices see and join; enterprise mode — per-user credentials via the NAC/RADIUS path, where RADIUS is the authentication protocol the access point or switch uses to check credentials against the directory — not a shared passphrase on a sticky note), a separate guest SSID tunneled straight to the internet with no interior path, rogue access-point detection (an employee's "helpful" personal AP bridged to the corporate LAN voids every boundary), and physical awareness — signal does not respect the building's walls, so the policy does. The review asks: who can join, what zone do they land in, and what would a parking-lot attacker get?

**NAC as a component** (placed in the architecture lesson, hardened here): the policy server's own availability is load-bearing — if NAC fails closed, the business stops; if it fails open, the boundary vanishes. The design states the failure mode deliberately, the policy server is redundant, and the exception inventory (devices that cannot do 802.1X) is reviewed, not grandfathered.

### Worked example: Harborlight Manufacturing — component-hardening review (fictional, continued)

**Scope.** Every enforcement and detection component on the Harborlight zone map: two edge firewalls (an HA — high-availability — pair, where the second takes over if the first fails), three inter-zone firewalls, the VPN concentrator, four IDS sensors, 60 switches, the wireless controllers, and the NAC policy servers.

**Findings (fictional, labeled).**

1. **Edge firewall ruleset drift.** 214 rules; 31 have no owner, 6 are any-any allows added as "temporary" between 2022 and 2024. *Decision: named owners assigned within 30 days; any-any rules either justified in writing with expiry or removed — the change process from now on requires an expiry date on every temporary rule.*
2. **IDS sensor misplacement.** The "DMZ sensor" is on a SPAN port that only sees post-firewall DMZ traffic — it cannot see the internet→DMZ attacks the firewall blocked, which was its stated detection goal. *Decision: re-mirror to the pre-firewall tap; detection goal rewritten to match what the sensor actually sees.*
3. **Switch management in-band.** Forty switches managed over the user VLAN with default SNMP community strings (the shared passwords devices use for monitoring; the defaults are public knowledge) still present. *Decision: migrate management to the management zone; rotate all credentials; disable SNMP v1/v2.*
4. **Wireless guest bridge risk.** The guest SSID is tunneled correctly, but two conference-room APs were found in bridge mode from a 2023 install, giving wireless clients a path to the corporate LAN. *Decision: reconfigure; add AP-mode audit to the quarterly wireless review.*
5. **NAC exception rot.** 47 MAC-bypass exceptions; 19 are devices decommissioned in 2024. *Decision: purge; exceptions now expire after 180 days unless re-justified.*
6. **IPS on the plant boundary in block mode without a bypass plan.** A false positive could halt the historian feed the business depends on. *Decision: alert-only on the OT boundary with a 24-hour analyst SLA; block mode only on the internet edge for known-malicious indicators.*

**Review close-out:** each finding has a decision, owner, and date; the next ruleset review is quarterly, the wireless and NAC reviews semi-annual. The review is the artifact the auditor asks for — and the mechanism that keeps the architecture honest.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the component-hardening review above, authored and self-reviewed in-session on 2026-10-10 against SP 800-41 Rev. 1, SP 800-94, and SP 800-153. Transcript: `runs/e-network-components.log`.

1. **Inventory the components.** From the zone map, list every enforcement, detection, and transport device — including the ones nobody owns (the conference-room APs from 2023 are always the find).
2. **Review each firewall ruleset against the boundary table.** Every rule needs a business reason, an owner, and correct ordering. Flag shadowing, any-any, and expired temporaries. The ruleset that implements the architecture is a document; the ruleset that drifted from it is the finding.
3. **Verify sensor placement against detection goals.** For each IDS/IPS sensor, write what it should see and confirm the tap/SPAN actually delivers that traffic. A sensor whose feed doesn't match its goal is a finding, not a control.
4. **Harden the transport.** Sample switches and routers: unused ports, unused services, management-plane separation, credential hygiene, firmware age, config-backup restorability. One device audited deeply beats ten glanced at.
5. **Review wireless as a boundary.** SSID inventory, authentication mode per SSID, zone each SSID lands in, rogue-AP detection status, and the physical question: what does the parking lot get?
6. **Decide the NAC failure mode in writing.** Fail closed or fail open, with the business impact of each stated and the redundancy that makes the choice survivable.
7. **Close out.** Findings with decisions, owners, dates; review cadence per component class.

## 5. On your own

**Task:** Run a component review on a network you control — home lab counts. Inventory every device, review one firewall ruleset rule-by-rule against what you believe the policy is, check where your IDS (or logging) actually sees, and audit your wireless.

**Success test:** You find at least one rule you cannot justify, one device with a default or stale credential, and one monitoring blind spot. If your network is perfect, your review was not.

## 6. Where it goes wrong

- **Ruleset archaeology.** Nobody knows why rule 47 exists, so nobody removes it. Every rule without an owner is a future incident's attack path.
- **The sensor facing the wrong way.** Mirrored the wrong interface, filtered at the tap, or watching post-NAT traffic (NAT — network address translation — rewrites source addresses, so the sensor sees the gateway's address instead of the real client's) it cannot attribute. Placement is verified, not assumed.
- **IPS block mode on the wrong boundary.** Blocking where false positives halt the business teaches everyone to disable the IPS — then nothing is blocked anywhere.
- **Default credentials on infrastructure.** The switch, the AP controller, the UPS management card. Attackers enumerate infrastructure first because it is rarely patched and often default.
- **Wireless as the forgotten boundary.** The guest network audited once at install, never again. Bridge-mode APs and rogue APs accumulate silently.
- **Management plane in the data plane.** Admin interfaces reachable from user networks. Compromise one workstation, reconfigure the firewall.
- **Firmware as technical debt.** Five-year-old switch firmware with known vulnerabilities, "because it still works." It works for the attacker too.
- **NAC exceptions as permanent bypasses.** The exception inventory only grows. Every exception is a device the NAC never sees — review them like the holes they are.

## 7. Read the source

Primary documents first:

- **NIST SP 800-41 Rev. 1, Guidelines on Firewalls and Firewall Policy** (csrc.nist.gov) — *read* the firewall policy and ruleset management guidance; this is the document firewall reviews are graded against.
- **NIST SP 800-94, Guide to Intrusion Detection and Prevention Systems (IDPS)** (csrc.nist.gov) — *read* the placement and deployment considerations; *skim* the technology taxonomy.
- **NIST SP 800-153, Guidelines for Securing Wireless Local Area Networks** (csrc.nist.gov) — *read* as the wireless review checklist.

Then at most three free resources:

1. **NSA: Network Infrastructure Security Guidance** (March 2022; mirrored PDF) — free; the device-hardening companion: what each component's configuration should look like.
2. **CISA: Zero Trust Maturity Model** (cisa.gov) — free; the device-identity and visibility pillars, for placing component hardening on the roadmap.
3. **CIS Benchmarks** (cisecurity.org) — free; the measurable hardening checks per device class — the review's evidence base.

## 8. Check yourself

1. A firewall ruleset has 300 rules, 40 without owners, and a broad allow above a narrow deny. Explain the two distinct failures (governance, ordering) and the review discipline that catches each.
2. An IDS sensor's stated goal is "detect inbound attacks against the DMZ," but it sits on a post-firewall SPAN. What does it actually see, what is it blind to, and where should the tap be?
3. The plant-floor IPS is in block mode. Argue for and against block mode on that specific boundary — what does a false positive cost here versus at the internet edge?
4. Two conference-room APs are found in bridge mode, giving wireless clients a path to the corporate LAN. Which trust boundary did this void, and what does the fix's verification look like?
5. NAC fails. Compare fail-closed versus fail-open: who is harmed by each, what redundancy changes the calculus, and why must the choice be written down before the failure?

## 9. Prove it

**Artifact:** your component-hardening review — device inventory, firewall ruleset review against the boundary table (every unjustified rule a finding), sensor placement verification against detection goals, switch/router hardening sample, wireless review, NAC failure-mode decision — each finding with a decision, owner, and date, for the Harborlight worked case in your own words or a network you control.

**Honest claim:** "I can review every component a network architecture depends on — I can verify each firewall rule against policy, each sensor against its detection goal, and each device against a hardening baseline, and drive findings to decisions."
**Can't claim yet:** "I can configure and tune these devices at enterprise scale" — rule authoring, IDS tuning, and wireless design are engineering disciplines; this lesson taught the review that keeps them honest.

## 10. Leads to

- `e-network-architecture` — the zone map this lesson's review defends; reread it as the "why" behind every placement here.
- `e-secure-channels` — the encrypted channels whose endpoints these components protect.
- `c-log-sources` — what each hardened component should log, and where those logs go.
- `a-tcpip-ports` — the mechanism layer every rule review here depends on.
- Map refs: **CISSP 4.2** (this lesson); feeds **CISSP 4.1** (architecture) and **7.7** (operating detective and preventive measures).

---

*Sources fetched 2026-10-10: NIST SP 800-41 Rev. 1, SP 800-94, SP 800-153 (csrc.nist.gov); NSA Network Infrastructure Security Guidance (Mar 2022); CISA Zero Trust Maturity Model; CIS Benchmarks. Full ledger in the batch manifest.*
