#!/usr/bin/env python3
"""Decrypt a one-alphabet drop-mode hit: enumerate all alphabets (CP-SAT) consistent with the 23 kept crib rows under
vig1/beau1 for a key VALUE stream, decrypt K4, score with it05 quadgrams.
Usage: python3 iterations/it35c_check_hit.py MODEL DROPROW 'python expr for the 97 key values' [QG.bin]"""
import sys
import numpy as np
from ortools.sat.python import cp_model
sys.path.insert(0, "/mnt/project-files/k4/tools")
import keygen as KG
from keygen import *
model, drop, kv = sys.argv[1], int(sys.argv[2]), [int(x) % 26 for x in eval(sys.argv[3])]
qg = np.fromfile(sys.argv[4] if len(sys.argv) > 4 else "/tmp/claude-0/it27/qg.bin", dtype=np.float32)
AZ, CT = KG.AZ, KG.CT; P = KG.crib_pairs(CT)
m = cp_model.CpModel(); a = {L: m.NewIntVar(0, 25, L) for L in AZ}; m.AddAllDifferent(list(a.values()))
for t, (i, p, c) in enumerate(P):
    if t == drop: continue
    q = m.NewIntVar(-3, 3, f"q{t}")
    m.Add((a[c] - a[p] if model == "vig1" else a[c] + a[p]) == kv[i - 1] + 26 * q)
sols = []
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(self):
        sols.append({L: self.Value(a[L]) for L in AZ})
        if len(sols) >= 50000: self.StopSearch()
s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.max_time_in_seconds = 120; s.Solve(m, CB())
def score(t):
    x = np.array([ord(ch) - 65 for ch in t]); i = ((x[:-3] * 26 + x[1:-2]) * 26 + x[2:-1]) * 26 + x[3:]; return float(qg[i].sum())
res = []
for so in sols:
    inv = {v: k for k, v in so.items()}
    t = "".join(inv[(kv[i] + so[CT[i]]) % 26] if False else inv[((so[CT[i]] - kv[i]) if model == "vig1" else (kv[i] - so[CT[i]])) % 26] for i in range(97))
    res.append((score(t), t))
res.sort(reverse=True); print("solutions", len(sols))
for sc, t in res[:3]: print(round(sc, 1), t)
