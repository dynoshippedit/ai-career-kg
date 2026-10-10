# Stage E — Expert: research output
Night research, 2026-10-09. Governed by SECURITY_GUIDEBOOK_BRIEF.md.
Sources fetched by this researcher today are marked [fetched]; everything else is a lead for the lesson author to fetch and verify.

---

## PART 1 — CISSP as a body of knowledge

### Source basis

- ISC2 CISSP Certification Exam Outline page, fetched 2026-10-09 [fetched]: https://www.isc2.org/certifications/cissp/cissp-certification-exam-outline — outline effective April 15, 2024; 8 domains; weights 16/10/13/13/13/12/13/10; CAT format 100–150 items, 3 hours, 700/1000 to pass; experience rules (see note below).
- ISC2 Exam Guidance for Artificial Intelligence, fetched 2026-10-09 from ISC2's own CDN [fetched]: https://edge.sitecorecloud.io/internationf173-xmc4e73-prodbc0f-9660/media/Project/ISC2/Main/Media/exam-guidance/ISC2-Exam-Guidance.pdf — document dated September 1, 2026 (first published April 2, 2026 per ISC2 PRNewswire release).
- Full objective numbering (1.1–8.5) cross-checked against the April 2024 detailed content outline text (mirror copy; outline wording below is paraphrased, never reproduced).

### CISSP map page note (say once, per brief)

Full CISSP certification requires five years of cumulative full-time work experience in two or more of the eight domains. A post-secondary degree in a related field or an approved credential from ISC2's list can substitute for up to one year — only one year total can be waived. Part-time work and internships may count. Passing the exam without the required experience makes someone an Associate of ISC2, who then has six years to earn the five years of experience. (Source: isc2.org outline page, fetched 2026-10-09.)

### AI notes: exam content or commentary? — determination

**Answer: the AI material is exam-relevant content, but it is not a separate set of numbered objectives — treat it as context woven into each domain's lessons, not as standalone map entries.**

Evidence:
- The isc2.org outline page itself carries the section "How is AI Security Incorporated into the CISSP Domains?", stating ISC2 interweaves "AI-specific security tasks and subtasks across all eight domains of the CISSP Exam Outline." [fetched]
- The ISC2 Exam Guidance for AI (ISC2's own document) states AI-focused tasks and security considerations are "regularly integrate[d]... into the certification exam blueprints" through the 3-year Job Task Analysis refresh cycle, and maps AI concepts across 50+ exam domains and 200+ subtasks portfolio-wide. [fetched]
- The April 15, 2024 outline's numbered objectives contain only minimal explicit AI references (awareness training covering emerging tech including AI; ML/AI-based defensive tools). There is no ninth domain and no new numbered objectives. The guidance document is dated September 2026 — it is supplementary guidance, not part of the 2024 outline.
- Practical consequence: exam scenarios may feature AI systems (a model to govern, training data to classify, an AI agent identity to manage, model drift to monitor), but the judgment tested is the domain's existing judgment. Each domain lesson should include its AI angle (per the guidance's per-domain mapping) and cross-link to the AI security track. Do not create separate "AI" objectives in the CISSP map.

Per-domain AI angles from the guidance (paraphrased, for lesson cross-links): D1 — AI governance, ethics, AI supply-chain/third-party risk; D2 — training datasets, models, and weights as classified assets, data integrity across the AI lifecycle; D3 — secure enclaves for AI compute, input validation against prompt injection/adversarial input, explainability; D4 — securing transit of training datasets, micro-segmentation of AI environments, AI-driven NDR; D5 — identities for AI agents and service accounts, behavioral/adaptive authentication; D6 — red-teaming AI systems (evasion/extraction robustness), AI-assisted vuln management; D7 — AI in SOAR, alert-fatigue reduction, model-drift monitoring, adversarial-attack response; D8 — risks of AI-generated code, AI security testing in CI/CD, ML supply chain (model hijacking, inference attacks).

### Objective → lesson mapping (62 objectives)

Format: objective — paraphrase of topic — lesson assignment.
"Earlier:" = covered by a lesson from Stages A–D (brief scope). "NEW" = specified Stage E lesson below.
Lesson IDs are proposed; the map author assigns final IDs.

