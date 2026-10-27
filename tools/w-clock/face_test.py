#!/usr/bin/env python3
"""H-501/H-801 single test: one keyed alphabet per Weltzeituhr face (period 24).
Input: text file with exactly 24 lines, face 0..23 in clock order (e.g. UTC-11..UTC+12),
each line = the face's keyword (e.g. city names concatenated in engraving order, no spaces).
For each alignment s (K4 pos i, 0-based, uses face (i+s) mod 24), both directions (+1/-1 around the clock),
keyed-alphabet fill (AZ or KA) and models S1-S4, counts satisfied crib pairs (24 total).
Random alphabets satisfy ~24/26 ~ 1 pair; a true hit satisfies all 24 -> then decrypt & run crib_check.py.
Usage: python3 face_test.py faces.txt"""
import sys; sys.path.insert(0,'/mnt/project-files/k4/tools')
from keystream_check import CT, crib_pairs, AZ, KA
def keyed(w, base):
    s=[]
    for ch in w.upper()+base:
        if ch.isalpha() and ch not in s: s.append(ch)
    return ''.join(s)
M={'S1 C=K[AZ(P)]':(lambda K,p:K[AZ.index(p)], lambda K,c:AZ[K.index(c)]),
   'S2 C=AZ[K(P)]':(lambda K,p:AZ[K.index(p)], lambda K,c:K[AZ.index(c)]),
   'S3 C=K[KA(P)]':(lambda K,p:K[KA.index(p)], lambda K,c:KA[K.index(c)]),
   'S4 C=KA[K(P)]':(lambda K,p:KA[K.index(p)], lambda K,c:K[KA.index(c)])}
faces=[l.strip() for l in open(sys.argv[1]) if l.strip()]
assert len(faces)==24, len(faces)
best=[]
for bn,base in (('AZ',AZ),('KA',KA)):
  alph=[keyed(f,base) for f in faces]
  for d in (1,-1):
    for s in range(24):
      for mn,(enc,dec) in M.items():
        sc=sum(enc(alph[(d*i+s)%24],p)==c for i,p,c in crib_pairs())
        best.append((sc,bn,d,s,mn))
best.sort(reverse=True)
for b in best[:10]: print(b)
sc,bn,d,s,mn=best[0]
if sc==24:
    base=AZ if bn=='AZ' else KA; alph=[keyed(f,base) for f in faces]
    pt=''.join(M[mn][1](alph[(d*i+s)%24],c) for i,c in enumerate(CT)); print('DECRYPT',pt)
