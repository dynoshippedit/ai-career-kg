---
lesson_id: c-cvss
slug: cvss
stage: C
level: 3
prerequisites: [c-cve-program]
roles: [security-analyst, pentester]
map_refs: []
test_date: 2026-10-09
description: "CVSS v3.1 and v4.0 scored by hand: the metric groups, three official calibration cases, and where the versions disagree — including E:U collapsing 7.7 to 5.2. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · v3.1 equations and FIRST's v4.0 reference implementation reproduced all published scores"
---
# CVSS v3.1 and v4.0, scored by hand


**Map ref:** Stage C — severity scoring, the language every downstream catalog speaks.

---

## 1. Where this shows up

Every prioritization decision in security runs through a CVSS score: the scanner output you triage, the KEV catalog's urgency, the vendor advisory's headline number, the risk register's "High." Most practitioners treat the score as weather — a number that arrives. This lesson makes you the meteorologist: you will compute the number yourself, in both current versions, and know exactly which judgment each decimal place rests on. That matters because the score is not a measurement — it is a structured argument, and arguments can be wrong in instructive ways. When a vendor disputes your severity rating during a disclosure (and they will), the person who can defend the vector metric by metric wins.

## 2. Before you start

- You can read a CVE record's metrics block (`c-cve-program`).
- You understand the vulnerability you are scoring — scoring what you do not understand produces confident nonsense.
- Primary references: the **FIRST CVSS v3.1 specification** and the **FIRST CVSS v4.0 specification** (version 1.2) plus its **official examples document** (version 1.8). This lesson's calibration vectors and scores were verified against the examples document on 2026-10-09.
- Tools for this lesson: a local v3.1 scorer (the walkthrough runs one) and FIRST's reference v4.0 implementation (the walkthrough runs that too). The reader's check is the FIRST web calculator.

## 3. How it works

CVSS answers one question: *how bad is this vulnerability, technically?* Not how likely it is to be exploited (that is EPSS's question — see `c-vuln-ecosystem`), not whether it is being exploited (that is KEV's question). Severity: the intrinsic technical characteristics, scored 0.0–10.0, always published with the **vector string** that produced it. A score without a vector is an opinion; a vector is an auditable argument.

**v3.1: three metric groups.** Base (the intrinsic properties — always scored), Temporal (what changes over time), Environmental (what changes for a specific deployer).

- **Base metrics** (prefix `CVSS:3.1`): Attack Vector `AV` (N etwork / A djacent / L ocal / P hysical — how the attacker reaches it), Attack Complexity `AC` (L ow / H igh), Privileges Required `PR` (N one / L ow / H igh), User Interaction `UI` (N one / R equired), Scope `S` (U nchanged / C hanged — does exploitation escape into another security authority?), and the impact triad Confidentiality / Integrity / Availability `C/I/A` (H igh / L ow / N one each).
- **Temporal metrics**: Exploit Code Maturity `E`, Remediation Level `RL`, Report Confidence `RC` — the score *as of now*. Rarely published in practice, which v4.0 noticed.
- **Environmental metrics**: Confidentiality/Integrity/Availability Requirements `CR/IR/AR` plus Modified Base metrics — the score *for your environment*.

The Base score comes from specified equations: exploitability from AV·AC·PR·UI, impact from C·I·A, combined with a round-up rule (the spec's Roundup: the smallest number to one decimal place at or above the computed value). Scope Changed uses a different impact formula — getting the scope judgment right is the highest-leverage decision in v3.1 scoring.

**v4.0: four metric groups.** Base, **Threat**, Environmental, **Supplemental**. Two changes from v3.x, and both are conceptual, not cosmetic:

1. **Threat replaced Temporal.** The time dimension is now a first-class group containing Exploit Maturity `E` (U nreported / P roof-of-concept / A ttacked). v3.1 *had* temporal metrics but almost nobody published them; v4.0's design forces the question: a vulnerability with no known exploit scores lower, visibly, on the record.
2. **Supplemental was added** — metrics that never change the score, only annotate it (Safety, Automatable, Recovery, Value Density, Vulnerability Response Effort, Provider Urgency). Context the score cannot carry.

The v4.0 Base metrics rename the impact triad into two systems: the **vulnerable system** (VC/VI/VA — what happens to the system with the flaw) and the **subsequent system** (SC/SI/SA — what happens to what it can reach afterward), replacing v3.1's single Scope bit with a real impact model. New metric **Attack Requirements** `AT` (N one / P resent) captures target-specific preconditions that v3.1 smeared into Attack Complexity. User Interaction is refined to None / Passive / Active.

v4.0 scoring is not equations but **MacroVectors**: each vector maps to an equivalence class (EQ1–EQ6), the class has a lookup-table score, and the vector's score interpolates within the class. The reference implementation is public (FIRST's cvss-v4-calculator) — the walkthrough runs it verbatim.

