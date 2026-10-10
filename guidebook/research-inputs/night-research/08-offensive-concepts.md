# 08 — Offensive Concepts at Professional Depth
### C2, evasion, malware analysis, phishing — concepts, what defenders see, detection
*Research for the learncomputerstuff.dev security guidebook · 2026-10-09*

**Safety line (brief §7, non-negotiable):** concepts + what defenders see + detection. No original malware, evasion tooling, C2 setup guides, phishing kits, or working exploits for real products. Hands-on goes only to established lab environments and published emulation tests. Depth here means deeper understanding and better detection — never operational instructions.

**Note on ATT&CK naming:** MITRE's current pages label tactic TA0005 as **Stealth** (formerly Defense Evasion). Both names refer to the same tactic; lessons should use the current name and note the alias.

---

## AREA 1 — COMMAND AND CONTROL (C2)

### First principles
A compromised host needs a channel back to the operator: to receive tasking and to return results. That channel must survive the network's normal filtering, so adversaries design C2 to look like traffic the network already allows. The core design tension is *stealth vs. reliability*: the stealthier the channel, the less bandwidth and the more fragile; the more reliable, the more visible. Every C2 design decision is a trade on this axis.

### The beaconing concept
Most C2 is *beaconing*: the implant initiates outbound connections to the operator on a schedule rather than listening for inbound connections (inbound is blocked by NAT and firewalls; outbound web traffic is allowed). A beacon has three observable properties:
1. **Periodicity** — check-ins at roughly regular intervals (often with jitter, a randomized ±percentage, specifically added to defeat naive interval detection).
2. **Asymmetry** — small, regular outbound requests with occasional larger inbound responses (tasking) or outbound bursts (results/exfiltration).
3. **Mimicry** — the traffic uses a legitimate protocol and, increasingly, legitimate-looking destinations.

Detection of beaconing is a *statistics* problem, not a signature problem: no single connection looks wrong; the *pattern across time* does.

### Channel space, mapped to ATT&CK (concept level)
- **T1071 Application Layer Protocol** — C2 inside ordinary protocols. Sub-techniques: .001 Web Protocols (HTTP/HTTPS — the dominant channel, blends with browsing), .002 File Transfer Protocols, .003 Mail Protocols, .004 DNS, .005 Publish/Subscribe. The principle: the protocol is chosen for what the firewall already permits.
- **T1090 Proxy** — intermediaries between implant and operator. .001 Internal Proxy (a compromised host relays for others), .002 External Proxy, .003 Multi-hop Proxy (chained relays; Tor is the canonical example), .004 **Domain Fronting**.
- **T1572 Protocol Tunneling** — one protocol wrapped inside another (e.g., traffic tunneled inside DNS or ICMP).
- **T1573 Encrypted Channel** — the C2 session itself encrypted (TLS), defeating payload inspection; defenders then work on metadata.
- **T1102 Web Service** — legitimate web services (cloud storage, messaging, social platforms) as the C2 medium; nearly unblockable by destination because the service is legitimate.
- **T1105 Ingress Tool Transfer** — downloading follow-on tooling over the C2 channel.
- **T1568 Dynamic Resolution** — the destination itself moves: fast-flux DNS and domain generation algorithms (DGAs) so blocklists can't keep up.
- **T1132 Data Encoding / T1001 Data Obfuscation** — payload encoding inside the channel.
- **T1571 Non-Standard Port / T1095 Non-Application Layer Protocol** — running C2 on unexpected ports or raw TCP/UDP.

### Domain fronting: rise and fall (concept)
Domain fronting exploited how CDNs route requests: the TLS handshake's SNI field named one domain (a high-reputation one hosted on the same CDN), while the HTTP Host header inside the encrypted session named the operator's real domain. To a network observer, the traffic appeared to go to the reputable domain. Major CDN operators disabled the SNI/Host mismatch that made this work (2018 wave), killing the technique in its classic form. The *lesson* for the professional: C2 tradecraft is an arms race against infrastructure owners, and techniques die when the platform changes. Teach the mechanism and the history, not a recipe.

