# Weltzeituhr "face offset + rotating ring" key: k_i = a + b*i + c*((i+o) mod 24)  (mod 26)
# i = 0-based K4 position. b = ring advance per letter, c*((i+o)%24) = face/time-zone offset.
import sys; sys.path.insert(0,'/mnt/project-files/k4/tools')
from keystream_check import crib_pairs, AZ, KA
pairs=crib_pairs()
rules={'vig':lambda x,y:(y-x)%26,'beau':lambda x,y:(y+x)%26,'vbeau':lambda x,y:(x-y)%26}
hits=[]; tot=0
for PA_n,PA in (('AZ',AZ),('KA',KA)):
  for CA_n,CA in (('AZ',AZ),('KA',KA)):
    for rn,f in rules.items():
      ks=[(i,f(PA.index(p),CA.index(c))) for i,p,c in pairs]
      for o in range(24):
        for b in range(26):
          for c in range(26):
            tot+=1
            a=(ks[0][1]-b*ks[0][0]-c*((ks[0][0]+o)%24))%26
            if all((a+b*i+c*((i+o)%24))%26==k for i,k in ks):
              hits.append((PA_n,CA_n,rn,a,b,c,o))
print('configs',tot*26,'hits',len(hits))
for h in hits[:50]: print(h)
