#!/usr/bin/env python3
"""Iteration 15: does a width-7 grid key k = f(row) + g(col) actually RAISE the doublet rate at one residue?
Algebra: c_i = c_{i+1} (same row) <=> alpha(p_i) - alpha(p_{i+1}) = g(col+1) - g(col) = D (fixed per column pair).
So doublets at a residue occur when the plaintext bigram there has alpha-difference D: rate ~ P_English(diff = D),
which is ~1/26 unless alpha is tuned. Monte Carlo on English text, random alpha/f/g:
count doublets at the best residue of width 7, versus a random (structureless) key."""
import random, re, sys
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
txt = re.sub("[^A-Z]", "", open(sys.argv[1]).read().upper())
rng = random.Random(5); T = 100000
def best_res(ct):
    cnt = [0] * 7
    for i in range(96):
        if ct[i] == ct[i + 1]: cnt[i % 7] += 1
    return max(cnt)
res = {"grid": 0, "random": 0}; tot = {"grid": 0, "random": 0}
for _ in range(T):
    s = rng.randrange(len(txt) - 97); pt = [AZ.index(ch) for ch in txt[s:s + 97]]
    al = list(range(26)); rng.shuffle(al)
    f = [rng.randrange(26) for _ in range(15)]; g = [rng.randrange(26) for _ in range(7)]
    grid = [(al[p] + f[i // 7] + g[i % 7]) % 26 for i, p in enumerate(pt)]
    rnd = [(al[p] + rng.randrange(26)) % 26 for p in pt]
    for n, ct in (("grid", grid), ("random", rnd)):
        b = best_res(ct); tot[n] += b; res[n] += b >= 5
for n in res: print(f"{n:6s}: mean best-residue doublets {tot[n]/T:.3f}; P(>=5 at one residue of width 7) = {res[n]/T:.5f}")
