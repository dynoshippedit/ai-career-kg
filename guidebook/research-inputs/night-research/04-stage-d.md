# Stage D — Specialist Tracks: Research File

Night research, 2026-10-09. Governs lesson drafting for the seven Stage D tracks.
Brief §7 safety line is absolute throughout: for C2, evasion, malware, and exploit
topics, lessons teach concepts + what defenders see + detection; hands-on work goes
to established lab environments and published emulation tests only. No original
malware, evasion tooling, C2 setup guides, phishing kits, or working exploits for
real products.

Lesson ID prefix per track: D-RT (red team), D-DF (DFIR), D-AP (AppSec),
D-EX (exploit dev/RE), D-MA (malware analysis), D-CL (cloud), D-AI (AI security).
Prerequisites reference Stage A/B/C lessons by topic name (IDs assigned by those
agents). Levels follow brief §1 (1 Recognize → 4 Extend).

---

## Track 1 — Red team operations

Reader: takes Stage B web-testing skill and Stage C disclosure discipline into
authorized adversary simulation. Prereqs: Stage A networking/HTTP, Stage B
methodology + toolbench + at least 5 web vuln classes, Stage C disclosure.

### D-RT1 — MITRE ATT&CK as the behavior language (level 2)
- What: tactics, techniques, sub-techniques, procedures; the three matrices
  (Enterprise, Mobile, ICS); groups, software, campaigns, mitigations, detections.
  Current Enterprise matrix has 15 tactics — Defense Evasion split into Stealth
  (TA0005) and Defense Impairment (TA0112) in April 2026 (verify edition at
  build time; ATT&CK releases biannually).
- Primary: https://attack.mitre.org/ (fetched 2026-10-09 — VERIFIED; tactic list
  and technique counts read directly).
- Free resources (≤3): ATT&CK Navigator (mitre-attack.github.io/attack-navigator,
  operator-added); ATT&CK STIX data repo github.com/mitre-attack/attack-stix-data
  (operator-added); the CSA "ATT&CK for Cloud" practitioner guide
  (cloudsecurityalliance.org, fetched via search 2026-10-09).
- Lab: map 10 disclosed breach reports to techniques in Navigator; export a layer.
- Proof: a Navigator layer file with technique annotations and a written note on
  what each technique's detection data source would be.
- Leads to: D-RT2, D-RT6, D-DF6.

### D-RT2 — Adversary emulation with Atomic Red Team (level 3)
- What: atomic tests — small, single-purpose, YAML-defined procedures mapped to
  ATT&CK technique IDs; executors Invoke-AtomicRedTeam (PowerShell) and the
  Python CLI; running tests against your own lab VM and checking what your
  defenses saw.
- Primary: https://github.com/redcanaryco/atomic-red-team (secondary-confirmed
  2026-10-09: actively maintained, 10,000+ stars, mapped to current ATT&CK —
  OPERATOR-ADDED, lesson writer re-fetches).
- Free resources: the repo's own atomics index and TTP YAML (primary when
  fetched); Red Canary's AtomicTestHarnesses for technique variants
  (operator-added).
- Lab: dedicated Windows/Linux VMs (never production); run 5 atomic tests
  (e.g. T1003.001 credential dumping variants are concepts-only — choose
  discovery/persistence tests first), record which generated telemetry.
- Proof: a technique→telemetry→detection table for 10 tests.
- Safety: lab VMs only; credential-dumping and defense-impairment atomics are
  run only in the isolated lab and taught with the defender's view attached.
- Leads to: D-RT6.

### D-RT3 — Planned emulation with MITRE Caldera (level 3)
- What: agent-based planned emulation vs atomic tests; Sandcat agents;
  pre-built adversary profiles (APT29, FIN6); C2 over HTTP/HTTPS/TCP in the lab.
- Primary: https://github.com/mitre/caldera (OPERATOR-ADDED — re-fetch).
- Lab: Caldera server + agents on isolated lab network; run one adversary
  profile; document the full kill chain as observed in logs.
- Proof: an emulation report with ATT&CK-mapped timeline and detection gaps.
- Safety: lab network only; C2 taught as concepts + what defenders see
  (beaconing patterns, jitter, domain fronting indicators) — no C2 setup guide
  for real operations.
- Leads to: D-RT6.

### D-RT4 — Command-and-control: concepts and what defenders see (level 2)
- What: what C2 is (beaconing, tasking, exfiltration channels); channel types
  (HTTP/S, DNS, cloud services); what defenders see — beaconing intervals,
  jitter analysis, JA3/JA4 TLS fingerprints, DNS tunneling indicators, data
  volume anomalies. NO setup instructions; NO original tooling.
- Primary: ATT&CK Command and Control tactic page (attack.mitre.org, VERIFIED
  as live 2026-10-09).
- Free resources: ATT&CK C2 technique pages (T1071, T1095, T1572 — read the
  detection sections); Zeek logs documentation (operator-added).
- Lab: analyze a provided PCAP of beaconing traffic (published training set);
  write the detection logic in words and as a Sigma rule draft (feeds D-DF6).
- Proof: a detection write-up: indicators, false-positive analysis, proposed
  rule.
- Leads to: D-DF5, D-DF6.

