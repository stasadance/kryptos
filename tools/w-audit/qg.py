from core import *
from vig import ks
import numpy as np,re,glob
txt=''.join(re.sub('[^A-Z]','',open(f,errors='ignore').read().upper()) for f in glob.glob('../dl/g*.txt'))
a=np.frombuffer(txt.encode(),dtype=np.uint8).astype(np.int64)-65
idx=((a[:-3]*26+a[1:-2])*26+a[2:-1])*26+a[3:]
cnt=np.bincount(idx,minlength=26**4).astype(float)+0.5
lq=np.log10(cnt/cnt.sum())
def score(s):  # mean quadgram logprob over fragments
    v=[];
    for frag in s:
        x=[AZ.index(c) for c in frag]
        for j in range(len(x)-3): v.append(lq[((x[j]*26+x[j+1])*26+x[j+2])*26+x[j+3]])
    return np.mean(v)
rng=np.random.default_rng(3)
N=len(a)-200; E=[];U=[]
for _ in range(20000):
    o=rng.integers(0,N); fr=txt[o:o+97]
    E.append(score([fr[21:34],fr[63:74]]))
    U.append(score([''.join(rng.choice(list(AZ),13)),''.join(rng.choice(list(AZ),11))]))
E=np.array(E);U=np.array(U)
print("English mean %.2f sd %.2f min %.2f; uniform mean %.2f sd %.2f"%(E.mean(),E.std(),E.min(),U.mean(),U.std()))
for PA,pn in [(AZ,'AZ'),(KA,'KA')]:
  for CA,cn in [(AZ,'AZ'),(KA,'KA')]:
    for m in 'VBv':
      d=ks(PA,CA,m)
      for KAl,kn in ([(PA,'kPA'),(CA,'kCA')] if PA!=CA else [(PA,'k')]):
        s=''.join(KAl[d[i]] for i in POS); sc=score([s[:13],s[13:]])
        print("%-10s %s %.2f  P(Eng<=)=%.5f"%(pn+cn+m+kn,s,sc,(E<=sc).mean()))
