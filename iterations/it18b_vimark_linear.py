#!/usr/bin/env python3
"""Iteration 18b: identifiability of mixed-alphabet Vimark by the cribs. The crib equations
a(c_i) - a(p_i) - sum_j V[i][j] P_j = 0 (Q3v; Q3b uses +a(p_i); G-AZ/G-KA have a known plain value)
are LINEAR mod 26 in (alphabet values, primer). Check consistency mod 2 and mod 13 (CRT) by Gaussian
elimination, ignoring the alphabet's all-different constraint (a necessary condition). Report rank,
free dimensions, and the fraction of random ciphertexts that pass, so we know where the test has power."""
import random, sys
sys.path.insert(0, "iterations"); from it18_vimark_mixed import coefs, PAIRS, CT, AZ, KA
def consistent(rows, p):
    rows = [[x % p for x in r] for r in rows]; m = len(rows[0]) - 1; rank = 0
    for col in range(m):
        piv = next((r for r in range(rank, len(rows)) if rows[r][col]), None)
        if piv is None: continue
        rows[rank], rows[piv] = rows[piv], rows[rank]; inv = pow(rows[rank][col], -1, p)
        rows[rank] = [x * inv % p for x in rows[rank]]
        for r in range(len(rows)):
            if r != rank and rows[r][col]:
                f = rows[r][col]; rows[r] = [(x - f * y) % p for x, y in zip(rows[r], rows[rank])]
        rank += 1
    ok = all(any(r[:-1]) or r[-1] == 0 for r in rows); return ok, rank, m
def system(ct, n, rule, model):
    V = coefs(n, rule); L = sorted({ct[i] for i, _ in PAIRS} | ({p for _, p in PAIRS} if model in ("Q3v", "Q3b") else set()))
    ix = {c: j for j, c in enumerate(L)}; rows = []
    for i, p in PAIRS:
        r = [0] * (len(L) + n + 1); r[ix[ct[i]]] += 1
        if model == "Q3v": r[ix[p]] -= 1
        elif model == "Q3b": r[ix[p]] += 1
        else: r[-1] = (AZ if model == "G-AZ" else KA).index(p)
        for j in range(n): r[len(L) + j] -= V[i][j]
        rows.append(r)
    return rows
def ok26(ct, n, rule, model):
    S = system(ct, n, rule, model); a = consistent(S, 2); b = consistent(S, 13); return a[0] and b[0], (a[1], b[1], a[2])
if __name__ == "__main__":
  rng = random.Random(1); nulls = ["".join(rng.choice(AZ) for _ in range(97)) for _ in range(200)]
  print("n rule model | K4 ok | rank2 rank13 unknowns | null pass rate")
  for n in range(2, 13):
    for rule in "AB":
        for model in ("Q3v", "Q3b", "G-AZ", "G-KA"):
            k, info = ok26(CT, n, rule, model)
            rate = sum(ok26(s, n, rule, model)[0] for s in nulls) / len(nulls)
            print(f"{n:2d} {rule} {model:5s} | {int(k)} | {info} | {rate:.2f}")