### D-RT5 — Evasion: concepts and what defenders see (level 2)
- What: evasion categories — obfuscation, masquerading, indicator removal,
  virtualization/sandbox evasion, defense impairment; what each looks like to
  a defender (AMSI triggers, ETW gaps, log tampering evidence). Concepts only;
  no evasion tooling written or configured.
- Primary: ATT&CK Stealth (TA0005) and Defense Impairment (TA0112) tactic pages
  (VERIFIED live 2026-10-09).
- Lab: given an EDR telemetry export from a published emulation, identify
  which evasion behaviors occurred and which telemetry gaps enabled them.
- Proof: an evasion→telemetry-gap→detection-improvement memo.
- Leads to: D-DF5.

### D-RT6 — Purple teaming: validate detections (level 3)
- What: the purple-team loop — select techniques, execute (Atomic/Caldera),
  measure (detected? blocked? alerted? response time?), report gaps, fix,
  re-run. Detection coverage as a living assessment, not a scoreboard.
- Primary: ATT&CK Navigator layers for coverage tracking (operator-added);
  CISA guidance on continuous validation (operator-added — re-fetch).
- Lab: build a 10-technique coverage layer for your lab; run the tests;
  score detected/alerted/missed; write one Sigma rule to close a gap.
- Proof: a coverage report with before/after layers and the new rule.
- Leads to: D-DF6, D-DF7.

### D-RT7 — Rules of engagement and authorization (level 2)
- What: what makes red teaming legal — written authorization, scope documents,
  rules of engagement, deconfliction, handling of production-adjacent systems;
  the difference between pentest, red team, and adversary emulation.
- Primary: brief §7 hard rules (operator input); PTES engagement sections
  (operator-added — re-fetch).
- Lab (no command line): write a scope/ROE document for a fictional
  engagement; peer-review another reader's for gaps.
- Proof: the scope document + a written explanation of what it permits and
  forbids.
- Leads to: Stage E governance.

### D-RT8 — Capstone: emulation plan (level 4)
- Design an adversary emulation plan for one technique family against your lab;
  execute it; publish the detection-gap report. Original work, made public.

---

## Track 2 — DFIR and detection engineering

Reader: takes Stage B defensive basics and Stage A packet skills into
investigation. Prereqs: Stage A Linux/networking/Wireshark, Stage B defensive
basics, Stage B methodology.

### D-DF1 — The incident response lifecycle, current revision (level 2)
- What: NIST SP 800-61 Rev. 3 (April 2025), "Incident Response Recommendations
  and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community
  Profile" — supersedes Rev. 2 (withdrawn 2025-04-03). Structured on CSF 2.0
  functions: Govern/Identify/Protect (preparation, broader risk management) and
  Detect/Respond/Recover (the incident itself), with continuous improvement fed
  back through Identify.
- Primary: https://csrc.nist.gov/pubs/sp/800/61/r3/final (fetched 2026-10-09 —
  VERIFIED: title, date, supersession).
- Free resources: the SP 800-61 Rev. 3 PDF itself (free at csrc.nist.gov);
  NIST CSF 2.0 (free); CISA incident response resources (operator-added).
- Lab (no command line): worked case — given an incident scenario, map response
  actions to the Rev. 3 functions and write the communications plan.
- Proof: the mapped response plan + a lessons-learned template.
- Leads to: D-DF2..D-DF8.

### D-DF2 — Disk forensics: artifacts (level 3)
- What: filesystem artifacts — MFT, USN journal, prefetch, event logs, registry
  hives, browser history, LNK files; order of volatility; write-blocking and
  imaging concepts.
- Primary: SANS SIFT Workstation docs (sans.org/tools/sift-workstation,
  OPERATOR-ADDED — re-fetch); NIST SP 800-86 (forensics in IR, operator-added).
- Free resources: SIFT Workstation (free); Autopsy (free); Eric Zimmerman's
  tools (free, operator-added).
- Lab: analyze a provided training disk image (published forensic challenge,
  e.g. HTB Sherlocks or SANS challenge image); build a timeline of attacker
  activity.
- Proof: a forensic timeline + findings memo.
- Leads to: D-DF8.

### D-DF3 — Memory forensics (level 3)
- What: what lives in RAM (processes, network connections, injected code,
  credentials); Volatility framework workflow: image info → pslist → netscan →
  malfind.
- Primary: Volatility documentation (volatilityfoundation.org, OPERATOR-ADDED
  — re-fetch).
- Free resources: Volatility 3 (free); SIFT Workstation (free).
- Lab: analyze a provided training memory image; find the injected process
  and extract its network indicators.
- Proof: memory analysis report with IOCs extracted.
- Leads to: D-MA4.

### D-DF4 — Network forensics (level 3)
- What: PCAP analysis, Zeek logs, NetFlow; following streams; identifying C2
  beaconing and exfiltration in packet captures; DNS log analysis.
- Primary: Zeek documentation (zeek.org, OPERATOR-ADDED — re-fetch).
- Free resources: Wireshark (free); Zeek (free); Security Onion (free,
  operator-added).
- Lab: given a training PCAP with an intrusion, reconstruct the attacker's
  actions and extract IOCs.
- Proof: network findings report with packet evidence references.
- Leads to: D-RT4, D-DF5.

### D-DF5 — Threat hunting hypotheses (level 3)
- What: hunting vs alerting; hypothesis-driven hunting (if adversary does X,
  we would see Y in data source Z); ATT&CK-informed hunt planning; documenting
  hunts so they become detections.
