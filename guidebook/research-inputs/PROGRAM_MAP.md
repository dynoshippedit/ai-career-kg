# Security Guidebook — Program Map
### learncomputerstuff.dev add-on | Research master document | Spawn-off structure for research agents

**Thesis:** the complete path from absolute beginner to employable security professional — ending with a CVE credited in your name and a clear run at Anthropic's Cyber Verification Program. The guidebook is FREE: every stage, every exam, every cert covered through free resources. No pricing, no paid tools, no paid courses — the research shows what free material teaches each exam's content.

**The deeper promise:** this is a recognition pathway, not just a learning path. Every stage produces public, verifiable proof of skill — lab completions, bounty track record, disclosure history, CVE credits, certifications — the kind of evidence that gets you hired without a degree. The guidebook shows the reader how to become *known* in the industry, stage by stage.

**How to use this file:** each research agent takes one STAGE section and expands every bullet to full depth (objectives, lessons, free resources, labs, milestone checks, CV lines). No thin sections — gaps get flagged, never smoothed over.

---

## STAGE A — FOUNDATIONS
*Goal: understand how computers, networks, and the web actually work. No vocabulary without mechanics.*

- **Linux internals** — filesystem, permissions, processes, users/groups, SSH, bash, logs, services, package management. *Free: OverTheWire Bandit (learns Linux through security challenges), Linux Journey, linuxcommand.org.* Lab: complete Bandit; harden a fresh VM's SSH.
- **Networking** — TCP/IP stack, OSI, IPv4/IPv6, subnetting, DNS resolution chain, DHCP, ports, routing, firewalls, VPNs, proxies, VLANs. *Free: Professor Messer Network+ (87 free episodes), Practical Networking (YouTube), Kurose & Ross "Computer Networking: A Top-Down Approach" (free online), Cisco NetAcad.* Lab: Wireshark capture — follow a TCP stream, dissect DNS and TLS handshakes; tcpdump on CLI.
- **HTTP, deeply** — methods, status codes, headers, cookies/sessions, auth schemes (Basic, Bearer, JWT structure, OAuth2/OIDC flows), TLS handshake step by step. *Free: PortSwigger Web Security Academy (starts at HTTP basics), MDN HTTP docs.* Lab: replay a login with curl, explain every header; decode a JWT at jwt.io.
- **Python for security tooling** — requests, sockets, argparse, parsing output. *Free: Python for Everybody, Automate the Boring Stuff (free online).* Lab: build a port scanner and a log parser from scratch.
- **Cryptography** — hashing vs encryption, symmetric/asymmetric, signatures, PKI/certificates, how each breaks when misused (never roll your own). *Free: CryptoHack (gamified), Dan Boneh Crypto I (audit free).* Lab: break a weak hash, verify a signature chain.
- **Reading code** — JavaScript and SQL literacy minimum; enough of target languages to follow a vulnerability.
- **Milestone:** explain the full packet-to-render path of a login submission.
- **CV:** nothing yet — honesty is the policy. **Unlocks:** Stage B.

## STAGE B — PRACTITIONER
*Goal: find real vulnerabilities in authorized targets, prove them reproducibly, report them.*

- **Tool catalog, 15 phases in activation order** — scope records → proxy (Burp Community free / OWASP ZAP fully open-source) → session isolation (separate browser profiles) → authorization comparison (manual + tool-assisted, human interprets) → asset discovery (subfinder, Amass — free) → crawling → content/parameter discovery (gobuster, ffuf — free) → data handling → API contracts (oasdiff compares specs; Schemathesis generates tests — neither knows business rules) → tokens/callbacks → source analysis → dependencies/secrets (TruffleHog, verification stays OFF) → local environments → reproduction → evidence.
- **Methodology** — OWASP Web Security Testing Guide (the category-by-category bible), PTES, NIST SP 800-115. Scope discipline: recon findings are candidates, not permission.
- **Web hacking chain** (each: how it works → how to find it → how to prove it): IDOR → broken access control → SQLi → command injection → API abuse → SSRF → XSS → CSRF → business logic flaws. *Free: PortSwigger Web Security Academy — the single best hands-on resource, its topic list IS the curriculum (15+ SQLi labs, 15+ XSS, 10+ access control, auth, SSRF, SSTI, XXE, deserialization, JWT, OAuth, GraphQL, race conditions, LLM attacks).*
- **Practice labs, all free** — DVWA (`docker run -p 80:80 vulnerables/web-dvwa`), OWASP Juice Shop (`docker run -p 3000:3000 bkimminich/juice-shop`), WebGoat, bWAPP, crAPI (OWASP API Top 10), DVGA (GraphQL), Google Gruyere (absolute beginners), VulnHub VMs, TryHackMe/HackTheBox free tiers, CTFtime.
- **Defensive basics** — SOC triage workflow, reading SIEM alerts, alert logic.
- **Bounty mechanics** — HackerOne, Bugcrowd, Intigriti: programs, scopes, safe harbor, payouts. Study disclosed reports (HackerOne Hacktivity, PentesterLand writeup archive) — real chains labs can't replicate.
- **Ethics hard rules** — no testing outside written authorization; Nuclei match for an existing CVE is not a new CVE; no credential use ever; automated tools produce false positives — confirm by hand.
- **Milestone:** first valid submitted finding. **CV:** bounty platform profile, first write-up. **Unlocks:** Stage C.

