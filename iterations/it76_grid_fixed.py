#!/usr/bin/env python3
"""it76: grid key k_i = r(row) + c(col) mod 26 (row = (i+o)//w, col = (i+o)%w) under FIXED standard tableaux
(AZ/KA x Vig/Beau/Var), all widths w = 2..96 and offsets o. This is the cylinder model whose disks are tableau
rows (a 'Kryptos cylinder'), with a generatrix per line. The crib key values are known, so consistency is a
union-find over row and column nodes with additive offsets (exact). The cylinder variant also requires distinct
c across columns (each disk used once). Null: shuffled K4. Control: planted grid-key encryption.
Usage: it76_grid_fixed.py"""
import random, re
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; KA = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
def kval(ct, X, f, i, p):
    c, q = X.index(ct[i]), X.index(p)
    return (c - q) % 26 if f == 0 else ((c + q) % 26 if f == 1 else (q - c) % 26)
def consistent(ct, X, f, w, o, distinct=False):
    par = {}; off = {}
    def find(x):
        if par.setdefault(x, x) == x: off.setdefault(x, 0); return x, 0
        r, d = find(par[x]); par[x] = r; off[x] = (off[x] + d) % 26; return r, off[x]
    for i, p in CRIB.items():   # value(row) + value(col) = k  ->  col = k - row: edge row--col with "sum" relation
        a, b, k = ('r', (i + o) // w), ('c', (i + o) % w), kval(ct, X, f, i, p)
        # represent col value as -row value + k: use signed potentials, x_col = k - x_row
        ra, da = find(a); rb, db = find(b)
        # potentials: node value = sign * root + d; track sign by parity via separate structure
    return None
# simpler exact approach: fix r(row of first crib)=0 gauge per component, BFS over bipartite graph with x_c = k - x_r
def check(ct, X, f, w, o, distinct):
    edges = {}
    for i, p in CRIB.items():
        edges.setdefault(('r', (i + o) // w), []).append((('c', (i + o) % w), kval(ct, X, f, i, p)))
        edges.setdefault(('c', (i + o) % w), []).append((('r', (i + o) // w), kval(ct, X, f, i, p)))
    val = {}; comps = []
    for s in edges:
        if s in val: continue
        val[s] = 0; st = [s]; comp = [s]
        while st:
            u = st.pop()
            for v, k in edges[u]:
                x = (k - val[u]) % 26
                if v in val:
                    if val[v] != x: return False
                else: val[v] = x; st.append(v); comp.append(v)
        comps.append(comp)
    if not distinct: return True
    # distinct column values: within a component fixed up to the gauge t (cols shift +t... cols get -t): need distinct within comp;
    for comp in comps:
        cs = [val[v] for v in comp if v[0] == 'c']
        if len(cs) != len(set(cs)): return False
    return True   # across components a free gauge can always separate (26 values, few comps)
def run(ct, distinct):
    out = []
    for xn, X in (('AZ', AZ), ('KA', KA)):
        for f in range(3):
            for w in range(2, 97):
                for o in range(w):
                    if check(ct, X, f, w, o, distinct): out.append((xn, f, w, o))
    return out
if __name__ == '__main__':
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    rng = random.Random(76); good = 0
    for t in range(6):
        X = rng.choice((AZ, KA)); f = rng.randrange(3); w = rng.randrange(5, 30); o = rng.randrange(w)
        c = rng.sample(range(26), w) if w <= 26 else [rng.randrange(26) for _ in range(w)]; r = [rng.randrange(26) for _ in range(30)]
        P = list(eng[(po := rng.randrange(len(eng) - 200)):po + 97])
        for i, ch in CRIB.items(): P[i] = ch
        ct = ''
        for i, p in enumerate(P):
            k = (r[(i + o) // w] + c[(i + o) % w]) % 26; q = X.index(p)
            ct += X[(q + k) % 26 if f == 0 else ((k - q) % 26 if f == 1 else (q - k) % 26)]
        h = run(ct, False); found = (('AZ' if X == AZ else 'KA'), f, w, o) in h; good += found
        print(f'control w={w} o={o}: found={found} total hits={len(h)}', flush=True)
    print(f'controls {good}/6')
    for distinct in (False, True):
        h = run(K4, distinct); ws = sorted({x[2] for x in h})
        print(f'K4 distinct={distinct}: {len(h)} (alph,form,w,o) hits; widths {ws}')
        nh = [len(run(''.join(rng.sample(K4, 97)), distinct)) for _ in range(5)]
        print(f'   nulls hits {nh}')
        if distinct: print('   small-w hits:', [x for x in h if x[2] <= 30][:40])
