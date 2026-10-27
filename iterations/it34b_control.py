#!/usr/bin/env python3
"""Iteration 34 control: plant random key letters at the 24 crib rows, encrypt the cribs under vig1/beau1 (random
alphabet, AZ/KA numbering) or a fixed KA/AZ tableau, corrupt ONE crib-position ciphertext letter (drop mode), then
check Err.latin + Err.deep report the planted model. Also shift mode: Err with cidx shifted is fed the key letters
read at the shifted positions (the plant is built on the shifted key)."""
import sys, random
import numpy as np
sys.path.insert(0, "iterations")
from it34_transkey_err import Err, TK
AZ = TK.AZ; rng = random.Random(34)
def enc(pairs, x, model, nb):
    A, d = TK.NUMB[nb]; al = list(range(26)); rng.shuffle(al); inv = {v: i for i, v in enumerate(al)}
    ct = list(TK.CT0)
    for t, (i, p, c) in enumerate(pairs):
        k = (A.index(AZ[x[t]]) + d) % 26
        cv = (al[AZ.index(p)] + k) % 26 if model == "vig1" else (k - al[AZ.index(p)]) % 26
        ct[i - 1] = AZ[inv[cv]]
    return "".join(ct)
ok = tot = 0
base = TK.Ctx(TK.CT0)
for trial in range(40):
    model = ("vig1", "beau1")[trial % 2]; nb = list(TK.NUMB)[trial % 4]
    for _ in range(1000):
        x = np.array([rng.randrange(26) for _ in range(24)])
        ct = enc(base.pairs, x, model, nb)
        if len(set(ct)) > 1: break
    r = rng.randrange(24); i = base.pairs[r][0] - 1
    ct = ct[:i] + AZ[(AZ.index(ct[i]) + rng.randrange(1, 26)) % 26] + ct[i + 1:]
    c = Err(ct, "drop")
    passed = bool(c.latin(x[None, :])[0]); h = c.deep(x) if passed else []
    f = any(t[0] == model and t[1] == nb for t in h); ok += f; tot += 1
    print(f"drop {model} {nb} bad row {r}: gate={passed} found={f} hits={h[:3]}", flush=True)
for d in (-1, 1):
    for trial in range(10):
        model = ("vig1", "beau1")[trial % 2]; nb = list(TK.NUMB)[trial % 4]
        x = np.array([rng.randrange(26) for _ in range(24)]); ct = enc(base.pairs, x, model, nb)
        c = Err(ct, "shift", d)        # x = key letters at the (shifted) key positions, cribs at carved CT positions
        passed = bool(c.latin(x[None, :])[0]); h = c.deep(x) if passed else []
        f = any(t[0] == model and t[1] == nb for t in h); ok += f; tot += 1
        print(f"shift {d} {model} {nb}: gate={passed} found={f}", flush=True)
print(f"controls recovered {ok}/{tot}")
