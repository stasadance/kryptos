#!/usr/bin/env python3
"""Iteration 19: two superimposed periodic keys k_i = a[i mod L1] + b[i mod L2] under ONE unknown
alphabet (Q3 Vig/Beau). Phase 1 (H-1501) covered this only with AZ/KA tableaux. Exact: the cribs are
linear mod 26 in (alphabet, a, b); solved by CRT + all-different enumeration (it18c machinery).
Control: planted L1=7, L2=10. Null: random ciphertexts."""
import random, sys, itertools
sys.path.insert(0, "iterations")
from it18_vimark_mixed import PAIRS, CT, AZ, CRIBS
from it18c_vimark_alldiff import solve_space
def system(ct, V, model):
    L = sorted({ct[i] for i, _ in PAIRS} | {p for _, p in PAIRS}); ix = {c: j for j, c in enumerate(L)}; m = len(V[0]); rows = []
    for i, p in PAIRS:
        r = [0] * (len(L) + m + 1); r[ix[ct[i]]] += 1; r[ix[p]] += -1 if model == "v" else 1
        for j in range(m): r[len(L) + j] -= V[i][j]
        rows.append(r)
    return rows, len(L)
def ok(ct, V, model, cap=2000000):
    S, nl = system(ct, V, model); a, b = solve_space(S, 2), solve_space(S, 13)
    if a is None or b is None: return 0
    (b2, B2), (b13, B13) = a, b
    if 13 ** len(B13) * 2 ** len(B2) > cap: return -1
    s2 = [tuple((b2[j] + sum(c * v[j] for c, v in zip(co, B2))) % 2 for j in range(nl)) for co in itertools.product(range(2), repeat=len(B2))]
    for co in itertools.product(range(13), repeat=len(B13)):
        x = [(b13[j] + sum(c * v[j] for c, v in zip(co, B13))) % 13 for j in range(nl)]
        if max(x.count(v) for v in set(x)) > 2: continue
        if any(len(set(zip(y, x))) == nl for y in s2): return 1
    return 0
def V2(L1, L2): return [[int(j == i % L1) for j in range(L1)] + [int(j == i % L2) for j in range(L2)] for i in range(97)]
PAIRSL = [(a, b) for a in range(2, 13) for b in range(a + 1, 16) if a + b <= 20]
if __name__ == "__main__":
    rng = random.Random(21); al = list(AZ); rng.shuffle(al); pos = {c: i for i, c in enumerate(al)}
    A = [rng.randrange(26) for _ in range(7)]; B = [rng.randrange(26) for _ in range(10)]
    pt = [rng.choice(AZ) for _ in range(97)]
    for s, w in CRIBS.items(): pt[s:s + len(w)] = w
    ctl = "".join(al[(pos[p] + A[i % 7] + B[i % 10]) % 26] for i, p in enumerate(pt))
    print("control (7,10,v):", ok(ctl, V2(7, 10), "v"))
    nulls = ["".join(rng.choice(AZ) for _ in range(97)) for _ in range(60)]
    for L1, L2 in PAIRSL:
        for m in "vb":
            V = V2(L1, L2); r = ok(CT, V, m)
            nr = [x for x in (ok(s, V, m) for s in nulls) if x >= 0]
            print(f"{L1:2d}+{L2:2d} {m} | K4 {r:2d} | null {sum(nr)}/{len(nr)} decidable", flush=True)