## STAGE C — PROFESSIONAL
*Goal: coordinated disclosure done right; a CVE with your name on it; the hireable line.*

- **Coordinated disclosure end-to-end** — finding → validation → vendor contact (security policy / security.txt first) → acknowledgment → assessment → patch window → CVE request → publication. Typical flow: OpenSSF CVD guide, CERT/CC. Good vs bad disclosure with real examples.
- **CVE program** — MITRE as editor; ~100+ CNAs (vendors like Microsoft/Cisco/Red Hat, bounty platforms, national CERTs) authorized to assign IDs. Request path: report to vendor/CNA → validation → ID reserved (CVE-YYYY-NNNNN) → coordinated disclosure → publication. CVE JSON 5.x record format. NVD (NIST) enriches with CVSS, CWE, CPE. Not every bug qualifies — must be independently fixable security impact.
- **CVSS v3.1 and v4.0** — FIRST.org standard. Base/Temporal/Environmental metric groups (v4.0 adds Supplemental). Severity bands: Critical 9.0–10.0, High 7.0–8.9, Medium 4.0–6.9, Low 0.1–3.9. *Free: NVD CVSS calculator.* Lab: score 5 real CVEs in both versions; find where v3.1 and v4.0 disagree and why.
- **CWE Top 25** (MITRE) with web relevance notes; **CAPEC** attack patterns; **CISA KEV catalog** — known-exploited vulns, what it is and why employers screen on it.
- **Public track record** — write-ups that teach: root cause, impact chain, remediation. Quality bar: reproducible, honest about limitations.
- **CVP Defense Access** — Anthropic's Cyber Verification Program tier for defensive work (vuln analysis, IR, malware analysis). Individuals CAN qualify with a track record of reported vulnerabilities — this is the hireable-professional milestone.
- **Milestone:** CVE credited in your name. **CV:** CVE credits, disclosure history. **Unlocks:** Stage D.

## STAGE D — SPECIALIST (pick a track, go deep)
*Goal: deep, employable expertise in one direction.*

- **Red team ops** — MITRE ATT&CK mapping, adversary emulation (Atomic Red Team — free), C2 infrastructure concepts, evasion, purple teaming. *Free: ATT&CK matrix, Atomic Red Team.*
- **DFIR** — forensic artifacts (disk, memory, network), IR lifecycle per NIST SP 800-61, threat hunting hypotheses, detection engineering (Sigma, YARA). *Free: Eric Zimmerman's tools, Velociraptor, SANS DFIR posters, REMnux.*
- **AppSec** — threat modeling (STRIDE), SAST/DAST/IAST/SCA, secure SDLC integration, code review technique. *Free: OWASP SAMM, OWASP ASVS, Semgrep, CodeQL (public repos).*
- **Exploit dev & reverse engineering** — binary basics, debugger workflows, buffer overflows through modern mitigations (ASLR, DEP, stack canaries). *Free: Ghidra (NSA), x64dbg, pwn.college (ASU).*
- **Malware analysis** — static vs dynamic, sandboxing, behavioral indicators. *Free: FLARE VM, REMnux, Any.Run community tier.*
- **Cloud security** — AWS/Azure IAM, common misconfigurations, shared responsibility. *Free: cloud free tiers, Prowler, ScoutSuite.*
- **Milestone:** deep employable specialization. **CV:** track cert, specialization proof, tool or talk. **Unlocks:** Stage E.

## STAGE E — EXPERT
*Goal: the person organizations hire to own security.*

- **CISSP Domain 1 — Security and Risk Management:** governance, policy, risk assessment/management, BCP/DRP, ethics, personnel security, compliance.
- **CISSP Domain 2 — Asset Security:** data classification, ownership, retention, privacy, secure handling and disposal.
- **CISSP Domain 3 — Security Architecture and Engineering:** security models, evaluation criteria (Common Criteria), crypto systems, physical security, system vulnerabilities.
- **CISSP Domain 4 — Communication and Network Security:** secure network architecture, transmission media, network attacks and countermeasures, secure communications.
- **CISSP Domain 5 — Identity and Access Management:** provisioning/deprovisioning, authentication (MFA, SSO, Kerberos), authorization models (RBAC, ABAC, MAC), identity lifecycle, access review.
- **CISSP Domain 6 — Security Assessment and Testing:** test strategies, security control testing, code review/audit, vulnerability assessment vs penetration test, log review, misuse/abuse case testing.
- **CISSP Domain 7 — Security Operations:** SOC operations, logging and monitoring, incident management, disaster recovery operations, physical and personnel security, investigations.
- **CISSP Domain 8 — Software Development Security:** SDLC security, OWASP, database security, secure coding practices, software assurance and maturity models.
- **Governance:** NIST CSF 2.0 (free), ISO 27001 (paid standard — say so), SOC 2 — what each is, who needs it.
- **CVP Red Team / Specialized tiers** — organization-only; unlock when hired or sponsored. The guide's promise fulfilled: you are now someone such an organization hires.
- **Leading programs:** security strategy, metrics that matter, board communication.
- **Milestone:** employable as a security leader. **CV:** CISSP + specialization + CVE history + CVP standing.

