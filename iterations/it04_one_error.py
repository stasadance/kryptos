#!/usr/bin/env python3
"""Iteration 4: did one carving error at a crib position hide a true key in the phase-1 generator screen?

For every keyword-driven generator stream in tools/keygen.py (families + twokey_families) and each
of the 12 fixed tableaux, count crib positions where the stream (shifted by any constant c) disagrees
with the key the cribs require. A true key with one carving error at a crib gives exactly 1 mismatch.
Chance of <=1 mismatch for a random stream: ~ 26*(24*25+1)/26^24, negligible -> decisive.
"""
import sys, collections, random
sys.path.insert(0, "tools")
import keygen as K

def best(stream, req):
    bestm = 99
    for c in range(26):
        m = sum((stream[i] + c) % 26 != v for i, v in req)
        if m < bestm: bestm = m
        if bestm == 0: break
    return bestm

def screen(ct, gens):
    REQ = K.required_keys(ct)
    hits, n = [], 0
    for fam, params, k, _ in gens:
        n += 1
        for tab, req in REQ.items():
            m = best(k, req)
            if m <= 1: hits.append((m, fam, params, tab))
    return n, hits

if __name__ == "__main__":
    # control: plant a progressive key on English with one carving error inside a crib
    rng = random.Random(11)
    fam = next(g for g in K.families(["PALIMPSEST"]) if g[0] == "F1-progressive" and g[1][3] == 5 and g[1][4] == 3)
    pt = list(("ANOTHERCONTROLTEXTTHATRUNSLONGENOUGHTOCOVERALLNINETYSEVENPOSITIONSOFTHECIPHERTEXTWITHOUTANYPROBLEMSATALL")[:97])
    for s, w in K.CRIBS.items(): pt[s - 1:s - 1 + len(w)] = w
    ctl = list(K.encrypt("".join(pt), fam[2], K.KA, K.KA, "vig"))
    ctl[29] = "Z" if ctl[29] != "Z" else "Y"            # carving error at 1-indexed position 30
    n, h = screen("".join(ctl), [fam])
    print("control (1 error at pos 30) found with 1 mismatch:", any(x[0] == 1 for x in h))
    n, h = screen(K.CT, list(K.families()) + list(K.twokey_families()))
    print("streams screened:", n, "x 12 tableaux x 26 shifts; K4 hits with <=1 mismatch:", len(h))
    for x in h[:20]: print("  ", x)
