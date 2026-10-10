# Production-readiness audit — 2026-10-10

Auditor: subagent (production-readiness track). Scope: `~/workspace/learncomputerstuff/` working tree,
branch `guidebook/gap-closing` @ `a9abf7e` + uncommitted audit fixes. Guidebook under `g/`
(70 pages: 53 lessons + 5 stages + 9 path pages + 2 maps + index). Builder:
`security-guidebook/build_site.py` — all fixes applied at SOURCE (lessons/ or build_site.py),
never hand-edited `g/` HTML. Nothing committed, nothing pushed.

## 1. Internal links — PASS
- Crawled 79 pages (70 `g/` + homepage + 8 modified `r/` pages).
- **1,805 internal hrefs checked, 0 broken.** Every relative and absolute-internal link resolves
  to a built page.

## 2. Outbound links — PASS with fixes
- 179 unique external URLs checked (HEAD→GET fallback, browser UA, redirects followed).
- **Found and fixed: the `linkify()` trailing-paren bug** (`build_site.py:270`). The bare-domain
  regex's path class included `)`, so `(rfc-editor.org/rfc/rfc8446)` produced
  `href="https://rfc-editor.org/rfc/rfc8446)"` — **81 unique outbound links were 404ing**.
  Fix: strip an unbalanced trailing `)` (balanced parens like Wikipedia titles preserved).
  Unit-tested, site rebuilt, zero trailing-paren hrefs remain.
- **Found and fixed: TLD truncation** — `TLD` list lacked `education`, so `exploit.education`
  linkified as `exploit.edu` (dead). Fix: added `education|college|eu|ch|ai|one|app|co` +
  `(?![A-Za-z0-9-])` lookahead to stop prefix truncation (`example.comment` no longer
  mis-links as `example.com`). 9 previously-unlinked bare domains now link correctly.
- **Found and fixed: prose mis-link** — "post-pwn.college" (prose, "after pwn.college") was
  linkified to a bogus domain. Fixed at lesson source (`lessons/d-exploit-concepts.md:73`
  reworded to "the stretch after pwn.college").
- **Found and fixed: typo** — `lessons/c-sigma-detection.md:107`
  `github.com/redcanaryco/atomic-red-teams` → `atomic-red-team` (verified 200).
- Residual non-issues (all pages confirmed alive): 5 hosts 403 this sandbox's client
  (Cloudflare, FIDO Alliance, TraceLabs, Pentegron/Pentest-Standard connection reset —
  all verified via live browser fetch; linuxjourney.com now redirects to its official
  LabEx successor page, link still resolves), volatilityfoundation.org 429 was transient
  (200/301 on retry), sqlite.org/huggingface.co timeouts were transient (200 on retry).
- Redirects observed are all benign (http→https, bare→www, owasp.org `/www-project-*` →
  `/projects/*`, securityonion.net → securityonionsolutions.com). No lesson changes needed;
  URLs resolve.

## 3. Sitemap — PASS
- `sitemap.xml`: 164 URLs. All 70 built `g/` pages listed, 1:1, none missing, none extra.
  lastmod: 94 × 2026-07-28 (pre-existing), 70 × 2026-10-09 (guidebook).

## 4. Mobile width — PASS with fix
- Rendered `/g/`, `/g/xss/`, `/g/stage-b/`, `/g/path/pentester/`, `/g/map-cissp/`,
  `/g/map-caisp/` at 390px and 1280px in headless Chromium (Playwright).
- **Found and fixed: horizontal overflow on `/g/xss/` @390px** (scrollWidth 829 vs 390 —
  inline `<code>` with a 153-char unbreakable curl command). The shared stylesheet
  (homepage `<style>`, inherited by all `g/` pages) had no code-wrapping rule.
  Fix: added `code{overflow-wrap:anywhere}` + `pre{overflow-x:auto;max-width:100%}` to
  `learncomputerstuff/index.html`, rebuilt. Re-checked `/g/xss/`, `/g/sqli/`,
  `/g/command-injection/`, `/g/toolbench/` @390px — all clean.

