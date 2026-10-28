#!/usr/bin/env python3
"""it61: progressive periodic keys through ONE arbitrary alphabet (it46 tested only keyword alphabets).
k_i = w_{i mod p} + s*i  ('lin')   or   k_i = w_{i mod p} + s*floor(i/p)  ('blk'),  s = 1..25, w arbitrary,
Vig a(C)=a(P)+k, Beau a(C)=k-a(P), Var a(C)=a(P)-k. Exact z3 per (p, s, form, kind), p = 1..26.
Control: planted encryptions must be SAT. Usage: it61_progressive_arb.py [--control]"""
import sys, random, re
from z3 import Solver, Int, Distinct, Or
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
def feasible(ct, p, s, form, kind):
    S = Solver(); S.set('timeout', 60000)
    a = [Int(f'a{x}') for x in range(26)]; w = [Int(f'w{j}') for j in range(p)]
    for v in a + w: S.add(v >= 0, v < 26)
    S.add(Distinct(a))
    if form != 1: S.add(a[0] == 0)
    for i, pc in CRIB.items():
        K = w[i % p] + (s * i if kind == 'lin' else s * (i // p)) % 26
        c, P = a[AZ.index(ct[i])], a[AZ.index(pc)]
        e = (c - P - K) if form == 0 else ((c + P - K) if form == 1 else (c - P + K))
        S.add(Or(*[e == 26 * t for t in range(-3, 3)]))
    return str(S.check())
if __name__ == '__main__':
    if '--control' in sys.argv:
        eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper()); rng = random.Random(61)
        for p, s, form, kind in ((7, 3, 0, 'lin'), (11, 5, 1, 'blk'), (13, 1, 2, 'lin'), (5, 2, 0, 'blk')):
            a = list(range(26)); rng.shuffle(a); inv = {v: x for x, v in enumerate(a)}; w = [rng.randrange(26) for _ in range(p)]
            o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97])
            for i, ch in CRIB.items(): P[i] = ch
            ct = ''
            for i, ch in enumerate(P):
                K = (w[i % p] + (s * i if kind == 'lin' else s * (i // p))) % 26; ap = a[AZ.index(ch)]
                ct += AZ[inv[(ap + K) % 26 if form == 0 else ((K - ap) % 26 if form == 1 else (ap - K) % 26)]]
            print(f'control p={p} s={s} form={form} {kind}: {feasible(ct, p, s, form, kind)} (must be sat)', flush=True)
        sys.exit()
    for p in range(1, 27):
        sat = []
        for kind in ('lin', 'blk'):
            for s in range(1, 26):
                for form in range(3):
                    r = feasible(K4, p, s, form, kind)
                    if r != 'unsat': sat.append(f'{kind}s{s}f{form}:{r[:3]}')
        print(f'p={p}: ' + (' '.join(sat) if sat else 'all unsat'), flush=True)
