#!/usr/bin/env python3
"""Gromark crib solver for K4 (w-gromark, T6 / H-301, 2026-10-26).

Model (ACA Gromark, Hall 1969; Bean HistoCrypt 2021 sec.2.5/3):
  key: primer k_0..k_{n-1} (base-b digits), k_{i+n} = (k_i + k_{i+1}) mod b   (n >= 2)
  enc: posC(C_i) = posP(P_i) + k_i  (mod 26), posP / posC = plain / cipher alphabets.
  With ARBITRARY alphabets the sign conventions (C=P-k, Beaufort C=k-P) are equivalent
  (negate/reflect an alphabet), so the "arb" model covers them all. With a FIXED alphabet
  (e.g. KRYPTOS-keyed KA) they are not: use --plain/--cipher with KA or its reverse.

Crib solver: weighted union-find over 52 nodes (P:a..z, C:a..z), one edge per crib letter
(posC - posP = k_i), optional fixed-alphabet chains, then
  (1) cycle consistency, (2) no two letters of one alphabet on the same slot inside a
  component, (3) exact packing of components into a 26-slot permutation (backtracking).
Decryption fills ONLY letters the crib system forces: position i decrypts to plain letter p
iff C_i's component also contains a plain node at offset off(C_i) - k_i. Otherwise '?'.

Usage:
  gromark.py scan BASE LEN            # exact crib-consistent primers (arb alphabets), numpy prefilter
  gromark.py dec BASE PRIMER [--plain KA|AZ|KAr|AZr] [--cipher ...] [--same]
       --same: one arbitrary alphabet, cipher = plain rotated by r (K1/K2 structure); tries r=0..25
Import: expand, solve, decrypt, scan
"""
import sys
CT = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
CRIBS = {22: "EASTNORTHEAST", 64: "BERLINCLOCK"}  # 1-indexed (facts/cribs.md)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
ALPHS = {"AZ": AZ, "KA": KA, "AZr": AZ[::-1], "KAr": KA[::-1]}
CRIB = [(s - 1 + j, p, CT[s - 1 + j]) for s, w in CRIBS.items() for j, p in enumerate(w)]  # 0-indexed
assert len(CT) == 97 and all(CT[i] == c for i, _, c in CRIB)
A = lambda ch: ord(ch) - 65


def expand(primer, base, n=97):
    k = list(primer)
    L = len(k)
    assert L >= 2
    while len(k) < n:
        k.append((k[-L] + k[-L + 1]) % base)
    return k[:n]


def digits(x, base, L):
    d = []
    for _ in range(L):
        d.append(x % base); x //= base
    return d[::-1]


class UF:
    def __init__(self):
        self.par = list(range(52)); self.off = [0] * 52; self.used = set()

    def find(self, x):
        if self.par[x] == x:
            return x, 0
        r, o = self.find(self.par[x])
        self.par[x] = r; self.off[x] = (self.off[x] + o) % 26
        return r, self.off[x]

    def union(self, a, b, w):  # pos(b) - pos(a) = w
        self.used.update((a, b))
        ra, oa = self.find(a); rb, ob = self.find(b)
        if ra == rb:
            return (ob - oa - w) % 26 == 0
        self.par[rb] = ra; self.off[rb] = (oa + w - ob) % 26
        return True

    def comps(self):
        cs = {}
        for x in self.used:
            r, o = self.find(x)
            cs.setdefault(r, []).append((x, o))
        return cs


def _pack(cs):
    """cs: list of (Pset, Cset) offsets; can components be shifted into disjoint slots?"""
    cs = sorted(cs, key=lambda t: -(len(t[0]) + len(t[1])))
    def rec(i, P, C):
        if i == len(cs):
            return True
        ps, qs = cs[i]
        for s in (range(1) if i == 0 else range(26)):
            p2 = {(x + s) % 26 for x in ps}; q2 = {(x + s) % 26 for x in qs}
            if not (p2 & P) and not (q2 & C) and rec(i + 1, P | p2, C | q2):
                return True
        return False
    return rec(0, set(), set())


def solve(key, plain=None, cipher=None, rot=None):
    """Return UF if the cribs are consistent with key under the model, else None.
    plain/cipher: fixed 26-letter alphabet strings (None = arbitrary).
    rot: if not None, single alphabet: posC(x) = posP(x) + rot for every letter x."""
    u = UF()
    for i, p, c in CRIB:
        if not u.union(A(p), 26 + A(c), key[i]):
            return None
    for alph, base in ((plain, 0), (cipher, 26)):
        if alph:
            for j, ch in enumerate(alph):
                if not u.union(base + A(alph[0]), base + A(ch), j):
                    return None
    if rot is not None:
        for x in range(26):
            if not u.union(x, 26 + x, rot):
                return None
    packs = []
    for r, mem in u.comps().items():
        P = [o for x, o in mem if x < 26]; C = [o for x, o in mem if x >= 26]
        if len(set(P)) < len(P) or len(set(C)) < len(C):
            return None
        packs.append((set(P), set(C)))
    return u if _pack(packs) else None