**Domain 1 — Security and Risk Management (16%)**
- 1.1 — professional ethics in security work — NEW E-D1-01
- 1.2 — core security concepts (CIA and related properties) — Earlier: Stage A foundations lesson on security concepts
- 1.3 — security governance: aligning security with business strategy, org roles, control frameworks — NEW E-D1-03
- 1.4 — legal, regulatory, and compliance landscape (cybercrime, IP, import/export, cross-border data, privacy law) — NEW E-D1-04
- 1.5 — investigation types and their requirements (administrative, criminal, civil, regulatory) — NEW E-D1-04 (same lesson)
- 1.6 — security policy, standards, procedures, guidelines — NEW E-D1-06
- 1.7 — business continuity requirements: BIA and dependencies — NEW E-D1-07
- 1.8 — personnel security across hiring, employment, and departure — NEW E-D1-08
- 1.9 — risk management concepts end to end — Earlier: pilot lesson "Risk assessment as a worked case" (brief §8 Phase 2)
- 1.10 — threat modeling concepts and methodologies — Earlier: Stage D AppSec threat-modeling lesson
- 1.11 — supply chain risk management — NEW E-D1-11
- 1.12 — security awareness, education, and training programs — NEW E-D1-12

**Domain 2 — Asset Security (10%)**
- 2.1 — identifying and classifying information and assets — NEW E-D2-01
- 2.2 — information and asset handling requirements — NEW E-D2-01 (same lesson)
- 2.3 — secure provisioning: ownership, inventory, asset management — NEW E-D2-01 (same lesson)
- 2.4 — the data lifecycle: roles, collection, location, maintenance, retention, remanence, destruction — NEW E-D2-04
- 2.5 — asset retention and end-of-life/support — NEW E-D2-04 (same lesson)
- 2.6 — data security controls and compliance: data states, scoping, standards selection, protective methods — NEW E-D2-06

**Domain 3 — Security Architecture and Engineering (13%)**
- 3.1 — secure design principles for engineering — NEW E-D3-01
- 3.2 — formal security models — NEW E-D3-02
- 3.3 — selecting controls from system security requirements — NEW E-D3-01 (same lesson)
- 3.4 — platform security capabilities (memory protection, hardware roots of trust, encryption) — NEW E-D3-01 (same lesson)
- 3.5 — assessing vulnerabilities across architecture and system types — NEW E-D3-05
- 3.6 — cryptographic solutions: lifecycle, methods, PKI, key management, signatures — NEW E-D3-06
- 3.7 — cryptanalytic attack methods — Earlier: Stage A cryptography lesson (attack taxonomy)
- 3.8 — site and facility design principles — NEW E-D3-08
- 3.9 — site and facility security controls — NEW E-D3-08 (same lesson)
- 3.10 — the information system lifecycle — NEW E-D3-10

**Domain 4 — Communication and Network Security (13%)**
- 4.1 — secure network architecture design — NEW E-D4-01
- 4.2 — securing network components — NEW E-D4-01 (same lesson)
- 4.3 — secure communication channels — NEW E-D4-01 (same lesson)

**Domain 5 — Identity and Access Management (13%)**
- 5.1 — controlling physical and logical access to assets — NEW E-D5-01
- 5.2 — identification and authentication strategy — NEW E-D5-02
- 5.3 — federated identity with third-party services — NEW E-D5-02 (same lesson)
- 5.4 — authorization mechanisms and models — NEW E-D5-04
- 5.5 — identity and access provisioning lifecycle — NEW E-D5-05
- 5.6 — implementing authentication systems — Earlier: Stage A HTTP-auth lesson + Stage D cloud IAM

**Domain 6 — Security Assessment and Testing (12%)**
- 6.1 — designing assessment, test, and audit strategies — NEW E-D6-01
- 6.2 — security control testing methods — Earlier: Stage B methodology and vulnerability lessons
- 6.3 — collecting security process data — NEW E-D6-03
- 6.4 — analyzing test output and reporting — Earlier: Stage B reporting lesson + Stage C disclosure lesson
- 6.5 — conducting and facilitating security audits — NEW E-D6-05

