#!/usr/bin/env python3
"""it59: key stream = digits of a mathematical constant (pi, e, phi, sqrt2, sqrt3, sqrt5, ln2, Euler gamma) at every
offset < 100000, used (a) as Gronsfeld digits 0-9, (b) as non-overlapping 2-digit numbers mod 26, through TWO arbitrary
alphabets posC(C) = posP(P) + k (covers Vig/Beau/Var/Quagmire with any alphabets) and through ONE alphabet
(rot=0). Exact union-find + packing check (tools/gromark.solve). Control: planted digit-key encryption at a random
offset must be found. Null: expected survivors from random digit streams. Usage: it59_constant_digits.py"""
import sys, random, re
import mpmath
sys.path.insert(0, 'tools'); import gromark as g
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; ND = 100400
mpmath.mp.dps = ND + 20
CONST = {'pi': mpmath.pi, 'e': mpmath.e, 'phi': mpmath.phi, 'sqrt2': mpmath.sqrt(2), 'sqrt3': mpmath.sqrt(3),
         'sqrt5': mpmath.sqrt(5), 'ln2': mpmath.log(2), 'gamma': mpmath.euler}
def digits(x): s = mpmath.nstr(x, ND, strip_zeros=False).replace('.', ''); return [int(c) for c in s[:ND]]
def streams(d):
    for o in range(len(d) - 200):
        yield o, 'gron', d[o:o + 97]
        yield o, 'pair', [(d[o + 2 * i] * 10 + d[o + 2 * i + 1]) % 26 for i in range(97)]
def check(key):
    return bool(g.solve(key)), bool(g.solve(key, rot=0))
def set_ct(ct): g.CT = ct; g.CRIB[:] = [(s - 1 + j, p, ct[s - 1 + j]) for s, w in g.CRIBS.items() for j, p in enumerate(w)]
if __name__ == '__main__':
    K4 = g.CT; rng = random.Random(59)
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    D = {k: digits(v) for k, v in CONST.items()}; print('digits ready', {k: ''.join(map(str, v[:12])) for k, v in D.items()}, flush=True)
    # control
    for t in range(4):
        name = rng.choice(list(D)); o = rng.randrange(1000, 90000); kind = ('gron', 'pair')[t % 2]
        key = D[name][o:o + 97] if kind == 'gron' else [(D[name][o + 2 * i] * 10 + D[name][o + 2 * i + 1]) % 26 for i in range(97)]
        q = rng.randrange(len(eng) - 200); pt = list(eng[q:q + 97]); pt[21:34] = 'EASTNORTHEAST'; pt[63:74] = 'BERLINCLOCK'
        A = rng.sample(range(26), 26); B = rng.sample(range(26), 26); Bi = {v: i for i, v in enumerate(B)}
        set_ct(''.join(AZ[Bi[(A[AZ.index(p)] + key[i]) % 26]] for i, p in enumerate(pt)))
        print(f'control {name} o={o} {kind}: two-alph pass={check(key)[0]}', flush=True)
    set_ct(K4)
    tot = {}; hits = []
    for name, d in D.items():
        for o, kind, key in streams(d):
            if key[27] != key[65]: continue          # alphabet-free necessary condition X28 == X66 (H-1209)
            two, one = check(key); tot[(name, kind)] = tot.get((name, kind), 0) + two
            if two: hits.append((name, kind, o, one))
        print(name, {k: v for k, v in tot.items() if k[0] == name}, flush=True)
    print('two-alphabet survivors:', len(hits), ' one-alphabet survivors:', sum(h[3] for h in hits))
    for h in hits[:200]: print('  HIT', h)
