import random,json,sys
from multiprocessing import Pool
from hybrid import solve
TEST=open('/tmp/claude-0/-home-user-kryptos/046a83fd-aa4b-57f6-97e0-639b3d9e1ef4/scratchpad/it05/test.txt').read()
CR={21:"EASTNORTHEAST",63:"BERLINCLOCK"}; CP={s+j for s,w in CR.items() for j in range(len(w))}; NC=[i for i in range(97) if i not in CP]
import numpy as np
QG=np.fromfile('qg.bin',dtype=np.float32)
def qs(t):
    a=[ord(c)-65 for c in t]; return float(sum(QG[((a[i]*26+a[i+1])*26+a[i+2])*26+a[i+3]] for i in range(94)))
def ctrl(seed):
    rng=random.Random(seed); o=rng.randrange(len(TEST)-200); t=list(TEST[o:o+97])
    for s,w in CR.items(): t[s:s+len(w)]=w
    pt=''.join(t); A=list(range(26)); rng.shuffle(A); Ainv=[0]*26
    for l,x in enumerate(A): Ainv[x]=l
    W=7;O=rng.randrange(4);f=[rng.randrange(26) for _ in range(20)];g=[rng.randrange(26) for _ in range(W)]
    ct=''.join(chr(65+Ainv[(A[ord(c)-65]+f[(i+O)//W]+g[(i+O)%W])%26]) for i,c in enumerate(pt))
    b=solve(ct,7,O,int(sys.argv[2]),int(sys.argv[3]),seed*1000)
    acc=sum(b[1][i]==pt[i] for i in NC)/73 if b[1] else 0
    return dict(seed=seed,O=O,true=round(qs(pt),1),best=b[0],acc=round(acc,2))
with Pool(4) as P:
    for r in P.imap(ctrl,range(int(sys.argv[1]))): print(json.dumps(r),flush=True)
