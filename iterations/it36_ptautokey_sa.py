#!/usr/bin/env python3
"""Iteration 36 (H-2103): plaintext-autokey with lag L (6..12) under ONE unknown mixed alphabet, decided from the full
text. For L <= 13 every residue mod L meets the EASTNORTHEAST crib, so the alphabet alone fixes the whole plaintext
(propagate forward from the crib and backward to position 0). Search: simulated annealing over the alphabet
(swap moves), score = quadgrams(plaintext) - W * (BERLINCLOCK mismatches + violated ENE-internal relations).
Key value of the letter L back: 'self' = a(p) (Quagmire-style), 'AZ' or 'KA' index. Forms: vig a(c)=a(p)+K,
beau a(c)=K-a(p), var a(c)=a(p)-K.
Usage: python3 iterations/it36_ptautokey_sa.py QG.bin --control | --k4 [restarts] [iters]"""
import sys, random, time
import numpy as np
from numba import njit
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
K4 = open("data/ciphertext.txt").read().strip()
KAI = np.array([KA.index(ch) for ch in AZ], dtype=np.int64)   # KA index of AZ letter
KAL = np.array([AZ.index(ch) for ch in KA], dtype=np.int64)   # AZ letter at KA index
ENE = np.array([AZ.index(c) for c in "EASTNORTHEAST"], dtype=np.int64)
BC = np.array([AZ.index(c) for c in "BERLINCLOCK"], dtype=np.int64)
qg = np.fromfile(sys.argv[1], dtype=np.float32)

@njit(cache=True)
def decrypt(c, a, inv, L, form, kr, p):
    n = c.shape[0]; bad = 0
    for i in range(n): p[i] = -1
    for t in range(13): p[21 + t] = ENE[t]
    for i in range(21 + L, 34):                                  # relations inside the crib
        pp = p[i - L]; K = a[pp] if kr == 0 else (pp if kr == 1 else KAI[pp])
        v = (a[p[i]] + K) % 26 if form == 0 else ((K - a[p[i]]) % 26 if form == 1 else (a[p[i]] - K) % 26)
        if v != a[c[i]]: bad += 1
    for i in range(34, n):
        pp = p[i - L]; K = a[pp] if kr == 0 else (pp if kr == 1 else KAI[pp])
        ap = (a[c[i]] - K) % 26 if form == 0 else ((K - a[c[i]]) % 26 if form == 1 else (a[c[i]] + K) % 26)
        p[i] = inv[ap]
    for j in range(20, -1, -1):
        i = j + L
        K = (a[c[i]] - a[p[i]]) % 26 if form == 0 else ((a[c[i]] + a[p[i]]) % 26 if form == 1 else (a[p[i]] - a[c[i]]) % 26)
        p[j] = inv[K] if kr == 0 else (K if kr == 1 else KAL[K])
    for t in range(11):
        if p[63 + t] != BC[t]: bad += 1
    return bad

@njit(cache=True)
def score(c, a, inv, L, form, kr, p, qg, W):
    bad = decrypt(c, a, inv, L, form, kr, p); s = 0.0
    for i in range(c.shape[0] - 3): s += qg[((p[i] * 26 + p[i + 1]) * 26 + p[i + 2]) * 26 + p[i + 3]]
    return s - W * bad, bad, s

@njit(cache=True)
def anneal(c, L, form, kr, qg, iters, seed, W, T0=20.0):
    np.random.seed(seed)
    a = np.random.permutation(26).astype(np.int64); inv = np.empty(26, np.int64)
    for x in range(26): inv[a[x]] = x
    p = np.empty(c.shape[0], np.int64)
    cur, bad, q = score(c, a, inv, L, form, kr, p, qg, W); best = cur; ba = a.copy()

    for it in range(iters):
        T = T0 * (1.0 - it / iters) + 0.2
        x = np.random.randint(26); y = np.random.randint(26)
        if x == y: continue
        a[x], a[y] = a[y], a[x]; inv[a[x]] = x; inv[a[y]] = y
        new, nb, nq = score(c, a, inv, L, form, kr, p, qg, W)
        if new >= cur or np.random.random() < np.exp((new - cur) / T):
            cur = new
            if cur > best: best = cur; ba[:] = a
        else:
            a[x], a[y] = a[y], a[x]; inv[a[x]] = x; inv[a[y]] = y
    for x in range(26): inv[ba[x]] = x
    s, bad, q = score(c, ba, inv, L, form, kr, p, qg, W)
    return s, bad, q, ba, p.copy()

def run(ct, L, form, kr, R, iters, W=40.0, T0=20.0):
    c = np.array([AZ.index(ch) for ch in ct], dtype=np.int64); best = None
    for r in range(R):
        s, bad, q, a, p = anneal(c, L, form, kr, qg, iters, r * 7919 + L, W, T0)
        if best is None or s > best[0]: best = (s, bad, q, "".join(AZ[x] for x in p))
    return best

def plant(L, form, kr, rng, eng):
    a = list(range(26)); rng.shuffle(a); inv = {v: k for k, v in enumerate(a)}
    o = rng.randrange(len(eng) - 200); pt = list(eng[o:o + 97]); pt[21:34] = "EASTNORTHEAST"; pt[63:74] = "BERLINCLOCK"
    P = [AZ.index(ch) for ch in pt]; out = []
    for i in range(97):
        if i < L: K = rng.randrange(26)          # primer key values
        else:
            pp = P[i - L]; K = a[pp] if kr == 0 else (pp if kr == 1 else KAI[pp])
        v = (a[P[i]] + K) % 26 if form == 0 else ((K - a[P[i]]) % 26 if form == 1 else (a[P[i]] - K) % 26)
        out.append(AZ[inv[v]])
    return "".join(out), "".join(pt)

if __name__ == "__main__":
    a = sys.argv[2:]; R = int(a[1]) if len(a) > 1 else 8; iters = int(a[2]) if len(a) > 2 else 400000
    FORMS = ("vig", "beau", "var"); KR = ("self", "AZ", "KA")
    if a[0] == "--control":
        import re
        eng = re.sub("[^A-Z]", "", open("/tmp/claude-0/it27/test.txt").read().upper()); rng = random.Random(36); ok = 0; n = 0
        for L in (6, 8, 10, 12):
            for form in range(3):
                kr = rng.randrange(3); ct, pt = plant(L, form, kr, rng, eng)
                s, bad, q, dec = run(ct, L, form, kr, R, iters)
                acc = sum(x == y for x, y in zip(dec[L:], pt[L:])) / (97 - L); ok += acc > 0.8; n += 1
                print(f"control L={L} {FORMS[form]}/{KR[kr]}: score {s:.1f} bad {bad} q {q:.1f} acc {acc:.2f} {dec}", flush=True)
        print(f"controls recovered {ok}/{n}"); sys.exit()
    for L in range(6, 13):
        for form in range(3):
            for kr in range(3):
                t = time.time(); s, bad, q, dec = run(K4, L, form, kr, R, iters)
                print(f"K4 L={L} {FORMS[form]}/{KR[kr]}: score {s:.1f} bad {bad} q {q:.1f} {dec} {time.time()-t:.0f}s", flush=True)
