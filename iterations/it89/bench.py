#!/usr/bin/env python3
"""it89 K5-readiness benchmark, class D (key reused for K5). Plants: PT4 English with K4 cribs, PT5 different English
with BERLINCLOCK at 63-73, random key per position, alphabets per NA. Measures P4 accuracy (non-crib).
usage: bench.py NA n R IT lam"""
import random, re, subprocess, sys, json
from multiprocessing import Pool
TXT = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/carter3.txt').read().upper())
NC = [i for i in range(97) if not (21 <= i <= 33 or 63 <= i <= 73)]
def job(a):
    NA, seed, R, IT, lam = a; g = random.Random(seed)
    def txt():
        o = g.randrange(len(TXT) - 200); return list(TXT[o:o+97])
    p4 = txt(); p4[21:34] = 'EASTNORTHEAST'; p4[63:74] = 'BERLINCLOCK'; p5 = txt(); p5[63:74] = 'BERLINCLOCK'
    A = list(range(26)); B = list(range(26))
    if NA >= 1: g.shuffle(A)
    B = A[:] if NA == 1 else (g.sample(range(26), 26) if NA == 2 else B)
    Bi = [0]*26
    for l, x in enumerate(B): Bi[x] = l
    k = [g.randrange(26) for _ in range(97)]
    enc = lambda p: ''.join(chr(65 + Bi[(A[ord(c)-65] + k[i]) % 26]) for i, c in enumerate(p))
    c4, c5 = enc(p4), enc(p5)
    o = subprocess.run(['./depth', str(NA), c4, c5, str(R), str(IT), str(seed), str(lam)], capture_output=True, text=True).stdout.split('\n')
    res = [l.split() for l in o if l.strip()]; b = max(res, key=lambda r: float(r[0]))
    acc4 = sum(b[2][i] == p4[i] for i in NC) / len(NC); acc5 = sum(b[3][i] == p5[i] for i in range(97) if not 63 <= i <= 73) / 86
    import numpy as np
    Q=np.fromfile('/tmp/claude-0/it27/qg.bin',dtype=np.float32); qs=lambda t: float(sum(Q[((ord(t[i])-65)*17576+(ord(t[i+1])-65)*676+(ord(t[i+2])-65)*26+ord(t[i+3])-65)] for i in range(94)))
    return dict(true=round(qs(''.join(p4))+qs(''.join(p5)),1), NA=NA, seed=seed, best=float(b[0]), viol=int(b[1]), acc4=round(acc4, 2), acc5=round(acc5, 2))
if __name__ == '__main__':
    NA, n, R, IT = map(int, sys.argv[1:5]); lam = float(sys.argv[5])
    with Pool(4) as P:
        for r in P.imap(job, [(NA, 2000+s, R, IT, lam) for s in range(n)]): print(json.dumps(r), flush=True)
