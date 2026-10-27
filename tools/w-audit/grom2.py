from core import *
from grom import key, consistent
import itertools
def fixed_ok(k, PA=None, CA=None, same=False):
    # PA fixed: y(L)=PA.index(L); CA fixed: x(L)=CA.index(L); same: x==y arbitrary
    if PA and CA:
        return all((CA.index(CT[i])-PA.index(PT[i]))%26==k[i]%26 for i in POS)
    if PA:  # x(C) = PA(P)+k: each C letter must get unique value, injective
        x={}
        for i in POS:
            v=(PA.index(PT[i])+k[i])%26
            if x.setdefault(CT[i],v)!=v: return False
        return len(set(x.values()))==len(x)
    if CA:
        y={}
        for i in POS:
            v=(CA.index(CT[i])-k[i])%26
            if y.setdefault(PT[i],v)!=v: return False
        return len(set(y.values()))==len(y)
    if same:
        from z3 import Solver,Int,Distinct,sat
        s=Solver(); L=sorted(set(PT.values())|set(CT[i] for i in POS)); X={c:Int(c) for c in L}
        for c in L: s.add(X[c]>=0,X[c]<26)
        s.add(Distinct(*X.values()))
        for i in POS:
            t=Int('t%d'%i); s.add(t>=-1,t<=1, X[CT[i]]==X[PT[i]]+k[i]-26*t)
        return s.check()==sat
alphs={'AZ':AZ,'ZA':AZ[::-1],'KA':KA,'AK':KA[::-1]}
tot=0
for b,L in [(10,5),(10,4),(8,5),(10,6),(10,3),(6,6),(7,6),(9,5)]:
    good=[pr for pr in itertools.product(range(b),repeat=L) if consistent(key(pr,b))]
    hits=[]
    for pr in good:
        k=key(pr,b)
        for an,A in alphs.items():
            if fixed_ok(k,PA=A): hits.append((pr,'PA='+an))
            if fixed_ok(k,CA=A): hits.append((pr,'CA='+an))
        if b<=10 and L<=5 and fixed_ok(k,same=True): hits.append((pr,'same'))
    print(b,L,'arb-consistent',len(good),'fixed/same hits',hits)
for b in [2,3,4,5]:
    print('base',b,[ (L,sum(consistent(key(pr,b)) for pr in itertools.product(range(b),repeat=L))) for L in range(2,7)])
