#!/usr/bin/env python3
"""it51b: exact stage-1 for PT-autokey under one unknown mixed alphabet, as a CP-SAT model (replaces akenum2 DFS,
which hit its node cap on kr0 controls). Variables: alphabet a (permutation), plaintext 34..62. Constraints: every
relation R_j, 21+L <= j <= 73:  form 0 a(c)=a(p)+K, 1 a(c)=K-a(p), 2 a(c)=a(p)-K (mod 26), K = a(q) | AZ(q) | KA(q),
q = P_{j-L}. Enumerates all solutions (cap). Gauge: kr1/2 with vig/var fix a(ct[73])=0.
Usage: it51b_cpsat.py --control SEED LAGS | --k4 LAGS [cap] [time]"""
import sys, random, re, time
from ortools.sat.python import cp_model
sys.path.insert(0, 'iterations')
from it51_control import plant, AZ, KA
KAI = [KA.index(ch) for ch in AZ]
K4 = open('data/ciphertext.txt').read().strip()

class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s, a, P, cap):
        super().__init__(); s.a, s.P, s.cap, s.sols = a, P, cap, []
    def on_solution_callback(s):
        s.sols.append(([s.Value(v) for v in s.a], ''.join(AZ[s.Value(v)] if not isinstance(v, int) else AZ[v] for v in s.P)))
        if len(s.sols) >= s.cap: s.StopSearch()

def solve(ct, L, form, kr, cap=20000, tlim=600, workers=1):
    m = cp_model.CpModel(); c = [AZ.index(x) for x in ct]
    a = [m.NewIntVar(0, 25, f'a{x}') for x in range(26)]; m.AddAllDifferent(a)
    P = [None] * 97
    for i, ch in enumerate('EASTNORTHEAST'): P[21 + i] = AZ.index(ch)
    for i, ch in enumerate('BERLINCLOCK'): P[63 + i] = AZ.index(ch)
    for j in range(34, 63): P[j] = m.NewIntVar(0, 25, f'P{j}')
    def aval(x, tag):
        if isinstance(x, int): return a[x]
        v = m.NewIntVar(0, 25, tag); m.AddElement(x, a, v); return v
    for j in range(21 + L, 74):
        q = P[j - L]; ap = aval(P[j], f'ap{j}'); ac = a[c[j]]
        if kr == 0: K = aval(q, f'K{j}')
        elif kr == 1: K = q
        else:
            if isinstance(q, int): K = KAI[q]
            else: K = m.NewIntVar(0, 25, f'K{j}'); m.AddElement(q, KAI, K)
        t = m.NewIntVar(-1, 2, f't{j}')
        if form == 0: m.Add(ac == ap + K - 26 * t)
        elif form == 1: m.Add(ac == K - ap + 26 * t)
        else: m.Add(ac == ap - K + 26 * t)
    if kr != 0 and form != 1: m.Add(a[c[73]] == 0)
    s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.max_time_in_seconds = tlim
    s.parameters.num_workers = workers
    cb = CB(a, P, cap); st = s.Solve(m, cb)
    return cb.sols, s.StatusName(st), len(cb.sols) >= cap

def matches(sols, a, Ptrue):
    for av, pt in sols:
        if pt[21:74] != Ptrue[21:74]: continue
        for sh in range(26):
            for mu in (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25):
                if all((mu * av[x] + sh) % 26 == a[x] for x in range(26)): return True
    return False

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == '--control':
        eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
        rng = random.Random(int(sys.argv[2])); ok = n = 0
        for L in map(int, sys.argv[3].split(',')):
            for form in range(3):
                for kr in range(3):
                    ct, a, P = plant(rng, L, form, kr, eng); t = time.time()
                    sols, st, capped = solve(ct, L, form, kr, cap=int(sys.argv[4]) if len(sys.argv) > 4 else 20000,
                                             tlim=float(sys.argv[5]) if len(sys.argv) > 5 else 300)
                    f = matches(sols, a, P); ok += f; n += 1
                    print(f'control L={L} f={form} kr={kr}: found={f} sols={len(sols)}{"+" if capped else ""} {st} {time.time()-t:.0f}s', flush=True)
        print(f'controls {ok}/{n}')
    else:
        cap = int(sys.argv[3]) if len(sys.argv) > 3 else 20000; tl = float(sys.argv[4]) if len(sys.argv) > 4 else 600
        for L in map(int, sys.argv[2].split(',')):
            for form in range(3):
                for kr in range(3):
                    t = time.time(); sols, st, capped = solve(K4, L, form, kr, cap, tl)
                    print(f'K4 L={L} f={form} kr={kr}: sols={len(sols)}{"+" if capped else ""} {st} {time.time()-t:.0f}s', flush=True)
                    for av, pt in sols[:5]: print('   ', pt, av, flush=True)
