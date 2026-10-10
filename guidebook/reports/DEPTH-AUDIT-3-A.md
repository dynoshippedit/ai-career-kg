# DEPTH-AUDIT-3-A — Third depth pass, Stage A (2026-10-10)

Worker pass, depth 2/2. Task: re-audit all 10 Stage A lessons with three **new** lenses, distinct from DEPTH-AUDIT-2.md's jargon/why/detection/reading-guidance work (skimmed, not repeated). Scope checklists taken from the brief's §5 scope. Rules honored: no commits/pushes, no full build, loopback-only labs, test servers killed by explicit PID and pgrep-verified, no currency symbols, no banned words, exactly ten `##` sections preserved in every file, frontmatter intact.

**Changed: 9 of 10.** `a-git-github.md` untouched (all three lenses passed it as-is). Datelines on the other nine note the third depth pass.

---

## Per-lesson table

| Lesson | Lens 1 (scope) | Lens 2 (prereqs) | Lens 3 (exercises) |
|---|---|---|---|
| a-tcpip-ports | **FIRED HARD** — 6 missing sub-items added | §10 lead-to line corrected | §8 Q2 rewritten; §9 artifact extended with address plan |
| a-http-depth | **FIRED** — 3 missing sub-items added | `a-linux-cli` added to prereqs | §8 Q1 rewritten; §9 artifact rebuilt around reader's own build |
| a-linux-cli | **FIRED** — "memory" missing from §5's "processes and memory" | **cycle broken**: removed `a-tcpip-ports` from prereqs; §1/§6 references fixed | §5(a) verifiability fixed; stale §9 "Can't claim yet" corrected |
| a-crypto | no fire | no fire (loose but acyclic) | §9 artifact was §5 replay → added unaided 4th paragraph |
| a-dns-depth | no fire | no fire | §8 Q1 rewritten |
| a-python-security | no fire | forward reference fixed (3-packet handshake now taught inline) | §8 Q2 rewritten |
| a-reading-code | no fire | **chain inverted**: removed `b-sqli` (Stage B) from prereqs | §8 Q1, Q3 rewritten |
| a-osint-research | no fire (N/A — not in §5 bullets) | **contradiction fixed**: removed `b-authorization-scope` from prereqs; rule now taught up front in §2 | §8 Q4 rewritten |
| a-windows-concepts | no fire | no fire | §8 Q2 rewritten |
| a-git-github | N/A | no fire | none — already explain/predict, verifiable, genuine |

---

## Lens 1 — Scope completeness (what was missing, what was added)

### a-tcpip-ports — fired hardest. Six §5 sub-items absent or name-dropped; all taught now.

The §5 networking bullet demands: "TCP/IP stack layer by layer, **IPv4 AND IPv6 addressing and subnetting**, how DNS resolves a name, **DHCP, routing**, ports, and **what firewalls, VPNs, proxies and VLANs do to traffic**." Grep confirmed the gaps were real: DHCP, subnet, VLAN, DORA, default-gateway, and `ip route` appeared in **zero** lessons; "proxy" appeared only as "a scanner or proxy"; "vpn" only as a subdomain name; IPv6 addressing was never taught.

Added four new §3 subsections:
- **Addresses: IPv4, IPv6, and subnetting.** CIDR `/N` reading (RFC 4632 §3.1: `/24` = first 24 bits network, 8 host, 256 addresses), subnetting as prefix-lengthening (`/24` → two `/25`s), the three RFC 1918 private ranges + `127.0.0.0/8`, and the "private or public first" log-reading rule.
- **IPv6 reading.** 128-bit hex-group form, RFC 5952 §4 compression rules (drop leading zeros; `::` = *longest* zero-run, once per address, never a single group; lowercase), and front-of-address literacy: `::1` loopback, `::` no-address, `fe80::/10` link-local (mandatory per RFC 4291 §2.8), `ff00::/8` multicast (no broadcast in IPv6), `2000::/3` global unicast, `fc00::/7` ULA (RFC 4193) — with the dual-stack firewall-blindness warning.
- **DHCP: DORA.** Discover/Offer/Request/ACK (RFC 2131 §3.1) with the attacker's leverage point: whoever answers DHCP picks the client's gateway and DNS. Rogue DHCP: attack (ATT&CK T1557.003), detection (unexpected server identifier in logs, clients on a foreign gateway), fix (DHCP snooping / knowing which server should answer).
- **Routing + middleboxes.** Default route, longest-prefix match, gateway-as-MITM position; stateful vs stateless firewall (why SSH-out works through a firewall that blocks inbound 22), VPN as trust-*shifting* (not trust-*creating*) with split tunneling, forward vs reverse proxy (and SSRF foreshadow), VLAN as 802.1Q segmentation-not-encryption with VLAN-hopping attack and switch-hygiene fix.

