import sys; sys.path.insert(0,'/mnt/project-files/k4/tools')
from keystream_check import CT, crib_pairs, gen_periods
from collections import defaultdict
cls=defaultdict(list)
for i,p,c in crib_pairs(): cls[i%24].append((i+1,p,c))
for r in range(24): print(r, cls.get(r,'-- unconstrained'))
print('gen periods ok incl 24:', 24 in gen_periods(52))
