#!/usr/bin/env python3
"""it53 (H-1208 follow-up): CT-autokey under ONE arbitrary mixed alphabet, 9 models
(key K = a(C_{i-L}) | AZ index | KA index; vig a(c)=a(p)+K, beau a(c)=K-a(p), var a(c)=a(p)-K), lags 1..73.
CT is always known, so given the alphabet the plaintext at i >= L is fixed: no chain, smooth landscape.
Stage 1: exact crib feasibility (z3, all 24 crib positions with i >= L). Stage 2: for feasible configs, annealing over
the alphabet with quadgrams on P[L..96] plus a heavy crib penalty; planted controls at the same L.
Usage: it53_ctautokey_arb.py QG --z3 | --null L f k seed | --sa LIST(L:f:k,...) [restarts iters] | --control L f k [restarts iters]"""
import sys, random, re, time
import numpy as np
from numba import njit
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; KA = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
KAI = np.array([KA.index(c) for c in AZ], dtype=np.int64)
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
CP = np.array(sorted(CRIB), dtype=np.int64); CV = np.array([AZ.index(CRIB[i]) for i in sorted(CRIB)], dtype=np.int64)
qg = np.fromfile(sys.argv[1], dtype=np.float32)

def z3check(ct, L, form, kr):
    from z3 import Solver, Int, Distinct, Or
    s = Solver(); s.set('timeout', 60000); a = [Int(f'a{x}') for x in range(26)]
    for v in a: s.add(v >= 0, v < 26)
    s.add(Distinct(a)); n = 0
    for i in CRIB:
        if i - L < 0: continue
        c, p, q = AZ.index(ct[i]), AZ.index(CRIB[i]), AZ.index(ct[i - L]); n += 1
        K = a[q] if kr == 0 else (q if kr == 1 else int(KAI[q]))
        e = (a[c] - a[p] - K) if form == 0 else ((a[c] + a[p] - K) if form == 1 else (a[c] - a[p] + K))
        s.add(Or(e == 0, e == 26, e == -26, e == 52, e == -52))
    if kr != 0 and form != 1: s.add(a[AZ.index(ct[73])] == 0)
    return str(s.check()), n

@njit(cache=True)
def dec(c, a, inv, L, form, kr, p):
    for i in range(c.shape[0]):
        if i < L: p[i] = -1; continue
        q = c[i - L]; K = a[q] if kr == 0 else (q if kr == 1 else KAI[q]); ac = a[c[i]]
        v = (ac - K) % 26 if form == 0 else ((K - ac) % 26 if form == 1 else (ac + K) % 26)
        p[i] = inv[v]

@njit(cache=True)
def score(c, a, inv, L, form, kr, p, qg, W):
    dec(c, a, inv, L, form, kr, p); s = 0.0; bad = 0
    for i in range(L, c.shape[0] - 3): s += qg[((p[i] * 26 + p[i + 1]) * 26 + p[i + 2]) * 26 + p[i + 3]]
    for t in range(CP.shape[0]):
        if CP[t] >= L and p[CP[t]] != CV[t]: bad += 1
    return s - W * bad, bad, s

@njit(cache=True)
def anneal(c, L, form, kr, qg, iters, seed, W, T0):
    np.random.seed(seed); a = np.random.permutation(26).astype(np.int64); inv = np.empty(26, np.int64)
    for x in range(26): inv[a[x]] = x
    p = np.empty(c.shape[0], np.int64); cur, bad, q = score(c, a, inv, L, form, kr, p, qg, W); best = cur; ba = a.copy()
    for it in range(iters):
        T = T0 * (1.0 - it / iters) + 0.05
        x = np.random.randint(26); y = np.random.randint(26)
        if x == y: continue
        a[x], a[y] = a[y], a[x]; inv[a[x]] = x; inv[a[y]] = y
        new, nb, nq = score(c, a, inv, L, form, kr, p, qg, W)
        if new >= cur or np.random.random() < np.exp((new - cur) / T):
            cur = new
            if cur > best: best = cur; ba[:] = a
        else:
            a[x], a[y] = a[y], a[x]; inv[a[x]] = x; inv[a[y]] = y
    for x in range(26): inv[ba[x]] = x
    s, bad, q = score(c, ba, inv, L, form, kr, p, qg, W)
    return s, bad, q, ba, p.copy()

