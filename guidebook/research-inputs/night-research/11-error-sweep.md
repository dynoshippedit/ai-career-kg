# 11 — Error Sweep / Gap-Closure Ledger

**Date:** 2026-10-09 · **Sweep agent:** subagent b9b3ac72 (session 41b51a2e-ee12-4fdd-83f7-b667b4bac63a)
**Governing brief:** `~/workspace/security-curriculum/site-run/SECURITY_GUIDEBOOK_BRIEF-2.md`
**Method:** every RESOLVED item below was fetched by this sweep from a primary source in this session, unless explicitly marked "carried." Dino's rule held: a gap is a valid result — what is missing and what was tried is logged, nothing smoothed over.

---

## PRIORITY GAPS (task-ordered)

### GAP-01 · NVD post-2026-04-15 enrichment policy — primary NIST/NVD statement
**TRIED:** nvd.nist.gov news archives, NIST newsroom, csrc.nist.gov, Google/Bing for "NIST NVD April 15 2026 enrich prioritized CVEs announcement", DoC OIG reports on oversight.gov.
**RESOLVED (government-confirmed, NOT NIST-direct):** DoC OIG report **OIG-26-020-I** (issued **2026-05-26**, oversight.gov): NIST announced 2026-04-15 that it will **only enrich vulnerabilities meeting new prioritization criteria** and will **no longer assign a score for each vulnerability**; remaining CVEs go to "**Not Scheduled**"; enrichment requests via nvd@nist.gov; criteria corroborated across 10+ outlets quoting NIST: CISA KEV (1-business-day target), federal software, EO 14028 critical software; pre-2026-03-01 unenriched CVEs reclassified to Not Scheduled. **Caveat:** NIST's own press-release text was not located anywhere public — record this as *government-confirmed via OIG, reported-not-verified at NIST-direct level*. The guidebook should state the policy as announced, with the OIG report cited, and note the primary release has not surfaced.
**Date fetched:** 2026-10-09.

### GAP-02 · CVE Record reporter-credit field — format documentation
**TRIED:** cve.org → CVE Record format docs → CVEProject/cve-schema on GitHub (the official schema repo, linked from cve.org itself).
**RESOLVED:** Per **cve.org/AllResources/CveServices** (primary): "credit for researchers" is an **optional** CVE Record field. Per the official CVE Record format schema **5.2.0** (cvedb.github.io mirror of CVEProject/cve-schema): the field is a `credits[]` array; each entry = acknowledgment of a person, org, or tool for research/discovery/remediation work. Fields: `lang` (BCP 47); optional `user` UUID (CVE User Registry); `type` enum default **`"finder"`** with values: finder (identifies the vuln), reporter (notifies vendor/CNA), analyst (validates), coordinator (facilitates coordinated response), remediation developer, remediation reviewer, remediation verifier, tool, sponsor, other.
**Dates fetched:** 2026-10-09. Guidebook note: credit on a CVE is the `credits` array — the "report in your name" milestone is this field.

### GAP-03 · OWASP LLM Top 10 2026 — full renumbered LLM01–LLM10
**TRIED:** genai.owasp.org (403 from this environment), fell back to the official OWASP source repo **github.com/GenAI-Security-Project/GenAI-LLM-Top10**, `2026/final/` directory.
**RESOLVED (primary, official repo):** **OWASP Top 10 for LLM Applications 2026 — edition released 2026-09-30.** LLM01 Prompt Injection · LLM02 Sensitive Information Disclosure · LLM03 Excessive Agency · LLM04 Supply Chain · LLM05 Data and Model Poisoning · LLM06 Unbounded Consumption · LLM07 Misinformation · LLM08 Hidden Context Exposure · LLM09 Vector and Embedding Weaknesses · LLM10 Improper Output Handling. **Caveat:** two secondary sources order LLM04–LLM10 differently; the repo is authoritative. Guidebook must **always name the edition** (2026) because codes were renumbered from 2025.
**Date fetched:** 2026-10-09.