**Domain 7 — Security Operations (13%)**
- 7.1 — investigations: evidence, techniques, forensics — Earlier: Stage D DFIR track
- 7.2 — logging and monitoring operations — Earlier: Stage B defensive basics + Stage D detection
- 7.3 — configuration management — NEW E-D7-03
- 7.4 — foundational security operations concepts — NEW E-D7-03 (same lesson)
- 7.5 — resource and media protection — NEW E-D2-06 (same lesson as 2.6)
- 7.6 — incident management — Earlier: Stage D DFIR track
- 7.7 — operating detective and preventive measures — Earlier: Stage B defensive basics + Stage D
- 7.8 — patch and vulnerability management operations — NEW E-D7-08
- 7.9 — change management — NEW E-D7-03 (same lesson)
- 7.10 — recovery strategies and resilience — NEW E-D7-10
- 7.11 — disaster recovery processes — NEW E-D7-11
- 7.12 — testing the disaster recovery plan — NEW E-D7-11 (same lesson)
- 7.13 — business continuity planning and exercises — NEW E-D1-07 (same lesson as 1.7)
- 7.14 — physical security implementation — NEW E-D3-08 (same lesson as 3.8/3.9)
- 7.15 — personnel safety and security concerns — NEW E-D1-08 (same lesson as 1.8)

**Domain 8 — Software Development Security (10%)**
- 8.1 — security in the SDLC — Earlier: Stage D AppSec track
- 8.2 — security controls in development ecosystems — Earlier: Stage D AppSec track
- 8.3 — assessing software security effectiveness — Earlier: Stage D AppSec track
- 8.4 — security impact of acquired software — Earlier: Stage D AppSec track (+ E-D1-11 cross-link)
- 8.5 — secure coding guidelines and standards — Earlier: Stage D AppSec track + Stage B vulnerability lessons

**Coverage: 62 of 62 objectives mapped. 47 via new Stage E lessons (several lessons serve multiple objectives across domains); 15 via earlier-stage lessons. Zero unmapped objectives.**

### New Stage E lesson specifications

Each: primary-source leads (fetch before writing), ≤3 free resources (leads), worked case, proof artifact, prerequisites. Levels per brief §1: most target level 3.

