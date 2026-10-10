---
lesson_id: e-secure-channels
slug: secure-channels
stage: E
level: 3
prerequisites: [a-http-depth, e-network-architecture]
roles: []
map_refs: ["CISSP 4.3"]
test_date: 2026-10-10
description: "Select TLS, VPN, SSH, and messaging channels per traffic class with written rationale for a fictional manufacturer. A free lesson in the security guidebook, serving CISSP objective 4.3."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Secure channels: which encrypted path for which traffic, and why


**Map ref:** serves **CISSP objective 4.3** — secure communication channels.

---

## 1. Where this shows up

Every architecture has traffic that must cross untrusted space: the remote engineer reaching the data center, the branch office reaching HQ, the web app reaching the payment processor, the administrator reaching the switch. Each crossing needs a channel — an encrypted, authenticated path — and the choice is an architecture decision with real consequences: the wrong channel leaks metadata, breaks under the wrong failure, or quietly downgrades to something weaker. It shows up in design reviews ("why is this over the internet at all?"), in VPN consolidation projects, and in incident reports where the attacker didn't break the encryption — they found the traffic that wasn't encrypted. This is the selection view: not the handshake's mathematics (`a-http-depth`, `e-crypto-applied`), but the judgment of which channel, for which traffic, and why.

## 2. Before you start

- You know the TLS handshake's steps (`a-http-depth`) and the zone map (`e-network-architecture`) — this lesson assigns a channel to every inter-zone and remote flow on it.
- No tools. The work product is a channel-selection rationale for a fictional company.

## 3. How it works

A **secure channel** provides three properties over untrusted transport: **confidentiality** (no eavesdropper reads it), **integrity** (no tampering undetected), and **authentication** (each endpoint knows who the other is). Every channel below provides all three when configured correctly — the selection question is never "encrypted or not" but *which* channel fits the traffic's shape: who the endpoints are, what network lies between, what failure looks like, and what the endpoints can actually run.

