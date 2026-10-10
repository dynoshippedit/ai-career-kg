---
lesson_id: b-authorization-scope
slug: authorization-scope
stage: B
level: 2
prerequisites: []
roles: [security-analyst, pentester]
map_refs: []
test_date: 2026-10-09
description: "Authorization, scope, and the hard rules: the gating lesson — written authorization, rules-of-engagement contents, the law in plain terms, and the six hard rules quoted verbatim. A free lesson in the security guidebook."
dateline: "Worked case authored and reviewed 2026-10-09 · no command line in this lesson"
---
# Authorization, scope, and the hard rules


**Map refs:** brief §7 (hard rules, authoritative); NIST SP 800-115 (planning / rules of engagement); feeds every hands-on lesson in the guidebook.

---

## 1. Where this shows up

This is the lesson that gates everything after it. Every hands-on lesson in Stage B — every lab you stand up, every PortSwigger exercise, every bounty report you will ever write — assumes you can state, in writing, what you are allowed to touch and why. Bug bounty platforms are scope-first by design: HackerOne, Bugcrowd and Intigriti all define the program by its scope before anything else. Penetration-test engagements begin with a signed rules-of-engagement document, and NIST's assessment guide treats planning as a full phase of the work, not paperwork. A finding obtained outside authorization is not a finding. It is a liability, and neither you nor this site can use it.

## 2. Before you start

- Stage A is complete — you can read traffic and operate a Linux system.
- Nothing to install. You need a text editor and the willingness to write things down.
- Read this lesson's section 3 slowly. The six hard rules at the end of it are quoted verbatim from the guidebook's governing brief. You will write them out by hand in the walkthrough, and you will not touch a hands-on target until you can state all six from memory.

## 3. How it works

**Written authorization** is a document — not a conversation, not an implication, not a terms-of-service page you skimmed — in which the owner of a system says: these assets, these test types, this time window, these accounts, and no further. The document has a name in the industry: **rules of engagement** (RoE). It exists because the default state of the world is that touching someone else's computer without permission is a crime, and the RoE is the narrow, written exception you operate inside.

A complete RoE contains, at minimum:

- **The parties.** Who is authorizing (name, title, organization) and who is authorized (you, by name). "The company" is not specific enough; a person with authority to grant it signs.
- **The objective.** What the engagement is for — "test the customer portal for access-control flaws," not "hack the site." The objective bounds everything else.
- **In-scope assets.** Named exactly: hostnames, IP ranges, URLs, API endpoints, mobile app versions. If it is not named, it is not in scope.
- **Out-of-scope assets.** Named too, especially the things that look in scope: the production database behind the portal, the third-party payment processor, the marketing site on shared hosting. Out-of-scope is written down because "I assumed" has ended careers.
- **The testing window.** Dates and hours. Some systems may only be tested at night; some not at all during business hours. Outside the window, you are not authorized.
- **Permitted and forbidden test types.** What you may do (automated scanning, manual testing, social engineering of in-scope staff) and what you may not (denial of service, phishing customers, physical intrusion, destructive payloads). Forbidden means forbidden even if you think it would prove something.
- **Accounts and access provided.** The test accounts you own, the VPN credentials, the API keys. You test with what you are given. You never use a credential you find — that is hard rule 4, and it applies inside authorized engagements too.
- **Communication and escalation.** Who you contact when you find something critical, how fast, and what to do if you accidentally touch something out of scope: stop, document, report. The accidental-touch procedure is the most important paragraph in the document, because accidents are how scope violations actually happen.
- **Data handling.** What you may collect, where you store it, when you destroy it. Customer data in your screenshots is a second liability on top of the first.
- **Termination.** Either party can stop the engagement. If authorization is withdrawn, you stop immediately — continued testing after withdrawal is unauthorized testing.

Notice what the RoE does: it converts a crime into a job by narrowing it. Every element above is a boundary, and the discipline of this lesson is to treat each boundary as absolute.

**Why the boundary is absolute: the law, in plain terms.** This is not legal advice — it is the shape of the risk, and you must read the actual law and your actual authorization with a professional's care.

In the United States, the **Computer Fraud and Abuse Act (18 U.S.C. § 1030)** makes it an offense to access a computer "without authorization" or to "exceed[] authorized access." The key phrase is the boundary: authorization is what separates testing from a federal offense, and "exceeding" means that even with some permission, going beyond what was granted is covered. A "protected computer" in the statute's terms effectively includes any computer used in interstate commerce — which is to say, any computer reachable over the internet. Penalties include fines and imprisonment, and they scale with the conduct and the damage.

In the United Kingdom, the **Computer Misuse Act 1990** defines three core offenses, and the names tell you the shape: section 1, unauthorized access to computer material; section 2, unauthorized access with intent to commit or facilitate further offenses; section 3, unauthorized acts with intent to impair, or recklessness as to impairing, the operation of a computer. Note section 3's "recklessness": you do not need to intend damage for careless testing to be an offense.

