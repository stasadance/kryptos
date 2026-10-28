#!/usr/bin/env python3
"""it56: autokey under an ARBITRARY Latin-square tableau (any 26x26 Latin square, i.e. any key-letter-indexed family
of alphabets with Latin property; covers Vig/Beau/Var/Quagmire I-IV with any alphabets and any key relabelling).
CT-autokey: C_i = T[C_{i-L}][P_i];  PT-autokey: C_i = T[P_{i-L}][P_i].
Every crib position with known row letter gives a triple (row, col=P_i, val=C_i). A Latin square needs
(row,col)->val, (row,val)->col and (col,val)->row all to be functions. Violation = exact refutation for every
Latin tableau. (Necessary conditions only: passing does not prove completability.)
Control: planted encryptions under random Latin squares must pass. Null: random ciphertexts.
Usage: it56_latin_autokey.py"""
import random, re
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
def triples(ct, L, kind):
    out = []
    for i, p in CRIB.items():
        if i - L < 0: continue
        r = ct[i - L] if kind == 'CT' else CRIB.get(i - L)
        if r is None: continue
        out.append((r, p, ct[i], i))
    return out
def consistent(tr):
    for f in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
        d = {}
        for t in tr:
            k = (t[f[0]], t[f[1]])
            if d.setdefault(k, t[f[2]]) != t[f[2]]: return False
    return True
def rand_latin(rng):
    # random Latin square via random row/col/symbol permutations of the cyclic square (enough for a control)
    r = list(range(26)); c = list(range(26)); s = list(range(26)); rng.shuffle(r); rng.shuffle(c); rng.shuffle(s)
    return [[s[(r[i] + c[j]) % 26] for j in range(26)] for i in range(26)]
def plant(rng, eng, L, kind):
    T = rand_latin(rng); o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97])
    for i, ch in CRIB.items(): P[i] = ch
    C = [rng.randrange(26) for _ in range(L)]
    for i in range(L, 97):
        row = C[i - L] if kind == 'CT' else AZ.index(P[i - L]); C.append(T[row][AZ.index(P[i])])
    return ''.join(AZ[x] for x in C)
if __name__ == '__main__':
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper()); rng = random.Random(56)
    for kind in ('CT', 'PT'):
        ok = sum(consistent(triples(plant(rng, eng, L, kind), L, kind)) for L in range(1, 97) for _ in range(3))
        print(f'{kind} controls pass {ok}/{96*3}')
        dead = []
        for L in range(1, 97):
            tr = triples(K4, L, kind)
            if not tr: continue
            r = consistent(tr)
            nul = sum(consistent(triples(''.join(rng.choice(AZ) for _ in range(97)), L, kind)) for _ in range(1000)) / 1000
            if not r: dead.append(L)
            print(f'{kind} L={L:2d}: {"PASS" if r else "DEAD"} triples={len(tr)} null-pass={nul:.3f}')
        print(f'{kind} dead lags: {dead}')
