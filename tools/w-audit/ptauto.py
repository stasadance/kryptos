from core import *
combos=[(PA,CA,m,pn+cn+m) for (PA,pn) in [(AZ,'AZ'),(KA,'KA')] for (CA,cn) in [(AZ,'AZ'),(KA,'KA')] for m in 'VB']
def enc_key(PA,CA,m,KA_,p,c):  # key letter given plain p, cipher c
    pi=PA.index(p); ci=CA.index(c)
    k=(ci-pi)%26 if m=='V' else (ci+pi)%26
    return KA_[k]
def dec(PA,CA,m,KA_,k,c):
    ki=KA_.index(k); ci=CA.index(c)
    return PA[(ci-ki)%26] if m=='V' else PA[(ki-ci)%26]
res={}
for PA,CA,m,name in combos:
  for KA_,kn in [(PA,'kPA'),(CA,'kCA')]:
    for L in range(1,97):
        P=dict(PT); conflict=False; changed=True
        while changed and not conflict:
            changed=False
            for i in list(P):
                # forward: P_{i+L} from key P_i
                j=i+L
                if j<97:
                    v=dec(PA,CA,m,KA_,P[i],CT[j])
                    if j in P:
                        if P[j]!=v: conflict=True;break
                    else: P[j]=v;changed=True
                j=i-L
                if j>=0:
                    v=enc_key(PA,CA,m,KA_,P[i],CT[i])
                    if j in P:
                        if P[j]!=v: conflict=True;break
                    else: P[j]=v;changed=True
        if not conflict:
            res.setdefault(L,[]).append((name+kn,len(P)-24,''.join(P.get(i,'.') for i in range(97))))
print("L surviving (no conflict) in some combo:",sorted(res))
for L in sorted(res):
    if L<53:
        for r in res[L][:16]: print(L,r)
