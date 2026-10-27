from core import *
from itertools import combinations
def conf(p,d):
    pos=[(i if i<40 else i+d, PT[i], CT[i], i) for i in POS]
    out=[]
    for a,b in combinations(pos,2):
        if (a[0]-b[0])%p==0 and ((a[1]==b[1])!=(a[2]==b[2])): out.append((a[3]+1,b[3]+1))
    return out
def minhit(c):
    ps=sorted(set(x for pr in c for x in pr))
    for r in range(0,6):
        for S in combinations(ps,r):
            if all(a in S or b in S for a,b in c): return r,S
    return 99,None
for p in [7,10,21,25,42,50]:
    for d in [0,-1,1,-2,2]:
        c=conf(p,d); print(p,d,len(c),minhit(c))
