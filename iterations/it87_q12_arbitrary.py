#!/usr/bin/env python3
"""it87: EXACT Quagmire-I/II with ONE arbitrary alphabet (the other AZ or KA) and Quagmire-IV with TWO arbitrary
alphabets ("two"), on the three stream libraries never tested under these models: keygen (900k), w-route
(grid routes/overlays x 4 numberings), w-transkey (19.2M transposed periodic/text streams x 4 numberings).
Supersedes coach item 1 (keyword alphabets are a subset of arbitrary alphabets).
Q1: PA arbitrary, CA in {AZ,KA}: PA(p) = CA(c) - k (vig; beau/sum is the negation -> same test).
Q2: CA arbitrary, PA in {AZ,KA}: CA(c) = k + PA(p) (vig) or k - PA(p) (beau).
Exact condition: grouped by the free alphabet's letter, values equal within a group, distinct across groups.
"two": keygen.feasible(k,'two') on the alphabet-free Latin gate survivors.
Usage: it87_q12_arbitrary.py keygen|route|transkey [--ct CT]"""
import sys, time, json
import numpy as np
sys.path.insert(0, "/mnt/project-files/k4/tools"); sys.path.insert(0, "/mnt/project-files/k4/workers/w-transkey/scripts")
sys.path.insert(0, "iterations")
import keygen as KG
AZ, KA = KG.AZ, KG.KA
class Q12:
    def __init__(self, ct):
        self.ct = ct; self.pairs = KG.crib_pairs(ct); self.kidx = np.array([i - 1 for i, _, _ in self.pairs])
        P = [p for _, p, _ in self.pairs]; C = [c for _, _, c in self.pairs]
        def struct(L):
            eq = [(a, b) for a in range(24) for b in range(a + 1, 24) if L[a] == L[b]]
            ne = [(a, b) for a in range(24) for b in range(a + 1, 24) if L[a] != L[b]]
            return np.array(eq).T, np.array(ne).T
        self.tests = []   # (label, base(24,), sign of k, eq, ne)
        for nm, A in (("AZ", AZ), ("KA", KA)):
            self.tests.append((f"Q1-PA*-CA{nm}", np.array([A.index(c) for c in C]), -1) + struct(P))
            pa = np.array([A.index(p) for p in P])
            self.tests.append((f"Q2-PA{nm}-CA*-vig", pa, 1) + struct(C))
            self.tests.append((f"Q2-PA{nm}-CA*-beau", -pa, 1) + struct(C))
    def check(self, V):
        """V: (m,24) key values at crib positions -> list of (row, label)"""
        V = np.asarray(V, dtype=np.int64); out = []
        for lab, base, sg, eq, ne in self.tests:
            Y = (base[None] + sg * V) % 26
            ok = (Y[:, eq[0]] == Y[:, eq[1]]).all(1)
            idx = np.nonzero(ok)[0]
            if len(idx): ok2 = (Y[idx][:, ne[0]] != Y[idx][:, ne[1]]).all(1); out += [(int(i), lab) for i in idx[ok2]]
        return out
def latin(X, pairs):
    P = pairs; EQ = [(a, b) for a in range(24) for b in range(a + 1, 24) if P[a][1] == P[b][1] and P[a][2] == P[b][2]]
    NE = [(a, b) for a in range(24) for b in range(a + 1, 24) if (P[a][1] == P[b][1]) != (P[a][2] == P[b][2])]
    ok = np.ones(len(X), dtype=bool)
    for a, b in EQ: ok &= X[:, a] == X[:, b]
    for a, b in NE: ok &= X[:, a] != X[:, b]
    return ok
class Sink:
    def __init__(self, ct, out):
        self.Q = Q12(ct); self.out = out; self.n = 0; self.nlat = 0; self.hits = 0
    def feed_values(self, V, metas):
        V = np.asarray(V, dtype=np.int64) % 26; self.n += len(V)
        h = self.Q.check(V)
        for i, lab in h: self.emit(metas[i], lab)
        for i in np.nonzero(latin(V, self.Q.pairs))[0]:
            self.nlat += 1; k = [0] * 97
            for t, ix in enumerate(self.Q.kidx): k[ix] = int(V[i, t])
            if KG.feasible(k, "two", self.Q.ct, self.Q.pairs): self.emit(metas[i], "Q4-two")
    def emit(self, meta, lab):
        self.hits += 1; print("HIT", meta, lab, file=self.out, flush=True)
if __name__ == "__main__":
    a = sys.argv[1:]; src = a[0]; ct = a[a.index("--ct") + 1] if "--ct" in a else KG.CT
    S = Sink(ct, sys.stdout); t0 = time.time()
    if src in ("keygen", "route"):
        import it35_keygen_route_err as R
        buf, met = [], []
        for m, k in (R.keygen_streams() if src == "keygen" else R.route_streams()):
            k = list(k) + [0] * max(0, 100 - len(k)); buf.append([k[j] for j in S.Q.kidx]); met.append(m)
            if len(buf) == 50000: S.feed_values(buf, met); buf, met = [], []
        if buf: S.feed_values(buf, met)
    else:
        import transkey as TK
        class Ctx(TK.Ctx):
            def latin(self, X):
                X = np.asarray(X, dtype=np.int64); ok = np.zeros(len(X), dtype=bool)
                for nb in TK.NUMB:
                    V = self.val[nb][X]; ok[[i for i, _ in S.Q.check(V)]] = True
                return ok | latin(X, self.pairs)
            def deep(self, x):
                hits = []
                for nb in TK.NUMB:
                    V = self.val[nb][x][None]; hits += [(lab, nb) for _, lab in S.Q.check(V)]
                    k = [0] * 97
                    for t, ix in enumerate(self.cidx): k[ix] = int(V[0, t])
                    if KG.feasible(k, "two", self.ct, self.pairs): hits.append(("Q4-two", nb))
                return hits
        ctx = Ctx(ct); rn = TK.Runner(ctx, out=sys.stdout); TK.run(ctx, rn)
        S.n, S.nlat, S.hits = rn.n, rn.nlat, len(rn.hits)
    print(f"TOTAL {src} streams {S.n} latin {S.nlat} hits {S.hits} time {time.time()-t0:.0f}s", flush=True)
