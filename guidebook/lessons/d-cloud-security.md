---
lesson_id: d-cloud-security
slug: cloud-security
stage: D
level: 3
prerequisites: [a-tcpip-ports, b-ssrf, e-risk-assessment]
roles: [cloud-security, iam-engineer]
map_refs: []
test_date: 2026-10-09
description: "Cloud security: the shared-responsibility line, IAM policies read as code, the classic misconfigurations, and posture auditing with Prowler and ScoutSuite — policies analyzed for real with Cloudsplaining. A free hands-on lesson in the security guidebook."
dateline: "Walkthrough run 2026-10-09 · local IAM policy analysis with Cloudsplaining; live-account scanning is reader-side in their own account"
---
# Cloud security: concepts


**Map refs:** serves the Stage D cloud-security specialist track; cloud logging feeds `c-log-sources`; the posture assessment is the track's level-4 capstone input.

---

## 1. Where this shows up

Most "cloud breaches" are not breaks of the cloud — they are misconfigurations by the customer: a storage bucket left public, a firewall rule opened to the world, an access key committed to a repo, a trail left disabled. Cloud security work is therefore mostly *configuration* work: knowing the shared-responsibility line, reading identity policies the way you read code, and auditing an estate against a benchmark with tooling. Every cloud role — engineer, auditor, responder — starts from this lesson.

## 2. Before you start

- **Authorization:** everything hands-on here runs against files on your own machine (IAM policies you write) or your *own* cloud lab account with a read-only audit role. You never scan, audit, or test an account you don't own — a misconfigured bucket belonging to someone else is a finding for *their* disclosure process, not your playground. Prowler and ScoutSuite steps are reader-side against your own account; this lesson marks them and gives the exact commands.
- You understand what a firewall rule filters (`a-tcpip-ports`) and why instance metadata matters (`b-ssrf`).
- You can write a finding with root cause and remediation (`e-risk-assessment`) — every misconfiguration below becomes one.
- Tooling: Python 3, the `cloudsplaining` package (used in the walkthrough; install command in the lesson). No cloud account needed for the walkthrough.

## 3. How it works

### The shared-responsibility line

Every major provider publishes the same deal with different words. AWS's phrasing is the clearest: AWS takes **security *of* the cloud** — the hardware, software, networking, and facilities that run the services. You take **security *in* the cloud** — what you put there and how you configure it. The line moves with the service model: on EC2 (infrastructure as a service) you own the guest OS, patching, the application, and the security-group firewall rules; on S3 or DynamoDB (abstracted services) AWS owns everything up to the API, and you own your data, its encryption, its classification, and who may touch it via IAM. Then there are **shared controls**, where both sides implement their own half — patch management (AWS patches the infrastructure, you patch your guest OS), configuration management, training — and **inherited controls** you get for free, like physical security of the data centers. The professional habit: for any breach scenario, first ask *which side of the line it sits on*, because that decides who fixes it.

### Cloud IAM: the policy is the perimeter

In the cloud there is no network edge to hide behind — identity *is* the perimeter. An IAM policy is a JSON document with an effect (`Allow`/`Deny`), actions, and resources. Three ideas do most of the work. **Least privilege**: a principal gets exactly the permissions its job needs, nothing more — the sentence is easy, the practice is a continuous negotiation. **Policy evaluation logic**: an explicit `Deny` beats any `Allow`; without any `Allow`, the default is deny. **Privilege-escalation paths**: over-broad permissions compose — `iam:PassRole` plus `ec2:RunInstances` can become full admin, because the role you pass might be the admin role. This is why policy review is reading, not skimming: the dangerous policies are the ones that *look* narrow.

### The classic misconfigurations

Each of these has the same shape — how it happens, how attackers find it, how defenders detect it:

- **Public storage bucket.** Happens with one checkbox or one policy statement. Found by scanners that enumerate predictable bucket names. Detected by the provider's own access logging and by posture tools flagging `public-read`.
- **Security group open to 0.0.0.0/0.** Happens during debugging ("just open it temporarily") and stays. Found by port-scanning the estate's public IPs. Detected by posture checks on ingress rules.
- **Disabled audit trail.** CloudTrail (AWS), Activity Log (Azure), Audit Logs (GCP) are the control plane's memory — who called which API, when, from where. Disabled, there is no record of the attacker's API calls. Attackers disable it first (Defense Impairment, `d-redteam-concepts`). Detected by the *absence* check: the posture tool asks "is the trail on in every region?"
- **Long-lived credentials.** Access keys that never rotate, committed to repos, embedded in apps. Found by secret scanners and by the provider's own credential reports. The fix is roles and short-lived credentials, not better-hidden keys.
- **Overly permissive IAM.** `Action: "*"` on `Resource: "*"` — the policy that ends every argument. Found by policy analyzers; exploited via escalation paths.

