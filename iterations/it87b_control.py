#!/usr/bin/env python3
"""it87 controls: plant each model (Q1 PA*, Q2 vig/beau CA*, Q4 two) with random alphabets and random key values,
build the CT crib letters, and check the exact test fires; then rate on random CTs (null) with random keys."""
import sys, random
import numpy as np
sys.path.insert(0, "/mnt/project-files/k4/tools"); sys.path.insert(0, "iterations")
import keygen as KG
from it87_q12_arbitrary import Q12, latin
AZ, KA = KG.AZ, KG.KA; r = random.Random(87)
pos = [i for i, _, _ in KG.crib_pairs()]; PT = [p for _, p, _ in KG.crib_pairs()]
ok = tot = 0
for model in ("Q1", "Q2v", "Q2b", "two") * 5:
    k = [r.randrange(26) for _ in range(24)]; A = ''.join(r.sample(AZ, 26)); B = ''.join(r.sample(AZ, 26)); F = r.choice([AZ, KA])
    if model == "Q1": C = [F[(A.index(p) + kk) % 26] for p, kk in zip(PT, k)]
    elif model == "Q2v": C = [A[(F.index(p) + kk) % 26] for p, kk in zip(PT, k)]
    elif model == "Q2b": C = [A[(kk - F.index(p)) % 26] for p, kk in zip(PT, k)]
    else: C = [B[(A.index(p) + kk) % 26] for p, kk in zip(PT, k)]
    ct = list(KG.CT)
    for i, c in zip(pos, C): ct[i - 1] = c
    ct = ''.join(ct); Q = Q12(ct); hit = [l for _, l in Q.check(np.array([k]))]
    if model == "two":
        kk = [0] * 97
        for i, v in zip(pos, k): kk[i - 1] = v
        hit += ["Q4-two"] if KG.feasible(kk, "two", ct) else []
    tot += 1; ok += bool(hit)
print(f"plants {ok}/{tot}")
# chance rates: random key values against K4 cribs
Q = Q12(KG.CT); V = np.random.default_rng(1).integers(0, 26, size=(2_000_000, 24))
h = Q.check(V); L = latin(V, Q.pairs); print("random-key Q1/Q2 hits", len(h), "of 2M; latin pass", L.sum())
two = 0; idx = np.nonzero(L)[0][:3000]
for i in idx:
    kk = [0] * 97
    for t, ix in enumerate(Q.kidx): kk[ix] = int(V[i, t])
    two += KG.feasible(kk, "two")
print(f"two feasible among {len(idx)} latin survivors: {two}")
