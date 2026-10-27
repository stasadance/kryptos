#!/usr/bin/env python3
"""Iteration 16: is residue-aligned doubling a Sanborn process artifact? Same statistic as it06
(max doublet starts at one residue of any width 2..30) on 97-letter windows of K1, K2, K3, vs random strings."""
import random, sys
sys.path.insert(0, "tools"); from kryptos_k123 import K1, K2, K3
def best(ct):
    d = [i for i in range(len(ct) - 1) if ct[i] == ct[i + 1]]; b = (0, 0, 0)
    for w in range(2, 31):
        for r in range(w): b = max(b, (sum(1 for i in d if i % w == r), w, r))
    return b, len(d)
rng = random.Random(4); AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
nul = [best("".join(rng.choice(AZ) for _ in range(97)))[0][0] for _ in range(20000)]
p = lambda m: sum(x >= m for x in nul) / len(nul)
for name, s in (("K1", K1), ("K2", K2.replace("?", "")), ("K3", K3.replace("?", "")), ("K4", open("data/ciphertext.txt").read().strip())):
    for st in range(0, max(1, len(s) - 96), 97):
        w = s[st:st + 97]; (m, ww, r), nd = best(w)
        print(f"{name}[{st}:{st+len(w)}] doublets {nd:2d}  best aligned {m} (w={ww}, r={r})  P_random(>= {m}) = {p(m):.4f}")
