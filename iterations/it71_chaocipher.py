#!/usr/bin/env python3
"""it71: Chaocipher (Byrne 1918; method published 2010). Two keyed wheels that permute after every letter.
Alphabet-free fingerprint test: simulate Chaocipher CTs (English with K4's cribs, random wheels) and compare
K4's statistics that do not depend on the wheels: IC and the coincidence counts at lags 1..12. Chaocipher's
permutation is structured, so its lag profile may be distinctive. Correctness control: Rubin's published
test vector. Usage: it71_chaocipher.py"""
import random, re
from collections import Counter
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
def chao(pt, left, right):
    left, right, out = list(left), list(right), []
    for p in pt:
        i = right.index(p); out.append(left[i])
        left = left[i:] + left[:i]; left = [left[0]] + left[2:14] + [left[1]] + left[14:]
        right = right[i:] + right[:i]; right = right[1:] + right[:1]; right = right[:2] + right[3:14] + [right[2]] + right[14:]
    return ''.join(out)
def ic(s):
    c = Counter(s); n = len(s); return sum(v * (v - 1) for v in c.values()) / (n * (n - 1))
def lags(s): return [sum(s[i] == s[i + L] for i in range(len(s) - L)) for L in range(1, 13)]
if __name__ == '__main__':
    tv = chao('WELLDONEISBETTERTHANWELLSAID', 'HXUCZVAMDSLKPEFJRIGTWOBNYQ', 'PTLNBQDEOYSFAVZKGJRIHWXUMC')
    print('test vector', tv, tv == 'OAHQHCNYNXTSZJRRHJBYHQKSOUJY')
    rng = random.Random(71); N = 20000; S = []
    for _ in range(N):
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        S.append(chao(P, rng.sample(AZ, 26), rng.sample(AZ, 26)))
    U = [''.join(rng.choice(AZ) for _ in range(97)) for _ in range(N)]
    k = lags(K4); x = ic(K4)
    print(f'IC: K4 {x:.4f} | chao mean {sum(map(ic, S))/N:.4f} P(<=K4) {sum(ic(s) <= x for s in S)/N:.4f}')
    print('lag | K4 | chao mean, P(chao<=K4), P(chao>=K4) | uniform mean')
    LS = [lags(s) for s in S]; LU = [lags(u) for u in U]
    for j in range(12):
        v = [l[j] for l in LS]
        print(f'{j+1:3d} | {k[j]:2d} | {sum(v)/N:5.2f} {sum(t <= k[j] for t in v)/N:.4f} {sum(t >= k[j] for t in v)/N:.4f} | {sum(l[j] for l in LU)/N:5.2f}')
