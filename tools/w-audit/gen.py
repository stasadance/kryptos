from core import *
from itertools import combinations
def conflicts(p, pos=POS, shift=None):
    # returns list of conflicting pairs (i,j) under period p, arbitrary per-residue bijection
    out=[]
    for i,j in combinations(pos,2):
        if (i-j)%p==0:
            a=(PT[i]==PT[j]); b=(CT[i]==CT[j])
            if a!=b: out.append((i+1,j+1))
    return out
def testable(p):
    return any((i-j)%p==0 for i,j in combinations(POS,2))
dead=[p for p in range(1,97) if conflicts(p)]
alive=[p for p in range(1,97) if testable(p) and not conflicts(p)]
vac=[p for p in range(1,97) if not testable(p)]
print("GEN dead:",dead); print("GEN alive testable:",alive); print("vacuous:",vac[:10],'...')
for p in [7,10,25,50]: print(p,conflicts(p))
