---
lesson_id: e-investigations
slug: investigations
stage: E
level: 3
prerequisites: [c-incident-response, d-dfir-deep]
roles: []
map_refs: ["CISSP 1.5"]
test_date: 2026-10-10
description: "Run the investigation-type decision tree: administrative, criminal, civil, regulatory. A free lesson in the security guidebook, serving CISSP objective 1.5."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Investigation types: which investigation you're in, and what it demands


**Map ref:** serves **CISSP objective 1.5** — investigation types and their requirements.

---

## 1. Where this shows up

An incident becomes an investigation the moment someone asks "what happened, who did it, and what do we do about it" — and the answer depends entirely on *which kind* of investigation you are in. The same suspicious database export is four different investigations: an HR matter if an employee did it, a criminal case if it was theft, a civil case if a customer sues over it, and a regulatory matter if a breach-notification law fires. Each type has different rules about who leads, what standard of proof applies, how evidence must be handled, and what rights the people involved have. Getting the type wrong is how organizations tip off suspects, destroy evidence, waive privilege, or hand a prosecutor a case they never meant to build. This lesson teaches the decision tree: given an incident, which investigation types are in play, and what does each one demand.

## 2. Before you start

- You have run the first hours of an incident in `c-incident-response` — this lesson starts where containment ends and the questions begin.
- You know evidence handling from `d-dfir-deep` — chain of custody, imaging, documentation. Every type below consumes that discipline differently.
- Bring your `e-cyber-law` matrix — regulatory investigations are obligations from that matrix coming due.
- The work product is a decision tree applied to three scenarios, each ending in: type, authority, evidence standard, the one mistake to avoid.

## 3. How it works

**The four types.** The industry's standard framing distinguishes investigations by who conducts them, to what end, and under what authority:

- **Administrative (internal).** The organization investigates its own people for policy violations — fraud, misuse, misconduct. Authority: the employer's. Standard: whatever internal policy says (commonly a preponderance — more likely than not). Goal: an employment decision, possibly a referral. The organization controls the timeline, the scope, and the evidence — which is exactly why the evidence must still be handled as if it will leave the building, because it might.
- **Criminal.** Law enforcement investigates suspected crime. Authority: the state's — warrants, subpoenas, arrests. Standard: probable cause to investigate, proof beyond a reasonable doubt to convict. Goal: prosecution. The critical fork: once law enforcement is involved, the organization *loses control* of the timeline and the scope. Evidence must meet criminal standards from the first touch — chain of custody unbroken, no alterations — because a gap that an internal review would forgive can kill a prosecution. The DOJ's Computer Crime and Intellectual Property Section (CCIPS) is the federal home of cybercrime prosecution; its public pages (fetched for this lesson) describe the remit — know it exists before you need it.
- **Civil.** One party sues another — a customer sues over a breach, a vendor sues over a contract. Authority: the court's. Standard: preponderance of the evidence. Goal: damages or injunctions. The load-bearing mechanism is the **litigation hold**: once litigation is reasonably anticipated, the organization must preserve all relevant evidence — and destroying it afterward is *spoliation*, which courts punish independently of the underlying case. The hold must go out fast, in writing, to everyone who might hold relevant data, including backups and personal devices used for work.
- **Regulatory.** A government agency investigates compliance — a data protection authority after a breach notification, a financial regulator after an incident. Authority: the agency's statutory powers (inspections, information demands, administrative fines). Standard: the statute's. Goal: compliance, remediation, penalties. Your `e-cyber-law` matrix is the preparation for this type: the obligations mapped there are what the regulator will ask about, and the evidence column is what you will hand over.

**One incident, multiple types.** Types stack. A sysadmin selling customer data is simultaneously administrative (fire them), criminal (refer to law enforcement), civil (customers sue), and regulatory (breach notification under `e-cyber-law`). The decision tree's job is not to pick one — it is to identify *all* that apply and sequence them, because the types interfere: an internal interview can taint a criminal case; a public regulatory filing can arm civil plaintiffs; a hasty termination can destroy the evidence every other type needs.

**Evidence across types.** NIST SP 800-86 (Guide to Integrating Forensic Techniques into Incident Response — fetched for this lesson) is the evidence-handling spine: document everything, maintain chain of custody, work from copies, keep the original pristine. The standard rises with the type: administrative work done to criminal standards is reusable everywhere; criminal-standard evidence handled to administrative standards is usable nowhere. The rule: **always work to the highest standard any plausible type requires**, because day one rarely reveals all the types in play. That means imaging before analysis, hashing at acquisition, and a written custody log from the first touch — even for the "simple HR matter."

