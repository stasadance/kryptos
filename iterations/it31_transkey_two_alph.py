#!/usr/bin/env python3
"""Iteration 31: w-transkey's transposed key streams (H-1701/1502: keyword/keyed-alphabet/K1-K3 text pushed through
decimation, K3 closed form, keyed columnar, grid routes, K3 double rotation; whole or chunked) under TWO arbitrary
alphabets, B(c) = A(p) + n(k), n = AZ or KA index (w-transkey only did fixed tableaux, one alphabet, Quagmire III).
Reuses transkey.run() with the crib index replaced by all 97 positions, so each config yields its full key stream.
Pipeline as it29: Latin gate + K4 additive identity -> exact two-alphabet check -> dedupe -> crib-exact annealing.
Usage: python3 iterations/it31_transkey_two_alph.py WORKDIR CANDS.jsonl [--anneal OUT.jsonl]"""
import sys, os, json
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, "/mnt/project-files/k4/workers/w-transkey/scripts")
import transkey as TK
W, CANDS = sys.argv[1], sys.argv[2]
args = sys.argv[3:]; sys.argv = [sys.argv[0], W]
sys.path.insert(0, "iterations")
import it29_runkey_two_alph as M
from it28b_two_alph_exact import feasible
K4 = M.K4; AZ, KA = M.AZ, M.KA
NB = {"AZ": np.array([AZ.index(AZ[x]) for x in range(26)]), "KA": np.array([KA.index(AZ[x]) for x in range(26)])}

class Full(TK.Ctx):
    def __init__(self, ct):
        super().__init__(ct)
        ci = self.cidx
        self.EQ = [(ci[a], ci[b]) for a, b in self.EQ]; self.NE = [(ci[a], ci[b]) for a, b in self.NE]
        self.cidx = np.arange(97); self.seen = set(); self.stat = [0, 0, 0]; self.f = open(CANDS, "a")
    def deep(self, x):
        for nb, T in NB.items():
            v = T[x]
            if (v[23] + v[33] - v[28] - v[32]) % 26: continue    # k24+k34 = k29+k33 (1-indexed)
            self.stat[0] += 1
            ks = "".join(chr(65 + int(t)) for t in v)
            if ks in self.seen: continue
            self.seen.add(ks); self.stat[1] += 1
            if feasible(K4, [int(t) for t in v]) != 0:
                self.stat[2] += 1; self.f.write(json.dumps({"nb": nb, "key": ks}) + "\n"); self.f.flush()
        return []

if __name__ == "__main__":
    if "--anneal" not in args:
        ctx = Full(K4); rn = TK.Runner(ctx, None)
        TK.run(ctx, rn)
        print(f"configs {rn.n}, latin {rn.nlat}, identity {ctx.stat[0]}, unique {ctx.stat[1]}, exact-not-excluded {ctx.stat[2]}", flush=True)
        for f, v in sorted(rn.fam.items()): print(f"  {f:18s} configs {v[0]:>9d} latin {v[1]:>7d}", flush=True)
        sys.exit()
    out = args[args.index("--anneal") + 1]
    done = {json.loads(l)["tag"] for l in open(out) if l.startswith("{")} if os.path.exists(out) else set()
    todo = []
    for i, l in enumerate(open(CANDS)):
        d = json.loads(l); tag = f"{d['nb']} {d['key']}"
        if tag not in done: todo.append((tag, d["key"], i))
    print(f"to anneal {len(todo)}", flush=True)
    with Pool(4) as P, open(out, "a") as fo:
        for r in P.imap(M.anneal, todo): fo.write(json.dumps(r) + "\n"); fo.flush()
