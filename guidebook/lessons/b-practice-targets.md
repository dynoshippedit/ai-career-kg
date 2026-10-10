---
lesson_id: b-practice-targets
slug: practice-targets
stage: B
level: 2
prerequisites: [a-linux-cli, a-tcpip-ports]
roles: [pentester]
map_refs: []
test_date: 2026-10-09
description: "Setting up practice targets locally: DVWA, Juice Shop, WebGoat, crAPI and DVGA, one verified command each, bound to localhost — so you never need a live system. A free lesson in the security guidebook."
dateline: "Procedures verified against the projects' own READMEs 2026-10-09 · DVGA additionally run for real on the build machine 2026-10-10 (native, from the project's own source — registry pull blocked, see runs log); other container runs not run by us"
---
# Setting up practice targets locally


**Map refs:** feeds every hands-on `b-…` lesson; `b-toolbench` phase 13 (local environment).

---

## 1. Where this shows up

Every hands-on lesson in this guidebook needs a target you are allowed to touch, and the answer is always the same: one you run yourself, on your own machine, bound to localhost. This lesson builds that bench of targets once, so every later lesson can say "stand up DVWA" instead of teaching installation for the tenth time. The five local targets plus PortSwigger's hosted labs cover every vulnerability class in Stage B. After this lesson, the sentence "I don't have anything legal to practice on" is never true again — and neither is its evil twin, "so I'll practice on a live site."

## 2. Before you start

- `a-linux-cli` is complete — you are comfortable with the shell, and you understand what "bind to localhost" means (`a-tcpip-ports`).
- Docker basics: you know what an image and a container are. If you do not have Docker installed, install it from Docker's official documentation (linked below) — the commands below assume the Docker daemon is running.
- `b-authorization-scope` is complete — and it applies here with a twist: each of these targets is vulnerable *by design*, and running one is its own authorization. Your scope is "this container, on my machine, right now." That scope does not extend to your roommate's laptop, your employer's network, or the internet.

## 3. How it works

A **practice target** is an intentionally vulnerable application you run locally so you can attack it legally. The five below are the standard set — each maintained by its own project, each the primary source for its own setup. The setup commands are quoted from each project's README as fetched in-session on 2026-10-09, not from memory. If a command below ever disagrees with the project's current README, the README wins — re-check at setup time.

**DVWA — Damn Vulnerable Web App.** The classic: PHP and MariaDB, with per-module difficulty levels from low to impossible. The difficulty ladder is the teaching feature — you run the same attack against low (no defense), medium, high, and impossible, and each level shows you what a defense actually does. Serves the injection, access-control, authentication, and XSS lessons.

```bash
git clone https://github.com/digininja/DVWA
cd DVWA
docker compose up -d
```

Then open `http://localhost:4280`. Reset: `docker compose down` (stops and removes the containers; your database changes go with them — that *is* the reset). Bring it back with `docker compose up -d` and you are at a clean slate.

**OWASP Juice Shop.** A modern Node.js shop application, gamified: dozens of challenges on a score board, from trivial to genuinely hard. This is where the business-logic, API, and injection lessons live most happily. The README's own run command already binds to loopback:

```bash
docker pull bkimminich/juice-shop
docker run --rm -p 127.0.0.1:3000:3000 bkimminich/juice-shop
```

Then `http://localhost:3000`. The `--rm` flag removes the container when you stop it — score progress resets, which is the point: you re-earn it. (Ephemeral — thrown away when the container stops; nothing persists. Scores can be persisted with a volume; the README documents how. For practice, ephemeral is better.)

**OWASP WebGoat.** A Java lessons application with structured lessons (each vulnerability is a taught lesson, not just a target) plus **WebWolf**, a companion "attacker mailbox" that receives the callbacks your attacks trigger. Serves the deserialization, XXE, and authentication lessons especially. Note the timezone flag: the README documents `-e TZ=<your-zone>` because the JWT lessons are time-sensitive — set it to your host's timezone or the token-expiry lessons will confuse you.

```bash
docker run -it -p 127.0.0.1:8080:8080 -p 127.0.0.1:9090:9090 webgoat/webgoat
```

