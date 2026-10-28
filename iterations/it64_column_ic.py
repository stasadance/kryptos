#!/usr/bin/env python3
"""it64: transposition-then-periodic test, free of alphabets. it55 found an excess of lag-7 CT coincidences
(9 vs 3.24). Hypothesis: K4 = (any transposition of PT) then period-p substitution with p ARBITRARY alphabets.
Then each column i mod p is monoalphabetic over English letters, so the mean column IC is English-like whatever
the alphabets or transposition. Statistic: mean column IC at p. Null = random-key CT (uniform shuffles of K4);
planted control = transposed English + p random alphabets. Usage: it64_column_ic.py"""
import random, re
from collections import Counter
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
def ic(s):
    c = Counter(s); n = len(s); return sum(v * (v - 1) for v in c.values()) / (n * (n - 1)) if n > 1 else 0
def colic(s, p): return sum(ic(s[i::p]) for i in range(p)) / p
rng = random.Random(64)
def planted(p):
    o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); rng.shuffle(P)
    al = [rng.sample(AZ, 26) for _ in range(p)]
    return ''.join(al[i % p][AZ.index(c)] for i, c in enumerate(P))
print(f'p | K4 colIC | null mean, P(null>=K4) | planted mean, P(planted<=K4)')
for p in range(2, 15):
    x = colic(K4, p)
    nul = [colic(''.join(rng.sample(K4, 97)), p) for _ in range(4000)]
    pl = [colic(planted(p), p) for _ in range(2000)]
    print(f'{p:2d} | {x:.4f} | {sum(nul)/4000:.4f} {sum(t >= x for t in nul)/4000:.4f} | '
          f'{sum(pl)/2000:.4f} {sum(t <= x for t in pl)/2000:.4f}', flush=True)
