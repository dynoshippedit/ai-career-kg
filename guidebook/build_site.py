#!/usr/bin/env python3
"""Build the security guidebook section into the learncomputerstuff.dev static site.

Usage: python3 build_site.py
Reads:  lessons/*.md (the 10-part lesson spec, markdown + YAML frontmatter)
Writes: <repo>/g/<slug>/index.html  (one per lesson)
        <repo>/g/index.html          (guidebook entry page)

Brief §4: lessons are data. Every lesson file carries frontmatter
(lesson_id, slug, stage, level, prerequisites, roles, map_refs, test_date,
description, dateline); the registry, link map, counts, path membership,
stage listings and knowledge-map references are all generated from it.
The HTML reuses the site's own inline CSS verbatim (extracted from the homepage)
so design tokens, header, nav, footer and voice stay native. No external
dependencies. Re-run for future batches: add the lesson .md with frontmatter,
append its id to ORDER, run again.
"""
import html
import re
import sys
from pathlib import Path

GUIDEBOOK = Path(__file__).parent
REPO = Path(__file__).resolve().parent.parent  # site repo root (guidebook/ lives inside it)
TODAY = "2026-10-09"


def numword(n):
    """Small number-to-words for lesson counts (site voice uses words)."""
    ones = ["zero", "one", "two", "three", "four", "five", "six", "seven",
            "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
            "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
            "eighty", "ninety"]
    if n < 20:
        return ones[n]
    if n < 100:
        t, o = divmod(n, 10)
        return tens[t] + ("" if o == 0 else "-" + ones[o])
    h, rest = divmod(n, 100)
    return ones[h] + " hundred" + ("" if rest == 0 else " " + numword(rest))

# lesson id -> url slug
# ================= Lesson registry: generated from frontmatter =================
# Brief §4: lessons are data, one file each. Every lesson file carries YAML
# frontmatter with: lesson_id, slug, stage, level, prerequisites, roles,
# map_refs, test_date, description, dateline. Everything below is DERIVED from
# those fields. The only hand list here is ORDER (editorial sequence for the
# index page) — validated against the registry at load.
STAGE_LABELS = {
    "A": "Stage A · Foundations",
    "B": "Stage B · Practitioner",
    "C": "Stage C · Professional",
    "D": "Stage D · Specialist",
    "E": "Stage E · Expert",
    "AI": "AI track",
}

# Brief §1: the four levels every lesson states.
LEVELS = {
    1: ("Recognize", "name it and spot it"),
    2: ("Operate", "do it by following steps on a prepared target"),
    3: ("Apply", "do it unaided on an unfamiliar authorized target, and explain "
                  "why it worked and what would have stopped it"),
    4: ("Extend", "work from the primary sources, build or change the tooling, "
                   "find what the references miss, publish something others verify"),
}


def parse_frontmatter(md: str):
    """Minimal YAML-subset parser for lesson frontmatter. Handles flat
    key: value pairs and inline [a, b] lists; values may be double-quoted."""
    if not md.startswith("---\n"):
        return None
    end = md.index("\n---", 4)
    fm = {}
    for line in md[4:end].split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, val = line.split(":", 1)
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            items = []
            cur, in_q = "", False
            for ch in inner:
                if ch == '"':
                    in_q = not in_q
                elif ch == "," and not in_q:
                    items.append(cur.strip().strip('"'))
                    cur = ""
                else:
                    cur += ch
            if cur.strip():
                items.append(cur.strip().strip('"'))
            fm[key.strip()] = [i for i in items if i]
        else:
            if val.startswith('"') and val.endswith('"') and len(val) >= 2:
                val = val[1:-1].replace('\\"', '"').replace("\\\\", "\\")
            fm[key.strip()] = val
    return fm


def load_registry():
    """Read every lessons/*.md frontmatter block into the lesson registry,
    validating every field. Any inconsistency is a hard build error."""
    reg = {}
    for path in sorted((GUIDEBOOK / "lessons").glob("*.md")):
        md = path.read_text()
        fm = parse_frontmatter(md)
        if fm is None:
            raise SystemExit(f"build error: {path.name} has no YAML frontmatter")
        lid = fm.get("lesson_id") or ""
        if not lid:
            raise SystemExit(f"build error: {path.name} frontmatter lacks lesson_id")
        if lid != path.stem:
            raise SystemExit(f"build error: lesson_id {lid!r} != filename {path.stem!r}")
        if lid in reg:
            raise SystemExit(f"build error: duplicate lesson_id {lid!r}")
        for f in ("slug", "stage", "level", "test_date", "description", "dateline"):
            if f not in fm or fm[f] in ("", []):
                raise SystemExit(f"build error: {lid} frontmatter lacks {f}")
        if fm["stage"] not in STAGE_LABELS:
            raise SystemExit(f"build error: {lid} has unknown stage {fm['stage']!r}")
        try:
            fm["level"] = int(fm["level"])
        except ValueError:
            raise SystemExit(f"build error: {lid} has non-integer level")
        if fm["level"] not in LEVELS:
            raise SystemExit(f"build error: {lid} has level {fm['level']} (want 1-4)")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(fm["test_date"])):
            raise SystemExit(f"build error: {lid} has bad test_date {fm['test_date']!r}")
        for r in fm.get("roles", []):
            if r not in PATHMAP:
                raise SystemExit(f"build error: {lid} has unknown role {r!r}")
        for ref in fm.get("map_refs", []):
            if not (re.fullmatch(r"CISSP \d+\.\d+", ref) or re.fullmatch(r"CAISP ch\d+", ref)):
                raise SystemExit(f"build error: {lid} has bad map_ref {ref!r}")
        reg[lid] = fm
    # cross-file checks
    for lid, fm in reg.items():
        for p in fm.get("prerequisites", []):
            if p not in reg:
                raise SystemExit(f"build error: {lid} prerequisite {p!r} is not a lesson")
    if set(reg) != set(ORDER):
        raise SystemExit(
            "build error: ORDER != registry: "
            f"missing={sorted(set(reg) - set(ORDER))} extra={sorted(set(ORDER) - set(reg))}")
    return reg


# Canonical lesson order (editorial sequence for the index page).
# Data lives in frontmatter; this list is sequence only, validated at load.
ORDER = [
    "a-http-depth", "b-idor", "e-risk-assessment", "ai-prompt-injection", "a-dns-depth", "a-tcpip-ports", "a-linux-cli", "a-git-github",
    "b-sqli", "b-command-injection", "b-ssrf", "b-csrf", "b-xss", "b-business-logic", "b-session-auth", "b-security-headers",
    "b-bug-bounty", "c-soc-triage", "c-log-sources", "c-sigma-detection", "c-incident-response", "c-cvd", "c-cve-program", "c-cvss",
    "c-vuln-ecosystem", "e-iam", "e-crypto-applied", "e-sdlc", "e-bcp-drp", "e-ethics", "e-security-concepts", "e-governance",
    "e-cyber-law", "e-investigations", "e-policy-docs", "e-personnel-security", "e-threat-modeling-concepts", "e-supply-chain-risk", "e-awareness-training", "e-asset-classification",
    "e-handling-requirements", "e-asset-provisioning", "e-data-lifecycle", "e-retention-eol", "e-data-protection-controls", "e-secure-design", "e-security-models", "e-control-selection",
    "e-platform-security", "e-arch-vuln-assessment", "e-cryptanalysis", "e-facility-design", "e-facility-controls", "e-system-lifecycle", "e-network-architecture", "e-network-components",
    "e-secure-channels", "e-auth-systems", "e-assessment-strategy", "e-control-testing", "e-security-metrics", "e-test-analysis-reporting", "e-security-audits", "e-investigation-forensics",
    "e-logging-monitoring", "e-config-management", "e-secops-concepts", "e-media-protection", "e-incident-management", "e-detective-preventive", "e-patch-management", "e-change-management",
    "e-physical-security", "e-personnel-safety", "ai-llm-architecture", "ai-llm-top10", "ai-supply-chain", "ai-governance", "d-redteam-concepts", "d-malware-analysis",
    "d-cloud-security", "d-appsec", "b-authorization-scope", "b-methodology", "b-toolbench", "b-practice-targets", "a-python-security", "a-reading-code",
    "a-windows-concepts", "a-osint-research", "ai-pipeline", "ai-threat-modeling", "e-security-program", "e-board-communication", "d-dfir-deep", "d-exploit-concepts",
    "c-public-track-record", "c-ai-tooling", "e-csf-20", "e-iso27001", "e-soc2",
    "a-crypto", "b-api-abuse", "b-ssti", "b-xxe", "b-deserialization", "b-graphql",
    "b-race-conditions", "b-jwt-oauth", "ai-sec-automation",
]

