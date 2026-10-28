#!/usr/bin/env python3
"""it88 calibration: plants (English PT with cribs, random A,B, random key) recovered by sa2? and K4 null under
random 'two'-feasible keys. usage: cal.py plant|null N R IT"""
import random, subprocess, sys, json, re
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, "/mnt/project-files/k4/tools"); import keygen as KG
QG = np.fromfile('/tmp/claude-0/it27/qg.bin', dtype=np.float32)
TXT = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/carter2.txt').read().upper())
CR = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}; NC = [i for i in range(97) if not (21 <= i <= 33 or 63 <= i <= 73)]
def qs(t): a = [ord(c) - 65 for c in t]; return float(sum(QG[((a[i]*26+a[i+1])*26+a[i+2])*26+a[i+3]] for i in range(94)))
def sa(ct, ks, R, IT, seed):
    out = subprocess.run(['./sa2', ct, ks, str(R), str(IT), str(seed)], capture_output=True, text=True).stdout.split('\n')
    if out[0].startswith('INF'): return None
    return max((float(l.split()[0]), l.split()[1]) for l in out if l.strip())
def plant(a):
    seed, R, IT = a; rng = random.Random(seed); o = rng.randrange(len(TXT) - 200); t = list(TXT[o:o+97])
    for s, w in CR.items(): t[s:s+len(w)] = w
    pt = ''.join(t); A = rng.sample(range(26), 26); B = rng.sample(range(26), 26); Bi = [0]*26
    for l, x in enumerate(B): Bi[x] = l
    k = [rng.randrange(26) for _ in range(97)]
    ct = ''.join(chr(65 + Bi[(A[ord(c)-65] + k[i]) % 26]) for i, c in enumerate(pt))
    b = sa(ct, ''.join(chr(65+x) for x in k), R, IT, seed)
    return dict(seed=seed, true=round(qs(pt), 1), best=b[0], acc=round(sum(b[1][i] == pt[i] for i in NC)/73, 2))
def null(a):
    seed, R, IT = a; rng = random.Random(seed)
    while True:
        k = [rng.randrange(26) for _ in range(97)]
        if KG.feasible(k, 'two'): break
    b = sa(KG.CT, ''.join(chr(65+x) for x in k), R, IT, seed)
    return dict(seed=seed, best=b[0], dec=b[1])
if __name__ == '__main__':
    m, n, R, IT = sys.argv[1], *map(int, sys.argv[2:5])
    with Pool(4) as P:
        for r in P.imap(plant if m == 'plant' else null, [(1000+s, R, IT) for s in range(n)]): print(json.dumps(r), flush=True)
