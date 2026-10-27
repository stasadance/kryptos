#!/usr/bin/env python3
"""Iteration 29: running key from a source text under TWO arbitrary alphabets, B(c) = A(p) + n(k), n = AZ or KA index
of the key letter (Beaufort/variant forms are the same model up to reflecting A and B).
Pipeline per offset: (1) alphabet-free gate on the key values at the cribs: k28 = k66, the 22 crib inequalities,
and the K4-specific additive identity k24 + k34 = k29 + k33 (all 1-indexed); (2) exact two-alphabet linear check
(it28b.feasible); (3) full-text crib-exact annealing (it05 sa.c) of what survives, compared with it05 null/controls.
Usage: python3 iterations/it29_runkey_two_alph.py WORKDIR text1 [text2 ...]"""
import sys, os, json, subprocess, itertools
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, "iterations"); sys.path.insert(0, "tools")
from it28b_two_alph_exact import feasible
import latin_filter as LF
from it23_runkey_mixed import norm
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; K4 = open("data/ciphertext.txt").read().strip()
W = sys.argv[1]
def gate(vals):
    """vals: (n,) key values for the whole text; returns offsets o where the stream vals[o:o+97] passes."""
    n = len(vals) - 97
    if n <= 0: return np.array([], dtype=np.int64)
    V = lambda pos: vals[pos - 1: pos - 1 + n]          # 1-indexed crib position
    ok = np.ones(n, dtype=bool)
    for i, j in LF.EQ: ok &= V(i) == V(j)
    for i, j in LF.NE: ok &= V(i) != V(j)
    ok &= (V(24) + V(34) - V(29) - V(33)) % 26 == 0
    return np.nonzero(ok)[0]
def anneal(a):
    tag, ks, seed = a
    out = subprocess.run([os.path.join(W, "sa"), "2", "0", K4, ks, os.environ.get("SA_R", "8"), os.environ.get("SA_IT", "3000000"), str(seed), "25"], cwd=W, capture_output=True, text=True).stdout.split("\n")
    res = [(float(l.split()[0]), l.split()[1]) for l in out if l.strip()]; b = max(res)
    return dict(tag=tag, best=b[0], dec=b[1])
if __name__ == "__main__":
    todo = []; tot = 0
    for f in sys.argv[2:]:
        raw = norm(open(f, errors="ignore").read())
        for d, t in (("fwd", raw), ("rev", raw[::-1])):
            for nm, N in (("AZ", AZ), ("KA", KA)):
                vals = np.array([N.index(ch) for ch in t], dtype=np.int64)
                offs = gate(vals); ex = [o for o in offs if feasible(K4, list(vals[o:o + 97])) != 0]
                tot += len(t) - 97
                print(f"{os.path.basename(f)} {d} {nm}: {len(t)-97} offsets, gate {len(offs)}, exact {len(ex)}", flush=True)
                todo += [(f"{os.path.basename(f)} {d} {nm} o={o}", "".join(chr(65 + x) for x in vals[o:o + 97]), int(o)) for o in ex]
    skip = set()
    if os.environ.get("SKIP"): skip = {json.loads(l)["tag"] for l in open(os.environ["SKIP"]) if l.startswith("{")}
    todo = [t for t in todo if t[0] not in skip]
    print(f"total offsets {tot}, to anneal {len(todo)}", flush=True)
    with Pool(4) as P:
        for r in P.imap(anneal, todo): print(json.dumps(r), flush=True)
