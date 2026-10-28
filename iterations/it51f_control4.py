#!/usr/bin/env python3
"""it51f: planted controls for akenum4 (English-pruned exact search). Usage: it51f_control4.py SEED LAGS NODECAP TOL"""
import sys, random, re, time, subprocess
sys.path.insert(0, 'iterations')
from it51_control import plant, matches
eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
rng = random.Random(int(sys.argv[1])); cap, tol = sys.argv[3], sys.argv[4]; ok = n = 0
for L in map(int, sys.argv[2].split(',')):
    for form in range(3):
        for kr in range(3):
            ct, a, P = plant(rng, L, form, kr, eng); t = time.time()
            r = subprocess.run(['iterations/c/akenum4', ct, str(L), str(form), str(kr), '2000000', cap, '1', tol],
                               capture_output=True, text=True)
            sols = [l.split() for l in r.stdout.splitlines()]; f = any(matches(s, a, P, form, kr) for s in sols)
            ok += f; n += 1
            print(L, form, kr, f, r.stderr.strip(), f'{time.time()-t:.0f}s', flush=True)
print(f'controls {ok}/{n}')
