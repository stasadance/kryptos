#!/usr/bin/env python3
"""it61b: shuffled-K4 null SAT rate for it61 configs. Usage: it61b_null.py p s form kind N"""
import sys, random
a = sys.argv[1:]; sys.argv = sys.argv[:1]; sys.path.insert(0, 'iterations')
from it61_progressive_arb import feasible, K4
p, s, form, kind, N = int(a[0]), int(a[1]), int(a[2]), a[3], int(a[4]); rng = random.Random(611); k = 0
for t in range(N):
    l = list(K4); rng.shuffle(l); k += feasible(''.join(l), p, s, form, kind) == 'sat'
print(f'null p={p} s={s} form={form} {kind}: sat {k}/{N}', flush=True)
