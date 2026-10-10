# AI attacks and defenses in the build pipeline

**ID:** `ai-pipeline` · **Stage:** AI track · **Level:** 3 (mechanism + pipeline hardening on your own build, each attack paired with its defense) · **Prerequisites:** `ai-supply-chain` (hashes, signing, admission policies); `ai-llm-architecture` (the stack you are protecting); `a-git-github` (the artifact pipeline); Python 3.

**Map refs:** **CAISP chapter 4** (AI Attacks and Defenses Using DevOps); **OWASP LLM Top 10:2026, LLM05** (Data and Model Poisoning) and **LLM04** (Supply Chain); MITRE ATLAS — Training Data Poisoning, AI Supply Chain Compromise, Publish Poisoned AI Artifacts; SLSA; feeds `ai-threat-modeling`, `ai-governance`.

---

## 1. Where this shows up

Every model you will ever deploy passed through a pipeline: data was collected, a training or fine-tuning job ran, an artifact was packaged, it landed in a registry, and something deployed it. That pipeline is an attack surface with its own threat model, and it is where the most consequential AI compromises happen — not because the model was clever, but because the build was trusted. ML platform engineers, AI security engineers, and DevSecOps teams own this. CAISP puts it in chapter 4 for a reason: securing the pipeline is the DevOps half of AI security, and everything the track taught about provenance in `ai-supply-chain` only works if the pipeline that produces the provenance is itself trustworthy.

## 2. Before you start

- You have read `ai-supply-chain` — you know what a hash proves (content identity), what a signature proves (origin), and what an admission policy enforces.
- You have read `ai-llm-architecture` — you can draw the six-layer stack and point at its trust boundaries.
- Python 3 on your machine. No model, no GPU, no network: the walkthrough's harness simulates the pipeline deterministically on loopback.
- Safety framing, stated once: this lesson teaches where pipeline attacks *enter* and how each is *detected and stopped*. It does not teach attack automation, and nothing here is run against anyone else's infrastructure.

## 3. How it works

A model pipeline has five stages, and each one has a characteristic attack. Learn them as pairs — attack, then the defense that catches it — because in practice you never meet one without needing the other.

**Stage 1 — Data collection and curation.** The attack is **training-data poisoning**: crafted samples inserted into the training or fine-tuning set so the resulting model behaves the attacker's way on chosen inputs — a backdoor trigger, a biased classifier, a model that leaks on demand. MITRE ATLAS names this directly (Training Data Poisoning), and it sits inside LLM05:2026. The defense is dataset provenance: a hash manifest over every training file, recorded at collection time, re-verified before every training run. A manifest turns "is this dataset the one we approved?" from a hope into a check. Layered on top: source allowlisting (data comes from named, reviewed origins — not "the internet"), duplication and canary checks (a known-clean canary file whose corruption proves tampering), and statistical screening of new batches (poisoning at scale shifts distributions; screening catches the clumsy kind, not the careful kind — say that honestly).

**Stage 2 — Training and fine-tuning.** The attack is **compute and configuration tampering**: a compromised training job, a malicious dependency in the training environment, or a modified checkpoint swapped in mid-run. The defense is build provenance: the training run emits an attestation — *this* artifact was built from *these* inputs by *this* builder at *this* time — and the registry verifies the attestation before accepting the artifact. This is SLSA's model applied to model builds: provenance answers *who built it and from what*, which a hash alone cannot. Hermetic builds (no network access during the build, pinned dependencies) shrink what a compromised build can reach.

**Stage 3 — Packaging.** The attack is **artifact substitution**: the model file that reaches the registry is not the one the training job produced — swapped in transit, in storage, or by a compromised packaging step. The defense is signing at the moment of creation: the training job signs the artifact with Sigstore keyless signing (you learned the mechanics in `ai-supply-chain` — Fulcio identity, Rekor transparency log), so substitution breaks the signature and the transparency entry won't match.

**Stage 4 — Registry.** The attack is **registry abuse**: mutable tags repointed at a different artifact, stale vulnerable models left downloadable, weak access control letting anyone push. The defense is registry hygiene: immutable tags (a published tag never changes — new artifact, new tag), version pinning by digest everywhere downstream, retention and vulnerability policies, and access control on who can push. A registry is a trust boundary; treat it like one.

