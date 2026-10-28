#!/usr/bin/env python3
"""it55: alphabet-free test for ciphertext-autokey with ANY two alphabets (H-903 lag-7 roughness).
Model: b(C_i) = b(C_{i-L}) + a(P_i)  or  b(C_i) = b(C_{i-L}) - a(P_i)  (a, b arbitrary permutations; the fed-back
ciphertext letter is valued by the same b with sign +1). NOT covered: b(C_i) = a(P_i) - b(C_{i-L}) (feedback sign -1). Then C_i == C_{i-L}  <=>  a(P_i) == 0  <=>  P_i == z
for ONE fixed letter z. So on crib positions i >= L the coincidence set must equal {i : P_i = z} for some z
(possibly empty). Exact, no search. Control: planted encryptions with random a, b must always pass; null rate from
random ciphertexts. Usage: it55_coincidence_lemma.py"""
import random, re
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
def passes(ct, L):
    pos = [i for i in CRIB if i >= L]
    if not pos: return True, 'vacuous'
    Z = {i for i in pos if ct[i] == ct[i - L]}
    for z in set(CRIB[i] for i in pos) | {None}:
        if Z == {i for i in pos if CRIB[i] == z}: return True, f'z={z} |Z|={len(Z)}'
    return False, f'Z={sorted(Z)}'
def encrypt(P, L, form, rng):
    a = list(range(26)); b = list(range(26)); rng.shuffle(a); rng.shuffle(b); binv = {v: x for x, v in enumerate(b)}
    c = [rng.randrange(26) for _ in range(L)]
    for i in range(L, len(P)):
        ap, bc = a[AZ.index(P[i])], b[c[i - L]]
        c.append(binv[(ap + bc) % 26 if form == 0 else ((bc - ap) % 26 if form == 1 else (ap - bc) % 26)])
    return ''.join(AZ[x] for x in c)
if __name__ == '__main__':
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper()); rng = random.Random(55)
    ok = n = 0
    for t in range(300):
        L = rng.randrange(1, 97); form = rng.randrange(2); o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97])
        for i, ch in CRIB.items(): P[i] = ch
        ok += passes(encrypt(P, L, form, rng), L)[0]; n += 1
    print(f'controls (planted, random a,b,L,form) pass {ok}/{n}')
    for L in range(1, 97):
        r, info = passes(K4, L)
        nul = sum(passes(''.join(rng.choice(AZ) for _ in range(97)), L)[0] for _ in range(2000)) / 2000
        print(f'L={L:2d}: {"PASS" if r else "dead"} {info}  null-pass {nul:.3f}')
