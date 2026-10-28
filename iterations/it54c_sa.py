#!/usr/bin/env python3
"""it54c: full-text annealing for periodic Gronsfeld (digits 0..m-1, period p) through ONE arbitrary alphabet,
form vig/beau/var, at the crib-feasible periods of it54. Moves: swap two alphabet values, or reset one key digit.
Score: quadgrams over all 94 windows - W * crib mismatches. Usage:
  it54c_sa.py QG --control p form m [R iters] | --k4 LIST(p:form,...) m [R iters]"""
import sys, random, re, time
import numpy as np
from numba import njit
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
CP = np.array(sorted(CRIB), dtype=np.int64); CV = np.array([AZ.index(CRIB[i]) for i in sorted(CRIB)], dtype=np.int64)
qg = np.fromfile(sys.argv[1], dtype=np.float32)

@njit(cache=True)
def score(c, a, inv, k, p, form, pt, qg, W):
    n = c.shape[0]
    for i in range(n):
        ac = a[c[i]]; K = k[i % p]
        pt[i] = inv[(ac - K) % 26 if form == 0 else ((K - ac) % 26 if form == 1 else (ac + K) % 26)]
    s = 0.0; bad = 0
    for i in range(n - 3): s += qg[((pt[i] * 26 + pt[i + 1]) * 26 + pt[i + 2]) * 26 + pt[i + 3]]
    for t in range(CP.shape[0]):
        if pt[CP[t]] != CV[t]: bad += 1
    return s - W * bad, bad, s

@njit(cache=True)
def anneal(c, p, form, m, qg, iters, seed, W, T0):
    np.random.seed(seed); a = np.random.permutation(26).astype(np.int64); inv = np.empty(26, np.int64)
    for x in range(26): inv[a[x]] = x
    k = np.random.randint(0, m, p).astype(np.int64); pt = np.empty(c.shape[0], np.int64)
    cur, b, q = score(c, a, inv, k, p, form, pt, qg, W); best = cur; ba = a.copy(); bk = k.copy()
    for it in range(iters):
        T = T0 * (1.0 - it / iters) + 0.05
        if np.random.random() < 0.7:
            x = np.random.randint(26); y = np.random.randint(26)
            if x == y: continue
            a[x], a[y] = a[y], a[x]; inv[a[x]] = x; inv[a[y]] = y
            new, nb, nq = score(c, a, inv, k, p, form, pt, qg, W)
            if new >= cur or np.random.random() < np.exp((new - cur) / T):
                cur = new
            else:
                a[x], a[y] = a[y], a[x]; inv[a[x]] = x; inv[a[y]] = y
        else:
            j = np.random.randint(p); old = k[j]; k[j] = np.random.randint(m)
            new, nb, nq = score(c, a, inv, k, p, form, pt, qg, W)
            if new >= cur or np.random.random() < np.exp((new - cur) / T):
                cur = new
            else:
                k[j] = old
        if cur > best: best = cur; ba[:] = a; bk[:] = k
    for x in range(26): inv[ba[x]] = x
    s, b, q = score(c, ba, inv, bk, p, form, pt, qg, W)
    return s, b, q, pt.copy()

def run(ct, p, form, m, R, iters, W=30.0, T0=15.0):
    c = np.array([AZ.index(x) for x in ct], dtype=np.int64); best = None
    for r in range(R):
        s, b, q, pt = anneal(c, p, form, m, qg, iters, r * 7919 + p * 13 + form, W, T0)
        if best is None or s > best[0]: best = (s, b, q / 94, ''.join(AZ[x] for x in pt))
    return best

if __name__ == '__main__':
    mode = sys.argv[2]
    if mode == '--control':
        p, form, m = map(int, sys.argv[3:6]); R = int(sys.argv[6]) if len(sys.argv) > 6 else 20
        it = int(sys.argv[7]) if len(sys.argv) > 7 else 2000000
        eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
        rng = random.Random(p * 100 + form * 10 + m)
        a = list(range(26)); rng.shuffle(a); inv = {v: x for x, v in enumerate(a)}; key = [rng.randrange(m) for _ in range(p)]
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97])
        for i, ch in CRIB.items(): P[i] = ch
        ct = ''.join(AZ[inv[((a[AZ.index(ch)] + key[i % p]) % 26) if form == 0 else (((key[i % p] - a[AZ.index(ch)]) % 26) if form == 1 else ((a[AZ.index(ch)] - key[i % p]) % 26))]] for i, ch in enumerate(P))
        t = time.time(); s, b, mq, d = run(ct, p, form, m, R, it); acc = sum(x == y for x, y in zip(d, P)) / 97
        print(f'control p={p} form={form} m={m}: bad={b} mean={mq:.2f} acc={acc:.2f} {d} {time.time()-t:.0f}s', flush=True)
    else:
        m = int(sys.argv[4]); R = int(sys.argv[5]) if len(sys.argv) > 5 else 20; it = int(sys.argv[6]) if len(sys.argv) > 6 else 2000000
        for cfg in sys.argv[3].split(','):
            p, form = map(int, cfg.split(':')); t = time.time(); s, b, mq, d = run(K4, p, form, m, R, it)
            print(f'K4 p={p} form={form} m={m}: bad={b} mean={mq:.2f} {d} {time.time()-t:.0f}s', flush=True)
