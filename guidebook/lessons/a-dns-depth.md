# DNS in depth

**ID:** `a-dns-depth` · **Stage:** A (Foundations) · **Level:** 3 (mechanism — you can explain every section of a DNS message and trace a name from keystroke to answer) · **Prerequisites:** A terminal you can type in. The shell itself gets its deep treatment in `a-linux-cli` — read it alongside this lesson if commands feel unfamiliar.

**Map refs:** Pre-map foundations; feeds Stage B (SSRF via DNS rebinding, subdomain enumeration) and Stage E.

---

## 1. Where this shows up

Nothing on a network happens before DNS. The login flow this whole stage builds toward starts with a name typed into a client, and the first question the machine asks is "what address is that?" — answered by DNS, before a single TCP packet moves. As a defender you will read DNS logs more than almost any other telemetry: every malware callback, every phishing page load, every data-theft trickle leaves a DNS question first, because the attacker also needs names to become addresses. As an attacker (authorized, in a lab) you will meet DNS as both a target — cache poisoning, tunneling — and a tool — subdomain enumeration is DNS questions asked cleverly. This lesson is the naming layer of the stack. `a-tcpip-ports` is the transport layer underneath it.

## 2. Before you start

- A terminal with `python3` (verify: `python3 --version`). No `dig` needed — the walkthrough uses a small stdlib DNS client you can read line by line, which teaches more than `dig` output anyway.
- Everything runs on `127.0.0.1`. The toy authoritative server answers only for `lab.example`, a name that exists nowhere else. Nothing leaves your machine except the read-only lookups your OS already performs.
- Optional: `a-linux-cli` open in another tab for the shell concepts.

## 3. How it works

IP addresses route packets; humans remember names. DNS is the distributed database that translates between them — and "distributed" is the whole design. No single machine holds all names. Instead, the namespace is a tree, and each branch is owned by whoever runs that zone.

Read a name right to left. In `web.lab.example.`, the trailing dot is the **root** — the top of the tree, served by the root nameservers. `example` is a **top-level domain (TLD)**; `lab` is a **zone** someone administers; `web` is a host inside it. A **zone** is the unit of authority: the set of names one organization is responsible for answering. The server that holds a zone's data is **authoritative** for it — its answer is the truth, not a guess. Your machine's **stub resolver** (the small client in every OS) never walks the tree itself; it asks one question of a **recursive resolver** — usually your ISP's or your company's — and that resolver does the walking: root, then TLD, then authoritative, following **referrals** ("I don't know, but the `.example` servers are over there") until it gets an answer. The eight-step version of this walk is described well in Cloudflare's DNS learning articles (see §7); the shape to internalize is *iterative descent with caching at every level*.

What travels on the wire is a **DNS message** (RFC 1035 §4.1), and it has four sections you must be able to read cold:

