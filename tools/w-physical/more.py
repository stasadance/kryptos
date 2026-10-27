import itertools
CT=open('/mnt/project-files/k4/facts/ciphertext.txt').read().strip()
CR={22:"EASTNORTHEAST",64:"BERLINCLOCK"}
PT={}
for s,w in CR.items():
    for j,ch in enumerate(w): PT[s-1+j]=ch
STD="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
# Generic tableau: plain alphabet PA, cipher alphabet CA; Vig: c = CA[(PA.index(p)+k)%26]; Beau: c=CA[(k-PA.index(p))%26]
combos=[("PA=STD,CA=STD",STD,STD),("PA=KA,CA=KA",KA,KA),("PA=STD,CA=KA (QuagII-like)",STD,KA),("PA=KA,CA=STD (QuagI-like)",KA,STD)]
for name,PA,CA in combos:
  for mode in ("vig","beau"):
    d={}
    for i,p in PT.items():
        ci=CA.index(CT[i]); pi=PA.index(p)
        d[i]=(ci-pi)%26 if mode=="vig" else (ci+pi)%26
    per=[p for p in range(1,27) if all(len({v for i,v in d.items() if i%p==r})<=1 for r in range(p))]
    grons=all(v<=9 for v in d.values())
    print(f"{name:28} {mode}: periods<=26 consistent={per}; gronsfeld(0-9) possible={grons}; max={max(d.values())}")
# Hill n=4 (standard and KA numbering)
for an,al in [("STD",STD),("KA",KA)]:
  n=4
  for off in range(n):
    blocks=[([al.index(PT[b+j]) for j in range(n)],[al.index(CT[b+j]) for j in range(n)]) for b in range(off,97-n+1,n) if all(b+j in PT for j in range(n))]
    cnt=[]
    for row in range(n):
        cnt.append(sum(1 for r in itertools.product(range(26),repeat=n) if all(sum(r[j]*p[j] for j in range(n))%26==c[row] for p,c in blocks)))
    print(f"{an} Hill n=4 off={off} blocks={len(blocks)} enc-row sols={cnt}")
