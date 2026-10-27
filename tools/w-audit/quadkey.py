from core import *
from z3 import *
for deg in [1,2]:
  for mod_ in ['two','one']:
    s=Solver(); s.set("timeout",600000)
    X={c:Int('x'+c) for c in AZ}; Y={c:Int('y'+c) for c in AZ} if mod_=='two' else X
    for c in AZ: s.add(X[c]>=0,X[c]<26,Y[c]>=0,Y[c]<26)
    s.add(Distinct(*X.values())); 
    if mod_=='two': s.add(Distinct(*Y.values()))
    a,b,c0=Ints('a b c')
    for v in (a,b,c0): s.add(v>=0,v<26)
    if deg==1: s.add(b==0)
    # exclude period<=2 keys: require a,b not both in {0,13}
    s.add(Not(And(Or(a==0,a==13),Or(b==0,b==13))))
    for i in POS:
        n=i+1
        t=Int('t%d'%i)
        s.add(X[CT[i]]-Y[PT[i]]-(a*n+b*n*n+c0)==26*t)
    print('deg',deg,mod_,'alphabet(s), key not period<=2:',s.check(),flush=True)
