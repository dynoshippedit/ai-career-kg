---
lesson_id: e-security-models
slug: security-models
stage: E
level: 2
prerequisites: [e-secure-design]
roles: []
map_refs: ["CISSP 3.2"]
test_date: 2026-10-10
description: "State the rules of Bell-LaPadula, Biba, Clark-Wilson, and Brewer-Nash, run a Bell-LaPadula rule check in Python, and write model-selection rationales. A free lesson in the security guidebook, serving CISSP objective 3.2."
dateline: "Walkthrough run 2026-10-10 · local stdlib Python, nothing external touched"
---
# Formal security models: what "secure" means, precisely


**Map ref:** serves **CISSP objective 3.2** — formal models of security policy: confidentiality, integrity, and conflict-of-interest models, and selecting among them.

---

## 1. Where this shows up

Security policies are usually written in English, and English is where precision goes to die. "Only authorized users may see sensitive data" means something different to everyone who reads it — which is why the field built formal models: mathematical definitions of what "secure" means for a system, precise enough that you can prove whether a given state, or a given operation, preserves the property. Bell-LaPadula defined confidentiality as a property of information flow; Biba defined integrity as its dual; Clark-Wilson defined it as commercial common sense; Brewer-Nash defined it for conflict of interest. They show up in evaluated operating systems, in the mandatory access control labels of government systems, in the design rationale of any system that must *prove* an information-flow property rather than merely assert it, and on the CISSP because they are the vocabulary in which the profession argues about policy. You will not deploy Bell-LaPadula raw — but you will recognize its rules inside SELinux type enforcement, inside data-loss-prevention policies, and inside every "no read up, no write down" argument you will ever have.

## 2. Before you start

- You can state the design principles this lesson formalizes — complete mediation and least privilege (`e-secure-design`).
- Python 3, stdlib only. The walkthrough runs locally; nothing touches the network.
- You will read sections of the original papers (all freely available): Bell and LaPadula's 1973/1976 MITRE reports, Brewer and Nash's 1989 IEEE paper, and university lecture notes on Clark-Wilson and Biba.

## 3. How it works

**What a model is.** A security model has three parts: a set of **subjects** (active entities — users, processes), a set of **objects** (passive entities — files, records), and a set of **rules** governing which operations subjects may perform on objects. The model defines a property — "no confidential information flows to an uncleared subject" — and then proves that if the initial state satisfies it and every operation preserves it, the system stays secure. That proof structure is the whole point: models move security from assertion to argument.

**Bell-LaPadula (confidentiality).** Bell and LaPadula (MITRE, 1973–76) model multilevel security: every subject has a **clearance** and every object a **classification**, drawn from an ordered lattice (Unclassified < Confidential < Secret < Top Secret, plus compartments). Two rules:

- **Simple security property ("no read up"):** a subject may read an object only if the subject's clearance dominates the object's classification. Information flows from object to subject, so reading up would carry high information down.
- **\*-property ("no write down"):** a subject may write to an object only if the object's classification dominates the subject's clearance. Writing down would carry high information into a low object.

Together they confine information to flow *upward or level* — never down. The model's power is its proof: the Basic Security Theorem shows the rules preserve security across state transitions. Its famous gaps: it says nothing about integrity (a low-integrity process can write *up* and corrupt high data — allowed by the rules), and it ignores covert channels. Real systems add the **strong \*-property** (read/write only at the same level) to close the write-up hole you will see in the demo.

**Biba (integrity, the dual).** Biba (MITRE, 1977) observed that integrity is the mirror image of confidentiality: assign **integrity levels** instead of clearances, and reverse the rules — **no read down** (a high-integrity subject must not read low-integrity data, lest it be contaminated) and **no write up** (low-integrity subjects must not modify high-integrity objects). Same lattice machinery, opposite direction. Where BLP protects secrets from the curious, Biba protects trusted data from the untrustworthy. It fits systems where correctness outranks secrecy — but the strict policy is so rigid that Biba also proposed weaker variants (low-water-mark, ring policies) that trade purity for usability.

**Clark-Wilson (commercial integrity).** Clark and Wilson (IEEE, 1987) argued that businesses don't think in lattices at all — they think in **well-formed transactions** and **separation of duties**. The model distinguishes **constrained data items** (CDIs, the data whose integrity matters) from unconstrained ones, and requires that CDIs change only through certified **transformation procedures** (TPs) — the double-entry bookkeeping of the digital world: the procedure, not the user's discretion, guarantees the result stays valid. **Integrity verification procedures** check the CDIs' consistency; access is mediated by triples (user, TP, CDI) so nobody can touch data except through approved procedures; and separation of duties is built in (the person who certifies a TP cannot be the person who executes it). Where BLP asks "what level are you?", Clark-Wilson asks "which approved procedure are you running, and who certified it?" It is the model of banking systems, and its vocabulary — well-formed transactions, separation of duties — is commercial security's native tongue.

