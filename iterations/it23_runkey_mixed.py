#!/usr/bin/env python3
"""Iteration 23: running key from a natural-language text under ONE unknown mixed alphabet a.
Models (all linear in a once the key letters are fixed by a source text and an offset):
  q3v  a(c) = a(p) + a(k)      Quagmire III proper, key letter looked up in the same alphabet (K1/K2 structure)
  q3b  a(c) = a(k) - a(p)      Beaufort form
  q3w  a(c) = a(p) - a(k)      variant Beaufort
  azv/kav  a(c) = a(p) + n(k)  key value = index of the key letter in AZ / KA (numeric key), likewise azb/kab, azw/kaw
Exact test: crib system mod 2 and mod 13 (CRT) + all-different on the letters involved (it18c solve_space).
A pass fixes a up to a small family, after which the whole text decrypts and can be read."""
import itertools, sys
sys.path.insert(0, "iterations"); from it18c_vimark_alldiff import solve_space
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CT = open("data/ciphertext.txt").read().strip()
CR = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}; PAIRS = [(s + j, p) for s, w in CR.items() for j, p in enumerate(w)]
MODELS = ["q3v", "q3b", "q3w", "azv", "azb", "azw", "kav", "kab", "kaw"]
def rows_for(ct, key, model):
    """key: dict pos->key letter for the crib positions. Returns (rows, letters)."""
    L = sorted({ct[i] for i, _ in PAIRS} | {p for _, p in PAIRS} | ({key[i] for i, _ in PAIRS} if model[:2] == "q3" else set()))
    ix = {c: j for j, c in enumerate(L)}; rows = []
    form = model[2]
    for i, p in PAIRS:
        r = [0] * (len(L) + 1); c = ct[i]; k = key[i]
        r[ix[c]] += 1
        if form == "v": r[ix[p]] -= 1; sk = -1     # a(c) - a(p) - k = 0
        elif form == "b": r[ix[p]] += 1; sk = -1   # a(c) + a(p) - k = 0
        else: r[ix[p]] -= 1; sk = +1               # a(c) - a(p) + k = 0
        if model[:2] == "q3": r[ix[k]] += sk
        else:
            kv = (AZ if model[:2] == "az" else KA).index(k); r[-1] -= sk * kv   # move constant to rhs
        rows.append(r)
    return rows, L
def solutions(ct, key, model, cap=400000, first=True):
    rows, L = rows_for(ct, key, model); nl = len(L)
    a, b = solve_space([r[:] for r in rows], 2), solve_space([r[:] for r in rows], 13)
    if a is None or b is None: return []
    (b2, B2), (b13, B13) = a, b
    if 13 ** len(B13) * 2 ** len(B2) > cap: return None
    s2l = [tuple((b2[j] + sum(c * v[j] for c, v in zip(co, B2))) % 2 for j in range(nl)) for co in itertools.product(range(2), repeat=len(B2))]
    out = []
    for co in itertools.product(range(13), repeat=len(B13)):
        x = [(b13[j] + sum(c * v[j] for c, v in zip(co, B13))) % 13 for j in range(nl)]
        if max(x.count(v) for v in set(x)) > 2: continue
        for y in s2l:
            if len(set(zip(y, x))) == nl:
                val = {L[j]: next(z for z in range(26) if z % 2 == y[j] and z % 13 == x[j]) for j in range(nl)}
                out.append(val)
                if first: return out
    return out
def norm(t): return "".join(ch for ch in t.upper() if ch in AZ)
