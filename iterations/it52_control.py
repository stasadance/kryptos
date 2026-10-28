#!/usr/bin/env python3
"""it52 controls: plant PT-autokey (random alphabet, English P&P text, K4 cribs) and check whether beam52 returns the
true plaintext 21..73 (rank among its final states). Usage: it52_control.py SEED LAGS W"""
import sys, random, re, time, subprocess
sys.path.insert(0, 'iterations')
from it51_control import plant
QG = '/tmp/claude-0/it27/qg.bin'
eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
rng = random.Random(int(sys.argv[1])); W = sys.argv[3]; ok = n = 0
for L in map(int, sys.argv[2].split(',')):
    for form in range(3):
        for kr in range(3):
            ct, a, P = plant(rng, L, form, kr, eng); t = time.time()
            r = subprocess.run(['iterations/c/beam52', ct, str(L), str(form), str(kr), W, QG, '1000'], capture_output=True, text=True)
            pts = [l.split()[1][21:74] for l in r.stdout.splitlines()]
            rank = pts.index(P[21:74]) if P[21:74] in pts else -1; ok += rank >= 0; n += 1
            print(f'L={L} f={form} kr={kr}: rank={rank} | {r.stderr.strip()} | {time.time()-t:.0f}s', flush=True)
print(f'controls {ok}/{n}')
