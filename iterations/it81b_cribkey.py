#!/usr/bin/env python3
"""it81b: under a fixed tableau, the running key at the crib positions is known exactly. If the key is English
text, those 13- and 11-letter fragments must look English. We score each fragment by mean quadgram and compare
with the distribution over 200k English fragments of the same length (2 books). Usage: it81b_cribkey.py"""
import re, random
import numpy as np
import sys; sys.path.insert(0, 'iterations')
from it81_runkey_beam import ktab, AZ, KA, K4, qg
def sc(s): return np.mean([qg[((AZ.index(s[i]) * 26 + AZ.index(s[i + 1])) * 26 + AZ.index(s[i + 2])) * 26 + AZ.index(s[i + 3])] for i in range(len(s) - 3)])
norm = lambda s: re.sub('[^A-Z]', '', s.upper())
eng = norm(open('/tmp/claude-0/corpus/pg84.txt', errors='ignore').read()) + norm(open('/tmp/claude-0/corpus/pg2600.txt', errors='ignore').read())
rng = random.Random(811)
d13 = np.array([sc(eng[(o := rng.randrange(len(eng) - 20)):o + 13]) for _ in range(100000)])
d11 = np.array([sc(eng[(o := rng.randrange(len(eng) - 20)):o + 11]) for _ in range(100000)])
for xn, X in (('AZ', AZ), ('KA', KA)):
    for f in range(3):
        T = ktab(X, f)
        k1 = ''.join(AZ[T[AZ.index(K4[21 + i]), AZ.index(p)]] for i, p in enumerate('EASTNORTHEAST'))
        k2 = ''.join(AZ[T[AZ.index(K4[63 + i]), AZ.index(p)]] for i, p in enumerate('BERLINCLOCK'))
        s1, s2 = sc(k1), sc(k2); p1 = (d13 <= s1).mean(); p2 = (d11 <= s2).mean()
        print(f'{xn} f={f}: {k1} {s1:.2f} P={p1:.5f} | {k2} {s2:.2f} P={p2:.5f} | joint P~{p1*p2:.2e}')
