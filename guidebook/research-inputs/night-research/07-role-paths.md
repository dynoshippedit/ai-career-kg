# Night research 07 — Role paths + NICE mapping + site conventions
Fetched 2026-10-09. Brief-governed: no prices, fees, salaries, or time estimates. Gaps logged at the end.

---

## 1. The eight role paths

Each path: ordered lesson sequence by stage (lesson topics use the brief's scope names; lesson IDs come from Phase 1's map.md), checkpoints, and a level-4 capstone (original work, made public). Difficulty and feeder-route notes are corrected against each live role page.

### Path 1 — SOC Analyst (`/r/soc-analyst/`)
**The job (per role page):** watch alerts, decide which matter, investigate the ones that do. Shift-based entry point; usually reached via IT support or networking, not straight off the street. Suits people who enjoy investigation and clear write-ups.
**Sequence:**
- Stage A (foundations, standard depth; lighter on cryptography internals): Linux, networking at packet level, HTTP in depth, Python for tooling, reading logs.
- Stage B — defensive basics: authorization/scope hard rules, SOC triage workflow, reading SIEM alerts, alert logic. Web vulnerability classes at Recognize/Operate level (know what the alerts mean, not full exploitation).
- Stage D — DFIR and detection: MITRE ATT&CK as vocabulary, NIST SP 800-61 incident handling, detection engineering (Sigma rules), threat hunting hypotheses.
**Checkpoints:** (1) triage a set of simulated alerts with written dispositions; (2) home SOC lab producing three documented investigation write-ups; (3) a detection rule written, deliberately triggered, with documented blind spots.
**Capstone (L4):** publish a detection-engineering project — e.g., a Sigma rule package for one ATT&CK technique with test evidence and a written investigation of a simulated intrusion mapped to ATT&CK, reproducible by a stranger.
**Credential link:** Security+ page on the site (role page names it as the entry credential); say nothing about cost.

