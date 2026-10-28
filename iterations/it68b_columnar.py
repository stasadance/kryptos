#!/usr/bin/env python3
"""it68b: follow-up of it68 survivors from motivated sources (K1-K3 CT, Kryptos tableau). The key stream = a
columnar transposition (width w = 2..7, every column order, both directions: write rows/read columns and the
inverse) of the surviving 97-letter window, checked exactly against the 24 crib key letters.
Control: plant one such key from a tableau window, encrypt English, and require recovery.
Usage: it68b_columnar.py"""
import sys, itertools, random, re
import numpy as np
sys.argv = sys.argv[:1]; sys.path.insert(0, 'iterations')
import it68_transposed_runkey as M
POS = sorted(M.keyletters.__globals__['CRIB'])
CRIB = M.keyletters.__globals__['CRIB']
def perms(w, n=97):
    rows = -(-n // w)
    for order in itertools.permutations(range(w)):
        idx = [r * w + c for c in order for r in range(rows) if r * w + c < n]   # read columns in order
        a = np.array(idx); inv = np.empty(n, dtype=int); inv[a] = np.arange(n)
        yield order, a, inv
def need_vec(ct, X, f):
    out = {}
    for i, p in CRIB.items():
        c, q = X.index(ct[i]), X.index(p)
        out[i] = X[(c - q) % 26 if f == 0 else ((c + q) % 26 if f == 1 else (q - c) % 26)]
    return np.array(POS), np.array([ord(out[i]) for i in POS])
def run(ct, cands):      # cands: list of (name, offset, xn, f)
    hits = []
    for w in range(2, 8):
        P = list(perms(w))
        for name, o, xn, f in cands:
            X = M.AZ if xn == 'AZ' else M.KA; pos, kv = need_vec(ct, X, f)
            win = np.frombuffer(M.SRC[name][o:o + 97].encode(), dtype=np.uint8)
            for order, a, inv in P:
                for d, perm in (('rc', a), ('cr', inv)):
                    if (win[perm[pos]] == kv).all(): hits.append((name, o, xn, f, w, order, d))
    return hits
if __name__ == '__main__':
    rng = random.Random(681); eng = M.SRC['pg1342.txt']; good = 0
    for t in range(4):
        o = rng.randrange(len(M.SRC['kryptos_tableau.txt']) - 97); w = rng.randrange(2, 8)
        order = tuple(rng.sample(range(w), w)); d = rng.choice(('rc', 'cr')); xn = rng.choice(('AZ', 'KA')); f = rng.randrange(3)
        _, a, inv = next((x for x in perms(w) if x[0] == order)); perm = a if d == 'rc' else inv
        win = M.SRC['kryptos_tableau.txt'][o:o + 97]; key = ''.join(win[j] for j in perm)
        po = rng.randrange(len(eng) - 200); Pt = list(eng[po:po + 97]); Pt[21:34] = 'EASTNORTHEAST'; Pt[63:74] = 'BERLINCLOCK'
        ct = M.enc(Pt, key, M.AZ if xn == 'AZ' else M.KA, f)
        h = run(ct, [('kryptos_tableau.txt', o, xn, f)]); found = any(x[4] == w and x[5] == order and x[6] == d for x in h); good += found
        print(f'control o={o} w={w} {order} {d} {xn} f={f}: found={found} hits={len(h)}', flush=True)
    print(f'controls {good}/4', flush=True)
    c = [x for x in M.run(M.K4, {k: M.SRC[k] for k in ('kryptos_ct.txt', 'kryptos_tableau.txt', 'kryptos_pt.txt')})]
    print('it68 survivors from motivated sources:', len(c), flush=True)
    h = run(M.K4, c); print('K4 exact hits', len(h)); [print(' ', x) for x in h[:30]]