**Privilege and counsel.** The moment an investigation might become criminal, civil, or regulatory, involve legal counsel — early, not after the interviews. Counsel's involvement can protect investigation materials under attorney-client privilege and the work-product doctrine (which shields materials prepared for litigation from being handed over); without it, your investigation notes are discoverable (the other side can legally demand to see them). The practical rule for interviews: the people conducting them must know, and the interviewees must be told, who counsel represents — the *company*, not the employee. This is process literacy, not legal advice: the shape of the protection is counsel's call, but engaging counsel late is the practitioner's failure.

**The decision tree.** For any incident, walk in order:

1. **Is a crime suspected?** (unauthorized access, theft, fraud, extortion) → If yes, preserve to criminal standards immediately, engage counsel, and decide *with counsel* whether and when to involve law enforcement. Do not interview the suspect first — an internal interview can compromise a prosecution.
2. **Is litigation reasonably anticipated?** (harmed customers, breached contracts, a demand letter) → If yes, issue the litigation hold *now*, in writing, broadly. Preservation beats analysis.
3. **Does a regulator need to know?** (breach-notification obligations from your `e-cyber-law` matrix) → If yes, the notification clock is running; the investigation must produce the facts the notification requires (scope, categories, approximate numbers — the Article 33 list) on the regulator's timeline, not yours.
4. **Is there an internal policy question regardless?** → Almost always yes: the administrative track runs in parallel, sequenced *after* counsel clears it, so it does not contaminate the other tracks.
5. **Reassess at every new fact.** Types are not decided once. The HR matter becomes criminal when the logs show exfiltration; the contained incident becomes regulatory when the data turns out to include another jurisdiction's residents.

**The one mistake per type.** Administrative: tipping off the subject before preservation. Criminal: breaking chain of custody in the first hour. Civil: no litigation hold, then routine deletion runs. Regulatory: missing the notification clock while "still investigating."

### Worked example: three scenarios at Copperline Freight (fictional)

**Scenario A — the suspected insider.** A dispatcher reports that a sysadmin with database access has been asking unusual questions about the customer export function; logs show two large exports to the admin's workstation last week. *Types:* administrative (certain — employment matter), criminal (plausible — theft of customer data). *Sequence:* counsel engaged first; evidence preserved to criminal standards (image the workstation before anyone touches it, hash at acquisition, custody log); *no interview yet* — the interview waits for counsel's sequencing decision, because a premature internal interview is the classic criminal-case contaminant. Law-enforcement referral is counsel's decision, not IT's. *The one mistake to avoid:* confronting the admin "to hear their side" before preservation — the confrontation tips them off, and the logs get wiped that night.

**Scenario B — the breach with customers.** The ransomware case from `e-bcp-drp`: customer shipment data was exfiltrated before encryption, including EU residents' personal data. *Types:* regulatory (certain — breach notification under the `e-cyber-law` matrix, 72-hour clock), civil (likely — customer lawsuits), criminal (the ransomware itself — law enforcement referral), administrative (the access path — how did they get in, whose credentials). *Sequence:* the regulatory clock dominates the first 72 hours — the investigation must produce scope, categories, and approximate numbers on that timeline. Litigation hold goes out on day one, broadly. The criminal track (law enforcement) runs parallel but does not set the notification timeline — the regulator's clock does. *The one mistake to avoid:* letting "we're still investigating" delay the notification — the clock runs on awareness, and the notification can be phased.

**Scenario C — the expense fraud.** A manager's expense reports show a pattern of personal charges just under the approval threshold. No customer data, no external parties, no regulator. *Types:* administrative only. *Sequence:* HR leads, security supports with log evidence; still preserve properly (write up the evidence handling — the habit is the point, and today's admin case is tomorrow's criminal referral if the pattern turns out to be kickbacks). Interview with HR present, documented. *The one mistake to avoid:* treating "administrative only" as "informal" — sloppy handling now means the evidence is unusable if the type escalates.

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the decision tree and the three scenario analyses above, authored and self-reviewed in-session on 2026-10-10 against NIST SP 800-86 and the DOJ CCIPS pages. Transcript: `runs/e-investigations.log` (records the tree, the per-scenario type/authority/standard/mistake, and the review checklist — no commands to transcribe).

1. **Draw the tree.** Copy the five-step decision tree from §3 onto one page. This is your incident-response runbook's companion — tape it next to the containment checklist.
2. **Take an incident.** Use a real past incident from your work or lab (sanitized), or one of the three scenarios above.
3. **Walk the five steps in order.** Crime? Litigation? Regulator? Internal track? Reassess. Write the answer to each — the tree is only useful written.
4. **Name the types and sequence them.** List every type in play and the order of operations. If two types conflict on timing, name the conflict and who resolves it (counsel).
5. **Set the evidence standard.** Default to the highest plausible type's standard from the first touch. Write the preservation actions: image, hash, custody log, hold notice.
6. **Name the one mistake.** For each type in play, write the single mistake that does the most damage. This is the checklist you read at 3 a.m.

