#!/usr/bin/env python3
"""it81c: English running key through a dictionary-KEYED tableau (Quagmire III style: X = keyed(word), the same
alphabet on PT/CT/key, as in K1/K2 with KRYPTOS). For each of 49k words x 3 forms, the key at the 24 crib
positions is known exactly; score its Englishness (mean quadgram of the 13- and 11-letter fragments).
Null: the same max over words for shuffled K4. Control: plant an English running key under a random keyed
alphabet; the true word must rank top. Usage: it81c_keyed_runkey.py"""
import sys, random, re
import numpy as np
sys.path.insert(0, 'iterations')
from it66_transposed_keyword import words
from it81_runkey_beam import AZ, K4, qg, enc
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
POS1 = list(range(21, 34)); POS2 = list(range(63, 74))
def keyed(w):
    s = []
    for ch in w + AZ:
        if ch not in s: s.append(ch)
    return ''.join(s)
W = sorted({keyed(w) for w in words() if 3 <= len(w) <= 30})   # distinct alphabets
def frag_scores(ct, Xs):
    """vectorised over alphabets: returns (n_alph, 3 forms) mean quadgram score of the crib key fragments."""
    A = np.array([[X.index(ch) for ch in AZ] for X in Xs])            # AZ letter -> X index
    Xarr = np.array([[ord(ch) - 65 for ch in X] for X in Xs])          # X index -> AZ letter
    out = np.zeros((len(Xs), 3))
    for f in range(3):
        tot = 0
        for pos in (POS1, POS2):
            ks = []
            for i in pos:
                c = A[:, AZ.index(ct[i])]; p = A[:, AZ.index(CRIB[i])]
                kv = (c - p) % 26 if f == 0 else ((c + p) % 26 if f == 1 else (p - c) % 26)
                ks.append(Xarr[np.arange(len(Xs)), kv])
            ks = np.array(ks)                                             # len(pos) x n
            q = ((ks[:-3] * 26 + ks[1:-2]) * 26 + ks[2:-1]) * 26 + ks[3:]
            tot = tot + qg[q].sum(0)
        out[:, f] = tot / (10 + 8)
    return out
if __name__ == '__main__':
    print('distinct keyed alphabets', len(W), flush=True)
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    e2 = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg84.txt', errors='ignore').read().upper())
    rng = random.Random(812)
    for t in range(5):
        X = rng.choice(W); f = rng.randrange(3)
        P = list(eng[(o := rng.randrange(len(eng) - 200)):o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        K = e2[(o2 := rng.randrange(len(e2) - 200)):o2 + 97]
        S = frag_scores(enc(P, K, X, f), W); rank = int((S[:, f] > S[W.index(X), f]).sum()) + int((S[:, [g for g in range(3) if g != f]] > S[W.index(X), f]).sum())
        print(f'control f={f}: true score {S[W.index(X), f]:.2f} rank {rank} best {S.max():.2f}', flush=True)
    S = frag_scores(K4, W); idx = np.dstack(np.unravel_index(np.argsort(-S.ravel())[:10], S.shape))[0]
    print(f'K4 best {S.max():.3f}')
    for a, f in idx: print(f'  {W[a]} f={f} {S[a, f]:.3f}')
    for t in range(5): print(f'null best {frag_scores("".join(rng.sample(K4, 97)), W).max():.3f}', flush=True)
