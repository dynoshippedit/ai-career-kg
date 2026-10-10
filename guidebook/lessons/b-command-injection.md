---
lesson_id: b-command-injection
slug: command-injection
stage: B
level: 3
prerequisites: [a-http-depth, a-linux-cli, b-sqli]
roles: [pentester, appsec]
map_refs: []
test_date: 2026-10-09
description: "OS command injection: shell metacharacters, blind time-delay proofs, and why allow-lists beat blocklists — reproduced locally and fixed. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · local demo app (no Docker on the build machine)"
---
# OS command injection: when your input reaches a shell


**Map refs:** OWASP Top 10:2025 A05 Injection · WSTG-INPV-13 · CWE-78

---

## 1. Where this shows up

OS command injection is SQL injection's sibling one layer down: instead of the database executing your input as code, the **operating system** does. It sits inside **OWASP Top 10:2025 A05 — Injection** as **CWE-78**, and its impact is usually worse than SQLi's — a compromised database is bad; a compromised server is the whole machine. You will meet it in legacy integrations (a script shelling out to a reporting binary), in network-device web interfaces, in "convenience" wrappers around system utilities, and — from the other side — in EDR process-creation telemetry, where a web worker spawning a shell is one of the highest-fidelity alerts in the building.

## 2. Before you start

