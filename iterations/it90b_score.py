#!/usr/bin/env python3
"""it90b: enumerate every crib-consistent Hill key (n=4 affine; n=5 lin/aff where combos <= 2e7), keep invertible D
(gcd(det,26)=1), decrypt full blocks, score per-letter with the 5-gram LM over decrypted letters. Same pipeline on
nulls: K4 with all CT letters shuffled (crib PT fixed) -> max per run. usage: it90b_score.py TAG (k4|nullN)"""
import sys, itertools, math, random
import numpy as np
sys.argv += [] ; sys.path.insert(0, 'iterations')
import it90_hill4_affine as H
LM = np.memmap('/tmp/claude-0/lm/ng5.bin', dtype=np.float32, mode='r')
tag = sys.argv[1]; ct = H.CT
if tag.startswith('null'):
    r = random.Random(int(tag[4:]) + 900); l = list(ct); r.shuffle(l); ct = ''.join(l)
def score(T):   # T: (m, L) letters, -1 = undecrypted -> score contiguous 5-grams fully decrypted
    L = T.shape[1]; s = np.zeros(len(T)); cnt = 0
    for i in range(L - 4):
        if (T[0, i:i+5] < 0).any(): continue
        idx = np.zeros(len(T), dtype=np.int64)
        for j in range(5): idx = idx * 26 + T[:, i + j]
        s += LM[idx]; cnt += 1
    return s / cnt
best = []
for n, aff in [tuple(map(int, x.split(":"))) for x in sys.argv[2].split(",")]:
    for an, A in (('AZ', H.AZ), ('KA', H.KA)):
        c = np.array([A.index(x) for x in ct])
        for o in range(n):
            rows = [np.array(r) for r in H.rows_for(c, A, n, o, aff)]
            tot = math.prod(len(r) for r in rows)
            print(n, aff, an, o, [len(r) for r in rows], tot, flush=True)
            if tot == 0 or tot > 2e7: continue
            starts = list(range(o, 97 - n + 1, n)); Cfull = np.array([[c[s + t] for t in range(n)] for s in starts])
            # per row j, per solution: letters at positions s+j
            Lj = [(r[:, :n] @ Cfull.T + r[:, n:]) % 26 for r in rows]          # (nsol_j, nblocks)
            for chunk in itertools.product(*[range(len(r)) for r in rows[:n - 2]]):
                a = np.array(list(itertools.product(range(len(rows[n - 2])), range(len(rows[n - 1])))))
                D = np.stack([np.repeat(rows[j][chunk[j], :n][None], len(a), 0) for j in range(n - 2)] + [rows[n - 2][a[:, 0], :n], rows[n - 1][a[:, 1], :n]], 1)
                det = np.rint(np.linalg.det(D.astype(float))).astype(np.int64) % 26
                ok = (det % 2 == 1) & (det % 13 != 0); a = a[ok]
                if not len(a): continue
                T = -np.ones((len(a), 97), dtype=np.int64)
                for k, s in enumerate(starts):
                    for j in range(n - 2): T[:, s + j] = Lj[j][chunk[j], k]
                    T[:, s + n - 2] = Lj[n - 2][a[:, 0], k]; T[:, s + n - 1] = Lj[n - 1][a[:, 1], k]
                sc = score(T); b = int(np.argmax(sc))
                best.append((float(sc[b]), n, aff, an, o, ''.join(A[x] if x >= 0 else '.' for x in T[b])))
best.sort(reverse=True)
print(tag, 'configs scored; best', best[0][:5] if best else None)
for b in best[:3]: print(f'{b[0]:.3f} n={b[1]} aff={b[2]} {b[3]} o={b[4]} {b[5]}')
