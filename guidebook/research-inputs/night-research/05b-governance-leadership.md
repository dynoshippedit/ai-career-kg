# 05b — Governance and leadership (Stage E research dossier)

Research date: 2026-10-09. All external facts below were fetched from primary sources on that date (see Key sources). Everything is paraphrased; no copyrighted text reproduced. No prices, fees, salaries, or time estimates anywhere.

Scope: four Stage E lessons — (1) NIST CSF 2.0, (2) ISO/IEC 27001, (3) SOC 2, (4) running a security program (strategy, metrics, board communication; includes the risk-register and board-memo worked cases). All four target **level 3 (Apply)**: the reader applies the framework to an unfamiliar (fictional) organization unaided, produces the real work product, and explains their choices.

Suggested lesson metadata: stage E; level 3; primary role path `/r/grc-analyst/`; candidate future role "security program lead" (for the Stop 1 candidate-role list — no role page created); CISSP map references by domain number only (domains 1, 6, 7).

---

## Lesson 1 — NIST Cybersecurity Framework 2.0

### Where this shows up
A GRC analyst, a security manager, or anyone asked "how secure are we, and what should we do next?" uses the CSF to answer in a language executives understand. It is the scaffolding the other three lessons hang on: ISO 27001 controls and SOC 2 criteria both map to CSF outcomes, and the risk register and board memo in Lesson 4 are built from CSF vocabulary.

### Before you start (prerequisites)
- Stage A foundations (lighter pass acceptable per brief §5 role path): what an asset, a control, and a risk are.
- The Stage E risk-assessment lesson (SP 800-30): likelihood, impact, risk response vocabulary.
- Nothing to install. Reading: the CSF 2.0 document itself (free).

### How it works
The CSF 2.0 (NIST CSWP 29, published February 26, 2024) is a taxonomy of cybersecurity *outcomes* — statements of what good looks like — not a checklist of actions and not a control catalog. NIST is explicit that it does not prescribe how outcomes are achieved; online Informative References point each outcome at existing standards and control catalogs (e.g., SP 800-53) that suggest how. This is the single most common misreading to correct early: the CSF says *what*, other documents say *how*.

**Structure (counts verified from the primary document, 2026-10-09):** the CSF Core is a three-level hierarchy — **6 Functions, 22 Categories, 106 Subcategories**. I verified this by counting the primary text: Appendix A, Table 1 lists all 22 Categories under their 6 Functions, and counting the numbered Subcategory statements in the appendix listing gives 106 (e.g., Govern 31, Identify 21, Protect 22, Detect 11, Respond 13, Recover 8; subcategory numbering is intentionally non-sequential — gaps are CSF 1.1 items relocated in 2.0).

**The six Functions, in my own words:**
- **Govern (GV)** — new in 2.0, and the center of the wheel. Senior-leadership work: set the cybersecurity risk strategy, define risk appetite and tolerance, assign roles and hold people accountable, write policy, watch over the whole program, and manage supply-chain risk. It tells the other five functions what to prioritize and why.
- **Identify (ID)** — know what you have and what threatens it. Inventory hardware, software, data, and suppliers; assess vulnerabilities, threats, likelihoods, and impacts; keep improving the program itself.
- **Protect (PR)** — put safeguards in place so identified risks are less likely or less damaging: who can access what, training, data safeguards, hardened platforms, resilient infrastructure.
- **Detect (DE)** — notice when something bad may be happening: continuous monitoring of networks, people, providers, and systems, plus analyzing anomalies to decide what counts as an incident.
- **Respond (RS)** — act on a declared incident: run the plan, analyze what happened, tell the right people, contain and eradicate.
- **Recover (RC)** — get back to normal: execute the recovery plan, verify restored systems, and communicate progress.

**How an organization uses it (Profiles and Tiers, in my own words):**
- An **Organizational Profile** is the organization's own statement of its posture in CSF terms. The **Current Profile** records which outcomes are actually achieved today and how well; the **Target Profile** records which outcomes leadership has chosen to pursue, given mission, threats, and requirements. A **Community Profile** is a published baseline for a sector or use case that an organization can adopt as its starting target.
- The standard workflow is five steps: scope the profile, gather information (policies, risk priorities, existing practices), write the Current and Target profiles, **run a gap analysis** between them and turn the gaps into a prioritized action plan (NIST names the risk register, risk detail report, or POA&M as the tracking vehicle), then implement and repeat.
- **Tiers** characterize how rigorously the organization does all this, on a four-step ladder: Tier 1 Partial (ad hoc), Tier 2 Risk Informed (management-approved but not organization-wide), Tier 3 Repeatable (formal policy, regularly updated, organization-wide), Tier 4 Adaptive (continuous improvement, lessons learned and predictive indicators, cyber risk discussed alongside financial risk). Tiers are a communication aid, not a score — and NIST warns they complement, not replace, the organization's own risk methodology.

