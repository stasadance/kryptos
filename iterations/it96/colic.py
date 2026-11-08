import random, collections
CT=open('/mnt/project-files/k4/facts/ciphertext.txt').read().strip()
corp=open('/mnt/project-files/k4/tools/lmdata/corpus_AZ.txt').read()
CR={}
for s,w in ((21,'EASTNORTHEAST'),(63,'BERLINCLOCK')):
    for i,ch in enumerate(w): CR[s+i]=ch
def colic(t,p):
    num=den=0
    for r in range(p):
        col=t[r::p]; N=len(col); c=collections.Counter(col)
        num+=sum(n*(n-1) for n in c.values()); den+=N*(N-1)
    return 26*num/den
rng=random.Random(11); T=4000
for fam in ('perm','columnar','identity'):
    res={}
    for p in (5,6,7,8,9,12,13,18):
        k4=colic(CT,p); le=0
        for _ in range(T):
            st=rng.randrange(len(corp)-100); pt=list(corp[st:st+97])
            for q,ch in CR.items(): pt[q]=ch
            if fam=='perm': rng.shuffle(pt)
            elif fam=='columnar':
                w=rng.randrange(2,21); key=list(range(w)); rng.shuffle(key)
                pt=[pt[i] for col in key for i in range(col,97,w)]
            # substitution with p alphabets does not change pooled colIC
            if colic(pt,p)<=k4: le+=1
        res[p]=(round(k4,3),le/T)
    print(fam,res,flush=True)
