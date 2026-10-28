#!/usr/bin/env python3
"""it39c: is K4's 5/8 GEN-consistent deltas at p=8 special?  Null = permuted crib CT letters,
conditioned on each crib being self-consistent alone at p (the intra-crib constraint is
delta-independent, so the honest statistic is #delta-ok GIVEN intra-ok)."""
import sys, random, collections
sys.path.insert(0, '/home/user/kryptos/iterations'); sys.argv = sys.argv[:1] + ['8', '1']
import it39_periodic_crib_offset as M
E = M.E
pos = [k for k, _ in M.ENE + M.BC]
rng = random.Random(8)
def intra(ct, p):
    a = [(k, pl, ct[k]) for k, pl in M.ENE]; b = [(k, pl, ct[k]) for k, pl in M.BC]
    return E.gen_tables(a, p) is not None and E.gen_tables(b, p) is not None
for p in (6, 8, 10, 11, 12, 16):
    kg = sum(E.gen_tables(M.pairs(E.CT, d), p) is not None for d in range(p))
    H = collections.Counter(); n = 0
    while n < 20000:
        L = [E.CT[k] for k in pos]; rng.shuffle(L)
        ct = list(E.CT)
        for k, x in zip(pos, L): ct[k] = x
        ct = ''.join(ct)
        if not intra(ct, p): continue
        n += 1
        H[sum(E.gen_tables(M.pairs(ct, d), p) is not None for d in range(p))] += 1
    tail = sum(v for g, v in H.items() if g >= kg) / n
    print(f'p={p} K4 {kg}/{p} intra-ok={intra(E.CT,p)} | null|intra-ok dist {dict(sorted(H.items()))} P(>=K4)={tail:.4f}', flush=True)