### GAP-04 · NIST SP 800-61 Rev. 3 — structure from csrc
**TRIED:** csrc.nist.gov/pubs/sp/800/61/r3/final.
**RESOLVED (primary):** Date Published **April 2025**; supersedes **SP 800-61 Rev. 2 (08/06/2012)**; title **"Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile"**; authors Alexander Nelson, Sanjay Rekhi, Murugiah Souppaya (NIST), Karen Scarfone (Scarfone Cybersecurity). Structure: it is a **CSF 2.0 Community Profile** — IR guidance mapped onto the NIST Cybersecurity Framework 2.0 — not a standalone incident-handling phase doc like Rev. 2. Guidebook: name Rev. 3 (April 2025) and its CSF 2.0 profile structure; Rev. 2 is withdrawn (2025-04-03).
**Date fetched:** 2026-10-09.

### GAP-05 · NICE Framework — no version newer than v2.0.0 at NIST
**TRIED:** niccs.cisa.gov NICE Framework page (authoritative, NIST program page).
**RESOLVED (primary):** **NICE Framework Components v2.0.0, released March 2025** — no newer version on the official page (page "Last Published Date: May 29, 2025"). Five Work Role Categories: **Oversight and Governance (OG)** (14 work roles listed), **Design and Development (DD)** (8), **Implementation and Operation (IO)** (7), **Protection and Defense (PD)** (7), **Investigation (IN)** (2). Confirmed on-page: **Cyberspace Effects and Cyberspace Intelligence removed** → moved to the **DoD Cyber Workforce Framework (DCWF)**.
**Date fetched:** 2026-10-09.

---

## FILE-BY-FILE GAPS

