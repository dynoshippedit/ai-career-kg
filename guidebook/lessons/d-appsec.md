---
lesson_id: d-appsec
slug: appsec
stage: D
level: 3
prerequisites: [a-http-depth, e-sdlc, a-python-security]
roles: [appsec]
map_refs: ["CISSP 8.1", "CISSP 8.2", "CISSP 8.3", "CISSP 8.4", "CISSP 8.5"]
test_date: 2026-10-10
description: "Application security: STRIDE threat modeling, the SAST/DAST/IAST/SCA scanner families and their blind spots, secure-SDLC integration, and code-review technique — with a scanner-blind-spot demo run locally. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · STRIDE worked case + teaching-sketch SAST with triage; real Semgrep step re-ran 2026-10-10; ZAP step is reader-side"
---
# Application security: concepts


**Map refs:** serves the Stage D AppSec specialist track; the hands-on techniques for **CISSP objectives 8.1–8.5** (secure software: design, verification, acquired software — governance taught in `e-sdlc`, tooling taught here).

---

## 1. Where this shows up

Someone has to make sure the software gets *built* securely, not just tested after release. Application security is that discipline: threat modeling before code, scanners and reviews during development, verification before release. It is where the Stage B vulnerability classes meet the development process — every SQL injection you learned to find becomes a SAST rule, a code-review checklist item, and a threat-model entry. AppSec engineers, security champions, and consultants do this work; every developer-adjacent security role touches it.

## 2. Before you start

- **Authorization:** everything hands-on here runs against code you write or training apps you run locally (Juice Shop, WebGoat). You review and scan your own code or code you are explicitly authorized to assess. Scanning or testing someone else's application without written scope is not AppSec; it is unauthorized testing.
- You recognize the Stage B vulnerability classes cold — a scanner's output is meaningless if you can't judge whether its SQL-injection finding is real.
- You know the secure-SDLC shape from `e-sdlc`: this lesson is the verification-phase tooling that program deploys.
- You can write small Python scripts (`a-python-security`) — the walkthrough's teaching scanner is one you build yourself.
- Tooling: Python 3 (stdlib only). Real SAST (Semgrep) and DAST (OWASP ZAP) steps are reader-side with exact commands; the walkthrough runs a labeled teaching sketch so the *triage* skill is practiced honestly here.

## 3. How it works

### Threat modeling with STRIDE: design-time security

Threat modeling happens at design time, not test time: you model the system, enumerate what can go wrong, and turn the answers into requirements before code exists. The OWASP cheat sheet frames it as four questions — *what are we working on? what can go wrong? what are we going to do about it? did we do a good enough job?* — and the standard technique for the second question is **STRIDE**, six prompts applied to every component, data flow, and trust boundary in your data-flow diagram. A **trust boundary** is where data crosses from one trust level to another — browser to server, app to database, your code to a third-party service; everything crossing it is suspect until checked. The six prompts are not arbitrary: each one threatens a different security property (spoofing → authentication, tampering → integrity, repudiation → accountability, information disclosure → confidentiality, denial of service → availability, elevation of privilege → authorization), which is what makes the enumeration systematic instead of a brainstorm:

| Letter | Threat | Violates | Example |
|---|---|---|---|
| **S**poofing | Impersonation | Authentication | Attacker reuses a stolen session token |
| **T**ampering | Unauthorized modification | Integrity | Attacker edits a price parameter in transit |
| **R**epudiation | Denying the action | Accountability | Attacker wipes the logs covering their tracks |
| **I**nformation disclosure | Data exposure | Confidentiality | Error message leaks a database schema |
| **D**enial of service | Availability loss | Availability | Login endpoint abused for account lockout |
| **E**levation of privilege | Gaining more access | Authorization | JWT role claim tampered to admin |

Each identified threat gets a response — mitigate, eliminate, transfer, or accept — and mitigations become testable security requirements. The model is maintained as the system changes; a threat model written once and filed is decoration.

