#!/usr/bin/env python3
"""it75: K4 = US Army M-94 (Jefferson-type) cylinder with its 25 published disks (data/sources/m94_disks.txt,
prc68.com and jproc.ca agree). The PT is set in lines of 25 on one row, and the CT is read g rows away (g = 1..25,
fixed per line). The disk order is a permutation of the 25 disks. Line start offset o = 0..24 (K4 may sit
anywhere in the message). Exact: for each (o, g per crib line), check that a disk assignment exists (bipartite
matching) for the constrained columns. Null: shuffled K4. Control: planted M-94 encryption.
Usage: it75_m94.py"""
import random, re, itertools
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
D = open('data/sources/m94_disks.txt').read().split()
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
SHIFT = [[{} for _ in range(26)] for _ in D]   # SHIFT[d][g][p] = c
for d, al in enumerate(D):
    for g in range(26):
        for k, p in enumerate(al): SHIFT[d][g][p] = al[(k + g) % 26]
def match(adj):
    m = {}
    def aug(j, seen):
        for d in adj[j]:
            if d in seen: continue
            seen.add(d)
            if d not in m or aug(m[d], seen): m[d] = j; return True
        return False
    return all(aug(j, set()) for j in adj)
def feasible(ct, o):
    lines = sorted({(i + o) // 25 for i in CRIB}); hits = []
    for gs in itertools.product(range(1, 26), repeat=len(lines)):
        g = dict(zip(lines, gs)); adj = {}
        for i, p in CRIB.items():
            j = (i + o) % 25; gl = g[(i + o) // 25]
            ok = {d for d in range(25) if SHIFT[d][gl][p] == ct[i]}
            adj[j] = adj[j] & ok if j in adj else ok
        if all(adj.values()) and match(adj): hits.append(gs)
    return hits
def plant(rng, eng):
    order = rng.sample(range(25), 25); o = rng.randrange(25)
    P = list(eng[(po := rng.randrange(len(eng) - 200)):po + 97])
    for i, ch in CRIB.items(): P[i] = ch
    gl = {}; out = ''
    for i, p in enumerate(P):
        ln = (i + o) // 25; gl.setdefault(ln, rng.randrange(1, 26)); out += SHIFT[order[(i + o) % 25]][gl[ln]][p]
    return out, o
if __name__ == '__main__':
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    rng = random.Random(75); good = 0
    for t in range(4):
        ct, o = plant(rng, eng); h = feasible(ct, o); good += bool(h); print(f'control o={o}: hits {len(h)}', flush=True)
    print(f'controls {good}/4', flush=True)
    tot = 0
    for o in range(25):
        h = feasible(K4, o); tot += len(h); print(f'K4 o={o}: hits {len(h)} {h[:5]}', flush=True)
    print('K4 total', tot, flush=True)
    for t in range(3):
        n = ''.join(rng.sample(K4, 97)); print('null total', sum(len(feasible(n, o)) for o in range(25)), flush=True)