- Primary: ATT&CK detection sections per technique (VERIFIED live 2026-10-09).
- Free resources: ATT&CK Navigator (operator-added); "Threat Hunting with
  ATT&CK" community materials (operator-added).
- Lab: write 3 hunt hypotheses for one technique family; execute one against
  lab telemetry (Security Onion or provided logs); document findings.
- Proof: hunt hypothesis cards + execution notes + one converted detection.
- Leads to: D-DF6.

### D-DF6 — Sigma: detection as code (level 3)
- What: Sigma as the generic signature format for log events — "what Snort is
  for network traffic and YARA is for files"; rule structure (title, logsource,
  detection, condition); converting to SIEM queries; testing rules against
  telemetry from D-RT2/D-RT6 emulation runs.
- Primary: https://sigmahq.io and the Sigma specification
  (github.com/SigmaHQ/sigma — secondary-confirmed 2026-10-09 via sigmahq.io
  description; OPERATOR-ADDED as primary — lesson writer fetches the repo).
- Free resources: SigmaHQ rule repository (free); sigmahq.io documentation.
- Lab: write 3 Sigma rules for techniques you emulated in D-RT6; validate
  them against the generated logs; tune false positives.
- Proof: the 3 rules + validation notes (could be published to a personal
  detection repo).
- Leads to: D-DF7.

### D-DF7 — YARA: file classification (level 3)
- What: YARA rule syntax (strings, conditions, metadata); writing rules for
  malware families; testing against training sample sets; YARA-X as the
  current implementation line.
- Primary: YARA documentation (github.com/VirusTotal/yara, OPERATOR-ADDED —
  re-fetch).
- Free resources: YARA-X (free); the "YARA in a nutshell" community docs
  (operator-added).
- Lab: write YARA rules for 3 training samples; test for false positives
  against a benign corpus.
- Proof: the rules + test results.
- Leads to: D-MA3.

### D-DF8 — Timeline analysis (level 3)
- What: super-timelines (Plaso/log2timeline); correlating disk, memory, and
  network evidence into one narrative; presenting findings.
- Primary: Plaso documentation (operator-added — re-fetch).
- Lab: combine artifacts from D-DF2/D-DF3/D-DF4 exercises into one timeline
  of the staged intrusion.
- Proof: the timeline + executive summary written for a non-technical reader.

### D-DF9 — Capstone: investigate a staged intrusion (level 4)
- Full investigation of a provided multi-artifact intrusion scenario; publish
  the report. Original work, made public.

---

## Track 3 — AppSec

Reader: takes Stage B vulnerability classes into building security into
software. Prereqs: Stage B web vuln classes (first wave), Stage A reading
code, Stage C disclosure basics.

### D-AP1 — Threat modeling with STRIDE (level 3)
- What: what threat modeling is (design-time, not test-time); STRIDE
  categories (Spoofing, Tampering, Repudiation, Information disclosure, DoS,
  Elevation of privilege); data-flow diagrams; turning threats into
  requirements.
- Primary: Microsoft's STRIDE documentation / OWASP threat modeling guidance
  (OPERATOR-ADDED — re-fetch; prefer OWASP as primary).
- Free resources: OWASP Threat Modeling Cheat Sheet (free); OWASP Cornucopia
  card game (free, operator-added).
- Lab (no command line): threat-model a small web app you built in Stage B
  labs; produce the threat list with mitigations.
- Proof: the threat model document.
- Leads to: D-AP5.

### D-AP2 — OWASP SAMM v2.0: measuring an AppSec program (level 2)
- What: Software Assurance Maturity Model — 5 business functions (Governance,
  Design, Implementation, Verification, Operations), 15 practices, 2 streams
  each, maturity levels 0–3; using it to assess and roadmap a program.
- Primary: https://owaspsamm.org/ (fetched 2026-10-09 — VERIFIED live; model
  structure confirmed via secondary 2026-10-09).
- Free resources: the SAMM model itself (free); SAMM Fundamentals free course
  (listed on owaspsamm.org, VERIFIED as advertised).
- Lab (no command line): run a SAMM self-assessment for a fictional 20-person
  dev team; write the 6-month improvement roadmap.
- Proof: the assessment + roadmap.
- Leads to: D-AP5.

### D-AP3 — SAST with Semgrep (level 3)
- What: static analysis concepts (taint tracking, pattern matching); writing
  Semgrep rules; running it in CI; triaging findings; what SAST cannot see
  (runtime behavior, business logic).
- Primary: Semgrep documentation (semgrep.dev/docs, OPERATOR-ADDED — re-fetch).
- Free resources: Semgrep (free); Semgrep rule registry (free).
- Lab: run Semgrep on a vulnerable training app (Juice Shop or WebGoat);
  write 2 custom rules for vuln classes from Stage B; triage the output.
- Proof: the custom rules + triage report with false-positive analysis.
- Leads to: D-AP6.

### D-AP4 — DAST and SCA (level 3)
- What: dynamic testing concepts (authenticated scanning, crawl coverage);
  software composition analysis (known-vulnerable dependencies, CVEs in libs);
  the two together as verification.
- Primary: OWASP ZAP documentation (zaproxy.org, OPERATOR-ADDED — re-fetch);
  OWASP Dependency-Check docs (operator-added).
