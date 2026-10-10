---
lesson_id: e-network-architecture
slug: network-architecture
stage: E
level: 3
prerequisites: [a-tcpip-ports]
roles: []
map_refs: ["CISSP 4.1"]
test_date: 2026-10-10
description: "Design network zones, trust boundaries, and zero-trust enforcement for a fictional manufacturer. A free lesson in the security guidebook, serving CISSP objective 4.1."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Network architecture: drawing the lines attackers must cross


**Map ref:** serves **CISSP objective 4.1** — secure network architecture design. (Objectives 4.2 and 4.3 are the companion lessons `e-network-components` and `e-secure-channels`.)

---

## 1. Where this shows up

`a-tcpip-ports` taught you the mechanism: what a packet carries and what a firewall rule matches. This lesson is the decision layer above it: which boundaries a network should have, where each one sits, what crosses it, and why. It shows up in every architecture review ("why is the vendor VPN allowed into the same VLAN as the domain controllers?"), every incident where lateral movement turned one compromised workstation into a company-wide event, and every design document that has to place NAC, firewalls, and monitoring before anyone buys hardware. Security architects and network security engineers own these drawings — and defend them against the two enemies of good segmentation: convenience and budget.

## 2. Before you start

- You can read a packet and a firewall rule (`a-tcpip-ports`) — this lesson never explains ports again; it decides where the rules live.
- Bring the discipline of writing decisions with owners and dates. A segmentation diagram without a decision log is decoration.
- No tools. The work product is a design review document for a fictional company.

## 3. How it works

A network is not one thing; it is a set of **zones** separated by **trust boundaries**. A zone is a group of systems that share a trust level and a policy — corporate workstations, the data-center server tier, the factory floor, the guest Wi-Fi. A trust boundary is the line between zones where trust changes and policy is enforced: traffic crossing it is inspected, filtered, logged, and denied by default. The entire discipline is deciding where those lines go and what crosses them.

**Segmentation is containment, not prevention.** No boundary stops a determined attacker forever. What segmentation buys is *blast radius control*: the compromised printer should not reach the payroll database. That is why the design question is never "is this network secure" but "when (not if) something inside is hostile, what can it reach?" Draw every path a compromised asset in each zone could take to the company's crown jewels, and the missing boundaries reveal themselves.

**Mechanisms, from coarse to fine.** VLANs carve a switch into separate broadcast domains — useful for organizing traffic, but a VLAN tag is not a security boundary by itself; inter-VLAN traffic must pass through a firewall or router with policy. **Firewalls** between zones enforce that policy: default deny, explicit allows, stateful connection tracking. **Micro-segmentation** pushes policy to the workload or host — each server enforces its own allow-list — which is how you segment east-west traffic (server-to-server traffic inside the network, as opposed to north-south traffic entering or leaving it) a perimeter firewall never sees. **NAC (network access control)** decides *before* connectivity: a device authenticating to the network (typically via 802.1X — the IEEE standard for port-based network access control, the protocol by which a switch asks a device to authenticate before granting connectivity) is identified, posture-checked, and placed in the right zone or quarantined. NAC is the bouncer; the firewall is the wall.

**Zero trust, per NIST SP 800-207.** The modern statement of the architecture: trust is never granted by network location; it is evaluated per session, per resource. SP 800-207 (August 2020) states seven tenets — every resource treated as a resource (no implicit zones of trust), all communication secured regardless of location, per-session grants with least privilege (because trust decays: a grant evaluated once and trusted forever is a standing opportunity — per-session grants re-check the decision while the context is current), access determined by dynamic policy (identity, asset state, behavior, environment), continuous monitoring of asset posture, dynamic authentication and authorization before every access, and collection of state data to improve policy. The logical components: the **policy engine** (makes the grant/deny decision), the **policy administrator** (executes it), the **policy enforcement point** (the PEP — in the traffic path, enforcing), and the **trust algorithm** (the decision function consuming identity, posture, behavioral and environmental attributes). Deployment varies — device agent/gateway, enclave-based, resource portal — but the principle is constant: the network is transport, and access decisions are explicit and continuous.

**The DMZ and the management plane.** Internet-facing services live in a **DMZ**: reachable from the internet, but not trusted by the interior — the firewall between DMZ and inside is as strict as the one facing the internet. The **management network** — the interfaces you use to administer firewalls, switches, and hypervisors — is its own zone, reachable only from admin workstations over encrypted, authenticated channels. It gets its own zone because the management plane is the highest-value target on the network: whoever can administer the firewalls owns every zone those firewalls enforce.

**Third-party connectivity** is where segmentation designs die. Vendors need access — to the HVAC controller, the CNC line, the SaaS integration. The architecture answer: vendors never join your zones. They land in an isolated vendor segment (a jump host or bastion in the DMZ — a hardened, session-recorded machine you log into first, the only door into the restricted zone), authenticate strongly, get time-bounded access to exactly the named systems, and every session is logged. The flat vendor VPN — "they needed access, so we gave them the same VPN as employees" — is how a compromised vendor becomes a compromised enterprise.

