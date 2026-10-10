# Engagement methodology: WSTG, PTES, and NIST SP 800-115

**ID:** `b-methodology` · **Stage:** B (Practitioner) · **Level:** 2 (operate: follow the methodology on a prepared target; the vulnerability lessons are the path to 3) · **Prerequisites:** `b-authorization-scope`; Stage A complete.

**Map refs:** OWASP WSTG v4.2 (12 categories, `WSTG-<CAT>-<NN>` IDs); PTES seven phases (verified on the primary page 2026-10-09); NIST SP 800-115 (Final, Sept 2008; three methods, three phases).

---

## 1. Where this shows up

Authorization tells you what you may touch. Methodology tells you what to do with it, in what order, and what each step produces. Without a methodology you poke at random: you find the easy bugs, miss the structural ones, and cannot explain to anyone what you covered. With one, your work is repeatable, your coverage is defensible, and your report writes itself from the artifacts each phase leaves behind. Penetration testers structure whole engagements this way; bounty hunters use the same shape compressed into a single target; SOC analysts will later read your report expecting exactly this structure. The three standards in this lesson are the field's shared vocabulary for "I did the work properly."

## 2. Before you start

- `b-authorization-scope` is complete — you have written a rules-of-engagement document and you can state the six hard rules.
- You can read HTTP traffic (`a-http-depth`) and operate a Linux system (`a-linux-cli`).
- No tools to install for this lesson. The walkthrough is a worked case: you will plan a fictional engagement end to end on paper, producing the documents a real engagement produces.

## 3. How it works

An **engagement** is a bounded piece of security testing: a scope, a window, an objective, a report. A **methodology** is the repeatable process that fills the engagement. Three standards define the shape; they overlap deliberately, and the lesson is in how they fit together rather than in picking one.

