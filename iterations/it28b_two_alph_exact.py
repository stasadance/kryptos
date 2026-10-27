#!/usr/bin/env python3
"""Exact check for a FIXED key stream under two arbitrary alphabets, B(c) = A(p) + k (mod 26): the 24 crib equations
are linear in the A- and B-values; CRT (mod 2, 13) + all-different within each alphabet. Used to confirm it28."""
import itertools, sys, random
sys.path.insert(0, "iterations"); from it18c_vimark_alldiff import solve_space
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CR = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}; PAIRS = [(s + j, p) for s, w in CR.items() for j, p in enumerate(w)]
def feasible(ct, k, cap=2000000):
    Bl = sorted({ct[i] for i, _ in PAIRS}); Al = sorted({p for _, p in PAIRS}); nb, na = len(Bl), len(Al); n = nb + na
    rows = []
    for i, p in PAIRS:
        r = [0] * (n + 1); r[Bl.index(ct[i])] += 1; r[nb + Al.index(p)] -= 1; r[-1] = k[i] % 26; rows.append(r)
    rows.append([1] + [0] * (n - 1) + [0])          # gauge: B(first) = 0
    a, b = solve_space([x[:] for x in rows], 2), solve_space([x[:] for x in rows], 13)
    if a is None or b is None: return 0
    (b2, B2), (b13, B13) = a, b
    if 13 ** len(B13) * 2 ** len(B2) > cap: return -1
    grp = [range(nb), range(nb, n)]
    s2l = [tuple((b2[j] + sum(c * v[j] for c, v in zip(co, B2))) % 2 for j in range(n)) for co in itertools.product(range(2), repeat=len(B2))]
    for co in itertools.product(range(13), repeat=len(B13)):
        x = [(b13[j] + sum(c * v[j] for c, v in zip(co, B13))) % 13 for j in range(n)]
        if any(max([x[j] for j in g].count(v) for v in set(x[j] for j in g)) > 2 for g in grp): continue
        for y in s2l:
            if all(len(set((y[j], x[j]) for j in g)) == len(g) for g in grp): return 1
    return 0
if __name__ == "__main__":
    sys.argv = ["x", "/tmp/claude-0/it27"]
    exec(open("iterations/it28_keyword_pair_two_alph.py").read().split("if __name__")[0])
    K4 = open("data/ciphertext.txt").read().strip(); allk = list(streams()); rng = random.Random(2); ok = 0
    for t in range(20):
        p, k = rng.choice(allk); A = list(range(26)); rng.shuffle(A); B = rng.sample(range(26), 26); Bi = {x: l for l, x in enumerate(B)}
        pt = [rng.choice(AZ) for _ in range(97)]; pt[21:34] = "EASTNORTHEAST"; pt[63:74] = "BERLINCLOCK"
        ct = "".join(AZ[Bi[(A[AZ.index(c)] + k[i]) % 26]] for i, c in enumerate(pt)); ok += feasible(ct, k) == 1
    print("controls", ok, "/20")
    res = [feasible(K4, k) for p, k in allk]
    print("K4 feasible", res.count(1), "infeasible", res.count(0), "undecided", res.count(-1), "of", len(allk))
    nul = ["".join(rng.choice(AZ) for _ in range(97)) for _ in range(3)]
    for c in nul: r = [feasible(c, k) for p, k in allk[:300]]; print("null feasible", r.count(1), "/300")
