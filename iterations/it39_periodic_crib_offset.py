#!/usr/bin/env python3
"""it39 (H-904): substitution THEN crib-preserving block transposition.

C = T(S(P)), S periodic (period p, class = plaintext index mod p), T a block/strip shuffle that
keeps each crib contiguous (w-transpo: the only crib-compatible transpositions).  Then the
plaintext gap between EASTNORTHEAST and BERLINCLOCK is unknown, so BERLINCLOCK's key classes are
shifted by an unknown delta mod p relative to the carved positions (delta=0 = plain periodic).
Exact consistency test of the 24 crib pairs for every (p, delta):
  GEN  arbitrary bijection per class
  TAB  Vig/Beau tableau with PA,CA in {AZ,KA}
  Q*   Quagmire I-IV (z3, p<=26)
Null: same test with the 24 crib CT letters redrawn from K4's letter distribution.
Control: plant PT with cribs at random plaintext offsets, encrypt, check true delta passes.
Usage: python3 it39_periodic_crib_offset.py [PMAX] [NNULL]
"""
import sys, random, collections
sys.path.insert(0, '/mnt/project-files/k4/tools')
import errtol as E
from z3 import sat

PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30
NNULL = int(sys.argv[2]) if len(sys.argv) > 2 else 200
A = {'AZ': E.AZ, 'KA': E.KA}
TABS = [(a, b, s) for a in A for b in A for s in 'VB']
QMS = [(m, s) for m in ('Q1AZ', 'Q1KA', 'Q2AZ', 'Q2KA', 'Q3', 'Q4') for s in 'VB']
ENE = [(21 + i, ch) for i, ch in enumerate('EASTNORTHEAST')]   # 0-idx carved pos
BC = [(63 + i, ch) for i, ch in enumerate('BERLINCLOCK')]


def pairs(ct, d):
    return [(k, pl, ct[k]) for k, pl in ENE] + [(k + d, pl, ct[k]) for k, pl in BC]


def tests(ct, p, d, quag=False):
    pr = pairs(ct, d)
    out = {}
    out['GEN'] = E.gen_tables(pr, p) is not None
    for a, b, s in TABS:
        out[f'T{a}{b}{s}'] = E.tab_forced_table(pr, p, A[a], A[b], s) is not None
    if quag:
        for m, s in QMS:
            out[f'{m}{s}'] = E.QModel(pr, p, m, s, 20000).check() == sat
    return out


def null_ct(rng):
    freq = [c for i, c in enumerate(E.CT) if i not in range(21, 34) and i not in range(63, 74)]
    ct = list(E.CT)
    for k, _ in ENE + BC:
        ct[k] = rng.choice(freq)
    return ''.join(ct)


def plant(rng, p, kind):
    """random English-free plant: only crib pairs matter. kind = 'GEN' or ('TAB',a,b,s)."""
    a = rng.randrange(0, 40); b = rng.randrange(a + 13, 86)
    d = (b - a - 42) % p
    if kind == 'GEN':
        perms = [rng.sample(E.AZ, 26) for _ in range(p)]
        enc = lambda k, x: perms[k % p][E.AZ.index(x)]
    else:
        _, pa, ca, s = kind
        key = [rng.randrange(26) for _ in range(p)]
        PA, CA = A[pa], A[ca]
        enc = (lambda k, x: CA[(PA.index(x) + key[k % p]) % 26]) if s == 'V' else \
              (lambda k, x: CA[(key[k % p] - PA.index(x)) % 26])
    ct = list(E.CT)
    for i, (k, ch) in enumerate(ENE):
        ct[k] = enc(a + i, ch)
    for j, (k, ch) in enumerate(BC):
        ct[k] = enc(b + j, ch)
    return ''.join(ct), d


if __name__ == '__main__':
    rng = random.Random(39)
    # --- control ---
    ok = tot = 0
    for p in (5, 7, 8, 11, 13):
        for kind in ['GEN'] + [('TAB',) + t for t in TABS[:4]]:
            for _ in range(3):
                ct, d = plant(rng, p, kind)
                r = tests(ct, p, d % p)
                name = 'GEN' if kind == 'GEN' else 'T%s%s%s' % kind[1:]
                ok += r[name]; tot += 1
    print(f'control: true delta consistent {ok}/{tot}')
    # --- K4 vs null, GEN/TAB ---
    print('p | K4: #delta GEN-ok, TAB-ok list | null mean #delta GEN, P(any TAB)')
    hits = []
    for p in range(1, PMAX + 1):
        kg = []; kt = []
        for d in range(p):
            r = tests(E.CT, p, d)
            if r['GEN']: kg.append(d)
            kt += [(d, n) for n, v in r.items() if n != 'GEN' and v]
        ng = 0; nt = 0
        for _ in range(NNULL):
            ct = null_ct(rng)
            rs = [tests(ct, p, d) for d in range(p)]
            ng += sum(r['GEN'] for r in rs)
            nt += any(v for r in rs for n, v in r.items() if n != 'GEN')
        print(f'{p:2d} | GEN {len(kg):2d}/{p} TAB {kt} | null GEN {ng/NNULL:.2f} TAB {nt/NNULL:.3f}', flush=True)
        hits += [(p, d, n) for d, n in kt]
    # --- Quagmire (z3) on K4 ---
    print('Quagmire SAT (p, delta, model) for p<=min(PMAX,20):')
    for p in range(1, min(PMAX, 20) + 1):
        for d in range(p):
            pr = pairs(E.CT, d)
            for m, s in QMS:
                if E.QModel(pr, p, m, s, 20000).check() == sat:
                    print('  Q', p, d, m + s, flush=True)
