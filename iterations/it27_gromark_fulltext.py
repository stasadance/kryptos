#!/usr/bin/env python3
"""Iteration 27: full-text decision of the Gromark survivors (Bean 2021 / w-gromark): base 10 primer 5 (39), base 10
primer 4 (3), base 8 primer 5 (4), all crib-consistent only under TWO arbitrary alphabets posC(C)=posP(P)+k.
Each survivor gives a fixed key stream; it05's crib-exact two-alphabet annealer (sa.c, quadgram score) then decides
it from the full text (it05 calibration: 17/20 planted streams recovered, English -395..-434, random-stream null max
about -498). Controls here: 8 planted Gromark encryptions (random primer, random alphabets, English + cribs).
Usage: python3 iterations/it27_gromark_fulltext.py WORKDIR   (WORKDIR holds sa, qg.bin, test.txt from it05/prep.py)"""
import sys, os, json, random, subprocess
from multiprocessing import Pool
sys.path.insert(0, "tools"); import gromark as G
W = sys.argv[1]; K4 = open("data/ciphertext.txt").read().strip()
CR = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}; AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def sa(ct, ks, seed, R=8, IT=3000000):
    out = subprocess.run([os.path.join(W, "sa"), "2", "0", ct, ks, str(R), str(IT), str(seed), "25"], cwd=W, capture_output=True, text=True).stdout.split("\n")
    res = [(float(l.split()[0]), l.split()[1]) for l in out if l.strip()]
    return max(res)
def keystr(primer, base): return "".join(chr(65 + d) for d in G.expand(primer, base))
def job(a):
    tag, ct, ks, seed, pt = a; b = sa(ct, ks, seed)
    acc = None if pt is None else round(sum(x == y for x, y in zip(b[1], pt)) / 97, 2)
    return dict(tag=tag, best=b[0], acc=acc, dec=b[1])
if __name__ == "__main__":
    test = open(os.path.join(W, "test.txt")).read(); rng = random.Random(27); jobs = []
    for s in range(8):
        base = rng.choice([8, 10]); L = rng.choice([4, 5]); primer = [rng.randrange(base) for _ in range(L)]
        o = rng.randrange(len(test) - 200); pt = list(test[o:o + 97])
        for st, w in CR.items(): pt[st:st + len(w)] = w
        pt = "".join(pt); A = list(range(26)); rng.shuffle(A); B = rng.sample(range(26), 26); Binv = {x: l for l, x in enumerate(B)}
        k = G.expand(primer, base); ct = "".join(AZ[Binv[(A[AZ.index(c)] + k[i]) % 26]] for i, c in enumerate(pt))
        jobs.append((f"control b{base} {''.join(map(str, primer))}", ct, keystr(primer, base), 100 + s, pt))
    surv = []
    for base, L in ((10, 5), (10, 4), (8, 5)):
        for v in G.scan(base, L):
            pr = [int(ch) for ch in G.fmt(v, base, L)] if isinstance(v, int) else list(v)
            surv.append((base, pr))
    print("survivors:", len(surv), flush=True)
    for j, (base, pr) in enumerate(surv):
        jobs.append((f"K4 b{base} {''.join(map(str, pr))}", K4, keystr(pr, base), j, None))
    with Pool(4) as P:
        for r in P.imap(job, jobs): print(json.dumps(r), flush=True)
