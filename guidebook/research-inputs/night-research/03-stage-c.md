# Stage C — Professional: night research
### Track 03 · Research date: 2026-10-09 · Researcher: subagent ff0930ea
### Governing doc: SECURITY_GUIDEBOOK_BRIEF.md (brief wins on all conflicts)

All primary sources below were fetched on 2026-10-09 unless noted. Brief rules honored: no prices, fees, salaries, or time-to-hire estimates; free resources only; original prose; gaps logged, never smoothed.

---

## Lesson C1 — Coordinated vulnerability disclosure, end to end

**Primary sources (fetched 2026-10-09):**
- CERT Guide to Coordinated Vulnerability Disclosure — https://certcc.github.io/CERT-Guide-to-CVD/ — phases adapted from ISO/IEC 30111:2019: Discovery → Reporting → Validation and Prioritization → Remediation → Public Awareness → Deployment. Roles: Finder, Reporter, Vendor, Deployer, Coordinator (one party often plays several). Principles: Reduce Harm, Presume Benevolence, Avoid Surprise, Incentivize Desired Behavior, Ethical Considerations, Process Improvement. Ideal process: reporter notifies vendor directly → vendor acknowledges → both agree a patch timeline and a same-day publication date → reporter may test the patch → advisories drafted and shared → if the vendor is a CNA it assigns the CVE ID, otherwise one is requested from the CVE Program → patch released (downstream vendors may get it first) → public disclosure.
- OpenSSF oss-vulnerability-guide, finder-guide.md — https://github.com/ossf/oss-vulnerability-guide/blob/HEAD/finder-guide.md — the finder's perspective for open source: disclosure options (No Disclosure / Coordinated / Limited / Full / 0-day — OpenSSF prefers Coordinated and Limited), how to write a complete report (reusable as advisory, disclosure note, and blog post), "Getting a CVE ID" section, troubleshooting unresponsive maintainers, plus policy/communication templates (SECURITY.md, embargo notifications, disclosure announcements).

**Free resources (≤3):** the two guides above; OWASP Vulnerability Disclosure Cheat Sheet (quick-reference checklist).

**Worked cases:**
1. *Heartbleed (CVE-2014-0160) — coordinated, imperfect.* Google's Neel Mehta privately reported to the OpenSSL team on 2014-04-01; Codenomicon independently discovered it and notified NCSC-FI on 2014-04-03; public disclosure with OpenSSL 1.0.1g on 2014-04-07. Good bones (private vendor notice, embargo, same-day patch). Criticized execution: only a tiny circle got pre-notification while ~17% of the internet's trusted web servers were vulnerable — downstream vendors scrambled. Lesson: coordination must include the deployers, not just the vendor.
2. *SandboxEscaper (2018) — the anti-pattern.* On 2018-08-27 a researcher posted a Windows Task Scheduler ALPC local-privilege-escalation zero-day on Twitter with a GitHub PoC, no prior vendor notice. CERT/CC verified it the same week; Microsoft had no patch ready; the flaw was exploited in the wild within days. More Twitter zero-days followed. Lesson: full disclosure without notice maximizes user harm and teaches nothing — it is the case study for why CVD exists.
3. *Project Zero's 90+30 policy — the framework made explicit.* Google's Project Zero gives vendors 90 days to fix (14-day grace available), then discloses; if patched early, details wait 30 more days for patch adoption. A 2025 "Reporting Transparency" trial announces the vendor/product/timeline within a week of the report without technical details. Lesson: a published, predictable deadline aligns incentives — vendors know the clock, users know disclosure is coming.

**Hand exercise:** take a historical CVE with a public timeline (e.g., Heartbleed) and reconstruct the CVD phases on a timeline: who was Finder, Reporter, Vendor, Coordinator; where the embargo held and where it leaked; what you would change. Write it as a one-page disclosure postmortem.

