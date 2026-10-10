# STOP 2 report — security guidebook build (2026-10-10)

Gate: the guidebook is built into the site and production-ready per brief §8.
Branch: `guidebook/gap-closing` (pushed to origin 2026-10-10). No merge to main yet.

## What was built

- **101 lessons** (`guidebook/lessons/`), each exactly ten `##` sections in the required sequence, ≤3 free resources, zero currency symbols, no exam dumps, no substantial copyrighted text.
- **111 guidebook pages** under `/g/`: 101 lesson pages, 5 stage pages (A–E), 8 role-path pages + index, 2 knowledge maps (CISSP, CAISP).
- **CISSP map: 62 of 62 objectives** covered, zero "No lesson yet."
- **Generator ships in-repo** (`guidebook/build_site.py` + lessons + ledger + research inputs); rebuild is byte-identical.
- **Sitemap:** 212 URLs, XML-valid. Homepage + 8 role pages link the new paths.

## Verification (all in-session, 2026-10-09/10)

- **Sources:** 312 ledger rows, **308 verified** (URL + fetch date + chars). 2 unreachable (HackerOne Hacktivity script-rendered; retired MS Learn module — replaced with registry-hives docs), 1 CIS Benchmarks (403 Cloudflare), 1 man-pages (no URL by definition).
- **Walkthroughs re-run for real:** nmap, tcpdump, dig steps; headless-Chromium browser steps (XSS reflected/DOM, CSRF click, CSP/frame-refusal); Semgrep 1.180.0 engine comparison. Real transcripts in `runs/`.
- **Production audit:** 4,688 internal links, 0 broken; 179 outbound checked (81 builder-generated 404s fixed at the source); sitemap 70/70→212 exact; one h1/title/description/canonical/OG per page; keyboard clean; 390px viewport clean; 12 screenshots in `reports/audit-2026-10-10/`.
- **Factual corrections applied:** OWASP Top 10:2025 Injection A05 (not A03); IDOR WSTG-ATHZ-04; LLM Top 10:2026 released 2026-08-04; ATT&CK 15 tactics; SP 800-61 Rev. 3; SP 800-88 Rev. 2; SP 800-63-4; SP 800-55 Vols. 1+2; SP 800-50 Rev. 1; BOD 26-04; RFC 6265bis SameSite §5.6.7; CISA KEV hyphenated URL; Kettle research URL; DVGA :5013.

## Decisions ratified (Dino, whole-permission order 2026-10-09)

1. OWASP LLM Top 10: teach the **2026** edition (brief §5 amended).
2. Walkthrough substitution policy **accepted**: labeled local demos + honest "not run by us" markers are the standard.
3. Push authorized ("go ahead"); merge-to-main (live deploy) not yet taken.

## Remaining honest gaps

- Docker / local AI model / Windows / sshd walkthrough steps: marked "not run by us," re-runnable by the reader. No Docker, model, or Windows on the build machine.
- CIS Benchmarks ledger row (403); man-pages row (no URL possible).
- Merge `guidebook/gap-closing` → main to ship to learncomputerstuff.dev.