def complete(u, rng):
    """Random full (plain, cipher) alphabet pair consistent with solved system u (random packing + fill).
    rng: random.Random. Returns (P, C) as 26-letter strings (index = slot) or None."""
    comps = list(u.comps().values()); rng.shuffle(comps)
    P, C = [None] * 26, [None] * 26
    def rec(i):
        if i == len(comps):
            return True
        sh = list(range(26)); rng.shuffle(sh)
        for s in sh:
            slots = [((o + s) % 26, x) for x, o in comps[i]]
            if all((P if x < 26 else C)[t] is None for t, x in slots):
                for t, x in slots:
                    (P if x < 26 else C)[t] = chr(65 + x % 26)
                if rec(i + 1):
                    return True
                for t, x in slots:
                    (P if x < 26 else C)[t] = None
        return False
    if not rec(0):
        return None
    for A_ in (P, C):
        left = [ch for ch in AZ if ch not in A_]; rng.shuffle(left)
        for t in range(26):
            if A_[t] is None:
                A_[t] = left.pop()
    return "".join(P), "".join(C)


def encrypt(pt, key, P, C):
    return "".join(C[(P.index(p) + k) % 26] for p, k in zip(pt, key))


def decrypt(key, u):
    pmap = {}
    for r, mem in u.comps().items():
        for x, o in mem:
            if x < 26:
                pmap[(r, o)] = chr(65 + x)
    out = []
    for i, c in enumerate(CT):
        n = 26 + A(c)
        if n not in u.used:
            out.append("?"); continue
        r, o = u.find(n)
        out.append(pmap.get((r, (o - key[i]) % 26), "?"))
    return "".join(out)


def _constraints():
    """Symbolic cycle equalities / slot inequalities of the arb crib graph (for numpy prefilter)."""
    import collections
    adj = collections.defaultdict(list)
    for e, (i, p, c) in enumerate(CRIB):
        a, b = A(p), 26 + A(c)
        adj[a].append((b, e, +1)); adj[b].append((a, e, -1))
    pot, comp, eq, tree = {}, {}, [], set()
    for s in sorted(adj):
        if s in pot:
            continue
        pot[s] = [0] * len(CRIB); comp[s] = s; q = [s]
        while q:
            x = q.pop()
            for y, e, sg in adj[x]:
                if y not in pot:
                    v = pot[x][:]; v[e] += sg; pot[y] = v; comp[y] = s; tree.add(e); q.append(y)
    for e, (i, p, c) in enumerate(CRIB):
        if e not in tree:
            a, b = A(p), 26 + A(c)
            v = [pb - pa for pa, pb in zip(pot[a], pot[b])]; v[e] -= 1; eq.append(v)
    ne = []
    nodes = sorted(pot)
    for ia, a in enumerate(nodes):
        for b in nodes[ia + 1:]:
            if comp[a] == comp[b] and (a < 26) == (b < 26):
                ne.append([pb - pa for pa, pb in zip(pot[a], pot[b])])
    return eq, ne


def scan(base, L, chunk=1 << 21):
    """All primers (as int, base-b digits) whose expansion is crib-consistent with arbitrary alphabets.
    Exact: numpy applies the necessary cycle/slot conditions, Python solve() confirms (incl. packing)."""
    import numpy as np
    eq, ne = _constraints()
    pos = np.array([i for i, _, _ in CRIB])
    EQ = np.array(eq, dtype=np.int64).T if eq else None
    NE = np.array(ne, dtype=np.int64).T
    total, out = base ** L, []
    for start in range(0, total, chunk):
        x = np.arange(start, min(total, start + chunk), dtype=np.int64)
        k = np.zeros((len(x), 75), dtype=np.int64)
        t = x.copy()
        for j in range(L - 1, -1, -1):
            k[:, j] = t % base; t //= base
        for j in range(L, 75):
            k[:, j] = (k[:, j - L] + k[:, j - L + 1]) % base
        K = k[:, pos]
        sel = np.arange(len(x))
        if EQ is not None:
            sel = sel[((K @ EQ) % 26 == 0).all(1)]
        idx = sel[((K[sel] @ NE) % 26 != 0).all(1)]
        for v in x[idx]:
            if solve(expand(digits(int(v), base, L), base), None, None):
                out.append(int(v))
    return out


def fmt(v, base, L):
    return "".join("0123456789ABCDEFG"[d] for d in digits(v, base, L))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "scan":
        b, L = int(a[1]), int(a[2])
        s = scan(b, L)
        print(f"base {b} len {L}: {len(s)} survivors")
        for v in s:
            print(fmt(v, b, L))
    elif a and a[0] == "dec":
        b, pr = int(a[1]), a[2]
        key = expand([int(ch, 17) for ch in pr], b)
        pl = ALPHS.get(a[a.index("--plain") + 1]) if "--plain" in a else None
        ci = ALPHS.get(a[a.index("--cipher") + 1]) if "--cipher" in a else None
        rots = range(26) if "--same" in a else [None]
        for r in rots:
            u = solve(key, pl, ci, r)
            if u:
                d = decrypt(key, u)
                print(("" if r is None else f"rot={r:2d} ") + d, f"known={97 - d.count('?')}")
    else:
        print(__doc__)
