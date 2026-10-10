# AI supply chain security

**ID:** `ai-supply-chain` · **Stage:** AI track · **Level:** 3 (mechanism + provenance verification on your own artifacts + admission policy) · **Prerequisites:** `ai-llm-architecture` (where weights enter the stack); `ai-llm-top10` (LLM04:2026, expanded here); `a-git-github` (hashes, commits, remotes).

**Map refs:** **OWASP Top 10 for LLM Applications 2026, LLM04:2026** (edition released 2026-08-04 — always name the edition); **CAISP chapter 6**.

---

## 1. Where this shows up

Every model you have ever downloaded is someone else's build artifact, produced on someone else's infrastructure, from data you have never seen. The question "is this model what it claims to be?" is the entire lesson, and it is asked in more places than people realize: pulling weights from a hub before fine-tuning, vendoring a dataset for training, adding a plugin to an agent, deploying a container that serves the model, auditing a vendor who says their model is "certified clean." CAISP devotes its sixth chapter to this because the AI supply chain has every classic supply-chain failure — typosquatting, compromised publishers, tampered artifacts, unvetted dependencies — plus two AI-specific ones: weight files that execute code on load, and training data that implants behavior. This lesson teaches provenance as a discipline: how to know what you have, how to prove it has not changed, and what a poisoned upstream looks like to a defender.

## 2. Before you start

