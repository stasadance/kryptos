from core import *
import itertools
N=97
def colA(order,w):
    # Dir-A: write plaintext row-wise width w, read columns in 'order'; return perm pi: CT position -> PT index
    out=[]
    for c in order: out+= list(range(c,N,w))
    return out
# Constructive search for Dir-A: require start(c)+r == j for every crib j=r*w+c
def feasible(w):
    L=[len(range(c,N,w)) for c in range(w)]
    req={}
    for j in POS:
        r,c=divmod(j,w); s=j-r
        if req.setdefault(c,s)!=s: return None
    items=sorted(req.items(),key=lambda x:x[1])
    for (c1,s1),(c2,s2) in zip(items,items[1:]):
        if s1+L[c1]>s2: return None
    free=[c for c in range(w) if c not in req]
    # gaps
    gaps=[]; cur=0
    for c,s in items: gaps.append(s-cur); cur=s+L[c]
    if any(g<0 for g in gaps): return None
    # fill gaps exactly with free columns (lengths), remaining go to tail: DP by brute force on counts
    from collections import defaultdict
    bylen=defaultdict(list)
    for c in free: bylen[L[c]].append(c)
    lens=sorted(bylen)
    avail={l:len(bylen[l]) for l in lens}
    order=[]; 
    def fill(g):
        # choose counts per length summing to g, greedy-ish with search
        for combo in itertools.product(*[range(avail[l]+1) for l in lens]):
            if sum(n*l for n,l in zip(combo,lens))==g: return combo
        return None
    # simple sequential (not globally optimal but fine to find examples)
    for (c,s),g in zip(items,gaps):
        combo=fill(g)
        if combo is None: return None
        for n,l in zip(combo,lens):
            for _ in range(n): order.append(bylen[l].pop()); avail[l]-=1
        order.append(c)
    for l in lens: order+=bylen[l]
    return order
ok=[]
for w in range(2,97):
    o=feasible(w)
    if o:
        pi=colA(o,w)
        assert all(pi[j]==j for j in POS), w
        ok.append(w)
print("Dir-A widths with a crib-fixing columnar key:",ok)
o=feasible(95); pi=colA(o,95); print("w=95 key order",o)
print("moved positions:",[ (k,pi[k]) for k in range(97) if pi[k]!=k][:20])
