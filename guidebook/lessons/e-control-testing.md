# Control testing: choosing the method that proves the claim

**ID:** `e-control-testing` · **Stage:** E (Expert) · **Level:** 3 (select, scope, and sequence test methods for a control set — and say what each result proves) · **Prerequisites:** `b-methodology` (the engagement walkthrough — this lesson is the program-level method-selection view above it), `e-assessment-strategy` (the strategy this lesson's methods serve); no command line in this lesson.

**Map ref:** serves **CISSP objective 6.2** — security control testing methods.

---

## 1. Where this shows up

`b-methodology` walks you through one engagement. This lesson stands one level up: across the year's testing, which method do you point at which control, and what does each method's result actually prove? It shows up when the CISO asks "we scan monthly — why did the pentest still find this?", when an auditor asks "how do you test that control?", and when a vulnerability scan's ten thousand findings need to become a remediation plan. The skill is method selection: matching the question to the method that answers it, knowing what each method cannot tell you, and sequencing them so cheap methods feed expensive ones.

## 2. Before you start

- You know the engagement shape (`b-methodology`) and the annual strategy (`e-assessment-strategy`) — this lesson fills the strategy's method menu.
- The primary spine is NIST SP 800-115's technique catalog: review techniques (§3), target identification and analysis (§4), and vulnerability validation (§5). Read those sections' shape from §7 before the walkthrough.
- No tools. The work product is a method-selection matrix for a fictional company.

## 3. How it works

A **security control** is a safeguard that claims something: "only authorized users reach the database," "systems are patched within 30 days," "changes are approved before deployment." **Control testing** checks the claim. The methods differ in what they observe, what they cost, and — critically — what a negative result means. A scan that finds nothing proves the scanner saw nothing; it does not prove the absence of vulnerabilities. Every method below gets the same three questions: what does it prove, what can't it prove, and what feeds it.

**Review techniques** (SP 800-115 §3) — examine without touching the target's behavior:

- **Documentation review:** read the policy, the architecture diagram, the runbook. Proves the control is *specified*. Can't prove it's *implemented* — the document describing the firewall policy is not the firewall.
- **Log review:** examine what the systems recorded. Proves what *happened* (or what was configured to be recorded). Can't prove completeness — the absence of alerts may mean absence of attacks or absence of logging.
- **Ruleset review:** read the firewall rules, the IAM policies, the group memberships line by line. Proves the *configured* state matches (or doesn't match) intent. Can't prove the running state matches the configuration — drift happens.
- **System configuration review:** compare hosts against a baseline (this is where CIS Benchmarks enter — free, measurable checks per platform). Proves deviation from the baseline. Can't prove the baseline is sufficient — a compliant host can still be vulnerable to what the baseline doesn't cover.
- **Network sniffing:** observe the traffic itself. Proves what actually crosses the wire — the plaintext credential, the unencrypted protocol. Can't prove anything about traffic you didn't capture.
- **File integrity checking:** detect changes to critical files. Proves *change*, not malice — the alert says something changed; the analyst decides what it means.

**Target identification and analysis** (SP 800-115 §4) — build the inventory, then probe it:

- **Network discovery and port/service identification:** find the hosts and what they expose. Proves the *attack surface as the scanner sees it*. Can't prove you've found everything — the scanner sees what responds.
- **Vulnerability scanning:** match observed services against known vulnerabilities. Proves *candidates* — "this looks like CVE-20XX-XXXX on this version." Can't prove exploitability — version banners lie, backports confuse scanners, and a match is a hypothesis awaiting validation. The scan's ten thousand findings are the start of triage, not the end of testing.
- **Wireless scanning:** passive and active discovery of the radio environment. Proves what's broadcasting — including the rogue AP nobody inventoried.

**Vulnerability validation** (SP 800-115 §5) — confirm the candidates:

- **Penetration testing:** attempt to demonstrate impact, minimally and within scope. Proves *exploitability* — the finding a defender can reproduce. Can't prove the absence of other paths — the tester found *a* way in, not *every* way in. This is the expensive method; it follows the cheap ones, validating what they surfaced.
- **Password cracking** (of captured hashes, within authorization): proves *password quality* — the policy says 12 characters, the crack says the users chose "Company2024!". Can't prove much about the authentication system's other weaknesses.
- **Social engineering** (tightly scoped, legally reviewed): proves the *human control* — whether the phishing control and the reporting culture work. Can't be run casually; the authorization and handling rules from the strategy lesson apply doubly.

**Two methods the catalog implies but the program needs explicitly:**

- **Misconfiguration checks:** the continuous version of configuration review — automated comparison of cloud accounts, SaaS settings, and infrastructure against benchmarks and policy. Proves drift, fast. Can't prove secure design — a perfectly configured instance of a bad architecture is still bad.
- **Synthetic transactions:** scripted probes that exercise the control as a user would — log in with an expired password (should fail), attempt the forbidden transfer (should block), submit the oversized file (should reject). Proves the control *behaves* correctly from the outside. Can't prove the internals — it's a behavioral sample, not an audit.

### The selection logic

Match the method to the claim: existence claims ("the policy exists") get documentation review; configuration claims ("all servers match the baseline") get configuration review plus misconfiguration checks; effectiveness claims ("unauthorized access is blocked") get synthetic transactions and penetration testing; detection claims ("we'd see the attack") get log review plus a covert exercise. Sequence cheap before expensive: scan, then validate the scan's candidates with targeted pentesting — never pentest blind when a scan would have aimed it. And every method's output feeds the next: the ruleset review's anomalies become the pentest's targets; the pentest's findings become the retest's checklist.

### Worked example: Alderpoint Mutual — method-selection matrix (fictional, continued)

**Five controls, methods selected with reasons.**

| Control claim | Primary method | Supporting method | What a pass proves / can't prove |
|---|---|---|---|
| Customer portal blocks OWASP Top 10 classes | Annual pentest (validation) | Monthly vuln scans (candidates) + per-release code review | Pass proves the tester couldn't break in *that way, that week*. Can't prove absence of flaws. |
| All servers match the hardening baseline | Quarterly config review vs CIS Benchmarks | Continuous misconfiguration checks | Pass proves baseline conformance on the sample date. Can't prove the baseline covers the threat. |
| Firewall rules implement the boundary table | Quarterly ruleset review | Annual pentest attempts to cross boundaries | Pass proves configured intent. The pentest proves (or disproves) the running reality. |
| Phishing emails are reported, not clicked | Annual scoped social-engineering exercise | Log review of the reporting mailbox + training completion | Pass proves the control worked on the sample. Can't prove culture — one exercise is a snapshot. |
| Customer PII access is logged and reviewed | Monthly log review (sampled) | Annual synthetic transaction: attempt unauthorized access, verify the alert fires | Pass proves logging *and* review happen. The synthetic proves the detection path end-to-end. |

**Sequencing decision recorded:** the pentest is scheduled *after* the quarter's scan and ruleset review, with their outputs handed to the testers as starting intelligence — the expensive method aims where the cheap methods pointed. Retest of last year's highs is a synthetic-transaction suite run by the internal team within 30 days of claimed remediation, not "next year's pentest."

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" is the method-selection matrix above, authored and self-reviewed in-session on 2026-10-10 against SP 800-115 §§3–5. Transcript: `runs/e-control-testing.log`.

1. **List the control claims.** From the risk assessment and the control catalog: what does each control claim? Write the claim as a sentence — "the method tests the sentence, not the control's name."
2. **Assign the primary method per claim.** Existence → review; configuration → review + benchmarks; effectiveness → behavioral/validation; detection → logs + synthetic. Write the reason as one line.
3. **Assign the supporting method.** No control gets a single method where two cheap ones exist. The pair should observe differently (one reads configuration, one exercises behavior).
4. **State what a pass proves — and doesn't.** For each row, write both. This is the section that prevents "the scan was clean" from becoming "we're secure."
5. **Sequence the year.** Cheap before expensive; scans feed pentests; findings feed retests. Draw the dependencies.
6. **Name the retest method per finding class.** Remediated highs get retested by *whom*, with *what method*, within *how long* — in the strategy, not negotiated later.

## 5. On your own

**Task:** Pick three controls on a system you run (your homelab firewall rules, your VPS's SSH config, your backup job). Write the claim sentence for each, select primary and supporting methods, and actually run the cheapest method against each.

**Success test:** At least one method returns something you didn't expect — a rule you forgot, a deviation from your baseline, a log gap. For each control you can state what your test proved and what it explicitly did not prove.

## 6. Where it goes wrong

- **The scan as the verdict.** "We scan monthly and it's clean." A scan proves the scanner's signature set saw nothing matching — it is the weakest form of assurance in the matrix, and treating it as the strongest is the industry's most common self-deception.
- **Pentesting blind.** Paying for a pentest without handing over the scan results and ruleset findings. The testers spend the first week rediscovering what you already knew.
- **Testing existence, claiming effectiveness.** The policy exists (documentation review: pass) therefore the control works (untested). Existence is the cheapest claim; effectiveness is the one that matters.
- **No negative-result discipline.** "The pentest found nothing" reported as "the system is secure." The report must say what was attempted, for how long, against what scope — the negative result's meaning is bounded by the effort.
- **Method monoculture.** Everything gets a vulnerability scan because scanning is what the team knows how to buy. Different claims need different methods.
- **Retest by calendar.** "We'll check next year" for a critical finding remediated in March. The retest method and window belong in the strategy.
- **Social engineering without the legal wrapper.** Run casually, it's an HR and legal incident. The strategy lesson's authorization rules exist for this method most of all.
- **Synthetic transactions that test the happy path.** The login works (pass) — but nobody tested the expired password, the locked account, the forbidden transfer. Behavior testing must include the denials.

## 7. Read the source

Primary documents first:

- **NIST SP 800-115** (csrc.nist.gov) — *read* §3 (review techniques), §4 (target identification and analysis), §5 (vulnerability validation) as the method catalog; *reread* §6.3 (selecting and customizing techniques) as the selection guidance.

Then at most three free resources:

1. **OWASP Web Security Testing Guide** (owasp.org) — free; the method catalog for web applications: what each test proves, organized by category.
2. **CIS Benchmarks** (cisecurity.org) — free; the measurable baseline that configuration review and misconfiguration checks test against.
3. **MITRE ATT&CK** (attack.mitre.org) — free; the adversary-behavior catalog — use it to aim validation testing at the techniques that matter to your threat model.

## 8. Check yourself

1. A monthly vulnerability scan reports zero findings for six months. Explain precisely what this proves, what it doesn't prove, and which method you'd add to answer the unanswered question.
2. The firewall ruleset review passes (rules match the boundary table) but the pentest crosses a boundary. Explain how both results can be true — and which method observed the reality.
3. A control claims "unauthorized PII access is detected." Design the two-method test (one behavioral, one observational) and state what each proves.
4. Why does the strategy sequence scanning before pentesting? Argue the cost case and the intelligence case separately.
5. A pentest finds nothing in its two-week window. Write the honest negative-result statement for the report — what was attempted, what it bounds, and what it must not claim.

## 9. Prove it

**Artifact:** your method-selection matrix — control claims as sentences, primary and supporting method per claim with reasons, what a pass proves and doesn't prove per row, the year's sequencing with dependencies, and retest method plus window per finding class — for the Alderpoint worked case in your own words or a system you run, with at least one cheap method actually executed.

**Honest claim:** "I can choose the right test for each control claim — I can say what each method proves, what it can't prove, how the methods sequence across the year, and how findings get retested."
**Can't claim yet:** "I can perform every method to professional depth" — executing pentests, tuning scanners, and running covert exercises are practitioner skills (`b-methodology`, `b-toolbench`); this lesson taught the selection judgment that directs them.

## 10. Leads to

- `e-assessment-strategy` — the strategy this lesson's methods serve; `e-test-analysis-reporting` — what happens to every method's output.
- `e-security-metrics` — measuring the program: scan coverage, retest rates, finding aging.
- `b-methodology` — the engagement walkthrough this lesson selects methods for; `b-toolbench` — the tools that implement the scanning half of the matrix.
- Map refs: **CISSP 6.2** (this lesson); feeds **CISSP 6.1** (strategy), **6.3** (metrics), and **6.4** (analysis and reporting).

---

*Sources fetched 2026-10-10: NIST SP 800-115 (csrc.nist.gov); OWASP Web Security Testing Guide; CIS Benchmarks; MITRE ATT&CK. Full ledger in the batch manifest.*
