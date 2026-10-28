#!/usr/bin/env python3
"""it68: running key + transposition of the KEY: key stream = any permutation of a 97-letter window of a source
text (K1-K3 PT/CT, tableau, Carter, Morse, dedication, the Gutenberg corpus), one standard tableau
(AZ/KA x Vig/Beau/Var). Necessary: the letter counts of the window dominate the crib-derived key-letter counts.
This covers every transposition of the key at once. Uses sliding counts (numpy cumsum), forward only, since
reversal does not change counts. Control: a window of a random source, randomly permuted.
Usage: it68_transposed_runkey.py"""
import sys, glob, random, re
import numpy as np
sys.path.insert(0, 'iterations')
from it66_transposed_keyword import keyletters, enc, K4, AZ, KA
def norm(s): return re.sub('[^A-Z]', '', s.upper())
SRC = {f.split('/')[-1]: norm(open(f, errors='ignore').read()) for f in sorted(glob.glob('/tmp/claude-0/corpus/*.txt'))}
MODELS = [(xn, X, f) for xn, X in (('AZ', AZ), ('KA', KA)) for f in range(3)]
def windows_ok(txt, need):
    a = np.frombuffer(txt.encode(), dtype=np.uint8) - 65
    oh = np.zeros((len(a) + 1, 26), dtype=np.int32); oh[np.arange(1, len(a) + 1), a] = 1; cum = oh.cumsum(0)
    w = cum[97:] - cum[:-97]; nv = np.array([need.get(c, 0) for c in AZ])
    return np.nonzero((w >= nv).all(1))[0]
def run(ct, src):
    out = []
    for xn, X, f in MODELS:
        need = keyletters(ct, X, f)
        for name, txt in src.items():
            for o in windows_ok(txt, need): out.append((name, int(o), xn, f))
    return out
if __name__ == '__main__':
    print('sources', len(SRC), 'letters', sum(map(len, SRC.values())), flush=True)
    eng = SRC['pg1342.txt']; rng = random.Random(68); good = 0
    for t in range(10):
        name = rng.choice([k for k in SRC if len(SRC[k]) > 300]); txt = SRC[name]; o = rng.randrange(len(txt) - 97); xn, X, f = rng.choice(MODELS)
        ks = list(txt[o:o + 97]); rng.shuffle(ks)
        po = rng.randrange(len(eng) - 200); P = list(eng[po:po + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        h = run(enc(P, ks, X, f), {name: txt}); found = any(x[1] == o and x[2] == xn and x[3] == f for x in h); good += found
        print(f'control {name}@{o} {xn} f={f}: found={found} hits={len(h)}', flush=True)
    print(f'controls {good}/10', flush=True)
    h = run(K4, SRC); print('K4 hits', len(h))
    for x in h[:50]: print(' ', x, SRC[x[0]][x[1]:x[1] + 97])
