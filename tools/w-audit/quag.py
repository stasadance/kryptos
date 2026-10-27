from core import *
from gen import testable
from z3 import *
import sys
def solve(p, typ, pos=None, timeout=60000):
    pos = pos if pos is not None else POS
    s=Solver(); s.set("timeout",timeout)
    letters=sorted(set(PT[i] for i in pos)|set(CT[i] for i in pos))
    X={c:Int('x'+c) for c in letters}   # cipher-side / shared alphabet
    Y={c:Int('y'+c) for c in letters}   # plain-side
    for c in letters:
        s.add(X[c]>=0,X[c]<26,Y[c]>=0,Y[c]<26)
    s.add(Distinct(*X.values())); s.add(Distinct(*Y.values()))
    K={}
    for i in pos:
        r=i%p
        if r not in K: K[r]=Int('k%d'%r); s.add(K[r]>=0,K[r]<26)
        P,C=PT[i],CT[i]
        if typ=='Q3V': lhs,rhs=X[C],X[P]+K[r]
        elif typ=='Q3B': lhs,rhs=X[C]+X[P],K[r]
        elif typ=='Q1': lhs,rhs=AZ.index(C),Y[P]+K[r]          # keyed plain, straight cipher
        elif typ=='Q2': lhs,rhs=X[C],AZ.index(P)+K[r]          # straight plain, keyed cipher
        elif typ=='Q1KA': lhs,rhs=KA.index(C),Y[P]+K[r]
        elif typ=='Q2KA': lhs,rhs=X[C],KA.index(P)+K[r]
        elif typ=='Q4': lhs,rhs=X[C],Y[P]+K[r]
        t=Int('t%d'%i); s.add(t>=-1,t<=2); s.add(lhs==rhs-26*t)
    # symmetry break: fix one value
    if typ in('Q3V','Q4','Q2'): s.add(X[letters[0]]==0) if typ!='Q2' else None
    r=s.check(); return str(r)
if __name__=="__main__":
    typ=sys.argv[1]
    dead=[];unk=[];alive=[]
    for p in range(1,53):
        if not testable(p): continue
        r=solve(p,typ)
        (dead if r=='unsat' else alive if r=='sat' else unk).append(p)
    print(typ,"UNSAT:",dead); print(typ,"SAT:",alive); print(typ,"UNKNOWN:",unk)
