#!/usr/bin/env python3
"""it90c: exact Hill n=4,5 (linear, affine) row counts on K4 + planted controls (English with cribs, random invertible
D, e): each row must use every crib position in its residue. usage: it90c_exact.py"""
import sys, random, math, re
import numpy as np
sys.path.insert(0, 'iterations'); import it90_hill4_affine as H
TXT = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/carter1.txt').read().upper())
def counts(ct, n, aff):
    out = {}
    for an, A in (('AZ', H.AZ), ('KA', H.KA)):
        c = np.array([A.index(x) for x in ct])
        for o in range(n):
            r = H.rows_for(c, A, n, o, aff); out[(an, o)] = [len(x) for x in r]
    return out
def plant(n, aff, seed):
    g = random.Random(seed); o = g.randrange(len(TXT) - 200); pt = list(TXT[o:o + 97])
    for k, v in H.CRIB.items(): pt[k] = v
    A = g.choice([H.AZ, H.KA]); off = g.randrange(n)
    while True:
        M = np.array([[g.randrange(26) for _ in range(n)] for _ in range(n)]); d = int(round(np.linalg.det(M))) % 26
        if d % 2 and d % 13: break
    b = np.array([g.randrange(26) if aff else 0 for _ in range(n)]); p = np.array([A.index(x) for x in pt]); c = p.copy()
    for s in range(off, 97 - n + 1, n): c[s:s + n] = (M @ p[s:s + n] + b) % 26
    ct = ''.join(A[x] for x in c); cn = counts(ct, n, aff)
    return all(min(v) > 0 for k, v in cn.items() if k == ((('AZ' if A == H.AZ else 'KA'), off)))
CFG = [tuple(map(int, x.split(':'))) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [(4, 0), (4, 1), (5, 0), (5, 1)]
for n, aff in CFG:
    if True:
        pl = sum(plant(n, aff, 90 + s) for s in range(5))
        cn = counts(H.CT, n, aff); alive = {k: v for k, v in cn.items() if min(v) > 0}
        print(f'n={n} {"aff" if aff else "lin"}: plants {pl}/5; K4 alive configs {len(alive)}/{len(cn)}', {k: v for k, v in alive.items()}, flush=True)