## 5. On your own

**Task:** Take the ransomware scenario from `e-bcp-drp` (or any incident you have actually worked) and run the full tree: types in play, sequencing, evidence standard, counsel engagement point, notification obligations with clocks, and the per-type mistake list.

**Success test:** Your analysis identifies at least three types, sequences them with reasons, sets the evidence standard *before* describing any analysis steps, and names the counsel engagement point explicitly. If your analysis starts with "we investigated," you skipped the tree.

## 6. Where it goes wrong

- **The premature interview.** Confronting the suspect before preservation and counsel. Evidence walks out the door that night; the criminal case dies in the morning.
- **Chain of custody as an afterthought.** Analysis first, documentation later. Later never reconstructs the first touch — and the gap is where defense counsel lives.
- **The missing litigation hold.** Routine deletion runs during the two weeks nobody issued the hold. Spoliation sanctions follow, independent of the merits.
- **Type blindness.** Running the whole thing as an HR matter while the regulator's clock runs and customers hire lawyers. The tree exists to prevent exactly this.
- **Counsel engaged too late.** Investigation notes written, interviews done, *then* the lawyers arrive — and discover the notes are discoverable.
- **Law enforcement as a first call.** Referring to law enforcement before counsel has sequenced the tracks — the organization loses control of timeline and scope before it has preserved its own position.
- **The single-type mindset.** "It's just an internal matter" said about exfiltrated customer data. Types stack; reassess at every new fact.
- **Evidence to the lowest standard.** Handling everything to administrative standards because "it's probably just HR" — then the type escalates and nothing is admissible.

## 7. Read the source

Primary documents first:

- **NIST SP 800-86, Guide to Integrating Forensic Techniques into Incident Response** (csrc.nist.gov) — *read* the evidence-handling guidance: documentation, chain of custody, working from copies. The standard every investigation type builds on.
- **DOJ Computer Crime and Intellectual Property Section (CCIPS)** (justice.gov) — *read* the section's remit pages: what federal cybercrime prosecution covers, so the criminal track is concrete before you need it.

Then at most three free resources:

1. **NIST SP 800-61 Rev. 3, Incident Response Recommendations and Considerations** (csrc.nist.gov — final April 2025, verified 2026-10-09) — free; the incident-response process this lesson's tree attaches to — reread the analysis and evidence-collection phases with investigation types in mind. (Rev. 2 is superseded; do not use it.)

## 8. Check yourself

1. A sysadmin is suspected of stealing customer data. Your manager wants to "have a chat with him first to hear his side." Name the investigation types in play, explain what the chat destroys, and state the correct first three actions in order.
2. Explain why evidence should be handled to the highest plausible type's standard from the first touch — using the "today's admin case is tomorrow's criminal referral" mechanism.
3. A breach involves EU residents' data and a major customer's contract with a 48-hour notice clause. Walk the decision tree: which clocks run, which dominates the first 72 hours, and what the investigation must produce on that timeline.
4. Distinguish the litigation hold from routine backup retention: what triggers it, who receives it, and what happens if routine deletion runs after the trigger but before the hold goes out.
5. Predict the failure of an investigation run entirely as an internal HR matter where the logs later show large-scale exfiltration: name the three types that were missed and the specific evidence-handling step whose absence hurts each one most.

## 9. Prove it

**Artifact:** your decision tree (one page) plus three scenario analyses (types, authority, evidence standard, sequencing, counsel point, clocks, the one mistake per type) — for the Copperline scenarios in your own words, or better, for a real incident you have worked, sanitized.

**Honest claim:** "Given an incident, I can determine which investigation types are in play, sequence them without contaminating each other, set the evidence standard from the first touch, and name the mistake each type punishes most."
**Can't claim yet:** "I can conduct a criminal investigation" — that authority belongs to law enforcement, and the legal strategy belongs to counsel. This lesson taught the practitioner's decisions around investigations: preservation, sequencing, and knowing when to hand off.

## 10. Leads to

- **d-dfir-deep — `d-dfir-deep`** — the evidence discipline every type consumes: imaging, hashing, custody, analysis.
- **c-incident-response — `c-incident-response`** — the first hours: containment before investigation, and the handoff between them.
- `e-cyber-law` — the regulatory type's obligations: notification clocks, evidence the regulator expects.
- `e-personnel-security` — the administrative type's home ground: the employment lifecycle and insider cases.
- Map refs: **CISSP 1.5** (this lesson); feeds **CISSP 7.1** (investigations and forensics) and **7.6** (incident management).
