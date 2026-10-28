#!/usr/bin/env python3
"""it66 (H-1502): key stream = keyword repeated, then permuted by ANY transposition (K3-style square, any width,
any route); one standard tableau (AZ/KA x Vig/Beau/Var). Whatever the transposition, the key stream is a
permutation of the periodic stream, so (1) every crib-derived key letter must be a letter of the keyword and
(2) each letter can occur at most mult(letter)*ceil(97/L) times. This covers every transposition at once.
Keywords: it42 dictionary (corpus words, K1-K3 word pairs, Kryptos names). Control: planted key stream = random
dictionary keyword repeated then randomly permuted, encrypted English; the true keyword must pass.
Usage: it66_transposed_keyword.py"""
import sys, random, re, math
from collections import Counter
sys.path.insert(0, 'iterations')
import glob
def words():                                    # same keyword set as it42_autokey_keyword.words()
    W = set()
    for f in glob.glob('/tmp/claude-0/corpus/*.txt'):
        W |= set(re.findall(r'[A-Z]{3,}', open(f, errors='ignore').read().upper()))
    pt = re.findall(r'[A-Z]+', open('/tmp/claude-0/corpus/kryptos_pt.txt').read().upper())
    W |= {pt[i] + pt[i + 1] for i in range(len(pt) - 1)}
    W |= {'KRYPTOS', 'PALIMPSEST', 'ABSCISSA', 'BERLINCLOCK', 'SANBORN', 'SCHEIDT', 'WEBSTER', 'LANGLEY',
          'URANIA', 'WELTZEITUHR', 'ALEXANDERPLATZ', 'BERLIN', 'CLOCK', 'SHADOW', 'ILLUSION', 'IQLUSION',
          'LUCID', 'MEMORY', 'DESPARATLY', 'UNDERGRUUND', 'EASTNORTHEAST', 'NORTHEAST', 'CARTER', 'EGYPT'}
    return sorted(W)
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; KA = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')} | {63 + i: c for i, c in enumerate('BERLINCLOCK')}
def keyletters(ct, X, f):
    out = []
    for i, p in CRIB.items():
        c, q = X.index(ct[i]), X.index(p)
        out.append(X[(c - q) % 26 if f == 0 else ((c + q) % 26 if f == 1 else (q - c) % 26)])
    return Counter(out)
def ok(need, w):
    m = Counter(w); cap = math.ceil(97 / len(w))
    return all(m[ch] * cap >= n for ch, n in need.items())
def run(ct, W):
    return [(w, xn, f) for xn, X in (('AZ', AZ), ('KA', KA)) for f in range(3)
            for need in [keyletters(ct, X, f)] for w in W if ok(need, w)]
def enc(P, key, X, f):
    out = ''
    for p, k in zip(P, key):
        q, kv = X.index(p), X.index(k)
        out += X[(q + kv) % 26 if f == 0 else ((kv - q) % 26 if f == 1 else (q - kv) % 26)]
    return out
if __name__ == '__main__':
    W = words(); print('keywords', len(W), flush=True)
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    rng = random.Random(66); good = 0
    for t in range(12):
        w = rng.choice([x for x in W if 5 <= len(x) <= 12]); X = rng.choice((AZ, KA)); f = rng.randrange(3)
        ks = list((w * 20)[:97]); rng.shuffle(ks)
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        hits = run(enc(P, ks, X, f), W); found = any(h[0] == w for h in hits); good += found
        print(f'control {w} L={len(w)} {"AZ" if X == AZ else "KA"} f={f}: found={found} hits={len(hits)}', flush=True)
    print(f'controls {good}/12')
    for xn, X in (('AZ', AZ), ('KA', KA)):
        for f in range(3):
            need = keyletters(K4, X, f)
            print(xn, f, 'key letters needed:', ''.join(sorted(need.elements())), 'distinct', len(need))
    hits = run(K4, W); short = [h for h in hits if len(h[0]) <= 30]
    print('K4 hits', len(hits), '| keyword length <= 30:', len(short), short[:40])
    print('longer hits are corpus run-ons (>=100 letters, nearly pangrams):', sorted({len(h[0]) for h in hits}))
