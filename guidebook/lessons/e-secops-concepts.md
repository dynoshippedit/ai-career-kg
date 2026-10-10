# Foundational security operations concepts: the principles you run on

**ID:** `e-secops-concepts` · **Stage:** E (Expert) · **Level:** 3 (apply need-to-know, least privilege, separation of duties, and defense in depth as daily operating decisions — and assess a zero-trust gap) · **Prerequisites:** `e-iam` (the lifecycle and access review where these principles get applied); no command line in this lesson.

**Map ref:** serves **CISSP objective 7.4** — the foundational concepts of security operations, used as operating principles rather than vocabulary.

---

## 1. Where this shows up

Every operational security decision is one of a small set of principles applied to a new situation: who really needs this access, what's the smallest privilege that works, who else must be involved before this happens, what catches it when this layer fails. These principles show up in the SoD matrix that stops one person from creating and paying a vendor, in the privilege review that converts standing admin to just-in-time, in the incident where the firewall rule failed but the host control caught it — and in the zero-trust program that rebuilds all of it for an estate with no perimeter. Security architects, SOC managers, and GRC analysts live here. Note the relationship with `e-iam`: that lesson built the identity lifecycle and the access review. This lesson is the principles underneath those decisions — the reasoning you'd use to defend any single grant, control, or architecture choice.

## 2. Before you start

- You have designed an identity lifecycle and run an access review in `e-iam` — the principles here are what make those reviews mean something.
- You know the control-type vocabulary (preventive/detective) at least by reputation; `e-detective-preventive` (same batch) goes deep.
- No tools. The work products are documents: a separation-of-duties matrix, a privilege-review disposition, and a zero-trust gap assessment. Primary spine: **NIST SP 800-207** (Zero Trust Architecture, August 2020).

## 3. How it works

Four classical principles plus the modern operating model that reframes them.

**Need-to-know and least privilege: the access question, asked twice.** **Need-to-know** says access follows demonstrated necessity: you get the data because your job requires it, not because you're senior, curious, or "might need it someday." **Least privilege** says the access you do get is the minimum that lets the job be done: read instead of write, one database instead of all of them, this week instead of forever. They sound identical and fail differently. Need-to-know fails at the *scope* decision (the analyst who can read every customer record when the job needs ten); least privilege fails at the *depth and duration* decision (the admin with permanent production rights for a quarterly task). In operation, need-to-know is enforced at grant time (the request must state the job need) and least privilege at review time (the `e-iam` access review asks "is this still the minimum?"). Both decay toward over-privilege without the review — access only ever grows unless something shrinks it.

**Separation of duties: no single pair of hands completes a sensitive act.** SoD says critical actions require collusion to abuse: the person who creates a vendor can't approve the payment; the developer who writes the code can't deploy it unreviewed; the administrator who grants access can't audit the grants. In operation, SoD is a **matrix**: sensitive duties down one axis, roles down the other, marking which combinations one person may not hold. The matrix is where the principle meets reality — small teams can't separate everything, so the matrix also records the **compensating controls** for the separations you can't afford (enhanced logging, mandatory review, dual authorization on the specific action). An SoD matrix with no compensating-control column is a document that small organizations can't implement and large ones can't audit. The failure mode is the toxic combination discovered after the fraud: duties that were never mapped, so nobody knew one person held both ends.

**Defense in depth: assume each layer fails.** No single control is reliable — it will be misconfigured, bypassed, or defeated — so protection is **layered**: the firewall rule, the host control, the application check, the monitoring that notices when the others fail. The operating discipline is in two questions. First, *are the layers independent?* Three controls that all fail when one credential is stolen are one layer wearing three hats. Second, *does anything watch the layers?* Defense in depth without monitoring is just defense in hope — the `e-detective-preventive` lesson's placement decisions are how you answer the second question per control. The common misreading: more layers as a substitute for understanding. Ten overlapping controls nobody can explain is not depth; it's clutter that hides the gap.

