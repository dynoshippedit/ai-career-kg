---
lesson_id: a-crypto
slug: crypto
stage: A
level: 2
prerequisites: [a-linux-cli, a-http-depth]
roles: []
map_refs: ["CISSP 3.6"]
test_date: 2026-10-10
description: "Cryptography: what hashing, encryption, signatures and certificates do — and the misuses that defeat each one, demonstrated live. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-10 · salt demonstration added 2026-10-10 (run, transcript appended) · transcript in runs/a-crypto.log"
---
# Cryptography: what the primitives do, and what breaks when you misuse them


**Map refs:** CISSP 3.6 (cryptography concepts — the deep companion is `e-crypto-applied`) · NICE Implementation and Operation

---

## 1. Where this shows up

Every login you will ever test touches cryptography: the password is *hashed*, the session cookie is *signed* or *encrypted*, the traffic runs over *TLS*, the server's identity is a *certificate*. Cryptography is also where beginners cause the most damage with the best intentions — choosing the wrong primitive, or the right primitive used wrong, silently removes the protection. This lesson is Level 2: you will operate the real primitives with OpenSSL, verify what each one guarantees, and reproduce the classic misuses so you recognize them in code. The Stage E companion `e-crypto-applied` takes the same ground to full depth (modes, key lifecycle, TLS 1.3 internals).

## 2. Before you start

- You can run shell commands and redirect files (`a-linux-cli`).
- OpenSSL is installed (`openssl version` — any 1.1.1+ or 3.x; the walkthrough notes version-specific flags).
- Work in an empty scratch directory. Everything here is local; nothing leaves the machine.
- The rule for this whole lesson, stated up front: **never roll your own cryptography.** You will use vetted primitives through vetted libraries. The walkthrough shows *why* the rule exists by demonstrating what breaks.

## 3. How it works

Four primitives, four different promises. Confusing them is the root of nearly every crypto misuse.

**Hashing: a fingerprint, not a lock.** A hash function takes any input and produces a fixed-size digest. It is **one-way**: given the digest, you cannot recover the input. It is **deterministic**: the same input always gives the same digest. And it has the **avalanche effect**: changing one bit of input changes about half the output bits. What hashing is *for*: integrity checks (did this file change?), password *verification* (with salt — random data mixed into each password before hashing, so two users with the same password get different digests — and slowness — see the misuse section), data structures. What it is *not* for: hiding data. A hash is not encryption; there is no key and no decryption.

**Symmetric encryption: one key locks and unlocks.** AES with a 256-bit key scrambles plaintext into ciphertext; the same key unscrambles it. Fast, and the workhorse for bulk data (TLS record encryption, disk encryption). The hard problem it does *not* solve: getting the key to the other party without anyone else seeing it — the **key distribution problem**.

**Asymmetric encryption: two keys, a pair.** RSA (or elliptic-curve) gives you a **public key** (share freely) and a **private key** (never share). Data encrypted with the public key decrypts only with the private key. Slow — so real systems use it to exchange a symmetric key, then switch to AES. This solves key distribution: the public key can travel in the open.

**Digital signatures: proof of authorship, not secrecy.** Sign with the **private** key, verify with the **public** key. A valid signature proves the data came from the private-key holder and hasn't changed. (Note the direction is the reverse of encryption.) In practice you sign the *hash* of the data, not the data itself — signing is slow, so you sign the short digest, and the digest commits to the exact content: change one byte and the digest changes, so the signature no longer verifies. Signatures authenticate software updates, certificates, and JWTs.

**PKI and certificates: scaling trust.** If everyone has a keypair, how do you know a public key belongs to your bank? A **certificate** binds a public key to an identity, signed by a **certificate authority (CA)** you already trust. Your browser ships a list of trusted CA certificates; a server presents its certificate plus the chain up to a trusted root; your browser verifies each signature. Break any link — expired cert, wrong hostname, untrusted CA — and TLS warns you, because the *binding* is what you were trusting.

### Each primitive, paired with the misuse that defeats it

