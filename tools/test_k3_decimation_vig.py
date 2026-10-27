#!/usr/bin/env python3
"""w-history H-205 test: K4 = affine/decimation transposition (K3-style: a*(i+1) mod 98, or a*i+b mod 97)
combined with K1/K2-style periodic Vigenere/Beaufort/var-Beaufort (KA or AZ alphabet), period 1-12,
substitution before or after transposition. Result 2026-10-26: 0 hits of 1,346,976 configs.
Sanity: detects a planted synthetic case (m98 a=5, ABSCISSA, KA)."""
# H: K4 = K3-style decimation transposition combined with K1/K2-style tableau substitution (period<=12)
from kryptos_k123 import KA
from math import gcd
CT=open('/mnt/project-files/k4/facts/ciphertext.txt').read().strip(); n=97
AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
crib={}
for s,w in {22:'EASTNORTHEAST',64:'BERLINCLOCK'}.items():
    for i,c in enumerate(w): crib[s-1+i]=c
def maps():
    for a in range(1,98):
        if gcd(a,98)==1: yield ('m98',a,0),[ (a*(i+1))%98-1 for i in range(n)]
    for a in range(1,97):
        for b in range(97): yield ('m97',a,b),[(a*i+b)%97 for i in range(n)]
hits=[]
cnt=0
for tag,sig in maps():   # sig[i] = CT index holding PT/intermediate position i
    inv={v:k for k,v in enumerate(sig)}
    for al in (KA,AZ):
      for mode in (0,1,2):
        f=[lambda c,p:(c-p)%26, lambda c,p:(c+p)%26, lambda c,p:(p-c)%26][mode]
        # order A: substitution on PT index p, CT char at sig[p]
        A={p:f(al.index(CT[sig[p]]),al.index(c)) for p,c in crib.items()}
        # order B: transposition first, substitution indexed by CT position m=sig[p]
        B={sig[p]:f(al.index(CT[sig[p]]),al.index(c)) for p,c in crib.items()}
        for name,ks in (('A',A),('B',B)):
          for P in range(1,13):
            cnt+=1
            d={}
            ok=True
            for k,v in ks.items():
                if d.setdefault(k%P,v)!=v: ok=False;break
            if ok: hits.append((tag,al[:3],mode,name,P))
print('configs tested',cnt,'hits',len(hits)); print(hits[:20])
