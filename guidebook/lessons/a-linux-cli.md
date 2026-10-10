# Linux command line for security work

**ID:** `a-linux-cli` · **Stage:** A (Foundations) · **Level:** 3 (operate — you can navigate, inspect, and control a Linux system from the shell, unaided) · **Prerequisites:** None. This is the bench everything else runs on; if you arrived from `a-tcpip-ports`, you already know why the machine matters.

**Map refs:** Pre-map foundations; feeds every later lesson (all walkthroughs assume this).

---

## 1. Where this shows up

Every tool in this program runs on Linux, and every one of them is driven from the command line. The walkthroughs in `a-dns-depth` and `a-tcpip-ports` were shell sessions; the servers you will attack and defend in Stage B are Linux machines; the logs you will triage as a SOC analyst are Linux logs; the cloud instances in Stage D are Linux. "Learn the command line" is not a prerequisite chore — it is the job's primary instrument. A practitioner who fumbles the shell fumbles everything downstream, and a practitioner fluent in it can investigate any unfamiliar system, because the shell is the one interface every Linux machine shares.

## 2. Before you start

- Any Linux terminal: your own VM, WSL2, or a container. The walkthrough ran on Ubuntu with bash 5.2, coreutils 9.4, OpenSSH 9.6.
- Work as a normal user where you can. The walkthrough shell ran as root (a container), and the transcript says so wherever it changes what you see — root bypasses permission checks, which hides the very errors this lesson teaches you to read.
- Nothing to install. Everything below ships with the OS.

## 3. How it works

The shell is a conversation with the kernel, mediated by programs. `ls` is a program; `cd` is built into the shell; the pipe `|` is the shell connecting one program's output to another's input. Internalize that split and the command line stops being incantations: every command is either a program you can inspect (`which`, `man`, the binary itself) or a shell feature you can look up (`help`).

**Files.** Everything is a file: regular files, directories, devices (`/dev/sda`), process information (`/proc/<pid>/`), even the kernel log. `ls -la` shows the truth about a directory: permissions, owner, group, size, timestamps. Learn to read that line the way a pilot reads instruments — in security work, a wrong permission bit *is* the vulnerability. `stat` spells out what `ls` abbreviates.

**Permissions are a bitmask.** Three triples — owner, group, other — each read/write/execute (`rwx`). Octal is the compact form: `r=4, w=2, x=1`, so `755` is `rwxr-xr-x` and `600` is `rw-------`. Directories need `x` to enter and `r` to list — a directory with `x` but not `r` lets you open files you can name but not browse, a subtlety that matters for web roots. New files don't get 666/777; the **umask** subtracts bits (umask `022` → files `644`, directories `755`). The walkthrough machine's umask was `0007` → files `660`: group-only, no world access. Default-deny arithmetic, applied at creation.

**Users, groups, and the setuid exception.** Every process runs as a user; every file has an owner and a group. The permission triples are evaluated against *who you are* — which is why running as root teaches you nothing about permissions: root bypasses the checks. The exception that matters: the **setuid** bit. A setuid program runs with its *owner's* privileges, not yours — that's how `sudo` and `passwd` work, and it's a classic privilege-escalation target: a setuid binary owned by root with a flaw *is* a root shell waiting to happen. `find / -perm -4000` is one of the first commands run on any unfamiliar Linux box, offensive or defensive.

**Processes.** Programs in motion. `ps` shows them; `pgrep` finds them by name; `kill` sends them signals. Signals are the vocabulary: `TERM` (15, the default — "please stop"), `KILL` (9 — unblockable, no cleanup), `HUP`, `USR1/2`. A process that ignores TERM but dies to KILL told you something about its signal handling. Parent/child (`PPID`), sessions, and job control (`&`, `jobs`, `fg`) complete the picture: the `&` in the walkthrough put `sleep` in the background of *that shell*, and `kill %1` would have worked too.

**Logs.** The machine's memory. `journalctl` (systemd's journal), `/var/log/` (the classic files: auth, syslog, application logs), `dmesg` (kernel ring buffer — needs privilege, as the walkthrough shows). In Stage B's defensive lessons and Stage D's forensics, these are the primary sources. Learn now where they live so later you're reading, not searching.

**Pipes and redirection.** The shell's superpower: `|` chains programs into pipelines, `>`/`>>` redirect to files, `<` feeds files in. `grep` filters, `cut`/`awk` extract fields, `sort | uniq -c | sort -rn` counts and ranks — the walkthrough's one-liner (`grep '^web' hits.log | cut -d' ' -f2 | sort | uniq -c | sort -rn`) is the exact shape of SOC triage: filter, extract, count, rank. On real access logs, that pipeline answers "what is this attacker doing" in seconds. `awk` deserves special mention: it's a whole language hiding as a field extractor, and fluency with `-F` and `{print $N}` pays off daily.

