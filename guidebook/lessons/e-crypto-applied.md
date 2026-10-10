---
lesson_id: e-crypto-applied
slug: crypto-applied
stage: E
level: 3
prerequisites: [a-http-depth]
roles: [cloud-security, iam-engineer]
map_refs: ["CISSP 3.6"]
test_date: 2026-10-09
description: "Applied cryptography: hashes, modes, signatures, PKI path validation and the key lifecycle — ECB-vs-CBC demonstrated live, TLS 1.3 handshake run locally. A free hands-on lesson in the security guidebook, serving CISSP objective 3.6."
dateline: "Walkthrough run 2026-10-09 · OpenSSL 3.0.13, loopback only, nothing external touched"
---
# Applied cryptography: what the primitives do, and how they break


**Map ref:** serves **CISSP objective 3.6** — cryptographic solutions: lifecycle, methods, PKI, key management, signatures. (Objective 3.7, cryptanalytic attack methods, is taught in `e-cryptanalysis`.)

---

## 1. Where this shows up

Cryptography is the one part of security where the math is essentially never the problem and the *use* of the math is almost always the problem. Nobody breaks AES; they store the key next to the data, or use ECB mode, or roll their own protocol, or let a certificate expire on a Friday. This lesson is the professional's view: you will not design ciphers — you will choose primitives correctly, manage keys through their lifecycle, read a PKI trust chain, and recognize the five misuses that defeat otherwise sound cryptography. It shows up in every architecture review ("where are the keys?"), every TLS misconfiguration finding, every "we encrypt at rest" claim that needs a follow-up question, and in the CISSP as Domain 3's most practical objective.

## 2. Before you start

- You can state the difference between hashing and encryption, and between symmetric and asymmetric encryption (Stage A).
- OpenSSL 3.x installed (`openssl version`). Everything runs locally — no network, no external hosts.
- Primary references for this lesson: **NIST SP 800-57 Part 1 Rev. 5** (key management, May 2020) and **RFC 5280** (X.509 PKI profile). You will read sections of both.

## 3. How it works

**The three primitives, by what they guarantee.** A **hash** (SHA-256) takes any input and produces a fixed-size fingerprint. It guarantees nothing about secrecy — it guarantees *integrity detection*: change one input bit and the fingerprint changes completely (the avalanche effect you will observe in the walkthrough). Hashes do not encrypt; "encrypted with SHA-256" is a sentence that marks its speaker as not to be trusted on this topic. **Symmetric encryption** (AES) uses one secret key for both directions: fast, and the key must be shared securely — which is the entire key-distribution problem. **Asymmetric encryption** (RSA, elliptic-curve) uses a key pair: the public key encrypts (or verifies), the private key decrypts (or signs). Slow, but it solves distribution: publish the public key freely, guard the private key absolutely. A **digital signature** is a hash signed with a private key — it gives you integrity *plus* origin: anyone with the public key can verify that the holder of the private key vouches for this exact content.

**Modes matter more than algorithms.** AES-128 in ECB mode and AES-128 in CBC mode are the same cipher and wildly different security. ECB encrypts each block independently, so identical plaintext blocks produce identical ciphertext blocks — structure leaks straight through the encryption. You will see this with your own eyes in the walkthrough: four identical blocks, four identical ciphertext blocks, the pattern visible without decrypting anything. The rule: never use ECB for data with structure (which is all real data); use an authenticated mode (GCM) or at minimum CBC with a random IV. This is the canonical example of "the algorithm is fine, the mode defeats it."

**PKI: how strangers trust each other's keys.** Asymmetric crypto has a bootstrapping problem: how do you know *this* public key belongs to your bank? A **certificate** binds an identity to a public key, signed by someone you already trust — a **certificate authority (CA)**. Trust chains upward: the server's certificate is signed by an intermediate CA, which is signed by a root CA sitting in your trust store. **Path validation** (RFC 5280 §6) is the algorithm your browser runs on every TLS connection: build the chain, check each signature, check each certificate's validity dates, check the name matches the site you asked for, check revocation status. Five checks; skip any one and the chain proves nothing. A **self-signed** certificate (issuer = subject, like the one you will mint) short-circuits this: there is no chain, so nothing is proven — fine for a lab, meaningless for trust.

