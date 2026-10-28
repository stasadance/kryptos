#!/usr/bin/env python3
"""it84 (coach W1 c): language-score the it83 periodic passes at p = 30..33 (keyword alphabets, Q1/Q2/Q3,
diff/sum). For p >= 30 the cribs fix the key on the residues they cover. Decrypt every position whose residue
is covered and score the mean quadgram over windows that are fully determined. Keep the best per run. The same
pipeline with the same N runs on shuffled-K4 nulls (crib letters kept in place: only non-crib CT letters are
shuffled), and K4's best is compared with the null maxima (Gumbel fit).
Usage: it84_w1c_score.py [n_nulls]"""
import sys, random
import numpy as np
sys.path.insert(0, 'iterations')
import it83_w1_bigwords as W
import it82_w1a3_hash as B
AZ, KA = B.AZ, B.KA
qg = np.fromfile('/tmp/claude-0/it27/qg.bin', dtype=np.float32)
POS = np.array(B.POS)
def scan(ct, alphs, P_RANGE=range(30, 34), C=100000, keep=20):
    best = []; ctv = np.array([AZ.index(c) for c in ct]); base = B.idx([AZ, KA])
    for i0 in range(0, len(alphs), C):
        I = B.idx(alphs[i0:i0 + C]); n = len(I)
        pairs = [('Q1-AZ', I, np.repeat(base[:1], n, 0)), ('Q1-KA', I, np.repeat(base[1:], n, 0)),
                 ('Q2-AZ', np.repeat(base[:1], n, 0), I), ('Q2-KA', np.repeat(base[1:], n, 0), I), ('Q3', I, I)]
        for tag, PAi, CAi in pairs:
            d, s = B.svecs(PAi, CAi, ct)
            for form, V in (('diff', d), ('sum', s)):
                for p in P_RANGE:
                    r = POS % p; ok = np.ones(n, bool); kres = {}
                    for res in np.unique(r):
                        cols = np.nonzero(r == res)[0]; kres[res] = cols[0]
                        if len(cols) > 1: ok &= (V[:, cols] == V[:, cols[:1]]).all(1)
                    js = np.nonzero(ok)[0]
                    if not len(js): continue
                    cov = [t for t in range(97) if t % p in kres]; covset = set(cov)
                    win = [t for t in range(94) if all(t + u in covset for u in range(4))]
                    if not win: continue
                    PAinv = np.argsort(PAi[js], axis=1)          # index -> AZ letter
                    P = np.zeros((len(js), 97), np.int64)
                    for t in cov:
                        k = V[js, kres[t % p]]; cv = CAi[js, ctv[t]]
                        pv = (cv - k) % 26 if form == 'diff' else (k - cv) % 26
                        P[:, t] = PAinv[np.arange(len(js)), pv]
                    w = np.array(win)
                    q = ((P[:, w] * 26 + P[:, w + 1]) * 26 + P[:, w + 2]) * 26 + P[:, w + 3]
                    sc = qg[q].mean(1)
                    for j in np.argsort(-sc)[:keep]:
                        best.append((float(sc[j]), tag, form, p, i0 + js[j], ''.join(AZ[x] if t in covset else '.' for t, x in enumerate(P[j]))))
        best = sorted(best, reverse=True)[:keep]
    return best
if __name__ == '__main__':
    nn = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    Wd = W.load_words(); alphs = list(dict.fromkeys([AZ, KA] + [a for w in Wd for a in B.alph_variants(w)]))
    print('alphabets', len(alphs), flush=True)
    b = scan(B.CT, alphs); print(f'K4 best {b[0][0]:.3f}', flush=True)
    for x in b[:10]: print(f'  {x[0]:.3f} {x[1]} {x[2]} p={x[3]} {alphs[x[4]]} {x[5]}', flush=True)
    rng = random.Random(84); mx = []
    nonc = [i for i in range(97) if i not in set(B.POS)]
    for t in range(nn):
        c = list(B.CT); vals = [c[i] for i in nonc]; rng.shuffle(vals)
        for i, v in zip(nonc, vals): c[i] = v
        m = scan(''.join(c), alphs)[0][0]; mx.append(m); print(f'null max {m:.3f}', flush=True)
    mu, sd = np.mean(mx), np.std(mx); beta = sd * np.sqrt(6) / np.pi; loc = mu - 0.5772 * beta
    pval = 1 - np.exp(-np.exp(-(b[0][0] - loc) / beta))
    print(f'Gumbel fit over {nn} null maxima: K4 best {b[0][0]:.3f}, p = {pval:.3g}', flush=True)
