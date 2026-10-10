---
lesson_id: b-xxe
slug: xxe
stage: B
level: 3
prerequisites: [a-http-depth, b-ssrf]
roles: [pentester, appsec]
map_refs: []
test_date: 2026-10-10
description: "XXE: when the XML parser works for the attacker — external entity injection reproduced locally, then fixed with secure parser configuration. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-10 · transcript in runs/b-xxe.log"
---
# XXE: when the parser works for the attacker


**Map refs:** CWE-611 (Improper Restriction of XML External Entity Reference) · PortSwigger Web Security Academy (XXE)

---

## 1. Where this shows up

XML is still everywhere: SOAP APIs, SAML assertions (SAML — Security Assertion Markup Language — the XML-based tokens used in single sign-on logins), document uploads (DOCX/XLSX are zipped XML), SVG images, configuration files. An XML parser that resolves **external entities** will fetch URLs and read files *on the attacker's behalf* — which makes XXE the XML-flavored cousin of SSRF, plus a denial-of-service variant (billion laughs) that needs no network at all. This lesson takes you to Level 3: you will reproduce entity expansion against a local parser, understand why real-world parsers are more dangerous than the demo, and verify the hardening.

## 2. Before you start

- You can read HTTP requests and responses cold (`a-http-depth`).
- You understand the SSRF lesson's shape — the server acting on attacker-chosen destinations — because XXE's file-read/SSRF impact is that shape through an XML parser.
- Your target is written down and authorizes your testing: this lesson's local parser demo, a PortSwigger Academy XXE lab, or a bounty program whose scope explicitly includes the asset. Never point an external-entity payload at a real file on a real target to "see if it works" — the file content in the response *is* the exfiltration. Re-read B-AUTH if this sentence surprised you.
- Tooling: curl or any HTTP client. The payloads are small enough to write by hand.

## 3. How it works

XML lets a document define its own shortcuts called **entities**:

```xml
<!DOCTYPE note [
  <!ENTITY greeting "Hello, world">
]>
<note>&greeting;</note>
```

`&greeting;` expands to `Hello, world`. Entities can also be **external**: instead of a literal value, the definition points at a URL or file, and the parser fetches it:

```xml
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

A parser with external entities enabled reads `/etc/passwd` and puts its content where `&xxe;` was. Change the SYSTEM identifier to `http://169.254.169.254/...` and you have SSRF through the parser. **Why it arises in real code:** the developer enabled a feature-rich XML parser with default settings, and the defaults of several major parsers (Java's, libxml2's, .NET's older ones, PHP's) historically resolved external entities. Why the defaults were dangerous: external entities were designed as a *feature* for trusted documents — shared boilerplate pulled into many files from one place. XML's threat model assumed the document author was trustworthy. On the web, the document author is the attacker, and the feature became the vulnerability. The developer never asked "what can the *document* make my parser do?"

**Billion laughs: the DoS variant.** Entities can reference other entities:

```xml
<!ENTITY lol "lollollollollollollollollollol">
<!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
<!ENTITY lol3 "&lol2;&lol2;...">  <!-- ten more levels -->
```

A few hundred bytes of definitions expand to gigabytes — exponential amplification. No network, no exfiltration, just a parser consuming all memory. It is called "billion laughs" after the `lol` entity names in the original report.

**What the demo shows honestly.** Python's `xml.etree` — the walkthrough's parser — *expands internal entities* (billion laughs works, demonstrated) but *refuses external entities* (raises an error, demonstrated). Real-world parsers in other ecosystems resolve external entities unless hardened — that is where the file-read and SSRF impact lives, and it is taught here at concept level with the exact hardening, practiced hands-on in PortSwigger's labs. The lesson's honesty rule: the demo proves what *this* parser does; the dangerous behavior is named, sourced, and not pretended about.

