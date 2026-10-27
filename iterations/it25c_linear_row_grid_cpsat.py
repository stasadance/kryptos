#!/usr/bin/env python3
"""Iteration 25c: CP-SAT version of it25b (the CRT enumeration was over its cap everywhere).
k_i = g[(i+o) mod w] + c*floor((i+o)/w); one unknown alphabet a (AllDifferent), numeric key;
Vig a(c)=a(p)+k, Beau a(c)=k-a(p), variant a(c)=a(p)-k, all mod 26. Feasibility only. Control + random nulls."""
import random, sys
from ortools.sat.python import cp_model
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; CT = open("data/ciphertext.txt").read().strip()
CR = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}; PAIRS = [(s + j, p) for s, w in CR.items() for j, p in enumerate(w)]
def feasible(ct, w, o, form, tl=20.0):
    m = cp_model.CpModel(); a = [m.NewIntVar(0, 25, f"a{x}") for x in range(26)]; m.AddAllDifferent(a)
    g = [m.NewIntVar(0, 25, f"g{j}") for j in range(w)]; c = m.NewIntVar(0, 25, "c")
    for i, p in PAIRS:
        row = (i + o) // w; ci, pi = AZ.index(ct[i]), AZ.index(p)
        t = m.NewIntVar(-60 - 26 * row, 60 + 26 * row, "")
        if form == "v": m.Add(a[ci] - a[pi] - g[(i + o) % w] - row * c == 26 * t)
        elif form == "b": m.Add(a[ci] + a[pi] - g[(i + o) % w] - row * c == 26 * t)
        else: m.Add(a[ci] - a[pi] + g[(i + o) % w] + row * c == 26 * t)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 4
    r = s.Solve(m)
    return {cp_model.FEASIBLE: 1, cp_model.OPTIMAL: 1, cp_model.INFEASIBLE: 0}.get(r, -1)
if __name__ == "__main__":
    rng = random.Random(9)
    al = list(range(26)); rng.shuffle(al); inv = {v: i for i, v in enumerate(al)}
    gg = [rng.randrange(26) for _ in range(7)]; cst = 25; o = 3
    pt = list(("WHENINTHECOURSEOFHUMANEVENTSITBECOMESNECESSARYFORONEPEOPLE" * 2)[:97])
    for s0, wd in CR.items(): pt[s0:s0 + len(wd)] = wd
    ctl = "".join(AZ[inv[(al[AZ.index(p)] + gg[(i + o) % 7] + cst * ((i + o) // 7)) % 26]] for i, p in enumerate(pt))
    print("control w7 o3 vig:", feasible(ctl, 7, o, "v"), flush=True)
    nulls = ["".join(rng.choice(AZ) for _ in range(97)) for _ in range(6)]
    for w in [int(x) for x in sys.argv[1:]] or [7]:
        for form in "vbw":
            k4 = [feasible(CT, w, o, form) for o in range(w)]
            nl = [feasible(cn, w, 0, form) for cn in nulls]
            print(f"w={w} {form}: K4 per-offset {k4}  nulls(o=0) {nl}", flush=True)
