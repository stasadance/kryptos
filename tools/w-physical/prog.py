CT=open('/mnt/project-files/k4/facts/ciphertext.txt').read().strip()
CR={22:"EASTNORTHEAST",64:"BERLINCLOCK"}
PT={}
for s,w in CR.items():
    for j,ch in enumerate(w): PT[s-1+j]=ch
STD="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
combos=[("STD/STD",STD,STD),("KA/KA",KA,KA),("STD/KA",STD,KA),("KA/STD",KA,STD)]
hits=0
for name,PA,CA in combos:
  for mode in ("vig","beau"):
    d={i:((CA.index(CT[i])-PA.index(p))%26 if mode=="vig" else (CA.index(CT[i])+PA.index(p))%26) for i,p in PT.items()}
    for m in range(1,25):
      for a in range(26):
        for b in range(1,26):
          for base in (0,1):  # index origin
            if all((a+b*((i+base)//m))%26==v for i,v in d.items()):
                hits+=1; print("HIT",name,mode,m,a,b,base)
    # period-24 bijection check for arbitrary alphabets
print("progressive clock-tick key hits:",hits)
# period 24 arbitrary alphabets: crib bijection check
cols={}
ok=True
for i,p in PT.items():
    r=i%24; cols.setdefault(r,[]).append((p,CT[i]))
conf=[]
for r,l in cols.items():
    for x in l:
        for y in l:
            if (x[0]==y[0])!=(x[1]==y[1]): conf.append((r,x,y))
print("period-24 arbitrary-alphabet conflicts:",conf)
print("residues with >=2 crib letters:",{r:l for r,l in cols.items() if len(l)>1})
