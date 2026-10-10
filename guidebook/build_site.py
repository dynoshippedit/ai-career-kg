#!/usr/bin/env python3
"""Build the security guidebook section into the learncomputerstuff.dev static site.

Usage: python3 build_site.py
Reads:  lessons/*.md (the 10-part lesson spec, markdown)
Writes: <repo>/g/<slug>/index.html  (one per lesson)
        <repo>/g/index.html          (guidebook entry page)

The HTML reuses the site's own inline CSS verbatim (extracted from the homepage)
so design tokens, header, nav, footer and voice stay native. No external
dependencies. Re-run for future batches: add the lesson .md, extend LESSONS,
run again.
"""
import html
import re
import sys
from pathlib import Path

GUIDEBOOK = Path(__file__).parent
REPO = Path(__file__).resolve().parent.parent  # site repo root (guidebook/ lives inside it)
TODAY = "2026-10-09"


def numword(n):
    """Small number-to-words for lesson counts (site voice uses words)."""
    ones = ["zero", "one", "two", "three", "four", "five", "six", "seven",
            "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
            "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
            "eighty", "ninety"]
    if n < 20:
        return ones[n]
    if n < 100:
        t, o = divmod(n, 10)
        return tens[t] + ("" if o == 0 else "-" + ones[o])
    h, rest = divmod(n, 100)
    return ones[h] + " hundred" + ("" if rest == 0 else " " + numword(rest))