# Stage pages (brief §4): the novice-to-expert backbone. Each row:
# (stage_key, slug, stage_label, title, lede, milestone_html, claims_html,
#  next_url, next_label, [lesson ids in reading order])
STAGES = [
    ("A", "stage-a", "Stage A · Foundations", "Stage A — Foundations",
     "The ground everything else stands on: how a computer runs programs and controls access, what actually crosses the wire when two machines talk, the protocol every web attack and defense is built on, enough Python to read and change the small tools the field runs on, how to follow a vulnerability through source code, and what the cryptographic primitives do — and what breaks when they are misused.",
     "Explain, <strong>packet by packet</strong>, what happens between pressing &ldquo;log in&rdquo; and the page rendering: the DNS lookup, the TCP handshake, the TLS handshake, the HTTP request and response, the cookie or token that carries identity, and the bytes on the wire at each step.",
     "After Stage A you can honestly claim: <strong>nothing yet</strong> — and that is the point. This is the brief's own reasoning, not a verdict on your effort: foundations are prerequisites, not proof of skill. The checkable evidence starts in Stage B. What you <em>can</em> say is that you can explain the login-to-render path from first principles, with no term you cannot unpack.",
     "/g/stage-b/", "Stage B — Practitioner",
     ["a-dns-depth", "a-tcpip-ports", "a-linux-cli", "a-windows-concepts",
      "a-git-github", "a-http-depth", "a-python-security", "a-reading-code",
      "a-osint-research", "a-crypto"]),
    ("B", "stage-b", "Stage B · Practitioner", "Stage B — Practitioner",
     "Doing the work under authorization: the hard rules and scope discipline that make everything legal, engagement methodology, the toolbench in activation order, the web vulnerability classes found, reproduced and fixed one by one, defensive basics, and how authorized testing is actually offered to beginners through bug bounty programs.",
     "A <strong>first valid finding submitted to a program that authorizes testing</strong> — in scope, reproducible by a stranger following your steps, with the impact argued honestly.",
     "You can honestly claim: you have found, reproduced, and fixed real vulnerability classes on targets you were authorized to test, and you can write a triage-ready report. You cannot yet claim: professional experience, any certification, or readiness for unsupervised work. Stage B is the <em>first</em> evidence, not the last.",
     "/g/stage-c/", "Stage C — Professional",
     ["b-authorization-scope", "b-methodology", "b-toolbench", "b-practice-targets",
      "b-idor", "b-api-abuse", "b-sqli", "b-command-injection", "b-ssrf", "b-csrf", "b-xss",
      "b-ssti", "b-xxe", "b-deserialization", "b-graphql", "b-race-conditions",
      "b-business-logic", "b-session-auth", "b-jwt-oauth", "b-security-headers", "b-bug-bounty"]),
    ("C", "stage-c", "Stage C · Professional", "Stage C — Professional",
     "Working like a professional: the defender's side — SOC triage, log sources, detection engineering, incident response — plus coordinated disclosure end to end, the CVE program and how credit works, severity scoring by hand, the vulnerability catalogs, and building the public track record the whole program's premise rests on.",
     "A <strong>coordinated disclosure completed</strong>, and a <strong>CVE record that credits you</strong> — a public, permanent entry with your name on it.",
     "You can honestly claim: you have reported a real flaw responsibly and can point to the public record; you can score severity and prioritize like a professional. You cannot yet claim: specialization depth — that is Stage D — or managerial breadth — that is Stage E.",
     "/g/stage-d/", "Stage D — Specialist",
     ["c-soc-triage", "c-log-sources", "c-sigma-detection", "c-incident-response",
      "c-cvd", "c-cve-program", "c-cvss", "c-vuln-ecosystem",
      "c-public-track-record", "c-ai-tooling"]),
    ("D", "stage-d", "Stage D · Specialist", "Stage D — Specialist",
     "One track, taken deep: red team operations, DFIR and detection engineering, application security, exploit development and reverse engineering, malware analysis, or cloud security. Each track is concepts plus defender telemetry plus established labs — the safety line holds all the way down.",
     "A <strong>capstone body of work in one track</strong>: original, public, verifiable — the level-4 work each role path ends in. (The brief sets no single artifact for Stage D; the milestone is the depth itself.)",
     "You can honestly claim: deep, demonstrable skill in one specialty, with public artifacts to prove it. You cannot yet claim: breadth across the field — the specialist knows their track cold and knows where its edges are.",
     "/g/stage-e/", "Stage E — Expert",
     ["d-redteam-concepts", "d-malware-analysis", "d-cloud-security",
      "d-appsec", "d-exploit-concepts", "d-dfir-deep"]),
    ("E", "stage-e", "Stage E · Expert", "Stage E — Expert",
     "Managerial and architectural breadth: the eight CISSP domains as bodies of knowledge, the governance frameworks organizations buy, and the work of the person who owns security — strategy, metrics, and board-level communication.",
     "<strong>Breadth across the whole field</strong>: you can reason about a security program end to end — risk, architecture, governance, leadership — from the primary sources.",
     "You can honestly claim: you have studied each CISSP domain's body of knowledge and can work from the primary sources. You cannot claim: the CISSP certification itself — full certification needs five cumulative years of experience in two or more domains (one year waivable by degree or approved credential); passing without it makes you an Associate of ISC2. Nor can you claim a title like CISO — these lessons teach the work, not the title.",
     "/g/", "The AI security track",
     ["e-risk-assessment",
      "e-ethics", "e-security-concepts", "e-governance", "e-cyber-law",
      "e-investigations", "e-policy-docs", "e-personnel-security",
      "e-threat-modeling-concepts", "e-supply-chain-risk", "e-awareness-training",
      "e-asset-classification", "e-handling-requirements", "e-asset-provisioning",
      "e-data-lifecycle", "e-retention-eol", "e-data-protection-controls",
      "e-secure-design", "e-security-models", "e-control-selection",
      "e-platform-security", "e-arch-vuln-assessment", "e-crypto-applied",
      "e-cryptanalysis", "e-facility-design", "e-facility-controls",
      "e-system-lifecycle",
      "e-network-architecture", "e-network-components", "e-secure-channels",
      "e-iam", "e-auth-systems",
      "e-assessment-strategy", "e-control-testing", "e-security-metrics",
      "e-test-analysis-reporting", "e-security-audits",
      "e-investigation-forensics", "e-logging-monitoring", "e-config-management",
      "e-secops-concepts", "e-media-protection", "e-incident-management",
      "e-detective-preventive", "e-patch-management", "e-change-management",
      "e-physical-security", "e-personnel-safety",
      "e-sdlc", "e-bcp-drp", "e-security-program", "e-board-communication",
      "e-csf-20", "e-iso27001", "e-soc2"]),
]

STAGEMAP = {key: f"/g/{slug}/" for key, slug, *_ in STAGES}

TLD = r"(?:education|college|org|com|dev|net|io|gov|se|uk|info|edu|eu|ch|ai|one|app|co)(?![A-Za-z0-9-])"
DOMAIN_RE = re.compile(
    r"(?<![\w/@])"                      # not mid-word, not inside an href
    r"(\()?((?:[A-Za-z0-9-]+\.)+" + TLD + r"(?:/[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]*)?)"
    r"(\))?"
)

def linkify(text: str) -> str:
    """Turn bare domain.tld/path tokens into real links. Assumes code spans
    and existing <a> tags are already protected as placeholders."""
    def sub(m):
        url = m.group(2).rstrip(".,;:!?")
        # A trailing ")" is the prose paren, not part of the URL, unless parens balance.
        while url.endswith(")") and url.count("(") < url.count(")"):
            url = url[:-1]
        trail = m.group(2)[len(url):]
        open_p, close_p = m.group(1) or "", m.group(3) or ""
        return f'{open_p}<a href="https://{url}">{html.escape(url)}</a>{trail}{close_p}'
    return DOMAIN_RE.sub(sub, text)

def inline(text: str) -> str:
    """Inline markdown: `code`, **bold**, *italic*, then bare-domain linkify.
    Code spans are protected from the other passes."""
    codes = []
    def stash(m):
        codes.append(m.group(1))
        return f"\x00CODE{len(codes)-1}\x00"
    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    # lesson-id backticks became \x00CODE markers; handle linkmap on restore
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = linkify(text)
    def restore(m):
        code = codes[int(m.group(1))]
        if code in LINKMAP:  # cross-link known lesson ids (map.md graph)
            return f'<a href="{LINKMAP[code]}"><code>{html.escape(code)}</code></a>'
        return f"<code>{html.escape(code)}</code>"
    text = re.sub(r"\x00CODE(\d+)\x00", restore, text)
    return text

def md_to_html(md: str) -> str:
    """Convert one lesson's markdown body to HTML. Handles the constructs the
    lessons actually use: ##/### headers, fenced code, blockquote, - and 1.
    lists, paragraphs. Returns the body HTML without the h1/meta header."""
    lines = md.split("\n")
    out = []
    i = 0
    in_ul = in_ol = False
    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul: out.append("</ul>"); in_ul = False
        if in_ol: out.append("</ol>"); in_ol = False
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            close_lists()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1  # closing fence
            out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
            continue
        if s.startswith("## "):
            close_lists()
            out.append(f"<h2>{inline(s[3:])}</h2>")
        elif s.startswith("### "):
            close_lists()
            out.append(f"<h3>{inline(s[4:])}</h3>")
        elif s.startswith("> "):
            close_lists()
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[2:]); i += 1
            out.append('<div class="note">' + " ".join(inline(b) for b in buf) + "</div>")
            continue
        elif re.match(r"^[-*] ", s):
            if in_ol: out.append("</ol>"); in_ol = False
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append(f"<li>{inline(s[2:])}</li>")
        elif re.match(r"^\d+\. ", s):
            if in_ul: out.append("</ul>"); in_ul = False
            if not in_ol: out.append("<ol>"); in_ol = True
            out.append(f"<li>{inline(re.sub(r'^\d+\. ', '', s))}</li>")
        elif s == "" or s == "---":
            close_lists()
        else:
            close_lists()
            out.append(f"<p>{inline(s)}</p>")
        i += 1
    close_lists()
    return "\n".join(out)

