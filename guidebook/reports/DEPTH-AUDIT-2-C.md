# Depth audit 2 — Stage C batch (stricter lenses)

Auditor: subagent 2e7885c9 · 2026-10-10 ~01:20–02:00 EDT.
Standard: brief §1 (the bar: "explain each mechanism from first principles, with no term
they can't unpack"; "Define each term where it is first needed, by what it does"),
§6 (ten ## sections in order), §7 (free-only, ≤3 resources, no hype).
Method: all 10 lessons re-read end to end against the FIVE new lenses. The first pass
(DEPTH-AUDIT.md, 10/10 SOLID) used different lenses and was deliberately not re-run.

Verdict: **all 10 lessons deepened.** Lenses fired 38 times total. No level changes
(levels were honest and stay). No lesson needed padding; every addition below is a
lens finding with a specific location.

## Per-lesson lens table

| Lesson | Lens 1 (jargon) | Lens 2 (why) | Lens 3 (detection) | Lens 4 (worked ex.) | Lens 5 (§7 quality) |
|---|---|---|---|---|---|
| c-cvd | embargo, adoption wait, zero-day | embargo trade + deadline rationale | — | already had | already guided |
| c-cve-program | BCP 47 | independently-fixable rule; private-first reservation | — | already had | skip-guidance added |
| c-cvss | MacroVector/equivalence class; Modified Base metrics | exploitability/impact split; why v4.0 dropped equations | — | already had (left alone) | reading-order strengthened |
| c-vuln-ecosystem | Binding Operational Directive; CPE | why the CNA record became the default | — | already had (left alone) | EPSS reading order; OIG skip guidance |
| c-incident-response | Community Profile; IOC; sinkhole; DGA; playbook; Run key | why comms order is risk management | spray-shape alert made concrete | already had | filler §7 item REPLACED (SANS Dynamic Incident Response, verified free CC BY 4.0); Velociraptor guidance |
| c-log-sources | telemetry; SIEM; C2; 5-tuple; XDR | why timing/volume survive encryption; why 4688 command lines default off | already concrete | already had | ATT&CK skip guidance |
| c-soc-triage | SIEM; threat intel; IOC; Tier 2 | why triage recommends-not-acts; why uncertainty escalates | MFA-denied burst as the concrete corroborating signal | already had | filler §7 item REPLACED (MITRE 11 Strategies, verified free) |
| c-sigma-detection | backend; pySigma; soak period | why a shared format exists; why tuning order is filters→thresholds→narrowing | — (the whole lesson is detection) | **NEW §4 step 9: real `sigma convert` run on loopback** | filler §7 item REPLACED (Sigma CLI, verified) |
| c-ai-tooling | red teaming vs pentesting; malware RE | why Red Team Access is orgs-only; why real-time blocks persist at Red Team | — | already had | already guided |
| c-public-track-record | primitive; triager; 0-day | why the 90-day deadline exists (embargo mechanism) | — | already had | already guided |

## What was added, per lesson (specific)

- **c-cvd** (§3): "Why the embargo exists — and whose interests it serves" paragraph
  (three-way trade: vendor time / deployer patch-ready / finder-and-user cost; deadline
  converts "trust us" into commitment). By-function definitions: **embargo**, **adoption
  wait** (the extra month after the patch before details publish), **zero-day**.
- **c-cve-program** (§3): "Why the rule is 'independently fixable'" (one ID per fixable
  unit — keeps the catalog aligned with the work of fixing); "private-first ordering is
  load-bearing" (a public reservation for an unpatched flaw is a pointer attackers can
  read). **BCP 47** defined (language tags `en`/`en-US`). (§7): skip-guidance on the
  cve.org Services page (skip API reference) and the schema repo (skip ADP on first pass).
- **c-cvss** (§3): equivalence class defined by function (grouping lets 15M+ vectors
  share 101 scores); "Why v4.0 abandoned the equations" (v3.x algebra vs expert ranking,
  per FIRST FAQ §3.17 — math serves judgment instead of overriding it); "Why the split"
  (exploitability = the flaw, vendor knows best; impact = the consequence, consumer
  knows best; one blended number would force the consumer to accept the vendor's
  judgment about their own losses); Modified Base metrics one-liner. (§7): read the
  Examples doc *before* the Specification; skim MacroVector math and run the reference
  implementation; skip version-history appendices; v3.1 Temporal/Environmental skip note.
- **c-vuln-ecosystem** (§3): **BOD** defined (mandatory CISA order to federal civilian
  agencies); **CPE** defined (NIST structured product naming); "Why the CNA record
  became the default" (OIG: 60,000/year projected, tenfold decade growth, NIST "no
  sustainable processes" — the default is what scales, not the best analysis). (§7):
  EPSS reading order (Why EPSS? → Using EPSS → How It Works; skip Research); OIG
  reading guidance (Report Highlights → Finding 2; skip appendices).
- **c-incident-response** (§3): **Community Profile**, **IOC**, **playbook**, **sinkhole**,
  **DGA**, **Run key** all defined by function; "the order is risk management, not
  politeness" (legal/regulatory exposure, tipping the adversary). Worked example:
  recommendation (2) now names the concrete spray-shape signal (multiple 4625s, one IP,
  ≥3 users, short window). (§7): filler item 1 ("SANS IR-related reading via free
  summaries") **replaced** with SANS *Dynamic Incident Response* (sans.org, verified
  free CC BY 4.0, no login) + read-first guidance; Velociraptor guidance added
  (Quickstart → Artifact Reference; skip VQL Reference on first pass).
- **c-log-sources** (§2/§3): **telemetry**, **SIEM**, **C2**, **5-tuple**, **XDR** defined
  by function where first needed. "Encryption hides the content, not the envelope"
  (packet sizes/send times visible — the rhythm is the signal). 4688: why command lines
  default off (Microsoft ships it Not Configured — every-process logging costs volume;
  lines land in plain text readable by anyone with log access). (§7): ATT&CK — read
  tactic pages as a map, skip technique pages on first pass.
- **c-soc-triage** (§1/§3): **SIEM**, **threat intel**, **IOC**, **Tier 2** defined by
  function. "The split is deliberate" (triage recommends; containment needs scoping,
  carries evidence/legal risk, needs authority). "The rule is asymmetric cost" (a missed
  compromise on a DC costs more than a hundred wasted escalations). Worked example
  step 7: the concrete corroborating signal (burst of "MFA denied" results after the
  travel-violating sign-in). (§7): filler item 1 ("references in sources.csv")
  **replaced** with MITRE *11 Strategies of a World-Class SOC* (mitre.org, verified free
  download, 20-page summary + full book) + read-first guidance.
- **c-sigma-detection** (§3): **backend**, **pySigma**, **soak period** defined;
  "Why a shared format exists at all" (every SIEM its own language — logic once,
  translation mechanical); "The order is load-bearing" (filters remove known-benign;
  thresholds trade TPs; narrowing is blindness wearing a tuning costume). (§4): **new
  step 9 — real backend conversion run on loopback** (sigma-cli 3.1.0, pySigma 1.5.1,
  pysigma-backend-splunk 2.1.0, pysigma-pipeline-sysmon 2.0.0, Python 3.12.3,
  2026-10-10): `sigma convert -t splunk -p sysmon encoded_ps_rule.yml` →
  `EventID=1 Image="*\\powershell.exe" CommandLine IN ("* -enc *", "* -EncodedCommand *")`
  (exit 0; transcript appended to `runs/c-sigma-detection.log`). The harness still
  stands in for corpus evaluation — the lesson says so. (§7): filler item 2
  ("references in sources.csv") **replaced** with Sigma CLI (github.com/SigmaHQ/sigma-cli,
  verified) + Usage reading guidance.
- **c-ai-tooling** (§3): red teaming vs pentesting distinguished (adversary emulation
  vs bounded assessment); malware RE defined (analysis, not reuse); why Red Team
  Access is organizations-only (accountability — a legal entity with contracts and
  someone to answer for misuse; authorization runs through organizations anyway);
  why real-time blocks persist at Red Team (those actions have no legitimate testing
  use case at any trust level — trust changes *which* work is allowed, not *whether*
  physics matters).
- **c-public-track-record** (§3): **primitive** defined (the basic capability the
  exploit is built from); **triager** defined; the 90-day deadline explained as the
  embargo mechanism (without a date, "responsible" becomes indefinite delay). (§6):
  **0-day** defined (a claim about the vendor's state, not the finding's severity).

## Lens-1 inventory (the highest-value lens, per the brief)

Terms the lessons USED but never DEFINED, now defined by function where first needed:
embargo, adoption wait, zero-day/0-day, BCP 47, MacroVector/equivalence class, Modified
Base metrics, Binding Operational Directive, CPE, CSF 2.0 Community Profile, IOC,
playbook, sinkhole, DGA, Run key, telemetry, SIEM, C2, 5-tuple, XDR, threat intel,
Tier 2, backend, pySigma, soak period, red teaming (vs pentesting), malware reverse
engineering, primitive, triager. That is 28 unpacked terms across 10 lessons.

## Sources staged

`guidebook/reports/sources-add-2-C.csv` — 12 rows, all status=verified, all fetched
in-session 2026-10-10 (in the repo, not /tmp; parent merges into sources.csv):
FIRST CVSS v4.0 FAQ (expert ranking/equivalency sets); MicrosoftDocs command-line
process auditing (default Not Configured; plain-text note); NIST NVD CPE page;
RFC Editor BCP 47; Commerce OIG OIG-26-020-I PDF (60,000/year, tenfold, "no
sustainable processes"); NIST CSF page (profiles); SANS Dynamic Incident Response
(free CC BY 4.0); MITRE 11 Strategies (free download); SigmaHQ sigma-cli README;
SigmaHQ sigma-specification README; FIRST EPSS page (section structure); Velociraptor
docs (section structure). Existing sources.csv checked first — no duplicates
(the OIG report row existed but not the fetched-PDF volume figures; the sigma-cli
and DAIR/11-Strategies URLs are new).

## Verification results

- All 10 lessons: exactly ten `^## ` sections; `^lesson_id:` present in each;
  frontmatter values untouched (no level changes).
- Banned voice words (`guaranteed`, `job-ready`, `undeniable`): zero hits across all
  10 files. No currency symbols in new copy (the one `$[0-9]` hit is pre-existing
  `$3` awk field references in c-log-sources §4).
- Resource counts: replacements only — every lesson still ≤3 free resources in §7;
  the three §7 filler rows ("references in sources.csv" / "SANS IR-related reading
  via free summaries") are gone, replaced with verified free primaries.
- Runs: `runs/c-sigma-detection.log` appended with the real sigma-cli conversion
  (tool versions + 2026-10-10 UTC date + the honest proxy-workaround note). No new
  walkthrough steps were added to any other lesson, so no other runs were needed.
- `python3 guidebook/build_site.py` from ~/workspace/learncomputerstuff: completed,
  "done", exit 0, zero errors.
- pgrep clean; /tmp test artifacts (sigma venv, rule file, corpora) removed.
- Nothing committed, nothing pushed. build_site.py, STATE.md, gaps.md, map.md,
  sources.csv untouched. No other stage's files touched.

## Word counts

2359 / 2460 / 2228 / 2414 / 2681 / 2363 / 2153 / 2439 / 2380 / 2516 (c-incident-response
and c-vuln-ecosystem sit slightly above the 2,500-word sanity band; the band is
explicitly not a target and every word above it is a lens finding, not padding).

## What I couldn't close

1. **c-ai-tooling §7 item 1 (CVP primary URL gap)** — still open from pass 1. The
   announcement URL was not fetched this session either; the lesson's honest "gap,
   stated plainly" note stands. The tier facts were not re-verified (no new factual
   claims added to this lesson, so no re-verification was triggered). Candidate for
   the coordinator's pre-publish re-fetch pass, as pass 1 recommended.
2. **BOD one-liner row** — c-vuln-ecosystem's "Binding Operational Directive is a
   mandatory CISA order to federal civilian agencies" gloss rests on the lesson's
   existing BOD-26-04 context (ledger-backed by the DEb batch: BOD 26-04 issuance
   and KEV-remediation content verified). The cisa.gov BOD page returned HTTP 403 to
   the text fetcher, so no new primary row was staged for the gloss itself; I did
   not invent one. If the parent wants a dedicated row, the BOD 26-04 directive text
   needs a fetch that clears the bot wall.
3. **Community Profile definition sourcing** — the one-liner's substance follows
   NIST CSWP 29's glossary (quoted via a search snippet, not fetched in-session);
   the staged row cites nist.gov/cyberframework (fetched: confirms CSF 2.0 Profiles
   exist as templates/resources). The staged claim is limited to what was fetched.
4. **Lens 3 on c-cvd / c-cve-program / c-cvss / c-public-track-record** — genuinely
   not applicable (disclosure mechanics, record formats, scoring math, and writing
   are not detection lessons; forcing "concrete signals" into them would be padding).
   Lens 4 on c-cvss and c-vuln-ecosystem — did not fire per the task's explicit
   instruction to leave the hand-scoring and three-way ranking alone; both already
   carry full worked examples.
