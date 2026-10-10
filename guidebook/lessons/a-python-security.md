---
lesson_id: a-python-security
slug: python-security
stage: A
level: 3
prerequisites: [a-linux-cli, a-http-depth]
roles: [security-analyst, pentester, appsec]
map_refs: []
test_date: 2026-10-09
description: "Python for security tooling: reading and changing small scripts — HTTP requests, response parsing, sockets, arguments and files — with every walkthrough step run locally. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · Python 3.12.3, loopback only, stdlib only, nothing external touched"
---
# Python for security tooling


**Map refs:** Stage A foundation; feeds `a-reading-code`, `b-toolbench`, and every walkthrough that ships a script.

---

## 1. Where this shows up

Every tool you will meet in Stage B is, under the hood, a program that opens connections, sends crafted input, and parses what comes back — and an enormous share of them are Python scripts. `b-toolbench` will hand you tools; this lesson is what lets you *read* them when they misbehave, *change* them when the job needs something slightly different, and *write* your own when no tool does exactly what you need. The goal is not software engineering. It is narrower and more useful: read a 60-line script and say what it does; change one behavior without breaking the rest; write a small tool from nothing when the task is "fetch these, check that, save the results." That is the whole of Python-for-security, and it is enough to carry you through the rest of the program.

## 2. Before you start

- Python 3 installed. The walkthrough ran on Python 3.12.3 — check yours with `python3 --version`.
- Comfort in the shell (`a-linux-cli`): you will run scripts, redirect output, and read tracebacks.
- A mental model of HTTP requests and responses (`a-http-depth`): your scripts will speak this protocol.
- Nothing to install. Every module used below — `urllib`, `json`, `socket`, `argparse` — ships in the standard library. That is deliberate: the first tools you write should have zero dependencies, so they run anywhere.

## 3. How it works

A Python script is a text file the interpreter executes top to bottom. `python3 fetch.py` runs it; `python3 -i` drops you into the interactive interpreter — the REPL (read-eval-print loop: read a line, evaluate it, print the result, repeat) — where you can try one line at a time. The interpreter is your laboratory: before a construct goes into a script, try it in the REPL and watch what it returns. Tracebacks read bottom-up — the last line names the error, the lines above show the call chain that reached it. Learning to read a traceback is half of debugging; the other half is `print()`.

**Making HTTP requests.** The standard library's `urllib.request` opens URLs and returns response objects. `urlopen(url)` gives you `.status`, `.headers`, and `.read()` for the body. Errors are exceptions: `HTTPError` (the server answered with 4xx/5xx — it still carries the status code) and `URLError` (no answer at all — connection refused, DNS failure). Catching them separately matters because they mean different things: an HTTPError is the *target speaking*, a URLError is the *network failing*. The walkthrough's `fetch.py` is fourteen lines that take a URL, print the status and content type, and optionally extract one key from a JSON body. That shape — fetch, check, extract, report — is the skeleton of half the reconnaissance tooling in existence.

**Parsing responses.** Bodies are bytes until you decide what they are. `json.loads()` turns a JSON body into dictionaries and lists — the moment a response becomes *data you can index into* instead of text you squint at. `r.headers.get("Content-Type")` tells you which parser to reach for. The discipline: never assume the shape; print it first (`print(type(data))`, `print(data.keys())`), then index. Scripts that assume response shapes are scripts that break on the first unexpected server.

**Sockets.** Below HTTP sits TCP, and `socket` lets you speak it directly. `socket.create_connection((host, port))` performs the handshake `a-tcpip-ports` taught you; `.sendall()` and `.recv()` move bytes. The walkthrough's `sockdemo.py` stands up a listener on 127.0.0.1, connects to it, sends `hello-socket`, and reads back `ACK:hello-socket`. Ten lines, and you have now done by hand what every port scanner does at its core: open a connection and see what answers. When a tool's output confuses you later, this is the layer to think at.

**Arguments and files.** A tool nobody can drive is a script, not a tool. `argparse` turns `sys.argv` into named options with `--help` text — `fetch.py` takes a URL positionally and `--json-key` optionally. Files are `open(path, mode)`: read the response, write it to disk, and the tool becomes a pipeline stage instead of a screenful of output. The walkthrough's final step does exactly the reader's first real edit: save the fetched body to `saved.json` — eleven lines that turn "look at this" into "keep this."

