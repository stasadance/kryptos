from core import *
from gen import testable
# tableau: plain alphabet PA, cipher alphabet CA. Vig: CA.idx(C)=PA.idx(P)+k ; Beau: CA.idx(C)= k - PA.idx(P); vBeau: CA.idx(C)=PA.idx(P)-k
def ks(PA,CA,mode):
    d={}
    for i in POS:
        p=PA.index(PT[i]); c=CA.index(CT[i])
        d[i]= (c-p)%26 if mode=='V' else (c+p)%26 if mode=='B' else (p-c)%26
    return d
def ok(d,p):
    seen={}
    for i,k in d.items():
        r=i%p
        if r in seen and seen[r]!=k: return False
        seen[r]=k
    return True
res={}
for PA,pn in [(AZ,'AZ'),(KA,'KA')]:
  for CA,cn in [(AZ,'AZ'),(KA,'KA')]:
    for m in 'VBv':
      d=ks(PA,CA,m)
      alive=[p for p in range(1,97) if testable(p) and ok(d,p)]
      res[(pn,cn,m)]=alive
      print(pn,cn,m,"alive testable periods:",alive)
d=ks(AZ,AZ,'V'); print(''.join(AZ[d[i]] for i in POS))
d=ks(KA,KA,'V'); print(''.join(KA[d[i]] for i in POS))
d=ks(AZ,AZ,'B'); print(''.join(AZ[d[i]] for i in POS))