**Zero trust: the operating model for the perimeter-less estate.** The classical principles assumed a network with an inside. Cloud, remote work, and SaaS dissolved the inside. **Zero trust** — per NIST SP 800-207 (August 2020) — is the operating model for that world: no implicit trust granted to assets or accounts based on network location or ownership; every access decision explicitly authenticated, authorized, and continuously re-evaluated. SP 800-207's tenets, operationalized: **all data sources and services are resources** (the network location stops being the trust criterion); **all communication is secured** (regardless of path); **access is granted per-session** (not per-network-login — the just-in-time elevation from `e-iam` is this tenet in practice); **policy is dynamic** (the decision uses identity, device posture, behavior — the ABAC thinking from `e-iam`); **the enterprise monitors everything** (the `e-logging-monitoring` program is a zero-trust prerequisite, not an accessory). CISA's Zero Trust Maturity Model (current edition v2.0) turns the tenets into an assessment: five pillars (identity, devices, networks, applications, data) each scored across stages, so "adopt zero trust" becomes a gap assessment with a roadmap instead of a slogan. The honest note: zero trust doesn't replace the classical principles — it *relocates* them. Least privilege becomes per-session and attribute-driven; SoD becomes policy the engine enforces rather than a matrix auditors sample; defense in depth becomes the explicit assumption that every component, including the policy engine, is compromisable.

### Worked example: Halcyon Health — SoD matrix, privilege review, zero-trust gaps

**The company (fictional).** Halcyon Health, 240 staff, regional clinic network. Two scopes: the billing system (money movement — the classic SoD territory) and the IT estate (15 admins, standing domain privilege for all of them, VPN as the perimeter).

**The SoD matrix (billing, excerpt — fictional).** Duties: create vendor, approve vendor, submit invoice, approve payment, reconcile accounts, modify billing codes. Findings: the office manager can create vendors *and* approve payments (toxic combination — the exact shape of most billing frauds); two billing clerks can both submit and approve invoices under a threshold nobody documented. Decisions: vendor creation moves to procurement with finance approval (separation restored); the approval threshold is written down and the system enforces it (the undocumented threshold was the real finding); the one separation the 240-person org can't afford — the same DBA maintains the billing database and its backups — gets a compensating control: restore tests witnessed by finance quarterly, and the DBA's privileged sessions recorded.

**The privilege review (IT).** All 15 admins hold standing domain admin. The review asks the least-privilege question per person: who needs it, for what, how often? Four keep standing (infrastructure team, session-recorded, with written justification); eleven move to just-in-time elevation — requested per task, approved by a second person (SoD on the elevation itself), auto-expiring. The help-desk password-reset path is checked against the `e-iam` weaker-path rule: it now requires the same MFA as the front door.

