# Security Guidebook: agent brief

Project: learncomputerstuff.dev · Owner: Dino Silvestri · Written 2026-10-09

Read the whole brief before you act. It covers what to build, the standard it has to meet, the order of work, and the two points where you stop and wait for me.

## 1. The job

My site already shows both ends of a security career. Role routes at `/r/<role>/` show the work. Credential pages at `/c/<credential>/` and the directory at `/x/` show the certifications. Both ends are finished.

The middle is missing: the material that takes someone from knowing nothing to being able to do the work. Build that for cybersecurity as an applied-knowledge guidebook with tutorials. A reader picks a role, follows a plan, learns how each thing works, practices it on targets they are allowed to touch, and ends each step holding something a stranger can check.

My readers have no degree and may be starting from zero. The site's bet is that checkable evidence can stand in for the degree, so every lesson ends in evidence.

### The bar

Doctoral depth without the doctorate. A reader who finishes a role path can:

- explain each mechanism from first principles, with no term they can't unpack;
- work from primary sources: RFCs, standards, specifications, source code, original papers;
- apply the skill unaided on an unfamiliar target they are authorized to test;
- produce original work that other people verify, and defend it in writing.

Every lesson states which of four levels it takes the reader to.

| Level | The reader can |
|---|---|
| 1 Recognize | name it and spot it |
| 2 Operate | do it by following steps on a prepared target |
| 3 Apply | do it unaided on an unfamiliar authorized target, and explain why it worked and what would have stopped it |
| 4 Extend | work from the primary sources, build or change the tooling, find what the references miss, publish something others verify |

Most lessons should reach level 3. A lesson that stops lower says so and names the lesson that finishes the job. Each role path ends in a capstone at level 4: original work, made public.

### Not in this project

Prices, exam fees, cost tables, salary figures, and promises about how long it takes to get hired. When a lesson mentions a certification, link to its page on the site and say nothing about cost. If the site has no page for it, link to its directory entry and tell me at Stop 1.

## 2. Inputs

- `PROGRAM_MAP.md`: my topic map. Five stages (A to E), the AI security track, the career ladder. This is the scope.
- `Web-Security-Tool-Catalog.md`: fifteen tool phases in activation order, with the question each tool answers. Use the catalog table and the activation order. Ignore its "Paid layer" table.
- The site's repository and the live site: the conventions you have to match.

Where those files disagree with this brief, the brief wins. Four things in `PROGRAM_MAP.md` are replaced outright:

- Its thesis line (a CVE and a run at Anthropic's Cyber Verification Program as the finish line) is replaced by section 1.
- Its "CV:" lines that list "CVP standing" are dropped. See the correction in section 3.
- Its statements that a stage "makes you hireable" are my reasoning. Present them as reasoning, never as fact.
- Its resource names are leads to check, never verified facts.

## 3. Corrections to my map

These were checked on 2026-10-09. "Confirmed" means the owner's page was read that day. Re-fetch everything yourself before it goes on the site.

| Topic | My map says | Current state | Status |
|---|---|---|---|
| NICE Framework | Seven categories, 2017 role names | The current NICE Framework Components have five Work Role Categories. Version 2.0.0 removed two. The five should be Oversight and Governance, Design and Development, Implementation and Operation, Protection and Defense, Investigation. Two NIST pages gave different current version numbers (2.1.0 and 2.2.0), so take the version, names and IDs from NIST's components file. | Change confirmed at NIST; names from memory |
| CVE Program | "~100+ CNAs", "MITRE as editor" | About 500 CNAs (502 reported for 2026-03-31). Describe the program structure and the credit field from cve.org's own documentation. cve.org only renders in a browser. | Reported; confirm |
| NVD | NVD enriches each CVE with CVSS, CWE, CPE | Reported by several outlets: since 2026-04-15 NIST enriches only prioritized CVEs (in CISA KEV, in software the federal government uses, or in designated critical software), leaves the rest unscheduled, and relies on the CNA's severity score. The lesson has to teach where severity, weakness and product data come from now. | Reported; confirm at nvd.nist.gov |
| CVSS | "Base/Temporal/Environmental (v4.0 adds Supplemental)" | v4.0 is the latest version. Its groups are Base, Threat, Environmental, Supplemental. Threat replaced Temporal. | Version confirmed at first.org; group names from memory |
| CISSP | Eight one-line domain summaries | Build from the official exam outline, effective 2024-04-15: eight domains, numbered objectives 1.1 to 8.5. No announcement of a newer one was found. ISC2's outline page also carries an AI note under each domain; use those to link each domain to the AI track, and find out whether they are exam content or commentary. Full certification needs five years of cumulative work experience in two or more domains (a degree or an approved credential can stand in for one year); passing without it makes someone an Associate of ISC2. Say that once on the CISSP map page. | Confirmed at isc2.org |
| CAISP | Seven chapters | Confirmed at the issuer (Practical DevSecOps): 1 Introduction to AI Security; 2 Understanding and Attacking Large Language Models; 3 LLM Top 10 Vulnerabilities; 4 AI Attacks and Defenses Using DevOps; 5 Threat Modeling AI Systems; 6 Supply Chain Attacks in AI; 7 Emerging Threats, Governance, and Compliance in AI. Different from CertNexus CAIP, which the site already lists. Never merge the two. | Confirmed |
| OWASP LLM Top 10 | No edition named | Current edition is 2025, LLM01 Prompt Injection through LLM10 Unbounded Consumption. | Confirmed |
| AAISM | Needs active CISSP or CISM | Same, per several secondary sources. ISACA also runs AAIA and AAIR; don't imply AAISM is its only AI credential. | Reported; confirm at isaca.org |
| SANS | SEC598 to GASAE, SEC535 to GOAA | Pairings confirmed at sans.org and giac.org. The courses are paid. Teach their subject areas from free material. | Confirmed |
| NIST SP 800-61 | "IR lifecycle per NIST SP 800-61" | Revised in 2025. Use the current revision and its structure. | From memory; confirm |
| Kurose and Ross | Textbook "free online" | The textbook is a commercial book. The authors publish lectures, slides and Wireshark labs free. | From memory; confirm |
| Anthropic's Cyber Verification Program | A milestone and a CV line | Use it as an example of what working professionals know. It is access to tooling, never a credential, a milestone or a CV line. Confirmed at Anthropic, announced 2026-10-06: three tiers. Defense Access covers SOC and incident response work, malware reverse engineering, and analyzing and validating vulnerabilities. Red Team Access adds authorized penetration testing and red teaming, organizations only. Specialized Access is for organizations authorized to test safety-critical systems. Individuals can hold Defense Access only, and Anthropic's example of a qualifying individual is a researcher "with a track record of reported vulnerabilities". Two uses: it shows how the field sorts professional security work, and it shows a public record of reported vulnerabilities being treated as evidence. The three-tier version is days old, so date every statement. | Confirmed |

## 4. What to build

Four page types, all generated from one set of lesson files.

- **Lesson.** One topic, taught to the spec in section 6. The unit of teaching.
- **Path.** One per role: the ordered plan through the lessons, with checkpoints and a capstone. Each existing role page links to its path.
- **Knowledge map.** One per body of knowledge a certification tests. CISSP first (every objective, 1.1 to 8.5) and CAISP (seven chapters). Each objective or chapter points to the lessons that teach it. This is where the site's two ends meet. Lighter maps at domain level for AIGP, GASAE, GOAA and AAISM come after.
- **Stage page.** A to E, the novice-to-expert backbone: the stage's goal, its milestone, and what a reader can and cannot honestly claim after it.

Write each lesson once. A lesson can sit in several paths and maps. Store lessons as data, one file each, with fields for stage, level, prerequisites, roles, map references, sources and test date. Generate paths, maps, stage pages and every count from those fields. The site already takes its counts from data files; keep it that way.

Show coverage as plain counts taken from the data, such as "14 of the outline's objectives have a lesson". Never show a percentage score.

Design the lesson format so other career families can use it later. Build only cybersecurity now.

## 5. Scope

### Stage A: Foundations

Milestone: explain, packet by packet, what happens between pressing "log in" and the page rendering. Claim: nothing yet.

- **Operating systems and Linux** — how a computer runs programs and controls access, because every later topic assumes it. Research and teach: processes and memory, the filesystem and permission model, users and groups, services and daemons, logs, package management, SSH, and the shell. Linux first because the tooling lives there; Windows second for the same concepts (registry, services, event logs, PowerShell).
- **Networking at packet level** — what actually crosses the wire when two machines talk, not just the vocabulary. Research and teach: the TCP/IP stack layer by layer, IPv4 and IPv6 addressing and subnetting, how DNS resolves a name, DHCP, routing, ports, and what firewalls, VPNs, proxies and VLANs do to traffic. The reader should be able to open a packet capture and say what each field is doing.
- **HTTP in depth** — the protocol every web attack and defense is built on, so it gets its own deep treatment. Research and teach: request methods, status codes, headers, how cookies and sessions carry identity, the authentication schemes (Basic, Bearer, JWT structure, OAuth 2.0 and OIDC flows), and the TLS handshake step by step. Everything in Stage B refers back to this.
- **Python for security tooling** — enough Python to read and adapt the small tools the field runs on. Research and teach: making HTTP requests, parsing responses, working with sockets, and handling arguments and files. The goal is reading and changing a script, not software engineering.
- **Reading code** — the ability to follow a vulnerability through source. Research and teach: enough JavaScript to read client-side behavior, and enough SQL to see how a query is built and where user input enters it.
- **Cryptography** — what the primitives do, and more importantly what breaks when they are misused. Research and teach: hashing versus encryption, symmetric and asymmetric encryption, digital signatures, and PKI and certificates — each paired with the common misuse that defeats it, and the rule that you never roll your own.

### Stage B: Practitioner

Milestone: a first valid finding submitted to a program that authorizes testing.

- **Authorization, scope and the hard rules** — the lesson that gates every hands-on lesson after it. Research and teach: what written authorization is, what a rules-of-engagement document contains, and why testing outside it is a crime (CFAA in the US, Computer Misuse Act in the UK). The hard rules in section 7 are taught here as written.
- **Methodology** — how an authorized engagement is structured from start to finish, so the reader works to a repeatable process instead of poking at random. Muse researches each standard and each phase and teaches what it is, what happens in it, and what it produces.
  - *Standards to research and summarize:* **OWASP Web Security Testing Guide (WSTG)** — the community standard for how to test a web app, organized by category (information gathering, configuration, authentication, session management, authorization, input validation, error handling, cryptography, business logic, client-side); teach how to read it and use its test cases as a checklist. **PTES (Penetration Testing Execution Standard)** — a seven-stage model of an engagement (pre-engagement, intelligence gathering, threat modeling, vulnerability analysis, exploitation, post-exploitation, reporting); teach it as the shape of a professional job. **NIST SP 800-115 (Technical Guide to Information Security Testing and Assessment)** — the US government guide; teach its planning / execution / post-execution structure and how it frames rules of engagement and handling of findings.
  - *Phases to define, each as a stage of a scoped, authorized test:* **Scoping** — agreeing in writing what may be tested, when, how hard, and what is off-limits; this is the authorization that makes everything after it legal, and it is taught first and hardest. **Reconnaissance** — gathering what is publicly known about an in-scope target; teach the split between passive (reading public sources) and active (touching the target), tied to the rule that a name found is not permission. **Enumeration** — turning the attack surface into a concrete inventory of hosts, services, endpoints, parameters and versions, and keeping that inventory inside scope. **Exploitation** — confirming a candidate weakness is real by demonstrating impact once and minimally on an authorized target; teach it as proof a defender can reproduce, not as persistence, spread or damage. **Post-exploitation** — assessing what a confirmed finding actually means for the organization, written in business terms; kept at impact-assessment level, not tooling to deepen or maintain access. **Reporting** — the deliverable the whole job exists for: root cause, reproduction steps, impact, remediation, and proof the tester stayed in scope. The site already says the report is the hard part; this is where that lands.
- **The toolbench** — the fifteen phases of `Web-Security-Tool-Catalog.md` in activation order. For each phase, research and teach the one question that phase answers, the free tool that answers it, how to read its output, and what it cannot tell you (a scanner's match is a candidate, not a confirmed finding). Teach tools as answers to questions, never as an install list.
- **Web vulnerability classes** — one lesson each, every one built on the same frame: what the flaw is, why it arises in real code, how it is found during authorized testing, how it is proven with a single minimal proof-of-concept against a local or permissioned target, and how it is remediated and detected. This is exactly how OWASP and the PortSwigger Academy teach them for free; match that depth. The classes: IDOR, broken access control, SQL injection, command injection, API abuse, SSRF, XSS, CSRF, business-logic flaws.
- **Second wave** — the same frame, for the harder classes once the first nine are solid: authentication flaws, server-side template injection, XXE, insecure deserialization, JWT and OAuth flaws, GraphQL abuse, race conditions.
- **Setting up practice targets locally** — how to stand up the legal targets the hands-on lessons use, so the reader never needs a live system. Research and teach the one-command setup for DVWA, OWASP Juice Shop, WebGoat, crAPI and DVGA, and how to reset them.
- **Defensive basics** — the other side of every attack, so the reader can see what a defender sees. Research and teach: the SOC triage workflow, how to read a SIEM alert, and the logic that decides which alerts matter.
- **Bug bounty mechanics** — how authorized testing is actually offered to beginners. Research and teach: how the platforms (HackerOne, Bugcrowd, Intigriti) define programs, scope and safe harbor; how to read disclosed reports to learn real chains; and how to write the finding up.

### Stage C: Professional

Milestone: a coordinated disclosure completed, and a CVE record that credits the reader.

- **Coordinated vulnerability disclosure** — the professional way to report a real flaw without harm. Research and teach, end to end with the OpenSSF and CERT/CC guides: finding the security contact (security.txt first), reporting privately, agreeing a timeline, and publishing responsibly. Show one good and one bad disclosure.
- **The CVE Program** — how a vulnerability gets a public identifier. Research and teach from cve.org: what a CVE is, what a CNA does, how an ID is requested, the record format, and how a reporter is credited. Note the current scale (about 500 CNAs) and that not every bug qualifies — it needs independently fixable security impact.
- **NVD, and where enrichment comes from now** — what the National Vulnerability Database adds on top of a CVE, and how that changed in 2026. Teach that NIST now enriches only prioritized records, so severity, weakness and product data increasingly come from the CNA, CISA and EPSS rather than from NVD.
- **CVSS v3.1 and v4.0** — how severity is scored, by hand. Research and teach the metric groups of each version, score real CVEs in both, and show where the two disagree and why. (v4.0 renames Temporal to Threat and adds Supplemental.)
- **CWE, CAPEC, CISA KEV, EPSS** — the surrounding catalogs. Research and teach what each is for: weakness types, attack patterns, what is known to be exploited in the wild, and the probability a flaw will be — and how they are used together to prioritize.
- **Building a public track record** — the write-ups that make skill visible to a stranger: root cause, impact chain, remediation, honest about limits. This is the evidence the site's whole premise rests on.
- **AI tooling professionals use** — what the field now expects a professional to understand about AI-assisted security work. Teach it using Anthropic's Cyber Verification Program as the worked example of how the industry separates defensive, authorized, and restricted work, and of how a public record of reported vulnerabilities is treated as evidence.

### Stage D: Specialist tracks

One track per reader, taken deep. Each gets a research gloss here; `PROGRAM_MAP.md` lists the topics inside each.

- **Red team operations** — emulating a real adversary against systems the organization authorizes. Research and teach the concepts: the MITRE ATT&CK model, adversary emulation, command-and-control and evasion at a conceptual level, and purple teaming. Hands-on work goes to published emulation tests (Atomic Red Team) in a lab, not to original offensive tooling.
- **DFIR and detection engineering** — working out what happened after an incident, and building the detections that catch the next one. Research and teach: disk, memory and network forensics, the incident-response lifecycle (NIST SP 800-61, current revision), threat hunting, and writing detections in Sigma and YARA.
- **AppSec** — stopping vulnerabilities before they ship. Research and teach: threat modeling (STRIDE), the scanner families (SAST, DAST, IAST, SCA) and what each can and cannot see, secure-SDLC integration, and code review technique.
- **Exploit development and reverse engineering** — understanding at the binary level how a flaw becomes control of execution, and the mitigations that stop it. Research and teach the concepts and the mitigation landscape (ASLR, DEP, stack canaries); send hands-on practice to a teaching environment built for it (pwn.college) rather than producing working exploits for real products.
- **Malware analysis** — determining what a hostile program does. Research and teach static versus dynamic analysis, sandboxing, and behavioral indicators, performed on known samples inside an isolated lab (REMnux, FLARE VM). Teach analysis and detection, not authoring.
- **Cloud security** — the attack surface of a cloud account. Research and teach the shared-responsibility model, cloud IAM, and the common misconfigurations, with hands-on auditing using open tools (Prowler, ScoutSuite) against the reader's own account.
- **AI security** — its own track, below.

### Stage E: Expert

- **The eight CISSP domains as bodies of knowledge** — managerial and architectural breadth, not hands-on. Research and teach each domain, writing a lesson for every objective (1.1 to 8.5) an earlier lesson doesn't already cover. This track and the CISSP knowledge map are the same material seen two ways.
- **Governance frameworks** — the language organizations buy. Research and teach what each is, who needs it, and how they relate: NIST CSF 2.0 (free), ISO/IEC 27001 (paid standard — say so and teach from free summaries), and SOC 2.
- **Running a security program** — the work of the person who owns security. Research and teach security strategy, the metrics that matter, and board-level communication, as the worked work-products described in section 6.

### AI security track

- **Securing AI systems** — CAISP's seven chapters as the spine. Research and teach: how LLM applications are built and where they are attacked, the OWASP LLM Top 10 (2025 edition, LLM01 to LLM10), attacks and defenses in the build pipeline, threat modeling an AI system, the AI supply chain (model and dataset provenance, signing), and governance (NIST AI RMF, ISO/IEC 42001, EU AI Act). Each attack is taught with its defense.
- **Using AI in security work** — the SEC598 subject area (automation for offense, defense and cloud) and the SEC535 subject area (AI-enabled attack techniques). Research and teach these as concepts paired with their defenses and what a defender detects, not as attack automation to run.
- **Governing AI** — the AIGP and AAISM subject areas: AI law and policy, risk management, and the controls that implement them.

### Across every stage

- The NICE work roles each stage prepares for, using current names.
- What can be claimed at each stage, and what cannot be claimed yet.

### Role paths

The site has eight cybersecurity role pages. These are my starting guesses. Correct them from what each role page says the job is.

| Role page | Path |
|---|---|
| `/r/soc-analyst/` | A, B defensive basics, D DFIR and detection |
| `/r/security-analyst/` | A, B, C, D DFIR and detection |
| `/r/pentester/` | A, B, C, D red team, then exploit development |
| `/r/appsec/` | A, B vulnerability classes, D AppSec, E domain 8 |
| `/r/dfir/` | A, B defensive basics, D DFIR, malware analysis |
| `/r/cloud-security/` | A, D cloud, E domains 3 and 5 |
| `/r/iam-engineer/` | A (HTTP authentication, cryptography), E domain 5, D cloud IAM |
| `/r/grc-analyst/` | A (lighter), E domains 1, 2 and 6, governance frameworks, AI governance |

The map implies roles the site doesn't have: red team operator, exploit developer, malware analyst, AI security engineer, security program lead. The site only lists roles with a complete, verified route. Don't create role pages. List the candidates at Stop 1.

## 6. Lesson spec

Every lesson has these parts, in this order.

1. **Where this shows up.** The task in the job that needs this skill, and the role paths that use it. Two to four sentences.
2. **Before you start.** Prerequisite lessons and what has to be installed.
3. **How it works.** The mechanism from first principles, with one worked example the reader can reproduce. Original prose. Define each term where it is first needed, by what it does.
4. **Walkthrough.** A guided exercise on a target the reader owns or runs locally: every command, what they should see, and why.
5. **On your own.** A task with a stated success test and no steps. Hints may be collapsed.
6. **Where it goes wrong.** Failure modes, false positives, common misreadings, and the limits of the tools.
7. **Read the source.** The primary documents for the topic and how to read them: which sections, in what order, what to skip. Then at most three free resources for going deeper, each with what it is for.
8. **Check yourself.** About five questions that need explaining or predicting, never recall. Write them yourself.
9. **Prove it.** The artifact that shows the skill to someone who has never met the reader, and what the reader can and cannot honestly claim after this lesson.
10. **Leads to.** Next lessons, and the map references this lesson serves, for example CISSP 5.4 or CAISP chapter 3.

For topics with no command line (risk, governance, asset classification, audit, program leadership), the walkthrough is a worked case that produces the real work product: a risk register, a data classification scheme, a business impact analysis, an access review, an audit plan, a board memo.

Most lessons will land between 1,200 and 2,500 words before the lab steps. Use that as a sanity check, never as a target. If you can't fill "How it works" and "Walkthrough" with substance, that is a gap. Log it. Don't pad.

## 7. Rules

### Evidence

The site's rule is "no verification URL, no row". It applies here.

- Keep a source ledger. Every external fact and every recommended resource gets a row: the claim or resource, the URL of the primary source, the date you fetched it, the characters fetched, and a status.
- You can only write a row for a URL you fetched in the current session. Search snippets and your own memory don't count.
- Use the status values the repo already has. If it has none for these cases, use `verified` (you read the primary source), `unreachable` (bot wall, script-only page or paywall, with what you tried), `operator-added` (from my files, unchecked), `conflict` (two primary sources disagree, both recorded).
- Primary means the body that owns the thing: the standards body for a standard, the issuer for a syllabus, the project for a tool. Training-company blogs can help you find things. They can't be the source for a row. Never repeat an issuer's marketing claims.
- Lists and frameworks get re-issued. Name the edition and its date wherever you cite one.
- Recommended resources must be free to learn. Label them with the site's existing free-status pills. At most three per lesson, because the site keeps its routes short on purpose. Extras go in the directory.
- When a body of knowledge is defined by a paid document, such as ISO/IEC 27001, say so in one line and teach from free equivalents. When a tool's free tier has a limit that changes the workflow, state the limit.
- Write original explanations. Summarize and link. Never reproduce exam questions or copyrighted outline text; refer to objectives by number and paraphrase. Exam dumps are never a source.
- Run every walkthrough. Execute each command in a clean environment, save the transcript, and record tool versions and the date on the lesson. Where you couldn't run a step, the lesson says "not run by us" at that step.
- A gap is a valid result. Log what is missing and what you tried. Never smooth one over.

### Safety and law

- Hands-on work uses only the reader's own machines, intentionally vulnerable applications run locally (DVWA, Juice Shop, WebGoat, crAPI, DVGA), and platforms that grant permission (PortSwigger's labs, pwn.college, OverTheWire, bounty programs within their scope). Every hands-on lesson opens with the site's existing authorization notice.
- My hard rules go into the lessons as written: a name found in recon is a candidate, never permission. A scanner match on a known issue is not a new CVE. A bearer token is not a JWT until the format is identified. Never use a credential you find. Secret scanners run with verification off. Automated findings are confirmed by hand.
- Teach the attack, how defenders detect it, and the fix together.
- For C2, evasion, malware, phishing and deepfakes, and AI-assisted attack automation, teach the concepts, what defenders see, and detection. Send hands-on work to established lab environments and published emulation tests. Don't write original malware, evasion tooling, C2 setup guides, phishing kits, or working exploits for real products. My readers are learners, and their legal safety and the site's standing depend on this line.
- During research, never scan, probe or test any live system. Fetch pages to read them and do nothing else. Run labs only against local containers. If a lesson's tool needs an internet-facing target, write the walkthrough against a local lab, mark what you couldn't run, and ask me at Stop 1 whether to use a domain I own.

### Voice

Match the site: plain, direct, second person, honest about difficulty. No hype and no guarantees. "PhD-level" and "undeniable" describe the bar you build to. Keep them, and words like "guaranteed" and "job-ready", out of page copy unless I say otherwise. Give no hiring statistics without a source; where you give the site's own reasoning, label it as reasoning. Give no time estimates unless a provider states one, and attribute it.

### Working discipline

- State lives on disk. Read `STATE.md` first in every session and update it last.
- Never replace a research file wholesale. Edit in place or append. Commit after each lesson, on a working branch.
- Never report a batch as done by assertion. Report counts.
- You don't need my permission to fetch pages for research.
- Stop outside the two planned stops only for a decision that is mine: changing scope, adding a role page, editing an existing page, anything touching deployment, or a conflict between this brief and the repo that following the repo doesn't settle. Otherwise decide, log the decision in `STATE.md`, and keep going.

## 8. Order of work

Keep everything in one working folder. Use the repo's existing research location if it has one; otherwise create `security-guidebook/`.

```
STATE.md         done, next, decisions made
map.md           every lesson: id, title, stage, level, prerequisites, roles, map references
sources.csv      the source ledger
gaps.md          what could not be verified, written or run, and what was tried
lessons/<id>.md  one file per lesson
runs/<id>.log    each walkthrough as executed
reports/         one short report per batch and per stop
```

### Phase 0: Orient (read only)

This brief was written from the live site, without sight of the repo. On how the site is built, the repo is right and the brief is the guess.

Read the repo: the generator, the data files and their schemas, the templates for role, credential and directory pages, how verified dates and status labels are stored, how the build runs. Read `/method/`, one role page and one credential page. Read the two input files. Then write `STATE.md` with what you found, your URL and data plan for the four page types, and anything in this brief that conflicts with the repo. Create the working branch. Change no existing page.

### Phase 1: Research the whole map

- For every lesson in scope, find the primary sources, the best free resources (three at most), the lab target, the proof artifact, the prerequisites, and the roles and map references it serves. Record them in `map.md` and the ledger.
- Map every CISSP objective from 1.1 to 8.5 to a lesson. An objective with no lesson becomes a new lesson or a logged gap. Do the same for CAISP's seven chapters.
- Draft the eight role paths: ordered lessons, checkpoints, capstone.
- Map each stage to current NICE work roles.
- If you can run parallel workers, give each one a stage or track and its own files. Two workers never write the same file.
- Then a reviewer that did not write the rows re-fetches at least one row in six from each track and tries to disprove it. Record the failures. If more than one sampled row in ten fails, re-check that whole track before moving on.

### Phase 2: Pilot

Write four lessons to the full spec and build them into the site locally, with the pentester path page and the CISSP and CAISP map pages around them:

1. HTTP in depth (Stage A, mechanism-heavy).
2. IDOR (Stage B, hands-on).
3. Risk assessment as a worked case, serving CISSP objective 1.9 (Stage E, no command line).
4. Prompt injection, OWASP LLM01:2025, serving the CAISP map (AI track).

### Stop 1

Report and wait for me. Include: what you found in the repo; your URL and data plan; the full lesson map with levels and paths; the gap log; corrections beyond the ones in section 3; ledger counts by status and the review failure rate; how to view the pilot locally; and the questions that need my judgment.

### Phase 3: Write the rest

After I approve, work in batches, one stage or track each, in this order: A, B, C, E (CISSP domains and governance), AI track, D tracks, program leadership. Treat each batch as a fresh start: re-read `STATE.md` and this brief, and rely on nothing from earlier conversation.

For each batch: write the lessons, run the walkthroughs, then have a reviewer that did not write them follow each walkthrough from a clean environment, attempt "On your own" without the hints, and check each factual claim against its ledger row. Fix what fails, commit, update `STATE.md`, and write the batch report.

### Phase 4: Build into the site

- Use the existing generator, templates, components and design. Add no framework. Redesign nothing.
- Add the four page types. Link each role page to its path and each credential page to its knowledge map where one exists. Those links are the only edits to existing pages; show me the diff.
- Add new resources to the directory through its existing data format, with verification fields filled.
- Ship only complete lessons. No stubs.
- Check: the build passes; every internal link resolves; outbound links respond; every lesson shows its test date and source dates; no currency symbols or salary figures appear in new pages; pages work at phone width; headings and keyboard navigation match existing pages; every count comes from data.
- Preview locally. Don't deploy, don't push to the production branch, and don't touch hosting or DNS.

### Stop 2

Before any merge or deploy, report: what is built, coverage counts, known gaps, the diff to existing pages, and how to preview.

## 9. Reports

Every batch report and stop report uses the same five headings: Done, Counts, Gaps, Decisions I made, Questions for Dino. Counts always include lessons drafted and complete; ledger rows by status; walkthroughs run and not run; gaps opened and closed.

## 10. Done means

- Every lesson in scope is complete to the spec with a tested walkthrough, or is in the gap log with reasons.
- Every CISSP objective and every CAISP chapter maps to a complete lesson or a logged gap.
- Each of the eight roles has a path that ends in a capstone.
- No ledger row lacks a fetched primary URL and a date.
- The site builds, and existing pages are unchanged apart from the approved links.

## 11. Where to start looking

Starting points from memory. None of them is a verified row until you fetch it.

- Web: PortSwigger Web Security Academy; OWASP WSTG, ASVS, Top 10, API Security Top 10; MDN; the IETF RFCs for HTTP (9110), cookies (6265), TLS 1.3 (8446), OAuth 2.0 (6749), JWT (7519), TCP (9293), DNS (1034, 1035), security.txt (9116).
- Vulnerabilities and disclosure: cve.org; nvd.nist.gov; first.org for CVSS and EPSS; cwe.mitre.org; capec.mitre.org; CISA's KEV catalog; the CERT/CC and OpenSSF disclosure guides.
- Tracks: attack.mitre.org; Atomic Red Team; NIST SP 800-61, 800-115, 800-53; Sigma; YARA; Ghidra; pwn.college; REMnux.
- Governance: NIST CSF 2.0; NIST SP 800-30 and 800-37; ISO/IEC 27001 (paid); the AICPA Trust Services Criteria.
- AI security: the OWASP GenAI Security Project; atlas.mitre.org; NIST AI RMF and its Generative AI Profile; the EU AI Act text; ISO/IEC 42001 (paid); CycloneDX; Sigstore.
- Bodies of knowledge: isc2.org for the CISSP outline; practical-devsecops.com for the CAISP syllabus; iapp.org; isaca.org; sans.org and giac.org.
- Careers: NIST's NICE Framework components.

## Amendment 2026-10-09 (Dino, whole-permission order)
- §5 "OWASP LLM Top 10 (2025)": amended to the 2026 edition (verified current; released 2026-08-04; codes renumbered). Lessons teach 2026 throughout.
- Walkthrough substitution policy: local-demo/deterministic substitutions and explicit "not run by us" markers are accepted as the guidebook's honesty standard.
