#!/usr/bin/env python3
"""it77: Hagelin M-209 / C-38 style key, k_i = sum_w a_w * pin_w[(i+s_w) mod p_w], periods 26,25,23,21,19,17, lug
weights a_w >= 0 with sum <= 27, Beaufort over AZ (c = k - p mod 26), the M-209 convention, plus a free constant.
Exact z3 feasibility for K4 and nulls. The prediction is "untestable": across the 24 crib positions only the
period-21 wheel reuses pins (63-21 = 2*21), so the other wheels' pins are free. Usage: it77_m209.py"""
import random, sys
from z3 import Solver, Bool, Int, If, Sum, Or
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
PER = (26, 25, 23, 21, 19, 17)
def feasible(ct):
    s = Solver(); s.set('timeout', 120000)
    a = [Int(f'a{w}') for w in range(6)]; c0 = Int('c0')
    pins = [[Bool(f'p{w}_{j}') for j in range(PER[w])] for w in range(6)]
    for v in a: s.add(v >= 0)
    s.add(Sum(a) <= 27, c0 >= 0, c0 < 26)
    for i, p in CRIB.items():
        k = Sum([If(pins[w][i % PER[w]], a[w], 0) for w in range(6)]) + c0
        e = k - AZ.index(p) - AZ.index(ct[i])
        s.add(Or([e == 26 * t for t in range(-2, 4)]))
    return str(s.check())
if __name__ == '__main__':
    rng = random.Random(77)
    print('K4', feasible(K4), flush=True)
    print('nulls', [feasible(''.join(rng.sample(K4, 97))) for _ in range(5)], flush=True)