def parse_lesson(lid: str):
    """Split a lesson md into (title, ledger_html, body_html, frontmatter).
    All lesson metadata comes from the YAML frontmatter (brief §4)."""
    fm = REGISTRY[lid]
    md = (GUIDEBOOK / "lessons" / f"{lid}.md").read_text()
    # strip frontmatter block
    end = md.index("\n---", 4)
    rest = md[end + 4:]
    title = re.match(r"\s*# (.+)", rest).group(1)
    # map-ref prose line (optional body content — kept, rendered in the ledger)
    mapref = ""
    for l in rest.split("\n"):
        if l.startswith("**Map ref"):
            mapref = re.sub(r"^\*\*Map refs?:\*\*\s*", "", l).strip()
            break
    # body: drop h1, any legacy **ID:** line, mapref line, and the first --- rule
    body_lines = []
    skipped_rule = False
    for l in rest.split("\n"):
        if l.startswith("# ") or l.startswith("**ID:**") or l.startswith("**Map ref"):
            continue
        if l.strip() == "---" and not skipped_rule:
            skipped_rule = True; continue
        body_lines.append(l)
    body_html = md_to_html("\n".join(body_lines).strip())
    # lede = first paragraph of section 1 ("Where this shows up")
    lede_m = re.search(r"<h2>1\. Where this shows up</h2>\s*<p>(.*?)</p>", body_html, re.S)
    lede = lede_m.group(1) if lede_m else ""
    lname, ldesc = LEVELS[fm["level"]]
    prereq_links = ", ".join(
        f'<a href="{LINKMAP[p]}"><code>{html.escape(p)}</code></a>'
        for p in fm["prerequisites"])
    if not prereq_links:
        prereq_links = "None — see §2 for what to have ready."
    rows = [
        ("Stage", html.escape(STAGE_LABELS[fm["stage"]])),
        ("Level", f"<strong>Level {fm['level']} · {html.escape(lname)}</strong> — "
                  f"{html.escape(ldesc)}"),
        ("Prerequisites", prereq_links + ' <span class="muted">(full list in §2)</span>'),
    ]
    if mapref:
        rows.append(("Map references", inline(mapref)))
    ledger = "".join(
        f'<tr><th scope="row">{html.escape(k)}</th><td>{v}</td></tr>'
        for k, v in rows)
    return title, lede, ledger, body_html

def page_shell(*, title, description, canonical, crumbs, breadcrumb_json, main_html):
    css = (REPO / "index.html").read_text().split("<style>")[1].split("</style>")[0]
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | Learn Computer Stuff</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{html.escape(title)} | Learn Computer Stuff"><meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="website"><meta property="og:url" content="{canonical}">
<style>{css}</style><script type="application/ld+json">{breadcrumb_json}</script>
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
<a class="brand" href="/"><span class="seal-dot" aria-hidden="true"></span>Learn Computer Stuff</a><nav class="top" aria-label="Main"><a href="/f/">Careers</a><a href="/method/">Method</a><a class="btn" href="/start/">Start here</a></nav>
</div></header>
<div class="wrap"><div class="crumbs">{crumbs}</div></div>
<main id="main"><div class="wrap">
{main_html}
</div></main>
<footer class="site"><div class="wrap"><div class="cols">
<div><strong>Learn Computer Stuff</strong><br>The free route in, and what the certificates really cost.</div>
<div><a href="/f/">All careers</a><br><a href="/start/">Start here</a><br><a href="/method/">How we verify</a></div>
<div>Claims here carry the date they were checked, or say plainly that they were not — an entry added by hand reads <em>operator-added</em> rather than borrowing a date it never earned.</div>
</div></div></footer>
</body></html>
"""

def breadcrumb(items):
    els = [{"@type": "ListItem", "position": n + 1, "name": name, "item": url}
           for n, (name, url) in enumerate(items)]
    import json
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                       "itemListElement": els}, separators=(",", ":"))

def build_lesson(lid):
    fm = REGISTRY[lid]
    slug = fm["slug"]
    stage_label = STAGE_LABELS[fm["stage"]]
    title, lede, ledger, body = parse_lesson(lid)
    nword = numword(TOTAL)
    lname, ldesc = LEVELS[fm["level"]]
    canonical = f"https://learncomputerstuff.dev/g/{slug}/"
    crumbs = (f'<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / '
              f'<span>{html.escape(title)}</span>')
    _skey = fm["stage"]
    _slink = (f' Part of <a href="{STAGEMAP[_skey]}">{html.escape(stage_label)}</a>.' if _skey in STAGEMAP else "")
    # section 10 heading gets the lesson's real name kept; body carries links
    main = f"""<section>
<span class="eyebrow">Security guidebook · {html.escape(stage_label)}</span><h1>{html.escape(title)}</h1>
<p class="lede prose">{lede}</p>
<p><span class="eyebrow">Level {fm["level"]} · {html.escape(lname)}</span> — {html.escape(ldesc)}</p>
<p class="dateline">{html.escape(fm["dateline"])}</p>
<table class="ledger"><tbody>
{ledger}
</tbody></table>
</section>
<section style="padding-top:0">
{body}
</section>
<section><div class="note"><span class="eyebrow">Keep going</span>
<p class="prose">This lesson is one of {nword} in the security guidebook.{_slink} <a href="/g/">See all {nword} lessons →</a></p></div></section>"""
    out = REPO / "g" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_shell(
        title=title, description=fm["description"], canonical=canonical,
        crumbs=crumbs,
        breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                    ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                    (title, canonical)]),
        main_html=main))
    print(f"wrote {out} ({len(out.read_text())} bytes)")

def build_index():
    doors = []
    for lid in ORDER:
        fm = REGISTRY[lid]
        title, lede, _ledger, _body = parse_lesson(lid)
        # one-sentence door text: reuse the title + stage
        doors.append(
            f'<a class="door" href="/g/{fm["slug"]}/"><h3>{html.escape(title)}</h3>'
            f'<p><span class="eyebrow">{html.escape(STAGE_LABELS[fm["stage"]])}</span></p>'
            f'<p>{lede[:220].rsplit(" ", 1)[0]}…</p></a>')
    canonical = "https://learncomputerstuff.dev/g/"
    main = f"""<section>
<span class="eyebrow">New · hands-on, free, no account needed</span><h1>The security guidebook</h1>
<p class="lede prose">A complete cybersecurity education, taught the way the work actually happens: you run the commands, reproduce the findings, fix the flaws, and write the reports — every walkthrough executed and dated, every claim checked against its source. {numword(TOTAL).capitalize()} lessons are live now: the Stage A foundations, the Stage A remainder (Python, reading code, Windows, OSINT), the pilots, the Stage B mechanics wave (authorization, methodology, toolbench, practice targets), the Stage B web-vulnerability wave, the Stage C detection-and-operations wave, the Stage C disclosure wave, the Stage E CISSP-domain wave, the Stage D specialist wave (red team, malware, cloud, AppSec), the Stage D wave 2 (exploit concepts, DFIR deep), the Stage C remainder (public track record, AI tooling), the AI security track, and the CISSP coverage wave (all 62 objectives, 1.1 to 8.5, each with its lesson); the full program builds out from here, stage by stage.</p>
<p class="dateline">Published {TODAY} · walkthroughs run 2026-10-09</p>
<div class="note"><span class="eyebrow">How a lesson is built</span>
<p class="prose">Every lesson follows the same ten parts: where it shows up, what you need first, how it works, a guided walkthrough, work on your own, where it goes wrong, the primary sources, check-yourself questions, a proof-of-skill artifact, and where it leads next. If a step could not be run, the lesson says so on the page.</p></div>
</section>
<section><h2>The lessons</h2>
<div class="grid">
{"".join(doors)}
</div>
<p class="muted" style="margin-top:1rem">Reading order: DNS → TCP/IP → Linux CLI → Windows concepts → Git &amp; GitHub → HTTP in depth → Python for security → Reading code → OSINT &amp; research discipline → Authorization &amp; scope → Methodology → Toolbench → Practice targets → IDOR → SQL injection → Command injection → SSRF → CSRF → XSS → Business-logic flaws → Session &amp; auth → Security headers → Bug bounty mechanics → SOC triage → Log sources → Sigma detection → Incident response → Coordinated disclosure → CVE Program → CVSS → Vulnerability ecosystem → IAM → Applied crypto → Secure SDLC → BCP/DR. AI track: Prompt injection → LLM architecture → LLM Top 10 → Supply chain → AI governance → AI pipeline → AI threat modeling. Risk assessment → IAM → Applied crypto → Secure SDLC → BCP/DR → Security program → Board communication. Stage D wave 1: Red team concepts → Malware analysis → Cloud security → AppSec. Stage D wave 2: Exploit concepts → DFIR deep. Stage C remainder: Vulnerability ecosystem → Public track record → AI tooling. AI track: Prompt injection → LLM architecture → LLM Top 10 → Supply chain → AI governance → AI pipeline → AI threat modeling.</p>
</section>
<section><h2>The stages</h2>
<div class="grid">
<a class="door" href="/g/stage-a/"><h3>Stage A — Foundations</h3><p><span class="eyebrow">Novice to grounded</span></p><p>The login-to-render path, packet by packet…</p></a>
<a class="door" href="/g/stage-b/"><h3>Stage B — Practitioner</h3><p><span class="eyebrow">First valid finding</span></p><p>Authorized testing, vulnerability classes, triage-ready reports…</p></a>
<a class="door" href="/g/stage-c/"><h3>Stage C — Professional</h3><p><span class="eyebrow">Disclosure and credit</span></p><p>Coordinated disclosure, CVE records, detection work…</p></a>
<a class="door" href="/g/stage-d/"><h3>Stage D — Specialist</h3><p><span class="eyebrow">One track, deep</span></p><p>Red team, DFIR, AppSec, exploit dev, malware, cloud…</p></a>
<a class="door" href="/g/stage-e/"><h3>Stage E — Expert</h3><p><span class="eyebrow">Breadth and leadership</span></p><p>CISSP domains, governance, running a security program…</p></a>
</div>
<p class="muted" style="margin-top:1rem">Each stage page states the stage's goal, its milestone, and what a reader can and cannot honestly claim after it.</p>
</section>
<section><h2>Role paths</h2>
<div class="grid">
<a class="door" href="/g/paths/"><h3>All eight role paths</h3><p><span class="eyebrow">Pick the job, follow the plan</span></p><p>SOC analyst, security analyst, pentester, AppSec, DFIR, cloud security, IAM, GRC \u2014 each with ordered lessons, checkpoints, and a level-4 capstone\u2026</p></a>
</div>
</section>
<section><h2>Knowledge maps</h2>
<div class="grid">
<a class="door" href="/g/map-cissp/"><h3>CISSP knowledge map</h3><p><span class="eyebrow">Every objective, 1.1 to 8.5</span></p><p>Each objective points to the lesson that teaches it \u2014 or is logged as a gap\u2026</p></a>
<a class="door" href="/g/map-caisp/"><h3>CAISP knowledge map</h3><p><span class="eyebrow">Seven chapters</span></p><p>Each chapter points to the lessons that teach it\u2026</p></a>
<a class="door" href="/g/map-aigp/"><h3>AIGP knowledge map</h3><p><span class="eyebrow">Four domains</span></p><p>IAPP\u2019s AI governance domains, mapped to lessons\u2026</p></a>
<a class="door" href="/g/map-gasae/"><h3>GASAE knowledge map</h3><p><span class="eyebrow">Ten objectives</span></p><p>GIAC\u2019s AI security automation objectives, mapped to lessons\u2026</p></a>
<a class="door" href="/g/map-goaa/"><h3>GOAA knowledge map</h3><p><span class="eyebrow">Ten objectives</span></p><p>GIAC\u2019s offensive AI objectives \u2014 defensive side only\u2026</p></a>
<a class="door" href="/g/map-aaism/"><h3>AAISM knowledge map</h3><p><span class="eyebrow">Three domains</span></p><p>ISACA\u2019s AI security management domains, mapped to lessons\u2026</p></a>
</div>
</section>
<section><h2>How we verify</h2>
<p class="prose">The same rules as the rest of this site: <a href="/method/">no verification URL, no row</a>. Every walkthrough command was executed in a clean local environment and the transcript kept; where a step could not run — no Docker, no local model, no packet capture, no UDP loopback on the build machine — the lesson marks it <strong>not run by us</strong> instead of pretending.</p>
</section>"""
    out = REPO / "g" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_shell(
        title="The security guidebook",
        description=f"A free, hands-on cybersecurity program: run the commands, reproduce the findings, fix the flaws. {numword(TOTAL).capitalize()} lessons live now — Stage A foundations, the Stage A remainder, pilots, the Stage B mechanics wave, the Stage B web-vulnerability wave, the Stage C detection-and-operations wave, the Stage C disclosure wave, the Stage E CISSP-domain wave, the Stage D specialist wave, and the AI security track — plus the CISSP coverage wave (all 62 objectives).",
        canonical=canonical,
        crumbs='<a href="/">Home</a> / <span>Security guidebook</span>',
        breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                    ("Security guidebook", canonical)]),
        main_html=main))
    print(f"wrote {out}")

def build_stage_pages():
    for key, slug, stage_label, title, lede, milestone, claims, next_url, next_label, lids in STAGES:
        doors = []
        for n, lid in enumerate(lids, 1):
            ltitle, llede, _ledger, _body = parse_lesson(lid)
            lslug = LINKMAP[lid]
            doors.append(
                f'<a class="door" href="{lslug}"><h3>{n}. {html.escape(ltitle)}</h3>'
                f'<p>{llede[:220].rsplit(" ", 1)[0]}…</p></a>')
        canonical = f"https://learncomputerstuff.dev/g/{slug}/"
        main = f"""<section>
