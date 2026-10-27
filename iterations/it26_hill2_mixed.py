#!/usr/bin/env python3
"""Iteration 26: 2x2 Hill cipher under an UNKNOWN letter numbering (mixed alphabet a), linear and affine.
Motivation: Sanborn's "matrix codes Ed gave me"; the extra L on the tableau spelling HILL (Bauer/Link/Molle 2016).
Phase 1 refuted Hill n=2,3,4 only with A=0 or KA numbering. Model: for blocks (x,y) at positions (2j+o, 2j+o+1):
  a(c_x) = m11 a(p_x) + m12 a(p_y) + b1,  a(c_y) = m21 a(p_x) + m22 a(p_y) + b2   (b=0 for linear).
For each invertible M (det a unit mod 26) this is linear in (a, b): exact CRT + all-different (numba).
All M (157,248) covers both C=MP and P=MC. Offsets o=0,1. Control: planted. Null: random ciphertexts."""
import sys, random, itertools, time
import numpy as np
from numba import njit, prange
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; CT = open("data/ciphertext.txt").read().strip()
CR = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}; PTP = {s + j: p for s, w in CR.items() for j, p in enumerate(w)}

@njit(cache=True)
def solve(A0, p, ncol, base, basis):
    m = A0.shape[0]; A = A0.copy() % p
    piv = np.full(ncol, -1, dtype=np.int64); rank = 0
    for col in range(ncol):
        r0 = -1
        for r in range(rank, m):
            if A[r, col] != 0: r0 = r; break
        if r0 < 0: continue
        for j in range(ncol + 1):
            t = A[rank, j]; A[rank, j] = A[r0, j]; A[r0, j] = t
        inv = 1
        for t in range(1, p):
            if (A[rank, col] * t) % p == 1: inv = t; break
        for j in range(ncol + 1): A[rank, j] = (A[rank, j] * inv) % p
        for r in range(m):
            if r != rank and A[r, col] != 0:
                f = A[r, col]
                for j in range(ncol + 1): A[r, j] = (A[r, j] - f * A[rank, j]) % p
        piv[col] = rank; rank += 1
    for r in range(rank, m):
        if A[r, ncol] != 0: return -1
    for j in range(ncol): base[j] = 0
    for col in range(ncol):
        if piv[col] >= 0: base[col] = A[piv[col], ncol]
    k = 0
    for col in range(ncol):
        if piv[col] < 0:
            for j in range(ncol): basis[k, j] = 0
            basis[k, col] = 1
            for c2 in range(ncol):
                if piv[c2] >= 0: basis[k, c2] = (-A[piv[c2], col]) % p
            k += 1
    return k

@njit(cache=True)
def feasible(A, nlet, ncol, cap13, cap2):
    """A: rows over ncol unknowns (first nlet are letters, must be distinct mod 26) + rhs."""
    b13 = np.zeros(ncol, dtype=np.int64); B13 = np.zeros((ncol, ncol), dtype=np.int64)
    b2 = np.zeros(ncol, dtype=np.int64); B2 = np.zeros((ncol, ncol), dtype=np.int64)
    k13 = solve(A, 13, ncol, b13, B13)
    if k13 < 0: return 0
    k2 = solve(A, 2, ncol, b2, B2)
    if k2 < 0: return 0
    t13 = 1
    for i in range(k13):
        t13 *= 13
        if t13 > cap13: return -1
    t2 = 1
    for i in range(k2):
        t2 *= 2
        if t2 > cap2: return -1
    x = np.zeros(nlet, dtype=np.int64); y = np.zeros(nlet, dtype=np.int64)
    cnt = np.zeros(13, dtype=np.int64); f1 = np.zeros(13, dtype=np.int64); f2 = np.zeros(13, dtype=np.int64)
    for idx in range(t13):
        for r in range(13): cnt[r] = 0; f1[r] = -1; f2[r] = -1
        bad = False
        for L in range(nlet):
            v = b13[L]; t = idx
            for i in range(k13): v += (t % 13) * B13[i, L]; t //= 13
            x[L] = v % 13; r = x[L]; cnt[r] += 1
            if cnt[r] > 2: bad = True; break
            if f1[r] < 0: f1[r] = L
            else: f2[r] = L
        if bad: continue
        for idx2 in range(t2):
            for L in range(nlet):
                v = b2[L]; t = idx2
                for i in range(k2): v += (t & 1) * B2[i, L]; t >>= 1
                y[L] = v % 2
            good = True
            for r in range(13):
                if f2[r] >= 0 and y[f1[r]] == y[f2[r]]: good = False; break
            if good: return 1
    return 0

