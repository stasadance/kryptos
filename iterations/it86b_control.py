#!/usr/bin/env python3
"""it86 planted controls: plant Quagmire-I (keyed PT alphabet, AZ CT) with a keygen stream, then (a) corrupt one crib
letter, (b) shift BERLINCLOCK's key by -1/+1. Run the it86 hash logic over a small alphabet list containing the plant
alphabet plus 2000 decoys. Expect the plant to hit in the matching variant."""
import sys, random
import numpy as np
sys.path.insert(0, 'iterations'); sys.path.insert(0, 'tools')
import it82_w1a3_hash as B
import keygen as KG
AZ = B.AZ
rng = np.random.default_rng(86); WH = rng.integers(1, 2**62, size=24, dtype=np.int64)
def hsub(V, cols):
    V = V[:, cols]; D = (V[:, 1:] - V[:, :1]) % 26; return (D.astype(np.int64) * WH[:D.shape[1]]).sum(1)
POS1 = list(range(21, 34)); POS2 = list(range(63, 74)); PT = 'EASTNORTHEAST' + 'BERLINCLOCK'
streams = [k for fam in (KG.families(), KG.twokey_families()) for f, par, k, _ in fam]
r = random.Random(7); ok = tot = 0
def keyed(w): s = ''.join(dict.fromkeys(w + AZ)); return s
for trial in range(6):
    k = streams[r.randrange(len(streams))]; alph = keyed(r.choice(['KRYPTOS', 'PALIMPSEST', 'ABSCISSA', 'SANBORN', 'BERLIN', 'CLOCK']))
    mode = ['del', 'shift'][trial % 2]; sh = r.choice([-1, 1]) if mode == 'shift' else 0; d = r.randrange(24)
    kv = [k[i] % 26 for i in POS1 + [j + sh for j in POS2]]
    C = [AZ[(alph.index(p) + kk) % 26] for p, kk in zip(PT, kv)]
    if mode == 'del': C[d] = AZ[(AZ.index(C[d]) + 1 + r.randrange(25)) % 26]
    cols = [c for c in range(24) if c != d] if mode == 'del' else list(range(24))
    lib = np.array([[k[i] % 26 for i in POS1 + [j + sh for j in POS2]]]); H = set(hsub(lib, cols).tolist())
    # full library hash would contain this; test the CT-side vector for plant alphabet vs decoys
    decoys = [keyed(''.join(r.sample(AZ, 6))) for _ in range(2000)]
    cand = [alph] + decoys
    PAi = np.array([[a.index(x) for x in PT] for a in cand]); CAi = np.array([[AZ.index(x) for x in C]] * len(cand))
    V = (CAi - PAi) % 26; h = hsub(V, cols); hit = [cand[j] for j in range(len(cand)) if h[j] in H]
    tot += 1; ok += alph in hit
    # also: unmodified (no tolerance) hash must miss for del-mode
    miss = hsub(V[:1], list(range(24)))[0] not in set(hsub(lib, list(range(24))).tolist())
    print(trial, mode, d if mode == 'del' else sh, 'plant hit' if alph in hit else 'MISS', 'decoy hits', len(hit) - (alph in hit), 'exact-hash miss' if miss else 'exact-hash hit')
print(f'controls {ok}/{tot}')