**Stage 5 — Deployment.** The attack is **the compromised build pipeline itself** — and this one deserves special attention, because OWASP's LLM04:2026 added it as an explicit scenario: an attacker compromises the CI/CD pipeline (a malicious build dependency, a stolen registry credential), and the resulting backdoored model is built and signed *by your own release infrastructure*. It passes every provenance and attestation check, because those checks scrutinize externally sourced components, not the builder. The defense is defense in depth around the builder: least-privilege CI credentials (the build job can write to the registry and nothing else), required reviews on pipeline definitions, anomaly detection on build behavior (a build that suddenly exfiltrates is not a build), and — the structural fix — **adversarial testing as a CI gate**: a red-team suite (promptfoo, garak, or your own probes) runs against every candidate model, and new findings block the release. The gate does not trust the pipeline; it tests the product.

### Worked example: the Meridian support-model pipeline

Meridian Analytics (the fictional company from `ai-governance`) fine-tunes a support chatbot monthly. Their pipeline, with defenses:

1. **Data:** fine-tuning pairs collected from support tickets. A manifest (SHA-256 per file) is committed alongside the dataset; the training job refuses to start if verification fails. A canary file — three known-clean examples — is checked first; corruption aborts the run.
2. **Build:** the training job runs in a hermetic container with pinned dependencies, emits a SLSA-style provenance attestation (source commit, builder identity, input digests), and signs the model with keyless Sigstore.
3. **Registry:** the signed model and its attestation are pushed under an immutable tag; the registry's admission policy (from `ai-supply-chain`) verifies signature + provenance + transparency-log entry before accepting.
4. **Gate:** the CI red-team suite runs 200 adversarial prompts against the candidate; any *new* failure vs. the baseline blocks promotion. Findings become regression tests — the suite grows with every incident.
5. **Deploy:** only promoted, signed, attested artifacts deploy; the deployment manifest pins digests, not tags.

Now the attacks, one per stage, and what catches each: a poisoned ticket pair fails the manifest check (stage 1); a compromised training dependency can't reach the network in the hermetic build, and its output still faces the red-team gate (stage 2); a swapped artifact fails signature verification (stage 3); a repointed tag is impossible under immutability, and downstream pins digests anyway (stage 4); a fully compromised builder — the LLM04 scenario — produces a signed, attested, backdoored model, and *only the adversarial gate* catches it, because the gate tests behavior, not provenance. That last sentence is the lesson's core: provenance proves the artifact is the one you built; only testing proves the artifact is the one you want.

## 4. Walkthrough

**Run by us** — transcript: `runs/ai-pipeline.log`. Clean environment: stock Python 3.12, no network, no model, 2026-10-09. The harness (`pipeline_demo.py`, deterministic) simulates Meridian's five stages: a dataset with a manifest, a build step emitting provenance, a registry with an admission policy, and a red-team gate.

1. **Manifest the dataset.** Run the harness's `manifest` command over the toy corpus. Read the manifest: one SHA-256 per file, plus the canary entry. *Teaching point:* the manifest is the dataset's identity; everything downstream trusts it.
2. **Verify clean.** Run `verify` — all files match, canary intact, build proceeds. Note what "proceeds" means here: the harness prints the provenance attestation (source digest, builder id, input digests).
3. **Poison the data.** Tamper one training file (the harness provides a `tamper` command that flips a byte and rewrites the file). Re-run `verify`: the manifest check fails, names the file, and the build aborts. *Teaching point:* detection is immediate and specific — this is what provenance buys you.
4. **Forge the provenance.** Restore the dataset, then hand the registry a forged attestation (wrong builder id). Run `admit`: the registry rejects it — the builder identity doesn't match the expected one. *Teaching point:* provenance is verified, not trusted.
5. **Run the red-team gate.** Promote a clean, signed, attested model, then run the gate: 12 adversarial prompts, all pass. Now promote the "compromised-builder" model — signed and attested correctly, but behaviorally backdoored (it complies with a planted instruction on one trigger prompt). Watch the gate catch exactly the trigger prompt, block promotion, and log the finding as a new regression test. *Teaching point:* this is the only stage that catches the LLM04 scenario, and the lesson says so plainly.
6. **Read the registry state.** Print the registry: immutable tags, digest pins, the rejected artifacts with reasons. Confirm the refused model is recorded with its reason — a registry that silently drops is an audit gap.

## 5. On your own