**E-D1-01 Professional ethics in security** — Serves 1.1. Primary: ISC2 Code of Professional Ethics (isc2.org). Free resources: the Code itself; a published ethics case collection (lead: ISC2 ethics resources). Worked case: written analysis of two ethical dilemmas (e.g., discovering a client's unpatched critical system during an unrelated engagement; pressure to understate findings), argued from the Code's canons. Artifact: the dilemma analyses. Prerequisites: none beyond Stage D. Level 2.

**E-D1-03 Security governance: aligning security to the business** — Serves 1.3. Primary: NIST CSF 2.0 governance function (nvlpubs.nist.gov); COBIT framework overview (isaca.org, free overview). Free resources: NIST CSF 2.0 (free); a governance charter template from a public source (lead). Worked case: draft a security governance charter for a fictional mid-size company — mission alignment statement, roles (CISO, risk committee), reporting lines, control framework selection rationale. Artifact: the charter. Prerequisites: E-D1-09 (risk). AI angle: AI governance roles per ISC2 guidance. Level 3.

**E-D1-04 Cyber law, regulation, and investigation requirements** — Serves 1.4, 1.5. Primary: GDPR text (eur-lex.europa.eu, free); a national cybercrime statute overview (lead: DOJ CCIPS pages, justice.gov). Free resources: EUR-Lex GDPR; NIST privacy framework (free); EFF or similar plain-language legal explainers (lead). Worked case: compliance-mapping matrix for a fictional company handling EU and US customer data — which obligations apply, what evidence each needs; plus an investigation-type decision tree (when an incident triggers administrative vs criminal vs regulatory paths). Artifact: the matrix + decision tree. Prerequisites: E-D2-01. AI angle: EU AI Act obligations per guidance. Level 3.

**E-D1-06 Security policy, standards, procedures, guidelines** — Serves 1.6. Primary: NIST SP 800-series policy guidance (lead: SP 800-53 control families as structure reference, nist.gov). Free resources: SANS policy templates (free); NIST CSF 2.0. Worked case: write a three-tier document set for one control area (e.g., acceptable encryption): one-page policy, standard with requirements, procedure with steps. Artifact: the document set. Prerequisites: E-D1-03. Level 3.

**E-D1-07 Business continuity: BIA and planning** — Serves 1.7, 7.13. Primary: NIST SP 800-34 (contingency planning, nist.gov, free). Free resources: NIST SP 800-34; a BIA questionnaire template (lead). Worked case: full BIA for a fictional company's three critical processes — impact tiers, RTO/RPO, dependencies — plus a BC exercise plan (tabletop scenario). Artifact: BIA + exercise plan. Prerequisites: E-D1-09. Level 3.

**E-D1-08 Personnel security across the employment lifecycle** — Serves 1.8, 7.15. Primary: NIST SP 800-53 personnel security family (lead). Free resources: public personnel-security checklists (lead); CISA insider-threat resources (cisa.gov, free). Worked case: termination checklist and access-revocation runbook for a privileged employee departure; travel-security briefing for one high-risk trip. Artifact: checklist + runbook. Prerequisites: E-D5-05. Level 3.

**E-D1-09 Risk assessment as a worked case** — Serves 1.9. This is pilot lesson 3 (brief §8 Phase 2). Primary: NIST SP 800-30 (risk assessment, nist.gov, free). Worked case: complete risk assessment for a fictional web application — threat/vulnerability identification, analysis, risk response decisions, control selection by type, monitoring plan, and a one-page risk report. Artifact: the risk assessment + report. Prerequisites: Stage C (vuln thinking). Level 3.

**E-D1-11 Supply chain risk management** — Serves 1.11. Primary: NIST SP 800-161 (C-SCRM, nist.gov, free). Free resources: NIST SP 800-161; CISA ICT SCRM resources (cisa.gov, free). Worked case: vendor risk assessment for a fictional SaaS purchase — acquisition risk factors, mitigations (assessment, minimum requirements, SBOM review), residual risk decision. Artifact: the assessment. Prerequisites: E-D1-09. AI angle: AI supply-chain transparency per guidance. Level 3.

**E-D1-12 Security awareness, education, and training** — Serves 1.12. Primary: NIST SP 800-50 (security awareness/training, nist.gov, free). Free resources: CISA awareness materials (cisa.gov); SANS security awareness planning kit (free). Worked case: a one-year awareness program plan — audience segments, topics calendar, phishing-simulation rules of engagement, effectiveness metrics. Artifact: the program plan. Prerequisites: none beyond Stage D. Level 3.

**E-D2-01 Asset identification, classification, and handling** — Serves 2.1, 2.2, 2.3. Primary: NIST SP 800-60 (guide to mapping types of information to security categories, nist.gov, free). Free resources: a public data-classification policy template (lead); NIST SP 800-60. Worked case: data classification scheme for a fictional company — four tiers with definitions, examples, handling rules per tier, ownership assignments. Artifact: the scheme. Prerequisites: E-D1-06. AI angle: classifying training datasets and model weights as assets. Level 3.

**E-D2-04 The data lifecycle and retention** — Serves 2.4, 2.5. Primary: NIST SP 800-88 (media sanitization, nist.gov, free). Free resources: NIST SP 800-88; a retention-schedule template (lead). Worked case: retention and destruction schedule for five data types — legal basis, retention period, destruction method per NIST 800-88, EOL handling for the systems holding them. Artifact: the schedule. Prerequisites: E-D2-01. Level 3.

**E-D2-06 Data protection controls** — Serves 2.6, 7.5. Primary: NIST SP 800-111 (storage encryption, nist.gov, free); DLP/CASB vendor-neutral explainers (lead). Free resources: OWASP data-protection cheat sheets; NIST SP 800-111. Worked case: control-selection matrix for data in use / in transit / at rest for a fictional company — method per state, compliance mapping, media-protection procedures. Artifact: the matrix. Prerequisites: Stage A cryptography. Level 3.

**E-D3-01 Secure design principles and control selection** — Serves 3.1, 3.3, 3.4. Primary: NIST SP 800-160 (systems security engineering, nist.gov, free). Free resources: OWASP Secure Design Principles (free); NIST SP 800-160 overview. Worked case: architecture review of a reference design — apply each principle, record pass/fail with rationale, select controls traceable to requirements. Artifact: the review. Prerequisites: Stage D (any track). AI angle: zero-trust for AI environments per guidance. Level 3.

**E-D3-02 Security models** — Serves 3.2. Primary: the original model papers are the ideal primary sources (lead: Bell-LaPadula, Biba summaries from academic sources). Free resources: a university lecture series on security models (lead); NIST IR 8360 (free). Worked case: model-selection rationale — which model fits a military records system vs a financial integrity system vs a commercial confidentiality system, and why the others don't. Artifact: the rationale write-up. Prerequisites: E-D3-01. Level 2 (recognition + application of selection judgment).

**E-D3-05 Architecture vulnerability assessment** — Serves 3.5. Primary: NIST SP 800-115 (technical testing, nist.gov, free) for assessment method. Free resources: MITRE ATT&CK (free); OWASP ASVS (free). Worked case: architecture risk assessment of a fictional hybrid system (cloud + IoT + API microservices) — enumerate per-component vulnerability classes, rate, recommend. Artifact: the assessment. Prerequisites: Stage D cloud or AppSec track. AI angle: AI compute enclave considerations. Level 3.

**E-D3-06 Cryptographic lifecycle, PKI, and key management** — Serves 3.6. Primary: NIST SP 800-57 (key management, nist.gov, free); RFC 5280 (PKI certificates, free). Free resources: NIST SP 800-57 overview; a PKI deployment guide (lead). Worked case: key-management policy for a fictional company — algorithm selection rationale, rotation schedule, PKI hierarchy sketch, compromise response. Artifact: the policy. Prerequisites: Stage A cryptography. Level 3.

**E-D3-08 Physical and site security** — Serves 3.8, 3.9, 7.14. Primary: NIST SP 800-53 physical/environmental family (lead). Free resources: ASIS or similar physical-security guidelines overview (lead); FEMA site-security resources (fema.gov, free). Worked case: facility security review checklist for a fictional office + data closet — perimeter, internal, environmental, power, fire. Artifact: the completed checklist with findings. Prerequisites: none beyond Stage D. Level 3.

**E-D3-10 Information system lifecycle** — Serves 3.10. Primary: NIST SP 800-160 (free). Free resources: ISO/IEC 15288 overview (lead, free summaries). Worked case: lifecycle gate-review template — security deliverables required at each phase from requirements to disposal, applied to a fictional system. Artifact: the template + one completed gate review. Prerequisites: E-D3-01. Level 3.

**E-D4-01 Secure network architecture** — Serves 4.1, 4.2, 4.3. Primary: NIST SP 800-207 (zero trust architecture, nist.gov, free); RFC 9293 (TCP), 1034/1035 (DNS) as protocol primaries (free). Free resources: NIST SP 800-207; a segmentation design guide (lead). Worked case: network segmentation design review for a fictional company — zones, trust boundaries, NAC placement, remote-access and third-party connectivity decisions, monitoring points. Artifact: the design review. Prerequisites: Stage A networking. AI angle: micro-segmentation for AI training environments per guidance. Level 3.

**E-D5-01 Enterprise access control** — Serves 5.1. Primary: NIST SP 800-53 access control family (lead). Free resources: NISTIR 7316 (attribute-based access control, free). Worked case: access-control matrix for a fictional company's crown-jewel system — who/what gets access to information, systems, devices, facilities, applications, services, and the control per asset. Artifact: the matrix. Prerequisites: E-D5-04. Level 3.

**E-D5-02 Identity and authentication strategy** — Serves 5.2, 5.3. Primary: NIST SP 800-63 (digital identity guidelines, nist.gov, free). Free resources: NIST SP 800-63; FIDO Alliance explainers (fidoalliance.org, free). Worked case: authentication architecture decision for a fictional company — assurance levels per user population, MFA/passwordless choices, SSO vs federation decision, third-party IdP evaluation criteria. Artifact: the decision document. Prerequisites: Stage A HTTP-auth lesson. AI angle: non-human identities (AI agents, service accounts) per guidance. Level 3.

**E-D5-04 Authorization models** — Serves 5.4. Primary: NISTIR 7316 (ABAC, free); RBAC standard INCITS 359 (lead). Free resources: NISTIR 7316; an authorization-model comparison (lead). Worked case: model-selection analysis — RBAC vs ABAC vs risk-based for three scenarios (hospital records, SaaS multi-tenant, trading floor), including PDP/PEP placement. Artifact: the analysis. Prerequisites: E-D5-02. Level 3.

**E-D5-05 Identity lifecycle and access reviews** — Serves 5.5. Primary: NIST SP 800-53 (lead). Free resources: an access-review template (lead); SANS IAM resources (free). Worked case: a full access review for a fictional company — reviewer assignments, recertification decisions on a sample account list, orphaned service accounts dispositioned, privilege-escalation paths (sudo) audited. Artifact: the completed review. Prerequisites: E-D5-02. Level 3.

**E-D6-01 Assessment, test, and audit strategy** — Serves 6.1. Primary: NIST SP 800-115 (free); ISACA audit guidance overviews (lead). Free resources: OWASP testing guide strategy section; NIST SP 800-115. Worked case: annual assessment strategy for a fictional company — internal vs external vs third-party coverage, locations (on-prem/cloud), cadence, scoping rules. Artifact: the strategy document. Prerequisites: Stage B methodology. Level 3.

**E-D6-03 Security process data and metrics** — Serves 6.3. Primary: NIST SP 800-55 (performance measurement, nist.gov, free). Free resources: NIST SP 800-55; CIS security metrics (free). Worked case: KPI/KRI set for a fictional SOC — definitions, data sources, collection method, review cadence; backup-verification and training-completion measures included. Artifact: the metrics specification. Prerequisites: Stage B defensive basics. Level 3.

**E-D6-05 Security audits** — Serves 6.5. Primary: ISACA IS audit standards overviews (lead); NIST SP 800-115. Free resources: a public audit work-program template (lead). Worked case: audit plan for one control family — objectives, procedures, evidence requests, sampling approach, finding write-up format. Artifact: the audit plan + one completed finding. Prerequisites: E-D6-01. Level 3.

**E-D7-03 Operational disciplines: configuration, change, privilege** — Serves 7.3, 7.4, 7.9. Primary: NIST SP 800-128 (configuration management, nist.gov, free). Free resources: CIS Benchmarks (free); NIST SP 800-128. Worked case: hardening baseline for a server role + a change-request review (approve/reject with rationale) + a privileged-access SoD matrix. Artifact: baseline + reviewed change + matrix. Prerequisites: Stage A Linux. Level 3.

**E-D7-08 Patch and vulnerability management operations** — Serves 7.8. Primary: CISA KEV catalog (cisa.gov, free); NIST SP 800-40 (patching, nist.gov, free). Free resources: CISA KEV; NIST SP 800-40. Worked case: patching SLA policy for a fictional company — severity-to-timeline mapping tied to KEV membership, exception process, emergency patching runbook. Artifact: the policy. Prerequisites: Stage C (CVE/CVSS/KEV lessons). Level 3.

**E-D7-10 Recovery strategies and resilience** — Serves 7.10. Primary: NIST SP 800-34 (free). Free resources: NIST SP 800-34; a recovery-strategy comparison (lead). Worked case: recovery strategy selection for three systems (backup strategies, site strategies, resilience options) with cost/complexity trade-off analysis — no currency figures, qualitative tiers only. Artifact: the selection document. Prerequisites: E-D1-07. Level 3.

**E-D7-11 Disaster recovery planning and testing** — Serves 7.11, 7.12. Primary: NIST SP 800-34 (free). Free resources: a DRP template (lead); a tabletop exercise scenario library (lead). Worked case: DR plan excerpt for one critical system (response roles, communications plan, restoration steps) + a tabletop exercise script with injects. Artifact: plan excerpt + exercise script. Prerequisites: E-D7-10. Level 3.

---

## PART 2 — Governance and leadership

Full dossier: `05b-governance-leadership.md` (same directory). Four Stage E lessons at level 3, all primary-source verified 2026-10-09. Condensed specs below; the dossier holds the full lesson-spec detail (how-it-works prose, check-yourself questions, leads-to).

**E-GOV-01 NIST Cybersecurity Framework 2.0** — Primary: NIST CSWP 29 (Feb 26, 2024), fetched from nist.gov [fetched]. Structure verified by counting the document: 6 Functions (Govern new in 2.0, at the center), 22 Categories, 106 Subcategories. CSF states outcomes (what), not actions (how) — never a checklist, and there is no such thing as "CSF certified." Method: Organizational Profiles (Current vs Target), gap analysis → action plan, Tiers 1–4 (Partial, Risk Informed, Repeatable, Adaptive) as a communication aid. Free resources: the CSF 2.0 PDF itself; NIST CSF 2.0 Quick-Start Guides; NIST SP 800-30 Rev. 1. Worked case: CSF gap assessment → target profile sketch for a fictional SaaS company, all 22 Categories, evidence per row. Artifact: Current-vs-Target profile sketch + prioritized action plan. Prerequisites: Stage A (lighter), Stage E risk lesson. Level 3.

**E-GOV-02 ISO/IEC 27001** — One line per brief: ISO/IEC 27001:2022 is a paid document sold by ISO. Structure taught from ISO's own free pages (iso.org standard page, ISO Help Centre) [fetched]: ISMS concept; Clauses 4–10 are the certifiable management system; Annex A is a reference catalog of 93 controls in four themes (organizational, people, physical, technological) — selected by risk assessment, never a mandatory checklist; the Statement of Applicability is the load-bearing artifact. Certification is voluntary, via accredited bodies. Free resources: ISO Help Centre overview; ISO standard page; CSF 2.0 Informative References (ISO↔CSF mapping). Worked case: theme-level readiness checklist + SoA sketch with risk-based justifications. Artifact: readiness checklist + SoA sketch. Prerequisites: E-GOV-01, E-D1-09. Level 3.

**E-GOV-03 SOC 2 and the Trust Services Criteria** — Primary: AICPA-authored testimony (AICPA Associate Director, Attestation Methodology, before the ERISA Advisory Council, hosted on dol.gov) [fetched]. SOC 2 is an examination engagement by a CPA against the AICPA Trust Services Criteria — an attestation report, not a certificate; no pass/fail. Five criteria (paraphrased): Security (mandatory — the common criteria), Availability, Processing Integrity, Confidentiality, Privacy. Type I = design at a point in time; Type II = design + operating effectiveness over a period, with test descriptions and results. Requested by customers/partners for vendor risk management; restricted use (SOC 3 is the general-use sibling). Free resources: the AICPA testimony PDF; CSF 2.0 Informative References; (third slot held for the AICPA's own SOC 2 page — not fetched, see gaps). Worked case: scoping memo for a fictional SaaS — each criterion tied to a specific contract/SLA/privacy commitment. Artifact: the scoping memo. Prerequisites: E-GOV-01, E-GOV-02. Level 3.

**E-LEAD-01/02 Running a security program: strategy, metrics, board communication** — Primary: CSF 2.0 §5 (risk communication, bidirectional exec/manager/practitioner flow) [fetched]; NIST SP 800-30 Rev. 1 (risk assessment method) [fetched]; NIST SP 800-55 v1/v2 release page (measurement program, final Dec 2024) [fetched]. Strategy = the Govern loop running continuously. Metrics: KPIs measure the program's work, KRIs measure the risk's size — green KPIs with worsening KRIs means busy but exposed. Board rule: business-impact language, decisions required, every number sourced; invented statistics are banned as a hard lesson rule. Free resources: CSF 2.0 §5; SP 800-30 Rev. 1; SP 800-55 release page. Worked cases: (a) 6-row risk register on SP 800-30 concepts with defined qualitative scale, responses, owners, review date; (b) one-page board memo skeleton with labeled placeholders. Artifacts: risk register + board memo. Prerequisites: E-GOV-01–03, E-D1-09. Level 3.

Source ledger and gaps for Part 2 live in `05b-governance-leadership.md` (Key sources table, 8 rows, all fetched 2026-10-09; 7 gaps logged, including: no aicpa.org fetch — TSC edition currency must be re-checked; ISO certification lifecycle unverified; 106-subcategory count to re-verify against the machine-readable Core; SP 800-55 volumes not read, only the release page).

---

## Gaps and verification notes

1. Objective numbering verified against the April 15, 2024 detailed content outline (effective date confirmed on isc2.org). If ISC2 publishes a newer outline, the 1.1–8.5 numbering must be re-verified.
2. The ISC2 Exam Guidance for AI PDF was fetched from ISC2's CDN (edge.sitecorecloud.io) — document dated September 1, 2026, first published April 2, 2026 per ISC2's PRNewswire release. Its per-domain AI mapping is summarized above in paraphrase.
3. No exam questions or outline text reproduced anywhere in this file — objectives referenced by number with original paraphrases only.
4. Lesson specs name primary-source leads; the lesson author must fetch each primary source in-session for the ledger per brief §7.
5. 15 objectives map to earlier-stage lessons whose exact lesson IDs don't exist yet (night research in progress) — the map author should confirm those lessons ship; any that don't become gaps or new E lessons.
6. No prices, fees, salaries, or time estimates appear in this file.
7. Part 2 (E-GOV-01–03, E-LEAD-01/02) merged from `05b-governance-leadership.md` 2026-10-09; its 8-row source ledger and 7 gaps are authoritative for those lessons — carry them into the site's sources.csv and gaps.md unchanged.
