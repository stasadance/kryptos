#!/usr/bin/env python3
"""Iteration 10: is the K4 key range small (a digit-like key) when ciphertext letters are read in
the standard alphabet?

Evidence: Bean 2021 "minor differences". Ciphertext letters that encrypt the same plaintext letter
lie close together in A-Z (mean 3.6; 1 in 240 under permutation).
Model: c_i = AZ[(alpha(p_i) + d_i) mod 26], with key digits d_i in [0, B-1] and unknown alphabet alpha.
For each plaintext letter, its ciphertext letters must fit in a cyclic window of size B.
B_min(K4) = the largest minimal window over the repeated plaintext letters. Compare with random
ciphertexts (the cribs fixed, random ciphertext letters at those 24 positions), for several cipher
alphabets (AZ, KA, reversed).
"""
import random
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CT = open("data/ciphertext.txt").read().strip()
CRIBS = {22: "EASTNORTHEAST", 64: "BERLINCLOCK"}
PAIRS = [(s - 1 + j, p) for s, w in CRIBS.items() for j, p in enumerate(w)]
def bmin(ctl, beta):
    groups = {}
    for i, p in PAIRS: groups.setdefault(p, set()).add(beta.index(ctl[i]))
    worst = 1
    for p, S in groups.items():
        S = sorted(S); best = 26
        for s in S:                      # window starting at s covering all of S cyclically
            span = max((x - s) % 26 for x in S) + 1; best = min(best, span)
        worst = max(worst, best)
    return worst
if __name__ == "__main__":
    rng = random.Random(1); N = 100000
    for name, beta in (("AZ", AZ), ("rAZ", AZ[::-1]), ("KA", KA), ("rKA", KA[::-1])):
        k = bmin(CT, beta); le = 0
        for _ in range(N):
            ctl = "".join(rng.choice(AZ) for _ in range(97))
            le += bmin(ctl, beta) <= k
        print(f"cipher alphabet {name}: K4 needs key range B >= {k}; P(random <= {k}) = {le/N:.4f}")
