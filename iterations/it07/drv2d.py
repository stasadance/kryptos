import random,subprocess,sys,json
from multiprocessing import Pool
TEST=open('/tmp/claude-0/-home-user-kryptos/046a83fd-aa4b-57f6-97e0-639b3d9e1ef4/scratchpad/it05/test.txt').read()
CR={21:"EASTNORTHEAST",63:"BERLINCLOCK"}; CP={s+j for s,w in CR.items() for j in range(len(w))}; NC=[i for i in range(97) if i not in CP]
K4=open('/home/user/kryptos/data/ciphertext.txt').read().strip()
R,IT,LAM=int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
def run(ct,W,O,seed):
    out=subprocess.run(['./sarow',str(W),str(O),ct,str(R),str(IT),str(seed),LAM],capture_output=True,text=True).stdout.split('\n')
    return max((float(l.split()[0]),l.split()[1]) for l in out if l.strip())
def ctrl(seed):
    rng=random.Random(seed); o=rng.randrange(len(TEST)-200); t=list(TEST[o:o+97])
    for s,w in CR.items(): t[s:s+len(w)]=w
    pt=''.join(t); A=list(range(26)); rng.shuffle(A); Ainv=[0]*26
    for l,x in enumerate(A): Ainv[x]=l
    W=7;O=rng.randrange(4);f=[rng.randrange(26) for _ in range(20)];g=[rng.randrange(26) for _ in range(W)]
    ct=''.join(chr(65+Ainv[(A[ord(c)-65]+f[(i+O)//W]+g[(i+O)%W])%26]) for i,c in enumerate(pt))
    b=run(ct,W,O,seed); acc=sum(b[1][i]==pt[i] for i in NC)/73
    return dict(kind='ctrl',seed=seed,O=O,best=b[0],acc=round(acc,2),dec=b[1])
def k4(O): b=run(K4,7,O,O+77); return dict(kind='k4',O=O,best=b[0],dec=b[1])
def dispatch(a): return ctrl(a[1]) if a[0]=='c' else k4(a[1])
if __name__=='__main__':
    jobs=[('c',s) for s in range(int(sys.argv[1]))]+([('k',o) for o in range(7)] if sys.argv[2]=='k4' else [])
    with Pool(4) as P:
        for r in P.imap(dispatch,jobs): print(json.dumps(r),flush=True)
