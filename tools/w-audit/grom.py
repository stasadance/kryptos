from core import *
import itertools,sys
def key(pr,b,N=97):
    k=list(pr)
    while len(k)<N: k.append((k[-len(pr)]+k[-len(pr)+1])%b)
    return k
def consistent(k):
    # nodes: ('p',L) value y(L); ('c',L) value x(L). constraint x(C)-y(P)=k_i mod 26
    par={};off={}  # off[n]=val(n)-val(root)
    def find(n):
        if n not in par: par[n]=n;off[n]=0;return n,0
        if par[n]==n: return n,0
        r,o=find(par[n]); par[n]=r; off[n]=(off[n]+o)%26; return r,off[n]
    for i in POS:
        a=('c',CT[i]); bb=('p',PT[i])
        ra,oa=find(a); rb,ob=find(bb)
        # val(a)-val(bb)=k
        if ra==rb:
            if (oa-ob)%26!=k[i]%26: return False
        else:
            par[ra]=rb; off[ra]=(ob+k[i]-oa)%26
    # injectivity within each side
    seen={}
    for n in list(par):
        r,o=find(n)
        key_=(n[0],r,o)
        if key_ in seen and seen[key_]!=n: return False
        seen[key_]=n
    return True
if __name__=="__main__":
  b=int(sys.argv[1]); L=int(sys.argv[2])
  good=[pr for pr in itertools.product(range(b),repeat=L) if consistent(key(pr,b))]
  print(b,L,len(good), [''.join(map(str,g)) for g in good][:50])
