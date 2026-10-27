from core import *
from z3 import *
import sys
def solve(p,typ,maxdrop=2,d=0,to=300000):
    s=Solver(); s.set("timeout",to)
    X={c:Int('x'+c) for c in AZ}
    for c in AZ: s.add(X[c]>=0,X[c]<26)
    s.add(Distinct(*X.values())); s.add(X['A']==0) if typ=='Q3V' else None
    K=[Int('k%d'%r) for r in range(p)]
    for k in K: s.add(k>=0,k<26)
    drops=[]
    for i in POS:
        ii = i if i<40 else i+d
        k=K[ii%p]; t=Int('t%d'%i); b=Bool('d%d'%i); drops.append(b)
        if typ=='Q3V': e=X[CT[i]]-X[PT[i]]-k
        elif typ=='Q3B': e=X[CT[i]]+X[PT[i]]-k
        elif typ=='Q2': e=X[CT[i]]-AZ.index(PT[i])-k
        elif typ=='Q2KA': e=X[CT[i]]-KA.index(PT[i])-k
        s.add(Or(b, e==26*t))
    s.add(Sum([If(b,1,0) for b in drops])<=maxdrop)
    r=s.check()
    return str(r)
if __name__=="__main__":
    for p in [7,10,21,42]:
        for typ in ['Q3V','Q3B','Q2','Q2KA']:
            res=[solve(p,typ,2,0), solve(p,typ,0,1), solve(p,typ,0,-1)]
            print(p,typ,'<=2subs:',res[0],' d=+1:',res[1],' d=-1:',res[2], flush=True)
