#!/usr/bin/env python3
"""it91 plants: English (held-out carter text) with K4 cribs, random A,B (NA=2) or A=B (NA=1), random period-p shifts.
usage: plant.py NA p n NREP SW MV lam -> jsonl with true score, found score, accuracy"""
import random, re, subprocess, sys, json, os
import numpy as np
from multiprocessing import Pool
TXT = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/carter2.txt').read().upper())
CR = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}; NC = [i for i in range(97) if not (21 <= i <= 33 or 63 <= i <= 73)]
L = np.memmap(os.environ.get('LM', '/tmp/claude-0/lm/ng6.bin'), dtype=np.float32, mode='r'); O = int(os.environ.get('ORD', '6'))
def lm(t):
    a = [ord(c) - 65 for c in t]; return float(sum(L[sum(a[i+j] * 26 ** (O-1-j) for j in range(O))] for i in range(97 - O + 1)))
def job(a):
    NA, p, seed, R, SW, MV, lam = a; g = random.Random(seed); o = g.randrange(len(TXT) - 200); t = list(TXT[o:o+97])
    for s, w in CR.items(): t[s:s+len(w)] = w
    pt = ''.join(t); A = g.sample(range(26), 26); B = A[:] if NA == 1 else g.sample(range(26), 26); Bi = [0]*26
    for l, x in enumerate(B): Bi[x] = l
    sh = [g.randrange(26) for _ in range(p)]
    ct = ''.join(chr(65 + Bi[(A[ord(c)-65] + sh[i % p]) % 26]) for i, c in enumerate(pt))
    out = subprocess.run(['./pt', str(NA), str(p), ct, str(R), str(SW), str(MV), str(seed), str(lam)], capture_output=True, text=True).stdout.split()
    acc = sum(out[2][i] == pt[i] for i in NC) / len(NC)
    return dict(NA=NA, p=p, seed=seed, true=round(lm(pt), 1), best=float(out[0]), viol=int(out[1]), acc=round(acc, 2))
if __name__ == '__main__':
    NA, p, n, R, SW, MV = map(int, sys.argv[1:7]); lam = float(sys.argv[7])
    with Pool(4) as P:
        for r in P.imap(job, [(NA, p, 3000 + s, R, SW, MV, lam) for s in range(n)]): print(json.dumps(r), flush=True)