### Auditing with tooling: Prowler and ScoutSuite

Two free tools do the heavy lifting, and they answer different questions. **Prowler** (open-source, Apache-2.0; verified 2026-10-09) runs hundreds of CIS-benchmark-mapped checks against your account and reports pass/fail per check — it answers *"what violates the benchmark?"* **ScoutSuite** (open-source, GPL-2.0; verified 2026-10-09) takes a point-in-time snapshot of the whole account and renders it as a browsable HTML report — it answers *"what does this estate actually look like?"* The workflow the lesson teaches: run Prowler for the check list, run ScoutSuite for the picture, then **verify every automated finding by hand** in the console before writing it up — the brief's rule that automated findings are confirmed by hand applies to cloud posture exactly as it does to vulnerability scanners. A finding the tool misread (a bucket that looks public but isn't, an open rule scoped to a load balancer) is a false positive you own if you report it.

### Cloud logging: the control plane remembers

CloudTrail / Activity Log / Audit Logs record API calls — the *management* plane, not the data plane. Attacker actions look like API calls: `CreateAccessKey`, `PutBucketPolicy`, `StopLogging`, `AssumeRole` from a new IP. Detection is log logic: alert on high-risk API calls, on calls from impossible geographies, on the trail going silent. The responder's first question in a cloud incident is always "show me the API history" — which is why the disabled-trail misconfiguration is the one that blinds everything downstream.

### Worked example: the bucket, end to end

Fictional company Northwind Traders, fictional estate. Posture scan flags: S3 bucket `northwind-invoices` with a policy granting `s3:GetObject` to `Principal: "*"`. Classification: customer-side (data + permissions are *in* the cloud). Mechanism: one policy statement made every object world-readable; bucket names are guessable, so discovery is trivial. Impact in business terms: customer invoices readable by anyone who guesses the name — the disclosure write-up from `e-risk-assessment` applies directly. Remediation: remove the wildcard principal, scope to the application's IAM role, enable access logging, add the posture check to the recurring scan. Verification: re-run the check, attempt anonymous `GetObject` (denied), confirm the invoice app still reads via its role (the fix must not break the app — the lesson from `b-idor` carries over). One misconfiguration, one finding, one fix, one verification — that is the unit of cloud security work.

## 4. Walkthrough

**Run by us** on this machine — transcript: `runs/d-cloud-security.log`. Clean environment: stock Python 3.12, `cloudsplaining` in a venv, no cloud account, 2026-10-09. The live-account scanning steps are reader-side and marked.

**Step 1 — Write three policies.** Create `policies/`: `correct.json` (a deployment role allowed `s3:GetObject`/`s3:PutObject` on one bucket prefix only), `overbroad.json` (same role plus `iam:PassRole` on `*`), `broken.json` (`Action: "*"` on `Resource: "*"`):
```
mkdir -p ~/tmp-guidebook/cloud/policies && cd ~/tmp-guidebook/cloud
# (three policy files written here - see log for contents)
```

**Step 2 — Analyze them with Cloudsplaining.** Cloudsplaining's `scan` expects an IAM *account authorization details* file (the shape of `aws iam get-account-authorization-details`), not bare policies — wrap the three policies in a minimal fixture with one role (`account-details.json`; the log shows the fixture). Then scan:
```
/tmp/yaravenv/bin/cloudsplaining scan -i account-details.json -o results-acct -s
```
Expected: `demo-correct` reports zero escalation findings; `demo-overbroad` flags `CreateEC2WithExistingIP` via `iam:PassRole` + `ec2:RunInstances` — the exact escalation path from the lesson; `demo-broken` flags multiple escalation methods (`CreateAccessKey`, `CreateLoginProfile`, …). The tool reads the policy the way the lesson teaches you to read it — the walkthrough is the habit, automated. (First attempt at bare-policy scanning failed honestly in the log: wrong input shape, corrected.)

**Step 3 — Classify responsibility.** Five fictional scenarios; write the classification with one line of reasoning each: (1) hypervisor vulnerability in the provider's fleet → provider; (2) EC2 instance unpatched for six months → customer; (3) S3 bucket policy with wildcard principal → customer; (4) provider employee accesses customer data → provider (physical/personnel controls are inherited); (5) customer disables CloudTrail, attacker wipes logs → customer — and note the shared-control nuance: the *capability* to log is the provider's, the *decision* to enable it is yours.

**Step 4 — The misconfiguration log.** Write the fictional before/after for the worked example's bucket: the offending policy statement, the fixed statement, the verification commands and their expected outputs. No CLI here by design — the artifact is the finding write-up, and the log records its authoring.

