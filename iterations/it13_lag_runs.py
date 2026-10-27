#!/usr/bin/env python3
"""Iteration 13: Stehle's DIAWINFBN observation (ct[i+4]-ct[i] = 5 for 5 consecutive i).
Look-elsewhere: longest run of equal lag-d differences, any d in 1..12, any value, in random 97-letter text.
Also report K4's longest run per lag, and whether the run sits in a crib (could be plaintext-driven)."""
import random
CT = open("data/ciphertext.txt").read().strip(); N = len(CT)
def runs(s, D=12):
    out = {}
    for d in range(1, D + 1):
        diff = [(ord(s[i + d]) - ord(s[i])) % 26 for i in range(len(s) - d)]
        best, cur, st, bst = 1, 1, 0, 0
        for i in range(1, len(diff)):
            cur = cur + 1 if diff[i] == diff[i - 1] else 1
            if cur > best: best, bst = cur, i - cur + 1
        out[d] = (best, bst, diff[bst])
    return out
r = runs(CT); print("K4 longest equal-difference run per lag:", {d: v for d, v in r.items()})
m = max(v[0] for v in r.values()); print("K4 max run:", m)
rng = random.Random(1); T = 200000; ge = 0
for _ in range(T):
    s = "".join(chr(65 + rng.randrange(26)) for _ in range(N))
    if max(v[0] for v in runs(s).values()) >= m: ge += 1
print(f"P(max run over lags 1..12 >= {m}) = {ge/T:.4f}")
