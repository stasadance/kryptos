from core import *
from vig import ks
import numpy as np
F=np.array([8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.153,0.772,4.025,2.406,6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.758,0.978,2.360,0.150,1.974,0.074]);F/=F.sum()
LL=np.log(F*26)
rng=np.random.default_rng(2)
null=LL[rng.choice(26,size=(200000,24),p=F)].sum(1)
unif=LL[rng.integers(0,26,size=(200000,24))].sum(1)
print("English-key null mean %.2f sd %.2f; uniform-key mean %.2f sd %.2f"%(null.mean(),null.std(),unif.mean(),unif.std()))
rows=[]
for PA,pn in [(AZ,'AZ'),(KA,'KA')]:
  for CA,cn in [(AZ,'AZ'),(KA,'KA')]:
    for m in 'VBv':
      d=ks(PA,CA,m)
      for KAl,kn in ([(PA,'kPA'),(CA,'kCA')] if PA!=CA else [(PA,'k')]):
        s=''.join(KAl[d[i]] for i in POS)
        sc=sum(LL[AZ.index(c)] for c in s)
        rows.append((sc,pn+cn+m+kn,s,(null<=sc).mean()))
for r in sorted(rows,reverse=True): print("%.2f %-10s %s P(English<=)=%.4f"%r)
print("n tests",len(rows),"best P*ntests",min(r[3] for r in rows)*len(rows) if False else max(r[3] for r in rows)*len(rows))