- **Hashing → using a fast hash for passwords.** MD5 and SHA-256 are *designed* to be fast; an attacker with your password database can try billions of guesses per second on a GPU. Password storage needs a **slow, salted** function (bcrypt, scrypt, Argon2): slowness is the feature. Finding `md5(password)` in code is a finding.
- **Symmetric encryption → ECB mode.** AES-ECB encrypts each block independently, so identical plaintext blocks produce identical ciphertext blocks — patterns survive encryption. The walkthrough shows it. Use CBC (with a random IV — an *initialization vector*, a random starting value so identical plaintexts encrypt differently) or, better, an authenticated mode (GCM — authenticated encryption also *proves the ciphertext wasn't tampered with*, which plain encryption never does).
- **Symmetric encryption → hardcoded keys and reused IVs.** A key in source code is not a secret; an IV reused across messages leaks information. Keys live in key management, never in the repo.
- **Asymmetric encryption → no integrity.** RSA/ECB-style "textbook" encryption without padding is malleable (an attacker can modify the ciphertext to produce predictable changes in the plaintext, without knowing the key). Real protocols use vetted padding and, critically, **authenticated** encryption — encryption alone never proves who sent a message.
- **Signatures → verifying with the wrong key, or not verifying.** The JWT `alg=none` class (`b-jwt-oauth`) is this misuse: the verifier accepts an unsigned token. A signature you don't check is decoration.
- **PKI → ignoring validation errors.** "Just click through the cert warning" trains users to accept attacker certificates. In code, disabling certificate verification "to make it work" removes the entire point of TLS.

**How defenders see misuse.** In code review: `md5(`, `sha1(` near passwords, `AES/ECB`, hardcoded key strings, `verify=False` / disabled cert validation, `alg=none`. In logs: nothing — crypto misuse is silent, which is why it survives. Detection is a code-review and configuration discipline, not a log search. The one log-side signal in this space: Certificate Transparency logs record every publicly-trusted certificate as it is issued — a certificate for your domain appearing there that you didn't request is the concrete signal of mis-issuance or an attacker minting certs in your name.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/a-crypto.log`. Clean environment: OpenSSL 3.0.13, empty scratch dir, 2026-10-10. Nothing leaves the machine.

1. **Hash, and watch the avalanche.** `printf 'hello' | openssl dgst -sha256` → note the digest. `printf 'hellp' | openssl dgst -sha256` → a completely different digest from a one-letter change. That is the avalanche effect, and it is why hashes work as fingerprints.
2. **Prove hashing is one-way.** There is no `openssl undgst`. Stare at that absence: the tool does not exist because the math does not allow it. (Rainbow tables attack *weak passwords*, not the hash function — which is why passwords need salt and slowness.)
3. **Symmetric round-trip.** `printf 'secret message' > plain.txt`; `openssl enc -aes-256-cbc -pbkdf2 -in plain.txt -out cipher.bin` (type a password); `openssl enc -d -aes-256-cbc -pbkdf2 -in cipher.bin` → the message returns. Now decrypt with the wrong password: it fails. The password-derived key is the entire security. (`-pbkdf2` selects PBKDF2, a password-based key-derivation function: it hashes your password many thousands of times to produce the key. The slowness is deliberate — this is the one legitimate use of slow hashing in the lesson.)
4. **ECB leaks patterns (the misuse).** Make a file of repeated 16-byte blocks: `python3 -c "open('repeat.bin','wb').write(b'A'*16*4)"`; encrypt with `-aes-128-ecb` and with `-aes-128-cbc`; `od -A d -t x1` both outputs. ECB: all four ciphertext blocks identical. CBC: all four different. Identical plaintext → identical ciphertext is the information leak; this is why ECB is never used for data with structure.
5. **Sign and verify.** `openssl genrsa -out key.pem 2048`; `openssl dgst -sha256 -sign key.pem -out sig.bin plain.txt`; `openssl dgst -sha256 -verify <(openssl rsa -in key.pem -pubout) -signature sig.bin plain.txt` → "Verified OK". Now change one byte of `plain.txt` and verify again → failure. The signature binds *this exact content* to the key holder.
6. **Certificates: inspect the binding.** `openssl req -x509 -newkey rsa:2048 -keyout srvkey.pem -out srvcert.pem -days 2 -nodes -subj "/CN=harborlight-books.example"`; `openssl x509 -in srvcert.pem -text -noout | head -30` → read the Subject, Issuer (self-signed: identical), validity dates, and the public key. In production this Issuer would be a CA your client trusts; here it is yourself, which is exactly why browsers would not trust it — the *chain* is the trust, not the math.
7. **The fast-hash password misuse.** `printf 'password123' | openssl dgst -md5` → `482c811da5d5b4bc6d497ffa98491e38`. That digest is in every breach list ever published; an attacker reverses it by *lookup*, not by math. State the fix out loud: per-password random salt, and a slow function (bcrypt/scrypt/Argon2) — speed is the enemy here.
8. **Salts, demonstrated.** `printf 'salt-A:password123' | openssl dgst -sha256` vs `printf 'salt-B:password123' | openssl dgst -sha256` — same password, two different digests, because the salt is part of the hashed input (see the transcript). That is the salt's whole job: identical passwords no longer collide, so a precomputed lookup table (a rainbow table) built for one salt is useless against another. Compare with the unsalted digest from step 7: one digest for everyone who chose that password.
9. **Clean up.** Delete the scratch dir. Keys generated for a lesson are never reused.

No step above is marked "not run by us" — every command ran locally against OpenSSL 3.0.13.

## 5. On your own

**Task:** Write a three-paragraph "crypto review" of a fictional login system: passwords stored with `sha256(password)`, session tokens as AES-ECB-encrypted user IDs with a hardcoded key, and API clients that disable certificate verification "because the staging CA isn't trusted." For each of the three, name the primitive, the promise it was supposed to keep, the misuse that defeats it, and the correct construction.

**Success test:** A stranger reading your review can (a) explain why each construction fails *in one sentence each*, (b) state the fix as a named primitive or configuration, and (c) quote the "never roll your own" rule and say what it forbids. If any paragraph blames "weak encryption" without naming the mechanism, rewrite it.

## 6. Where it goes wrong

- **"Encrypted" means nothing by itself.** Encrypted *with what, in which mode, with the key stored where?* Every one of those answers can void the encryption. Ask all three.
- **Hashing a password with SHA-256 and calling it secure.** Fast hashes are for integrity, not for password storage. The fix is slowness + salt, not a "stronger" fast hash.
- **ECB anywhere near structured data.** If you can see the shape of the plaintext in the ciphertext, the mode failed. GCM (or CBC with HMAC) is the default answer.
- **Rolling your own.** "I'll just XOR with the password" / "my own cipher" — the failure mode is always the same: unreviewed constructions break in ways their authors cannot see. Use vetted libraries; the lesson's rule is absolute.
- **Confusing signing with encrypting.** A signature proves *who*; encryption provides *secrecy*. A signed-but-unencrypted message is readable by everyone; an encrypted-but-unsigned message could come from anyone.
- **Treating a self-signed cert as "basically fine."** The math is identical; the *trust* is absent. In production, the chain to a trusted root is the whole product.

## 7. Read the source

Primary documents first:

- **OWASP Cryptographic Storage Cheat Sheet** (cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html — verified 2026-10-09): the practitioner checklist — which primitive for which job, key management rules. *Read* the primitive-selection and key-management sections.
- **NIST SP 800-57 Part 1 Rev. 5** (csrc.nist.gov — verified 2026-10-09): key management guidance — key lifecycle, cryptoperiods. *Skim* for the lifecycle concept; the lesson's "keys never in the repo" is this document's advice in one line.
- **RFC 5280** (rfc-editor.org/rfc/rfc5280.txt — verified 2026-10-09): X.509 certificates and path validation. *Skim* §6 (certification path validation) to see what "the chain" means formally.

Then at most three free resources:

1. **Latacora's cryptographic right answers** (latacora.com/blog — free): opinionated, current "what to use" guidance. Read once, then check it against the OWASP sheet above.
2. **`e-crypto-applied`** (this guidebook, Stage E): the deep companion — modes, key lifecycle, TLS 1.3 internals, all run locally.
3. **PortSwigger Academy — crypto-adjacent labs** (portswigger.net/web-security — free): the JWT and authentication labs make the signature-verification misuse concrete.

## 8. Check yourself

1. You find `md5(password)` in a login system. Explain *why* this is a finding in two sentences: what property of MD5 the attacker exploits, and what the correct construction is.
2. An encrypted database column shows repeating 16-byte ciphertext blocks wherever the plaintext repeats. Name the mode, explain the leak, and state the fix.
3. Explain the difference between "the message is signed" and "the message is encrypted" — what each guarantees, and what each does *not* guarantee.
4. A developer disables certificate validation in the API client "temporarily." Explain what protection just disappeared, using the chain-of-trust concept.
5. Why does the rule "never roll your own cryptography" exist, given that AES itself was designed by two people? (Hint: what happened *after* they designed it?)

## 9. Prove it

**Artifact:** the three-paragraph crypto review from "On your own," plus your walkthrough notes showing each command and what it proved (avalanche observed, ECB blocks identical, signature failed after tampering, cert fields read).

**This lesson takes you to Level 2 (Operate).** You can honestly claim: you can operate the core primitives, verify their guarantees hands-on, and recognize the six classic misuses in code or configuration. You cannot yet claim: cryptographic design judgment or protocol analysis — that is what `e-crypto-applied` finishes, including modes, key lifecycle, and TLS 1.3.

## 10. Leads to

- `e-crypto-applied` — the deep companion: same ground at Stage E depth (modes, key lifecycle, TLS 1.3 handshake internals).
- `b-jwt-oauth` — where the signature-verification misuse becomes a live vulnerability class (`alg=none`, key confusion).
- `a-http-depth` (re-read the TLS section) — now that you know what the handshake is *for*.
- Map refs: **CISSP 3.6** (with `e-crypto-applied`) · **NICE Implementation and Operation**.
