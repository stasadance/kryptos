#!/usr/bin/env python3
"""it70b: calibrate it70's one-alphabet m=6 result (K4 SAT, 0/5 nulls) with 40 shuffled-K4 nulls per form.
Usage: it70b_m6_null.py"""
import sys, random; sys.argv = sys.argv[:1]; sys.path.insert(0, 'iterations')
from it70_smalldigit_mask import feasible, K4
rng = random.Random(701); nulls = [''.join(rng.sample(K4, 97)) for _ in range(40)]
for f in (0, 1, 2):
    for m in (5, 6, 7):
        print(f'form={f} m={m}: K4 {feasible(K4, m, f)} | nulls sat {sum(feasible(n, m, f) == "sat" for n in nulls)}/40', flush=True)
