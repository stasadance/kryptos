#!/usr/bin/env python3
"""Iteration 12: width-7 grid key whose column part is the keyword KRYPTOS itself.

k_i = f(row) + g((i+o) mod 7), with g = KRYPTOS as numbers (4 numberings: AZ0/AZ1/KA0/KA1), any row
shifts f, unknown plaintext alphabet alpha (Quagmire III, beta = alpha; or beta in {AZ, KA}).
This is the most natural concrete form of the it06/it07 mechanism. K1/K2 used the KRYPTOS
alphabet with keywords, and KRYPTOS has 7 letters. Exact CP-SAT feasibility; null = random ct.
"""
import sys, random
from ortools.sat.python import cp_model
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CT = open("data/ciphertext.txt").read().strip()
CRIBS = {22: "EASTNORTHEAST", 64: "BERLINCLOCK"}
PAIRS = [(s - 1 + j, p) for s, w in CRIBS.items() for j, p in enumerate(w)]
NUMB = {"AZ0": (AZ, 0), "AZ1": (AZ, 1), "KA0": (KA, 0), "KA1": (KA, 1)}
def feasible(ct, g, o, model, beta=None):
    M = cp_model.CpModel()
    A = {L: M.NewIntVar(0, 25, "a" + L) for L in AZ}; M.AddAllDifferent(list(A.values()))
    rows = {(i + o) // 7 for i, _ in PAIRS}; F = {r: M.NewIntVar(0, 25, f"f{r}") for r in rows}
    for n, (i, p) in enumerate(PAIRS):
        t = M.NewIntVar(-4, 4, f"t{n}"); gc = g[(i + o) % 7]
        cval = A[ct[i]] if beta is None else beta.index(ct[i])
        if model == "vig": M.Add(cval - A[p] - F[(i + o) // 7] - gc == 26 * t)
        else: M.Add(cval + A[p] - F[(i + o) // 7] - gc == 26 * t)
    S = cp_model.CpSolver(); S.parameters.max_time_in_seconds = 20; S.parameters.num_workers = 1
    r = S.Solve(M); return {cp_model.OPTIMAL: 1, cp_model.FEASIBLE: 1, cp_model.INFEASIBLE: 0}.get(r, -1)
def scan(ct):
    hits = []
    for nb, (al, d) in NUMB.items():
        g = [(al.index(c) + d) % 26 for c in "KRYPTOS"]
        for o in range(7):
            for model in ("vig", "beau"):
                for bn, beta in (("same", None), ("AZ", AZ), ("KA", KA)):
                    r = feasible(ct, g, o, model, beta)
                    if r != 0: hits.append((nb, o, model, bn, r))
    return hits
if __name__ == "__main__":
    if sys.argv[1:] == ["control"]:
        rng = random.Random(8); al = list(AZ); rng.shuffle(al); alpha = {c: i for i, c in enumerate(al)}
        g = [(KA.index(c)) for c in "KRYPTOS"]; f = [rng.randrange(26) for _ in range(15)]
        pt = list("WHATSOEVERTHEMESSAGEMAYBEITMUSTBEDELIVEREDTOTHERIGHTPLACEATTHERIGHTTIMESOTHATTHEYCANUNDERSTANDIT"[:97])
        for s, w in CRIBS.items(): pt[s - 1:s - 1 + len(w)] = w
        ctl = "".join(al[(alpha[p] + f[(i + 2) // 7] + g[(i + 2) % 7]) % 26] for i, p in enumerate(pt))
        print("control (KA0, o=2, vig, same) hit:", [h for h in scan(ctl) if h[:4] == ("KA0", 2, "vig", "same")])
    elif sys.argv[1:2] == ["null"]:
        rng = random.Random(int(sys.argv[2])); ctl = "".join(rng.choice(AZ) for _ in range(97))
        print(len(scan(ctl)), "of 168")
    else:
        h = scan(CT); print("K4 feasible/unknown:", len(h), "of 168"); [print("  ", x) for x in h]
