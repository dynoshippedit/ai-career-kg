# The surrounding catalogs: CWE, CAPEC, KEV, EPSS — and where enrichment comes from now

**ID:** `c-vuln-ecosystem` · **Stage:** C (Professional) · **Level:** 3 (prioritize a vulnerability queue using the catalogs together, and defend the ranking) · **Prerequisites:** `c-cvss` (severity), `c-cve-program` (records).

**Map ref:** Stage C — the prioritization lesson; the other half of the stage's "professional" claim.

---

## 1. Where this shows up

A CVE record tells you a flaw exists. It does not tell you what to do first. Every security team on earth faces the same queue — thousands of CVEs, finite patching windows — and the industry built four catalogs to answer "what first," each answering a different question. This lesson is where they come together: the weakness taxonomy, the attack-pattern catalog, the exploited-in-the-wild list, and the exploitation forecast. It also teaches the 2026 change that rearranged where all of this data comes from: NIST no longer enriches every CVE, so the professional has to know which source each field comes from and what "no data" actually means.

## 2. Before you start

- You can score severity by hand (`c-cvss`) and read CVE records (`c-cve-program`).
- You accept the lesson's central discipline: **no single number prioritizes anything**. CVSS answers "how bad," EPSS answers "how likely," KEV answers "is it happening." A queue sorted by one of them is a guess with arithmetic.
- Primary sources: **cwe.mitre.org**, **first.org/epss**, **CISA's KEV catalog**, and the U.S. Commerce OIG report OIG-26-020-I (2026-05-26) for the NVD change — all fetched on 2026-10-09.

## 3. How it works

**CWE — the weakness vocabulary.** The Common Weakness Enumeration is MITRE's catalog of *what went wrong in the code*: the root-cause types. CWE-79 is Cross-site Scripting, CWE-89 is SQL Injection, CWE-352 is Cross-Site Request Forgery, CWE-787 is Out-of-bounds Write. Every finding you write up should carry its CWE — it is the shared vocabulary that scanners, employers, and other researchers all speak. MITRE publishes the **CWE Top 25** (current edition: **2025**, computed from 39,080 CVE records): the most dangerous weakness types by prevalence and severity, led by CWE-79, CWE-89, CWE-352, CWE-862 (Missing Authorization), CWE-787. There is also a Top 10 KEV Weaknesses (weaknesses ranked by presence in exploited CVEs) and an "On the Cusp" list. Use: when you map each of your Stage B findings to its CWE, you are building the taxonomy your future employer queries.

**CAPEC — the attack-pattern catalog.** Where CWE names the weakness, the Common Attack Pattern Enumeration and Classification names *how the weakness gets attacked*: the attacker's-side patterns, mapped to CWEs. In a write-up, the CWE names the root cause and the CAPEC entry names the attack pattern — together they say "this kind of flaw, exploited this kind of way." (Catalog-level treatment here; the lesson sends you to capec.mitre.org for the patterns in your write-ups.)

**CISA KEV — what is being exploited right now.** The Known Exploited Vulnerabilities catalog lists CVEs with *reliable evidence of active exploitation in the wild*, each with remediation guidance and a due date. A CVE is added only with a valid ID, exploitation evidence, and clear remediation. Under federal Binding Operational Directive 26-04, agencies must remediate KEV entries — which makes KEV membership the industry's strongest "fix now" signal. Anyone can nominate an exploited CVE. Each entry also carries a known-ransomware-use field. Use: KEV membership outranks every score. A CVSS 5.5 in KEV beats a CVSS 9.8 that nobody is touching — because the question "is it happening" dominates "how bad."

**EPSS — what will probably be exploited soon.** The Exploit Prediction Scoring System, maintained by FIRST's EPSS Special Interest Group, is a data-driven model estimating the **probability (0–1) that a CVE will be exploited in the wild in the next 30 days**, published daily with ranking percentiles for every CVE, freely available via API, CSV, and GitHub. EPSS answers "how likely" where CVSS answers "how bad." The professional move is combining them: high CVSS *and* high EPSS is the patch-first set; high CVSS with near-zero EPSS can wait behind medium CVSS with high EPSS.

**Where enrichment comes from now.** This is the 2026 change the whole lesson is built around. The National Vulnerability Database used to enrich every CVE with a NIST CVSS score, a CWE classification, and CPE product mappings. It no longer does. On **April 15, 2026**, NIST moved to risk-based enrichment: it now enriches only **prioritized** CVEs — those in CISA's KEV catalog, those affecting software the federal government uses, and those in critical software as defined by Executive Order 14028 — with KEV entries targeted for enrichment within one business day. Everything else is published but marked **"Not Scheduled"**: no NIST score, no NIST CWE, no NIST product mapping. The unenriched backlog is being reclassified the same way. NIST also no longer issues its own severity score when the submitting CNA already scored the CVE, and anyone can request enrichment of a specific CVE via nvd@nist.gov.

