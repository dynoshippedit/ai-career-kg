---
lesson_id: c-public-track-record
slug: public-track-record
stage: C
level: 3
prerequisites: [c-cvd, c-cve-program, c-vuln-ecosystem, b-methodology]
roles: [security-analyst, pentester]
map_refs: []
test_date: 2026-10-09
description: "Building a public track record: write-ups that teach — root cause first, mechanism re-derivable, honest impact — the Project Zero bar, one finding in two formats. A free lesson in the security guidebook."
dateline: "Worked write-up authored and reviewed 2026-10-09 · no command line in this lesson"
---
# Building a public track record: write-ups that teach


**Map refs:** serves the Stage C professional-recognition track — this lesson is the recognition pathway's keystone: every earlier stage's proof artifacts become entries here.

---

## 1. Where this shows up

The guidebook's thesis, stated in the brief and repeated in every stage, is that skill should leave **public, verifiable evidence**: lab artifacts, reports, disclosed findings, CVE credits, detection work, capstones. This is the lesson that teaches how to make that evidence *count* — how to write a finding so that a stranger, reading it a year later, can see exactly what you proved and how. The formats differ — a research write-up, a bug bounty report, a CVE request, a conference talk — but the bar is one: **mechanism first, claims checkable, limits stated.** A write-up that meets the bar is a credential no issuer can revoke, because it doesn't depend on any issuer at all.

## 2. Before you start

- You have findings worth writing about — from the Stage B labs, the practice targets, the disclosure lessons. If your evidence folder is empty, this lesson still works (the walkthrough uses the SQL-injection lab finding), but the On-your-own step assumes you have at least one real finding of your own.
- You know the disclosure path (`c-cvd`): nothing in this lesson changes the 90-day discipline — you write the finding up *after* the timeline allows publication, never before.
- You know what a CVE record contains (`c-cve-program`): the write-up and the CVE entry are companions, not substitutes.
- Honesty prerequisites, non-negotiable: you will state what you proved versus what you assumed, you will not inflate impact, and you will never publish someone else's finding as your own.

## 3. How it works

### What makes a write-up teach

Study the write-ups the field respects and the same anatomy appears every time:

1. **Root cause first.** One paragraph, before any exploitation detail: what was wrong, in what component, and why it was wrong. The Project Zero discipline — crash → root cause → primitive — exists because readers who understand the cause can find the *class*; readers who only see the exploit can only replay the *instance*. (A *primitive* is a basic capability the exploit is built from — a controlled read, a controlled write, a way to steer execution. Naming the primitive says what the bug *gives* you, before you build anything on it.)
2. **The mechanism from first principles.** Not "I ran tool X and got a shell" but the chain of reasoning: what the code did, what assumption it made, how the assumption was violated, what that violation bought. The reader should be able to re-derive your finding, not just re-run it.
3. **Confirmation.** How you verified it — the request/response pair, the second account, the fixed-build retest. A finding with one observation is a hypothesis; the write-up shows the work that promoted it.
4. **Honest impact.** What you proved (data read, in this table, with these rows) versus what you assumed (and therefore don't claim). Inflated impact is the fastest way to lose a reader's trust permanently.
5. **The fix and its verification.** What the correct fix is, why weaker fixes fail, and the retest that proves the fix holds. A write-up without the fix is a weapon with documentation.
6. **Dead ends, briefly.** What you tried that didn't work — one or two lines. It teaches the search strategy, and it signals that the author actually did the work.

### The formats and what each demands

- **The research write-up** (blog, Project Zero style): mechanism-first, full technical depth, aimed at peers. The bar is novelty of understanding — a new class, a new technique, a surprising interaction. Length is whatever the mechanism needs.
- **The bounty report**: one page, structured for triage — summary, impact, reproduction steps (exact), the fix. The reader is a tired triager (the person who first reviews incoming reports and decides which ones deserve investigation) with fifty reports in the queue; clarity is respect. Reproduction steps must work *exactly as written* — every failed repro burns your reputation with that program.
- **The CVE request**: the permanent record (`c-cve-program`) — product, versions, the independently-fixable flaw, references. Dry by design; the write-up is where the story lives.
- **The talk**: the write-up performed — narrative arc, one mechanism per talk, the demo that proves it. Same bar, different medium.

### The Project Zero bar, concretely

Google's Project Zero publishes under a 90-day disclosure policy (90 days to fix, then details publish; a 2026 "Reporting Transparency" trial announces the report's existence within a week). The deadline is the same mechanism as the embargo in `c-cvd`: without a date, "responsible" publication becomes indefinite delay. Ninety days converts the vendor's promise into a commitment — and the write-up's publication date is the receipt. But the policy isn't the lesson — the *writing* is. Read any two posts and notice: the root cause stated in one paragraph before any exploitation detail; the dead ends documented; the closing recommendations aimed at the *systemic* fix (the whole class), not just the instance. James Kettle's HTTP/2 research is the other template: novel mechanism → real-world validation against real stacks → open tooling and free labs so readers can learn. In both cases the write-up *teaches the class*, and the specific bugs are evidence for the lesson.

