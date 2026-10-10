---
lesson_id: e-test-analysis-reporting
slug: test-analysis-reporting
stage: E
level: 3
prerequisites: [c-cvss, b-methodology]
roles: []
map_refs: ["CISSP 6.4"]
test_date: 2026-10-10
description: "Triage findings, rate risk with context, and write the two-layer report with remediation tracking for a fictional insurer. A free lesson in the security guidebook, serving CISSP objective 6.4."
dateline: "Local demo run and reviewed 2026-10-10 · transcript runs/e-test-analysis-reporting.log"
---
# Test analysis and reporting: from ten thousand findings to decisions


**Map ref:** serves **CISSP objective 6.4** — analyzing test output and reporting.

---

## 1. Where this shows up

Every testing method in `e-control-testing` produces output: scanner lists, pentest notes, review findings. Raw output is not a report — it's inventory. The analysis turns it into decisions: which findings are real, how bad each is, what fixes it, who owns it, and by when. It shows up in the morning after the scan ("ten thousand findings — now what?"), in the pentest report the executives actually read (two pages, not eighty), and in the remediation tracking meeting six months later where the same criticals reappear. Security analysts and the GRC function live here — the report is the deliverable the whole testing program exists for.

## 2. Before you start

- You can score severity (`c-cvss`) and you know the engagement lifecycle (`b-methodology`) — this lesson is the analysis-and-reporting phase done at program scale.
- Every finding below arrives with the method that produced it, which bounds what the finding means: a scanner finding is unverified until triaged, a pentest finding is point-in-time evidence, an audit finding is sampled evidence — the full method matrix is `e-control-testing`'s subject.
- One local demo in §4: Python 3, no packages, no network. The script and its fictional findings list are reproduced so you can run the exact transcript.

## 3. How it works

Analysis has four stages, and skipping any one corrupts the rest: **triage** (is it real?), **risk rating** (how bad?), **reporting** (so what, now what?), and **remediation tracking** (did it get fixed?).

**Triage: the finding must survive contact with reality.** Every finding enters triage with a disposition, and only four exist:

- **Confirmed:** reproduced or verified by a second method — the scanner's match checked by hand, the banner checked against the backport record, the open port connected to.
- **False positive:** the tool was wrong — the version banner (the version string a service advertises — what banner-grabbing scanners read) predates the backported fix (the vendor applied the security patch to the older version without changing the version number, so banner-based scanners misidentify it), the "vulnerability" is a honeypot (a decoy system designed to attract attackers — its intentional weaknesses fool scanners), the finding describes a control that exists under a different name. False positives are *documented and closed*, never silently deleted — next quarter's scan will find them again, and the triage note is what prevents re-work.
- **Duplicate:** two tools, one finding. Merged and counted once — duplicate inflation is how ten findings become thirty on the dashboard.
- **Risk-accepted:** real, but deliberately not fixed — with an owner, an expiry date, and the compensating control named. (Per `e-risk-assessment`'s rule: acceptance without owner and date is abandonment.)

The triage discipline: no finding reaches the report without a disposition, and the analyst who triaged it signs the note. Triage precedes scoring because scoring an unverified finding launders the tool's error into a decision — a false positive scored "critical" becomes the top priority by arithmetic. Automated findings are confirmed by hand — the guidebook's hard rule from `b-toolbench` applies at program scale.

**Risk rating: severity is not risk.** The scanner's severity is a property of the vulnerability; risk is a property of the vulnerability *in your environment*. The rating combines: the technical severity (CVSS base score — `c-cvss`'s work, v4.0's Base/Threat/Environmental/Supplemental groups per the brief), the **exposure** (internet-facing vs internal vs segmented — the zone map from `e-network-architecture` is an input to every rating), the **asset criticality** (the crown-jewel database vs the lobby printer), and **exploitability evidence** (known exploitation in the wild — CISA KEV, the Known Exploited Vulnerabilities catalog — versus theoretical). A "critical" on an isolated test VM is not the organization's top priority; a "medium" with a cleartext admin protocol on the core switch might be. The rating is written as a sentence — "rated high because…" — so the reasoning survives the analyst who wrote it.

**Reporting: the structure that drives action.** The report has two audiences and therefore two layers. The **executive summary** (one to two pages): what was tested, the risk posture in plain language, the top findings with business impact, and the remediation priorities with owners and dates — no CVE numbers, no tool output. The **technical detail**: per finding — description, affected assets, evidence (the proof, reproducible), risk rating with reasoning, remediation guidance (specific, not "apply best practices"), and references. The report also states its own limits: scope, methods, window, and what was *not* tested — the honest negative-result statement from `e-control-testing`. A report without stated limits implies a completeness it doesn't have.

**Remediation tracking: the report is a loan, not a gift.** Findings enter tracking with owner and due date at report delivery — not "when someone gets around to it." The tracking states: the finding, the owner, the due date (by risk rating — criticals in days, not quarters), the verification method (retest, rescan, or evidence review), and the escalation path for missed dates. The metrics lesson's "aged criticals" KRI is fed from this tracker. And the cycle closes: remediated findings are retested by the method the strategy named, and the retest result — pass or fail — is recorded. A finding closed without verification is a finding that moved, not one that died.

### Worked example: Alderpoint Mutual — findings analysis and report excerpt (fictional, continued)

**The scan output (fictional).** The quarterly vulnerability scan returns 8 notable findings (the demo's list — F-001 through F-008).

**Triage dispositions.** F-007 merged into F-001 (duplicate — same expired certificate, second scanner). F-003 held as false-positive candidate: the banner suggests the CVE, but the vendor backported the fix without updating the banner — verified against the vendor advisory, closed as FP with the note that next quarter's scan will flag it again (the note prevents re-triage). The remaining six confirmed by hand.

**Risk rating (excerpt).** F-001 (expired portal cert): rated *high* — internet-facing, PII in transit, trust warnings train users to click through. F-008 (telnet on core switch): rated *high* — cleartext admin credentials on the highest-value network device; scanner said "high," the asset context confirms it. F-005 (missing CSP header): rated *low* alone, noted as an amplifier for any future XSS — the rating says what it is, not what it might become.

**Report excerpt — executive summary (fictional).** "Quarterly scan of the customer portal environment and internal infrastructure, 2026-Q3. Two high-rated findings require action within 14 days: the customer portal's TLS certificate has expired (customer trust impact, 6 days expired at report time), and cleartext Telnet remains enabled on the core switch (administrative credential exposure on the network's highest-value device). Four additional findings are scheduled by priority with owners. One scanner-reported critical was verified as a false positive (backported fix, unchanged banner). Remediation owners and dates are in the tracking register; retesting is scheduled for 30 days."

## 4. Walkthrough

**Local demo — run in-session 2026-10-10.** The triage scorer below was executed on this machine (Python 3.12.3, no network, deterministic); full transcript: `runs/e-test-analysis-reporting.log`. Reproduce it exactly:

1. **Run the scorer.** Save the script (fictional findings F-001–F-008, embedded below) as `triage_demo.py` and run `python3 triage_demo.py`. You should see the prioritized order: F-001 (45), F-008 (30), F-002 (18), F-005 (15), F-006 (8), F-004 (4) — with F-003 held as false-positive candidate and F-007 merged as duplicate. If your output differs, your script differs; the transcript is the reference.
2. **Check the ranking logic.** Note that F-008 (telnet, "high") outranks F-002 (SMBv1, "high") — the scorer multiplies scanner severity by exposure by asset criticality, so equal scanner severities separate on context. This is the lesson's core move: *severity is not risk*.
3. **Verify the triage discipline.** The scorer refuses to score F-003 (held for manual verification — never auto-closed) and F-007 (merged, not double-counted). Change F-003's `fp_signal` to `False` and rerun: it scores 24 and would outrank F-002 — which is exactly why the FP check must happen *before* scoring, by hand.
4. **Write the report excerpt.** From the ranked output, draft the two-layer report: the executive summary (plain language, priorities, owners, dates) and one technical finding in full (description, assets, evidence, rating with reasoning, remediation, references).
5. **Build the tracking register.** Each scored finding gets owner, due date by rating, verification method, and escalation path. F-001 and F-008: 14 days, owner named, retest by rescan plus manual verification.
6. **Close the loop on paper.** Schedule the retest (30 days), name the method, and write the KRI the metrics lesson would compute from this register ("aged criticals").

```python
#!/usr/bin/env python3
"""Findings triage scorer — fictional data, deterministic. No network."""
SEV_W = {"critical": 4, "high": 3, "medium": 2, "low": 1}
EXP_W = {"internet": 3, "internal": 2, "segmented": 1}
FINDINGS = [
    {"id": "F-001", "title": "TLS certificate expired on customer portal",
     "scanner_sev": "high", "exposure": "internet", "asset_crit": 5,
     "fp_signal": False, "dup_of": None},
    {"id": "F-002", "title": "SMBv1 enabled on file server FS-02",
     "scanner_sev": "high", "exposure": "internal", "asset_crit": 3,
     "fp_signal": False, "dup_of": None},
    {"id": "F-003", "title": "Apache banner suggests CVE-2024-XXXXX",
     "scanner_sev": "critical", "exposure": "internet", "asset_crit": 2,
     "fp_signal": True, "dup_of": None},   # backported fix; verify by hand
    {"id": "F-004", "title": "Default credentials on printer PR-07",
     "scanner_sev": "medium", "exposure": "internal", "asset_crit": 1,
     "fp_signal": False, "dup_of": None},
    {"id": "F-005", "title": "Missing Content-Security-Policy header",
     "scanner_sev": "low", "exposure": "internet", "asset_crit": 5,
     "fp_signal": False, "dup_of": None},
    {"id": "F-006", "title": "Open RDP on jump host JH-01",
     "scanner_sev": "medium", "exposure": "segmented", "asset_crit": 4,
     "fp_signal": False, "dup_of": None},
    {"id": "F-007", "title": "Duplicate of F-001 (second scanner)",
     "scanner_sev": "high", "exposure": "internet", "asset_crit": 5,
     "fp_signal": False, "dup_of": "F-001"},
    {"id": "F-008", "title": "Telnet enabled on core switch SW-CORE-01",
     "scanner_sev": "high", "exposure": "internal", "asset_crit": 5,
     "fp_signal": False, "dup_of": None},
]
for f in FINDINGS:
    if f["dup_of"]:
        print(f"[{f['id']}] DUPLICATE of {f['dup_of']} — merge, count once"); continue
    if f["fp_signal"]:
        print(f"[{f['id']}] FALSE-POSITIVE CANDIDATE — verify by hand before scoring"); continue
    score = SEV_W[f["scanner_sev"]] * EXP_W[f["exposure"]] * f["asset_crit"]
    print(f"[{f['id']}] score={score:3d} {f['title']}")
```

## 5. On your own

**Task:** Take real output from a tool you run — a vulnerability scan of your homelab, a linter, even your OS's update list. Triage every item (confirmed / FP / duplicate / accepted), rate risk with asset context in writing, and produce the two-layer report plus the tracking register.

**Success test:** Your report's executive summary fits on one page and names owners and dates; at least one "critical" from the tool was downgraded by context and at least one "medium" was upgraded — with the reasoning written down. If the tool's severities survived untouched, you rated nothing.

## 6. Where it goes wrong

- **The un-triaged dump.** Ten thousand findings forwarded to IT as "the report." Nobody reads it, nothing gets fixed, and the program's credibility dies with it.
- **Scanner severity as risk rating.** The dashboard sorted by the tool's column. Context — exposure, asset, exploitability — is the analyst's job, and skipping it is how the lobby printer outranks the core switch.
- **False positives deleted, not documented.** Next quarter they return, and the triage work repeats forever. The FP note is an asset.
- **Duplicates counted.** Two scanners, one finding, twice the panic. Merge before scoring.
- **The executive summary nobody can act on.** Eighty pages of tool output with no priorities, no owners, no dates. The report exists to produce remediation; everything else is appendix.
- **Missing limits.** No scope, no window, no "not tested" statement. The reader assumes completeness the testing never had.
- **Remediation without verification.** "Fixed" claimed, never retested. The tracker needs the verification method and the retest date at report delivery. The tell: the tracker's "closed" findings with empty verification columns — or the next rescan, still listing them.
- **Risk acceptance as a rug.** Findings swept under "accepted" with no owner and no expiry. Acceptance is a decision with a name and a date, or it's abandonment. The tell: the accepted rows with blank owner and expiry columns.

## 7. Read the source

Primary documents first:

- **NIST SP 800-115** (csrc.nist.gov) — *read* the post-execution phase (§4.4 in the brief's framing; the guide's reporting and findings-handling guidance): what a finding must contain and how it is delivered.
- **FIRST CVSS v4.0** (first.org) — *use* the calculator (verified) and *read* the specification's metric groups (Base, Threat, Environmental, Supplemental) — the severity input your risk rating starts from, not ends at.

Then at most three free resources:

1. **OWASP Web Security Testing Guide — reporting section** (owasp.org) — free; the report structure for web findings: evidence, risk, remediation.
2. **CISA Known Exploited Vulnerabilities (KEV) catalog** (cisa.gov/known-exploited-vulnerabilities-catalog) — free; the exploitability-evidence input: what is known to be exploited in the wild.
3. Your guidebook's own `c-cvss` — the scoring mechanics; `e-security-metrics` — where the tracker's aging numbers go.

## 8. Check yourself

1. A scan reports a "critical" on an isolated lab VM and a "medium" on the internet-facing payment API. Walk the risk-rating reasoning that inverts their priority — name each input (severity, exposure, asset, exploitability).
2. The same expired certificate appears in two scanners' outputs. Explain the triage disposition, why double-counting corrupts the metrics, and what the merged record contains.
3. A banner-based CVE match is disputed: the vendor backported the fix. Lay out the verification steps that decide FP versus confirmed — and what gets documented either way.
4. Write the executive summary for the worked case's two highs in three sentences: what was tested, what needs action in 14 days and why, and what happens next. No CVE numbers allowed.
5. A "remediated" critical is closed in the tracker without retesting. Six months later it's still present. Name the two process failures (tracking, verification) and the strategy-level fix for each.

## 9. Prove it

**Artifact:** your triage output (the scorer's run or your hand triage with dispositions), the two-layer report (executive summary plus full technical findings with evidence and rated reasoning), and the tracking register (owner, due date, verification method, escalation path per finding) — for the Alderpoint worked case reproduced by running the demo, or better, for real tool output you triaged yourself.

**Honest claim:** "I can turn test output into decisions — I can triage findings honestly, rate risk with context instead of parroting scanner severity, write the report both audiences need, and track remediation to verified closure."
**Can't claim yet:** "I can find the vulnerabilities myself" — discovery is the testers' work (`b-methodology`, `b-toolbench`); this lesson taught what happens after the findings land.

## 10. Leads to

- `e-control-testing` — where every finding came from; `e-security-metrics` — where the tracker's aging becomes KRIs.
- `e-assessment-strategy` — the retest commitments this lesson's tracker enforces; `e-security-audits` — the independent check on whether remediation actually happened.
- `c-cvss` — the severity input; `b-methodology` — the engagement report this lesson generalizes to program scale.
- Map refs: **CISSP 6.4** (this lesson); feeds **CISSP 6.2** (methods) and **6.3** (metrics).

---

*Sources fetched 2026-10-10: NIST SP 800-115 (csrc.nist.gov); FIRST CVSS v4.0 calculator (first.org/cvss/calculator/4.0); OWASP WSTG reporting section; CISA KEV catalog. Full ledger in the batch manifest.*
