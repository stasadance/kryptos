#!/usr/bin/env python3
"""Iteration 24: plaintext- and ciphertext-autokey under one unknown mixed alphabet, every lag, all 45 role/form
models of it23 (cipher/plain/key letters valued by the unknown alphabet a, AZ or KA; Vig/Beau/variant).
CT-autokey: k_i = c_{i-L}; rows with i-L < 0 (primer) dropped. PT-autokey: k_i = p_{i-L}; only rows where p_{i-L}
is a crib letter are kept. Exact linear test (it23_scan.test_one). Null: 200 random ciphertexts per (L, mode)."""
import sys, random
import numpy as np
sys.path.insert(0, "iterations")
from it23_scan import test_one, MODELS2, POS, PT, arr, CT, AZ
CR = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}; PTPOS = {s + j: p for s, w in CR.items() for j, p in enumerate(w)}
def keys(ct, L, mode):
    key = np.zeros(24, dtype=np.int64); mask = np.zeros(24, dtype=np.int64)
    for r in range(24):
        j = POS[r] - L
        if mode == "ct" and j >= 0: key[r] = AZ.index(ct[j]); mask[r] = 1
        if mode == "pt" and j in PTPOS: key[r] = AZ.index(PTPOS[j]); mask[r] = 1
    return key, mask
def passes(ct, L, mode, m):
    key, mask = keys(ct, L, mode)
    if mask.sum() < 3: return None
    return test_one(arr(ct), key, m, 3000000, 65536, -1, mask)
def plant(L, mode, m, rng):
    from it23_scan import RC, RP, RK, FM, KA
    rc, rp, rk, f = RC[m], RP[m], RK[m], FM[m]
    al = list(range(26)); rng.shuffle(al); inv = {v: i for i, v in enumerate(al)}
    val = lambda ro, ch: al[AZ.index(ch)] if ro == 0 else (AZ.index(ch) if ro == 1 else KA.index(ch))
    eng = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOGWHILETHEFARMERSLEPTUNDERANOLDOAKTREENEARTHERIVERBANKANDDREAMTOFGOLDENFIELDSOFWHEATANDCORN"
    pt = list((eng * 2)[:97])
    for s0, w in CR.items(): pt[s0:s0 + len(w)] = w
    prim = [rng.choice(AZ) for _ in range(L)]; ct = []
    for i, p in enumerate(pt):
        k = (prim[i] if i < L else (ct[i - L] if mode == "ct" else pt[i - L]))
        kv = val(rk, k); pv = val(rp, p)
        cv = ((pv + kv) if f == 0 else ((kv - pv) if f == 1 else (pv - kv))) % 26
        ct.append(AZ[inv[cv]] if rc == 0 else (AZ[cv] if rc == 1 else KA[cv]))
    return "".join(ct)
if __name__ == "__main__":
    rng = random.Random(11)
    # controls: a sample of (L, mode, model)
    ok = tot = 0
    for mode in ("ct", "pt"):
        for L in (1, 7, 13, 40, 70) if mode == "ct" else (1, 4, 7, 31, 45):
            for m in range(0, len(MODELS2), 4):
                r = passes(plant(L, mode, m, rng), L, mode, m)
                if r is None: continue
                tot += 1; ok += (r == 1)
    print(f"controls {ok}/{tot}", flush=True)
    nulls = ["".join(rng.choice(AZ) for _ in range(97)) for _ in range(100)]
    for mode in ("ct", "pt"):
        for L in range(1, 97):
            k4 = [passes(CT, L, mode, m) for m in range(len(MODELS2))]
            if all(v is None for v in k4): continue
            hitm = [MODELS2[m] for m, v in enumerate(k4) if v == 1]; und = sum(1 for v in k4 if v == -1)
            nr = [sum(1 for c in nulls if passes(c, L, mode, m) == 1) for m in range(len(MODELS2)) if k4[m] is not None]
            neq = int(keys(CT, L, mode)[1].sum())
            print(f"{mode} L={L:2d} rows={neq:2d} K4 hits={len(hitm)} {hitm[:6]} und={und} null mean pass={np.mean(nr)/len(nulls):.3f} max={max(nr)/len(nulls):.2f}", flush=True)
