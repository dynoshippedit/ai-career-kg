---
lesson_id: e-facility-design
slug: facility-design
stage: E
level: 3
prerequisites: [e-risk-assessment]
roles: []
map_refs: ["CISSP 3.8"]
test_date: 2026-10-10
description: "Review a facility design against CPTED, layered defense, and site-selection factors, writing findings fixable at the design stage. A free lesson in the security guidebook, serving CISSP objective 3.8."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Site and facility design: security before the first brick


**Map ref:** serves **CISSP objective 3.8** — site and facility design principles: CPTED, layered defense, and site selection.

---

## 1. Where this shows up

Every control in this guidebook assumes an attacker who arrives over the network. But the server has a street address, a loading dock, a cleaning crew, and a power feed — and the cheapest way past a firewall is often a door. Site and facility design is the discipline of making the *physical* environment hostile to attack and friendly to legitimate use, starting before construction: where the building sits, how its spaces are arranged, how each layer from the property line to the server rack delays, detects, and deters. It shows up in the data-center tour where the guide points out the mantrap with practiced pride, in the office whose parking lot lighting was a security decision, in the site-selection memo that rejected the flood plain, and in the CISSP as the domain where information security remembers it has a body. Design-phase decisions are nearly free; retrofit is ruinous — which is why this lesson exists at the design stage, not after the break-in.

## 2. Before you start

- You can assess threats and rate risk (`e-risk-assessment`) — the facility's threat environment (crime, natural hazard, adversary capability) is this lesson's input.
- No tools. The work product is a facility design review: CPTED assessment, layered-defense analysis, site-selection evaluation, findings with recommendations.

## 3. How it works

**CPTED: crime prevention through environmental design.** The premise, developed from Oscar Newman's defensible-space work and codified in CPTED practice: the proper design and use of the built environment reduces both the incidence and the fear of crime. Four strategies:

- **Natural surveillance.** Design spaces so legitimate users can see and be seen — windows overlooking entrances and parking, open sightlines, lighting that eliminates hiding places. The mechanism is perceived risk of observation: offenders avoid places where they feel watched. A reception desk with sightlines to the lobby and the parking lot is a control; a solid wall facing the parking lot is an invitation.
- **Natural access control.** Guide movement through the environment — defined entrances, pathways that channel visitors past observation points, landscaping and barriers that make the intended route the easy route and other routes effortful. Thorny plantings under ground-floor windows, bollards that stop vehicles but not pedestrians, a single public entrance with all other doors alarmed: the environment says "this way" without a guard having to.
- **Territorial reinforcement.** Express ownership — signage, maintained landscaping, clear transitions from public to semi-private to private space. People defend territory they feel is theirs; offenders read the same signals. The well-kept facility with clear boundaries communicates "someone watches this place" before any camera does.
- **Maintenance.** The "broken windows" insight applied to facilities: neglected space signals that nobody is watching, which invites the behavior that further degrades it. Maintenance is a security control with a landscaping budget — graffiti removed promptly, lighting repaired immediately, landscaping kept to preserve sightlines.

**Layered defense (defense in depth, physically).** No single physical barrier stops a determined attacker; layers buy *time* and *detection opportunities*, and time is what lets response arrive. The standard layering, outside in: **deterrence** (visible measures that persuade the attacker to choose another target — lighting, signage, fencing), **the property perimeter** (fences, gates, vehicle barriers — the first delay), **the building perimeter** (walls, locked doors, windows — the second delay), **interior zoning** (public, semi-private, private, restricted areas with increasing controls — the visitor never reaches the third floor without passing two checkpoints), and **the asset itself** (the locked rack, the safe, the encrypted drive — the last delay, protecting the thing even when every layer above has failed). Each layer has a designed delay time and a detection mechanism; a layer with no detection is just a slower defeat, and a layer with no delay is just an alarm with no response time.

**Site selection factors.** Before the building exists, the site is the decision:

