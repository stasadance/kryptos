#!/usr/bin/env python3
"""it74: why Chaocipher cannot be refuted by K4's cribs (an analytic bound, checked numerically on one wheel).
Lemma: Chaocipher's LEFT (CT) wheel evolves from its start state using only the CT, because the zenith index is
i_t = position of C_t in L_t and the left permutation depends only on i_t. So a start wheel L fixes every i_t,
whatever the PT. The RIGHT wheel then has to satisfy only the 24 crib constraints R_21[pos_t] = P_t, where pos_t
is a known function of the i's. That is consistent iff equal crib letters map to equal positions and
different letters to different positions. With 24 crib letters but only 13 distinct, there are 11 forced
coincidences, each with probability ~1/26: E[#consistent L] ~ 26! * 26^-11 ~ 1e11 for ANY ciphertext.
Check: simulate the lemma (left-wheel trajectory is PT-independent) on random wheels.
Usage: it74_chao_bound.py"""
import random, math, sys
sys.path.insert(0, 'iterations')
from it71_chaocipher import chao
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
rng = random.Random(74); ok = 0
for t in range(200):   # two different PTs giving the same CT? check i-sequence = function of (L, CT) only
    L = rng.sample(AZ, 26); R = rng.sample(AZ, 26); P = ''.join(rng.choice(AZ) for _ in range(60)); C = chao(P, L, R)
    l = list(L); seq = []
    for c in C:
        i = l.index(c); seq.append(i); l = l[i:] + l[:i]; l = [l[0]] + l[2:14] + [l[1]] + l[14:]
    l2, r2, seq2 = list(L), list(R), []
    for p in P:
        i = r2.index(p); seq2.append(i); l2 = l2[i:] + l2[:i]; l2 = [l2[0]] + l2[2:14] + [l2[1]] + l2[14:]
        r2 = r2[i:] + r2[:i]; r2 = r2[1:] + r2[:1]; r2 = r2[:2] + r2[3:14] + [r2[2]] + r2[14:]
    ok += seq == seq2
print(f'lemma check: i-sequence from (L, CT) alone equals true sequence in {ok}/200')
p = 'EASTNORTHEAST' + 'BERLINCLOCK'; forced = len(p) - len(set(p))
print(f'crib letters {len(p)}, distinct {len(set(p))}, forced coincidences {forced}')
print(f'log10 E[#consistent left wheels] ~ {math.lgamma(27)/math.log(10) - forced*math.log10(26):.1f}')
