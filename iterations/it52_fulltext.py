#!/usr/bin/env python3
"""it52 stage 2: complete every akenum crib-consistent solution (<= 3 free alphabet letters) in all ways, decrypt the
FULL 97 letters (forward 34..96, backward 20..0, as it36 decrypt) and score quadgram mean over all 94 windows.
English 97-letter windows: mean -4.21, min -4.73 (it45 calibration). Usage: it52_fulltext.py QG files..."""
import sys, glob, itertools, numpy as np
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; KA = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
KAI = [KA.index(c) for c in AZ]; KAL = [AZ.index(c) for c in KA]
qg = np.fromfile(sys.argv[1], dtype=np.float32); CT = [AZ.index(c) for c in open('data/ciphertext.txt').read().strip()]
def dec(a, P0, L, form, kr):
    inv = [0] * 26
    for x in range(26): inv[a[x]] = x
    P = list(P0)
    for i in range(74, 97):
        q = P[i - L]; K = a[q] if kr == 0 else (q if kr == 1 else KAI[q]); ac = a[CT[i]]
        P[i] = inv[(ac - K) % 26 if form == 0 else ((K - ac) % 26 if form == 1 else (ac + K) % 26)]
    for j in range(20, -1, -1):
        i = j + L; ac, ap = a[CT[i]], a[P[i]]
        K = (ac - ap) % 26 if form == 0 else ((ac + ap) % 26 if form == 1 else (ap - ac) % 26)
        P[j] = inv[K] if kr == 0 else (K if kr == 1 else KAL[K])
    return P
def score(P): return np.mean([qg[((P[i] * 26 + P[i + 1]) * 26 + P[i + 2]) * 26 + P[i + 3]] for i in range(94)])
best = []
for f in sys.argv[2:]:
    tag = f.split('k4_')[1]; L, form, kr = int(tag.split('_')[0][1:]), int(tag.split('_f')[1][0]), int(tag.split('_k')[1][0])
    fb = (-99, '')
    for l in open(f):
        s = l.split()
        if len(s) != 2 or len(s[1]) != 97: continue
        a0 = list(map(int, s[0].split(",")))
        if len(a0) != 26: continue
        P0 = [AZ.index(c) if c != '.' else -1 for c in s[1]]
        free = [x for x in range(26) if a0[x] < 0]; vals = [v for v in range(26) if v not in a0]
        if any(P0[i] < 0 for i in range(21, 74)): continue
        for perm in itertools.permutations(vals):
            a = a0[:]
            for x, v in zip(free, perm): a[x] = v
            P = dec(a, P0, L, form, kr); sc = score(P)
            if sc > fb[0]: fb = (sc, ''.join(AZ[p] for p in P))
    best.append((fb[0], f, fb[1])); print(f'{f}: best full-text {fb[0]:.3f} {fb[1]}', flush=True)
print('overall best', max(best))
