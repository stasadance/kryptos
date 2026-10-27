from core import *
from vig import ks
import itertools
combos=[(PA,CA,m,pn+cn+m) for (PA,pn) in [(AZ,'AZ'),(KA,'KA')] for (CA,cn) in [(AZ,'AZ'),(KA,'KA')] for m in 'VB']
# CT autokey: key letter k_i = idx_KEYALPH(C_{i-L}); key alphabet: use PA index (key letter located in plain alphabet row header) -> try both PA and CA indexing
surv=[]
for PA,CA,m,name in combos:
    d=ks(PA,CA,m)
    for KAlph,kn in [(PA,'kPA'),(CA,'kCA')]:
        for L in range(1,97):
            ok=True;checked=0
            for i in POS:
                if i-L<0: continue
                checked+=1
                if d[i]!=KAlph.index(CT[i-L]): ok=False;break
            if ok and checked>0: surv.append((name,kn,L,checked))
print("CT-autokey survivors with >=1 check:",surv)
# PT autokey: k_i = idx(P_{i-L}); only check where i-L in POS
surv2=[];nochk=set(range(1,97))
for PA,CA,m,name in combos:
    d=ks(PA,CA,m)
    for KAlph,kn in [(PA,'kPA'),(CA,'kCA')]:
        for L in range(1,97):
            ok=True;checked=0
            for i in POS:
                if (i-L) in PT:
                    checked+=1
                    if d[i]!=KAlph.index(PT[i-L]): ok=False;break
            if checked==0: continue
            nochk.discard(L)
            if ok: surv2.append((name,kn,L,checked))
print("PT-autokey survivors with checks:",surv2)
print("PT-autokey L with no direct check:",sorted(nochk))