# lesson id -> url slug
LESSONS = [
    # (lesson_id, slug, stage_label, dateline_note, meta_description)
    ("a-http-depth", "http-depth", "Stage A · Foundations",
     "Walkthrough run 2026-10-09 · loopback only, nothing external touched",
     "HTTP in depth: requests, responses, cookies, JWTs and TLS — explained byte by byte, with every walkthrough step run locally. A free lesson in the security guidebook."),
    ("b-idor", "idor", "Stage B · Practitioner",
     "Walkthrough run 2026-10-09 · local demo app (no Docker on the build machine)",
     "IDOR: how a missing authorization check lets one user read another's data — reproduced locally, fixed, and verified. A free hands-on lesson in the security guidebook."),
    ("e-risk-assessment", "risk-assessment", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-09 · no command line in this lesson",
     "Risk assessment as a worked case: scope, rate, respond and report, end to end — serving CISSP objective 1.9. A free lesson in the security guidebook."),
    ("ai-prompt-injection", "prompt-injection", "AI track",
     "Walkthrough steps 1–4 run 2026-10-09 · step 5 (live model) not run by us",
     "Prompt injection, the #1 LLM application risk (OWASP LLM Top 10 2026, LLM01:2026): mechanism, code-level defenses and detection. A free lesson in the security guidebook."),
    # --- Stage A foundation batch (2026-10-09) ---
    ("a-dns-depth", "dns-depth", "Stage A · Foundations",
     "Walkthrough run 2026-10-09 · loopback only; TCP form of DNS used (sandbox blocks UDP)",
     "DNS in depth: the resolution chain, message format, record types, caching and DNSSEC — every step run locally against a toy authoritative server. A free lesson in the security guidebook."),
    ("a-tcpip-ports", "tcpip-ports", "Stage A · Foundations",
     "Walkthrough run 2026-10-09 · loopback only; UDP step not run by us (sandbox blocks UDP loopback); packet-capture step re-ran 2026-10-10 with real tcpdump",
     "TCP/IP and ports: the handshake, connection states, what a port really is — observed live with ss on loopback. A free lesson in the security guidebook."),
    ("a-linux-cli", "linux-cli", "Stage A · Foundations",
     "Walkthrough run 2026-10-09 · local scratch dir; shell ran as root (flagged in-lesson)",
     "Linux command line for security work: files, permissions, processes, logs, pipes and SSH keys — the instrument every later lesson assumes. A free lesson in the security guidebook."),
    ("a-git-github", "git-github", "Stage A · Foundations",
     "Walkthrough run 2026-10-09 · local repos only; GitHub-side steps not run by us",
     "Git and GitHub: snapshots, staging, branching, remotes and pull requests — the evidence pipeline for the whole program. A free hands-on lesson in the security guidebook."),
    # --- Stage B web-vulnerability wave (2026-10-09) ---
    ("b-sqli", "sqli", "Stage B · Practitioner",
     "Walkthrough run 2026-10-09 · local demo app (no Docker on the build machine)",
     "SQL injection: when input becomes the query — in-band, blind and time-based families reproduced locally, then fixed with parameterized queries. A free hands-on lesson in the security guidebook."),
    ("b-command-injection", "command-injection", "Stage B · Practitioner",
     "Walkthrough run 2026-10-09 · local demo app (no Docker on the build machine)",
     "OS command injection: shell metacharacters, blind time-delay proofs, and why allow-lists beat blocklists — reproduced locally and fixed. A free hands-on lesson in the security guidebook."),
    ("b-ssrf", "ssrf", "Stage B · Practitioner",
     "Walkthrough run 2026-10-09 · local demo app; metadata tree is a labeled loopback simulation",
     "SSRF: when the server fetches what you tell it to — loopback, cloud-metadata angle, filter bypasses and the allow-list fix. A free hands-on lesson in the security guidebook."),
    ("b-csrf", "csrf", "Stage B · Practitioner",
     "Walkthrough run 2026-10-09 · local demo app; browser-click sub-step re-ran 2026-10-10 (headless Chromium)",
     "CSRF: when the victim's browser does the attacker's work — token defense, SameSite, and the no-state-changing-GET rule. A free hands-on lesson in the security guidebook."),
    # --- Stage B web-vulnerability wave, continued (2026-10-09) ---
    ("b-xss", "xss", "Stage B · Practitioner",
     "Walkthrough run 2026-10-09 · local demo app; browser-execution sub-steps re-ran 2026-10-10 (headless Chromium)",
     "Cross-site scripting: reflected, stored and DOM-based — the trust-boundary mechanism, context-aware output encoding, and CSP as defense in depth. A free hands-on lesson in the security guidebook."),
    ("b-business-logic", "business-logic", "Stage B · Practitioner",
     "Walkthrough run 2026-10-09 · local demo shop (price tamper, coupon race, negative quantity)",
     "Business-logic flaws: map the workflow, violate its assumptions — price tampering, coupon races and negative quantities, with server-side fixes and business-anomaly detection. A free hands-on lesson in the security guidebook."),
    ("b-session-auth", "session-auth", "Stage B · Practitioner",
     "Walkthrough run 2026-10-09 · local demo login; MFA enrollment step not run by us",
     "Broken authentication and session management: fixation, predictable tokens, missing rate limits — reproduced locally, fixed, with MFA as the structural answer. A free hands-on lesson in the security guidebook."),
    ("b-security-headers", "security-headers", "Stage B · Practitioner",
     "Walkthrough run 2026-10-09 · local demo; browser-enforcement sub-steps re-ran 2026-10-10 (headless Chromium)",
     "Security headers and browser defenses: CSP, HSTS, frame-ancestors, nosniff, cookie flags — what each buys, verified header by header with curl. A free hands-on lesson in the security guidebook."),
    ("b-bug-bounty", "bug-bounty", "Stage B · Practitioner",
     "Walkthrough run 2026-10-09 · report-drafting worked case; no real submission, no live target",
     "Bug bounty mechanics: how programs define scope and safe harbor, how triage decides, and how to write a report a stranger can reproduce — the dry run before your first real submission. A free lesson in the security guidebook."),
    # --- Stage C detection/operations wave (2026-10-09) ---
    ("c-soc-triage", "soc-triage", "Stage C · Professional",
     "Walkthrough run 2026-10-09 · labeled fictional event set; decision trees executed locally",
     "SOC triage: from alert to decision — the eight-stage pipeline, impossible-travel and beaconing decision trees, and the five classification buckets. A free lesson in the security guidebook."),
    ("c-log-sources", "log-sources", "Stage C · Professional",
     "Walkthrough run 2026-10-09 · fictional sample logs parsed with CLI tools",
     "Log sources that matter: endpoint, network, identity, email, cloud — what each sees, what goes blind without it, and cross-source correlation. A free hands-on lesson in the security guidebook."),
    ("c-sigma-detection", "sigma-detection", "Stage C · Professional",
     "Walkthrough run 2026-10-09 · rule validated and evaluated against labeled corpora",
     "Writing detections with Sigma: rule anatomy against the spec, the tuning loop, and detection-as-code discipline — measured, not asserted. A free hands-on lesson in the security guidebook."),
    ("c-incident-response", "incident-response", "Stage C · Professional",
     "Worked case authored and reviewed 2026-10-09 · no command line in this lesson",
     "Incident response basics: the NIST SP 800-61 Rev. 3 lifecycle and the full IR report — timeline, scope, ordered containment, honest limitations. A free lesson in the security guidebook."),
    # --- Stage C disclosure wave (2026-10-09) ---
    ("c-cvd", "cvd", "Stage C · Professional",
     "Worked case authored 2026-10-09 · local security.txt lab run; no command line beyond it",
     "Coordinated vulnerability disclosure: finding the security contact, writing the report, negotiating the timeline, publishing responsibly — Heartbleed vs the zero-day drops. A free lesson in the security guidebook."),
    ("c-cve-program", "cve-program", "Stage C · Professional",
     "Real CVE record fetched via CVE API 2026-10-09 · fictional request worksheet; no real submission",
     "The CVE Program: 555 CNAs, the request path, Record Format 5.2.0, and the credits field that puts your name in the permanent record. A free lesson in the security guidebook."),
    ("c-cvss", "cvss", "Stage C · Professional",
     "Walkthrough run 2026-10-09 · v3.1 equations and FIRST's v4.0 reference implementation reproduced all published scores",
     "CVSS v3.1 and v4.0 scored by hand: the metric groups, three official calibration cases, and where the versions disagree — including E:U collapsing 7.7 to 5.2. A free hands-on lesson in the security guidebook."),
    ("c-vuln-ecosystem", "vuln-ecosystem", "Stage C · Professional",
     "Walkthrough run 2026-10-09 · live EPSS, CISA KEV CSV, three-method ranking comparison",
     "CWE, CAPEC, CISA KEV, EPSS — and where enrichment comes from now that NVD enriches only prioritized CVEs. A free hands-on lesson in the security guidebook."),
    # --- Stage E CISSP-domain wave (2026-10-09) ---
    ("e-iam", "iam", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-09 · no command line in this lesson",
     "Identity and access management: the joiner-mover-leaver lifecycle, assurance levels, federation, RBAC/ABAC, privileged access — with a full access review worked case. A free lesson in the security guidebook, serving CISSP objectives 5.1–5.5."),
    ("e-crypto-applied", "crypto-applied", "Stage E · Expert",
     "Walkthrough run 2026-10-09 · OpenSSL 3.0.13, loopback only, nothing external touched",
     "Applied cryptography: hashes, modes, signatures, PKI path validation and the key lifecycle — ECB-vs-CBC demonstrated live, TLS 1.3 handshake run locally. A free hands-on lesson in the security guidebook, serving CISSP objective 3.6."),
    ("e-sdlc", "sdlc", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-09 · no command line in this lesson",
     "Secure SDLC: threat modeling with STRIDE, security gates per phase, the SSDF practice groups, and metrics that measure effectiveness — with a gate review worked case. A free lesson in the security guidebook, serving CISSP objectives 8.1–8.5."),
    ("e-bcp-drp", "bcp-drp", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-09 · no command line in this lesson",
     "Business continuity and disaster recovery: the BIA, RTO/RPO as decisions, recovery strategy selection, and a tabletop exercise — worked end to end. A free lesson in the security guidebook, serving CISSP objectives 1.7, 7.10–7.13."),
    # --- CISSP coverage wave (2026-10-10): the 45 remaining objectives ---
    ("e-ethics", "ethics", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Argue real security-work dilemmas from the ISC2 Code of Ethics' four canons, in priority order. A free lesson in the security guidebook, serving CISSP objective 1.1."),
    ("e-security-concepts", "security-concepts", "Stage E · Expert",
     "Local demo run 2026-10-10 (transcript in runs/e-security-concepts.log) · worked case authored and reviewed 2026-10-10",
     "Map a system's assets onto confidentiality, integrity, availability and the AAA properties, and name the trade-offs. A free lesson in the security guidebook, serving CISSP objective 1.2."),
    ("e-governance", "governance", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Draft a security governance charter that ties security decisions to business objectives, with roles, reporting lines, and a framework rationale. A free lesson in the security guidebook, serving CISSP objective 1.3."),
    ("e-cyber-law", "cyber-law", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Build an obligation-to-evidence compliance matrix from GDPR and related regimes. A free lesson in the security guidebook, serving CISSP objective 1.4."),
    ("e-investigations", "investigations", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Run the investigation-type decision tree: administrative, criminal, civil, regulatory. A free lesson in the security guidebook, serving CISSP objective 1.5."),
    ("e-policy-docs", "policy-docs", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Author a four-tier document set — policy, standard, procedure, guideline — with traceability both ways. A free lesson in the security guidebook, serving CISSP objective 1.6."),
    ("e-personnel-security", "personnel-security", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Run the human side of hiring, transfer, departure, and travel security with owners and timing. A free lesson in the security guidebook, serving CISSP objective 1.8."),
    ("e-threat-modeling-concepts", "threat-modeling-concepts", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Survey STRIDE, PASTA, OCTAVE, and attack trees, and choose the right methodology per situation. A free lesson in the security guidebook, serving CISSP objective 1.10."),
    ("e-supply-chain-risk", "supply-chain-risk", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Complete a vendor risk assessment ending in a residual-risk decision with owner and date. A free lesson in the security guidebook, serving CISSP objective 1.11."),
    ("e-awareness-training", "awareness-training", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Design a one-year security learning program measured by behavior change. A free lesson in the security guidebook, serving CISSP objective 1.12."),
    ("e-asset-classification", "asset-classification", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Build a four-tier classification scheme — tiers, examples, handling hooks, owners — anchored in impact per FIPS 199 and NIST SP 800-60. A free lesson in the security guidebook, serving CISSP objective 2.1."),
    ("e-handling-requirements", "handling-requirements", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Turn classification tiers into enforceable handling rules — labeling, storage, transmission, disposal — as a testable matrix. A free lesson in the security guidebook, serving CISSP objective 2.2."),
    ("e-asset-provisioning", "asset-provisioning", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Design a provisioning workflow with ownership assignment and run an inventory audit that reconciles against the CMDB. A free lesson in the security guidebook, serving CISSP objective 2.3."),
    ("e-data-lifecycle", "data-lifecycle", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · local demo run 2026-10-10",
     "Trace five data types across the lifecycle — roles, collection, location, retention, remanence, destruction per SP 800-88 Rev. 2 — with a live deletion-vs-overwrite demo. A free lesson in the security guidebook, serving CISSP objective 2.4."),
    ("e-retention-eol", "retention-eol", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Build a retention and destruction schedule with legal basis and computable triggers, plus legal-hold and secure-decommissioning procedures. A free lesson in the security guidebook, serving CISSP objective 2.5."),
    ("e-data-protection-controls", "data-protection-controls", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · local demo run 2026-10-10",
     "Select protective controls per data state — at rest, in transit, in use — with scoping, key management, DLP, and compliance mapping; the selection view above e-crypto-applied's primitives. A free lesson in the security guidebook, serving CISSP objective 2.6."),
    ("e-secure-design", "secure-design", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Apply the eight Saltzer and Schroeder design principles in an architecture review, trace requirements to controls, and survey platform capabilities for a deployment decision. A free lesson in the security guidebook, serving CISSP objectives 3.1, 3.3 and 3.4."),
    ("e-security-models", "security-models", "Stage E · Expert",
     "Walkthrough run 2026-10-10 · local stdlib Python, nothing external touched",
     "State the rules of Bell-LaPadula, Biba, Clark-Wilson, and Brewer-Nash, run a Bell-LaPadula rule check in Python, and write model-selection rationales. A free lesson in the security guidebook, serving CISSP objective 3.2."),
    ("e-control-selection", "control-selection", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Derive testable security requirements, select and tailor NIST SP 800-53 controls with written rationale, and defend the omissions. A free lesson in the security guidebook, serving CISSP objective 3.3."),
    ("e-platform-security", "platform-security", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Survey boot integrity, memory protection, virtualization isolation, and key storage across deployment options and write a conditional recommendation. A free lesson in the security guidebook, serving CISSP objective 3.4."),
    ("e-arch-vuln-assessment", "arch-vuln-assessment", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Decompose a hybrid cloud-plus-IoT-plus-API architecture, name per-component vulnerability classes, rate with structural judgment, and prioritize fixes. A free lesson in the security guidebook, serving CISSP objective 3.5."),
    ("e-cryptanalysis", "cryptanalysis", "Stage E · Expert",
     "Walkthrough run 2026-10-10 · local stdlib Python, nothing external touched",
     "Compute brute-force and birthday-bound estimates, demonstrate classical frequency analysis in Python, and pair every attack method with its defense. A free lesson in the security guidebook, serving CISSP objective 3.7."),
    ("e-facility-design", "facility-design", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Review a facility design against CPTED, layered defense, and site-selection factors, writing findings fixable at the design stage. A free lesson in the security guidebook, serving CISSP objective 3.8."),
    ("e-facility-controls", "facility-controls", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Complete a five-family facility controls checklist — perimeter, access, environmental, power, fire — with findings, owners, and dates. A free lesson in the security guidebook, serving CISSP objective 3.9."),
    ("e-system-lifecycle", "system-lifecycle", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Write a gate-review template with security deliverables per phase, complete one gate review to a go/no-go decision, and plan secure disposal. A free lesson in the security guidebook, serving CISSP objective 3.10."),
    ("e-network-architecture", "network-architecture", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Design network zones, trust boundaries, and zero-trust enforcement for a fictional manufacturer. A free lesson in the security guidebook, serving CISSP objective 4.1."),
    ("e-network-components", "network-components", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Harden firewalls, IDS/IPS, switches, wireless, and NAC with placement rationale for a fictional manufacturer. A free lesson in the security guidebook, serving CISSP objective 4.2."),
    ("e-secure-channels", "secure-channels", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Select TLS, VPN, SSH, and messaging channels per traffic class with written rationale for a fictional manufacturer. A free lesson in the security guidebook, serving CISSP objective 4.3."),
    ("e-auth-systems", "auth-systems", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Plan an MFA and passwordless rollout — phases, recovery, SSO migration, authenticator lifecycle — for a fictional company. A free lesson in the security guidebook, serving CISSP objective 5.6."),
    ("e-assessment-strategy", "assessment-strategy", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Write an annual assessment strategy: coverage tiers, assessor classes, cadence, and scoping rules for a fictional insurer. A free lesson in the security guidebook, serving CISSP objective 6.1."),
    ("e-control-testing", "control-testing", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Select and sequence control-testing methods — reviews, scans, validation — stating what each proves, for a fictional insurer. A free lesson in the security guidebook, serving CISSP objective 6.2."),
    ("e-security-metrics", "security-metrics", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Specify a SOC measurement program: KPI/KRI definitions, sources, collection, and cadence for a fictional insurer. A free lesson in the security guidebook, serving CISSP objective 6.3."),
    ("e-test-analysis-reporting", "test-analysis-reporting", "Stage E · Expert",
     "Local demo run and reviewed 2026-10-10 · transcript runs/e-test-analysis-reporting.log",
     "Triage findings, rate risk with context, and write the two-layer report with remediation tracking for a fictional insurer. A free lesson in the security guidebook, serving CISSP objective 6.4."),
    ("e-security-audits", "security-audits", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "Write an audit plan for one control family and complete a five-part finding for a fictional insurer. A free lesson in the security guidebook, serving CISSP objective 6.5."),
    ("e-investigation-forensics", "investigation-forensics", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "How to run investigations as a management and legal discipline — forensic readiness, evidence handling, chain of custody, and working with counsel and law enforcement. A free lesson in the security guidebook, serving CISSP objective 7.1."),
    ("e-logging-monitoring", "logging-monitoring", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "How to design the logging and monitoring program — event taxonomy, retention schedule, log integrity, and the SOC workflow that turns logs into detections. A free lesson in the security guidebook, serving CISSP objective 7.2."),
    ("e-config-management", "config-management", "Stage E · Expert",
     "Worked case authored and drift-demo run 2026-10-10 · local demo on fictional files, transcript in runs/e-config-management.log",
     "How to write a hardening baseline for a server role and operate drift detection against it — with a real local demo of the baseline-and-compare mechanism. A free lesson in the security guidebook, serving CISSP objective 7.3."),
    ("e-secops-concepts", "secops-concepts", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "How to apply need-to-know, least privilege, separation of duties, and defense in depth as daily operating decisions — plus a zero-trust gap assessment. A free lesson in the security guidebook, serving CISSP objective 7.4."),
    ("e-media-protection", "media-protection", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "How to protect the physical object — media inventory and labeling, custody in storage and transport, and sanitization per NIST SP 800-88. A free lesson in the security guidebook, serving CISSP objective 7.5."),
    ("e-incident-management", "incident-management", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "How to build the incident-management structure around the response lifecycle — team roles, escalation criteria, communications planning, and improvement metrics. A free lesson in the security guidebook, serving CISSP objective 7.6."),
    ("e-detective-preventive", "detective-preventive", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "How to choose, place, and tune detective and preventive controls in operation — IDS/IPS, honeypots, DLP, and allow-listing. A free lesson in the security guidebook, serving CISSP objective 7.7."),
    ("e-patch-management", "patch-management", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "How to run the patching operation — KEV-driven prioritization, severity-to-timeline SLAs, the exception register, and the emergency-patching runbook. A free lesson in the security guidebook, serving CISSP objective 7.8."),
    ("e-change-management", "change-management", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "How to run change management — the change request, CAB review with written rationale, change paths, and the emergency procedure that keeps a spine. A free lesson in the security guidebook, serving CISSP objective 7.9."),
    ("e-physical-security", "physical-security", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "How to run physical security day to day — guards and post orders, the badge lifecycle, mantraps and doors, CCTV operation, and environmental controls. A free lesson in the security guidebook, serving CISSP objective 7.14."),
    ("e-personnel-safety", "personnel-safety", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "How to protect the people — travel-security briefings, workplace-violence prevention, duress and check-in procedures. A free lesson in the security guidebook, serving CISSP objective 7.15."),
    # --- AI security track wave (2026-10-09) ---
    ("ai-llm-architecture", "llm-architecture", "AI track",
     "Walkthrough run 2026-10-09 · deterministic stack simulation, no model needed",
     "How LLM applications are built: tokens, embeddings, the transformer mechanism, the RAG/tool/agent stack — and the attack surface of every layer, mapped. A free lesson in the security guidebook, serving CAISP chapters 1–2."),
    ("ai-llm-top10", "llm-top10", "AI track",
     "Walkthrough run 2026-10-09 · deterministic classification drill, no model needed",
     "The OWASP LLM Top 10:2026 beyond prompt injection — data, system and agency risks, each with mechanism and defense. A free lesson in the security guidebook, serving CAISP chapter 3."),
    ("ai-supply-chain", "supply-chain", "AI track",
     "Walkthrough steps 1–5 run 2026-10-09 · step 6 (live keyless signing) not run by us",
     "AI supply chain security: provenance, hashes, CycloneDX AIBOMs, Sigstore keyless signing, and the pickle hazard — demonstrated locally. A free hands-on lesson in the security guidebook, serving CAISP chapter 6."),
    ("ai-governance", "ai-governance", "AI track",
     "Worked case authored and reviewed 2026-10-09 · no command line in this lesson",
     "Governing AI: the NIST AI RMF functions, the Generative AI Profile, EU AI Act risk tiers as concepts, and ISO/IEC 42001 noted as paid — applied to a full risk register. A free lesson in the security guidebook, serving CAISP chapter 7."),
    # --- Stage D specialist wave 1 (2026-10-09) ---
    ("d-redteam-concepts", "redteam-concepts", "Stage D · Specialist",
     "Walkthrough run 2026-10-09 · synthetic data on loopback; emulation tooling is reader-side in their own lab",
     "Red team operations concepts: ATT&CK as the behavior language (15 tactics, v19.2), C2 and evasion as concepts, what defenders see, and the purple-team loop — with beaconing statistics run locally. A free lesson in the security guidebook."),
    ("d-malware-analysis", "malware-analysis", "Stage D · Specialist",
     "Walkthrough run 2026-10-09 · synthetic benign training files only; real YARA via yara-python; detonation is reader-side in their isolated lab",
     "Malware analysis concepts: static vs dynamic, the triage workflow (hash, strings, entropy), YARA rule craft with false-positive discipline — demonstrated on synthetic samples with a real YARA engine. A free hands-on lesson in the security guidebook."),
    ("d-cloud-security", "cloud-security", "Stage D · Specialist",
     "Walkthrough run 2026-10-09 · local IAM policy analysis with Cloudsplaining; live-account scanning is reader-side in their own account",
     "Cloud security: the shared-responsibility line, IAM policies read as code, the classic misconfigurations, and posture auditing with Prowler and ScoutSuite — policies analyzed for real with Cloudsplaining. A free hands-on lesson in the security guidebook."),
    ("d-appsec", "appsec", "Stage D · Specialist",
     "Walkthrough run 2026-10-09 · STRIDE worked case + teaching-sketch SAST with triage; real Semgrep step re-ran 2026-10-10; ZAP step is reader-side",
     "Application security: STRIDE threat modeling, the SAST/DAST/IAST/SCA scanner families and their blind spots, secure-SDLC integration, and code-review technique — with a scanner-blind-spot demo run locally. A free hands-on lesson in the security guidebook."),
    # --- Stage B mechanics wave (2026-10-09) ---
    ("b-authorization-scope", "authorization-scope", "Stage B · Practitioner",
     "Worked case authored and reviewed 2026-10-09 · no command line in this lesson",
     "Authorization, scope, and the hard rules: the gating lesson — written authorization, rules-of-engagement contents, the law in plain terms, and the six hard rules quoted verbatim. A free lesson in the security guidebook."),
    ("b-methodology", "methodology", "Stage B · Practitioner",
     "Worked case authored and reviewed 2026-10-09 · no command line in this lesson",
     "Engagement methodology: OWASP WSTG, PTES, and NIST SP 800-115, and the six phases from scoping to reporting — the repeatable process behind every engagement. A free lesson in the security guidebook."),
    ("b-toolbench", "toolbench", "Stage B · Practitioner",
     "Walkthrough run 2026-10-09 · loopback only; nmap/Semgrep/Chromium steps re-ran 2026-10-10; remaining tools marked not run by us with reader procedures",
     "The toolbench: fifteen tool phases in activation order — for each, the one question it answers, the free tool that answers it, and what it cannot tell you. A free hands-on lesson in the security guidebook."),
    ("b-practice-targets", "practice-targets", "Stage B · Practitioner",
     "Procedures verified against the projects' own READMEs 2026-10-09 · container runs not run by us (no Docker on the build machine)",
     "Setting up practice targets locally: DVWA, Juice Shop, WebGoat, crAPI and DVGA, one verified command each, bound to localhost — so you never need a live system. A free lesson in the security guidebook."),
    # --- Stage A remainder wave (2026-10-09) ---
    ("a-python-security", "python-security", "Stage A · Foundations",
     "Walkthrough run 2026-10-09 · Python 3.12.3, loopback only, stdlib only, nothing external touched",
     "Python for security tooling: reading and changing small scripts — HTTP requests, response parsing, sockets, arguments and files — with every walkthrough step run locally. A free hands-on lesson in the security guidebook."),
    ("a-reading-code", "reading-code", "Stage A · Foundations",
     "Walkthrough run 2026-10-09 · labeled teaching snippets, local string-trace only, nothing executed against a database",
     "Reading code through a vulnerability: tracing untrusted input from a JavaScript form to a SQL query — source, path, sink — with the injection located by reading. A free lesson in the security guidebook."),
    ("a-windows-concepts", "windows-concepts", "Stage A · Foundations",
     "Hands-on steps not run by us (no Windows on the build machine) · Microsoft docs fetched and verified 2026-10-09",
     "Windows concepts for security: the registry, services, event logs and PowerShell — the Linux lesson's concepts in Windows form, taught from Microsoft's own docs with exact reader procedures. A free lesson in the security guidebook."),
    ("a-osint-research", "osint-research", "Stage A · Foundations",
     "Walkthrough run 2026-10-09 · fictional target, local files only, passive recon — no real target touched",
     "OSINT and research discipline: passive vs active recon, what 'public' means, the standard sources, and documentation a stranger can re-derive — on a fictional target. A free lesson in the security guidebook."),
    # --- AI track completion + program leadership (2026-10-09) ---
    ("ai-pipeline", "ai-pipeline", "AI track",
     "Walkthrough run 2026-10-09 · deterministic pipeline simulation, no model, no network",
     "AI attacks and defenses in the build pipeline: training-data poisoning, build provenance, registry hygiene, and the red-team CI gate — each attack taught with the defense that catches it. A free hands-on lesson in the security guidebook, serving CAISP chapter 4."),
    ("ai-threat-modeling", "threat-modeling-ai", "AI track",
     "Worked case authored and reviewed 2026-10-09 · no command line in this lesson",
     "Threat modeling AI systems: data-flow mapping, trust boundaries at the prompt, retrieval and tool layers, STRIDE adapted to AI, and MITRE ATLAS as the attacker's library — a complete worked threat model. A free lesson in the security guidebook, serving CAISP chapter 5."),
    ("e-security-program", "security-program", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-09 · no command line in this lesson",
     "Running a security program: strategy in the Govern loop, the metrics that matter vs vanity metrics (KPI vs KRI), risk-based prioritization, and the program charter as the worked artifact. A free lesson in the security guidebook."),
    ("e-board-communication", "board-communication", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-09 · no command line in this lesson",
     "Board-level communication: translating technical risk into business decisions — the one-page board memo as the worked artifact, what to report, what to leave out, and the director test. A free lesson in the security guidebook."),
    # --- Final wave: Stage D wave 2 + Stage C remainder (2026-10-09) ---
    ("d-dfir-deep", "dfir-deep", "Stage D · Specialist",
     "Walkthrough run 2026-10-09 · labeled synthetic evidence; tool runs on real images are reader-side in their own lab",
     "DFIR deep: disk, memory and network forensics — the order of volatility, evidence handling, timeline construction from labeled data, and hypothesis-driven threat hunting. A free hands-on lesson in the security guidebook."),
    ("d-exploit-concepts", "exploit-concepts", "Stage D · Specialist",
     "Walkthrough run 2026-10-09 · mitigation mechanics demonstrated live (ASLR, checksec survey); exploitation technique is reader-side on pwn.college",
     "Exploit development and reverse engineering concepts: how a flaw becomes control of execution, and the mitigation landscape (NX, ASLR, canaries, RELRO) that makes it expensive — demonstrated live, training targets only. A free lesson in the security guidebook."),
    ("c-public-track-record", "public-track-record", "Stage C · Professional",
     "Worked write-up authored and reviewed 2026-10-09 · no command line in this lesson",
     "Building a public track record: write-ups that teach — root cause first, mechanism re-derivable, honest impact — the Project Zero bar, one finding in two formats. A free lesson in the security guidebook."),
    ("c-ai-tooling", "ai-tooling", "Stage C · Professional",
     "Evidence map authored 2026-10-09 · CVP details dated 2026-10-06 (announcement); primary URL to re-fetch at publish",
     "AI tooling professionals use: Anthropic's Cyber Verification Program as the dated worked example — three tiers, what each admits, and why it is access to tooling, never a credential. A free lesson in the security guidebook."),
    # --- Governance-framework lessons (2026-10-10) ---
    ("e-csf-20", "csf-20", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "NIST Cybersecurity Framework 2.0: outcomes not actions — the 6 Functions, 22 Categories, Current-vs-Target profiles, and Tiers, with a worked gap assessment. A free lesson in the security guidebook."),
    ("e-iso27001", "iso27001", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "ISO/IEC 27001:2022: the ISMS, Clauses 4–10, the 93-control Annex A catalog, and the Statement of Applicability — taught from free sources (the standard is paid). A free lesson in the security guidebook."),
    ("e-soc2", "soc2", "Stage E · Expert",
     "Worked case authored and reviewed 2026-10-10 · no command line in this lesson",
     "SOC 2 and the Trust Services Criteria: the examination engagement, the five criteria, Type I vs Type II, and how to scope it — with a worked scoping memo. A free lesson in the security guidebook."),
]

# lesson id -> site-relative url, for cross-linking (map.md dependency graph)
LINKMAP = {lid: f"/g/{slug}/" for lid, slug, *_ in LESSONS}

TOTAL = len(LESSONS)

# Stage pages (brief §4): the novice-to-expert backbone. Each row:
# (stage_key, slug, stage_label, title, lede, milestone_html, claims_html,
#  next_url, next_label, [lesson ids in reading order])
STAGES = [
    ("A", "stage-a", "Stage A · Foundations", "Stage A — Foundations",
     "The ground everything else stands on: how a computer runs programs and controls access, what actually crosses the wire when two machines talk, the protocol every web attack and defense is built on, enough Python to read and change the small tools the field runs on, how to follow a vulnerability through source code, and what the cryptographic primitives do — and what breaks when they are misused.",
     "Explain, <strong>packet by packet</strong>, what happens between pressing &ldquo;log in&rdquo; and the page rendering: the DNS lookup, the TCP handshake, the TLS handshake, the HTTP request and response, the cookie or token that carries identity, and the bytes on the wire at each step.",
     "After Stage A you can honestly claim: <strong>nothing yet</strong> — and that is the point. This is the brief's own reasoning, not a verdict on your effort: foundations are prerequisites, not proof of skill. The checkable evidence starts in Stage B. What you <em>can</em> say is that you can explain the login-to-render path from first principles, with no term you cannot unpack.",
     "/g/stage-b/", "Stage B — Practitioner",
     ["a-dns-depth", "a-tcpip-ports", "a-linux-cli", "a-windows-concepts",
      "a-git-github", "a-http-depth", "a-python-security", "a-reading-code",
      "a-osint-research"]),
    ("B", "stage-b", "Stage B · Practitioner", "Stage B — Practitioner",
     "Doing the work under authorization: the hard rules and scope discipline that make everything legal, engagement methodology, the toolbench in activation order, the web vulnerability classes found, reproduced and fixed one by one, defensive basics, and how authorized testing is actually offered to beginners through bug bounty programs.",
     "A <strong>first valid finding submitted to a program that authorizes testing</strong> — in scope, reproducible by a stranger following your steps, with the impact argued honestly.",
     "You can honestly claim: you have found, reproduced, and fixed real vulnerability classes on targets you were authorized to test, and you can write a triage-ready report. You cannot yet claim: professional experience, any certification, or readiness for unsupervised work. Stage B is the <em>first</em> evidence, not the last.",
     "/g/stage-c/", "Stage C — Professional",
     ["b-authorization-scope", "b-methodology", "b-toolbench", "b-practice-targets",
      "b-idor", "b-sqli", "b-command-injection", "b-ssrf", "b-csrf", "b-xss",
      "b-business-logic", "b-session-auth", "b-security-headers", "b-bug-bounty"]),
    ("C", "stage-c", "Stage C · Professional", "Stage C — Professional",
     "Working like a professional: the defender's side — SOC triage, log sources, detection engineering, incident response — plus coordinated disclosure end to end, the CVE program and how credit works, severity scoring by hand, the vulnerability catalogs, and building the public track record the whole program's premise rests on.",
     "A <strong>coordinated disclosure completed</strong>, and a <strong>CVE record that credits you</strong> — a public, permanent entry with your name on it.",
     "You can honestly claim: you have reported a real flaw responsibly and can point to the public record; you can score severity and prioritize like a professional. You cannot yet claim: specialization depth — that is Stage D — or managerial breadth — that is Stage E.",
     "/g/stage-d/", "Stage D — Specialist",
     ["c-soc-triage", "c-log-sources", "c-sigma-detection", "c-incident-response",
      "c-cvd", "c-cve-program", "c-cvss", "c-vuln-ecosystem",
      "c-public-track-record", "c-ai-tooling"]),
    ("D", "stage-d", "Stage D · Specialist", "Stage D — Specialist",
     "One track, taken deep: red team operations, DFIR and detection engineering, application security, exploit development and reverse engineering, malware analysis, or cloud security. Each track is concepts plus defender telemetry plus established labs — the safety line holds all the way down.",
     "A <strong>capstone body of work in one track</strong>: original, public, verifiable — the level-4 work each role path ends in. (The brief sets no single artifact for Stage D; the milestone is the depth itself.)",
     "You can honestly claim: deep, demonstrable skill in one specialty, with public artifacts to prove it. You cannot yet claim: breadth across the field — the specialist knows their track cold and knows where its edges are.",
     "/g/stage-e/", "Stage E — Expert",
     ["d-redteam-concepts", "d-malware-analysis", "d-cloud-security",
      "d-appsec", "d-exploit-concepts", "d-dfir-deep"]),
    ("E", "stage-e", "Stage E · Expert", "Stage E — Expert",
     "Managerial and architectural breadth: the eight CISSP domains as bodies of knowledge, the governance frameworks organizations buy, and the work of the person who owns security — strategy, metrics, and board-level communication.",
     "<strong>Breadth across the whole field</strong>: you can reason about a security program end to end — risk, architecture, governance, leadership — from the primary sources.",
     "You can honestly claim: you have studied each CISSP domain's body of knowledge and can work from the primary sources. You cannot claim: the CISSP certification itself — full certification needs five cumulative years of experience in two or more domains (one year waivable by degree or approved credential); passing without it makes you an Associate of ISC2. Nor can you claim a title like CISO — these lessons teach the work, not the title.",
     "/g/", "The AI security track",
     ["e-risk-assessment",
      "e-ethics", "e-security-concepts", "e-governance", "e-cyber-law",
      "e-investigations", "e-policy-docs", "e-personnel-security",
      "e-threat-modeling-concepts", "e-supply-chain-risk", "e-awareness-training",
      "e-asset-classification", "e-handling-requirements", "e-asset-provisioning",
      "e-data-lifecycle", "e-retention-eol", "e-data-protection-controls",
      "e-secure-design", "e-security-models", "e-control-selection",
      "e-platform-security", "e-arch-vuln-assessment", "e-crypto-applied",
      "e-cryptanalysis", "e-facility-design", "e-facility-controls",
      "e-system-lifecycle",
      "e-network-architecture", "e-network-components", "e-secure-channels",
      "e-iam", "e-auth-systems",
      "e-assessment-strategy", "e-control-testing", "e-security-metrics",
      "e-test-analysis-reporting", "e-security-audits",
      "e-investigation-forensics", "e-logging-monitoring", "e-config-management",
      "e-secops-concepts", "e-media-protection", "e-incident-management",
      "e-detective-preventive", "e-patch-management", "e-change-management",
      "e-physical-security", "e-personnel-safety",
      "e-sdlc", "e-bcp-drp", "e-security-program", "e-board-communication",
      "e-csf-20", "e-iso27001", "e-soc2"]),
]

STAGEMAP = {key: f"/g/{slug}/" for key, slug, *_ in STAGES}

TLD = r"(?:education|college|org|com|dev|net|io|gov|se|uk|info|edu|eu|ch|ai|one|app|co)(?![A-Za-z0-9-])"
DOMAIN_RE = re.compile(
    r"(?<![\w/@])"                      # not mid-word, not inside an href
    r"(\()?((?:[A-Za-z0-9-]+\.)+" + TLD + r"(?:/[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]*)?)"
    r"(\))?"
)

def linkify(text: str) -> str:
    """Turn bare domain.tld/path tokens into real links. Assumes code spans
    and existing <a> tags are already protected as placeholders."""
    def sub(m):
        url = m.group(2).rstrip(".,;:!?")
        # A trailing ")" is the prose paren, not part of the URL, unless parens balance.
        while url.endswith(")") and url.count("(") < url.count(")"):
            url = url[:-1]
        trail = m.group(2)[len(url):]
        open_p, close_p = m.group(1) or "", m.group(3) or ""
        return f'{open_p}<a href="https://{url}">{html.escape(url)}</a>{trail}{close_p}'
    return DOMAIN_RE.sub(sub, text)

def inline(text: str) -> str:
    """Inline markdown: `code`, **bold**, *italic*, then bare-domain linkify.
    Code spans are protected from the other passes."""
    codes = []
    def stash(m):
        codes.append(m.group(1))
        return f"\x00CODE{len(codes)-1}\x00"
    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    # lesson-id backticks became \x00CODE markers; handle linkmap on restore
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = linkify(text)
    def restore(m):
        code = codes[int(m.group(1))]
        if code in LINKMAP:  # cross-link known lesson ids (map.md graph)
            return f'<a href="{LINKMAP[code]}"><code>{html.escape(code)}</code></a>'
        return f"<code>{html.escape(code)}</code>"
    text = re.sub(r"\x00CODE(\d+)\x00", restore, text)
    return text

def md_to_html(md: str) -> str:
    """Convert one lesson's markdown body to HTML. Handles the constructs the
    lessons actually use: ##/### headers, fenced code, blockquote, - and 1.
    lists, paragraphs. Returns the body HTML without the h1/meta header."""
    lines = md.split("\n")
    out = []
    i = 0
    in_ul = in_ol = False
    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul: out.append("</ul>"); in_ul = False
        if in_ol: out.append("</ol>"); in_ol = False
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            close_lists()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1  # closing fence
            out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
            continue
        if s.startswith("## "):
            close_lists()
            out.append(f"<h2>{inline(s[3:])}</h2>")
        elif s.startswith("### "):
            close_lists()
            out.append(f"<h3>{inline(s[4:])}</h3>")
        elif s.startswith("> "):
            close_lists()
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[2:]); i += 1
            out.append('<div class="note">' + " ".join(inline(b) for b in buf) + "</div>")
            continue
        elif re.match(r"^[-*] ", s):
            if in_ol: out.append("</ol>"); in_ol = False
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append(f"<li>{inline(s[2:])}</li>")
        elif re.match(r"^\d+\. ", s):
            if in_ul: out.append("</ul>"); in_ul = False
            if not in_ol: out.append("<ol>"); in_ol = True
            out.append(f"<li>{inline(re.sub(r'^\d+\. ', '', s))}</li>")
        elif s == "" or s == "---":
            close_lists()
        else:
            close_lists()
            out.append(f"<p>{inline(s)}</p>")
        i += 1
    close_lists()
    return "\n".join(out)

def parse_lesson(lid: str):
    """Split a lesson md into (title, meta_html_ledger_rows, body_html)."""
    md = (GUIDEBOOK / "lessons" / f"{lid}.md").read_text()
    title = re.match(r"# (.+)", md).group(1)
    # meta line: **ID:** `x` · **Stage:** ... · **Level:** ... · **Prerequisites:** ...
    meta_line = [l for l in md.split("\n") if l.startswith("**ID:**")][0]
    meta = {}
    for key in ("Stage", "Level", "Prerequisites"):
        m = re.search(rf"\*\*{key}:\*\*\s*(.+?)(?=\s*·\s*\*\*|\s*$)", meta_line)
        if m: meta[key] = m.group(1).strip().rstrip(".")
    # map-ref line (optional)
    mapref = ""
    for l in md.split("\n"):
        if l.startswith("**Map ref") or l.startswith("**Map refs"):
            mapref = re.sub(r"^\*\*Map refs?:\*\*\s*", "", l).strip()
            break
    # body: drop h1, meta line, mapref line, and the first --- rule
    body_lines = []
    skipped_rule = False
    for l in md.split("\n"):
        if l.startswith("# ") or l.startswith("**ID:**") or l.startswith("**Map ref"):
            continue
        if l.strip() == "---" and not skipped_rule:
            skipped_rule = True; continue
        body_lines.append(l)
    body_html = md_to_html("\n".join(body_lines).strip())
    # lede = first paragraph of section 1 ("Where this shows up")
    lede_m = re.search(r"<h2>1\. Where this shows up</h2>\s*<p>(.*?)</p>", body_html, re.S)
    lede = lede_m.group(1) if lede_m else ""
    rows = [("Stage", meta.get("Stage", "")), ("Level", meta.get("Level", "")),
            ("Prerequisites", meta.get("Prerequisites", ""))]
    if mapref: rows.append(("Map references", mapref))
    ledger = "".join(
        f'<tr><th scope="row">{html.escape(k)}</th><td>{inline(v)}</td></tr>'
        for k, v in rows)
    return title, lede, ledger, body_html

def page_shell(*, title, description, canonical, crumbs, breadcrumb_json, main_html):
    css = (REPO / "index.html").read_text().split("<style>")[1].split("</style>")[0]
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | Learn Computer Stuff</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{html.escape(title)} | Learn Computer Stuff"><meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="website"><meta property="og:url" content="{canonical}">
<style>{css}</style><script type="application/ld+json">{breadcrumb_json}</script>
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
<a class="brand" href="/"><span class="seal-dot" aria-hidden="true"></span>Learn Computer Stuff</a><nav class="top" aria-label="Main"><a href="/f/">Careers</a><a href="/method/">Method</a><a class="btn" href="/start/">Start here</a></nav>
</div></header>
<div class="wrap"><div class="crumbs">{crumbs}</div></div>
<main id="main"><div class="wrap">
{main_html}
</div></main>
<footer class="site"><div class="wrap"><div class="cols">
<div><strong>Learn Computer Stuff</strong><br>The free route in, and what the certificates really cost.</div>
<div><a href="/f/">All careers</a><br><a href="/start/">Start here</a><br><a href="/method/">How we verify</a></div>
<div>Claims here carry the date they were checked, or say plainly that they were not — an entry added by hand reads <em>operator-added</em> rather than borrowing a date it never earned.</div>
</div></div></footer>
</body></html>
"""

def breadcrumb(items):
    els = [{"@type": "ListItem", "position": n + 1, "name": name, "item": url}
           for n, (name, url) in enumerate(items)]
    import json
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                       "itemListElement": els}, separators=(",", ":"))

def build_lesson(lid, slug, stage_label, dateline_note, description):
    title, lede, ledger, body = parse_lesson(lid)
    nword = numword(TOTAL)
    canonical = f"https://learncomputerstuff.dev/g/{slug}/"
    crumbs = (f'<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / '
              f'<span>{html.escape(title)}</span>')
    # stage_label like "Stage A · Foundations" -> /g/stage-a/
    _skey = stage_label.split("·")[0].strip().split()[-1] if "·" in stage_label else None
    _slink = (f' Part of <a href="{STAGEMAP[_skey]}">{html.escape(stage_label)}</a>.' if _skey in STAGEMAP else "")
    # section 10 heading gets the lesson's real name kept; body carries links
    main = f"""<section>
<span class="eyebrow">Security guidebook · {html.escape(stage_label)}</span><h1>{html.escape(title)}</h1>
<p class="lede prose">{lede}</p>
<p class="dateline">Lesson published {TODAY} · {html.escape(dateline_note)}</p>
<table class="ledger"><tbody>
{ledger}
</tbody></table>
</section>
<section style="padding-top:0">
{body}
</section>
<section><div class="note"><span class="eyebrow">Keep going</span>
<p class="prose">This lesson is one of {nword} in the security guidebook.{_slink} <a href="/g/">See all {nword} lessons →</a></p></div></section>"""
    out = REPO / "g" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_shell(
        title=title, description=description, canonical=canonical,
        crumbs=crumbs,
        breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                    ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                    (title, canonical)]),
        main_html=main))
    print(f"wrote {out} ({len(out.read_text())} bytes)")

def build_index():
    doors = []
    for lid, slug, stage_label, _note, _desc in LESSONS:
        title, lede, _ledger, _body = parse_lesson(lid)
        # one-sentence door text: reuse the title + stage
        doors.append(
            f'<a class="door" href="/g/{slug}/"><h3>{html.escape(title)}</h3>'
            f'<p><span class="eyebrow">{html.escape(stage_label)}</span></p>'
            f'<p>{lede[:220].rsplit(" ", 1)[0]}…</p></a>')
    canonical = "https://learncomputerstuff.dev/g/"
    main = f"""<section>
<span class="eyebrow">New · hands-on, free, no account needed</span><h1>The security guidebook</h1>
<p class="lede prose">A complete cybersecurity education, taught the way the work actually happens: you run the commands, reproduce the findings, fix the flaws, and write the reports — every walkthrough executed and dated, every claim checked against its source. {numword(TOTAL).capitalize()} lessons are live now: the Stage A foundations, the Stage A remainder (Python, reading code, Windows, OSINT), the pilots, the Stage B mechanics wave (authorization, methodology, toolbench, practice targets), the Stage B web-vulnerability wave, the Stage C detection-and-operations wave, the Stage C disclosure wave, the Stage E CISSP-domain wave, the Stage D specialist wave (red team, malware, cloud, AppSec), the Stage D wave 2 (exploit concepts, DFIR deep), the Stage C remainder (public track record, AI tooling), the AI security track, and the CISSP coverage wave (all 62 objectives, 1.1 to 8.5, each with its lesson); the full program builds out from here, stage by stage.</p>
<p class="dateline">Published {TODAY} · walkthroughs run 2026-10-09</p>
<div class="note"><span class="eyebrow">How a lesson is built</span>
<p class="prose">Every lesson follows the same ten parts: where it shows up, what you need first, how it works, a guided walkthrough, work on your own, where it goes wrong, the primary sources, check-yourself questions, a proof-of-skill artifact, and where it leads next. If a step could not be run, the lesson says so on the page.</p></div>
</section>
<section><h2>The lessons</h2>
<div class="grid">
{"".join(doors)}
</div>
<p class="muted" style="margin-top:1rem">Reading order: DNS → TCP/IP → Linux CLI → Windows concepts → Git &amp; GitHub → HTTP in depth → Python for security → Reading code → OSINT &amp; research discipline → Authorization &amp; scope → Methodology → Toolbench → Practice targets → IDOR → SQL injection → Command injection → SSRF → CSRF → XSS → Business-logic flaws → Session &amp; auth → Security headers → Bug bounty mechanics → SOC triage → Log sources → Sigma detection → Incident response → Coordinated disclosure → CVE Program → CVSS → Vulnerability ecosystem → IAM → Applied crypto → Secure SDLC → BCP/DR. AI track: Prompt injection → LLM architecture → LLM Top 10 → Supply chain → AI governance → AI pipeline → AI threat modeling. Risk assessment → IAM → Applied crypto → Secure SDLC → BCP/DR → Security program → Board communication. Stage D wave 1: Red team concepts → Malware analysis → Cloud security → AppSec. Stage D wave 2: Exploit concepts → DFIR deep. Stage C remainder: Vulnerability ecosystem → Public track record → AI tooling. AI track: Prompt injection → LLM architecture → LLM Top 10 → Supply chain → AI governance → AI pipeline → AI threat modeling.</p>
</section>
<section><h2>The stages</h2>
<div class="grid">
<a class="door" href="/g/stage-a/"><h3>Stage A — Foundations</h3><p><span class="eyebrow">Novice to grounded</span></p><p>The login-to-render path, packet by packet…</p></a>
<a class="door" href="/g/stage-b/"><h3>Stage B — Practitioner</h3><p><span class="eyebrow">First valid finding</span></p><p>Authorized testing, vulnerability classes, triage-ready reports…</p></a>
<a class="door" href="/g/stage-c/"><h3>Stage C — Professional</h3><p><span class="eyebrow">Disclosure and credit</span></p><p>Coordinated disclosure, CVE records, detection work…</p></a>
<a class="door" href="/g/stage-d/"><h3>Stage D — Specialist</h3><p><span class="eyebrow">One track, deep</span></p><p>Red team, DFIR, AppSec, exploit dev, malware, cloud…</p></a>
<a class="door" href="/g/stage-e/"><h3>Stage E — Expert</h3><p><span class="eyebrow">Breadth and leadership</span></p><p>CISSP domains, governance, running a security program…</p></a>
</div>
<p class="muted" style="margin-top:1rem">Each stage page states the stage's goal, its milestone, and what a reader can and cannot honestly claim after it.</p>
</section>
<section><h2>Role paths</h2>
<div class="grid">
<a class="door" href="/g/paths/"><h3>All eight role paths</h3><p><span class="eyebrow">Pick the job, follow the plan</span></p><p>SOC analyst, security analyst, pentester, AppSec, DFIR, cloud security, IAM, GRC \u2014 each with ordered lessons, checkpoints, and a level-4 capstone\u2026</p></a>
</div>
</section>
<section><h2>Knowledge maps</h2>
<div class="grid">
<a class="door" href="/g/map-cissp/"><h3>CISSP knowledge map</h3><p><span class="eyebrow">Every objective, 1.1 to 8.5</span></p><p>Each objective points to the lesson that teaches it \u2014 or is logged as a gap\u2026</p></a>
<a class="door" href="/g/map-caisp/"><h3>CAISP knowledge map</h3><p><span class="eyebrow">Seven chapters</span></p><p>Each chapter points to the lessons that teach it\u2026</p></a>
</div>
</section>
<section><h2>How we verify</h2>
<p class="prose">The same rules as the rest of this site: <a href="/method/">no verification URL, no row</a>. Every walkthrough command was executed in a clean local environment and the transcript kept; where a step could not run — no Docker, no local model, no packet capture, no UDP loopback on the build machine — the lesson marks it <strong>not run by us</strong> instead of pretending.</p>
</section>"""
    out = REPO / "g" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_shell(
        title="The security guidebook",
        description=f"A free, hands-on cybersecurity program: run the commands, reproduce the findings, fix the flaws. {numword(TOTAL).capitalize()} lessons live now — Stage A foundations, the Stage A remainder, pilots, the Stage B mechanics wave, the Stage B web-vulnerability wave, the Stage C detection-and-operations wave, the Stage C disclosure wave, the Stage E CISSP-domain wave, the Stage D specialist wave, and the AI security track — plus the CISSP coverage wave (all 62 objectives).",
        canonical=canonical,
        crumbs='<a href="/">Home</a> / <span>Security guidebook</span>',
        breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                    ("Security guidebook", canonical)]),
        main_html=main))
    print(f"wrote {out}")

def build_stage_pages():
    for key, slug, stage_label, title, lede, milestone, claims, next_url, next_label, lids in STAGES:
        doors = []
        for n, lid in enumerate(lids, 1):
            ltitle, llede, _ledger, _body = parse_lesson(lid)
            lslug = LINKMAP[lid]
            doors.append(
                f'<a class="door" href="{lslug}"><h3>{n}. {html.escape(ltitle)}</h3>'
                f'<p>{llede[:220].rsplit(" ", 1)[0]}…</p></a>')
        canonical = f"https://learncomputerstuff.dev/g/{slug}/"
        main = f"""<section>
<span class="eyebrow">{html.escape(stage_label)}</span><h1>{html.escape(title)}</h1>
<p class="lede prose">{html.escape(lede)}</p>
<p class="dateline">Published {TODAY} · generated from the lesson data</p>
</section>
<section><h2>The milestone</h2>
<p class="prose">{milestone}</p>
</section>
<section><h2>The lessons</h2>
<div class="grid">
{"".join(doors)}
</div>
<p class="muted" style="margin-top:1rem">In reading order, {len(lids)} lessons. Every lesson follows the same ten parts — mechanism, walkthrough, sources, proof — and every walkthrough was executed and dated.</p>
</section>
<section><h2>What you can honestly claim</h2>
<p class="prose">{claims}</p>
</section>
<section><h2>What comes next</h2>
<p class="prose">When the milestone is met, continue to <a href="{next_url}">{html.escape(next_label)}</a>.</p>
</section>"""
        out = REPO / "g" / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_shell(
            title=f"{title} | The security guidebook",
            description=f"{title}: the stage's goal, its milestone, and what a reader can and cannot honestly claim after it. {len(lids)} free lessons. A free page in the security guidebook.",
            canonical=canonical,
            crumbs=f'<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / <span>{html.escape(title)}</span>',
            breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                        ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                        (title, canonical)]),
            main_html=main))
        print(f"wrote {out}")

# ================= Role paths (brief §4) =================
# One per role: the ordered plan through the lessons, with checkpoints and a
# level-4 capstone. Each existing /r/<role>/ page links to its path.
# (role_key, slug, role_title, job_html, groups, checkpoints, capstone_title, capstone_html)
# groups: [(group_label, [items])]; items are lesson ids or ("note", html) tuples.
PATHS = [
    ("soc-analyst", "soc-analyst", "SOC analyst",
     "You watch the alerts, work out which ones matter, and investigate the ones that do. It is shift-based work, usually reached via IT support or networking rather than straight off the street. It suits people who enjoy investigation \u2014 noticing the odd detail, chasing it down, and writing up what happened clearly enough that someone else can act on it.",
     [("Foundations", ["a-linux-cli", "a-tcpip-ports", "a-dns-depth", "a-http-depth", "a-windows-concepts",
                        ("note", "Lighter on cryptography internals than the pentester path \u2014 you need the vocabulary, not the math.")]),
      ("Detection basics", ["c-soc-triage", "c-log-sources", "c-sigma-detection", "c-incident-response"]),
      ("Deeper", ["d-dfir-deep", "d-redteam-concepts",
                  ("note", "ATT&CK is the vocabulary every alert and report on this path is written in.")])],
     ["Triage a labeled set of simulated alerts and write a disposition for each: true positive, false positive, or benign \u2014 with a one-line reason a stranger could check.",
      "Run a home SOC lab on your own machines and produce three investigation write-ups a stranger can follow end to end.",
      "Write a Sigma rule, trigger it deliberately, and document what it misses \u2014 the blind spots are part of the deliverable."],
     "Published detection-engineering project",
     "A <strong>Sigma rule package for one ATT&CK technique, with test evidence</strong>, plus a <strong>written investigation of a simulated intrusion mapped to ATT&CK</strong> \u2014 in a public repository, reproducible by a stranger. That is the artifact a hiring stranger checks."),
    ("security-analyst", "security-analyst", "Security analyst",
     "You work out what an attacker did, or is doing, and write it up so someone can act. It is the broader analysis role next to the SOC\u2019s shift-based entry point: ATT&CK is the working vocabulary and CISA advisories are the reading diet. It suits people who chase loose ends and can write clearly under time pressure.",
     [("Foundations", ["a-linux-cli", "a-tcpip-ports", "a-dns-depth", "a-http-depth", "a-python-security", "a-windows-concepts"]),
      ("Practitioner", ["b-authorization-scope", "b-methodology", "b-idor", "b-sqli", "b-xss", "b-session-auth",
                        ("note", "Studied to Apply level \u2014 you must understand exploitation to analyze it, even though you are not the one breaking in.")]),
      ("Professional, lighter", ["c-cve-program", "c-cvss", "c-vuln-ecosystem", "c-public-track-record",
                                 ("note", "Disclosure literacy and write-up craft, not CVE-chasing: the full disclosure pipeline is optional on this path.")]),
      ("Detection and DFIR", ["c-soc-triage", "c-log-sources", "c-sigma-detection", "d-dfir-deep", "d-redteam-concepts"])],
     ["An investigation of a simulated incident written up in ATT&CK vocabulary, with the evidence chain a stranger can re-derive.",
      "A detection rule written and tested against labeled data, with the tuning decisions documented.",
      "A one-page threat brief from a current CISA advisory, written for a non-technical manager."],
     "Published original threat analysis",
     "A <strong>technique deep-dive with detection logic and test evidence</strong>, or a <strong>detection pack derived from a real advisory series</strong> \u2014 published, sources dated, reproducible. That is the artifact a hiring stranger checks."),
    ("pentester", "pentester", "Penetration tester",
     "You are paid to break in \u2014 with permission and in writing \u2014 and then explain exactly how. It is open without a degree and cares about demonstrable skill more than almost any other field here, but it is rarely entry-level: people tend to arrive from help desk, networking, sysadmin, or defensive security. The hardest part is the report, not the exploit.",
     [("Foundations, full depth", ["a-linux-cli", "a-tcpip-ports", "a-dns-depth", "a-http-depth", "a-python-security", "a-reading-code", "a-osint-research", "a-git-github", "a-windows-concepts"]),
      ("Practitioner, full", ["b-authorization-scope", "b-methodology", "b-toolbench", "b-practice-targets",
                              "b-idor", "b-sqli", "b-command-injection", "b-ssrf", "b-csrf", "b-xss",
                              "b-business-logic", "b-session-auth", "b-security-headers", "b-bug-bounty"]),
      ("Professional, full", ["c-cvd", "c-cve-program", "c-cvss", "c-vuln-ecosystem", "c-public-track-record"]),
      ("Specialist", ["d-redteam-concepts", "d-exploit-concepts",
                      ("note", "Exploit development stays at concepts plus mitigations here; hands-on technique is reader-side on pwn.college, per the safety line.")])],
     ["The PortSwigger Web Security Academy core labs, completed \u2014 the free standard the industry actually respects.",
      "A first valid finding submitted to a program that authorizes testing \u2014 in scope, reproducible, impact argued honestly.",
      "A full pentest report on a lab target: the scope record, findings with business impact, remediation, and proof you stayed in scope."],
     "Published original work at professional standard",
     "One of: a <strong>coordinated disclosure with CVE credit</strong>, a <strong>novel technique-variation write-up</strong>, or a <strong>meaningful open-source tool contribution</strong> \u2014 with the full engagement report (scope record, findings, business impact, remediation) as the artifact. That is what a hiring stranger checks."),
    ("appsec", "appsec", "Application security engineer",
     "You stop vulnerabilities from being written rather than finding them after they ship. It is two disciplines \u2014 code and security \u2014 and you cannot fake either: the most common route is a few years of development followed by a deliberate turn toward security.",
     [("Code fluency first", ["a-python-security", "a-reading-code", "a-git-github", "a-linux-cli",
                               ("note", "The role page is explicit: read and write code well before the security layer means anything. Do not skip this block.")]),
      ("HTTP and identity", ["a-http-depth"]),
      ("Vulnerability classes, from the fix side", ["b-idor", "b-sqli", "b-command-injection", "b-xss", "b-csrf", "b-ssrf", "b-session-auth", "b-security-headers", "b-business-logic",
                                                   ("note", "Each class studied for how it is found <em>and</em> how it is fixed \u2014 the fix is your half of the job.")]),
      ("AppSec specialist", ["d-appsec"]),
      ("CISSP Domain 8", ["e-sdlc"])],
     ["A STRIDE threat model for something you built \u2014 not a tutorial app, your code.",
      "SAST integrated into a real pipeline, with the findings triaged and the false positives documented.",
      "A security fix responsibly disclosed and merged into real code."],
     "Merged fix or original secure-design guide",
     "A <strong>merged security fix in a real open-source project, with a teaching write-up</strong>, or an <strong>original secure-design guide others can verify</strong> \u2014 public and reviewable. That is the artifact a hiring stranger checks."),
    ("dfir", "dfir", "DFIR analyst",
     "You work out what happened after a breach, in enough detail that it stands up later \u2014 your findings may end up in a legal process, and how you handle evidence can decide whether it is admissible. It is essentially always entered from a SOC or security analyst role: you need to have watched alerts before you can reconstruct an intrusion from them.",
     [("Before you start", [("note", "This path assumes the <a href=\"/g/path/soc-analyst/\">SOC analyst path</a> is complete. The role page is explicit: DFIR is a step up from SOC work, not a first job \u2014 it does not start at Stage A directly.")]),
      ("Forensics and response", ["d-dfir-deep", "d-malware-analysis", "c-log-sources", "c-sigma-detection", "c-incident-response",
                                  ("note", "Malware analysis is concepts plus triage workflow here; detonation is reader-side in your own isolated lab.")])],
     ["A timeline reconstructed from lab logs or a disk image, with every entry sourced.",
      "A memory-forensics exercise with documented findings \u2014 what you looked for, what you found, what you ruled out.",
      "A chain-of-custody record maintained across an exercise, unbroken.",
      "An incident report written for non-technical readers \u2014 a lawyer or executive must be able to act on it."],
     "Full forensic case study from a simulated breach",
     "A <strong>published case study: timeline, evidence-handling notes, findings, and an executive report</strong> \u2014 all reproducible from the labeled data you publish alongside it. That is the artifact a hiring stranger checks."),
    ("cloud-security", "cloud-security", "Cloud security engineer",
     "You make sure the cloud account nobody is watching is not the way in. Most breaches now involve a misconfigured cloud resource rather than an exotic exploit \u2014 and the blast radius of a mistake is unusually large, which is why this is not entry-level work.",
     [("Foundations", ["a-linux-cli", "a-tcpip-ports", "a-http-depth"]),
      ("Cloud fluency first", [("note", "No guidebook lesson covers core cloud services yet \u2014 logged as a gap. Learn one major cloud\u2019s compute, storage, networking, and IAM in your own account, <strong>billing alarm on before anything else</strong> (the role page\u2019s warning), before the security content below.")]),
      ("Cloud security", ["d-cloud-security", "b-ssrf", "e-iam",
                           ("note", "SSRF is here for the cloud-metadata-service angle \u2014 the classic cloud attack path.")]),
      ("CISSP Domains 3 and 5", ["e-crypto-applied", "e-iam"])],
     ["A misconfiguration found and fixed in your own lab account \u2014 before, after, and what stops it recurring.",
      "Least privilege applied to a working setup end to end, with the breakage notes.",
      "An automated guardrail that fails a deployment reintroducing the problem."],
     "Published cloud security baseline",
     "A <strong>published cloud security baseline: an audited reference architecture with detective controls</strong>, or <strong>original research on a misconfiguration class with detection logic</strong>. That is the artifact a hiring stranger checks."),
    ("iam-engineer", "iam-engineer", "IAM engineer",
     "You decide who can do what, and you make sure nobody quietly accumulates more than they need. Stolen credentials, not clever exploits, start most intrusions \u2014 which is why identity is where organizations are actively spending, and why this work is steadier than it sounds.",
     [("Foundations", ["a-http-depth", "a-linux-cli",
                       ("note", "HTTP here means the authentication layer: Basic, Bearer, JWT structure, OAuth 2.0 and OIDC flows. Linux here means the permission model \u2014 the oldest access-control system you will ever administer.")]),
      ("CISSP Domain 5", ["e-iam"]),
      ("Cloud IAM", ["d-cloud-security", ("note", "For the cloud IAM deep dive: policies read as code, roles, federation.")]),
      ("Cryptography", ["e-crypto-applied", ("note", "Hashing, signatures, PKI \u2014 and what breaks when each is misused.")])],
     ["A permissions audit of a lab environment, with a written removal rationale for every grant you would revoke.",
      "Least privilege applied end to end, with the breakage notes \u2014 a fix that breaks the app is not a fix.",
      "A joiner-mover-leaver process document: what happens on day one, on transfer, on departure."],
     "Published IAM reference others can run",
     "A <strong>least-privilege policy library for a common stack, with rationale per policy</strong>, or an <strong>access-review methodology with a worked example</strong> \u2014 published, runnable. That is the artifact a hiring stranger checks."),
    ("grc-analyst", "grc-analyst", "GRC analyst",
     "You turn a security standard into things the organization actually does, and prove it did them. It is the most reachable security role for non-technical backgrounds \u2014 audit, admin, project, legal transfer in \u2014 and the least hands-on of this family: written artifacts carry the role.",
     [("Foundations, lighter", ["a-http-depth",
                                ("note", "Read for vocabulary \u2014 enough networking, HTTP, and crypto language to read a control intelligently. The packet labs are optional on this path.")]),
      ("Risk and continuity", ["e-risk-assessment", "e-bcp-drp"]),
      ("Asset security", ["e-asset-classification", "e-data-lifecycle", "e-data-protection-controls"]),
      ("Assessment and testing", ["e-assessment-strategy", "e-security-audits"]),
      ("Running the program", ["e-security-program", "e-board-communication"]),
      ("AI governance", ["ai-governance"]),
      ("Governance frameworks", ["e-csf-20", "e-iso27001", "e-soc2"])],
     ["One control mapped to exact evidence \u2014 the control, the artifact that proves it, where it lives.",
      "A risk written so a director can decide on it: one page, no jargon.",
      "A policy a real employee could follow without asking questions."],
     "Complete published GRC work product",
     "A <strong>risk assessment of a fictional company, a control implementation guide, or an audit plan</strong> \u2014 published and written to be used, not to be admired. That is the artifact a hiring stranger checks."),
]

PATHMAP = {key: f"/g/path/{slug}/" for key, slug, *_ in PATHS}


def _lesson_door(lid, lesson_info, n):
    title, slug, stage_label = lesson_info[lid]
    return (f'<a class="door" href="/g/{slug}/"><h3>{n}. {html.escape(title)}</h3>'
            f'<p><span class="eyebrow">{html.escape(stage_label)}</span></p></a>')


def build_paths():
    lesson_info = {}
    for lid, slug, stage_label, _n, _d in LESSONS:
        lesson_info[lid] = (parse_lesson(lid)[0], slug, stage_label)
    for key, slug, role_title, job, groups, checkpoints, cap_title, cap_html in PATHS:
        sections = []
        n = 0
        for group_label, items in groups:
            doors, notes = [], []
            for it in items:
                if isinstance(it, tuple):
                    notes.append(f'<div class="note"><p class="prose">{it[1]}</p></div>')
                else:
                    n += 1
                    doors.append(_lesson_door(it, lesson_info, n))
            gh = f"<h2>{html.escape(group_label)}</h2>"
            if doors:
                gh += f'\n<div class="grid">\n{"".join(doors)}\n</div>'
            if notes:
                gh += "\n" + "\n".join(notes)
            sections.append(f"<section>\n{gh}\n</section>")
        checks = "".join(f"<li>{c}</li>" for c in checkpoints)
        canonical = f"https://learncomputerstuff.dev/g/path/{slug}/"
        main = f"""<section>
<span class="eyebrow">Security guidebook \u00b7 Role path</span><h1>The {html.escape(role_title)} path</h1>
<p class="lede prose">{job}</p>
<p class="dateline">Published {TODAY} \u00b7 generated from the lesson data \u00b7 serves <a href="/r/{key}/">{html.escape(role_title)}</a></p>
<div class="note"><span class="eyebrow">How to use this path</span>
<p class="prose">Work the groups in order. Each checkpoint is a gate: do not move on until you can do it unaided. The capstone is level 4 \u2014 original work, made public, verifiable by a stranger.</p></div>
</section>
{"".join(sections)}
<section><h2>Checkpoints</h2>
<ol>
{checks}
</ol>
</section>
<section><h2>The capstone</h2>
<p class="prose"><strong>Level 4 \u2014 Extend: {html.escape(cap_title)}.</strong> {cap_html}</p>
</section>
<section><div class="note"><span class="eyebrow">Keep going</span>
<p class="prose"><a href="/g/paths/">All eight role paths \u2192</a> \u00b7 <a href="/g/">The security guidebook \u2192</a></p></div></section>"""
        out = REPO / "g" / "path" / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_shell(
            title=f"The {role_title} path",
            description=f"The {role_title} study path: ordered lessons, checkpoints, and a level-4 capstone. A free page in the security guidebook.",
            canonical=canonical,
            crumbs=(f'<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / '
                    f'<a href="/g/paths/">Role paths</a> / <span>The {html.escape(role_title)} path</span>'),
            breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                        ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                        ("Role paths", "https://learncomputerstuff.dev/g/paths/"),
                                        (f"The {role_title} path", canonical)]),
            main_html=main))
        print(f"wrote {out}")


def build_path_index():
    doors = []
    for key, slug, role_title, job, _g, _c, _ct, _ch in PATHS:
        first = job.split(". ")[0] + "."
        doors.append(
            f'<a class="door" href="/g/path/{slug}/"><h3>The {html.escape(role_title)} path</h3>'
            f'<p>{html.escape(first)}</p></a>')
    canonical = "https://learncomputerstuff.dev/g/paths/"
    main = f"""<section>
<span class="eyebrow">Security guidebook \u00b7 Role paths</span><h1>Role paths</h1>
<p class="lede prose">One ordered plan per role: the lessons in sequence, checkpoints that gate each stage, and a level-4 capstone \u2014 original public work a stranger can verify. Pick the job, follow the plan.</p>
<p class="dateline">Published {TODAY} \u00b7 generated from the lesson data</p>
</section>
<section><h2>The eight paths</h2>
<div class="grid">
{"".join(doors)}
</div>
</section>
<section><div class="note"><span class="eyebrow">Keep going</span>
<p class="prose"><a href="/g/">The security guidebook \u2192</a></p></div></section>"""
    out = REPO / "g" / "paths" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_shell(
        title="Role paths",
        description="Eight ordered study plans through the security guidebook \u2014 one per role, each with checkpoints and a level-4 capstone. Free pages in the security guidebook.",
        canonical=canonical,
        crumbs='<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / <span>Role paths</span>',
        breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                    ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                    ("Role paths", canonical)]),
        main_html=main))
    print(f"wrote {out}")


# ================= Knowledge maps (brief \u00a74) =================
# CISSP: every objective 1.1\u20138.5. Lesson ids are real lessons; [] = logged gap.
# Paraphrases are the guidebook's own, never outline text.
CISSP_DOMAINS = [
    ("1", "Security and Risk Management", "16", [
        ("1.1", "Professional ethics in security work", ["e-ethics"]),
        ("1.2", "Core security concepts: confidentiality, integrity, availability, and related properties", ["e-security-concepts"]),
        ("1.3", "Security governance: aligning security with business strategy", ["e-governance"]),
        ("1.4", "Legal, regulatory, and compliance landscape", ["e-cyber-law"]),
        ("1.5", "Investigation types and their requirements", ["e-investigations"]),
        ("1.6", "Security policy, standards, procedures, and guidelines", ["e-policy-docs"]),
        ("1.7", "Business continuity requirements: business impact analysis and dependencies", ["e-bcp-drp"]),
        ("1.8", "Personnel security across hiring, employment, and departure", ["e-personnel-security"]),
        ("1.9", "Risk management concepts, end to end", ["e-risk-assessment"]),
        ("1.10", "Threat modeling concepts and methodologies", ["e-threat-modeling-concepts"]),
        ("1.11", "Supply chain risk management", ["e-supply-chain-risk"]),
        ("1.12", "Security awareness, education, and training programs", ["e-awareness-training"]),
    ]),
    ("2", "Asset Security", "10", [
        ("2.1", "Identifying and classifying information and assets", ["e-asset-classification"]),
        ("2.2", "Information and asset handling requirements", ["e-handling-requirements"]),
        ("2.3", "Secure provisioning: ownership, inventory, asset management", ["e-asset-provisioning"]),
        ("2.4", "The data lifecycle: roles, collection, location, retention, remanence, destruction", ["e-data-lifecycle"]),
        ("2.5", "Asset retention and end-of-life/support", ["e-retention-eol"]),
        ("2.6", "Data security controls and compliance", ["e-data-protection-controls"]),
    ]),
    ("3", "Security Architecture and Engineering", "13", [
        ("3.1", "Secure design principles for engineering", ["e-secure-design"]),
        ("3.2", "Formal security models", ["e-security-models"]),
        ("3.3", "Selecting controls from system security requirements", ["e-control-selection"]),
        ("3.4", "Platform security capabilities", ["e-platform-security"]),
        ("3.5", "Assessing vulnerabilities across architecture and system types", ["e-arch-vuln-assessment"]),
        ("3.6", "Cryptographic solutions: lifecycle, methods, PKI, key management", ["e-crypto-applied"]),
        ("3.7", "Cryptanalytic attack methods", ["e-cryptanalysis"]),
        ("3.8", "Site and facility design principles", ["e-facility-design"]),
        ("3.9", "Site and facility security controls", ["e-facility-controls"]),
        ("3.10", "The information system lifecycle", ["e-system-lifecycle"]),
    ]),
    ("4", "Communication and Network Security", "13", [
        ("4.1", "Secure network architecture design", ["e-network-architecture"]),
        ("4.2", "Securing network components", ["e-network-components"]),
        ("4.3", "Secure communication channels", ["e-secure-channels"]),
    ]),
    ("5", "Identity and Access Management", "13", [
        ("5.1", "Controlling physical and logical access to assets", ["e-iam"]),
        ("5.2", "Identification and authentication strategy", ["e-iam"]),
        ("5.3", "Federated identity with third-party services", ["e-iam"]),
        ("5.4", "Authorization mechanisms and models", ["e-iam"]),
        ("5.5", "Identity and access provisioning lifecycle", ["e-iam"]),
        ("5.6", "Implementing authentication systems", ["e-auth-systems"]),
    ]),
    ("6", "Security Assessment and Testing", "12", [
        ("6.1", "Designing assessment, test, and audit strategies", ["e-assessment-strategy"]),
        ("6.2", "Security control testing methods", ["e-control-testing"]),
        ("6.3", "Collecting security process data", ["e-security-metrics"]),
        ("6.4", "Analyzing test output and reporting", ["e-test-analysis-reporting"]),
        ("6.5", "Conducting and facilitating security audits", ["e-security-audits"]),
    ]),
    ("7", "Security Operations", "13", [
        ("7.1", "Investigations: evidence, techniques, forensics", ["e-investigation-forensics"]),
        ("7.2", "Logging and monitoring operations", ["e-logging-monitoring"]),
        ("7.3", "Configuration management", ["e-config-management"]),
        ("7.4", "Foundational security operations concepts", ["e-secops-concepts"]),
        ("7.5", "Resource and media protection", ["e-media-protection"]),
        ("7.6", "Incident management", ["e-incident-management"]),
        ("7.7", "Operating detective and preventive measures", ["e-detective-preventive"]),
        ("7.8", "Patch and vulnerability management operations", ["e-patch-management"]),
        ("7.9", "Change management", ["e-change-management"]),
        ("7.10", "Recovery strategies and resilience", ["e-bcp-drp"]),
        ("7.11", "Disaster recovery processes", ["e-bcp-drp"]),
        ("7.12", "Testing the disaster recovery plan", ["e-bcp-drp"]),
        ("7.13", "Business continuity planning and exercises", ["e-bcp-drp"]),
        ("7.14", "Physical security implementation", ["e-physical-security"]),
        ("7.15", "Personnel safety and security concerns", ["e-personnel-safety"]),
    ]),
    ("8", "Software Development Security", "10", [
        ("8.1", "Security in the SDLC", ["e-sdlc", "d-appsec"]),
        ("8.2", "Security controls in development ecosystems", ["e-sdlc", "d-appsec"]),
        ("8.3", "Assessing software security effectiveness", ["e-sdlc", "d-appsec"]),
        ("8.4", "Security impact of acquired software", ["e-sdlc", "d-appsec"]),
        ("8.5", "Secure coding guidelines and standards", ["e-sdlc", "d-appsec"]),
    ]),
]

# CAISP (Practical DevSecOps): seven chapters. All have lessons.
CAISP_CHAPTERS = [
    ("1", "Introduction to AI Security", ["ai-llm-architecture"]),
    ("2", "Understanding and Attacking Large Language Models", ["ai-llm-architecture"]),
    ("3", "LLM Top 10 Vulnerabilities", ["ai-prompt-injection", "ai-llm-top10"]),
    ("4", "AI Attacks and Defenses Using DevOps", ["ai-pipeline"]),
    ("5", "Threat Modeling AI Systems", ["ai-threat-modeling"]),
    ("6", "Supply Chain Attacks in AI", ["ai-supply-chain"]),
    ("7", "Emerging Threats, Governance, and Compliance in AI", ["ai-governance"]),
]


def _lesson_link(lid):
    title = parse_lesson(lid)[0]
    return f'<a href="{LINKMAP[lid]}">{html.escape(title)}</a>'


def build_maps():
    lesson_info = {lid: parse_lesson(lid)[0] for lid, *_ in LESSONS}
    covered = sum(1 for _n, _t, _w, objs in CISSP_DOMAINS for _o, _p, lids in objs if lids)
    total = sum(len(objs) for _n, _t, _w, objs in CISSP_DOMAINS)

    # ---- CISSP map ----
    dom_sections = []
    for dnum, dtitle, weight, objs in CISSP_DOMAINS:
        rows = []
        for obj, paraphrase, lids in objs:
            if lids:
                cell = ", ".join(_lesson_link(l) for l in lids)
            else:
                cell = "<em>No lesson yet \u2014 logged as a gap.</em>"
            rows.append(
                f'<tr><th scope="row">{html.escape(obj)}</th>'
                f'<td>{html.escape(paraphrase)}</td><td>{cell}</td></tr>')
        dom_sections.append(
            f"<section><h2>Domain {html.escape(dnum)} \u2014 {html.escape(dtitle)} <span class=\"eyebrow\">{html.escape(weight)}% of the exam</span></h2>"
            f'\n<table class="ledger"><thead><tr><th>Objective</th><th>Topic</th><th>Lesson</th></tr></thead>'
            f"<tbody>\n{''.join(rows)}\n</tbody></table></section>")
    canonical = "https://learncomputerstuff.dev/g/map-cissp/"
    main = f"""<section>
<span class="eyebrow">Security guidebook \u00b7 Knowledge map</span><h1>CISSP knowledge map</h1>
<p class="lede prose">Every objective of the CISSP exam outline (effective April 15, 2024), 1.1 to 8.5, pointing to the lesson that teaches it \u2014 or logged as a gap where no lesson exists yet. Objectives are numbered and paraphrased in the guidebook\u2019s own words; the outline text itself is never reproduced.</p>
<p class="dateline">Published {TODAY} \u00b7 generated from the lesson data \u00b7 <strong>{covered} of {total} objectives have a lesson</strong></p>
<div class="note"><span class="eyebrow">The issuer\u2019s rule, stated once</span>
<p class="prose">Full CISSP certification needs five cumulative years of work experience in two or more of the eight domains \u2014 a degree or an approved credential can stand in for one year. Passing the exam without the experience makes someone an Associate of ISC2. The lessons teach the bodies of knowledge; they do not confer the certification.</p></div>
<div class="note"><span class="eyebrow">AI in the outline</span>
<p class="prose">ISC2 weaves AI-specific security tasks across all eight domains rather than numbering separate AI objectives, so the map treats AI as context inside each domain\u2019s lessons \u2014 cross-linked to the AI security track \u2014 not as standalone entries.</p></div>
</section>
{"".join(dom_sections)}
<section><div class="note"><span class="eyebrow">Keep going</span>
<p class="prose"><a href="/g/">The security guidebook \u2192</a></p></div></section>"""
    out = REPO / "g" / "map-cissp" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_shell(
        title="CISSP knowledge map",
        description=f"Every CISSP exam objective (1.1 to 8.5) mapped to the guidebook lesson that teaches it. {covered} of {total} objectives have a lesson. A free page in the security guidebook.",
        canonical=canonical,
        crumbs='<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / <span>CISSP knowledge map</span>',
        breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                    ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                    ("CISSP knowledge map", canonical)]),
        main_html=main))
    print(f"wrote {out}")

    # ---- CAISP map ----
    ch_rows = []
    for cnum, ctitle, lids in CAISP_CHAPTERS:
        cell = ", ".join(_lesson_link(l) for l in lids)
        ch_rows.append(
            f'<tr><th scope="row">Chapter {html.escape(cnum)}</th>'
            f'<td>{html.escape(ctitle)}</td><td>{cell}</td></tr>')
    ch_covered = sum(1 for _n, _t, lids in CAISP_CHAPTERS if lids)
    ch_total = len(CAISP_CHAPTERS)
    canonical = "https://learncomputerstuff.dev/g/map-caisp/"
    main = f"""<section>
<span class="eyebrow">Security guidebook \u00b7 Knowledge map</span><h1>CAISP knowledge map</h1>
<p class="lede prose">The seven chapters of the CAISP syllabus (Practical DevSecOps), each pointing to the guidebook lessons that teach it. Chapter titles are the issuer\u2019s; everything else is the guidebook\u2019s own words.</p>
<p class="dateline">Published {TODAY} \u00b7 generated from the lesson data \u00b7 <strong>{ch_covered} of {ch_total} chapters have a lesson</strong></p>
<div class="note"><span class="eyebrow">Two credentials, never merged</span>
<p class="prose">CAISP (Practical DevSecOps) is a separate credential from CertNexus CAIP, which the site lists separately. This map covers CAISP only.</p></div>
<div class="note"><span class="eyebrow">Edition note</span>
<p class="prose">The lessons teach the OWASP LLM Top 10 <strong>2026 edition</strong> (verified against the official OWASP GenAI Security Project repo, 2026-10-09). The project brief named the 2025 edition \u2014 that reference is pending the owner\u2019s confirmation.</p></div>
</section>
<section><h2>The seven chapters</h2>
<table class="ledger"><thead><tr><th>Chapter</th><th>Title</th><th>Lessons</th></tr></thead><tbody>
{"".join(ch_rows)}
</tbody></table></section>
<section><div class="note"><span class="eyebrow">Keep going</span>
<p class="prose"><a href="/g/">The security guidebook \u2192</a></p></div></section>"""
    out = REPO / "g" / "map-caisp" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_shell(
        title="CAISP knowledge map",
        description=f"The seven CAISP chapters mapped to the guidebook lessons that teach them. {ch_covered} of {ch_total} chapters have a lesson. A free page in the security guidebook.",
        canonical=canonical,
        crumbs='<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / <span>CAISP knowledge map</span>',
        breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                    ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                    ("CAISP knowledge map", canonical)]),
        main_html=main))
    print(f"wrote {out}")


if __name__ == "__main__":
    for lid, slug, stage_label, note, desc in LESSONS:
        build_lesson(lid, slug, stage_label, note, desc)
    build_stage_pages()
    build_paths()
    build_path_index()
    build_maps()
    build_index()
    print("done")