### What telemetry betrays C2
**Network (NetFlow/IPFIX, proxy, DNS, Zeek):**
- Beaconing: regular-interval connections to the same destination with low byte variance — visible in NetFlow (timing + bytes) and proxy logs (URL + user-agent + bytes). Jitter raises the bar but statistical regularity analysis still works.
- DNS: high query volume to rare domains, long or encoded-looking labels, high NXDOMAIN rates (DGA), DNS tunneling (unusual query types, large TXT responses). T1071.004 / T1568.
- TLS metadata: JA3/JA4 fingerprints that don't match the claimed application (an implant's TLS client hello differs from Chrome's); certificates that don't match the SNI; connections to newly-registered domains.
- Proxy logs: odd user-agents, POSTs to static-looking URLs, large outbound transfers to uncommon destinations, non-standard ports (T1571).
- Web-service C2 (T1102): hard — the destination is legitimate; detection shifts to *behavior* (a workstation uploading to personal cloud storage it never used before).

**Endpoint (Sysmon/EDR):**
- The *process* making the connection matters more than the connection: `rundll32.exe` or a renamed binary opening persistent HTTPS sessions (Sysmon Event ID 3, network connection) is the signal. ATT&CK's own detection strategy DET0444 keys on "suspicious usage of common application-layer protocols by abnormal processes, with high outbound byte counts or irregular ports."
- Ingress tool transfer (T1105): a process with no business downloading files writing executables to disk (Sysmon Event ID 11, file create) after a network connection.

### How detection is built
1. **Beaconing analytics:** aggregate NetFlow/proxy logs by (source, destination, destination port); compute inter-arrival time statistics. Regular intervals + low jitter + long-lived = beacon candidate. Free tooling: **RITA** (Real Intelligence Threat Analytics) runs beacon analysis over Zeek logs — established, free, designed exactly for this.
2. **DNS analytics:** passive DNS / DNS log analysis for DGA (entropy of labels, NXDOMAIN rates), tunneling (query-type and size anomalies).
3. **TLS fingerprinting:** JA3/JA4 allowlists — alert on fingerprints never seen in the environment.
4. **Proxy rules:** user-agent anomalies, rare-destination POSTs, byte-threshold alerts.
5. **Sigma rules:** the SigmaHQ repository carries C2 rules mapped to T1071/T1090 (e.g., proxy-bypass, suspicious outbound connection rules) — portable across SIEMs.

### Established labs
- **Atomic Red Team** (T1071, T1090 tests) — published emulation tests, run in an isolated lab.
- **RITA** against captured lab traffic — practice beacon detection on generated data.
- Zeek + a lab network — build the NetFlow/DNS/TLS telemetry pipeline yourself.

---

## AREA 2 — EVASION

### First principles
Evasion is the adversary's answer to the defender's sensors. Every defensive control makes an *assumption* — about what malicious looks like, where it runs, what name it carries. Evasion techniques each break one specific assumption: signature matching assumes known bytes (obfuscation breaks it); process reputation assumes the binary's name tells you what it does (masquerading and LOLBins break it); forensic timelines assume timestamps are honest (timestomping breaks it); behavioral monitoring assumes code runs in its own process (process injection breaks it). The professional mental model: **for each evasion technique, name the defensive assumption it defeats** — that is what makes the technique understandable and detectable.

