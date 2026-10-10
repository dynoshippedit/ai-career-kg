# map.md — lessons (pilot + Stage A + Stage A remainder + Stage B mechanics + Stage B vuln waves + Stage C + Stage E CISSP wave + AI track wave + Stage D wave 1 + AI completion/leadership)

| id | title | stage | level | prerequisites | roles served | map refs |
|---|---|---|---|---|---|---|
| `a-http-depth` | HTTP in depth | A (Foundations) | 3 — mechanism: explain every byte on the wire | Linux CLI basics; Python 3, curl | All roles (foundational); NICE: Implementation and Operation, Protection and Defense | Pre-map foundations; feeds CISSP 5.4 (via Stage B), CISSP 4.3 (via Stage E) |
| `b-idor` | IDOR: Insecure Direct Object References | B (Practitioner) | 3 — mechanism + live reproduction + fix verification | `a-http-depth`; B-AUTH (authorization discipline); two test accounts you own | Penetration Tester; Bug Bounty Researcher; NICE: Implementation and Operation | OWASP Top 10:2025 A01; WSTG-ATHZ-04; OWASP API Top 10:2023 API1 (BOLA twin); CISSP 5.4 (via Stage E) |
| `b-authorization-scope` | Authorization, scope, and the hard rules | B (Practitioner) | 2 — operate: every engagement inside written scope | Stage A complete; no tools | All roles (gating lesson); NICE: Oversight and Governance, Implementation and Operation | Brief §7 hard rules (verbatim); NIST SP 800-115 planning; 18 U.S.C. § 1030; Computer Misuse Act 1990 ss.1–3; feeds CISSP 1.9 (via Stage E) |
| `b-methodology` | Engagement methodology: WSTG, PTES, NIST SP 800-115 | B (Practitioner) | 2 — operate: follow the methodology on a prepared target | `b-authorization-scope`; Stage A | Penetration Tester; Security Analyst; NICE: Implementation and Operation | OWASP WSTG v4.2; PTES seven phases; NIST SP 800-115; feeds CISSP 1.9 (via Stage E) |
| `b-toolbench` | The toolbench: fifteen phases, one question each | B (Practitioner) | 2 — operate: answer each phase's question on a prepared target | `b-authorization-scope`; `b-methodology`; `a-http-depth`; `a-linux-cli` | Penetration Tester; Bug Bounty Researcher; NICE: Implementation and Operation | Fifteen tool phases in activation order (owner's catalog); feeds CISSP 5.4 (via Stage E) |
| `b-practice-targets` | Setting up practice targets locally | B (Practitioner) | 2 — operate: stand up and reset every target | `a-linux-cli`; Docker basics | All roles (foundational); NICE: Implementation and Operation | DVWA / Juice Shop / WebGoat / crAPI / DVGA READMEs; PortSwigger Academy; feeds all Stage B hands-on lessons |
| `e-risk-assessment` | Risk assessment as a worked case | E (Expert) | 3 — produce a complete, defensible assessment | Stage C vulnerability thinking; no CLI | Security Analyst; GRC / Governance roles; NICE: Oversight and Governance | **CISSP 1.9** (served directly); feeds CISSP 1.3, 1.7; NIST SP 800-30 Rev. 1; NIST CSF 2.0 Govern |
| `ai-prompt-injection` | Prompt injection, the #1 LLM risk | AI track | 3 — mechanism + demonstrated defense + detection | LLM app basics (`ai-01`); Stage B injection mindset; Python 3 (local model for live step) | AI Security Engineer; AppSec; NICE: Design and Development, Protection and Defense | **OWASP Top 10 for LLM Applications 2026, LLM01:2026**; MITRE ATLAS AML.T0051; CAISP ch. 3 (feeds ch. 5, ch. 7; NIST AI RMF) |
| `ai-llm-architecture` | How LLM applications are built and where they are attacked | AI track | 3 — mechanism + attack-surface mapping on your own app | `ai-prompt-injection`; Stage A Python/HTTP; Stage B injection mindset | AI Security Engineer; AppSec; NICE: Design and Development, Protection and Defense | **CAISP ch. 1–2**; MITRE ATLAS (tactics/techniques); feeds `ai-llm-top10`, `ai-supply-chain`, `ai-governance` |
| `ai-llm-top10` | The OWASP LLM Top 10 beyond prompt injection | AI track | 3 — mechanism + defense per risk + classification on unseen scenarios | `ai-prompt-injection`; `ai-llm-architecture` | AI Security Engineer; AppSec; NICE: Design and Development, Protection and Defense | **OWASP Top 10 for LLM Applications 2026, LLM02–LLM10:2026**; **CAISP ch. 3** |
| `ai-supply-chain` | AI supply chain security | AI track | 3 — mechanism + provenance verification + admission policy | `ai-llm-architecture`; `ai-llm-top10` (LLM04); `a-git-github` | AI Security Engineer; ML Platform; NICE: Design and Development, Protection and Defense | **OWASP Top 10 for LLM Applications 2026, LLM04:2026**; **CAISP ch. 6**; CycloneDX; Sigstore; SLSA |
| `ai-governance` | Governing AI | AI track | 2 — framework literacy + applied classification in a worked case | `ai-llm-top10`; `e-risk-assessment` | GRC Analyst; AI Security Engineer; NICE: Oversight and Governance | **CAISP ch. 7**; NIST AI RMF 1.0; NIST AI 600-1; EU AI Act (tiers as concepts); ISO/IEC 42001 (paid — one line) |
| `a-dns-depth` | DNS in depth | A (Foundations) | 3 — mechanism: read a DNS message field by field, trace the resolution chain | A terminal; `a-linux-cli` alongside for shell fluency | All roles (foundational); NICE: Implementation and Operation, Protection and Defense | Pre-map foundations; feeds Stage B (subdomain enum, DNS rebinding/SSRF), Stage E |
| `a-tcpip-ports` | TCP/IP and ports | A (Foundations) | 3 — mechanism: handshake/teardown, connection states, what a port guarantees | `a-dns-depth` | All roles (foundational); NICE: Implementation and Operation, Protection and Defense | Pre-map foundations; feeds `a-http-depth`, Stage B, Stage D network forensics |
| `a-linux-cli` | Linux command line for security work | A (Foundations) | 3 — operate: navigate, inspect, control a Linux system unaided | None (the bench everything runs on) | All roles (foundational); NICE: Implementation and Operation | Pre-map foundations; feeds every later lesson |
| `a-git-github` | Git and GitHub | A (Foundations) | 3 — operate: version work, collaborate, read history | `a-linux-cli` | All roles (foundational); NICE: Implementation and Operation | Pre-map foundations; the artifact pipeline for all stages |
| `b-sqli` | SQL injection: when your input becomes the query | B (Practitioner) | 3 — mechanism + live reproduction (3 families) + fix verification | `a-http-depth`; B-AUTH; SQL reading | Penetration Tester; AppSec Engineer; NICE: Implementation and Operation | OWASP Top 10:2025 A05; WSTG-INPV-05; CWE-89 |
| `b-command-injection` | OS command injection: when your input reaches a shell | B (Practitioner) | 3 — mechanism + live reproduction (incl. blind) + fix verification | `a-http-depth`; `a-linux-cli`; `b-sqli`; B-AUTH | Penetration Tester; AppSec Engineer; NICE: Implementation and Operation | OWASP Top 10:2025 A05; WSTG-INPV-13; CWE-78 |
| `b-ssrf` | SSRF: when the server fetches what you tell it to | B (Practitioner) | 3 — mechanism + live reproduction + fix verification | `a-http-depth`; `b-idor`; B-AUTH | Penetration Tester; Cloud Security; NICE: Implementation and Operation, Protection and Defense | OWASP Top 10:2025 A01; WSTG-INPV-19; CWE-918 |
| `b-csrf` | CSRF: when the victim's browser does the attacker's work | B (Practitioner) | 3 — mechanism + live reproduction + fix verification | `a-http-depth`; `b-idor`; B-AUTH | Penetration Tester; AppSec Engineer; NICE: Implementation and Operation | OWASP Top 10:2025 A01; WSTG-SESS-05; CWE-352 |
| `b-xss` | Cross-site scripting: when the browser can't tell your code from the attacker's | B (Practitioner) | 3 — mechanism + live reproduction (3 types) + fix verification | `a-http-depth`; Stage A JS reading; B-AUTH | Penetration Tester; AppSec Engineer; Bug Bounty Researcher; NICE: Implementation and Operation | OWASP Top 10:2025 A05; WSTG-INPV-01/02; CWE-79; feeds `ai-prompt-injection` |
| `b-business-logic` | Business-logic flaws: when the code works and the rules don't | B (Practitioner) | 3 — methodology + live workflow abuse + fix verification | `b-idor`; `b-sqli`; `b-xss`; B-AUTH | Penetration Tester; Bug Bounty Researcher; NICE: Implementation and Operation | OWASP Top 10:2025 A06; WSTG-BUSL; CWE-840/841; feeds Stage C disclosure |
| `b-session-auth` | Broken authentication and session management | B (Practitioner) | 3 — mechanism + local reproduction + fix verification | `a-http-depth`; `b-csrf`; B-AUTH | Penetration Tester; SOC Analyst; AppSec Engineer; NICE: Protection and Defense | OWASP Top 10:2025 A07; WSTG-ATHN; CWE-287/384; feeds SOC-analyst path |
| `b-security-headers` | Security headers and browser defenses | B (Practitioner) | 3 — mechanism + curl-verified deployment of every header | `a-http-depth`; `b-xss`; `b-csrf`; `b-session-auth` | AppSec Engineer; Penetration Tester; NICE: Implementation and Operation | OWASP Top 10:2025 A02; WSTG-CONF; CWE-693; closes `b-xss`/`b-csrf`/`b-session-auth` |
| `c-soc-triage` | SOC triage: from alert to decision | C (Professional) | 3 — triage workflow + live decision trees + classification discipline | `a-linux-cli`; `b-session-auth` | SOC Analyst; Detection Engineer; NICE: Protection and Defense | Stage C milestone skill; feeds `c-incident-response`; impossible-travel/beaconing trees |
| `c-log-sources` | Log sources that matter | C (Professional) | 3 — source selection + live parsing + blind-spot reasoning | `a-linux-cli`; `a-tcpip-ports` | SOC Analyst; DFIR; NICE: Protection and Defense, Investigation | NIST SP 800-92; feeds `c-sigma-detection`, `c-incident-response`; Stage B telemetry reread |
| `c-sigma-detection` | Writing detections with Sigma | C (Professional) | 3 — rule anatomy + live evaluation + tuning loop | `c-log-sources`; `c-soc-triage` | Detection Engineer; SOC Analyst; NICE: Protection and Defense | Sigma spec 2.x; ATT&CK tags; detection-as-code; feeds D-DFIR/detection track |
| `e-iam` | Identity and access management: who gets in, and to what | E (Expert) | 3 — lifecycle design + access review with decisions | `a-http-depth`; `a-linux-cli`; `b-session-auth`; no CLI | IAM Engineer; GRC Analyst; NICE: Oversight and Governance, Protection and Defense | **CISSP 5.1, 5.2, 5.3, 5.4, 5.5** (served directly); NIST SP 800-63; NISTIR 7316 |
| `e-crypto-applied` | Applied cryptography: what the primitives do, and how they break | E (Expert) | 3 — correct primitive use + cert-chain reading + misuse spotting | Stage A crypto concepts; `a-http-depth`; OpenSSL 3.x | Security Architect; AppSec Engineer; NICE: Design and Development | **CISSP 3.6** (served directly); NIST SP 800-57 Pt.1 Rev.5; RFC 5280; RFC 8446 |
| `e-sdlc` | Secure SDLC: catching the vulnerability before it ships | E (Expert) | 3 — threat model + gate review that change what ships | Stage B vuln classes; `e-risk-assessment`; no CLI | AppSec Engineer; Security Architect; NICE: Oversight and Governance | **CISSP 8.1–8.5** (governance level); NIST SP 800-218 (SSDF v1.1); feeds D-AppSec track |
| `e-bcp-drp` | Business continuity and disaster recovery: deciding what survives the outage | E (Expert) | 3 — BIA + tested recovery plan | `e-risk-assessment`; `c-incident-response`; no CLI | GRC Analyst; Security Analyst; NICE: Oversight and Governance | **CISSP 1.7, 7.10, 7.11, 7.12, 7.13** (served directly); NIST SP 800-34 Rev.1 |
| `c-cvd` | Coordinated vulnerability disclosure | C (Professional) | 3 — disclosure package + timeline + advisory, run end to end | Stage B (finding/proving); `b-methodology`; no CLI | Security Engineer; Bug Bounty Hunter; NICE: Oversight and Governance | Stage C milestone (half); CERT CVD guide; OpenSSF finder guide; feeds `c-cve-program` |
| `c-cve-program` | The CVE Program: IDs, CNAs, records, credit | C (Professional) | 3 — record autopsy + correct request path + credits JSON | `c-cvd`; JSON reading | Security Engineer; NICE: Oversight and Governance | Stage C milestone (half); cve.org; Record Format 5.2.0; 555 CNAs; feeds `c-cvss`, `c-vuln-ecosystem` |
| `c-cvss` | CVSS v3.1 and v4.0, scored by hand | C (Professional) | 3 — hand-score both versions + defend the vector | `c-cve-program`; comfort with arithmetic | Security Engineer; SOC Analyst; NICE: Protection and Defense | FIRST CVSS v4.0 (Base/Threat/Environmental/Supplemental); v3.1 equations; feeds `c-vuln-ecosystem` |
| `c-vuln-ecosystem` | CWE, CAPEC, KEV, EPSS — and where enrichment comes from now | C (Professional) | 3 — three-method prioritization, defended | `c-cvss`; `c-cve-program` | SOC Analyst; Security Engineer; NICE: Protection and Defense | CWE Top 25:2025; CISA KEV; EPSS; NVD prioritized-enrichment (OIG-26-020-I); feeds triage/detection |
| `c-incident-response` | Incident response basics | C (Professional) | 3 — IR lifecycle + worked report + containment reasoning | `c-soc-triage`; `c-log-sources` | DFIR; SOC Analyst; NICE: Protection and Defense, Investigation | **NIST SP 800-61 Rev. 3** (Apr 2025, CSF 2.0 Community Profile); feeds D-DFIR track |
| `d-redteam-concepts` | Red team operations: concepts | D (Specialist) | 2 — behavior language + tactic mapping + defender-view description; emulation is reader-side | `a-http-depth`; `a-tcpip-ports`; `c-soc-triage`; `c-log-sources`; B-AUTH | Red Teamer; Detection Engineer; NICE: Protection and Defense | **ATT&CK Enterprise v19.2** (15 tactics; Stealth TA0005 + Defense Impairment TA0112); Atomic Red Team (reader-side lab) |
| `d-malware-analysis` | Malware analysis: concepts | D (Specialist) | 3 — static triage workflow + YARA rule with false-positive testing; detonation is reader-side | `a-linux-cli`; `d-redteam-concepts`; `c-log-sources` | Malware Analyst; DFIR; NICE: Investigation | YARA 4.4.0 rule docs; FLARE VM + REMnux (reader-side isolated lab); feeds `c-sigma-detection` |
| `d-cloud-security` | Cloud security: concepts | D (Specialist) | 3 — responsibility classification + IAM policy analysis + posture audit workflow; live scan is reader-side | `a-tcpip-ports`; `b-ssrf`; `e-risk-assessment` | Cloud Security Engineer; Auditor; NICE: Implementation and Operation, Protection and Defense | AWS Shared Responsibility Model; Prowler + ScoutSuite (reader-side, own account); CIS Benchmarks |
| `a-python-security` | Python for security tooling | A (Foundations) | 3 — apply: read, adapt, write small tools unaided | `a-linux-cli`; `a-http-depth` | All roles (foundational); NICE: Implementation and Operation | docs.python.org tutorial; feeds `a-reading-code`, `b-toolbench`, all scripted walkthroughs |
| `a-reading-code` | Reading code through a vulnerability | A (Foundations) | 3 — apply: trace untrusted input source-to-sink in unfamiliar code | `a-http-depth`; `a-python-security`; `b-sqli` (recommended) | Penetration Tester; AppSec Engineer; Bug Bounty Researcher; NICE: Implementation and Operation | javascript.info; SQLBolt; feeds every Stage B web-vulnerability lesson |
| `a-windows-concepts` | Windows concepts for security | A (Foundations) | 2 — recognize + operate guided (hands-on not run by us; reader's VM reaches 3) | `a-linux-cli` (translation of its concepts) | SOC Analyst; DFIR; NICE: Implementation and Operation, Protection and Defense | Microsoft Registry Hives + Get-WinEvent docs (verified); feeds `c-log-sources`, `d-malware-analysis` |
| `a-osint-research` | OSINT and research discipline | A (Foundations) | 3 — apply: passive recon + re-derivable documentation | `a-http-depth`; `b-authorization-scope` (read first) | Penetration Tester; SOC Analyst; NICE: Implementation and Operation | OWASP WSTG information gathering; feeds `b-methodology` recon phase |
| `d-appsec` | Application security: concepts | D (Specialist) | 3 — STRIDE threat model + SAST triage + security code review; production scanner ops are reader-side | Stage B vuln classes; `a-http-depth`; `e-sdlc` | AppSec Engineer; Security Champion; NICE: Design and Development | **CISSP 8.1–8.5** (hands-on half; governance in `e-sdlc`); OWASP Threat Modeling Cheat Sheet (STRIDE); Semgrep/ZAP (reader-side) |
| `ai-pipeline` | AI attacks and defenses in the build pipeline | AI track | 3 — mechanism + pipeline hardening on your own build, each attack paired with its defense | `ai-supply-chain`; `ai-llm-architecture`; `a-git-github`; Python 3 | AI Security Engineer; ML Platform; NICE: Design and Development, Protection and Defense | **CAISP ch. 4** (served directly); **OWASP LLM Top 10:2026 LLM04/LLM05** (Supply Chain / Data and Model Poisoning — codes corrected 2026-10-09 against the official repo's final list); MITRE ATLAS (Training Data Poisoning, AI Supply Chain Compromise); SLSA |
| `ai-threat-modeling` | Threat modeling AI systems | AI track | 3 — complete, defensible threat model produced unaided; no CLI by design | `ai-llm-architecture`; `ai-llm-top10`; `ai-pipeline`; `e-risk-assessment` helps | AI Security Engineer; AppSec; NICE: Design and Development, Protection and Defense | **CAISP ch. 5** (served directly); MITRE ATLAS (TTP library); NIST AI RMF (MAP) |
| `e-security-program` | Running a security program | E (Expert) | 3 — complete, defensible program charter produced unaided; no CLI by design | `e-risk-assessment`; `e-sdlc`; `c-incident-response` | Security program lead (candidate role); GRC Analyst; NICE: Oversight and Governance | Brief §5 "Running a security program" (served directly); **CISSP Domain 1** (program level); NIST CSF 2.0; NIST SP 800-55 |
| `e-board-communication` | Board-level communication | E (Expert) | 3 — board-ready memo unaided, survives the director test; no CLI by design | `e-security-program`; `e-risk-assessment` | Security program lead (candidate role); GRC Analyst; NICE: Oversight and Governance | Brief §5 "Running a security program" (board communication, served directly); **CISSP Domain 1** (risk communication); NIST CSF 2.0 §5 |
| `e-csf-20` | NIST Cybersecurity Framework 2.0 | E (Expert) | 3 — scope and run a CSF gap assessment unaided: Current-vs-Target profile sketch + prioritized action plan; no CLI by design | `e-risk-assessment`; `e-governance` | GRC Analyst; Security Consultant; NICE: Oversight and Governance | Brief §5 "Governance frameworks" (served directly); NIST CSF 2.0 (CSWP 29, Feb 26 2024) |
| `e-iso27001` | ISO/IEC 27001 | E (Expert) | 3 — draft a risk-based control selection with a defensible Statement of Applicability unaided; no CLI by design | `e-csf-20`; `e-risk-assessment` | GRC Analyst; Security Consultant; NICE: Oversight and Governance | Brief §5 "Governance frameworks" (served directly); ISO/IEC 27001:2022 (paid — one line; taught from free equivalents) |
| `e-soc2` | SOC 2 and the Trust Services Criteria | E (Expert) | 3 — scope a SOC 2 engagement and read the report like a customer: criteria against commitments; no CLI by design | `e-csf-20`; `e-iso27001` | GRC Analyst; Security Consultant; NICE: Oversight and Governance | Brief §5 "Governance frameworks" (served directly); AICPA Trust Services Criteria 2017 (revised points of focus 2022) |
| `e-ethics` | Professional ethics in security work | E (Expert) | 2 — argue a security ethics dilemma from a professional code's canons, in writing, naming which canon decides | `ai-governance` | Security Consultant; GRC Analyst | **CISSP 1.1** (served directly); ISC2 Code of Professional Ethics; ACM Code of Ethics and Professional Conduct |
| `e-security-concepts` | Core security concepts: the CIA triad and the properties around it | E (Expert) | 2 — map a real system's security onto confidentiality, integrity, availability and the surrounding properties, and name the trade-offs between them | `a-http-depth`, `e-crypto-applied` | Security Architect; GRC Analyst | **CISSP 1.2** (served directly); RFC 4949, Internet Security Glossary Version 2; NIST CSRC Glossary |
| `e-governance` | Security governance: aligning security with business strategy | E (Expert) | 3 — draft a security governance charter that ties security decisions to business objectives, with roles, reporting lines, and a framework rationale | `e-risk-assessment`, `e-board-communication` | CISO; GRC Analyst | **CISSP 1.3** (served directly); NIST Cybersecurity Framework 2.0 (CSWP 29); ISACA COBIT framework overview |
| `e-cyber-law` | Legal, regulatory, and compliance: mapping obligations to evidence | E (Expert) | 3 — build an obligation-to-evidence map for a real regulatory regime: which obligations apply, what evidence each needs, who owns it | `e-risk-assessment`, `e-governance` | GRC Analyst; Security Consultant | **CISSP 1.4** (served directly); Regulation (EU) 2016/679 — General Data Protection Regulation; NIST Privacy Framework v1.0 |
| `e-investigations` | Investigation types: which investigation you're in, and what it demands | E (Expert) | 3 — run the investigation-type decision tree on a real incident: name the type, the authority, the evidence standard, and the one mistake to avoid | `c-incident-response`, `d-dfir-deep` | Incident Responder; GRC Analyst | **CISSP 1.5** (served directly); NIST SP 800-86, Guide to Integrating Forensic Techniques into Incident Response; DOJ Computer Crime and Intellectual Property Section (CCIPS) |
| `e-policy-docs` | Security policy, standards, procedures, and guidelines: the document hierarchy | E (Expert) | 3 — author a three-tier document set — policy, standard, procedure — for one control area, plus the guideline, with owners and review dates | `e-governance` | GRC Analyst; Security Architect | **CISSP 1.6** (served directly); NIST SP 800-53 Rev. 5, Security and Privacy Controls; SANS Information Security Policy Templates |
| `e-personnel-security` | Personnel security: the human side of the employment lifecycle | E (Expert) | 3 — produce a termination checklist and access-revocation runbook for a privileged departure, plus a travel-security briefing — with owners and timing for every action | `e-iam` | GRC Analyst; Security Manager | **CISSP 1.8** (served directly); NIST SP 800-53 Rev. 5, Personnel Security (PS) family; CISA Insider Threat Mitigation |
| `e-threat-modeling-concepts` | Threat modeling concepts and methodologies: choosing how to think about what can go wrong | E (Expert) | 3 — select a threat-modeling methodology for a given situation and justify the choice — strengths, limits, staffing, and what the output feeds | `e-sdlc`, `ai-threat-modeling` | Security Architect; Security Consultant | **CISSP 1.10** (served directly); Microsoft Threat Modeling documentation (STRIDE); OWASP Threat Modeling Cheat Sheet |
| `e-supply-chain-risk` | Supply chain risk management: trusting what you didn't build | E (Expert) | 3 — complete a vendor risk assessment for a real acquisition: risk factors, mitigations, and a residual-risk decision with owner and date | `e-risk-assessment`, `ai-supply-chain` | GRC Analyst; Security Architect | **CISSP 1.11** (served directly); NIST SP 800-161 Rev. 1, Cybersecurity Supply Chain Risk Management Practices; CISA ICT Supply Chain Risk Management |
| `e-awareness-training` | Security awareness, education, and training: building the learning program | E (Expert) | 3 — write a one-year security learning program plan — audience segments, topic calendar, phishing-simulation rules of engagement, effectiveness metrics — that a real organization could run | `c-soc-triage` | Security Manager; GRC Analyst | **CISSP 1.12** (served directly); NIST SP 800-50 Rev. 1, Building a Cybersecurity and Privacy Learning Program; CISA Cybersecurity Awareness Month resources |
| `e-asset-classification` | Classifying information and assets: the scheme everything else hangs on | E (Expert) | 3 — produce a classification scheme — tiers, examples, handling hooks, owners — that survives a review | `e-risk-assessment` | GRC Analyst; Data Protection Officer | **CISSP 2.1** (served directly); SANS Information Security Policy Templates; NIST SP 800-60 Vol. 2 Rev. 1 (appendices: information-type catalog) |
| `e-handling-requirements` | Handling requirements: what each classification tier demands | E (Expert) | 3 — write handling rules per tier — labeling, storage, transmission, disposal — and turn them into an enforceable matrix | `e-asset-classification` | GRC Analyst; Security Analyst | **CISSP 2.2** (served directly); NIST SP 800-88 Rev. 2 FAQ; SANS Information Security Policy Templates |
| `e-asset-provisioning` | Secure provisioning: ownership, inventory, and the CMDB | E (Expert) | 3 — design a provisioning workflow and run an inventory audit that reconciles | `e-asset-classification` | GRC Analyst; Security Architect | **CISSP 2.3** (served directly); SANS Data Inventory Management Policy template; SANS Information Security Policy Templates |
| `e-data-lifecycle` | The data lifecycle: from collection to destruction | E (Expert) | 3 — map five data types across the lifecycle and select destruction methods per SP 800-88 Rev. 2 | `e-asset-classification`, `a-linux-cli` | GRC Analyst; Data Protection Officer | **CISSP 2.4** (served directly); NIST SP 800-88 Rev. 2 FAQ; SANS Information Security Policy Templates |
| `e-retention-eol` | Retention schedules and end-of-life: when to let go, and how | E (Expert) | 3 — build a retention and destruction schedule with legal basis, and handle end-of-life systems securely | `e-data-lifecycle` | GRC Analyst; Data Protection Officer | **CISSP 2.5** (served directly); GDPR Article 5(1)(e), storage limitation; SANS Information Security Policy Templates |
| `e-data-protection-controls` | Data security controls: protecting data at rest, in transit, and in use | E (Expert) | 3 — select protective controls per data state, scope them to a requirement, and map them to compliance | `e-crypto-applied`, `e-asset-classification` | Security Architect; GRC Analyst | **CISSP 2.6** (served directly); OWASP Cryptographic Storage Cheat Sheet; OWASP Transport Layer Protection Cheat Sheet |
| `e-secure-design` | Secure design principles: engineering judgment before controls | E (Expert) | 3 — run an architecture review: apply each principle with pass/fail rationale, trace controls to requirements | `e-risk-assessment`, `d-appsec` | Security Architect; AppSec Engineer | **CISSP 3.1** (served directly); OWASP Security by Design Principles; Microsoft Learn: TPM fundamentals |
| `e-security-models` | Formal security models: what "secure" means, precisely | E (Expert) | 2 — state each model's rules, run the BLP rule check, and write a selection rationale for a scenario | `e-secure-design` | Security Architect; Security Engineer | **CISSP 3.2** (served directly); Purdue CS 526 handout 06: Integrity Protection; NIST Early Computer Security Papers (1970-1985) |
| `e-control-selection` | Selecting controls: from requirements to a defensible set | E (Expert) | 3 — derive requirements from a scenario, select and tailor controls with written rationale, and defend the omissions | `e-risk-assessment`, `e-secure-design` | Security Architect; GRC Analyst | **CISSP 3.3** (served directly); OWASP ASVS; MITRE ATT&CK |
| `e-platform-security` | Platform security: the ground your architecture stands on | E (Expert) | 3 — survey a platform's security capabilities and write a deployment recommendation with conditions | `e-secure-design`, `e-crypto-applied` | Security Architect; Platform Engineer | **CISSP 3.4** (served directly); Intel: Control-Flow Enforcement Technology; NIST SP 800-53 Rev. 5, SC family |
| `e-arch-vuln-assessment` | Assessing vulnerabilities across the architecture | E (Expert) | 3 — assess a hybrid architecture component by component, name the vulnerability classes per component, and write prioritized recommendations | `d-appsec`, `d-cloud-security`, `e-risk-assessment` | Security Architect; Security Engineer | **CISSP 3.5** (served directly); MITRE ATT&CK; NIST SP 800-53 Rev. 5 |
| `e-cryptanalysis` | Cryptanalytic attacks: how ciphers fail, and what that teaches | E (Expert) | 3 — compute key-space and birthday-bound estimates, demonstrate classical frequency analysis, and pair every attack method with its defense | `e-crypto-applied` | Security Engineer; AppSec Engineer | **CISSP 3.7** (served directly); OWASP Cryptographic Storage Cheat Sheet; NIST SP 800-115 |
| `e-facility-design` | Site and facility design: security before the first brick | E (Expert) | 3 — review a facility design against CPTED, layered defense, and site selection — findings with recommendations | `e-risk-assessment` | Security Architect; Physical Security Specialist | **CISSP 3.8** (served directly); NIST SP 800-53 Rev. 5, PE family; LAPD: Crime Prevention Through Environmental Design |
| `e-facility-controls` | Site and facility controls: the checklist that holds | E (Expert) | 3 — complete a facility controls checklist with findings, covering perimeter, access, environmental, power, and fire | `e-facility-design` | Security Engineer; Physical Security Specialist | **CISSP 3.9** (served directly); NIST SP 800-53 Rev. 5, PE family; FEMA: Risk Management |
| `e-system-lifecycle` | The information system lifecycle: security at every gate | E (Expert) | 3 — write a gate-review template with security deliverables per phase, and complete one gate review with a go/no-go decision | `e-secure-design`, `e-sdlc` | Security Architect; GRC Analyst | **CISSP 3.10** (served directly); SEBoK: System Life Cycle Process Models; NIST SP 800-53 Rev. 5 |
| `e-network-architecture` | Network architecture: drawing the lines attackers must cross | E (Expert) | 3 — design a segmentation scheme and defend every trust boundary in it | `a-tcpip-ports` | Security Architect; Network Security Engineer | **CISSP 4.1** (served directly); CISA: Layering Network Security Through Segmentation; CISA: Zero Trust Maturity Model |
| `e-network-components` | Network components: hardening everything the architecture trusts | E (Expert) | 3 — produce a component-hardening review with placement rationale for each control | `e-network-architecture`, `a-tcpip-ports` | Security Architect; Network Security Engineer | **CISSP 4.2** (served directly); NSA: Network Infrastructure Security Guidance (Mar 2022, mirrored PDF); CISA: Zero Trust Maturity Model |
| `e-secure-channels` | Secure channels: which encrypted path for which traffic, and why | E (Expert) | 3 — select and justify the communication channel for every traffic class in an architecture | `a-http-depth`, `e-network-architecture` | Security Architect; Network Security Engineer | **CISSP 4.3** (served directly); OWASP Transport Layer Protection Cheat Sheet; CISA: Layering Network Security Through Segmentation |
| `e-auth-systems` | Implementing authentication systems: the rollout, not the theory | E (Expert) | 3 — write and defend an authentication implementation and rollout plan | `e-iam`, `a-http-depth` | IAM Engineer; Security Architect | **CISSP 5.6** (served directly); FIDO Alliance: passkeys and WebAuthn explainers; OWASP Authentication Cheat Sheet |
| `e-assessment-strategy` | Assessment strategy: deciding what gets tested, by whom, and how often | E (Expert) | 3 — write an annual assessment strategy that covers the estate without gaps or waste | `b-methodology` | GRC Analyst; Security Analyst | **CISSP 6.1** (served directly); OWASP Web Security Testing Guide — the testing framework; CISA: Cyber Assessments |
| `e-control-testing` | Control testing: choosing the method that proves the claim | E (Expert) | 3 — select, scope, and sequence test methods for a control set — and say what each result proves | `b-methodology`, `e-assessment-strategy` | GRC Analyst; Security Analyst | **CISSP 6.2** (served directly); OWASP Web Security Testing Guide; CIS Benchmarks |
| `e-security-metrics` | Security metrics: measuring the program without lying to yourself | E (Expert) | 3 — specify a measurement program: definitions, data sources, collection method, cadence — for a real SOC | `c-soc-triage`, `c-log-sources` | GRC Analyst; SOC Analyst | **CISSP 6.3** (served directly); CIS Critical Security Controls; NIST Cybersecurity Framework (CSF) 2.0 |
| `e-test-analysis-reporting` | Test analysis and reporting: from ten thousand findings to decisions | E (Expert) | 3 — triage findings, rate risk honestly, and write a report that drives remediation | `c-cvss`, `b-methodology` | GRC Analyst; Security Analyst | **CISSP 6.4** (served directly); OWASP Web Security Testing Guide — reporting; CISA Known Exploited Vulnerabilities (KEV) catalog |
| `e-security-audits` | Security audits: independence, evidence, and the finding that holds up | E (Expert) | 3 — write an audit plan for a control family and execute it to a defensible finding | `e-assessment-strategy` | GRC Analyst; Security Analyst | **CISSP 6.5** (served directly); ISACA Now: ITAF 5th edition overview; NIST SP 800-53 Rev. 5, control families |
| `e-investigation-forensics` | Investigations and digital forensics: the management and legal view | E (Expert) | 3 — design a forensic-readiness program and run an investigation's evidence handling so it survives legal scrutiny | `c-incident-response` | DFIR Lead; SOC Manager | **CISSP 7.1** (served directly); NIST SP 800-86, Guide to Integrating Forensic Techniques into Incident Response (Aug 2006); RFC 3227, Guidelines for Evidence Collection and Archiving (Feb 2002) |
| `e-logging-monitoring` | Logging and monitoring operations: deciding what gets watched, and by whom | E (Expert) | 3 — design a logging program — what to log, retention, and the SOC workflow that consumes it | `c-log-sources` | SOC Manager; Detection Engineer | **CISSP 7.2** (served directly); NIST SP 800-92, Guide to Computer Security Log Management (Sep 2006); NIST SP 800-53 Rev. 5, Audit and Accountability (AU) family (via publication page) |
| `e-config-management` | Configuration management: baselines, hardening, and catching drift | E (Expert) | 3 — write a hardening baseline for a server role and operate drift detection against it | `a-linux-cli` | Systems Administrator; SOC Engineer | **CISSP 7.3** (served directly); NIST SP 800-128, Guide for Security-Focused Configuration Management (Aug 2011); NIST SP 800-70 Rev. 4, National Checklist Program for IT Products (Feb 2018) |
| `e-secops-concepts` | Foundational security operations concepts: the principles you run on | E (Expert) | 3 — apply need-to-know, least privilege, separation of duties, and defense in depth as daily operating decisions — and assess a zero-trust gap | `e-iam` | Security Architect; SOC Manager | **CISSP 7.4** (served directly); NIST SP 800-207, Zero Trust Architecture (Aug 2020); NIST SP 800-53 Rev. 5, AC-5 separation of duties / AC-6 least privilege (via publication page) |
| `e-media-protection` | Media protection: handling the physical object | E (Expert) | 3 — write media-handling and sanitization procedures an auditor can follow | `e-security-program` | GRC Analyst; Operations Lead | **CISSP 7.5** (served directly); NIST SP 800-88 Rev. 1, Guidelines for Media Sanitization (Dec 2014); NIST SP 800-53 Rev. 5, Media Protection (MP) family (via publication page) |
| `e-incident-management` | Incident management: the team, the escalation, and the communications | E (Expert) | 3 — stand up the incident-management structure — team, escalation, comms, metrics — around the response lifecycle | `c-incident-response` | SOC Manager; Incident Commander | **CISSP 7.6** (served directly); NIST SP 800-61 Rev. 3, Computer Security Incident Handling Guide (Apr 2025); FIRST CSIRT Services Framework v2.1 |
| `e-detective-preventive` | Detective and preventive measures in operation: choosing, placing, and tuning controls | E (Expert) | 3 — select, place, and tune detective and preventive controls for a SOC's needs | `c-soc-triage` | SOC Engineer; Detection Engineer | **CISSP 7.7** (served directly); NIST SP 800-94, Guide to Intrusion Detection and Prevention Systems (Feb 2007); NIST SP 800-53 Rev. 5, System and Information Integrity (SI) family (via publication page) |
| `e-patch-management` | Patch and vulnerability management operations: from CVE to deployed fix | E (Expert) | 3 — run the patching operation — SLA policy, exception process, emergency runbook | `c-vuln-ecosystem` | Vulnerability Manager; SOC Lead | **CISSP 7.8** (served directly); NIST SP 800-40 Rev. 4, Guide to Enterprise Patch Management Planning (Apr 2022); CISA Known Exploited Vulnerabilities (KEV) catalog |
| `e-change-management` | Change management: approving the change before it ships | E (Expert) | 3 — review change requests with written rationale and run the change process including emergencies | `e-config-management` | Operations Lead; GRC Analyst | **CISSP 7.9** (served directly); NIST SP 800-128, Guide for Security-Focused Configuration Management (Aug 2011); NIST SP 800-53 Rev. 5, CM-3 Baseline Change Control (via publication page) |
| `e-physical-security` | Physical security in operation: running the building's defenses day to day | E (Expert) | 3 — run the physical-security operation — people, procedures, and environmental controls in daily use |  | Facilities Lead; GRC Analyst | **CISSP 7.14** (served directly); NIST SP 800-53 Rev. 5, Physical and Environmental Protection (PE) family (via publication page); CISA: Physical Security (topic page) |
| `e-personnel-safety` | Personnel safety: protecting the people, not just the accounts | E (Expert) | 3 — produce a travel-security briefing and a workplace-safety procedure set |  | Security Manager; GRC Analyst | **CISSP 7.15** (served directly); OSHA: Workplace Violence — Overview; CISA: Insider Threat Mitigation |

## Pilot dependency graph

```
a-http-depth ──→ b-idor ──→ (Phase 3: B-VULN-02, B-VULN-05, B-DEF, B-BOUNTY)
     │
     └──→ (Phase 3: Stage B/C/D traffic-dependent lessons)

e-risk-assessment ──→ (Phase 3: E-GOV-01, E-D1-11, E-LEAD, E-D1-07)

ai-prompt-injection ──→ ai-llm-architecture ──→ ai-llm-top10 ──→ ai-supply-chain ──→ ai-governance

## Stage A foundation batch dependency graph (2026-10-09)

```
a-dns-depth ──→ a-tcpip-ports ──→ a-linux-cli ──→ a-git-github ──→ a-http-depth ──→ b-idor
     │                │                │                 │
     └────→ a-http-depth (DNS answers where, HTTP answers what)
```

## Stage B web-vulnerability wave dependency graph (2026-10-09)

```
b-idor ──→ b-sqli ──→ b-command-injection ──→ b-ssrf ──→ b-csrf ──→ b-xss ──→ b-business-logic ──→ b-session-auth ──→ b-security-headers
   │           │              │                    │           │
   └─(trust    └─(input→code  └─(same pattern,     └─(server    └─(browser
     the         in the DB)    OS layer)           fetches)     forges)
     client)
```

## Stage C detection/operations wave dependency graph (2026-10-09)

```
b-security-headers ──→ c-soc-triage ──→ c-incident-response
                           │                    ▲
                           ▼                    │
                      c-log-sources ──→ c-sigma-detection
                           │
                           └── (rereads b-session-auth / b-command-injection / b-xss telemetry)
```

## Stage C disclosure wave dependency graph (2026-10-09)

```
incident-response ──→ c-cvd ──→ c-cve-program ──→ c-cvss ──→ c-vuln-ecosystem
(detection wave)      (CERT/OpenSSF;          (555 CNAs;          (v3.1+v4.0           (CWE Top 25:2025;
                       Heartbleed vs           Record Format        hand-scored;         KEV; EPSS;
                       SandboxEscaper)         5.2.0; credits[])    E:U 7.7→5.2)        NVD via OIG-26-020-I)
                          │                        │
                          └────→ b-methodology ─────┘
                                 (reporting phase prerequisite)
```
c-cvd is the disclosure half of the Stage C milestone; c-cve-program the record half. c-cvss feeds c-vuln-ecosystem's prioritization; the ecosystem lesson feeds c-soc-triage (triage is prioritization under time pressure) and e-risk-assessment (severity as risk input).

## Notes

- All four pilot lessons target level 3 per the brief; nothing in the pilot is labeled below 3.
- `b-idor` assumes the B-AUTH lesson (authorization discipline) ships before it in the final ordering.
- `ai-prompt-injection` assumes the `ai-01` lesson (how LLM apps are built) ships before it in the final ordering.
- No lesson in the pilot reproduces exam questions or copyrighted outline text; CISSP objectives referenced by number with paraphrase only.
- All four Stage B wave lessons target level 3. `b-csrf` walkthrough step 4's browser-click sub-step is marked **not run by us** (no live browser on the build machine); the request shape it fires was verified server-side.

## Stage E CISSP-domain wave (2026-10-09)

```
e-risk-assessment ──→ e-iam ──→ (E-D1-08 personnel security)
       │                 │
       │                 └──→ E-D7-03 (privileged access ops)
       │
       └──→ e-bcp-drp ──→ (E-D7-10 recovery strategies; E-GOV-01 CSF Recover)
              │
              └──→ c-incident-response (handoff: IR ends, continuity begins)

a-http-depth ──→ e-crypto-applied ──→ (E-D2-06 data protection; E-D3-01 secure design)
b-session-auth ──→ e-iam (the processes behind the technical failures)
Stage B vuln classes ──→ e-sdlc ──→ (D-AppSec track: the tooling this program deploys)
```

## AI security track wave dependency graph (2026-10-09)

```
ai-prompt-injection ──→ ai-llm-architecture ──→ ai-llm-top10 ──→ ai-supply-chain ──→ ai-governance
     (LLM01:2026)            (CAISP ch.1-2)          (LLM02-10:2026)      (LLM04:2026)         (CAISP ch.7)
                                                      │                       │
                                                      └────→ e-risk-assessment (risk method reused)
                                                              e-sdlc (AI gates join the SDLC)
```
CAISP chapters 1–7 now all map to lessons (ch. 4 pipeline and ch. 5 threat-modeling remain as logged future lessons). CAISP kept separate from CertNexus CAIP throughout.

## Stage D specialist wave 1 dependency graph (2026-10-09)

```
Stage B/C foundations ──→ d-redteam-concepts ──→ d-malware-analysis
(c-soc-triage, c-log-sources,        (ATT&CK behavior      (static triage + YARA;
  Stage B vuln classes)               language; C2/evasion   detonation reader-side)
                                      concepts)
        ├──→ d-cloud-security (shared responsibility → IAM → misconfigs → Prowler/ScoutSuite)
        └──→ d-appsec (STRIDE → SAST/DAST/IAST/SCA → SDLC gates → code review)
                   │
                   └──→ e-sdlc (the program this tooling serves; CISSP 8.1–8.5 governance half)
```
d-redteam-concepts is the concept hub: C2/evasion concepts feed the DFIR track's detections; malware-analysis feeds c-sigma-detection; cloud-security feeds c-log-sources (cloud audit logs) and c-incident-response (cloud IR); d-appsec is the hands-on half of CISSP 8.1–8.5.

## AI track completion + program leadership dependency graph (2026-10-09)

```
ai-supply-chain ──→ ai-pipeline ──→ ai-threat-modeling ──→ ai-governance
(CAISP ch.6)         (CAISP ch.4)      (CAISP ch.5)            (CAISP ch.7)
     │                    │                  │
     │                    └──→ ai-governance (pipeline controls as register evidence)
     └──→ ai-pipeline (signing/admission assumed)

ai-prompt-injection ──→ ai-llm-architecture ──→ ai-llm-top10 ──→ ai-threat-modeling
     (LLM01:2026)            (CAISP ch.1-2)          (LLM02-10:2026)

e-risk-assessment ──→ e-security-program ──→ e-board-communication
(register method)      (charter + metrics)      (the memo; director test)
       │                       │
       └──→ e-board-communication (register IDs cited in risk bullets)
```
CAISP chapters 1–7 now all map to complete lessons (ch. 4 `ai-pipeline`, ch. 5 `ai-threat-modeling` close the two logged future lessons). Program leadership is the final brief §5 scope item: strategy → charter → board memo, ending in the Stage E capstone path.

## Final wave: Stage D wave 2 + Stage C remainder (2026-10-09)

| id | title | stage | level | prerequisites | roles served | map refs |
|---|---|---|---|---|---|---|
| `d-dfir-deep` | DFIR deep: disk, memory, network forensics | D (Specialist) | 3 — evidence handling + timeline from labeled data; tool runs on real images reader-side | `c-incident-response`; `c-log-sources`; `a-linux-cli`; `d-malware-analysis` helps | DFIR Analyst; SOC L3; NICE: Investigation | NIST SP 800-86 (process spine); order of volatility; Volatility workflow; feeds `c-sigma-detection` |
| `d-exploit-concepts` | Exploit development and reverse engineering: concepts | D (Specialist) | 3 — mitigation mechanics demonstrated live; exploitation technique reader-side on pwn.college | `a-reading-code`; `a-python-security`; `d-redteam-concepts`; `d-malware-analysis` | Exploit Developer (candidate role); Vulnerability Researcher; NICE: Design and Development | pwn.college (training only); NX/ASLR/canaries/RELRO; Ghidra; how2heap |
| `c-public-track-record` | Building a public track record: write-ups that teach | C (Professional) | 3 — worked write-up authored to the bar; publication reader-side | `c-cvd`; `c-cve-program`; `c-vuln-ecosystem`; `b-methodology` | All roles (recognition keystone); NICE: Oversight and Governance | Project Zero bar (mechanism-first); Kettle HTTP/2 template; brief recognition pathway |
| `c-ai-tooling` | AI tooling professionals use (CVP worked example) | C (Professional) | 3 — program mechanics + evidence mapping; application reader-side | `c-public-track-record`; `ai-governance`; `c-cvd` | Security Engineer; AI Security Engineer; NICE: Protection and Defense | Anthropic CVP 2026-10-06 (3 tiers, dated); brief §3 correction (tooling, never credential) |

### Final-wave dependency graph

```
c-incident-response ──→ d-dfir-deep ──→ c-sigma-detection (hunts become rules)
d-redteam-concepts ──→ d-exploit-concepts ──→ c-public-track-record (research write-ups)
c-vuln-ecosystem ──→ c-public-track-record ──→ c-ai-tooling (track record as evidence)
ai-governance ──→ c-ai-tooling (governing AI vs wielding AI tooling)
```
| `b-bug-bounty` | Bug bounty mechanics: how authorized testing is actually offered to beginners | B (Practitioner) | 3 — apply: read a program policy cold, stay in scope, write a triage-ready report | `b-authorization-scope`; Stage B vuln classes; no live target | Penetration Tester; Bug Bounty Researcher; NICE: Implementation and Operation | Stage B milestone lesson (first valid finding submitted to an authorized program); feeds `c-cvd`, `c-public-track-record`, `c-cve-program`; brief §7 hard rules |

## Role paths (brief §4) — 8 paths, all generated from the lesson data

| path | role page | sequence | checkpoints | capstone (public artifact) |
|---|---|---|---|---|
| `/g/path/soc-analyst/` | `/r/soc-analyst/` | A (lighter on crypto) → detection basics → D deeper | 3: alert triage dispositions; home-lab write-ups; Sigma rule + blind spots | Published detection-engineering project: Sigma rule package for one ATT&CK technique + intrusion investigation, public repo |
| `/g/path/security-analyst/` | `/r/security-analyst/` | A → B (Apply level) → C lighter (disclosure literacy) → D detection/DFIR | 3: ATT&CK investigation; tested detection rule; one-page CISA threat brief | Published original threat analysis: technique deep-dive or advisory-derived detection pack |
| `/g/path/pentester/` | `/r/pentester/` | A full → B full → C full → D red team + exploit concepts | 3: PortSwigger core labs; first valid finding; full lab pentest report | Coordinated disclosure with CVE credit, technique write-up, or OSS tool contribution + full engagement report |
| `/g/path/appsec/` | `/r/appsec/` | Code fluency first → HTTP/auth → vuln classes (fix side) → D AppSec → E domain 8 | 3: STRIDE threat model; SAST in pipeline; disclosed+merged fix | Merged security fix in a real OSS project with teaching write-up, or original secure-design guide |
| `/g/path/dfir/` | `/r/dfir/` | PREREQ: complete the SOC analyst path → D forensics/response | 4: timeline; memory forensics; chain of custody; non-technical report | Full forensic case study from a simulated breach — timeline, evidence notes, findings, executive report |
| `/g/path/cloud-security/` | `/r/cloud-security/` | A → cloud fluency block (GAP: no lesson) → D cloud → E domains 3, 5 | 3: misconfig fixed + recurrence prevention; least privilege end to end; failing guardrail | Published cloud security baseline: audited reference architecture or misconfiguration-class research |
| `/g/path/iam-engineer/` | `/r/iam-engineer/` | A (HTTP auth, crypto) → E domain 5 → D cloud IAM | 3: permissions audit with rationale; least privilege + breakage notes; joiner-mover-leaver doc | Published IAM reference: least-privilege policy library or access-review methodology with worked example |
| `/g/path/grc-analyst/` | `/r/grc-analyst/` | A lighter → E risk/continuity → program leadership → AI governance | 3: control→evidence map; one-page director risk; followable policy | Complete published GRC work product: risk assessment, control guide, or audit plan — written to be used |

## Knowledge maps (brief §4)

- `/g/map-cissp/`: all 62 objectives (1.1–8.5), guidebook paraphrases, lesson links or gaps. **17 of 62 have a lesson** (1.7, 1.9, 3.6, 5.1–5.5, 7.10–7.13, 8.1–8.5). 45 gaps logged (see gaps.md).
- `/g/map-caisp/`: 7 chapters → lessons. **7 of 7 have a lesson.** CAISP kept separate from CertNexus CAIP (one line, never merged).
| `ai-sec-automation` | AI security automation: concepts | AI track | 2 — concepts + detection: name the SEC598/SEC535 subject areas, pair every attack concept with defense and telemetry, write a detection plan | `ai-llm-architecture`, `ai-llm-top10`, `c-soc-triage` | AI track; GASAE/GOAA light maps | GASAE + GOAA subject areas as concepts (SANS SEC598/SEC535) |