<span class="eyebrow">{html.escape(stage_label)}</span><h1>{html.escape(title)}</h1>
<p class="lede prose">{html.escape(lede)}</p>
<p class="dateline">Published {TODAY} · generated from the lesson data</p>
</section>
<section><h2>The milestone</h2>
<p class="prose">{milestone}</p>
</section>
<section><h2>The lessons</h2>
<div class="grid">
{"".join(doors)}
</div>
<p class="muted" style="margin-top:1rem">In reading order, {len(lids)} lessons. Every lesson follows the same ten parts — mechanism, walkthrough, sources, proof — and every walkthrough was executed and dated.</p>
</section>
<section><h2>What you can honestly claim</h2>
<p class="prose">{claims}</p>
</section>
<section><h2>What comes next</h2>
<p class="prose">When the milestone is met, continue to <a href="{next_url}">{html.escape(next_label)}</a>.</p>
</section>"""
        out = REPO / "g" / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_shell(
            title=f"{title} | The security guidebook",
            description=f"{title}: the stage's goal, its milestone, and what a reader can and cannot honestly claim after it. {len(lids)} free lessons. A free page in the security guidebook.",
            canonical=canonical,
            crumbs=f'<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / <span>{html.escape(title)}</span>',
            breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                        ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                        (title, canonical)]),
            main_html=main))
        print(f"wrote {out}")

# ================= Role paths (brief §4) =================
# One per role: the ordered plan through the lessons, with checkpoints and a
# level-4 capstone. Each existing /r/<role>/ page links to its path.
# (role_key, slug, role_title, job_html, groups, checkpoints, capstone_title, capstone_html)
# groups: [(group_label, [items])]; items are lesson ids or ("note", html) tuples.
PATHS = [
    ("soc-analyst", "soc-analyst", "SOC analyst",
     "You watch the alerts, work out which ones matter, and investigate the ones that do. It is shift-based work, usually reached via IT support or networking rather than straight off the street. It suits people who enjoy investigation \u2014 noticing the odd detail, chasing it down, and writing up what happened clearly enough that someone else can act on it.",
     [("Foundations", ["a-linux-cli", "a-tcpip-ports", "a-dns-depth", "a-http-depth", "a-windows-concepts",
                        ("note", "Lighter on cryptography internals than the pentester path \u2014 you need the vocabulary, not the math.")]),
      ("Detection basics", ["c-soc-triage", "c-log-sources", "c-sigma-detection", "c-incident-response"]),
      ("Deeper", ["d-dfir-deep", "d-redteam-concepts",
                  ("note", "ATT&CK is the vocabulary every alert and report on this path is written in.")])],
     ["Triage a labeled set of simulated alerts and write a disposition for each: true positive, false positive, or benign \u2014 with a one-line reason a stranger could check.",
      "Run a home SOC lab on your own machines and produce three investigation write-ups a stranger can follow end to end.",
      "Write a Sigma rule, trigger it deliberately, and document what it misses \u2014 the blind spots are part of the deliverable."],
     "Published detection-engineering project",
     "A <strong>Sigma rule package for one ATT&CK technique, with test evidence</strong>, plus a <strong>written investigation of a simulated intrusion mapped to ATT&CK</strong> \u2014 in a public repository, reproducible by a stranger. That is the artifact a hiring stranger checks."),
    ("security-analyst", "security-analyst", "Security analyst",
     "You work out what an attacker did, or is doing, and write it up so someone can act. It is the broader analysis role next to the SOC\u2019s shift-based entry point: ATT&CK is the working vocabulary and CISA advisories are the reading diet. It suits people who chase loose ends and can write clearly under time pressure.",
     [("Foundations", ["a-linux-cli", "a-tcpip-ports", "a-dns-depth", "a-http-depth", "a-python-security", "a-windows-concepts"]),
      ("Practitioner", ["b-authorization-scope", "b-methodology", "b-idor", "b-sqli", "b-xss", "b-session-auth",
                        ("note", "Studied to Apply level \u2014 you must understand exploitation to analyze it, even though you are not the one breaking in.")]),
      ("Professional, lighter", ["c-cve-program", "c-cvss", "c-vuln-ecosystem", "c-public-track-record",
                                 ("note", "Disclosure literacy and write-up craft, not CVE-chasing: the full disclosure pipeline is optional on this path.")]),
      ("Detection and DFIR", ["c-soc-triage", "c-log-sources", "c-sigma-detection", "d-dfir-deep", "d-redteam-concepts"])],
     ["An investigation of a simulated incident written up in ATT&CK vocabulary, with the evidence chain a stranger can re-derive.",
      "A detection rule written and tested against labeled data, with the tuning decisions documented.",
      "A one-page threat brief from a current CISA advisory, written for a non-technical manager."],
     "Published original threat analysis",
     "A <strong>technique deep-dive with detection logic and test evidence</strong>, or a <strong>detection pack derived from a real advisory series</strong> \u2014 published, sources dated, reproducible. That is the artifact a hiring stranger checks."),
    ("pentester", "pentester", "Penetration tester",
     "You are paid to break in \u2014 with permission and in writing \u2014 and then explain exactly how. It is open without a degree and cares about demonstrable skill more than almost any other field here, but it is rarely entry-level: people tend to arrive from help desk, networking, sysadmin, or defensive security. The hardest part is the report, not the exploit.",
     [("Foundations, full depth", ["a-linux-cli", "a-tcpip-ports", "a-dns-depth", "a-http-depth", "a-python-security", "a-reading-code", "a-osint-research", "a-git-github", "a-windows-concepts"]),
      ("Practitioner, full", ["b-authorization-scope", "b-methodology", "b-toolbench", "b-practice-targets",
                              "b-idor", "b-sqli", "b-command-injection", "b-ssrf", "b-csrf", "b-xss",
                              "b-business-logic", "b-session-auth", "b-security-headers", "b-bug-bounty"]),
      ("Professional, full", ["c-cvd", "c-cve-program", "c-cvss", "c-vuln-ecosystem", "c-public-track-record"]),
      ("Specialist", ["d-redteam-concepts", "d-exploit-concepts",
                      ("note", "Exploit development stays at concepts plus mitigations here; hands-on technique is reader-side on pwn.college, per the safety line.")])],
     ["The PortSwigger Web Security Academy core labs, completed \u2014 the free standard the industry actually respects.",
      "A first valid finding submitted to a program that authorizes testing \u2014 in scope, reproducible, impact argued honestly.",
      "A full pentest report on a lab target: the scope record, findings with business impact, remediation, and proof you stayed in scope."],
     "Published original work at professional standard",
     "One of: a <strong>coordinated disclosure with CVE credit</strong>, a <strong>novel technique-variation write-up</strong>, or a <strong>meaningful open-source tool contribution</strong> \u2014 with the full engagement report (scope record, findings, business impact, remediation) as the artifact. That is what a hiring stranger checks."),
    ("appsec", "appsec", "Application security engineer",
     "You stop vulnerabilities from being written rather than finding them after they ship. It is two disciplines \u2014 code and security \u2014 and you cannot fake either: the most common route is a few years of development followed by a deliberate turn toward security.",
     [("Code fluency first", ["a-python-security", "a-reading-code", "a-git-github", "a-linux-cli",
                               ("note", "The role page is explicit: read and write code well before the security layer means anything. Do not skip this block.")]),
      ("HTTP and identity", ["a-http-depth"]),
      ("Vulnerability classes, from the fix side", ["b-idor", "b-sqli", "b-command-injection", "b-xss", "b-csrf", "b-ssrf", "b-session-auth", "b-security-headers", "b-business-logic",
                                                   ("note", "Each class studied for how it is found <em>and</em> how it is fixed \u2014 the fix is your half of the job.")]),
      ("AppSec specialist", ["d-appsec"]),
      ("CISSP Domain 8", ["e-sdlc"])],
     ["A STRIDE threat model for something you built \u2014 not a tutorial app, your code.",
      "SAST integrated into a real pipeline, with the findings triaged and the false positives documented.",
      "A security fix responsibly disclosed and merged into real code."],
     "Merged fix or original secure-design guide",
     "A <strong>merged security fix in a real open-source project, with a teaching write-up</strong>, or an <strong>original secure-design guide others can verify</strong> \u2014 public and reviewable. That is the artifact a hiring stranger checks."),
    ("dfir", "dfir", "DFIR analyst",
     "You work out what happened after a breach, in enough detail that it stands up later \u2014 your findings may end up in a legal process, and how you handle evidence can decide whether it is admissible. It is essentially always entered from a SOC or security analyst role: you need to have watched alerts before you can reconstruct an intrusion from them.",
     [("Before you start", [("note", "This path assumes the <a href=\"/g/path/soc-analyst/\">SOC analyst path</a> is complete. The role page is explicit: DFIR is a step up from SOC work, not a first job \u2014 it does not start at Stage A directly.")]),
      ("Forensics and response", ["d-dfir-deep", "d-malware-analysis", "c-log-sources", "c-sigma-detection", "c-incident-response",
                                  ("note", "Malware analysis is concepts plus triage workflow here; detonation is reader-side in your own isolated lab.")])],
     ["A timeline reconstructed from lab logs or a disk image, with every entry sourced.",
      "A memory-forensics exercise with documented findings \u2014 what you looked for, what you found, what you ruled out.",
      "A chain-of-custody record maintained across an exercise, unbroken.",
      "An incident report written for non-technical readers \u2014 a lawyer or executive must be able to act on it."],
     "Full forensic case study from a simulated breach",
     "A <strong>published case study: timeline, evidence-handling notes, findings, and an executive report</strong> \u2014 all reproducible from the labeled data you publish alongside it. That is the artifact a hiring stranger checks."),
    ("cloud-security", "cloud-security", "Cloud security engineer",
     "You make sure the cloud account nobody is watching is not the way in. Most breaches now involve a misconfigured cloud resource rather than an exotic exploit \u2014 and the blast radius of a mistake is unusually large, which is why this is not entry-level work.",
     [("Foundations", ["a-linux-cli", "a-tcpip-ports", "a-http-depth"]),
      ("Cloud fluency first", [("note", "No guidebook lesson covers core cloud services yet \u2014 logged as a gap. Learn one major cloud\u2019s compute, storage, networking, and IAM in your own account, <strong>billing alarm on before anything else</strong> (the role page\u2019s warning), before the security content below.")]),
      ("Cloud security", ["d-cloud-security", "b-ssrf", "e-iam",
                           ("note", "SSRF is here for the cloud-metadata-service angle \u2014 the classic cloud attack path.")]),
      ("CISSP Domains 3 and 5", ["e-crypto-applied", "e-iam"])],
     ["A misconfiguration found and fixed in your own lab account \u2014 before, after, and what stops it recurring.",
      "Least privilege applied to a working setup end to end, with the breakage notes.",
      "An automated guardrail that fails a deployment reintroducing the problem."],
     "Published cloud security baseline",
     "A <strong>published cloud security baseline: an audited reference architecture with detective controls</strong>, or <strong>original research on a misconfiguration class with detection logic</strong>. That is the artifact a hiring stranger checks."),
    ("iam-engineer", "iam-engineer", "IAM engineer",
     "You decide who can do what, and you make sure nobody quietly accumulates more than they need. Stolen credentials, not clever exploits, start most intrusions \u2014 which is why identity is where organizations are actively spending, and why this work is steadier than it sounds.",
     [("Foundations", ["a-http-depth", "a-linux-cli",
                       ("note", "HTTP here means the authentication layer: Basic, Bearer, JWT structure, OAuth 2.0 and OIDC flows. Linux here means the permission model \u2014 the oldest access-control system you will ever administer.")]),
      ("CISSP Domain 5", ["e-iam"]),
      ("Cloud IAM", ["d-cloud-security", ("note", "For the cloud IAM deep dive: policies read as code, roles, federation.")]),
      ("Cryptography", ["e-crypto-applied", ("note", "Hashing, signatures, PKI \u2014 and what breaks when each is misused.")])],
     ["A permissions audit of a lab environment, with a written removal rationale for every grant you would revoke.",
      "Least privilege applied end to end, with the breakage notes \u2014 a fix that breaks the app is not a fix.",
      "A joiner-mover-leaver process document: what happens on day one, on transfer, on departure."],
     "Published IAM reference others can run",
     "A <strong>least-privilege policy library for a common stack, with rationale per policy</strong>, or an <strong>access-review methodology with a worked example</strong> \u2014 published, runnable. That is the artifact a hiring stranger checks."),
    ("grc-analyst", "grc-analyst", "GRC analyst",
     "You turn a security standard into things the organization actually does, and prove it did them. It is the most reachable security role for non-technical backgrounds \u2014 audit, admin, project, legal transfer in \u2014 and the least hands-on of this family: written artifacts carry the role.",
     [("Foundations, lighter", ["a-http-depth",
                                ("note", "Read for vocabulary \u2014 enough networking, HTTP, and crypto language to read a control intelligently. The packet labs are optional on this path.")]),
      ("Risk and continuity", ["e-risk-assessment", "e-bcp-drp"]),
      ("Asset security", ["e-asset-classification", "e-data-lifecycle", "e-data-protection-controls"]),
      ("Assessment and testing", ["e-assessment-strategy", "e-security-audits"]),
      ("Running the program", ["e-security-program", "e-board-communication"]),
      ("AI governance", ["ai-governance"]),
      ("Governance frameworks", ["e-csf-20", "e-iso27001", "e-soc2"])],
     ["One control mapped to exact evidence \u2014 the control, the artifact that proves it, where it lives.",
      "A risk written so a director can decide on it: one page, no jargon.",
      "A policy a real employee could follow without asking questions."],
     "Complete published GRC work product",
     "A <strong>risk assessment of a fictional company, a control implementation guide, or an audit plan</strong> \u2014 published and written to be used, not to be admired. That is the artifact a hiring stranger checks."),
]

PATHMAP = {key: f"/g/path/{slug}/" for key, slug, *_ in PATHS}

# ---- The registry is the single source of truth (brief §4). ----
# Loaded here, after PATHS/PATHMAP exist for validation. Every count,
# link map, path, stage listing and knowledge map below derives from it.
REGISTRY = load_registry()

# lesson id -> site-relative url, for cross-linking
LINKMAP = {lid: f"/g/{fm['slug']}/" for lid, fm in REGISTRY.items()}

TOTAL = len(REGISTRY)


def validate_tables():
    """Cross-check every hand table against the registry. Membership is owned
    by frontmatter; ordering stays editorial. Any drift is a build error."""
    # PATHS: every group id exists + carries the path's role; every lesson
    # with the role appears in the path (completeness).
    for key, _slug, _title, _job, groups, _cps, _ct, _ch in PATHS:
        gids = []
        for _glabel, items in groups:
            for it in items:
                if isinstance(it, tuple):
                    continue
                if it not in REGISTRY:
                    raise SystemExit(f"build error: path {key} lists unknown lesson {it!r}")
                if key not in REGISTRY[it]["roles"]:
                    raise SystemExit(
                        f"build error: path {key} lists {it}, but its frontmatter "
                        f"roles are {REGISTRY[it]['roles']} (fix the frontmatter)")
                gids.append(it)
        missing = sorted(lid for lid, fm in REGISTRY.items()
                         if key in fm["roles"] and lid not in gids)
        if missing:
            raise SystemExit(
                f"build error: path {key} omits lessons whose frontmatter claims "
                f"the role: {missing} (fix the frontmatter or the path)")
    # STAGES: every listed id matches the stage; every A–E lesson is listed.
    staged = {}
    for skey, _slug, _label, _t, _l, _m, _c, _n, _nl, lids in STAGES:
        for lid in lids:
            if lid not in REGISTRY:
                raise SystemExit(f"build error: stage {skey} lists unknown lesson {lid!r}")
            if REGISTRY[lid]["stage"] != skey:
                raise SystemExit(
                    f"build error: stage {skey} lists {lid}, but its frontmatter "
                    f"stage is {REGISTRY[lid]['stage']!r} (fix the frontmatter)")
            staged[lid] = skey
    for lid, fm in REGISTRY.items():
        if fm["stage"] in ("A", "B", "C", "D", "E") and lid not in staged:
            raise SystemExit(
                f"build error: lesson {lid} has stage {fm['stage']} but is in no stage list")
    # map_refs point at real objectives/chapters (the mapping itself derives
    # from frontmatter in build_maps).
    cissp_objs = {o for _d, _t, _w, objs in CISSP_DOMAINS for o, _p in objs}
    caisp_ch = {n for n, _t in CAISP_CHAPTERS}
    for lid, fm in REGISTRY.items():
        for ref in fm["map_refs"]:
            if ref.startswith("CISSP "):
                if ref.split(" ", 1)[1] not in cissp_objs:
                    raise SystemExit(f"build error: {lid} map_ref {ref!r} is not an objective")
            elif ref.startswith("CAISP ch"):
                if ref.split("ch", 1)[1] not in caisp_ch:
                    raise SystemExit(f"build error: {lid} map_ref {ref!r} is not a chapter")


def _lesson_door(lid, n):
    fm = REGISTRY[lid]
    title = parse_lesson(lid)[0]
    return (f'<a class="door" href="/g/{fm["slug"]}/"><h3>{n}. {html.escape(title)}</h3>'
            f'<p><span class="eyebrow">{html.escape(STAGE_LABELS[fm["stage"]])}</span></p></a>')


def build_paths():
    validate_tables()
    lesson_info = {}
    for lid in REGISTRY:
        lesson_info[lid] = parse_lesson(lid)[0]
    for key, slug, role_title, job, groups, checkpoints, cap_title, cap_html in PATHS:
        sections = []
        n = 0
        for group_label, items in groups:
            doors, notes = [], []
            for it in items:
                if isinstance(it, tuple):
                    notes.append(f'<div class="note"><p class="prose">{it[1]}</p></div>')
                else:
                    n += 1
                    doors.append(_lesson_door(it, n))
            gh = f"<h2>{html.escape(group_label)}</h2>"
            if doors:
                gh += f'\n<div class="grid">\n{"".join(doors)}\n</div>'
            if notes:
                gh += "\n" + "\n".join(notes)
            sections.append(f"<section>\n{gh}\n</section>")
        checks = "".join(f"<li>{c}</li>" for c in checkpoints)
        canonical = f"https://learncomputerstuff.dev/g/path/{slug}/"
        main = f"""<section>