Two honest caveats. First, the legal landscape moves — courts reinterpret these statutes, and new guidance appears. What you read here is the concept, not the current edge of the case law. Second, **safe harbor** (the promise some bounty programs make not to pursue researchers who follow the rules) is a promise from one organization about its own response. It is not immunity, it is not a defense against anyone else, and it only covers you while you are inside the written rules. Read the exact wording of the safe-harbor clause on every program you join. "We will not pursue" and "we consider this authorized" are different sentences with different weight.

**The six hard rules.** These are quoted verbatim from the guidebook's governing brief. They are not suggestions.

1. A name found in recon is a candidate, never permission. Recheck scope before probing, crawling, or sending a request.
2. A scanner match on a known issue is not a new CVE.
3. A bearer token is not a JWT until the format is identified.
4. Never use a credential you find.
5. Secret scanners run with verification off.
6. Automated findings are confirmed by hand.

Each rule exists because someone learned it the expensive way. Rule 1 is the whole lesson in one line: discovery is not authorization. Rule 2 stops you from filing a scanner's guess as your own finding. Rule 3 stops a misidentification from becoming a false report. Rule 4 is the line between testing and unauthorized access — a found credential used "to prove impact" is still used without authorization. Rule 5 keeps your secret-scanning from becoming credential-testing (which would violate rule 4). Rule 6 is the quality bar: the tool proposes, you dispose.

## 4. Walkthrough

**Worked case — no command line in this lesson.** You will produce two documents: a rules-of-engagement document for a fictional engagement, and a scope-violation triage. Transcript: `runs/b-authorization-scope.log`. Worked and self-reviewed 2026-10-09.

**The fictional engagement.** Harborlight Books is a fictional regional bookstore chain. They have hired you — a fictional tester — to assess their customer loyalty portal. Everything below is invented; no real system is involved.

**Step 1 — Write the RoE.** Draft a one-to-two-page rules-of-engagement document containing every element from section 3: parties, objective, in-scope assets (name them: `portal.harborlight-books.example`, `api.harborlight-books.example/v2`, the iOS app build 4.2.1), out-of-scope assets (`payments.harborlight-books.example` — third-party processor; the warehouse inventory system; the corporate email), the testing window (2026-11-03 to 2026-11-14, 18:00–06:00 ET), permitted test types (automated scanning at ≤10 requests/second, manual testing, no DoS, no social engineering, no phishing), provided accounts (two test customer accounts, `tester01` and `tester02`), the accidental-touch procedure (stop, screenshot the request, email the named contact within one hour), data handling (no real customer data in reports; destroy all engagement data within 30 days), and termination (either party, immediate).

**Step 2 — Triage five scope scenarios.** For each, write: in scope or out, which RoE element decides it, and what you do.

1. While testing the portal, you notice `admin.harborlight-books.example` resolves and serves a login page. It is not named in the RoE.
2. Your scanner, running against the in-scope API at the permitted rate, flags a known CVE in the server's TLS library.
3. A test account's welcome email contains a session token for a *different* test user.
4. You find `staging.harborlight-books.example` in a JavaScript file on the in-scope portal. It is not named in the RoE.
5. At 03:00 ET on 2026-11-20 — six days after the window closed — you remember one test you never ran, against the in-scope portal.

