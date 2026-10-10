# Git and GitHub

**ID:** `a-git-github` · **Stage:** A (Foundations) · **Level:** 3 (operate — you can version your work, collaborate, and read a repository's history unaided) · **Prerequisites:** `a-linux-cli` (everything here happens in the shell).

**Map refs:** Pre-map foundations; the artifact pipeline for every stage (all "Prove it" work lives in git).

---

## 1. Where this shows up

Every artifact this program asks you to produce — lab notebooks, Bandit notes, tools, reports, disclosures — lives in a git repository, and the public ones live on GitHub. That is not administrative overhead; it is the mechanism of the site's whole bet: *checkable evidence*. A stranger evaluating your skill doesn't take your word for it — they read your commits. Beyond evidence, git is how security work is actually done: you will clone tools, read their history to understand a vulnerability's introduction (`git log -S`, `git blame`), submit fixes as pull requests, and keep your notes under version control so no ransomware, dead laptop, or `rm -rf` takes them. Learn it now, properly, and it disappears into the background of everything else.

## 2. Before you start

- `git` installed (verify: `git --version` — the walkthrough used 2.43.0).
- A GitHub account (free). The walkthrough's "remote" is a local bare repository — identical mechanics, no network — and the GitHub-side steps are marked not-run for you to do on your account.
- Set your identity *locally per repo* (`git config user.name`), never `--global` on a shared machine.

## 3. How it works

Most version control tracks *changes*. Git tracks **snapshots**. Every commit is a complete picture of your files at that moment, identified by a SHA-1 (moving to SHA-256) hash of its contents. This one design decision explains nearly everything: history is a chain of snapshots, branching is cheap (it's just a pointer), and the entire repository — full history — lives in every clone. There is no central server in git's model. GitHub is a convenient place to put a clone everyone can reach; the protocol doesn't need it.

Three places hold your work, and confusing them is the #1 beginner failure:

1. **Working tree** — your files, as you edit them.
2. **Staging area (the index)** — the draft of the next commit. `git add` copies file states here; nothing is recorded until you commit.
3. **Repository (`.git/`)** — the committed snapshots, immutable.

`git status` tells you which files live in which place at any moment. Read it constantly until you don't need to.

A **commit** is an object: the snapshot (a tree hash), the parent commit(s), author/committer, timestamp, message. Its hash covers all of that — change one byte of history and every downstream hash changes, which is why history is tamper-evident and why "rewriting history" is a deliberate, visible act. A **branch** is a file containing a hash — a movable pointer to a commit. `main` is not special to git; it's a pointer that moves forward with each commit. Merging moves pointers and records the union in a merge commit. `HEAD` is the pointer to "where you are" (usually a branch, hence `ref: refs/heads/main`).

**Remotes** are just named clones. `origin` is the conventional name for where you cloned from. `git push` sends your commits to the remote's branch; `git fetch` brings theirs to yours (as `origin/main` — a *remote-tracking* branch, read-only by convention); `git pull` is fetch + merge. The walkthrough proves remotes need no network: a bare repository (`git init --bare` — no working tree, the server form) at a local path behaves exactly like GitHub for push/clone purposes.

**GitHub** adds the social layer git lacks: **forks** (your server-side clone of someone else's repo), **pull requests** (a proposal: "merge my branch into yours," with discussion, review, and CI), **issues**, and identity. The pull request is the smallest professional artifact in open source — and the mechanism behind coordinated disclosure contributions, tool fixes, and every "good first issue" you'll ever take.

The undo ladder, in order of destructiveness — learn this before you need it: `git restore <file>` (working tree back to staged), `git restore --staged <file>` (unstage, keep the file), `git commit --amend` (fix the last commit, only if unpushed), `git revert` (a *new* commit that undoes — the safe choice for shared history), `git reset` (moves the branch pointer — rewrites history; never on pushed commits). When in doubt, `revert`. The reflog (`git reflog`) records where your pointers *were* — the safety net under every mistake for ~90 days.

History is also an investigation tool, and this is where git pays rent in security work. `git log -S 'suspicious_string'` finds every commit that added or removed a string — the fastest way to answer "when did this vulnerable code appear?" `git blame` annotates each line with its last-modifying commit. A CVE fix's commit message names the flaw; the *parent* of that commit shows you the vulnerable code. Reading a project's history this way is a legitimate, quiet form of vulnerability research — and it's why the "Prove it" artifacts in later lessons ask for write-ups, not just findings.

And the rule this program cares about most: **never commit secrets.** API keys, private keys, tokens — once pushed, they're compromised; deleting the file doesn't purge history (`git filter-repo` exists for the cleanup, but rotation is the real fix). `.gitignore` lists what git must never track, and it goes in *before* the first commit containing anything sensitive.

### Worked example: a repo's whole life in seven minutes

From the walkthrough (§4): `git init -b main` creates the repository — note `.git/` appears and nothing else changes. Identity is set locally. `README.md` written, `add`ed (status shows `A`: staged, new), committed: `5ca7088`. A second change staged selectively — `closed.txt` stays untracked (`??`) while `README.md` is staged (`M `): staging is a *draft*, and you choose what goes in it. A branch `add-service-names` diverges, gets a commit, merges back with `--no-ff`: the graph shows the merge commit with two parents — the history now *records that a branch existed*, which is documentation. A bare repo becomes `origin`; push sends the commits; a fresh clone arrives with full history and `main` tracking `origin/main`. Inside `.git`: `HEAD` says `ref: refs/heads/main`, `refs/heads/main` contains `4b4281e…` — a branch is a 41-byte file. `git cat-file -p HEAD` shows the commit object: tree, two parents, author, message. The undo ladder demonstrated twice: `restore` for the working tree, `restore --staged` for the index. Every abstraction in the paragraphs above was a file you read or a command you ran.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/a-git-github.log`. Clean environment: git 2.43.0, all repos under `/tmp/gitwalk`, 2026-10-09. The GitHub-side step is marked not-run (no authentication here).

1. **Create a repository.** `git init -b main`, set identity locally. Write `README.md`, `git add`, `git status --short` (read the `A`), `git commit`, `git log --oneline`.
2. **Learn the staging area.** Modify `README.md`, create `closed.txt`; `git status --short` shows ` M` and `??`. `git add README.md` only — `closed.txt` stays out. Commit. Explain what the index held at each step.
3. **Branch and merge.** `git switch -c add-service-names`, commit there, `git switch main`, `git merge --no-ff`. Read the graph: the merge commit's two parents.
4. **Add a remote without the internet.** `git init --bare lab-remote.git`, `git remote add origin <path>`, `git push -u origin main`. Fix the bare repo's HEAD (`symbolic-ref HEAD refs/heads/main` — bare repos default to `master`). Clone it fresh: full history, tracking set up.
5. **Look inside.** `cat .git/HEAD`, `git rev-parse HEAD`, `git cat-file -p HEAD` (tree, parents, author), `cat .git/refs/heads/main` — the branch as a file.
6. **Undo at two levels.** Dirty the working tree → `git restore` (gone). Stage a change → `git restore --staged` (unstaged, file kept). Say which of `revert`/`reset` you'd use on a pushed mistake and why.
7. **GitHub — not run by us.** No authentication on this machine. On your account: fork a repo, clone *your fork*, branch, commit, push, open a pull request. And add a `.gitignore` before your first real commit — that's where secret leaks are born.

## 5. On your own

**Task:** Create a public GitHub repository called `security-notes`. Push your Bandit notes from `a-linux-cli` (one commit per level, messages describing what you learned). Then: (a) fork `OWASP/www-community` (or any repo you read), clone your fork, fix one typo in a page you actually read, push, and open a pull request; (b) add a `.gitignore` that excludes `*.key`, `*.pem`, and `.env`.

**Success test:** The repo shows a commit history a stranger can read as a learning record; the PR is open with a description explaining *what* you changed and *why*; `git status` shows a clean tree with the `.gitignore` committed.

**Hints:** `gh repo create` and `gh pr create` do the GitHub side from the terminal if you install the GitHub CLI — but do it once in the browser first so you know what the CLI is doing for you.

## 6. Where it goes wrong

- **Committing secrets.** The #1 git disaster. Tokens in history are compromised even after deletion — rotate them, then clean with `filter-repo`. Prevention (`.gitignore` first) beats cure.
- **`git push --force` on shared branches.** Rewriting history someone else has pulled corrupts their clone. Force-push only your own unshared branches; use `revert` for shared ones.
- **Committing everything with `git add .`** — including the 2GB packet capture, the `.env`, the private key. Stage selectively; `git status` before every commit until it's reflex.
- **Merge conflicts committed blindly.** Conflict markers (`<<<<<<<`) in pushed code mean someone "resolved" by accepting both. Read the conflict, understand both sides, then mark resolved.
- **Huge files in git.** Git snapshots whole files — a 500MB pcap in history makes every clone download it forever. Git LFS exists for this; better, don't commit captures at all (notebooks describe them; artifacts stay out).
- **No identity or a joke identity on professional work.** `user.name`/`user.email` are attached to every commit you will ever show anyone. Set them per repo, for real.
- **Treating GitHub as a backup instead of a publication.** Private repos for notes are fine; but the evidence this program builds toward is *public* — a stranger must be able to read it. Default new learning repos to public unless there's a reason not to.

## 7. Read the source

Primary documents first — the project's own docs:

- **Pro Git, chapters 1–3** (git-scm.com/book/en/v2 — verified 2026-10-09; Creative Commons licensed, free to read) — *read* 1.3 (what git is — snapshots not differences), 2.2 (recording changes — the three states), 3.1–3.2 (branching in a nutshell, basic branching/merging); *skim* 2.5 (remotes); *skip* the server chapters until you run one.
- **Pro Git, chapter 10** (Git Internals) — *read* 10.2 (Git objects) and 10.3 (references) after the walkthrough's step 5; *skim* the rest. This is the level-4 door.
- **Git reference** (git-scm.com/docs — verified 2026-10-09) — not reading material; the lookup habit. `git help <command>` is the same content offline.

Then at most three free resources:

1. **Pro Git, full book** (same URL above) — the one deep resource; chapters 5–6 (distributed workflows, GitHub) when you do step 7 for real.
2. *(Second slot intentionally empty — the book plus the reference are complete. Interactive git visualizers go in the directory, not the lesson.)*

## 8. Check yourself

1. `git status` shows `M README.md` (staged) and ` M notes.txt` (unstaged, leading space). Explain exactly what a commit right now would record, and the two commands that would change the answer.
2. You pushed a commit containing an API key, then deleted the file in the next commit and pushed again. Explain why the key is still compromised, and name the two things you must do (one about the key, one about the history).
3. A branch pointer is a file containing a hash. Explain what `git merge --no-ff feature` does to pointers and objects, and why the graph still shows the branch existed after it's deleted.
4. Your clone's `origin/main` is behind your local `main`, and a teammate's push added commits to `origin/main`. Explain what `git pull` does mechanically (two operations), and what could go wrong if you had local commits too.
5. Explain why `git revert` is safe on shared history but `git reset --hard` is not — using the words "pointer" and "object" correctly.

## 9. Prove it

**Artifact:** your public `security-notes` repository: Bandit notes (one commit per level), the `.gitignore`, and the merged-or-open pull request to a real project. The commit messages alone should narrate your learning.

**Honest claim:** "I keep my work in version control, collaborate through forks and pull requests, read history to understand how code evolved, and never commit secrets."
**Can't claim yet:** "I can do advanced git surgery" — interactive rebase, bisect-driven debugging, and history rewriting are the level-4 extension (Pro Git ch. 7); this lesson built the daily workflow.

## 10. Leads to

- `a-http-depth` — the Stage A milestone: your lab server, your packet notes, your repo — everything converges on narrating one login packet by packet.
- Stage B (later): every vulnerability lesson's "Prove it" expects a write-up committed to your repo; `git log -S` and `git blame` become investigation tools for finding when a flaw was introduced.
- The recognition pathway (the site's bet): this lesson built the *medium* — public, timestamped, checkable evidence. Every later artifact travels through it.
