"""CP-SAT gives a crib-consistent alphabet (random objective for diversity); annealer starts there."""
import random,subprocess,sys,json
from ortools.sat.python import cp_model
CR={22:"EASTNORTHEAST",64:"BERLINCLOCK"}; PAIRS=[(s-1+j,p) for s,w in CR.items() for j,p in enumerate(w)]
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def cpsat_alpha(ct,w,o,seed):
    M=cp_model.CpModel(); rng=random.Random(seed)
    A={L:M.NewIntVar(0,25,"a"+L) for L in AZ}; M.AddAllDifferent(list(A.values()))
    F={r:M.NewIntVar(0,25,f"f{r}") for r in {(i+o)//w for i,_ in PAIRS}}; G={c:M.NewIntVar(0,25,f"g{c}") for c in {(i+o)%w for i,_ in PAIRS}}
    for n,(i,p) in enumerate(PAIRS):
        t=M.NewIntVar(-4,4,f"t{n}"); M.Add(A[ct[i]]-A[p]-F[(i+o)//w]-G[(i+o)%w]==26*t)
    M.Maximize(sum(rng.randrange(-50,50)*A[L] for L in AZ))
    S=cp_model.CpSolver(); S.parameters.max_time_in_seconds=5; S.parameters.random_seed=seed; S.parameters.num_workers=1
    r=S.Solve(M)
    if r not in (cp_model.OPTIMAL,cp_model.FEASIBLE): return None
    val={L:S.Value(A[L]) for L in AZ}; inv=[None]*26
    for L,v in val.items(): inv[v]=L
    # sa2u's A maps letter index -> value ; pass as string where position x holds chr(65+A[x])
    return "".join(chr(65+val[L]) for L in AZ)
def solve(ct,w,o,restarts,it,seed0,T0="8"):
    best=(-1e9,"")
    for r in range(restarts):
        a=cpsat_alpha(ct,w,o,seed0+r)
        if a is None: continue
        out=subprocess.run(['./sa2u',str(w),str(o),ct,'1',str(it),str(seed0+r),'25',a,T0],capture_output=True,text=True).stdout.split()
        if out and float(out[0])>best[0]: best=(float(out[0]),out[1])
    return best