- Free resources: OWASP ZAP (free); OWASP Dependency-Check (free).
- Lab: ZAP authenticated scan of a local Juice Shop; Dependency-Check on the
  same app; reconcile both finding sets with manual Stage B results.
- Proof: combined verification report noting what each method missed.
- Leads to: D-AP5.

### D-AP5 — Secure SDLC integration (level 2)
- What: where security gates fit (requirements → design → implementation →
  verification → release → operations); security champions; pipeline gates that
  don't break delivery; metrics that matter.
- Primary: OWASP SAMM Implementation/Verification practices (VERIFIED live
  2026-10-09); NIST SP 800-218 SSDF (operator-added — re-fetch).
- Lab (no command line): design the SDLC security gates for a fictional
  startup shipping weekly; write the one-page policy.
- Proof: the SDLC security plan.
- Leads to: Stage E governance.

### D-AP6 — Code review technique (level 3)
- What: how to read code for security (data flow first, then trust boundaries);
  common patterns per language; reviewing diffs vs reviewing systems; writing
  findings developers will fix.
- Primary: OWASP Code Review Guide (operator-added — re-fetch).
- Free resources: OWASP Code Review Guide (free); Semgrep (free, from D-AP3).
- Lab: review a provided vulnerable PR; find 5 issues; write the findings as
  a developer would want to receive them.
- Proof: the code review with severity-ranked findings.
- Leads to: D-AP8 capstone.

### D-AP7 — OWASP ASVS as the verification standard (level 2)
- What: Application Security Verification Standard — what it is (a
  requirements catalog in 3 levels), how to scope verification to Level 1/2/3,
  using it as a test plan.
- Primary: OWASP ASVS (owasp.org/www-project-application-security-verification-
  standard, OPERATOR-ADDED — re-fetch; name edition and date).
- Lab (no command line): scope an ASVS Level 2 verification plan for the
  Juice Shop; map 20 requirements to test cases.
- Proof: the verification plan.
- Leads to: D-AP8 capstone.

### D-AP8 — Capstone: AppSec assessment (level 4)
- Threat-model, SAST/DAST/SCA, and code-review a real open-source app;
  publish the assessment. Original work, made public.

---

## Track 4 — Exploit development and reverse engineering

Reader: takes Stage A/B systems knowledge to its deepest end. Prereqs: Stage A
Linux/Python/crypto, Stage B methodology. SAFETY: all exploitation against
training targets only (pwn.college, exploit.education, ROP Emporium, crackmes);
no working exploits for real products, ever.

### D-EX1 — Binary anatomy: ELF and PE (level 2)
- What: headers, sections, segments; entry points; imports/exports; what the
  loader does; reading binaries with readelf/objdump.
- Primary: ELF specification / PE format documentation (Microsoft PE docs,
  OPERATOR-ADDED — re-fetch).
- Free resources: pwn.college "program misuse" modules (VERIFIED live
  2026-10-09); "Practical Binary Analysis" community notes (operator-added).
- Lab: dissect 3 training binaries with readelf/objdump; document every
  section's purpose.
- Proof: annotated binary maps.
- Leads to: D-EX2, D-EX3.

### D-EX2 — Reading x86-64 assembly (level 3)
- What: registers, the stack, calling conventions, common instruction
  patterns; reading compiler output; from C to assembly and back.
- Primary: pwn.college dojos (VERIFIED live 2026-10-09 — ASU-run, free,
  belt progression; note their rule: do not publish challenge writeups).
- Free resources: pwn.college (free); Open Security Training (OST2,
  operator-added).
- Lab: pwn.college assembly modules; translate 5 C functions to assembly
  by hand and verify with gcc -S.
- Proof: belt progress + translation exercises.
- Safety note for the lesson: link pwn.college itself, never solution
  material (their published rule).
- Leads to: D-EX4, D-EX5.

### D-EX3 — Static analysis with Ghidra (level 3)
- What: disassembly vs decompilation; navigating functions, cross-references,
  data types; renaming and retyping; scripting basics.
- Primary: Ghidra documentation (ghidra-sre.org, OPERATOR-ADDED — re-fetch).
- Free resources: Ghidra (free, NSA); Ghidra's built-in help and training
  material.
- Lab: reverse a training crackme (crackmes.one, beginner-rated); recover
  the algorithm without running it.
- Proof: annotated disassembly + algorithm write-up.
- Leads to: D-EX4.

### D-EX4 — Debugger workflows (level 3)
- What: breakpoints, watchpoints, stepping; examining registers/memory;
  gdb with GEF/pwndbg; x64dbg on Windows; dynamic confirmation of static
  hypotheses.
- Primary: GDB manual (sourceware.org, OPERATOR-ADDED); pwntools docs
  (github.com/Gallopsled/pwntools, operator-added).
- Free resources: gdb + pwndbg (free); x64dbg (free).
- Lab: debug a training binary through a function call; document register
  and stack state at each step.
- Proof: the annotated debug session transcript.
- Leads to: D-EX5.

### D-EX5 — Stack buffer overflows on training targets (level 3)
- What: the stack layout; overwriting the return address; shellcode concepts;
  end-to-end exploitation of an intentionally vulnerable training binary.
  TRAINING TARGETS ONLY. Taught alongside: why this class still matters
  (memory-unsafe code in the wild) and how defenders/mitigations respond.