**The zero-trust gap assessment (against the ZTMM pillars, excerpt).** Identity: SSO everywhere except two legacy clinical apps (gap — the weaker path again). Devices: no posture check before VPN grants network access (gap — the VPN trusts the device implicitly). Networks: flat clinical network, no segmentation between guest Wi-Fi and clinical devices (gap). Data: the patient database encrypted at rest but no per-session access policy (gap). The roadmap is ordered by the principle each gap violates: identity first (it's the new perimeter), then devices, then networks. Each gap gets an owner and a quarter — a roadmap without dates is a wish list.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the SoD matrix, privilege review, and zero-trust gap assessment above, authored and self-reviewed in-session on 2026-10-10 against SP 800-207's tenets and the ZTMM pillar structure. Transcript: `runs/e-secops-concepts.log`.

1. **Map the sensitive duties.** For your fictional (or real) organization, list the duties where one person's unchecked action causes harm: money movement, access grants, code deployment, data export, backup deletion. If the list is short, you haven't thought about it enough.
2. **Build the SoD matrix.** Duties on one axis, roles on the other; mark the toxic combinations. For every separation you can't afford, write the compensating control in the adjacent column — enhanced monitoring, dual authorization, witnessed procedures.
3. **Run the privilege review.** List every standing privileged account. Per account: who, what for, how often, standing or just-in-time? "Might need it someday" converts to just-in-time. Record the justification for what stays standing.
4. **Check the weaker paths.** For every strong control (SSO with MFA, just-in-time elevation), find the bypass: the legacy app, the help-desk reset, the shared break-glass. Each bypass gets a decision — eliminate, match the strength, or document as a risk acceptance with owner and date.
5. **Assess zero-trust gaps.** Against the five pillars (identity, devices, networks, applications, data): where is trust still implicit — granted by network location, by device ownership, by "internal" status? Each implicit-trust finding becomes a roadmap item with owner and quarter.
6. **Order the roadmap by principle.** The gaps that violate identity-first (the new perimeter) come before network segmentation. Write the one-paragraph rationale an executive would read: what changes, in what order, and what risk each step retires.

## 5. On your own

**Task:** Pick one system you administer. List every privilege you hold on it, and for each, answer: what job need justifies this, and is it the minimum? Convert one standing privilege to just-in-time (even if "just-in-time" means a documented request to yourself with an expiry).

**Success test:** At least one privilege gets reduced or time-boxed, and you find one weaker path (a recovery method, a legacy protocol, a shared credential) that bypasses a stronger control. If your access is already minimal, audit someone else's — with permission.

## 6. Where it goes wrong

- **Need-to-know as hierarchy.** Access granted by seniority instead of job need. The executive with the full customer database "because they're an executive" is need-to-know inverted.
- **Least privilege without review.** Granted minimally on day one, never reviewed again. Access only grows; the review is the mechanism, not the initial grant.
- **The unmapped toxic combination.** The fraud nobody designed for because nobody mapped which duties one person held. The matrix is the control; the fraud is what happens without it.
- **SoD without compensating controls.** The matrix demands separations the org can't staff, so it's ignored entirely. The compensating-control column is what makes the matrix implementable.
- **Layers that share a fate.** Three controls, one credential — one compromise defeats all three. Independence of layers is the question; count is the distraction.
- **Depth without watchers.** Layered controls, no monitoring. Defense in depth assumes each layer fails; something has to notice the failure.
- **Zero trust as product.** Buying the platform and declaring the tenets satisfied. Zero trust is an operating model — per-session decisions, dynamic policy, monitored everything. The product is at most one layer.
- **Implicit trust that survived the migration.** The VPN that grants network access without checking the device, the "internal" app with no authentication. Every implicit-trust remnant is a gap the assessment exists to find.

## 7. Read the source

Primary documents first:

- **NIST SP 800-207, Zero Trust Architecture** (csrc.nist.gov, August 2020) — *read* the tenets and the logical-component architecture (policy engine, policy administrator, policy enforcement point); *skim* the deployment models. The tenets are the operating principles; everything else is implementation.
- **NIST SP 800-53 Rev. 5** (csrc.nist.gov) — *read* AC-5 (separation of duties) and AC-6 (least privilege) as the control-language version of this lesson's first half; *skim* the AU and SI families for the monitoring the principles assume.

Then at most three free resources:

1. **CISA Zero Trust Maturity Model, v2.0** (cisa.gov) — free; the assessment method — five pillars scored across stages, which turns "adopt zero trust" into a gap assessment with a roadmap.
2. **NISTIR 7316, Assessment of Access Control Systems** (csrc.nist.gov) — free; how access-control authorizations are structured and assessed — read after `e-iam`'s authorization-models section for the assessment lens.

## 8. Check yourself

1. A 30-person company maps its billing SoD and finds the same person must create vendors and approve payments — no staff to separate. Explain the compensating-control design: what specifically compensates, and why "we trust her" isn't one.
2. Distinguish a need-to-know failure from a least-privilege failure using one concrete access grant that exhibits each — then explain which failure the periodic access review catches and which it misses.
3. Three controls protect a database: a firewall rule, a database login, and an IDS watching the segment — all administered with the same credential. Using the layer-independence question, explain what an attacker who steals that credential defeats, and what you'd change.
4. A company buys a zero-trust platform, deploys agents, and declares the migration complete — but VPN still grants network access without device checks and two apps bypass SSO. Name the two implicit-trust remnants and the ZTMM pillar each belongs to.
5. Predict the privilege state of an IT team two years after a just-in-time program launches but the approval step is routinely rubber-stamped: what does "separation of duties on elevation" look like in practice, and what failed?

## 9. Prove it

**Artifact:** your SoD matrix (duties, roles, toxic combinations marked, compensating controls for unaffordable separations), privilege-review disposition (per-account standing/just-in-time decision with reasons), weaker-path inventory with decisions, and zero-trust gap assessment (implicit-trust findings per pillar, ordered roadmap with owners and quarters) — for the Halcyon worked case in your own words, or better, for an organization you actually advise or administer.

**Honest claim:** "I can apply the operating principles — need-to-know, least privilege, separation of duties, defense in depth — as concrete decisions, and I can assess where an estate still runs on implicit trust and order the work to remove it."
**Can't claim yet:** "I can architect a zero-trust enterprise" — the policy-engine design, device-posture infrastructure, and migration at scale are their own engineering discipline; this lesson taught the principles and the assessment, not the build.

## 10. Leads to

- `e-iam` — the lifecycle and review where these principles get applied; reread its privileged-access section as the SoD companion.
- `e-detective-preventive` — layer placement and monitoring: the "who watches the layers" half of defense in depth.
- `e-logging-monitoring` — the monitoring program zero trust assumes.
- Map refs: **CISSP 7.4** (this lesson); feeds **CISSP 5.x** (identity and access) and **7.7** (detective/preventive measures).

---

*Worked case authored and self-reviewed 2026-10-10; all scenario data fictional. Sources fetched in-session — see `runs/e-secops-concepts.log`.*
