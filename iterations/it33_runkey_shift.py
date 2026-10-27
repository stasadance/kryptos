#!/usr/bin/env python3
"""Iteration 33: running key under one unknown alphabet (it23's 45 models) when ONE ciphertext letter was omitted or
inserted between the cribs (as K2's missing S; H-708). Then the key index of the BERLINCLOCK rows is shifted by
d in {-2,-1,+1,+2} relative to the carved position, while the ciphertext letters stay as carved.
(A slip before position 21 or after 73 is absorbed by the free offset, so only the between-crib case is new.)
Usage: python3 iterations/it33_runkey_shift.py --control SRC ENG | --null SRC | text1 [text2 ...]"""
import sys, time, random
import numpy as np
from numba import njit, prange
sys.path.insert(0, "iterations")
import it23_scan as S
from it23_scan import CT, AZ, MODELS2, norm, arr, test_one, POS
SHIFTS = (-2, -1, 1, 2)
@njit(parallel=True, cache=True)
def scan_k(ct, txt, kpos, nmodels, cap13, cap2):
    nofs = txt.shape[0] - 100
    out = np.zeros((max(nofs, 0), nmodels), dtype=np.int8)
    for o in prange(2, max(nofs, 0)):
        key = np.empty(24, dtype=np.int64)
        for r in range(24): key[r] = txt[o + kpos[r]]
        for m in range(nmodels): out[o, m] = test_one(ct, key, m, cap13, cap2)
    return out
def kpos(d):
    k = POS.copy(); k[13:] += d; return k
def plant(src, eng, model, rng, d):
    """S.plant with BERLINCLOCK at original position 63+d, so that it lands at carved 63 after the slip."""
    rc, rp, rk = S.RC[model], S.RP[model], S.RK[model]; f = S.FM[model]
    al = list(range(26)); rng.shuffle(al); inv = {v: i for i, v in enumerate(al)}
    val = lambda ro, ch: al[AZ.index(ch)] if ro == 0 else (AZ.index(ch) if ro == 1 else S.KA.index(ch))
    o = rng.randrange(5000, len(src) - 5200); po = rng.randrange(len(eng) - 200)
    pt = list(eng[po:po + 99])
    pt[21:34] = "EASTNORTHEAST"; pt[63 + d:74 + d] = "BERLINCLOCK"
    out = []
    for i, p in enumerate(pt):
        kv = val(rk, src[o + i]); pv = val(rp, p)
        cv = ((pv + kv) if f == 0 else ((kv - pv) if f == 1 else (pv - kv))) % 26
        out.append(AZ[inv[cv]] if rc == 0 else (AZ[cv] if rc == 1 else S.KA[cv]))
    return "".join(out), o
def run(ct, txt, d):
    res = scan_k(arr(ct), arr(txt), kpos(d), len(MODELS2), 30000, 4096)
    return [(int(o), MODELS2[m]) for o, m in np.argwhere(res == 1)], int((res == -1).sum()), res.shape[0]
if __name__ == "__main__":
    args = sys.argv[1:]; files = [a for a in args if not a.startswith("--")]
    if "--control" in args:
        src = norm(open(files[0], errors="ignore").read()); eng = norm(open(files[1], errors="ignore").read())
        rng = random.Random(33); nf = 0; tot = 0
        for d in SHIFTS:
            for m in rng.sample(range(len(MODELS2)), 3):
                ctl, o = plant(src, eng, m, rng, d)                # true key aligned with original positions
                i = rng.randrange(35, 61 + min(d, 0))              # then CT letter(s) between the cribs slip
                if d > 0: ctl = (ctl[:i] + ctl[i + d:])[:97]                                         # omitted
                else: ctl = (ctl[:i] + "".join(rng.choice(AZ) for _ in range(-d)) + ctl[i:])[:97]     # inserted
                assert len(ctl) == 97
                hits, und, n = run(ctl, src[o - 2000:o + 2000], d)
                f = any(h[0] == 2000 and h[1] == MODELS2[m] for h in hits); nf += f; tot += 1
                print(f"control d={d} {MODELS2[m]}: found={f} other={len(hits) - f} und={und}", flush=True)
        print(f"controls recovered {nf}/{tot}"); sys.exit()
    if "--null" in args:
        src = norm(open(files[0], errors="ignore").read()); rng = random.Random(6)
        for t in range(4):
            o = rng.randrange(len(src) - 20000); ct = "".join(rng.choice(AZ) for _ in range(97))
            for d in SHIFTS:
                hits, und, n = run(ct, src[o:o + 20000], d)
                print(f"null {t} d={d}: {len(hits)} passes of {n * len(MODELS2)}, und={und}", flush=True)
        sys.exit()
    for f in files:
        raw = norm(open(f, errors="ignore").read())
        for dn, txt in (("fwd", raw), ("rev", raw[::-1])):
            for d in SHIFTS:
                t = time.time(); hits, und, n = run(CT, txt, d)
                print(f"{f} {dn} d={d}: {n} offsets x {len(MODELS2)}, hits={len(hits)}, und={und}, {time.time()-t:.0f}s", flush=True)
                for h in hits: print("  HIT", dn, d, h, txt[h[0]:h[0] + 100], flush=True)
