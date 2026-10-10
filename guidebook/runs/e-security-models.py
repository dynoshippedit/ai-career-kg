#!/usr/bin/env python3
"""Bell-LaPadula rule demo: tiny labeled file set. Levels as ints; read=observe, write=alter."""
print("== Bell-LaPadula demonstration ==")
print("Levels: 0=Unclassified 1=Confidential 2=Secret 3=TopSecret")
subjects = {"analyst_smith": 2, "operator_jones": 1, "director_cho": 3}
objects  = {"press_release.txt": 0, "shift_schedule.txt": 1,
            "incident_report.txt": 2, "source_identities.txt": 3}

def read(s, o):
    ok = subjects[s] >= objects[o]          # simple security property: no read up
    return ok, "ALLOW" if ok else "DENY (no read up)"

def write(s, o):
    ok = subjects[s] <= objects[o]          # *-property: no write down
    return ok, "ALLOW" if ok else "DENY (no write down)"

tests = [("read","analyst_smith","incident_report.txt"),
         ("read","analyst_smith","source_identities.txt"),
         ("read","operator_jones","shift_schedule.txt"),
         ("read","director_cho","press_release.txt"),
         ("write","analyst_smith","incident_report.txt"),
         ("write","analyst_smith","press_release.txt"),
         ("write","director_cho","source_identities.txt"),
         ("write","operator_jones","source_identities.txt")]
allows = denies = 0
for op, s, o in tests:
    ok, verdict = (read if op == "read" else write)(s, o)
    allows += ok; denies += not ok
    print(f"{op:5} {s:15} (L{subjects[s]}) -> {o:22} (L{objects[o]}): {verdict}")
print(f"== {allows} allowed, {denies} denied ==")