### From 02-stage-b (Stage B: tools & web hacking)
- **DVGA port — RESOLVED (primary):** github.com/dolevf/Damn-Vulnerable-GraphQL-Application README: `docker run -d -t -p 5013:5013 …`, browser to `http://localhost:5013`. Port is **:5013**; :5000 references are stale/mirror artifacts. Fetched 2026-10-09.
- **Juice Shop canonical repo — RESOLVED (primary):** github.com/juice-shop/juice-shop; README: `docker pull bkimminich/juice-shop`; `docker run --rm -p 127.0.0.1:3000:3000 bkimminich/juice-shop`; browse `http://localhost:3000`. Official project site owasp-juice.shop. Fetched 2026-10-09.
- **WebGoat canonical repo — RESOLVED (primary):** github.com/WebGoat/WebGoat; README: `docker run -it -p 127.0.0.1:8080:8080 -p 127.0.0.1:9090:9090 webgoat/webgoat`. Ports **8080/9090**. Fetched 2026-10-09.
- **SigmaHQ repo — RESOLVED (primary):** github.com/SigmaHQ/sigma — "Main Sigma Rule Repository", 3000+ detection rules, official site sigmahq.io. Fetched 2026-10-09.
- **SP 800-92 — RESOLVED (primary):** csrc.nist.gov/pubs/sp/800/92/final — "Guide to Computer Security Log Management", **Date Published: September 2006**, authors Karen Kent, Murugiah Souppaya. Fetched 2026-10-09.
- **OWASP API Security Top 10 edition currency — RESOLVED (primary):** owasp.org/API-Security/editions/2023/en/0x11-t10 — **"OWASP Top 10 API Security Risks – 2023"**: API1:2023 Broken Object Level Authorization · API2:2023 Broken Authentication · API3:2023 Broken Object Property Level Authorization · API4:2023 Unrestricted Resource Consumption · API5:2023 Broken Function Level Authorization · API6:2023 Unrestricted Access to Sensitive Business Flows · API7:2023 SSRF · API8:2023 Security Misconfiguration · API9:2023 Improper Inventory Management · API10:2023 Unsafe Consumption of APIs. Project page owasp.org/API-Security confirmed. Fetched 2026-10-09.
- **PortSwigger lab slugs — RESOLVED (primary, pattern):** `portswigger.net/web-security/sql-injection` (SQLi tutorial + "View all SQL injection labs") and `portswigger.net/web-security/access-control/idor` both live; pattern `/web-security/<topic>/<subtopic>` confirmed. Guidebook should verify each slug individually at build time. Fetched 2026-10-09.
- **RFC 7519 / 6749 — resolved, carried:** fetched in 01-stage-a by the Stage A agent (mark as primary-verified, no re-fetch).
- **PTES Technical Guidelines — STILL OPEN:** pentest-standard.org returns **403** on two attempts (this session and the 02 agent's). The 7 PTES phases are corroborated from secondary sources; the primary document page is unreachable from this environment. Carry forward; retry from a live browser at build time.
- **PortSwigger topic count ("18+") — STILL OPEN:** count not primary-verified. Record as unverified; confirm at build time.

### From 03-stage-c (Stage C: disclosure, CVE, scoring)
- **cve.org CNA directory — RESOLVED (primary):** cve.org/ProgramOrganization/CNAs — "**Currently, there are 555 CNAs (552 CNAs and 3 CNA-LRs)** from **43 countries** and 1 no country affiliation." CNAs = vendor, researcher, open source, CERT, hosted service, bug bounty provider, and consortium orgs; "there are minimal requirements, and **there is no monetary fee or contract to sign**" (supports free-only framing). Fetched 2026-10-09.
- **CVSS v3.1 spec — RESOLVED (primary):** first.org/cvss/v3.1/specification-document — CVSS is owned/managed by FIRST; **three metric groups: Base, Temporal, Environmental** (v4.0 renamed Temporal→Threat; v3.1 retains Temporal — guidebook must name versions). Fetched 2026-10-09.
- **CISA KEV page — RESOLVED (primary):** cisa.gov/known-exploited-vulnerabilities-catalog — "authoritative source of vulnerabilities that have been exploited in the wild"; KEV nomination process; CSV/JSON formats (JSON Schema updated 09-02-2026); references **BOD 26-04** ("Prioritizing Security Updates Based on Risk"). Fetched 2026-10-09.
- **CAPEC — RESOLVED (primary):** capec.mitre.org — CAPEC is "a comprehensive dictionary of known patterns of attack employed by adversaries." Fetched 2026-10-09.
- **Anthropic CVP — resolved, carried:** confirmed at anthropic.com by the 00 agent (announced 2026-10-06; three tiers: Defense Access individuals-with-track-record, Red Team Access org-only, Specialized Access org-only). No re-fetch.

### From 04-stage-d (Stage D: specialist tracks)
- **ATT&CK current version — RESOLVED (primary):** attack.mitre.org/resources/versions — **ATT&CK v19.2, April 28, 2026 – current.** Homepage fetch confirms the tactic list now has **15 tactics**: Reconnaissance, Resource Development, Initial Access, Execution, Persistence, Privilege Escalation, **Stealth, Defense Impairment** (Defense Evasion split/renamed), Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact. **FLAG for assembler:** guidebook must cite v19.2 and check tactic names — any lesson text using "Defense Evasion" is now stale. Fetched 2026-10-09.
- **NIST AI RMF revision status — RESOLVED (primary):** nist.gov/itl/ai-risk-management-framework — **AI RMF 1.0 (released Jan 26, 2023) is current**; "being revised as part of the White House AI Action Plan." GenAI Profile **NIST-AI-600-1** released July 26, 2024; concept note April 7, 2026 for an AI RMF Profile on Trustworthy AI in Critical Infrastructure. No AI RMF 2.0 as of 2026-10-09. Fetched 2026-10-09.
- **SAMM — RESOLVED (identity, primary):** owaspsamm.org — SAMM = **Software Assurance Maturity Model**, "an effective and measurable way for any organization to analyze and improve their security posture"; **free SAMM Fundamentals course** (fits free-only framing). Version number not captured from homepage — record "version not primary-verified." Fetched 2026-10-09.
- **Ghidra — RESOLVED (primary):** github.com/NationalSecurityAgency/ghidra — "Ghidra is a software reverse engineering (SRE) framework created and maintained by the NSA Research Directorate"; free, Apache 2.0. Fetched 2026-10-09.
- **MITRE ATLAS — RESOLVED (org/data level, primary):** github.com/mitre-atlas — repos atlas-website, **atlas-data** ("ATLAS tactics, techniques, and case studies data", updated Sep 15, 2026), atlas-knowledge-base-agent, atlas-navigator-data. Caveat: atlas.mitre.org itself is cookie-walled in this environment (content not fetched). Fetched 2026-10-09.

### From 05-stage-e / 05b-governance-leadership
- **SP 800-55 — RESOLVED (primary):** csrc.nist.gov/pubs/sp/800/55/r1/final — **Rev. 1 (July 2008) withdrawn December 4, 2024**; superseded by **SP 800-55 Vol. 1 and SP 800-55 Vol. 2**. Guidebook must cite the two volumes, not Rev. 1. (First attempt at /r2/final returned 404 — there is no Rev. 2; corrected input r1 succeeded.) Fetched 2026-10-09.
- **SOC 2 / Trust Services Criteria edition — PARTIALLY RESOLVED (secondary-corroborated, primary stale):** current form per two independent sources citing AICPA is "**2017 Trust Services Criteria for Security, Availability, Processing Integrity, Confidentiality, and Privacy (with Revised Points of Focus – 2022)**", TSP Section 100 — the 2022 revision changed points of focus, not criteria. aicpa-cima.com SOC suite page confirms AICPA promulgates the professional standards; the direct AICPA PDF URL (2017-trust-services-criteria-with-revised-points-of-focus-2022.pdf) returns **404** (site restructured to aicpa-cima.com). **STILL OPEN at primary level:** current TSC edition not confirmed on an AICPA-hosted page. Guidebook should name the 2017-with-2022-POF edition and re-verify at build time.
- **ISO 27001 certification lifecycle — STILL OPEN:** not attempted beyond confirming it is a paid-standard domain; iso.org pages are paywalled/script-heavy. Carry forward — the guidebook covers ISO 27001 through *free* resources only per the free-only rule, and the lifecycle detail may not need a primary ISO source (secondary auditor guidance is adequate, flagged as such).

### From 06-ai-track
- **EU AI Act dates — CORROBORATED (5+ secondary sources citing EUR-Lex, not primary-fetched):** Regulation (EU) 2024/1689: in force 1 Aug 2024; prohibited practices 2 Feb 2025; GPAI model obligations 2 Aug 2025; transparency Art. 50 2 Aug 2026; **Digital Omnibus on AI, Regulation (EU) 2026/1744** — OJ published 24 Jul 2026, in force 27 Jul 2026; moved Annex III high-risk to **2 Dec 2027** and Annex I product-embedded high-risk to **2 Aug 2028**; **2 Dec 2026** — marking grace period ends + new bans on AI-generated non-consensual intimate imagery / CSAM; GPAI and transparency dates untouched. All five sources consistent. **Not primary-verified** (EUR-Lex text of 2026/1744 not fetched this session) — guidebook should cite Regulation (EU) 2026/1744 and EUR-Lex; treat dates as corroborated, not primary.
- **OWASP Agentic AI Top 10 — STILL OPEN:** genai.owasp.org page returned **403** (access denied in this environment); per runtime rules it was not retried. It is an OWASP extension initiative, not the brief's named reference (brief names LLM Top 10 2026 — resolved). Note in the guidebook as an adjacent project; verify from a live browser at build time if referenced.
- **SANS pages (SEC598→GASAE, SEC535→GOAA) — STILL OPEN:** script-rendered, unreachable in this environment. Carry forward; verify from live browser at build time. The brief already asserts the course codes, so the guidebook may cite the brief with a verification flag.

### From 07-role-paths
- **NICE components — RESOLVED:** see GAP-05; the NICCS page itself enumerates all work roles per category, superseding the raw components JSON need.
- **AI Security Engineer page + credential URL pattern — STILL OPEN:** repo-dependent; the learncomputerstuff.dev repo is not on this VM (Threadripper off). These close only after repo placement is resolved.

### Carried from earlier sessions (not re-fetched)
- OWASP LLM Top 10 **2025** edition list — resolved in the pre-sweep session from the official repo (records in session notes; the 2026 edition is the current one — prefer it).
- RFC 7519 (JWT) / RFC 6749 (OAuth 2.0) — fetched by 01-stage-a from primary RFC sources.
- Anthropic CVP — fetched by 00 agent at anthropic.com (announced 2026-10-06; three tiers).

---

## STILL-OPEN REGISTER (8 items)
1. **NIST-direct NVD release text** — exhaustive search done; government-confirmed via DoC OIG OIG-26-020-I. Carry as reported-not-verified at NIST-direct level.
2. **PTES Technical Guidelines** — 403 twice; retry from live browser at build time.
3. **OWASP Agentic AI Top 10** — 403 at genai.owasp.org; extension project, non-blocking.
4. **SANS course pages** (SEC598→GASAE, SEC535→GOAA) — script-rendered; verify from live browser at build time.
5. **ISO 27001 certification lifecycle** — paywalled domain; use secondary guidance, flagged.
6. **TSC edition at AICPA primary level** — secondary-corroborated (2017 with 2022 revised points of focus); AICPA PDF URL stale; re-verify at build time.
7. **PortSwigger topic count "18+"** — unverified; confirm at build time.
8. **AI Security Engineer page + credential URL pattern** — repo-dependent; blocked until repo placement.

## CRITICAL FLAGS FOR THE ASSEMBLER (breaks in round-1/2 research)
- **ATT&CK v19.2** (2026-04-28) restructured tactics: **Defense Evasion → Stealth + Defense Impairment**; 15 tactics. Any lesson text listing 14 tactics with Defense Evasion is stale.
- **SP 800-55 Rev. 1 withdrawn 2024-12-04**; current = **Vol. 1 and Vol. 2**.
- **OWASP LLM Top 10: always name the edition (2026)**; codes renumbered from 2025.
- **SP 800-61 = Rev. 3 (April 2025), a CSF 2.0 Community Profile**; Rev. 2 withdrawn 2025-04-03.
- **DVGA port is :5013**, not :5000.
- **CVE CNA count = 555 (552 + 3 CNA-LRs)** as of 2026-10-09 — date the figure; it moves.

---

## 5-LINE HANDOFF
1. **Gaps closed this session: 23** (all primary-sourced: LLM Top 10 2026, NVD policy via DoC OIG, CVE credit field schema 5.2.0, SP 800-61 Rev. 3, NICE v2.0.0, CNA directory 555, ATT&CK v19.2, AI RMF 1.0 status, SP 800-92, SP 800-55 volumes, SigmaHQ, Juice Shop, WebGoat, DVGA :5013, CVSS v3.1, CISA KEV, CAPEC, API Top 10 2023, PortSwigger slugs, Ghidra, ATLAS org, SAMM identity).
2. **Still open: 8** (NIST-direct NVD text, PTES 403, Agentic Top 10 403, SANS pages script-rendered, ISO cert lifecycle paywalled, TSC edition primary, PortSwigger "18+" count, AI Security Engineer page — repo-blocked).
3. **Important still-opens:** the NIST-direct NVD statement (OIG confirmation stands, but the guidebook cites a report, not NIST); ATT&CK v19.2's tactic restructure invalidates any round-1/2 text using Defense Evasion — flag for the assembler now.
4. **Corroborated-not-primary (usable with citation caveats):** EU AI Act post-Omnibus dates (5 sources, cites Regulation (EU) 2026/1744 — EUR-Lex verification needed at build); TSC 2017-with-2022-POF edition (AICPA PDF URL stale).
5. **Next:** write 11-error-sweep.md → DONE (this file). Agents 08/09/10 outputs still pending; repo placement still blocked awaiting Dino's call.