Then `http://localhost:8080/WebGoat` (the app) and `http://localhost:9090/WebWolf` (the mailbox). Both ports are loopback-bound in the command above.

**OWASP crAPI — completely ridiculous API.** A full vulnerable API (a car-shop with users, vehicles, and orders) plus a MailHog instance that catches the app's outgoing mail. Purpose-built for API abuse: it is the target the BOLA and API Top 10 lessons were written against.

```bash
# from the deploy/docker directory of the cloned repo, or with the
# compose file downloaded from the repo:
docker compose pull
docker compose -f docker-compose.yml --compatibility up -d
```

Then `http://localhost:8888` (the API) and `http://localhost:8025` (MailHog — read the password-reset emails your attacks trigger). Reset: `docker compose -f docker-compose.yml --compatibility down`.

**DVGA — Damn Vulnerable GraphQL Application.** A small GraphQL service built to be attacked: introspection, field-level authorization, batching — the whole GraphQL abuse surface in one container. Port confirmed as **:5013** on the current README (older mirrors say :5000; the project's own page as fetched today says 5013 — trust the README, and this resolves the old gap).

```bash
docker pull dolevf/dvga
docker run -t -p 127.0.0.1:5013:5013 -e WEB_HOST=0.0.0.0 dolevf/dvga
```

Then `http://localhost:5013`. Note the deliberate correction in the command above: the README shows `-p 5013:5013`, which binds the container's port to *all* host interfaces. The lesson's version binds it to loopback only (`127.0.0.1:5013:5013`). The `-e WEB_HOST=0.0.0.0` stays — that is the *container-internal* bind (the app must listen inside its own network namespace — the container's private view of the network: its own interfaces, its own localhost, separate from your machine's); the `-p` flag is the *host* bind, and that is where your safety lives. Why the app must bind 0.0.0.0 *inside* the container: the container's localhost is not your machine's localhost. If the app bound 127.0.0.1 inside its own namespace, Docker's port-forward could never reach it — the app would be up and unreachable. So the app listens on all interfaces *of its own private network*, and the `-p 127.0.0.1:5013:5013` flag decides which of *your* interfaces may knock on the door. Understand the difference between those two binds before you run anything else in this lesson.

**PortSwigger Web Security Academy.** Not local, but the sixth target: hosted, free, authorized by design — every lab is its own ephemeral target with defined scope, resettable per lab. Account signup and lab launch are reader-side (your browser, your account). The Academy's front page confirms: free, interactive labs, Burp Community compatible (verified in-session, 2026-10-09). Use it for every vulnerability class alongside the local targets.

**The safety rules for all of the above** (brief §7, non-negotiable):

- Bind everything to localhost / 127.0.0.1. Never expose a vulnerable app to a network — the DVGA correction above is the pattern; apply it everywhere.
- DVWA and WebGoat both warn, in their own documentation, that the running container makes the host vulnerable. Run them only while you are practicing, then `compose down`. A vulnerable app you forgot about is an attack surface you installed yourself.
- Never scan, probe, or test any live system during setup or practice. If a target needs to be reachable for a technique, the technique waits until you have a local lab for it.

**Resetting, summarized:** DVWA and crAPI reset with `compose down`; Juice Shop resets by stopping the `--rm` container; WebGoat resets by stopping and removing the container; DVGA the same; PortSwigger labs reset with the lab's own reset control. "Reset and re-attack" is a core practice loop — a finding you can only demonstrate once, on a dirty database, is not a clean proof.

## 4. Walkthrough

**Procedure verification + one real bring-up.** Steps 1–4 verify every setup procedure against the primary source (transcript: `runs/b-practice-targets.log`). Step 6 runs DVGA for real on this machine — the one target light enough to run natively, and the one whose all-interfaces bind is this lesson's key teaching moment. Docker is installed on this machine now (static binaries, 28.5.2) but the registry is unreachable from this network — the runs log carries the full attempt log, so the honest marker below stands on evidence, not assumption. Verified 2026-10-09; DVGA run 2026-10-10.

1. **Fetch the canonical READMEs.** All five project pages fetched in-session (HTTP 200): DVWA, Juice Shop, WebGoat, crAPI, DVGA. These are the primary sources; everything below is quoted from them.
2. **Extract and record the run commands.** Each command in section 3 was extracted from its README's text: DVWA's `docker compose up -d` with the `127.0.0.1:4280:80` mapping; Juice Shop's loopback-bound `docker run`; WebGoat's dual-port command with the `-e TZ=` note; crAPI's `docker compose pull` + `--compatibility up -d`; DVGA's `docker pull` + `docker run -t -p 5013:5013`.
3. **Confirm the ports.** DVWA `:4280`, Juice Shop `:3000`, WebGoat `:8080`/`:9090`, crAPI `:8888` + MailHog `:8025`, DVGA `:5013` — all confirmed in the READMEs; all distinct, so all five targets can run simultaneously.
4. **Apply the safety correction.** DVGA's README binds all interfaces; the lesson teaches the loopback override and explains the two-bind distinction (container-internal vs host). This is the lesson's key teaching moment, and it is marked as a lesson decision, not a README quote.
5. **Container runs: not run by us.** The Docker daemon runs on this machine now, but Docker Hub is unreachable from this network (registry TLS timeouts; the full attempt — static binaries, vfs driver, proxy-aware pull tools — is logged in `runs/b-practice-targets.log`). The commands are verified quotes from the projects' own documentation as fetched today — but the containers were not started here. The reader runs them on their own machine, following `b-authorization-scope`'s rules.
6. **DVGA, run for real (native, 2026-10-10).** With the registry blocked, DVGA ran from the project's own source instead: cloned `github.com/dolevf/Damn-Vulnerable-GraphQL-Application`, installed its `requirements.txt` in a venv (two substitutions logged in the runs log: the pinned gevent 22.10.2 won't build on Python 3.12 → gevent 26.9.0; pinned greenlet 2.0.1 conflicts → 3.5.6), ran `setup.py` to build the database. Then, with `WEB_HOST=127.0.0.1`: the app listened on **127.0.0.1:5013 only** (`ss -tlnp` confirms — loopback, not all interfaces), served HTTP 200 on `/`, and answered a real GraphQL introspection query (`{ __schema { types { name } } }` → the full type list, introspection enabled) plus `{ systemHealth }`. Then restarted with `WEB_HOST=0.0.0.0` — the README's setting — and `ss` showed **0.0.0.0:5013 LISTEN**: the vulnerable app exposed on every interface. That pair of `ss` outputs is the whole lesson in one line: the README's `-e WEB_HOST=0.0.0.0` (plus `-p 5013:5013`) is what you're overriding when you bind loopback. Teardown: app killed by PID, port verified free, no stray processes.

