---
lesson_id: c-sigma-detection
slug: sigma-detection
stage: C
level: 3
prerequisites: [c-log-sources, c-soc-triage]
roles: [soc-analyst, security-analyst, dfir]
map_refs: []
test_date: 2026-10-09
description: "Writing detections with Sigma: rule anatomy against the spec, the tuning loop, and detection-as-code discipline — measured, not asserted. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · rule validated and evaluated against labeled corpora"
---
# Writing Detections with Sigma


---

## 1. Where this shows up

Every alert triage ever performed started as a detection someone wrote. Detection engineering is the discipline of turning "we should notice when X happens" into a tested, tuned rule that fires on X and stays quiet on everything else — then keeping it honest as the environment changes. It is the core skill of the detection-engineering and DFIR tracks, the producer side of the SOC analyst's consumer side, and the mechanism behind every "detection coverage" claim you will ever be asked to defend. Write rules badly and the SOC drowns; write them well and triage becomes decisions instead of archaeology.

## 2. Before you start

- You know what each log source records (`c-log-sources`) — a rule is dead on arrival if its environment can't feed its `logsource`.
- You know what a triage analyst needs from an alert (`c-soc-triage`) — the rule's title, fields, and false-positive profile are a user interface.
- You can read YAML — or you can after this paragraph, which is the whole syntax this lesson needs. Sigma rules are YAML: `key: value` pairs; **indentation is nesting** (two spaces per level — tabs are illegal); a line starting with `- ` is a **list item**; `|` after a key name is a **modifier** that changes how matching works, not part of the field name (`Image|endswith` means "the Image field, matched by suffix"). If you can read that much, you can read every rule here; the walkthrough's validation step checks your reading field by field.

## 3. How it works