**How defenders see it.** `<!DOCTYPE` and `<!ENTITY` in request bodies are the tripwire — legitimate XML from your own clients rarely contains either (your schemas don't use DTDs — document type definitions, the XML mechanism that declares entities and structure). In the request log, the attack announces itself:

```
POST /upload 200 312ms  body="<?xml version=\"1.0\"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]>..."
```

Legitimate clients send data; only an attacker sends a DOCTYPE. Alert on both strings in XML-bearing endpoints. In code review: any XML parser configured with DTD processing or external-entity resolution enabled; `DocumentBuilderFactory` without `disallow-doctype-decl`; `XmlReader` without `DtdProcessing.Prohibit`. The fix is parser configuration, and the detection is the DOCTYPE string.

### Worked example: the upload demo

An XML upload endpoint (stdlib Python, local only — the walkthrough runs it):

- Benign `<root>hello</root>` → parsed, 5 chars. Baseline.
- Billion-laughs document (300 bytes of entity definitions) → parsed, **30,000 chars** of expanded text. The 1000x amplification is the vulnerability: scale the definitions slightly and the parser falls over.
- External-entity document (`SYSTEM "file:///etc/hostname"`) → **rejected by the parser** (this parser doesn't resolve externals — the dangerous behavior is documented, not demonstrated, per the honesty rule above).

The fix, in the same app: **reject any document containing a DOCTYPE** — no DTD means no entities of either kind. (A DOCTYPE — the declaration at the top of an XML document that can carry the document's own entity definitions.) Re-test: billion laughs → 400 rejected; benign XML → still parses. Then the general rule for real stacks: disable DTD processing and external-entity resolution in the parser configuration (the OWASP XML Security Cheat Sheet lists the exact flags per parser), and prefer JSON where the format is your choice.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-xxe.log`. Clean environment: stock Python 3.12 (`xml.etree`), loopback only, 2026-10-10. The demo parser stands in for the resolving parsers the reader meets in PortSwigger's labs (see the honesty note in section 3).

1. **Start the app.** Save the `app.py` from this lesson's companion and run it on port 8334. Confirm the baseline: POST `<root>hello</root>` to `/upload` → 200, parsed.
2. **Prove entity expansion.** POST the billion-laughs document (in the companion) → 200 with `text_len=30000` from ~300 bytes of definitions. Compute the amplification factor and write it down — this number is the finding.
3. **Probe external entities.** POST the `SYSTEM "file:///etc/hostname"` document → 400, parser refuses. Write down *exactly* what happened (refusal, not resolution) and why this parser differs from Java/libxml2/.NET defaults — the difference is the lesson.
4. **Apply the fix.** Restart with `HARDENED=1` on port 8335: any `<!DOCTYPE` → 400.
5. **Verify the fix — two cases.** Billion laughs → 400 rejected; benign XML → 200, still parses. A fix that breaks legitimate documents is not a fix.
6. **Read the defender view.** The companion logs the raw request bodies. Find your `<!ENTITY` and `<!DOCTYPE` strings. Write the detection rule: alert on either string in XML-bearing request bodies — and note beside it that your own clients' schemas never emit them.

No step above is marked "not run by us" — expansion, refusal, and hardening all ran locally. External-entity *resolution* (the file-read/SSRF impact) is PortSwigger-lab material by design: the concept, the parser flags, and the detection are taught here; the resolving behavior is practiced there.

## 5. On your own

**Task:** Pick one authorized target you have not touched in this lesson — a PortSwigger Academy XXE lab (start with "Exploiting XXE using external entities to retrieve files"). Before touching the lab, read its parser context: the lab tells you the stack. Then: (1) prove entity *definition* is processed (billion-laughs-shaped probe, small), (2) escalate to the file read exactly as the lab documents, (3) state the parser-hardening fix for that stack from the OWASP cheat sheet.

**Success test:** A one-page report: the parser/stack, the expansion proof (with the amplification factor), the file-read evidence (exact request/response), the per-parser hardening flags, and the defender detection (which log, which strings). If the lab's parser is already hardened, document the hardening you found — a characterized defense is a result.

## 6. Where it goes wrong

- **"Our parser doesn't resolve externals, so we're safe."** Billion laughs needs no external resolution — internal entity expansion alone is a DoS. Harden against *both*.
- **Allowlists of "safe" SYSTEM URLs.** `file:///etc/passwd` blocked but `http://169.254.169.254/` allowed is SSRF through the parser. The fix is disabling the feature, not filtering its targets.
- **Testing file reads against real files on real targets.** The file content in the response is exfiltration the moment it works. In labs, read the lab's designated canary file (a canary file — a harmless file the lab provides specifically for you to read as proof, so you never touch real data); nowhere else.
- **Assuming JSON APIs can't have XXE.** The content type is negotiated, not declared: if the endpoint *parses* XML anywhere in the chain (a library, a middleware, a document converter), the XML you send is the XML that matters. Test what is parsed, not what the docs say.
- **Forgetting SVG and document uploads.** SVG is XML. DOCX is zipped XML. "File upload" features are XML parser features in disguise — the XXE checklist applies to every upload that gets parsed.
- **Partial hardening.** Disabling external entities but leaving DTDs on still allows billion laughs. The cheat sheet's rule is total: disallow DOCTYPE declarations entirely unless the application genuinely needs DTDs (it almost never does).

## 7. Read the source

Primary documents first:

- **PortSwigger Web Security Academy — XXE** (portswigger.net/web-security/xxe — verified 2026-10-10): the canonical treatment — file retrieval, SSRF via XXE, blind XXE via out-of-band techniques. *Read* fully, then do the labs.
- **OWASP XML Security Cheat Sheet** (cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet.html — verified 2026-10-10): per-parser hardening flags (Java, .NET, Python, PHP). *Read* the section for your stack; this is the fix.
- **CWE-611** (cwe.mitre.org/data/definitions/611.html — verified 2026-10-10): Improper Restriction of XML External Entity Reference. *Skim*; cite the ID.

Then at most three free resources:

1. **PortSwigger XXE labs** (portswigger.net/web-security — free): file-retrieval and blind XXE labs, hosted and authorized.
2. **`b-ssrf`** (this guidebook): the SSRF half of XXE's impact — the metadata-service angle applies through parsers too.
3. **OWASP XXE Prevention Cheat Sheet** (via the XML Security sheet above — free): the one-page fix summary.

## 8. Check yourself

1. Explain the difference between an internal entity and an external entity, and which of billion laughs / file-read each one enables.
2. A 300-byte XML document produces 30,000 characters of parsed text. Explain the amplification mechanism and why no network access was needed.
3. Your parser refuses `SYSTEM "file:///etc/hostname"` with "undefined entity." Explain what this tells you about the parser's configuration, and what you would check next on a Java stack.
4. A developer "fixes" XXE by blocking the string `file://` in uploads. Explain two bypasses (SSRF via http:// to metadata; billion laughs needs no URL at all) and state the correct fix.
5. Explain why SVG upload features and DOCX processing belong on the XXE checklist, even though the feature is called "image upload" or "document import."

## 9. Prove it

**Artifact:** the one-page report from "On your own": parser/stack, expansion proof with amplification factor, file-read evidence, per-parser hardening flags, defender detection.

**This lesson takes you to Level 3 (Apply).** You can honestly claim: you can prove XML entity expansion, characterize a parser's external-entity behavior, apply the DOCTYPE-rejection hardening, and write the detection rule — on authorized targets. You cannot yet claim: blind-XXE exfiltration technique on live stacks — the out-of-band escalation is lab-bounded practice in PortSwigger's labs.

## 10. Leads to

- `b-ssrf` (re-read the metadata angle) — XXE's SSRF impact is the same destination reached through a parser.
- `b-deserialization` — the next "parser works for the attacker" class: untrusted input reaching object construction.
- `d-malware-analysis` — document-format parsing as an attack surface from the defender's side.
- Map refs: **CWE-611** · **PortSwigger XXE** · **OWASP XML Security Cheat Sheet**.