- Primary: pwn.college memory-error modules (VERIFIED live); exploit.education
  Protostar/Phoenix (operator-added — re-fetch).
- Free resources: pwn.college (free); pwntools (free).
- Lab: complete the introductory buffer-overflow series on pwn.college;
  write up the exploit's mechanics in your own words (not the flag).
- Proof: mechanics write-up + belt progress.
- Leads to: D-EX6, D-EX7.

### D-EX6 — Modern mitigations (level 2–3)
- What: NX/DEP, ASLR/PIE, stack canaries, RELRO, FORTIFY; what each stops and
  what it doesn't; checking mitigations with checksec; the defender's view.
- Primary: pwn.college mitigation modules (VERIFIED live); how2heap
  (github.com/shellphish/how2heap, operator-added).
- Lab: run checksec on 10 system binaries; explain which mitigations are
  present and what attack primitive each blocks.
- Proof: the mitigation survey + explanations.
- Leads to: D-EX7.

### D-EX7 — Return-oriented programming on training targets (level 3)
- What: ROP concepts (gadgets, chains); building a chain against a
  no-NX-disabled training binary; TRAINING TARGETS ONLY.
- Primary: ROP Emporium (ropemporium.com, operator-added — re-fetch).
- Free resources: ROP Emporium (free); pwntools ROP module (free).
- Lab: complete ROP Emporium's x86-64 series.
- Proof: chain write-ups (mechanics, not flags).
- Leads to: D-EX8 capstone.

### D-EX8 — Capstone: pwn series (level 4)
- Complete an advanced pwn.college dojo series; publish a mechanics-focused
  write-up series respecting their no-solutions rule. Original work, public.

---

## Track 5 — Malware analysis

Reader: takes DFIR curiosity into safe, structured sample analysis. Prereqs:
Stage A Linux/Windows basics, D-DF2/D-DF3 helpful but not required. SAFETY:
isolated VMs, host-only networking, snapshots, samples from published training
sets only (e.g. MalwareBazaar training corpora via controlled channels);
concepts + defender view + detection; no live-malware handling instructions.

### D-MA1 — Building the safe lab (level 2–3)
- What: the two-VM pattern — FLARE VM (Windows, Mandiant's analysis
  distribution, 100+ tools via package manager) runs the sample; REMnux
  (Linux, 200+ tools) fakes the internet with INetSim; host-only networking;
  snapshots before detonation; no shared folders.
- Primary: https://github.com/mandiant/flare-vm and https://remnux.org/
  (secondary-confirmed active 2026-10-09 via zeltser.com and practitioner
  write-ups; OPERATOR-ADDED as primary — lesson writer fetches).
- Free resources: FLARE VM (free); REMnux (free, prebuilt VM).
- Lab: build both VMs; verify host-only isolation (no route to the real
  internet); take clean snapshots; document the network diagram.
- Proof: the network diagram + isolation verification notes.
- Leads to: D-MA2, D-MA4.

### D-MA2 — Static analysis: the triage workflow (level 3)
- What: hash first (VirusTotal/OTX lookup by hash only — never upload
  sensitive samples); strings; PE headers (imports, sections, entropy);
  packer detection; suspicious-import flagging; FLOSS for obfuscated strings.
- Primary: PE format docs (Microsoft, operator-added); FLOSS docs
  (github.com/mandiant/flare-floss, operator-added).
- Free resources: PEStudio (free); Detect It Easy (free); FLOSS (free).
- Lab: triage 3 training samples; produce the triage sheet for each
  (hashes, packer verdict, suspicious imports, strings of interest).
- Proof: triage sheets.
- Leads to: D-MA3, D-MA4.

### D-MA3 — YARA for malware classification (level 3)
- What: writing family/behavior rules; testing against training sets;
  sharing rules; YARA-X current line.
- Primary: YARA docs (github.com/VirusTotal/yara, OPERATOR-ADDED — re-fetch).
- Free resources: YARA-X (free); community rule repos for study
  (operator-added).
- Lab: write rules classifying 3 training samples; false-positive test
  against benign corpus. (Shared with D-DF7 — one lesson, two tracks.)
- Proof: rules + test results.
- Leads to: D-MA7 capstone.

### D-MA4 — Dynamic analysis: behavioral monitoring (level 3)
- What: ProcMon (file/registry/process), Wireshark (network), INetSim logs
  (fake services); what to start before detonation; 2–5 minute observation
  windows; killing and reverting.
- Primary: Sysinternals ProcMon docs (Microsoft, operator-added); INetSim
  docs (operator-added).
- Free resources: ProcMon (free); Wireshark (free); INetSim via REMnux (free).
- Lab: detonate a training sample in the D-MA1 lab; collect the three
  artifact streams; write the behavioral timeline.
- Proof: behavioral report with IOCs.
- Leads to: D-MA5.

### D-MA5 — From behavior to IOCs and detection (level 3)
- What: turning observed behavior into indicators (hashes, IPs, domains,
  mutexes, registry keys, YARA/Sigma); IOC confidence levels; feeding
  detections back to the DFIR track.
- Primary: ATT&CK technique pages for observed behaviors (VERIFIED live).
- Lab: convert a D-MA4 behavioral report into a detection package
  (IOCs + one YARA rule + one Sigma rule).
- Proof: the detection package.
- Leads to: D-DF6, D-DF7.