- **Threat environment:** local crime patterns, civil-stability history, proximity to high-risk neighbors (chemical plants, symbolic targets that attract attention you didn't order). The threat assessment from `e-risk-assessment` is the input — the site inherits its neighborhood.
- **Natural hazards:** flood plains, seismic zones, hurricane and tornado exposure, wildfire risk. FEMA's risk-management resources frame the analysis: identify the hazards, assess exposure, and either avoid or engineer for them. A data center in a flood plain is a design decision to regret at leisure.
- **Infrastructure:** power grid reliability and dual-feed availability, telecommunications diversity (two carriers, two paths — one backhoe should not isolate you), water for cooling and fire suppression, transportation access for staff and emergency services.
- **Visibility and symbolism:** high-profile locations attract attention; discreet facilities attract less. The decision cuts both ways — a visible headquarters deters petty crime and invites targeted attention — and it must be made deliberately, not inherited from the real-estate listing.
- **Emergency response:** proximity and capability of police, fire, and medical response; the facility's own muster points and evacuation routes designed before occupancy.
- **Legal and regulatory:** zoning, environmental constraints, data-residency obligations that make some jurisdictions unsuitable regardless of their other virtues.

**The design review method.** Walk the design (or the existing facility) from the property line inward, layer by layer, asking three questions per layer: *deter* (does it discourage the attempt?), *delay* (how long does it slow an attacker?), *detect* (who notices, and how fast does response arrive?). Record CPTED observations per space (surveillance, access control, territoriality, maintenance). Evaluate the site against the six selection factors. Findings become recommendations with the same honesty as any assessment: the loading dock with no natural surveillance gets a finding, not a shrug.

### Worked example: Harborline Logistics — distribution hub design review

**The facility (fictional).** Harborline is building a regional distribution hub: a 40,000-square-foot warehouse with offices, a small data closet (the on-premise end of the network from `e-arch-vuln-assessment`), truck bays on the east side, employee parking on the west, in a light-industrial park outside a mid-size city. The site sits outside the mapped flood plain, on a seismic-low grid, with dual power feeds available.

**CPTED assessment (per space):**

- *Employee parking (west):* FAIL — natural surveillance. The lot sits behind the building relative to the offices; no windows overlook it, lighting is specified at the code minimum, and landscaping plans show dense shrubs along the lot's far edge — hiding places by design. *Recommendation:* relocate the lot to the building's south face within office sightlines, raise lighting above minimum, replace dense shrubs with low plantings that preserve sightlines.
- *Truck bays (east):* PARTIAL — natural access control. The bay apron is well-defined with bollards separating pedestrian and vehicle paths (pass), but the design shows an unfenced service road running behind the bays with no gate — an unobserved approach (fail). *Recommendation:* gate the service road; the fence line must be continuous or it is decoration.
- *Main entrance:* PASS — territorial reinforcement. Clear public-to-private transition: signage, a defined visitor path channeled past the reception window, landscaping marking the boundary. The reception desk has sightlines to the entrance, the visitor lot, and the interior corridor — natural surveillance by design.
- *Data closet:* FAIL — interior zoning. The closet sits off the main ground-floor corridor with a standard office door and a keypad — one layer between the public corridor and the network core. *Recommendation:* relocate to a second-floor restricted zone (two interior checkpoints from any public space) or, minimum, upgrade to a mantrap-style vestibule with logging.

**Layered defense analysis (outside in):**

1. *Deterrence:* perimeter lighting and signage specified (pass); no visible camera coverage of the parking lot (fail — deterrence requires the measures be *seen*).
2. *Property perimeter:* 8-foot fence on three sides; the fourth side is the service road (fail — see above). Vehicle barriers at the truck entrance (pass).
3. *Building perimeter:* solid walls, minimal ground-floor windows on east/west (pass — fewer openings, fewer problems); all personnel doors with access control, alarmed (pass).
4. *Interior zoning:* public (lobby), semi-private (offices), private (warehouse floor), restricted (data closet, electrical room) — defined on the plans (pass), but the data closet's single-layer placement (fail — see above).
5. *Asset:* server rack with locking cabinet specified (pass); no safe for backup media (finding — see controls lesson).

**Site selection evaluation:** threat environment — light-industrial park, moderate property-crime history, no symbolic-target neighbors (acceptable); natural hazards — outside flood plain, low seismic, region has tornado exposure (tornado shelter designated in the plans — pass); infrastructure — dual power feeds available, two telecom carriers with diverse paths (pass); visibility — discreet industrial location (acceptable for a distribution hub); emergency response — fire station 1.2 miles, police substation 3 miles (pass); legal — zoning confirmed for the use (pass).

**Findings summary:** 5 findings (parking surveillance, service-road gap, data-closet zoning, camera visibility, backup-media storage), each with a recommendation and an owner (facilities manager) — the design-phase advantage: every fix here costs a plan revision, not a retrofit.

## 4. Walkthrough

**Worked-case lesson — no command line.** The Harborline hub review above, authored and self-reviewed in-session on 2026-10-10. Transcript: `runs/e-facility-design.log`.

1. **Describe the facility and site.** Fictional is fine: purpose, size, spaces, neighborhood, hazards. If you're reviewing a real site, start with the threat environment — crime, hazards, neighbors.
2. **Walk the CPTED four per space.** For each distinct space (parking, entrances, corridors, sensitive rooms), assess natural surveillance, natural access control, territorial reinforcement, and maintenance. Write the specific observation, not "CPTED considered."
3. **Analyze the layers outside in.** Deterrence, property perimeter, building perimeter, interior zoning, asset. For each: what deters, what delays (estimate minutes), what detects, and how fast response arrives. A layer with no detection gets flagged.
4. **Evaluate the site.** The six selection factors, pass/fail/acceptable with one-line rationale each. Hazards you can't engineer away are findings, not footnotes.
5. **Write findings with recommendations.** Each finding: the observation, the principle or layer it violates, the recommendation, the owner. Design-phase findings note the cost advantage explicitly — "plan revision now vs retrofit later."
6. **Close out.** The review document: CPTED table, layer analysis, site evaluation, findings register. The controls lesson (`e-facility-controls`) implements what this lesson's findings require.

## 5. On your own

**Task:** Review a facility you can walk — your office, your apartment building's common areas, a site you know. Walk it outside-in, assess the CPTED four per space, and write five findings.

**Success test:** At least one finding is a CPTED failure (sightlines, access control, territoriality, or maintenance) rather than a missing gadget — the design lens, not the shopping list. At least one finding surprises the facility's occupants when you tell them; the obvious findings are the ones everyone already discounted.

## 6. Where it goes wrong

- **Gadgets before design.** Cameras and card readers specified before the sightlines and zoning are right. Technology enforces a design; it cannot substitute for one — a camera watching a blind corner the architecture created is an expensive witness.
- **The discontinuous perimeter.** Fencing on three sides with an open service road, a loading dock propped open, the "temporary" gate left unlocked. A perimeter is binary: continuous or decorative.
- **Detection without delay, delay without detection.** The alarmed door with no response plan; the fence nobody monitors. Layers need both: time for response to arrive, and someone noticing in time to use it.
- **Interior zoning by org chart.** Zones drawn around departments instead of sensitivity — the data closet off the public corridor because "IT sits near the lobby." Zone by what needs protection, not by who sits where.
- **Maintenance as non-security.** The burned-out parking-lot light, the overgrown shrubs, the broken gate latch — each a small CPTED failure that compounds. Maintenance budgets are security budgets; treat the work order queue as a findings register.
- **Site selection by real estate.** The site chosen for price and highway access, with the flood plain discovered during the insurance quote. Threat environment and hazards are selection criteria, not due-diligence afterthoughts.
- **Designing for the last incident.** The mantrap installed after the tailgating incident, while the unobserved parking lot goes unreviewed. Review the whole facility, not the scar tissue.

## 7. Read the source

Primary documents first:

- **LISC: Crime Prevention Through Environmental Design (2-pager)** (lisc.org) — *read* the four strategies and the practice examples; short, concrete, free. The CPTED canon in two pages.
- **CISA: Physical Security** (cisa.gov) — *read* the protective-measures guidance; *skim* the sector-specific material. The operational companion: what measures exist and how they're chosen.
- **FEMA: Risk Management** (fema.gov) — *read* the hazard-identification and assessment framing for the site-selection factors; natural hazards are selection criteria.

Then at most three free resources:

1. **NIST SP 800-53 Rev. 5, PE family** (csrc.nist.gov) — free; the physical/environmental controls in catalog form — the implementation language for this lesson's findings.
2. **LAPD: Crime Prevention Through Environmental Design** (lapdonline.org) — free; a law-enforcement CPTED page with the three core strategies and practical recommendations — a good second voice.
3. **FEMA: How to Use a Portable Fire Extinguisher** (fema.gov) — free; fire classes and response basics — read before the controls lesson's fire section.

## 8. Check yourself

1. A warehouse has cameras covering the loading dock but the footage is reviewed only after incidents. Using the layer model, explain what's missing (deter/delay/detect) and the cheapest fix.
2. An office's parking lot sits behind the building with no window sightlines and code-minimum lighting. Name the CPTED strategy violated, the offender's-eye reasoning, and two design fixes that aren't cameras.
3. A site is cheap, highway-adjacent, and in a mapped flood plain. The team plans to "engineer for it." Name the two site-selection questions they must answer before that plan is credible, and what answer would kill the site.
4. A data closet sits off the public corridor behind a keypad door. Analyze it in layers: which layers protect it, what's missing, and why the keypad alone is insufficient.
5. Predict the failure sequence when facility maintenance is treated as non-security: name the first three degradations, who notices each (if anyone), and the incident they eventually enable.

## 9. Prove it

**Artifact:** your facility design review — CPTED assessment per space, layered-defense analysis outside in (deter/delay/detect per layer), site-selection evaluation against the six factors, and the findings register with recommendations and owners — for the Harborline hub in your own words, or for a facility you can walk.

**Honest claim:** "I can review a facility's design against CPTED, layered defense, and site-selection factors, and write findings that are fixable at the design stage."
**Can't claim yet:** "I can design the physical security systems" — the hardware specification is the controls lesson's work (`e-facility-controls`).

## 10. Leads to

- `e-facility-controls` — this lesson's findings become that lesson's checklist rows: design requires, controls implement.
- `e-risk-assessment` — the threat environment that opens every facility review; reread its threat-source analysis as site input.
- `e-platform-security` — the server in the data closet whose boot you attested sits in the building this lesson reviewed.
- Map refs: **CISSP 3.8** (this lesson); feeds **CISSP 7.14** (physical security implementation).