Extend the harness with a statistical screening step: before the manifest check, compute a simple distribution metric over the training files (e.g., label frequencies, average document length) and flag any batch whose metric shifts more than a threshold you choose from the clean baseline. Then poison the dataset *without* breaking the manifest (edit a file and re-run `manifest` to bless the poisoned version — this simulates an attacker who owned the data before the manifest was written) and show that your screening step catches what the manifest cannot.

**Success test:** your screening flags the poisoned batch, misses nothing in the clean baseline across three runs, and you can state in one paragraph why screening is a complement to — never a replacement for — the manifest.

## 6. Where it goes wrong

- **A hash is not provenance.** The manifest proves the dataset is unchanged since the manifest was written; it says nothing about whether the dataset was clean when written. The On-your-own task exists because this confusion is the single most common pipeline failure.
- **Signing without verification is theater.** A signature nobody checks is a sticker. The admission policy is the control; the signature is its input.
- **Gates everyone overrides.** A red-team gate with a "skip" button that requires no justification will be skipped exactly when it matters. The gate's override path — who can approve it, what gets recorded — is part of the design, not an afterthought.
- **Provenance that trusts the builder.** SLSA provenance attests what the builder *claims*. A compromised builder claims lies truthfully. This is why the LLM04:2026 scenario is in the lesson: provenance and behavioral testing are complements, and either alone is insufficient.
- **Registry hygiene decay.** Immutable tags, digest pinning, and retention policies are easy to set and easy to erode under deadline pressure. The erosion is silent until an incident.

## 7. Read the source

- **SLSA specification** (slsa.dev) — the provenance model: what an attestation contains, what the levels require, and why "hermetic" and "hosted" matter. Read the overview, then the provenance and build-requirements pages; skim the level definitions. (Fetched 2026-10-09.)
- **Sigstore documentation** (docs.sigstore.dev) — keyless signing mechanics: Fulcio, Rekor, and the verification checks. You read this in `ai-supply-chain`; re-read the verification section with pipeline eyes: *what* is being signed, and *when*.
- **OWASP LLM Top 10:2026, LLM04 (Supply Chain)** — the compromised-build-pipeline attack scenario and the model-signing/AIBOM defenses. Read the scenario, then the prevention list; note what it assumes about your registry.

Free resources for going deeper (≤3): the SLSA spec itself; the Sigstore docs; the OWASP GenAI Security Project's LLM04:2026 page.

## 8. Check yourself

1. An attacker poisons the fine-tuning data *before* the manifest is written. Which of the five defenses catches it, and why does the manifest not?
2. Your pipeline signs every model with keyless Sigstore, and the registry verifies signatures. Walk through the LLM04 compromised-builder scenario: which checks pass, which check catches it, and why?
3. A teammate proposes replacing the red-team gate with "we review the training data carefully." Using the manifest/screening distinction from this lesson, explain what that proposal gets wrong.
4. The registry uses mutable tags ("latest") and downstream deploys pin tags, not digests. Name two attacks this enables and the two registry-hygiene fixes.
5. Your CI credentials can push to the registry *and* read production secrets. Rewrite the credential scope using least privilege, and state what breaks in the attacker's plan when you do.

## 9. Prove it

**Artifact:** the extended harness (your screening step committed), a run log showing the tamper caught, the forged provenance rejected, and the red-team gate blocking the backdoored model — plus a one-page pipeline threat summary naming each stage's attack and its catching defense.

**You can claim:** "I can design and verify the security controls of an ML build pipeline — dataset provenance, build attestation, registry admission, and adversarial gating — and I can explain which attack each control catches and which it doesn't."

**You cannot claim:** experience operating a production ML platform; the ability to detect a careful, adaptive poisoning campaign (screening catches the clumsy kind — the lesson says so); or that any pipeline is "secure" — only that its controls are defined, verified, and tested.

## 10. Leads to

- `ai-threat-modeling` — the pipeline is one system inside the larger threat model; this lesson's five stages become five elements in its data-flow diagram.
- `ai-supply-chain` — the companion lesson: provenance and signing mechanics this lesson assumes.
- `ai-governance` — pipeline controls become the evidence the governance lesson's risk register cites.
- **Map refs:** **CAISP chapter 4** (served directly); **OWASP LLM Top 10:2026 LLM04/LLM05**; MITRE ATLAS (Training Data Poisoning, AI Supply Chain Compromise).
