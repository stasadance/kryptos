#!/usr/bin/env python3
"""it51d: planted controls for akenum3. Usage: it51d_control3.py L NODECAP"""
import sys, random, re, time, subprocess
sys.path.insert(0,'iterations')
from it51_control import plant, matches
eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
rng = random.Random(51)
L=int(sys.argv[1]); cap=sys.argv[2]
for form in range(3):
    for kr in range(3):
        ct,a,P = plant(rng,L,form,kr,eng); t=time.time()
        r = subprocess.run(['iterations/c/akenum3',ct,str(L),str(form),str(kr),'2000000',cap],capture_output=True,text=True)
        sols=[l.split() for l in r.stdout.splitlines()]
        print(L,form,kr,any(matches(s,a,P,form,kr) for s in sols),r.stderr.strip(),f'{time.time()-t:.0f}s',flush=True)
