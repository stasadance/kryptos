#!/usr/bin/env python3
"""it86 (coach W3 on W1): error-tolerant version of the it82/85 hash. Variants: (a) each of the 24 crib letters
deleted in turn (a carving error or a wrong crib letter), matching on the remaining 23 values; (b) BERLINCLOCK
shifted by -1/+1 (an omitted or inserted letter between the cribs), with the stream values taken at the shifted
positions. Alphabets: the 3.63M big-list keyword alphabets; tableaux Q1-AZ/KA, Q2-AZ/KA, Q3; diff/sum.
Library: 900k keygen streams. Expected chance collisions (deletion): N_lib*N_vec*24/26^22 ~ 2e-15.
Checkpointed per chunk. Usage: it86_w3_errtol_hash.py CT_TAG OUTFILE"""
import sys, random, os
import numpy as np
sys.path.insert(0, 'iterations'); sys.path.insert(0, 'tools')
import it83_w1_bigwords as W
import it82_w1a3_hash as B
import keygen as KG
AZ, KA = B.AZ, B.KA
tag, outf = sys.argv[1], sys.argv[2]
ct = B.CT
if tag.startswith('null'):
    r = random.Random(int(tag[4:]) + 860); nonc = [i for i in range(97) if i not in set(B.POS)]
    c = list(ct); v = [c[i] for i in nonc]; r.shuffle(v)
    for i, x in zip(nonc, v): c[i] = x
    ct = ''.join(c)
rng = np.random.default_rng(86); WH = rng.integers(1, 2**62, size=24, dtype=np.int64)
def hsub(V, cols):
    V = V[:, cols]; D = (V[:, 1:] - V[:, :1]) % 26; return (D.astype(np.int64) * WH[:D.shape[1]]).sum(1)
POS1 = list(range(21, 34)); POS2 = list(range(63, 74)); PT = 'EASTNORTHEAST' + 'BERLINCLOCK'
# library: values at crib positions, and at BERLINCLOCK shifted -1/+1
ks = {-1: bytearray(), 0: bytearray(), 1: bytearray()}
for fam in (KG.families(), KG.twokey_families()):
    for f, par, k, _ in fam:
        for sh in (-1, 0, 1): ks[sh].extend(k[i] % 26 for i in POS1 + [j + sh for j in POS2])
L = {sh: np.frombuffer(bytes(b), dtype=np.uint8).reshape(-1, 24).astype(np.int64) for sh, b in ks.items()}
VARS = [('del', d, 0, [c for c in range(24) if c != d]) for d in range(24)] + [('shift', sh, sh, list(range(24))) for sh in (-1, 1)]
HS = {}
for name, d, sh, cols in VARS:
    Lv = L[sh]; HS[(name, d)] = np.sort(np.unique(np.concatenate([hsub(Lv, cols), hsub((-Lv) % 26, cols)])))
def member(H, h):
    j = np.searchsorted(H, h); j[j >= len(H)] = 0; return H[j] == h
done = set()
if os.path.exists(outf):
    for l in open(outf):
        if l.startswith('chunk'): done.add(int(l.split()[1]))
Wd = W.load_words(); alphs = list(dict.fromkeys([AZ, KA] + [a for w in Wd for a in B.alph_variants(w)]))
base = B.idx([AZ, KA]); C = 100000
cpos = np.array([AZ.index(ct[i]) for i in POS1 + POS2]); ppos = np.array([AZ.index(x) for x in PT])
with open(outf, 'a') as fo:
    for ci, i0 in enumerate(range(0, len(alphs), C)):
        if ci in done: continue
        I = B.idx(alphs[i0:i0 + C]); n = len(I); hits = []
        pairs = [('Q1-AZ', I, np.repeat(base[:1], n, 0)), ('Q1-KA', I, np.repeat(base[1:], n, 0)),
                 ('Q2-AZ', np.repeat(base[:1], n, 0), I), ('Q2-KA', np.repeat(base[1:], n, 0), I), ('Q3', I, I)]
        for t, PAi, CAi in pairs:
            d_, s_ = (CAi[:, cpos] - PAi[:, ppos]) % 26, (CAi[:, cpos] + PAi[:, ppos]) % 26
            for form, V in (('diff', d_), ('sum', s_)):
                for name, dd, sh, cols in VARS:
                    for j in np.nonzero(member(HS[(name, dd)], hsub(V, cols)))[0]: hits.append(f'{t} {form} {name}{dd} {alphs[i0 + j]}')
        for h in hits: fo.write('hit ' + h + '\n')
        fo.write(f'chunk {ci} hits {len(hits)}\n'); fo.flush()
    fo.write('DONE\n')
