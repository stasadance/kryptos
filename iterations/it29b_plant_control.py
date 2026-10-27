#!/usr/bin/env python3
"""Iteration 29 control: end-to-end planted running-key encryptions under two random alphabets, B(c) = A(p) + n(k).
Key = Carter vol. 1 at a random offset (AZ or KA numbering); plaintext = Austen (pg11) with K4's cribs at 21/63.
Each plant goes through the generic exact check (it28b.feasible) and the same annealer call as it29 (sa.c, SA_R x SA_IT).
Usage: python3 iterations/it29b_plant_control.py WORKDIR CARTER AUSTEN [n]"""
import sys, os, random, subprocess
sys.path.insert(0, "iterations")
from it28b_two_alph_exact import feasible
from it23_runkey_mixed import norm
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
W, key_t, pt_t = sys.argv[1], norm(open(sys.argv[2], errors="ignore").read()), norm(open(sys.argv[3], errors="ignore").read())
n = int(sys.argv[4]) if len(sys.argv) > 4 else 6
rng = random.Random(29)
for t in range(n):
    N = (AZ, KA)[t % 2]
    o = rng.randrange(len(key_t) - 97); k = [N.index(ch) for ch in key_t[o:o + 97]]
    q = rng.randrange(len(pt_t) - 97); pt = list(pt_t[q:q + 97])
    pt[21:34] = "EASTNORTHEAST"; pt[63:74] = "BERLINCLOCK"; pt = "".join(pt)
    A = rng.sample(range(26), 26); B = rng.sample(range(26), 26); Binv = {v: i for i, v in enumerate(B)}
    ct = "".join(chr(65 + Binv[(A[ord(p) - 65] + k[i]) % 26]) for i, p in enumerate(pt))
    ex = feasible(ct, k)
    out = subprocess.run([os.path.join(W, "sa"), "2", "0", ct, "".join(chr(65 + x) for x in k), os.environ.get("SA_R", "6"),
                          os.environ.get("SA_IT", "3000000"), str(t), "25"], cwd=W, capture_output=True, text=True).stdout.split("\n")
    s, dec = max((float(l.split()[0]), l.split()[1]) for l in out if l.strip())
    acc = sum(a == b for a, b in zip(dec, pt)) / 97
    print(f"plant {t} {('AZ','KA')[t%2]} o={o} exact={ex} best={s:.2f} acc={acc:.2f} {dec}", flush=True)