### Walkthrough (worked case): CSF gap assessment → target profile sketch
Fictional organization: "ExampleCo," a 25-person SaaS company hosting a customer-facing app and storing customer data in the cloud. No dedicated security staff; one IT generalist.

The reader builds a three-column working table for a sample of Categories (the lesson instructs doing all 22; the dossier shows the pattern):

| Category | Current (evidence) | Target | Gap → action |
|---|---|---|---|
| GV.RM Risk Management Strategy | Tier ~1: no written risk strategy; decisions ad hoc | Written risk appetite statement, approved by founders | Draft one-page risk strategy; record in risk register |
| ID.AM Asset Management | Partial inventory: production servers known, SaaS tools not inventoried | Inventories of hardware, software/services, data maintained | Run SaaS-discovery; assign asset owners |
| PR.AA Identity Mgmt & Access Control | Passwords + MFA on email only | MFA everywhere; least-privilege reviews | Roll out MFA to all services; quarterly access review |
| PR.DS Data Security | Backups exist, never test-restored | Backups created, protected, and *tested* | Quarterly restore test; document results |
| DE.CM Continuous Monitoring | No central logging | Log records generated and available for monitoring | Ship logs to one place; define what "adverse event" means here |
| RS.MA Incident Management | No written plan | Incident response plan exists and names who does what | Write the plan; run one tabletop |
| RC.RP Recovery Plan Execution | "We'd rebuild from backups" | Recovery actions selected, scoped, prioritized, and practiced | Tie recovery steps to the backup test |

Success test for the reader's own version: every row names *evidence* for the current state (not vibes), every gap maps to exactly one action with an owner, and the target column references the CSF outcome by ID (e.g., PR.DS-11) without copying its text.

Common misreadings to call out: treating the CSF as a compliance checklist; assessing subcategories without reading the category outcome they serve; setting the target profile at Tier 4 everywhere on day one.

### Prove it (artifact)
A Current-vs-Target profile sketch (spreadsheet or markdown table) for the fictional org covering all 22 Categories, plus a one-page prioritized action plan. The reader can claim: "I can scope a CSF profile, run a gap analysis, and turn gaps into an action plan." They cannot claim certification or audit competence — the CSF has no certification.

### Read the source
NIST CSWP 29, *The NIST Cybersecurity Framework (CSF) 2.0* (Feb 26, 2024). Read in this order: §1 (overview — what it is and is not), §2 (the six Functions), §3 (Profiles and Tiers — the working method), §5 (risk communication — feeds Lesson 4), then Appendix A (the Core itself), Appendix B (Tier illustration). Skim the Preface/Acknowledgments. The PDF states the Core is also available in machine-readable form via the CSF 2.0 Reference Tool for anyone who wants to automate the profile.

### Free resources (≤3)
1. The CSF 2.0 document itself (NIST CSWP 29, free PDF) — the lesson's primary text. https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=957258
2. NIST's CSF 2.0 Quick-Start Guides (referenced in CSWP 29 §4 as the on-ramp for small organizations) — for readers who find the full document heavy; find via the NIST CSF website linked from the PDF.
3. NIST SP 800-30 Rev. 1 (free PDF) — the risk-assessment method that fills in ID.RA in practice. https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=912091

### Check yourself
1. A vendor tells you they are "CSF certified." What is wrong with that sentence, and what would you ask them instead?
2. Why does the CSF put Govern at the center of the wheel rather than treating it as a seventh step after Recover?
3. Your Current and Target profiles are identical. Is that success or a problem? Explain what it implies about the gap analysis.
4. Two teams both claim Tier 3. One has written policies nobody follows; the other has consistent practice but thin documentation. How does Appendix B's Tier illustration help you tell them apart?
5. A startup adopts a Community Profile as its Target Profile unchanged. When is that reasonable, and what must they still do themselves?

### Leads to
Lesson 2 (ISO 27001 readiness — controls that achieve CSF outcomes); Lesson 4 (the profile feeds the board memo).

---

## Lesson 2 — ISO/IEC 27001

ISO/IEC 27001:2022 is a paid document sold by ISO; the lesson teaches its structure from free equivalents and never reproduces its text.

