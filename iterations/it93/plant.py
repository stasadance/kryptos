#!/usr/bin/env python3
"""it93 plants/runs. plant: English+cribs, random cube, Trifid(n,o) -> recover? k4: run K4 at (n,o).
usage: plant.py plant n o cnt R IT lam | plant.py k4 n o cnt R IT lam (cnt = independent seeds)"""
import random, re, subprocess, sys, json, os
import numpy as np
from multiprocessing import Pool
TXT = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/carter1.txt').read().upper())
CR = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}; NC = [i for i in range(97) if not (21 <= i <= 33 or 63 <= i <= 73)]
K4 = open('/mnt/project-files/k4/facts/ciphertext.txt').read().strip()
L = np.memmap('/tmp/claude-0/lm/ng6.bin', dtype=np.float32, mode='r')
def lm(t): a = [ord(c)-65 for c in t]; return float(sum(L[sum(a[i+j]*26**(5-j) for j in range(6))] for i in range(92)))
def blocks(n, o):
    b = []; s = 0
    if o: b.append((0, o)); s = o
    while s < 97: b.append((s, min(n, 97 - s))); s += n
    return b
def enc(pt, n, o, cube):   # cube: dict letter->code 0..26
    sym = {v: k for k, v in cube.items()}; out = []
    for s, Lb in blocks(n, o):
        tr = [[cube[pt[s+q]] // 9, (cube[pt[s+q]] // 3) % 3, cube[pt[s+q]] % 3] for q in range(Lb)]
        stream = [tr[q][r] for r in range(3) for q in range(Lb)]
        for q in range(Lb):
            c = sym[stream[3*q]*9 + stream[3*q+1]*3 + stream[3*q+2]]; out.append(c)
    return ''.join(out)
def job(a):
    mode, n, o, seed, R, IT, lam = a; g = random.Random(seed)
    if mode == 'plant':
        while True:
            off = g.randrange(len(TXT) - 200); t = list(TXT[off:off+97])
            for s, w in CR.items(): t[s:s+len(w)] = w
            pt = ''.join(t); syms = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ#'); g.shuffle(syms); cube = {c: i for i, c in enumerate(syms)}
            ct = enc(pt, n, o, cube)
            if '#' not in ct: break           # K4 never shows the 27th symbol
    else: ct, pt = K4, None
    out = subprocess.run(['./trifid', str(n), str(o), ct, str(R), str(IT), str(seed), str(lam)], capture_output=True, text=True).stdout.split()
    r = dict(mode=mode, n=n, o=o, seed=seed, best=float(out[0]), viol=int(out[1]), dec=out[2])
    if pt: r.update(true=round(lm(pt), 1), acc=round(sum(out[2][i] == pt[i] for i in NC)/len(NC), 2))
    return r
if __name__ == '__main__':
    mode = sys.argv[1]; n, o, cnt, R, IT = map(int, sys.argv[2:7]); lam = float(sys.argv[7])
    with Pool(4) as P:
        for r in P.imap(job, [(mode, n, o, 4000 + s, R, IT, lam) for s in range(cnt)]): print(json.dumps(r), flush=True)
