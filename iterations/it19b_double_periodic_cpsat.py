#!/usr/bin/env python3
"""Iteration 19b: same model as it19 (k_i = a[i mod L1] + b[i mod L2], one unknown alphabet), decided
with CP-SAT because the CRT enumeration blows up (gauge freedom). Gauge fixed: a[0] = 0."""
import random, sys
from ortools.sat.python import cp_model
sys.path.insert(0, "iterations"); from it18_vimark_mixed import PAIRS, CT, AZ, CRIBS
def ok(ct, L1, L2, model, T=30):
    M = cp_model.CpModel(); A = {L: M.NewIntVar(0, 25, L) for L in AZ}; M.AddAllDifferent(list(A.values()))
    a = [M.NewIntVar(0, 25, f"a{j}") for j in range(L1)]; b = [M.NewIntVar(0, 25, f"b{j}") for j in range(L2)]; M.Add(a[0] == 0)
    for n, (i, p) in enumerate(PAIRS):
        t = M.NewIntVar(-3, 3, f"t{n}"); sgn = -1 if model == "v" else 1
        M.Add(A[ct[i]] + sgn * A[p] - a[i % L1] - b[i % L2] == 26 * t)
    S = cp_model.CpSolver(); S.parameters.max_time_in_seconds = T; S.parameters.num_workers = 8
    return {cp_model.OPTIMAL: 1, cp_model.FEASIBLE: 1, cp_model.INFEASIBLE: 0}.get(S.Solve(M), -1)
PAIRSL = [(x, y) for x in range(2, 13) for y in range(x + 1, 19) if x + y <= 20 and y % x]
if __name__ == "__main__":
    rng = random.Random(21); al = list(AZ); rng.shuffle(al); pos = {c: i for i, c in enumerate(al)}
    A = [rng.randrange(26) for _ in range(7)]; B = [rng.randrange(26) for _ in range(10)]
    pt = [rng.choice(AZ) for _ in range(97)]
    for s, w in CRIBS.items(): pt[s:s + len(w)] = w
    ctl = "".join(al[(pos[p] + A[i % 7] + B[i % 10]) % 26] for i, p in enumerate(pt))
    print("control (7,10,v):", ok(ctl, 7, 10, "v"), flush=True)
    nulls = ["".join(rng.choice(AZ) for _ in range(97)) for _ in range(5)]
    for L1, L2 in PAIRSL:
        for m in "vb":
            r = ok(CT, L1, L2, m); nr = [ok(s, L1, L2, m, 15) for s in nulls]
            print(f"{L1:2d}+{L2:2d} {m} | K4 {r:2d} | nulls {nr}", flush=True)