### Technique space, mapped to ATT&CK (concept level)
- **T1027 Obfuscated Files or Information** (18 sub-techniques) — making payloads hard to discover or analyze: .002 Software Packing, .010 Command Obfuscation (PowerShell `-EncodedCommand`, environment-variable mangling), .013 Encrypted/Encoded File, .009 Embedded Payloads, .006 HTML Smuggling, .004 Compile After Delivery, .007 Dynamic API Resolution (hiding which system functions are called), .014 Polymorphic Code. Concept: obfuscation raises the *cost of analysis*, it does not make anything invisible — and the deobfuscation moment (T1140) is itself observable.
- **T1218 System Binary Proxy Execution** (14 sub-techniques) — "living off the land": signed, trusted OS binaries used to execute attacker content. Examples at concept level: rundll32 (.011), regsvr32 (.010), mshta (.005), msiexec (.007), cmstp (.003), installutil (.004). The defensive assumption broken: "signed Microsoft binary = benign." Detection per ATT&CK's own strategy (DET0081): execution of trusted signed binaries used to run externally hosted, unsigned, or suspicious payloads — keyed on command-line parameters and network retrieval.
- **T1036 Masquerading** — names, paths, and metadata that mimic legitimate software: renamed binaries, processes running from wrong directories, mismatched version info.
- **T1070 Indicator Removal** — destroying forensic evidence: .001 clearing event logs (Windows Event IDs 1102/104 — the clearing *itself* is the loudest signal), .004 file deletion, .006 **timestomping** (modifying file timestamps to blend into a timeline; concept: the MACE timestamps in NTFS; detection via timeline anomalies and USN journal comparison).
- **T1055 Process Injection** (12 sub-techniques) — executing code inside another process's address space: .001 DLL injection, .012 Process Hollowing (a legitimate process started suspended, its memory replaced), .013 Process Doppelgänging (abusing transactional NTFS to execute a file that never visibly exists), .004 Asynchronous Procedure Call, .008 Ptrace (Linux/macOS). Concept: injection defeats *process-based* trust — the malicious code wears a legitimate process as a mask. What it looks like: cross-process memory writes followed by remote thread creation.
- **T1564 Hide Artifacts** — hidden files, ADS (alternate data streams, .004 NTFS attributes), hidden windows, hidden registry keys.
- **T1497 Virtualization/Sandbox Evasion** — .001 System Checks (sleep timers, VM artifact checks) to avoid detonating in analysis sandboxes; concept: malware that refuses to misbehave when watched.
- **T1562 Impair Defenses** — disabling or blinding the sensors themselves (.001 disable tools, .002 disable event logging, .006 indicator blocking via exclusion lists). The meta-evasion: attack the detector.
- **T1620 Reflective Code Loading** — loading code from memory without touching disk (fileless execution).

### What each looks like to EDR/Sysmon (concept level)
- **Obfuscation:** PowerShell Script Block Logging (Event ID 4104) captures the *deobfuscated* script content — the defender's answer to T1027.010. AMSI (Antimalware Scan Interface) inspects script content at runtime. High-entropy command lines and `-EncodedCommand` are triage signals, not verdicts.
- **LOLBins:** the binary is legitimate, so detection is *contextual*: parent process, command-line arguments, and network activity. `rundll32.exe` with no command line is normal; `rundll32.exe` launching a DLL from a temp path with a URL in the arguments is not. **LOLBAS** (lolbas-project.github.io) documents each binary's legitimate vs. abusive uses — the defender's reference.
- **Timestomping:** Sysmon Event ID 2 (file creation time changed); timeline analysis showing files whose timestamps contradict their neighbors; the USN change journal as ground truth.
- **Process injection:** Sysmon Event ID 8 (CreateRemoteThread) and Event ID 10 (ProcessAccess with memory-write/thread-creation access masks) — cross-process handle opens from unusual parents. Memory forensics (Volatility) shows injected regions: private memory with execute permissions in a process that shouldn't have them.
- **Log clearing:** Event ID 1102 (Security log cleared) is itself a critical alert — the absence of logs is evidence.
- **Masquerading:** Sysmon Event ID 1 captures both `Image` (path) and `OriginalFileName` (from version info) — a mismatch is the classic detection.

### How detection is built
1. **Behavioral, not binary:** every one of these detections keys on *context* (parent, arguments, path, network follow-on), never on the binary's existence.
2. **Sigma rules:** SigmaHQ's repository has rules for T1055 (CreateRemoteThread), T1070.006 (timestomping), T1027 (encoded PowerShell), T1218 (suspicious rundll32/regsvr32/mshta usage) — write once, run on any SIEM.
3. **Sysmon configuration:** a tuned Sysmon config (SwiftOnSecurity / Olaf Hartong baselines) is the free telemetry foundation; Event IDs 1, 2, 3, 7, 8, 10, 11, 13 are the evasion-detection workhorses.
4. **Hunting queries:** "processes whose OriginalFileName doesn't match their Image name"; "remote threads created in processes owned by a different user"; "event-log gaps."

### Established labs
- **Atomic Red Team** — published tests for T1027, T1036, T1055, T1070, T1218; run in an isolated lab, detect with your own Sysmon+Sigma stack.
- **pwn.college** — program-misuse and binary-abuse concepts in a teaching environment.
- **LOLBAS project** — study each binary's documented abuse patterns (defensive reference, not a toolkit).

---

## AREA 3 — MALWARE ANALYSIS (professional depth)

