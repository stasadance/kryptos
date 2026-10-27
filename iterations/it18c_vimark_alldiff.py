#!/usr/bin/env python3
"""Iteration 18c: exact test of mixed-alphabet Vimark, one unknown alphabet (Q3v/Q3b), with the
all-different constraint. Solve the linear crib system mod 2 and mod 13 separately (CRT), enumerate the
small solution spaces, and accept only if the crib letters get distinct values in Z26
(value = CRT(x mod 2, x mod 13)). Primer variables are free. Control: planted key. Null: random ct."""
import random, sys, itertools
sys.path.insert(0, "iterations"); from it18_vimark_mixed import keystream, PAIRS, CT, AZ, CRIBS
from it18b_vimark_linear import system
def solve_space(rows, p):
    rows = [[x % p for x in r] for r in rows]; m = len(rows[0]) - 1; piv = []; rank = 0
    for col in range(m):
        r0 = next((r for r in range(rank, len(rows)) if rows[r][col]), None)
        if r0 is None: continue
        rows[rank], rows[r0] = rows[r0], rows[rank]; inv = pow(rows[rank][col], -1, p)
        rows[rank] = [x * inv % p for x in rows[rank]]
        for r in range(len(rows)):
            if r != rank and rows[r][col]:
                f = rows[r][col]; rows[r] = [(x - f * y) % p for x, y in zip(rows[r], rows[rank])]
        piv.append(col); rank += 1
    if any(not any(r[:-1]) and r[-1] for r in rows): return None
    free = [c for c in range(m) if c not in piv]
    base = [0] * m
    for i, c in enumerate(piv): base[c] = rows[i][-1]
    basis = []
    for f in free:
        v = [0] * m; v[f] = 1
        for i, c in enumerate(piv): v[c] = (-rows[i][f]) % p
        basis.append(v)
    return base, basis
def ok(ct, n, rule, model, nl, cap=2000000):
    S = system(ct, n, rule, model)
    a, b = solve_space(S, 2), solve_space(S, 13)
    if a is None or b is None: return 0
    (b2, B2), (b13, B13) = a, b
    if 13 ** len(B13) * 2 ** len(B2) > cap: return -1
    sols2 = []
    for co in itertools.product(range(2), repeat=len(B2)):
        sols2.append(tuple((b2[j] + sum(c * v[j] for c, v in zip(co, B2))) % 2 for j in range(nl)))
    for co in itertools.product(range(13), repeat=len(B13)):
        x13 = [(b13[j] + sum(c * v[j] for c, v in zip(co, B13))) % 13 for j in range(nl)]
        cnt = {}
        for v in x13: cnt[v] = cnt.get(v, 0) + 1
        if max(cnt.values()) > 2: continue
        for x2 in sols2:
            if len(set(zip(x2, x13))) == nl: return 1
    return 0
def nletters(ct): return len({ct[i] for i, _ in PAIRS} | {p for _, p in PAIRS})
CONF = [(n, r, m) for n in range(2, 9) for r in "AB" for m in ("Q3v", "Q3b")]
if __name__ == "__main__":
    rng = random.Random(11); al = list(AZ); rng.shuffle(al); pos = {c: i for i, c in enumerate(al)}
    k = keystream([rng.randrange(26) for _ in range(5)], "A"); pt = [rng.choice(AZ) for _ in range(97)]
    for s, w in CRIBS.items(): pt[s:s + len(w)] = w
    ctl = "".join(al[(pos[p] + k[i]) % 26] for i, p in enumerate(pt))
    print("control (5,A,Q3v):", ok(ctl, 5, "A", "Q3v", nletters(ctl)))
    nulls = ["".join(rng.choice(AZ) for _ in range(97)) for _ in range(100)]
    print("n rule model | K4 | null pass rate (-1 = space too big)")
    for c in CONF:
        r = ok(CT, *c, nletters(CT))
        nr = [ok(s, *c, nletters(s)) for s in nulls]
        dn = [x for x in nr if x >= 0]; rate = f"{sum(dn)/len(dn):.2f} over {len(dn)} decidable" if dn else "none decidable"
        print(f"{c[0]:2d} {c[1]} {c[2]} | {r} | {rate}", flush=True)