**TLS: the channel for application traffic.** TLS (current version 1.3, RFC 8446, August 2018) is the channel between applications — browser to server, service to service, app to API. Its properties matter to the selector: handshake messages after the ServerHello are encrypted (less metadata leaks than 1.2), forward secrecy is standard (a stolen server key does not decrypt past sessions), and a 0-RTT mode exists for resumption — fast, but replayable, so the selection decision restricts 0-RTT to idempotent requests (idempotent: an operation safe to repeat — same result whether it runs once or twice). The replay property is the reason: anyone who captures 0-RTT data can re-send it, and the server cannot distinguish the replay from the original — so only requests that are harmless when executed twice may use it. The architecture decision with TLS is *where it terminates*: TLS to a load balancer means plaintext inside the data center — acceptable only if the interior zone is genuinely trusted (it isn't; see the east-west lesson in `e-network-architecture`), so sensitive flows terminate TLS at the application or use mutual TLS (both endpoints present certificates and authenticate each other — not just the server proving itself to the client) between services. Certificate management is the operational half of the decision: expiry monitoring, automated renewal, and a private CA or public CA choice with reasons — the most common TLS failure is not cryptanalysis but an expired certificate on a Sunday.

**VPNs: the channel for network traffic.** When whole networks or devices must behave as adjacent, the channel is a VPN — and the type follows the endpoints:

- **IPsec site-to-site** (per NIST SP 800-77, Guide to IPsec VPNs): gateway to gateway, the branch office's LAN joined to HQ's. The architecture decision: which traffic enters the tunnel (interesting-traffic selectors), where the gateways sit (in front of the interior firewall, in the DMZ's edge), and what happens when the tunnel drops (fail closed or spill to the internet — stated in advance).
- **Remote-access VPN** (per NIST SP 800-113, Guide to SSL VPNs): device to gateway, the traveling engineer joining the network. The decision here is posture: the concentrator authenticates the user *and* checks the device before granting the zone access the architecture lesson designed — the VPN is the on-ramp to the remote-access zone, not a tunnel past the firewall.
- **WireGuard-style modern tunnels** for the cases where simplicity is the security feature: fewer options, less to misconfigure, small attack surface. The selection rationale names it where operational simplicity outweighs IPsec's flexibility.

The persistent VPN failure mode is the flat tunnel: the site-to-site link that carries every VLAN, the remote-access VPN that lands users in the interior. The channel is encrypted; the architecture is not.

**SSH: the channel for administration.** Administrator to device — switches, servers, jump hosts. SSH provides the encrypted shell and file transfer, but the selection decisions are key management (no password authentication on infrastructure; keys issued, tracked, and revoked per the authenticator lifecycle in `e-auth-systems`) and the jump-host topology (administrators reach the management zone only through the bastion, whose sessions are logged). SSH agent forwarding through the bastion is the classic footgun (a feature that makes it easy to shoot yourself in the foot) — the key that unlocks everything, forwarded to a host you just logged into. The danger is delegation: the forwarded agent lets that host authenticate as you for as long as the session lasts — compromise the bastion and the attacker borrows your keys everywhere they work.

**Messaging and email: the channel for people.** Person-to-person traffic needs end-to-end encryption where the content matters: the property to select for is that the *service provider* cannot read it, not just the network eavesdropper. The architecture decision is which conversations require it (incident response coordination, executive communications, anything crossing untrusted networks with sensitive content) and the key-verification discipline that makes it real (verified safety numbers — the key fingerprints users compare out-of-band to confirm no one tampered with the exchange — not just the padlock icon). Email's store-and-forward reality means encryption at the message layer for the sensitive classes, with the key-management burden stated honestly.

### The selection method

For each traffic class: name the endpoints, the networks crossed, the channel selected, the properties required (and which the channel provides), the termination points, the failure mode (what happens when the channel is unavailable — fail closed or open, by decision), and the operational burden (certificates, keys, tunnel monitoring). A traffic class without a named channel is unencrypted by default — the inventory is the control.

### Worked example: Harborlight Manufacturing — channel selection (fictional, continued)

**Traffic inventory (excerpt).**

| Traffic | Endpoints | Networks crossed | Channel selected | Rationale |
|---|---|---|---|---|
| Customer portal | Browser → web tier | Internet | TLS 1.3, terminating at the app servers (not the load balancer) | Interior zone untrusted; mutual TLS between web and app tiers |
| Branch plant link | Plant gateway → HQ gateway | Internet | IPsec site-to-site, fail closed | Whole-LAN adjacency needed; selectors limited to plant/HQ subnets, not the guest VLAN |
| Remote engineers | Laptops → concentrator | Internet | Remote-access VPN with device posture check | On-ramp to the remote-access zone only; split tunneling (letting the VPN client send some traffic straight to the internet instead of through the tunnel) denied for engineering (all traffic inspected) |
| Vendor maintenance | Vendor laptop → jump host | Internet | TLS to the jump host, then SSH to the PLC | No network-level adjacency for vendors — application-level session, recorded |
| Admin to switches | Admin workstation → devices | Management zone | SSH, key-only auth, via bastion | Management zone is trusted transport but SSH still required — defense in depth, and sessions logged at the bastion |
| OT historian feed | Historian → data-center DB | Inter-zone | TLS with mutual authentication | Even "internal" crossings get channels; the OT boundary's allow-list names this flow explicitly |
| Incident response chat | Responders' devices | Any | End-to-end encrypted messaging, verified keys | Coordination during an incident is the highest-value traffic to intercept |

**Decisions recorded:** 0-RTT disabled for the portal's state-changing endpoints (replay risk); TLS 1.2 retained only for the legacy vendor integration with a dated deprecation plan and owner; the IPsec fail-closed decision signed off by operations with the documented outage procedure for tunnel loss.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the channel-selection rationale above, authored and self-reviewed in-session on 2026-10-10 against RFC 8446, SP 800-77, and SP 800-113. Transcript: `runs/e-secure-channels.log`.

1. **Inventory the traffic.** From the zone map, list every flow that crosses a trust boundary or untrusted network — including the ones nobody thought of (the historian feed, the backup replication, the printer's scan-to-email).
2. **Classify each flow.** Endpoints, networks crossed, sensitivity, and what failure looks like. The classification drives the selection; unclassified traffic gets the strongest channel by default.
3. **Select the channel per flow.** TLS, IPsec site-to-site, remote-access VPN, SSH, end-to-end messaging — with the rationale written as a sentence that would survive a design review ("selected because…; rejected alternative… because…").
4. **Name the termination points.** Where encryption starts and ends, and what travels in plaintext between. Every plaintext segment gets a justification or a finding.
5. **Decide the failure modes.** Tunnel down, certificate expired, VPN concentrator unreachable — fail open or closed, per flow, in advance.
6. **Assign the operational burden.** Certificate renewals, key rotation, tunnel monitoring — each with an owner. A channel nobody operates decays into a vulnerability (the expired certificate is the classic).
7. **Close out.** The rationale document with decisions, owners, dates.

## 5. On your own

**Task:** Inventory the traffic of a system you run — home lab, VPS, side project. Every flow crossing a boundary gets a row: endpoints, channel, termination points, failure mode. Include the flows you forgot at first (backups, monitoring, DNS).

**Success test:** You find at least one flow with no channel (plaintext where it shouldn't be), one TLS termination point earlier than you assumed, and one failure mode you hadn't decided. Each becomes a decision with an owner (you) and a date.

## 6. Where it goes wrong

- **TLS terminating at the edge, plaintext inside.** The load balancer decrypts; the interior carries secrets in the clear. The interior is not trusted — the architecture lesson said so.
- **The flat VPN.** Encrypted tunnel, unsegmented landing. The attacker who compromises the remote laptop inherits the interior.
- **0-RTT on state-changing endpoints.** Replayable resumption on anything but idempotent reads. Fast and wrong.
- **Certificate expiry as an outage class.** No renewal automation, no expiry monitoring. The most common TLS incident, entirely operational. The tell: the expiry dashboard shows a certificate under 30 days with no renewal ticket — the outage is already scheduled.
- **SSH with passwords on infrastructure.** Brute-forceable admin access. Keys, tracked and revoked — the lifecycle from `e-auth-systems` applies to every authenticator, including these.
- **Agent forwarding through the jump host.** Convenience that turns the bastion into a key-distribution service for anyone who compromises it.
- **Downgrade by compatibility.** TLS 1.2 (or worse) retained "for the legacy integration" with no deprecation date. Legacy exceptions need owners and dates or they become permanent. The tell: a TLS scan of the endpoint still negotiates the old version with no deprecation ticket open.
- **Messaging without key verification.** End-to-end encryption with unverified keys is a padlock icon, not a guarantee.
- **The forgotten flows.** Backups, monitoring telemetry, the printer's email — inventoried never, encrypted never.

## 7. Read the source

Primary documents first:

- **RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3** (IETF, August 2018) — *read* §1 (the changes from 1.2: encrypted handshake, forward secrecy, 0-RTT) and §2 (the protocol overview); *skim* the handshake details — the selection decisions live in §1, not in the state machine.
- **NIST SP 800-77, Guide to IPsec VPNs** (csrc.nist.gov) — *read* for the site-to-site selection: gateway placement, traffic selectors, failure handling.
- **NIST SP 800-113, Guide to SSL VPNs** (csrc.nist.gov) — *read* for the remote-access selection: the concentrator as policy enforcement point.

Then at most three free resources:

1. **OWASP Transport Layer Protection Cheat Sheet** (cheatsheetseries.owasp.org) — free; the practitioner checklist for TLS configuration that implements this lesson's selections.
2. **CISA: Layering Network Security Through Segmentation** (cisa.gov) — free; the zone map your channel inventory is drawn against.
3. **NIST SP 800-52 Rev. 2, Guidelines for the Selection, Configuration, and Use of TLS** (csrc.nist.gov) — free; the TLS configuration companion: versions, cipher suites, certificate guidance.

## 8. Check yourself

1. TLS terminates at the load balancer; the web-to-app hop is plaintext "because it's inside." Using the interior-trust argument from the architecture lesson, explain the failure — and the two alternative termination designs.
2. A branch-office IPsec tunnel carries all VLANs including guest. Explain the blast-radius consequence and how traffic selectors fix it.
3. Compare 0-RTT for a read-only API versus a funds-transfer endpoint: what property of 0-RTT creates the difference, and what is the selection decision for each?
4. An administrator SSHes directly to switches with password auth and forwards their agent through a jump host. Name the three distinct failures and the fix for each.
5. During an active incident, responders coordinate over a messaging app. Why is end-to-end encryption with verified keys the selection here — what adversary does it defeat that TLS to the provider does not?

## 9. Prove it

**Artifact:** your channel-selection rationale — traffic inventory, per-flow channel with written rationale and rejected alternatives, termination points with plaintext segments justified or flagged, failure-mode decisions, operational owners — for the Harborlight worked case in your own words or a system you run.

**Honest claim:** "I can choose the right encrypted channel for every traffic class — I can say which channel each flow uses, where encryption starts and ends, what happens when the channel fails, and who operates it."
**Can't claim yet:** "I can configure and troubleshoot these channels" — VPN, PKI, and TLS deployment are engineering work; this lesson taught the selection judgment those deployments must satisfy.

## 10. Leads to

- `e-network-architecture` — the zones and boundaries your channels cross; `e-network-components` — the devices your channels terminate on and pass through.
- `a-http-depth` — the handshake mechanics under the TLS selections; `e-crypto-applied` — the cryptographic properties (forward secrecy, AEAD) your selections rely on.
- `e-auth-systems` — the authenticator lifecycle covering every key and certificate this lesson assigns.
- Map refs: **CISSP 4.3** (this lesson); feeds **CISSP 4.1** (architecture) and **3.6** (cryptographic lifecycle — certificate and key management).

---

*Sources fetched 2026-10-10: RFC 8446 (rfc-editor.org); NIST SP 800-77, SP 800-113 (csrc.nist.gov); OWASP Transport Layer Protection Cheat Sheet; CISA segmentation infographic; NIST SP 800-52 Rev. 2. Full ledger in the batch manifest.*
