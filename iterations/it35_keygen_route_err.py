#!/usr/bin/env python3
"""Iteration 35 (H-2104, continued): w-keygen's generator families (F0-F5, F2 two-keyword; ~900k value streams) and
w-route's grid-route/overlay letter streams (1.59M placements x 4 numberings) re-screened with ONE wrong crib row
(drop) or a 1-2 letter CT slip between the cribs (shift d). Models: 12 fixed tableaux (<=1 / 0 mismatch) and one
arbitrary alphabet vig1/beau1 (integer crib-relation gate from it34, then exact keygen.feasible).
Usage: python3 iterations/it35_keygen_route_err.py keygen|route drop|shift D [--ct CT]"""
import sys, time
import numpy as np
sys.path.insert(0, "/mnt/project-files/k4/tools"); sys.path.insert(0, "iterations")
import keygen as KG
from it34_transkey_err import relations
class Screen:
    def __init__(self, ct, mode, d=0):
        self.ct = ct; self.pairs = KG.crib_pairs(ct); self.mode = mode
        self.kidx = np.array([i - 1 for i, _, _ in self.pairs]); self.kidx[13:] += d if mode == "shift" else 0
        req = KG.required_keys(ct); self.tabs = list(req); self.req = np.array([[v for _, v in req[t]] for t in self.tabs])
        drops = list(range(24)) if mode == "drop" else [None]; self.groups = {}
        for model in ("vig1", "beau1"):
            R, st, own = [], [], []
            for r in drops:
                rel = relations(self.pairs, model, r) or [[0] * 24]; st.append(len(R)); own.append(r); R += rel
            self.groups[model] = (np.array(R, dtype=np.int64).T, np.array(st), own)
        self.maxmis = 1 if mode == "drop" else 0; self.n = self.gate = 0; self.hits = []
    def feed(self, V, metas):
        """V: (m,97+) key VALUE streams; metas: list of labels"""
        V = np.asarray(V, dtype=np.int64)[:, self.kidx] % 26; self.n += len(V)
        mis = (self.req[None] != V[:, None]).sum(2); ok = (mis <= self.maxmis).any(1); G = {}
        for model, (RT, st, own) in self.groups.items():
            G[model] = np.logical_and.reduceat((V @ RT) % 26 == 0, st, axis=1); ok |= G[model].any(1)
        for i in np.nonzero(ok)[0]:
            self.gate += 1; h = [("fixed",) + self.tabs[j] for j in np.nonzero(mis[i] <= self.maxmis)[0]]
            for model, (RT, st, own) in self.groups.items():
                for g in np.nonzero(G[model][i])[0]:
                    r = own[g]; keep = [t for t in range(24) if t != r]; k = [0] * 97
                    for t in keep: k[self.pairs[t][0] - 1] = int(V[i, t])
                    if KG.feasible(k, model, self.ct, [self.pairs[t] for t in keep]): h.append((model, r))
            if h: self.hits.append((metas[i], h)); print("HIT", metas[i], h, flush=True)
def keygen_streams():
    for fam, par, k, sym in KG.families(): yield f"{fam} {par}", k
    for fam, par, k, sym in KG.twokey_families(): yield f"{fam} {par}", k
def route_streams():
    sys.path.insert(0, "/mnt/project-files/k4/workers/w-route/scripts"); import route as RT
    G = RT.grids()
    for g, tn, rn, dn, s in RT.streams(G):
        if len(s) < 30: continue
        ext = (s * (100 // len(s) + 2))
        for o in range(len(s)):
            for nb, (A, dd) in KG.NUMBERINGS.items():
                yield f"stream {g} {tn} {rn} {dn} o={o} {nb}", [(A.index(c) + dd) % 26 for c in ext[o:o + 100]]
    for meta, k in RT.overlay_streams(G):
        for nb, (A, dd) in KG.NUMBERINGS.items():
            yield f"overlay {meta} {nb}", [(A.index(c) + dd) % 26 for c in k] + [0, 0, 0]
if __name__ == "__main__":
    a = sys.argv[1:]; src, mode = a[0], a[1]; d = int(a[2]) if mode == "shift" else 0
    ct = a[a.index("--ct") + 1] if "--ct" in a else KG.CT
    S = Screen(ct, mode, d); t0 = time.time(); buf, met = [], []
    for m, k in (keygen_streams() if src == "keygen" else route_streams()):
        k = list(k) + [0] * max(0, 100 - len(k)); buf.append(k[:100]); met.append(m)
        if len(buf) == 20000: S.feed(buf, met); buf, met = [], []
    if buf: S.feed(buf, met)
    print(f"TOTAL {src} mode={mode} d={d} streams {S.n} gate {S.gate} hits {len(S.hits)} time {time.time()-t0:.0f}s", flush=True)
