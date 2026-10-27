import re,sys,math,collections
import numpy as np
def clean(p):
    t=open(p,encoding='utf-8',errors='ignore').read()
    m=re.search(r"\*\*\* ?START OF.*?\*\*\*",t); n=re.search(r"\*\*\* ?END OF",t)
    t=t[m.end() if m else 0:n.start() if n else len(t)]
    return re.sub('[^A-Z]','',t.upper())
C='/tmp/claude-0/-home-user-kryptos/046a83fd-aa4b-57f6-97e0-639b3d9e1ef4/scratchpad/it05/corpus/'
train=clean(C+'pg2600.txt'); test=clean(C+'pg1342.txt')
open('test.txt','w').write(test)
a=np.frombuffer(train.encode(),dtype=np.uint8)-65
idx=((a[:-3].astype(np.int64)*26+a[1:-2])*26+a[2:-1])*26+a[3:]
cnt=np.bincount(idx,minlength=26**4).astype(np.float64)
N=cnt.sum(); lp=np.log10((cnt+0.01)/N).astype(np.float32); lp.tofile('qg.bin')
# conditional entropies on held-out test (orders 0..3 context), add-0.5 smoothing
b=np.frombuffer(test[:500000].encode(),dtype=np.uint8)-65
for k in range(0,4):
    # model of order k (context k letters) from train
    def code(x,k):
        c=np.zeros(len(x)-k,dtype=np.int64)
        for j in range(k+1): c=c*26+x[j:len(x)-k+j]
        return c
    ctr=np.bincount(code(a,k),minlength=26**(k+1)).astype(float)+0.5
    ctx=ctr.reshape(-1,26).sum(1)
    cb=code(b,k)
    h=-np.mean(np.log2(ctr[cb]/ctx[cb//26]))
    print('order',k+1,'gram cond entropy bits/letter %.3f  redundancy %.3f'%(h,math.log2(26)-h))
