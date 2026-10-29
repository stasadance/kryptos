#!/usr/bin/env python3
"""it90f: Hill n=5 affine, exact-ish search. Decrypted letter at position i comes from row (i-o) mod 5, so a BIGRAM
score is a cycle of pairwise potentials over the 5 row choices. Enumerate the two largest rows (a,b) fully; the
other three are maximised by max-plus DP along both cycle paths; every (xa,xb) pair with its best completion is then
rescored with the 5-gram LM (invertible D only). Controls: plants (true key is among the row solutions, verified).
Null: shuffled-K4. usage: it90f_n5aff_dp.py"""
import sys, random, re, glob, os
import numpy as np
sys.path.insert(0, 'iterations'); import it90_hill4_affine as H
LM5 = np.memmap('/tmp/claude-0/lm/ng5.bin', dtype=np.float32, mode='r')
BG = '/tmp/claude-0/lm/bigram.npy'
if not os.path.exists(BG):
    t = ''.join(re.sub('[^A-Z]', '', open(p, errors='ignore').read().upper()) for p in sorted(glob.glob('/tmp/claude-0/corpus/top/pg*.txt'))[:40])
    a = np.frombuffer(t.encode(), dtype=np.uint8) - 65; c = np.bincount(a[:-1].astype(int) * 26 + a[1:], minlength=676).reshape(26, 26) + 0.5
    np.save(BG, np.log10(c / c.sum(1, keepdims=True)))
LB = np.load(BG)
TXT = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/carter3.txt').read().upper())
def maxplus(X, Y):   # (m,k) (k,n) -> max over k, argmax
    best = np.full((X.shape[0], Y.shape[1]), -1e9); arg = np.zeros(best.shape, dtype=np.int64)
    for k in range(X.shape[1]):
        v = X[:, k:k+1] + Y[k:k+1, :]; m = v > best; best[m] = v[m]; arg[m] = k
    return best, arg
def solve(ct, A, o):
    c = np.array([A.index(x) for x in ct]); rows = [np.array(r) for r in H.rows_for(c, A, 5, o, True)]
    if min(len(r) for r in rows) == 0: return None
    starts = list(range(o, 93, 5)); Cf = np.array([[c[s + t] for t in range(5)] for s in starts])
    Lj = [(r[:, :5] @ Cf.T + r[:, 5:]) % 26 for r in rows]          # (nopt_j, nblocks): letter at s+j
    nbk = len(starts)
    # pairwise bigram potential between row j (letter at s+j) and row j+1 (letter at s+j+1); j=4 -> next block's row 0
    def pot(j):
        k = (j + 1) % 5
        if j < 4: X, Y = Lj[j], Lj[k]
        else: X, Y = Lj[4][:, :-1], Lj[0][:, 1:]
        return LB[X[:, None, :], Y[None, :, :]].sum(2)              # (n_j, n_k)
    Pt = [pot(j) for j in range(5)]
    sz = [len(r) for r in rows]; a = int(np.argmax(sz)); sz2 = sz[:]; sz2[a] = -1; b = int(np.argmax(sz2))
    def path(u, v):   # max-plus product of potentials from u to v going forward around the cycle
        M = Pt[u]; args = []; j = (u + 1) % 5
        while j != v:
            M, ar = maxplus(M, Pt[j]); args.append((j, ar)); j = (j + 1) % 5
        return M, args
    W1, A1 = path(a, b); W2, A2 = path(b, a)
    tot = W1 + W2.T                                                    # (n_a, n_b)
    cand = []
    xa, xb = np.unravel_index(np.argsort(-tot, axis=None)[:200000], tot.shape)
    ch = np.zeros((len(xa), 5), dtype=np.int64); ch[:, a] = xa; ch[:, b] = xb
    def back(args, start_idx, end_idx, end_var):
        # recover intermediate choices: args list of (var, argmax matrix over [start, var_next])
        nxt = end_idx
        for (var, ar) in reversed(args):
            k = ar[start_idx, nxt]; ch[np.arange(len(start_idx)), var] = k; nxt = k
    back(A1, xa, xb, b); back(A2, xb, xa, a)
    # rescore with 5-gram (letters over the decrypted span) + invertibility
    pos = np.array([[s + j for s in starts] for j in range(5)]); lo, hi = pos.min(), pos.max() + 1
    best = (-99, None)
    for i0 in range(0, len(ch), 20000):
        C = ch[i0:i0 + 20000]; T = np.zeros((len(C), 97), dtype=np.int64)
        for j in range(5): T[:, pos[j]] = Lj[j][C[:, j]]
        T = T[:, lo:hi]; idx = ((((T[:, :-4]*26 + T[:, 1:-3])*26 + T[:, 2:-2])*26 + T[:, 3:-1])*26 + T[:, 4:])
        v = LM5[idx].mean(1)
        D = np.stack([rows[j][C[:, j], :5] for j in range(5)], 1); d = np.rint(np.linalg.det(D.astype(float))).astype(np.int64) % 26
        v = np.where((d % 2 == 1) & (d % 13 != 0), v, -99); k = int(np.argmax(v))
        if v[k] > best[0]: best = (float(v[k]), ''.join(A[x] for x in T[k]))
    return best
def plant(seed):
    g = random.Random(seed); off = g.randrange(len(TXT) - 200); pt = list(TXT[off:off + 97])
    for k, v in H.CRIB.items(): pt[k] = v
    A = g.choice([H.AZ, H.KA]); o = g.randrange(5)
    while True:
        M = np.array([[g.randrange(26) for _ in range(5)] for _ in range(5)]); d = int(round(np.linalg.det(M))) % 26
        if d % 2 and d % 13: break
    b = np.array([g.randrange(26) for _ in range(5)]); p = np.array([A.index(x) for x in pt]); cc = p.copy()
    for s in range(o, 93, 5): cc[s:s + 5] = (M @ p[s:s + 5] + b) % 26
    r = solve(''.join(A[x] for x in cc), A, o)
    if r is None: return None
    acc = sum(x == y for x, y in zip(r[1], ''.join(pt)[o:o + len(r[1])])) / len(r[1])
    return round(r[0], 3), round(acc, 2)
if __name__ == '__main__':
    for s in range(6): print('plant', s, plant(500 + s), flush=True)
    for an, o in (('AZ', 1), ('AZ', 4), ('KA', 0), ('KA', 3), ('KA', 4)):
        r = solve(H.CT, H.AZ if an == 'AZ' else H.KA, o); print('K4', an, o, round(r[0], 3), r[1], flush=True)
    for t in range(10):
        l = list(H.CT); random.Random(t + 950).shuffle(l); ct = ''.join(l); out = []
        for an in ('AZ', 'KA'):
            for o in range(5):
                r = solve(ct, H.AZ if an == 'AZ' else H.KA, o)
                if r: out.append(r[0])
        print('null', t, 'configs alive', len(out), 'max', round(max(out), 3) if out else None, flush=True)
