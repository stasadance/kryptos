#!/usr/bin/env python3
"""it93 sweep: K4 (or shuffled-K4 null) under Trifid for n=2..40 all offsets, n=41..97 offset 0. One SA run per config."""
import sys, json, random, subprocess
from multiprocessing import Pool
K4 = open('/mnt/project-files/k4/facts/ciphertext.txt').read().strip(); tag = sys.argv[1]
ct = K4
if tag.startswith('null'): l = list(K4); random.Random(int(tag[4:]) + 930).shuffle(l); ct = ''.join(l)
cfg = [(n, o) for n in range(2, 41) for o in range(n)] + [(n, 0) for n in range(41, 98)]
import os
out_f = sys.argv[2] if len(sys.argv) > 2 else None
done = set()
if out_f and os.path.exists(out_f):
    for l in open(out_f):
        try: r = json.loads(l); done.add((r['n'], r['o']))
        except Exception: pass
cfg = [c for c in cfg if c not in done]
def job(c):
    n, o = c; out = subprocess.run(['./trifid', str(n), str(o), ct, '8', '1500000', str(93 + n * 100 + o), '25'], capture_output=True, text=True).stdout.split()
    return dict(n=n, o=o, best=float(out[0]), viol=int(out[1]), dec=out[2])
with Pool(4) as P:
    fo = open(out_f, 'a') if out_f else sys.stdout
    for r in P.imap_unordered(job, cfg, chunksize=2): fo.write(json.dumps(r) + '\n'); fo.flush()
