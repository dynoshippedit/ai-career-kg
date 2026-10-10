---
lesson_id: e-board-communication
slug: board-communication
stage: E
level: 3
prerequisites: [e-security-program, e-risk-assessment]
roles: [grc-analyst]
map_refs: []
test_date: 2026-10-09
description: "Board-level communication: translating technical risk into business decisions — the one-page board memo as the worked artifact, what to report, what to leave out, and the director test. A free lesson in the security guidebook."
dateline: "Worked case authored and reviewed 2026-10-09 · no command line in this lesson"
---
# Board-level communication


**Map ref:** brief §5 "Running a security program" (board-level communication); **CISSP Domain 1** (risk communication); NIST CSF 2.0 §5; feeds the Stage E capstone path.

---

## 1. Where this shows up

Every security program eventually faces its real audience: people who control the budget, accept the risk, and do not read firewall logs. The board memo, the quarterly briefing, the incident call where you have ninety seconds — these are the moments when technical work either converts into decisions or dies in translation. Security program leads write them; GRC analysts draft them; CISOs live or die by them. The skill is not "presenting" — it is translation under constraint: turning the register, the metrics, and the threat model into the smallest document that still produces a decision.

## 2. Before you start

- You have a program charter with a measurement plan (`e-security-program`) — the memo reports *on* something real.
- You have a risk register (`e-risk-assessment`) — the memo summarizes it, never reproduces it.
- No tools, no terminal. The work product is a one-page memo. Bring the discipline from both prerequisite lessons: no invented numbers, every figure sourced, business impact first.

## 3. How it works

The board's problem is not ignorance — it is *attention under uncertainty*. Directors decide about cyber risk the way they decide about financial or operational risk: given limited time, what must I know, what changed, and what do you need from me? CSF 2.0 §5 states the translation rule explicitly: express cybersecurity in the general risk-management language executives already use, and integrate it with the enterprise risk picture rather than presenting cyber as a separate universe. Why this rule exists: the board holds the risk-acceptance authority — only it can formally accept a residual risk — and it can only accept what it understands in its own terms. A risk the board never understood is a risk nobody accepted; it just happened. The memo is that rule, applied.

**The one-page structure.** Five sections, in this order, each earning its place:

1. **What we protect and why it matters.** One to two lines: customer data and service availability, and what a breach or outage *costs the business* — contractual penalties, lost customers, regulatory exposure — in plain words. This is the frame; everything after it is detail under this frame.
2. **Where we stand.** Posture vs. target in one sentence: current profile, target profile, the gap that matters most. No maturity-model lecture (a maturity model is a staged scale describing how developed a capability is — ad-hoc, defined, managed, and so on; the Tier concept from `e-security-program` is one) — the sentence exists to orient, not to educate.
3. **Top risks.** Three bullets maximum. Each bullet leads with *business impact*, follows with *technical cause in half a line*, and cites the register ID. "Extended outage of the customer portal if backups fail — restore has never been tested (R-02)." The discipline: impact first is not dumbing down, it is respecting the reader's job — they decide on impact.
4. **What changed since last time.** KRI movements with sources: "Risks above tolerance: 4 → 2 (risk register); mean time to patch internet-facing systems: 21 → 12 days (vulnerability scans)." (KPI: key performance indicator — did we do the work, e.g. patches deployed. KRI: key risk indicator — is the risk changing, e.g. risks above tolerance. KPIs measure effort; KRIs measure exposure.) Trends, not snapshots — a board that sees only the current number cannot tell whether the program is working.
5. **Decisions required.** Numbered asks, each naming the decision type: *approve* (fund this), *accept* (formally accept this residual risk until a date), or *direct* (tell the organization to do this). "1. Approve managed backup testing to close R-02. 2. Formally accept residual risk R-04 until the supplier review completes in Q1." The ask is the memo's reason for existing — a memo with no decisions required is a newsletter.

**Appendix (half page, allowed to spill).** The metric definitions used above and where each number came from: "Risks above tolerance — count of High/Critical risks without a funded response; source: risk register, reviewed [date]." This is where the honesty lives — a director who doubts a number can check it.