### D-MA6 — Packing and unpacking: concepts (level 2)
- What: what packers do (compression/encryption layers); entropy analysis;
  generic vs manual unpacking concepts; what defenders see (packed binaries
  in telemetry). Concepts only — no unpacking tooling authored.
- Primary: practitioner references (operator-added — re-fetch).
- Lab: entropy-survey 10 training samples with DIE; classify packed vs not
  with written reasoning.
- Proof: the survey + reasoning.
- Leads to: D-MA7 capstone.

### D-MA7 — Capstone: full analysis report (level 4)
- End-to-end analysis of a training sample (static + dynamic + IOCs +
  detection package); publish the report. Original work, made public.

---

## Track 6 — Cloud security

Reader: takes Stage A networking and Stage B methodology into cloud estates.
Prereqs: Stage A networking/HTTP, Stage B recon/methodology. All hands-on
against the reader's own lab account with read-only audit roles — never
production, never anyone else's account.

### D-CL1 — The shared responsibility model (level 1–2)
- What: what the provider secures vs what you secure, across IaaS/PaaS/SaaS;
  why most cloud breaches are customer-side misconfigurations.
- Primary: AWS / Azure / GCP shared-responsibility documentation
  (OPERATOR-ADDED — re-fetch all three).
- Lab (no command line): given 5 breach scenarios, classify each as
  provider-side or customer-side with reasoning.
- Proof: the classification exercise.
- Leads to: D-CL2, D-CL3.

### D-CL2 — Cloud IAM: users, roles, policies (level 3)
- What: identity types; policy structure (effect/action/resource); least
  privilege; privilege-escalation paths via over-broad policies; access
  analyzers.
- Primary: AWS IAM documentation (docs.aws.amazon.com, OPERATOR-ADDED —
  re-fetch); Azure RBAC docs (operator-added).
- Free resources: Cloudsplaining (free, IAM policy analysis); Parliament
  (free, operator-added).
- Lab: in your lab account, write 3 policies (correct, over-broad, broken);
  analyze each with Cloudsplaining; fix the broken ones.
- Proof: the 3 policies + analysis + fixes.
- Leads to: D-CL4.

### D-CL3 — The classic misconfigurations (level 3)
- What: public S3 buckets; open security groups (0.0.0.0/0); public RDS;
  disabled CloudTrail; unrotated keys; overly permissive IAM — each with how
  it happens, how attackers find it, how defenders detect it.
- Primary: CIS Benchmarks for AWS/Azure/GCP (operator-added — re-fetch;
  name edition).
- Free resources: the CIS Benchmarks (free PDF); AWS Free Tier lab account.
- Lab: deliberately misconfigure-then-fix each class in your lab account;
  document the before/after state.
- Proof: misconfiguration→remediation log.
- Leads to: D-CL4, D-CL5.

### D-CL4 — Posture assessment with Prowler (level 3)
- What: running CIS-benchmark checks against your own account; reading
  findings; prioritizing remediation; output formats (CSV/JSON).
- Primary: https://github.com/prowler-cloud/prowler (secondary-confirmed
  2026-10-09: open-source, AWS/Azure/GCP, CIS-mapped; OPERATOR-ADDED as
  primary — lesson writer fetches).
- Free resources: Prowler (free, Apache-2.0); CIS Benchmarks (free).
- Lab: run Prowler against your lab account with a read-only audit role;
  remediate the top 5 findings; re-run and show the delta.
- Proof: before/after reports + remediation notes.
- Leads to: D-CL8 capstone.

### D-CL5 — Visual assessment with ScoutSuite (level 3)
- What: point-in-time multi-cloud snapshots as browsable HTML reports;
  when a visual report beats a CLI table (sharing with non-engineers).
- Primary: https://github.com/nccgroup/ScoutSuite (secondary-confirmed
  2026-10-09; OPERATOR-ADDED as primary — lesson writer fetches).
- Free resources: ScoutSuite (free).
- Lab: run ScoutSuite against your lab account; pick 5 findings and verify
  each by hand in the console (automated findings are confirmed by hand —
  brief §7).
- Proof: the verified-findings report.
- Leads to: D-CL8 capstone.

### D-CL6 — Cloud logging and detection (level 3)
- What: CloudTrail / Azure Activity Log / GCP Audit Logs as the control
  plane's memory; what attacker actions look like in them; alerting on
  high-risk API calls.
- Primary: AWS CloudTrail documentation (OPERATOR-ADDED — re-fetch).
- Free resources: CloudTrail (free tier); Stratus Red Team's technique list
  as a "what to look for" catalog (read-only use).
- Lab: perform 5 high-risk actions in your lab account; find each in the
  logs; write the detection logic for 3.
- Proof: the 3 detection write-ups.
- Leads to: D-DF6.

### D-CL7 — Cloud attack paths: concepts and detection (level 2)
- What: how cloud attacks chain (exposed key → privilege escalation →
  persistence → exfiltration); concepts + what defenders see in logs.
  Hands-on ONLY via Stratus Red Team against a dedicated sandbox account,
  never production. No exploitation guides for real estates.
- Primary: https://github.com/DataDog/stratus-red-team (secondary-confirmed
  2026-10-09: "Atomic Red Team for the cloud", sandbox-only design;
  OPERATOR-ADDED — re-fetch).
