#!/usr/bin/env python3
"""it71c: exact Chaocipher crib feasibility with CP-SAT. Wheel states L_t, R_t (permutations of 0..25) for
t = 21..74; zenith index i_t; L_{t+1}[j] = L_t[PL(i_t, j)], R_{t+1}[j] = R_t[PR(i_t, j)] (table + element);
L_t[i_t] = CT_t for all t; R_t[i_t] = PT_t on the crib positions. Gauge i_21 = 0. Relaxation (prefix ignored),
so INFEASIBLE refutes Chaocipher. Controls: planted Chaocipher CTs must be FEASIBLE; nulls give the base rate.
Usage: it71c_chao_cpsat.py [timelimit_s]"""
import sys, random, re
from ortools.sat.python import cp_model
sys.path.insert(0, 'iterations')
from it71b_chao_dfs import PL, PR, CRIB, K4, AZ
from it71_chaocipher import chao
def solve(ct, tl, t0=21, t1=74):
    m = cp_model.CpModel()
    L = {t: [m.NewIntVar(0, 25, f'L{t}_{j}') for j in range(26)] for t in range(t0, t1 + 1)}
    R = {t: [m.NewIntVar(0, 25, f'R{t}_{j}') for j in range(26)] for t in range(t0, t1 + 1)}
    for t in L: m.AddAllDifferent(L[t]); m.AddAllDifferent(R[t])
    for t in range(t0, t1):
        i = m.NewIntVar(0, 25, f'i{t}')
        if t == t0: m.Add(i == 0)
        m.AddElement(i, L[t], AZ.index(ct[t]))
        if t in CRIB: m.AddElement(i, R[t], AZ.index(CRIB[t]))
        for j in range(26):
            kl = m.NewIntVar(0, 25, ''); kr = m.NewIntVar(0, 25, '')
            m.AddAllowedAssignments([i, kl], [(x, PL[x][j]) for x in range(26)])
            m.AddAllowedAssignments([i, kr], [(x, PR[x][j]) for x in range(26)])
            m.AddElement(kl, L[t], L[t + 1][j]); m.AddElement(kr, R[t], R[t + 1][j])
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 1
    return s.StatusName(s.Solve(m))
if __name__ == '__main__':
    tl = float(sys.argv[1]) if len(sys.argv) > 1 else 600
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    rng = random.Random(712)
    for t in range(2):
        o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
        print('control', solve(chao(P, rng.sample(AZ, 26), rng.sample(AZ, 26)), tl), flush=True)
    print('K4', solve(K4, tl), flush=True)
    for t in range(3): print('null', solve(''.join(rng.sample(K4, 97)), tl), flush=True)