Sigma is the vendor-agnostic detection format: one YAML rule compiles — via pySigma backends (Sigma CLI, sigconverter.io, Detection Studio) — into Splunk SPL, Sentinel KQL, Elastic EQL, and others. Write once, run on whatever SIEM the employer has. (pySigma is the shared conversion library; a *backend* is the converter that turns one Sigma rule into the target SIEM's own query language — Splunk's SPL, Sentinel's KQL, Elastic's EQL. The rule's logic lives once, in YAML; the backend translates it.)

**Why a shared format exists at all.** Every SIEM speaks its own query language. Before Sigma, a detection written for one employer's Splunk had to be rewritten from scratch for the next employer's Sentinel — and community rule-sharing was impossible, because there was no common tongue. The format is the fix: the *logic* lives once and the *translation* is mechanical, so rules survive job changes and SIEM migrations instead of dying with the console they were written in. The format is defined by the Sigma specification (SigmaHQ/sigma-specification): the rules spec, the correlation spec (multi-event rules), the filters spec, and appendices for modifiers, tags, and the taxonomy of supported log sources. The community rule repository (SigmaHQ/sigma) holds thousands of rules in four types: generic detection, threat hunting, emerging threat, and compliance.

Read a real rule field by field — suspicious encoded PowerShell:

```yaml
title: Suspicious Encoded PowerShell Command
id: 8f3a1c2e-7d4f-4e8a-9c11-2f6b8d0a1e33
status: experimental
description: Detects PowerShell launched with an encoded command, a common obfuscation technique
references:
    - https://attack.mitre.org/techniques/T1059/001/
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains:
            - ' -enc '
            - ' -EncodedCommand '
    condition: selection
falsepositives:
    - Legitimate administration scripts
level: high
```

- **title / description:** what a human reads in the alert queue. Name the *behavior*, not the malware family — behaviors outlive campaigns.
- **id:** UUIDv4, globally unique. How rules are tracked across versions, forks, and SIEM conversions. Generate one with `python3 -c "import uuid; print(uuid.uuid4())"`.
- **status:** maturity — `experimental`, `test`, `stable`, `deprecated`, `unsupported`. Never ship `experimental` to production without a soak period (running the rule against live data in count-only mode — no pages — to measure its real false-positive rate before it can wake anyone).
- **references:** the research the rule is built on — ATT&CK technique pages, write-ups. A rule without references is un-auditable.
- **tags:** ATT&CK mapping (`attack.execution`, `attack.t1059.001`). The union of tags across your ruleset *is* your detection map — this is what makes coverage measurable.
- **logsource:** where the rule looks. `category: process_creation` + `product: windows` means "Windows process-creation telemetry" — Sysmon Event ID 1 or Windows 4688 in practice. The category is the contract: if your environment doesn't produce it, the rule is a paper rule.
- **detection / selection:** the matching logic. Fields within a selection are ANDed; list values are ORed. `Image|endswith` and `CommandLine|contains` are **modifiers** — they change *how* matching works (suffix, substring, prefix, regex, base64offset). Modifiers are the difference between a rule that fires on noise and one that fires on signal.
- **detection / condition:** the boolean combining selections — `selection`, `selection and not filter`, `1 of them`, aggregations like `count() by Hostname > 5`. Filters are named selections of known-benign patterns excluded from the alert.
- **falsepositives:** the documented benign triggers. Writing these honestly separates a production rule from a lab experiment.
- **level:** `informational / low / medium / high / critical` — the severity the rule *suggests*. Triage sets the priority; the rule does not get the last word.

**The tuning loop** keeps detections honest — detections are maintained, not launched:

1. **Baseline.** Before shipping, know what normal looks like *in your environment* — run the logic against historical data and count hits.
2. **Threshold.** Set the firing bar from the baseline: frequency thresholds, rarity windows, allowlisted entities. A rule firing 200 times a day on updater activity is broken, not sensitive.
3. **Suppress.** Build benign filters into the rule, narrow the logsource, add context. Tune in order: filters first, thresholds second, narrowing third. The order is load-bearing: a filter removes *known-benign* matches without changing what the rule catches; a threshold trades true positives for fewer false positives; narrowing the logsource changes the *population watched* — which is blindness wearing a tuning costume.
4. **Ship with a runbook.** Every production rule carries its expected FP profile and a triage runbook — analysts can't action what they can't interpret.

**Detection-as-code** treats rules like software: Sigma YAML in git; CI on every change (schema validation against the spec, linting for missing ATT&CK tags or impossible conditions, conversion to each SIEM backend, behavioral tests — the rule fires on a positive corpus and stays silent on a benign corpus); staging soak against live data to measure the real FP rate; quarterly review and retirement. A proven gap is a deliverable: run an Atomic Red Team test for a technique and get no alert — that false negative is a finding, not an absence of findings.

**Reading coverage honestly.** Rule tags aggregate into an ATT&CK Navigator layer: techniques with detections light up. But technique coverage is not *procedure* coverage — a rule for "PowerShell with encoded command" covers one procedure of T1059.001, and an adversary using a different procedure walks past it. Coverage needs the negative test, and coverage decays: new procedures, new tools, environment drift. "What we detect" means validated, tuned, production detections with runbooks, measured against positive and negative corpora, reviewed this quarter. Anything less is a claim.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/c-sigma-detection.log`. Clean environment: stock Python 3.12.3 with PyYAML, 2026-10-09. The rule and both corpora are **fictional and labeled as such**; the evaluator is a teaching harness that applies the rule's selection logic the way a SIEM backend would, so you can watch the tuning loop change the numbers.

1. **Write the rule.** Save the encoded-PowerShell rule above as `encoded_ps_rule.yml`. Note every required spec field is present: title, id, status, description, logsource, detection, level.
2. **Validate the schema.** Parse the YAML and check the required top-level fields plus the logsource contract (`category: process_creation`, `product: windows`). The script prints each modifier found (`Image|endswith`, `CommandLine|contains`) — say out loud what each modifier does to matching.
3. **Build the corpora.** `positive_corpus.jsonl`: two encoded-PowerShell executions that *should* fire. `benign_corpus.jsonl`: three events that should *not* — a normal script launch, a known-benign updater using `-EncodedCommand`, and a `cmd.exe` launch (wrong image entirely).
4. **Run v1 — the rule as written.** Positive: 2 fired of 2 (TP=2, FN=0). Benign: 1 fired of 3 — the updater trips the rule (FP=1, TN=2). This is the moment most beginners skip: *measure the false positives before shipping*.
5. **Tune — add the benign filter.** The updater is known: same user, same identifiable command marker. Add it as a named filter (`selection and not filter`) — filters first, per the tuning order.
6. **Run v2.** Positive: still 2/2. Benign: 0/3. False positives: 1 → 0, true positives unchanged. That delta is the entire tuning loop in miniature: the rule got *quieter* without getting *blinder*.
7. **Write the runbook stub.** Three lines per the lesson: what the alert means, the first three triage checks (parent process? user context? decode the command?), and the escalation criterion. A rule without a runbook doesn't ship.
8. **Record the honest limitation.** The harness matched substrings; a real backend compiles to the SIEM's query language, and translation can change semantics (case sensitivity, regex dialect). The lesson's corpora are two and three events — production behavioral tests use hundreds. Note both in the log.
9. **Convert for real.** Install the reference compiler and a backend on your own machine: `pip install sigma-cli pysigma-backend-splunk pysigma-pipeline-sysmon`. Then run `sigma convert -t splunk -p sysmon encoded_ps_rule.yml`. The run (transcript: `runs/c-sigma-detection.log`, 2026-10-10) produced the Splunk search below — the rule you wrote, now as the query the SIEM would execute:
   ```
   EventID=1 Image="*\\powershell.exe" CommandLine IN ("* -enc *", "* -EncodedCommand *")
   ```
   Compare it with the harness's matching logic from step 4: same behavior, real syntax. This is the detection-as-code promise made concrete — the YAML you maintain compiles to whatever the employer's console speaks.

No step above is marked "not run by us" — the schema validation, both corpus runs, the tuning delta, the limitation notes, and the backend conversion all executed and the transcript records the real numbers. (The corpus *evaluation* still uses the teaching harness — only the conversion step runs the real compiler.)

## 5. On your own

**Task:** Write a Sigma rule for a *different* behavior from the log-sources lesson — the password-spray shape (many 4625s, one source IP, multiple users, short window). You'll need an aggregation condition (`count() by`), which the walkthrough rule didn't use. Build a positive corpus (spray events) and a benign corpus (a user fat-fingering their password six times, a service account's normal auth pattern), and tune until FP=0 without losing the TP.

**Success test:** Your rule fires on the spray, stays silent on both benign cases, carries a valid ATT&CK tag, and has a three-line runbook. If you can't write the runbook, you don't understand your own rule yet.

## 6. Where it goes wrong

- **Matching the tool, not the behavior.** A rule for `mimikatz.exe` misses the renamed binary; a rule for LSASS access catches the technique. Behaviors outlive filenames — the title guidance exists for this reason.
- **Shipping experimental.** `status: experimental` in production is a pager-duty generator. Soak new rules, measure the FP rate, promote deliberately.
- **Tuning by narrowing the logsource.** Restricting the rule to "only servers" because workstations are noisy doesn't tune the rule — it blinds it. Filters first, thresholds second, narrowing last, and narrowing needs a written justification.
- **No negative corpus.** A rule tested only against events it should catch is untested. The benign corpus is where production FPs come from; build it from *your* environment's actual noise.
- **Tagging without testing.** An `attack.t1059.001` tag claims technique coverage. Without an executed test (Atomic Red Team or equivalent), it's a claim, not coverage — and procedure coverage is narrower than the tag suggests.
- **Letting rules rot.** Environment changes, vendor API changes, attacker drift: rule decay is silent. The quarterly review exists because "it worked last year" is not a status.

## 7. Read the source

Primary documents first:

- **Sigma specification** (github.com/SigmaHQ/sigma-specification) — *read* the Sigma Rules Specification fully; *skim* the modifiers appendix (it's a reference); *read* the tags appendix before you tag anything; *note* the 2.x version changes. This is the contract your rules are written against.
- **Sigma main rule repository** (github.com/SigmaHQ/sigma) — *read* five rules in your logsource categories as style references; *note* the four rule types (generic detection, threat hunting, emerging threat, compliance).
- **NIST SP 800-61 Rev. 3** (csrc.nist.gov/pubs/sp/800/61/r3/final) — *read* the detection-and-analysis framing; *note* the April 2025 date and CSF 2.0 Community Profile structure — old four-phase summaries are stale.

Then at most three free resources:

1. **Atomic Red Team** (github.com/redcanaryco/atomic-red-team) — free adversary-emulation tests mapped to ATT&CK: the positive corpus for validating your detections, and the honest way to prove a gap.
2. **Sigma CLI** (github.com/SigmaHQ/sigma-cli) — the reference compiler this lesson's walkthrough now runs. Read the README's Usage section: the commands that matter are `sigma plugin list` / `sigma plugin install <backend>` (fetching backends) and `sigma convert -t <backend> -p <pipeline> <rule.yml>` (the conversion, with `-p` naming the log-source pipeline). Skip the output-format options (`-f`, `--output-dir`) until you ship to a real SIEM.
3. **MITRE ATT&CK Navigator** (mitre-attack.github.io/attack-navigator/) — free; layer your rule tags over the matrix and look at what's dark — that darkness is your roadmap.

## 8. Check yourself

1. Your rule fires 200 times a day, all on the same updater process. Walk the tuning loop in order and explain what you change at each step — and which step you must *not* reach for first.
2. Explain why `status: experimental` must never ship to production, and what the soak period is actually measuring.
3. A rule tagged `attack.t1059.001` fires on encoded PowerShell. An adversary runs the same objective via `mshta.exe` and JavaScript. Explain, using procedure-vs-technique coverage, why the tag overclaims — and what would make the claim true.
4. Your benign corpus has three events and production has three million. Explain what the tiny corpus can prove, what it cannot, and where the real FP risk comes from.
5. Two rules detect the same behavior; one has a runbook, one doesn't. Explain why the runbook-less rule is a liability to the triage analyst even if its logic is perfect.

## 9. Prove it

**Artifact:** the §5 password-spray rule bundle — the Sigma YAML (valid against the spec, ATT&CK-tagged), both corpora, the before/after tuning numbers, and the three-line runbook — committed as a detection-as-code bundle. Not the walkthrough's encoded-PowerShell rule: the walkthrough taught the loop; the spray rule proves you can run it on a behavior you weren't handed.

**Honest claim:** "I can write a Sigma rule against the specification, validate it, measure it against positive and negative corpora, tune it without losing true positives, and ship it with a runbook."
**Can't claim yet:** "I have production detection coverage" — that needs a SIEM, a soak period, quarterly review, and executed adversary tests (`d-dfir-deep` track).

## 10. Leads to

- `c-soc-triage` — back to the consumer: your close codes are the tuning telemetry for the next rule revision.
- `c-incident-response` — what happens when a tuned, validated detection fires on something real.
- `b-command-injection`, `b-sqli`, `b-xss` — the attack lessons whose procedures your future rules will encode; each "how defenders see it" section is a rule waiting to be written.
- Map refs: **Stage C · Professional**; NICE **Protection and Defense**; the `/r/soc-analyst/` and `/r/dfir/` paths.
