# Per-residue keyword-substitution test (period 24): which city keywords satisfy each residue's crib pairs?
import sys; sys.path.insert(0,'/mnt/project-files/k4/tools')
from keystream_check import crib_pairs, AZ, KA
from collections import defaultdict
def keyed(w, base=AZ):
    s=[]
    for ch in w+base:
        if ch not in s: s.append(ch)
    return ''.join(s)
res=defaultdict(list)
for i,p,c in crib_pairs(): res[i%24].append((p,c))
words=[w.strip() for w in open(sys.argv[1]) if w.strip()]
models={
 'S1 C=K[AZ.idx(P)]': lambda K,p,c: K[AZ.index(p)]==c,
 'S2 C=AZ[K.idx(P)]': lambda K,p,c: AZ[K.index(p)]==c,
 'S3 C=K[KA.idx(P)]': lambda K,p,c: K[KA.index(p)]==c,
 'S4 C=KA[K.idx(P)]': lambda K,p,c: KA[K.index(p)]==c,
}
for mn,f in models.items():
  for base_n,base in (('AZ',AZ),('KA',KA)):
    print(f'== {mn}  keyed alphabet = word + rest of {base_n}')
    tot=0
    for r in sorted(res):
        ok=[w for w in words if all(f(keyed(w,base),p,c) for p,c in res[r])]
        tot+= bool(ok)
        print(f'  r{r:2} {res[r]} -> {len(ok)} {ok[:8]}')
    print('  residues satisfiable by some word:',tot,'of',len(res))