def run(ct, L, form, kr, R=8, iters=300000, W=30.0, T0=15.0):
    c = np.array([AZ.index(x) for x in ct], dtype=np.int64); best = None
    for r in range(R):
        s, bad, q, a, p = anneal(c, L, form, kr, qg, iters, r * 7919 + L * 31 + form * 7 + kr, W, T0)
        n = c.shape[0] - L - 3; m = q / n
        if best is None or s > best[0]: best = (s, bad, m, ''.join(AZ[x] if x >= 0 else '.' for x in p))
    return best

def plant(rng, L, form, kr, eng):
    a = list(range(26)); rng.shuffle(a); inv = [0] * 26
    for x in range(26): inv[a[x]] = x
    o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97])
    for i, ch in CRIB.items(): P[i] = ch
    pi = [AZ.index(x) for x in P]; ct = [rng.randrange(26) for _ in range(L)]
    for i in range(L, 97):
        q = ct[i - L]; K = a[q] if kr == 0 else (q if kr == 1 else int(KAI[q]))
        v = (a[pi[i]] + K) % 26 if form == 0 else ((K - a[pi[i]]) % 26 if form == 1 else (a[pi[i]] - K) % 26)
        ct.append(inv[v])
    return ''.join(AZ[x] for x in ct), ''.join(P)

if __name__ == '__main__':
    mode = sys.argv[2]
    if mode == '--z3':
        for L in range(1, 74):
            row = []
            for form in range(3):
                for kr in range(3):
                    r, n = z3check(K4, L, form, kr)
                    if r != 'unsat': row.append(f'f{form}k{kr}:{r}({n})')
            print(f'L={L}: ' + (' '.join(row) if row else 'all unsat'), flush=True)
    elif mode == '--control':
        L, form, kr = map(int, sys.argv[3:6]); R = int(sys.argv[6]) if len(sys.argv) > 6 else 8
        it = int(sys.argv[7]) if len(sys.argv) > 7 else 300000
        eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
        rng = random.Random(L * 100 + form * 10 + kr); ct, P = plant(rng, L, form, kr, eng); t = time.time()
        s, bad, m, d = run(ct, L, form, kr, R, it); acc = sum(x == y for x, y in zip(d[L:], P[L:])) / (97 - L)
        print(f'control L={L} f={form} k={kr}: bad={bad} mean={m:.2f} acc={acc:.2f} {d} {time.time()-t:.0f}s', flush=True)
    elif mode == '--null':   # same search on shuffled K4 (no planted truth): the junk level an SA "best" reaches
        L, form, kr, seed = map(int, sys.argv[3:7]); l = list(K4); random.Random(seed).shuffle(l); t = time.time()
        s, bad, m, d = run(''.join(l), L, form, kr, 30, 2000000)
        print(f'null L={L} f={form} k={kr} seed={seed}: bad={bad} mean={m:.2f} {d} {time.time()-t:.0f}s', flush=True)
    else:
        R = int(sys.argv[4]) if len(sys.argv) > 4 else 8; it = int(sys.argv[5]) if len(sys.argv) > 5 else 300000
        for cfg in sys.argv[3].split(','):
            L, form, kr = map(int, cfg.split(':')); t = time.time()
            s, bad, m, d = run(K4, L, form, kr, R, it)
            print(f'K4 L={L} f={form} k={kr}: bad={bad} mean={m:.2f} {d} {time.time()-t:.0f}s', flush=True)
