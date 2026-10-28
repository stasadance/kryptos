#!/usr/bin/env python3
"""it58 (H-601 open remainder): base-26 Gromark ("Vimark"-style lagged Fibonacci k_{i+n} = k_i + k_{i+1} mod 26)
and other bases 17-25, primer lengths 2-4, two arbitrary alphabets, exact crib scan (tools/gromark.py).
Control: plant a random primer + two random alphabets on English with K4's cribs, swap it in as the scan's
ciphertext, and require the true primer among the survivors. Usage: it58_vimark.py"""
import sys, random, re
sys.path.insert(0, 'tools'); import gromark as g
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = g.CT
def set_ct(ct):
    g.CT = ct; g.CRIB[:] = [(s - 1 + j, p, ct[s - 1 + j]) for s, w in g.CRIBS.items() for j, p in enumerate(w)]
eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper()); rng = random.Random(58)
ok = n = 0
for b, L in ((26, 3), (26, 4), (20, 4), (17, 4)):
    for t in range(2):
        pr = [rng.randrange(b) for _ in range(L)]; key = g.expand(pr, b)
        q = rng.randrange(len(eng) - 200); pt = list(eng[q:q + 97]); pt[21:34] = 'EASTNORTHEAST'; pt[63:74] = 'BERLINCLOCK'
        A = rng.sample(range(26), 26); B = rng.sample(range(26), 26); Bi = {v: i for i, v in enumerate(B)}
        set_ct(''.join(AZ[Bi[(A[AZ.index(p)] + key[i]) % 26]] for i, p in enumerate(pt)))
        surv = g.scan(b, L); v = sum(d * b ** (L - 1 - j) for j, d in enumerate(pr)); f = v in surv; ok += f; n += 1
        print(f'control b{b}/{L} primer {pr}: found={f} survivors={len(surv)}', flush=True)
print(f'controls {ok}/{n}')
set_ct(K4)
for b in range(17, 27):
    row = []
    for L in (2, 3, 4):
        s = g.scan(b, L); row.append(f'L{L}:{len(s)}')
        if s and b == 26: print('  b26 survivors', [g.digits(x, b, L) for x in s[:20]])
    print(f'K4 base {b}: ' + ' '.join(row), flush=True)
