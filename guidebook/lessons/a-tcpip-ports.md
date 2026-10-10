# TCP/IP and ports

**ID:** `a-tcpip-ports` · **Stage:** A (Foundations) · **Level:** 3 (mechanism — you can explain the handshake, read connection states, and say what a port is without hand-waving) · **Prerequisites:** `a-dns-depth` (names resolve to addresses; this lesson moves bytes to those addresses).

**Map refs:** Pre-map foundations; feeds `a-http-depth`, Stage B (every vulnerability lesson opens connections), Stage D (network forensics reads these states).

---

## 1. Where this shows up

Every connection you will ever investigate or exploit is TCP (or UDP) to an IP address and a port. The SOC analyst triaging "suspicious outbound connection" is reading exactly the states this lesson teaches: who connected to whom, on what port, and whether the handshake completed. The penetration tester whose scan shows "port 8080 open" is reading a completed handshake. The incident responder deciding whether data left the network is asking whether a connection was ever ESTABLISHED. Ports are also the first access-control boundary you will meet — a firewall is, at its simplest, a list of which ports may complete handshakes. Learn what a port really is now, and "open port," "listening service," and "connection" stop being vocabulary and become things you can observe.

## 2. Before you start

- A terminal with `python3` and `ss` (verify: `ss --version`). The walkthrough's listener is a ~15-line Python server on `127.0.0.1`.
- `a-dns-depth` done — you know how a name becomes an address; the address is where this lesson starts.
- No packet capture on the build machine: the tcpdump/Wireshark step is marked not-run and given as the reader's exercise.

## 3. How it works

Two machines, one problem: deliver a stream of bytes, in order, without loss, over a network that drops, duplicates, and reorders packets. TCP's answer has three parts — the handshake, the stream, and the port numbers that make it all addressable.

**A port is an address within a host.** An IP address gets the packet to the right machine; the port gets it to the right *conversation* on that machine. The pair (IP, port) on each end — the **socket pair**, four numbers total — identifies one connection uniquely, which is why one web server can hold ten thousand simultaneous connections on port 443: the clients' ephemeral ports differ. Ports are 16-bit numbers. Below 1024 are the **privileged** (well-known) ports — binding them requires privilege, a relic of the era when port numbers authenticated the *sender* (only root could bind below 1024, so a connection *from* a low port meant "this came from a privileged process"). Above that: registered ports (1024–49151, convention, e.g. 8080, 8443) and the **ephemeral** range (the kernel picks these for outgoing connections — `32768–60999` on the walkthrough machine). The `/etc/services` registry maps numbers to names, but it is convention, not enforcement: anything may listen on any unprivileged port, and malware counts on you assuming otherwise.

**The three-way handshake** exists because both sides must agree on where the byte stream starts. A opens with **SYN** ("I want to talk; my sequence starts at X"). B replies **SYN-ACK** ("agreed; my sequence starts at Y; I acknowledge your X"). A sends **ACK** ("I acknowledge your Y"). Only then is the connection **ESTABLISHED** and application data flows. Two details with security weight. First, sequence numbers are randomized per connection (RFC 9293) — predictable sequence numbers were the 1990s' remote-hijacking primitive (the Mitnick/Shimomura attack), and the fix was cryptographic randomness in the initial sequence number. Second, a SYN to a closed port gets a **RST** (reset), not silence — and that difference is the entire basis of port scanning: SYN-scan sends SYNs and reads RST-vs-SYN-ACK as closed-vs-open, never completing the handshake.

**The stream** is TCP's promise: bytes arrive in order, without gaps or duplicates, or the connection tells you it failed. Sequence and acknowledgment numbers track every byte; lost segments are retransmitted; the receiver's **window** advertises how much it can accept (flow control). For security work, the stream abstraction is what lets every higher protocol — TLS, HTTP, SSH — pretend the network is a reliable pipe. When that pretense breaks (RST injection, sequence prediction), the pipe itself is the attack surface.

**Closing is a negotiation**, not an event. Each side sends **FIN** ("I'm done sending") and the other ACKs it; the connection is fully closed only after both FINs. A side that FINs first and sees the full exchange parks in **TIME_WAIT** so late duplicate packets can't corrupt the *next* connection reusing the port — which is why a restarted server can briefly report "address already in use" (SO_REUSEADDR exists for exactly this). The half-close states in the walkthrough (FIN-WAIT-2, CLOSE-WAIT) are what you see when one side said goodbye and the other hasn't answered yet.

**UDP** is the deliberate absence of all this: no handshake, no sequence numbers, no connection — just addressed datagrams. DNS uses UDP first (fast, one question one answer) with TCP fallback. The price of no handshake is no authenticity, which is why `a-dns-depth`'s poisoning discussion lives where it does.

