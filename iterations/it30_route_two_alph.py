#!/usr/bin/env python3
"""Iteration 30: w-route's grid-route and panel-overlay key streams (H-1804) under TWO arbitrary alphabets,
B(c) = A(p) + n(k), n = AZ or KA index of the key letter (it29 pipeline: alphabet-free gate incl. K4's additive
identity -> exact two-alphabet check (it28b) -> crib-exact full-text annealing of survivors).
Streams come from /mnt/project-files/k4/workers/w-route/scripts/route.py (carved tableau, cipher panel, sculpture,
KA26, Morse; 8 dihedral images x rows/boustrophedon/diagonal/spiral, fwd/rev, every cyclic offset; overlays at
every torus shift).
Usage: python3 iterations/it30_route_two_alph.py WORKDIR [--list-only]"""
import sys, os, json
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, "/mnt/project-files/k4/workers/w-route/scripts")
import route as RT
sys.argv, W = [sys.argv[0], sys.argv[1]] + sys.argv[2:], sys.argv[1]
sys.path.insert(0, "iterations")
import it29_runkey_two_alph as M
from it28b_two_alph_exact import feasible
K4 = M.K4
def cands():
    G = RT.grids(); n_off = n_gate = 0; out = []
    for g, tn, rn, dn, s in RT.streams(G):
        if len(s) < 30: continue
        ext = (s * (97 // len(s) + 2))[:len(s) + 96]             # cyclic stream
        for nm, N in (("AZ", M.AZ), ("KA", M.KA)):
            vals = np.array([N.index(ch) for ch in ext], dtype=np.int64)
            offs = M.gate(vals); offs = offs[offs < len(s)]; n_off += len(s); n_gate += len(offs)
            for o in offs:
                k = list(vals[o:o + 97])
                if feasible(K4, k) != 0: out.append((f"stream {g} {tn} {rn} {dn} {nm} o={o}", "".join(chr(65 + x) for x in k), int(o)))
    for meta, k in RT.overlay_streams(G):
        for nm, N in (("AZ", M.AZ), ("KA", M.KA)):
            vals = np.array([N.index(ch) for ch in k] + [0], dtype=np.int64)  # gate wants len > 97
            n_off += 1
            if len(M.gate(vals)) and 0 in M.gate(vals):
                n_gate += 1
                kk = list(vals[:97])
                if feasible(K4, kk) != 0: out.append((f"overlay {' '.join(map(str, meta))} {nm}", "".join(chr(65 + x) for x in kk), 0))
    print(f"placements {n_off}, gate {n_gate}, exact-not-excluded {len(out)}", flush=True)
    return out
if __name__ == "__main__":
    todo = cands()
    if "--list-only" in sys.argv: sys.exit()
    skip = set()
    if os.environ.get("SKIP") and os.path.exists(os.environ["SKIP"]):
        skip = {json.loads(l)["tag"] for l in open(os.environ["SKIP"]) if l.startswith("{")}
    todo = [t for t in todo if t[0] not in skip]
    print(f"to anneal {len(todo)}", flush=True)
    with Pool(4) as P:
        for r in P.imap(M.anneal, todo): print(json.dumps(r), flush=True)
