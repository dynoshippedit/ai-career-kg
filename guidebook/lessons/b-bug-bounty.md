# Bug bounty mechanics: how authorized testing is actually offered to beginners

**ID:** `b-bug-bounty` · **Stage:** B (Practitioner) · **Level:** 3 (apply: read a program's policy cold, stay in scope, and write a triage-ready report) · **Prerequisites:** `b-authorization-scope` (read first — non-negotiable), the Stage B vulnerability classes (`b-idor` through `b-security-headers`).

---

## 1. Where this shows up

Every vulnerability class you have learned to find and fix has to be *found somewhere legal* before any of it matters. Bug bounty programs are the market where that happens: an organization publishes what you may test, under what rules, and what a valid finding is worth to them. The Penetration Tester and Bug Bounty Researcher paths run straight through this lesson, and it is the bridge from Stage B's hands-on skills to Stage C's coordinated disclosure — the program is the training ground where you learn to write a finding up before you ever report one for real.

## 2. Before you start

- `b-authorization-scope` is read and understood. Everything in this lesson is scope discipline applied to someone else's program.
- You can find, reproduce, and fix at least one vulnerability class end to end (any of the Stage B lessons).
- Nothing to install. The walkthrough is a report-drafting worked case — no real program, no real submission, no live target touched.
- Do not create platform accounts or submit anything as part of this lesson. Reading program policies is free; the submission step stays fictional here.

## 3. How it works

A bug bounty program is a standing offer of written authorization. Read it as a legal document first and a treasure map second, because the authorization is the whole point: the same request that is a felony outside scope is contracted work inside it.

**The anatomy of a program.** Every program page has the same load-bearing parts. *Scope* lists the assets you may touch — domains, apps, APIs — and, more important, what is out of scope. Out-of-scope almost always includes the platform's own infrastructure, third-party services the company merely uses, and anything involving other users' data. *Rules of engagement* name the forbidden test types: typically denial of service, social engineering, physical testing, and automated scanning at aggressive rates. *Safe harbor* is the sentence that matters most: the organization states it will not pursue legal action for good-faith testing inside the policy. Safe harbor is what turns the CFAA question from "maybe" into "no" — and it only covers what the policy actually authorizes, so its boundaries are the boundaries of your testing. *Severity and rewards* tie payout (or points, or reputation) to impact, usually through the company's own severity rubric.

**Program types.** A *public* program is open to anyone with an account. A *private* program is invite-only — invitations go to researchers with a track record, which is why your first work happens in public. A *time-bound* program runs for a fixed window, often a launch or a major release. A *VDP* (vulnerability disclosure program) is the same structure with no bounty attached: structured reporting and safe harbor, no payout. VDPs are where many researchers start, because the discipline is identical and the competition is thinner.

**The report lifecycle.** You submit a report: the finding, reproduction steps, and impact. It enters *triage* — the platform's or the company's reviewers reproduce your steps on their side. Triage decides three things: is it in scope, is it reproducible, is it novel (first reporter wins; duplicates are closed as duplicates). A valid finding moves to *reward* and then to *remediation*, after which the company may invite you to *retest* the fix. Some reports are later *disclosed* publicly — HackerOne's Hacktivity is the public archive — and disclosed reports are this lesson's textbook.

**What makes a finding valid.** Three gates, in order: in scope, reproducible by a stranger following your steps, and a genuine security impact rather than a hardening suggestion. Impact is the part beginners under-write. "I can read another user's invoice" is a finding; "I can read another user's invoice, which contains their full billing address and the last four digits of their card, and the endpoint requires no privilege beyond a free account" is a finding triage can act on without asking you a single follow-up question. The difference between paid and closed-as-informative is usually the impact paragraph, not the bug.

**Reading disclosed reports to learn.** Disclosed reports are the only place you can watch real researchers work. Read each one four times, for four different things: how the researcher scoped (what they chose to look at and why); the precision of the reproduction steps (could you follow them cold?); how impact was argued (this is the skill to steal); and what the fix was (this closes the loop back to the Stage B fix lessons). Read ten reports in one vulnerability class before you hunt that class — duplicates are the tuition beginners pay, and reading first is how you skip most of it.

### Worked example: the anatomy of a triage-ready report

Take the IDOR from `b-idor` — alice reads bob's invoice 1043 — and dress it as a submission. A triage-ready report has five parts.

**Title.** One line, mechanism + impact: "IDOR in /invoice endpoint exposes other customers' invoices including billing details." Titles are searchable; triage reads dozens a day.

**Summary.** Three sentences: what the flaw is, where it lives, and the worst honest consequence. "The invoice endpoint accepts an arbitrary invoice ID with no ownership check. Any authenticated user can read any customer's invoice by changing one digit. Invoices contain full billing addresses and partial payment data."

**Reproduction steps.** Numbered, starting from a clean state, with the exact requests. "1. Log in as alice (free account). 2. GET /invoices — note IDs 1041, 1042. 3. GET /invoice?id=1043. 4. Observe 200 OK with owner: bob, including his billing address." Every step must work for a stranger. If a step needs a second account, say so and say both are yours.

**Impact.** The honest worst case, no inflation: who is affected (every customer), what is exposed (the exact fields), what an attacker needs (a free account, one changed digit), and what they cannot do (no write access, no admin functions — say the limits too; restraint is credibility).

**Remediation suggestion.** One paragraph, from the fix lessons: verify ownership against the authenticated identity on every object access, deny by default. You are not the vendor's engineer; you are showing you understand the fix class.

That is the whole craft. Most rejected reports fail at steps 3 or 4: reproduction a stranger cannot follow, or impact asserted instead of shown.

## 4. Walkthrough

**Worked case — no live target, no real submission.** The transcript is `runs/b-bug-bounty.log`: the report drafted below, then self-reviewed against the five-part anatomy.

Take the fictional Harborlight Books shop (the setting used across Stage B). You are alice, a free-tier customer. You found that `GET /invoice?id=N` returns any customer's invoice with no ownership check — invoice 1043 belongs to bob and contains his name, billing address, and the last four digits of his card.

**Step 1 — Write the title.** One line: mechanism, location, impact. Draft it, then cut every word that does not help triage find or route the report.

**Step 2 — Write the three-sentence summary.** Flaw, location, worst honest consequence. Read it back and check: does it name the exact endpoint and the exact missing check?

**Step 3 — Write the reproduction steps.** Numbered from a clean login, both accounts identified as yours, exact request for each step, exact expected response. Then perform the stranger test: hand the steps to your past self from before this lesson. Anything they could not follow gets rewritten.

**Step 4 — Write the impact paragraph.** Affected population, exact exposed fields, attacker prerequisites, and the limits of what the flaw allows. Delete any sentence you cannot defend from the reproduction steps.

**Step 5 — Write the remediation suggestion.** The fix class, one paragraph: ownership verification against the authenticated identity, deny by default.

**Step 6 — Self-review against the anatomy.** Score your draft 0–2 on each of the five parts (0 missing, 1 present but weak, 2 triage-ready). Anything scoring 1 gets one rewrite pass. The checklist and scores are in the log.

**Step 7 — The duplicate check.** Before any real submission you would search the program's disclosed reports for the same endpoint and flaw class. Do the equivalent here: list three ways your finding could already be known (same endpoint disclosed, same class across the app, fixed in a recent release) and what you would check for each. This step is the habit that saves you from the most common beginner outcome.

**Step 8 — The scope re-read.** Re-read the fictional program policy (scope: harborlight-books.example web app only; out of scope: the payment processor, the blog, other customers' accounts used without consent — yours are consented test accounts). Confirm in writing, in the log, that every step stayed inside it.

No step in this walkthrough touches a real system. That is deliberate: the skill being built is the report, and the report is built from a finding you already proved in `b-idor`.

## 5. On your own

Pick a disclosed IDOR or access-control report on HackerOne Hacktivity. Without looking at the researcher's write-up beyond the title, reconstruct the five-part report from the finding description alone: title, summary, reproduction steps, impact, remediation. Then compare against the original.

**Success test:** your reproduction steps let a reader reproduce the finding without the original report, and your impact paragraph names the exposed data and the attacker's prerequisites with nothing you cannot defend.

## 6. Where it goes wrong

**Duplicates.** The most common beginner outcome, and it is tuition, not failure. Two defenses: read disclosed reports in your target area first, and hunt flaw classes the program's history shows it under-tests. Never resubmit a duplicate with reworded steps.

**Scope drift.** The finding is real but the asset was out of scope, or you touched a third-party service on the way. Triage closes these without reward and remembers the researcher. When in doubt, ask through the program's channel before testing — that question is free and it is on the record.

**Unreproducible steps.** "Log in and go to the invoice page" is not a reproduction step. If triage cannot reproduce it in fifteen minutes, it dies. The stranger test from the walkthrough is the fix.

**Impact inflation.** Claiming account takeover from a read-only IDOR, or "could lead to" chains with three unproven links. Triage discounts everything after the first inflated sentence, including the true parts. State the proven impact and stop.

**Testing the platform, not the program.** Scanning HackerOne or Bugcrowd's own infrastructure, or the program's out-of-scope marketing site, is the fastest way to lose an account. Scope is the asset list, not the company name.

**Forgetting the forbidden list.** Automated scanners at aggressive rates, any denial-of-service testing, social engineering of employees or customers, and anything touching real user data without consent are banned in nearly every program. The RoE is not suggestions.

## 7. Read the source

Read the platforms' own researcher documentation first — the program policy is the primary source for this topic, and each platform writes its own.

- **HackerOne's researcher documentation** — how programs, reports, triage, and reputation work on the largest platform. Read the program-structure and report-writing sections; skim the API docs.
- **Bugcrowd's researcher documentation** — the second platform's model: researcher onboarding, what counts as valid, how triage and kudos points work. Compare its validity definition against HackerOne's.
- **HackerOne Hacktivity (disclosed reports)** — the textbook. Read ten reports in one flaw class before hunting it; study scoping, reproduction precision, and impact argument.

Free resources (≤3), each with what it is for:

- **HackerOne Hacker101** — free training modules from the platform itself; the fastest structured on-ramp to the report format triage expects.
- **PortSwigger Web Security Academy** — the lab discipline behind the findings; every flaw class in Stage B has a lab here, all inside authorized scope.
- **Intigriti researcher resources** — the European platform's guides; a third policy model to compare against the first two.

## 8. Check yourself

1. A program's scope lists `*.acme.example` as in scope and `status.acme.example` as out of scope. You find a flaw on the status page. Walk through exactly what happens if you submit it — and what you should have done instead.
2. Two researchers submit the same IDOR an hour apart. The second report has better reproduction steps and a stronger impact section. Who gets the bounty, and why is that the right rule?
3. A report says "this could potentially allow an attacker to maybe escalate to admin." Rewrite the impact as a triage-ready paragraph — or explain why you cannot, and what you would need to establish first.
4. A VDP offers no bounty. Give three reasons a beginner should still consider starting there rather than on a paid public program.
5. Your scan finds the same reflected XSS on twelve pages of an in-scope app. Is that twelve findings or one? Defend your answer from the triage validity gates.

## 9. Prove it

**The artifact:** a complete dry-run report in the five-part anatomy, written against a local lab finding (your `b-idor` or `b-sqli` lab work is ideal source material), self-scored against the walkthrough checklist — and then reviewed against two disclosed Hacktivity reports in the same flaw class, with a paragraph on what the disclosed reports do that yours does not yet.

**What you can honestly claim after this lesson:** you can read a bounty program's policy and state what is authorized; you can write a report that triage can reproduce without asking you questions; you know the beginner failure modes and how to avoid them.

**What you cannot claim yet:** any bounty earned, any live finding submitted, any platform reputation. The walkthrough was a dry run by design. The first real submission happens on a real program, inside its scope, after this lesson — and Stage C's disclosure lessons are where that workflow matures.

## 10. Leads to

- `c-cvd` — Coordinated vulnerability disclosure: the professional version of this workflow when there is no program — finding the contact, the timeline, publishing responsibly.
- `c-public-track-record` — Building a public track record: turning findings into write-ups a stranger can verify — the recognition pathway this whole program is built on.
- `c-cve-program` — The CVE Program: when a finding qualifies for a permanent public identifier with your name on it.

Map references: Stage B milestone lesson (first valid finding submitted to an authorized program); feeds CISSP 1.9 via `e-risk-assessment` (reporting as risk communication); the site's hard rules (brief §7) as the standing authority for every hands-on step.
