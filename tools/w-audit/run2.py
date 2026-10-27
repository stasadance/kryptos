import sys
from mask2 import base, ctauto
from qerr import solve
from q4b import q4
job=sys.argv[1]
if job=='base': 
    m=int(sys.argv[2]); print('base',m,'Vig',base(m,False),'Beau',base(m,True),flush=True)
elif job=='ct':
    L=int(sys.argv[2]); print('ctauto L',L,'Vig',ctauto(L,False),'Beau',ctauto(L,True),flush=True)
elif job=='qerr':
    p=int(sys.argv[2]); t=sys.argv[3]; print(p,t,'<=2subs',solve(p,t,2,0,600000),'d+1',solve(p,t,0,1,600000),'d-1',solve(p,t,0,-1,600000),flush=True)
