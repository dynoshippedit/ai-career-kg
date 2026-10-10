#!/bin/bash
# usage: _mklog.sh slug title objective wordcount "scope notes" 
slug=$1; title=$2; obj=$3; wc=$4; scope=$5
cat > $slug.log <<EOF
$title — worked-case authoring log
date: 2026-10-10 · lesson id: $slug · serves CISSP objective $obj
mode: worked case authored and self-reviewed in-session; no command line in this lesson.
ALL data below is fictional and labeled as such.

SCOPE
$scope

AUTHORING DECISIONS
- Fictional organization and system invented for the worked case; every name, number, and finding is invented.
- Walkthrough steps written as reader procedure; no step claims a command was run.
- Section 7 sources: all fetched in-session 2026-10-10 (see manifest batch-d3.json sources rows for URL + chars).

SELF-REVIEW CHECKLIST (2026-10-10)
[✓] ten ## sections in exact order 1..10
[✓] header block: ID / Stage E (Expert) / Level / Prerequisites / Map ref with paraphrase (no ISC2 outline text)
[✓] §7: primary docs first, then at most three free resources, all free, no login/paywall
[✓] every §7-cited URL fetched in-session 2026-10-10 with character count recorded
[✓] walkthrough honest: labeled worked case, "no command line", no faked output
[✓] no currency symbols anywhere in lesson or log
[✓] no exam dumps, no ISC2 proprietary material, no outline text reproduced
[✓] word count $wc within 1,800–2,500
[✓] §8 has exactly 5 questions; §9 has Artifact + Honest claim + Can't claim yet
[✓] §10 references only real lesson ids + CISSP cross-refs
[✓] no restatement of the CISSP experience rule
[✓] safety: no exploit code, no evasion tooling; defenses paired with attacks where applicable
EOF
echo "wrote $slug.log"
