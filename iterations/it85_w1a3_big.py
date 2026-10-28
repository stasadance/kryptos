#!/usr/bin/env python3
"""it85 (coach W1 a3 at big-list scale, resumable): 3.63M keyword alphabets (it83 lists) x the 900k keygen stream
library by exact normalised hash. Tableaux: Q1/Q2 (AZ/KA), Q3, and Q4 = 83 motivated alphabets x all, both
roles; diff/sum forms. Lookup uses searchsorted on a sorted hash array. Checkpoint: one line per finished chunk
in the output file (resumes by skipping finished chunks). Usage: it85_w1a3_big.py CT_TAG OUTFILE (CT_TAG = k4|nullN)"""
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
    r = random.Random(int(tag[4:]) + 850); nonc = [i for i in range(97) if i not in set(B.POS)]
    c = list(ct); v = [c[i] for i in nonc]; r.shuffle(v)
    for i, x in zip(nonc, v): c[i] = x
    ct = ''.join(c)
done = set()
if os.path.exists(outf):
    for l in open(outf):
        if l.startswith('chunk'): done.add(int(l.split()[1]))
Wd = W.load_words(); alphs = list(dict.fromkeys([AZ, KA] + [a for w in Wd for a in B.alph_variants(w)]))
K, meta = B.library(); H = np.sort(np.unique(np.concatenate([B.hv(K), B.hv((-K) % 26)])))
pos_of = {a: i for i, a in enumerate(alphs)}
M = sorted({pos_of[a] for w in KG.KEYWORDS for a in B.alph_variants(w) if a in pos_of}); del pos_of
Mi_all = B.idx([alphs[m] for m in M]); base = B.idx([AZ, KA])
def member(h):
    j = np.searchsorted(H, h); j[j >= len(H)] = 0; return H[j] == h
C = 100000
with open(outf, 'a') as fo:
    for ci, i0 in enumerate(range(0, len(alphs), C)):
        if ci in done: continue
        I = B.idx(alphs[i0:i0 + C]); n = len(I); hits = []
        pairs = [('Q1-AZ', I, np.repeat(base[:1], n, 0)), ('Q1-KA', I, np.repeat(base[1:], n, 0)),
                 ('Q2-AZ', np.repeat(base[:1], n, 0), I), ('Q2-KA', np.repeat(base[1:], n, 0), I), ('Q3', I, I)]
        for mj in range(len(M)):
            Mi = np.repeat(Mi_all[mj:mj + 1], n, 0); pairs += [(f'Q4-M{M[mj]}-CA', Mi, I), (f'Q4-M{M[mj]}-PA', I, Mi)]
        for t, PAi, CAi in pairs:
            d, s = B.svecs(PAi, CAi, ct)
            for form, V in (('diff', d), ('sum', s)):
                for j in np.nonzero(member(B.hv(V)))[0]: hits.append(f'{t} {form} {alphs[i0 + j]}')
        for h in hits: fo.write('hit ' + h + '\n')
        fo.write(f'chunk {ci} hits {len(hits)}\n'); fo.flush()
    fo.write('DONE\n')
