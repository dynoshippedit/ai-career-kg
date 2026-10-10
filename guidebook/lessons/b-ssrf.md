---
lesson_id: b-ssrf
slug: ssrf
stage: B
level: 3
prerequisites: [a-http-depth, b-idor]
roles: [pentester, appsec, cloud-security]
map_refs: []
test_date: 2026-10-09
description: "SSRF: when the server fetches what you tell it to — loopback, cloud-metadata angle, filter bypasses and the allow-list fix. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · local demo app; metadata tree is a labeled loopback simulation"
---
# SSRF: when the server fetches what you tell it to


**Map refs:** OWASP Top 10:2025 A01 (SSRF folded into Broken Access Control) · WSTG-INPV-19 · CWE-918

---

## 1. Where this shows up

Server-side request forgery is the vulnerability where the *attacker* doesn't make the request — the **server** does, on the attacker's behalf, to a destination the attacker chose. It sits in **OWASP Top 10:2025 A01** (the 2025 edition folds SSRF into Broken Access Control — the category is "the server does something for you that it shouldn't") and carries **CWE-918**. You will meet it in any feature that fetches a URL: webhooks, file-import-by-URL, image proxies, PDF generators, "check stock" APIs, OAuth `redirect_uri` handling. And on cloud-hosted targets it has a famous impact multiplier: the cloud **instance metadata service**, which hands out credentials to whoever can reach it — and the vulnerable server can always reach it.

## 2. Before you start

