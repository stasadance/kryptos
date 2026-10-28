#!/usr/bin/env python3
"""it72 (H-403/H-402): grid key. K4 written in rows of width w; key = r(row) + c(col), with r FREE per row and c
periodic in w, through ONE arbitrary alphabet: a(C_i) = a(P_i) + r[i//w] + c[i%w] (Vig; Beau/Var analogous).
This generalises periodic keys (r constant) and clock-hand keys (r linear). It is motivated by the five CT
doublets that all start at i = 4 mod 7 (BB QQ SS ZZ TT): under w=7 these need a constant column step c5-c4.
Exact z3 feasibility for w=2..34. Null: shuffled K4. Control: planted grid-key encryption.
Usage: it72_grid_key.py"""
import sys, random, re
from z3 import Solver, Int, Distinct, Or
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
def feasible(ct, w, form, off=0):
    s = Solver(); s.set('timeout', 30000)
    a = [Int(f'a{x}') for x in range(26)]; c = [Int(f'c{j}') for j in range(w)]; r = [Int(f'r{j}') for j in range(98 // w + 2)]
    for v in a + c + r: s.add(v >= 0, v < 26)
    s.add(Distinct(a)); s.add(c[0] == 0)
    if form != 1: s.add(a[0] == 0)
    for i, pc in CRIB.items():
        C, P, K = a[AZ.index(ct[i])], a[AZ.index(pc)], r[(i + off) // w] + c[(i + off) % w]
        e = (C - P - K) if form == 0 else ((C + P - K) if form == 1 else (C - P + K))
        s.add(Or([e == 26 * t for t in range(-3, 3)]))
    return str(s.check())
def plant(rng, eng, w, form):
    al = rng.sample(range(26), 26); inv = {v: x for x, v in enumerate(al)}
    c = [rng.randrange(26) for _ in range(w)]; r = [rng.randrange(26) for _ in range(98 // w + 2)]
    o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97])
    for i, ch in CRIB.items(): P[i] = ch
    out = ''
    for i, ch in enumerate(P):
        q = al[AZ.index(ch)]; K = r[i // w] + c[i % w]
        out += AZ[inv[(q + K) % 26 if form == 0 else ((K - q) % 26 if form == 1 else (q - K) % 26)]]
    return out
if __name__ == '__main__':
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    rng = random.Random(72); good = 0
    for t in range(6):
        w = rng.randrange(3, 22); f = rng.randrange(3); res = feasible(plant(rng, eng, w, f), w, f); good += res == 'sat'
        print(f'control w={w} form={f}: {res}', flush=True)
    print(f'controls {good}/6', flush=True)
    nulls = [''.join(rng.sample(K4, 97)) for _ in range(5)]
    for f in range(3):
        for w in range(2, 35):
            res = feasible(K4, w, f)
            ns = sum(feasible(n, w, f) == 'sat' for n in nulls) if res != 'unsat' else '-'
            print(f'form={f} w={w}: K4 {res} | nulls sat {ns}/5', flush=True)
