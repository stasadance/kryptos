#!/usr/bin/env python3
"""it54b: null rate of crib feasibility for periodic Gronsfeld/Quagmire III through one arbitrary alphabet:
shuffled K4 (same letters), N trials. Usage: it54b_null.py p m form N"""
import sys, random
sys.argv, args = sys.argv[:1], sys.argv[1:]
sys.path.insert(0, 'iterations')
from it54_gronsfeld_arb import feasible, K4
p, m, form, N = map(int, args); rng = random.Random(p * 1000 + m * 10 + form); sat = 0
for t in range(N):
    l = list(K4); rng.shuffle(l); r = feasible(''.join(l), p, m, form); sat += r == 'sat'
print(f'null p={p} m={m} form={form}: sat {sat}/{N}', flush=True)