- You can read HTTP requests and responses cold (`a-http-depth`), including redirects and URL structure (userinfo, fragments, encoding).
- You understand the IDOR lesson's core pattern — the server trusting client-supplied input — because SSRF is that pattern aimed at the network instead of the database.
- Your target is written down and authorizes your testing: your own local lab (this lesson's demo app), a PortSwigger Academy SSRF lab, or a bounty program whose scope explicitly includes the asset. On cloud-hosted targets, the metadata endpoint is in scope only if the program says so — assume it doesn't until written down. Re-read B-AUTH if this sentence surprised you.
- Tooling: curl is enough. For blind cases, an OAST/collaborator domain you control.

## 3. How it works

A normal request goes from your browser to the server. In SSRF, the server itself becomes the requester: it takes a URL (or part of one) from your input and fetches it. The vulnerable shape:

```
stockApi = request.form["stockApi"]        # attacker-controlled
response = http.get(stockApi)              # the SERVER fetches it
return response.text
```

The developer built a feature that needs to fetch a back-end URL. The mistake is letting the user choose *which* URL. Your browser can't reach the internal admin panel at `http://127.0.0.1:8080/admin` — but the server can, because the server *is* at 127.0.0.1. So you hand the server `stockApi=http://localhost/admin`, and the server fetches its own admin page and returns it to you. The trust relationship being abused is the network's: internal services that never authenticate loopback requests because "only the server would ask."

**Why it arises in real code.** Every feature that fetches: webhooks (user registers a callback URL), import-by-URL, URL preview cards, document converters, "check availability" APIs that take a `stockApi`-style parameter, analytics that visit Referer URLs, XML parsers that resolve external entities (XXE's cousin). The developer tested the happy path — the feature fetching its intended URL — and never asked "what if the URL is the attacker's?"

**The cloud metadata angle.** Cloud instances expose a metadata service at a well-known link-local address (`169.254.169.254` on AWS and Azure; `metadata.google.internal` on GCP) that returns information about the instance — including, on some paths, **temporary IAM credentials** for the instance's role. These endpoints are reachable from the instance itself, which means they're reachable from any SSRF on that instance. AWS's IMDSv2 requires a PUT-issued session token, and GCP/Azure require a special header — but a header requirement stops only the simplest SSRF; if the vulnerable fetcher forwards headers, the attacker supplies them. The lesson: metadata endpoints turn "the server fetched a URL" into "the attacker holds cloud credentials." Defense in depth runs infrastructure-side (enforce IMDSv2, deny egress to the metadata range from workloads that don't need it) *and* application-side (the fix below).

**Why denylists fail — the checkpoint version.** The instinct is to block `127.0.0.1`, `localhost`, `/admin`. Every one of these has a bypass, and the bypasses are the reason the fix must be an allow-list on the *canonicalized* URL:

- **Alternate IP representations:** `2130706433`, `017700000001`, `127.1` — all route to loopback; a string denylist sees none of them.
- **DNS rebinding:** an attacker domain that resolves to 127.0.0.1 — the validator sees a public name, the fetcher resolves the private IP.
- **URL parser tricks:** `https://expected-host@evil-host` (everything before `@` is userinfo — the real host is `evil-host`); `https://evil-host#expected-host` (the fragment is never sent — the real host is `evil-host`); `expected-host.evil-host` (subdomain shadowing); double-encoding that the validator decodes once and the fetcher decodes twice.
- **Open-redirect chains:** the validator approves an allowed domain; the allowed domain redirects to the internal target; the fetcher follows the redirect without re-validating.

The checkpoint rule: validate the **resolved, canonicalized URL after following redirects**, against an **allow-list**, with no userinfo, no fragments, and every resolved IP checked against the deny ranges (127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16). Anything less is a bypass waiting to happen.

**How defenders see it.** Egress logs are the highest-value signal: outbound connections **from application servers** to `169.254.169.254`, metadata hostnames, or internal RFC-1918 ranges the app never legitimately contacts. The rule writes itself: alert on any app-tier host initiating connections to link-local metadata IPs. In application logs: `stockApi`/webhook parameters containing unexpected hosts, `@` or `#` in URL parameters, redirect chains in fetch logs. WAF coverage for SSRF is thin — treat URL-parameter tripwires as tripwires, not barriers.

### Worked example: the stock-check demo

A minimal shop app (stdlib Python, local only — the walkthrough runs it). `POST /product/stock` with `stockApi=<url>` fetches the URL server-side and returns the result. A second, "internal" server on another loopback port serves `/admin` ("internal admin panel — no auth for loopback") and a fake metadata tree at `/latest/meta-data/` (standing in for the cloud metadata service; labeled as a simulation in the companion).

Baseline: `stockApi=http://127.0.0.1:<PUBLIC>/products/1/stock` returns stock data. Probe: `stockApi=http://127.0.0.1:<INTERNAL>/admin` — the response contains the internal admin page. That page in your response *is* the vulnerability: the server fetched a destination you chose and it trusted. Metadata angle: `stockApi=http://127.0.0.1:<INTERNAL>/latest/meta-data/iam/security-credentials/role` — the response contains simulated temporary credentials. Read the role *name* and stop; even in a lab you own, the discipline is to prove the channel, not to exfiltrate.

The fix, in the same app: replace the open fetcher with an allow-list — the `stockApi` value must be one of the known back-end endpoints, mapped server-side from an identifier; the fetcher disables redirects, strips userinfo and fragments, resolves the host, and denies private/loopback/link-local ranges. Re-test: the admin URL → rejected; the metadata URL → rejected; the legitimate stock endpoint → still works. Then the infrastructure note: on real cloud targets, enforce IMDSv2 / header-required metadata and deny metadata-range egress from app workloads regardless of application fixes — because the next SSRF won't ask permission.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-ssrf.log`. Clean environment: stock Python 3.12, curl 8.5.0, loopback only, 2026-10-09. The demo app stands in for the PortSwigger targets the reader uses (no Docker on this machine — see gaps).

1. **Start the two servers.** Save the `app.py` from this lesson's companion (public app on port 8325 with `POST /product/stock`; internal server on port 8326 with `/admin` and the simulated `/latest/meta-data/` tree) and run both. Confirm the baseline: `curl -d 'stockApi=http://127.0.0.1:8325/products/1/stock' localhost:8325/product/stock` returns stock data.
2. **SSRF against loopback.** `curl -d 'stockApi=http://127.0.0.1:8326/admin' localhost:8325/product/stock` — observe the internal admin page in the response. Write down, verbatim, the request and the response — this pair is the finding.
3. **SSRF against the metadata simulation.** `curl -d 'stockApi=http://127.0.0.1:8326/latest/meta-data/iam/security-credentials/' localhost:8325/product/stock` — observe the role name returned. Read the name; do not request the credentials themselves. The channel is proven.
4. **Try a denylist bypass — at the validator layer.** A naive denylist checks the *string* (`"127.0.0.1" not in url`); the network stack *resolves* the name. Run the transcript's Python snippet: `http://2130706433:8326/admin`, `http://127.1:8326/admin`, and `http://0x7f.0.0.1:8326/admin` all pass the string check, and `getaddrinfo` resolves every one of them to 127.0.0.1. (Python's urllib normalizes some of these forms, so the demo fetches the canonical address; curl, Java, and browsers follow the alternates to loopback. The bypass class lives in the *validator*, not the fetcher.) Write that sentence in your notes.
5. **Apply the fix.** Patch the fetcher: identifier→allow-listed-endpoint mapping, redirects disabled, userinfo/fragments stripped, resolved IP checked against deny ranges. Restart the app.
6. **Verify the fix — four cases.** `127.0.0.1:8326/admin` → rejected; `2130706433:8326/admin` → rejected; the metadata URL → rejected; the legitimate stock endpoint → still returns stock data (a fix that breaks the app is not a fix).
7. **Read the defender view.** Open the app's fetch log: find your requests to the internal port and the metadata path. Write the detection rule: alert on any outbound fetch from the app process to 127.0.0.0/8, RFC-1918, or 169.254.0.0/16 — destinations the app never legitimately contacts.

No step above is marked "not run by us" — loopback SSRF, the metadata simulation, the denylist-bypass demonstration, the fix, and all four verification cases ran locally. Real cloud metadata endpoints were not touched (the simulation stands in; see gaps).

