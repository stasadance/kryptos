#!/usr/bin/env python3
"""Iteration 20: Quagmire-III-proper double keyword. k_i = s1*a(W1[i mod L1]) + s2*a(W2[i mod L2]) where the key letters
are looked up in the SAME unknown alphabet a as the text (as on the Kryptos tableau). Cipher: Vig a(c)=a(p)+k or
Beau a(c)=k-a(p). Everything is linear in a, so the cribs decide it exactly: CRT (mod 2, mod 13) + all-different.
Words: the three Kryptos keywords. Signs s1,s2 in {+1,-1}. Control: planted KRYPTOS+PALIMPSEST Vig. Null: random ct."""
import itertools, random, sys
sys.path.insert(0, "iterations"); from it18c_vimark_alldiff import solve_space
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; CT = open("data/ciphertext.txt").read().strip()
CR = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}; PAIRS = [(s + j, p) for s, w in CR.items() for j, p in enumerate(w)]
WORDS = ["KRYPTOS", "PALIMPSEST", "ABSCISSA"]
def ok(ct, W1, W2, s1, s2, beau, cap=3000000):
    L = sorted({ct[i] for i, _ in PAIRS} | {p for _, p in PAIRS} | set(W1) | set(W2)); ix = {c: j for j, c in enumerate(L)}; rows = []
    for i, p in PAIRS:
        r = [0] * (len(L) + 1); r[ix[ct[i]]] += 1; r[ix[p]] += 1 if beau else -1
        r[ix[W1[i % len(W1)]]] -= s1; r[ix[W2[i % len(W2)]]] -= s2; rows.append(r)
    a, b = solve_space(rows, 2), solve_space(rows, 13)
    if a is None or b is None: return 0
    (b2, B2), (b13, B13) = a, b; nl = len(L)
    if 13 ** len(B13) * 2 ** len(B2) > cap: return -1
    s2l = [tuple((b2[j] + sum(c * v[j] for c, v in zip(co, B2))) % 2 for j in range(nl)) for co in itertools.product(range(2), repeat=len(B2))]
    for co in itertools.product(range(13), repeat=len(B13)):
        x = [(b13[j] + sum(c * v[j] for c, v in zip(co, B13))) % 13 for j in range(nl)]
        if max(x.count(v) for v in set(x)) > 2: continue
        if any(len(set(zip(y, x))) == nl for y in s2l): return 1
    return 0
CONF = [(w1, w2, s1, s2, beau) for w1, w2 in itertools.permutations(WORDS, 2) if w1 < w2 for s1 in (1, -1) for s2 in (1, -1) for beau in (0, 1)]
CONF += [(w, w, 1, 0, beau) for w in WORDS for beau in (0, 1)]  # single keyword, Quagmire III proper, as a sanity baseline
if __name__ == "__main__":
    rng = random.Random(3); al = list(range(26)); rng.shuffle(al); inv = {v: i for i, v in enumerate(al)}
    pt = [rng.choice(AZ) for _ in range(97)]
    for s, w in CR.items(): pt[s:s + len(w)] = w
    A = lambda ch: al[AZ.index(ch)]
    ctl = "".join(AZ[inv[(A(p) + A("KRYPTOS"[i % 7]) + A("PALIMPSEST"[i % 10])) % 26]] for i, p in enumerate(pt))
    print("control KRYPTOS+PALIMPSEST vig:", ok(ctl, "KRYPTOS", "PALIMPSEST", 1, 1, 0))
    nulls = ["".join(rng.choice(AZ) for _ in range(97)) for _ in range(40)]
    for c in CONF:
        r = ok(CT, *c); nr = [x for x in (ok(s, *c) for s in nulls) if x >= 0]
        print(c, "K4", r, f"null {sum(nr)}/{len(nr)}", flush=True)
