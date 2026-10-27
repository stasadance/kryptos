#!/usr/bin/env python3
"""Iteration 8: which keyword-mixed alphabets fit the width-7 grid-key model (it07)?

Necessary condition from it06/it07: if the key step k(i+1)-k(i) is the same at every residue-4
boundary and the crib doublets NO->QQ, ST->SS, IN->TT are produced by the cipher, then the plaintext
alphabet alpha satisfies alpha(O)-alpha(N) = alpha(T)-alpha(S) = alpha(N)-alpha(I) (mod 26)
(Vigenere and Beaufort forms give the same condition up to sign; holds for 1 or 2 alphabets).
Random alphabet passes with p = 1/676. Survivors then get the exact grid test (fixed alphabet,
union-find on crib key values, widths 7/14/21/28/35/42, all offsets) under Quagmire-III (beta = alpha).
"""
import sys
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CT = open("data/ciphertext.txt").read().strip()
CRIBS = {22: "EASTNORTHEAST", 64: "BERLINCLOCK"}
PAIRS = [(s - 1 + j, p) for s, w in CRIBS.items() for j, p in enumerate(w)]

def dedup(s):
    out = []
    for c in s:
        if c not in out: out.append(c)
    return "".join(out)
def variants(word):
    k = dedup(word.upper())
    a1 = k + "".join(c for c in AZ if c not in k)                       # keyword then rest
    last = AZ.index(k[-1]); rest = AZ[last + 1:] + AZ[:last + 1]
    a2 = k + "".join(c for c in rest if c not in k)                     # keyword then continue after last letter
    L = len(k); rows = [a1[i:i + L] for i in range(0, 26, L)]
    a3 = "".join("".join(r[c] for r in rows if c < len(r)) for c in range(L))   # columnar keyed (ACA K3-ish)
    for a in (a1, a2, a3):
        yield a; yield a[::-1]

def cond(a):
    x = {c: i for i, c in enumerate(a)}
    d1 = (x["O"] - x["N"]) % 26; d2 = (x["T"] - x["S"]) % 26; d3 = (x["N"] - x["I"]) % 26
    return d1 == d2 == d3

def grid_ok(a, w, o, beau):
    x = {c: i for i, c in enumerate(a)}
    par, pot = {}, {}
    def find(n):
        if par.setdefault(n, n) == n: pot.setdefault(n, 0); return n
        r = find(par[n]); pot[n] = (pot[n] + pot[par[n]]) % 26; par[n] = r; return r
    cyc = 0
    for i, p in PAIRS:
        k = (x[CT[i]] + x[p]) % 26 if beau else (x[CT[i]] - x[p]) % 26
        u, v = ("r", (i + o) // w), ("c", (i + o) % w)
        ru, rv = find(u), find(v)
        if ru == rv:
            cyc += 1
            if (pot[u] - pot[v] - k) % 26: return False
        else: par[ru] = rv; pot[ru] = (k + pot[v] - pot[u]) % 26
    return cyc > 0

if __name__ == "__main__":
    words = [w.strip() for w in open(sys.argv[1]) if 3 <= len(w.strip()) <= 20 and w.strip().isalpha()]
    n = passed = 0; surv = {}
    for wd in words:
        for a in variants(wd):
            n += 1
            if cond(a):
                passed += 1; surv.setdefault(a, wd)
    print(f"alphabets tested {n}, pass doublet condition {passed} ({passed/n:.5f}; random expectation {1/676:.5f}), distinct {len(surv)}")
    hits = []
    for a, wd in surv.items():
        for beau in (False, True):
            for w in (7, 14, 21, 28, 35, 42):
                for o in range(w):
                    if grid_ok(a, w, o, beau): hits.append((wd, a, "beau" if beau else "vig", w, o))
    print("grid-model hits:", len(hits))
    for h in hits[:30]: print("  ", h)

def grid_ok2(a, b, w, o, beau):
    """two alphabets: plaintext alphabet a (keyword), ciphertext alphabet b (AZ or KA)"""
    x = {c: i for i, c in enumerate(a)}; y = {c: i for i, c in enumerate(b)}
    par, pot = {}, {}
    def find(n):
        if par.setdefault(n, n) == n: pot.setdefault(n, 0); return n
        r = find(par[n]); pot[n] = (pot[n] + pot[par[n]]) % 26; par[n] = r; return r
    cyc = 0
    for i, p in PAIRS:
        k = (y[CT[i]] + x[p]) % 26 if beau else (y[CT[i]] - x[p]) % 26
        u, v = ("r", (i + o) // w), ("c", (i + o) % w)
        ru, rv = find(u), find(v)
        if ru == rv:
            cyc += 1
            if (pot[u] - pot[v] - k) % 26: return False
        else: par[ru] = rv; pot[ru] = (k + pot[v] - pot[u]) % 26
    return cyc > 0