### First principles
Malware analysis answers one question: *what does this program do?* There are two complementary approaches. **Static analysis** reads the program without running it — fast, safe, defeated by packing and obfuscation. **Dynamic analysis** runs it and watches — truthful about behavior, defeated by sandbox evasion, and requires isolation. Professionals do static first (triage), dynamic second (behavior), and iterate: static tells you where to look, dynamic tells you what it actually did, and the gap between them tells you what it's hiding.

### Static analysis, professional depth
- **File identification and hashing:** file type (magic bytes, not extension), cryptographic hashes (SHA-256) for pivoting to threat intel (MalwareBazaar/abuse.ch — free sample and intel sharing).
- **PE structure (concept level):** the Portable Executable format — DOS header, NT headers, the section table (.text code, .data, .rdata, .rsrc resources). What each section *should* contain vs. what anomalies mean: an executable section with high entropy and a suspicious name is the classic packed-binary tell. Import Address Table (IAT): the list of system functions the binary calls — a small, security-relevant import set (process, memory, network, registry, crypto APIs) sketches the binary's capabilities before a single instruction is read. Tools: PE-bear, CFF Explorer, pestudio (free).
- **Strings:** readable text extracted from the binary — URLs, IPs, registry paths, error messages, PDB paths. Encoded/encrypted strings (few readable strings + high entropy) indicate packing or string encryption — itself a finding.
- **Entropy:** Shannon entropy per section, 0–8 scale. Normal code sections sit in a middle band; packed or encrypted sections approach 8.0. Concept: entropy measures *randomness*; compressed/encrypted data looks random. It is a triage signal, never a verdict — installers and legitimate packed software also score high.
- **Packing/unpacking (concept level):** packers (UPX being the canonical open example) compress/encrypt the real payload; the on-disk binary is a small stub that unpacks in memory at runtime. Static analysis sees the stub; the real code only exists in memory. Defeating it conceptually: let it unpack itself (run to the unpacking stub's end in a debugger, dump the memory region) or use automated unpackers. The *analyst's* view: packed = "the author didn't want static analysis to work," which is itself intelligence.
- **Capabilities, not just IOCs:** the professional output of static analysis is a *capability assessment* (what this family can do), not just hashes and strings.

### Dynamic analysis, professional depth
- **API tracing:** watching which system functions the malware calls at runtime (file, registry, process, network, crypto) — tools: API Monitor, or EDR telemetry in a lab. The call *sequence* reveals intent: e.g., persistence writes followed by network connections.
- **Network behavior:** DNS queries, HTTP/S connections, unusual ports — captured with Wireshark/INetSim (INetSim fakes internet services so the malware's network behavior is observable safely in isolation).
- **Filesystem and registry changes:** ProcMon snapshots before/after — dropped files, Run keys, services.
- **Sandbox evasion awareness:** malware that sleeps, checks for VMs, or requires user interaction before misbehaving (T1497) — the analyst's counter is patience and realistic lab environments, not cleverer tools.
- **Memory forensics:** Volatility for dumped memory — finds injected code, unpacked payloads, and hidden processes that static analysis never sees.

### Behavioral indicators (the detection payoff)
Analysis produces *behavioral* IOCs, which outlive any single sample: persistence mechanisms used, C2 channel shape, process-injection targets, distinctive registry keys, mutex names, user-agent strings. These become Sigma/YARA/detection rules — analysis feeding detection is the whole point.

### YARA for classification (professional depth)
YARA is the pattern-matching language for identifying and classifying malware. From the official docs (yara.readthedocs.io, v4.5.0, fetched 2026-10-09):
- A rule has an identifier, an optional `meta` section (descriptive, doesn't affect matching), a `strings` section (text, hex with wildcards/jumps/alternatives, regex — with modifiers like `nocase`, `wide`, `ascii`, `xor`, `base64`), and a required `condition` (boolean logic over the strings, plus file properties: `filesize`, `uint16(0)==0x5A4D` for MZ headers, PE module attributes like imports and section entropy via `import "pe"`).
- Rule-writing discipline for professionals: anchor on strings *unique to the family* (not generic API names); combine weak indicators (`2 of ($a,$b,$c)`) rather than one strong one; use the PE module (`pe.number_of_sections`, `pe.imphash()`, section entropy) for structural rules that survive string changes; **always test against a benign corpus** before deploying — a rule that fires on legitimate software is worse than no rule.
- Workflow: yarGen generates candidate rules from samples (starting point only — manual review mandatory); test with `yara`/`yarac`; validate against larger corpora (Unpac.Me, MalwareBazaar).

### Established labs (isolated only)
- **REMnux** (remnux.org) — Linux toolkit distro for malware analysis: network services, document/script analysis, memory forensics. Runs as a VM; the standard free lab.
- **FLARE VM** (github.com/mandiant/flare-vm) — Mandiant's Windows analysis VM: disassemblers, debuggers, PE tools pre-installed. Isolated VM only.
- **Known samples only** — MalwareBazaar (abuse.ch) for sample sourcing; never analyze unknown live malware outside isolation; lab network must be host-only with INetSim, no route to the real internet.

---

## AREA 4 — PHISHING

### First principles
Phishing is social engineering delivered electronically: the attacker *borrows trust* — of a brand, a colleague, a process — to make the victim act. ATT&CK T1566: spearphishing attachment (.001), spearphishing link (.002), spearphishing via service (.003, e.g., LinkedIn/Teams messages). Related: T1598 phishing-for-information (reconnaissance phish), thread hijacking (replying inside a real thread the attacker can read), and email hiding rules (T1564.008 — inbox rules that hide the attacker's replies from the victim). BEC (business email compromise) is phishing where the payload is *a fraudulent instruction*, not malware — wire transfers, gift cards, invoice redirection. Credential harvesting pages are phishing where the payload is the victim's login.

### The concepts, defender's view
- **Pretexting:** the invented scenario (the "pretext") — IT support, a vendor, an executive. Defense: out-of-band verification procedures for sensitive actions, not cleverness.
- **BEC:** no malicious link or attachment — pure text, often from a compromised real account. Defeats every content filter; defeated only by *process* (verification workflows) and anomaly detection (impossible-travel logins, new forwarding rules).
- **Credential harvesting:** lookalike domains, cloned login pages. Defense: MFA (especially phishing-resistant MFA), browser warnings, and user reporting.
- **Thread hijacking / conversation takeover:** the attacker, inside a compromised mailbox, replies to a real thread with a malicious link. Defeats "do I know this sender" heuristics.
- **Evasive techniques per ATT&CK:** manipulating email headers/metadata from compromised accounts, email hiding rules so the victim never sees the attacker's messages.

### Email authentication: the defensive spine (SPF, DKIM, DMARC)
The core problem: SMTP (RFC 5321) never authenticated the sender — any host could claim any address. Three DNS-published standards fix this, each answering a different question:
- **SPF (RFC 7208, Standards Track, April 2014 — fetched):** "Is this *sending server* authorized to send for this domain?" The domain publishes a TXT record listing authorized senders (`v=spf1` with mechanisms: `ip4`, `ip6`, `a`, `mx`, `include`, `all`, each with qualifiers `+ - ~ ?`). The receiver checks the *envelope-from* (MAIL FROM, not the visible From header) against the connecting IP. Results: pass/fail/softfail/neutral/none/temperror/permerror. **What breaks it:** forwarding (the forwarder's IP isn't in the original record); the 10-DNS-lookup limit (too many `include`s → permerror); it authenticates the envelope domain, *not* the address the human sees.
- **DKIM (RFC 6376):** "Is this message *authentic and unaltered*, and which domain vouches for it?" The sending domain signs selected headers and the body with its private key; the signature travels in a `DKIM-Signature` header; the receiver fetches the public key from DNS and verifies. Survives forwarding (the signature travels with the message) — this is why DKIM is the more robust of the two. **What breaks it:** mailing lists that modify the body; key management failures.
- **DMARC (RFC 7489):** "Does the authenticated domain *match the domain the human sees*, and what should receivers do otherwise?" DMARC requires **alignment**: the domain that passed SPF or DKIM must match the visible `From:` header domain. Then the domain's published policy (`p=none/quarantine/reject`) tells receivers what to do with failures, and aggregate reports (`rua=`) tell the domain owner who's sending as them. **The key insight:** SPF or DKIM alone can be passed by an attacker using *their own* domain while forging your display name — only DMARC alignment closes that gap. Staged rollout: `p=none` (collect reports) → `quarantine` → `reject`.
- **Supporting:** RFC 7601 `Authentication-Results` header (where receivers record the verdicts — the triage analyst's first read); ARC (RFC 8617) preserves authentication across forwarding hops.

### Header and URL analysis for triage (concept level)
What a SOC analyst reads in a reported phish:
1. **Authentication-Results:** SPF/DKIM/DMARC verdicts — a `dmarc=fail` on a message claiming to be the CEO is the fastest verdict available.
2. **Received chain:** bottom-up — the earliest Received header is the most trustworthy; look for the true origin IP vs. the claimed sender.
3. **From vs. envelope-from vs. Reply-To:** mismatches are the classic tell (visible From says the bank; Reply-To goes to the attacker).
4. **URLs:** expand shorteners mentally — read right-to-left for the real registrable domain; punycode/homoglyph domains; newly-registered domains; URL redirect chains.
5. **Attachments:** file type vs. extension, macros, HTML smuggling (T1027.006) — detonate in sandbox, never on the workstation.

### User-reporting workflows
The human sensor network: a one-click report-phishing button beats forwarding (forwarding breaks headers); reports feed the SOC triage queue; confirmed phish become detection content (block the URLs, YARA the attachments, hunt the campaign). Metrics that matter: report rate and mean-time-to-report, not click rate alone. Simulated phishing is a *measurement* tool for the program, not a punishment tool for users.

### Established labs
- **Email header analysis** on the analyst's own mail (Authentication-Results is in every Gmail/Outlook message) — free, zero risk.
- **GoPhish in an isolated lab** — the standard open-source phishing *simulation* framework, used by defenders to run their own awareness programs; lab-only, own infrastructure, never pointed at real third parties.
- **Phishing triage practice:** public phishing email corpora and header-analysis exercises; URL analysis against VirusTotal/abuse.ch URL feeds.

---

## SOURCE LEDGER

| # | Claim / resource | Primary URL (fetched 2026-10-09) | Status |
|---|---|---|---|
| 1 | T1055 Process Injection: 12 sub-techniques; tactics Stealth + Privilege Escalation; definition | https://attack.mitre.org/techniques/T1055/ | verified |
| 2 | T1027 Obfuscated Files or Information: 18 sub-techniques; Stealth tactic | https://attack.mitre.org/techniques/T1027/ | verified |
| 3 | T1218 System Binary Proxy Execution: 14 sub-techniques; LOLBin concept; detection strategy DET0081 | https://attack.mitre.org/techniques/T1218/ | verified |
| 4 | T1566 Phishing: spearphishing attachment/link/via service; email hiding rules; thread hijacking; spoofing | https://attack.mitre.org/techniques/T1566/ | verified |
| 5 | T1564 Hide Artifacts: hidden files/registry/services; tactic Stealth | https://attack.mitre.org/techniques/T1564/ | verified |
| 6 | T1071 Application Layer Protocol: 5 sub-techniques; detection strategy DET0444 (AN1225–AN1228) | https://attack.mitre.org/techniques/T1071/ | verified |
| 7 | T1090 Proxy: 4 sub-techniques incl. T1090.004 Domain Fronting; CDN routing schemes | https://attack.mitre.org/techniques/T1090/ | verified |
| 8 | YARA 4.5.0 rule syntax: rule/meta/strings/condition; string types and modifiers; PE module | https://yara.readthedocs.io/en/latest/writingrules.html | verified |
| 9 | RFC 7208 SPF: v=spf1, mechanisms, qualifiers, results, 10-lookup limit; Standards Track, April 2014 | http://www.rfc-editor.org/info/rfc7208/ | verified |
| 10 | LOLBAS project: MITRE-mapped LOLBin catalog with detection info | https://lolbas-project.github.io/ | operator-added (in search results, not fetched) |
| 11 | SigmaHQ: generic signature format, ATT&CK-mapped rule repository | https://github.com/SigmaHQ/sigma | operator-added (in search results, not fetched) |
| 12 | REMnux: Linux malware-analysis toolkit distro | https://remnux.org/ | operator-added (in search results, not fetched) |
| 13 | FLARE VM: Mandiant Windows analysis VM | https://github.com/mandiant/flare-vm | operator-added (in search results, not fetched) |
| 14 | RFC 6376 DKIM signatures; RFC 7489 DMARC; RFC 7601 Authentication-Results; RFC 8617 ARC | rfc-editor.org (full text not fetched this pass) | operator-added — fetch full text at lesson-writing time |
| 15 | ATT&CK tactic TA0005 currently labeled "Stealth" (alias Defense Evasion) | observed on T1055/T1027/T1218/T1564 pages | verified |
| 16 | RITA beacon analysis over Zeek logs (free) | lead from research; no URL fetched | operator-added — verify at lesson time |
| 17 | Sysmon Event IDs 1/2/3/7/8/10/11/13 as evasion-detection workhorses; SwiftOnSecurity/Hartong baselines | corroborated across secondary sources | operator-added — verify against Sysinternals docs at lesson time |
| 18 | INetSim fake internet services for isolated detonation | standard practice, widely documented | operator-added — verify at lesson time |
| 19 | GoPhish as defender phishing-simulation framework (lab-only) | widely documented | operator-added — verify at lesson time |
| 20 | Domain fronting disabled by major CDNs (2018 wave) | historical, multi-source | operator-added — cite dated sources at lesson time |

## GAPS
1. DKIM (RFC 6376), DMARC (RFC 7489), Authentication-Results (RFC 7601), ARC (RFC 8617) — full texts not fetched this pass; mechanics described from stable standards knowledge. Fetch at lesson-writing time.
2. LOLBAS, SigmaHQ, REMnux, FLARE VM project pages — appeared in search results but not fetched; re-fetch as primary rows before lessons ship.
3. Sysmon event-ID semantics — verify against Microsoft Sysinternals documentation at lesson time (currently corroborated secondary).
4. T1070 (Indicator Removal), T1036 (Masquerading), T1497 (Sandbox Evasion), T1562 (Impair Defenses), T1140 (Deobfuscate/Decode) — referenced at concept level from corroborated knowledge; fetch primary ATT&CK pages at lesson time if lessons need deeper procedure detail.
5. RITA, INetSim, GoPhish — verify current project state/URLs at lesson time.
6. BEC/financial-fraud specifics — kept at concept level deliberately; lesson authors should use published case studies (e.g., FBI IC3 reports) rather than inventing scenarios.

## 5-LINE HANDOFF
1. **Coverage:** all four areas researched to lesson-grade depth — C2 (beaconing, T1071/T1090/T1572/T1573/T1102/T1105/T1568 channel space, domain fronting rise-and-fall, NetFlow/DNS/TLS/endpoint telemetry, beaconing/DGA/TLS-fingerprint analytics, Atomic Red Team + RITA labs); evasion (T1027/T1218/T1036/T1070/T1055/T1564/T1497/T1562/T1620 mapped to the defensive assumption each breaks, Sysmon/EDR observables per technique, Sigma + tuned-Sysmon detection, LOLBAS reference); malware analysis (static: PE/IAT/strings/entropy/packing; dynamic: API tracing/network/ProcMon/memory forensics; behavioral IOCs; YARA 4.5.0 rule craft with testing discipline; REMnux + FLARE VM isolated labs); phishing (T1566, pretexting/BEC/harvesting/thread-hijacking concepts, SPF/DKIM/DMARC mechanics with failure modes, header/URL triage, user-reporting workflows, GoPhish lab-only).
2. **Key sources:** 9 primary rows verified by direct fetch 2026-10-09 — ATT&CK T1055/T1027/T1218/T1566/T1564/T1071/T1090, YARA 4.5.0 docs, RFC 7208; 11 rows operator-added for lesson-time re-fetch.
3. **Gaps:** DKIM/DMARC/ARC RFC full texts, LOLBAS/SigmaHQ/REMnux/FLARE project pages, Sysmon docs, and T1070/T1036/T1497/T1562 primaries all queued for lesson-writing time — logged, not smoothed.
4. **Safety line held:** concepts + defender view + detection throughout; no malware, evasion tooling, C2/phishing kit instructions, or working exploits anywhere in the file.
5. **Notable corrections for the build:** ATT&CK now labels TA0005 "Stealth" (alias Defense Evasion) — lessons must use the current name; domain fronting is dead as a technique but essential as history; SPF/DKIM alone never stop spoofing — only DMARC alignment does.