<span class="eyebrow">Security guidebook \u00b7 Role path</span><h1>The {html.escape(role_title)} path</h1>
<p class="lede prose">{job}</p>
<p class="dateline">Published {TODAY} \u00b7 generated from the lesson data \u00b7 serves <a href="/r/{key}/">{html.escape(role_title)}</a></p>
<div class="note"><span class="eyebrow">How to use this path</span>
<p class="prose">Work the groups in order. Each checkpoint is a gate: do not move on until you can do it unaided. The capstone is level 4 \u2014 original work, made public, verifiable by a stranger.</p></div>
</section>
{"".join(sections)}
<section><h2>Checkpoints</h2>
<ol>
{checks}
</ol>
</section>
<section><h2>The capstone</h2>
<p class="prose"><strong>Level 4 \u2014 Extend: {html.escape(cap_title)}.</strong> {cap_html}</p>
</section>
<section><div class="note"><span class="eyebrow">Keep going</span>
<p class="prose"><a href="/g/paths/">All eight role paths \u2192</a> \u00b7 <a href="/g/">The security guidebook \u2192</a></p></div></section>"""
        out = REPO / "g" / "path" / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_shell(
            title=f"The {role_title} path",
            description=f"The {role_title} study path: ordered lessons, checkpoints, and a level-4 capstone. A free page in the security guidebook.",
            canonical=canonical,
            crumbs=(f'<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / '
                    f'<a href="/g/paths/">Role paths</a> / <span>The {html.escape(role_title)} path</span>'),
            breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                        ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                        ("Role paths", "https://learncomputerstuff.dev/g/paths/"),
                                        (f"The {role_title} path", canonical)]),
            main_html=main))
        print(f"wrote {out}")


def build_path_index():
    doors = []
    for key, slug, role_title, job, _g, _c, _ct, _ch in PATHS:
        first = job.split(". ")[0] + "."
        doors.append(
            f'<a class="door" href="/g/path/{slug}/"><h3>The {html.escape(role_title)} path</h3>'
            f'<p>{html.escape(first)}</p></a>')
    canonical = "https://learncomputerstuff.dev/g/paths/"
    main = f"""<section>
