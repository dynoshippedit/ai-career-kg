---
lesson_id: c-ai-tooling
slug: ai-tooling
stage: C
level: 3
prerequisites: [c-public-track-record, ai-governance, c-cvd]
roles: []
map_refs: []
test_date: 2026-10-09
description: "AI tooling professionals use: Anthropic's Cyber Verification Program as the dated worked example — three tiers, what each admits, and why it is access to tooling, never a credential. A free lesson in the security guidebook."
dateline: "Evidence map authored 2026-10-09 · CVP details dated 2026-10-06 (announcement); primary URL to re-fetch at publish"
---
# AI tooling professionals use: the Cyber Verification Program as the worked example


**Map refs:** serves the Stage C professional-recognition track and the AI track — the brief's §3 correction governs this entire lesson.

---

## 1. Where this shows up

Frontier AI models ship with conservative safeguards, and those safeguards block legitimate security work — malware analysis looks like malware creation to a classifier, authorized penetration testing looks like attack planning. The field's answer, so far, is *verified access tiers*: prove you are who you say you are and that your work is legitimate, and the blocks lift for your use case. On **2026-10-06**, Anthropic rebuilt its Cyber Verification Program (CVP) into three such tiers, merging the earlier CVP with Project Glasswing. This lesson uses the CVP as its worked example — dated on every statement, because the program is days old and details will move.

The lesson's purpose is not to get you into the program. It is the brief's §3 correction, taught in full: **the CVP is access to tooling — never a credential, never a milestone, never a CV line.** Its two uses in this guidebook: first, it shows how the field *sorts* professional security work (defensive validation vs. authorized offense vs. safety-critical testing); second, it shows a **public record of reported vulnerabilities being treated as professional evidence** — Anthropic's own example of a qualifying individual is a researcher "with a track record of reported vulnerabilities," which is exactly what Stages B and C build. Standard models still handle routine security tasks — code review, patching known issues, triage — without any program at all.

## 2. Before you start

- **The correction, up front:** nothing in this lesson makes the CVP a certification, a course completion, or a line on a résumé. If you catch yourself describing it that way — or describing anyone else's access that way — re-read this section. Access to better tooling is not proof of better judgment.
- You have a track record to map — or you are building one (`c-public-track-record`). The walkthrough maps *your* evidence against the program's descriptions; it works as a gap analysis either way.
- You understand coordinated disclosure (`c-cvd`): "reported vulnerabilities" means findings handled through a real process, not screenshots of alerts.
- Every dated claim below carries its date. The program was announced 2026-10-06; treat anything undated in other coverage as unverified.

## 3. How it works

### The three tiers (Anthropic, announced 2026-10-06)

The rebuilt program folds Project Glasswing (the invite-only Claude Mythos access for organizations securing critical software) into the CVP. All three tiers cover the same frontier models — Claude Opus 5.5, Sonnet 5.5, Mythos 5.1, and future models — with progressively fewer cyber safeguards. What differs is the verification burden and the work each tier permits:

- **Defense Access** — security operations and incident response, malware reverse engineering, analyzing and validating vulnerabilities. Open to security teams at companies, nonprofits, universities, and government; critical-infrastructure operators of any size; smaller security firms; open-source maintainers; and **individual researchers with a record of reported vulnerabilities**. Anthropic aims to answer applications within a few days. This is the tier the guidebook's reader maps against: the qualifying individual is described in terms of *evidence*, not credentials.
- **Red Team Access** — everything above plus **authorized penetration testing and red teaming**. Organizations only: in-house and government red teams, professional penetration-testing firms, testing limited to systems the organization is authorized to assess. Review takes weeks; applicants get Defense Access while they wait. Even here, real-time blocks remain on actions that could cause physical harm or mass disruption — ransomware deployment is the named example.
- **Specialized Access** — the fewest blocks, for testing safety-critical systems: flight systems, power grids, telecom, interbank transfer, government networks. A limited set of verified organizations, reviewed in depth **in collaboration with the U.S. government**. Existing Glasswing members moved here.

### What the tiers do, on Anthropic's own test