The sourcing is worth stating precisely, because the lesson's honesty depends on it: the April 15, 2026 change was announced by NIST's Harold Booth at VulnCon26 and reported consistently across industry outlets; it is **government-confirmed via the U.S. Commerce OIG's evaluation report OIG-26-020-I** (May 26, 2026), which states that NIST "publicly announced updates to NVD operations, on April 15, 2026" and "will only enrich vulnerabilities that meet its new criteria, meaning it will no longer assign a score for each vulnerability." There is no NIST-direct announcement page this lesson could find — so the lesson describes the policy as government-confirmed via OIG, not NIST-direct. That distinction is the site's "no verification URL, no row" rule applied to itself.

**What this means for you, practically.** Severity, weakness, and product data for a CVE now come from up to three places, in this order: (1) the **CNA's own record** — its CVSS, its CWE, its affected-product list, as published by the assigner. This is now the *default* source of truth for most CVEs. (2) **NVD enrichment** — but only for prioritized CVEs. (3) **ADP containers and community sources** for the rest. And the cardinal rule: **"no NVD score" means "not yet analyzed," never "not serious."** The absence of enrichment is a statement about NIST's queue, not about the vulnerability.

### Worked example: three CVEs, three rankings

Fetched live on 2026-10-09 (transcript: `runs/c-vuln-ecosystem.log`):

| CVE | CVSS v3.1 | EPSS (30-day) | EPSS percentile | KEV |
|---|---|---|---|---|
| CVE-2021-44228 (Log4Shell) | 10.0 | 0.99999 | 100th | **Yes** |
| CVE-2022-41741 (NGINX mp4) | 7.0 | 0.00794 | 55th | No |
| CVE-2023-3089 (OpenShift FIPS) | 7.5 | 0.00520 | 42nd | No |

Three rankings of the same three flaws:

- **CVSS-only:** 44228 (10.0) → 3089 (7.5) → 41741 (7.0). Clean, defensible, and wrong about what matters: it treats a 7.5 nobody is exploiting as more urgent than a 7.0 nobody is exploiting, based on decimal dust.
- **EPSS-only:** 44228 (0.99999) → 41741 (0.00794, 55th percentile) → 3089 (0.00520, 42nd). Note the reversal: EPSS says 41741 is *more* likely to be exploited than 3089, disagreeing with CVSS's order. The probabilities are all small except 44228's — which is the point: EPSS separates "the one" from "the rest."
- **KEV-first:** 44228 first, by a mile — it is under active exploitation with a federal due date. The other two are not scheduled for KEV-driven remediation at all.

All three agree 44228 is first. They disagree about the order of the rest — and the disagreement is the lesson: a CVSS-only queue patches 3089 before 41741; an EPSS-informed queue reverses them; a KEV-first queue does not care about either until 44228 is handled. The SOC you will work in uses all three, in that order of authority: KEV membership, then EPSS, then CVSS.

## 4. Walkthrough

**Runnable.** Transcript: `runs/c-vuln-ecosystem.log` (2026-10-09).

1. **Pull EPSS for three CVEs.** `curl "https://api.first.org/data/v1/epss?cve=CVE-2021-44228"` — the run recorded epss, percentile, and date for all three. Note the date on the response: EPSS is daily data; a score without its date is stale on arrival.
2. **Check KEV membership.** Download the CISA KEV CSV (the run: 1,051,684 bytes, fetched 2026-10-09) and grep for each CVE ID. Record yes/no — and for the yes, read the due date and the known-ransomware-use field.
3. **Assemble the comparison.** Build the three-row table above: CVSS (from the record or `c-cvss`), EPSS + percentile, KEV yes/no. This table is the prioritization input — everything before it was data collection.
4. **Rank three ways and defend one.** Write the CVSS-only, EPSS-only, and KEV-first rankings in one paragraph each, then state which ranking your (fictional) SOC should actually use and why. The run's conclusion: KEV-first, because exploitation evidence dominates both severity and probability estimates.
5. **Trace field provenance for one CVE.** For CVE-2022-41741: where did its CVSS come from (CNA record or NVD enrichment)? Its CWE? Its product mapping? Write each field's source. This is the post-2026 skill: knowing *who said it*, not just what was said.

## 5. On your own