<span class="eyebrow">Security guidebook \u00b7 Role paths</span><h1>Role paths</h1>
<p class="lede prose">One ordered plan per role: the lessons in sequence, checkpoints that gate each stage, and a level-4 capstone \u2014 original public work a stranger can verify. Pick the job, follow the plan.</p>
<p class="dateline">Published {TODAY} \u00b7 generated from the lesson data</p>
</section>
<section><h2>The eight paths</h2>
<div class="grid">
{"".join(doors)}
</div>
</section>
<section><div class="note"><span class="eyebrow">Keep going</span>
<p class="prose"><a href="/g/">The security guidebook \u2192</a></p></div></section>"""
    out = REPO / "g" / "paths" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_shell(
        title="Role paths",
        description="Eight ordered study plans through the security guidebook \u2014 one per role, each with checkpoints and a level-4 capstone. Free pages in the security guidebook.",
        canonical=canonical,
        crumbs='<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / <span>Role paths</span>',
        breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                    ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                    ("Role paths", canonical)]),
        main_html=main))
    print(f"wrote {out}")


# ================= Knowledge maps (brief \u00a74) =================
# CISSP: every objective 1.1\u20138.5. Lesson ids are real lessons; [] = logged gap.
# Paraphrases are the guidebook's own, never outline text.
CISSP_DOMAINS = [
    ("1", "Security and Risk Management", "16", [
        ("1.1", "Professional ethics in security work"),
        ("1.2", "Core security concepts: confidentiality, integrity, availability, and related properties"),
        ("1.3", "Security governance: aligning security with business strategy"),
        ("1.4", "Legal, regulatory, and compliance landscape"),
        ("1.5", "Investigation types and their requirements"),
        ("1.6", "Security policy, standards, procedures, and guidelines"),
        ("1.7", "Business continuity requirements: business impact analysis and dependencies"),
        ("1.8", "Personnel security across hiring, employment, and departure"),
        ("1.9", "Risk management concepts, end to end"),
        ("1.10", "Threat modeling concepts and methodologies"),
        ("1.11", "Supply chain risk management"),
        ("1.12", "Security awareness, education, and training programs"),
    ]),
    ("2", "Asset Security", "10", [
        ("2.1", "Identifying and classifying information and assets"),
        ("2.2", "Information and asset handling requirements"),
        ("2.3", "Secure provisioning: ownership, inventory, asset management"),
        ("2.4", "The data lifecycle: roles, collection, location, retention, remanence, destruction"),
        ("2.5", "Asset retention and end-of-life/support"),
        ("2.6", "Data security controls and compliance"),
    ]),
    ("3", "Security Architecture and Engineering", "13", [
        ("3.1", "Secure design principles for engineering"),
        ("3.2", "Formal security models"),
        ("3.3", "Selecting controls from system security requirements"),
        ("3.4", "Platform security capabilities"),
        ("3.5", "Assessing vulnerabilities across architecture and system types"),
        ("3.6", "Cryptographic solutions: lifecycle, methods, PKI, key management"),
        ("3.7", "Cryptanalytic attack methods"),
        ("3.8", "Site and facility design principles"),
        ("3.9", "Site and facility security controls"),
        ("3.10", "The information system lifecycle"),
    ]),
    ("4", "Communication and Network Security", "13", [
        ("4.1", "Secure network architecture design"),
        ("4.2", "Securing network components"),
        ("4.3", "Secure communication channels"),
    ]),
    ("5", "Identity and Access Management", "13", [
        ("5.1", "Controlling physical and logical access to assets"),
        ("5.2", "Identification and authentication strategy"),
        ("5.3", "Federated identity with third-party services"),
        ("5.4", "Authorization mechanisms and models"),
        ("5.5", "Identity and access provisioning lifecycle"),
        ("5.6", "Implementing authentication systems"),
    ]),
    ("6", "Security Assessment and Testing", "12", [
        ("6.1", "Designing assessment, test, and audit strategies"),
        ("6.2", "Security control testing methods"),
        ("6.3", "Collecting security process data"),
        ("6.4", "Analyzing test output and reporting"),
        ("6.5", "Conducting and facilitating security audits"),
    ]),
    ("7", "Security Operations", "13", [
        ("7.1", "Investigations: evidence, techniques, forensics"),
        ("7.2", "Logging and monitoring operations"),
        ("7.3", "Configuration management"),
        ("7.4", "Foundational security operations concepts"),
        ("7.5", "Resource and media protection"),
        ("7.6", "Incident management"),
        ("7.7", "Operating detective and preventive measures"),
        ("7.8", "Patch and vulnerability management operations"),
        ("7.9", "Change management"),
        ("7.10", "Recovery strategies and resilience"),
        ("7.11", "Disaster recovery processes"),
        ("7.12", "Testing the disaster recovery plan"),
        ("7.13", "Business continuity planning and exercises"),
        ("7.14", "Physical security implementation"),
        ("7.15", "Personnel safety and security concerns"),
    ]),
    ("8", "Software Development Security", "10", [
        ("8.1", "Security in the SDLC"),
        ("8.2", "Security controls in development ecosystems"),
        ("8.3", "Assessing software security effectiveness"),
        ("8.4", "Security impact of acquired software"),
        ("8.5", "Secure coding guidelines and standards"),
    ]),
]

# CISSP AI notes: from ISC2's "Exam Guidance for Artificial Intelligence"
# (September 1, 2026) — exam-relevant AI topics woven into each domain, not
# commentary. Verified 2026-10-10. Each note links the domain to AI-track lessons.
CISSP_AI_NOTES = {
    "1": ("AI assets shift your risk posture \u2014 fold ML models and LLMs into the risk frameworks you already use, govern AI ethics and algorithmic bias, and assess AI vendors the way you assess any third party.", ["ai-governance", "ai-supply-chain"]),
    "2": ("Training datasets, pre-trained models, and model weights are high-value assets to classify and handle; protect data integrity across the AI lifecycle and use differential privacy and masking where AI touches PII.", ["ai-supply-chain", "ai-llm-architecture"]),
    "3": ("Host AI compute in secure enclaves, validate inputs against prompt injection and adversarial attacks, and engineer in explainability so an AI's decisions stay auditable.", ["ai-prompt-injection", "ai-llm-architecture"]),
    "4": ("Isolate AI training environments with micro-segmentation and zero trust to stop lateral movement, and know how AI-driven NDR finds anomalies that signature-based tools miss.", ["ai-threat-modeling", "ai-sec-automation"]),
    "5": ("Give AI agents and service accounts full identity-lifecycle treatment under least privilege, and use AI \u2014 behavioral biometrics, adaptive authentication \u2014 to defend your identity estate in turn.", ["ai-sec-automation", "ai-llm-architecture"]),
    "6": ("Red-team AI systems against evasion and extraction attacks, audit model outputs for exploitable logic flaws, and automate vulnerability management with AI-powered scanning.", ["ai-threat-modeling", "ai-sec-automation"]),
    "7": ("Put AI/ML into SOAR to cut alert fatigue, and monitor production models for drift and live adversarial attacks as part of normal operations.", ["ai-sec-automation"]),
    "8": ("AI-assisted coding ships hallucinated vulnerabilities and insecure generated snippets \u2014 catch them with AI security testing in CI/CD, and secure the ML supply chain against model hijacking and inference attacks.", ["ai-pipeline", "ai-llm-top10"]),
}

# CAISP (Practical DevSecOps): seven chapters. All have lessons.
CAISP_CHAPTERS = [
    ("1", "Introduction to AI Security"),
    ("2", "Understanding and Attacking Large Language Models"),
    ("3", "LLM Top 10 Vulnerabilities"),
    ("4", "AI Attacks and Defenses Using DevOps"),
    ("5", "Threat Modeling AI Systems"),
    ("6", "Supply Chain Attacks in AI"),
    ("7", "Emerging Threats, Governance, and Compliance in AI"),
]


# Light knowledge maps (brief §4): domain-level maps for AI-adjacent credentials.
# Each entry: (slug, page title, issuer, credential name, lede, [notes], [(domain, title, [lesson ids])]).
# Lesson ids must exist in the registry; empty list renders "No lesson yet".
LIGHT_MAPS = [
    ("map-aigp", "AIGP knowledge map", "IAPP", "Artificial Intelligence Governance Professional",
     "You don\u2019t need a law degree to govern AI systems, but you do need to know what the exam\u2019s four domains demand: the principles of responsible AI, the laws and frameworks that apply, how development gets governed, and how deployment and use are kept honest. This map points each domain to the guidebook lessons that teach the underlying material \u2014 from how LLM applications are built to the EU AI Act and the NIST AI Risk Management Framework. The exam itself is paid; everything this map teaches is free. Domain titles are IAPP\u2019s; everything else is the guidebook\u2019s own words.",
     ["This map follows the AIGP Body of Knowledge version 2.1 (effective February 2, 2026), verified against IAPP\u2019s official PDF on 2026-10-10.",
      "The AIGP exam is a paid exam. This map teaches the four domains from free guidebook lessons; it is not the exam."],
     [("I", "Understanding the foundations of AI governance", ["ai-llm-architecture", "ai-governance", "e-policy-docs", "e-awareness-training"]),
      ("II", "Understanding how laws, standards and frameworks apply to AI", ["ai-governance", "e-cyber-law"]),
      ("III", "Understanding how to govern AI development", ["ai-pipeline", "ai-supply-chain", "ai-threat-modeling", "e-sdlc", "e-data-lifecycle"]),
      ("IV", "Understanding how to govern AI deployment and use", ["ai-governance", "e-incident-management", "e-logging-monitoring", "e-security-metrics"])]),
    ("map-gasae", "GASAE knowledge map", "GIAC", "GIAC AI Security Automation Engineer",
     "GASAE tests whether you can apply automation and AI across offensive, defensive, and cloud security work \u2014 SOAR playbooks, adversary emulation, cloud security automation, detection engineering with AI. This map points each of GIAC\u2019s ten exam objectives to the guidebook lessons that teach the underlying skill \u2014 scripting, SOC workflows, cloud security, adversary emulation, incident response. The exam is hands-on in GIAC\u2019s CyberLive lab format and paid; the lessons this map points to are free. Objective titles are GIAC\u2019s; everything else is the guidebook\u2019s own words.",
     ["SANS\u2019s SEC598: AI and Security Automation for Red, Blue, and Purple Teams is the course GIAC pairs with this exam \u2014 five course sections mapped to the ten objectives, confirmed at sans.org on 2026-10-10. The course is paid; this map teaches the same objectives from free lessons.",
      "GASAE uses GIAC\u2019s CyberLive hands-on exam format \u2014 performance-based lab challenges rather than traditional multiple choice: 82 questions over 3 hours, 70% to pass."],
     [("1", "Adversary Emulation Fundamentals", ["d-redteam-concepts", "ai-sec-automation"]),
      ("2", "Artificial Intelligence Fundamentals", ["ai-llm-architecture"]),
      ("3", "Automating Offensive Workflows", ["d-redteam-concepts", "ai-sec-automation"]),
      ("4", "Automating Workflows", ["a-python-security", "ai-sec-automation"]),
      ("5", "AWS Cloud Security and Incident Response Automation", ["d-cloud-security", "ai-sec-automation"]),
      ("6", "Azure Cloud Security and Incident Response Automation", ["d-cloud-security", "ai-sec-automation"]),
      ("7", "Defensive Security Automation", ["c-log-sources", "ai-sec-automation"]),
      ("8", "Security Automation Fundamentals", ["ai-sec-automation"]),
      ("9", "Security Orchestration Automation and Response", ["c-soc-triage", "c-incident-response", "ai-sec-automation"]),
      ("10", "Using Automation and AI for Detection Engineering and Incident Response", ["c-sigma-detection", "c-incident-response", "ai-sec-automation"])]),
    ("map-goaa", "GOAA knowledge map", "GIAC", "GIAC Offensive AI Analyst",
     "GOAA tests AI-driven offensive technique \u2014 reconnaissance, web exploitation, AI-assisted phishing and deepfakes, AI-generated malware, control evasion. The guidebook teaches these topics the way it teaches all offensive material: the concepts, what a defender sees, and how to detect and stop it \u2014 no working malware, no phishing kits, no evasion tooling. Each objective points to the lessons that teach its defensive side; three objectives have no lesson yet, and they are marked honestly. Objective titles are GIAC\u2019s; everything else is the guidebook\u2019s own words.",
     ["SANS\u2019s SEC535: Offensive AI \u2013 Attack Tools and Techniques is the course GIAC pairs with this exam, confirmed at sans.org on 2026-10-10. The course is paid; this map teaches the objectives\u2019 defensive side from free lessons.",
      "How the guidebook handles offensive AI: the linked lessons teach each attack\u2019s concepts, the telemetry a defender sees, and the fix. Three objectives have no lesson \u2014 deepfakes, AI-written phishing email, social-engineering fundamentals \u2014 and they stay unmapped rather than taught badly; the guidebook does not write phishing kits or working malware, so those gaps do not get closed with how-to content."],
     [("1", "Artificial Intelligence Fundamentals", ["ai-llm-architecture"]),
      ("2", "Audio, Image, and Video Deepfakes", []),
      ("3", "Bypassing Defensive Controls", ["d-exploit-concepts"]),
      ("4", "Creating Malicious Software with AI", ["d-malware-analysis"]),
      ("5", "Creating Phishing Emails with AI", []),
      ("6", "Malware Fundamentals", ["d-malware-analysis"]),
      ("7", "Network Scanning and Vulnerability Detection", ["b-toolbench", "b-methodology"]),
      ("8", "Social Engineering Fundamentals", []),
      ("9", "Using AI for OSINT", ["a-osint-research"]),
      ("10", "Using AI for Web Exploitation", ["b-sqli", "b-command-injection"])]),
    ("map-aaism", "AAISM knowledge map", "ISACA", "Advanced in AI Security Management",
     "AAISM is ISACA\u2019s AI-security credential for people who already hold an active CISM or CISSP \u2014 it layers AI governance, AI risk management, and AI controls on top of that security-management foundation. This map points each of ISACA\u2019s three job practice domains to the guidebook lessons that teach the underlying material \u2014 AI governance and risk frameworks, threat modeling AI systems, controls for the AI lifecycle. The exam is paid; the lessons are free. This map covers AAISM only: ISACA\u2019s separate AI credentials for audit (AAIA) and risk (AAIR) are listed separately. Domain titles are ISACA\u2019s; everything else is the guidebook\u2019s own words.",
     ["ISACA\u2019s rule, stated once: only security professionals who hold an active CISM or CISSP are eligible to pursue AAISM. The lessons teach the AI-specific material; they do not confer the credential and do not replace the prerequisite.",
      "ISACA runs three separate Advanced AI credentials: AAIR (Advanced in AI Risk), AAISM (Advanced in AI Security Management), and AAIA (Advanced in AI Audit). This map covers AAISM only.",
      "This map follows ISACA\u2019s AAISM exam content outline as published at isaca.org, verified 2026-10-10: a 90-question exam across three job practice domains."],
     [("1", "AI Governance and Program Management", ["ai-governance", "e-security-program", "e-policy-docs"]),
      ("2", "AI Risk Management", ["e-risk-assessment", "ai-threat-modeling", "e-threat-modeling-concepts", "e-supply-chain-risk"]),
      ("3", "AI Technologies and Controls", ["ai-llm-architecture", "ai-pipeline", "ai-supply-chain", "e-data-protection-controls", "e-logging-monitoring"])]),
]


def _lesson_link(lid):
    title = parse_lesson(lid)[0]
    return f'<a href="{LINKMAP[lid]}">{html.escape(title)}</a>'


def build_maps():
    # Objective/chapter -> lessons, inverted from lesson frontmatter map_refs.
    cissp_index = {}
    caisp_index = {}
    for lid, fm in REGISTRY.items():
        for ref in fm["map_refs"]:
            if ref.startswith("CISSP "):
                cissp_index.setdefault(ref.split(" ", 1)[1], []).append(lid)
            elif ref.startswith("CAISP ch"):
                caisp_index.setdefault(ref.split("ch", 1)[1], []).append(lid)
    # deterministic order: registry ORDER
    order_pos = {lid: n for n, lid in enumerate(ORDER)}
    for idx in (cissp_index, caisp_index):
        for k in idx:
            idx[k].sort(key=lambda lid: order_pos[lid])
    covered = sum(1 for _n, _t, _w, objs in CISSP_DOMAINS
                  for _o, _p in objs if cissp_index.get(_o))
    total = sum(len(objs) for _n, _t, _w, objs in CISSP_DOMAINS)

    # ---- CISSP map ----
    dom_sections = []
    for dnum, dtitle, weight, objs in CISSP_DOMAINS:
        rows = []
        for obj, paraphrase in objs:
            lids = cissp_index.get(obj, [])
            if lids:
                cell = ", ".join(_lesson_link(l) for l in lids)
            else:
                cell = "<em>No lesson yet \u2014 logged as a gap.</em>"
            rows.append(
                f'<tr><th scope="row">{html.escape(obj)}</th>'
                f'<td>{html.escape(paraphrase)}</td><td>{cell}</td></tr>')
        ai_note, ai_lids = CISSP_AI_NOTES.get(dnum, ("", []))
        ai_html = ""
        if ai_note:
            ai_links = ", ".join(_lesson_link(l) for l in ai_lids)
            ai_html = (f'\n<p class="prose"><span class="eyebrow">AI note</span> '
                       f'{ai_note} See: {ai_links}.</p>')
        dom_sections.append(
            f"<section><h2>Domain {html.escape(dnum)} \u2014 {html.escape(dtitle)} <span class=\"eyebrow\">{html.escape(weight)}% of the exam</span></h2>{ai_html}"
            f'\n<table class="ledger"><thead><tr><th>Objective</th><th>Topic</th><th>Lesson</th></tr></thead>'
            f"<tbody>\n{''.join(rows)}\n</tbody></table></section>")
    canonical = "https://learncomputerstuff.dev/g/map-cissp/"
    main = f"""<section>
