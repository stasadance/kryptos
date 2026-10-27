import collections
CT=open('/mnt/project-files/k4/facts/ciphertext.txt').read().strip()
assert len(CT)==97
CR={22:"EASTNORTHEAST",64:"BERLINCLOCK"}
PT={}
for s,w in CR.items():
    for j,ch in enumerate(w): PT[s-1+j]=ch
STD="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
print("CT counts",sorted(collections.Counter(CT).items()))
need=collections.Counter("".join(CR.values()))
have=collections.Counter(CT)
print("crib letters exceeding CT supply:",{k:(v,have[k]) for k,v in need.items() if v>have[k]})
def derive(alpha,mode):
    out={}
    for i,p in PT.items():
        c=CT[i]; ci=alpha.index(c); pi=alpha.index(p)
        if mode=='vig': k=(ci-pi)%26
        elif mode=='beau': k=(ci+pi)%26
        elif mode=='varb': k=(pi-ci)%26
        out[i]=k
    return out
res={}
for an,al in [("STD",STD),("KA",KA)]:
    for m in ['vig','beau','varb']:
        d=derive(al,m); res[(an,m)]=d
        s="".join(al[d[i]] for i in sorted(d))
        print(f"{an:3} {m:4} key@22-34,64-74 letters={s[:13]} {s[13:]}  nums={[d[i] for i in sorted(d)]}")
# periodic consistency for periods 1..48
print("\nPeriods consistent (no conflicting key at same residue):")
for k,d in res.items():
    ok=[]
    for p in range(1,49):
        r={}
        good=True
        for i,v in d.items():
            if r.setdefault(i%p,v)!=v: good=False;break
        if good: ok.append(p)
    print(k, ok)
# Gronsfeld (key digits 0-9 only) under STD vig/varb
for k in [("STD","vig"),("STD","varb"),("STD","beau")]:
    print("max key value",k,max(res[k].values()),"all<=9:",all(v<=9 for v in res[k].values()))
# progressive/linear key k_i = a+b*i mod 26
print("\nLinear progressive key fits:")
for k,d in res.items():
    fits=[(a,b) for a in range(26) for b in range(26) if all((a+b*i)%26==v for i,v in d.items())]
    print(k,fits)
