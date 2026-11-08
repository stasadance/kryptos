import numpy as np, itertools, random, sys
CT=open('/mnt/project-files/k4/facts/ciphertext.txt').read().strip()
AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'; KA='KRYPTOSABCDEFGHIJLMNQUVWXZ'
CR={}
for s,w in ((21,'EASTNORTHEAST'),(63,'BERLINCLOCK')):
    for i,ch in enumerate(w): CR[s+i]=ch
n=4
G=np.array(list(itertools.product(range(26),repeat=n)),dtype=np.int64)  # 456976 x 4
def masks_for(vals, affine):
    # vals: (M, nb) residues; return set of kept-masks (maximal not needed)
    nb=vals.shape[1]; w=(1<<np.arange(nb)).astype(np.int64)
    out=set()
    targets=range(26) if affine else [0]
    for t in targets:
        m=((vals==t)*w).sum(1)
        out.update(np.unique(m).tolist())
    return out
def mindrop(rowmasks, nb):
    full=(1<<nb)-1
    for k in range(nb+1):
        for D in itertools.combinations(range(nb),k):
            keep=full & ~sum(1<<d for d in D)
            if all(any((keep & ~m)==0 for m in ms) for ms in rowmasks): return k,D
    return None
def bounds(ct, cr, num, o, affine, lin1=False):
    N={ch:(num.index(ch)+(1 if lin1 else 0)) for ch in AZ}
    c=np.array([N[x] for x in ct])
    # dec form: every crib letter, block containing it
    blocks=sorted({(q-o)//n for q in cr})
    bi={b:i for i,b in enumerate(blocks)}
    rowmasks=[]
    for r in range(n):
        qs=[q for q in cr if (q-o)%n==r]
        idx=[bi[(q-o)//n] for q in qs]
        C=np.array([c[o+n*((q-o)//n):o+n*((q-o)//n)+n] for q in qs])  # (m,4)
        P=np.array([N[cr[q]] for q in qs])
        v=(P[None,:]-G@C.T)%26
        ms=masks_for(v,affine)
        # map per-equation mask to block mask
        bm=set()
        for m in ms:
            bb=0
            for e,i in enumerate(idx):
                if m>>e&1: bb|=1<<i
            # equations not kept -> their blocks must be dropped; kept-block mask = blocks with all eqs kept
            allb=0
            for e,i in enumerate(idx):
                if not (m>>e&1): allb|=1<<i
            bm.add(((1<<len(blocks))-1) & ~allb)
        rowmasks.append(bm)
    dec=mindrop(rowmasks,len(blocks))
    # enc form: wholly crib blocks
    wb=[b for b in blocks if all((o+n*b+i) in cr for i in range(n))]
    enc=0
    for r in range(n):
        Pm=np.array([[N[cr[o+n*b+i]] for i in range(n)] for b in wb])
        cv=np.array([c[o+n*b+r] for b in wb])
        v=(cv[None,:]-G@Pm.T)%26
        if affine:
            best=max(int(((v==t).sum(1)).max()) for t in range(26))
        else:
            best=int((v==0).sum(1).max())
        enc+=len(wb)-best
    return enc,dec
mode=sys.argv[1] if len(sys.argv)>1 else 'k4'
if mode=='k4':
    for affine in (True,False):
        cfgs=[('AZ0',AZ,False),('KA0',KA,False)]+([] if affine else [('AZ1',AZ,True),('KA1',KA,True)])
        for name,num,l1 in cfgs:
            for o in range(n):
                e,d=bounds(CT,CR,num,o,affine,l1)
                print('aff' if affine else 'lin',name,'off',o,'enc',e,'dec',d,'bound',max(e,d[0]),flush=True)
elif mode=='plant':
    rng=random.Random(int(sys.argv[2]))
    corpus=open('/mnt/project-files/k4/tools/lmdata/corpus_AZ.txt').read()
    for t in range(3):
        st=rng.randrange(len(corpus)-200); pt=list(corpus[st:st+97])
        for q,ch in CR.items(): pt[q]=ch
        o=rng.randrange(4); num=rng.choice([AZ,KA]); N={ch:num.index(ch) for ch in AZ}
        while True:
            K=np.array([[rng.randrange(26) for _ in range(4)] for _ in range(4)])
            d=int(round(np.linalg.det(K)))%26
            if d%2 and d%13: break
        b=np.array([rng.randrange(26) for _ in range(4)])
        ct=list(''.join(rng.choice(AZ) for _ in range(97)))
        for blk in range(o, 97-3, 4):
            p=np.array([N[x] for x in pt[blk:blk+4]]); cc=(K@p+b)%26
            for i in range(4): ct[blk+i]=num[cc[i]]
        nerr=int(sys.argv[3]); qs=rng.sample(sorted(CR),nerr)
        for q in qs: ct[q]=rng.choice([x for x in AZ if x!=ct[q]])
        print('plant',t,'err',nerr,'at',sorted(qs),'true off',o,'num',num[:3],'bound(true)',bounds(''.join(ct),CR,num,o,True),flush=True)
