#!/usr/bin/env python3
"""Iteration 23c: it23's 45-model running-key scan with ONE crib letter allowed wrong (scan_err drops each of the 24
crib rows in turn). Answers "what if one crib letter (e.g. a Sanborn typo, or the 2020 NORTHEAST order) is off".
Usage: python3 iterations/it23c_scan_err.py --control SRC ENG | --null SRC | text1 [text2 ...]"""
import sys, time, random
import numpy as np
sys.path.insert(0, "iterations")
import it23_scan as S
from it23_scan import CT, AZ, MODELS2, norm, arr, scan_err, rescan
def run(ct, txt, cap13=30000, cap2=4096):
    res = scan_err(arr(ct), arr(txt), len(MODELS2), cap13, cap2)
    hits = np.argwhere(res > 0); und = int((res == -1).sum())
    return [(int(o), MODELS2[m], int(res[o, m]) - 1) for o, m in hits], und, res.shape[0]
if __name__ == "__main__":
    args = sys.argv[1:]; files = [a for a in args if not a.startswith("--")]
    if "--control" in args:
        src = norm(open(files[0], errors="ignore").read()); eng = norm(open(files[1], errors="ignore").read())
        rng = random.Random(23); nf = 0; picks = rng.sample(range(len(MODELS2)), 12)
        for m in picks:
            ctl, o = S.plant(src, eng, m, rng)
            r = rng.randrange(24); i = S.POS[r]                     # corrupt the ciphertext at one crib position
            ctl = ctl[:i] + AZ[(AZ.index(ctl[i]) + rng.randrange(1, 26)) % 26] + ctl[i + 1:]
            hits, und, n = run(ctl, src[o - 2000:o + 2000])
            found = any(h[0] == 2000 and h[1] == MODELS2[m] for h in hits); nf += found
            print(f"control {MODELS2[m]} bad row {r}: found={found} other hits={len(hits) - found} undecided={und} of {n}", flush=True)
        print(f"controls recovered {nf}/{len(picks)}"); sys.exit()
    if "--null" in args:
        src = norm(open(files[0], errors="ignore").read()); rng = random.Random(5)
        for t in range(5):
            o = rng.randrange(len(src) - 20000); ct = "".join(rng.choice(AZ) for _ in range(97))
            hits, und, n = run(ct, src[o:o + 20000])
            print(f"null {t}: {len(hits)} passes of {n * len(MODELS2)} (offset, model), undecided={und}", flush=True)
        sys.exit()
    for f in files:
        raw = norm(open(f, errors="ignore").read())
        for d, txt in (("fwd", raw), ("rev", raw[::-1])):
            t = time.time(); hits, und, n = run(CT, txt)
            print(f"{f} {d}: {n} offsets x {len(MODELS2)} models, err-hits={len(hits)}, undecided={und}, {time.time()-t:.0f}s", flush=True)
            for h in hits: print("  HIT", d, h, txt[h[0]:h[0] + 97], flush=True)
