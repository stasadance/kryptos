#!/usr/bin/env python3
"""Iteration 18: base-26 Gromark ("Vimark") under mixed alphabets. Phase 1 covered Vimark only with AZ/KA
tableaux (H-1503) and Gromark only in bases 2-16. Key: primer k_0..k_{n-1}, then
  rule A: k_{j+n} = k_j + k_{j+1}  (ACA Gromark)      rule B: k_{j+n} = k_j + k_{j+n-1}
Every k_i is linear in the primer mod 26, so crib consistency is exact in CP-SAT.
Models: Q3v/Q3b: one unknown alphabet a, a(c) = a(p) +/- k (Vig) or a(c) = k - a(p) (Beau);
        G-AZ / G-KA: plain alphabet AZ or KA, unknown cipher alphabet b, b(c) = plain(p) + k (ACA Gromark shape).
Control: planted Q3v n=7 rule A. Null: random ciphertexts give the false-feasible rate."""
import sys, random
from ortools.sat.python import cp_model
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CT = open("data/ciphertext.txt").read().strip()
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
PAIRS = [(s + j, p) for s, w in CRIBS.items() for j, p in enumerate(w)]
def coefs(n, rule, N=97):
    v = [[int(i == j) for j in range(n)] for i in range(n)]
    while len(v) < N:
        j = len(v) - n; o = v[j + 1] if rule == "A" else v[j + n - 1]
        v.append([(x + y) % 26 for x, y in zip(v[j], o)])
    return v
def keystream(pr, rule, N=97):
    k = list(pr)
    while len(k) < N:
        j = len(k) - len(pr); k.append((k[j] + (k[j + 1] if rule == "A" else k[j + len(pr) - 1])) % 26)
    return k
def feasible(ct, n, rule, model):
    V = coefs(n, rule); M = cp_model.CpModel()
    P = [M.NewIntVar(0, 25, f"p{j}") for j in range(n)]
    A = {L: M.NewIntVar(0, 25, "a" + L) for L in AZ}; M.AddAllDifferent(list(A.values()))
    plain = {"G-AZ": AZ, "G-KA": KA}.get(model)
    for idx, (i, p) in enumerate(PAIRS):
        k = sum(c * P[j] for j, c in enumerate(V[i]) if c)
        t = M.NewIntVar(-400, 400, f"t{idx}")
        if model == "Q3v": M.Add(A[ct[i]] - A[p] - k == 26 * t)
        elif model == "Q3b": M.Add(A[ct[i]] + A[p] - k == 26 * t)
        else: M.Add(A[ct[i]] - plain.index(p) - k == 26 * t)
    S = cp_model.CpSolver(); S.parameters.max_time_in_seconds = 30; S.parameters.num_workers = 8
    r = S.Solve(M); return {cp_model.OPTIMAL: 1, cp_model.FEASIBLE: 1, cp_model.INFEASIBLE: 0}.get(r, -1)
CONF = [(n, rule, m) for n in range(2, 13) for rule in "AB" for m in ("Q3v", "Q3b", "G-AZ", "G-KA")]
def scan(ct): return [(c, r) for c in CONF if (r := feasible(ct, *c)) != 0]
if __name__ == "__main__":
    arg = sys.argv[1:]
    if arg == ["control"]:
        rng = random.Random(11); al = list(AZ); rng.shuffle(al); pos = {c: i for i, c in enumerate(al)}
        k = keystream([rng.randrange(26) for _ in range(7)], "A")
        pt = [rng.choice(AZ) for _ in range(97)]
        for s, w in CRIBS.items(): pt[s:s + len(w)] = w
        ctl = "".join(al[(pos[p] + k[i]) % 26] for i, p in enumerate(pt))
        print("control (7,A,Q3v):", feasible(ctl, 7, "A", "Q3v"))
    elif arg[:1] == ["null"]:
        rng = random.Random(int(arg[1])); h = scan("".join(rng.choice(AZ) for _ in range(97)))
        print(f"null {arg[1]}: {len(h)} of {len(CONF)}", sorted({c[0] for c, _ in h}))
    else:
        h = scan(CT); print(f"K4: {len(h)} of {len(CONF)}"); [print("  ", x) for x in h]
