---
lesson_id: c-cvd
slug: cvd
stage: C
level: 3
prerequisites: [b-methodology]
roles: [pentester]
map_refs: []
test_date: 2026-10-09
description: "Coordinated vulnerability disclosure: finding the security contact, writing the report, negotiating the timeline, publishing responsibly — Heartbleed vs the zero-day drops. A free lesson in the security guidebook."
dateline: "Worked case authored 2026-10-09 · local security.txt lab run; no command line beyond it"
---
# Coordinated vulnerability disclosure


**Map ref:** Stage C milestone lesson — a completed coordinated disclosure is half the stage's milestone.

---

## 1. Where this shows up

Everything before this lesson taught you to find flaws on targets you are allowed to touch. The moment you find a real flaw in software you do not own, you have a second problem: telling the people who can fix it without getting users hurt, getting yourself threatened, or watching the flaw get exploited while everyone argues. Coordinated vulnerability disclosure (CVD) is the professional answer — the process the industry converged on after decades of learning what happens without one. It shows up in security-engineer job descriptions ("experience with coordinated disclosure"), in bug bounty work (every valid report is a small disclosure), and in the public record the later Stage C lessons build on: a CVE credit starts with a disclosure done right.

## 2. Before you start

- You can prove a vulnerability with a minimal, reproducible demonstration (Stage B). Disclosure without proof is a rumor; proof without restraint is a weapon.
- Read the CERT Guide to Coordinated Vulnerability Disclosure's quick-start and roles sections (see §7) — this lesson follows its model.
- You understand the authorization boundary cold: this lesson is about reporting flaws you *found*, never about finding flaws by testing systems you were not invited to touch.
- No tools. The work products are documents: a report, a timeline, a published advisory.

## 3. How it works

A **vulnerability** becomes a **disclosure problem** the moment someone other than you needs to act on it. The actors have names, and the names matter because each one has different incentives:

- **Finder** — you. You discovered the flaw.
- **Reporter** — the party who notifies the vendor. Often the finder, sometimes a coordinator or a bounty platform.
- **Vendor** — the party who can fix it (the software's maintainer or company).
- **Deployer** — everyone running the software. They cannot fix the code; they can only patch, mitigate, or wait. They are the people harmed when disclosure goes wrong.
- **Coordinator** — a neutral third party (CERT/CC is the classic example) who relays between finder and vendor when direct contact fails or when multiple vendors are affected.

The process, adapted from ISO/IEC 30111:2019 and taught the CERT way, runs in phases: **Discovery** (you find and confirm it) → **Reporting** (private notification to the vendor) → **Validation and prioritization** (the vendor confirms and scopes the fix) → **Remediation** (the patch is built) → **Public awareness** (the advisory and, usually, the CVE record) → **Deployment** (deployers patch). The phases overlap in practice; the order does not change.

What makes it *coordinated* is the agreement at the center: the finder gives the vendor a private head start, and the vendor commits to a fix and a publication date.

**Why the embargo exists — and whose interests it serves.** The **embargo** is the agreement to keep the flaw private until the coordinated publication date, so the vendor can build a fix before attackers learn the flaw exists. It is a three-way trade. The *vendor* gets time to build a correct fix instead of a rushed one. The *deployers* get a patch waiting on the day the flaw goes public. The cost is paid by the *finder* (delayed publication) and by *users* (anyone who already knows the flaw can exploit it during the wait). The deadline exists because an open-ended embargo serves only the vendor: a fixed date converts "trust us, we're fixing it" into a commitment.

The CERT guide's principles are worth memorizing because they resolve nearly every judgment call you will face:

- **Reduce harm** — every decision is scored by who gets hurt and how badly.
- **Presume benevolence** — assume the other side is acting in good faith until proven otherwise. Most disclosure fights start with someone assuming malice.
- **Avoid surprise** — no party learns about the disclosure from a third party. The vendor does not learn from Twitter; you do not learn the patch shipped from a changelog.
- **Incentivize desired behavior** — the process should make the *next* finder want to report, and the *next* vendor want to respond well.
- **Ethical considerations** — you hold a live flaw in software strangers depend on. Act like it.
- **Process improvement** — every disclosure ends with asking what the process got wrong.

**Finding the security contact** is the first practical step, and there is a right order. Check for a `security.txt` file first: `/.well-known/security.txt`, falling back to `/security.txt` (RFC 9116). A good one names a contact, an expiry date, an encryption key, and the policy. If there is no security.txt, look for a `SECURITY.md` in the project's repository, then the project's security page, then a general contact with a clear subject line. Document every attempt with dates — "I tried to reach them" is only credible with a paper trail.

**The report** is a technical document, not a negotiation. The OpenSSF finder guide's structure is the professional standard: what the software and version are, what the flaw is, how to reproduce it (exact steps), what the impact is (proven, not assumed), and what you suggest as a fix. Write it so the advisory can be derived from it later. Include your disclosure expectations plainly: that you intend to publish after an agreed date, and what that date is. Ambiguity here is where relationships die.

**The timeline** is the coordination itself. A common shape: private report on day 0; vendor acknowledgment within days; agreement on a fix target (30–90 days is the normal range — Google's Project Zero publishes a 90-day policy with a 30-day adoption wait after patching, which is the industry's best-known explicit clock; the adoption wait is the extra month *after* the patch ships before the technical details publish, so users get time to install the fix before the exploit instructions go public); check-ins if the vendor goes quiet; coordinated publication when the patch ships (or at the deadline if the vendor stalls, with the vendor warned in advance). If the vendor is unresponsive, a coordinator (CERT/CC) or a CNA can relay. If the vendor is hostile, you still do not publish the exploit — you publish the *existence* of the flaw and the fact that the vendor was notified, on the agreed date, and let the pressure work.

### Worked cases: one good, one bad

**The good pattern — Heartbleed (CVE-2014-0160), coordinated but imperfect.** In early April 2014, two parties independently found the OpenSSL heartbeat flaw: Google's Neel Mehta reported privately to the OpenSSL team on April 1; Codenomicon notified Finland's NCSC-FI on April 3. The OpenSSL team prepared a patch; public disclosure landed with OpenSSL 1.0.1g on April 7, alongside the CVE record and coordinated announcements. The bones were right: private vendor notice, an embargo, a same-day patch. The execution drew criticism that still teaches: only a tiny circle got pre-notification while roughly one-sixth of the internet's trusted web servers were vulnerable, so downstream vendors and deployers scrambled. The lesson the field took: coordination must include the *deployers*, not just the vendor — telling the fixer is half the job; getting the fix to the people running the software is the other half.

**The bad pattern — the 2018 zero-day drops.** In August 2018 a researcher posted a Windows local-privilege-escalation zero-day — a flaw with no patch yet, so the vendor has had "zero days" to fix it — on social media with a public proof of concept, with no prior notice to the vendor. The vendor had no patch ready; the flaw was exploited in the wild within days; more drops followed. Nothing was learned that a private report would not have taught, and users absorbed the entire cost. This is the case study for why CVD exists: full disclosure without notice maximizes user harm, teaches the vendor nothing they could act on, and — the part finders forget — teaches the *next* vendor to treat the next finder as a threat.

## 4. Walkthrough

**Worked-case lesson with one runnable lab.** The "run" for this lesson is the disclosure package itself, authored and reviewed in-session on 2026-10-09, plus a local `security.txt` lab. Transcript: `runs/c-cvd.log`.

1. **Write the contact file.** Create `/.well-known/security.txt` for the fictional Harborlight Books (the company from `b-authorization-scope`), with `Contact`, `Expires`, `Encryption`, `Preferred-Languages`, and `Policy` fields. The run validated it: required fields present per RFC 9116, `Expires` parses and is future-dated, and the lookup order (`/.well-known/` first, `/security.txt` as fallback) was demonstrated.
2. **Draft the report.** For a fictional finding (an IDOR in Harborlight's order history — the class from `b-idor`), write the report: affected product and version, the flaw, exact reproduction steps, proven impact, suggested fix. One page of technical writing; no adjectives about severity that the evidence does not support.
3. **Set the timeline.** Day 0: private report to the security contact. Day 3: acknowledgment expected; if none, follow up through a second channel. Day 7: propose the fix target (60 days) and the publication date in writing. Day 30: check-in. Day 60: coordinated publication — advisory, CVE request, your write-up. Write the "vendor goes quiet" branch now, while you are calm: at day 14 of silence, engage a coordinator; at the deadline, publish existence and notification facts, never the exploit.
4. **Draft the advisory.** The public document: what is affected, what the impact is, what users should do (patch to version X, or the mitigation), who found it, the timeline of the coordination. This is the document the deployers read — write it for them, not for other researchers.
5. **Self-review.** Read the whole package as the vendor's security lead on a bad day: is anything in the report unproven? Is the timeline fair? Does the advisory give deployers an action? Fix what fails.

## 5. On your own

**Task:** Pick a real open-source project you use that publishes a security policy (find it via its `SECURITY.md` or `security.txt`). Do not test the project. Write the complete disclosure package you *would* send if you found a flaw: the report template filled with a clearly labeled fictional finding, the timeline with dates, the advisory draft, and the "vendor goes quiet" branch. Then write a one-paragraph postmortem of the Heartbleed disclosure: who was Finder, Reporter, Vendor, Coordinator; where the embargo held; what you would change.

**Success test:** A stranger reading your package can tell exactly what you would do on day 0, day 14 of silence, and day 60 — with no step requiring improvisation. Your Heartbleed postmortem names the deployer-notification gap specifically.

## 6. Where it goes wrong

- **Publishing before notifying.** The single most harmful mistake. Once the details are public, every unpatched deployer is exposed and you cannot unpublish.
- **The vague report.** "Your site has vulnerabilities, contact me" is not a report — it is indistinguishable from extortion. Specifics or nothing.
- **Negotiating with the vulnerability.** Threatening to publish unless paid, or unless the vendor meets demands unrelated to fixing the flaw, converts a disclosure into coercion. Bounty terms are negotiated with platforms, not with fear.
- **Testing to "confirm" on systems you were not invited to touch.** Finding a flaw does not retroactively authorize the testing that found it. Report what you found through authorized means; do not expand scope to "be thorough."
- **The silent vendor panic.** A vendor that goes quiet for two weeks is usually overwhelmed, not hostile. The coordinator path exists for exactly this. Escalate the *process*, not the rhetoric.
- **Over-claiming impact.** "Could allow full system compromise" when you proved read-only access destroys your credibility with the one team whose cooperation you need. Proven impact only.
- **Forgetting the deployers.** The Heartbleed lesson: the disclosure is not complete when the vendor patches. It is complete when the advisory tells deployers what to do.

## 7. Read the source

Primary documents first — read them in this order:

1. **The CERT Guide to Coordinated Vulnerability Disclosure** (certcc.github.io/CERT-Guide-to-CVD/) — the model this lesson follows. Read: the quick-start ("in a Nutshell"), Principles, Roles, Phases. Skim: Preparation, Operation, Troubleshooting. This is the professional reference you will return to.
2. **OpenSSF Guidance for Security Researchers (finder guide)** (github.com/ossf/oss-vulnerability-guide, `finder-guide.md`) — the finder's perspective for open source: disclosure options, how to write a complete report, the "Getting a CVE ID" section, what to do about unresponsive maintainers, and the SECURITY.md/embargo templates. Read the report-writing and troubleshooting sections end to end.
3. **RFC 9116 — security.txt** (rfc-editor.org/rfc/rfc9116) — the contact-file standard: required fields, lookup order, expiry semantics. Short; read it whole.

## 8. Check yourself

1. You find a flaw in a vendor's product. Their site has no security.txt, no SECURITY.md, and no security page — just a general contact form. Walk the CERT contact-finding order: what do you try, in what order, and what do you document at each step?
2. The vendor acknowledges your report but proposes publishing the advisory in six months, with no patch date committed. Which CERT principle does this violate, and what is your counter-proposal?
3. Why does the OpenSSF guide insist the report be written so "the advisory can be derived from it"? What goes wrong when the report and the advisory are written as separate documents by different people?
4. A researcher publishes a zero-day on social media with no vendor notice, arguing "the vendor would have sat on it." Using the SandboxEscaper case, explain who paid the cost of that decision and what the coordinated alternative would have changed.
5. Your disclosure timeline hits day 14 of vendor silence. Name the exact next step from this lesson's walkthrough — and what you must not do.

## 9. Prove it

**Artifact:** the complete disclosure package for a fictional finding (report + timeline + advisory draft + the "vendor goes quiet" branch), plus the one-paragraph Heartbleed postmortem. Publish the postmortem on your blog or GitHub — it shows you can reason about disclosure, not just recite the phases.

**Honest claims after this lesson:** you can run a coordinated disclosure end to end — find the contact, write the report, negotiate the timeline, publish responsibly. **Cannot yet claim:** a completed real-world disclosure. That requires a real flaw and a real vendor; this lesson is the rehearsal. The milestone is real when the advisory is.

## 10. Leads to

- `c-cve-program` — the CVE ID request is the public half of the disclosure you just ran; the credits field is where your name goes.
- `c-vuln-ecosystem` — after disclosure comes prioritization: where your finding sits in everyone else's queue.
- `b-methodology`'s reporting phase is the prerequisite skill; this lesson is that phase with a clock and a vendor attached.