### Path 2 — Security Analyst (`/r/security-analyst/`)
**The job (per role page):** work out what an attacker did or is doing, and write it up so someone can act. Broader analysis role; the SOC page is the shift-based entry, this is the wider remit. ATT&CK vocabulary and CISA advisories are the core reading diet.
**Sequence:**
- Stage A (standard).
- Stage B: methodology (WSTG awareness, PTES phases), defensive basics, web vulnerability classes to Apply level for the common ones (analysts must understand exploitation to analyze it).
- Stage C (lighter than the pentester's): coordinated disclosure awareness, how CVE records and CVSS scores are produced and read, write-ups that teach. Full CVE pursuit is optional, not required.
- Stage D — DFIR and detection: as SOC Analyst, plus threat-brief writing from real advisories.
**Checkpoints:** (1) an investigation of a simulated incident written up in ATT&CK vocabulary; (2) a detection rule written and tested; (3) a one-page threat brief from a current CISA advisory for a non-technical manager.
**Capstone (L4):** publish original threat analysis — e.g., a technique deep-dive with detection logic and test evidence, or a detection pack derived from a real advisory series.
**Correction vs brief's guess:** the brief lists "A, B, C, D DFIR and detection." Kept, but Stage C is disclosure literacy and write-up craft here, not CVE-chasing; the role page's proof artifacts are investigations, detections, and briefs.

### Path 3 — Penetration Tester (`/r/pentester/`)
**The job (per role page):** break in with written permission and explain exactly how. Open without a degree; rarely entry-level — arrivals come from help desk, networking, sysadmin, or defensive security. The report is the hardest part. Opens with a written-authorization notice (keep that convention in every hands-on lesson).
**Sequence:**
- Stage A (full depth, including cryptography — needed for auth attacks).
- Stage B (full): authorization/scope hard rules; methodology (OWASP WSTG, PTES, NIST SP 800-115); the 15-phase toolbench in activation order; web vulnerability classes wave 1 (IDOR, broken access control, SQLi, command injection, API abuse, SSRF, XSS, CSRF, logic flaws) then wave 2 (auth flaws, SSTI, XXE, deserialization, JWT/OAuth flaws, GraphQL, race conditions); local practice targets; reporting.
- Stage C (full): coordinated disclosure end to end; CVE program (structure, CNAs, requesting an ID, record format, credit); NVD and where enrichment data comes from now; CVSS v3.1 and v4.0 scored by hand; CWE/CAPEC/KEV/EPSS; write-ups that teach.
- Stage D — red team operations, then exploit development basics.
**Checkpoints:** (1) PortSwigger Web Security Academy core labs complete; (2) first valid finding submitted to an authorizing program; (3) a full pentest report on a lab target with business-impact statements and a rules-of-engagement record.
**Capstone (L4):** publish original work — e.g., a coordinated disclosure with CVE credit, a novel technique variation write-up, or a meaningful open-source tool contribution.

### Path 4 — AppSec Engineer (`/r/appsec/`)
**The job (per role page):** stop vulnerabilities from being written rather than finding them after they ship. Two disciplines (code + security); not entry-level — the common route is development first, then a deliberate turn to security.
**Sequence:**
- Stage A: HTTP in depth (auth, sessions, TLS), reading code (JavaScript, SQL) to fluency, cryptography. **Correction vs brief's guess:** the role page insists code fluency comes first — the path must front-load code reading/writing before security content, or the security layer means nothing.
- Stage B: vulnerability classes studied from the fix side (how each is found AND how it is fixed); source analysis; dependency/secret scanning.
- Stage D — AppSec: threat modeling methodologies, SAST/DAST/IAST/SCA, secure SDLC integration, code review technique.
- Stage E — CISSP Domain 8 (Software Development Security).
**Checkpoints:** (1) a threat model for something the reader built; (2) SAST integrated into a real pipeline with findings triaged; (3) a security fix responsibly disclosed and merged into real code.
**Capstone (L4):** publish a merged security fix in a real open-source project with a teaching write-up, or an original secure-design guide others can verify.

### Path 5 — DFIR (`/r/dfir/`)
**The job (per role page):** reconstruct what happened after a breach in enough detail that it stands up later — findings may enter a legal process. Evidence handling decides admissibility. **Correction vs brief's guess:** the role page says this is "essentially always entered from a SOC or security analyst role" — a step up from SOC, not a first job. The path therefore routes THROUGH the SOC Analyst or Security Analyst path first; it does not start at Stage A directly.
**Sequence:**
- Prerequisite: complete the SOC Analyst path (or Security Analyst path).
- Stage D — DFIR and malware analysis: forensic artifact categories (disk, memory, network), IR lifecycle per current NIST SP 800-61, threat hunting, detection engineering (Sigma, YARA), chain-of-custody practice, report writing for non-technical readers (lawyers, executives, regulators).
**Checkpoints:** (1) a timeline reconstructed from lab logs or a disk image; (2) a memory-forensics exercise with documented findings; (3) a chain-of-custody record maintained across an exercise; (4) an incident report written for non-technical readers.
**Capstone (L4):** publish a full forensic case study from a simulated breach — timeline, evidence-handling notes, findings, and an executive report, all reproducible.

### Path 6 — Cloud Security Engineer (`/r/cloud-security/`)
**The job (per role page):** keep the unwatched cloud account from being the way in. In real demand; not entry-level — **correction vs brief's guess:** the usual route is cloud or DevOps work first, then a turn toward security. The path must therefore include a genuine cloud-platform fluency block before cloud security content; "A, D cloud" alone undersells it.
**Sequence:**
- Stage A: Linux, networking, HTTP.
- Cloud fluency block (new; sits before security): core services of one major cloud, IAM model, networking, logging — learned in the reader's own account with billing alarms set (role page's warning, keep it).
- Stage D — cloud security: IAM deep dive, the most common real-world misconfigurations, Well-Architected security pillars (AWS and GCP), preventive/detective guardrails (policy-as-code, posture scanning).
- Stage E — CISSP Domain 3 (Security Architecture and Engineering) and Domain 5 (IAM).
**Checkpoints:** (1) a misconfiguration found and fixed in the reader's own lab account, with before/after and recurrence prevention; (2) least privilege applied to a working setup end to end; (3) an automated guardrail that fails a deployment reintroducing the problem.
**Capstone (L4):** publish a cloud security baseline — e.g., an audited reference architecture with detective controls, or original research on a misconfiguration class with detection logic.

### Path 7 — IAM Engineer (`/r/iam-engineer/`)
**The job (per role page):** decide who can do what; stop privilege quietly accumulating. Steadier than it sounds; common route is help desk or sysadmin where the reader already administered accounts. Much of the work is audit-driven.
**Sequence:**
- Stage A: HTTP authentication (Basic, Bearer, JWT, OAuth 2.0/OIDC), cryptography (hashing, signatures, PKI).
- Stage E — CISSP Domain 5 (Identity and Access Management): provisioning/deprovisioning, authentication models, authorization models (RBAC, ABAC), identity lifecycle, access review.
- Stage D — cloud IAM: AWS IAM policies/roles deep dive; directory concepts; federation/SSO.
**Checkpoints:** (1) a permissions audit of a lab environment with written removal rationale; (2) least privilege applied end to end with breakage notes; (3) a joiner-mover-leaver process document.
**Capstone (L4):** publish an IAM reference others can run — e.g., a least-privilege policy library for a common stack with rationale per policy, or an access-review methodology with a worked example.

