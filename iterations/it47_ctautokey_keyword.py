#!/usr/bin/env python3
"""it47: CT-autokey (K_i = C_{i-L}) under a keyword-mixed alphabet, L = 1..96, 9 models (key value a(c)/AZ/KA
x vig/beau/var), 49k vocabulary.  Exact: every crib position with i-L >= 0 must satisfy the relation; if all
pass, the whole text (i >= L) decrypts directly -> quadgram score.  Positions i < L use an unknown primer
(not scored).  Control: plant."""
import sys, re, random
sys.argv[1:] = sys.argv[1:] or ["/tmp/claude-0/it27/qg.bin"]
import numpy as np
from numba import njit
sys.path.insert(0, 'iterations')
from it42_autokey_keyword import words, keyed, A
AZ = A.AZ; CT = A.K4; KAI = A.KAI; qg = A.qg
CR = np.full(97, -1, dtype=np.int64)
for i, ch in enumerate('EASTNORTHEAST'): CR[21 + i] = AZ.index(ch)
for i, ch in enumerate('BERLINCLOCK'): CR[63 + i] = AZ.index(ch)
@njit(cache=True)
def test(c, a, inv, L, form, kr, cr, qg):
    p = np.full(97, -1, dtype=np.int64); nrel = 0
    for i in range(L, 97):
        cc = c[i - L]; K = a[cc] if kr == 0 else (cc if kr == 1 else KAI[cc])
        ap = (a[c[i]] - K) % 26 if form == 0 else ((K - a[c[i]]) % 26 if form == 1 else (a[c[i]] + K) % 26)
        p[i] = inv[ap]
        if cr[i] >= 0:
            nrel += 1
            if p[i] != cr[i]: return -1e9, nrel
    s = 0.0; n = 0
    for i in range(L, 94):
        s += qg[((p[i]*26+p[i+1])*26+p[i+2])*26+p[i+3]]; n += 1
    return (s / n if n > 0 else 0.0), nrel
def run(ct, W, Ls):
    c = np.array([AZ.index(x) for x in ct], dtype=np.int64); hits = []
    for w in W:
        K = keyed(w); a = np.array([K.index(x) for x in AZ], dtype=np.int64); inv = np.array([AZ.index(x) for x in K], dtype=np.int64)
        for L in Ls:
            for form in range(3):
                for kr in range(3):
                    s, nrel = test(c, a, inv, L, form, kr, CR, qg)
                    if s > -1e8: hits.append((s, nrel, w, L, form, kr))
    return hits
if __name__ == '__main__':
    W = words(); rng = random.Random(47)
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    ok = 0
    for t in range(6):
        w = rng.choice(W); L = rng.randint(1, 80); form = rng.randrange(3); kr = rng.randrange(3)
        K = keyed(w); a = [K.index(x) for x in AZ]; inv = [AZ.index(x) for x in K]
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        ci = []
        for i, x in enumerate(P):
            cc = ci[i - L] if i >= L else rng.randrange(26)
            Kv = a[cc] if kr == 0 else (cc if kr == 1 else KAI[cc])
            pv = a[AZ.index(x)]
            v = (pv + Kv) % 26 if form == 0 else ((Kv - pv) % 26 if form == 1 else (pv - Kv) % 26)
            ci.append(inv[v])
        h = run(''.join(AZ[x] for x in ci), [w] + rng.sample(W, 1000), [L])
        f = any(x[2] == w and x[4] == form and x[5] == kr for x in h)
        ok += f; print(f'control {w} L={L} f={form} kr={kr}: found={f} total={len(h)}', flush=True)
    print(f'controls {ok}/6', flush=True)
    h = run(CT, W, range(1, 97))
    from collections import Counter
    print(f'K4: {len(h)} crib-exact; by L: {sorted(Counter(x[3] for x in h).items())}')
    h.sort(reverse=True)
    for x in h[:10]: print(x)
