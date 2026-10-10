---
lesson_id: e-ethics
slug: ethics
stage: E
level: 2
prerequisites: [ai-governance]
roles: []
map_refs: ["CISSP 1.1"]
test_date: 2026-10-10
description: "Argue real security-work dilemmas from the ISC2 Code of Ethics' four canons, in priority order. A free lesson in the security guidebook, serving CISSP objective 1.1."
dateline: "Worked case authored and reviewed 2026-10-10 · no command line in this lesson"
---
# Professional ethics in security work: the Code is the floor, not the ceiling


**Map ref:** serves **CISSP objective 1.1** — professional ethics in security work.

---

## 1. Where this shows up

Ethics in security work is not a graduation speech; it is a Tuesday-afternoon decision. A client asks you to soften a critical finding so a deal closes. During an engagement scoped to a web application, you notice the client's internet-facing VPN appliance is unpatched against a known critical flaw — out of scope, but you are the only person who knows. A bug bounty researcher finds a vulnerability in a hospital system and the vendor goes silent. A former colleague asks for "a quick look" at their new employer's network. Each of these is a moment where the technically correct move and the professionally right move are different things, and where "the client told me to" is not an answer. This lesson teaches the framework the profession uses to decide: the ISC2 Code of Professional Ethics, read as an instrument rather than a poster.

## 2. Before you start

- No technical prerequisites. This lesson is entirely about judgment.
- You have done real security work somewhere in Stages A–D — the dilemmas below will feel hypothetical until you map each one onto something you have actually seen.
- Bring the AI-ethics material from `ai-governance` (the canons applied to AI systems).
- The work product is writing: two dilemma analyses argued from the canons, each ending in a named decision.

## 3. How it works

Security practitioners hold asymmetric power: privileged access, knowledge of vulnerabilities, the ability to cause or prevent serious harm. The Code of Professional Ethics is the profession's answer to that asymmetry — a public commitment to use that power under constraints, with violations adjudicated by a peer review panel that can revoke certification. Read the ISC2 page itself (fetched for this lesson): adherence is a *condition of certification*, and members must follow the ethics complaint procedure on observing a breach by another member — looking away is itself a breach.

**The four canons, paraphrased.** The Code states there are only four mandatory canons, deliberately high-level — the page says plainly they are not a substitute for the professional's own ethical judgment. The preamble's ordering is a priority ordering (society first, then principals, then each other):

1. **Protect society, the common good, public trust, and the infrastructure.** The public interest outranks every private interest. When a client's request and the public's safety conflict, the public wins.
2. **Act honorably, honestly, justly, responsibly, and legally.** No dishonest reports, no fabricated data, no illegal acts even when ordered. Honesty here includes honesty about your own competence — taking work you cannot do well is a Canon II problem.
3. **Provide diligent and competent service to principals.** Your client or employer is owed real diligence: thorough work, competent methods, loyalty to their legitimate interests. Note "legitimate" — a principal's interest in deceiving others is not legitimate.
4. **Advance and protect the profession.** Do not damage the field's credibility; mentor, share knowledge responsibly, and hold peers to the standard (this is the canon behind the duty to report observed breaches).

The ordering matters more than the wording. Canon I over Canon III is the entire theory of the Code in one line: your duty to the public outranks your duty to the person paying you. Most real dilemmas are a lower canon pulling against a higher one, and the Code's answer is almost always the higher canon.

**How the canons resolve conflicts.** The Code contains no algorithm — the ISC2 page says so explicitly, and the ACM Code says the same about itself: a code is a basis for ethical decision-making, with the public good paramount. The working method: (1) name the stakeholders; (2) name which canon each possible action serves or violates; (3) apply the priority ordering; (4) check whether the "compromise" actually satisfies the higher canon or merely delays violating it. Step 4 is where most rationalizations die — "I'll report it quietly later" usually means "I'll never report it."

**The ACM comparison.** The ACM Code of Ethics and Professional Conduct (2018) organizes the same territory differently: general principles (contribute to society, avoid harm, be honest, be fair, respect privacy, honor confidentiality), professional responsibilities, leadership, and compliance. Two contrasts matter. First, ACM's "avoid harm" explicitly includes reporting signs of system risks — and considering whistleblowing if leaders do not act — which maps directly onto disclosure dilemmas. Second, ACM's "honor confidentiality" holds *except* in cases of law, regulation, or Code violations, with disclosure only to appropriate authorities. Both codes converge: broad duties to society first, confidentiality and loyalty second, with defined escape hatches.