## 5. On your own

**Task:** Stand up all five local targets simultaneously, each on its documented localhost port, plus one PortSwigger Academy lab of your choice. For each of the six, write one line: what the target is for (which vulnerability classes it serves). Then attack nothing — this lesson is setup only. Instead, practice the reset: `compose down` DVWA, restart it, and confirm the login page is clean.

**Success test:** All five local targets respond on their `127.0.0.1` ports at once (curl each one and record the HTTP status), the PortSwigger lab loads in your browser, and your one-line "what this is for" list covers all six. If any target is reachable on a non-loopback interface of your machine, fix the bind before doing anything else — that misconfiguration is itself the first finding of your practice career, and you found it with `ss`.

## 6. Where it goes wrong

- **Binding to all interfaces.** The DVGA default (`-p 5013:5013`) and any command you copy without reading will expose a deliberately vulnerable app to your whole network. Loopback-bind everything, verify with `ss -tlnp`, and understand the container-internal vs host bind distinction.
- **Leaving them running.** A vulnerable app left up "for later" is an installed attack surface. The discipline: start when you practice, `down` when you stop. Put it in your notes as a checklist item.
- **Stale images.** `docker pull` before you start a new practice cycle — projects fix their own tooling and occasionally their vulnerabilities' difficulty. Practicing against a year-old image teaches last year's app.
- **Port conflicts.** Two targets on `:3000` (Juice Shop and the WebGoat desktop variant) — the documented ports in section 3 are conflict-free; if you improvise, check `ss` first.
- **The WebGoat timezone trap.** JWT lessons failing mysteriously is the classic WebGoat gotcha, documented in its README: set `-e TZ=` to your host zone. When time-based behavior confuses you, check the clock first — containers and hosts disagree more often than you'd think.
- **Practicing on a live system "because the lab didn't have it."** No. The technique waits for a lab. This is hard rule 1 wearing a lab coat: a missing target is not permission.
- **Treating PortSwigger labs as unlimited.** Each lab is its own scope and its own ephemeral target. The authorization covers the lab, not portswigger.net generally, and not the internet beyond it.

