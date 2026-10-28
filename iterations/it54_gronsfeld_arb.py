#!/usr/bin/env python3
"""it54 (H-1205 x periodic): periodic Gronsfeld (key digits 0..m-1, period p) through ONE arbitrary mixed alphabet,
Vig a(c)=a(p)+k_{i mod p}, Beau a(c)=k-a(p), Var a(c)=a(p)-k. Exact z3 crib feasibility for p=1..48, m=10 (decimal,
e.g. K2 coordinates) and m=26 (= Quagmire III with arbitrary alphabet, reference). Control: planted decimal-key
encryption of English must be SAT at its true period.
Usage: it54_gronsfeld_arb.py [--control]"""
import sys, random, re
from z3 import Solver, Int, Distinct, Or, And
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
def feasible(ct, p, m, form):
    s = Solver(); s.set('timeout', 120000)
    a = [Int(f'a{x}') for x in range(26)]; k = [Int(f'k{j}') for j in range(p)]
    for v in a: s.add(v >= 0, v < 26)
    for v in k: s.add(v >= 0, v < m)
    s.add(Distinct(a)); s.add(a[0] == 0) if form != 1 else None   # vig/var: shift gauge a -> a+s, fix a(A)=0
    for i, pc in CRIB.items():
        c, P, K = a[AZ.index(ct[i])], a[AZ.index(pc)], k[i % p]
        e = (c - P - K) if form == 0 else ((c + P - K) if form == 1 else (c - P + K))
        s.add(Or(e == 0, e == 26, e == -26, e == 52, e == -52))
    return str(s.check())
if __name__ == '__main__':
    if '--control' in sys.argv:
        eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper()); rng = random.Random(54)
        for p, form in ((7, 0), (13, 1), (24, 2), (31, 0)):
            a = list(range(26)); rng.shuffle(a); inv = {v: x for x, v in enumerate(a)}; key = [rng.randrange(10) for _ in range(p)]
            o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97])
            for i, ch in CRIB.items(): P[i] = ch
            ct = ''
            for i, ch in enumerate(P):
                ap = a[AZ.index(ch)]; K = key[i % p]
                ct += AZ[inv[(ap + K) % 26 if form == 0 else ((K - ap) % 26 if form == 1 else (ap - K) % 26)]]
            print(f'control p={p} form={form}: {feasible(ct, p, 10, form)} (must be sat)', flush=True)
        sys.exit()
    for p in range(1, 49):
        row = []
        for m in (10, 26):
            for form in range(3): row.append(f'm{m}f{form}:{feasible(K4, p, m, form)[:3]}')
        print(f'p={p}: ' + ' '.join(row), flush=True)