### The scanner families: what each can and cannot see

Four families, four different views of the same code. Know what each sees *and* what it is blind to — that is the professional skill; running the tool is the easy part.

- **SAST** (static application security testing) reads source or bytecode without running it: pattern matching plus taint tracking (this user input *flows* into that SQL query). **Sees:** known-bad patterns across the whole codebase, fast, in the IDE or CI. **Blind to:** anything runtime — authentication flows, business logic, configuration, and whether the flagged pattern is actually reachable. A SAST SQL-injection finding is a *candidate*, exactly like a scanner match in Stage B.
- **DAST** (dynamic) attacks the running app like Stage B testing, automated: crawls, injects, observes responses. **Sees:** real exploitable behavior, including config and auth issues SAST can't reach. **Blind to:** code it can't reach (uncrawled endpoints, authenticated areas without valid sessions), and anything requiring business understanding.
- **IAST** (interactive) instruments the running app — an agent inside the process watches data flow at runtime. **Sees:** the taint path *proven* by execution (SAST's precision plus DAST's proof). **Blind to:** everything outside the executed paths; needs the app running with realistic traffic.
- **SCA** (software composition analysis) inventories third-party dependencies and matches them against known CVEs. **Sees:** vulnerable libraries you'd never find by reading your own code. **Blind to:** your code entirely — and to whether the vulnerable function is actually called.

The lesson that organizes all four: *no family sees business logic.* A coupon that can be applied twice, a price taken from the client, a workflow skippable by URL-guessing — `b-business-logic` taught you these are found by *thinking*, and no scanner thinks. Anyone selling "full coverage" from tooling alone is selling the absence of exactly the flaws that cost the most.

### Secure-SDLC integration

Security gates fit the development phases: requirements get abuse cases (misuse scenarios: what an attacker would do with this feature, written as requirements the design must survive); design gets the threat model; implementation gets SAST in the IDE and pre-commit hooks (scripts that run checks automatically every time code is committed); verification gets DAST/SCA plus manual testing against the threat model; release gets the go/no-go on open findings; operations gets the feedback loop. The gates that survive are the ones that don't break delivery — a SAST gate that blocks every merge on 200 false positives gets disabled by Friday. Tuning (the Sigma lesson's false-positive discipline, applied to code) is what keeps gates alive.

### Code review technique

Review data flow first, trust boundaries second: where does untrusted input enter, where does it go, what validates it, what assumes it's safe? Read diffs with the vulnerability classes as a checklist (injection at every sink, auth on every new endpoint, crypto misuse at every new secret). Review findings are written for developers: location, what's wrong, why it matters (one sentence), the fix shape — never just "vulnerable." A finding a developer can't act on is a finding that doesn't get fixed.

### Worked example: STRIDE on "Acme Invoicer"

Fictional app: users log in, upload invoice PDFs, the server extracts totals, managers approve payments. Data-flow diagram: browser → web app → (auth service, file store, database). Trust boundaries: browser/app, app/auth-service, app/file-store.

STRIDE pass, one threat per letter with response:
- **S:** session token theft via XSS → mitigate: `HttpOnly; Secure; SameSite` cookies + CSP (from `b-xss`, `b-security-headers`).
- **T:** invoice total tampered in the approval POST → mitigate: server recomputes the total from the stored PDF; never trust the client's number (`b-business-logic`).
- **R:** approver denies approving a fraudulent payment → mitigate: append-only audit log of approvals with identities.
- **I:** PDF parser error messages leak temp paths → mitigate: generic error pages; parser runs sandboxed.
- **D:** login endpoint hammered for credential stuffing → mitigate: rate limiting + alerting (`b-session-auth`).
- **E:** `role` parameter in the profile endpoint → mitigate: server-side role from the session, never from the client (`b-idor`).