Anthropic ran Claude Opus 5.5 through CyScenarioBench — its evaluation of multi-stage cyber operations, 50 trials — and published the results with the announcement (2026-10-06). Without the program: every task blocked on the first prompt, 0 of 50 completed. Defense Access: 46 of 50 blocked at some point, 4 completed. Red Team Access: no blocks, 34 of 50 completed — the same rate Anthropic measured with no safeguards at all. Read this the way the guidebook teaches you to read vendor numbers: it is **Anthropic's own benchmark, run by Anthropic**, and independent validation was explicitly flagged as absent in coverage. The shape is still informative — the tiers behave as designed, Defense blocks offensive scenarios, Red Team removes the blocks — but the numbers are the vendor's, not the field's.

### What Glasswing found (April–July 2026)

With the announcement, Anthropic published Glasswing's first numbers: partners found **at least 129,000 verified vulnerabilities** between April and July 2026, more than **33,000** rated critical or high severity, plus 5,500 more from Anthropic's own open-source scanning. Anthropic calls these an undercount. Two professional readings: first, the scale argument for the program's existence — verified teams with capable tooling find real vulnerabilities at volume; second, the evidence argument this lesson cares about — *verified vulnerabilities, reported through a process, are the currency the field accepts*. That is the same currency the disclosure lessons teach you to mint.

### The two uses, restated as the lesson's spine

**Use one: how the field sorts professional work.** The tier structure is a map of the profession's own categories: defensive validation (SOC, IR, malware RE, vuln analysis) is one kind of work with one risk profile; authorized offense (pentesting, red teaming) is another, restricted to organizations with authorization to match; safety-critical testing is a third, gated by government review. When you describe your own work — in a write-up, a report, an interview — sort it the same way: what kind of work was it, under whose authorization, with what safeguards. The tiers are useful as *vocabulary* even if you never apply.

**Use two: the track record as evidence.** Defense Access admits individual researchers on the strength of reported vulnerabilities — not degrees, not certifications, not course completions. That is the recognition pathway made concrete by the field itself: the write-ups (`c-public-track-record`), the disclosures (`c-cvd`), the CVE credits (`c-cve-program`) are *the application*. The walkthrough below is the gap analysis: what you have, what's missing, what comes next.

### What doesn't need the program

Anthropic is explicit, and the lesson repeats it because the hype will not: standard models handle routine security work without any program — code review, patching known issues, vulnerability finding in owned source code, triage of security alerts. If your work fits in that list, you don't need access tiers; you need the skills the earlier stages teach. The program exists for the work that *looks offensive to a classifier* — and most professional careers are built entirely in the unblocked list.

## 4. Walkthrough

**Authored by us** — transcript: `runs/c-ai-tooling.log`. No command line by design: the work is evidence mapping, dated 2026-10-09, three days after the announcement.

Steps: (1) restate the three tiers from memory, then check against the table in section 3 — the discipline is dating every claim; (2) inventory your own Stage B–C evidence: bounty profile entries, disclosed findings with timelines, CVE credits, published write-ups, detection rules merged upstream — one line each, with the URL or record; (3) map each item against the Defense Access description: which items count as "a record of reported vulnerabilities" (disclosed through a process, vendor-confirmed or CVE-recorded) versus which are practice (lab findings, unpublished); (4) write the gap analysis: what is missing for the description to fit — typically *vendor-confirmed* disclosures, which is exactly what `c-cvd` teaches; (5) write the next three evidence items as a plan, each with the disclosure path it will travel; (6) write the one-paragraph "never a credential" statement in your own words — the correction internalized, ready for the day someone misdescribes the program to you. The log records the worked example using the guidebook's own fictional track record (the b-sqli lab finding → write-up → disclosure-lesson exercise), mapped honestly: lab evidence, not yet qualifying, with the named next step.

## 5. On your own

Do the walkthrough with your *real* evidence. Inventory everything — every lab artifact, every report, every finding — and sort it into three piles: **reported** (through a disclosure process, with a timeline), **published** (write-up or CVE record, public and verifiable), and **practice** (labs, exercises, unpublished). The gap between the piles is your next quarter's plan, and the plan's items each name their disclosure path. Success test: you can state, in one paragraph, what your track record currently proves to a stranger — and what single next disclosure would most strengthen it. Then check whether the CVP's Defense Access description fits yet; if it doesn't, the answer is more evidence, not a better application.

