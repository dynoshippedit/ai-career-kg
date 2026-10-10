# Investigations and digital forensics: the management and legal view

**ID:** `e-investigation-forensics` · **Stage:** E (Expert) · **Level:** 3 (design a forensic-readiness program and run an investigation's evidence handling so it survives legal scrutiny) · **Prerequisites:** `c-incident-response` (the response lifecycle this wraps around), `d-dfir-deep` (the analyst bench work this lesson manages — timelines, memory and disk forensics); no command line in this lesson.

**Map ref:** serves **CISSP objective 7.1** — how investigations are run: evidence, investigative techniques, digital forensics, and the legal frame that makes evidence admissible.

---

## 1. Where this shows up

Someone has to decide, before the incident, that evidence will exist when needed — and after, that it can actually be used. That's the management view: forensic readiness (logging, imaging capability, trained first responders), evidence handling (who touches what, in what order, documented how), and the legal frame (admissibility, counsel, when to call law enforcement). It shows up when the laptop was wiped before legal approved imaging, when nobody can prove the logs weren't altered, and in the CISO's meeting with counsel about an FBI referral. DFIR leads, SOC managers, and GRC analysts live here. Note the split with `d-dfir-deep`: that lesson taught the analyst's bench — timelines, memory forensics. This lesson teaches the program around the bench: the decisions that determine whether the bench's output is trusted, admissible, and complete.

## 2. Before you start

- You have run the incident-response lifecycle in `c-incident-response` — investigations begin where containment ends, or run in parallel.
- You know what forensic artifacts look like from `d-dfir-deep` — this lesson teaches what governs their collection.
- No tools. The work products are documents: a forensic-readiness plan, a chain-of-custody procedure, an investigation decision log. Bring the `e-risk-assessment` habit of writing reasons, owners, and dates — a court may read them.

## 3. How it works

An investigation answers "what happened" under constraints a purely technical analysis doesn't have: the evidence must be **complete**, **authentic**, and **lawfully obtained**. Four concerns organize the management view.

**Forensic readiness: the investigation starts before the incident.** Readiness is the difference between an organization that *can* investigate and one that wishes it could. Four components: **logging and retention** sufficient to reconstruct events (the `e-logging-monitoring` retention schedule is the evidence base — if logs aged out at 30 days, a 60-day-old intrusion is uninvestigable); **imaging and collection capability** (write-blockers, imaging tools, storage for forensic copies, or a contracted retainer — decided in advance, not sourced mid-incident); **trained first responders** who know the order of volatility and the "do not" list (don't shut down a running system you intend to memory-capture; don't browse the suspect drive); **pre-authorized procedures** — counsel-reviewed playbooks for the common scenarios, so the first hour isn't spent arguing about authority.

**The forensic process: collect, examine, analyze, report.** NIST SP 800-86 — the federal guide to integrating forensics into incident response (August 2006, still the structural reference) — organizes forensic work into four phases: **collection**, **examination**, **analysis**, **reporting**. The management insight is that each phase has a quality gate the manager owns: was collection complete and documented? Was the examination method sound? Does the analysis support the conclusion or leap past it? Can a non-technical reader — a judge, an executive — follow the report? The 2006 date is honest context — the document predates cloud and smartphones, but the four-phase structure and the data-source taxonomy (files, operating systems, network traffic, applications) still describe competent investigations — and SP 800-86 is explicit that it presents forensics "from an IT view, not a law enforcement view," which is why this lesson pairs it with the legal frame below.

**The order of volatility and the collection discipline.** Some evidence evaporates and some endures. RFC 3227 (February 2002, "Guidelines for Evidence Collection and Archiving") — short, free, still cited — teaches the **order of volatility**: collect the most ephemeral first (registers/cache, RAM, network state, running processes, then disk, logs, archival media). The management translation: first responders need a one-page card with this order, because the instinct to "just pull the plug" destroys the volatile evidence the investigation needs most. RFC 3227 also teaches **transparency** (document every action so another expert could reproduce it) and treats **chain of custody** as its own archiving procedure.

**Chain of custody and admissibility.** Evidence is only useful if its integrity is provable from collection to presentation. **Chain of custody** is the documented, unbroken record of who handled the evidence, when, and what they did — every handoff signed, every storage access logged, the original sealed and worked from copies. Break the chain and authenticity becomes arguable; in a legal proceeding, arguable authenticity is often fatal. That's why forensic copies are hashed at acquisition (the hash, verified at every later step, proves the working copy matches the original) and why analysts never work from originals. The NIJ's "Electronic Crime Scene Investigation: A Guide for First Responders" (second edition, a free Department of Justice publication) is written for the non-specialist first responder whose early mistakes — booting the suspect machine, browsing files — destroy admissibility. Its message for managers: your first responders usually aren't forensic specialists, so their procedures must be simple, written, and rehearsed.

**The legal and organizational frame.** Three decisions sit above the technical work. **When to involve counsel:** early, and before collection in any case that might become an employment action, a regulatory filing, or a criminal referral — counsel determines privilege, directs scope, and decides what must be preserved (litigation hold) versus what may be destroyed under retention policy. **When to involve law enforcement:** referral is a business decision made with counsel, not a reflex — the organization loses control of timing, direction, and potentially the evidence itself. **Administrative vs. criminal vs. regulatory paths:** the same facts can travel all three tracks at once, and evidence collected for one must be handled to standards that survive the others. The manager's rule: handle every investigation as if it will face the hardest audience, because you don't get to re-collect.

### Worked example: Meridian Analytics — insider investigation, managed end to end

**The company (fictional, continued from `e-iam`).** Meridian Analytics, 180 people. The trigger: a DLP alert — a departing sales engineer, last day Friday, has copied an unusual volume from the customer-data share to a personal cloud drive over two weeks. HR wants the laptop secured; legal is on notice; the employee's manager wants to "just ask him about it."

**Readiness check (what existed before the trigger).** Meridian has: 90-day retention on file-access logs (barely enough — the copying started 14 days ago, inside the window); a forensic retainer with 4-hour SLA; a written first-responder card; a counsel-reviewed playbook. What it lacks: the personal cloud drive is outside corporate visibility — the plan records that limitation honestly and works from endpoint and network evidence.

**The investigation plan (the manager's document).**

1. **Authority and privilege.** Outside counsel directs; the litigation-hold notice goes to IT (preserve the engineer's mailbox, file-access, VPN, and badge logs — don't delete). HR gets the scope in writing: fact-finding, not yet accusation.
2. **Collection, in volatility order.** Laptop still running and docked: memory capture first, then full disk image via write-blocker, then SIEM log pulls. Each acquisition hashed at collection; hashes in the custody log. Original sealed; analysis on copies.
3. **What not to do.** No interview before collection is complete (tip-off risks destruction). No "quick look" at the live laptop. The manager's "just ask him" is deferred in writing, with the reason.
4. **Analysis gates.** The examiner's findings get a leap-check: each conclusion cites the artifact supporting it. "Copied 14 GB to personal storage" must trace to DLP logs plus endpoint artifacts, not to suspicion.
5. **Decision points, logged.** Day 3: evidence confirms exfiltration of the customer list. Counsel decides: employment action proceeds on the forensic report; criminal referral deferred pending the full report (recorded with rationale); breach-notification analysis begins (the regulatory track).
6. **Reporting.** Two reports: technical (methods, hashes, artifacts, conclusions with confidence levels) and executive (what happened, proven vs. suspected, recommended actions). Both go to counsel first.

**Chain-of-custody excerpt (fictional, labeled):** item MA-2026-041 (laptop, asset tag LT-1834): collected 2026-10-12 09:14 by J. Okafor (outside firm), SHA-256 at acquisition, sealed in bag EB-2201; accessed 2026-10-13 by examiner R. Ito for imaging (working copy WC-2201-A, hash verified against original); every access signed. The form's printed rule: *a gap in this log is a gap in the evidence.*

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the investigation plan, readiness assessment, and chain-of-custody procedure above, authored and self-reviewed in-session on 2026-10-10 against SP 800-86's four phases, RFC 3227, and the NIJ first-responders guide. Transcript: `runs/e-investigation-forensics.log`.

1. **Assess readiness.** For your fictional (or real) organization, score the four readiness components: log retention vs. realistic investigation windows, imaging capability (in-house or retainer), first-responder training (does the one-page card exist?), pre-authorized procedures (counsel-reviewed playbooks for the three common scenarios). Every gap gets an owner and a date.
2. **Write the first-responder card.** One page: the order of volatility, the "do not" list, the call tree (who pages counsel, who pages the retainer). If it doesn't fit on one page, it's not a field card.
3. **Design the chain-of-custody form.** Fields: item ID, description, collected by/when/where, hash at acquisition, storage location, every access (who, when, purpose, hash re-verified), seal numbers. Rule: analysis on copies, originals sealed.
4. **Run the scenario.** Take the Meridian case (or your own): write the investigation plan with authority, collection order, the "do not" decisions, analysis gates, and the three-track decision log. Plant one complication — key evidence on a personal device, or logs aged out — and record how the plan adapts honestly.
5. **Write the two reports.** Technical (methods, hashes, artifact-to-conclusion traceability) and executive (proven vs. suspected, recommended actions). Have a non-technical reader tell you what they'd decide from the executive summary — if they can't, the report failed.
6. **After-action on readiness.** What did the investigation reveal about the step-1 gaps? The investigation's findings include findings about the program.

## 5. On your own

**Task:** For a system you control (homelab, VPS), write the forensic-readiness page: what logs exist and their retention, what you'd image and with what (even "I'd call a retainer — here's the one I'd pick and why"), and your first-responder card. Then test the weakest link: verify one log source actually retains what you claim — check its oldest entry.

**Success test:** Your page names a specific retention gap you found by checking, not assuming. If you assumed every retention setting, you did the exercise wrong — the check is the exercise.

## 6. Where it goes wrong

- **The premature interview.** Asking the suspect "about it" before collection is complete destroys evidence; the procedure exists to overrule the instinct.
- **Booting the evidence.** Powering on a suspect machine or browsing its files alters the evidence and hands the other side an authenticity argument. Untrained first responders do helpful things; helpful things destroy cases.
- **The broken chain.** Evidence collected carefully, then handed around unsigned and stored unlogged. Admissibility dies in the gaps, not at collection.
- **Analysis on originals.** Working from the original makes every examination step an alteration step. Copies are cheap; authenticity arguments are expensive.
- **Single-track thinking.** Collecting to HR standards, then discovering the case needs criminal-grade handling. Handle to the hardest standard from the start; you can't upgrade retroactively.
- **No litigation hold.** Deletion under a normal retention schedule, after the duty to preserve attached, is spoliation — and spoliation inferences are worse than most evidence. Counsel decides when the hold attaches; IT executes it the same day.
- **Readiness theater.** The retainer signed but never tested, the playbook counsel never reviewed, the write-blocker in a drawer nobody can find. Readiness is verified by drill, not by purchase order.

## 7. Read the source

Primary documents first:

- **NIST SP 800-86, Guide to Integrating Forensic Techniques into Incident Response** (csrc.nist.gov, August 2006) — *read* Chapter 3 (the forensic process: collection, examination, analysis, reporting) and the data-source taxonomy; *note* its age honestly — pre-cloud, but the structure endures. Explicitly an IT view, not a law-enforcement view.
- **RFC 3227, Guidelines for Evidence Collection and Archiving** (rfc-editor.org, February 2002) — *read* all of it; it's short. The order of volatility, transparency, collection steps, and chain of custody in a dozen pages.
- **NIJ, Electronic Crime Scene Investigation: A Guide for First Responders, Second Edition** (ojp.gov, free DOJ publication) — *read* as the field manual for the non-specialist first responder; this is what your one-page card distills.

Then at most three free resources:

1. **NIST SP 800-61 Rev. 3, Computer Security Incident Handling Guide** (csrc.nist.gov, April 2025) — free; where forensics plugs into the incident-response lifecycle this lesson wraps around.
2. **FIRST CSIRT Services Framework, v2.1** (first.org) — free; forensic and investigation services as a defined CSIRT offering — useful when scoping a retainer or building the team.

## 8. Check yourself

1. A first responder arrives to find the suspect's laptop running and docked. They shut it down "to preserve it," then boot it with a forensic USB. Name the two distinct evidence losses and the order-of-volatility principle each violates.
2. Explain why analysts work from hashed copies rather than originals — what specific legal argument does the hash-at-acquisition defeat, and at which later steps must the hash be re-verified?
3. An investigation collects evidence to support an HR termination. Midway, counsel decides a criminal referral is likely. What changes about the handling, and why can't the team "upgrade" retroactively?
4. Distinguish forensic readiness from incident response: which of the four readiness components would have prevented the "logs aged out at 30 days" failure, and who owns that component?
5. Predict the state of a chain-of-custody log six months into an investigation with no form and no procedure: which admissibility argument does the other side make?

## 9. Prove it

**Artifact:** your forensic-readiness assessment (four components scored, gaps with owners and dates), the one-page first-responder card, the chain-of-custody form, and the investigation plan with the three-track decision log — for the Meridian worked case in your own words, or better, for your own environment.

**Honest claim:** "I can design the program that makes investigations possible and run an investigation's evidence handling so findings survive scrutiny — what to collect in what order, how to prove it wasn't altered, when to bring in counsel and law enforcement."
**Can't claim yet:** "I can perform forensic analysis" — the bench work (timelines, memory forensics) is `d-dfir-deep`'s territory; this lesson taught the management and legal frame, not the analysis. Nor "I can give legal advice" — this is issue-spotting for counsel, not counsel.

## 10. Leads to

- `d-dfir-deep` — the analyst's bench this lesson manages: timelines, disk and memory forensics; reread it as the "what the readiness program feeds" companion.
- `c-incident-response` — the response lifecycle investigations run inside or alongside.
- `e-logging-monitoring` — the retention decisions that determine whether evidence exists when you need it.
- `e-bcp-drp` — preservation discipline rhymes with continuity's records discipline.
- Map refs: **CISSP 7.1** (this lesson); feeds **CISSP 7.6** (incident management) and **1.4/1.5** (legal and investigative requirements).

---

*Worked case authored and self-reviewed 2026-10-10; all scenario data fictional. Sources fetched in-session — see `runs/e-investigation-forensics.log`.*
