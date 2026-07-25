# SEO Review — AI Career KG / learncomputerstuff.dev

_Last updated: 2026-07-25_

## Purpose

This file is a **model-switch handoff artifact**. It preserves the SEO research
and — most importantly — the constraints, so that when the owner switches AI
models, the next model reads this file instead of re-deriving everything (or
worse, editing the site without permission).

**Read this first: the owner does NOT want website changes made without explicit
approval.** The current site was difficult to set up and works. Treat this
document as research and planning context only. Nothing here is a mandate to
implement.

---

## Site / Repo Context

- Local site folder: `/home/dino/Desktop/ComputerSurferSITE/`
- GitHub repo: `dynoshippedit/ai-career-kg` (public)
- GitHub Pages mirror: `dynoshippedit.github.io/ai-career-kg/`
- Target production domain: `learncomputerstuff.dev`
- Site is **not yet connected to Cloudflare Pages** — nothing is live at the
  target domain as of this writing.

### Hard constraints (respect these)

- **Cloudflare FREE tier only.** Every solution must fit free hosting:
  - Pages: 500 builds/month, 1 concurrent build, 20,000 files max
  - Workers/Functions: 100,000 requests/day, 10ms CPU/request
- The owner's Cloudflare tokens are **zone-scoped**; Pages/Workers-Scripts are
  **account-level** permissions, so every direct write 403'd. The working
  deploy route is **GitHub → Cloudflare Pages auto-deploy**, not the CF API.
- **GitHub operations use the GitHub API / authenticated git with the owner's
  fine-grained PAT. Never Composio.** (Composio truncates >1MB files and its
  use here has caused problems.)
- Prefer **pure static** changes over any runtime/Worker-based solution.

---

## Files Audited

Current HTML pages (8):
`index.html`, `pathways.html`, `path.html`, `explorer.html`, `builder.html`,
`nocred.html`, `learn.html`, `patterns.html`

Supporting files: `sky.css` (~19 KB), `skybg.js`, `fonts/*.woff2` (7 files).

---

## Research Findings (measured, not estimated)

### 1. KG blob duplication — biggest single issue

The same Knowledge-Graph JSON blob is embedded inline in **every** HTML page.

- Embedded KG JSON: **1,379,727 bytes per page**
- Each HTML file: ~1.38–1.40 MB
- Across 8 files the site ships **~10.6 MB of HTML**, of which
  **~10.5 MB (99.2%) is the repeated KG blob** and **~9.2 MB is pure
  duplication** (the same blob 8×).

Implication: heavy page weight, poor crawl efficiency, poor mobile perf.
**Caution:** extracting the blob to a shared file must NOT be done casually —
if pages then fetch it client-side, crawlers would see *less* than they do now.
Extraction is only safe *after* real static HTML content exists on each page
(see "Corrected order" below).

### 2. JavaScript-rendered content risk

Most page content (cards/resources/path detail) is rendered by JS from the KG
blob after load. Static, crawler-visible text measured:

- `index.html`: ~1,034 chars static crawlable text
- `path.html`: **~90 chars** unique static text, and its hero is an **empty
  container**: `<div class="hero" id="phero"></div>` — no `<h1>`, no path name
  in the first-pass HTML.
- Other pages: mostly 300–1,900 unique static chars; `learn.html` is the best
  (~1,908 chars, largely static prose).

Implication: Google renders JS, but on a **new/low-authority domain** rendering
is queued and can lag days–weeks (industry data: ~9× slower than plain HTML).
Thin first-pass HTML risks "Crawled – currently not indexed" and thin/near-
duplicate flags (several pages share ~60–74% of their static shell).

### 3. Metadata gaps

All 8 pages have unique `<title>` tags, but they are thin and brand-led
("Careers — AI Career KG"). Missing on **all 8 pages**:

- Meta descriptions (0/8)
- Canonical tags (0/8)
- Open Graph tags (0/8)
- Twitter card tags (0/8)
- Valid SEO JSON-LD structured data (0/8 — the KG blob is `application/json`
  for the app, not `application/ld+json`)
- Favicon, theme-color

### 4. Cloudflare-specific gotcha

Cloudflare Pages auto-308-redirects `/foo.html` → `/foo`. With no canonical tag
and internal links pointing at `.html`, Google may index both variants or pick
the wrong one. Any future canonical/sitemap should use **clean URLs** (`/foo`),
which is why `sitemap.xml` in this repo lists clean paths.

### 5. E-E-A-T / trust signals

Strong original angle: "learn free → attest strategically → prove with a
project," with employer-signal bands **Recognized / Respected / Signal**. This
is genuinely unique, link-worthy data.

Trust concerns in the KG data/UI:
- ~8,179 `null` field values, ~1,610 nodes with confidence < 1.0
- "Pending adjudication" wording can read as unfinished. If copy is ever
  approved for change, "Not yet assessed" / "Unverified — pending review" reads
  as deliberate methodology rather than an oversight.

### 6. AI search / Bing

Bing powers ChatGPT/Copilot grounding. Once live, submit the sitemap to **both**
Google Search Console and **Bing Webmaster Tools**. The site's answer-shaped,
structured content is well-suited to AI-Overview citation — but only once it is
crawlable (see finding #2).

---

## Structured Data Plan (FUTURE — requires approval)

If implementation is ever approved, use page-type-specific JSON-LD:

- Site-wide: `WebSite` + `EducationalOrganization`
- Homepage / collection pages: `CollectionPage` + `ItemList`
- Path pages: `EducationalOccupationalProgram` + `Course` + `BreadcrumbList`
- `learn.html`: `Article` (+ `FAQPage` only because it has real visible Q&A;
  note Google deprecated FAQ *rich results* in May 2026 — the schema still helps
  AI extraction, so keep it only where Q&A is genuinely on-page)
- **Do NOT use `JobPosting`** — the site is not listing actual open jobs.

---

## Recommended Priority (FUTURE — requires explicit owner approval)

Do not implement any of this automatically.

1. Keep the current working site stable.
2. Safe standalone crawler files — **done in this commit**: `robots.txt`,
   `sitemap.xml`.
3. Metadata only, if approved: meta descriptions, canonical tags, OG/Twitter
   tags, favicon.
4. Static-generated content, if approved — via a **local build script that emits
   pure static HTML** (NOT Cloudflare Pages Functions; Functions burn the free
   Workers budget and add per-request latency).
5. **Corrected order:** generate static HTML content FIRST, then — and only
   then — extract the repeated KG JSON into a shared cached file.

---

## Explicit Non-Goals Unless Approved

- Do not rewrite HTML structure.
- Do not change CSS/design.
- Do not change JavaScript behavior.
- Do not extract the KG JSON yet.
- Do not add a build system yet.
- Do not generate new/expanded path pages yet.
- Do not connect or deploy Cloudflare Pages without owner approval.
- Do not use Composio for GitHub operations.

---

## Files Added In This Step (documentation / crawler only)

- `SEO_REVIEW.md` (this file)
- `robots.txt`
- `sitemap.xml`

No HTML, CSS, JS, KG data, or build files were modified.
