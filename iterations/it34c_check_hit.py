import sys, numpy as np
sys.path.insert(0,'/mnt/project-files/k4/workers/w-transkey/scripts')
import transkey as TK
from keygen import keyed
from ortools.sat.python import cp_model
AZ=TK.AZ; KA=TK.KA; CT=TK.CT0
alph=keyed("LAYERTWO",KA); n=97; d,b=65,74
S=TK.periodic_stream(alph,0,n)
key=[S[(d*i+b)%n] for i in range(97)]
kl="".join(AZ[x] for x in key); print("key letters",kl)
kv=[(AZ.index(AZ[x])+1)%26 for x in key]  # AZ1 numbering
c=TK.Ctx(CT); pairs=c.pairs
print("dropped row", pairs[2])
def solve(extra=None, limit=50):
    m=cp_model.CpModel(); a={L:m.NewIntVar(0,25,L) for L in AZ}; m.AddAllDifferent(list(a.values()))
    for t,(i,p,cc) in enumerate(pairs):
        if t==2: continue
        q=m.NewIntVar(-3,3,f"q{t}"); m.Add(a[cc]+a[p]==kv[i-1]+26*q)
    m.Add(a['A']==0) if False else None
    s=cp_model.CpSolver(); s.parameters.enumerate_all_solutions=True; s.parameters.max_time_in_seconds=60
    sols=[]
    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            sols.append({L:self.Value(a[L]) for L in AZ})
            if len(sols)>=limit: self.StopSearch()
    s.Solve(m,CB()); return sols
sols=solve(limit=2000); print("solutions",len(sols))
from collections import Counter
for so in sols[:5]:
    inv={v:k for k,v in so.items()}
    print("".join(inv[(kv[i]-so[CT[i]])%26] for i in range(97)))
qg=np.fromfile('/tmp/claude-0/it27/qg.bin',dtype=np.float32)
def score(t):
    x=np.array([ord(ch)-65 for ch in t]); i=((x[:-3]*26+x[1:-2])*26+x[2:-1])*26+x[3:]; return float(qg[i].sum())
res=[]
for so in sols:
    inv={v:k for k,v in so.items()}; t="".join(inv[(kv[i]-so[CT[i]])%26] for i in range(97)); res.append((score(t),t))
res.sort(reverse=True); print(len(res)); [print(round(s,1),t) for s,t in res[:3]]