**Remote access and monitoring points.** The VPN concentrator (the appliance that terminates many remote users' VPN tunnels in one place) sits at the edge, in front of the interior firewall, and remote users land in a zone of their own — filtered like any other untrusted source, then posture-checked. The design also places **monitoring**: IDS/IPS sensors and packet-capture points at zone boundaries (full detail in `e-network-components`), because a boundary you cannot see across is one you cannot prove is working.

**AI training environments** get micro-segmentation: GPU clusters hold the company's most valuable data (training sets, model weights) and generate east-west traffic perimeter tools never inspect. The cluster's zone permits only the training workflow's communication paths — and treats an unexpected outbound connection from a training job as the primary threat to design against.

### The design method (SP 800-207 §7.3, adapted)

NIST's migration steps read as a design checklist: identify the actors (who and what needs access), identify the assets (what must be protected), identify key processes and their risks, formulate the access policies, then identify candidate solutions. In practice: inventory first, draw the current flat reality, propose zones from data sensitivity and blast radius, place enforcement at each boundary, and record every decision — including the ones you deferred.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the segmentation design review below, authored and self-reviewed in-session on 2026-10-10 against SP 800-207's structure. Transcript: `runs/e-network-architecture.log`.

**The company (fictional).** Harborlight Manufacturing: 450 employees, two plants, a corporate HQ. Today the network is flat — one large address space, the firewall only at the internet edge, plant-floor controllers reachable from any workstation, vendors on the employee VPN.

**Step 1 — inventory and current state.** Actors: employees, plant operators, maintenance vendors, remote engineers, the R&D team training defect-detection models on a GPU cluster. Assets: ERP and payroll, CNC controllers and PLCs, engineering file shares, the training dataset and model weights, customer order data. Headline finding: a compromised workstation can reach the PLCs — no trust boundary exists between corporate IT and the plant floor.

**Step 2 — the zone map.** Eight zones: (1) Corporate user zone, (2) Data-center services, (3) DMZ (public web, customer portal), (4) Plant OT zone (controllers, HMIs — no internet path), (5) R&D/AI training zone (GPU cluster, dataset storage), (6) Management zone (admin interfaces of every network device), (7) Guest Wi-Fi (internet only), (8) Vendor access segment (jump hosts, isolated). Each zone gets a one-line trust statement: e.g., "OT zone: trusted devices, untrusted traffic — every flow crossing its boundary is explicitly allowed or denied."

**Step 3 — trust boundaries and enforcement.** Boundary table (excerpt): Corporate→Data-center: firewall, default deny, only the application's required ports; DMZ→Interior: firewall, deny all initiated from DMZ inward except the portal's database replica pull through a dedicated proxy; Corporate→OT: firewall, deny by default, allow only the historian server's (the server that collects and archives plant-floor data) read-only feed *out* of OT and two named engineering workstations *in* via jump host; AI zone→anywhere: deny all except training-data ingest from the labeled source and artifact export through the artifact repository — no direct internet; Management zone: reachable only from admin workstations, MFA'd, encrypted.

**Step 4 — zero-trust decisions per tenet.** Per-session grants for the OT jump host (no standing vendor access — tenet 3); device posture checks on the corporate NAC before data-center access (tenet 5); all inter-zone traffic encrypted where the protocol allows, authenticated everywhere (tenet 2); the trust algorithm's inputs named per zone (tenet 4): user identity + device certificate + patch posture for corporate; service identity + workload attestation for the AI cluster.

**Step 5 — NAC placement.** 802.1X on all wired access ports and corporate Wi-Fi: unknown devices land in quarantine (internet only, remediation portal); known devices are profiled into the corporate zone. Printers and other non-802.1X devices go through MAC-based exception with a documented inventory — each exception named, not a blanket bypass.

**Step 6 — vendor and remote access.** Vendors: VPN into the vendor segment only, MFA, time-bounded tickets, jump host with session recording to the named OT asset. Remote engineers: VPN concentrator at the edge, posture check, landing in a remote-access zone filtered identically to the vendor segment — location grants nothing.

**Step 7 — monitoring points and the decision log.** IDS sensors on SPAN feeds (a SPAN port is a switch port configured to copy traffic to a sensor) at: internet edge, DMZ boundaries, OT boundary, AI-zone boundary. Every allow/deny at a trust boundary logs to the SIEM (the central log platform — see `e-logging-monitoring`) (your `c-log-sources` lesson names what to collect). The design states the detection goal per sensor: edge = inbound attack, OT boundary = any unexpected flow (the OT allow-list is small enough that *any* anomaly is notable), AI zone = outbound anomalies. Finally, the decision log: each boundary decision records what was decided, why, owner, date, and what was deferred (e.g., "micro-segmentation inside the data center deferred to phase 2 — owner: network lead, revisit 2027-Q1"). Deferred items with owners and dates are plans; without them, holes.

## 5. On your own

**Task:** Draw the zone map and boundary table for a network you know — your home lab, your employer's (from memory, unclassified), or a fictional company of your invention. Minimum: five zones, every trust boundary named with its enforcement mechanism, NAC placement decided, and a vendor-access design.

**Success test:** For each zone, you can name one compromised asset inside it and list exactly what it can and cannot reach — with the firewall rule or NAC policy that enforces each answer. Any "it probably can't" without a named enforcement point is a gap in your design, not in the attacker's.

## 6. Where it goes wrong

- **The flat network with a strong perimeter.** The firewall at the edge is excellent and irrelevant once the attacker is inside — which phishing guarantees eventually. Perimeter-only is the architecture ransomware loves.
- **VLANs mistaken for security boundaries.** VLANs organize; firewalls enforce. Inter-VLAN routing with "allow all" is a flat network wearing a costume. The tell is in the router config: the inter-VLAN access list is empty or ends in permit-any — the reviewer reads it, not the diagram.
- **The DMZ that trusts inward.** A web server in the DMZ with an open path to the interior database "for performance" is just an internet-facing interior server.
- **Firewall rule sprawl.** Ten years of "temporary" any-any rules nobody owns. Every rule needs an owner and a review date or it becomes permanent.
- **NAC in monitor-only mode forever.** Deployed, never enforced, because enforcement might break something. A control that is never enforced is a monitoring project with a NAC price tag.
- **Third-party flat access.** The vendor VPN that lands vendors in the employee zone. Compromise the vendor, inherit their access.
- **Unencrypted east-west traffic.** "It's inside the firewall." The firewall never sees host-to-host traffic in the data center; the sniffer on the compromised hypervisor does.
- **Zero trust as a product purchase.** Tenets are architecture decisions, not a SKU. Buying a "zero trust" appliance while the vendor VPN stays flat is theater.

## 7. Read the source

Primary documents first:

- **NIST SP 800-207, Zero Trust Architecture** (csrc.nist.gov, August 2020) — *read* §2.1 (the seven tenets — the vocabulary of the whole discipline), §3 (logical components: policy engine/administrator/enforcement point, the trust algorithm, deployment models); *read* §7.3 (the migration steps — the design checklist this lesson adapts); *skim* §4 (deployment scenarios, including contracted/nonemployee access).
- **NIST SP 800-207's deployment scenarios** are the closest thing to worked examples in the standard — match your company's shape to one of them before inventing your own.

Then at most three free resources:

1. **CISA: Layering Network Security Through Segmentation** (cisa.gov, infographic) — free; the one-page visual of the zone model to check your diagram against.
2. **CISA: Zero Trust Maturity Model** (cisa.gov) — free; the roadmap view: where an organization sits today and what the next step costs in effort.
3. **NSA: Network Infrastructure Security Guidance** (March 2022; mirrored PDF) — free; the hardening companion to this lesson's architecture — segmentation plus device hardening, written for network administrators.

## 8. Check yourself

1. A flat network has an excellent edge firewall and gets ransomwared through a phishing email. Explain, using the blast-radius frame, why the edge firewall's quality was irrelevant — and name the single boundary whose absence mattered most.
2. Compare what a VLAN provides versus what a firewall between zones provides. An engineer says "we segmented with VLANs, so we're done." What is missing, concretely?
3. A maintenance vendor needs weekly access to one PLC. Design the access (segment, authentication, bounds, logging) and explain why "add them to the employee VPN" fails the per-session, least-privilege tenets.
4. The R&D GPU cluster trains on proprietary data and a training job opens an outbound connection to an unknown host. Which boundary and which monitoring point catches this, and what does the boundary's policy say about the flow?
5. Predict the state of a firewall ruleset five years after the architect who wrote it leaves, if no rule has an owner or review date. Which class of rule accumulates, and what incident reveals it?

## 9. Prove it

**Artifact:** your segmentation design review — current-state findings, zone map with trust statements, boundary table (each boundary: enforcement mechanism, default posture, named exceptions), NAC placement decision, vendor and remote-access design, monitoring points with detection goals, and the decision log with owners and dates — for the Harborlight worked case in your own words, or better, for a real network you know.

**Honest claim:** "I can design a network's trust boundaries and defend each one — I can say what each zone contains, what crosses each boundary, what enforces it, and what a compromise in any zone can reach."
**Can't claim yet:** "I can implement and operate this network" — device configuration, firewall rule authoring, and NAC tuning are their own engineering work; this lesson taught the architecture decisions those implementations must satisfy. (`e-network-components` is the hardening companion.)

## 10. Leads to

- `e-network-components` — the hardening companion: what each device at your boundaries must look like.
- `e-secure-channels` — the traffic companion: which encrypted channel each inter-zone and remote flow should use.
- `a-tcpip-ports` — the mechanism layer under every boundary decision here.
- `c-log-sources` — what each monitoring point feeds the SIEM.
- Map refs: **CISSP 4.1** (this lesson); feeds **CISSP 4.2** (components), **4.3** (channels), and **7.7** (operating the detective measures your boundaries host).

---

*Sources fetched 2026-10-10: NIST SP 800-207 (csrc.nist.gov/pubs/sp/800/207/final); CISA Layering Network Security Through Segmentation; CISA Zero Trust Maturity Model; NSA Network Infrastructure Security Guidance (Mar 2022). Full ledger in the batch manifest.*