Above TCP sits IP (RFC 791 for v4, RFC 8200 for v6): the header carries source and destination addresses, and TCP's checksum even covers a **pseudo-header** of IP fields so a misrouted segment fails validation. One IP mechanic you will trip over constantly: **NAT** (network address translation). Your home router gives your machine a private address (192.168.x.x, 10.x.x.x) and rewrites it to the router's public address on the way out, tracking the mapping by port. Inbound SYNs to your machine die at the router unless port-forwarded — which is why your walkthrough listener is reachable on loopback but not from the internet, and why "the server can't reach my lab" is almost always NAT, not a firewall rule you wrote. The layering is the point of the whole stage: IP gets it to the host, TCP gets it to the conversation, and the application protocol — next lesson — decides what the conversation means.

### Worked example: one connection, observed three ways

From the walkthrough (§4): a Python server listens on `127.0.0.1:18443`. `ss -tln` shows it in LISTEN — the kernel, not the application, is now answering SYNs. A client connects; `ss -tn` shows two ESTABLISHED rows: `127.0.0.1:37494 → 127.0.0.1:18443` (client, ephemeral port from the kernel's range) and the mirror (server side, on 18443). The handshake completed inside `create_connection()`, before any application byte moved. Binding 18443 a second time fails with `EADDRINUSE` — one owner per port. Binding port 80 as the unprivileged `nobody` user fails with `Permission denied` — the privileged-port rule, demonstrated rather than asserted. The client closes; the server holds; `ss` shows FIN-WAIT-2/CLOSE-WAIT — the half-close. Both close; the first closer lands in TIME-WAIT for 60 seconds. Every state has a name, every name was observed, and a packet capture (your exercise, step 8) would show you the SYN/SYN-ACK/ACK/FIN segments behind each one.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/a-tcpip-ports.log`. Clean environment: stock Python 3.12, `ss` (iproute2 6.1.0), loopback only, 2026-10-09. One step marked not-run (UDP datagrams — sandbox blocks UDP loopback). Packet capture re-ran 2026-10-10 with real tcpdump (see step 8).

1. **Open a listener and see LISTEN.** Start the background Python server on `127.0.0.1:18443`; `ss -tln | grep 18443`. The kernel holds the port now — SYNs get SYN-ACKs before your code runs.
2. **Connect and see ESTABLISHED.** Connect with Python, hold the socket; `ss -tn | grep 18443` shows both directions. Name the ephemeral port and say which range it came from.
3. **Bind it twice.** A second `bind()` on 18443 → `OSError: [Errno 98] Address already in use`. One owner per address+port.
4. **Try a privileged port without privilege.** `setpriv --reuid=nobody ... bind(('127.0.0.1',80))` → `Permission denied`. Read `/proc/sys/net/ipv4/ip_local_port_range` and match step 2's ephemeral port to the range.
5. **UDP — not run by us.** Sandbox blocks UDP loopback. On your machine, run the two one-liners in the log: a UDP server printing `recvfrom`, a client `sendto`-ing one datagram. Note there is nothing to `ss` for: no handshake, no ESTABLISHED.
6. **Close and watch the states.** Client closes while the server holds: FIN-WAIT-2/CLOSE-WAIT — the half-close, named. Then the both-close demo: the first closer sits in TIME-WAIT (`ss -tna`), 60s on this machine. Explain what TIME_WAIT protects against.
7. **Read the registry.** `grep -E '^(http|https|domain|ssh)[[:space:]]' /etc/services` — convention, not enforcement.
8. **Capture it.** **Update 2026-10-10: now RUN BY US** — tcpdump 4.99.4 installed (via .deb; this container has no `tcpdump` user so capture needs `-Z root`). `tcpdump -Z root -i lo -n 'tcp port 18445'` during a loopback connect showed the full exchange on the wire: `[S]` SYN, `[S.]` SYN-ACK, `[.]` ACK, `[P.]` data each way, `[F.]` FIN each way with final ACKs — 10 packets. See `runs/a-tcpip-ports.log` re-run entry. On your machine: `sudo tcpdump -i lo -n 'tcp port 18443'` while repeating step 2. Match each packet (SYN, SYN-ACK, ACK, FIN) to the `ss` states above.

## 5. On your own

**Task:** Write a minimal port scanner in Python (stdlib only): for ports 1–1024 on `127.0.0.1`, attempt `connect_ex` with a short timeout and report which ports complete the handshake. Run it against your walkthrough listener on 18443 (add that port to the range) and against a port you know is closed.

**Success test:** The scanner reports 18443 as open and the closed port as closed, with no exceptions and a runtime you can explain (hint: why is it slow? what would you change — and what does that change cost in accuracy?).

**Hints:** `connect_ex` returns an errno instead of raising — 0 means the handshake completed. Think about what a RST vs a timeout tells you, and why scanning a *remote* host you don't own would be a different legal universe from scanning loopback.

## 6. Where it goes wrong

- **"Open port" ≠ "vulnerable service."** A completed handshake says a program is listening, nothing more. Scanners report candidates; humans confirm findings. (The brief's hard rule, restated at the transport layer.)
- **Assuming the port number identifies the service.** Anything can listen on 8080; malware does. Banner-grab and fingerprint — never trust the number.
- **Forgetting the ephemeral side.** Incident responders who log only the server port lose the client identity. A connection is four numbers; record all four.
- **TIME_WAIT exhaustion.** A scanner or proxy opening thousands of short connections can fill the ephemeral range with TIME_WAIT sockets — a self-inflicted denial of service with a one-line cause.
- **Half-open confusion.** FIN-WAIT and CLOSE-WAIT in `ss` output are normal mid-close states, not attacks — but a *pile* of CLOSE-WAIT sockets means the application stopped closing connections, which is a bug or a resource-exhaustion attack in progress.
- **UDP's honesty problem.** No handshake means no proof anyone is listening — a UDP "scan" that reports "open" often means "no RST came back," which also means "firewall ate it." Treat UDP results as weaker evidence, always.
- **Scanning outside your scope.** Everything in step 5's "on your own" runs on loopback. Pointing a scanner at someone else's host without written authorization is the CFAA-shaped mistake this program exists to prevent — the authorization lesson (Stage B) gates all of it.

## 7. Read the source

Primary documents first — read with a purpose, skip without guilt:

- **RFC 9293, Transmission Control Protocol** (rfc-editor.org/rfc/rfc9293, obsoletes 793, Aug 2022) — *read* §3.1 (header format — ports, sequence numbers, flags; the diagram is the lesson), §3.4 (sequence numbers), §3.5 (establishing a connection — the handshake, normative), §3.6 (closing); *skim* §3.7–3.8 (segmentation, retransmission — concepts); *skip* §3.9–3.10 (API/event processing — implementer material).
- **RFC 791 (IPv4)** and **RFC 8200 (IPv6)** headers — *read* just the header diagrams (addresses, protocol/next-header fields); the lesson needs the layering, not the full texts.

Then at most three free resources:

1. **Practical Networking** (practicalnetworking.net) — free; the clearest plain-language walkthroughs of the handshake, sequence numbers, and the OSI/TCP-IP model framing. Read the TCP articles after RFC 9293 §3.5.
2. *(Second slot intentionally empty — RFC 9293 plus one guide is the right depth. A Wireshark lab list goes in the directory, not the lesson.)*

## 8. Check yourself

1. `ss -tn` shows `SYN-SENT` for a connection that never becomes ESTABLISHED. Explain what the kernel is waiting for, and name two different reasons it might wait forever.
2. A scanner reports port 8080 "open" on a target. Explain, using the handshake, what the scanner actually observed — and why that observation alone is not a vulnerability.
3. Two connections share server port 443 but have different client ports. Explain why the server can tell them apart, and what would break if the client ports were also identical.
4. After a benchmark, `ss` shows thousands of sockets in TIME_WAIT and new connections fail. Explain the mechanism and two ways to relieve it (one kernel-side, one application-side).
5. A firewall blocks all inbound SYNs to port 22 but the admin can still SSH *out*. Explain what the firewall is distinguishing, using connection states and direction.

## 9. Prove it

**Artifact:** a lab notebook containing: the `ss` outputs from steps 1, 2, and 6 with every column and state explained; the `EADDRINUSE` and `Permission denied` errors with the kernel rule each demonstrates; and your port-scanner script with its open/closed results and your explanation of its speed.

**Honest claim:** "I can read TCP connection states, explain the handshake and teardown packet by packet, and say what a port number does and doesn't guarantee."
**Can't claim yet:** "I can find vulnerabilities in network services" — that is Stage B, on authorized targets; this lesson built the observation skill every such lesson assumes.

## 10. Leads to

- `a-linux-cli` — next: you've seen the wire; now learn to read your own machine's side of it (`ss`, `netstat`'s successor, lives here).
- `a-http-depth` — after the CLI: the handshake gets you a reliable pipe; HTTP is what applications say over it. The Stage A milestone (narrating a login packet by packet) is assessed there.
- `b-idor` and the Stage B vulnerability lessons (later): every one of them opens connections to authorized targets — the states in this lesson are what "the request went through" looks like from below.
