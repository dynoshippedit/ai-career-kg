# OSINT and research discipline

**ID:** `a-osint-research` · **Stage:** A (Foundations) · **Level:** 3 (apply — you can conduct passive reconnaissance against public sources and document it to a professional standard) · **Prerequisites:** `a-http-depth` (you will read a lot of HTTP), `b-authorization-scope` (the rules that make this lesson safe — read it first if you haven't).

**Map refs:** Stage A foundation; the passive half of `b-methodology`'s reconnaissance phase; feeds every Stage B engagement.

---

## 1. Where this shows up

Every authorized engagement in `b-methodology` begins with reconnaissance — and the first half of reconnaissance never touches the target at all. OSINT (open-source intelligence) is the discipline of learning from what is already public: DNS records, certificate logs, archived pages, job postings, code repositories, social profiles, regulatory filings. Done well, it builds the target map *before* a single packet is sent in anger, which means less active probing, less risk of stepping outside scope, and findings the target didn't know were public. Done badly, it becomes stalking, harassment, or the pretext for unauthorized access. This lesson teaches the technique and the discipline together, because in this field they are the same skill: knowing what is public, what is not, and where the line sits. The walkthrough uses a fictional company and local files only — you will never touch a real target in this lesson.

## 2. Before you start

- `b-authorization-scope` read and understood — especially the hard rule that testing outside written authorization is a crime, and the subtler rule this lesson adds: **a name found is not permission.** Finding an admin panel in a sitemap does not authorize you to log into it.
- `a-http-depth` — you will read robots.txt, sitemaps, headers, and HTML source.
- The fictional target dossier in `/tmp/osintwalk/harborlight/` (created in the walkthrough): robots.txt, sitemap.xml, index.html, and a zone file for the fictional `harborlight-books.example`. Everything below runs against these local files.
- A notebook (paper or text file). OSINT without notes is just browsing; the artifact of this lesson is documentation.

## 3. How it works

**Passive vs active: the bright line.** Passive reconnaissance reads information someone else published or that a third party recorded: DNS zone data from a public resolver, certificates from transparency logs, pages from web archives, the target's own robots.txt. You never send a packet *to the target* that it didn't invite. Active reconnaissance touches the target: port scans, directory brute-forcing, sending requests to endpoints you found. The distinction matters legally and ethically — `b-methodology` teaches that active recon belongs inside a signed scope, and passive recon is what you do *before* the scope exists, to write an informed one. The walkthrough never leaves passive: every finding below comes from reading files.

**What "public" actually means.** A fact is public if it was published for the world to read: a DNS record served to any resolver, a page on the open web, a certificate submitted to a transparency log, a job ad describing the tech stack. A fact is *not* public because you *could* reach it: an unlisted admin panel, an open S3 bucket, a staging server with no authentication are *exposed*, not public — accessing them without authorization is the crime `b-authorization-scope` describes, and finding them via OSINT doesn't change that. The discipline: OSINT tells you what exists; authorization tells you what you may touch. Never let the first answer the second.

**The standard sources, and what each answers.** DNS records (what names exist, where mail goes — MX records name the mail provider, TXT records leak verification tokens and SPF policy), certificate transparency logs (every publicly-trusted certificate is logged with its domain names — the classic subdomain enumeration source), robots.txt and sitemap.xml (the site's own map of itself, including the parts it asked crawlers not to index), HTML source (comments, meta generator tags, JavaScript file paths), web archives (what the site *used to* say — removed pages, old employee names), job postings and tech blogs (the stack, the vendors, the team), code repositories (committed secrets, internal hostnames in config examples), and social/professional profiles (who works there, what they work on — people are the softest source and the most ethically loaded; read, don't contact).

**Reading robots.txt like an analyst.** The walkthrough's fictional robots.txt disallows `/admin/`, `/staging/`, and `/backup-2024/`. Three observations, in analyst order: (1) these paths exist or existed — the site told you; (2) `/backup-2024/` with a year in it smells like a forgotten artifact, the highest-value shape; (3) none of this authorizes a visit — `Disallow` is a request to crawlers, not a lock, and not an invitation. The finding goes in your notes as "exposed path *candidates*, passive only, do not touch without scope." That sentence is the discipline made concrete.

**HTML source is a confession booth.** The walkthrough's index.html contains two comments — one naming a staging link to remove, one stating the admin panel "uses default creds" — plus a generator meta tag (`HarborPress 2.4.1`) and an author name. Comments are developers talking to each other in a medium the whole world can read; generator tags version the stack for free (a version number plus a vulnerability database is a finding pipeline); author names feed the people-mapping half of OSINT. None of this required anything but *reading the page the site serves to everyone*.

**DNS as biography.** The fictional zone file lists `www`, `mail` (with its MX), `staging`, and `vpn` subdomains. Each answers a question: `mail` → who handles email (phishing-relevant, defensively); `staging` → a pre-production environment exists (often weaker than production); `vpn` → remote access exists (an authentication surface). In the real world you read this from public resolvers and certificate logs without touching the target's infrastructure. The zone file also demonstrates the mindset: every name is a hypothesis about infrastructure, and infrastructure is attack surface.

**Documentation is the deliverable.** Raw findings are noise; a reconnaissance report is signal. For each finding record: the source (exact: "robots.txt, line 3"), what it states (quote it), what it *implies* (clearly labeled as inference), and its status (passive/public vs needs-authorized-followup). The walkthrough's step 5 compresses nine findings into one line per source — that compression, source-first, is the format. A stranger should be able to re-derive every finding from your citations. That standard — *re-derivable* — is what makes OSINT evidence rather than trivia.

**The ethics, stated plainly.** Do not contact employees. Do not create accounts to see more. Do not use personal data (addresses, family, non-public profiles) — if your "reconnaissance" would read as stalking to the person, stop. Do not publish personal data you find, even if it was public; the lesson's proof artifact uses the fictional company for exactly this reason. And never use OSINT findings to justify exceeding scope: "I found it on Shodan" has never been authorization.

### Worked example: the Harborlight dossier

Fictional company `harborlight-books.example`, nine findings from four local files, zero packets sent:

| # | Source | States | Implies (labeled inference) |
|---|---|---|---|
| 1–3 | robots.txt | Disallows `/admin/`, `/staging/`, `/backup-2024/` | Those paths exist or existed; `/backup-2024/` is the highest-interest shape |
| 4 | sitemap.xml | Lists `/staging/preview` | Staging content is indexed — pre-production exposed |
| 5–6 | index.html comments | Staging link TODO; admin panel "uses default creds" | Developer hygiene gap; credential weakness *claimed by the site itself* |
| 7 | index.html meta | `HarborPress 2.4.1`, author `M. Okafor` | Stack versioned (vuln-DB lookup possible); a named person |
| 8–9 | zone file | `staging`, `vpn` subdomains | Pre-prod and remote-access infrastructure exist |

Every row re-derivable from the cited file. Findings 1–9 are all *passive/public*; acting on any of them (visiting `/admin/`, trying the default creds) requires written authorization — the sentence that connects this lesson to `b-authorization-scope`.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/a-osint-research.log`. Clean environment: local files only in `/tmp/osintwalk/harborlight/`, 2026-10-09. The target is fictional; no real system was touched, no network request left the machine.

1. **Assemble the dossier.** `ls /tmp/osintwalk/harborlight/` — four files. State the rule before you begin: everything below is reading; nothing below touches a target.
2. **Read robots.txt.** `cat robots.txt` — three `Disallow` entries plus a sitemap pointer. Write each as a candidate finding with the "do not touch without scope" caveat.
3. **Enumerate the sitemap.** `grep -o "<loc>[^<]*" sitemap.xml` — four paths; flag `/staging/preview` as the anomaly (staging in the *public* sitemap).
4. **Read the HTML source.** `grep -o "<!--.*-->" index.html` (two comments — quote both in your notes) and the meta tags (generator version + author name). Note which findings are *stated* vs *inferred*.
5. **Read the zone file.** Extract subdomain names — `www`, `mail`, `staging`, `vpn`. For each, write the one-sentence infrastructure hypothesis.
6. **Write the report.** Compress to the table format from §3: source, states, implies, status. Nine findings, each re-derivable. This table *is* the walkthrough's output.

## 5. On your own

**Task:** Build a second fictional dossier for a made-up company (different industry, your choice): write its robots.txt (with at least two interesting disallows), a sitemap.xml (with one anomaly), an index.html (with one revealing comment and one generator/author meta), and a zone file (with at least three subdomains beyond www). Then produce the findings table: minimum eight findings, each with source line, stated fact, labeled inference, and status. Then write the three-sentence "scope memo" you'd attach: what this passive recon justifies *proposing* for authorized active follow-up, and what it does not authorize.

**Success test:** Eight findings, each re-derivable from a cited line; every inference labeled as inference; the scope memo correctly withholds authorization for touching anything found (passive findings propose, they never permit).

**Hints:** The most realistic fictional details come from real patterns: year-stamped backup paths, staging subdomains, version-revealing generator tags, MX records pointing at big providers.

## 6. Where it goes wrong

- **"It's public, so I can use it."** Public to read is not permission to act. The admin panel in the sitemap is readable knowledge; logging into it is unauthorized access. This confusion is the single most common ethical failure in beginner OSINT.
- **Contacting people.** OSINT is reading, not interviewing. Messaging employees "for research" is social engineering with extra steps, and it burns the target's trust before an engagement begins.
- **Collecting personal data.** Home addresses, family members, non-public photos — if it's about a person rather than infrastructure, the bar is far higher, and for this program's purposes it's out of scope entirely.
- **Publishing findings about real targets.** Even accurate, public-source findings can harm when aggregated and published. The program's proof artifacts use fictional companies; keep it that way until a real engagement's reporting rules apply.
- **Treating absence as evidence.** "No LinkedIn profile found" proves nothing — people opt out, names collide. OSINT findings are positive claims from positive sources; negative results are notes, not conclusions.
- **Skipping documentation.** Findings without sources are rumors. The table format exists because six months later, you (or an auditor) must re-derive everything.

## 7. Read the source

Primary documents first:

- **OWASP WSTG — Information Gathering** (owasp.org/www-project-web-security-testing-guide — the WSTG v4.2 information-gathering category, verified 2026-10-09 via the `b-methodology` lesson's research) — *read* the category's test cases as the professional checklist this lesson's techniques feed into: WSTG-INFO-01 through 10 map nearly 1:1 to the sources in §3.

Then at most three free resources:

1. **OSINT Framework** (osintframework.com — lead, verify at build time) — the community's categorized tool directory for OSINT sources. Use it as a *menu*, not a to-do list: pick the source that answers your question.
2. **Bellingcat's Online Investigation Toolkit** (bellingcat.com — lead, verify at build time) — the investigative-journalism standard for open-source research discipline; its verification chapters (geolocation, chronolocation, source evaluation) are the rigor this lesson's documentation standard comes from.
3. **Tracelabs / search-party exercises** (tracelabs.org — lead, verify at build time) — consent-based missing-persons OSINT exercises: real technique practice inside an ethical frame, with permission built in.

## 8. Check yourself

1. You find `/backup-2024/` in a real target's robots.txt during pre-scope recon. State exactly what you may do with this finding, and what you may not do — citing the rule, not your instincts.
2. A certificate transparency log shows 40 subdomains for the target. Is querying that log passive or active? Explain what makes it so.
3. Your notes say "admin panel uses default creds (per HTML comment)." Break that into *stated fact* vs *inference*, and state what would be needed to turn it into a confirmed finding.
4. Name three things a job posting can reveal about a target's infrastructure, and for each, whether acting on it needs authorization.
5. A teammate proposes messaging a target's developer on social media "to ask about their stack." Explain why this is out of bounds, in two sentences.

## 9. Prove it

**Artifact:** A reconnaissance report on a fictional company (yours from §5, or a fresh one): the dossier files, the findings table (≥8 findings, each re-derivable), and the scope memo. Published in your repo.

**Honest claim:** "I can conduct passive reconnaissance from public sources and document it so a stranger can re-derive every finding — demonstrated on a fictional target, report linked here."

**You cannot yet claim:** reconnaissance against real targets — that happens inside authorized engagements (`b-methodology`), where the reporting rules and scope boundaries of real work apply. The technique is real; the target here is deliberately not.

## 10. Leads to

- `b-authorization-scope` — the rules that govern everything this lesson's findings might one day justify proposing.
- `b-methodology` — where passive recon becomes the first phase of a real engagement, and this lesson's report format becomes professional practice.
- `b-toolbench` — the tools that automate the sources in §3 (subdomain enumeration, certificate search).
- `c-soc-triage` — the defender's mirror: your recon techniques are what the SOC watches for.