**What to report:** posture vs. target; top risks in business-impact language; what changed (trends with sources); what you need decided. **What to leave out:** raw activity counts ("10,000 attacks blocked" — the vanity metric from `e-security-program`, never board material); the full risk register (it has 20 rows; the board gets 3); undefined acronyms (every acronym either defined or cut); technical detail without a business consequence attached; anything you cannot source; and — the hard rule — any number you did not measure. A placeholder labeled "[to be measured]" is honest; a plausible-looking number is a lie that will be quoted back at you.

### Worked example: one-page board memo for Beacon Logistics

Built from the `e-security-program` charter and the `e-risk-assessment` register. Placeholders in brackets are labeled, never filled with invented values.

> **To:** Board of Directors · **From:** Security program lead · **Date:** [date] · **Subject:** Cybersecurity posture and decisions required
>
> **1. What we protect and why it matters.** Beacon's business is customer trust in our shipment data and portal availability. A breach of the customer database triggers breach-notification obligations and customer loss; an extended portal outage stops dispatch and incurs contractual penalties.
>
> **2. Where we stand.** Current posture ~Tier 2 (risk-informed but not yet organization-wide); target Tier 3 (repeatable, formal policy). The gap that matters most: recovery is untested — we believe backups work, we have never proven it.
>
> **3. Top risks.**
> - Extended customer-portal outage if backups fail — restore has never been tested (R-02).
> - Bulk customer-data exposure through the tracking portal's internet-facing search — flaw confirmed in review, fix in progress (R-01).
> - Operations halt from ransomware via the unpatched edge VPN — patch window scheduled, executive sponsor assigned (R-03).
>
> **4. What changed since last quarter.** Risks above tolerance: [n] → [n] (risk register, reviewed [date]). Mean time to patch internet-facing systems: [n] → [n] days (vulnerability scans). Backup restore test: not yet run — first test scheduled [date] (test log).
>
> **5. Decisions required.**
> 1. Approve managed backup testing (quarterly restore tests with documented results) to close R-02.
> 2. Approve the emergency patching window for the edge VPN this month to address R-03.
> 3. Formally accept residual risk R-04 — residual risk is the risk that remains *after* controls are applied, the part you live with, not the part you fixed — (supplier compromise) until the supplier review completes in Q1, or direct accelerated review.
>
> **Appendix — metric definitions and sources.** Risks above tolerance: count of High/Critical risks without a funded response; source: risk register. Patch latency: days from disclosure to deployed fix for internet-facing systems; source: vulnerability scans. Restore-test status: pass/fail with log reference; source: quarterly test log.

Read it the way a director reads it: sections 3 and 5 alone state the top risk and the decisions needed. That is the test the walkthrough applies.

## 4. Walkthrough

No command line in this lesson — the walkthrough is the memo, and the transcript is the authoring log with the self-review checklist: `runs/e-board-communication.log`.

1. **Draft section 1** in two lines of business language. Test: it names what breaks and what that costs — not what the technology is.
2. **Draft section 2** in one sentence: current posture, target, the single gap that matters most. Test: no maturity-model jargon survives unexplained.
3. **Draft section 3**: pick the three highest-priority risks from the `e-risk-assessment` register. Rewrite each as impact-first, half a line of cause, register ID cited. Test: cover the technical detail with your thumb — the bullet still makes sense.
4. **Draft section 4** with two trend lines from the `e-security-program` measurement plan, each with its source. Where real data doesn't exist, write labeled placeholders — and log that you did.
5. **Draft section 5**: two to three numbered asks, each typed approve/accept/direct. Test: each ask names exactly one decision and the risk it addresses.
6. **Write the appendix**: every number's definition and source.
7. **The director test**: hand sections 3 and 5 (only) to your self-review persona — a skeptical director with nine minutes. Can they state the top risk and the decisions needed? Log the verdict honestly, revise, re-test.
8. **Acronym sweep**: every acronym defined on first use or cut. Log each cut.

## 5. On your own

