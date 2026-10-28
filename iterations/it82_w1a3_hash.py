#!/usr/bin/env python3
"""it82 (coach W1 a3): keyword ALPHABETS x the stream library (tools/keygen families + two-key, ~1M streams).
For a concrete tableau (PA, CA) the 24 crib positions force s_i = CA(C_i) - PA(P_i) (Vig/vBeau) or
CA(C_i) + PA(P_i) (Beau), which must equal the stream's k_i up to a global constant (and sign for vBeau).
Every library stream's 24 crib values are normalised (subtract the value at position 21) and hashed (with
negation). Alphabets: the 49k vocabulary under (i) keyed+AZ, (ii) keyed+AZ wrapping after the last keyword
letter, (iii) keyed+KA, and their reverses, plus AZ/KA. Tableaux: Q1 (PA keyed, CA in AZ/KA), Q2, Q3 (PA=CA),
and Q4 = motivated-keyword alphabets x all alphabets, both roles. Expected chance collisions ~ N_lib*N_s/26^23 << 1.
Controls: random library stream + random keyword tableau, English PT with cribs, must hit.
Usage: it82_w1a3_hash.py"""
import sys, random, re
import numpy as np
sys.path.insert(0, 'tools'); sys.path.insert(0, 'iterations')
import keygen as KG
from it66_transposed_keyword import words
AZ, KA = KG.AZ, KG.KA
CT = open('data/ciphertext.txt').read().strip()
POS = list(range(21, 34)) + list(range(63, 74)); PT = 'EASTNORTHEAST' + 'BERLINCLOCK'
rng = np.random.default_rng(82); W64 = rng.integers(1, 2**62, size=23, dtype=np.int64)
def hv(V):   # V: (n,24) ints -> normalised hash (n,)
    D = (V[:, 1:] - V[:, :1]) % 26
    return (D.astype(np.int64) * W64).sum(1)
def library():
    ks = bytearray(); meta = []
    for fam in (KG.families(), KG.twokey_families()):
        for f, par, k, _ in fam:
            ks.extend(k[i] % 26 for i in POS); meta.append((f, par))
    return np.frombuffer(bytes(ks), dtype=np.uint8).reshape(-1, 24).astype(np.int64), meta
def alph_variants(w):
    kw = ''.join(dict.fromkeys(w))
    a = KG.keyed(kw); out = [a, KG.keyed(kw, KA)]
    last = AZ.index(kw[-1]); rest = [c for c in AZ[last + 1:] + AZ[:last + 1] if c not in kw]; out.append(kw + ''.join(rest))
    return out + [x[::-1] for x in out]
def svecs(PAi, CAi, ct):
    """PAi, CAi: (n,26) letter->index arrays. returns diff and sum crib vectors (n,24)."""
    c = np.array([AZ.index(ct[i]) for i in POS]); p = np.array([AZ.index(x) for x in PT])
    return (CAi[:, c] - PAi[:, p]) % 26, (CAi[:, c] + PAi[:, p]) % 26
def idx(alphs): return np.array([[a.index(ch) for ch in AZ] for a in alphs], dtype=np.int64)
def run(ct, H, alphs, mot):
    I = idx(alphs); base = idx([AZ, KA]); hits = []
    def look(PAi, CAi, tag, ia, ib):
        d, s = svecs(PAi, CAi, ct)
        for form, V in (('diff', d), ('sum', s)):
            m = np.isin(hv(V), H)
            for j in np.nonzero(m)[0]: hits.append((tag, form, ia[j] if hasattr(ia, '__len__') else ia, ib[j] if hasattr(ib, '__len__') else ib))
    n = len(alphs); ar = np.arange(n)
    for b in range(2):
        look(I, np.repeat(base[b:b + 1], n, 0), 'Q1', ar, ['AZ', 'KA'][b])
        look(np.repeat(base[b:b + 1], n, 0), I, 'Q2', ['AZ', 'KA'][b], ar)
    look(I, I, 'Q3', ar, ar)
    for m in mot:
        Mi = np.repeat(idx([alphs[m]]), n, 0)
        look(Mi, I, 'Q4', m, ar); look(I, Mi, 'Q4', ar, m)
    return hits
if __name__ == '__main__':
    K, meta = library(); print('library streams', len(K), flush=True)
    H = np.unique(np.concatenate([hv(K), hv((-K) % 26)])); print('hash entries', len(H), flush=True)
    W = [w for w in words() if 3 <= len(w) <= 30]
    alphs = list(dict.fromkeys([AZ, KA, AZ[::-1], KA[::-1]] + [a for w in W for a in alph_variants(w)]))
    motw = set(KG.KEYWORDS); mot = [i for i, a in enumerate(alphs) if any(a in alph_variants(w) for w in motw)]
    print('alphabets', len(alphs), 'motivated', len(mot), flush=True)
    print(f'expected chance collisions ~ {len(H) * len(alphs) * (5 + 2 * len(mot)) * 2 / 26**23:.1e}', flush=True)
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    r = random.Random(82); good = 0
    for t in range(6):
        j = r.randrange(len(K)); PA = alphs[r.randrange(len(alphs))]; CA = r.choice([PA, AZ, KA, alphs[r.choice(mot)]])
        fam, par = meta[j]; kfull = None
        for f, p_, k, _ in (KG.families() if fam != 'F2-twokey' else KG.twokey_families()):
            if f == fam and p_ == par: kfull = k; break
        P = list(eng[(o := r.randrange(len(eng) - 200)):o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        ct = ''.join(CA[(PA.index(p) + k) % 26] for p, k in zip(P, kfull))
        sub_al = list(dict.fromkeys([PA, CA, AZ, KA])); sub_mot = [sub_al.index(CA)] if CA not in (AZ, KA) else []
        h = run(ct, H, sub_al, sub_mot); good += bool(h); print(f'control {fam}: hits {len(h)} {h[:3]}', flush=True)
    print(f'controls {good}/6', flush=True)
    h = run(CT, H, alphs, mot); print('K4 hits', len(h), flush=True)
    for x in h[:50]: print(' ', x[0], x[1], alphs[x[2]] if isinstance(x[2], (int, np.integer)) else x[2], alphs[x[3]] if isinstance(x[3], (int, np.integer)) else x[3])
    for t in range(3):
        n = list(CT); r.shuffle(n); print('null hits', len(run(''.join(n), H, alphs, mot)), flush=True)