## 6. Where it goes wrong

- **Listing access as a credential.** "CVP-verified" on a résumé, a badge on a profile, a course-style claim. The program grants tooling access; it certifies nothing. The brief's correction exists because this mistake is already happening.
- **Treating access as expertise.** The tiers sort *authorization and risk*, not skill. A Red Team tier user is not a better operator than a Defense tier user — they are an operator with different authorization.
- **Applying with no track record.** Defense Access for individuals keys on reported vulnerabilities. An application with no evidence is not brave; it's a misunderstanding of what the program selects for.
- **Confusing the tiers.** Applying for Red Team Access as an individual (organizations only), or assuming Specialized Access is "the best one" rather than the narrowest gate for safety-critical systems.
- **Chasing the program instead of the evidence.** The program is three days old as this lesson is written; your track record is the durable asset. Build the evidence — the write-ups, the disclosures, the CVE records — and any program's description will fit when it's true.
- **Citing undated claims.** Coverage of a days-old program moves fast. Every statement you repeat about the CVP should carry its date; undated repetition is how stale tiers become folklore.

## 7. Read the source

Read the primary material in this order:

1. **Anthropic's CVP announcement** (anthropic.com, 2026-10-06 — "Expanding the Cyber Verification Program") — read the tier table and the Glasswing numbers from the vendor's own words; note the publish time. *Gap, stated plainly: the announcement URL was not fetched in this session (the guessed path 404'd); the tier details below are consistent across 6+ outlets dated 2026-10-06–08 and one secondary page that read the announcement directly — re-fetch the primary before publishing.*
2. **The secondary reading** (cellcog.ai/blog/anthropic-cyber-verification-program, read 2026-10-09) — the tier table, the CyScenarioBench numbers, and the Glasswing figures as transcribed from the announcement, with the independent-validation caveat stated.
3. **Anthropic Help Center: real-time cyber safeguards** (support.claude.com) — what the safeguards block in the general product, so you understand what the tiers lift.

Then at most three free resources, each genuinely free: **Project Zero's disclosure policy** (googleprojectzero.blogspot.com — the 90-day clock your future disclosures will run on), **the CERT CVD guide** (cert.org — the process behind "reported vulnerabilities"), **your evidence repo** (free — where the track record already lives).

## 8. Check yourself

Answer in your own words — no peeking at section 3:

1. State the brief's §3 correction about the CVP in one sentence, then explain why mistaking tooling access for a credential harms both the individual and the field.
2. Name the three tiers, who each admits, and what distinguishes Red Team Access from Defense Access beyond "more blocks removed."
3. Anthropic's CyScenarioBench numbers are 0/50, 4/50, 34/50 across the settings. Explain the two caveats a professional attaches before repeating these numbers.
4. A peer says "I'm going to apply for Specialized Access — it's the highest tier." Explain the two misunderstandings in that sentence.
5. Map this fictional evidence set against Defense Access: one CVE credit (vendor-confirmed), two bounty reports (one triaged-valid, one duplicate-closed), three lab write-ups (unpublished). Which items count as "a record of reported vulnerabilities," and what is the single most valuable next step?

## 9. Prove it

**Artifact:** the dated evidence map from the walkthrough — your inventory sorted into reported / published / practice, the gap analysis, and the three-item plan with disclosure paths.

**Honest claim:** "I can describe the CVP's three tiers as of 2026-10-06, state what each admits, and map my own evidence against the Defense Access description — including what's missing." **What you cannot claim:** eligibility, access, or any credential. The program is days old; your track record is the asset. When the description fits, it will fit because the evidence is real.

## 10. Leads to

- `c-public-track-record` — the evidence the map inventories: write the next entry to the bar.
- `c-cvd` — the process that converts a finding into a *reported* vulnerability.
- `c-cve-program` — the permanent record that makes the report verifiable by strangers.
- `ai-governance` — the other side of AI in security: governing the systems, not just wielding the tooling.

---

*Walkthrough transcript: `runs/c-ai-tooling.log` · Every CVP statement dated 2026-10-06 (announcement) or 2026-10-09 (this lesson's verification). Access to tooling — never a credential, a milestone, or a CV line.*