### Where this shows up
Customers — especially outside the US — ask vendors "are you ISO 27001 certified?" A GRC analyst runs the readiness effort: scoping the management system, driving the risk assessment, choosing controls, surviving the audit. Unlike the CSF (a voluntary taxonomy), ISO 27001 is a *certifiable requirements standard*.

### Before you start (prerequisites)
- Lesson 1 (CSF 2.0): outcome-vs-control distinction.
- The Stage E risk-assessment lesson: risk assessment drives everything in this standard.

### How it works (structure in my own words, from free ISO sources)
An **ISMS (Information Security Management System)** is the organization's whole apparatus for managing information risk — policies, processes, people, and tools run as a system, not a pile of tools. ISO/IEC 27001:2022 (Edition 3, published 2022-10, maintained jointly by ISO and IEC under JTC 1/SC 27) specifies the *requirements* such a system must meet. ISO's own page states the standard's purpose plainly: it helps organizations become risk-aware and proactively address weaknesses, across people, policies, and technology, to preserve confidentiality, integrity, and availability.

Two halves, and confusing them is the classic beginner error:
- **Clauses 4–10** are the management system itself — the part an auditor certifies. In plain terms: define the context and scope of the system (4), get leadership to own it and set policy (5), plan around risk — assess risks, decide how to treat them, set objectives (6), resource and support it — people, competence, awareness, documentation (7), operate it day to day (8), check that it works — monitoring, internal audit, management review (9), and fix and improve it (10). Certification is against these clauses.
- **Annex A** is a *reference catalog* of controls you select from based on your risk assessment — not a mandatory checklist. The 2022 revision organizes **93 controls into four themes** (confirmed on ISO's own Help Centre page): organizational, people, physical, and technological. You record your choices and justifications in the **Statement of Applicability (SoA)**: one row per control, applicable or not, why, and what evidence shows it works. The SoA is the document an auditor will spend the most time in.

Certification, per ISO's own page: voluntary, performed by an accredited certification body (an external auditor), and a way to demonstrate to customers and stakeholders that the system is real. (Certification lifecycle details such as certificate duration and surveillance cadence were not verified on a primary source — logged as a gap.)

### Walkthrough (worked case): ISO 27001 readiness checklist mapped to Annex A themes
Same fictional ExampleCo. The reader builds a readiness checklist at theme level (the lesson notes the full 93-control SoA comes later, one row per control):

| Theme (Annex A) | Readiness questions (paraphrased topics) | Status | Evidence / SoA note |
|---|---|---|---|
| A.5 Organizational | Is there a written information-security policy approved by leadership? Are supplier security requirements in contracts? Is there a threat-intelligence source? An incident-management procedure? | P | Policy drafted, not approved → SoA: applicable, implementing |
| A.6 People | Are background checks done for privileged roles? Is security awareness training tracked? Are remote-working rules written? | N | No training records → SoA: applicable, not started |
| A.7 Physical | Is office/server access restricted and logged? Is equipment disposal handled? | Y | Badge logs exist → SoA: applicable, operating |
| A.8 Technological | Is access provisioned by least privilege and reviewed? Is cryptography used for data in transit/at rest? Are logs collected? Is development change-controlled? Is there web filtering / malware protection? | P | MFA partial; no log centralization → SoA: applicable, partial |

Success test: every row has an evidence pointer (a document, a log, a ticket — or "none, gap"), and the SoA column states applicable/not-applicable *with a risk-based justification* for each. "Not applicable because we're small" is not a justification; "not applicable because we have no remote workers and the risk assessment records that" is.

Where it goes wrong: treating Annex A as 93 mandatory checkboxes; writing the SoA before doing the risk assessment; scoping the ISMS as "the IT department" while customer data lives in marketing's SaaS tools; confusing ISO 27001 (requirements, certifiable) with ISO 27002 (guidance on implementing controls, not certifiable).

### Prove it (artifact)
A completed readiness checklist plus a Statement of Applicability sketch for the fictional org. Claim: "I can scope an ISMS, run a theme-level readiness review, and draft an SoA with risk-based justifications." Cannot claim: ability to pass or conduct a certification audit.

### Read the source
- https://www.iso.org/standard/27001 — ISO's own page: what the standard is, why it matters, the voluntary-certification FAQ, the CIA-triad FAQ. Read "What is ISO/IEC 27001?", "Why is it important?", and the FAQ.
- ISO Help Centre article (above) — the free summary of the 93-control / four-theme Annex A structure and the ongoing processes (plan on risk, train, monitor, audit, improve).
- Then the CSF 2.0 Informative References (referenced in CSWP 29 §4) to see how ISO controls map to CSF outcomes.

### Free resources (≤3)
1. ISO Help Centre: "ISO/IEC 27001 — Information Security Management Systems" (ISO's own free overview; confirms the 93-control, four-theme structure). https://help.iso.org/en/articles/376290-iso-iec-27001-information-security-management-systems
2. ISO's official standard page (describes the standard, its purpose, and certification; the document itself is paid). https://www.iso.org/standard/27001
3. NIST CSWP 29 §4 + the CSF 2.0 Reference Tool's Informative References — free mapping between ISO 27001 controls and CSF outcomes (shows how Lessons 1 and 2 connect). (Reference Tool not fetched this session; reach it via the NIST CSF website named in CSWP 29.)

### Check yourself
1. An auditor asks for your Statement of Applicability and you hand them a list of the 93 controls with checkmarks. What is missing, and why does the standard require it?
2. Your risk assessment finds no significant risk from physical theft (fully cloud, no office). Can you mark the physical theme "not applicable" outright? What must the SoA row contain?
3. Why does certification test Clauses 4–10 rather than counting how many Annex A controls you implemented?
4. A vendor says "we follow ISO 27002, so we're basically ISO 27001 certified." Unpack the two errors in that sentence.
5. Your ISMS scope covers "the engineering department" but customer data is processed by the support team's SaaS helpdesk. What breaks, and which clause is it a problem for?

### Leads to
Lesson 3 (SOC 2 — the other audit customers ask for; compare certification vs. attestation); Lesson 4 (the internal audit and management review feed program metrics).

---

## Lesson 3 — SOC 2

### Where this shows up
A US enterprise buying SaaS sends the vendor a security questionnaire, and the fastest way to answer it is "here is our SOC 2 Type II report." The GRC analyst scopes which criteria the report covers, herds the evidence, and hands the auditor a coherent system description. SOC 2 is the American counterpart to the ISO conversation in Lesson 2 — and the differences between them are the lesson.

### Before you start (prerequisites)
- Lesson 1 (CSF 2.0): control objectives stated as outcomes.
- Lesson 2 (ISO 27001): certification vs. attestation distinction (below).

### How it works (in my own words; sourced to AICPA-authored testimony hosted by the US Department of Labor, fetched 2026-10-09)
SOC 2 is an **examination engagement**: a licensed CPA examines a *service organization's* system and gives an opinion on whether its controls meet the AICPA's **Trust Services Criteria (TSC)**. Key contrasts with ISO 27001: SOC 2 produces an *attestation report* (an auditor's opinion), not a *certificate*; it is scoped to the services you sell to customers, not to a whole management system; and there is no pass/fail — the report describes the system, the controls, the tests, and the results, and the *reader* decides whether to trust you.

**The five Trust Services Criteria** (2017 TSC, with Revised Points of Focus 2022, per the AICPA testimony):
- **Security** — the system resists unauthorized access, disclosure, and damage that could undermine everything else. This one is mandatory in every SOC 2; the criteria for it alone are called the *common criteria* (control environment, communication and information, risk assessment, monitoring activities, and control activities such as logical/physical access, system operations, and change management).
- **Availability** — the system is actually up and usable as promised.
- **Processing integrity** — the system processes data completely, correctly, on time, and only when authorized. Matters most when customers rely on your processing being *right* (billing, calculations, data pipelines).
- **Confidentiality** — information the company has designated confidential is protected as promised.
- **Privacy** — personal information is collected, used, kept, shared, and disposed of in line with the company's own privacy commitments.

**Type I vs. Type II** (per the AICPA testimony): a **Type I** report gives the CPA's opinion on the system description and whether the controls were *suitably designed* as of a single point in time — a design snapshot. A **Type II** report covers design *plus* whether the controls *operated effectively over a period of time*, and it includes a detailed description of the auditor's tests and their results. Type II is what enterprise procurement usually asks for, because a control that exists on paper but never ran is the exact failure mode they fear.

**Who asks for SOC 2 reports and why:** customers and business partners request them to support their own risk assessments — vendor selection, vendor management, and understanding how the service organization's controls interact with their own. (The testimony notes SOC 2 is considered a standard instrument of third-party risk management.) Use of a SOC 2 report is restricted to parties who understand it (user entities and their auditors); the general-use sibling is SOC 3.

### Walkthrough (worked case): scoping criteria for a fictional SaaS company
Fictional "ExampleCo": multi-tenant project-management SaaS; stores customers' project data; contracts promise 99.9% monthly uptime; bills customers by monthly invoice generated from usage metering; customers' MSAs designate their project data confidential; the privacy notice commits to deleting personal data on request.

The reader writes a scoping memo — one decision per criterion, with reasoning:

| Criterion | In scope? | Reasoning |
|---|---|---|
| Security | Yes — always | Mandatory; it's the common criteria |
| Availability | Yes | Uptime is a contractual commitment (99.9% SLA); customers will test this claim |
| Processing integrity | Yes | Usage metering → invoicing must be complete, accurate, authorized; customers pay based on it |
| Confidentiality | Yes | Customer project data is contractually designated confidential |
| Privacy | Yes, but narrowly | The privacy notice makes commitments (deletion on request); scope covers only personal-information handling the company committed to — not a general GDPR assessment |

Success test: each "yes" cites a *specific commitment* (contract clause, SLA, privacy notice) — never "we chose it to look thorough." Each "no" would need the same treatment (which commitment is absent). The memo also states the report type recommendation (Type II, with why) and the examination period the company must sustain.

Where it goes wrong: scoping all five criteria "to be safe" and then failing the privacy criteria you never needed; writing the system description to match the marketing site instead of reality; confusing SOC 2 (operational/data controls, CPA opinion) with SOC 1 (financial-reporting controls); treating Type I as "the easy version of Type II" rather than a different assurance.

### Prove it (artifact)
A SOC 2 scoping memo for the fictional SaaS company: criteria decisions with commitment-based reasoning, Type I/II recommendation, and a list of the evidence each in-scope criterion will demand. Claim: "I can scope a SOC 2 engagement and explain each criterion choice." Cannot claim: ability to perform the examination (that requires a CPA).

### Read the source
The AICPA testimony PDF (M. Blanco-Best, AICPA Associate Director for Attestation Methodology and Guidance, before the ERISA Advisory Council, July 18, 2022; hosted at dol.gov). Read: the SOC 2® section (what the examination enables, who requests reports and why), "SOC 2 Criteria" (Type 1 vs Type 2 definitions, the two criteria sets — 2018 Description Criteria and 2017 Trust Services Criteria — and the five categories), and the SOC for Cybersecurity contrast (useful for board-reporting conversations). Note the document's date: the TSC edition references (2017 criteria, 2022 points of focus, 2022 description guidance) postdate it in part — check the AICPA for anything newer before the lesson ships (logged as gap).

### Free resources (≤3)
1. The AICPA testimony PDF itself — the primary fetched source for this lesson's SOC 2 content. https://www.dol.gov/sites/dolgov/files/EBSA/about-ebsa/about-us/erisa-advisory-council/soc-1-2-cybersecurity-examinations.pdf
2. NIST CSWP 29 §4 (Informative References) — shows how Trust Services Criteria map to CSF outcomes; teaches the "same controls, different reporting languages" point.
3. *(Slot held open — see gaps: no aicpa.org primary page was fetched this session. Candidate: the AICPA's own SOC 2 overview page, to be fetched and verified before the lesson ships.)*

### Check yourself
1. A prospect asks for your SOC 2 and you send a Type I report from 14 months ago. What are the two problems with that?
2. Your SaaS has no uptime commitment anywhere — no SLA, no marketing claim. Should Availability be in scope? What changes if sales starts promising "always on" on calls?
3. Why is a SOC 2 report "restricted use" while a SOC 3 can be posted publicly? What does that imply about what goes in each?
4. Your system description says "all changes require peer review," but the auditor samples five changes and two have none. Is this a Type I problem, a Type II problem, or both? Explain.
5. A customer asks: "Are you SOC 2 *certified*?" What is the precise correction, and why does the distinction matter to them?

### Leads to
Lesson 4 (running the program that keeps the controls operating between audits — the thing Type II actually tests).

---

## Lesson 4 — Running a security program: strategy, metrics, board communication

### Where this shows up
Someone has to turn frameworks into a functioning program: set direction, know whether it's working, and explain it to people who don't read firewall logs. That someone is the security program lead — the candidate role this lesson feeds. The GRC analyst supports it with the register and the reporting pack.

### Before you start (prerequisites)
- Lessons 1–3 (CSF, ISO 27001, SOC 2).
- The Stage E risk-assessment lesson (SP 800-30): the register below is its direct application.

### How it works
**Strategy.** A security program starts in Govern: leadership establishes the risk management strategy, states risk appetite and tolerance, assigns accountability, and folds cyber risk into enterprise risk management. CSF 2.0 §5 is explicit about the mechanism — a *bidirectional flow*: executives set priorities and communicate expectations about risk appetite, accountability, and resources; managers build Target Profiles and action plans; practitioners implement, measure operational risk, and report back up. The program is that loop running continuously, not a project with an end date.

**Metrics.** Two primary sources anchor this:
- NIST SP 800-55 (Measurement Guide for Information Security; v1 *Identifying and Selecting Measures* and v2 *Developing an Information Security Measurement Program*, both final December 2024) gives the method: develop, select, prioritize, and validate measures — quantitative and qualitative — with attention to documentation, reporting, data quality, and uncertainty, then run them as a program with defined roles and communication.
- CSF 2.0 §5.1 names the two metric families practitioners owe their leadership: **key performance indicators (KPIs)** — how well the program's activities are performing (e.g., control coverage, patch latency, training completion); and **key risk indicators (KRIs)** — the level of exposure itself (e.g., number of critical risks above tolerance, unpatched internet-facing systems, mean time to detect). The distinction: KPIs measure the *program's work*; KRIs measure the *risk's size*. A program can have excellent KPIs and terrible KRIs (busy but exposed) — that sentence is the whole point of reporting both.

**Operational vs. board-level metrics.** Operators need diagnostic detail (which systems, which vulnerabilities, trend lines). The board needs *decisions*: posture vs. target, top risks in business-impact language, what changed since last time, and what leadership must approve (fund, accept, or direct). CSF 2.0 §5.2 adds the translation rule: express cybersecurity in general risk-management language executives already use, and integrate it with the enterprise risk picture (financial, operational, reputational) rather than presenting cyber as a separate universe.

**No invented statistics.** The lesson states this as a hard rule with a reason: a metric nobody measured is worse than no metric — it teaches leadership to trust numbers that aren't real. Every figure in the board pack traces to a named source (tool output, register, audit result). The worked memo below uses labeled placeholders, never fabricated values.

### Walkthrough, part A: risk register (SP 800-30 concepts)
Same fictional ExampleCo. SP 800-30 Rev. 1 (Sept 2012) structures assessment as: **prepare** (scope, method, inputs), **conduct** (identify threat sources and events, identify vulnerabilities and predisposing conditions, determine likelihood and impact, determine risk level), **communicate** results, **maintain** the assessment over time. Its appendices supply working materials: a threat-source taxonomy (App. D), threat-event examples (App. E), and a risk-assessment report template — executive summary plus detailed body — (App. K).

The reader builds this register (qualitative Low/Moderate/High scale, defined once at the top of the document):

| ID | Risk statement (threat source → event → vulnerability → impact) | Likelihood | Impact | Level | Response | Owner | Status |
|---|---|---|---|---|---|---|---|
| R-01 | Phishing crew → credential theft → no MFA on admin consoles → full customer-data exposure | M | H | High | Mitigate: enforce MFA (PR.AA), phishing-resistant for admins | IT lead | In progress |
| R-02 | Ransomware affiliate → encryption of file shares → backups untested → extended outage | M | H | High | Mitigate: quarterly restore tests; Accept residual after test passes | IT lead | Open |
| R-03 | Admin error (non-adversarial) → public S3-style bucket → no config baseline → customer-data exposure | M | H | High | Mitigate: config baseline + automated drift check | Cloud eng | Open |
| R-04 | Software supplier → compromised update → no supplier assessment → malicious code in production | L | H | Moderate | Transfer where possible (contract terms) + Mitigate: supplier review for critical suppliers | Founder | Open |
| R-05 | Departure of sole admin (non-adversarial) → loss of access/knowledge → no succession → cannot recover systems | M | M | Moderate | Mitigate: document + cross-train; break-glass accounts | Founder | Open |
| R-06 | Unpatched internet-facing app → exploitation → 45-day patch lag → defacement/data theft | H | M | High | Mitigate: 14-day patch SLA for internet-facing | IT lead | Open |

Responses use the vocabulary CSF 2.0 §5 gives: mitigate, transfer, avoid, or accept negative risks (and the lesson notes the positive-risk side — realize, share, enhance, accept — exists but is out of scope for this register). Each row's response must name a concrete action, not just the verb.

Success test: every risk traces threat source → event → vulnerability without gaps; likelihood/impact use the register's defined scale; no row says "mitigate" without saying *how*; the register has an owner and a review date (maintenance is part of the method, per SP 800-30).

### Walkthrough, part B: one-page board memo
The reader converts the register and the CSF profile into a single page a non-technical director can act on. Skeleton (placeholders in brackets — the lesson forbids inventing the numbers):

> **To:** Board of Directors · **From:** Security program lead · **Date:** [date] · **Subject:** Cybersecurity posture and decisions required
>
> **1. What we protect and why it matters.** [One line: customer data and service availability; breach or outage means (contractual/regulatory/revenue consequence in plain words).]
> **2. Where we stand.** Current profile ~Tier [n]; target Tier [n]. [One sentence on the gap that matters most.]
> **3. Top risks.** [Three bullets max, each: business impact first, technical cause second. E.g., "Extended outage of customer service if backups fail — restore has never been tested (R-02)."]
> **4. What changed since last quarter.** [KRI movements with sources: e.g., "High risks above tolerance: [n] → [n] (risk register); mean time to patch internet-facing systems: [n] days (vulnerability scans)."]
> **5. Decisions required.** [Numbered asks: "Approve [amount-less description, e.g., 'managed backup testing'] to close R-02" / "Formally accept residual risk R-04 until supplier review completes" / "Direct [x]".]
> **Appendix (half page):** KPI/KRI definitions used above and where each number came from.

Success test: a director who reads only sections 3 and 5 can state the top risk and the decision needed; no acronym goes undefined; every number has a source label.

Where it goes wrong: reporting activity instead of risk ("we blocked 10,000 attacks" — blocked attacks are a KPI at best, and usually just noise); burying the ask; presenting the register's raw table as the memo; letting metrics drift from their definitions (data quality and uncertainty are SP 800-55 v1 topics for a reason).

### Prove it (artifacts)
1. A risk register (≥6 risks) built on SP 800-30 concepts, with defined scale, responses, owners, and review date.
2. A one-page board memo with labeled placeholders and sourced metric definitions.
Claim: "I can maintain a risk register and brief leadership on posture, risk, and decisions." Cannot claim: executive experience or authority to accept risk on a company's behalf.

### Read the source
- NIST CSWP 29 §5 (Improving Cybersecurity Risk Communication and Integration) — the bidirectional exec/manager/practitioner flow, KPI/KRI mention, ERM integration, and the IR 8286 / SP 800-221 companion list for deeper study.
- NIST SP 800-30 Rev. 1 — §1 (purpose), §3 (the process: prepare / conduct / communicate / maintain), Appendices D (threat sources), E (threat events), J (risk level determination), K (report template).
- NIST's SP 800-55 release page (Dec 4, 2024) — what v1 (selecting measures) and v2 (measurement program) cover; follow its links to the volumes for the full method.

### Free resources (≤3)
1. NIST CSWP 29 (CSF 2.0) §5 + Appendix B — the communication model and Tier language, free. https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=957258
2. NIST SP 800-30 Rev. 1 (free PDF) — the risk assessment method and report template. https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=912091
3. NIST SP 800-55 release page (Dec 2024) — v1/v2 scope; links to both free volumes. https://WWW.NIST.GOV/news-events/news/2024/12/measurement-guide-information-security-nist-releases-volumes-1-and-2-sp-800

### Check yourself
1. Your KPIs are all green and your KRIs are getting worse. Explain how that is possible, and what you tell the board.
2. A director asks "are we secure?" Why is that the wrong question, and what three-part answer does the memo structure give instead?
3. Your risk register lists "hackers" as the threat source for every row. What does SP 800-30's threat-source thinking require you to add, and why does it change the responses?
4. The board wants a single "security score." Argue for or against it using the Tier concept and the KPI/KRI distinction.
5. You inherit a register where every risk is marked "Mitigate" with no action named. What is the minimum you must add to each row before it is usable, and why?

### Leads to
The Stage E capstone path: a full program plan for a real (authorized) small organization — profile, register, measurement plan, and board pack — as the level-4 artifact.

---

## Key sources (all fetched 2026-10-09)

| # | Claim(s) it supports | Primary URL | Fetched | Status |
|---|---|---|---|---|
| 1 | CSF 2.0 identity (NIST CSWP 29, Feb 26 2024, authors Pascoe/Quinn/Scarfone); outcome-taxonomy nature; Profiles/Tiers definitions; §5 communication model; KPI/KRI mention; risk-response vocabulary | https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=957258 (via https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) | 2026-10-09 | verified |
| 2 | CSF 2.0 structure counts: 6 Functions, 22 Categories (Table 1, App. A), 106 Subcategories (counted from the appendix listing) | same as #1 | 2026-10-09 | verified |
| 3 | Tier names and progression: Tier 1 Partial, Tier 2 Risk Informed, Tier 3 Repeatable, Tier 4 Adaptive ( §3.2 + App. B) | same as #1 | 2026-10-09 | verified |
| 4 | ISO/IEC 27001:2022 identity (Ed. 3, 2022-10, ISO+IEC JTC 1/SC 27); ISMS purpose (risk-aware, people/policies/technology, CIA); certification voluntary via accredited bodies | https://www.iso.org/standard/27001 | 2026-10-09 | verified |
| 5 | Annex A: 93 controls in four themes — organizational, people, physical, technological (2022 revision); ongoing ISMS processes (plan on risk, train, monitor, audit, improve) | https://help.iso.org/en/articles/376290-iso-iec-27001-information-security-management-systems | 2026-10-09 | verified |
| 6 | SOC 2: examination engagement by CPA against Trust Services Criteria; Type 1 (design, point in time) vs Type 2 (design + operating effectiveness over period, incl. test descriptions/results); the five TSC categories; 2017 TSC / 2022 points of focus / 2018 description criteria; who requests reports and why (customers/business partners: vendor selection, vendor management, risk assessment); SOC 2 restricted use vs SOC 3 general use | https://www.dol.gov/sites/dolgov/files/EBSA/about-ebsa/about-us/erisa-advisory-council/soc-1-2-cybersecurity-examinations.pdf (AICPA-authored testimony: M. Blanco-Best, AICPA Assoc. Director, Attestation Methodology and Guidance, ERISA Advisory Council, 2022-07-18) | 2026-10-09 | verified |
| 7 | SP 800-30 Rev. 1 identity (Sept 2012, Ross); process = prepare / conduct / communicate results / maintain; App. D threat sources, App. E threat events, App. J risk levels, App. K report template (exec summary + body) | https://www.nist.gov/publications/guide-conducting-risk-assessments and https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=912091 | 2026-10-09 | verified |
| 8 | SP 800-55 v1 (Identifying and Selecting Measures) + v2 (Developing an Information Security Measurement Program), final Dec 4 2024; v1 covers quantitative/qualitative assessment, data analysis, impact/likelihood modeling, documentation/reporting/data quality; v2 covers program workflow, roles, measures communication | https://WWW.NIST.GOV/news-events/news/2024/12/measurement-guide-information-security-nist-releases-volumes-1-and-2-sp-800 | 2026-10-09 | verified |

Notes on primary-source choice: the ISO 27001 document itself is paid (one line, per brief §7); structure taught from ISO's own free pages (#4, #5). The AICPA Trust Services Criteria publication is likewise an AICPA publication; this dossier used AICPA-authored testimony (#6) rather than the criteria text — see gaps.

## Gaps

1. **No aicpa.org fetch for SOC 2.** Searches returned no usable aicpa.org URL for the SOC 2 / Trust Services Criteria pages, so Lesson 3's primary source is AICPA-authored testimony hosted on dol.gov. Before the lesson ships: fetch the AICPA's own SOC 2 overview page and confirm the TSC edition references (2017 criteria, 2022 points of focus, 2022 description-criteria guidance) are still current — the testimony is from July 2022 and its edition references may have been superseded.
2. **ISO 27001 certification lifecycle unverified.** ISO's page confirms certification is voluntary and done by accredited bodies, but certificate duration, surveillance-audit cadence, and Stage 1/Stage 2 audit structure were not verified on a primary source. Do not state them in the lesson until verified (likely via ISO/IEC 17021 or an accreditation body's public documents — secondary until confirmed).
3. **Lesson 2's third free resource unverified.** The CSF 2.0 Reference Tool / Informative References mapping ISO 27001 ↔ CSF outcomes is named in CSWP 29 §4 but was not fetched this session. Verify the tool URL before listing it as a resource.
4. **Clause 4–10 paraphrase basis.** The clause-by-clause plain-language summary is my paraphrase of the standard's well-known structure, cross-checked against ISO's free pages — but the paid standard text itself was not read (per brief §7, correctly). Flag for the lesson reviewer: confirm the paraphrase against the Online Browsing Platform preview if accessible.
5. **Counts method.** The 106-subcategory count was produced by counting the appendix listing in the fetched PDF (Govern 31, Identify 21, Protect 22, Detect 11, Respond 13, Recover 8). The machine-readable Core (Reference Tool) is the cleaner verification; re-verify from it before the lesson ships.
6. **SP 800-55 volumes not read.** Only NIST's release page was fetched (scope of v1/v2 confirmed); the volumes themselves were not read. The lesson's metrics guidance beyond the release-page summary needs the volumes fetched before writing.
7. **No invented numbers anywhere in this dossier.** The worked cases use qualitative scales (Low/Moderate/High) and labeled placeholders — this is intentional per the brief's ban on invented statistics. The lesson must keep it that way.
