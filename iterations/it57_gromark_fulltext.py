#!/usr/bin/env python3
"""it57 (H-601 follow-up): the 46 crib-consistent Gromark primers (b10/5: 39, b10/4: 3, b8/5: 4; tools/gromark.py scan)
under TWO arbitrary alphabets, B(C_i) = A(P_i) + k_i, decided by FULL-TEXT crib-exact annealing (it05 sa.c, NALPH=2,
known key stream) instead of the crib-forced letters only. Controls: planted Gromark (random primer, two random
alphabets, English + cribs) must be recovered. Usage: it57_gromark_fulltext.py control N | k4 SHARD NSHARDS"""
import sys, json, random, re, subprocess
sys.path.insert(0, 'tools'); import gromark as g
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; W = '/tmp/claude-0/it27'
K4 = open('data/ciphertext.txt').read().strip()
R, IT = '8', '4000000'
def sa(ct, key, seed):
    out = subprocess.run([W + '/sa', '2', '0', ct, ''.join(AZ[x] for x in key), R, IT, str(seed), '25'], cwd=W,
                         capture_output=True, text=True).stdout.split('\n')
    return max((float(l.split()[0]), l.split()[1]) for l in out if l.strip())
if __name__ == '__main__':
    if sys.argv[1] == 'control':
        eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
        rng = random.Random(57)
        for t in range(int(sys.argv[2])):
            b, L = ((10, 5), (10, 4), (8, 5))[t % 3]; key = g.expand([rng.randrange(b) for _ in range(L)], b)
            q = rng.randrange(len(eng) - 200); pt = list(eng[q:q + 97]); pt[21:34] = 'EASTNORTHEAST'; pt[63:74] = 'BERLINCLOCK'
            A = rng.sample(range(26), 26); B = rng.sample(range(26), 26); Bi = {v: i for i, v in enumerate(B)}
            ct = ''.join(AZ[Bi[(A[AZ.index(p)] + key[i]) % 26]] for i, p in enumerate(pt))
            s, d = sa(ct, key, t); acc = sum(x == y for x, y in zip(d, pt)) / 97
            print(f'control {t} b{b}/{L}: score {s:.1f} mean {s/94:.2f} acc {acc:.2f} {d}', flush=True)
    else:
        sh, ns = int(sys.argv[2]), int(sys.argv[3])
        for j, (b, L, pr) in enumerate(json.load(open('iterations/out/it57_primers.json'))):
            if j % ns != sh: continue
            s, d = sa(K4, g.expand(pr, b), j)
            print(f'K4 b{b}/{L} {"".join(map(str, pr))}: score {s:.1f} mean {s/94:.2f} {d}', flush=True)
