#!/usr/bin/env python3
"""it70 (H-1205): non-periodic small-digit key (each k_i in 0..m-1, free per position, e.g. coordinates or a
date) through mixed alphabets. One alphabet: a(C)=a(P)+k (Vig), k-a(P) (Beau), a(P)-k (Var). Two alphabets:
b(C)=a(P)+k. Exact z3 feasibility of the 24 crib pairs for m=2..13. Null: shuffled K4. Control: planted
encryption at its true m. Usage: it70_smalldigit_mask.py"""
import sys, random, re
from z3 import Solver, Int, Distinct, Or, And
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
def feasible(ct, m, form, two=False):
    s = Solver(); s.set('timeout', 60000)
    a = [Int(f'a{x}') for x in range(26)]; b = [Int(f'b{x}') for x in range(26)] if two else a
    for v in set(a + b): s.add(v >= 0, v < 26)
    s.add(Distinct(a)); s.add(Distinct(b)) if two else None
    for i, pc in CRIB.items():
        c, P = b[AZ.index(ct[i])], a[AZ.index(pc)]
        e = (c - P) if form == 0 else ((c + P) if form == 1 else (P - c))   # value of k mod 26
        s.add(Or([Or(e == k, e == k + 26, e == k - 26, e == k + 52) for k in range(m)]))
    return str(s.check())
def plant(rng, eng, m, form):
    al = rng.sample(range(26), 26); inv = {v: x for x, v in enumerate(al)}
    o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97])
    for i, ch in CRIB.items(): P[i] = ch
    out = ''
    for ch in P:
        q = al[AZ.index(ch)]; k = rng.randrange(m)
        out += AZ[inv[(q + k) % 26 if form == 0 else ((k - q) % 26 if form == 1 else (q - k) % 26)]]
    return out
if __name__ == '__main__':
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    rng = random.Random(70); good = 0
    for t in range(6):
        m = rng.randrange(2, 11); f = rng.randrange(3); r = feasible(plant(rng, eng, m, f), m, f); good += r == 'sat'
        print(f'control m={m} form={f}: {r}', flush=True)
    print(f'controls {good}/6', flush=True)
    nulls = [''.join(rng.sample(K4, 97)) for _ in range(5)]
    for two in (False, True):
        for f in ((0, 1, 2) if not two else (0,)):
            for m in range(2, 14):
                r = feasible(K4, m, f, two); nr = sum(feasible(n, m, f, two) == 'sat' for n in nulls)
                print(f'{"two" if two else "one"} alph form={f} m={m}: K4 {r} | nulls sat {nr}/5', flush=True)