- **Header** — an ID (matches question to answer), flags, and four counts: how many questions, answers, authority records, and additional records follow. Two flags carry security meaning you will meet again: the `rcode` field (`NOERROR`, `NXDOMAIN`, `SERVFAIL` — three very different failures) and, in DNSSEC, the `ad` (authenticated data) flag.
- **Question** — the name, the query type (`QTYPE`: A, AAAA, MX, …), and the class (almost always `IN`, Internet).
- **Answer** — the **resource records (RRs)** that answer the question. Each RR has a name, type, class, **TTL** (time-to-live, in seconds), and the data itself (`RDATA`).
- **Authority / Additional** — who is authoritative, and helpful extras (like the IP of the nameserver just named, so you don't need a second lookup to continue the chase).

The record types you must know (RFC 1035 §3.3): **A** (IPv4 address), **AAAA** (IPv6), **CNAME** (alias — "this name is really that name; go ask again"), **MX** (mail exchanger), **NS** (the nameservers for a zone — the delegation mechanism itself), **PTR** (reverse lookup: address → name, used in the `in-addr.arpa` zone), **SOA** (start of authority: the zone's metadata), **TXT** (free text — SPF, DKIM, domain verification, and, in attacker hands, a covert channel).

Two mechanics make DNS fast and make it dangerous. First, **caching**: every answer carries a TTL, and every resolver along the path may serve the cached copy until it expires. This is why DNS changes take time to propagate — and why a poisoned cache entry persists: the attacker only needs to win once per TTL window. Second, **transport**: DNS normally rides **UDP** (one question, one answer, no handshake — fast), with **TCP fallback** for large answers and zone transfers (RFC 1035 §4.2). UDP's lack of a handshake is exactly what made classic cache-poisoning attacks possible: forging a reply is cheap when there is no connection to hijack. (The 2008 Kaminsky attack is the famous demonstration — understand *that unauthenticated UDP was the flaw*, not the exploit code.)

**DNSSEC** is the fix for authenticity, and you must understand precisely what it does and does not do. It adds signatures (`RRSIG` records) over the data, with keys (`DNSKEY`) linked up the tree through delegation-signer (`DS`) records — a **chain of trust from the root's key down to the zone**. A validating resolver checks the signatures and sets the `ad` flag. What it fixes: forged answers. What it does *not* fix: privacy (queries and answers are still plaintext — that needs DoT/DoH, a different lesson), or the last mile between the stub resolver and your application.

One more resolution source lives *before* DNS: **`/etc/hosts`** (and its Windows equivalent). The OS checks local files before asking the network. Malware has abused this for decades — a hosts-file entry silently redirects a name without touching DNS at all. When a name resolves strangely, check the files first.

### Worked example: one name, end to end

From the walkthrough (§4): the toy server is authoritative for `lab.example`. Ask for `web.lab.example.` type A. The question section names the name and type; the answer section returns one RR: `web.lab.example. ttl=300 A 127.0.0.1`. Ask for `alias.lab.example.` and the answer is a CNAME pointing at `web.lab.example.` — the resolver's job is now to issue a *second* query for the target, which is why CNAME chains cost round trips. Ask for a name that doesn't exist and the header comes back with `rcode=NXDOMAIN` and zero answers: the server is authoritative and *certain* the name doesn't exist — different from `SERVFAIL` ("I tried and failed"), a distinction that matters when you're debugging or detecting.

Now map that onto the real world. When you type a public name, your stub resolver asks your recursive resolver; the recursor walks root → TLD → authoritative, caching each step by its TTL; the final A record comes home and your application opens a TCP connection to it. That connection is `a-tcpip-ports`; what the application says over it is `a-http-depth`. The three lessons are one story told in order.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/a-dns-depth.log`. Clean environment: stock Python 3.12, loopback only, 2026-10-09. This sandbox blocks UDP loopback, so the toy server and the lesson's stdlib client speak the TCP form of DNS (RFC 1035 §4.2) on `127.0.0.1:53535`; the message format on the wire is identical. **Update 2026-10-10:** every query step re-ran with real `dig` 9.18.39 (`+tcp -p 53535 @127.0.0.1`) — A, CNAME, TXT, NS, and NXDOMAIN all corroborated; see the re-run entry in the log.

1. **See what your machine knows without DNS.** `getent hosts localhost` — the answer comes from `/etc/hosts`, no query sent. Read the top of `/etc/hosts` and note: files beat the network.
2. **Start the toy authoritative server** (`python3 toy_dns.py` — ~90 lines of stdlib, in the transcript header). It serves only `lab.example`.
3. **Ask an A question and read the sections.** `python3 dnsq.py web.lab.example. 1 --tcp` — identify the header (id, rcode, counts), the question, and the answer RR. Point at the TTL and say what it controls.
4. **Chase a CNAME.** `python3 dnsq.py alias.lab.example. 1 --tcp` — the answer names another name, not an address. Issue the follow-up query yourself and note that a resolver does this automatically.
5. **Read TXT and NS.** Query type 16 and type 2 for `lab.example.` — TXT carries arbitrary text (here an SPF record); NS names the zone's servers (delegation made visible).
6. **Ask for something that doesn't exist.** `python3 dnsq.py nosuchhost.lab.example. 1 --tcp` — `rcode=NXDOMAIN`, zero answers. Say out loud why NXDOMAIN differs from SERVFAIL.
7. **Reverse it.** `python3 -c "import socket; print(socket.gethostbyaddr('127.0.0.1'))"` — the PTR direction: addresses have names too.
8. **Watch caching logic.** Query the A record twice; both carry `ttl=300`. Explain to yourself why a real resolver would only send the first query.
9. **DNSSEC — not run by us.** Verifying a real chain needs a validating resolver and a signed zone. On your own machine: `dig +dnssec example.com` and look for `RRSIG` records and the `ad` flag.

## 5. On your own

**Task:** Extend the toy server with two records: an MX record for `lab.example.` pointing at `mail.lab.example.` with preference 10, and an A record for `mail.lab.example.`. Then answer, with query transcripts: (a) where does mail for `lab.example.` go? (b) what does a query for `mail.lab.example.` type MX return, and why is the rcode not an error?

**Success test:** Two transcripts showing the MX answer (with the preference value visible in the RDATA) and the follow-up A query, plus one paragraph explaining why MX exists as a separate type instead of reusing A.

**Hints:** The MX RDATA is a 2-byte preference followed by an encoded domain name — look at how the CNAME RDATA is built in `toy_dns.py`. For (b), think about what "authoritative and certain" means when the name exists but the type doesn't.

## 6. Where it goes wrong

- **NXDOMAIN is not SERVFAIL is not timeout.** NXDOMAIN: authoritative "no." SERVFAIL: "I broke trying." Timeout: "nobody answered." Misreading these sends debugging in exactly the wrong direction — and in detection, a burst of NXDOMAINs is the classic signature of malware's domain-generation algorithm (DGA) fishing for its controller.
- **TTL blindness.** Assuming a DNS change is instant. It isn't; caches at four levels each honor the TTL. During incident response, "we fixed the record" means nothing until the longest TTL in the chain dies.
- **Trusting DNS answers.** Without DNSSEC, any answer is an assertion by whoever replied fastest. Cache poisoning, on-path injection, and rogue resolvers all exploit this. DNSSEC fixes authenticity, not privacy — know which problem each tool solves.
- **TXT as a junk drawer.** SPF, DKIM, verification tokens — and attacker-controlled text. A TXT record is data, not a trust signal; reading it as one is how domain-verification bypasses happen.
- **CNAME chains and loops.** Every CNAME is another query (latency, another cache entry) and a misconfigured pair can loop. Resolvers cap the chase; know the cap exists.
- **The hosts file shadow.** A name resolving "wrong" with clean DNS means checking `/etc/hosts` — and on a compromised box, the hosts file is a persistence mechanism, not a misconfiguration.
- **DNS as a covert channel.** DNS tunneling (data encoded in queries to an attacker-controlled authoritative server) exfiltrates through the one protocol every firewall allows. Defenders: monitor query volume, label entropy, and TXT-heavy patterns per domain — this is Stage D detection work, built on this lesson.

## 7. Read the source

Primary documents first — read with a purpose, skip without guilt:

- **RFC 1034, Domain Names — Concepts and Facilities** (rfc-editor.org/rfc/rfc1034) — *read* the concept sections on the name space, zones, and the resolver/name-server split. This is the vocabulary; 1035 is the machinery.
- **RFC 1035, Domain Names — Implementation and Specification** (rfc-editor.org/rfc/rfc1035) — *read* §2.1–2.2 (overview, common configurations — the diagrams of who asks whom), §3.2–3.3 (RR definitions and the standard types), §4.1 (message format — match each field to the walkthrough output), §4.2 (transport — UDP normally, TCP when); *skim* §6–7 (server/resolver implementation); *skip* §5 (master file syntax) until you run a real nameserver.
- **RFC 4033–4035, DNSSEC** (rfc-editor.org) — *read* 4033 §2–3 (what DNSSEC adds: RRSIG, DNSKEY, DS, the chain of trust) when you do step 9 on your own machine; *skip* the cryptographic details.

Then at most three free resources:

1. **Cloudflare Learning Center — DNS** (cloudflare.com/learning/dns/what-is-dns) — the clearest free walkthrough of the 8-step resolution chain, recursive vs authoritative servers, and caching; read after the RFCs to consolidate.
2. *(Second slot intentionally empty — the RFCs plus one guide are the right depth here. A DNSSEC visualization tool goes in the directory, not the lesson.)*

## 8. Check yourself

1. Your stub resolver asks for `shop.example.com`. List every server the recursive resolver contacts in the worst case (nothing cached), and name what each one returns — a referral or an answer.
2. A response has `rcode=NXDOMAIN` with `an=0`. A colleague says "DNS is down." Explain precisely what is wrong with that conclusion and what you would check next.
3. You add a CNAME `www` → `web` and an A record for `web`. A user reports the site is slow to first byte but fast after. Explain using TTLs and the CNAME chase.
4. An attacker can see but not modify your DNS traffic. Which of these does DNSSEC protect you against: (a) the attacker forging an answer, (b) the attacker learning which names you look up? Explain what each protection would actually require.
5. `getent hosts payroll` returns an address, but `dig payroll` (against your resolver) returns NXDOMAIN. Explain the discrepancy and name the security-relevant reason to check the local answer first on a suspect machine.

## 9. Prove it

**Artifact:** a lab notebook containing: the annotated message-section dissection from step 3 (every field named), the CNAME chase from step 4 as two transcripts, and a hand-drawn diagram of the full resolution chain for a public name (stub → recursor → root → TLD → authoritative) with where caching happens at each level.

**Honest claim:** "I can read a DNS message field by field, trace a name through the resolution chain, and explain what TTL, CNAME, NXDOMAIN, and DNSSEC do and don't guarantee."
**Can't claim yet:** "I can run or attack DNS infrastructure" — operating a real nameserver and the offensive/defensive DNS work are later lessons; this one built the mental model and the reading skill.

## 10. Leads to

- `a-tcpip-ports` — next: the name resolved to an address; now learn what actually crosses the wire to that address (the handshake, ports, connections).
- `a-http-depth` — after TCP: DNS answers *where*, HTTP answers *what* — the three lessons together narrate one page load, the Stage A milestone.
- Stage B (later): subdomain enumeration is DNS asked at scale; DNS rebinding turns this lesson's mechanics into an SSRF primitive — you will meet both with authorization and a lab.