Also: new §4 **step 9 (RUN)** — `ip route` + `ip -br addr`, classify every address, transcript appended to `runs/a-tcpip-ports.log` (re-run showed `default via 198.19.0.1 dev host0`, `198.19.0.2/30`, `::1/128`, an `fd8b:…/64` ULA, `fe80::/64`); §6 two new bullets (IPv6 blindness, rogue DHCP); §7 five new RFC entries (1918, 4632, 5952, 4291, 2131).

### a-http-depth — fired. Three §5 sub-items missing.

The §5 HTTP bullet demands "auth schemes (Basic, Bearer, JWT structure, OAuth 2.0 and OIDC flows), TLS handshake step by step." JWT structure existed; everything else was absent or a one-paragraph skim.

- **Auth schemes section** (§3, new): Basic per RFC 7617 (base64 `user:password` per request; "not a secure method… unless used with TLS"; attack = wire/log theft, fix = TLS or don't use it), Bearer (anyone-holding-it-is-authorized; stateless but every leak is total compromise), OAuth 2.0 authorization-code flow's four moves (request → code → back-channel token exchange → token; RFC 6749 §4.1) with PKCE, `state`, redirect-URI registration as the three trust anchors, and the OAuth2=authorization / OIDC=authentication distinction (OIDC = OAuth2 + `id_token` JWT with `iss/sub/aud/exp/iat`; OAuth2 alone "incapable of providing information about the authentication of an End-User" per OIDC Core 1.0).
- **TLS handshake step-by-step** (§3, expanded): six numbered messages — ClientHello (key shares = one-round-trip trick), ServerHello, EncryptedExtensions, Certificate, CertificateVerify (transcript signature = the authentication step), Finished ×2 — each matched to RFC 8446 §4 sections. New §4 **step 12 (RUN)**: `openssl s_client -connect 127.0.0.1:8443 -trace`, find all six messages in order; transcript in `runs/a-http-depth.log` (captured ClientHello 284B → ServerHello 118B → EncryptedExtensions → Certificate 790B → CertificateVerify 260B → Finished ×2, `TLS_AES_256_GCM_SHA384`, X25519).
- New §4 **step 11 (RUN)**: Basic-auth demo — `printf 'alice:wonderland' | base64` ↔ decode, seeing `YWxpY2U6d29uZGVybGFuZA==` become credentials by hand.

### a-linux-cli — fired. "Memory" was named in §5 but never taught.

The §5 OS/Linux bullet demands "processes and **memory**". Grep for RSS/VSZ/swap/OOM/`maps`: zero hits across the lesson. Added §3 **"Memory: what a process is actually holding"**: VSZ (address space reserved) vs RSS (physically resident — the number that matters for "who's eating my RAM"), `/proc/<pid>/status` (`VmSize` = total program size, `VmRSS` = resident; per kernel docs), `/proc/<pid>/maps` (mappings to executables and libraries), swap (`kswapd` paging, thrashing), OOM killer (sacrifices the fattest process when RAM + swap are exhausted), and core dumps as a security fact (dumps contain whatever was in memory — crash a credential-handling process and the dump *is* the leak). New §4 **step 10 (RUN)**: `free -h`, `ps -o pid,rss,vsz,comm`, `/proc/1/status` VmRSS/VmSize; transcript in `runs/a-linux-cli.log`.

### No fire: a-crypto, a-dns-depth, a-python-security, a-reading-code.

- **a-crypto**: all six §5 sub-items present, each misuse-pair explicit (ECB shows the pattern; key-reuse kills one-time pads and nonces; `Math.random()` tokens; unsigned "signature" fields; self-signed-without-pinning; "never roll your own" present).
- **a-dns-depth**: the §5 bullet for this lesson is only "how DNS resolves a name" — fully taught (recursive vs iterative, glue, TTL, caching).
- **a-python-security**: "HTTP requests, parsing responses, sockets, arguments and files" — all four in §4/§5 with walkthrough coverage.
- **a-reading-code**: "enough JavaScript to read client-side behavior; enough SQL to see how a query is built and where user input enters" — both present (DOM sink/source walkthrough, query-builder dissection).

---

## Lens 2 — Prerequisite chain integrity (chains broken, fixes)

1. **Cycle broken: a-linux-cli → a-tcpip-ports → a-dns-depth → a-linux-cli.** The cli lesson's frontmatter listed `a-tcpip-ports` as a prerequisite; tcpip lists `a-dns-depth`; dns lists `a-linux-cli`. A true cycle. Fix: removed `a-tcpip-ports` from a-linux-cli's prereqs (now `[]` — the CLI teaches nothing that needs TCP/IP, and it is the root of the whole graph). Every other lesson lists cli as prereq, so the root is sound. Also corrected the fallout: a-linux-cli §1 ("were shell sessions" → "are shell sessions too — this lesson is the fluency they assume"), §6's `ss -tlnp` usage → forward pointer ("`a-tcpip-ports` dissects these states"), and a-tcpip-ports §10's stale "leads to a-linux-cli — next" → prerequisite framing.
2. **a-reading-code listed `b-sqli` as a prerequisite** — a Stage B lesson required *before* a Stage A lesson that teaches the injection mechanism itself. Fix: prereqs are now `[a-http-depth, a-python-security]`; b-sqli stays where it belongs, as a "Leads to." Verified nothing strands: b-sqli's own prereqs (`[a-http-depth, a-git-github]`) don't include a-reading-code.
3. **a-osint-research listed `b-authorization-scope` as a prerequisite** while its own §10 *also* listed b-authorization-scope as a "leads to" — the lesson both required and deferred the authorization rule. Fix: prereqs → `[a-http-depth]`; §2 now states the rule up front ("testing outside written authorization is a crime… a name found is not permission") and §10 keeps the pointer as leads-to. The authorization boundary is now taught inline rather than borrowed from a later lesson.
4. **a-http-depth listed no prerequisites but §2 assumed shell fluency** (cd, curl, pipes). Fix: added `a-linux-cli` to prereqs, plus a §4-step-1 primer ("Reading the server") so the first walkthrough step doesn't strand CLI-fluent-but-new readers. §5's Python server extension was handled the other way: adding `a-python-security` as a prereq would re-create a cycle (python-security lists http-depth), so §5 now carries a "The Python you'll need" copy-adapt primer instead.
5. **a-python-security had a forward reference**: "performs the handshake `a-tcpip-ports` taught you" — but a-tcpip-ports is *not* a prerequisite. Fix: the lesson now teaches the 3-packet shape inline and points to a-tcpip-ports for the full dissection, instead of assuming knowledge it doesn't require.
6. **Orphan assumption (gap section, not fixable in-lesson)**: a-dns-depth names DNS-over-TLS / DNS-over-HTTPS as the fix for passive DNS eavesdropping, deferring to "a different lesson" — but **no lesson in the guidebook teaches DoT/DoH** (e-secure-channels has zero mentions). The pointer was rewritten so it doesn't promise a lesson that doesn't exist; Stage E or a crypto revision should claim the topic.

No other broken chains: a-crypto's `[a-linux-cli, a-http-depth]` is loose but acyclic and honest; a-git-github, a-windows-concepts prereqs are clean.

---

## Lens 3 — Exercise quality (rewrites, counts kept)

Every "Check yourself" section was audited for recall questions; every "On your own" for vague success tests; every "Prove it" for walkthrough-replay artifacts.

### Before/after — the worst offender (a-dns-depth §8 Q1, pure recall):

> **Before:** *"List every server involved in resolving `shop.example.com`, in order."*
> **After:** *"Your stub resolver asks for `shop.example.com` and gets an answer in 4ms. Explain which servers were actually contacted and why it was that fast — then predict what changes, server by server, when the same query runs against a completely cold cache, and what each server returns at each step (referral or answer)."*

The before rewarded reciting a list; the after forces the reader to reconcile a timing observation with the resolution model, then predict the cold-cache sequence server by server — explain and predict, never recall.

### Other rewrites:

- **a-http-depth §8 Q1** — before: *"Name the two mechanisms HTTP uses to keep state across requests."* → after: a shopping cart surviving page loads — *"Explain where the 'memory' actually lives in each of the two session designs from this lesson, predict what breaks for each one if the server's session store is wiped, and explain why the other design is unaffected."*
- **a-python-security §8 Q2** — before: *"Name the two things you check before trusting the output of urlopen."* → after: *"Your script prints `bytes: 11` for a page you expected to be JSON. Explain what could produce that output, how you'd confirm which cause it is, and why calling `json.loads` blindly is the wrong next step."*
- **a-reading-code §8 Q1** — before: *"What single character breaks out of the string literal in the vulnerable login query?"* → after: *"An attacker submits `admin'-- ` as the username to the walkthrough's vulnerable builder. Mark the exact character where the input stops being data and becomes structure, and explain what the database now *does* with the rest of the query that the author didn't intend."*
- **a-reading-code §8 Q3** — before: *"Name two ways an ORM can still be vulnerable to injection."* → after: teammate says "the ORM handles it" next to `db.execute("SELECT * FROM users ORDER BY " + sort_param)` — explain why ORM protection doesn't cover that line, and name one other ORM escape hatch to grep for.
- **a-osint-research §8 Q4** — before: *"Name three things a job posting can reveal about a target's infrastructure."* → after: a real posting ("migrating our on-prem Exchange to M365 and hiring a Splunk admin") — extract three facts, state what passive inference each supports, whether acting on it needs authorization, and why the authorization answer is source-independent.
- **a-windows-concepts §8 Q2** — before: *"Name the three facts you'd gather about a suspicious service."* → after: a LocalSystem + Automatic service with an executable in `C:\Users\Public\` — ordered investigation walk-through, what each check tells you, and the exact evidence threshold for escalating "unusual" to "likely malicious."
- **a-tcpip-ports §8 Q2** — rewritten to an explain/predict form consistent with the above.
- **a-linux-cli §5(a)** — *"prove you can read `secret.txt` but another local user cannot — or reason it out"* was weakened by "or reason it out" (no check). Now: `sudo -u nobody cat ~/clilab/secret.txt` (the `nobody` account exists on every Linux — no second account needed), show `Permission denied` vs your own success, and name which triple the kernel evaluated for each.
- **a-crypto §9** — the artifact was §5 replay ("extend the walkthrough's hash demo"). Now requires a **fourth paragraph of unaided application** to a system the reader actually uses (password manager, bank login, own lab server): name the primitive, the promise, the misuse (or a defended "correctly constructed because…"), and the evidence.
- **a-tcpip-ports §9** — artifact now demands the reader's own address plan: classify every address on their machine (IPv4/IPv6; loopback, link-local, private, global) and state the default route in words — a stranger should draw the machine's network position from the notebook.
- **a-http-depth §9** — artifact was a worked-example replay; now centers the reader's own `/profile` build plus one design-decision write-up ("why your four 401 responses are indistinguishable, and what you changed to make them so").

Reviewed and solid already, no changes: a-git-github's full exercise chain (explain/predict questions, verifiable success test, genuine artifact), a-osint-research §5/§9, a-dns-depth §5/§9, a-python-security §5/§9, a-reading-code §5/§9, a-windows-concepts §5/§9.

### Also fixed while in there:

- a-linux-cli §9 "Can't claim yet" was **stale**: it described package management and services as topics of "a later Stage A lesson" — but this lesson has taught them since 2026-10-10 (pass 1). Corrected to the real remaining gaps.

---

## Verification summary (all done in-session 2026-10-10, loopback only)

- **New walkthrough steps RUN**, transcripts appended: `runs/a-tcpip-ports.log` (step 9: `default via 198.19.0.1 dev host0`, `198.19.0.2/30`, `::1/128`, `fd8b:…/64` ULA, `fe80::/64`); `runs/a-linux-cli.log` (step 10: `free -h`, `ps -o pid,rss,vsz,comm`, `/proc/1/status` VmRSS/VmSize); `runs/a-http-depth.log` (step 11: `alice:wonderland` ↔ `YWxpY2U6d29uZGVybGFuZA==`; step 12: full `-trace` capture of the six handshake messages).
- **Primary sources fetched and verified**, rows written to `reports/sources-add-3-A.csv` (12 rows, all `status=verified`, `fetch_date=2026-10-10`; `sources.csv` untouched for coordinator merge): RFC 1918 §3, RFC 4632 §3.1, RFC 5952 §4, RFC 4291 §§2.4–2.5/2.8, RFC 4193 §3.1, RFC 2131 §3.1 (via RFC 4039 §3.1's verbatim quotation), ATT&CK T1557.003, RFC 7617, RFC 6749 §4.1, OIDC Core 1.0, RFC 8446 §4, kernel proc docs.
- **Post-pass citation correction:** a-tcpip-ports' ULA line was tightened after verification — ULA (`fc00::/7`) is RFC 4193, not RFC 4291; the lesson now cites correctly, and the link-local claim is pinned to RFC 4291 §2.8 with IPv6's no-broadcast rule stated.
- **File validation:** all 10 files = exactly ten `## ` sections; frontmatter intact (`lesson_id, slug, stage, level, prerequisites, roles, map_refs, test_date, description, dateline`); zero banned words; the only `$<digit>` match is the pre-existing `awk '{print $7}'` field reference, not currency.
- **Prereq graph:** all 10 prerequisites lists are Stage-A-only and acyclic (cli is root; no forward references remain).
- **Test servers:** killed by explicit PID during each run; `pgrep` sweep verified clean. **Footgun recorded:** `pkill -f tls_srv.py` matched the exec wrapper's own command line and killed my shell — use the bracket trick `pgrep -f "[t]ls_srv\.py"` for self-safe matching.
- **No commits, no pushes.** `git status` shows the 9 edited lessons + 2 report files as uncommitted working-tree changes, as required.

## Gap for the coordinator

- **DoT/DoH has no home**: a-dns-depth prescribes DNS-over-TLS / DNS-over-HTTPS as the fix, but no lesson teaches either. Candidate owners: a-crypto (a "protocols that encrypt metadata" subsection) or a new Stage E micro-lesson. Currently the dns pointer is de-promised rather than resolved.