**SSH.** The secure remote shell, and the key lesson is *keys, not passwords*. `ssh-keygen -t ed25519` makes a keypair: the private key stays on your machine (permissions 600 — the OS enforces this), the public key is one line appended to `~/.ssh/authorized_keys` on the server. Authentication becomes a challenge-response the server verifies against the public key — no password crosses the network, none can be brute-forced. `ssh -G` shows your effective client config; `/etc/ssh/sshd_config` on the server is where `PasswordAuthentication no` lives — the single most impactful hardening line on any Linux server, and the reason this lesson teaches key generation before anything else about SSH.

### Worked example: reading a machine like an investigator

From the walkthrough (§4): in `/tmp/cliwalk`, `plans.txt` is created (note its initial mode `660` — the umask at work), tightened to `600`, then to `000`. As root, `cat` still succeeds — the transcript flags this explicitly: *running as root hides permission errors*. On your machine as a normal user, `000` gives `Permission denied`, and that error is information: it tells you the check happens per-triple against your identity. `id` shows who you are; `find /usr/bin -perm -4000` lists the setuid binaries (`chfn`, `mount`, `newgidmap`…) — each one a program that will run as its owner. A `sleep 300` backgrounded, found via `ps` and `pgrep`, and killed with SIGTERM. The hits.log pipeline counts status codes by frequency. An ed25519 keypair generated, the public key displayed as the single line a server needs. Each command is small; the skill is chaining them without hesitation on a machine you've never seen before.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/a-linux-cli.log`. Clean environment: Ubuntu container, bash 5.2.21, coreutils 9.4, OpenSSH 9.6p1, scratch dir `/tmp/cliwalk`, 2026-10-09. This shell ran as **root**; the transcript marks every place that changes the output.

1. **Read a directory listing like an instrument.** `echo 'secret plans' > plans.txt && ls -la` — name every column. Then `stat -c '%a %U:%G %n' plans.txt`: octal mode, owner, group.
2. **Change permissions and feel the bitmask.** `chmod 600`, `chmod 000` — as root, `cat` still works; the transcript explains why and what a normal user would see. Restore to `644`. Run `umask` and compute the default mode for a new file yourself before reading the explanation.
3. **Meet the user database and setuid.** `id`, `head -3 /etc/passwd` (name, `x`, uid, gid, home, shell — say what the `x` means), `find /usr/bin -perm -4000 | head -5`. For one binary, explain *why* it needs to run as its owner.
4. **Start, find, and stop a process.** `sleep 300 &`, `ps -o pid,ppid,user,etime,cmd -p $!`, `pgrep -a 'sleep 300'`, `kill $!`, verify it's gone. Name the signal you sent.
5. **Find the logs.** `ls /var/log/`, `journalctl --no-pager -n 3`, `dmesg | tail -2` — note which one failed and why (privilege), and where you'd look for SSH login attempts on a real server (`/var/log/auth.log` or the journal).
6. **Build the triage pipeline.** Create `hits.log`, then `grep '^web' hits.log | cut -d' ' -f2 | sort | uniq -c | sort -rn`. Explain what each stage of the pipe does. Then `awk -F: '{print $7}' /etc/passwd | sort | uniq -c | sort -rn` — shells in use on the system.
7. **Make an SSH keypair.** `ssh-keygen -t ed25519 -f labkey -N '' -C 'guidebook-lab'` — read the public key aloud as three fields. `ssh -G localhost | grep -iE '^(user|port|identityfile)'` — your effective client config. Note: no `sshd_config` on this machine (no sshd); on yours, read every uncommented line.

## 5. On your own

**Task:** On your own machine as a *normal user* (not root): create a directory `~/clilab` containing a file `secret.txt` with mode `600` and a subdirectory `shared` with mode `755` containing `note.txt` mode `644`. Then, as that user: (a) prove you can read `secret.txt` but a *different* local user cannot (use `su`/`sudo -u` if you have a second account, or reason it out from the triples and state the answer); (b) find all setuid binaries on the system and pick one — explain in two sentences why it legitimately needs the bit; (c) write a one-liner that lists the five largest files under `/var/log`.

