#!/usr/bin/env python3
"""it72c: proper null calibration of the w=7 grid key (K4 SAT in all forms at 900 s). 10 shuffled-K4 nulls per
form at w=7 with a 900 s timeout, reporting sat/unsat/unknown. Usage: it72c_w7_null.py"""
import sys, random; sys.argv = sys.argv[:1]; sys.path.insert(0, 'iterations')
import it72_grid_key as G
orig = G.Solver
class S(orig):
    def set(self, *a): super().set('timeout', 900000)
G.Solver = S
rng = random.Random(723); nulls = [''.join(rng.sample(G.K4, 97)) for _ in range(10)]
for f in (0, 1, 2):
    r = [G.feasible(n, 7, f) for n in nulls]
    print(f'form={f} w=7 nulls: sat {r.count("sat")} unsat {r.count("unsat")} unknown {r.count("unknown")}', flush=True)