### Path 8 — GRC Analyst (`/r/grc-analyst/`)
**The job (per role page):** turn a security standard into things the organisation actually does, and prove it did them. The most reachable security role for non-technical backgrounds (audit, admin, project, legal transfer in). Less hands-on; written artifacts carry the role.
**Sequence:**
- Stage A (lighter, conceptual): enough networking/HTTP/crypto vocabulary to read a control intelligently — no packet labs.
- Stage E — CISSP Domains 1 (Security and Risk Management), 2 (Asset Security), 6 (Security Assessment and Testing).
- Governance frameworks: NIST CSF 2.0, ISO/IEC 27001 (paid document — one line saying so, teach from free equivalents), SOC 2.
- AI governance: the AIGP subject area.
**Checkpoints:** (1) a control mapped to evidence (one control, exact evidence); (2) a risk written so a director can decide on it — one page, no jargon; (3) a policy a real employee could follow without asking questions.
**Capstone (L4):** publish a complete GRC work product — e.g., a risk assessment of a fictional company, a control implementation guide, or an audit plan, written to be used.
**Note:** if CISSP itself is referenced, state once that full certification needs five years of cumulative experience in two or more domains (degree or approved credential can substitute one year); passing without it makes someone an Associate of ISC2.

---

## 2. NICE Framework mapping (current categories)

The brief's 2026-10-09 check at NIST stands: version 2.0.0 has **five** Work Role Categories. Corroborated tonight by a v2.0-based third-party implementation (5 categories, 41 work roles; category codes OG, DD, IO, PD, IN) and by NIST's own work-role video library, which tabs the same five names. The old seven-category names (Securely Provision, Operate and Maintain, Analyze, Collect and Operate) are retired from the workforce framework; several removed defense-specific roles moved to the DCWF.
GAP: NIST's components file itself could not be re-fetched from this session (fetch failed twice); category names/IDs below follow the brief's NIST check plus corroboration. Take exact work-role IDs from NIST's components file at build time.

- **Oversight and Governance (OG)** — leadership, policy, strategy. Work roles include Executive Cybersecurity Leadership, Cybersecurity Management, Cybersecurity Policy and Planning, Cybersecurity Legal Advice, Cybersecurity Workforce Management, Communications Security (COMSEC) Management.
- **Design and Development (DD)** — architecture and building secure systems/software. Work roles include Security Architect, Systems Security Architecture, Software Development, OT Cybersecurity Engineering (new in 2.0.0).
- **Implementation and Operation (IO)** — deploying and running systems. Work roles include Systems Administration, Network Services, Systems Analysis.
- **Protection and Defense (PD)** — defending against threats. Work roles include Cyber Defense Analyst, Cyber Defense Infrastructure Support Specialist, Cyber Defense Incident Responder, Cyber Defense Forensics Analyst, Security Control Assessor, Vulnerability Analyst, Insider Threat Analysis.
- **Investigation (IN)** — analyzing incidents and threats. Work roles include Cyber Investigation, Digital Evidence Analysis.

### Stage → NICE mapping
- **Stage A** → IO (Systems Administration, Network Services). Foundations are operations work.
- **Stage B** → PD (Cyber Defense Analyst for defensive basics; Vulnerability Analyst and Security Control Assessor for testing) and IO (tooling administration).
- **Stage C** → PD (Vulnerability Analyst — disclosure and assessment; Security Control Assessor). The CVE/CVSS/CWE body of knowledge sits here.
- **Stage D** → track-dependent: red team → no direct NICE work role (offensive roles such as Exploitation Analysis moved to the DCWF in v2.0.0 — say so plainly); DFIR → IN (Cyber Investigation, Digital Evidence Analysis) + PD (Cyber Defense Incident Responder, Cyber Defense Forensics Analyst); AppSec → DD (Security Architect, Software Development); exploit dev → DD at best fit, no direct role; malware analysis → IN/PD forensics roles; cloud security → IO + DD (Security Architect); AI security → no NICE work role yet (gap to note on the page).
- **Stage E** → OG (Executive Cybersecurity Leadership, Cybersecurity Management, Cybersecurity Policy and Planning) + DD (Security Architect).

---

## 3. Candidate roles the site doesn't have yet