- You can read HTTP requests and responses cold (`a-http-depth`).
- You know what a shell is and what it does with `;`, `&`, `|` (`a-linux-cli`) — this lesson is what happens when a stranger gets to type into one.
- Your target is written down and authorizes your testing: your own local lab (this lesson's demo app), a PortSwigger Academy command-injection lab, DVWA's Command Injection module, or a bounty program whose scope explicitly includes the asset. Never test outside authorization; re-read B-AUTH if this sentence surprised you.
- Tooling: curl is enough. Keep your proofs to `whoami`/`id`/`echo` — the finding is proven the moment injected output renders. Do not pivot, persist, or touch other systems.

## 3. How it works

Some applications call out to the operating system: a diagnostic page that pings a host, a feedback form that invokes the `mail` program, a report generator that shells out to a converter. The dangerous pattern, in Python-flavored pseudocode:

```
os.system("ping -c 1 " + user_input)
```

`os.system` hands the string to a **shell**, and the shell parses the whole thing as a command line. If `user_input` is `127.0.0.1`, the command is what the developer meant. If `user_input` is `127.0.0.1; whoami`, the shell runs `ping -c 1 127.0.0.1`, then runs `whoami`. The input stopped being an argument and became code — the same sentence as SQLi, one layer down. The vulnerability is not the `ping`; it is the shell sitting between the application and the operating system, interpreting metacharacters the developer never intended the user to supply.

**The metacharacter classes, in probe order.** These are what the shell understands, so these are what you test:

- **Command separators (Windows + Unix):** `&`, `&&`, `|`, `||` — chain a new command after the original.
- **Separators (Unix only):** `;`, newline — end the original command entirely.
- **Inline execution (Unix):** backticks and `$(...)` — the injected command runs *inside* the original command's arguments.
- **Quoted contexts:** if your input lands inside quotes in the original command, terminate the quote first (`"` or `'`), then use a separator.

**Blind command injection.** Often the application's response doesn't include the command output — the feedback form sends mail and shows "thanks." The finding is still provable, through side channels: **time delays** (`; sleep 10` — the response takes 10 seconds), **output redirection** (write to a file under the web root, then fetch it), or **out-of-band** (cause a DNS lookup to infrastructure you control and watch for it). A blind injection is a finding, not a failed test — you just need a different channel.

**Why it arises in real code.** Legacy integrations nobody dares rewrite, convenience wrappers ("it's just a ping"), and the false belief that a constrained input can't contain metacharacters. The DVWA case is canonical: an IP address passed to `ping` via `shell_exec()`.

**Why allow-lists beat blocklists.** The instinct is to block the metacharacters — strip `;`, `&`, `|`, backticks. This loses, every time: shells have more metacharacters than you can enumerate (newlines, `$()`, `${IFS}`, encoded forms), and one missed character reopens everything. An **allow-list** inverts the problem: instead of naming what's forbidden (infinite), you name what's permitted (finite) — "this field is an IPv4 address," "this field is one of these five report names" — and reject everything else. You can't bypass a check that never lets your input reach a shell in the first place.

**How defenders see it.** Process-creation telemetry is the crown jewel: Sysmon Event ID 1 on Windows, `auditd` execve on Linux. The hunt is structural — a web-server worker (`w3wp.exe`, `httpd`, `php-fpm`, `node`) as the **parent process** spawning `cmd.exe`, `powershell.exe`, `sh`, or `bash`. A web process has no legitimate reason to spawn shells; that parent-child pair is high-fidelity. Command lines containing separators or `whoami`/`curl`/`wget` from that parent confirm it. WAF coverage exists (ModSecurity CRS 932xxx family, e.g. `REQUEST-932-APPLICATION-ATTACK-RCE.conf`) but it's a tripwire, not a barrier. Application logs show the probing phase: distinctive 500s and timeouts from malformed separator payloads.

### Worked example: the diagnostic demo

A minimal diagnostic app (stdlib Python, local only — the walkthrough runs it). `GET /diag?host=127.0.0.1` builds `ping -c 1 <host>` and runs it **through a shell**, returning the output. The app also simulates a `mail`-style blind endpoint at `/feedback?email=` that invokes a shell command and returns only "thanks."

Baseline: `host=127.0.0.1` returns ping output. Probe: `host=127.0.0.1; echo PROBE-XYZ` — the response contains `PROBE-XYZ`. That string in the output *is* the vulnerability: your input was executed as a shell command. Confirm with `whoami` — the response now tells you which OS user the web app runs as (impact evidence, read-only). Blind channel: `email=x; sleep 5` at `/feedback` — the "thanks" takes 5 seconds. The delay is the proof, no output needed.

The fix, in the same app: stop calling the shell. The ping becomes a subprocess call with an argument list and no shell (`["ping", "-c", "1", host]` — the host can never become a command), plus an allow-list check that the host is a valid IP or hostname. Re-test: `; echo PROBE-XYZ` now fails the allow-list (or is passed as a literal argument to ping, which errors harmlessly); `sleep 5` changes nothing; legitimate `127.0.0.1` still works. Then the rule, stated once and kept: the single most effective defense is to **never call out to OS commands from application code** — almost every use case has a safer platform API. If you must, allow-list; never escape metacharacters.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/b-command-injection.log`. Clean environment: stock Python 3.12, curl 8.5.0, loopback only, 2026-10-09. The demo app stands in for the PortSwigger/DVWA targets the reader uses (no Docker on this machine — see gaps).

1. **Start the vulnerable app.** Save the `app.py` from this lesson's companion (diagnostic page building `ping -c 1 <host>` through a shell; `/feedback` blind endpoint) and run it on port 8324. Confirm the baseline: `curl 'localhost:8324/diag?host=127.0.0.1'` returns ping output.
2. **Separator probe.** `curl 'localhost:8324/diag?host=127.0.0.1; echo PROBE-XYZ'` — observe `PROBE-XYZ` in the response. Write down, verbatim, the request and the response — this pair is the finding.
3. **Confirm impact, read-only.** `host=127.0.0.1 && whoami` — the response shows the OS user the app runs as. Note what that user could reach; do not reach for it. The finding is proven; stop.
4. **Blind channel.** `curl 'localhost:8324/feedback?email=x; sleep 5'` — time the response (~5s) versus `email=x` (~instant). The delay is the proof where there is no output.
5. **Apply the fix.** Patch the handler: no shell (argument-list subprocess), plus an allow-list that the host matches an IP/hostname pattern. Restart the app.
6. **Verify the fix — four cases.** `; echo PROBE-XYZ` → rejected by the allow-list (or passed inertly to ping); `&& whoami` → same; `sleep 5` on `/feedback` → no delay; `host=127.0.0.1` → ping output unchanged (legitimate function unbroken).
7. **Read the defender view.** The companion logs every spawned command. Find your probe in the log: the parent process (the Python app) spawning `/bin/sh` with your metacharacters in the command line. Write the detection rule: alert on any web-worker process spawning a shell, with the command line attached.

No step above is marked "not run by us" — in-band, blind, the fix, and all four verification cases ran locally.

## 5. On your own

**Task:** Pick one authorized target you have not touched in this lesson — a PortSwigger Academy OS command injection lab (the simple in-band one first), or DVWA's Command Injection module. Find the injection point with the `echo` probe, then determine whether it is in-band or blind (if blind, prove it with the time-delay channel). Then check the quoted-context case: does the input land inside quotes in the original command, and if so, what terminates it?

**Success test:** A one-page report: the vulnerable parameter, the metacharacter class that worked, in-band vs blind with evidence, the read-only impact confirmation (`whoami` output), the fix (no-shell API + allow-list, stated as code-level remediation), and the defender detection (which telemetry, which parent-child pattern). If you cannot determine the quoting context, say so and name the experiment that would settle it.

## 6. Where it goes wrong

- **Blocklist "sanitization."** Stripping `;` and `&` while leaving newlines, `$()`, backticks, or `${IFS}` — the shell has more metacharacters than your list. Allow-list or no-shell; there is no third option that holds.
- **"The input is numeric."** Validation that isn't actually enforced, or enforced client-side — the server is the only place a check counts.
- **Fixing the sink but not the pattern.** You patched the ping page; the feedback form still shells out. Every `system()`/`shell_exec()`/backtick call in the codebase is the same bug wearing a different feature.
- **Blind = not vulnerable.** The absence of output is a channel problem, not a verdict. Time delays and OAST exist precisely for this case.
- **Over-proving.** Running `whoami` proves the finding. Pivoting, reading `/etc/passwd`, or establishing persistence on an authorized target is outside every scope — the impact statement says what the access *could* reach, and stops.
- **Forgetting the parent process.** Defenders don't hunt your payload string; they hunt the web-worker-spawns-shell pair. Your report's detection section should say so.

## 7. Read the source

Primary documents first:

- **PortSwigger Web Security Academy — OS command injection** (portswigger.net/web-security/os-command-injection) — *read* fully; the canonical treatment (metacharacter classes, blind techniques: time/redirect/OAST, prevention). *Note* the prevention order: never shell out first, allow-list second, never escape.
- **CWE-78** (cwe.mitre.org/data/definitions/78.html) — *skim* the definition and its parent CWE-77 (command injection); cite the ID in findings.

Then at most three free resources:

1. **PortSwigger Academy — OS command injection labs** (portswigger.net/web-security) — free, hosted, authorized; in-band plus the three blind techniques from this lesson.
2. **DVWA — Command Injection module** (github.com/digininja/DVWA) — free; run locally via Docker: the Low→High ladder shows naive escaping failing, and Impossible shows the allow-list fix.
3. **OWASP Command Injection Defense Cheat Sheet** (cheatsheetseries.owasp.org) — free; the fix side: safe APIs per language, allow-list patterns.

## 8. Check yourself

1. Explain why `os.system("ping -c 1 " + user_input)` is vulnerable but `subprocess.run(["ping", "-c", "1", user_input])` is not, in terms of who parses the input.
2. A feedback form returns only "thanks" no matter what you submit, but `; sleep 8` makes the response take 8 seconds. Explain why this proves command injection and which metacharacter class did the work.
3. Predict the process tree a defender sees during active command-injection probing, and explain why the parent-child relationship is a better detector than the payload string.
4. A developer proposes stripping `;`, `&`, `|`, and backticks from the input as the fix. Name two shell features this misses and explain why allow-listing is structurally stronger.
5. You confirm injection with `whoami` on an authorized target. Explain what you write in the impact section of the report, and what you must not do next.

## 9. Prove it

**Artifact:** the one-page report from "On your own": vulnerable parameter, working metacharacter class, in-band vs blind evidence, read-only impact, code-level fix, defender detection.

**Honest claim:** "I can find OS command injection with metacharacter probes, prove blind cases through side channels, demonstrate read-only impact, and verify the no-shell/allow-list fix."
**Can't claim yet:** "I can assess the full blast radius" — post-exploitation impact assessment is a Stage C/D skill; this lesson proves the hole, not the house.

## 10. Leads to

- `b-ssrf` — the server makes requests instead of running commands; compare which trust relationship each one abuses.
- B-DEF (defensive basics) — sit on the other side: write the Sysmon/auditd rule for your own attack traffic.
- D red-team concepts (Stage D) — why this class is the first thing an adversary wants, taught as defender telemetry.
- Map refs: **OWASP Top 10:2025 A05**, **WSTG-INPV-13**, **CWE-78**.
