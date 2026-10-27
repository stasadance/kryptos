#!/usr/bin/env python3
"""Iteration 36 diagnostic: the stage-1 (one-step-from-crib windows) score of the TRUE alphabet vs the SA optimum."""
import sys, random, re, numpy as np
sys.argv=['x','/tmp/claude-0/it27/qg.bin','--none']; sys.path.insert(0,'iterations')
import it36_ptautokey_sa as M
eng = re.sub("[^A-Z]", "", open("/tmp/claude-0/it27/test.txt").read().upper())
for seed in range(3):
    rng=random.Random(100+seed); L,form,kr=8,0,seed%3
    st=rng.getstate(); ct,pt=M.plant(L,form,kr,rng,eng); rng.setstate(st); a=list(range(26)); rng.shuffle(a)
    A=np.array(a,dtype=np.int64); inv=np.empty(26,np.int64)
    for x in range(26): inv[A[x]]=x
    c=np.array([M.AZ.index(ch) for ch in ct],dtype=np.int64); p=np.empty(97,np.int64)
    tl=M.local(c,A,inv,L,form,kr,p,M.qg,10.0)
    best=None
    for r in range(4):
        np.random.seed(r); a0=np.random.permutation(26).astype(np.int64); iv=np.empty(26,np.int64)
        for x in range(26): iv[a0[x]]=x
        ba=M.anneal_stage(c,L,form,kr,M.qg,3000000,10.0,10.0,a0,iv,p,1)
        for x in range(26): iv[ba[x]]=x
        sc=M.local(c,ba,iv,L,form,kr,p,M.qg,10.0)
        dec="".join(M.AZ[x] if x>=0 else '.' for x in p)
        if best is None or sc[0]>best[0]: best=(sc[0],sc[1],dec, int((ba==A).sum()))
    print('truth local',round(tl[0],1),'found',round(best[0],1),'bad',best[1],'alph agree',best[3],best[2])