## 5. On your own

**Task:** Pick one authorized target you have not touched in this lesson — a PortSwigger Academy SSRF lab (the "basic SSRF against the local server" lab is the closest match). Find the URL-bearing parameter using normal traffic inspection (look for full or partial URLs in requests). Confirm the server fetches your value with a collaborator/OAST domain first (blind-safe), then escalate to loopback. Then test one denylist bypass from section 3 against the lab's filter, if it has one.

**Success test:** A one-page report: the URL-bearing parameter, the collaborator confirmation, the loopback evidence (exact requests), the bypass result (worked/blocked, with the mechanism), the fix (allow-list + canonicalized validation + egress controls, stated as code-level and infrastructure-level remediation), and the defender detection (which log, which destinations). If the lab's filter blocks your bypass, document the filter's behavior — a characterized defense is a result.

## 6. Where it goes wrong

- **Denylisting `127.0.0.1` and calling it done.** Decimal octets, DNS rebinding, `@`/`#` tricks, open-redirect chains — the bypass list is longer than the block list. Canonicalize, resolve, then allow-list.
- **Validating before the redirect.** The filter approves the allowed domain; the fetcher follows the redirect to the internal target without re-validating. Validate after every hop, or disable redirects.
- **Forgetting partial URLs.** The parameter holds only a hostname or path, which the server completes — limited but not eliminated impact. Test what the server *assembles*, not just what you *send*.
- **"The metadata needs a header, so we're safe."** Header requirements stop only SSRFs that can't set headers. If the fetcher forwards attacker headers, the requirement is theater. Enforce IMDSv2 and egress denies at the infrastructure level.
- **Exfiltrating in the lab.** Reading the role name proves the channel. Pulling full credentials — even on infrastructure you own — builds a habit that will end a career on someone else's. Prove the channel, then stop.
- **WAF as the fix.** SSRF-specific WAF coverage is thin and bypassable. The fix is in the fetcher and the network, not the filter.

## 7. Read the source

Primary documents first:

- **PortSwigger Web Security Academy — SSRF** (portswigger.net/web-security/ssrf) — *read* fully; the canonical treatment (loopback attacks, back-end systems, blacklist/whitelist bypasses, open-redirect bypass, blind SSRF). *Do* the labs after this lesson.
- **CWE-918** (cwe.mitre.org/data/definitions/918.html) — *skim* the definition; cite the ID in findings.
- **Your cloud provider's metadata docs** (docs.aws.amazon.com for IMDSv2, cloud.google.com for the metadata server, learn.microsoft.com for Azure IMDS) — *read* the authentication requirements for the one you use; *note* what each requires and what that stops.

Then at most three free resources:

1. **PortSwigger Academy — SSRF labs** (portswigger.net/web-security) — free, hosted, authorized; basic, blind, and filter-bypass labs.
2. **OWASP SSRF Prevention Cheat Sheet** (cheatsheetseries.owasp.org) — free; the fix side: allow-lists, canonicalization, egress controls.
3. **HackerOne Hacktivity — disclosed SSRF reports** (hackerone.com/hacktivity) — free; read two disclosed reports to see how real findings chain SSRF to impact.

## 8. Check yourself

1. Explain why `https://expected-host@evil-host/path` fetches from `evil-host` and not `expected-host`, and which part of the URL the naive validator looked at.
2. A fetcher validates the URL against an allow-list, then follows redirects without re-validating. Explain how an open redirect on an allowed domain defeats this, and state the fix.
3. Predict what a defender sees in egress firewall logs during active SSRF probing of a cloud-hosted app, and explain why that signal is higher-value than any WAF rule for this class.
4. The metadata service requires a special header. Explain why this stops a naive SSRF but not one where the vulnerable fetcher forwards attacker-controlled headers.
5. You prove SSRF to a loopback admin panel on an authorized target. Explain what you put in the impact section, and why you stop at reading the role name on the metadata path.

## 9. Prove it

**Artifact:** the one-page report from "On your own": the URL-bearing parameter, collaborator confirmation, loopback evidence, bypass characterization, code-level + infrastructure-level fix, defender detection.

**Honest claim:** "I can find SSRF in URL-fetching features, prove it against loopback and metadata-shaped endpoints, characterize filter bypasses, and verify the allow-list/canonicalization fix."
**Can't claim yet:** "I can assess SSRF on live cloud infrastructure" — real metadata endpoints and real egress controls are practiced in authorized bounty scope, not claimed from this lesson.

## 10. Leads to

- `b-csrf` — the browser makes the request instead of the server; compare which party's trust each class abuses.
- B-VULN second wave: XXE — the same server-fetches-attacker-URL shape through XML parsers.
- B-DEF (defensive basics) — sit on the other side: write the egress alert for your own attack traffic.
- Map refs: **OWASP Top 10:2025 A01**, **WSTG-INPV-19**, **CWE-918**.
