#!/usr/bin/env python3
"""it69 (H-708 x periodic): one CT letter was omitted (d=+1) or inserted (d=-1) between the cribs (positions
34..62), like K2's missing S. The key index of BERLINCLOCK is then i+d. Model: periodic Quagmire III through ONE
arbitrary alphabet (key 0..25, period p), Vig/Beau/Var, exact z3 crib feasibility for p=1..48. Null: shuffled K4
at the periods K4 survives. Control: plant an encryption, then delete or insert one CT letter; it must be SAT at
its true (p, d). Usage: it69_omission_periodic.py"""
import sys, random, re
from z3 import Solver, Int, Distinct, Or
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
def feasible(ct, p, form, d):
    s = Solver(); s.set('timeout', 60000)
    a = [Int(f'a{x}') for x in range(26)]; k = [Int(f'k{j}') for j in range(p)]
    for v in a: s.add(v >= 0, v < 26)
    for v in k: s.add(v >= 0, v < 26)
    s.add(Distinct(a))
    if form != 1: s.add(a[0] == 0)
    for i, pc in CRIB.items():
        c, P, K = a[AZ.index(ct[i])], a[AZ.index(pc)], k[(i + (d if i >= 63 else 0)) % p]
        e = (c - P - K) if form == 0 else ((c + P - K) if form == 1 else (c - P + K))
        s.add(Or(e == 0, e == 26, e == -26, e == 52, e == -52))
    return str(s.check())
def plant(rng, eng, p, form, d):
    al = rng.sample(range(26), 26); key = [rng.randrange(26) for _ in range(p)]
    o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 98])
    for i, ch in CRIB.items(): P[i + (d if i >= 63 else 0)] = ch
    inv = {v: x for x, v in enumerate(al)}; C = []
    for i, ch in enumerate(P):
        q = al[AZ.index(ch)]; K = key[i % p]
        C.append(AZ[inv[(q + K) % 26 if form == 0 else ((K - q) % 26 if form == 1 else (q - K) % 26)]])
    if d > 0:                         # true text 98 long, CRIB2 at 64; delete one CT letter in 34..62
        j = rng.randrange(34, 63); C = C[:j] + C[j + 1:]
    else:                             # K4-length 96 true + inserted letter: build 96 with CRIB2 at 62, insert one
        C = C[:96]; j = rng.randrange(34, 63); C = C[:j] + [rng.choice(AZ)] + C[j:]
    return ''.join(C[:97])
if __name__ == '__main__':
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    rng = random.Random(69); good = 0
    for t in range(6):
        p = rng.randrange(3, 15); form = rng.randrange(3); d = rng.choice((1, -1))
        r = feasible(plant(rng, eng, p, form, d), p, form, d); good += r == 'sat'
        print(f'control p={p} form={form} d={d}: {r}', flush=True)
    print(f'controls {good}/6', flush=True)
    for d in (1, -1):
        for form in range(3):
            res = {p: feasible(K4, p, form, d) for p in range(1, 49)}
            print(f'd={d:+d} form={form}: UNSAT p={[p for p, r in res.items() if r == "unsat"]}', flush=True)
            print(f'   feasible/unknown p={[(p, r) for p, r in res.items() if r != "unsat"]}', flush=True)