**Nomenclature** tells you what a number claims: `CVSS-B` (Base only), `CVSS-BT` (+Threat), `CVSS-BE` (+Environmental), `CVSS-BTE` (all three). A bare "7.3" is meaningless until you know which of these it is. Base assumes worst-case Threat and Environmental defaults; consumers refine downward or upward.

### The three calibration cases (from FIRST's official examples, v1.8)

**CVE-2022-41741** (NGINX mp4 module — attacker-controlled memory disclosure via the mp4 module):
- v3.1: `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` → **7.0**
- v4.0 Base: `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` → **7.3**
- *Where they disagree:* v3.1 says Attack Complexity High; v4.0 splits that judgment — AC:Low (the attack itself is not complex) with AT:Present (it needs a specific target precondition: the mp4 module handling attacker media). The new AT metric says what v3.1 could only mumble. Score moves 7.0 → 7.3: same severity band, better argument.

**CVE-2020-3549** (Cisco Firepower Management Center — static credentials in the sftunnel service):
- v3.1: `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` → **8.1**
- v4.0 Base: `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` → **7.7**
- v4.0 Base+Threat with Exploit Maturity Unreported: same vector + `/E:U` → **5.2**
- *Where they disagree:* twice. First, the Base refinement (AC:H→AC:L/AT:P, UI:N→UI:P — the attacker needs a user to do something passive) drops 8.1 → 7.7. Second, and this is the big one: adding the Threat group with no known exploit drops 7.7 → **5.2**. v3.1's Temporal group could have done this, but nobody published Temporal vectors; v4.0 makes the time dimension visible on the record. A "High" becomes a "Medium" the moment you ask "is anyone actually exploiting this?" — which is exactly the question a defender needs answered.

