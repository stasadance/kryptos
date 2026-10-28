#!/usr/bin/env python3
"""it44: Quagmire IV (independent PT and CT keyword alphabets), Vig/Beau, periods 1..25.
One alphabet from a MOTIVATED list (Kryptos/K1-K3/Berlin terms), the other from the 49k corpus vocabulary,
both assignments (motivated as PT or as CT alphabet).  Exact crib-class consistency; numba.
Control: planted Q4 encryption with a motivated + random vocabulary keyword."""
import sys, re, random
sys.argv[1:] = sys.argv[1:] or ["/tmp/claude-0/it27/qg.bin"]
import numpy as np
from numba import njit
sys.path.insert(0, 'iterations')
from it42_autokey_keyword import words, keyed, A
AZ = A.AZ; CT = A.K4
MOT = ['KRYPTOS', 'PALIMPSEST', 'ABSCISSA', 'BERLIN', 'CLOCK', 'BERLINCLOCK', 'SANBORN', 'SCHEIDT', 'WEBSTER',
       'LANGLEY', 'URANIA', 'WELTZEITUHR', 'ALEXANDERPLATZ', 'SHADOW', 'ILLUSION', 'IQLUSION', 'LUCID', 'MEMORY',
       'UNDERGRUUND', 'UNDERGROUND', 'EASTNORTHEAST', 'NORTHEAST', 'CARTER', 'EGYPT', 'TUTANKHAMUN', 'LAYERTWO',
       'IDBYROWS', 'XLAYERTWO', 'VIRTUALLY', 'INVISIBLE', 'DESPARATLY', 'SLOWLY', 'CANDLE', 'CHAMBER', 'MAGNETIC',
       'FIELD', 'LATITUDE', 'LONGITUDE', 'POSITION', 'COMPASS', 'LODESTONE', 'ANTIPODES', 'MATRIX', 'ENIGMA',
       'CIA', 'AGENCY', 'SECRET', 'HIDDEN', 'MESSAGE', 'DIGETAL', 'INTERPRETATU', 'TOTALLY', 'WORLDCLOCK',
       'MENGENLEHREUHR', 'FERNSEHTURM', 'CHECKPOINT', 'CHARLIE', 'WALL', 'BERLINWALL', 'KOMPASS']
PAIRS = [(21 + i, c) for i, c in enumerate('EASTNORTHEAST')] + [(63 + i, c) for i, c in enumerate('BERLINCLOCK')]
POS = np.array([i for i, _ in PAIRS], dtype=np.int64)
def idx(K): return np.array([K.index(x) for x in AZ], dtype=np.int64)
@njit(cache=True)
def check(pa, ca, pl, cl, pos, out):
    """pa/ca: AZ letter -> position. returns count of passing (p,style); writes flags into out[style,p]"""
    n = 0
    for st in range(2):
        for p in range(1, 26):
            key = np.full(p, -1, dtype=np.int64); ok = True
            for t in range(pos.shape[0]):
                s = (ca[cl[t]] - pa[pl[t]]) % 26 if st == 0 else (ca[cl[t]] + pa[pl[t]]) % 26
                r = pos[t] % p
                if key[r] < 0: key[r] = s
                elif key[r] != s: ok = False; break
            out[st, p] = ok
            n += ok
    return n
def run(ct, M, W):
    pl = np.array([AZ.index(c) for _, c in PAIRS], dtype=np.int64)
    cl = np.array([AZ.index(ct[i]) for i, _ in PAIRS], dtype=np.int64)
    out = np.zeros((2, 26), dtype=np.bool_); hits = []
    for m in M:
        km = idx(keyed(m))
        for w in W:
            kw = idx(keyed(w))
            for role, (pa, ca) in (('motPT', (km, kw)), ('motCT', (kw, km))):
                if check(pa, ca, pl, cl, POS, out):
                    for st in range(2):
                        for p in range(1, 26):
                            if out[st, p]: hits.append((m, w, role, 'VB'[st], p))
    return hits
if __name__ == '__main__':
    W = words(); rng = random.Random(44)
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    ok = 0
    for t in range(6):
        m = rng.choice(MOT); w = rng.choice(W); PA, CA = (keyed(m), keyed(w)) if t % 2 else (keyed(w), keyed(m))
        st = rng.choice('VB'); p = rng.randint(3, 20); key = [rng.randrange(26) for _ in range(p)]
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        ct = ''.join(CA[(PA.index(x) + key[i % p]) % 26] if st == 'V' else CA[(key[i % p] - PA.index(x)) % 26] for i, x in enumerate(P))
        h = run(ct, [m], [w] + rng.sample(W, 2000))
        f = any(x[0] == m and x[1] == w and x[3] == st and x[4] == p for x in h)
        ok += f; print(f'control {m}/{w} {st} p={p}: found={f} total={len(h)}', flush=True)
    print(f'controls {ok}/6', flush=True)
    h = run(CT, MOT, W)
    from collections import Counter
    print(f'K4: {len(h)} consistent (motivated x 49k x 2 roles x V/B x p<=25)')
    print('by period:', sorted(Counter(x[4] for x in h).items()))
    for x in h[:30]: print(x)
