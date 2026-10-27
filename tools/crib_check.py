#!/usr/bin/env python3
"""Check a candidate K4 decryption against all known cribs.
Usage: python3 crib_check.py <candidate_plaintext_97_chars>
Exit 0 only if every crib matches."""
import sys
CRIBS = {22: "EASTNORTHEAST", 64: "BERLINCLOCK"}  # 1-indexed start
def check(pt):
    pt = pt.upper()
    ok = len(pt) == 97
    for s, w in CRIBS.items():
        got = pt[s-1:s-1+len(w)]
        hit = got == w
        ok &= hit
        print(f"{s:>3} {w:<14} got {got:<14} {'OK' if hit else 'FAIL'}")
    print("LENGTH", len(pt), "OK" if len(pt) == 97 else "FAIL")
    return ok
if __name__ == "__main__":
    sys.exit(0 if check(sys.argv[1]) else 1)
