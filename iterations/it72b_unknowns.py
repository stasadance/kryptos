#!/usr/bin/env python3
"""it72b: rerun it72's UNKNOWN (timeout) grid-key cases on K4 with a 900 s z3 timeout.
Usage: it72b_unknowns.py"""
import sys; sys.argv = sys.argv[:1]; sys.path.insert(0, 'iterations')
import it72_grid_key as G
from z3 import Solver
CASES = {0: [4, 5, 7, 8, 13], 1: [3, 4, 7, 8, 12, 14], 2: [3, 5, 7, 10]}
orig = G.Solver
class S(orig):
    def set(self, *a):
        super().set('timeout', 900000)
G.Solver = S
for w in (7, 8, 4, 5, 3, 10, 12, 13, 14):
    for f, ws in CASES.items():
        if w in ws: print(f'form={f} w={w}: K4 {G.feasible(G.K4, w, f)}', flush=True)