The brief says don't create role pages; list candidates at Stop 1. One line each on what the path would need:
- **Red team operator:** A → B → C → D red team; adversary emulation (ATT&CK, Atomic Red Team), C2 concepts taught defensively with detection, purple teaming; proof is emulation plans and reports; note NICE has no direct work role for it.
- **Exploit developer:** A → B → D exploit dev/RE; binary analysis, debugger fluency, modern mitigations; proof is original research and tooling; no NICE work role.
- **Malware analyst:** A → B defensive → D malware analysis; static/dynamic analysis, sandboxing, behavioral indicators; proof is published analyses; partially covered by IN/PD forensics roles.
- **AI security engineer:** A → B → D AI track (CAISP seven chapters, OWASP LLM Top 10 2025, MITRE ATLAS); proof is secured-AI-system write-ups; no NICE work role yet. MISMATCH: the brief lists this as a role the site doesn't have, but the SOC Analyst and Security Analyst pages both link an "AI Security Engineer" continuation — check whether that page exists before claiming it doesn't.
- **Security program lead:** A → E + OG; CISSP domains, NIST CSF 2.0, metrics, board communication; maps to NICE OG roles (Executive Cybersecurity Leadership, Cybersecurity Management).

---

## 4. Site conventions (for the build phase)

**Role page structure** (`/r/<role>/`): family tag (Cybersecurity) → one-line job description → "No degree needed" + difficulty → optional "Read this first" notice (authorization/legal/safety — pentester, appsec, dfir, cloud-security all carry one; keep the convention for every hands-on lesson) → "Can I actually do this?" (who it suits, feeder roles, honest difficulty) → "Also advertised as" → "The route": four stations in order — 1. Learn it free, 2. Attest strategically, 3. Prove it, 4. Get hired → "Where this route continues" → footer "This page last verified <date> · How we verify" with research notes.

**Free-status pills** (three-way split, never a bare "free"): "Free to learn · no certificate", "Free to learn · paid certificate", plus "Recognized" marker and "No credential needed" where nothing is named. Route cards say what is and isn't free on each card.

**Verification:** per-resource "Verified <date>"; page footer "This page last verified <date>"; research notes cite what was fetched and read (e.g., character counts). Method page rule: "No verification URL, no row" — "we could not verify this" is a legitimate result.

**Counts:** "Counts come from the data files, not from a hand-edited number." Homepage: 889 resources, 758 free, 17 credentials costed, 61 routes, 272 more credentials listed without full ledgers.

**Reasoning labeled as reasoning:** e.g., "That is our reasoning, not a hiring statistic we have verified." / "not a measured statistic about applicant pools."

**No salary estimates** published anywhere; the salary section explains why.

**Credential card format** (embedded in role pages): name, issuer, exam code → free pill → "The honest cost" table (cost / validity / renewal / assessment / proctored / verify-via / cost per active year) → assessment notes → "Read this before you buy" → "Verified <date> · Official page". NOTE: the guidebook project itself must not carry prices/fees — lessons link to the site's credential pages and say nothing about cost (brief §1).

**Directory** (`/x/`): 889 resources from 560 providers; verification tiers — checked date, *operator-added*, bot-wall/browser-only, *needs checking*. "Nothing here is padding — every row was reviewed by a person."

**Method page rules:** no verification URL no row; "free" always split three ways; costs show arithmetic; a badge is not a certification; retirements are first-class; no salary estimates; dates on everything.

**Guidebook additions per the brief:** lessons as data (one file each: stage, level 1–4, prerequisites, roles, map references, sources, test date); paths, maps, stage pages, and all counts generated from those fields; coverage as plain counts ("14 of the outline's objectives have a lesson"), never percentages; lesson format designed for reuse by other career families later.

---

## 5. Gaps
1. NIST NICE Framework components file could not be re-fetched from this session (two failed fetches); category names/IDs rest on the brief's 2026-10-09 NIST check plus a v2.0-based secondary source. Take exact work-role IDs from NIST's components file at build time.
2. Credential page URL pattern (`/c/<credential>/`) not confirmed — the one slug tried 404'd and the credential slug isn't indexed in search. Resolve from the repo, not by guessing.
3. "AI Security Engineer" page existence unresolved: brief says the site lacks it; two role pages link it as a continuation. Check the repo/live site before listing it as a candidate.
4. Lesson IDs don't exist yet — path sequences above use topic names; map to IDs in Phase 1's map.md.
5. No exact work-role numeric IDs asserted above (e.g., PD-WRL-001); only names and category codes, pending the components file.