---

## AI SECURITY CERTIFICATION TRACK (runs alongside D/E)

Prerequisite ladder, easiest gate first. No cert presented as automatically worth pursuing — each covered through its free preparation path: what free material teaches its domains, who it's for, and what knowledge it requires.

1. **AIGP (IAPP)** — no prerequisites; 100-Q knowledge exam; privacy/law/risk aptitude. 4 domains: AI governance foundations, AI laws & standards (EU AI Act heavy), dev lifecycle governance, deployment & use. Renewal via CPEs.
2. **CAISP (Practical DevSecOps)** — no credential gate; needs Linux CLI + some Python; 6-hour practical exam (5 challenges + 24-hr report); lifetime validity. 7 chapters: AI security intro, attacking LLMs, OWASP LLM Top 10, AI attacks/defenses via DevOps, threat modeling (STRIDE), AI supply chain (SBOMs, Cosign model signing), governance (NIST AI RMF, ISO/IEC 42001, EU AI Act). Follow-on: CAASE (agentic AI). *Free prep: OWASP LLM Top 10 docs, MITRE ATLAS.*
3. **SEC598 → GIAC GASAE (SANS)** — needs working SOC/security background + scripting (Python/PowerShell) + cloud/SOAR familiarity. 6 sections: GenAI/LLM foundations; automation engineering (PowerShell, Terraform, Ansible, Python, Jupyter); AWS/Azure cloud automation; red team automation & offensive AI agents (adversary emulation); defensive automation & AI-augmented IR; capstone. 25 labs. Exam: 82 Qs, 70% pass.
4. **SEC535 → GIAC GOAA (SANS)** — needs pentesting fundamentals first (recon, enumeration, exploitation). AI-enabled attacking: pentesting GPTs, AI OSINT (Spiderfoot, Bbot, AI dorking), AI-augmented SQLi/brute force/command injection, deepfake phishing, AI malware, guardrail bypassing, SOAR/N8N offensive workflows. 14 labs + CTF. Exam: 56 Qs, 67% pass.
5. **AAISM (ISACA)** — HARD GATE: active CISSP or CISM required, no test-first path. 3 domains: AI governance & program management, AI risk management, AI technologies & controls. 90 scenario MCQs, scaled score 450.

Wider SANS AI family (reference): SEC545 (securing LLM apps → GAIPS), SEC573 (Python automation → GPYC), SEC595 (ML for security → GMLE), SEC536 (pentesting AI systems → GAIPT).

**Positioning rule:** AIGP and CAISP reachable from the core track; SANS courses need practitioner experience; AAISM downstream of CISSP entirely.

---

## CAREER LADDER (cross-cutting)

- **NICE framework** (NIST, 7 categories) mapped to stages: Securely Provision, Operate & Maintain, Oversee & Govern, Protect & Defend, Analyze, Collect & Operate, Investigate. Each stage names its NICE work roles (e.g., B→ Cyber Defense Analyst / Vulnerability Analyst; C→ Security Control Assessor; D→ track roles like Cyber Defense Incident Responder, Digital Forensics; E→ Information Systems Security Manager, Executive Cyber Leader).
- **CV at every stage:** what you can honestly claim, what you cannot claim yet, what unlocks next.
- **The hireable narrative:** Stage C (CVE credit + disclosure history) is the employable-professional line; CVP Defense Access is the individual milestone; Red Team/Specialized tiers open through organizational sponsorship.
- **Free-only:** every stage completable with free tooling and free resources. No prices, no paid items — the guidebook is the free path through everything each exam requires.

---

## RESEARCH ASSIGNMENTS (spawn one agent per track)

1. **Stage A** — expand every bullet: objectives, lessons, free resources, labs, milestone checks
2. **Stage B** — tool phases, hacking chain, methodology, bounty mechanics
3. **Stage C** — disclosure, CVE/CNA/NVD, CVSS v3.1+v4.0, CWE, KEV, CVP Defense Access
4. **Stage D** — all six specialist tracks + cloud + AI cert ladder
5. **Stage E** — all 8 CISSP domains expanded + governance + AIGP/AAISM + CVP org tiers
6. **Career ladder** — NICE mapping, CV lines per stage, free-first costing

**Standards:** primary sources verified; no copied text — summarize and link; depth over breadth per node; gaps flagged honestly, never smoothed over.
**Output:** `~/workspace/security-curriculum/curriculum.md` — the guidebook manuscript.
**Then:** gap review against this map, then build as a native route/guide on learncomputerstuff.dev.