<span class="eyebrow">Security guidebook \u00b7 Knowledge map</span><h1>CISSP knowledge map</h1>
<p class="lede prose">Every objective of the CISSP exam outline (effective April 15, 2024), 1.1 to 8.5, pointing to the lesson that teaches it \u2014 or logged as a gap where no lesson exists yet. Objectives are numbered and paraphrased in the guidebook\u2019s own words; the outline text itself is never reproduced.</p>
<p class="dateline">Published {TODAY} \u00b7 generated from the lesson data \u00b7 <strong>{covered} of {total} objectives have a lesson</strong></p>
<div class="note"><span class="eyebrow">The issuer\u2019s rule, stated once</span>
<p class="prose">Full CISSP certification needs five cumulative years of work experience in two or more of the eight domains \u2014 a degree or an approved credential can stand in for one year. Passing the exam without the experience makes someone an Associate of ISC2. The lessons teach the bodies of knowledge; they do not confer the certification.</p></div>
<div class="note"><span class="eyebrow">AI in the outline \u2014 exam content, not commentary</span>
<p class="prose">ISC2\u2019s \u201cExam Guidance for Artificial Intelligence\u201d (September 1, 2026) maps AI-specific security tasks across all eight domains of the CISSP exam outline (still the April 15, 2024 edition) \u2014 examinable topics woven into each domain, not separate AI objectives and not third-party commentary. Each domain section below carries its AI note with links to the AI security track lessons.</p></div>
</section>
{"".join(dom_sections)}
<section><div class="note"><span class="eyebrow">Keep going</span>
<p class="prose"><a href="/g/">The security guidebook \u2192</a></p></div></section>"""
    out = REPO / "g" / "map-cissp" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_shell(
        title="CISSP knowledge map",
        description=f"Every CISSP exam objective (1.1 to 8.5) mapped to the guidebook lesson that teaches it. {covered} of {total} objectives have a lesson. A free page in the security guidebook.",
        canonical=canonical,
        crumbs='<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / <span>CISSP knowledge map</span>',
        breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                    ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                    ("CISSP knowledge map", canonical)]),
        main_html=main))
    print(f"wrote {out}")

    # ---- CAISP map ----
    ch_rows = []
    for cnum, ctitle in CAISP_CHAPTERS:
        lids = caisp_index.get(cnum, [])
        cell = ", ".join(_lesson_link(l) for l in lids)
        ch_rows.append(
            f'<tr><th scope="row">Chapter {html.escape(cnum)}</th>'
            f'<td>{html.escape(ctitle)}</td><td>{cell}</td></tr>')
    ch_covered = sum(1 for _n, _t in CAISP_CHAPTERS if caisp_index.get(_n))
    ch_total = len(CAISP_CHAPTERS)
    canonical = "https://learncomputerstuff.dev/g/map-caisp/"
    main = f"""<section>
