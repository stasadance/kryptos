#!/usr/bin/env python3
"""Iteration 7: separable grid key k = f(row) + g(col) under UNKNOWN mixed alphabet(s).

Motivation (it06): the K4 doublets cluster at i = 4 mod 7 and every crib-covered residue-4 pair is a
doublet although the plaintext differs (NO->QQ, ST->SS, IN->TT). A plaintext-independent random key
makes that very unlikely (~1e-5). A key with a column component g of width 7 explains it: inside
each row the step k(i+1)-k(i) is the same at every residue-4 boundary, so the doublets happen
exactly where alpha(p_{i+1}) - alpha(p_i) = -(g5 - g4).
it01 refuted this only for FIXED tableaux. Here alpha (and beta) are unknown permutations (z3).
Models: "q3v" beta=alpha, beta(c)=alpha(p)+k ; "q3b" beta=alpha, beta(c)=k-alpha(p) ;
        "two" independent alpha, beta, beta(c)=alpha(p)+k.
"""
import sys, random
CT = open("data/ciphertext.txt").read().strip()
CRIBS = {22: "EASTNORTHEAST", 64: "BERLINCLOCK"}
PAIRS = [(s - 1 + j, p) for s, w in CRIBS.items() for j, p in enumerate(w)]

def sat(ct, w, o, model):
    """Exact via OR-tools CP-SAT: integer slack t makes each crib equation hold mod 26."""
    from ortools.sat.python import cp_model
    M = cp_model.CpModel()
    letters = sorted({p for _, p in PAIRS} | {ct[i] for i, _ in PAIRS})
    A = {L: M.NewIntVar(0, 25, "a" + L) for L in letters}
    B = A if model != "two" else {L: M.NewIntVar(0, 25, "b" + L) for L in letters}
    M.AddAllDifferent(list(A.values()))
    if model == "two": M.AddAllDifferent(list(B.values()))
    F = {r: M.NewIntVar(0, 25, f"f{r}") for r in {(i + o) // w for i, _ in PAIRS}}
    G = {c: M.NewIntVar(0, 25, f"g{c}") for c in {(i + o) % w for i, _ in PAIRS}}
    for n, (i, p) in enumerate(PAIRS):
        t = M.NewIntVar(-4, 4, f"t{n}")
        sg = -1 if model != "q3b" else 1
        M.Add(B[ct[i]] + sg * A[p] - F[(i + o) // w] - G[(i + o) % w] == 26 * t)
    S = cp_model.CpSolver(); S.parameters.max_time_in_seconds = 30; S.parameters.num_workers = 1
    r = S.Solve(M)
    return {cp_model.OPTIMAL: "sat", cp_model.FEASIBLE: "sat", cp_model.INFEASIBLE: "unsat"}.get(r, "unknown")

def scan(ct, models=("q3v", "q3b", "two"), widths=range(2, 49)):
    out = {}
    for m in models:
        out[m] = [(w, o) for w in widths for o in range(w) if sat(ct, w, o, m) == "sat"]
    return out

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "k4"
    if which == "control":
        rng = random.Random(4); alpha = list(range(26)); rng.shuffle(alpha)
        AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; inv = {v: AZ[i] for i, v in enumerate(alpha)}
        pt = list(("SOMEPLANTEDENGLISHTEXTUSEDASACONTROLFORTHEMIXEDALPHABETGRIDKEYTESTWHICHNEEDSNINETYSEVENLETTERSINTOTAL")[:97])
        for s0, wd in CRIBS.items(): pt[s0 - 1:s0 - 1 + len(wd)] = wd
        W, O = 7, 3; f = [rng.randrange(26) for _ in range(20)]; g = [rng.randrange(26) for _ in range(W)]
        ctl = "".join(inv[(alpha[AZ.index(p)] + f[(i + O) // W] + g[(i + O) % W]) % 26] for i, p in enumerate(pt))
        print("control planted q3v w=7 o=3 found:", (7, 3) in scan(ctl, ("q3v",), range(7, 8))["q3v"])
    elif which == "null":
        rng = random.Random(int(sys.argv[2])); AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ct = "".join(rng.choice(AZ) for _ in range(97)); res = scan(ct, ("q3v", "q3b"), range(2, 31))
        print({m: len(v) for m, v in res.items()})
    else:
        res = scan(CT, ("q3v", "q3b"), range(2, 49))
        for m, v in res.items(): print(m, len(v), v[:40])
