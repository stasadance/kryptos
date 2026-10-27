#!/usr/bin/env python3
"""Iteration 38: propagation-aware beam search for plaintext-autokey with lag L under ONE unknown alphabet a,
key value = AZ or KA index of the plaintext letter L back; forms vig a(c)=a(p)+K and var a(c)=a(p)-K (difference
relations only). Instead of guessing the alphabet, branch on PLAINTEXT letters outward from EASTNORTHEAST
(forward 34..96, then backward 20..0); every step adds one difference relation a(c_i) - a(p_i) = +-K_i, kept in an
offset union-find over the 26 letters (a(x) = a(root) + off(x)); a state dies on a cycle conflict or when two letters
in one component get the same value. BERLINCLOCK letters are forced. Score = quadgrams of the determined text.
Usage: python3 iterations/it38_autokey_beam.py QG.bin --control [B] | --k4 [B]"""
import sys, random, re, time
import numpy as np
from numba import njit
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
KAI = np.array([KA.index(ch) for ch in AZ], dtype=np.int64)
ENE = np.array([AZ.index(c) for c in "EASTNORTHEAST"], dtype=np.int64)
BC = np.array([AZ.index(c) for c in "BERLINCLOCK"], dtype=np.int64)
qg = np.fromfile(sys.argv[1], dtype=np.float32)

@njit(cache=True)
def find(root, off, x):
    o = 0
    while root[x] != x:
        o += off[x]; x = root[x]
    return x, o % 26

@njit(cache=True)
def add_rel(root, off, x, y, d):
    """impose a(x) - a(y) = d (mod 26). returns False on conflict. union by attaching ry under rx."""
    rx, ox = find(root, off, x); ry, oy = find(root, off, y)
    if rx == ry:
        return (ox - oy - d) % 26 == 0
    # a(x) = a(rx)+ox, a(y) = a(ry)+oy ; a(ry) = a(rx) + ox - oy - d
    delta = (ox - oy - d) % 26
    # all-different inside the merged component
    seen = np.zeros(26, np.bool_)
    for z in range(26):
        rz, oz = find(root, off, z)
        if rz == rx: seen[oz] = True
    for z in range(26):
        rz, oz = find(root, off, z)
        if rz == ry:
            v = (oz + delta) % 26
            if seen[v]: return False
    root[ry] = rx; off[ry] = delta
    return True

@njit(cache=True)
def rel(c, pi, pk, form, kr):
    """relation for a(c) - a(p_i) = +-K with K from letter pk; returns (x, y, d) meaning a(x)-a(y)=d"""
    K = pk if kr == 1 else KAI[pk]
    return c, pi, (K if form == 0 else (26 - K) % 26)

@njit(cache=True)
def qscore(p, i):
    """sum of quadgrams fully inside determined letters that include position i"""
    s = 0.0
    for j in range(i - 3, i + 1):
        if j < 0 or j + 3 >= p.shape[0]: continue
        ok = True
        for t in range(4):
            if p[j + t] < 0: ok = False
        if ok: s += qg[((p[j] * 26 + p[j + 1]) * 26 + p[j + 2]) * 26 + p[j + 3]]
    return s