**What the Code does not do.** It does not give you the answer to any specific dilemma — that is your judgment. It does not override the law (Canon II requires legal conduct as a minimum). It does not protect you from the consequences of refusing an unethical order; it tells you which consequences to accept. And it is not the only code in the room: when codes conflict, the Code's priority ordering is your tiebreaker, not your shield.

### Worked example: two dilemmas argued from the canons

**The setting (fictional).** You are an independent security consultant. Your client is "Northwind Freight" (fictional), a 300-person logistics company. The engagement is a scoped web-application assessment of their customer portal.

**Dilemma A — the out-of-scope finding.** Mid-engagement, while verifying the portal's IP ranges, you discover Northwind's internet-facing VPN appliance is running firmware with a publicly known critical remote-code-execution flaw — patched by the vendor nine months ago, exploit code widely available. It is outside your scope. The client's IT lead, when you mention it informally, says "yeah, we're aware, it's on the list" and changes the subject. Your scope document says findings outside the portal are not your deliverable.

Argue it from the canons. Canon III (diligent service): the client is served by a warning and harmed by silence — a compromised VPN endangers everything the portal assessment protects. Canon I (protect the infrastructure): a compromised logistics company becomes infrastructure for further attacks. Canon II (honest conduct): delivering a clean portal report while knowing the front door is open misleads by omission. The scope document is a contract term; no contract term outranks Canon I, and Canon II's honesty is not waivable by scope. The counter-argument — "not my job, they know, I'd overstep" — misreads Canon III as obedience. The Code asks for diligence, and diligence includes telling the principal what they need to hear.

Decision: put it in writing, formally, to the engagement sponsor (not just the IT lead), as an out-of-scope critical observation with the CVE reference and the patch, distinct from the scoped findings. Document the notification. If the client instructs you to remove it, that becomes Dilemma B.

**Dilemma B — the softened report.** The portal assessment finds a genuine critical: an authenticated endpoint that exposes other customers' shipment data, trivially exploitable, affecting the full customer base. Northwind's VP of Sales calls you: their largest prospect is doing vendor due diligence next week, and a critical finding "would kill the deal." The ask: downgrade it to medium, or move it to an appendix "for the next cycle." The implied offer is a follow-on engagement.

Argue it from the canons. Canon II is dispositive: a deliberately misrated finding is a dishonest work product, full stop. Canon I reinforces: other customers' data is exposed, and misrating prolongs the exposure of third parties who never consented to be part of a deal negotiation. Canon III is the trap: it looks like service, but the Code protects the principal's *legitimate* interests — deceiving a prospect is not one. Canon IV adds the professional dimension: every softened report degrades the credibility of every assessment, including your peers'. "Everybody does it" is specifically what Canon IV exists to reject.

