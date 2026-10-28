#!/usr/bin/env python3
"""it67: H-1502 with KEYED tableaux. Same as it66, but the tableau alphabet X = keyed(Y) for every dictionary
word Y (Quagmire III style, the same alphabet for PT/CT/key). The key stream = keyword W repeated and then
put through ANY transposition. Necessary condition: every crib-derived key letter is in W, with enough
multiplicity. Checks all Y x W pairs (49k x 49k x 3 forms) with bitmasks.
Control: random Y, W, form; the key stream is permuted at random.
Usage: it67_transposed_keyword_keyed.py"""
import sys, random, re, math
import numpy as np
from collections import Counter
sys.path.insert(0, 'iterations')
from it66_transposed_keyword import words, keyletters, enc, K4, AZ
def keyed(w):
    s = []
    for ch in w + AZ:
        if ch not in s: s.append(ch)
    return ''.join(s)
W = [w for w in words() if 3 <= len(w) <= 30]
MASK = np.array([sum(1 << (ord(c) - 65) for c in set(w)) for w in W], dtype=np.int64)
CNT = [Counter(w) for w in W]
def run(ct, Ys):
    hits = []
    for y in Ys:
        X = keyed(y)
        for f in range(3):
            need = keyletters(ct, X, f); nm = sum(1 << (ord(c) - 65) for c in need)
            for j in np.nonzero((MASK & nm) == nm)[0]:
                w = W[j]; cap = math.ceil(97 / len(w))
                if all(CNT[j][c] * cap >= n for c, n in need.items()): hits.append((y, w, f))
    return hits
if __name__ == '__main__':
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    rng = random.Random(67); good = 0; print('words', len(W), flush=True)
    for t in range(10):
        y = rng.choice(W); w = rng.choice([x for x in W if 5 <= len(x) <= 12]); f = rng.randrange(3); X = keyed(y)
        ks = list((w * 20)[:97]); rng.shuffle(ks)
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        h = run(enc(P, ks, X, f), [y]); found = any(a[1] == w and a[2] == f for a in h); good += found
        print(f'control Y={y} W={w} f={f}: found={found} hits(this Y)={len(h)}', flush=True)
    print(f'controls {good}/10', flush=True)
    hits = run(K4, W)
    print('K4 hits', len(hits)); dist = Counter(len(h[1]) for h in hits); print('by keyword length', sorted(dist.items()))
    for h in sorted(hits, key=lambda h: len(h[1]))[:80]: print(' ', h)