**Proof artifact:** the disclosure postmortem, published on the reader's blog/GitHub — demonstrates they can reason about disclosure, not just recite it.

**Prerequisites:** Stage B (finding and proving vulnerabilities); Stage B ethics rules.

---

## Lesson C2 — The CVE Program: structure, CNAs, requesting an ID, record format, credit

**Primary sources (fetched 2026-10-09):**
- https://www.cve.org/ — mission: "Identify, define, and catalog publicly disclosed cybersecurity vulnerabilities." As of 2026-09-29: 554 CNAs (551 CNAs + 3 CNA-LRs) from 43 countries; 384,000+ CVE Records accessible via download or keyword search.
- https://www.cve.org/AllResources/CveServices — CVE Services is the program's automation infrastructure: CNAs reserve IDs and publish/update records through it; records publish to the CVE List hourly. Current CVE Record Format schema: **5.2.0** (CVE Services 2.8.5). The record format "normalizes and enriches how CVE information is presented, and adds optional data fields such as: severity scores, **credit for researchers**, additional languages, affected product lists, additional references." Roots named: CISA ICS, CERT@VDE, ENISA, Google, INCIBE, JPCERT/CC, Red Hat, Thales Group; Top-Level Roots: CISA and MITRE. CVE Program request web forms live at cveform.mitre.org.
- CVE Record Format schema repository (CVEProject/cve-schema on GitHub, maintained by the CVE Quality Working Group): defines the JSON 5.x structure — `cveMetadata` (ID, assigner, state), `containers.cna` (descriptions, affected products/versions, references, metrics, **credits**), `containers.adp` (Authorized Data Publishers enrich later). Credit entries carry a `type` — observed values include `finder`, `reporter`, `remediation developer`, `coordinator`, `remediation reviewer`, `remediation verifier`, `tool`, `sponsor`, `other`. The `finder` credit is the field that puts the researcher's name in the permanent record.