Decision: refuse, in writing, with the reasoning stated plainly — the rating follows the evidence, and the report is a professional attestation, not a marketing document. Offer what *is* legitimate: an expedited retest after remediation, and a documented risk-acceptance path (per `e-risk-assessment` — acceptance needs an owner and a date; it is the client's decision to make openly, not yours to make for them by misrating). If the client terminates the engagement, that is a consequence the Code requires you to accept.

**The pattern.** Both dilemmas resolve the same way: identify the highest canon engaged, and refuse to trade it for a lower one. The Code's priority ordering does the work — which is why step one of the method is always "name the canons," not "weigh the feelings."

## 4. Walkthrough

**Worked-case lesson — no command line.** The "run" for this lesson is the two dilemma analyses above, authored and self-reviewed in-session on 2026-10-10 against the ISC2 Code of Ethics page (fetched 2026-10-10). Transcript: `runs/e-ethics.log` (records the dilemmas, the canon-by-canon arguments, the decisions, and the review checklist — there are no commands to transcribe).

1. **Read the Code itself.** Open the ISC2 Code of Ethics page and read the preamble and the four canons. Note the two load-bearing sentences: adherence is a condition of certification, and the canons are not a substitute for your judgment.
2. **Build your stakeholder map.** List every stakeholder before you argue: the public, the principal, the profession, yourself. Bad reasoning skips stakeholders who are not in the room.
3. **Argue canon by canon.** For each candidate action, walk the four canons in order, in writing. Unwritten ethical reasoning is where rationalization hides.
4. **Apply the priority ordering.** When canons conflict, the higher canon wins — state this explicitly.
5. **Name the decision and its cost.** Every honest ethical decision costs something. Name it. An analysis that costs the analyst nothing is a dilemma avoided.
6. **File it.** Keep your analyses. In a dispute, the contemporaneous written record beats your memory.

## 5. On your own

**Task:** Write a third dilemma analysis, argued canon by canon, for this scenario (fictional): doing research in your own lab, you realize a technique you developed would also work against a hospital's patient portal — no bounty program, no published disclosure contact. You have not tested it against the hospital. Walk the canons: what do you do with the knowledge, whom do you tell, and what do you *not* do (no testing against the hospital — its own Canon II legal-conduct problem)?

**Success test:** Your analysis names all four canons, applies the priority ordering explicitly, reaches a decision with a named cost to you, and includes the "what I will not do" section. If your decision is "do nothing," your analysis must show which canon permits that — and it will not survive the attempt, which is the point.

## 6. Where it goes wrong

- **Canon shopping.** Reading the four canons and picking the one that blesses the decision you already made. The priority ordering exists to prevent this — if your analysis never lets a higher canon overrule your preference, you are shopping.
- **Obedience as service.** Treating Canon III as "do what the client says." The Code asks for diligent, competent service to the principal's *legitimate* interests — not obedience. A client instruction to falsify a report is not a principal's interest the Code recognizes.
- **Scope as shield.** "It was out of scope" is a contract defense, not an ethical one. Canon I does not contain a scope clause.
- **The unreported peer.** Observing another member's breach and staying silent violates the complaint-procedure obligation. Solidarity runs toward the standard, not the person.
- **Competence theater.** Taking work beyond your competence — Canon II covers honesty about your own limits — then hiding behind the engagement's brand name.
- **Ethics as a poster.** A code quoted in a slide deck and never applied to a real decision. A code that has never cost anyone anything is decoration.

## 7. Read the source

Primary documents first:

- **ISC2 Code of Professional Ethics** (isc2.org/ethics) — *read* the preamble and the four canons; note the complaint-procedure obligation and the "not a substitute for judgment" line. This is the profession's enforcement document.

Then at most three free resources:

1. **ACM Code of Ethics and Professional Conduct** (acm.org) — free; the computing profession's parallel code — compare its "avoid harm" reporting duty and its confidentiality-with-exceptions structure against the ISC2 canons.
2. **ISC2 Ethics Complaint Procedures** (isc2.org) — free; what actually happens when a breach is reported: the peer review panel and revocation. Read this so the Code's enforcement is concrete, not abstract.

## 8. Check yourself

1. A client instructs you, in writing, to remove a critical finding from your report before it goes to their prospect's due-diligence team. Walk the four canons in order and state which canon is dispositive — and why the client's instruction does not change the answer.
2. During a scoped engagement you discover a critical flaw in an out-of-scope system, and the client's IT lead says they are aware of it. Explain why "out of scope" and "they know" are both insufficient as ethical defenses, naming the canons.
3. Compare the ISC2 and ACM codes on confidentiality: under what conditions does each permit (or require) breaking confidentiality, and to whom does the disclosure go?
4. A peer at another firm tells you they routinely downgrade findings to keep clients happy. What does the Code require of *you* in that moment, and which canon creates the requirement?
5. Predict the failure mode of a practitioner who treats Canon III (service to principals) as the highest canon: describe a realistic scenario where that ordering produces the wrong decision, and show how the Code's actual ordering fixes it.

## 9. Prove it

**Artifact:** your two dilemma analyses (the out-of-scope finding and the softened report, reproduced in your own words — or your own dilemmas from real work), each argued canon by canon with a named decision and a named cost, plus the "On your own" disclosure analysis.

**Honest claim:** "I can take a real security-work dilemma, argue it from a professional code's canons in writing, apply the priority ordering when canons conflict, and reach a decision I can defend — including when the decision costs me."
**Can't claim yet:** "I can navigate the legal exposure of whistleblowing or compelled disclosure" — where ethics meets employment law, criminal liability, and regulator procedure, you need counsel, not a code; this lesson taught the ethical reasoning, not the legal strategy.

## 10. Leads to

- **ai-governance — `ai-governance`** — the canons applied to AI systems: training data, automated decisions, deployment ethics.
- **c-cvd — `c-cvd`** — coordinated vulnerability disclosure in practice: the disclosure dilemma with real process around it.
- **b-bug-bounty — `b-bug-bounty`** — researcher ethics in bounty work: scope, disclosure, and the no-testing-without-permission line.
- Map refs: **CISSP 1.1** (this lesson); the canon method is reused in **1.4** (legal obligations) and **1.8** (personnel decisions).
