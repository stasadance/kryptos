import random,subprocess,sys,json,numpy as np
from multiprocessing import Pool
QG=np.fromfile('qg.bin',dtype=np.float32); TEST=open('test.txt').read()
CR={21:"EASTNORTHEAST",63:"BERLINCLOCK"}; CP={s+j for s,w in CR.items() for j in range(len(w))}; NC=[i for i in range(97) if i not in CP]
def qs(t):
    a=[ord(c)-65 for c in t]; return float(sum(QG[((a[i]*26+a[i+1])*26+a[i+2])*26+a[i+3]] for i in range(94)))
def inst(na,per,seed):
    rng=random.Random(seed); o=rng.randrange(len(TEST)-200); t=list(TEST[o:o+97])
    for s,w in CR.items(): t[s:s+len(w)]=w
    pt=''.join(t); A=list(range(26)); rng.shuffle(A); B=A[:] if na==1 else rng.sample(range(26),26)
    Binv=[0]*26
    for l,x in enumerate(B): Binv[x]=l
    if per: sh=[rng.randrange(26) for _ in range(per)]; k=[sh[i%per] for i in range(97)]
    else: k=[rng.randrange(26) for _ in range(97)]
    ct=''.join(chr(65+Binv[(A[ord(c)-65]+k[i])%26]) for i,c in enumerate(pt))
    return pt,ct,''.join(chr(65+x) for x in k)
def job(a):
    na,per,seed,R,IT=a; pt,ct,ks=inst(na,per,seed)
    out=subprocess.run(['./sa',str(na),str(per),ct,'-' if per else ks,str(R),str(IT),str(seed),__import__('os').environ.get('LAM','5')],capture_output=True,text=True).stdout.split('\n')
    res=[(float(l.split()[0]),l.split()[1]) for l in out if l.strip()]
    b=max(res); accs=sum(b[1][i]==pt[i] for i in NC)/73
    return dict(na=na,per=per,seed=seed,true=round(qs(pt),1),best=b[0],acc=round(accs,2),all=[r[0] for r in res],dec=b[1])
if __name__=='__main__':
    na,per,n,R,IT=map(int,sys.argv[1:6])
    with Pool(4) as P:
        for r in P.imap(job,[(na,per,1000+s,R,IT) for s in range(n)]):
            print(json.dumps(r),flush=True)
