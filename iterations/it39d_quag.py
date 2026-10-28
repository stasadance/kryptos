#!/usr/bin/env python3
"""it39d: Quagmire I-IV (Vig/Beau) exact z3 check for every (p, delta), p=1..PMAX, on K4 and on
NNULL permuted-crib-CT nulls (power: fraction of nulls with any SAT delta at that p)."""
import sys, random, time
sys.path.insert(0, '/home/user/kryptos/iterations'); a = sys.argv[1:]; sys.argv = sys.argv[:1]
import it39_periodic_crib_offset as M
from z3 import sat
E = M.E
PMAX = int(a[0]) if a else 14; NNULL = int(a[1]) if len(a) > 1 else 5
pos = [k for k, _ in M.ENE + M.BC]
rng = random.Random(394)
def perm_ct():
    L = [E.CT[k] for k in pos]; rng.shuffle(L)
    ct = list(E.CT)
    for k, x in zip(pos, L): ct[k] = x
    return ''.join(ct)
def sats(ct, p):
    out = []
    for d in range(p):
        pr = M.pairs(ct, d)
        for m, s in M.QMS:
            r = E.QModel(pr, p, m, s, 30000).check()
            if r != E.unsat: out.append((d, m + s, str(r)))
    return out
nulls = [perm_ct() for _ in range(NNULL)]
for p in range(1, PMAX + 1):
    t = time.time()
    k = sats(E.CT, p)
    nn = sum(bool(sats(c, p)) for c in nulls)
    print(f'p={p} K4 SAT/unknown: {k} | nulls with any: {nn}/{NNULL} ({time.time()-t:.0f}s)', flush=True)