**The key lifecycle** (SP 800-57 Part 1): keys are born (generated with proper randomness), distributed, used (only for their intended purpose and within their **cryptoperiod** — the window a key is authorized), stored (with protection matching their value), rotated or revoked, and destroyed. Every stage has a characteristic failure: weak generation (predictable keys), distribution in the clear, over-long cryptoperiods, keys in source code or backups nobody inventories, and "deletion" that leaves copies in snapshots. The professional question is never "which algorithm?" — it is "show me the key inventory, the rotation schedule, and the compromise procedure."

**TLS as the worked system.** TLS 1.3 does in one handshake what this whole lesson describes: the server presents its certificate chain (PKI), the client validates the path (RFC 5280), they negotiate parameters, derive ephemeral session keys (asymmetric/key-agreement doing the distribution, symmetric doing the bulk encryption), and everything after is authenticated encryption. When you see `TLS_AES_256_GCM_SHA384` in the walkthrough, read it as: TLS 1.3, AES-256 in GCM (authenticated) mode, SHA-384 in the key schedule. The handshake is the primitives composed correctly — which is why misconfiguration findings are about versions, cipher suites, and certificate hygiene, not about the math.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/e-crypto-applied.log`. Clean environment: OpenSSL 3.0.13, 2026-10-09, loopback only, nothing external touched. (One correction logged in the transcript: `xxd` is absent on this machine, so `od` was used for the block dumps — same information.)

1. **Hash and avalanche.** `echo -n "hello" | openssl dgst -sha256` → `2cf24dba…9824`. Change one bit of input (`hellO`) → `04a6f55f…770`, completely different. *Expect:* total change from a one-character difference. This is why hashes detect tampering — and why they provide zero secrecy.
2. **Symmetric roundtrip.** Encrypt a local file with `openssl enc -aes-256-cbc -pbkdf2`, decrypt with the right password (plaintext returns), then with the wrong password (`bad decrypt`). *Expect:* the failure is loud and total — there is no "almost right" password. Note `-pbkdf2`: password-based key derivation with salt and iterations; without it, the password *is* the key and dictionary attacks are trivial.
3. **ECB vs CBC.** Encrypt four identical 16-byte blocks with AES-128-ECB and AES-128-CBC (fixed key/IV for determinism). *Expect:* ECB shows the same 16-byte ciphertext block four times (`*` in the `od` output marks repeated lines); CBC shows five different blocks. You have just observed, without decrypting anything, that ECB leaks plaintext structure. This is the single most persuasive demo in applied cryptography — keep it.
4. **Sign and verify.** Generate an RSA-2048 keypair, sign a document, verify with the public key (`Verified OK`), tamper one byte, verify again (`Verification failure`). *Expect:* the signature binds the *exact* bytes; any change breaks it. This is what code signing, certificate issuance, and update verification all rest on.
5. **Mint and inspect a certificate.** `openssl req -x509 -newkey rsa:2048 -selfsigned -subj "/CN=lab.local"`, then `openssl x509 -noout -subject -issuer -dates`. *Expect:* subject = issuer = `CN = lab.local` (self-signed — no chain, no trust), validity exactly the 1 day requested. Ask the validator's five questions against it: chain? (none) dates? (ok) name match? (only if you asked for lab.local) revocation? (uncheckable) — it fails at step one, correctly.
6. **TLS handshake, locally.** Serve the self-signed cert with `openssl s_server` on 127.0.0.1:18443, connect with `openssl s_client`. *Expect:* `Protocol: TLSv1.3`, `Cipher: TLS_AES_256_GCM_SHA384`, the server presenting the lab.local chain. Read the cipher suite name as the composition from §3. Kill the server afterward and verify it is gone.

## 5. On your own

**Task:** Perform a cryptographic inventory of a system you control (your VPS, your home lab, a project repo): list every key, certificate, token, and secret — where each is stored, what it protects, its cryptoperiod/rotation state, and what happens on compromise. Then pick the worst finding and write the remediation as a key-management policy paragraph in the style of SP 800-57.

**Success test:** Your inventory includes at least one non-obvious item (a backup containing a key, a long-lived token in CI config, an expired or self-signed cert somewhere). The compromise procedure for your most valuable key is written down before you need it — if you had to invent it during the exercise, that was the finding.

## 6. Where it goes wrong

- **ECB mode (or any unauthenticated mode) on structured data.** The walkthrough's demo is the archetype. Rule: authenticated encryption (GCM) by default; if you must use CBC, random IV per message and a separate MAC.
- **Keys with the data.** Encrypted database backups on the same volume as the key file; API keys in the repo next to the code they protect. Encryption with accessible keys is obfuscation with extra steps.
- **Homegrown protocols.** "We XOR with a secret" / "we do two rounds of something." Never roll your own — the failure modes are subtle and the review you need costs more than the protocol saves.
- **Hashing passwords with SHA-256.** Fast hashes are the enemy of password storage — use a password-hashing function (bcrypt, scrypt, Argon2) with work factors, unique salts. SHA-256 is for integrity, not credentials.
- **Certificate hygiene.** Expired certs, name mismatches, missing chain intermediates, no revocation story. Path validation has five checks; operations teams routinely maintain one.
- **Cryptoperiod neglect.** Keys generated in 2019 still signing in 2026, with no rotation procedure and no inventory. SP 800-57's lifecycle exists because keys decay through exposure, not through math.
- **Confusing the guarantees.** "It's hashed" offered as confidentiality; "it's encrypted" offered as integrity (without authentication); a signature offered as proof of *who* when the key's owner is unverified. Name the guarantee before you claim it.

## 7. Read the source

Primary documents first:

- **NIST SP 800-57 Part 1 Rev. 5, Recommendation for Key Management** (csrc.nist.gov, May 2020) — *read* the key-lifecycle sections and the cryptoperiod guidance; *skim* the algorithm-specific advice. This is the document behind every "key management policy" you will ever write.
- **RFC 5280, Internet X.509 PKI Certificate and CRL Profile** (rfc-editor.org, May 2008) — *read* §3 (trust model), §4.1 (certificate fields), §6 (path validation algorithm); *skim* the extension catalog; *skip* the ASN.1 appendices on first pass.
- **RFC 8446, TLS 1.3** (rfc-editor.org) — *read* the handshake overview; this is where §3's composition happens for real.

Then at most three free resources:

1. **NIST SP 800-52 Rev. 2, Guidelines for the Selection and Use of TLS** (csrc.nist.gov) — free; the operational companion: which versions and suites to actually configure.
2. **OWASP Cryptographic Storage Cheat Sheet** (cheatsheetseries.owasp.org) — free; the practitioner checklist for choosing primitives correctly.
3. **"Serious Cryptography" chapter excerpts / Dan Boneh's Crypto I (Coursera, free to audit)** — free; the mathematical foundations behind the primitives, when you want to go deeper than this lesson.

## 8. Check yourself

1. Explain why ECB mode leaks plaintext structure while CBC does not — then explain what CBC still fails to provide that GCM adds, and what attack that enables.
2. A team stores AES-encrypted backups in the same cloud bucket as the key file, with a README explaining the arrangement. Explain which guarantee the encryption still provides and which it does not — and what the single cheapest fix is.
3. Walk the five path-validation checks against a certificate that is valid, unexpired, properly chained, but issued for `app.example.com` while the user visited `api.example.com`. Which check fails, and what does the browser do?
4. A developer proposes "double SHA-256" for password storage, arguing two rounds is stronger than one. Explain the actual threat model for stored passwords and why iteration count is the wrong axis — what property must the function have instead?
5. Predict what breaks first in an organization that deploys mutual-TLS service authentication with 10-year client certificates and no inventory: the math, the rotation, or the revocation — and describe the incident that reveals it.

## 9. Prove it

**Artifact:** your cryptographic inventory (every key/cert/token/secret, storage location, cryptoperiod state, compromise procedure) plus the ECB-vs-CBC demonstration reproduced on your own machine with your own explanation of what it proves.

**Honest claim:** "I can select cryptographic primitives correctly, read a certificate chain against the validation algorithm, and spot the five common misuses — I know what breaks and where to look."
**Can't claim yet:** "I can design cryptographic protocols" — protocol design is a specialist discipline with its own review process; this lesson taught correct *use* of established primitives, which is what the job needs.

## 10. Leads to

- **e-data-protection-controls — Data protection controls** — encryption at rest/in transit as an organizational control set; this lesson's inventory becomes its input.
- **e-secure-design — Secure design principles** — "use established cryptography" as a design principle with teeth.
- `a-http-depth` — reread the TLS handshake section now that you have run one; `b-security-headers` — HSTS as the policy that keeps TLS from being optional.
- Map refs: **CISSP 3.6** (this lesson); feeds **CISSP 2.6** (data protection), **4.3** (secure channels).