**Reading other people's scripts.** The skill this lesson exists for. Read top-down: imports first (they name the capabilities — `socket` means networking, `argparse` means it's meant to be driven), then `main()` or the bottom of the file (the entry point — start where execution starts, not where the file starts), then outward into functions. When you want to change behavior, change *one thing* and re-run. The walkthrough models this: the "add --save" edit is five lines appended to a working script, verified immediately.

### Worked example: the fetcher, annotated

`fetch.py` in full, because short tools deserve to be read whole:

```python
import sys, urllib.request, urllib.error, json, argparse

def main():
    p = argparse.ArgumentParser(description="Fetch a URL and show status/headers")
    p.add_argument("url")
    p.add_argument("--json-key", default=None)
    args = p.parse_args()
    try:
        with urllib.request.urlopen(args.url, timeout=5) as r:
            body = r.read()
            print("status:", r.status)
            print("content-type:", r.headers.get("Content-Type"))
            if args.json_key:
                data = json.loads(body)
                print(args.json_key, "=", data[args.json_key])
            else:
                print("bytes:", len(body))
    except urllib.error.HTTPError as e:
        print("HTTP error:", e.code); sys.exit(1)
    except urllib.error.URLError as e:
        print("URL error:", e.reason); sys.exit(1)

if __name__ == "__main__":
    main()
```

Read it the way the lesson teaches: imports (`urllib` → network, `argparse` → drivable, `json` → parses bodies) — entry point (the `if __name__ == "__main__"` guard runs `main()` only when the file is executed directly, not when another script imports it — the standard Python entry-point idiom) — the try block is the whole job (fetch, then branch on whether the user asked for a JSON key) — the except blocks separate "server said no" from "nobody answered," and `sys.exit(1)` tells the calling shell the script failed (a nonzero exit is how scripts report failure to whatever runs them). The `timeout=5` is the line beginners omit and then learn about the hard way: without it, a hung server hangs your script forever.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/a-python-security.log`. Clean environment: Python 3.12.3, loopback only, scratch dir `/tmp/pywalk`, 2026-10-09. A local HTTP server stood in for any remote target.

1. **Check the interpreter.** `python3 --version` → `Python 3.12.3`. Know your version; behavior differences between 3.8 and 3.12 are real.
2. **Stand up the target.** A 20-line stdlib HTTP server on 127.0.0.1:8471 serving `/` (text) and `/json` (a JSON body). Your scripts will only ever touch this loopback target.
3. **Fetch and inspect.** `python3 fetch.py http://127.0.0.1:8471/` → `status: 200`, `content-type: text/plain`, `bytes: 11`. The three facts every fetch starts with.
4. **Parse the body.** `python3 fetch.py http://127.0.0.1:8471/json --json-key service` → `service = pywalk`. Bytes became a dictionary became one value — the parse chain.
5. **Watch it fail well.** `python3 fetch.py http://127.0.0.1:9999/` → `URL error: [Errno 111] Connection refused`, exit 1. The URLError branch, doing its job: the network failed, and the script said so instead of trace-backing.
6. **Speak TCP directly.** `python3 sockdemo.py` → `received: b'ACK:hello-socket'`. Listener, connect, send, receive — the handshake made explicit.
7. **Change the tool.** The `--save` edit: fetch `/json`, write the bytes to `saved.json`, print the byte count → `saved 47 bytes`. One behavior changed, immediately verified. This is the whole skill.

## 5. On your own

**Task:** Extend `fetch.py` into `scan.py`: it takes a file of URLs (one per line, your own local servers), fetches each with a 5-second timeout, and writes one JSON line per URL to `results.jsonl` containing the URL, status code (or the string `"unreachable"`), content type, and body length. Handle both exception types. Then point it at three local endpoints — one that answers, one that 404s (add a path to the demo server), one with nothing listening — and show the three different outcomes in your results file.

**Success test:** `results.jsonl` has one valid JSON object per input URL; the unreachable target records `"unreachable"` instead of crashing; the script exits 0; you can explain what each `except` branch caught.

**Hints:** Read the file with `open(...).read().splitlines()`; skip blank lines. Build a dict per URL and `json.dumps()` it per line.

## 6. Where it goes wrong

