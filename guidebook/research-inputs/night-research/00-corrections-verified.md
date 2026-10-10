# Brief §3 — Corrections Verification
All rows checked against primary sources on **2026-10-09**. Verdicts: confirmed / corrected / could-not-verify.

## 1. NICE Framework — CONFIRMED (with version resolved)
- **Fact:** NICE Framework Components **v2.0.0**, released March 2025. Five Work Role Categories: **Oversight and Governance (OG)**, **Design and Development (DD)**, **Implementation and Operation (IO)**, **Protection and Defense (PD)**, **Investigation (IN)**. Two categories removed in v2.0.0: **Cyberspace Effects** and **Cyberspace Intelligence** — moved to the DoD Cyber Workforce Framework (DCWF).
- **Version resolution:** the official NICCS page lists v2.0.0 (page last published May 29, 2025). Third-party pages claiming 2.1.0/2.2.0 were found, but no NIST primary page confirms any version newer than 2.0.0. Take version, names, and IDs from the components data as the brief instructs.
- **Primary URL:** https://niccs.cisa.gov/workforce-development/nice-framework
- **Note:** older NIST pages (e.g., the K12 FAQ) still describe seven categories — they are stale relative to v2.0.0.

## 2. CVE Program — CONFIRMED, count UPDATED
- **Fact:** cve.org's CNA page currently reports **555 CNAs (552 CNAs + 3 CNA-LRs)** from 43 countries + 1 no-country-affiliation. The brief's "502 (reported 2026-03-31)" is stale — the CVE Program's own Q1 2026 report confirms 502 as of March 31, 2026, and 25 more were added in Q2 2026.
- **Structure (from cve.org):** federated model — vendor, researcher, open source, CERT, hosted service, bug bounty provider, and consortium organizations authorized to assign CVE IDs and publish CVE Records within their own scopes; CNA-LRs as last resort; no fee or contract to join.
- **Primary URL:** https://www.cve.org/ProgramOrganization/CNAs
- **Gap:** the CVE Record **credit field** was not reached at cve.org in this pass. cve.org rendered fine (no special browser needed). The credits array lives in the CVE JSON 5.x record schema — verify at cve.org's record documentation before the lesson ships.

## 3. NVD enrichment policy — COULD NOT VERIFY AT PRIMARY
- **Reported fact (consistent across 7+ independent outlets quoting NIST directly):** announced April 15, 2026 by NIST's Harold Booth at VulnCon26. NVD now enriches only: (a) CVEs in CISA's KEV catalog (target: within one business day), (b) CVEs in software used by the US federal government, (c) CVEs in critical software per EO 14028. Everything else is added but marked **"Not Scheduled"** for enrichment. Unenriched CVEs published before March 1, 2026 were dropped to "Not Scheduled". NIST no longer issues its own severity score when the CNA already scored the CVE. Users can request enrichment of specific CVEs via nvd@nist.gov.
- **What I tried:** fetched nvd.nist.gov homepage directly — it carries no announcement text (the announcement was delivered at the conference, not posted as an NVD news item I could find). Searched for an NVD-published statement — none located.
- **Status for the lesson:** treat as reported-by-multiple-outlets, not primary-verified. The lesson must teach where severity/weakness/product data comes from now: the CNA's own record first, NVD only for prioritized CVEs.

## 4. CVSS v4.0 — CONFIRMED
- **Fact:** CVSS v4.0 is the latest version (spec document version 1.2). Four metric groups: **Base, Threat, Environmental, Supplemental**. The Threat group replaced v3.x's Temporal group. Nomenclature CVSS-B / -BT / -BE / -BTE reflects which groups are included.
- **Primary URL:** https://www.first.org/cvss/v4.0/specification-document

## 5. CISSP exam outline — CONFIRMED; AI notes are COMMENTARY
- **Fact:** isc2.org lists the eight domains (Security and Risk Management; Asset Security; Security Architecture and Engineering; Communication and Network Security; Identity and Access Management (IAM); Security Assessment and Testing; Security Operations; Software Development Security). Current exam outline effective **April 15, 2024** — no newer outline announced.
- **AI notes:** ISC2 publishes a separate document, **"Exam Guidance for Artificial Intelligence"** (April 2, 2026), mapping where AI security concepts appear across 50+ exam domains in its portfolio. It is a guidance/mapping document, **not** numbered exam objectives — the 1.1–8.5 outline contains no AI objectives. Per ISC2, AI concepts are woven into existing domains through the standard refresh cycle (no ninth domain). Use the guidance to link domains to the AI track; do not present AI items as exam objectives.
- **Experience rule (confirmed at isc2.org):** five years cumulative paid experience in two or more domains; a degree or approved credential substitutes one year; passing without it makes you an Associate of ISC2 (six years to earn the experience).
- **Primary URLs:** https://isc2.org/cissp ; https://www.isc2.org/certifications/cissp/cissp-experience-requirements

## 6. CAISP — CONFIRMED; distinct from CertNexus CAIP — CONFIRMED
- **Fact:** Practical DevSecOps's CAISP has seven chapters, matching the brief: 1 Introduction to AI Security; 2 Understanding and Attacking Large Language Models; 3 LLM Top 10 Vulnerabilities; 4 AI Attacks and Defenses Using DevOps; 5 Threat Modeling AI Systems; 6 Supply Chain Attacks in AI; 7 Emerging Threats, Governance, and Compliance in AI.
- **Distinctness:** CertNexus's **CAIP** (certnexus.com, primary) is the **Certified Artificial Intelligence Practitioner**, exam AIP-210 — a vendor-neutral ML practitioner certification for data professionals (select/train/implement ML solutions). Different issuer, different audience, different subject. Never merge the two.
- **Primary URLs:** https://www.practical-devsecops.com/ (issuer; chapter list confirmed on its CAISP comparison pages) ; https://certnexus.com/certified-artificial-intelligence-practitioner-caip/

