#!/usr/bin/env python3
"""it84b: planted controls for the it84 scorer. English PT with cribs, a random big-list keyword alphabet X,
Q3 Vig periodic p in 30..33. Scan the 50k random alphabets plus X; the planted X must come out on top with an
English-band score. Usage: it84b_control.py"""
import sys, random, re
sys.path.insert(0, 'iterations')
import it84_w1c_score as S
import it82_w1a3_hash as B
Wd = S.W.load_words(); r = random.Random(842)
eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
pool = [a for w in r.sample(Wd, 20000) for a in B.alph_variants(w)][:50000]
for t in range(4):
    X = B.alph_variants(r.choice(Wd))[0]; p = r.randrange(30, 34); key = [r.randrange(26) for _ in range(p)]
    P = list(eng[(o := r.randrange(len(eng) - 200)):o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
    ct = ''.join(X[(X.index(c) + key[i % p]) % 26] for i, c in enumerate(P))
    b = S.scan(ct, pool + [X]); top = b[0]
    print(f'control p={p}: top {top[0]:.3f} p={top[3]} planted_on_top={(pool + [X])[top[4]] == X} | {top[5]}', flush=True)
