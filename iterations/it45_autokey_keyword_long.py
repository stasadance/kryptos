#!/usr/bin/env python3
"""it45: PT-autokey lag L = 14..96 under a keyword-mixed alphabet (49k vocabulary), 9 models (as it42).
Propagate every crib letter along its chain both ways (P_{i+L} from P_i and C_{i+L}; P_{i-L} = key value at i
inverted), mark conflicts with crib letters / between chains.  Pass = no conflict.  Survivors: report the
determined plaintext fraction and quadgram score of determined runs.  Control: plant."""
import sys, re, random
sys.argv[1:] = sys.argv[1:] or ["/tmp/claude-0/it27/qg.bin"]
import numpy as np
from numba import njit
sys.path.insert(0, 'iterations')
from it42_autokey_keyword import words, keyed, A
AZ = A.AZ; CT = A.K4; KAI = A.KAI; KAL = A.KAL
CR = np.full(97, -1, dtype=np.int64)
for i, c in enumerate('EASTNORTHEAST'): CR[21 + i] = AZ.index(c)
for i, c in enumerate('BERLINCLOCK'): CR[63 + i] = AZ.index(c)
@njit(cache=True)
def prop(c, a, inv, L, form, kr, cr, p):
    n = 97
    for i in range(n): p[i] = cr[i]
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if p[i] < 0: continue
            j = i + L                                   # forward: P_j from key P_i
            if j < n:
                pp = p[i]; K = a[pp] if kr == 0 else (pp if kr == 1 else KAI[pp])
                ap = (a[c[j]] - K) % 26 if form == 0 else ((K - a[c[j]]) % 26 if form == 1 else (a[c[j]] + K) % 26)
                v = inv[ap]
                if p[j] < 0: p[j] = v; changed = True
                elif p[j] != v: return -1
            j = i - L                                   # backward: key at i gives P_{i-L}
            if j >= 0:
                K = (a[c[i]] - a[p[i]]) % 26 if form == 0 else ((a[c[i]] + a[p[i]]) % 26 if form == 1 else (a[p[i]] - a[c[i]]) % 26)
                v = inv[K] if kr == 0 else (K if kr == 1 else KAL[K])
                if p[j] < 0: p[j] = v; changed = True
                elif p[j] != v: return -1
    k = 0
    for i in range(n): k += p[i] >= 0
    return k
def run(ct, W, Ls):
    c = np.array([AZ.index(x) for x in ct], dtype=np.int64); p = np.zeros(97, dtype=np.int64); hits = []
    for w in W:
        K = keyed(w); a = np.array([K.index(x) for x in AZ], dtype=np.int64); inv = np.array([AZ.index(x) for x in K], dtype=np.int64)
        for L in Ls:
            for form in range(3):
                for kr in range(3):
                    k = prop(c, a, inv, L, form, kr, CR, p)
                    if k >= 0: hits.append((k, w, L, form, kr, ''.join(AZ[x] if x >= 0 else '.' for x in p)))
    return hits
if __name__ == '__main__':
    W = words(); rng = random.Random(45); Ls = range(14, 97)
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    ok = 0
    for t in range(6):
        w = rng.choice(W); L = rng.randint(14, 60); form = rng.randrange(3); kr = rng.randrange(3)
        K = keyed(w); a = [K.index(x) for x in AZ]; inv = [AZ.index(x) for x in K]
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        pi = [AZ.index(x) for x in P]; prim = [rng.randrange(26) for _ in range(L)]
        ci = []
        for i in range(97):
            pp = pi[i - L] if i >= L else prim[i]
            Kv = a[pp] if kr == 0 else (pp if kr == 1 else KAI[pp])
            v = (a[pi[i]] + Kv) % 26 if form == 0 else ((Kv - a[pi[i]]) % 26 if form == 1 else (a[pi[i]] - Kv) % 26)
            ci.append(inv[v])
        ct = ''.join(AZ[x] for x in ci)
        h = run(ct, [w] + rng.sample(W, 300), [L])
        f = any(x[1] == w and x[3] == form and x[4] == kr for x in h)
        ok += f; print(f'control {w} L={L} f={form} kr={kr}: found={f} total={len(h)}', flush=True)
    print(f'controls {ok}/6', flush=True)
    h = run(CT, W, Ls)
    from collections import Counter
    print(f'K4: {len(h)} conflict-free configs; by L: {sorted(Counter(x[2] for x in h).items())[:40]}')
    h.sort(reverse=True)
    for x in h[:12]: print(x)