**Brewer-Nash, the Chinese Wall (conflict of interest).** Brewer and Nash (IEEE, 1989) model a different problem: a consultancy whose analysts serve competing clients. Objects are grouped into **conflict-of-interest classes** (e.g., all banks), each containing **datasets** (individual clients). The rule: once a subject reads from one dataset in a class, the wall *rises* — the subject can never read from another dataset in the same class, because the first dataset's knowledge would taint the second engagement. Unlike BLP's static labels, the wall is **dynamic**: access history changes what is permitted next. Sanitized (public) data sits outside the wall and is freely readable. It is the model of investment banking, law firms, and any organization where the threat is not clearance but conflict.

**How they relate.** BLP and Biba are duals — same lattice, opposite flow, confidentiality versus integrity. Clark-Wilson abandons the lattice for procedures — integrity as *correct process* rather than *level hygiene*. Brewer-Nash abandons static labels for history — policy as a function of what you have already seen. Selecting among them is the expert judgment this lesson teaches.

### Worked example: model selection for three scenarios

**Scenario A — military intelligence records system.** Multiple classification levels, uncleared analysts must never see compartmented data, and the system's job is to prevent disclosure. **Selection: Bell-LaPadula.** The requirement is exactly BLP's property: information must never flow down. Biba is wrong here — integrity is secondary to preventing disclosure, and Biba's "no read down" would bizarrely forbid analysts from reading *unclassified* reference data. Clark-Wilson is wrong — there are no well-formed transactions, only read-mostly analysis. Brewer-Nash is wrong — the conflict structure is static hierarchy, not dynamic client conflicts.

**Scenario B — a bank's ledger system.** The catastrophe is not disclosure but an unbalanced book: unauthorized or malformed updates to account balances. **Selection: Clark-Wilson.** The requirement is that every state change goes through certified procedures (post, reconcile, audit) with separation of duties between the clerk who enters and the officer who approves. BLP is wrong — tellers legitimately see balances, and lattice labels add nothing to transaction correctness. Biba's strict policy is nearly unusable here (a clerk could never read a low-integrity memo and then post), and Brewer-Nash answers a question nobody asked.

**Scenario C — a consultancy serving competing bidders.** Analysts advise multiple clients; the danger is one client's strategy leaking into advice for a competitor. **Selection: Brewer-Nash.** The conflict structure is dynamic: the wall must rise based on which engagements each analyst has actually touched. BLP is wrong — there is no hierarchy of clearances, only a flat set of conflicts. Clark-Wilson is wrong — the procedures are bespoke advice, not certifiable transactions. Sanitized market data stays outside the wall for everyone.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/e-security-models.log`. Python 3, stdlib only, 2026-10-10, no network. The script implements BLP's two rules over a tiny labeled file set (4 subjects, 4 objects, levels 0–3) and evaluates 8 operations.

1. **Read the transcript's setup.** Four clearance levels (0=Unclassified … 3=Top Secret); subjects `analyst_smith` (2), `operator_jones` (1), `director_cho` (3); objects from `press_release.txt` (0) to `source_identities.txt` (3). All labels are fictional.
2. **Check the two DENYs.** `analyst_smith` reading `source_identities.txt` is denied — clearance 2 < classification 3, the simple security property ("no read up"). `analyst_smith` writing `press_release.txt` is denied — writing down would move Secret information into an Unclassified object, the \*-property.
3. **Find the allowed operation the model purists dislike.** `operator_jones` (clearance 1) *writing* `source_identities.txt` (level 3) is ALLOWED — "no write down" permits write-up. This is BLP as published: the \*-property constrains only downward flow. Real systems close it with the strong \*-property (read/write at equal level only), because a low process writing high objects is an integrity disaster — which is exactly the gap Biba was built to address.
4. **Verify the count.** 6 allowed, 2 denied — matches the transcript. Reproduce it: run the script yourself with different labels and confirm the rule decisions change exactly where the dominance relation changes.
5. **Write the selection rationale.** For each of the three scenarios above, write one paragraph: the chosen model, the property it enforces, and why each of the other three fails. If you cannot name the failure mode of the rejected models, you have not understood the chosen one.

## 5. On your own

**Task:** Extend the BLP script with Biba's rules as a second mode (integrity levels, no read down / no write up), then evaluate the same 8 operations under Biba and diff the decisions. Write one paragraph explaining, for each operation where the verdicts differ, which property (confidentiality vs integrity) the operation threatens.

