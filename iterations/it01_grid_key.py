#!/usr/bin/env python3
"""Iteration 1: is K4's key a separable 2-D positional function k = f(row) + g(col) (mod 26)
on a grid of width w with start offset o, under a fixed tableau?

Exact test: crib key values define edges row--col with weight k; consistent iff every cycle
sums to 0 mod 26 (weighted union-find). Power = number of independent cycles (edges - nodes + comps).
"""
import random, sys
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CT = open(sys.argv[1] if len(sys.argv) > 1 else "data/ciphertext.txt").read().strip()
CRIBS = {22: "EASTNORTHEAST", 64: "BERLINCLOCK"}
RULES = {"vig": lambda c, p: c - p, "beau": lambda c, p: c + p, "vbeau": lambda c, p: p - c}

def keyvals(ct, alph, rule):
    out = {}
    for s, w in CRIBS.items():
        for j, p in enumerate(w):
            i = s - 1 + j
            out[i] = RULES[rule](alph.index(ct[i]), alph.index(p)) % 26
    return out

def test(kv, w, o):
    par, pot = {}, {}
    def find(x):
        if par.setdefault(x, x) == x:
            pot.setdefault(x, 0); return x
        r = find(par[x]); pot[x] = (pot[x] + pot[par[x]]) % 26; par[x] = r; return r
    # node value: f(row) for ('r',row), -g(col) for ('c',col); edge: f(r) - (-g(c)) = k
    cycles = 0
    for i, k in kv.items():
        a, b = ("r", (i + o) // w), ("c", (i + o) % w)
        ra, rb = find(a), find(b)
        # pot[x] = value(x) - value(root)
        if ra == rb:
            cycles += 1
            if (pot[a] - pot[b] - k) % 26: return False, cycles
        else:
            par[ra] = rb; pot[ra] = (k + pot[b] - pot[a]) % 26
    return True, cycles

def run(ct, label):
    hits = []
    for alph_name, alph in (("AZ", AZ), ("KA", KA)):
        for rule in RULES:
            kv = keyvals(ct, alph, rule)
            for w in range(2, 49):
                for o in range(w):
                    ok, cyc = test(kv, w, o)
                    if ok and cyc > 0: hits.append((alph_name, rule, w, o, cyc))
    return hits

if __name__ == "__main__":
    # positive control: plant a separable key on English text with cribs at K4 positions
    rng = random.Random(1)
    pt = list(("WEHOPETHISTEXTISLONGENOUGHTOSERVEASACONTROLFORTHEGRIDKEYTESTANDITKEEPSGOINGUNTILNINETYSEVENLETTERS" * 2)[:97])
    for s, wd in CRIBS.items(): pt[s - 1:s - 1 + len(wd)] = wd
    W, O = 21, 5; f = [rng.randrange(26) for _ in range(10)]; g = [rng.randrange(26) for _ in range(W)]
    ctl = "".join(KA[(KA.index(p) + f[(i + O) // W] + g[(i + O) % W]) % 26] for i, p in enumerate(pt))
    h = run(ctl, "control")
    print("control (KA vig, w=21, o=5) recovered:", any(x[:4] == ("KA", "vig", 21, 5) for x in h), "| total hits", len(h))
    # null: random ciphertexts, how often does a (w,o) with >=1 cycle pass by chance?
    hk = run(CT, "K4")
    print("K4 hits (alphabet, rule, width, offset, #cycles):", len(hk))
    for x in sorted(hk, key=lambda x: -x[4])[:20]: print("  ", x)