**Step 5 — Posture scan (reader-side).** Against **your own** lab account with a read-only audit role: `prowler aws` (Prowler CLI — install via pip per the project's docs; verify the version with `prowler --version`), then `python scout.py aws` (ScoutSuite). Remediate the top 5 findings, re-run, and record the delta. Running these here is **not run by us** — there is no cloud account on this machine, and scanners run only against accounts you own.

**Step 6 — Verify by hand.** Pick two findings from any scan output (or the walkthrough's policies) and confirm each in the provider console before writing it up. The log records the checklist; the habit is the deliverable.

## 5. On your own

Take the `overbroad.json` policy from the walkthrough and write the privilege-escalation path it enables as a three-step chain (which API calls, in which order, ending in what permission). Then write the minimal fixed policy. Success test: Cloudsplaining reports no escalation findings on your fixed policy, and a second reader can follow your three steps without asking what any call does.

## 6. Where it goes wrong

- **Scanning someone else's account.** "It's just a read-only scan" is not authorization. The scanner authenticates as *you* against *their* estate — that is the line.
- **Trusting the scanner's verdict.** A bucket flagged public that serves only through CloudFront with an origin-access identity is not public. Every automated finding gets a console check before it becomes a report line.
- **The temporary rule.** Security groups opened "just for debugging" are the most common finding in every estate audit because temporary has no expiry date. The fix is process (time-boxed rules, reviewed weekly), not memory.
- **Keys in code.** Rotation doesn't help if the new key goes to the same repo. The fix is eliminating the long-lived credential, not managing it better.
- **Confusing the shared line.** "The provider handles security" is the sentence behind most cloud breaches. The provider handles *their* half. Your half is the larger one in practice.
- **Tool version drift.** Prowler's check counts move fast (hundreds of checks across providers at the time of writing) — record the tool version and the benchmark edition with every assessment.

## 7. Read the source

Primary, in this order:
1. **AWS Shared Responsibility Model** (aws.amazon.com/compliance/shared-responsibility-model/) — read the "Security of the Cloud" vs "Security in the Cloud" split, then the inherited/shared/customer control examples. One page; it is the whole mental model.
2. **Prowler repository** (github.com/prowler-cloud/prowler) — read the README's description and the check/framework table to see what an assessment covers; note the CLI-first workflow.
3. **ScoutSuite repository** (github.com/nccgroup/ScoutSuite) — read the description: point-in-time, API-gathered, offline-after-collection, HTML report. Understand *why* that shape fits audits.

Free resources for going deeper (at most three):
- **CIS Benchmarks** (free PDFs) — the actual check definitions behind Prowler's CIS-mapped checks; name the benchmark edition you audit against. *For: knowing what each check asserts.*
- **Cloudsplaining** (open-source IAM policy analyzer) — the walkthrough's tool; run it on every policy you write. *For: the reading habit, automated.*
- **Stratus Red Team** (github.com/DataDog/stratus-red-team) — cloud adversary emulation for a dedicated sandbox account; the "what to look for" catalog for the detection half. *For: learning cloud attack paths safely, sandbox-only.*

## 8. Check yourself

1. A startup runs its app on EC2, stores uploads in S3, and uses a managed database. A breach exposes the uploads. List every layer of the stack and mark each "provider" or "customer" — then say which single misconfiguration is the most likely cause and why.
2. A policy allows `s3:*` on `arn:aws:s3:::app-bucket/*` but nothing else. Is this least privilege? What breaks if you narrow it to `s3:GetObject`, and what risk remains if you don't?
3. CloudTrail is enabled but the attacker deleted the log files from the S3 bucket. Which half of the shared model failed, and what control would have preserved the evidence?
4. Prowler flags 40 findings; ScoutSuite's HTML shows 3 of them are on resources scheduled for deletion next week. How do you prioritize, and what do you write for the 3?
5. Your scan finds an access key last used 400 days ago. Walk through the response: verify, assess, remediate, and prevent — in that order.

## 9. Prove it

**Artifact:** a posture mini-assessment of the walkthrough's fictional estate: the three analyzed policies with Cloudsplaining output, the five scenario classifications, and the bucket finding written as a full report entry (root cause, impact in business terms, remediation, verification).

**You can honestly claim:** you can classify cloud responsibility, read IAM policies for escalation paths, run posture tooling, and write cloud findings that get fixed. **You cannot yet claim:** you have assessed a real estate — that needs your own lab account and the reader-side scan, with findings verified by hand.

## 10. Leads to

- `c-log-sources` — cloud audit logs as a detection source; this lesson's logging section is the reason those logs exist.
- `c-incident-response` — the cloud incident: API history first, containment second.
- `e-risk-assessment` — the finding write-up format this lesson reuses.
- Map: Stage D cloud track (responsibility → IAM → misconfigurations → posture assessment with Prowler/ScoutSuite → cloud logging → attack-path concepts) → level-4 capstone: full CIS-benchmark assessment of a lab account, published.