@njit(cache=True)
def beam(c, L, form, kr, B, truth=np.zeros(0, np.int64)):
    n = c.shape[0]
    P = -np.ones((1, n), np.int64); R = np.empty((1, 26), np.int64); O = np.zeros((1, 26), np.int64); S = np.zeros(1)
    for x in range(26): R[0, x] = x
    for t in range(13): P[0, 21 + t] = ENE[t]
    for i in range(21 + L, 34):                                   # ENE-internal relations
        x, y, d = rel(c[i], P[0, i], P[0, i - L], form, kr)
        if not add_rel(R[0], O[0], x, y, d): return -1e9, P[0]
    for t in range(11): P[0, 63 + t] = BC[t]
    for i in range(63 + L, 74):                                   # BERLINCLOCK-internal relations
        x, y, d = rel(c[i], P[0, i], P[0, i - L], form, kr)
        if not add_rel(R[0], O[0], x, y, d): return -1e9, P[0]
    order = []
    lo, hi = 34, 62
    while lo <= hi:                                               # fill the gap from both cribs inwards
        order.append(lo); lo += 1
        if lo <= hi: order.append(hi); hi -= 1
    order += list(range(74, n)) + list(range(20, -1, -1))
    for i in order:
        m = P.shape[0]
        NP = np.empty((m * 26, n), np.int64); NR = np.empty((m * 26, 26), np.int64); NO = np.empty((m * 26, 26), np.int64)
        NS = np.empty(m * 26); k = 0
        for s in range(m):
            for letter in range(26):
                r = R[s].copy(); o = O[s].copy(); p = P[s].copy(); p[i] = letter; good = True
                for j in (i, i + L):                              # every relation that is now fully known
                    if j - L < 0 or j >= n or p[j] < 0 or p[j - L] < 0: continue
                    x, y, d = rel(c[j], p[j], p[j - L], form, kr)
                    if not add_rel(r, o, x, y, d): good = False; break
                if not good: continue
                NP[k] = p; NR[k] = r; NO[k] = o; NS[k] = S[s] + qscore(p, i); k += 1
        if k == 0: return -1e9, P[0]
        idx = np.argsort(-NS[:k])
        if truth.shape[0] > 0:                                    # diagnostics: rank of the true partial
            for rnk in range(k):
                q = NP[idx[rnk]]; same = True
                for t in range(n):
                    if q[t] >= 0 and q[t] != truth[t]: same = False; break
                if same:
                    print(i, rnk); break
        idx = idx[:B]
        P = NP[idx]; R = NR[idx]; O = NO[idx]; S = NS[idx]
    return S[0], P[0]

def plant(L, form, kr, rng, eng):
    a = list(range(26)); rng.shuffle(a); inv = {v: k for k, v in enumerate(a)}
    o = rng.randrange(len(eng) - 200); pt = list(eng[o:o + 97]); pt[21:34] = "EASTNORTHEAST"; pt[63:74] = "BERLINCLOCK"
    P = [AZ.index(ch) for ch in pt]; out = []
    for i in range(97):
        if i < L: K = rng.randrange(26)
        else: K = P[i - L] if kr == 1 else int(KAI[P[i - L]])
        v = (a[P[i]] + K) % 26 if form == 0 else (a[P[i]] - K) % 26
        out.append(AZ[inv[v]])
    return "".join(out), "".join(pt)

if __name__ == "__main__":
    a = sys.argv[2:]; B = int(a[1]) if len(a) > 1 else 2000
    FORMS = ("vig", "var"); KR = {1: "AZ", 2: "KA"}
    if a[0] == "--control":
        eng = re.sub("[^A-Z]", "", open("/tmp/claude-0/it27/test.txt").read().upper()); rng = random.Random(38); ok = n = 0
        for L in (6, 7, 9, 12):
            for form in (0, 1):
                kr = rng.choice((1, 2)); ct, pt = plant(L, form, kr, rng, eng); t = time.time()
                tr = np.array([AZ.index(ch) for ch in pt], dtype=np.int64) if "--diag" in a else np.zeros(0, np.int64)
                s, p = beam(np.array([AZ.index(ch) for ch in ct], dtype=np.int64), L, form, kr, B, tr)
                dec = "".join(AZ[x] if x >= 0 else "?" for x in p)
                acc = sum(x == y for x, y in zip(dec[L:], pt[L:])) / (97 - L); ok += acc > 0.8; n += 1
                print(f"control L={L} {FORMS[form]}/{KR[kr]}: score {s:.1f} acc {acc:.2f} {dec} {time.time()-t:.0f}s", flush=True)
        print(f"controls recovered {ok}/{n}"); sys.exit()
    c = np.array([AZ.index(ch) for ch in open("data/ciphertext.txt").read().strip()], dtype=np.int64)
    for L in range(6, 13):
        for form in (0, 1):
            for kr in (1, 2):
                t = time.time(); s, p = beam(c, L, form, kr, B)
                print(f"K4 L={L} {FORMS[form]}/{KR[kr]}: score {s:.1f} {''.join(AZ[x] if x >= 0 else '?' for x in p)} {time.time()-t:.0f}s", flush=True)