Six threats, six mitigations, each traceable to a Stage B lesson. That traceability is the point: the threat model *is* the Stage B curriculum applied at design time.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/d-appsec.log`. Clean environment: stock Python 3.12, 2026-10-09. The ZAP step is reader-side and marked; the SAST triage below uses a labeled teaching sketch so the skill practiced here is *judging findings*, which transfers to any scanner — and step 5 now shows the real Semgrep engine's output on the same fixture for comparison.

**Step 1 — Threat-model on paper.** Take the worked example's Acme Invoicer and add the file-upload flow: user → upload endpoint → virus-scan stub → file store → manager preview. Run STRIDE on the new flow only and write two threats with mitigations. No CLI by design — the log records the authoring; the artifact is the threat list.

**Step 2 — Build the teaching scanner.** Write `sketch_sast.py`: a small Python script that flags three patterns in Python source — string-concatenated SQL (`execute(` with `+`), hardcoded secrets (`password = "` / `api_key = "`), and weak hashes (`md5(` / `sha1(`):
```
python3 sketch_sast.py vuln_app.py
```
Expected: 3 findings with file:line locations (vuln_app.py:2 hardcoded secret, :6 string-concat SQL, :10 weak hash). The script is ~30 lines and the lesson says plainly what it is: pattern matching with no taint tracking, no data flow — a sketch of SAST's *dumbest* layer, not a scanner.

**Step 3 — Triage like a professional.** For each of the 3 findings, judge: true positive, false positive, or needs runtime context? Write one line each. Then add a *business-logic* flaw to `vuln_app.py` (a discount applied from a client-supplied parameter) and re-run the scanner:
```
python3 sketch_sast.py vuln_app.py
```
Expected: still 3 findings — the scanner is blind to the logic flaw, exactly as the lesson teaches. The triage notes plus the demonstrated blind spot are the artifact.

**Step 4 — Review the diff.** Read the provided `review.diff` (a 40-line pull request adding a password-reset endpoint) and write findings as for a developer: location, what's wrong, why it matters, the fix shape. The log records the review; expect at least: reset token in URL (logged/leaked), no rate limit, token not expired after use.

**Step 5 — Real SAST (run by us 2026-10-10).** The Semgrep 1.180.0 engine runs here (clean venv; the earlier "dead shim" report is superseded — transcript: `runs/d-appsec.log`). Real engine, local 4-rule file (registry `--config auto` needs login, so equivalent rules were written locally), against the step-2 `vuln_app.py` fixture: **4 findings** — the sketch's 3 pattern findings (hardcoded secret, string-concat SQL, md5) **plus** a taint-tracked flow (`user`/`pw` → `db.execute`) the sketch's pattern matching cannot see. Both the sketch and the real tool **missed the business-logic flaw** (client-controlled discount in `checkout()`) — the lesson's core point, now demonstrated against the real engine. On your own machine: `pipx install semgrep`, `semgrep login`, `semgrep ci` at your project root, and run the same comparison.

**Step 6 — Real DAST + SCA (reader-side).** Against your local Juice Shop: run OWASP ZAP's authenticated scan and OWASP Dependency-Check on the same app; reconcile both finding sets with your manual Stage B results in a short verification report noting what each method missed. Reader-side — **not run by us** here (no Docker on this machine).

## 5. On your own

Threat-model the login flow of any app you built in Stage B labs: draw the data-flow diagram (components, flows, trust boundaries), run STRIDE, and write the threat list with responses. Success test: every threat names the trust boundary it crosses, every mitigation is testable ("verify by…" with a concrete check), and at least one threat maps to each of the six STRIDE letters — if R or D comes up empty, that is a finding about your model, not a pass.

## 6. Where it goes wrong

- **Scanner worship.** "SAST is clean" means "no known patterns matched," not "secure." The walkthrough's step 3 exists to make this physical.
- **Gates that cry wolf.** An untuned SAST gate with hundreds of false positives gets disabled — and then you have no gate. Tuning is maintenance, not setup.
- **Threat-model theater.** A STRIDE session that produces only generic threats ("spoofing possible") with no data-flow diagram is a meeting, not a model. No DFD, no model.
- **Review as style policing.** Security review that bikesheds formatting while missing the auth check trains developers to ignore reviews.
- **SCA without reachability.** Flagging a CVE in a dependency whose vulnerable function is never called creates panic without risk. Reachability analysis (or a quick code read) comes before the ticket.
- **DAST without auth.** An unauthenticated crawl tests the login page thoroughly and the app barely. Authenticated scanning is a setup task, not an option.

## 7. Read the source

Primary, in this order:
1. **OWASP Threat Modeling Cheat Sheet** (cheatsheetseries.owasp.org) — read the four questions, the STRIDE table, and the cloud-threat-modeling section; it is the process this lesson teaches, from its authors.
2. **Semgrep documentation** (semgrep.dev/docs) — read the quickstart (install via pipx/uv, `semgrep login`, `semgrep ci`) to see the real tool's shape; note the login-centered flow.
3. **OWASP ASVS** (owasp.org/www-project-application-security-verification-standard) — the verification requirements catalog; skim the level structure to see what "verified" can mean at three depths. Skip the individual requirement text on first pass — open the catalog when you are writing requirements, not as reading.

Free resources for going deeper (at most three):
- **OWASP SAMM** (owaspsamm.org) — the maturity model for the AppSec program around the tooling; free, verified live 2026-10-09. *For: placing scanners inside a program instead of a toolbox.*
- **OWASP Code Review Guide** — the reviewer's reference for the technique in section 3. *For: the checklist behind step 4.*
- **PortSwigger Web Security Academy** — free labs for confirming scanner findings by hand. *For: the "automated findings are confirmed by hand" habit.*

## 8. Check yourself

1. Your SAST flags 50 SQL-injection candidates; manual review confirms 3. Your DAST finds 2 more the SAST missed, both in code the SAST scanned. Give two distinct technical reasons the SAST missed them.
2. A team proposes replacing code review with SAST + DAST "to move faster." Using the four families' blind spots, write the three-sentence rebuttal.
3. In the Acme Invoicer threat model, the file-upload flow crosses a new trust boundary at the virus-scan stub. Name one STRIDE threat specific to that boundary and a testable mitigation.
4. SCA flags a critical CVE in a library; the vulnerable function is dead code in your app. What do you do, and what do you write in the ticket?
5. Your threat model's mitigations are all "validate input." What does that tell you about the quality of the model, and what would you do in the review session?

## 9. Prove it

**Artifact:** the STRIDE threat list for the upload flow (step 1), the sketch-scanner triage notes including the demonstrated blind spot (steps 2–3), and a diff review written as developer-actionable findings — but not on the walkthrough's `review.diff`: pick a real recent commit or PR from your own Stage B lab code (or any code you are authorized to review) and review that instead. The walkthrough's artifacts stay in the log; this artifact proves the technique transfers to code the lesson didn't pick for you.

**You can honestly claim:** you can threat-model a small app with STRIDE, operate SAST and judge its output, and write security review findings developers can act on. **You cannot yet claim:** production scanner operation and tuning — that needs the reader-side Semgrep/ZAP work against a real codebase, which this lesson specifies but does not perform.

## 10. Leads to

- `e-sdlc` — the program that deploys this tooling: gates, champions (developers trained to carry security into their own teams), metrics.
- `c-sigma-detection` — the same triage discipline, applied to detection rules instead of code findings.
- Stage D capstone direction: threat-model, scan, and review a real open-source app; publish the assessment.
- Map: Stage D AppSec track (STRIDE → SAST/DAST/IAST/SCA → SDLC integration → code review → ASVS verification) — the hands-on half of CISSP 8.1–8.5, whose governance half lives in `e-sdlc`.
