#!/usr/bin/env python3
"""it90 (N6): Hill n=4 AFFINE (never tested) and n=5 linear/affine, AZ and KA numbering, every block offset.
Work in the decryption form P = D*C + e (mod 26): each row j of (D,e) solves independently against the crib blocks
(blocks lying wholly inside a crib). Rows: brute force all 26^(n+1) (n=4) / per-row linear-algebra-free enumeration.
If every row has solutions, enumerate the product (all row combos), require D invertible mod 26, decrypt all full
blocks, score with the 6-gram LM. Null: same pipeline on K4 with the non-crib letters... (exact part: chance rate
computed from random-CT runs). usage: it90_hill4_affine.py"""
import sys, itertools, math
import numpy as np
CT = open('/mnt/project-files/k4/facts/ciphertext.txt').read().strip()
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; KA = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
CRIB = {**{21 + i: c for i, c in enumerate('EASTNORTHEAST')}, **{63 + i: c for i, c in enumerate('BERLINCLOCK')}}
def blocks(n, o):
    return [s for s in range(o, 97 - n + 1, n) if all(s + t in CRIB for t in range(n))]
_G = {}
def row_solutions(n, Cb, Pj, affine):
    """Cb: (m,n) cipher blocks, Pj: (m,) target plaintext letters -> list of (n+1) solutions (row of D, e)"""
    if n not in _G: _G[n] = np.indices((26,) * n, dtype=np.int16).reshape(n, -1).T.copy()
    G = _G[n]; sols = []
    if len(Cb) == 0: return None                                                   # unconstrained row
    V = (G.astype(np.int32) @ Cb.T.astype(np.int32)) % 26
    for e in (range(26) if affine else [0]):
        ok = ((V + e) % 26 == Pj[None]).all(1)
        for g in G[ok]: sols.append(list(map(int, g)) + [e])
    return sols
def rows_for(c, A, n, o, affine):
    """row j uses EVERY block (start s = o mod n, fully inside 0..96) whose position s+j is a crib position"""
    out = []
    for j in range(n):
        S = [s for s in range(o, 97 - n + 1, n) if s + j in CRIB]
        Cb = np.array([[c[s + t] for t in range(n)] for s in S]); Pj = np.array([A.index(CRIB[s + j]) for s in S])
        out.append(row_solutions(n, Cb, Pj, affine))
    return out
def run(ct, n, affine, verbose=True):
    res = []
    for an, A in (('AZ', AZ), ('KA', KA)):
        c = np.array([A.index(x) for x in ct]); 
        for o in range(n):
            rows, bl = rows_for(c, A, n, o, affine), blocks(n, o)
            cnt = [len(r) for r in rows]; tot = math.prod(cnt)
            res.append((an, o, len(bl), cnt, tot))
            if verbose: print(f'n={n} {"aff" if affine else "lin"} {an} off={o} blocks={len(bl)} row-solutions={cnt} combos={tot}', flush=True)
    return res
if __name__ == '__main__':
    for n, aff in ((4, True), (5, False), (5, True)):
        run(CT, n, aff)