- Free resources: Stratus Red Team (free); MITRE ATT&CK cloud platform
  techniques (VERIFIED live — cloud is a platform filter inside the
  Enterprise matrix, not a separate matrix).
- Lab: detonate 3 Stratus techniques in a sandbox account; find each in
  CloudTrail; write detections.
- Proof: technique→log→detection write-ups.
- Leads to: D-CL8 capstone.

### D-CL8 — Capstone: posture assessment (level 4)
- Full CIS-benchmark assessment of a lab account (Prowler + ScoutSuite +
  manual verification); publish the remediation report. Original work, public.

---

## Track 7 — AI security (applied specialist track)

Reader: takes Stage B/C skill into securing AI systems. Prereqs: Stage A
HTTP/Python, Stage B web vuln classes, Stage B API testing. (Cert syllabi —
CAISP chapters, AIGP/AAISM domains — belong to the AI-track agent; this track
is the applied counterpart.)

### D-AI1 — How LLM applications are built (level 2)
- What: tokens and context windows; system vs user prompts; RAG
  (retrieval-augmented generation); tool/function calling; agents; where the
  trust boundaries are in each pattern.
- Primary: OWASP GenAI Security Project (genai.owasp.org, OPERATOR-ADDED —
  re-fetch); NIST AI 600-1 Generative AI Profile §2 risk list
  (secondary-confirmed 2026-10-09: 12 risk categories incl. prompt injection,
  data privacy, information integrity).
- Free resources: OWASP GenAI docs (free); NIST AI 600-1 (free PDF).
- Lab: build a tiny RAG app locally; draw its trust boundaries and data flows.
- Proof: the architecture diagram with marked trust boundaries.
- Leads to: D-AI2, D-AI6.

### D-AI2 — OWASP LLM Top 10 (2025 edition) (level 2–3)
- What: the 2025 edition, LLM01 Prompt Injection through LLM10 Unbounded
  Consumption (edition confirmed by owner 2026-10-09; lesson writer re-fetches
  genai.owasp.org for the current list and names the edition + date).
- Primary: https://genai.owasp.org/ (OPERATOR-ADDED — re-fetch).
- Free resources: the LLM Top 10 document itself (free).
- Lab: for each of the 10, write one paragraph: the mechanism, an example
  scenario, and the defense class.
- Proof: the 10-paragraph survey.
- Leads to: D-AI3, D-AI5.

### D-AI3 — Prompt injection: mechanics and defenses (level 3)
- What: direct vs indirect injection; how injected instructions override
  system prompts; defenses (input/output handling, privilege separation in
  tool design, human-in-the-loop for high-stakes actions); what defenders see
  in logs.
- Primary: OWASP LLM01:2025 page (OPERATOR-ADDED — re-fetch).
- Free resources: PortSwigger Web Security Academy LLM labs (free,
  operator-added); OWASP GenAI docs (free).
- Lab: against PortSwigger's LLM labs and a local test app, demonstrate
  injection and then implement and verify a defense.
- Proof: attack→defense lab report with verification evidence.
- Safety: lab targets only; no prompt-injection kits for real products.
- Leads to: D-AI7.

### D-AI4 — MITRE ATLAS (level 2)
- What: the Adversarial Threat Landscape for AI systems — ATT&CK-style
  tactics/techniques for ML attacks; how to read a technique page; mapping
  AI attacks to defenses.
- Primary: https://atlas.mitre.org/ (OPERATOR-ADDED — re-fetch).
- Free resources: ATLAS matrix and case studies (free).
- Lab: map 5 published AI-attack case studies to ATLAS techniques.
- Proof: the mapped case studies.
- Leads to: D-AI6, D-AI7.

### D-AI5 — AI supply chain: provenance and signing (level 2–3)
- What: model provenance (where did this model come from); model signing
  with Sigstore; SBOMs for AI (CycloneDX ML-BOM); why a downloaded model is
  untrusted code.
- Primary: Sigstore docs (sigstore.dev, OPERATOR-ADDED); CycloneDX ML-BOM
  spec (operator-added).
- Free resources: Sigstore (free); CycloneDX tooling (free).
- Lab: sign a locally trained toy model with Sigstore; verify the signature;
  write what the signature does and does not prove.
- Proof: the signed artifact + verification notes + limitations write-up.
- Leads to: D-AI8 capstone.

### D-AI6 — Threat-modeling AI systems (level 3)
- What: applying threat modeling to LLM apps (D-AI1 architectures +
  D-AI2 risks); abuse cases specific to AI (data extraction, model theft,
  tool misuse); turning threats into controls.
- Primary: NIST AI RMF 1.0 functions Govern/Map/Measure/Manage
  (secondary-confirmed 2026-10-09: voluntary, Jan 2023; OPERATOR-ADDED —
  re-fetch nist.gov).
- Free resources: NIST AI RMF (free); OWASP GenAI docs (free).
- Lab (no command line): threat-model the D-AI1 RAG app; produce threats,
  controls, and residual risks.
- Proof: the threat model.
- Leads to: D-AI8 capstone.

### D-AI7 — Testing AI systems in the lab (level 3)
- What: structured testing of an LLM app you built (D-AI1): injection,
  data-extraction attempts, guardrail evaluation; measuring and documenting;
  the defender's view (logging prompts/outputs, abuse detection).
  Concepts + lab only; no attack automation for real systems.