@njit(parallel=True, cache=True)
def scan_all(blocks, mats, affine, nlet, cap13, cap2):
    """blocks: (nb,4) letter-ids (cx, cy, px, py); mats: (nm,4). Returns per-matrix result."""
    nm = mats.shape[0]; nb = blocks.shape[0]; out = np.zeros(nm, dtype=np.int8)
    ncol = nlet + (2 if affine else 0)
    for mi in prange(nm):
        m11, m12, m21, m22 = mats[mi, 0], mats[mi, 1], mats[mi, 2], mats[mi, 3]
        A = np.zeros((2 * nb, ncol + 1), dtype=np.int64)
        for b in range(nb):
            cx, cy, px, py = blocks[b, 0], blocks[b, 1], blocks[b, 2], blocks[b, 3]
            r = 2 * b
            A[r, cx] += 1; A[r, px] -= m11; A[r, py] -= m12
            A[r + 1, cy] += 1; A[r + 1, px] -= m21; A[r + 1, py] -= m22
            if affine: A[r, nlet] -= 1; A[r + 1, nlet + 1] -= 1
        out[mi] = feasible(A, nlet, ncol, cap13, cap2)
    return out

def mats():
    units = {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25}
    return np.array([m for m in itertools.product(range(26), repeat=4) if (m[0] * m[3] - m[1] * m[2]) % 26 in units], dtype=np.int64)
def blocks_for(ct, o):
    bl = []
    for x in range(o, 96, 2):
        if x in PTP and x + 1 in PTP: bl.append((ct[x], ct[x + 1], PTP[x], PTP[x + 1]))
    letters = sorted({ch for b in bl for ch in b}); ix = {c: i for i, c in enumerate(letters)}
    return np.array([[ix[ch] for ch in b] for b in bl], dtype=np.int64), len(letters)
def run(ct, M, affine, cap13=200000, cap2=4096):
    res = {}
    for o in (0, 1):
        B, nl = blocks_for(ct, o); r = scan_all(B, M, affine, nl, cap13, cap2)
        res[o] = (int((r == 1).sum()), int((r == -1).sum()), np.argwhere(r == 1).ravel()[:5].tolist(), B.shape[0])
    return res
if __name__ == "__main__":
    M = mats(); print("matrices:", len(M), flush=True)
    rng = random.Random(4)
    for affine in (False, True):
        al = list(range(26)); rng.shuffle(al); inv = {v: i for i, v in enumerate(al)}
        mi = rng.randrange(len(M)); m = M[mi]; bb = (rng.randrange(26), rng.randrange(26)) if affine else (0, 0)
        pt = list(("ATTACKATDAWNTHEBRIDGEISGUARDEDBYTWOSENTRIESANDADOG" * 2)[:98])
        for s0, w in CR.items(): pt[s0:s0 + len(w)] = w
        o = 1; ct = list(pt)
        for x in range(o, 96, 2):
            u, v = al[AZ.index(pt[x])], al[AZ.index(pt[x + 1])]
            ct[x] = AZ[inv[(m[0] * u + m[1] * v + bb[0]) % 26]]; ct[x + 1] = AZ[inv[(m[2] * u + m[3] * v + bb[1]) % 26]]
        ct = "".join(ct[:97]); t = time.time()
        r = run(ct, M, affine)
        print(f"control affine={affine}: planted matrix #{mi} offset {o}: {r[o]}  found={mi in r[o][2] or r[o][0] > 0}  {time.time()-t:.0f}s", flush=True)
    for affine in (False, True):
        t = time.time(); r = run(CT, M, affine)
        print(f"K4 affine={affine}: {r}  {time.time()-t:.0f}s", flush=True)
        for k in range(3):
            nul = "".join(rng.choice(AZ) for _ in range(97)); print(f"  null {k}: {run(nul, M, affine)}", flush=True)
