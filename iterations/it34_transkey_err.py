#!/usr/bin/env python3
"""Iteration 34 (H-2104): are w-transkey's exact nulls (19.2M transposed key streams; fixed tableaux and one arbitrary
alphabet vig1/beau1) robust to ONE crib carving error?
Modes: drop    -- any one of the 24 crib rows may be wrong (the 23 others must be consistent);
       shift D -- CT letter(s) omitted/inserted between the cribs: BERLINCLOCK key index shifted by D.
Fast necessary gate: (a) fixed tableaux: <=1 (drop) / 0 (shift) mismatch with the required key letters;
(b) vig1/beau1: the integer crib relations y.k = 0 (mod 26) from the left null space of the crib incidence matrix
(a(C) -+ a(P) = k), restricted to relations not using the dropped row. Survivors get the exact keygen.feasible.
Quagmire-III (self) models are not re-tested here. Reuses transkey.run(); only Ctx.latin/deep are replaced.
Usage: python3 iterations/it34_transkey_err.py drop|shift D [--only FAMILY] [--ct CT]"""
import sys, time
from fractions import Fraction
from math import lcm
import numpy as np
import sympy as sp
sys.path.insert(0, "/mnt/project-files/k4/workers/w-transkey/scripts")
import transkey as TK
from transkey import feasible, NUMB, N

def relations(pairs, model, drop):
    L = sorted({x for _, p, c in pairs for x in (p, c)})
    E = sp.zeros(24, len(L))
    for t, (i, p, c) in enumerate(pairs):
        if t == drop: continue
        E[t, L.index(c)] += 1; E[t, L.index(p)] += -1 if model == "vig1" else 1
    out = []
    for y in E.T.nullspace():
        if drop is not None and y[drop] != 0: continue            # (row zeroed -> unit vector e_drop is in the null space)
        m = lcm(*[Fraction(str(v)).denominator for v in y]); out.append([int(v * m) % 26 for v in y])
    return out

class Err(TK.Ctx):
    def __init__(self, ct, mode, d=0):
        super().__init__(ct); self.mode = mode
        if mode == "shift": self.cidx = self.cidx.copy(); self.cidx[13:] += d
        drops = list(range(24)) if mode == "drop" else [None]
        self.groups = {}
        for model in ("vig1", "beau1"):
            R, starts, owner = [], [], []
            for r in drops:
                rel = relations(self.pairs, model, r)
                if not rel: rel = [[0] * 24]
                starts.append(len(R)); owner.append(r); R += rel
            self.groups[model] = (np.array(R, dtype=np.int64).T, np.array(starts), owner)
        self.maxmis = 1 if mode == "drop" else 0
    def cand(self, X):
        """list per config of candidate (kind, nb/meta, drop row)"""
        X = np.asarray(X, dtype=np.int64)
        mis = (self.req[None, :, :] != X[:, None, :]).sum(2)            # m x 48
        ok = (mis <= self.maxmis).any(1)
        flags = []
        for nb in NUMB:
            V = self.val[nb][X]
            for model, (RT, st, own) in self.groups.items():
                Z = ((V @ RT) % 26 == 0)
                G = np.logical_and.reduceat(Z, st, axis=1)              # m x ndrops
                flags.append((nb, model, G, own)); ok |= G.any(1)
        return ok, mis, flags
    def latin(self, X):
        return self.cand(X)[0]
    def deep(self, x):
        ok, mis, flags = self.cand(x[None, :]); hits = []
        for j in np.nonzero(mis[0] <= self.maxmis)[0]:
            hits.append(("fixed",) + self.reqmeta[j] + (int(np.argmax(self.req[j] != x)) if mis[0, j] else None,))
        for nb, model, G, own in flags:
            for g in np.nonzero(G[0])[0]:
                r = own[g]; keep = [t for t in range(24) if t != r]
                v = self.val[nb][x]; k = [0] * N
                for t in keep: k[self.pairs[t][0] - 1] = int(v[t])
                if feasible(k, model, self.ct, [self.pairs[t] for t in keep]): hits.append((model, nb, r))
        return hits

if __name__ == "__main__":
    a = sys.argv[1:]; mode = a[0]; d = int(a[1]) if mode == "shift" else 0
    ct = a[a.index("--ct") + 1] if "--ct" in a else TK.CT0
    only = a[a.index("--only") + 1] if "--only" in a else None
    ctx = Err(ct, mode, d); rn = TK.Runner(ctx, sys.stdout); t0 = time.time()
    TK.run(ctx, rn, only)
    print(f"TOTAL mode={mode} d={d} configs {rn.n} gate-pass {rn.nlat} hits {len(rn.hits)} time {time.time()-t0:.0f}s", flush=True)
    for f, v in sorted(rn.fam.items()): print(f"  {f:18s} configs {v[0]:>9d} gate {v[1]:>8d} deep-hits {v[2]}", flush=True)