**CVE-2023-3089** (OpenShift — FIPS crypto mode bypass):
- v3.1: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` → **7.5**
- v4.0 Base: `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N` → **8.3**
- v4.0 Base+Environmental: + `/CR:H/IR:L/AR:L/MAV:N/MAC:H/MVC:H/MVI:L/MVA:L` → **8.1**
- *Where they disagree:* v3.1's single impact triad (C:H/I:N/A:N) cannot express that the *vulnerable* system's confidentiality is fully lost while integrity and availability are only lightly touched — v4.0's split VC/VI/VA says exactly that, and the score rises 7.5 → 8.3. The Environmental refinement then *lowers* it slightly (8.3 → 8.1) because this deployer's integrity/availability requirements are Low. Direction matters: v4.0 Base can score *higher* than v3.1 when the impact model is more expressive.

## 4. Walkthrough

**Fully runnable.** Transcript: `runs/c-cvss.log` (2026-10-09; python3 3.12.3, node v24.20.0).

1. **Run the v3.1 scorer.** A local implementation of the FIRST v3.1 Base equations (`cvss31.py` in the run scratch). Feed it the three calibration vectors. The run: all three computed scores matched the published scores exactly (7.0, 8.1, 7.5). *Correction logged in the transcript:* the first implementation rounded to five decimals; the spec's Roundup means one decimal place — fixed, then matched.
2. **Run the v4.0 reference implementation.** FIRST publishes its calculator logic (cvss-v4-calculator, BSD-2-Clause); the run executes it verbatim under node against the five calibration vectors (three Base, one +Threat, one +Environmental). The run: all five matched the published scores exactly (7.3, 7.7, 5.2, 8.3, 8.1), with the MacroVector shown for each.
3. **Hand-score one vector yourself.** Take CVE-2022-41741's v4.0 vector. For each metric, write one sentence of justification from the vulnerability description (e.g., "AV:L — the attacker needs local ability to supply media to the mp4 module"). Then run your vector through the reference implementation. If your score differs from 7.3, your justification is wrong somewhere — find the metric, not an excuse.
4. **Write the disagreement analysis.** For CVE-2020-3549, write the paragraph: why v3.1 says 8.1, why v4.0 Base says 7.7, and why adding E:U collapses it to 5.2. Name the mechanism (Threat group as first-class time dimension), not just the numbers.
5. **State the nomenclature.** For each of your scores, write whether it is CVSS-B, -BT, -BE, or -BTE — and what a consumer who only reads the number would wrongly assume.

## 5. On your own

**Task:** Pick a CVE from the KEV catalog that has both a v3.1 and a v4.0 vector on its record (the catalog is in `c-vuln-ecosystem`'s walkthrough). Score it by hand in both versions — metric-by-metric justifications, assembled vectors — then verify against the FIRST web calculator. Write the disagreement paragraph: where the versions differ and which version's argument you find more honest, and why.

**Success test:** Your hand-computed vectors match the calculator's scores to the decimal. Your disagreement paragraph names specific metrics (not "v4.0 is stricter") and takes a defensible position on which version argues better for *this* vulnerability.

## 6. Where it goes wrong

- **Scoring the description instead of the vulnerability.** Advisory prose exaggerates; the metrics must come from the technical facts. "Could allow" is not "does allow."
- **The Scope reflex (v3.1).** Flipping Scope to Changed because the impact *sounds* big, without identifying the second security authority. If you cannot name the subsequent system, Scope is Unchanged.
- **Confusing AT with AC (v4.0).** Attack Complexity is about the attacker's effort; Attack Requirements is about the target's preconditions. A attack that is trivial *if* the target runs a specific module is AC:L, AT:P — not AC:H.
- **Publishing Threat scores as Base scores.** A CVSS-BTE 5.2 next to a CVSS-B 7.7 without labels is a lie by omission. The nomenclature exists because the number alone misleads.
- **Treating the score as a risk rating.** CVSS measures technical severity. A 9.8 nobody can reach and a 7.5 under active exploit are different planets — likelihood and exposure live in the next lesson, not in this one.
- **Calculator worship.** The calculator computes; you judge. If the vector the calculator confirms does not match your understanding of the flaw, the flaw description needs re-reading, not the calculator.

## 7. Read the source

1. **FIRST CVSS v4.0 Specification Document** (version 1.2, first.org/cvss/v4.0/specification-document) — the metric definitions and the MacroVector scoring description. Read the Base, Threat, Environmental, and Supplemental sections; skim the scoring math, then run the reference implementation.
2. **FIRST CVSS v4.0 Examples Document** (version 1.8, first.org/cvss/v4.0/examples) — the official worked examples with v3.x comparisons. Study all three calibration cases above; they are the answer key for your hand-scoring.
3. **FIRST CVSS v3.1 Specification** (first.org/cvss/v3.1/) — the equations. Read the Base scoring section; you implemented it in the walkthrough.

Free resources (≤3): the **FIRST v4.0 web calculator** (first.org/cvss/calculator/4.0) — your verification tool; the **cvss-v4-calculator repository** (github.com/FIRSTdotorg/cvss-v4-calculator) — the reference implementation the walkthrough ran; the **v3.1 user guide** (first.org/cvss/v3.1/user-guide) — scoring judgment guidance.

## 8. Check yourself

1. A vulnerability's v4.0 Base vector scores 7.7; adding `/E:U` drops it to 5.2. Explain the mechanism — what does the Threat group know that the Base group does not, and why did v3.1 fail to make this visible in practice?
2. You score AV:N/AC:L/PR:N/UI:N with VC:H/VI:N/VA:N and no subsequent-system impact. A colleague argues Scope should be Changed "because confidentiality loss is total." What is wrong with their argument, and how does v4.0's model handle this case without a Scope bit?
3. Two vectors differ only in AT:N vs AT:P. In plain language, what fact about the world changed between them — and which v3.1 metric was doing double duty before AT existed?
4. A vendor publishes "CVSS 5.2" for a flaw you scored CVSS-B 7.7. List the two most likely innocent explanations before assuming bad faith.
5. Why must every published score carry its vector string? Give the concrete failure mode of a score without one, using the CVE-2023-3089 Environmental refinement as your example.

## 9. Prove it

**Artifact:** your three hand-scored calibration vectors with metric-by-metric justifications, the run output showing they match the published scores, and the disagreement analysis for CVE-2020-3549. This is the document you show a vendor when they dispute your severity.

**Honest claims after this lesson:** you can score any CVE by hand in v3.1 and v4.0, defend every metric choice in writing, and explain exactly where and why the versions disagree. **Cannot yet claim:** that your score is *right* in any absolute sense — CVSS is an argument framework, and two honest scorers can differ by a metric. What you can claim is that your argument is complete and checkable.

## 10. Leads to

- `c-vuln-ecosystem` — the score is one input. Likelihood (EPSS), exploitation evidence (KEV), and weakness types (CWE) are the others — and where each comes from now.
- `e-risk-assessment` reuses this lesson's discipline: severity is an input to risk, never the whole of it.
- Every Stage D track reads CVSS daily; scoring by hand is what makes you trust — and question — the numbers.
