#!/usr/bin/env python3
"""it81: running key from an UNKNOWN English source (no source text needed). Model: K4 = tableau(P, K) with BOTH
P and K English, under AZ/KA x Vig/Beau/Var. Beam search over positions; the state is (last 3 P letters, last
3 K letters); score = quadgram(P) + quadgram(K); cribs force P. This is the classical two-stream running-key
attack. Controls: planted English P (with cribs) + English K from another book; we measure recovered P letters
and the score. Nulls: shuffled K4. Usage: it81_runkey_beam.py [beam]"""
import sys, random, re
import numpy as np
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; KA = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
qg = np.fromfile('/tmp/claude-0/it27/qg.bin', dtype=np.float32)
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
def ktab(X, f):
    """T[c][p] = AZ index of key letter for CT letter c, PT letter p (both AZ indices)."""
    xi = [X.index(ch) for ch in AZ]; T = np.zeros((26, 26), dtype=np.int64)
    for c in range(26):
        for p in range(26):
            cv, pv = xi[c], xi[p]; kv = (cv - pv) % 26 if f == 0 else ((cv + pv) % 26 if f == 1 else (pv - cv) % 26)
            T[c, p] = AZ.index(X[kv])
    return T
def beam(ct, X, f, B, crib=True):
    T = ktab(X, f); c = [AZ.index(ch) for ch in ct]; n = len(c)
    p3 = np.zeros(1, np.int64); k3 = np.zeros(1, np.int64); sc = np.zeros(1, np.float32)
    hist = []   # per step: (parent index, p, k)
    for i in range(n):
        ps = np.array([AZ.index(CRIB[i])]) if (crib and i in CRIB) else np.arange(26)
        par = np.repeat(np.arange(len(p3)), len(ps)); pp = np.tile(ps, len(p3)); kk = T[c[i], pp]
        q_p = p3[par] * 26 + pp; q_k = k3[par] * 26 + kk
        s = sc[par] + ((qg[q_p] + qg[q_k]) if i >= 3 else 0)
        np3 = q_p % 17576; nk3 = q_k % 17576
        key = np3 * 17576 + nk3; order = np.argsort(-s, kind='stable'); key_o = key[order]
        _, first = np.unique(key_o, return_index=True); keep = order[first]
        keep = keep[np.argsort(-s[keep])][:B]
        hist.append((par[keep], pp[keep], kk[keep])); p3, k3, sc = np3[keep], nk3[keep], s[keep]
    j = 0; P = []; K = []
    for par, pp, kk in reversed(hist): P.append(AZ[pp[j]]); K.append(AZ[kk[j]]); j = par[j]
    return float(sc[0]) / (2 * (n - 3)), ''.join(reversed(P)), ''.join(reversed(K))
def enc(P, K, X, f):
    out = ''
    for p, k in zip(P, K):
        pv, kv = X.index(p), X.index(k); out += X[(pv + kv) % 26 if f == 0 else ((kv - pv) % 26 if f == 1 else (pv - kv) % 26)]
    return out
if __name__ == '__main__':
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    norm = lambda s: re.sub('[^A-Z]', '', s.upper())
    e1 = norm(open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read()); e2 = norm(open('/tmp/claude-0/corpus/pg84.txt', errors='ignore').read())
    rng = random.Random(81); M = [(xn, X, f) for xn, X in (('AZ', AZ), ('KA', KA)) for f in range(3)]
    for t in range(4):
        xn, X, f = M[t % 6]
        P = list(e1[(o := rng.randrange(len(e1) - 200)):o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'; P = ''.join(P)
        K = e2[(o2 := rng.randrange(len(e2) - 200)):o2 + 97]
        s, Pg, Kg = beam(enc(P, K, X, f), X, f, B); acc = sum(a == b for a, b in zip(P, Pg)) / 97
        print(f'control {xn} f={f}: score {s:.3f} P-acc {acc:.2f} | {Pg}', flush=True)
    for xn, X, f in M:
        s, Pg, Kg = beam(K4, X, f, B); print(f'K4 {xn} f={f}: score {s:.3f}\n  P {Pg}\n  K {Kg}', flush=True)
    for t in range(3):
        n = ''.join(rng.sample(K4, 97)); s, Pg, Kg = beam(n, AZ, 0, B); print(f'null AZ vig: score {s:.3f}', flush=True)
