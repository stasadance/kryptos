#!/usr/bin/env python3
"""Iteration 6: do K4's aligned doublets argue against a plaintext-independent key?

Observation: 6 doublets in K4 (0-idx starts 18,25,32,42,46,67). Five sit at i = 4 mod 7.
Residue-4 pairs covered by the cribs: i = 25 (NO->QQ), 32 (ST->SS), 67 (IN->TT): all three are doublets,
although the plaintext letters differ.
Under ANY plaintext-independent key (the only model class left open), the ciphertext is a uniformly
random string independent of the plaintext, so the doublet pattern should look like that of random text.
Monte Carlo: P(some width w in 2..30 and residue r has >= 5 doublet starts) and, jointly, P(that every
crib-covered pair at that (w, r) is a doublet, with >= 3 such pairs).
"""
import random
CT = open("data/ciphertext.txt").read().strip()
CRIB = set(range(21, 34)) | set(range(63, 74))
def stat(ct):
    d = [i for i in range(96) if ct[i] == ct[i + 1]]
    best = (0, 0)
    for w in range(2, 31):
        for r in range(w):
            al = [i for i in d if i % w == r]
            cov = [i for i in range(r, 96, w) if i in CRIB and i + 1 in CRIB]
            allcrib = len(cov) >= 3 and all(i in al for i in cov)
            best = max(best, (len(al), int(allcrib)))
    return best
k4 = stat(CT); print("K4: max aligned doublets", k4[0], "| crib-covered pairs all doublets:", bool(k4[1]))
rng = random.Random(2); N = 200000; a = b = 0
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for _ in range(N):
    s = stat("".join(rng.choice(AZ) for _ in range(97)))
    a += s[0] >= 5; b += (s[0] >= 5 and s[1] == 1)
print(f"random strings: P(>=5 aligned) = {a/N:.5f}; P(>=5 aligned AND all >=3 crib pairs doublets) = {b/N:.6f}")