Write the incident briefing version: the same Beacon Logistics, but the edge VPN from R-03 has just been exploited — ransomware is encrypting the file shares, and you have ninety seconds on the incident call with the founders. Write the 150-word verbal briefing: what happened (one sentence), business impact (one sentence), what you're doing (two sentences), what you need decided *right now* (one ask). Then write the paragraph explaining what you cut from the quarterly memo format and why the incident format demands it.

**Success test:** the briefing fits in ninety seconds read aloud, contains exactly one ask, and names no metric that isn't already being measured.

## 6. Where it goes wrong

- **The register as the memo.** Twenty rows of threat-source → vulnerability → impact is the analyst's working document, not the board's. The memo's job is triage, and triage means leaving things out.
- **Burying the ask.** The decisions required sit at the end because the memo earns them — but "at the end" still means *present and numbered*, not implied in paragraph four. A board that has to infer the ask will infer the wrong one.
- **Activity as reassurance.** "The team blocked 10,000 attacks this quarter" feels like good news and means nothing. If it appears in a draft, it is a signal the author doesn't trust the real metrics — fix the metrics, not the sentence.
- **The single security score.** A board that wants one number is asking for comfort, not information. The Tier concept and the KPI/KRI distinction (from `e-security-program`) are the honest answer: posture is a profile, risk is a set of indicators, and any single number hides exactly what the board needs to see. The observable symptom of this failure: a board that never asks a follow-up question. Questions mean the memo landed; silence means it was filed.
- **Unexamined placeholders.** A "[n]" that survives three quarters becomes a number everyone has seen and nobody measured. The appendix's source labels exist to catch this — review them every cycle.

## 7. Read the source

- **NIST CSWP 29 (CSF 2.0), §5** — Improving Cybersecurity Risk Communication and Integration: the bidirectional flow, the translation rule, KPI/KRI families, enterprise-risk integration. This section is the lesson's primary text; read it whole. (NIST CSF page fetched 2026-10-09; the document is CSWP 29.)
- **NIST SP 800-30 Rev. 1, Appendix K** — the risk-assessment report template: executive summary plus detailed body. Read it as the structural ancestor of the memo — what the template puts up front is what executives need first.
- **`e-security-program`'s measurement plan** — your own prior work: re-read it as the memo's data contract. Every number in the memo traces to a metric defined there.

Free resources for going deeper (≤3): the CSF 2.0 document (CSWP 29); SP 800-30 Rev. 1; your `e-security-program` charter (the honest answer — the best reference for *your* memo is the program it reports on).

## 8. Check yourself

1. A director asks "are we secure?" Why is that the wrong question, and what three-part answer does the memo structure give instead? (Posture vs. target; top risks; what changed.)
2. Your draft's section 4 says "attacks blocked: 47,000 (↑12%)." Using the decision test from `e-security-program`, argue for cutting it — and name the metric you'd put in its place.
3. The board wants a single "security score" from 1–100. Make the case against it using the Tier concept and the KPI/KRI distinction, in language a director would accept.
4. You have four risks competing for three bullet slots. Walk through how you choose — and what happens to the fourth risk (it doesn't vanish; where does it go?).
5. Your memo's appendix lists a metric whose source is "analyst estimate." What is wrong with that source label, and what are your two honest options?

## 9. Prove it

**Artifact:** the one-page board memo for Beacon Logistics — five sections plus appendix, placeholders labeled, acronym sweep logged, director test passed and recorded.

**You can claim:** "I can brief leadership on cybersecurity posture, risk, and decisions — translating technical findings into business-impact language, reporting only what I can source, and structuring every communication around the decision it needs."

**You cannot claim:** executive experience; that good communication substitutes for a working program (the memo reports on the charter's program — without it, the memo is fiction with good formatting); or authority to accept risk on a company's behalf.

## 10. Leads to

- The Stage E capstone path: a full program plan for a real (authorized) small organization — profile, register, measurement plan, and board pack — as the level-4 artifact. This lesson's memo is the board pack's core.
- `e-security-program` — the charter this memo reports on; the two lessons are a pair.
- `e-risk-assessment` — the register method behind the memo's risk bullets.
- **Map refs:** brief §5 "Running a security program" (board-level communication, served directly); **CISSP Domain 1** (risk communication).