- `ai-llm-architecture` (you know where the weights sit in the stack) and `ai-llm-top10` (LLM04:2026 is this lesson's headline risk).
- Python 3 and OpenSSL on your machine. No model download needed — the walkthrough builds a fake model directory and treats it as the artifact under test. The live-signing step uses Sigstore's keyless flow against the public Rekor log; it needs network and an OIDC identity, so it is marked **not run by us** here with the exact reader procedure.
- Safety framing: you will deliberately craft a malicious pickle file *on your own machine, in a scratch directory, labeled as a hazard demo* — the classic `__reduce__` demonstration. This is the standard teaching demo for deserialization risk, contained to your own files. Nothing leaves your machine.

## 3. How it works

Supply-chain security is one question asked at every handoff: **did this artifact come from who I think, and is it bit-for-bit what they published?** Three mechanisms answer it, from weakest to strongest.

**Hashes: identity of content.** A SHA-256 hash names *content*, not intent — if the bytes change by one bit, the hash changes completely. Pinning a model to a commit hash (not a branch name, not "latest") means you always get the same bytes. Verifying the hash after download means the bytes survived transit. What hashes do *not* tell you: whether the publisher was trustworthy in the first place. A hash of a poisoned model is a perfectly valid hash of a poisoned model. Hashes answer "did it change," never "should I trust it."

**Provenance: identity of origin.** Provenance records *how* the artifact was produced: which source commit, which build steps, which identity ran them. SLSA (Supply-chain Levels for Software Artifacts) standardizes this as signed build provenance: the builder attests "I built these bytes from this source with these steps," and you verify the attestation instead of trusting the artifact alone. For models, the equivalents are: the publisher's verified identity on the hub, the training-data references, and the framework versions — recorded in a machine-readable bill of materials.

**Signatures: binding the two together.** A signature says "this identity vouches for these bytes." Traditional signing drowns in key management — whose key, where is it stored, was it revoked. Sigstore's keyless flow removes the long-lived key: you authenticate with an OIDC identity (your GitHub Actions workflow, your email), the Fulcio certificate authority issues a short-lived certificate bound to that identity, you sign with an ephemeral key that is discarded after one use, and the signing event is recorded in Rekor, an append-only transparency log anyone can audit. Verification checks four things: the signature matches the bytes, the certificate's identity is the expected publisher, the certificate chains to Sigstore's root of trust, and the signing event is present in Rekor. Unsigned artifact, unexpected identity, missing log entry — any one of them fails closed.

**The AIBOM.** A CycloneDX bill of materials extended to machine-learning components: for each model, the hash, the source URL, the framework and version, the dataset references, and the license. The walkthrough generates one for a fake model directory. The defender's use: when a vulnerability lands in a framework version or a dataset is found poisoned, the AIBOM answers "are we exposed?" in minutes instead of weeks. The OpenSSF model-signing work and CycloneDX's ML component support are converging on this as the standard shape — cite the spec, not a vendor.

**The weight-format hazard.** Model weights ship in formats, and some formats are programs. Python's pickle — still common in the ecosystem via `.pkl`/`.pt` conventions and legacy loaders — executes arbitrary code during deserialization by design: a crafted file runs attacker code the moment you *load* it, before any model inference happens. The defense hierarchy: prefer safe formats (safetensors and friends, which store tensors as data, not code); never unpickle a file you did not create or verify; treat weight files with the same suspicion as executables. The walkthrough demonstrates the mechanism on a labeled local file so you respect it, then shows the safe-format alternative.

**What a poisoned upstream looks like to a defender.** You rarely catch the poisoning; you catch its *traces*: a model whose hash does not match the publisher's published value; a new "official-looking" publisher account with a similar name; an artifact with no signature where the publisher normally signs; dependencies in the serving container that changed without a corresponding release; evaluation metrics that shifted on a narrow slice of inputs (the backdoor signature from LLM05:2026). Detection is provenance monitoring: watch the identities and hashes, not just the behavior.

### Worked example: the three-handoff model

A team fine-tunes a base model and ships it. Three handoffs, three questions:

1. **Hub → team.** They download `acme-corp/support-7b`. Provenance check: is the publisher the verified `acme-corp` org or `acme_corp` (typosquat)? Is the download pinned to a commit hash, and does the hash of the bytes match? Is there a signature, and does it verify?
2. **Team → registry.** After fine-tuning, they push to their internal registry. Provenance created: the AIBOM records the base model's hash, the fine-tuning dataset's hash and source, the framework version, and the training script's commit. The registry signs the artifact keyless; the Rekor entry is the public witness.
3. **Registry → production.** The deploy job verifies before serving: signature valid, identity expected, hash matches the AIBOM, framework version not on the known-vulnerable list. Any check fails → the deploy stops. That policy, written as code in the pipeline, is the lesson's real product.

## 4. Walkthrough

**Partially run by us** — transcript: `runs/ai-supply-chain.log`. Clean environment: stock Python 3.12, OpenSSL, no network, 2026-10-09. Steps 1–5 ran locally; step 6 (live keyless signing against Rekor) is marked **not run by us**.

1. **Build the artifact.** Run the harness: it creates `model_dir/` with three fake weight shards, a `config.json`, and a `README.md`. This directory stands in for a downloaded model.
2. **Hash everything.** Run the harness's `hash` command: SHA-256 per file, written to `SHA256SUMS`. Re-run it: identical output. *Teaching point:* the hash names the bytes. Now you have something tampering cannot survive silently.
3. **Tamper and detect.** Append one byte to a shard. Re-run verification: it names the exact file whose hash changed. Restore the file. *Teaching point:* detection is mechanical and total — but only if you kept the reference hashes somewhere the attacker cannot rewrite.
4. **Write the AIBOM.** Run the harness's `aibom` command: it emits `bom.json` in the CycloneDX shape — one component per file with hash, plus model-level metadata (name, source URL, framework, dataset reference, license). Read it: this is the document a vulnerability scanner consumes.
5. **Demonstrate the pickle hazard — labeled, local, contained.** The harness writes `evil.pkl`, a deliberately crafted pickle whose payload creates a marker file when *loaded*. Load it with `pickle.load` in the scratch directory: the marker appears. Then load the safe-format equivalent (a JSON tensor stub): no code runs, ever. Delete both files. *Teaching point:* the danger is not the model — it is the *loader*. Prefer formats that cannot execute.
6. **Keyless signing — NOT RUN BY US.** On your machine, with network: install cosign; `cosign sign-blob --yes bom.json` using your OIDC identity (GitHub Actions or email); then `cosign verify-blob` against the expected identity, and check the Rekor entry. Record the four verification checks from §3 and confirm each passes. Then write the admission policy from §5 of the worked example as a script that refuses any model directory without a verified signature — that policy is your artifact's companion.

## 5. On your own

**Task:** Take any model artifact on your machine (a real download, or the walkthrough's `model_dir`). Produce its AIBOM (hashes, source, framework, dataset reference), verify it, tamper one file, and show the verification catching it. Then write the admission policy: a script that takes a model directory and exits non-zero unless every file's hash matches the AIBOM and the AIBOM itself carries a signature from an expected identity (stub the signature check with a comment marking where cosign verification plugs in, until you complete step 6 above).

**Success test:** The tamper is caught and named; the policy script refuses the tampered directory and accepts the clean one; the stub comment says exactly which cosign command fills it. If your policy trusts the hub's web page instead of hashes and signatures, it fails.

## 6. Where it goes wrong

- **Trusting the hub UI.** Badges, download counts, and "verified" checkmarks are UI, not provenance. The checks that matter are the commit hash, the publisher identity, and the signature — all verifiable offline from the bytes.
- **"Latest" as a pin.** Branch names and tags move. An attacker who compromises a publisher's account does not need to poison every version — just the one your pipeline pulls next Tuesday. Pin the hash.
- **Signing without verifying.** A signature nobody checks is theater. The admission policy in §5 is the part most teams skip: the signature must gate the deploy, in code, with failure closed.
- **The README hash.** A hash printed on the same page as the download, served by the same compromised host, verifies nothing. Reference hashes must come through a separate trust path — the transparency log exists for exactly this reason.
- **Pickle "just this once."** Every incident in this class starts with a legacy loader and a deadline. Migrate to safe tensor formats; quarantine anything you must unpickle (isolated machine, no network, no credentials).
- **Forgetting the data.** Datasets are supply chain too — a poisoned fine-tuning set is LLM05 wearing LLM04's clothes. Hash and pin datasets with the same discipline as weights.

## 7. Read the source

Primary documents first:

- **CycloneDX Specification — Object Model Overview** (cyclonedx.org/specification/overview/) — *read* the Components section (it covers machine-learning models explicitly) and *skim* the rest; *note* the recognized predicate type `https://cyclonedx.org/bom` for attestations.
- **Sigstore documentation — Overview** (docs.sigstore.dev) — *read* fully: keyless signing, Fulcio, Rekor, and the four verification checks. *Then* read the cosign sign/verify pages when you do walkthrough step 6.
- **SLSA specification** (slsa.dev) — *skim* the "about" page and the provenance model; you are learning the vocabulary (attestation, provenance, levels), not implementing SLSA on day one.

Then at most three free resources:

1. **OpenSSF model-signing project** (github.com/sigstore/model-transparency) — free; where model-specific signing is being built — read the README and the threat model.
2. **Hugging Face model-card and commit-hash documentation** (huggingface.co/docs) — free; how pinning and provenance actually look on the hub you will use.
3. **OWASP LLM04:2026** (github.com/GenAI-Security-Project/GenAI-LLM-Top10, `2026/final/LLM04_SupplyChain.md`) — free; the Top 10 entry this lesson expands, with its own prevention checklist.

## 8. Check yourself

1. A team downloads a model by tag (`v2.1`), checks the SHA-256 printed on the hub page, and it matches. Explain the two distinct attacks this workflow still permits, and what pinning to a commit hash plus signature verification would close.
2. Explain why a transparency log (Rekor) is necessary even when every artifact is signed — what attack does the log prevent that signatures alone do not?
3. A `.pt` file from an unverified publisher arrives for fine-tuning. Explain the exact mechanism by which loading it could compromise the training machine, and the two mitigations in order of preference.
4. Your AIBOM lists framework version X, and a vulnerability is later found in X's model loader. Explain the two questions the AIBOM answers in the first ten minutes of triage, and which question it cannot answer.
5. A vendor says their model registry "signs all models." List the four verification checks from §3 and explain which one fails if the team never wrote the admission policy.

## 9. Prove it

**Artifact:** the AIBOM (`bom.json`) for a model directory, the verification transcript (clean accept + tamper caught and named), and the admission-policy script from §5.

**Honest claim:** "I can establish provenance for a model artifact — hashes, AIBOM, signature verification — and enforce an admission policy that refuses unverified models."
**Can't claim yet:** "My supply chain is secure" — provenance proves *identity and integrity*, not *benevolence*. A signed, hashed, perfectly-provenanced model can still be backdoored (LLM05:2026); that is what evaluation and monitoring are for.

## 10. Leads to

- **`ai-governance`** — the supply-chain controls become governance evidence: provenance records are what auditors ask for.
- **`ai-llm-top10`** — re-read LLM04:2026 and LLM05:2026 with provenance vocabulary; notice where they overlap and where they split.
- **`ai-prompt-injection`** — the other end of the lifecycle: supply chain secures what you *deploy*; prompt-injection defenses secure what you *run*.
- Map refs: **OWASP LLM Top 10:2026, LLM04:2026**; **CAISP ch. 6**; CycloneDX and Sigstore as the standards spine; SLSA for build provenance.
