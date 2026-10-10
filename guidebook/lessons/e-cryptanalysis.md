---
lesson_id: e-cryptanalysis
slug: cryptanalysis
stage: E
level: 3
prerequisites: [e-crypto-applied]
roles: []
map_refs: ["CISSP 3.7"]
test_date: 2026-10-10
description: "Compute brute-force and birthday-bound estimates, demonstrate classical frequency analysis in Python, and pair every attack method with its defense. A free lesson in the security guidebook, serving CISSP objective 3.7."
dateline: "Walkthrough run 2026-10-10 · local stdlib Python, nothing external touched"
---
# Cryptanalytic attacks: how ciphers fail, and what that teaches


**Map ref:** serves **CISSP objective 3.7** — cryptanalytic attack methods: attacker models, brute force, birthday attacks, classical analysis, side channels, and the defenses each one demands. (This lesson fills the gap logged in `e-crypto-applied`'s Map ref.)

---

## 1. Where this shows up

Cryptography fails in two places: in its *use* (`e-crypto-applied` — keys with the data, ECB mode, expired certificates) and in its *math* — this lesson's subject. Cryptanalysis studies how attackers recover plaintext or keys without being given them: what the attacker knows, the brute-force arithmetic that sets key sizes, the birthday mathematics that sets hash sizes, the statistical techniques that broke classical ciphers, and the side channels that bypass the math by watching the implementation. Taught here as concepts, mathematics, and tiny classical-cipher demonstrations — no real-product exploit code. The point is defensive: every method is paired with the detection or remediation it demands.

## 2. Before you start

- You can use the primitives correctly and manage keys through their lifecycle (`e-crypto-applied`) — this lesson explains *why* those rules exist.
- Python 3, stdlib only. All three demonstrations run locally on your machine; nothing touches the network, no real ciphers are attacked.
- Primary references: NIST SP 800-57 Part 1 (key-size and cryptoperiod reasoning) and the standard treatment of the attack models below.

## 3. How it works

**The attacker's knowledge: four models.** Cryptanalysis classifies attacks by what the attacker is assumed to know — and the discipline's hard lesson is that you must assume the strongest model your threat model allows, because attackers don't volunteer their limitations:

- **Ciphertext-only:** the attacker sees only ciphertext. The weakest assumption — and therefore the minimum bar every cipher must clear. Breaking a modern cipher here is essentially unheard of; breaking *misused* cryptography here is routine (ECB's pattern leakage from `e-crypto-applied` is a ciphertext-only break of a *mode*, not of AES).
- **Known-plaintext:** the attacker has some plaintext-ciphertext pairs — guessed message headers, predictable protocol fields, a known file encrypted. Classical ciphers fall here; modern ciphers are designed to resist it.
- **Chosen-plaintext:** the attacker can get arbitrary plaintext encrypted — the realistic model for any system where the attacker can submit data (an API that encrypts what you send it, a disk-encryption system holding attacker-chosen files). Any cipher deployed at scale must survive this.
- **Chosen-ciphertext:** the attacker can get arbitrary ciphertext decrypted — the model for padding-oracle attacks, where a server's error messages ("bad padding" vs "bad MAC") leak one bit of information per query until the plaintext surrenders. This is why authenticated encryption (GCM) replaced "encrypt then hope."

**Brute force and key-space arithmetic.** The baseline attack: try every key. Its cost is pure arithmetic — a k-bit key has 2^k possibilities, average case 2^(k-1) tries — which is why key sizes are what they are. The demonstration below computes it: a 56-bit key (the DES era) falls to a modest cluster in hours; 80 bits survives casual attackers but not serious ones; 128 bits requires ~10^21 years at a billion keys per second — longer than the universe has existed, by a factor with twenty-one digits. The professional reading: brute force is not a threat to AES-128; it is the *justification* for AES-128, and the reason 64-bit block/key constructions keep dying. **Defense:** adequate key sizes (128-bit minimum for symmetric keys per SP 800-57), and — the part people forget — the brute-force arithmetic applies to *passwords* too, which is why password-based keys go through deliberately slow derivation (PBKDF2, bcrypt, Argon2): the defense is making each guess expensive.

**Birthday attacks on hashes.** Hashes don't have keys to brute-force; they have the birthday paradox. Among n-bit outputs, a collision becomes likely after roughly 2^(n/2) inputs — not 2^n. The demonstration computes it: a 64-bit hash collides after ~2^32 inputs (four billion — a weekend's hashing), which is why 64-bit hashes are toys; 128-bit needs 2^64 (borderline — this is why MD5's 128 bits died the moment collision attacks got practical); 256-bit needs 2^128, safely beyond reach. The 2^32-on-64-bit demo shows ~39% collision probability — the paradox made concrete. **Defense:** hash sizes with birthday margin (256-bit for collision resistance that must last), and treating any collision attack on your hash function as a migration trigger, not a theoretical curiosity. Detection is the hard part — collisions are silent, which is why the defense is algorithm agility: the ability to swap the hash function before the break, not after.

**Frequency analysis (the classical break).** Monoalphabetic substitution preserves the statistics of the plaintext: in English, 'e' is the most common letter, and a Caesar cipher just renames the letters — the most common ciphertext letter is 'e' wearing a mask. The demonstration encrypts English prose with an unknown shift, counts letter frequencies, guesses the shift from the most common letter, and recovers the full plaintext. It works because the cipher's structure leaks through the statistics. The modern lesson: any encryption that preserves *any* exploitable structure of the plaintext is broken in the same spirit — ECB's identical-blocks leak is frequency analysis's grandchild, and format-preserving mistakes in real systems are its descendants. **Defense:** ciphers whose output is statistically indistinguishable from random (modern block ciphers in proper modes), and modes that destroy structure (randomized IVs, authenticated encryption).

**Side channels: bypassing the math.** The most important modern attack class doesn't attack the cipher at all — it watches the *implementation*. **Timing attacks** measure how long operations take (a password comparison that returns early on the first wrong byte leaks the password one byte at a time — this is why comparisons must be constant-time). **Power and electromagnetic analysis** read the device's physical emissions during crypto operations — devastating against smart cards and IoT devices, the reason hardware crypto exists. **Cache-timing attacks** (Spectre/Meltdown's cousins) exploit shared microarchitectural state between mutually distrusting processes. The lesson: the cipher can be perfect and the system still leaks, because the implementation is part of the cryptosystem. **Defense:** constant-time implementations (no secret-dependent branches or memory accesses), blinding and masking in hardware, physical shielding for high-assurance devices — and the design principle from `e-secure-design`: least common mechanism, because shared caches and shared branch predictors are shared mechanisms.

**Differential and linear cryptanalysis (as concepts).** The two great academic breaks-in-technique of the 1990s, taught here as concepts, not procedures. **Differential cryptanalysis** studies how *differences* in plaintext pairs propagate through the cipher's rounds — if a particular input difference leads to a particular output difference more often than chance, that bias leaks key material round by round. **Linear cryptanalysis** finds *linear approximations* — equations relating plaintext, ciphertext, and key bits that hold with probability slightly above one-half — and amplifies the bias over many known plaintexts. Both need enormous numbers of chosen/known plaintexts against a well-designed cipher (2^47 against DES for linear — practical only to academics and intelligence agencies), which is exactly why modern ciphers are *designed* with provable resistance: AES's design criteria bound the maximum differential and linear probabilities. The professional takeaway is not the technique but the design lesson: cipher selection means choosing algorithms that survived decades of exactly this analysis — never a novel or proprietary cipher, per `e-crypto-applied`'s "never roll your own."

### The demonstrations (run by us)

**Demo A — brute-force key-space estimates.** Script: `runs/e-cryptanalysis-brute.py`. Average-case search time (half the key space) at three stated-as-assumption guess rates: single CPU (~10^9 keys/s), GPU cluster (~10^12), hypothetical exascale (~10^18). Results (transcript `runs/e-cryptanalysis.log`): 40-bit falls in ~9 minutes on one CPU; 56-bit in ~10 hours on the cluster; 64-bit in ~107 days; 80-bit in ~19,000 years; 128-bit in ~5×10^18 years on the cluster — ~5×10^12 years even at exascale. Below 80 bits, serious attackers win; at 128, arithmetic itself is the defense.

**Demo B — the birthday bound.** Same script: collision expected after ~2^(n/2) inputs — 2^32 for 64-bit (exact P(collision) after 2^32 inputs: 0.3935, nearly 40%), 2^64 for 128-bit, 2^128 for 256-bit. At a trillion hashes per second, the 64-bit collision arrives in a fraction of a second; the 256-bit one in ~10^19 years. Hash output size is doubled relative to the security level you want.

**Demo C — frequency analysis on a Caesar cipher.** Script: `runs/e-cryptanalysis-caesar.py`. English prose, shift 17, unknown to the analyst: count letter frequencies, most common ciphertext letter 'v' (1,068 occurrences) masks 'e', derive shift 17, decrypt — full recovery verified byte-for-byte. Classical, tiny, and the exact shape of every structural-leakage break since.

## 4. Walkthrough

**Run by us** on this machine — transcripts: `runs/e-cryptanalysis.log` (brute-force + birthday, `e-cryptanalysis-brute.py`) and the Caesar transcript inside the same log (`e-cryptanalysis-caesar.py`). Python 3, stdlib only, 2026-10-10, no network, no real ciphers attacked.

1. **Run the brute-force script.** `python3 runs/e-cryptanalysis-brute.py`. *Expect:* 40-bit in minutes, 56-bit in hours (GPU cluster), 128-bit in ~5×10^18 years. Change the guess rates to your own assumptions — 128-bit doesn't move.
2. **Run the birthday section.** Same script, second half. *Expect:* 2^32 for 64-bit with P(collision) ≈ 0.39. Compute it for 160-bit (SHA-1's size) and ask what 2^80 work means for a well-funded attacker — the arithmetic behind SHA-1's retirement.
3. **Run the Caesar break.** `python3 runs/e-cryptanalysis-caesar.py`. *Expect:* most common letter 'v', guessed shift 17 = true shift, `recovery successful: True`. Change the shift and the prose and re-run — the attack doesn't care about the shift, only about surviving statistics.
4. **Break the attack on purpose.** Feed the script random bytes instead of English prose. *Expect:* the most-common-letter guess fails — frequency analysis needs the plaintext's statistics to survive. This is the property modern ciphers are designed to have.
5. **Pair every method with its defense.** For each of the six methods in §3, write the detection and the remediation. If you can't write the detection — as with hash collisions — say so and name the agility that substitutes for it.

## 5. On your own

**Task:** (a) Extend the brute-force script with password guessing: compute the effective key space of an 8-character lowercase password vs a 5-word passphrase, at 10^9 guesses/s with and without a slow hash (assume the slow hash costs 0.1 s per guess — state it as an assumption). (b) Write the detection/remediation paragraph for a timing attack against a login endpoint you control.

**Success test:** Your numbers show the passphrase winning by orders of magnitude and the slow hash multiplying the attacker's cost by the work factor — and your timing-attack paragraph names constant-time comparison as the fix *and* describes what you'd monitor to detect the attack in progress (request timing distributions per account, not just failure counts).

## 6. Where it goes wrong

- **"Nobody can break AES" as a complete argument.** True of the cipher, irrelevant to the system. The breaks that matter are padding oracles, timing leaks, and ECB/IV misuse — the cipher is the strongest link, so attackers don't attack it.
- **64-bit anything.** The birthday bound halves your margin, and 2^32 is a weekend. Every 64-bit construction in production is a migration waiting for a deadline.
- **Treating collision attacks as theoretical.** MD5 and SHA-1 were "theoretically" broken years before the practical demos; organizations that waited migrated in a panic. The migration trigger is the first serious cryptanalytic result, not the first exploit.
- **Variable-time crypto code.** Secret-dependent branches, early-exit comparisons, table lookups indexed by secrets — each is a side channel wearing an optimization's clothes.
- **Homegrown ciphers.** Differential and linear cryptanalysis exist because smart people designed ciphers that looked fine and weren't. The defense is selection from algorithms that survived decades of public analysis.
- **Ignoring the attacker's model.** Designing for ciphertext-only when the attacker gets chosen-plaintext (any API that encrypts attacker input), or ignoring chosen-ciphertext where error messages leak. Assume the strongest model your system offers.
- **Key sizes as magic numbers.** Deploying "128-bit" without knowing *what* is 128 bits — key, block, or hash output — and therefore not knowing whether the birthday bound halves it.

## 7. Read the source

Primary documents first:

- **NIST SP 800-57 Part 1 Rev. 5, Recommendation for Key Management** (csrc.nist.gov) — *read* the key-size and cryptoperiod sections: the authoritative source for why 128 bits is the floor and how long keys may live.
- **NIST SP 800-53 Rev. 5, SC family** (csrc.nist.gov) — *skim* SC-12 (key management) and SC-13 (cryptographic protection) as the control-language form of this lesson's defenses.

Then at most three free resources:

1. **OWASP Cryptographic Storage Cheat Sheet** (cheatsheetseries.owasp.org) — free; the practitioner checklist: which primitives, which modes, which mistakes — the defensive companion to every attack in this lesson.
2. **NIST SP 800-115, Technical Guide to Information Security Testing and Assessment** (csrc.nist.gov) — free; where cryptanalytic testing fits in a real assessment program (and where its limits are).
3. **Purdue CS 526 integrity handout** (cs.purdue.edu) — free; the university treatment of classical analysis concepts alongside the integrity models — good second voice on frequency-style reasoning.

## 8. Check yourself

1. An API encrypts whatever clients submit and returns the ciphertext; errors distinguish "bad padding" from "bad MAC." Name the attacker model, the attack it enables, and the single design change that closes it.
2. A team proposes a 64-bit hash "for integrity, not security." Using the birthday bound, compute the collision workload and explain why the integrity/security distinction doesn't save them.
3. A login endpoint compares password hashes with an early-exit byte loop. Name the attack class, describe what the attacker measures, and give the fix plus what you'd monitor to detect the attack.
4. Explain why differential cryptanalysis needing 2^47 chosen plaintexts against DES is both a devastating academic result and, practically, the reason DES died — then state the design lesson for cipher selection.
5. Predict the migration crisis for an organization that standardizes on one hash function with no agility: which event triggers it, what the first 48 hours look like, and what the pre-built agility would have changed.

## 9. Prove it

**Artifact:** the three demonstration scripts run on your machine (brute-force table, birthday computation, Caesar break with recovery verified) plus your six detection/remediation paragraphs — one per attack method in §3.

**Honest claim:** "I can compute what key and hash sizes survive which attackers, demonstrate classical frequency analysis, and pair every cryptanalytic method with its defense."
**Can't claim yet:** "I can perform cryptanalysis on real ciphers" — academic cryptanalysis of modern algorithms is a research discipline; this lesson taught the models, the mathematics, and the defensive reasoning, using a classical cipher as the demonstration vehicle.

## 10. Leads to

- `e-crypto-applied` — the use-side failures this lesson's math-side complements; reread its §6 as the attacker's easier path.
- `e-secure-design` — open design and least common mechanism as the principles behind "never roll your own" and side-channel defense.
- `e-data-protection-controls` — data security controls: hash-function selection and migration as an organizational control.
- Map refs: **CISSP 3.7** (this lesson); feeds **CISSP 2.6** (data protection) and **8.3** (software security effectiveness).
