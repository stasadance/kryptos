#!/usr/bin/env python3
"""it94 (coach S4a): which key models reproduce K4's positional anomalies?
Stats (Bean): D7 = max number of doublets (C_i = C_{i+1}) starting in one column at width 7 (K4: 5 of 6);
V21 = width-21 vertical bigram repeats = sum over repeated (C_i, C_{i+21}) bigrams of (count - 1) (K4: 11).
Models on English 97-letter plaintext (held-out text with K4 cribs at their places), alphabets random:
 shuffled-K4 (null), OTP, periodic-7 Q4, grid-7 r+c Q4, grid-21 r+c, Gromark base 2 (5-digit primer, mixed alphabet),
 PT-autokey L=7 and CT-autokey L=7 (one mixed alphabet), periodic-21 Q4.
Report P(D7 >= 5), P(V21 >= 11), and the ratio to shuffled-K4."""
import re, sys
import numpy as np
rng = np.random.default_rng(94)
K4 = open('/mnt/project-files/k4/facts/ciphertext.txt').read().strip(); k4 = (np.frombuffer(K4.encode(), dtype=np.uint8) - 65).astype(np.int64)
TXT = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/carter1.txt').read().upper() + open('/tmp/claude-0/corpus/carter2.txt').read().upper())
T = np.frombuffer(TXT.encode(), dtype=np.uint8).astype(np.int64) - 65
CR = {21: 'EASTNORTHEAST', 63: 'BERLINCLOCK'}
def D7(C):   # C: (m,97)
    d = (C[:, :-1] == C[:, 1:]); cols = np.arange(96) % 7
    return np.stack([d[:, cols == j].sum(1) for j in range(7)], 1).max(1)
def V21(C):
    b = C[:, :-21] * 26 + C[:, 21:]; out = np.zeros(len(C), dtype=np.int64)
    for i in range(len(C)):
        cnt = np.bincount(b[i], minlength=676); out[i] = (cnt[cnt > 1] - 1).sum()
    return out
def plaintexts(m):
    o = rng.integers(0, len(T) - 100, m); P = T[o[:, None] + np.arange(97)[None]]
    for s, w in CR.items(): P[:, s:s + len(w)] = np.frombuffer(w.encode(), dtype=np.uint8) - 65
    return P
def perms(m): return np.argsort(rng.random((m, 26)), 1)
def inv(A): I = np.empty_like(A); np.put_along_axis(I, A, np.arange(26)[None].repeat(len(A), 0), 1); return I
def q4(P, K, same=False):   # C = B^-1(A(P) + K)
    m = len(P); A = perms(m); B = A if same else perms(m); Bi = inv(B)
    v = (np.take_along_axis(A, P, 1) + K) % 26; return np.take_along_axis(Bi, v, 1)
def model(name, m):
    P = plaintexts(m); i = np.arange(97)
    if name == 'shuffled-K4': return np.array([rng.permutation(k4) for _ in range(m)])
    if name == 'OTP': return q4(P, rng.integers(0, 26, (m, 97)))
    if name.startswith('periodic-'):
        p = int(name.split('-')[1]); return q4(P, rng.integers(0, 26, (m, p))[:, i % p])
    if name.startswith('grid-'):
        w = int(name.split('-')[1]); r = rng.integers(0, 26, (m, 97 // w + 1)); c = rng.integers(0, 26, (m, w))
        return q4(P, r[:, i // w] + c[:, i % w])
    if name == 'gromark2':
        K = np.zeros((m, 97), dtype=np.int64); K[:, :5] = rng.integers(0, 2, (m, 5))
        for t in range(5, 97): K[:, t] = (K[:, t - 5] + K[:, t - 4]) % 2
        return q4(P, K, same=True)
    if name == 'gromark10':
        K = np.zeros((m, 97), dtype=np.int64); K[:, :5] = rng.integers(0, 10, (m, 5))
        for t in range(5, 97): K[:, t] = (K[:, t - 5] + K[:, t - 4]) % 10
        return q4(P, K, same=True)
    if name in ('ptauto7', 'ctauto7'):
        A = perms(m); Ai = inv(A); C = np.zeros((m, 97), dtype=np.int64); key = rng.integers(0, 26, (m, 7))
        Pa = np.take_along_axis(A, P, 1)
        for t in range(97):
            k = key[:, t] if t < 7 else (Pa[:, t - 7] if name == 'ptauto7' else np.take_along_axis(A, C[:, t - 7:t - 6], 1)[:, 0])
            C[:, t] = Ai[np.arange(m), (Pa[:, t] + k) % 26]
        return C
    raise ValueError(name)
if __name__ == '__main__':
    print('K4: D7 =', D7(k4[None])[0], ' V21 =', V21(k4[None])[0])
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 50000; base = None
    for name in ['shuffled-K4', 'OTP', 'periodic-7', 'grid-7', 'grid-14', 'grid-21', 'periodic-21', 'gromark2', 'gromark10', 'ptauto7', 'ctauto7']:
        C = model(name, m); d, v = D7(C), V21(C)
        pd, pv, pb = (d >= 5).mean(), (v >= 11).mean(), ((d >= 5) & (v >= 11)).mean()
        if base is None: base = (pd, pv)
        print(f'{name:12s} P(D7>=5)={pd:.2e} (x{pd/base[0] if base[0] else float("nan"):.1f})  P(V21>=11)={pv:.2e} (x{pv/base[1] if base[1] else float("nan"):.1f})  both={pb:.1e}  meanD7={d.mean():.2f} meanV21={v.mean():.2f}', flush=True)