(The answers: 1 — out of scope; not named (rule 1: a name found is a candidate, never permission); do not touch it; optionally ask the contact to add it in writing. 2 — in scope to *observe*, but the scanner match is not a finding (rule 2); confirm by hand against the in-scope target, and check whether the CVE is even reachable before writing it up. 3 — in scope; do not use the other user's token (rule 4); report the token-leak as the finding, demonstrated with your own two accounts. 4 — out of scope; found in recon is not permission (rule 1); do not probe it; note it as a candidate for a scope amendment. 5 — out of scope; the window is part of the authorization; testing after it is unauthorized testing, full stop.)

**Step 3 — Write out the six hard rules from memory.** Then check yourself against section 3. Any rule you paraphrased instead of quoting goes back into your notes verbatim. The point is not memorization for its own sake: in the middle of an engagement, the rule you can state exactly is the rule you will follow.

**Step 4 — Self-review.** Read your RoE against the ten-element checklist in section 3. Every element must be present and specific — "the portal" is not an in-scope asset; a hostname is. Read your five triage answers: each must name the deciding element and the action, not just "out of scope." File both documents where you keep engagement records. They are the first artifacts of your practice.

No step above is marked "not run by us" — this lesson's work product is writing, and the writing was done and reviewed.

## 5. On your own

**Task:** Pick three real, public bug bounty programs or vulnerability disclosure policies — one each from HackerOne, Bugcrowd, and Intigriti, or three VDPs. For each, extract into a one-page scope card: (a) the in-scope assets, named exactly; (b) the out-of-scope assets; (c) the forbidden test types; (d) the safe-harbor wording, quoted verbatim. Then write the six hard rules in your own words underneath — and then, separately, the verbatim versions. Keep both: the paraphrase proves you understand them, the verbatim proves you respect them.

**Success test:** A scope card for each of the three programs that a stranger could use to decide "may I test this asset, with this technique, right now" — plus your signed (written, dated) personal rules list: the six hard rules, verbatim, with your name and the date. If any program's safe-harbor wording is ambiguous to you, quote the ambiguous sentence and write down the most restrictive reasonable reading. Restrictive is correct when the alternative is unauthorized access.

## 6. Where it goes wrong

- **Scope creep by curiosity.** "Just one more subdomain" is the most common violation, and it is still a violation when nothing bad happens. The boundary does not bend for good intentions.
- **Permission by silence.** The program didn't answer your scope question, so you proceeded. Silence is not authorization. If the question matters, wait for the answer in writing.
- **The "researcher" framing.** Calling yourself a security researcher does not create authorization. Authorization comes from the asset owner, in writing, naming you.
- **Safe harbor as a shield.** A program's safe-harbor promise covers the program's own response to in-rules testing. It does not bind law enforcement, it does not cover other organizations' systems you touched along the way, and it evaporates the moment you step outside the rules.
- **Responsible disclosure without permission.** Finding a vulnerability in a system you were not authorized to test and then disclosing it "responsibly" does not retroactively authorize the testing. The disclosure can be responsible and the access still unauthorized. This is why coordinated disclosure (Stage C) starts with finding the security contact, not with testing.
- **Using a found credential "to prove impact."** Rule 4 has no exception for thoroughness. Log it, report the exposure, demonstrate with your own accounts.
- **Scanning at engagement scale against a VDP.** A disclosure program that invites reports is not inviting your scanner's full crawl. Read the forbidden-test-types list; rate limits and scope apply to automation too.
- **Assuming scope is static.** Programs change scope. Re-read the policy before each session, not just the first one.

## 7. Read the source

Primary documents first:

- **NIST SP 800-115, Technical Guide to Information Security Testing and Assessment** (csrc.nist.gov/pubs/sp/800/115/final — Final, September 2008) — *read* the planning phase: it is the document that treats rules of engagement and assessment boundaries as part of the methodology, not as paperwork. *Skim* the technique catalogs; *skip* the tool lists (dated).
- **18 U.S.C. § 1030** (law.cornell.edu/uscode/text/18/1030) — *read* the "without authorization or exceeding authorized access" language in subsection (a); *note* how many distinct offenses hang on that one boundary. This is the statute's shape, not legal advice.
- **Computer Misuse Act 1990, sections 1–3** (legislation.gov.uk/ukpga/1990/18/contents) — *read* the three offense headings; *note* section 3's recklessness standard.

Then at most three free resources:

1. **Bugcrowd researcher documentation** (docs.bugcrowd.com) — free; how a real platform defines valid, in-scope, reproducible findings and safe harbor. Read the onboarding and scope sections.
2. **HackerOne Hacktivity — disclosed reports** (HackerOne.com/hacktivity) — free; read disclosed reports' scope and reproduction sections as the textbook for how professionals write scope and proof.
3. **PortSwigger Web Security Academy** (portswigger.net/web-security) — free; every lab is its own authorized target with defined scope — practice reading scope before you touch anything, starting now.

## 8. Check yourself

1. A bounty program's scope lists `example.com` but your recon finds `internal.example.com`, which is not named. You are confident it belongs to the same company. Explain, using hard rule 1, exactly what you may and may not do — and what the correct next step is.
2. Your scanner flags a critical CVE on an in-scope host. Explain why hard rules 2 and 6 both apply before this becomes a finding, and what "confirmed by hand" concretely requires.
3. During an authorized test you receive another user's session token in an error message. Explain what hard rule 4 requires you to do, what you must not do, and how you still produce a valid finding from the situation.
4. A program promises: "We will not take legal action against researchers who follow this policy." Explain the difference between this sentence and "your testing is authorized," and name two situations the promise does not cover.
5. Your testing window ended yesterday and you discover you never tested one in-scope endpoint. Explain why retesting it now is a scope violation, and what the lawful alternative is.

## 9. Prove it

**Artifact:** the rules-of-engagement document and the five-scenario scope triage from the walkthrough, plus your dated personal rules list (the six hard rules, verbatim, signed with your name and date). Three documents, each specific enough that a stranger could audit your decisions against them.

**Honest claim:** "I can state in writing what I am authorized to touch, for how long, and with what techniques — and I can recognize the six hard-rule violations before I commit them."
**Can't claim yet:** "I can conduct an engagement" — methodology, tooling, and the vulnerability classes are the next lessons. Authorization is the gate, not the job.

## 10. Leads to

- **`b-methodology`** — the engagement structured end to end: WSTG, PTES, and NIST SP 800-115, and the six phases from scoping to reporting.
- **`b-toolbench`** — the fifteen tool phases in activation order, each gated by this lesson's rules.
- **`b-practice-targets`** — the local targets where you will practice, each its own written scope.
- Every `b-sqli`, `b-xss`, `b-…` vulnerability lesson — each one opens inside the authorization this lesson establishes.
- Map refs: brief §7 (hard rules); **NIST SP 800-115** planning phase; feeds **CISSP 1.9** (risk framing of unauthorized testing, via Stage E).
