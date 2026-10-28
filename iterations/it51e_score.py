#!/usr/bin/env python3
"""it51e stage 2a: rank akenum3 solutions by quadgram mean over the fully determined span 21..73.
English 53-letter spans average about -4.2/quadgram; random text about -6.
Usage: it51e_score.py QG.bin files..."""
import sys, numpy as np
qg = np.fromfile(sys.argv[1], dtype=np.float32)
def score(s):
    v = [qg[((ord(s[i])-65)*26+ord(s[i+1])-65)*26*26+(ord(s[i+2])-65)*26+ord(s[i+3])-65] for i in range(len(s)-3)
         if '.' not in s[i:i+4]]
    return sum(v)/len(v) if v else -99
for f in sys.argv[2:]:
    sols = [s for s in (l.split() for l in open(f)) if len(s) == 2 and len(s[1]) == 97]
    r = sorted(((score(pt[21:74]), pt) for _, pt in sols), reverse=True)
    print(f, len(sols), 'best:', *(f'{s:.2f} {p[21:74]}' for s, p in r[:3]))