- Primary: OWASP GenAI testing guidance (OPERATOR-ADDED — re-fetch).
- Free resources: PortSwigger LLM labs (free); your local test app.
- Lab: run a structured test battery against your local app; document
  pass/fail per test with evidence.
- Proof: the test report.
- Leads to: D-AI8 capstone.

### D-AI8 — Capstone: secure an LLM app end to end (level 4)
- Build (or take) an LLM app; threat-model it, test it, harden it, document
  the residual risks; publish. Original work, made public.

---

## Source ledger (brief §7 statuses)

| # | Claim / resource | Primary URL | Fetched | Status |
|---|---|---|---|---|
| 1 | MITRE ATT&CK Enterprise matrix: 15 tactics incl. Stealth (TA0005) + Defense Impairment (TA0112) split April 2026 | https://attack.mitre.org/ | 2026-10-09 | verified |
| 2 | NIST SP 800-61 Rev. 3 (Apr 2025), "Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile", supersedes Rev. 2 (withdrawn 2025-04-03) | https://csrc.nist.gov/pubs/sp/800/61/r3/final | 2026-10-09 | verified |
| 3 | OWASP SAMM live; SAMM Fundamentals free course advertised | https://owaspsamm.org/ | 2026-10-09 | verified |
| 4 | pwn.college: ASU-run, free, belt progression; rule against publishing challenge writeups | https://pwn.college/ | 2026-10-09 | verified |
| 5 | Atomic Red Team actively maintained (10k+ stars, current ATT&CK mapping) | https://github.com/redcanaryco/atomic-red-team | 2026-10-09 | operator-added (via secondary reports; re-fetch as primary) |
| 6 | Sigma: generic signature format for log events (sigmahq.io) | https://sigmahq.io / https://github.com/SigmaHQ/sigma | 2026-10-09 | operator-added (re-fetch repo as primary) |
| 7 | Prowler: open-source AWS/Azure/GCP assessment, CIS-mapped | https://github.com/prowler-cloud/prowler | 2026-10-09 | operator-added (re-fetch) |
| 8 | ScoutSuite: multi-cloud auditing, HTML reports | https://github.com/nccgroup/ScoutSuite | 2026-10-09 | operator-added (re-fetch) |
| 9 | FLARE VM (Mandiant) + REMnux: active analysis distributions | https://github.com/mandiant/flare-vm / https://remnux.org/ | 2026-10-09 | operator-added (re-fetch) |
| 10 | MITRE Caldera: agent-based adversary emulation | https://github.com/mitre/caldera | 2026-10-09 | operator-added (re-fetch) |
| 11 | Stratus Red Team: cloud adversary emulation, sandbox design | https://github.com/DataDog/stratus-red-team | 2026-10-09 | operator-added (re-fetch) |
| 12 | NIST AI RMF 1.0 (Jan 2023): Govern/Map/Measure/Manage; GenAI Profile AI 600-1 (Jul 2024), 12 risk categories | https://www.nist.gov/itl/ai-risk-management-framework | 2026-10-09 | operator-added (re-fetch) |
| 13 | OWASP SAMM v2.0: 5 functions, 15 practices, levels 0–3 | https://owaspsamm.org/ | 2026-10-09 | operator-added (model structure via secondary; site verified) |
| 14 | Ghidra (NSA, free); x64dbg (free); ROP Emporium; exploit.education | various | 2026-10-09 | operator-added (re-fetch each) |
| 15 | OWASP LLM Top 10 current edition 2025 (LLM01–LLM10) | https://genai.owasp.org/ | 2026-10-09 | operator-added (edition per owner check 2026-10-09; re-fetch) |
| 16 | MITRE ATLAS | https://atlas.mitre.org/ | 2026-10-09 | operator-added (re-fetch) |

## Gaps

1. **Primary fetches outstanding** (rows 5–16): this pass verified 4 primary
   pages directly; the rest are secondary-confirmed or from prior knowledge.
   Lesson writers re-fetch every one per brief §7 before writing rows.
2. **ATT&CK version drift**: matrix releases biannually; lessons must name the
   edition/date at write time (current: 15 tactics post-April-2026 split).
3. **OWASP LLM Top 10 edition**: one secondary source referenced a 2026
   mapping; owner confirmed 2025 as current on 2026-10-09 — re-fetch
   genai.owasp.org at lesson time and name the edition.
4. **NIST SP 800-61 Rev. 3 structure**: fetched the landing page only; the
   lesson writer reads the full PDF for the function-by-function structure.
5. **Tool version pins**: Prowler/ScoutSuite/Caldera/Stratus CLIs move fast;
   lessons record tool versions and test dates per brief §7.
6. **Windows licensing for FLARE VM lab**: FLARE installs onto the reader's
   own Windows VM — the lesson states the reader supplies a licensed Windows
   copy; REMnux is the free-Linux alternative path for readers without one.
7. **pwn.college no-writeup rule**: lessons link the platform, never solution
   material; proof artifacts are mechanics write-ups, not flags.
8. **D-DF7/D-MA3 shared lesson**: YARA serves both tracks — write once, reference
   from both (brief §4: write each lesson once).
9. **CIS Benchmark editions**: name the edition and date when citing in D-CL3.
10. **No live-system testing**: all labs are local VMs, training platforms, or
    the reader's own cloud lab account with read-only roles — restated in every
    track's lab notes per brief §7.
