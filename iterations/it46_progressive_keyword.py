#!/usr/bin/env python3
"""it46: progressive periodic key (K1-K3-style tableau, key shifted by s each full period:
k_i = k[i mod p] + s*floor(i/p), and also + s*i 'running shift') under Quagmire I/II/III keyword alphabets
(49k vocabulary; Q1/Q2 with AZ or KA as the fixed one), Vig/Beau, p = 1..25, s = 1..25.  Exact crib test.
Control: plant."""
import sys, re, random
sys.argv[1:] = sys.argv[1:] or ["/tmp/claude-0/it27/qg.bin"]
import numpy as np
from numba import njit
sys.path.insert(0, 'iterations')
from it42_autokey_keyword import words, keyed, A
AZ = A.AZ; KA = A.KA; CT = A.K4
PAIRS = [(21 + i, c) for i, c in enumerate('EASTNORTHEAST')] + [(63 + i, c) for i, c in enumerate('BERLINCLOCK')]
POS = np.array([i for i, _ in PAIRS], dtype=np.int64)
def idx(K): return np.array([K.index(x) for x in AZ], dtype=np.int64)
@njit(cache=True)
def check(pa, ca, pl, cl, pos, res):
    n = 0
    for st in range(2):
        for mode in range(2):
            for p in range(1, 26):
                for s in range(1, 26):
                    key = np.full(p, -1, dtype=np.int64); ok = True
                    for t in range(pos.shape[0]):
                        i = pos[t]
                        v = (ca[cl[t]] - pa[pl[t]]) % 26 if st == 0 else (ca[cl[t]] + pa[pl[t]]) % 26
                        sh = s * (i // p) if mode == 0 else s * i
                        v = (v - sh) % 26 if st == 0 else (v - sh) % 26
                        r = i % p
                        if key[r] < 0: key[r] = v
                        elif key[r] != v: ok = False; break
                    if ok:
                        res[n, 0] = st; res[n, 1] = mode; res[n, 2] = p; res[n, 3] = s; n += 1
    return n
def run(ct, W):
    pl = np.array([AZ.index(c) for _, c in PAIRS], dtype=np.int64)
    cl = np.array([AZ.index(ct[i]) for i, _ in PAIRS], dtype=np.int64)
    res = np.zeros((2 * 2 * 25 * 25, 4), dtype=np.int64); hits = []
    azi, kai = idx(AZ), idx(KA)
    for w in W:
        k = idx(keyed(w))
        for model, (pa, ca) in (('Q1AZ', (k, azi)), ('Q1KA', (k, kai)), ('Q2AZ', (azi, k)), ('Q2KA', (kai, k)), ('Q3', (k, k))):
            n = check(pa, ca, pl, cl, POS, res)
            for r in res[:n]: hits.append((w, model, 'VB'[r[0]], ('perperiod', 'perletter')[r[1]], int(r[2]), int(r[3])))
    return hits
if __name__ == '__main__':
    W = words(); rng = random.Random(46)
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    ok = 0
    for t in range(6):
        w = rng.choice(W); K = keyed(w); model = rng.choice(['Q1KA', 'Q2AZ', 'Q3']); st = rng.choice('VB')
        mode = rng.randrange(2); p = rng.randint(3, 20); s = rng.randint(1, 25); key = [rng.randrange(26) for _ in range(p)]
        PA = K if model in ('Q1KA', 'Q3') else AZ; CA = K if model in ('Q2AZ', 'Q3') else KA
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        ct = []
        for i, x in enumerate(P):
            kv = (key[i % p] + (s * (i // p) if mode == 0 else s * i)) % 26
            ct.append(CA[(PA.index(x) + kv) % 26] if st == 'V' else CA[(kv - PA.index(x)) % 26])
        h = run(''.join(ct), [w] + rng.sample(W, 500))
        f = any(x[0] == w and x[1] == model and x[2] == st and x[4] == p and x[5] == s for x in h)
        ok += f; print(f'control {w} {model} {st} mode={mode} p={p} s={s}: found={f} total={len(h)}', flush=True)
    print(f'controls {ok}/6', flush=True)
    h = run(CT, W)
    from collections import Counter
    print(f'K4: {len(h)} consistent; by p: {sorted(Counter(x[4] for x in h).items())}')
    for x in h[:30]: print(x)
