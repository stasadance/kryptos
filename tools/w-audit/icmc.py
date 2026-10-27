from core import *
import numpy as np
F=np.array([8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.153,0.772,4.025,2.406,6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.758,0.978,2.360,0.150,1.974,0.074]);F/=F.sum()
def pooled(arr,p):
    # arr: (...,97) ints; pooled column IC = sum pairs same / total pairs within columns
    num=0;den=0
    for r in range(p):
        col=arr[...,r::p]; n=col.shape[-1]
        cnt=np.stack([(col==a).sum(-1) for a in range(26)],-1)
        num=num+(cnt*(cnt-1)).sum(-1); den+=n*(n-1)
    return num/den
x=np.array([AZ.index(c) for c in CT])
rng=np.random.default_rng(1)
N=200000
sims=rng.choice(26,size=(N,97),p=F)
# force crib letters into plaintext sims (they are known plaintext)
for i in POS: sims[:,i]=AZ.index(PT[i])
for p in [1,2,3,4,5,6,8,9,12,13,18,23,26]:
    o=pooled(x,p); s=pooled(sims,p)
    print(p, round(float(o),4), "null mean %.4f"%s.mean(), "P(<=obs)=%.2e"%((s<=o).mean()))
