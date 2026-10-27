#!/usr/bin/env python3
"""Iteration 23 scanner: numba version of it23_runkey_mixed.solutions() for every offset of a source text.
Usage: python3 iterations/it23_scan.py [--control] text1 [text2 ...]   (texts forward and reversed)
Prints every (source, direction, offset, model) that passes the exact crib test; passes are then decrypted by
it23_runkey_mixed for reading. Returns -1 (undecided) when a solution space exceeds the enumeration cap."""
import sys, time, random
import numpy as np
from numba import njit, prange
sys.path.insert(0, "iterations")
from it23_runkey_mixed import CT, PAIRS, MODELS, AZ, KA, norm, solutions
POS = np.array([i for i, _ in PAIRS], dtype=np.int64)
PT = np.array([AZ.index(p) for _, p in PAIRS], dtype=np.int64)
AZI = np.arange(26, dtype=np.int64); KAI = np.array([KA.index(ch) for ch in AZ], dtype=np.int64)  # KA index of AZ letter

@njit(cache=True)
def solve_mod(M, rhs, p, cols, ncols, base, basis):
    """RREF of M (24 x 26) restricted to columns cols[:ncols], mod p. Fills base (26) and basis (k x 26); returns k or -1."""
    m = M.shape[0]
    A = np.zeros((m, ncols + 1), dtype=np.int64)
    for r in range(m):
        for j in range(ncols): A[r, j] = M[r, cols[j]] % p
        A[r, ncols] = rhs[r] % p
    piv = np.full(ncols, -1, dtype=np.int64); rank = 0
    for col in range(ncols):
        r0 = -1
        for r in range(rank, m):
            if A[r, col] != 0: r0 = r; break
        if r0 < 0: continue
        for j in range(ncols + 1):
            t = A[rank, j]; A[rank, j] = A[r0, j]; A[r0, j] = t
        inv = 1
        for t in range(1, p):
            if (A[rank, col] * t) % p == 1: inv = t; break
        for j in range(ncols + 1): A[rank, j] = (A[rank, j] * inv) % p
        for r in range(m):
            if r != rank and A[r, col] != 0:
                f = A[r, col]
                for j in range(ncols + 1): A[r, j] = (A[r, j] - f * A[rank, j]) % p
        piv[col] = rank; rank += 1
    for r in range(rank, m):
        if A[r, ncols] != 0: return -1
    for j in range(26): base[j] = 0
    for col in range(ncols):
        if piv[col] >= 0: base[cols[col]] = A[piv[col], ncols]
    k = 0
    for col in range(ncols):
        if piv[col] < 0:
            for j in range(26): basis[k, j] = 0
            basis[k, cols[col]] = 1
            for c2 in range(ncols):
                if piv[c2] >= 0: basis[k, cols[c2]] = (-A[piv[c2], col]) % p
            k += 1
    return k

# Roles: each of cipher letter, plain letter, key letter is valued by the unknown alphabet a (0), AZ index (1) or KA index (2).
# Form 0: X(c) - X(p) - X(k) = 0 (Vigenere), 1: X(c) + X(p) - X(k) = 0 (Beaufort), 2: X(c) - X(p) + X(k) = 0 (variant).
ROLES = [(rc, rp, rk) for rc in range(3) for rp in range(3) for rk in range(3) if 0 in (rc, rp)]
MODELS2 = [f"c{'aAK'[rc]}p{'aAK'[rp]}k{'aAK'[rk]}-{'vbw'[f]}" for rc, rp, rk in ROLES for f in range(3)]
RC = np.array([r[0] for r in ROLES for f in range(3)], dtype=np.int64); RP = np.array([r[1] for r in ROLES for f in range(3)], dtype=np.int64)
RK = np.array([r[2] for r in ROLES for f in range(3)], dtype=np.int64); FM = np.array([f for r in ROLES for f in range(3)], dtype=np.int64)

