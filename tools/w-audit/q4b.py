from core import *
from z3 import *
import sys
# alternative encoding: one-hot-free, BitVec-free; use explicit Q4 with key as differences, no symmetry break, Beau variant too
def q4(p,beau=False,to=600000):
    s=Solver(); s.set("timeout",to)
    X={c:Int('x'+c) for c in AZ}; Y={c:Int('y'+c) for c in AZ}
    for c in AZ: s.add(X[c]>=0,X[c]<26,Y[c]>=0,Y[c]<26)
    s.add(Distinct(*X.values()),Distinct(*Y.values()))
    K=[Int('k%d'%r) for r in range(p)]
    for i in POS:
        k=K[i%p]
        e = (X[CT[i]] - Y[PT[i]] - k) if not beau else (X[CT[i]] + Y[PT[i]] - k)
        t=Int('t%d'%i); s.add(e==26*t)
    for k in K: s.add(k>=0,k<26)
    return s.check()
if __name__=="__main__":
    for p in map(int,sys.argv[1:]):
        print(p, q4(p), q4(p,True))
