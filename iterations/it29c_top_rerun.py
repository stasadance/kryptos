#!/usr/bin/env python3
"""Iteration 29 follow-up: re-anneal the top-N it29 K4 candidates with more restarts (SA_R, default 24).
Usage: SA_R=24 python3 iterations/it29c_top_rerun.py WORKDIR CORPUS_DIR it29.out [N]"""
import sys, json
W, C, src = sys.argv[1], sys.argv[2], sys.argv[3]; N = int(sys.argv[4]) if len(sys.argv) > 4 else 20
sys.path.insert(0, "iterations"); sys.argv = ["x", W]
import it29_runkey_two_alph as M
from it23_runkey_mixed import norm
from multiprocessing import Pool
rows = sorted((json.loads(l) for l in open(src) if l.startswith("{")), key=lambda x: -x["best"])[:N]
todo = []
for x in rows:
    f, d, nm, o = x["tag"].split(); o = int(o[2:]); t = norm(open(f"{C}/{f}", errors="ignore").read())
    t = t if d == "fwd" else t[::-1]; A = M.AZ if nm == "AZ" else M.KA
    todo.append((x["tag"], "".join(chr(65 + A.index(c)) for c in t[o:o + 97]), o + 1))
with Pool(4) as P:
    for r in P.imap(M.anneal, todo): print(json.dumps(r), flush=True)
