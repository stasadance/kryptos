#!/usr/bin/env python3
"""it20 driver: make planted 7+10 / 7+8 controls from English (cribs inserted), random nulls, run sa2p."""
import random, re, subprocess, sys
LAM = "8"; BIN = "./sa2h"
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; SP = "/tmp/claude-0/-home-user-kryptos/046a83fd-aa4b-57f6-97e0-639b3d9e1ef4/scratchpad/it05/corpus/pg1342.txt"
txt = re.sub("[^A-Z]", "", open(SP).read().upper())
def control(seed, L1, L2, beau):
    r = random.Random(seed); s = r.randrange(len(txt) - 100); pt = list(txt[s:s + 97])
    pt[21:34] = "EASTNORTHEAST"; pt[63:74] = "BERLINCLOCK"
    al = list(range(26)); r.shuffle(al); a = [r.randrange(26) for _ in range(L1)]; b = [r.randrange(26) for _ in range(L2)]
    inv = {v: i for i, v in enumerate(al)}; ct = ""
    for i, p in enumerate(pt):
        k = a[i % L1] + b[i % L2]; v = (k - al[AZ.index(p)]) % 26 if beau else (al[AZ.index(p)] + k) % 26
        ct += AZ[inv[v]]
    return "".join(pt), ct
def run(ct, L1, L2, m, R, IT, seed):
    out = subprocess.run([BIN, str(L1), str(L2), m, ct, str(R), str(IT), str(seed), LAM], capture_output=True, text=True).stdout
    return max((float(l.split()[0]), l.split()[1]) for l in out.splitlines())
if __name__ == "__main__":
    kind, L1, L2, m, n, R, IT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
    for s in range(n):
        if kind == "ctrl":
            pt, ct = control(100 + s, L1, L2, m == "b"); sc, dec = run(ct, L1, L2, m, R, IT, s)
            acc = sum(x == y for x, y in zip(pt, dec)) / 97; print(f"ctrl {s} {sc:.1f} acc={acc:.2f} {dec}", flush=True)
        elif kind == "null":
            r = random.Random(500 + s); ct = "".join(r.choice(AZ) for _ in range(97)); sc, dec = run(ct, L1, L2, m, R, IT, s)
            print(f"null {s} {sc:.1f} {dec}", flush=True)
        else:
            ct = open("../../data/ciphertext.txt").read().strip(); sc, dec = run(ct, L1, L2, m, R, IT, s); print(f"K4 {s} {sc:.1f} {dec}", flush=True)
