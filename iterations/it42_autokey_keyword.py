#!/usr/bin/env python3
"""it42 (H-2103/H-1207, restricted): PT-autokey, lag L = 1..13, under ONE KEYWORD-MIXED alphabet
(keyword + rest of A-Z, Sanborn's K1-K3 construction), all 9 models of it36 (key value a(p)/AZ/KA x
vig/beau/var).  Exact: it36's decrypt() propagates the whole plaintext from the cribs; a candidate
must reproduce the ENE-internal relations AND BERLINCLOCK (bad == 0).  Survivors are quadgram-scored.
Keywords: every distinct word (>=3 letters) of the local corpora + K1-K3 plaintext word pairs + Kryptos
keywords.  Control: planted English encrypted under a random dictionary keyword, random L/model.
Usage: python3 it42_autokey_keyword.py QG.bin"""
import sys, re, glob, random, time
import numpy as np
sys.argv = [sys.argv[0], sys.argv[1]] + sys.argv[2:]
sys.path.insert(0, 'iterations')
import it36_ptautokey_sa as A
AZ = A.AZ
def keyed(w):
    s = []
    for ch in w + AZ:
        if ch not in s: s.append(ch)
    return ''.join(s)
def words():
    W = set()
    for f in glob.glob('/tmp/claude-0/corpus/*.txt'):
        W |= set(re.findall(r'[A-Z]{3,}', open(f, errors='ignore').read().upper()))
    pt = re.findall(r'[A-Z]+', open('/tmp/claude-0/corpus/kryptos_pt.txt').read().upper())
    W |= {pt[i] + pt[i + 1] for i in range(len(pt) - 1)}
    W |= {'KRYPTOS', 'PALIMPSEST', 'ABSCISSA', 'BERLINCLOCK', 'SANBORN', 'SCHEIDT', 'WEBSTER', 'LANGLEY',
          'URANIA', 'WELTZEITUHR', 'ALEXANDERPLATZ', 'BERLIN', 'CLOCK', 'SHADOW', 'ILLUSION', 'IQLUSION',
          'LUCID', 'MEMORY', 'DESPARATLY', 'UNDERGRUUND', 'EASTNORTHEAST', 'NORTHEAST', 'CARTER', 'EGYPT'}
    return sorted(W)
def score(p, qg):
    s = 0.0
    for i in range(len(p) - 3):
        s += qg[((p[i] * 26 + p[i + 1]) * 26 + p[i + 2]) * 26 + p[i + 3]]
    return s
def run(ct, W, qg):
    c = np.array([AZ.index(x) for x in ct], dtype=np.int64)
    p = np.zeros(97, dtype=np.int64); hits = []
    for w in W:
        K = keyed(w)
        a = np.array([K.index(x) for x in AZ], dtype=np.int64)
        inv = np.array([AZ.index(x) for x in K], dtype=np.int64)
        for L in range(1, 14):
            for form in range(3):
                for kr in range(3):
                    if A.decrypt(c, a, inv, L, form, kr, p) == 0:
                        hits.append((score(p, qg), w, L, form, kr, ''.join(AZ[x] for x in p)))
    return hits
if __name__ == '__main__':
    qg = A.qg
    W = words(); print('keywords', len(W), flush=True)
    rng = random.Random(42)
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    # control: plant
    ok = 0; NC = 6
    for t in range(NC):
        w = rng.choice(W); L = rng.randint(1, 13); form = rng.randrange(3); kr = rng.randrange(3)
        K = keyed(w); a = [K.index(x) for x in AZ]; inv = [AZ.index(x) for x in K]
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97])
        P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        pi = [AZ.index(x) for x in P]; ci = []
        for i in range(97):
            pp = pi[i - L] if i >= L else pi[i]  # primer = first L PT letters themselves
            Kv = a[pp] if kr == 0 else (pp if kr == 1 else A.KAI[pp])
            v = (a[pi[i]] + Kv) % 26 if form == 0 else ((Kv - a[pi[i]]) % 26 if form == 1 else (a[pi[i]] - Kv) % 26)
            ci.append(inv[v])
        ct = ''.join(AZ[x] for x in ci)
        h = run(ct, [w] + rng.sample(W, 2000), qg)
        found = any(x[1] == w and x[2] == L and x[3] == form and x[4] == kr and x[5][34:63] == ''.join(P[34:63]) for x in h)
        ok += found
        print(f'control {t}: {w} L={L} form={form} kr={kr} found={found} total hits={len(h)}', flush=True)
    print(f'controls {ok}/{NC}', flush=True)
    t = time.time(); h = run(A.K4, W, qg)
    h.sort(reverse=True)
    print(f'K4: {len(h)} crib-exact keyword configs ({time.time()-t:.0f}s)')
    for x in h[:15]: print(f'{x[0]:.1f} {x[1]} L={x[2]} form={x[3]} kr={x[4]} {x[5]}')
