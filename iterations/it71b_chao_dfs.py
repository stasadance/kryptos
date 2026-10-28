#!/usr/bin/env python3
"""it71b: exact crib test for Chaocipher. Unknown wheel state at step 21, which is arbitrary because the wheels
and prefix are unknown. DFS from step 21 to 73 over the zenith index i at each step. The CT letter at each
step is known; the PT is known on the cribs and free in the 34..62 gap. Partial wheels are updated with
Chaocipher's fixed position permutation. Gauge: i=0 at the first step, since both wheels are rotated to zenith.
A full solution = a partial wheel pair consistent with all 53 steps. This is a relaxation (prefix 0..20 and
suffix ignored), so 0 solutions refutes Chaocipher. Control: a planted Chaocipher CT must be SAT; nulls give
the base rate. Usage: it71b_chao_dfs.py [cap]"""
import sys, random, re
sys.setrecursionlimit(10000)
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K4 = open('data/ciphertext.txt').read().strip()
CRIB = {21 + i: c for i, c in enumerate('EASTNORTHEAST')}; CRIB.update({63 + i: c for i, c in enumerate('BERLINCLOCK')})
def permL(i):   # new[j] = old[perm[j]]
    rot = [(j + i) % 26 for j in range(26)]; return [rot[0]] + rot[2:14] + [rot[1]] + rot[14:]
def permR(i):
    rot = [(j + i) % 26 for j in range(26)]; rot = rot[1:] + rot[:1]; return rot[:2] + rot[3:14] + [rot[2]] + rot[14:]
PL = [permL(i) for i in range(26)]; PR = [permR(i) for i in range(26)]
class Search:
    def __init__(s, ct, cap): s.ct, s.cap, s.nodes, s.sols = ct, cap, 0, 0
    def go(s, t, L, R):
        if s.nodes > s.cap or s.sols: return
        s.nodes += 1
        if t == 74: s.sols += 1; return
        c = s.ct[t]; p = CRIB.get(t)
        if t == 21: cands = [0]
        elif c in L: cands = [L.index(c)]
        elif p is not None and p in R: cands = [R.index(p)]
        else: cands = [i for i in range(26) if L[i] is None and (p is None or R[i] is None)]
        for i in cands:
            if L[i] not in (None, c): continue
            if p is not None:
                if R[i] not in (None, p): continue
                if R[i] is None and p in R: continue
            if L[i] is None and c in L: continue
            L2 = list(L); R2 = list(R); L2[i] = c
            if p is not None: R2[i] = p
            s.go(t + 1, [L2[k] for k in PL[i]], [R2[k] for k in PR[i]])
    def run(s):
        s.go(21, [None] * 26, [None] * 26); return 'sat' if s.sols else ('unsat' if s.nodes <= s.cap else 'cap')
if __name__ == '__main__':
    sys.path.insert(0, 'iterations'); from it71_chaocipher import chao
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    rng = random.Random(711)
    for t in range(3):
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        S = Search(chao(P, rng.sample(AZ, 26), rng.sample(AZ, 26)), cap); print('control', S.run(), S.nodes, flush=True)
    S = Search(K4, cap); r = S.run(); print('K4', r, S.nodes, flush=True)
    for t in range(5):
        S = Search(''.join(rng.sample(K4, 97)), cap); print('null', S.run(), S.nodes, flush=True)