## 5. Keyboard navigation — PASS
- Tabbed through `/g/` (60 stops of 82 links — iteration cap, no repeats, all visible)
  and `/g/xss/` (all 25 links reachable). Every stop visible with a solid 3px focus
  outline. The 3 "repeated" stops on `/g/xss/` were two *distinct* links sharing one
  href (`/g/business-logic/` cited in two paragraphs) — focus moves correctly, no trap.

## 6. Headings/metadata — PASS
- All 79 pages: exactly one `<h1>`, no heading-level jumps, `<title>`, meta description,
  canonical link, og:title/og:description/og:type present. Zero issues.

## 7. Content hygiene — PASS with fixes
- Currency: only `$` hits are shell/awk code samples (`$7`, `$3`, `$N`) and the
  b-business-logic fictional worked-example amounts ("$25 shirt", "$0.01") — the
  vulnerability mechanism being taught, clearly fictional, reviewed-and-kept per
  gaps.md. No real prices/fees/salaries anywhere.
- No lorem/placeholder text (hits were legitimate prose uses: SQL placeholders, labeled
  `[to be measured]` placeholders; one "TODO" is inside the lesson's *fictional* OSINT
  dossier artifact — the target's data, not a site placeholder).
- **Found and fixed: stale "not run by us" markers.** The 2026-10-10 re-runs appended
  "now RUN BY US" notes but left the old "Not run by us:" clauses in place, producing
  self-contradictory steps and stale walkthrough headers. Fixed at source:
  - `lessons/b-xss.md` steps 4, 6 + header (rewrote as "Re-ran 2026-10-10 — now RUN BY US")
  - `lessons/b-security-headers.md` steps 3, 4 (same rewrite)
  - `lessons/a-tcpip-ports.md` header ("Two steps marked not-run" → UDP only; packet
    capture re-ran)
  - `build_site.py` dateline notes (6): tcpip-ports, csrf, xss, security-headers,
    appsec (Semgrep re-ran; ZAP still reader-side), toolbench (nmap/Semgrep/Chromium
    re-ran; rest still reader-side)
  - Verified zero stale markers remain on built pages. Remaining "not run by us"
    markers (27 pages) are all honest: Docker, local AI model, Windows, sshd, DNSSEC,
    UDP loopback, ZAP/Dependency-Check, MFA enrollment, reader-side tool installs.
- CISSP no-dump/no-copyright spot-check (e-iam, e-sdlc, e-bcp-drp, e-security-program,
  e-risk-assessment): no exam questions, no question banks; map-cissp quotes only short
  objective titles (5–8 words, fair-use citation), no substantial outline text.

## 8. Screenshots — saved
12 PNGs under `reports/audit-2026-10-10/` (6 pages × 390px + 1280px):
`g-index-*.png`, `g-xss-*.png`, `g-stage-b-*.png`, `g-path-pentester-*.png`,
`g-map-cissp-*.png`, `g-map-caisp-*.png`, plus `render-keyboard.json` (overflow +
keyboard measurements).

## Files changed (all uncommitted, working tree)
- `security-guidebook/build_site.py` — linkify paren fix, TLD list + lookahead, 6 dateline notes
- `security-guidebook/lessons/b-xss.md`, `b-security-headers.md`, `a-tcpip-ports.md`,
  `c-sigma-detection.md`, `d-exploit-concepts.md` — marker/typo/prose fixes
- `learncomputerstuff/index.html` — `code`/`pre` wrap rules in shared `<style>`
- `learncomputerstuff/g/*` — rebuilt (linkify, TLD, CSS, dateline, marker fixes)
- NOTE: `lessons/` grew 53 → 73 files during the audit (parallel CISSP crew); their new
  lessons are not yet in build_site.py's LESSONS table and not built. Final crawl ran
  after all fixes: 79 pages, 0 broken internal, 0 meta issues.

## Could NOT verify / remaining
- The 5 bot-blocking 403s were confirmed alive via alternate fetch, not via the same
  HEAD/GET path as the rest — recorded as alive, method noted.
- New CISSP lessons landing after this audit need a fresh crawl before publish.
- Hygiene: all test http.servers killed by explicit PID; `pgrep` confirms zero remain.
