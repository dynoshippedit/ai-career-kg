#!/usr/bin/env python3
print("== Brute-force key-space estimates (average case = half the key space) ==")
RATES = [("single CPU (~1e9 keys/s)", 1e9),
         ("GPU cluster (~1e12 keys/s)", 1e12),
         ("hypothetical exascale (~1e18 keys/s)", 1e18)]
def human(s):
    if s < 60: return f"{s:.1f} seconds"
    if s < 3600: return f"{s/60:.1f} minutes"
    if s < 86400: return f"{s/3600:.1f} hours"
    if s < 31557600: return f"{s/86400:.1f} days"
    y = s / 31557600
    return f"{y:,.1f} years" if y < 1e6 else f"{y:.2e} years"
for bits in (40, 56, 64, 80, 112, 128, 256):
    print(f"\n{bits}-bit key: 2^{bits} = {2**bits:,} keys")
    for name, rate in RATES:
        print(f"   {name}: ~{human((2**bits/2)/rate)}")