**Success test:** Your diff shows exactly the operations where confidentiality and integrity rules diverge (hint: the two BLP DENYs and the write-up ALLOW behave differently under Biba). Your paragraph names the threatened property per operation without hedging.

## 6. Where it goes wrong

- **Deploying the model instead of its lesson.** Nobody runs raw BLP; its value is the vocabulary and the proof structure. Teams that "implement Bell-LaPadula" usually implement labels and call it done, without the state-machine discipline the theorem requires.
- **Confidentiality models for integrity problems.** Applying BLP where Clark-Wilson belongs — labeling bank ledgers by secrecy while tellers run arbitrary SQL — protects the wrong property against the wrong threat.
- **The write-up hole.** Forgetting that published BLP permits low-to-high writes, and therefore permits integrity corruption by design. The strong \*-property or a companion integrity model is not optional.
- **Static labels for dynamic conflicts.** BLP labels never change with history; Brewer-Nash exists because some policies *must*. Using clearances for conflict-of-interest is a category error.
- **Ignoring the model's stated limits.** BLP proves nothing about covert channels, availability, or correct initial labeling. A proof is only as strong as its assumptions — the initial secure state is assumed, not derived.
- **Lattice worship.** Real organizations have incomparable categories (compartments) and messy exceptions; forcing a total order where none exists produces labels everyone ignores. The model serves the policy, not the reverse.

## 7. Read the source

Primary documents first:

- **Bell, D. E. & LaPadula, L. J., "Secure Computer Systems: Mathematical Foundations"** (MITRE MTR-2547, 1973; freely hosted mirror) — *read* the model definition and the security properties; *skim* the systems-theory framing. The founding document.
- **Brewer, D. F. C. & Nash, M. J., "The Chinese Wall Security Policy"** (IEEE Symposium on Security and Privacy, 1989; freely hosted mirror) — *read* the wall rules and the sanitized-data treatment; short and precise.
- **Cornell CS 513 lecture notes, "Commercial Security Policies"** (cs.cornell.edu) — *read* the Clark-Wilson treatment: well-formed transactions, the CDI/TP distinction, separation of duties. The clearest free exposition of the 1987 paper's argument.

Then at most three free resources:

1. **Purdue CS 526 handout 06, "Integrity Protection"** (cs.purdue.edu) — free; Biba's policies (strict, low-water-mark, ring) and the Clark-Wilson/Brewer-Nash summaries in one university handout.
2. **NIST's Early Computer Security Papers collection** (csrc.nist.gov) — free; the historical context in which BLP was written, including the original bibliographic record.
3. **MITRE ATT&CK** (attack.mitre.org) — free; not a model, but the modern catalog of what the models' adversaries actually do — read it to ground the abstractions.

## 8. Check yourself

1. Under BLP, a Secret-cleared analyst writes a summary into an Unclassified file. Name the rule violated, the information-flow direction the rule protects, and what the analyst must do instead under the strong \*-property.
2. A bank proposes BLP labels on its ledger: tellers get "Confidential," the ledger is "Secret." Explain the category error — which property the bank actually needs, and which model enforces it.
3. An analyst reads sanitized market data, then client A's strategy memo, then requests client B's memo (A and B compete). Under Brewer-Nash, which request is denied and why — and what is the status of the sanitized data throughout?
4. Under Biba's strict integrity policy, a high-integrity reporting process needs to ingest a low-integrity web feed. Name the rule that blocks the naive design and sketch two compliant alternatives.
5. Predict what breaks first when a consultancy implements Chinese-Wall policy with static BLP-style labels assigned at hire: the confidentiality of client data, the usability for new engagements, or the auditability — and describe the incident that reveals it.

## 9. Prove it

**Artifact:** the BLP script run on your machine (transcript showing allowed/denied per operation) plus your Biba-mode extension with the diff, and the three-scenario selection rationale written in your own words.

**Honest claim:** "I can state each model's rules, demonstrate what Bell-LaPadula permits and denies on a labeled system, and argue which model fits a scenario — including why the others don't."
**Can't claim yet:** "I can build a verified multilevel-secure system" — implementing an evaluated system (reference monitor, covert-channel analysis, formal proof) is a specialized engineering discipline; this lesson taught the models' logic and selection, not their construction.

## 10. Leads to

- `e-secure-design` — reread complete mediation and least privilege now that you have seen their formal clothing.
- `e-iam` — authorization models: RBAC/ABAC as the discretionary, implementable cousins of these mandatory models.
- `e-iam` — mandatory vs discretionary control in a real enterprise: where labels help and where the lifecycle matters more.
- Map refs: **CISSP 3.2** (this lesson); feeds **CISSP 5.4** (authorization mechanisms).
