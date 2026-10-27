#!/usr/bin/env python3
"""Iteration 35 control: random 100-value key stream, cribs encrypted under vig1/beau1 (random alphabet) or a fixed
tableau; drop mode corrupts one crib-position CT letter, shift mode uses the key value at position i+d for the
BERLINCLOCK rows. Screen must report the planted model."""
import sys, random
sys.path.insert(0, "iterations"); sys.path.insert(0, "/mnt/project-files/k4/tools")
import keygen as KG
from it35_keygen_route_err import Screen
AZ = KG.AZ; rng = random.Random(35); ok = tot = 0
for trial in range(48):
    mode, d = (("drop", 0), ("shift", 1), ("shift", -2))[trial % 3]; model = ("vig1", "beau1", "fixed")[(trial // 3) % 3]
    k = [rng.randrange(26) for _ in range(100)]; ct = list(KG.CT); P = KG.crib_pairs(KG.CT)
    al = list(range(26)); rng.shuffle(al); inv = {v: i for i, v in enumerate(al)}
    for t, (i, p, c) in enumerate(P):
        kv = k[i - 1 + (d if t >= 13 else 0)]
        if model == "vig1": ct[i - 1] = AZ[inv[(al[AZ.index(p)] + kv) % 26]]
        elif model == "beau1": ct[i - 1] = AZ[inv[(kv - al[AZ.index(p)]) % 26]]
        else: ct[i - 1] = AZ[(AZ.index(p) + kv) % 26]                       # AZ/AZ Vigenere tableau
    if mode == "drop":
        r = rng.randrange(24); i = P[r][0] - 1; ct[i] = AZ[(AZ.index(ct[i]) + rng.randrange(1, 26)) % 26]
    S = Screen("".join(ct), mode, d); S.feed([k], ["plant"])
    f = any(any(h[0] == model or (model == "fixed" and h[0] == "fixed") for h in hs) for _, hs in S.hits); ok += f; tot += 1
    print(f"{mode} d={d} {model}: found={f}", flush=True)
print(f"controls recovered {ok}/{tot}")
