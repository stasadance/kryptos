#!/usr/bin/env python3
"""it83 (coach W1, big wordlists): the it82 hash sweep and an exact periodic test, over keyword alphabets from
370k English words (dwyl words_alpha) + 686k German words (enz/german-wordlist, umlauts -> AE/OE/UE, ss).
Constructions: keyed+AZ, keyed+KA, wrap, and reverses. Tests:
 (a3) keygen 900k-stream library by exact hash, for Q1/Q2/Q3, and Q4 with the motivated alphabets;
 (a1) periodic key p = 1..48 for Q1/Q2/Q3: s must be constant on every residue class of the crib positions.
Controls: planted (a3) and (a1) encryptions with a random big-list keyword. Nulls: shuffled K4.
Usage: it83_w1_bigwords.py"""
import sys, random, re
import numpy as np
sys.path.insert(0, 'tools'); sys.path.insert(0, 'iterations')
import keygen as KG
import it82_w1a3_hash as B
AZ, KA = KG.AZ, KG.KA
def load_words():
    en = [w.strip().upper() for w in open('/tmp/claude-0/wl/en.txt', errors='ignore')]
    de = []
    for w in open('/tmp/claude-0/wl/de.txt', errors='ignore'):
        w = w.strip().upper()
        for a, b in (('Ä', 'AE'), ('Ö', 'OE'), ('Ü', 'UE'), ('ß', 'SS')): w = w.replace(a, b)
        de.append(w)
    return [w for w in set(en + de) if re.fullmatch('[A-Z]{3,30}', w)]
def periodic_hits(ct, alphs, P_MAX=48):
    I = B.idx(alphs); base = B.idx([AZ, KA]); n = len(alphs); out = []
    pos = np.array(B.POS)
    pairs = [('Q1-AZ', I, np.repeat(base[:1], n, 0)), ('Q1-KA', I, np.repeat(base[1:], n, 0)),
             ('Q2-AZ', np.repeat(base[:1], n, 0), I), ('Q2-KA', np.repeat(base[1:], n, 0), I), ('Q3', I, I)]
    for tag, PAi, CAi in pairs:
        d, s = B.svecs(PAi, CAi, ct)
        for form, V in (('diff', d), ('sum', s)):
            for p in range(1, P_MAX + 1):
                ok = np.ones(n, bool); r = pos % p
                for res in np.unique(r):
                    cols = np.nonzero(r == res)[0]
                    if len(cols) > 1: ok &= (V[:, cols] == V[:, cols[:1]]).all(1)
                if p <= STORE_P:
                    for j in np.nonzero(ok)[0]: out.append((tag, form, p, j))
                else: COUNTS[p] = COUNTS.get(p, 0) + int(ok.sum())
    return out
STORE_P = 25; COUNTS = {}
if __name__ == '__main__':
    W = load_words(); print('words', len(W), flush=True)
    alphs = list(dict.fromkeys([AZ, KA] + [a for w in W for a in B.alph_variants(w)])); print('alphabets', len(alphs), flush=True)
    K, meta = B.library(); H = np.unique(np.concatenate([B.hv(K), B.hv((-K) % 26)]))
    pos_of = {a: i for i, a in enumerate(alphs)}
    mot = [pos_of[a] for w in KG.KEYWORDS for a in B.alph_variants(w) if a in pos_of]; del pos_of
    mot = sorted(set(mot)); print('motivated', len(mot), flush=True)
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    r = random.Random(83); good = 0
    for t in range(6):   # (a1) periodic plants
        X = alphs[r.randrange(len(alphs))]; p = r.randrange(3, 25); key = [r.randrange(26) for _ in range(p)]
        P = list(eng[(o := r.randrange(len(eng) - 200)):o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        ct = ''.join(X[(X.index(c) + key[i % p]) % 26] for i, c in enumerate(P))
        h = periodic_hits(ct, [X, AZ, KA]); f = any(x[0] == 'Q3' and x[1] == 'diff' and x[2] == p and x[3] == 0 for x in h); good += f
        print(f'a1 control p={p}: found={f}', flush=True)
    print(f'a1 controls {good}/6', flush=True)
    from collections import Counter
    C = 150000
    def chunked_a1(ct):
        out = []
        for i in range(0, len(alphs), C):
            out += [(a, b, p, j + i) for a, b, p, j in periodic_hits(ct, alphs[i:i + C])]
        return out
    def chunked_a3(ct):
        M = [alphs[m] for m in mot]; out = []
        for i in range(0, len(alphs), C):
            sub = M + alphs[i:i + C]
            out += B.run(ct, H, sub, list(range(len(M))))
        return out
    COUNTS.clear(); h = chunked_a1(B.CT)
    print('K4 a1 hits by p<=25:', sorted(Counter(x[2] for x in h).items()), '| p>25 pass counts:', sorted(COUNTS.items()), flush=True)
    for x in [x for x in h if x[2] <= 25][:30]: print('  ', x[0], x[1], x[2], alphs[x[3]])
    for t in range(2):
        n = list(B.CT); r.shuffle(n); COUNTS.clear(); hn = chunked_a1(''.join(n))
        print('null a1 hits by p<=25:', sorted(Counter(x[2] for x in hn).items()), '| p>25:', sorted(COUNTS.items()), flush=True)
    h = chunked_a3(B.CT); print('K4 a3 hits', len(h), h[:10], flush=True)
    n = list(B.CT); r.shuffle(n); print('null a3 hits', len(chunked_a3(''.join(n))), flush=True)
