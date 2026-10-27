#!/usr/bin/env python3
"""Iteration 14: the aligned doublets are copying errors. At crib positions 26, 33, 68 (0-idx, second
letter of each residue-4 doublet) the true ciphertext letter was overwritten by its left neighbour.
Mask those 3 positions and re-test periodic Vig/Beau/varBeau over AZ and KA, periods 1..48.
Phase 1 only allowed <=2 errors anywhere; this is 3 errors at fixed positions.
Null: mask 3 random crib positions (20k draws) to get the base rate of consistent periods."""
import random
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CT = open("data/ciphertext.txt").read().strip()
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
PAIRS = [(s + j, p) for s, w in CRIBS.items() for j, p in enumerate(w)]
def key(c, p, al, m):
    c, p = al.index(c), al.index(p)
    return {"vig": c - p, "beau": c + p, "vbeau": p - c}[m] % 26
def consistent(mask, ct=CT):
    out = []
    for an, al in (("AZ", AZ), ("KA", KA)):
        for m in ("vig", "beau", "vbeau"):
            for per in range(1, 49):
                seen, ok = {}, True
                for i, p in PAIRS:
                    if i in mask: continue
                    k = key(ct[i], p, al, m)
                    if seen.setdefault(i % per, k) != k: ok = False; break
                if ok: out.append((an, m, per))
    return out
if __name__ == "__main__":
    rng = random.Random(3)
    # control: periodic Vig/KA period 11 key, then overwrite positions 26,33,68 by left neighbour
    pt = list("X" * 97)
    for s, w in CRIBS.items(): pt[s:s + len(w)] = w
    for i in range(97):
        if pt[i] == "X": pt[i] = rng.choice(AZ)
    kk = [rng.randrange(26) for _ in range(11)]
    ctl = [KA[(KA.index(p) + kk[i % 11]) % 26] for i, p in enumerate(pt)]
    for j in (26, 33, 68): ctl[j] = ctl[j - 1]
    ctl = "".join(ctl)
    print("control, unmasked:", [h for h in consistent(set(), ctl) if h[2] <= 24][:5])
    print("control, masked  :", [h for h in consistent({26, 33, 68}, ctl) if h[2] <= 24][:5])
    real = consistent({26, 33, 68}); print("K4 masked, consistent configs (per<=48):", real)
    small = lambda hs: sum(1 for h in hs if h[2] <= 20)
    crib_pos = [i for i, _ in PAIRS]; T = 20000
    base = sum(small(consistent(set(rng.sample(crib_pos, 3)))) > 0 for _ in range(T)) / T
    print(f"null: P(any config with period<=20 consistent | 3 random crib positions masked) = {base:.4f}")
    print("K4 configs with period<=20:", small(real))