**OWASP WSTG — the Web Security Testing Guide** is the community standard for *how to test a web application*. The current stable release is **v4.2 (December 2020)**; v5.0 is in active development but is not the baseline — you report against v4.2 test IDs. The guide is organized into **12 test categories**: information gathering; configuration and deployment management; identity management; authentication; authorization; session management; input validation; error handling; weak cryptography; business logic; client-side; API testing. Every test has a stable ID of the form `WSTG-<CATEGORY>-<NN>` — for example, the IDOR test is `WSTG-ATHZ-04` (verified on the guide's own page, 2026-10-09; note that the authorization-test numbering is easy to misquote — always check the ID on the page, not from memory). You use the WSTG as a checklist and as a citation: finding → test ID → OWASP Top 10 category. Its companion is **OWASP ASVS** (verification requirements in three levels): roughly, ASVS states what should hold, WSTG tests whether it holds.

**PTES — the Penetration Testing Execution Standard** is the engagement-lifecycle standard: seven phases that describe a professional job from first contact to final report. **Pre-engagement Interactions** (scoping, RoE, the authorization this guide's previous lesson built); **Intelligence Gathering** (reconnaissance against the target); **Threat Modeling** (what matters to this organization, where the high-value assets are); **Vulnerability Analysis** (finding candidate weaknesses); **Exploitation** (confirming them); **Post Exploitation** (assessing what they mean); **Reporting** (the deliverable). The PTES Technical Guidelines page was unreachable from some networks during earlier research; it fetched cleanly in-session on 2026-10-09 and all seven phase names were confirmed on the primary page. Cite the phases from the standard, and note the date you checked.

**NIST SP 800-115 — Technical Guide to Information Security Testing and Assessment** (Final, September 2008; it superseded SP 800-42) is the US government's assessment guide, and its value is the frame it puts around the technical work. It defines **three assessment methods**: *testing* (exercising objects under specified conditions — what you normally think of as "the test"), *examination* (checking, inspecting, reviewing — reading configurations, reviewing code and architecture), and *interviewing* (discussions that clarify or locate evidence). And it structures every assessment into **three phases**: **planning** (scope, RoE, rules for handling findings — confirmed in the document's planning-phase section), **execution** (the technical work: identifying vulnerabilities and validating them), and **post-execution** (analysis and reporting — the document treats reporting as occurring alongside the other phases, not as an afterthought). The teaching point: assessment is not only technical testing. When an engagement must verify compliance with policy rather than just find bugs, 800-115 is the citation.

**How the three fit:** PTES frames the engagement — it is the only one of the three that covers scoping, threat modeling, post-exploitation, and reporting as first-class phases. WSTG fills the technical middle with test cases — when PTES says "vulnerability analysis" on a web app, the WSTG categories are the actual tests you run. 800-115 reminds you that examination and interviewing are assessment too, and gives you the planning/execution/post-execution spine for writing the whole thing up. A Stage B web finding typically cites all three layers at once: the WSTG test ID for what you did, the OWASP Top 10:2025 category for what it is, and the PTES phase for where it sits in the job.

**The six phases, each defined by what it produces.** These are the stages of a scoped, authorized test, in order. Learn them as producer-of-artifact pairs:

1. **Scoping** produces the written authorization. Agreeing in writing what may be tested, when, how hard, and what is off-limits. This is the authorization that makes everything after it legal, and it is taught first and hardest — it is the entire previous lesson.
2. **Reconnaissance** produces notes on what is publicly known about the in-scope target. Teach the split: **passive** recon reads public sources without touching the target (DNS records, certificate transparency logs, archived pages, the organization's own publications); **active** recon touches the target (DNS queries against its servers, connecting to its ports). The split matters because active recon is testing, and testing needs scope: a name found in passive recon is a candidate, never permission (hard rule 1). Your recon notes list every candidate *and* its scope status.
3. **Enumeration** produces the attack-surface inventory: hosts, services, endpoints, parameters, versions, technologies — each item tied back to scope. Enumeration turns "the portal" into a concrete list of things to test. It stays inside scope by construction: the inventory is built from the RoE's in-scope assets, and anything discovered that is not in scope goes on the candidate list, not the test list.
4. **Exploitation** produces a confirmed finding: proof, once and minimally, that a candidate weakness is real on an authorized target. The standard is *reproduceable by the defender*: exact requests, exact responses, the impact demonstrated and no further. Not persistence, not spread, not damage. One clean proof beats ten noisy ones, and "I got a shell" is not a finding — the finding is the vulnerability with its root cause, impact, and remediation.
5. **Post-exploitation** produces the impact assessment, written in business terms: what does this finding mean for the organization. What data is reachable, what trust is broken, what the blast radius is. It stays at impact-assessment level — the lesson here is *not* tooling to deepen or maintain access. The question is always "so what, for them," not "what else can I reach."
6. **Reporting** produces the deliverable the whole job exists for: for each finding, root cause, reproduction steps, impact, remediation, and evidence; plus proof you stayed in scope (what you tested, what you excluded, the window you kept). The site's standing position is that the report is the hard part of the job. A brilliant finding in a sloppy report is a rumor; a modest finding in a precise report is a professional product.

## 4. Walkthrough

**Worked case — no command line in this lesson.** You will plan a fictional authorized engagement end to end, producing the scoping document, recon notes, and report outline that a real engagement would produce. Transcript: `runs/b-methodology.log`. Worked and self-reviewed 2026-10-09.

**The fictional engagement.** Harborlight Books again (invented; no real system involved): the customer loyalty portal, `portal.harborlight-books.example` and `api.harborlight-books.example/v2`, window 2026-11-03 to 2026-11-14, 18:00–06:00 ET. You completed `b-authorization-scope`; the RoE from that lesson is this engagement's scoping artifact — reference it, do not rewrite it.

**Step 1 — Write the threat model (PTES phase 3, one page).** What matters to Harborlight Books: customer accounts (names, emails, purchase history), loyalty points (a stored-value equivalent — theft is fraud), the admin interface (price and promotion control). Rank the assets: loyalty-point balances first (direct financial impact), customer PII second (breach-notification impact), admin functions third (integrity of the business). For each, name the attacker who wants it: the fraudster (points), the data thief (PII), the disgruntled insider (admin). This page decides where your testing time goes.

**Step 2 — Write the recon plan and passive recon notes (PTES phase 2).** List what you would read passively: the portal's own pages and JavaScript (in-scope, no touching beyond normal browsing), certificate transparency logs for the domain, archived copies of the portal's public pages. For each item, write the scope status: in-scope assets may be touched; anything else (a `staging` hostname in the JavaScript, a third-party analytics domain) goes on the candidate list with status "not in scope — amendment required." Then write the active-recon boundary: DNS queries against the in-scope names, connecting to the in-scope ports — and nothing else. The recon notes must show the passive/active split explicitly, because that split is where scope violations begin.

**Step 3 — Draft the enumeration inventory (PTES phase 4 input).** From the RoE's in-scope assets, build the table: asset → endpoints observed → parameters → technologies guessed (to be confirmed) → WSTG categories to apply. Example row: `api.harborlight-books.example/v2` → `/points/balance`, `/points/transfer` → `account_id`, `amount` → (to confirm) → WSTG-ATHZ (authorization), WSTG-BUSL (business logic — points are value). Every row traces to an in-scope asset; the candidate list stays separate.

**Step 4 — Write the exploitation proof template (PTES phase 5).** Not an actual exploit — the template your proofs will fill: finding title, WSTG test ID, exact reproduction requests, observed vs expected behavior, impact in business terms (from the threat model), remediation direction. Fill it once with a hypothetical: "WSTG-ATHZ-04: `GET /v2/points/balance?account_id=` returns another customer's balance — fraudster impact: loyalty-point theft at scale." The template forces the discipline: no proof without a test ID, no finding without business impact.

**Step 5 — Write the post-exploitation impact paragraph (PTES phase 6).** For the hypothetical above: what the organization faces — fraudulent point redemption, customer notification obligations, loss of trust in the loyalty program — and what it does *not* face (no evidence, in this hypothetical, of payment-card exposure: say what you did not find, too). Impact assessment stays in business terms; no tooling, no further access.

**Step 6 — Draft the report outline (PTES phase 7).** Executive summary (three sentences: what was tested, what was found, what matters most), scope and methodology (RoE reference, PTES phases followed, WSTG categories covered with a coverage note for any category not applicable), findings (each in the template from step 4, ordered by business impact), remediation roadmap (quick wins vs structural fixes), appendices (scope compliance log: what was tested, what was excluded, the window kept). The outline is the skeleton your real findings will hang on.

**Step 7 — Self-review.** Check: does every artifact trace to the RoE? Does the recon plan show the passive/active split? Does every inventory row name its WSTG categories? Does the proof template require a test ID and business impact? Does the report outline include the scope-compliance log? File the six documents as one engagement plan.

No step above is marked "not run by us" — this lesson's work product is planning, and the planning was done and reviewed.

## 5. On your own

**Task:** Pick one DVWA module (low difficulty). Run it as a methodology exercise, not a bug hunt: write the one-page methodology sheet first — the PTES phases you will touch, the WSTG test IDs you will run, and which 800-115 method (testing, examination, or interviewing) each test is. Then run the tests, and after each one, fill in: what you did, what you observed, the PTES phase it belongs to.

**Success test:** A one-page methodology sheet plus a test log where every entry carries a WSTG test ID, a PTES phase, and an 800-115 method — and one entry where the method is *examination* (reading the module's source or configuration) rather than testing, to prove the point that assessment is not only technical testing. If you cannot find an examination entry, you have not read the module's code yet.

## 6. Where it goes wrong

- **Methodology theater.** The checklist is filled in after the fact to look professional. A methodology you do not follow during the work is decoration. The test log in "On your own" is the antidote: phase and ID recorded *as you go*.
- **Skipping scoping under time pressure.** "The client wants results, not paperwork." The RoE is what makes the results legal. No engagement starts without it — that is the previous lesson, and it is non-negotiable.
- **Recon bleed.** Passive recon shades into active touching without a decision point. Write the boundary before you start (walkthrough step 2), and recheck scope the moment a candidate appears.
- **Exploitation without a proof plan.** Poking until something breaks, then trying to reconstruct what you did. The proof template (walkthrough step 4) exists so the proof is designed before the test, not reverse-engineered after.
- **Post-exploitation creep.** "While I'm in here, let me check…" — every further access needs its own authorization. Impact assessment is the phase; deeper access is a new engagement.
- **The report as afterthought.** Findings written from memory a week later, reproduction steps approximate, scope compliance unstated. The report outline (walkthrough step 6) is drafted at planning time so evidence is collected in its shape.
- **WSTG version drift.** Citing test IDs from memory or from v5.0 drafts. Report against v4.2 IDs and verify each ID on the guide's page — the IDOR test is `WSTG-ATHZ-04`, not the `-02` your memory suggests (confirmed on the primary page in-session, 2026-10-09).
- **800-115 as a formality.** Treating the government guide as irrelevant to "real" testing. Its planning phase is the best written treatment of rules of engagement in the public literature, and its three methods are the vocabulary for work that is not packet-sending.

## 7. Read the source

Primary documents first:

- **OWASP WSTG v4.2** (owasp.org/www-project-web-security-testing-guide/v42/) — *read* the category list and one full test (start with `WSTG-ATHZ-04`, the IDOR test — ID confirmed on the primary page in-session); *use* the guide as the checklist for every web test you run. *Skip* v5.0 drafts for reporting purposes.
- **PTES Technical Guidelines** (pentest-standard.org — Technical Guidelines page) — *read* the seven phase descriptions; this page was unreachable from some networks during earlier research and fetched cleanly in-session on 2026-10-09. If it 403s for you, the phase names are corroborated widely — but cite the date you checked.
- **NIST SP 800-115** (csrc.nist.gov/pubs/sp/800/115/final — Final, September 2008) — *read* the planning phase (rules of engagement, handling of findings); *skim* the execution techniques; *note* the three methods (testing, examination, interviewing) as the frame for non-technical assessment work.

Then at most three free resources:

1. **PortSwigger Web Security Academy** (portswigger.net/web-security) — free; the hands-on companion: every vulnerability lesson in this guidebook maps to Academy topics, and each lab is a chance to practice citing WSTG IDs.
2. **OWASP ASVS** (owasp.org — Application Security Verification Standard) — free; read alongside the WSTG to learn the verify-vs-test relationship: ASVS states requirements, WSTG tests them.
3. **HackerOne Hacktivity disclosed reports** (HackerOne.com/hacktivity) — free; read two reports' methodology sections and map each step the researcher describes to a PTES phase.

## 8. Check yourself

1. A colleague says "I follow PTES" and shows you a report with findings but no scoping section and no threat model. Explain which PTES phases are missing and why their absence undermines the findings that *are* present.
2. You are testing a web app and also reviewing its access-control configuration document. Name the 800-115 method for each activity, and explain why the methodology treats the second as assessment rather than "not real testing."
3. Explain the division of labor between PTES and WSTG on a web-application engagement: what PTES covers that WSTG does not, and what WSTG provides that PTES does not.
4. Your proof-of-concept for an authorization flaw works, but you ran it three times with slightly different requests and are no longer sure which exact request the defender should reproduce. Explain what went wrong methodologically and which walkthrough artifact would have prevented it.
5. The WSTG v5.0 draft renumbers a test you cited as `WSTG-ATHZ-04`. Explain why your published report should still cite the v4.2 ID, and what you must do before citing any v5.0 ID.

## 9. Prove it

**Artifact:** the six-document engagement plan from the walkthrough (threat model, recon plan + notes, enumeration inventory, proof template with one filled hypothetical, impact paragraph, report outline) — or the one-page methodology sheet plus test log from "On your own" against a real DVWA module.

**Honest claim:** "I can structure an authorized engagement end to end — scope it, plan the recon within scope, enumerate to an inventory, prove findings reproduceably, assess impact in business terms, and report it — citing the standard each step comes from."
**Can't claim yet:** "I can find vulnerabilities" — the vulnerability classes are the next lessons. Methodology is the frame; the findings come next.

## 10. Leads to

- **`b-toolbench`** — the fifteen tool phases in activation order: the instruments that execute the methodology's technical phases.
- **`b-practice-targets`** — the local targets where you will run the methodology for real.
- **The `b-sqli`, `b-xss`, `b-…` vulnerability lessons** — each one is a WSTG-category deep dive inside this lesson's frame; each cites its WSTG test ID.
- **`b-authorization-scope`** (back-link) — the scoping phase, expanded to a full lesson: re-read it before every engagement.
- Map refs: **OWASP WSTG v4.2**; **PTES** (seven phases); **NIST SP 800-115**; feeds **CISSP 1.9** (assessment methodology, via Stage E).
