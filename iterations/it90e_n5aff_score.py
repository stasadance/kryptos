#!/usr/bin/env python3
"""it90e: Hill n=5 affine, the 5 crib-consistent (numbering, offset) configs on K4 are crib-undecidable (row
solution counts up to 1352). Decide by full text: SA over the 5 row-choice indices (invertible D required), 5-gram LM
per decrypted letter. Controls: plant n=5 affine on English, same pipeline must recover. Null: shuffled-K4 configs.
usage: it90e_n5aff_score.py"""
import sys, random, math, re, json
import numpy as np
sys.path.insert(0, 'iterations'); import it90_hill4_affine as H
LM = np.memmap('/tmp/claude-0/lm/ng5.bin', dtype=np.float32, mode='r')
TXT = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/carter3.txt').read().upper())
def solve(ct, A, o, seed, iters=60000):
    c = np.array([A.index(x) for x in ct]); rows = [np.array(r) for r in H.rows_for(c, A, 5, o, True)]
    if min(len(r) for r in rows) == 0: return None
    starts = list(range(o, 93, 5)); Cf = np.array([[c[s + t] for t in range(5)] for s in starts])
    Lj = [(r[:, :5] @ Cf.T + r[:, 5:]) % 26 for r in rows]
    pos = np.array([[s + j for s in starts] for j in range(5)])
    lo, hi = pos.min(), pos.max() + 1
    def text(ch):
        T = np.zeros(97, dtype=np.int64)
        for j in range(5): T[pos[j]] = Lj[j][ch[j]]
        return T[lo:hi]
    def sc(ch):
        T = text(ch); idx = ((((T[:-4]*26 + T[1:-3])*26 + T[2:-2])*26 + T[3:-1])*26 + T[4:]); return float(LM[idx].mean())
    def inv(ch):
        D = np.array([rows[j][ch[j], :5] for j in range(5)]); d = int(round(np.linalg.det(D))) % 26; return d % 2 == 1 and d % 13 != 0
    g = random.Random(seed); best = (-99, None)
    def scmany(ch, j):   # score every option of row j, others fixed; non-invertible -> -99
        k = len(rows[j]); T = np.zeros((k, 97), dtype=np.int64)
        for q in range(5):
            T[:, pos[q]] = Lj[q][ch[q]][None] if q != j else Lj[j]
        T = T[:, lo:hi]; idx = ((((T[:, :-4]*26 + T[:, 1:-3])*26 + T[:, 2:-2])*26 + T[:, 3:-1])*26 + T[:, 4:])
        v = LM[idx].mean(1)
        D = np.stack([np.repeat(rows[q][ch[q], :5][None], k, 0) if q != j else rows[j][:, :5] for q in range(5)], 1)
        d = np.rint(np.linalg.det(D.astype(float))).astype(np.int64) % 26
        return np.where((d % 2 == 1) & (d % 13 != 0), v, -99)
    for rst in range(40):
        ch = [g.randrange(len(r)) for r in rows]; cur = -99
        for sweep in range(12):
            imp = False
            for j in g.sample(range(5), 5):
                v = scmany(ch, j); b = int(np.argmax(v))
                if v[b] > cur + 1e-9: cur = float(v[b]); ch[j] = b; imp = True
            if not imp: break
        if cur > best[0]: best = (cur, ''.join(A[x] for x in text(ch)))
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
    r = solve(''.join(A[x] for x in cc), A, o, seed); lo = min(o, 0)
    acc = sum(a == b2 for a, b2 in zip(r[1], ''.join(pt)[o:o + len(r[1])])) / len(r[1])
    return r[0], acc
if __name__ == '__main__':
    for s in range(4): print('plant', s, plant(500 + s), flush=True)
    for an, o in (('AZ', 1), ('AZ', 4), ('KA', 0), ('KA', 3), ('KA', 4)):
        A = H.AZ if an == 'AZ' else H.KA; print('K4', an, o, solve(H.CT, A, o, 77), flush=True)
    for t in range(3):
        l = list(H.CT); random.Random(t + 950).shuffle(l); ct = ''.join(l); out = []
        for an in ('AZ', 'KA'):
            for o in range(5):
                r = solve(ct, H.AZ if an == 'AZ' else H.KA, o, 78)
                if r: out.append(r[0])
        print('null', t, 'configs alive', len(out), 'max', max(out) if out else None, flush=True)
