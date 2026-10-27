#!/usr/bin/env python3
"""Iteration 25: numeric key read from the K3 transposition "matrix" (NSA 2007 summary Fig. 21/22: the extraction
order of K3's 86 columns written 7 wide). Motivation: WaPo 14 Jan 1990 puts K3 and K4 in one "modern system" half
(it22); Sanborn's "matrix codes". Streams: the 86 numbers read by rows, by columns (down/up), reversed, cycled;
key value = n mod 26 and (n-1) mod 26. All cyclic offsets, all 45 it23 role/form models (key role AZ = numeric value).
Exact linear crib test with all-different. Control: planted stream recovered."""
import sys, random
import numpy as np
sys.path.insert(0, "iterations")
from it23_scan import test_one, MODELS2, POS, arr, CT, AZ, RK
from it24_autokey_mixed import plant as _p
# Fig. 21: 13 rows x 7 columns, last row has 37 and 86 only
cols = [list(range(49, 36, -1)), list(range(12, 0, -1)) + [86], list(range(61, 49, -1)), list(range(24, 12, -1)),
        list(range(73, 61, -1)), list(range(36, 24, -1)), list(range(85, 73, -1))]
grid = [[cols[c][r] if r < len(cols[c]) else None for c in range(7)] for r in range(13)]
rows = [v for r in grid for v in r if v is not None]
colsdown = [v for c in cols for v in c]
colsup = [v for c in cols for v in c[::-1]]
assert sorted(rows) == list(range(1, 87))
STREAMS = {"rows": rows, "rows_rev": rows[::-1], "cols_down": colsdown, "cols_up": colsup, "cols_down_rev": colsdown[::-1]}
def stream_vals(s, sub): return [(v - sub) % 26 for v in s]
def test_stream(ct, vals, models):
    hits = []; n = len(vals); c = arr(ct)
    for o in range(n):
        key = np.array([vals[(o + p) % n] for p in POS], dtype=np.int64)
        for m in models:
            if test_one(c, key, m, 3000000, 65536) == 1: hits.append((o, MODELS2[m]))
    return hits
NUMERIC = [m for m in range(len(MODELS2)) if RK[m] == 1]   # key valued as a number (AZ index == value)
if __name__ == "__main__":
    rng = random.Random(5)
    # control: plant rows stream (sub=1) at offset 17 under several numeric-key models with a random alphabet
    from it23_scan import RC, RP, FM, KA
    vals = stream_vals(rows, 1); ok = 0
    for m in NUMERIC:
        al = list(range(26)); rng.shuffle(al); inv = {v: i for i, v in enumerate(al)}
        val = lambda ro, ch: al[AZ.index(ch)] if ro == 0 else (AZ.index(ch) if ro == 1 else KA.index(ch))
        pt = list(("THEREWASNOTHINGTOSEEBUTSANDANDSTONEFORMILESINEVERYDIRECTION" * 2)[:97])
        for s0, w in {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}.items(): pt[s0:s0 + len(w)] = w
        ct = []
        for i, p in enumerate(pt):
            kv = vals[(17 + i) % 86]; pv = val(RP[m], p); f = FM[m]
            cv = ((pv + kv) if f == 0 else ((kv - pv) if f == 1 else (pv - kv))) % 26
            ct.append(AZ[inv[cv]] if RC[m] == 0 else (AZ[cv] if RC[m] == 1 else KA[cv]))
        ok += (17, MODELS2[m]) in test_stream("".join(ct), vals, [m])
    print(f"control: {ok}/{len(NUMERIC)} planted numeric-key models recovered", flush=True)
    nulls = ["".join(rng.choice(AZ) for _ in range(97)) for _ in range(5)]
    for name, s in STREAMS.items():
        for sub in (0, 1):
            v = stream_vals(s, sub); h = test_stream(CT, v, range(len(MODELS2)))
            nh = [len(test_stream(c, v, range(len(MODELS2)))) for c in nulls]
            print(f"{name} sub={sub}: K4 hits {len(h)} {h[:5]}  null hits {nh}", flush=True)
