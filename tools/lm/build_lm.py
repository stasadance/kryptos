#!/usr/bin/env python3
"""W4 scorer: char n-gram LMs (n=4,5,6) with interpolated absolute discounting (d=0.75), trained on the Gutenberg
corpus (~55M letters), held-out pg1342 + carter* for D measurement. Writes ngN.bin (float32 log10 P(x_n | x_1..x_{n-1}),
index = base-26 of the n letters). usage: build_lm.py OUTDIR"""
import re, sys, glob, os, math
import numpy as np
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
def clean(p):
    t = open(p, encoding='utf-8', errors='ignore').read()
    m = re.search(r"\*\*\* ?START OF.*?\*\*\*", t); n = re.search(r"\*\*\* ?END OF", t)
    t = t[m.end() if m else 0:n.start() if n else len(t)]
    return re.sub('[^A-Z]', '', t.upper())
HOLD = {'pg1342.txt'}
tr = [clean(p) for p in sorted(glob.glob('/tmp/claude-0/corpus/top/pg*.txt')) if os.path.basename(p) not in HOLD]
test = clean('/tmp/claude-0/corpus/pg1342.txt') + ''.join(clean(f'/tmp/claude-0/corpus/carter{i}.txt') for i in (1, 2, 3))
a = np.frombuffer(''.join(tr).encode(), dtype=np.uint8) - 65; print('train letters', len(a), 'test', len(test), flush=True)
b = np.frombuffer(test[:2000000].encode(), dtype=np.uint8) - 65
def codes(x, n):
    c = np.zeros(len(x) - n + 1, dtype=np.int64)
    for j in range(n): c = c * 26 + x[j:len(x) - n + 1 + j]
    return c
d = 0.75; P = np.bincount(a, minlength=26).astype(np.float64); P /= P.sum()   # order-1 (unigram)
for n in range(2, 7):
    c = np.bincount(codes(a, n), minlength=26 ** n).astype(np.float64).reshape(-1, 26)
    ctx = c.sum(1, keepdims=True); n1 = (c > 0).sum(1, keepdims=True)
    lower = np.tile(P.reshape(-1, 26), (26, 1)) if n > 2 else np.tile(P, (26, 1))   # P(x | last n-2 letters)
    with np.errstate(divide='ignore', invalid='ignore'):
        Pn = np.where(ctx > 0, np.maximum(c - d, 0) / ctx + d * n1 / ctx * lower, lower)
    P = Pn.reshape(-1); del c
    if n >= 4:
        L = np.log10(P).astype(np.float32); L.tofile(f'{out}/ng{n}.bin')
        h = -np.mean(np.log2(P[codes(b, n)])); print(f'n={n} held-out cross-entropy {h:.3f} bits/letter, redundancy D={math.log2(26)-h:.3f}', flush=True)
