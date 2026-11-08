import sys, random
sys.path.insert(0,'/home/user/kryptos/tools')
from errtol import QModel, CT, CRIB, AZ
from z3 import sat, unsat
pairs=[(k-1,CRIB[k],CT[k-1]) for k in sorted(CRIB)]
# vacuous periods
for p in range(20,60):
    cls={}
    for k,_,_ in pairs: cls.setdefault(k%p,0); cls[k%p]+=1
    if max(cls.values())<2: print('vacuous',p)
for p in (46,47,48,49,50,51):
    for st in 'VB':
        r=QModel(pairs,p,'Q3',st,timeout_ms=600000).check()
        print('K4 Q3',st,p,r,flush=True)
# plants at 48, 50 Beau: random alphabet, random shifts, random PT
rng=random.Random(7)
for p in (48,50):
    for t in range(3):
        a=list(range(26)); rng.shuffle(a); A=dict(zip(AZ,a)); inv={v:k for k,v in A.items()}
        s=[rng.randrange(26) for _ in range(p)]
        pp=[(k,pl,inv[(s[k%p]-A[pl])%26]) for k,pl,_ in pairs]
        print('plant B',p,t,QModel(pp,p,'Q3','B').check(),flush=True)
