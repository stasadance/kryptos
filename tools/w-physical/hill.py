import itertools
CT=open('/mnt/project-files/k4/facts/ciphertext.txt').read().strip()
CR={22:"EASTNORTHEAST",64:"BERLINCLOCK"}
PT={}
for s,w in CR.items():
    for j,ch in enumerate(w): PT[s-1+j]=ch
STD="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
for an,al in [("STD",STD),("KA",KA)]:
  for n in (2,3):
    for off in range(n):
        blocks=[]
        for b in range(off,97-n+1,n):
            if all(b+j in PT for j in range(n)):
                blocks.append(([al.index(PT[b+j]) for j in range(n)],[al.index(CT[b+j]) for j in range(n)]))
        # Each matrix row r: sum_j r_j*p_j == c_row (mod 26), for C = M P
        rows_ok=[]
        for row in range(n):
            sols=[r for r in itertools.product(range(26),repeat=n) if all(sum(r[j]*p[j] for j in range(n))%26==c[row] for p,c in blocks)]
            rows_ok.append(len(sols))
        # also decryption direction P = M C
        rows_ok2=[]
        for row in range(n):
            sols=[r for r in itertools.product(range(26),repeat=n) if all(sum(r[j]*c[j] for j in range(n))%26==p[row] for p,c in blocks)]
            rows_ok2.append(len(sols))
        print(f"{an} Hill n={n} offset={off} blocks={len(blocks)} enc-row solutions={rows_ok} dec-row solutions={rows_ok2}")
