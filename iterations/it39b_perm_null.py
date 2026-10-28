#!/usr/bin/env python3
"""it39b: rerun it39 GEN/TAB with a stricter null: permute K4's own 24 crib CT letters among the
crib positions (keeps the letter multiset; it39's iid null did not). p=1..PMAX.
Also reports, per p, the null tail P(#delta GEN-ok >= K4's)."""
import sys, random
sys.path.insert(0, '/home/user/kryptos/iterations'); sys.argv[1:] = sys.argv[1:] or ['48', '400']
import it39_periodic_crib_offset as M
E = M.E
PMAX, N = int(sys.argv[1]), int(sys.argv[2])
pos = [k for k, _ in M.ENE + M.BC]
rng = random.Random(391)
def perm_ct():
    L = [E.CT[k] for k in pos]; rng.shuffle(L)
    ct = list(E.CT)
    for k, x in zip(pos, L): ct[k] = x
    return ''.join(ct)
def count(ct, p):
    g = t = 0
    for d in range(p):
        r = M.tests(ct, p, d)
        g += r['GEN']; t += sum(v for n, v in r.items() if n != 'GEN')
    return g, t
print('p | K4 GEN-ok TAB-ok | perm-null mean GEN, P(null GEN>=K4), P(any TAB)')
for p in range(1, PMAX + 1):
    kg, kt = count(E.CT, p)
    ns = [count(perm_ct(), p) for _ in range(N)]
    mg = sum(g for g, _ in ns) / N
    tail = sum(g >= kg for g, _ in ns) / N
    at = sum(t > 0 for _, t in ns) / N
    print(f'{p:2d} | {kg:2d}/{p} {kt} | {mg:.2f} {tail:.3f} {at:.3f}', flush=True)
