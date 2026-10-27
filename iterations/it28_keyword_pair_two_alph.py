#!/usr/bin/env python3
"""Iteration 28: KRYPTOS/PALIMPSEST/ABSCISSA keyword-pair keys under TWO arbitrary alphabets, decided from the full text.
k_i = s1*n(W1[(i+o1) mod L1]) + s2*n(W2[(i+o2) mod L2]) mod 26, n = AZ or KA index (same for both words), s = +-1.
Model B(c) = A(p) + k (two unknown alphabets). Crib-untestable (it19: 7+8, 7+10 feasible for nulls), but a fixed
stream is decidable by it05's annealer. Prefilter: tools/latin_filter (X28=X66, 22 inequalities) plus the additive
two-alphabet identity k24+k34 = k29+k33 (1-indexed). Survivors annealed (sa.c), compared with it05 null/controls."""
import sys, os, json, itertools, subprocess
from multiprocessing import Pool
sys.path.insert(0, "tools"); import latin_filter as LF
W = sys.argv[1]; K4 = open("data/ciphertext.txt").read().strip(); AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
WORDS = ["KRYPTOS", "PALIMPSEST", "ABSCISSA"]
def streams():
    for w1, w2 in itertools.combinations(WORDS, 2):
        for nm, N in (("AZ", AZ), ("KA", KA)):
            for s1, s2 in ((1, 1), (1, -1), (-1, 1)):
                for o1 in range(len(w1)):
                    for o2 in range(len(w2)):
                        k = [(s1 * N.index(w1[(i + o1) % len(w1)]) + s2 * N.index(w2[(i + o2) % len(w2)])) % 26 for i in range(97)]
                        yield (w1, w2, nm, s1, s2, o1, o2), k
def passes(k):
    s = "".join(chr(65 + x) for x in k)
    return not LF.check(s) and (k[23] + k[33] - k[28] - k[32]) % 26 == 0
def job(a):
    j, par, k = a; s = "".join(chr(65 + x) for x in k)
    out = subprocess.run([os.path.join(W, "sa"), "2", "0", K4, s, "8", "3000000", str(j), "25"], cwd=W, capture_output=True, text=True).stdout.split("\n")
    res = [(float(l.split()[0]), l.split()[1]) for l in out if l.strip()]; b = max(res)
    return dict(par=par, best=b[0], dec=b[1])
if __name__ == "__main__":
    allk = list(streams()); surv = [(j, p, k) for j, (p, k) in enumerate(allk) if passes(k)]
    # (s1,s2)=(-1,-1) is the negation of (1,1): B(c)=A(p)-k is the same model with A,B reflected, so omitted
    print(f"streams {len(allk)}, pass crib prefilter {len(surv)}", flush=True)
    with Pool(4) as P:
        for r in P.imap(job, surv): print(json.dumps(r), flush=True)
