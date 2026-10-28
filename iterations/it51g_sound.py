#!/usr/bin/env python3
"""it51g soundness + null controls for akenum4 (tol=1000 = no English pruning, i.e. the pure exact solver).
(a) planted instance + H true alphabet values given as hints (in the solver's gauge): search must COMPLETE and contain
    the truth. (b) random ciphertext (no truth): reports node count, to compare with K4's fast completions.
Usage: it51g_sound.py SEED LAGS H"""
import sys, random, re, time, subprocess
sys.path.insert(0, 'iterations')
from it51_control import plant, matches, AZ
eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
rng = random.Random(int(sys.argv[1])); H = int(sys.argv[3])
def go(ct, L, f, k, hint):
    r = subprocess.run(['iterations/c/akenum4', ct, str(L), str(f), str(k), '2000000', '300000000', '1', '1000', '-', hint],
                       capture_output=True, text=True)
    return [l.split() for l in r.stdout.splitlines()], r.stderr.strip()
ok = n = 0
for L in map(int, sys.argv[2].split(',')):
    for f in range(3):
        for k in range(3):
            ct, a, P = plant(rng, L, f, k, eng)
            # express the truth in the solver's gauge: kr1/2 & f!=1 fix a(ct[73])=0
            s = a[AZ.index(ct[73])] if (k != 0 and f != 1) else 0
            g = [(v - s) % 26 for v in a]
            hl = rng.sample(range(26), H); hint = ','.join(f'{AZ[x]}:{g[x]}' for x in hl)
            sols, info = go(ct, L, f, k, hint); fo = any(matches(x, a, P, f, k) for x in sols)
            rct = ''.join(rng.choice(AZ) for _ in range(97)); _, rinfo = go(rct, L, f, k, '')
            ok += fo and 'CAP' not in info; n += 1
            print(f'L={L} f={f} k={k}: hinted found={fo} [{info}] | null [{rinfo}]', flush=True)
print(f'complete+found {ok}/{n}')