**Success test:** The three modes are exactly as specified (`stat` output to prove it); your setuid explanation names the privileged operation the program must perform; the one-liner runs without errors and its output is sorted by size.

**Hints:** `du -b` gives bytes; `sort -n` sorts numerically. For (a), the permission check is owner → group → other, first match wins.

## 6. Where it goes wrong

- **Running everything as root.** The walkthrough did it (container); you shouldn't. Root hides permission errors, makes every mistake catastrophic (`rm -rf` with no safety net), and teaches you nothing about the access model you're supposed to be learning. Use a normal user and `sudo` deliberately.
- **Permission triples misread.** `777` "to make it work" is how web shells get uploaded. If a tutorial tells you to chmod 777, the tutorial is wrong — find the *actual* owner/group mismatch instead.
- **`kill -9` as a first resort.** SIGKILL denies the process cleanup: corrupted files, held locks, orphaned children. TERM first; KILL when TERM fails and you know why.
- **Piping curl to shell.** `curl URL | sudo bash` executes unaudited code as root — the exact opposite of everything this program teaches. Download, read, then run.
- **Private keys with bad permissions or in repos.** SSH refuses keys readable by others (and tells you so — read the error). A private key committed to git is compromised the moment it's pushed; the fix is rotation, not deletion (history remembers).
- **Trusting `ps` output at face value on a suspect box.** Rootkits hide processes. `ps` is a starting point; cross-check with `/proc` and network state (`ss -tlnp`) — Stage D teaches the full paranoia.
- **Forgetting which machine you're on.** An `rm`, a `chmod -R`, a `kill` in the wrong terminal is the classic self-inflicted incident. The prompt shows hostname for a reason — customize yours to make production unmistakable.

## 7. Read the source

Primary documents first — the shell's documentation *is* the machine:

- **Man pages** (`man ls`, `man chmod`, `man ssh`, `man sshd_config`, `man journalctl`) — *read* the DESCRIPTION and EXAMPLES sections; *skim* the option lists; *skip* nothing permanently — the man page is the reference you return to for years. No fetch needed: they ship with the OS.
- **OpenSSH manual pages** (openssh.com/manual.html — verified 2026-10-09) — the project's own docs: `ssh(1)`, `ssh-keygen(1)`, `sshd_config(5)`. *Read* ssh-keygen's key-type notes; *skim* sshd_config's authentication section.

Then at most three free resources:

1. **OverTheWire: Bandit** (overthewire.org/wargames/bandit — verified 2026-10-09) — SSH-based wargame for absolute beginners; each level *requires* the commands this lesson teaches. Start at level 0 today.
2. **Linux Journey** (linuxjourney.com, now on LabEx — verified free and open-source 2026-10-09) — structured reading on the filesystem, permissions, processes, and users; the concepts Bandit makes you exercise.

## 8. Check yourself

1. A file has mode `640`, owned by `root:adm`. You are user `ops`, in group `adm`. Can you read it? Write it? Explain which triple applies and why the other two don't.
2. `umask` returns `027`. A program creates a file requesting mode `666`. What mode does the file get? Show the arithmetic.
3. `ps` shows a process, but `kill <pid>` reports "No such process" a second later. Explain what happened — and why `kill -9` would not have helped.
4. You find a setuid-root binary in `/opt/vendor/bin` that you don't recognize. Name the two questions you ask before deciding whether it's legitimate, and the command that tells you when it was installed.
5. Explain why appending your *public* key to a server's `authorized_keys` is safe to do over an untrusted channel, but sending the *private* key anywhere is not — using the word "challenge" correctly.

## 9. Prove it

**Artifact:** a published "Bandit notes" page (Markdown in your new git repo — see `a-git-github`): one entry per Bandit level you complete, each naming the command you learned, what it does, and the exact invocation that beat the level. Plus: your hardened SSH client config (`~/.ssh/config` with key-only defaults) documented with one line per option.

**Honest claim:** "I can navigate, inspect, and control a Linux system from the shell, chain tools into pipelines, manage permissions and processes, and use SSH keys correctly."
**Can't claim yet:** "I can administer or harden a server" — that needs the SSH *server* side, package management, and services (a later Stage A lesson); this one built fluency, not administration.

## 10. Leads to

- `a-git-github` — next: your Bandit notes and every later artifact live in version control — learn the tool before you need it.
- `a-http-depth` — the Stage A milestone lesson: the shell runs the lab server whose traffic you'll narrate packet by packet.
- Every Stage B lesson: their walkthroughs assume this lesson's fluency without re-teaching it. If a later walkthrough's commands feel like incantations, come back here.
