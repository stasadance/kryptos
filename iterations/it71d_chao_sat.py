#!/usr/bin/env python3
"""it71d: exact Chaocipher crib feasibility as pure SAT (CaDiCaL via python-sat). One-hot wheel states
L_t[j][x], R_t[j][x] for t = 21..74, one-hot zenith I_t[i]; (I_t=i) -> (L_{t+1}[j]=x <-> L_t[PL_i(j)]=x), the
same for R; (I_t=i) -> L_t[i]=CT_t; on cribs (I_t=i) -> R_t[i]=PT_t; wheels at t=21 are permutations; gauge
I_21 = 0. This is a relaxation (prefix ignored), so UNSAT refutes Chaocipher for K4.
Controls: planted Chaocipher CTs must be SAT. Nulls: shuffled K4. Usage: it71d_chao_sat.py [n_nulls]"""
import sys, random, re, itertools, time
from pysat.solvers import Solver
sys.path.insert(0, 'iterations')
from it71b_chao_dfs import PL, PR, CRIB, K4, AZ
from it71_chaocipher import chao
T0, T1 = 21, 74
def build(ct):
    n = [0]
    def new(): n[0] += 1; return n[0]
    L = {t: [[new() for x in range(26)] for j in range(26)] for t in range(T0, T1 + 1)}
    R = {t: [[new() for x in range(26)] for j in range(26)] for t in range(T0, T1 + 1)}
    I = {t: [new() for i in range(26)] for t in range(T0, T1)}
    cl = []
    def exactly_one(vs): cl.append(list(vs)); cl.extend([[-a, -b] for a, b in itertools.combinations(vs, 2)])
    for W in (L, R):
        for j in range(26): exactly_one(W[T0][j])
        for x in range(26): exactly_one([W[T0][j][x] for j in range(26)])
    for t in range(T0, T1):
        exactly_one(I[t])
        c = AZ.index(ct[t]); p = CRIB.get(t)
        for i in range(26):
            v = I[t][i]; cl.append([-v, L[t][i][c]])
            if p is not None: cl.append([-v, R[t][i][AZ.index(p)]])
            for W, P in ((L, PL), (R, PR)):
                for j in range(26):
                    src = P[i][j]
                    for x in range(26):
                        cl.append([-v, -W[t][src][x], W[t + 1][j][x]]); cl.append([-v, W[t][src][x], -W[t + 1][j][x]])
    cl.append([I[T0][0]])
    return cl
def solve(ct, tl=None):
    s = Solver(name='cadical153', bootstrap_with=build(ct)); t = time.time(); r = s.solve(); s.delete()
    return ('SAT' if r else 'UNSAT'), round(time.time() - t)
if __name__ == '__main__':
    nn = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    rng = random.Random(714)
    for t in range(2):
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        print('control', solve(chao(P, rng.sample(AZ, 26), rng.sample(AZ, 26))), flush=True)
    print('K4', solve(K4), flush=True)
    for t in range(nn): print('null', solve(''.join(rng.sample(K4, 97))), flush=True)