- **`pip install` as a first resort.** Every dependency is attack surface and a future breakage. The walkthrough uses stdlib only, on purpose — write it with the standard library first, and reach for third-party packages only when the stdlib genuinely cannot do it. When you do install, pin versions and read what you installed.
- **Running scripts you haven't read.** `curl URL | python3` is the Python twin of piping to shell — you just gave a stranger code execution. Download, read (you now can), then run. The defender's version of the same habit: when you inherit an unknown script — or triage a suspicious one — the first greps are `eval(`, `exec(`, `base64`, `os.system`, `subprocess`, and any hardcoded IP or hostname. An obfuscated blob plus network calls is the shape of a malicious script; ruling that out is what "read before you run" buys you.
- **No timeouts.** A script without timeouts is a script that hangs in production at 3 AM. Every network call gets a timeout, no exceptions.
- **Catching everything.** `except Exception:` swallows the distinction the walkthrough's two branches preserve. Catch what you can handle; let the rest traceback loudly.
- **Hardcoded targets and credentials.** The walkthrough's `127.0.0.1:8471` is fine for a lab; a "tool" with a hardcoded IP and password is a liability. Arguments for targets, environment or files for secrets, never literals.
- **Assuming response shape.** `data["key"]` on a response that returned an error page raises `KeyError` — or worse, silently proceeds on wrong data. Print the shape first, index second, and handle the missing-key case.

## 7. Read the source

Primary documents first — the language documents itself:

- **The Python Tutorial** (docs.python.org/3/tutorial/ — verified 2026-10-09) — the language's own introduction. *Read* chapters 3–5 (informal intro, control flow, data structures) and 7 (input/output); *skim* 10 (stdlib tour — note §10.7 internet access, §10.3 command-line arguments); *skip* 9 (classes) for now — you don't need OOP to write tools.
- **The standard library reference** (docs.python.org/3/library/ — same site, verified via the tutorial's own links) — not read cover-to-cover; this is where you look up `urllib.request`, `json`, `socket`, `argparse` *as you use them*. The habit of reading the library docs is the skill.

Then at most three free resources:

1. **Python for Everybody** (py4e.com — verified 2026-10-09) — free materials, lectures, and book for programming from zero. If you have never coded, start here before this lesson's walkthrough.
2. **Automate the Boring Stuff with Python** (automatetheboringstuff.com — verified free to read 2026-10-09) — practical scripting with security-direct chapters: regex, files, web scraping, SQLite. The bridge from "can code" to "codes tools."
3. **Bandit** (overthewire.org/wargames/bandit — verified 2026-10-09) — not Python, but the shell fluency from `a-linux-cli` needs somewhere to live, and your scripts will run in that shell.

## 8. Check yourself

1. `urlopen` raises `HTTPError` on one URL and `URLError` on another. Explain, without running anything, what the difference tells you about where the failure happened.
2. Your script prints `bytes: 11` for a page you expected to be JSON. Name the two things you check before you call `json.loads`.
3. Why does every network call in a tool need a timeout? Describe the failure mode of the script that omits it.
4. You inherit a 200-line script. Describe the exact order you read it in, and what the imports tell you before you read a single function.
5. `sockdemo.py` uses `socket.create_connection` instead of building the socket by hand. What layer of the stack is it letting the standard library handle, and why is that the right default?

## 9. Prove it

**Artifact:** A small original tool in a public repo with a README: what it does, how to run it, what its output means. Examples: a header auditor (fetch a URL, report missing security headers — pairs with `b-security-headers`), a log parser (the `hits.log` pipeline from `a-linux-cli` as a script with arguments), or an HTTP request replayer (read a saved request, resend it, diff the response).

**Honest claim:** "I can read a small Python security tool, explain what each part does, and adapt it to a new task — demonstrated on my own tool, linked here."

**You cannot yet claim:** production-grade engineering (testing, packaging, performance) — that's software engineering, explicitly out of scope. The `a-reading-code` lesson extends the reading half of this skill to JavaScript and SQL.

## 10. Leads to

- `a-reading-code` — the same read-first discipline applied to JavaScript and SQL: trace input through code you didn't write.
- `b-toolbench` — the fifteen tool phases, where this lesson pays off: you will read tool output *and* tool source.
- `b-security-headers` — a natural first target for your header-auditor artifact.
- Every Stage B walkthrough from here on assumes you can run and tweak the scripts it ships.
