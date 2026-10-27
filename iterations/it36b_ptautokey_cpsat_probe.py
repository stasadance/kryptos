#!/usr/bin/env python3
"""Iteration 36 probe: CP-SAT model of PT-autokey under one unknown alphabet (alphabet + plaintext letter vars, AddElement
links, crib-fixed letters); (1) solution enumeration, (2) bigram-score maximisation. Neither recovers planted keys in
120-300 s (see JOURNAL it36). Run from repo root; needs /tmp/claude-0/it27/{qg.bin,test.txt}."""
import sys, random, re, numpy as np, time
from ortools.sat.python import cp_model
sys.argv=['x','/tmp/claude-0/it27/qg.bin','--none']; sys.path.insert(0,'iterations')
import it36_ptautokey_sa as M
eng = re.sub("[^A-Z]", "", open("/tmp/claude-0/it27/test.txt").read().upper())
AZ=M.AZ
def model(ct,L,form,kr):
    m=cp_model.CpModel(); a=[m.NewIntVar(0,25,f"a{x}") for x in range(26)]; m.AddAllDifferent(a)
    p=[m.NewIntVar(0,25,f"p{i}") for i in range(97)]; av=[m.NewIntVar(0,25,f"v{i}") for i in range(97)]
    for t,ch in enumerate("EASTNORTHEAST"): m.Add(p[21+t]==AZ.index(ch))
    for t,ch in enumerate("BERLINCLOCK"): m.Add(p[63+t]==AZ.index(ch))
    for i in range(97): m.AddElement(p[i],a,av[i])
    # inverse consistency: p determined by av (a is a bijection) -> AllDifferent on a suffices
    for i in range(L,97):
        if kr==0: K=av[i-L]
        elif kr==1: K=p[i-L]
        else:
            K=m.NewIntVar(0,25,f"k{i}"); m.AddElement(p[i-L],[int(x) for x in M.KAI],K)
        q=m.NewIntVar(-3,3,f"q{i}"); ac=a[AZ.index(ct[i])]
        if form==0: m.Add(ac==av[i]+K+26*q)
        elif form==1: m.Add(ac==K-av[i]+26*q)
        else: m.Add(ac==av[i]-K+26*q)
    return m,a,p
rng=random.Random(36)
for L,form,kr in ():
    ct,pt=M.plant(L,form,kr,rng,eng)
    m,a,p=model(ct,L,form,kr)
    sols=[]
    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            sols.append("".join(AZ[self.Value(x)] for x in p))
            if len(sols)>=20000: self.StopSearch()
    s=cp_model.CpSolver(); s.parameters.enumerate_all_solutions=True; s.parameters.max_time_in_seconds=120
    t=time.time(); st=s.Solve(m,CB())
    print(L,form,kr,'status',s.StatusName(st),'solutions',len(sols),'distinct pt',len(set(sols)),'truth in',pt in set(sols),round(time.time()-t),flush=True)

# ---- bigram-optimising CP-SAT
cnt=np.zeros((26,26))
x=np.frombuffer(eng.encode(),dtype=np.uint8)-65
np.add.at(cnt,(x[:-1],x[1:]),1); lp=np.log10((cnt+0.5)/cnt.sum(1,keepdims=True)); BG=[int(round(v*100)) for v in lp.flatten()]
rng=random.Random(7)
for L,form,kr in ((8,0,0),(10,1,1),(7,2,2),(12,0,1)):
    ct,pt=M.plant(L,form,kr,rng,eng)
    m,a,p=model(ct,L,form,kr)
    terms=[]
    for i in range(96):
        idx=m.NewIntVar(0,675,f"i{i}"); m.Add(idx==26*p[i]+p[i+1]); v=m.NewIntVar(min(BG),max(BG),f"b{i}"); m.AddElement(idx,BG,v); terms.append(v)
    m.Maximize(sum(terms))
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=300; s.parameters.num_workers=4
    t=time.time(); st=s.Solve(m); dec="".join(AZ[s.Value(x)] for x in p)
    tv=sum(BG[26*AZ.index(pt[i])+AZ.index(pt[i+1])] for i in range(96))
    print(L,form,kr,s.StatusName(st),'obj',s.ObjectiveValue(),'truth obj',tv,'acc',sum(u==w for u,w in zip(dec,pt)),dec,round(time.time()-t),flush=True)
