#!/usr/bin/env python3
"""Iteration 32: it25's K3-matrix numeric key streams (NSA Fig. 21 extraction order, rows/columns/reversed, n or n-1
mod 26, every cyclic offset) under TWO arbitrary alphabets, B(c) = A(p) + k. it29 pipeline: gate -> exact -> anneal.
Usage: python3 iterations/it32_k3matrix_two_alph.py WORKDIR"""
import sys, json
import numpy as np
from multiprocessing import Pool
W = sys.argv[1]
sys.path.insert(0, "iterations")
from it25_k3_matrix_key import STREAMS, stream_vals
import it29_runkey_two_alph as M
from it28b_two_alph_exact import feasible
if __name__ == "__main__":
    todo = []; n_all = n_gate = 0
    for name, s in STREAMS.items():
        for sub in (0, 1):
            v = stream_vals(s, sub); ext = np.array((v * 3)[:len(v) + 96], dtype=np.int64)
            offs = M.gate(ext); offs = offs[offs < len(v)]; n_all += len(v); n_gate += len(offs)
            for o in offs:
                k = [int(x) for x in ext[o:o + 97]]
                if feasible(M.K4, k) != 0: todo.append((f"{name} sub={sub} o={o}", "".join(chr(65 + x) for x in k), int(o)))
    print(f"streams {n_all}, gate {n_gate}, exact-not-excluded {len(todo)}", flush=True)
    with Pool(4) as P:
        for r in P.imap(M.anneal, todo): print(json.dumps(r), flush=True)
