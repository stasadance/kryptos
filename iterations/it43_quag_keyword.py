#!/usr/bin/env python3
"""it43: Quagmire I/II/III with a KEYWORD-mixed alphabet (49k corpus words), period p = 1..26, Vig/Beau style.
Q1: plain alphabet = keyed(w), cipher = AZ or KA; Q2: plain AZ/KA, cipher keyed(w); Q3: both keyed(w).
The cribs fix the shift of every class they touch; a config passes if all crib classes are consistent.
For p <= 13 every class is fixed (ENE covers 13 consecutive residues) -> full decrypt + quadgram score.
Control: planted Q1/Q2/Q3 encryption with a random keyword."""
import sys, re, glob, random
sys.argv[1:] = sys.argv[1:] or ["/tmp/claude-0/it27/qg.bin"]
import numpy as np
sys.path.insert(0, 'iterations')
from it42_autokey_keyword import words, keyed, score, A
AZ = A.AZ; KA = A.KA; CT = A.K4
PAIRS = [(21 + i, c) for i, c in enumerate('EASTNORTHEAST')] + [(63 + i, c) for i, c in enumerate('BERLINCLOCK')]
def run(ct, W, qg, out):
    hits = 0
    for w in W:
        K = keyed(w)
        for model in ('Q1AZ', 'Q1KA', 'Q2AZ', 'Q2KA', 'Q3'):
            PA = K if model in ('Q1AZ', 'Q1KA', 'Q3') else (AZ if model == 'Q2AZ' else KA)
            CA = K if model in ('Q2AZ', 'Q2KA', 'Q3') else (AZ if model == 'Q1AZ' else KA)
            for st in 'VB':
                for p in range(1, 27):
                    key = {}; ok = True
                    for i, pl in PAIRS:
                        s = (CA.index(ct[i]) - PA.index(pl)) % 26 if st == 'V' else (CA.index(ct[i]) + PA.index(pl)) % 26
                        if key.setdefault(i % p, s) != s: ok = False; break
                    if not ok: continue
                    hits += 1
                    if len(key) == p:
                        pt = ''.join(PA[(CA.index(c) - key[i % p]) % 26] if st == 'V' else PA[(key[i % p] - CA.index(c)) % 26] for i, c in enumerate(ct))
                        out.append((score(np.array([AZ.index(x) for x in pt]), qg), w, model, st, p, pt))
                    else:
                        out.append((None, w, model, st, p, len(key)))
    return hits
if __name__ == '__main__':
    qg = A.qg; W = words(); rng = random.Random(43)
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    ok = 0
    for t in range(6):
        w = rng.choice(W); K = keyed(w); model = rng.choice(['Q1AZ', 'Q2KA', 'Q3']); st = rng.choice('VB'); p = rng.randint(3, 13)
        PA = K if model in ('Q1AZ', 'Q3') else KA; CA = K if model in ('Q2KA', 'Q3') else AZ
        key = [rng.randrange(26) for _ in range(p)]
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        ct = ''.join(CA[(PA.index(x) + key[i % p]) % 26] if st == 'V' else CA[(key[i % p] - PA.index(x)) % 26] for i, x in enumerate(P))
        out = []; run(ct, [w] + rng.sample(W, 300), qg, out)
        f = any(x[1] == w and x[2] == model and x[3] == st and x[4] == p and x[5] == ''.join(P) for x in out)
        ok += f; print(f'control {w} {model} {st} p={p}: found={f}, configs passing={len(out)}', flush=True)
    print(f'controls {ok}/6')
    out = []; n = run(CT, W, qg, out)
    full = sorted([x for x in out if x[0] is not None], reverse=True)
    from collections import Counter
    print(f'K4: {n} crib-consistent configs; fully determined (all classes fixed): {len(full)}')
    print('consistent by period:', sorted(Counter(x[4] for x in out).items()))
    for x in full[:10]: print(f'{x[0]:.1f} {x[1]} {x[2]} {x[3]} p={x[4]} {x[5]}')