@njit(cache=True)
def test_one(ct, key, model, cap13, cap2):
    form = FM[model]; roles = (RC[model], RP[model], RK[model])
    M = np.zeros((24, 26), dtype=np.int64); rhs = np.zeros(24, dtype=np.int64); used = np.zeros(26, dtype=np.int64)
    for r in range(24):
        lets = (ct[POS[r]], PT[r], key[r])
        if form == 0: sg = (1, -1, -1)
        elif form == 1: sg = (1, 1, -1)
        else: sg = (1, -1, 1)
        for t in range(3):
            L = lets[t]; ro = roles[t]
            if ro == 0: M[r, L] += sg[t]; used[L] = 1
            elif ro == 1: rhs[r] -= sg[t] * L
            else: rhs[r] -= sg[t] * KAI[L]
    cols = np.zeros(26, dtype=np.int64); n = 0
    for j in range(26):
        if used[j]: cols[n] = j; n += 1
    b13 = np.zeros(26, dtype=np.int64); B13 = np.zeros((26, 26), dtype=np.int64)
    b2 = np.zeros(26, dtype=np.int64); B2 = np.zeros((26, 26), dtype=np.int64)
    k13 = solve_mod(M, rhs, 13, cols, n, b13, B13)
    if k13 < 0: return 0
    k2 = solve_mod(M, rhs, 2, cols, n, b2, B2)
    if k2 < 0: return 0
    tot13 = 1
    for i in range(k13):
        tot13 *= 13
        if tot13 > cap13: return -1
    tot2 = 1
    for i in range(k2):
        tot2 *= 2
        if tot2 > cap2: return -1
    co = np.zeros(26, dtype=np.int64); x = np.zeros(26, dtype=np.int64); cnt = np.zeros(13, dtype=np.int64)
    y = np.zeros(26, dtype=np.int64); first = np.full(13, -1, dtype=np.int64); second = np.full(13, -1, dtype=np.int64)
    for idx in range(tot13):
        t = idx
        for i in range(k13): co[i] = t % 13; t //= 13
        for j in range(n):
            L = cols[j]; v = b13[L]
            for i in range(k13): v += co[i] * B13[i, L]
            x[L] = v % 13
        for r in range(13): cnt[r] = 0; first[r] = -1; second[r] = -1
        bad = False
        for j in range(n):
            L = cols[j]; r = x[L]; cnt[r] += 1
            if cnt[r] > 2: bad = True; break
            if first[r] < 0: first[r] = L
            else: second[r] = L
        if bad: continue
        for idx2 in range(tot2):
            t = idx2
            for j in range(n):
                L = cols[j]; v = b2[L]; tt = idx2
                for i in range(k2):
                    v += (tt & 1) * B2[i, L]; tt >>= 1
                y[L] = v % 2
            good = True
            for r in range(13):
                if second[r] >= 0 and y[first[r]] == y[second[r]]: good = False; break
            if good: return 1
    return 0

@njit(parallel=True, cache=True)
def scan(ct, txt, nmodels, cap13, cap2):
    nofs = txt.shape[0] - 97
    out = np.zeros((max(nofs, 0), nmodels), dtype=np.int8)
    for o in prange(max(nofs, 0)):
        key = np.empty(24, dtype=np.int64)
        for r in range(24): key[r] = txt[o + POS[r]]
        for m in range(nmodels): out[o, m] = test_one(ct, key, m, cap13, cap2)
    return out

def arr(s): return np.array([AZ.index(ch) for ch in s], dtype=np.int64)
@njit(parallel=True, cache=True)
def rescan(ct, txt, offs, mods, cap13, cap2):
    out = np.zeros(offs.shape[0], dtype=np.int8)
    for i in prange(offs.shape[0]):
        key = np.empty(24, dtype=np.int64)
        for r in range(24): key[r] = txt[offs[i] + POS[r]]
        out[i] = test_one(ct, key, mods[i], cap13, cap2)
    return out

def run(ct, name, txt, cap13=30000, cap2=4096, cap13b=3000000, cap2b=65536):
    res = scan(arr(ct), arr(txt), len(MODELS2), cap13, cap2)
    u = np.argwhere(res == -1)
    if len(u):
        r2 = rescan(arr(ct), arr(txt), u[:, 0].astype(np.int64), u[:, 1].astype(np.int64), cap13b, cap2b)
        res[u[:, 0], u[:, 1]] = r2
    hits = np.argwhere(res == 1); und = int((res == -1).sum())
    return [(name, int(o), MODELS2[m]) for o, m in hits], und, res.shape[0]

def plant(src, eng, model, rng):
    rc, rp, rk = RC[model], RP[model], RK[model]; f = FM[model]
    al = list(range(26)); rng.shuffle(al); inv = {v: i for i, v in enumerate(al)}
    val = lambda ro, ch: al[AZ.index(ch)] if ro == 0 else (AZ.index(ch) if ro == 1 else KA.index(ch))
    o = rng.randrange(5000, len(src) - 5200); po = rng.randrange(len(eng) - 200)
    pt = list(eng[po:po + 97])
    for s0, w in {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}.items(): pt[s0:s0 + len(w)] = w
    out = []
    for i, p in enumerate(pt):
        kv = val(rk, src[o + i]); pv = val(rp, p)
        cv = (pv + kv) if f == 0 else ((kv - pv) if f == 1 else (pv - kv))
        cv %= 26
        out.append(AZ[inv[cv]] if rc == 0 else (AZ[cv] if rc == 1 else KA[cv]))
    return "".join(out), o

if __name__ == "__main__":
    args = sys.argv[1:]; control = "--control" in args; files = [a for a in args if not a.startswith("--")]
    if control:
        src = norm(open(files[0], errors="ignore").read()); eng = norm(open(files[1], errors="ignore").read())
        rng = random.Random(7); nf = 0
        for m, model in enumerate(MODELS2):
            ctl, o = plant(src, eng, m, rng)
            hits, und, n = run(ctl, "ctl", src[o - 5000:o + 5000])
            found = any(h[1] == 5000 and h[2] == model for h in hits); nf += found
            print(f"control {model}: found={found} other hits={len(hits) - found} undecided={und}", flush=True)
        print(f"controls recovered {nf}/{len(MODELS2)}"); sys.exit()
    for f in files:
        raw = norm(open(f, errors="ignore").read())
        for d, txt in (("fwd", raw), ("rev", raw[::-1])):
            t = time.time(); hits, und, n = run(CT, f, txt)
            print(f"{f} {d}: {n} offsets x {len(MODELS2)} models, hits={len(hits)}, undecided={und}, {time.time()-t:.0f}s", flush=True)
            for h in hits: print("  HIT", d, h, txt[h[1]:h[1] + 97], flush=True)
