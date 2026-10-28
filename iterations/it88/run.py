#!/usr/bin/env python3
"""it88: crib-exact class-C SA on every Q4-two crib-feasible stream of a library. usage: run.py keygen|route [--ct CT] OUT"""
import sys, json, subprocess
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, "/mnt/project-files/k4/tools"); sys.path.insert(0, "/home/user/kryptos/iterations")
import keygen as KG, it35_keygen_route_err as R
from it87_q12_arbitrary import latin
src = sys.argv[1]; out = sys.argv[-1]; CT = sys.argv[sys.argv.index('--ct')+1] if '--ct' in sys.argv else KG.CT
pairs = KG.crib_pairs(CT); kidx = [i-1 for i, _, _ in pairs]
def cands():
    for m, k in (R.keygen_streams() if src == 'keygen' else R.route_streams()):
        k = [int(x) % 26 for x in (list(k) + [0]*100)[:97]]
        if not latin(np.array([[k[j] for j in kidx]]), pairs)[0]: continue
        if KG.feasible(k, 'two', CT, pairs): yield m, ''.join(chr(65+x) for x in k)
def job(a):
    m, ks = a; o = subprocess.run(['./sa2', CT, ks, '8', '2000000', '88'], capture_output=True, text=True).stdout.split('\n')
    if o[0].startswith('INF'): return dict(meta=m, best=None)
    b = max((float(l.split()[0]), l.split()[1]) for l in o if l.strip()); return dict(meta=m, key=ks, best=b[0], dec=b[1])
with Pool(4) as P, open(out, 'w') as f:
    for r in P.imap_unordered(job, cands(), chunksize=4): f.write(json.dumps(r) + '\n'); f.flush()
