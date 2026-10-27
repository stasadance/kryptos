from core import *
from z3 import *
import sys
def base(m,beau):
    s=Solver(); s.set("timeout",300000)
    X={c:Int('x'+c) for c in AZ}
    for c in AZ: s.add(X[c]>=0,X[c]<26)
    s.add(Distinct(*X.values()))
    for i in POS:
        k=Int('k%d'%i); t=Int('t%d'%i); s.add(k>=0,k<m)
        e = X[CT[i]]-X[PT[i]]-k if not beau else X[CT[i]]+X[PT[i]]-k
        s.add(e==26*t)
    return s.check()
def ctauto(L,beau):
    s=Solver(); s.set("timeout",300000)
    X={c:Int('x'+c) for c in AZ}
    for c in AZ: s.add(X[c]>=0,X[c]<26)
    s.add(Distinct(*X.values()))
    for i in POS:
        if i-L<0: continue
        t=Int('t%d'%i); k=X[CT[i-L]]
        e = X[CT[i]]-X[PT[i]]-k if not beau else X[CT[i]]+X[PT[i]]-k
        s.add(e==26*t)
    return s.check()
if __name__=="__main__":
    if sys.argv[1]=='base':
        for m in [3,4,5,6]: print('base',m,'Vig',base(m,False),'Beau',base(m,True),flush=True)
    else:
        for L in [1,7,20,31,32,36,37,40]:
            print('ctauto L',L,'Vig',ctauto(L,False),'Beau',ctauto(L,True),flush=True)
