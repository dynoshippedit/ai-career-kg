# Assessing vulnerabilities across the architecture

**ID:** `e-arch-vuln-assessment` · **Stage:** E (Expert) · **Level:** 3 (assess a hybrid architecture component by component, name the vulnerability classes per component, and write prioritized recommendations) · **Prerequisites:** `d-appsec` (threat modeling), `d-cloud-security` (cloud threat model), `e-risk-assessment` (rating and response); no command line in this lesson.

**Map ref:** serves **CISSP objective 3.5** — assessing and mitigating vulnerabilities across architecture and system types.

---

## 1. Where this shows up

Vulnerability assessment usually means scanning: point the scanner at the network, collect the CVEs, argue about the criticals. That finds known bugs in known software. Architecture assessment asks the harder question — what is *structurally* wrong, the kind of wrong no scanner reports because the scanner checks configurations and the flaw is in the design. The missing authorization check between two microservices, the IoT fleet with one shared credential, the API that trusts its mobile client, the cloud storage bucket whose policy nobody owns: these are architecture vulnerabilities, and they are where the serious breaches live. This lesson teaches the assessment as a discipline: decompose the system, enumerate the vulnerability classes each component type invites, rate them, and recommend in priority order. It shows up in pre-deployment architecture reviews, in the risk assessment's technical appendix, and in the incident retrospective that concludes "we knew the trust boundary was wrong and shipped it anyway."

## 2. Before you start

- You can threat-model an application (`d-appsec`) and reason about cloud trust boundaries (`d-cloud-security`).
- You can rate and respond to risk (`e-risk-assessment`) — ratings here use the same discipline: likelihood × impact, with owners and dates.
- No tools. The work product is a written architecture vulnerability assessment: component inventory, per-component vulnerability classes, ratings, and prioritized recommendations.

## 3. How it works

**Decompose first.** An architecture assessment begins with an inventory, not a scanner: every component, every data flow, every trust boundary, every identity the components use to talk to each other. The decomposition follows the data: where does it originate, where does it rest, where does it cross a boundary, and who can observe or alter it at each point. Components you cannot inventory are unassessed by definition — "the third-party video service" gets a row marked *limited visibility* with the assessment scoped to your integration boundary, not a pass.

**Vulnerability classes per component type.** Each architecture pattern invites characteristic flaw classes — not specific CVEs, but the *shapes* of failure. Assessing a component means asking which of its type's classes are present:

- **Cloud control plane and configuration:** identity and permission sprawl (over-broad roles, long-lived keys), storage misconfiguration (public-by-default buckets, unencrypted volumes), network exposure (overly permissive security groups, management ports reachable from the internet), and logging blind spots (control-plane actions nobody records). The cloud's vulnerability class is *configuration at scale* — one bad policy replicated everywhere instantly.
- **APIs and microservices:** broken object-level authorization (the caller names an object; nothing checks ownership), excessive data exposure (endpoints returning full objects the client filters), mass assignment (clients setting fields they shouldn't), missing rate limits and resource caps (one client starving the service), and **service-to-service trust gaps** — the internal API that authenticates nothing because "it's inside the VPC," the `e-secure-design` complete-mediation failure in microservice clothes.
- **IoT and edge devices:** shared or hardcoded credentials across the fleet, unencrypted or unauthenticated device-to-cloud channels, firmware without signed updates (the fleet you cannot patch is the fleet you will lose), physical exposure (devices an attacker can touch, extract, and clone), and telemetry spoofing (the cloud trusting whatever the device reports). The IoT vulnerability class is *scale times immutability* — thousands of devices you cannot easily reach, running code you cannot easily change.
- **Data stores:** encryption without key management (the `e-crypto-applied` failure), excessive privilege on service accounts, backups that bypass the production controls, and cross-tenant isolation enforced only in application code.
- **Identity and integration seams:** every place two systems meet — SSO integrations, webhooks, third-party SDKs — invites confused-deputy and trust-boundary flaws: the webhook endpoint that doesn't verify signatures, the SDK with more permissions than the feature needs.

**Rating.** Each finding gets likelihood and impact in the organization's qualitative scale (from `e-risk-assessment`), plus two architecture-specific modifiers: **blast radius** (how much of the system the flaw reaches — a flaw in shared auth code outranks a flaw in one endpoint) and **structural persistence** (how hard the flaw is to fix — a design flaw costs an order of magnitude more than a configuration flaw, so it rates higher even at equal likelihood).

**Recommendations in priority order.** Recommendations are architectural, not patch-level: introduce the authorization service, rotate the fleet credential design, add the signature check — each with the component, the effort tier (configuration change / component change / architecture change), and the risk it retires. Priority follows rating, but structural fixes that unblock many smaller fixes come first even when their individual rating is moderate — fixing the shared auth library retires a dozen endpoint findings.

**What assessment is not.** It is not a penetration test (no exploitation — the assessment argues from design, and its findings are valid whether or not anyone has exploited them yet). It is not a compliance checklist (a compliant architecture can still be structurally wrong). And it is not a one-time event: the assessment is re-run when the architecture changes, because every new component brings its type's vulnerability classes with it.

### Worked example: Harborline Logistics — hybrid architecture assessment

**The system (fictional).** Harborline's fleet platform from `e-secure-design`, now assessed as built: 2,000 vehicle telematics gateways (cellular IoT, ARM-based) report to a cloud ingestion API; a dispatch microservice cluster (12 services) serves the web app; a billing service reads from PostgreSQL; a third-party mapping SDK is embedded in the driver app; the fleet firmware updates over the air.

**Findings (per component, rated High/Moderate/Low):**

1. **IoT fleet — shared device credential (High).** All 2,000 gateways authenticate to the ingestion API with the same client certificate. Blast radius: total — one extracted key impersonates the fleet. Structural persistence: high — rotating a shared credential across 2,000 devices is a fleet-wide operation. *Class:* hardcoded/shared credentials. *Recommendation:* per-device certificates issued at manufacturing/enrollment, with the attestation flow from `e-platform-security` as the enrollment gate. Effort: architecture change.
2. **Ingestion API — no per-device authorization (High).** The API authenticates the fleet certificate but does not check *which* device is reporting — any valid fleet credential can submit telemetry for any vehicle. *Class:* broken object-level authorization. *Recommendation:* bind the device identity to the vehicle record at enrollment; reject telemetry for other vehicles. Effort: component change. (Note: finding 1 makes this worse — the shared credential means "any valid credential" is currently "anyone with the extracted key.")
3. **Dispatch microservices — unauthenticated service mesh (High).** Services call each other over the VPC with no mutual authentication; compromise of one service gives unauthenticated access to eleven others. *Class:* service-to-service trust gap (complete mediation failure). *Recommendation:* mutual TLS between services with per-service identities; the central authorization service from the design review as the policy point. Effort: architecture change — and it retires findings 4 and 5 below as instances.
4. **Billing service — direct database reads (Moderate, structural).** The design-review finding, still present: billing bypasses the API's authorization. *Class:* trust-boundary bypass. *Recommendation:* route through the API; remove database credentials from the billing host. Effort: component change.
5. **Driver app — mapping SDK with excessive permissions (Moderate).** The third-party SDK requests location-always and holds an API key with write scope to the dispatch service. *Class:* integration-seam over-privilege. *Recommendation:* scope the key to read-only map tiles; move dispatch writes server-side. Effort: configuration + component change. Visibility limit noted: the SDK's internals are unassessed — the assessment covers only the integration boundary.
6. **Cloud storage — telemetry bucket policy (Moderate).** Raw telemetry archives sit in a bucket whose policy grants the analytics contractor's whole organization read access, not the named analysts. *Class:* permission sprawl. *Recommendation:* scope to named identities; enable access logging on the bucket. Effort: configuration change.
7. **Firmware updates — unsigned OTA images (High).** Gateways accept firmware over the air with no signature verification — anyone who can reach the update endpoint (or spoof it) owns the fleet. *Class:* missing update integrity. *Recommendation:* signed firmware with the TPM-measured boot chain verifying before install; rollback protection. Effort: architecture change. This is the finding that keeps the assessor up at night: it converts every other fleet finding into full device compromise.

**Prioritized recommendations:** (1) signed firmware + measured boot (finding 7 — it underwrites fleet integrity, without which per-device credentials are theater); (2) per-device certificates with attestation enrollment (finding 1); (3) mutual TLS + central authorization in the service mesh (finding 3, retiring 4's class across services); (4) per-device authorization in ingestion (finding 2); (5) billing through the API (finding 4); (6) SDK scoping (finding 5); (7) bucket policy (finding 6). The ordering logic: fix the foundations that other fixes depend on first, then the blast-radius findings, then the configuration items.

## 4. Walkthrough

**Worked-case lesson — no command line.** The Harborline assessment above, authored and self-reviewed in-session on 2026-10-10. Transcript: `runs/e-arch-vuln-assessment.log`.

1. **Inventory the architecture.** List every component, data flow, trust boundary, and inter-component identity. Mark anything with limited visibility (third-party internals) explicitly — unassessed is a scope statement, not a pass.
2. **Assign vulnerability classes per component.** For each component, walk its type's class list (cloud config, API auth, IoT fleet, data store, integration seam) and record which classes are present, with the specific mechanism — not "auth issues" but "services call each other with no mutual authentication."
3. **Rate with the two modifiers.** Likelihood × impact, then adjust for blast radius and structural persistence. A design flaw with moderate likelihood outranks a configuration flaw with high likelihood — write down why.
4. **Write architectural recommendations.** Each names the component, the fix, the effort tier, and the risk retired. Note which recommendations retire other findings as instances — those go first.
5. **Prioritize and justify the order.** The priority list is an argument: foundations before instances, blast radius before convenience. If two findings tie, the structural one wins.
6. **Close out.** The assessment document: inventory, findings with ratings, prioritized recommendations, scope limits, and the re-assessment trigger (what architecture change re-opens it).

## 5. On your own

**Task:** Assess a hybrid system you can observe — your home lab plus a cloud account counts (the "IoT" can be any network device you own). Inventory, assign classes, rate, recommend.

**Success test:** You find at least one service-to-service trust gap (the internal path with no authentication) and at least one permission broader than the function needs. Your priority list justifies its order in writing — "fix the foundation first" must name which foundation and which findings depend on it.

## 6. Where it goes wrong

- **Scanning instead of assessing.** The scanner finds the unpatched library; the architecture review finds the missing authorization layer. Both matter; only one finds structural flaws. An assessment that never leaves the scanner output is a patch list wearing an assessment's name.
- **Component types assessed with the wrong class list.** Applying web-app classes to an IoT fleet (looking for XSS on a telematics gateway) while missing the fleet's actual classes (shared credentials, unsigned firmware). The class list must match the component type.
- **Trust boundaries drawn where the firewall is.** The assessment that treats "inside the VPC" as a boundary will miss every service-to-service finding. Boundaries are drawn where *authentication and authorization* happen, not where packets are filtered.
- **Third-party components waved through.** "The vendor handles security" as a scope exclusion without assessing the integration seam. You cannot assess their internals; you must assess your boundary with them — signatures, scoping, minimum data.
- **Ratings without the structural modifier.** A design flaw rated equal to a config flaw will be scheduled equal to a config flaw, and the design flaw will still be there in three years. Structural persistence is what makes architecture findings actually get fixed.
- **Recommendations as patch tickets.** "Fix finding 4" without the architectural change that retires the class. Instance fixes without class fixes are how the same finding returns next assessment with a different component name.
- **The assessment that never re-runs.** Architectures drift; every new service, device, and integration re-opens the assessment. No re-assessment trigger means the document describes a system that no longer exists.

## 7. Read the source

Primary documents first:

- **NIST SP 800-115, Technical Guide to Information Security Testing and Assessment** (csrc.nist.gov) — *read* the assessment methodology sections (planning, execution, reporting); *skim* the technique catalog. The method behind this lesson's walkthrough.
- **OWASP ASVS (Application Security Verification Standard)** (owasp.org) — *read* the API and access-control verification sections as the class list for the application components; *use* the rest as the requirement catalog.

Then at most three free resources:

1. **MITRE ATT&CK** (attack.mitre.org) — free; map each finding to the techniques it enables — the bridge from architecture flaw to adversary behavior.
2. **NIST SP 800-53 Rev. 5** (csrc.nist.gov) — free; the control catalog for writing recommendations that trace to something (feeds `e-control-selection`).
3. **CISA physical security resources** (cisa.gov) — free; the IoT devices are physical objects — assess their physical exposure with the same seriousness as their firmware.

## 8. Check yourself

1. An assessment finds an unauthenticated internal API and rates it Low because "it's inside the VPC." Name the two errors (one in the trust-boundary reasoning, one in the rating) and re-rate it with the structural modifier.
2. A scanner reports zero criticals on a microservice cluster whose services mutually trust each other with no authentication. Explain why the scanner is blind to the cluster's worst finding and which vulnerability class names it.
3. Two findings: (a) a storage bucket with an over-broad policy (configuration change to fix), (b) a shared fleet credential across 2,000 devices (architecture change to fix). Both rate High on likelihood × impact. Argue the priority order using structural persistence.
4. A third-party SDK is embedded in your mobile app. State precisely what the assessment can and cannot cover, and name the three integration-boundary controls the assessment must verify.
5. Predict the next assessment's finding when this assessment's recommendations fix each instance but not the class: describe the finding's shape and which component it appears in.

## 9. Prove it

**Artifact:** your architecture vulnerability assessment — component inventory with trust boundaries, per-component vulnerability classes with specific mechanisms, ratings with the structural modifier, prioritized recommendations with effort tiers and retirement notes, scope limits, and the re-assessment trigger — for the Harborline case in your own words, or for a system you can observe.

**Honest claim:** "I can decompose a hybrid architecture, name the vulnerability classes each component type invites, rate findings with structural judgment, and prioritize architectural fixes."
**Can't claim yet:** "I can penetration-test the architecture" — exploitation is a separate discipline; this lesson argued from design.

## 10. Leads to

- `e-control-selection` — recommendations become selections: trace each architectural fix to its control.
- `e-risk-assessment` — the rating discipline and the residual-risk statement this assessment feeds.
- `e-patch-management` — patch and vulnerability management operations: the operational half — the scanner findings this lesson deliberately set aside.
- `d-cloud-security`, `d-appsec` — the component-type knowledge this assessment draws on.
- Map refs: **CISSP 3.5** (this lesson); feeds **CISSP 6.1** (assessment strategy) and **7.8** (vuln management operations).