<span class="eyebrow">Security guidebook \u00b7 Knowledge map</span><h1>CAISP knowledge map</h1>
<p class="lede prose">The seven chapters of the CAISP syllabus (Practical DevSecOps), each pointing to the guidebook lessons that teach it. Chapter titles are the issuer\u2019s; everything else is the guidebook\u2019s own words.</p>
<p class="dateline">Published {TODAY} \u00b7 generated from the lesson data \u00b7 <strong>{ch_covered} of {ch_total} chapters have a lesson</strong></p>
<div class="note"><span class="eyebrow">Two credentials, never merged</span>
<p class="prose">CAISP (Practical DevSecOps) is a separate credential from CertNexus CAIP, which the site lists separately. This map covers CAISP only.</p></div>
<div class="note"><span class="eyebrow">Edition note</span>
<p class="prose">The lessons teach the OWASP LLM Top 10 <strong>2026 edition</strong> (verified against the official OWASP GenAI Security Project repo, 2026-10-09). The project brief named the 2025 edition \u2014 that reference is pending the owner\u2019s confirmation.</p></div>
</section>
<section><h2>The seven chapters</h2>
<table class="ledger"><thead><tr><th>Chapter</th><th>Title</th><th>Lessons</th></tr></thead><tbody>
{"".join(ch_rows)}
</tbody></table></section>
<section><div class="note"><span class="eyebrow">Keep going</span>
<p class="prose"><a href="/g/">The security guidebook \u2192</a></p></div></section>"""
    out = REPO / "g" / "map-caisp" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_shell(
        title="CAISP knowledge map",
        description=f"The seven CAISP chapters mapped to the guidebook lessons that teach them. {ch_covered} of {ch_total} chapters have a lesson. A free page in the security guidebook.",
        canonical=canonical,
        crumbs='<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / <span>CAISP knowledge map</span>',
        breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                    ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                    ("CAISP knowledge map", canonical)]),
        main_html=main))
    print(f"wrote {out}")

    # ---- Light maps: AIGP, GASAE, GOAA, AAISM (brief §4, domain level) ----
    for slug, page_title, issuer, cred_name, lede, notes, domains in LIGHT_MAPS:
        rows = []
        for dnum, dtitle, lids in domains:
            # validate lesson ids against the registry
            for lid in lids:
                if lid not in REGISTRY:
                    raise ValueError(f"light map {slug}: unknown lesson id {lid}")
            if lids:
                cell = ", ".join(_lesson_link(l) for l in lids)
            else:
                cell = "<em>No lesson yet \u2014 logged as a gap.</em>"
            rows.append(
                f'<tr><th scope="row">{html.escape(dnum)}</th>'
                f'<td>{html.escape(dtitle)}</td><td>{cell}</td></tr>')
        covered_n = sum(1 for _n, _t, lids in domains if lids)
        total_n = len(domains)
        notes_html = "".join(
            f'<div class="note"><p class="prose">{html.escape(n)}</p></div>' for n in notes)
        canonical = f"https://learncomputerstuff.dev/g/{slug}/"
        main = f"""<section>
<span class="eyebrow">Security guidebook \u00b7 Knowledge map</span><h1>{html.escape(page_title)}</h1>
<p class="lede prose">{html.escape(lede)}</p>
<p class="dateline">Published {TODAY} \u00b7 generated from the lesson data \u00b7 <strong>{covered_n} of {total_n} domains have a lesson</strong></p>
{notes_html}
</section>
<section><h2>The domains</h2>
<table class="ledger"><thead><tr><th>Domain</th><th>Title</th><th>Lessons</th></tr></thead><tbody>
{"".join(rows)}
</tbody></table></section>
<section><div class="note"><span class="eyebrow">Keep going</span>
<p class="prose"><a href="/g/">The security guidebook \u2192</a></p></div></section>"""
        out = REPO / "g" / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_shell(
            title=page_title,
            description=f"{cred_name} ({issuer}) mapped domain by domain to the guidebook lessons that teach it. {covered_n} of {total_n} domains have a lesson. A free page in the security guidebook.",
            canonical=canonical,
            crumbs=f'<a href="/">Home</a> / <a href="/g/">Security guidebook</a> / <span>{html.escape(page_title)}</span>',
            breadcrumb_json=breadcrumb([("Home", "https://learncomputerstuff.dev/"),
                                        ("Security guidebook", "https://learncomputerstuff.dev/g/"),
                                        (page_title, canonical)]),
            main_html=main))
        print(f"wrote {out}")


if __name__ == "__main__":
    validate_tables()
    for lid in ORDER:
        build_lesson(lid)
    build_stage_pages()
    build_paths()
    build_path_index()
    build_maps()
    build_index()
    print("done")
