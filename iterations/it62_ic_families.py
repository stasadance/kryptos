#!/usr/bin/env python3
"""it62: alphabet-free statistical test of model families by K4's index of coincidence (IC), which is invariant
under any relabelling of CT letters (so independent of the unknown alphabets). For each family, simulate the IC
distribution of 97-letter ciphertexts (English P&P text with K4's cribs, random alphabets/keys) and report the
one-sided P(IC_model <= IC_K4) / P(>=). Families whose IC distribution excludes K4 are rejected for ANY alphabet.
Usage: it62_ic_families.py"""
import random, re
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
def ic(s):
    from collections import Counter
    c = Counter(s); n = len(s); return sum(v * (v - 1) for v in c.values()) / (n * (n - 1))
rng = random.Random(62)
def ptext():
    o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
    return [AZ.index(x) for x in P]
def enc_one(P, key):        # one alphabet: a(C) = a(P) + k
    a = list(range(26)); rng.shuffle(a); inv = {v: i for i, v in enumerate(a)}
    return ''.join(AZ[inv[(a[p] + k) % 26]] for p, k in zip(P, key))
def fam(name, keyf, N=4000):
    v = [ic(enc_one(ptext(), keyf())) for _ in range(N)]; x = ic(K4)
    lo = sum(t <= x for t in v) / N; hi = sum(t >= x for t in v) / N
    print(f'{name:38s} mean IC {sum(v)/N:.4f}  P(<=K4)={lo:.4f}  P(>=K4)={hi:.4f}', flush=True)
if __name__ == '__main__':
    print(f'K4 IC = {ic(K4):.4f}  (English ~0.066, uniform 0.0385)')
    fam('monoalphabetic (k=0)', lambda: [0] * 97)
    for m in (2, 3, 4, 5, 6, 8, 10, 13):
        fam(f'iid key digits 0..{m-1} (Gronsfeld-like)', lambda m=m: [rng.randrange(m) for _ in range(97)])
    for p in (2, 3, 4, 5, 6, 7):
        fam(f'periodic p={p}, random shifts', lambda p=p: (lambda w: [w[i % p] for i in range(97)])([rng.randrange(26) for _ in range(p)]))
    fam('English running key (AZ index)', lambda: (lambda o: [AZ.index(c) for c in eng[o:o + 97]])(rng.randrange(len(eng) - 200)))
    fam('iid uniform key', lambda: [rng.randrange(26) for _ in range(97)])