**How a researcher requests an ID (step by step):**
1. Confirm the issue is a vulnerability (independently fixable, one codebase, security impact — per the CVE Program's counting rules) and that no CVE ID already exists.
2. Make a good-faith effort to contact the vendor directly (security policy / security.txt first).
3. If the vendor is a CNA, request the ID through them. If not, try the vendor's parent/root or a third-party coordinator CNA (CERT/CC, JPCERT/CC, HackerOne, and others operate as CNAs).
4. If no CNA path works, request via the CVE Program's web form at cveform.mitre.org (MITRE acts as CNA of Last Resort).
5. The ID is reserved privately first; the record is populated and published to the CVE List (hourly publication) once disclosure is coordinated.

**Free resources (≤3):** the two cve.org pages above; RedHatProductSecurity/CVE-HOWTO on GitHub (practical researcher-oriented request walkthrough).

**Hand exercise:** pick a historical CVE and read its raw JSON 5.x record (bulk downloads at cve.org/Downloads). Identify: the assigner CNA, the `credits` array and each entry's type, the affected-product block, the metrics block. Then draft a CNA-style record for a fictional local-lab finding (clearly labeled fictional) with a correct `credits` entry for yourself as `finder`.

**Proof artifact:** the annotated record walkthrough + fictional record — shows the reader understands the permanent public artifact their name will appear in.

**Prerequisites:** C1 (disclosure); Stage B (proving a vulnerability).

---

## Lesson C3 — NVD: where severity, weakness, and product data come from now

**What changed (verified 2026-10-09):** On 2026-04-15, at VulnCon26, NIST's Harold Booth announced the NVD is moving to a risk-based enrichment model because CVE volume outran analyst capacity (263% submission growth 2020–2025; ~42,000 CVEs enriched in 2025 — a record — and still not enough). Going forward NIST enriches only three categories:
1. CVEs in CISA's Known Exploited Vulnerabilities catalog (target: enriched within one business day),
2. CVEs affecting software used by the US federal government,
3. CVEs in critical software as defined by Executive Order 14028.
Everything else is published to the NVD but labeled **"Not Scheduled"** — no NIST-provided CVSS score, no CWE classification, no CPE product mapping. The unenriched backlog from before 2026-03-01 is being reclassified the same way in batches. Two further changes: NIST no longer issues its own severity score when the submitting CNA already scored the CVE, and previously enriched records are only re-analyzed if a modification materially affects the enrichment. Anyone can request enrichment of a specific CVE by emailing nvd@nist.gov. Industry estimates put the prioritized categories at roughly 15–20% of CVE volume.
*Sources: infosecurity-magazine.com (2026-10-06), inventivehq.com, tamnoon.io, recordedfuture.com, medium.com analyses — all consistent; the NVD homepage (nvd.nist.gov, fetched 2026-10-09) did not surface the policy text itself — see gap log.*

**What this means for the lesson:** severity, weakness, and product data for a CVE now come from up to three places, in this order: (1) the **CNA's own record** (CVSS, CWE, affected products as published by the assigner — this is now the default source of truth for most CVEs); (2) **NVD enrichment**, but only for prioritized CVEs; (3) **ADP containers** and community sources for the rest. The lesson must teach readers to read the CNA record first and to treat "no NVD score" as "not yet analyzed," never as "not serious."

**Free resources (≤3):** NVD homepage and search (nvd.nist.gov); the NVD dashboard's status labels; CISA KEV catalog (the fastest path to enrichment).

**Hand exercise:** take three CVEs — one in CISA KEV, one recent non-KEV, one from 2024 — and compare their NVD pages: which have NIST enrichment, which carry "Not Scheduled," and what the CNA record itself provides. Document where each field (score, weakness, products) came from.

**Proof artifact:** the three-record comparison table with sourced field provenance.

**Prerequisites:** C2 (CVE records); C4 (CVSS) may be taken in parallel.

---

## Lesson C4 — CVSS v3.1 and v4.0, scored by hand

**Primary sources (fetched 2026-10-09):**
- CVSS v4.0 Specification Document, version 1.2 — https://www.first.org/cvss/v4.0/specification-document — four metric groups: **Base** (intrinsic, constant), **Threat** (changes over time — exploit maturity), **Environmental** (unique to the consumer's environment), **Supplemental** (context only, never changes the score). Nomenclature communicates what was scored: CVSS-B (Base), CVSS-BT (+Threat), CVSS-BE (+Environmental), CVSS-BTE (all three). Base assumes worst-case Threat/Environmental defaults; consumers refine. Scores must always be published with the vector string.
- CVSS v4.0 Examples Document, version 1.8 — https://www.first.org/cvss/v4.0/examples — official worked examples with v3.x scores for comparison:
  - **CVE-2022-41741** (NGINX mp4 module): v3.1 7.0 → v4.0 Base 7.3. New v4.0 metric **Attack Requirements (AT)** captures target-specific preconditions v3.1 folded into Attack Complexity.
  - **CVE-2020-3549** (Cisco FMC sftunnel): v3.1 8.1 → v4.0 Base 7.7 → Base+Threat **5.2** with Exploit Maturity Unreported (E:U). The Threat group visibly discounts a vuln with no known exploit — v3.1's Temporal metrics existed but were rarely published; v4.0 makes the time dimension first-class.
  - **CVE-2023-3089** (OpenShift FIPS crypto): v3.1 7.5 → v4.0 Base 8.3 → Base+Environmental 8.1. v4.0's split impact metrics (vulnerable vs. subsequent system) and refined User Interaction (None/Passive/Active) move the score.
- v3.1 reference: Base/Temporal/Environmental groups; Base metrics AV/AC/PR/UI/Scope/C/I/A; vector prefix `CVSS:3.1`. (v3.1 spec not re-fetched this pass — see gap log; vectors verified against the v4.0 examples doc.)

**Hand-scoring method to teach:** (1) read the vulnerability description and identify the vulnerable system vs. any subsequent system; (2) score each Base metric from the rubric, writing one sentence of justification per metric; (3) assemble the vector string; (4) verify with the FIRST reference calculator (https://www.first.org/cvss/calculator/4.0); (5) state the nomenclature (CVSS-B vs BTE) so the reader knows what the number claims.

**Free resources (≤3):** the two FIRST documents above; the FIRST v4.0 calculator.

**Hand exercise:** score three CVEs by hand in both v3.1 and v4.0 (use the examples doc's cases as calibration, then three of the reader's own choosing from KEV). For each, write the metric-by-metric justification and explain in one paragraph where and why the versions disagree.

**Proof artifact:** the six scored vectors with justifications, calculator-verified — the reader can now defend a severity rating to a vendor.

**Prerequisites:** C2 (reading CVE records); C3 (where scores come from).

---

## Lesson C5 — CWE, CAPEC, CISA KEV, EPSS

**CWE (fetched 2026-10-09, primary):** https://cwe.mitre.org/top25/ — the **2025 CWE Top 25** is the current edition, computed from 39,080 CVE records. Top of the list: CWE-79 (XSS) #1, CWE-89 (SQL injection) #2, CWE-352 (CSRF) #3, CWE-862 (Missing Authorization) #4, CWE-787 (Out-of-bounds Write) #5. MITRE also publishes a **2025 Top 10 KEV Weaknesses** (weaknesses ranked by CISA KEV presence) and an **"On the Cusp"** list of 15 near-misses. Use: map every finding to its CWE — it is the shared vocabulary for root causes, and employers and scanners both speak it.

**CAPEC (not fetched — gap log):** MITRE's Common Attack Pattern Enumeration and Classification — the attacker's-side catalog (~hundreds of patterns) describing how weaknesses get exploited, mapped to CWEs. Use: when writing up a finding, the CAPEC entry names the attack pattern the way CWE names the weakness.

**CISA KEV (verified via consistent reporting, cisa.gov page not fetched — gap log):** the Known Exploited Vulnerabilities catalog. A CVE is added only with: a valid CVE ID, reliable evidence of active exploitation, and clear remediation/mitigation guidance. Federal agencies remediate KEV entries under Binding Operational Directive 26-04 (risk-based prioritization; compromise assessment where exposure preceded the patch). Anyone can nominate an exploited CVE for inclusion. Each entry carries a remediation due date and a known-ransomware-use field. Use: KEV membership is the strongest "fix now" signal in the industry — and since April 2026 it is also the fastest path to NVD enrichment.

**EPSS (fetched 2026-10-09, primary):** https://www.first.org/epss — the Exploit Prediction Scoring System, maintained by FIRST's EPSS Special Interest Group. A data-driven ML model estimating the **probability (0–1) that a CVE will be exploited in the wild in the next 30 days**, published daily with ranking percentiles for every CVE, freely available via CSV, API, and GitHub. Use: EPSS answers "how likely is this to be exploited soon" where CVSS answers "how bad if exploited" — practitioners combine EPSS + KEV + CVSS instead of sorting by CVSS alone.

**Free resources (≤3):** cwe.mitre.org (Top 25 + per-weakness pages); first.org/epss (score lookup + data); CISA KEV catalog.

**Hand exercise:** take five CVEs from the reader's Stage B lab work; for each record the CWE, the CVSS-B vector, the EPSS score and percentile, and KEV membership. Rank them three ways (CVSS-only, EPSS-only, KEV-first) and write one paragraph on how the ranking changes and which ranking a SOC should actually use.

**Proof artifact:** the prioritization comparison with a defended recommendation.

**Prerequisites:** C4 (CVSS); Stage B (vulnerability classes).

---

## Lesson C6 — Building a public track record: write-ups that teach

**What makes a write-up teach** (studied 2026-10-09): root cause before exploit; the mechanism explained from first principles; what the vulnerable code/system was doing wrong; how the finder confirmed it; impact stated honestly (what was proven vs. assumed); the fix and how to verify it; enough detail that a reader can reproduce the *class*, not just replay the *instance*.

**Exemplars studied:**
1. *James Kettle, "HTTP/2: The Sequel is Always Worse" (PortSwigger Research, presented Black Hat USA 2021)* — https://portswigger.net — mechanism-first: HTTP/2 framing vs. HTTP/1.1 downgrading, implementation flaws and RFC imperfections, case studies against real stacks (ALB, WAFs, CDNs), critical impact demonstrated responsibly, then open-source tooling and free interactive labs so readers can learn. The template for a research-grade write-up: novel mechanism → real-world validation → community tooling.
2. *Google Project Zero blog* — https://googleprojectzero.blogspot.com/ (fetched 2026-10-09; active, current posts include 2026 Android/Windows research) — the root-cause discipline exemplar: posts walk from crash to root cause to exploit primitive, document dead ends, and close with systemic recommendations (e.g., the Android 0-click attack-surface series, the Windows Administrator Protection bypass series). Study any two posts: note how each states the root cause in one paragraph before any exploitation detail.
3. *HackerOne Hacktivity disclosed reports* — the bounty-report exemplar: real reports show the professional minimum — clear reproduction steps, impact statement, severity justification. Read five disclosed reports in the reader's Stage B vuln classes; note which ones teach and which merely assert.

**Free resources (≤3):** the two above; HackerOne Hacktivity (disclosed reports).

**Hand exercise:** write up one of the reader's own Stage B lab findings to the Project Zero bar: root cause paragraph first, mechanism, confirmation, honest impact, fix, verification. Then rewrite the same finding as a one-page bounty report. Compare what each format demands.

**Proof artifact:** the published write-up — the first entry in the reader's public track record.

**Prerequisites:** Stage B (a real finding to write about); C1 (disclosure context).

---

## Lesson C7 — What professionals know about AI tooling for security work (the CVP example)

**The example, dated:** On **2026-10-06** Anthropic rebuilt its Cyber Verification Program (CVP) into three tiers (merging the earlier CVP with Project Glasswing). Reporting is consistent across 6+ outlets dated 2026-10-06 through 2026-10-08; Anthropic's own page was not fetched in this pass — re-verify at anthropic.com before publishing (gap log).

- **Defense Access:** SOC and incident response work, malware reverse engineering, analyzing and validating vulnerabilities. Open to security teams, critical-infrastructure operators, smaller firms, open-source maintainers, and **individual researchers with a track record of reported vulnerabilities**. Reviewed within days.
- **Red Team Access:** adds authorized penetration testing and red teaming. **Organizations only.** Reviewed over weeks; applicants hold Defense Access meanwhile. Real-time blocks remain on actions risking physical harm or mass disruption.
- **Specialized Access:** fewest cyber blocks, for testing safety-critical systems (flight systems, power grids, telecom, interbank transfer). Limited verified organizations, reviewed in depth **with the US government**; Glasswing members moved here.

**What the lesson teaches (brief §3 correction, owner-checked):** CVP is **access to tooling, never a credential, a milestone, or a CV line.** Its two uses in the guidebook: (1) it shows how the field sorts professional security work — defensive validation vs. authorized offense vs. safety-critical testing; (2) it shows a **public record of reported vulnerabilities being treated as professional evidence** — Anthropic's own example of a qualifying individual is a researcher "with a track record of reported vulnerabilities," which is exactly what Stages B–C build. Standard models still handle routine tasks (code review, patching known issues, triage) without any program.

**Free resources (≤3):** Anthropic's CVP page (primary — fetch at build time); the October 2026 announcement coverage; Project Glasswing reporting (129,000+ verified vulns found by partners Apr–Jul 2026, per Anthropic via outlets).

**Hand exercise:** map the reader's own Stage B–C evidence (bounty profile, disclosures, CVE credits) against the Defense Access description: which items count as a "track record of reported vulnerabilities," what is missing, what comes next. One page, honest.

**Proof artifact:** the self-assessment — the reader sees their public record the way a verifier would.

**Prerequisites:** C1–C6 (the track record itself).

---

## Gap log

1. **cve.org deeper docs:** homepage and CVE Services pages rendered; the CNA directory and program-structure pages did not render in this pass (JS-heavy). CNA count (554) and record-format version (5.2.0) verified from rendered pages. Re-check program-structure docs at build time.
2. **NVD enrichment policy:** change verified via 5+ consistent secondary outlets (2026-04-15, VulnCon26, Booth); nvd.nist.gov homepage fetched but did not surface the policy announcement. Check the NVD dashboard/news pages directly before publishing.
3. **CVSS v3.1 spec:** v4.0 spec and official examples doc fetched from first.org; v3.1 described from the examples doc's vectors and standard knowledge — re-fetch the v3.1 spec at build time for the hand-scoring lesson.
4. **CISA KEV catalog page:** criteria (CVE ID + exploitation evidence + mitigation guidance), BOD 26-04, and nomination process consistently reported; cisa.gov catalog page not fetched this pass — fetch at build time.
5. **CAPEC:** not fetched this pass; described at catalog level only — fetch capec.mitre.org at build time.
6. **CVEProject/cve-schema on GitHub:** fetch timed out (not a denial — local worker error); credit-field types (`finder`, `reporter`, `remediation developer`, etc.) confirmed via cve.org ("credit for researchers") and a CVE tooling schema doc — verify against the schema repo at build time.
7. **Anthropic CVP page:** tier details consistent across 6+ outlets dated 2026-10-06–08; anthropic.com not fetched — fetch the primary page at build time and date every statement (program is days old).
8. **HackerOne Hacktivity:** cited as the bounty-report exemplar from knowledge of the platform; no specific report fetched — the lesson's Phase 2 build should fetch 2–3 specific disclosed reports as primary rows.

## Source ledger (fetched 2026-10-09)

| Claim / resource | Primary URL | Status |
|---|---|---|
| CVE Program mission, 554 CNAs, 384k+ records | https://www.cve.org/ | verified |
| CVE Services, Record Format 5.2.0, researcher credit field, Roots | https://www.cve.org/AllResources/CveServices | verified |
| CVSS v4.0 spec (4 groups, nomenclature) | https://www.first.org/cvss/v4.0/specification-document | verified |
| CVSS v4.0 official examples (v3.1↔v4.0 cases) | https://www.first.org/cvss/v4.0/examples | verified |
| EPSS (0–1 probability, 30 days, daily, free data) | https://www.first.org/epss | verified |
| CWE Top 25 2025 (39,080-record dataset) | https://cwe.mitre.org/top25/ | verified |
| CVD phases (ISO/IEC 30111:2019), roles, principles | https://certcc.github.io/CERT-Guide-to-CVD/ | verified |
| OSS finder guide (disclosure options, CVE ID section) | https://github.com/ossf/oss-vulnerability-guide/blob/HEAD/finder-guide.md | verified |
| Project Zero blog (active, current research) | https://googleprojectzero.blogspot.com/ | verified |
| PortSwigger HTTP/2 research (exemplar) | https://portswigger.net (research section) | reported |
| NVD enrichment change (2026-04-15) | nvd.nist.gov (no policy text found) + 5 outlets | reported |
| Heartbleed timeline | en.wikipedia.org + secondary | reported |
| SandboxEscaper case | techtarget.com, threatpost.com, thehackernews.com | reported |
| Project Zero 90+30 policy | infosecurity-magazine.com, hothardware.com | reported |
| CVP three tiers (2026-10-06) | 6 outlets 2026-10-06–08 | reported |
| KEV criteria, BOD 26-04 | therealistjuggernaut.com, huntaegis.com | reported |