**Task:** Take five CVEs from your own Stage B lab work (or five from the KEV catalog if you have none). For each, record: the CWE, the CVSS-B vector and score, the EPSS score and percentile with its date, and KEV membership. Rank them three ways (CVSS-only, EPSS-only, KEV-first) and write one paragraph on how the ranking changes between methods — and which ranking a SOC should actually use, defended in two sentences.

**Success test:** Your three rankings differ in at least one position (if they do not, your sample was too tame — pick harder CVEs). Your defended ranking cites exploitation evidence or probability, not just severity. Every EPSS score carries its date.

## 6. Where it goes wrong

- **Sorting by CVSS alone.** The most common professional error in prioritization. CVSS was never designed to rank queues — it measures technical severity, and severity without likelihood or exposure is half the question.
- **Reading "Not Scheduled" as "not serious."** The post-2026 trap. An unenriched CVE is one NIST has not analyzed, full stop. Some of the worst flaws in the next year will sit in that bucket.
- **EPSS without the date.** A 30-day forecast read six months later is not data — it is a souvenir. EPSS scores decay; always record the fetch date.
- **KEV as a complete list.** KEV lists what CISA has *confirmed* exploited with remediation guidance. Absence from KEV is not evidence of absence of exploitation — it is evidence of absence of confirmation.
- **CWE as decoration.** Mapping every finding to CWE-79 because "it was kind of XSS" corrupts the taxonomy you will later query. The Top 25 is computed from these mappings; sloppy mapping makes the industry's statistics lie.
- **Treating the catalogs as competing.** They answer different questions. The failure mode is picking a favorite; the skill is combining them in the right order of authority.

## 7. Read the source

1. **CWE Top 25 (2025)** (cwe.mitre.org/top25/) — the current edition, its 39,080-record dataset, and the per-weakness pages for the CWEs in your findings. Read the methodology note so you know what the ranking actually measures.
2. **FIRST EPSS** (first.org/epss) — what the model predicts (probability of exploitation in the next 30 days), the daily publication, the free data access. Read the documentation; query the API.
3. **CISA KEV catalog** (cisa.gov/known-exploited-vulnerabilities-catalog) — the addition criteria (valid ID + exploitation evidence + remediation guidance), the due dates, the nomination process. Download the CSV.
4. **Commerce OIG report OIG-26-020-I** (oversight.gov, 2026-05-26) — the government confirmation of the NVD policy change. Read the findings on enrichment prioritization.

Free resources (≤3): the **EPSS API documentation** (api.first.org) — your programmatic access; **CAPEC** (capec.mitre.org) — the attack-pattern side of your write-ups; the **NVD dashboard** (nvd.nist.gov) — to see "Not Scheduled" with your own eyes and practice reading past it.

## 8. Check yourself

1. A CVE has CVSS 9.8, EPSS 0.001 (12th percentile), and is not in KEV. Another has CVSS 6.5, EPSS 0.42 (93rd percentile), and is not in KEV. Your patch window covers one. Which one, and what is the two-sentence defense you give your manager?
2. You open an NVD page and see no NIST CVSS score, no CWE, and a "Not Scheduled" label. List the three places you look next, in order, and what each can give you.
3. Why does KEV membership outrank a higher CVSS score in every serious prioritization scheme? What question does KEV answer that CVSS cannot?
4. A colleague sorts the queue by CVSS and calls it "risk-based prioritization." Using the three-CVE worked example, show the concrete decision this gets wrong.
5. The OIG report confirms NIST's April 2026 change but you cannot find a NIST-direct announcement page. How do you describe the policy's sourcing in a write-up without overstating it?

## 9. Prove it

**Artifact:** the five-CVE prioritization comparison with the three rankings and your defended recommendation, published on your blog or GitHub. This is the artifact a SOC hiring manager actually wants to see: not that you know the catalogs exist, but that you can combine them into a decision.

**Honest claims after this lesson:** you can prioritize any vulnerability queue using CWE, CVSS, EPSS, and KEV together; you can trace every field to its source; you know what "Not Scheduled" means and does not mean. **Cannot yet claim:** that your ranking is optimal — prioritization is judgment under uncertainty, and the honest claim is that your method is sound and auditable, not that it is right.

## 10. Leads to

- `c-cvd` and `c-cve-program` feed this lesson: the records and disclosures you produce are the inputs this lesson prioritizes.
- `c-soc-triage` and `c-sigma-detection` consume it: triage is prioritization under time pressure, and this lesson is the slow version.
- Stage E's risk assessment (`e-risk-assessment`) takes this further: prioritization across an organization, with owners and decisions.