## 7. Read the source

Primary documents first — the projects' own READMEs (all fetched in-session, 2026-10-09):

- **DVWA** (github.com/digininja/DVWA) — *read* the setup and difficulty-level sections; the README is the authority on `compose up` and on what each level's defenses do.
- **OWASP Juice Shop** (github.com/juice-shop/juice-shop) — *read* the run section and the challenge-hint policy; *note* how the score board structures practice.
- **OWASP WebGoat** (github.com/WebGoat/WebGoat) — *read* the Docker run section including the `-e TZ=` note; *skim* the lesson list to map lessons to this guidebook's vulnerability classes.
- **OWASP crAPI** (github.com/OWASP/crAPI) — *read* the deploy/docker instructions; *note* the MailHog companion and what it is for.
- **DVGA** (github.com/dolevf/Damn-Vulnerable-GraphQL-Application) — *read* the run section; *note* the `:5013` port and the all-interfaces default you will override.

Then at most three free resources:

1. **Docker's official install documentation** (docs.docker.com) — free; the only install guide this lesson endorses. Install from the vendor, not from a blog's curl pipe.
2. **PortSwigger Web Security Academy** (portswigger.net/web-security) — free; the hosted sixth target, each lab its own authorized scope.
3. **OWASP WSTG v4.2** (owasp.org/www-project-web-security-testing-guide/v42/) — free; once the targets are up, this is the checklist you run against them — the methodology lesson's companion.

## 8. Check yourself

1. Explain the difference between the container-internal bind (`WEB_HOST=0.0.0.0` inside DVGA) and the host bind (`-p 127.0.0.1:5013:5013`), and why getting them confused exposes a vulnerable app to your network.
2. Your WebGoat JWT lessons fail while everything else works. Explain the most likely cause, where the README documents it, and the exact flag that fixes it.
3. You want to practice the same SQL injection twice to compare your technique. Explain the reset procedure for DVWA and why "reset and re-attack" produces cleaner proof than attacking a dirty database.
4. A friend suggests practicing directory brute-forcing against a real company's site "because DVWA doesn't have enough paths." Explain which hard rule this violates and what the lawful alternative is.
5. You have all five local targets running and want to add a sixth container from an unrelated tutorial that maps `-p 8080:80`. Explain what you check first and why.

## 9. Prove it

**Artifact:** the six one-line "what this is for" descriptions from "On your own," plus a curl transcript showing all five local targets responding on their `127.0.0.1` ports, plus your PortSwigger Academy account's lab-completion record (or the lab you chose, launched). The artifact proves the bench exists and is correctly bound.

**Honest claim:** "I can stand up, bind safely, and reset the five standard local practice targets plus PortSwigger labs, and I know which vulnerability classes each one serves."
**Can't claim yet:** "I can find vulnerabilities in them" — that is what the bench is *for*, and the vulnerability lessons are next.

## 10. Leads to

- **The `b-sqli`, `b-xss`, `b-…` vulnerability lessons** — each one names its target from this lesson's bench; re-read the target's README section before you start each one.
- **`b-toolbench`** (back-link) — phase 13 (local environment): this lesson *is* that phase, built out.
- **`b-methodology`** (back-link) — the engagement frame; the bench is where its technical phases execute.
- **`b-authorization-scope`** (back-link) — each target is its own written scope; the safety rules here are that lesson applied.
- Map refs: feeds all Stage B hands-on lessons; `b-toolbench` phase 13.
