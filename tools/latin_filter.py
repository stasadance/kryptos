#!/usr/bin/env python3
"""Alphabet-free filter for any candidate key/mask letter stream X aligned to K4 (w-mask, T12).
Model: C_i = T[X_i](P_i) where T is ANY Latin-square tableau (each key letter gives a permutation,
and (P,C) determines the key letter uniquely) -- covers Vig/Beau/var-Beau/Quagmire I-IV with ANY
mixed alphabets, and any additive/XOR 'mask' over any relabelling (regular group action).
Necessary conditions from the 24 cribs:
  EQ : X28 == X66              (R->P at both positions)
  NE : X_i != X_j for the 22 crib pairs with same P & different C, or same C & different P.
For 'two-alphabet additive' (C=b^-1(a(P)+g(X)) any a,b,g) also g(X24)+g(X34)==g(X29)+g(X33).
Usage: python3 latin_filter.py STREAM [--scan]   ('?' = unknown letter; STREAM >= 74 chars)   (--scan: try every alignment offset of a long stream)"""
import sys
from itertools import combinations
CT="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
CRIBS={22:"EASTNORTHEAST",64:"BERLINCLOCK"}
PAIRS=[(s+k,ch,CT[s-1+k]) for s,w in CRIBS.items() for k,ch in enumerate(w)]
EQ=[(i,j) for (i,p,c),(j,q,d) in combinations(PAIRS,2) if p==q and c==d]
NE=[(i,j) for (i,p,c),(j,q,d) in combinations(PAIRS,2) if (p==q)!=(c==d)]
def check(X):  # X: dict pos->letter or string of len>=74 (1-indexed alignment X[0]=pos1)
    g=(lambda i:X[i-1]) if isinstance(X,str) else (lambda i:X.get(i))
    kn=lambda i,j: g(i) not in (None,'?') and g(j) not in (None,'?')   # '?' = unknown key letter
    bad=[("EQ",i,j) for i,j in EQ if kn(i,j) and g(i)!=g(j)]+[("NE",i,j) for i,j in NE if kn(i,j) and g(i)==g(j)]
    return bad
if __name__=="__main__":
    s="".join(ch for ch in sys.argv[1].upper() if ch.isalpha() or ch=="?")
    if "--scan" in sys.argv:
        ok=[o for o in range(len(s)-73) if not check(s[o:o+97])]
        print(f"{len(ok)} of {len(s)-73} alignments pass; offsets {ok[:40]}")
    else:
        b=check(s); print("PASS" if not b else f"FAIL {b[:6]}")
