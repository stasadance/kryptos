from core import *
import numpy as np, itertools
def blocks(n,o,alph):
    B=[]
    for s in range(o,97-n+1,n):
        idx=range(s,s+n)
        if all(i in PT for i in idx):
            B.append(([alph.index(PT[i]) for i in idx],[alph.index(CT[i]) for i in idx]))
    return B
def rowsols(B,n,affine):
    m=n+(1 if affine else 0)
    P=np.array([b[0]+([1] if affine else []) for b in B])  # (nb,m)
    # enumerate all rows in chunks
    total=26**m; cnt=np.zeros(n,dtype=np.int64)
    chunk=26**min(m,4)
    for start in range(0,total,chunk):
        ids=np.arange(start,min(total,start+chunk))
        R=np.stack([(ids//26**k)%26 for k in range(m)],1)  # (c,m)
        V=(R@P.T)%26  # (c,nb)
        for r in range(n):
            C=np.array([b[1][r] for b in B])
            cnt[r]+=np.all(V==C,axis=1).sum()
    return cnt
for alph,an in [(AZ,'AZ'),(KA,'KA')]:
  for n in [2,3,4]:
    for affine in [False,True]:
      if n==4 and affine: continue
      for o in range(n):
        B=blocks(n,o,alph)
        cnt=rowsols(B,n,affine)
        print(an,'n=%d'%n,'affine' if affine else 'linear','off',o,'blocks',len(B),'row-solutions',list(cnt),'DEAD' if 0 in cnt else 'ALIVE')
