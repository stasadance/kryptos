#!/usr/bin/env python3
"""Iteration 3: K4 enciphered with a flipped/rotated copy of the Kryptos tableau, periodic key.

Lead: Sanborn (quoted by a Schneier-blog commenter, Oct 2025, source unverified):
"You take that chart and you flip it this way and it turns into this chart, so the final
letter in a coding system might be the W up there."

Model: body T[r][c] = KA[(r+c)%26] transformed by one of the 8 symmetries of the square;
header alphabet H in {AZ, KA, reversed AZ, reversed KA}. Two lookup conventions:
  A: c = T'[r][H.index(p)]           (plaintext in header, key picks row)
  B: p found in row r at column x, c = H[x]   (reverse lookup)
Periodic key of period P: each residue class must admit one row r matching every crib pair.
Exact; a planted control is recovered first.
"""
import sys, random
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CT = open("data/ciphertext.txt").read().strip()
CRIBS = {22: "EASTNORTHEAST", 64: "BERLINCLOCK"}
PAIRS = [(s - 1 + j, p) for s, w in CRIBS.items() for j, p in enumerate(w)]
HEADERS = {"AZ": AZ, "KA": KA, "rAZ": AZ[::-1], "rKA": KA[::-1]}

def body(sym):
    T = [[KA[(r + c) % 26] for c in range(26)] for r in range(26)]
    f = {"id": lambda r, c: T[r][c], "fh": lambda r, c: T[r][25 - c], "fv": lambda r, c: T[25 - r][c],
         "r180": lambda r, c: T[25 - r][25 - c], "tr": lambda r, c: T[c][r], "atr": lambda r, c: T[25 - c][25 - r],
         "r90": lambda r, c: T[25 - c][r], "r270": lambda r, c: T[c][25 - r]}[sym]
    return [[f(r, c) for c in range(26)] for r in range(26)]

def rows_ok(Tb, H, conv, p, c):
    if conv == "A":
        j = H.index(p); return {r for r in range(26) if Tb[r][j] == c}
    return {r for r in range(26) if p in Tb[r] and H[Tb[r].index(p)] == c}

def consistent(ct, Tb, H, conv, P):
    for res in range(P):
        S = set(range(26))
        for i, p in PAIRS:
            if i % P == res:
                S &= rows_ok(Tb, H, conv, p, ct[i])
                if not S: return False
    return True

def scan(ct):
    hits = []
    for sym in ("id", "fh", "fv", "r180", "tr", "atr", "r90", "r270"):
        Tb = body(sym)
        for hn, H in HEADERS.items():
            for conv in "AB":
                for P in range(1, 49):
                    if consistent(ct, Tb, H, conv, P): hits.append((sym, hn, conv, P))
    return hits

if __name__ == "__main__":
    rng = random.Random(5)
    pt = list(("THISISAPLANTEDCONTROLTEXTFORTHEFLIPPEDTABLEAUTESTWHICHMUSTBERECOVEREDBYTHESCANNERBEFOREWETRUSTITATALL")[:97])
    for s, w in CRIBS.items(): pt[s - 1:s - 1 + len(w)] = w
    Tb = body("fh"); H = HEADERS["KA"]; key = [rng.randrange(26) for _ in range(13)]
    ctl = "".join(Tb[key[i % 13]][H.index(p)] for i, p in enumerate(pt))
    print("control (fh, KA, A, P=13) recovered:", ("fh", "KA", "A", 13) in scan(ctl))
    h = scan(CT)
    print("K4 hits:", len(h))
    for x in h: print("  ", x)