### Worked example: one finding, two formats

Take the SQL-injection lab finding from `b-sqli` — the quote probe that returned a 500, the UNION read across tables, the parameterized-query fix. As a **research-style write-up**, it opens with the root cause paragraph: *the search endpoint built its query by concatenating the `q` parameter into the SQL string, so attacker-controlled text became query syntax — the code/data boundary from `b-sqli` section 3, violated at line 41.* Then the mechanism (how the 500 confirmed injectability, how ORDER BY counted columns, how the UNION crossed tables), the confirmation (the fixed build's four verification cases), the honest impact (table contents read in the lab; no claim about production data), the fix (parameterized queries; why escaping is weaker), the dead ends (the first UNION attempt failed on column-count mismatch — corrected, logged).

As a **one-page bounty report**, the same finding compresses: title, severity with the CVSS reasoning, three exact reproduction steps (the curl commands, verbatim), the observed vs expected behavior, the suggested fix. Everything the triager needs, nothing they don't. Compare the two: the write-up teaches the *class* (string-built queries), the report *routes* the instance. Both meet the bar; they serve different readers.

## 4. Walkthrough

**Authored by us** — transcript: `runs/c-public-track-record.log`. No command line in this lesson by design: the work is writing, and the walkthrough is the worked example above plus a self-review checklist, executed against the `b-sqli` lab finding.

Steps: (1) re-read the `b-sqli` run log and extract the finding's facts — separating *observed* (the 500, the UNION output, the 4.0s timing) from *inferred*; (2) draft the root-cause paragraph — one paragraph, no exploitation detail allowed; (3) draft the mechanism section — the chain a stranger could re-derive; (4) draft the honest-impact statement — what was proven in the lab, what is not claimed; (5) draft the fix and verification — parameterized queries, the four retest cases; (6) compress the same finding into the one-page bounty format — title, severity, exact repro steps, fix; (7) run the self-review checklist: root cause first? mechanism re-derivable? every claim checkable? impact honest? dead ends noted? fix verified? disclosure timeline respected? The checklist answers are recorded in the log. Publication of your own write-up is reader-side — this walkthrough builds the muscle, not the audience.

## 5. On your own

Take one finding of your own — a Stage B lab result, a practice-target chain, a disclosure-lesson exercise — and write it twice: the mechanism-first write-up and the one-page bounty report. Run the self-review checklist from the walkthrough on both. Then publish the write-up (your blog, a GitHub repo, the bounty platform's disclosure — wherever your track record lives). Success test: a peer who has never seen your lab can read the write-up and state the root cause, the confirmation, and the fix — and can point at the exact lines that prove each. That published URL is the first entry in your public track record, and the artifact this lesson's Prove-it section asks for.

## 6. Where it goes wrong

- **Hype over mechanism.** "Critical 0-day!!" (a 0-day is a flaw with no patch available, so defenders have had "zero days" to fix it — it is a claim about the *vendor's* state, not your finding's severity) for a finding whose impact section can't name the data at risk. The field has a long memory for inflated severity; one hype write-up costs more credibility than ten quiet ones earn.
- **Claiming unproven impact.** "Could lead to full database compromise" when you read one table. State what you proved; mark the rest as untested. The honest-impact discipline from section 3 is the whole game.
- **Publishing before the timeline allows.** The disclosure lesson's clock governs: vendor deadline first, publication after. A write-up that burns a vendor mid-patch is not research, it's an attack with footnotes.
- **Publishing pwn.college solutions.** Their no-solutions rule is explicit (`d-exploit-concepts`). Mechanics in your own words: yes. Flags, solution scripts, challenge write-ups: no. Violating a community's stated rule in your first public artifact is a remarkable way to start.
- **The write-up as bragging.** If the reader learns nothing they can reuse, it's a trophy, not a track record. The test from section 1: a year later, a stranger, the mechanism re-derivable.
- **Plagiarism, including self-plagiarism of others' work.** Findings are yours or they aren't. Reproducing someone else's published technique without credit is the end of the track record before it starts.

## 7. Read the source

Read the primary material in this order:

1. **Google Project Zero blog** (googleprojectzero.blogspot.com) — read any two recent posts end to end with a pencil: mark where the root-cause paragraph lands, where the dead ends are documented, where the systemic recommendation appears. Study the *structure*, not just the bugs. (Verified active 2026-10-09.)
2. **James Kettle, "HTTP/2: The Sequel is Always Worse"** (portswigger.net/research/http2 — PortSwigger Research, presented Black Hat USA 2021) — read for the research-write-up template: novel mechanism → validation against real stacks → open tooling and free labs. Notice how the tooling section makes the finding *reusable*.
3. **CERT Guide to Coordinated Vulnerability Disclosure** (cert.org) — re-read the publication-timing section from `c-cvd`: the write-up's release date is a disclosure decision, not a marketing decision.

Then at most three free resources, each genuinely free: **PortSwigger Web Security Academy** (free — the lab findings you'll write up first), **the CVE Program's request documentation** (cve.org — the permanent-record companion to every write-up), **your own evidence repo** (free — where every artifact this program produced already lives).

## 8. Check yourself

Answer in your own words — no peeking at section 3:

1. Explain the difference between teaching the *class* and replaying the *instance* — and why the Project Zero root-cause-first discipline serves the former.
2. A lab finding let you read one table via UNION injection. Write the honest-impact statement: what you claim, and the two things you explicitly do not claim.
3. Your bounty report's reproduction steps fail on the triager's machine because you omitted a setup step. Explain what this costs you beyond this one report.
4. Why does the disclosure timeline govern the write-up's publication date — and what does publishing mid-patch turn the write-up into?
5. A peer's write-up opens with three paragraphs of exploit output before stating what was wrong. Rewrite its opening as the root-cause paragraph the bar demands.

## 9. Prove it

**Artifact:** the published write-up URL plus the one-page bounty-format version — the first entry in your public track record.

**Honest claim:** "I can write a vulnerability finding so that a stranger can re-derive the mechanism, check every claim, and verify the fix." **What you cannot claim:** that the finding is novel, that a vendor will act on it, or that one write-up makes you a researcher. The track record is built one honest entry at a time; this lesson is the first entry's template, and the brief's recognition pathway is the reason every earlier stage ended in an artifact.

## 10. Leads to

- `c-cvd` — the write-up's release is a disclosure decision: the timeline, the negotiation, the publication.
- `c-cve-program` — the permanent record that companions the write-up.
- `c-ai-tooling` — where the track record becomes professional evidence: what the field accepts as proof of skill, and how it's sorted.
- `d-exploit-concepts` — when the finding graduates to original research: the capstone write-up series, mechanics-first, under the community's rules.

---

*Walkthrough transcript: `runs/c-public-track-record.log` · The bar: mechanism first, claims checkable, limits stated.*