## 7. OWASP LLM Top 10 — CORRECTED: current edition is 2026, not 2025
- **Fact:** genai.owasp.org states **"OWASP Top 10 for LLM Applications 2026 is the latest"** community-driven guide. The 2026 edition reuses the LLM01–LLM10 code space with **renumbered meanings** (e.g., LLM03 = Excessive Agency, LLM04 = Supply Chain, LLM06 = Unbounded Consumption, LLM08 = Hidden Context Exposure, LLM10 = Improper Output Handling). The 2025 list (LLM01 Prompt Injection … LLM10 Unbounded Consumption) is the **prior** edition.
- **Implication for the lesson:** name the edition and date on every citation; a bare "LLM03" is ambiguous across editions. Teach from the 2026 edition.
- **Primary URL:** https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/

## 8. AAISM — CONFIRMED at isaca.org; AAIA/AAIR exist — CONFIRMED
- **Fact:** ISACA's press release: "Security professionals who hold a **Certified Information Security Manager (CISM)** or **Certified Information Systems Security Professional (CISSP)** are eligible to pursue the AAISM." Exam content outline (isaca.org): 90 questions across three job-practice domains (AI governance and program management; AI risk management; AI technologies and controls).
- **Siblings confirmed on isaca.org's certification listing:** **AAIA** (Advanced in AI Audit) and **AAIR** (Advanced in AI Risk). Do not imply AAISM is ISACA's only AI credential.
- **Primary URLs:** https://www.isaca.org/about-us/newsroom/press-releases/2025/isaca-introduces-first-and-only-ai-centric-security-management-certification ; https://www.isaca.org/credentialing/aaism/aaism-exam-content-outline

## 9. SANS pairings — CONFIRMED at sans.org
- **Fact:** **SEC598: AI and Security Automation for Red, Blue, and Purple Teams → GIAC AI Security Automation Engineer (GASAE)** — exam: 3 hours, 82 questions, 70% pass. **SEC535: Offensive AI – Attack Tools and Techniques → GIAC Offensive AI Analyst (GOAA)** — confirmed on sans.org's AI training index.
- **Primary URLs:** https://www.sans.org/cyber-security-certifications/ai-security-automation-engineer-gasae ; https://www.sans.org/go/ai-training

## 10. NIST SP 800-61 — CONFIRMED at csrc.nist.gov
- **Fact:** **Revision 3 is final**: "Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile." Rev. 2 withdrawn April 3, 2025. Structure is CSF 2.0-aligned (Govern, Identify, Protect, Detect, Respond, Recover); incident response itself sits at the top level as Detect → Respond → Recover, with continuous improvement as the middle layer. Scope differs significantly from Rev. 2 — it no longer attempts step-by-step playbooks for every technology.
- **Primary URLs:** https://csrc.nist.gov/Projects/incident-response ; https://CSRC.NIST.gov/News/2025/nist-revises-sp-800-61

## 11. Kurose & Ross — CONFIRMED at authors' site
- **Fact:** the textbook *Computer Networking: A Top-Down Approach* is a commercial book (Pearson; 9th edition current). The authors publish **Wireshark labs free** (HTTP, DNS, TCP, UDP, IP, NAT, DHCP, ICMP, Ethernet/ARP, WiFi, 5G, TLS — Word and PDF) at gaia.cs.umass.edu; slides historically free; lab **solutions are instructors-only from the publisher**, not the authors.
- **Primary URL:** https://gaia.cs.umass.edu/kurose_ross/wireshark.php

## 12. Anthropic Cyber Verification Program — CONFIRMED at anthropic.com
- **Fact:** newsroom post dated **October 6, 2026**: CVP expanded to three tiers, merging Project Glasswing.
  - **Defense Access:** SOC/IR work, malware reverse engineering, analyzing and validating vulnerabilities. Open to security teams (companies, nonprofits, universities, government), critical infrastructure operators of any size, smaller security firms, open-source maintainers, **and individual researchers with a track record of reported vulnerabilities**. Review: days.
  - **Red Team Access:** adds authorized pentesting/red-teaming. In-house and government red teams, pentesting firms. **Organizations only — individual researchers not eligible.** Review: weeks (Defense Access granted meanwhile). Real-time blocks retained on physical-harm/mass-disruption actions.
  - **Specialized Access:** fewest cyber blocks; limited verified organizations authorized to test safety-critical systems (flight systems, power grids, telecom, interbank, government networks); reviewed in depth **with the US government**; Glasswing members transition here.
- **Nature:** "makes advanced cyber capabilities and reduced blocking classifiers available to qualifying security professionals" — it is **tooling access, never a credential, milestone, or CV line**. Date every statement; the three-tier version is days old.
- **Primary URL:** https://www.anthropic.com/news/cyber-verification-program

## Gaps to close before lessons ship
1. CVE Record **credit field** — verify at cve.org's record documentation (cve.org rendered fine; page not reached this pass).
2. NVD enrichment policy — no primary-source text found; currently multi-outlet reported. Recheck nvd.nist.gov / NIST newsroom before publishing.
3. NICE components — confirm no NIST version newer than 2.0.0 exists at build time.
4. OWASP LLM Top 10 2026 — pull the full renumbered list from genai.owasp.org; never cite bare LLM codes without edition.
