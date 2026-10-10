# Platform security: the ground your architecture stands on

**ID:** `e-platform-security` · **Stage:** E (Expert) · **Level:** 3 (survey a platform's security capabilities and write a deployment recommendation with conditions) · **Prerequisites:** `e-secure-design` (platform capabilities as design inputs), `e-crypto-applied` (what the encryption primitives guarantee); no command line in this lesson.

**Map ref:** serves **CISSP objective 3.4** — platform security capabilities: memory protection, hardware roots of trust, secure boot, virtualization isolation, and encryption.

---

## 1. Where this shows up

Every security architecture rests on a platform — firmware, bootloader, hypervisor, CPU — and every platform makes promises the layers above inherit, silently. When the platform keeps its promises, the architecture above gets measured boot, sealed keys, and memory that resists corruption; when it doesn't, the architecture inherits a basement nobody inspected. Platform security shows up in the procurement question nobody asks ("does this server have a TPM, and is it enabled?"), in the cloud instance-type decision that determines whether your keys live in hardware or in a config file, in the secure-boot failure that bricks a fleet at 3 a.m., and in the confidential-computing pitch that promises your data is safe from the cloud provider itself. It is the least glamorous layer and the most load-bearing: compromise below the operating system is compromise of everything above it, usually without evidence.

## 2. Before you start

- You know what platform capabilities are for (`e-secure-design` §3) — this lesson teaches how to evaluate them.
- You can state what encryption guarantees and what it doesn't (`e-crypto-applied`) — the platform is where keys live or die.
- No tools. The work product is a platform capability survey: what the platform offers, what is actually enabled, and what the deployment decision depends on.

## 3. How it works

**The boot chain and why it matters.** A machine does not start secure; it *becomes* trustworthy one stage at a time. Firmware initializes hardware, the bootloader loads the OS, the OS starts services — and each stage can subvert every stage after it. Platform security is the discipline of making each handoff verifiable: either the next stage is measured (its hash recorded, so tampering is detectable) or verified (its signature checked, so tampering is prevented). Everything above trusts the chain; the chain's first link is trusted without evidence, which is why it must be as small and as hard to change as possible.

**Hardware roots of trust: the TPM.** The Trusted Platform Module is a small cryptographic coprocessor — discrete chip, firmware implementation, or virtual — that provides three capabilities nothing in software can replicate. **Measured boot:** as each boot component loads, its hash is extended into Platform Configuration Registers (PCRs) — a tamper-evident log of *what actually booted*, not what was supposed to boot. **Sealed storage:** keys and secrets can be bound to a PCR state, so they unseal only when the boot measurements match — a stolen disk yields nothing because the measurements on the attacker's machine differ. **Attestation:** the TPM can sign a quote of the PCRs with its attestation key, proving to a remote verifier what software booted — the basis of fleet enrollment decisions ("this gateway may join because it booted the approved firmware"). The root of trust is minimal by design: a small, fixed-function component whose compromise requires physical access or a supply-chain attack, not a phishing email.

**Secure boot (UEFI).** Where measured boot *detects* tampering, Secure Boot *prevents* it: the firmware verifies each boot stage's signature against keys in its database before transferring control. An unsigned or revoked bootloader simply does not run. The operational reality: Secure Boot is only as good as its key management — machines ship with vendor keys, organizations enroll their own, and a compromised or misconfigured key database silently downgrades the guarantee. "Secure Boot enabled" is a claim; the key inventory is the evidence.

**Memory protection.** Most remote code execution still begins with memory corruption, so the platform's memory defenses are the exploit author's tax code. **Non-executable memory** (NX/XD/W^X) marks data pages non-executable — injected shellcode cannot run where it lands. **Address-space layout randomization** (ASLR) randomizes where code and data load, turning a reliable exploit into a guessing game (defeated by information leaks, which is why it is a layer, not a wall). **Control-flow enforcement** — Intel CET is the worked example — adds a **shadow stack** (a second, hardware-protected copy of return addresses, so return-oriented programming finds its targets don't match) and **indirect-branch tracking** (indirect jumps may land only on designated entry points). None of these fix buggy code; all of them raise exploitation from scripting to research.

**Virtualization isolation.** The hypervisor is a smaller, simpler trust boundary than a general-purpose OS: guests are isolated by hardware-assisted virtualization (separate address spaces, trapped privileged instructions), and a compromised guest should not reach the host or its neighbors. The threat model matters: classic virtualization protects guests *from each other* but not from the host — the hypervisor sees all guest memory. **Confidential computing** (memory encryption per VM, with attestation of the guest's initial state) extends the boundary to protect the guest *from the host* — relevant wherever mutually distrusting parties share hardware, or where the threat model includes the infrastructure operator. The capability to survey is not "virtualization: yes" but *which* boundary the platform actually enforces and against whom.

**Platform encryption capabilities.** Encryption the platform makes cheap gets used; encryption that fights the platform gets skipped. Survey: **hardware AES acceleration** (instructions that make bulk encryption effectively free), **key storage** (TPM-sealed keys, platform keystores, managed key services — where the keys live determines the whole key-management story from `e-crypto-applied`), **full-disk encryption** with pre-boot authentication, and **per-VM memory encryption** where offered. The question is never "does it support AES" — everything does — but "where do the keys live, who can extract them, and what happens at boot, at migration, and at decommissioning?"

**The survey method.** For each deployment option, verify five capability groups — boot integrity (measured/verified boot, TPM presence and enablement), memory protection (NX, ASLR support, CET-class enforcement), virtualization boundary (what is isolated from what, and from whom), key storage (where keys live), and firmware update integrity (signed updates, rollback protection). A capability the vendor cannot confirm in writing does not exist for decision purposes. "Enabled by default" beats "supported"; "attested" beats "enabled."

### Worked example: Meridian Analytics — platform survey for the database tier

**The decision (fictional).** Meridian Analytics (from `e-iam`) is moving its production database tier — the system holding the data its access reviews protect — off shared cloud instances. Two options: **Option A**, the cloud provider's confidential-computing instance family; **Option B**, colocated single-tenant servers from a hardware vendor. The survey:

| Capability | Option A (cloud, confidential VMs) | Option B (colo, single-tenant) |
|---|---|---|
| Boot integrity | vTPM with measured boot; attestation API available; Secure Boot enforced by the provider | TPM 2.0 discrete chips on the BOM (confirmed in writing); Secure Boot with customer-enrolled keys; attestation flow must be built by Meridian |
| Memory protection | NX + ASLR standard; CET-class enforcement available on the instance family | Same CPU generation — same NX/ASLR/CET; no difference at the silicon level |
| Virtualization boundary | Guest memory encrypted per VM; host (provider) cannot read guest memory; attestation of initial guest state | No hypervisor — bare metal; boundary is physical (single tenant per machine); no host in the threat model at all |
| Key storage | Managed key service backed by hardware; keys never leave the boundary in clear | TPM-sealed keys; operationally heavier — Meridian owns rotation, backup, and the compromise procedure |
| Firmware updates | Provider-managed, signed, with rollback protection | Vendor-signed firmware; Meridian owns the update cadence and must track advisories |

**Analysis.** The silicon is equivalent — the difference is *who operates the trust*. Option A outsources the firmware, attestation, and key-management operations to the provider and adds a real technical boundary (memory encryption) against the provider itself. Option B removes the provider from the threat model entirely but transfers every operational burden — attestation flow, key ceremonies, firmware tracking — to a 180-person company with one platform team. The confidential-computing boundary in Option A is the more *verifiable* posture for Meridian's size: the attestation API exists today, while Option B's attestation flow is a project that must be built before migration or the boot-integrity story silently degrades.

**Recommendation (with conditions):** Option A, *conditioned on* (1) confirming in the contract that the vTPM attestation API and memory-encryption features are available in the regions Meridian deploys to — features vary by region and the sales deck is not the contract; (2) a key-management runbook for the managed key service covering rotation and compromise, owned by the platform team; (3) re-survey at contract renewal, because the provider's feature set is the part of the platform Meridian doesn't control. The honest statement: Meridian is trading operational burden for provider trust, and the memory-encryption boundary is what makes that trade defensible.

## 4. Walkthrough

**Worked-case lesson — no command line.** The Meridian survey above, authored and self-reviewed in-session on 2026-10-10. Transcript: `runs/e-platform-security.log`.

1. **Name the decision.** One sentence: what is being deployed, and what are the options? If there is only one option, the survey is still worth doing — it becomes the list of assumptions you are betting on.
2. **Survey the five capability groups per option.** Boot integrity, memory protection, virtualization boundary, key storage, firmware updates. For each cell: what the platform offers, whether it is enabled by default, and the evidence (documentation link, contract clause, or "vendor confirmed in writing on [date]").
3. **Draw the trust boundary per option.** Who is inside, who is outside, and — critically — whether the infrastructure operator is inside or outside. This is the row most surveys skip and the row that determines the decision.
4. **Write the analysis.** Silicon equivalence is common; operational burden is where options differ. Name who operates each trust mechanism and whether your team can actually operate it.
5. **Recommend with conditions.** No unconditional recommendations — every platform choice has conditions (contract terms, runbooks to write, features to confirm per region). List them; they are the action items.
6. **Close out.** File the survey as the artifact. Date it — platform capabilities change, and a survey is a snapshot, not a permanent truth.

## 5. On your own

**Task:** Survey the platform you actually run on — your VPS provider's instance types, your home server's motherboard/CPU, or your laptop. Check: TPM present and enabled? Secure Boot on, and whose keys? Memory encryption offered? Where do your disk-encryption keys live?

**Success test:** You find at least one capability you assumed and cannot confirm — the gap between "supported" and "enabled and attested" is the finding. Your survey names the trust boundary: who (including the provider) is inside it.

## 6. Where it goes wrong

- **"The cloud handles it."** The most expensive sentence in platform security. The cloud offers the capabilities; *you* enable, configure, and attest them. Unconfigured platform security is a brochure, not a boundary.
- **TPM present, never attested.** Measured boot without a verifier is a log nobody reads. If nothing checks the PCRs, tampering is recorded faithfully and ignored completely.
- **Secure Boot with vendor-default keys.** The signature check runs against keys you never inventoried. Key management doesn't stop at the OS — the firmware's key database is part of the trust chain.
- **Confusing the virtualization boundary.** "It's in a VM, so it's isolated" — isolated from what, from whom? The classic hypervisor boundary excludes the host; if your threat model includes the operator, you need the confidential-computing boundary, not just any VM.
- **Keys in the config file.** Platform key storage exists precisely so keys don't live next to the data. Every survey should ask where the keys live at boot, at migration, and at decommissioning — the three moments keys leak.
- **Firmware as an afterthought.** Signed updates, rollback protection, and an update cadence with an owner. The firmware is the most privileged code on the machine and the least monitored — that asymmetry is the attacker's business model.
- **Surveying once.** Platform capabilities are a moving target: new instance families, new CPU extensions, provider feature changes. A survey without a review date is a snapshot treated as a permanent truth.

## 7. Read the source

Primary documents first:

- **UEFI Forum: Specifications** (uefi.org) — *read* the Secure Boot sections of the UEFI specification overview; *skim* the rest. The primary source for what "verified boot" actually verifies.
- **Microsoft Learn: Trusted Platform Module (TPM) fundamentals** (learn.microsoft.com) — *read* the measured-boot, sealed-storage, and attestation explanations; *skim* the Windows-specific integration. The clearest free TPM treatment.

Then at most three free resources:

1. **Intel: A Technical Look at Control-Flow Enforcement Technology (CET)** (intel.com) — free; shadow stacks and indirect-branch tracking explained by the people who built them.
2. **NIST SP 800-53 Rev. 5, SC family** (csrc.nist.gov) — free; the platform controls in catalog form (SC-12 key management, SC-28 at-rest protection) for the trace.
3. **CISA physical security resources** (cisa.gov) — free; the facility half of platform trust — hardware you can touch is hardware someone else can touch.

## 8. Check yourself

1. A server has a TPM and "measured boot enabled," but nothing ever reads the PCRs. Explain what guarantee is actually provided, what is missing, and the cheapest fix.
2. Two offerings use the same CPU. One runs your database in a confidential VM; the other on colocated bare metal. Name the threat each option handles better, and the operational burden each imposes.
3. A team's Secure Boot deployment uses the vendor's default key database. Explain the trust assumption this bakes in and what enrolling their own keys changes — and what new responsibility it creates.
4. An architect cites ASLR as the mitigation for a memory-corruption vulnerability class. Explain why ASLR is a layer rather than a fix, what defeats it, and which platform capability raises the bar further.
5. Predict the incident that reveals a platform survey was never re-done: which capability silently changed, who depended on the old assumption, and what the first symptom is.

## 9. Prove it

**Artifact:** your platform capability survey — the decision, the five capability groups per option with evidence, the trust boundary per option (naming the operator's position), the analysis, and the conditional recommendation — for the Meridian case in your own words, or for a platform you actually use.

**Honest claim:** "I can survey a platform's security capabilities, draw the trust boundary including the operator, and write a deployment recommendation with explicit conditions."
**Can't claim yet:** "I can implement measured boot and attestation" — building the attestation flow (verifier service, PCR policies, enrollment) is implementation work this lesson scoped as a condition, not a deliverable.

## 10. Leads to

- `e-secure-design` — platform capabilities as design inputs; reread its R5 as a survey row.
- `e-crypto-applied` — key lifecycle: the survey says where keys live; that lesson says how they must be managed.
- `e-facility-controls` — site and facility security controls: the physical half — the server whose boot you attested sits in a building someone can walk into.
- `d-cloud-security` — shared-responsibility done right: which platform capabilities the provider owns vs you.
- Map refs: **CISSP 3.4** (this lesson); feeds **CISSP 7.14** (physical security implementation).
