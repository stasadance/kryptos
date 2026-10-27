#!/usr/bin/env python3
"""Keyword-driven, plaintext-independent key-stream generators + exact crib tests (w-keygen, T14, 2026-10-26).

Positions are 1-indexed in K4; generators index the key stream by t = (i-1) + offset, t>=0.
Every generator returns a list of 97 ints mod 26 (a key VALUE stream) given a letter numbering g
(g = 'AZ' -> A=0..Z=25, or 'KA' -> index in KRYPTOSABCDEFGHIJLMNQUVWXZ).

Cipher models tested on a value stream k (C_i, P_i letters):
  fixed  : Vig  CA.idx(C) = PA.idx(P) + k ; Beau CA.idx(C) = k - PA.idx(P) ; vBeau = Vig with -k
           PA, CA any concrete alphabets (AZ, KA, keyword-mixed).            -> 24 crib equations
  vig1   : one ARBITRARY alphabet a: a(C) = a(P) + k   (Quagmire-III-general, K1/K2 structure)
           crib relations (derived symbolically, rel.py):  k33=0, k74=0, k28=k66, k24+k34=k29
  beau1  : one ARBITRARY alphabet a: a(C) + a(P) = k
           crib relations: k28=k66, k24+k34=k29+k33, k33 even, k74 even
  two    : two ARBITRARY alphabets a,b: b(C) = a(P) + k (covers Q1-Q4, Beaufort via b->-b, any relabel+mask)
           crib relations: k28=k66, k24+k34=k29+k33
  feasible(k, model) is EXACT: signed weighted union-find over Z26 + injectivity + backtracking packing.
Library use:  from keygen import *   ;  CLI: python3 keygen.py selftest
"""
import sys, random
from itertools import product

CT = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
CRIBS = {22: "EASTNORTHEAST", 64: "BERLINCLOCK"}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
N = 97

def crib_pairs(ct=CT):
    return [(s + k, ch, ct[s - 1 + k]) for s, w in CRIBS.items() for k, ch in enumerate(w)]

def keyed(kw, base=AZ):
    """keyword-mixed alphabet: keyword letters (dedup) then rest of base"""
    out = []
    for ch in kw + base:
        if ch not in out: out.append(ch)
    return "".join(out)

def num(word, g="AZ"):
    A = AZ if g == "AZ" else (KA if g == "KA" else g)
    return [A.index(c) for c in word]

def colorder(word):
    """keyed-columnar digit order: rank of each letter (ties left->right), 0-based"""
    idx = sorted(range(len(word)), key=lambda i: (word[i], i))
    r = [0] * len(word)
    for rank, i in enumerate(idx): r[i] = rank
    return r

# ---------------------------------------------------------------- generators
def g_periodic(w, o=0):
    L = len(w); return [w[(t + o) % L] for t in range(N)]

def g_progressive(w, s, m=None, o=0):
    """ACA progressive key: keyword cycle, every m stream letters (default m=len(w)) add +s.
    m=1 -> keyword + position counter s*t."""
    L = len(w); m = m or L
    return [(w[(t + o) % L] + s * ((t + o) // m)) % 26 for t in range(N)]

def g_twokey(w1, w2, o1=0, o2=0, sign=1):
    """compound key: k = w1[t+o1] + sign*w2[t+o2]  (period lcm(L1,L2))"""
    return [(w1[(t + o1) % len(w1)] + sign * w2[(t + o2) % len(w2)]) % 26 for t in range(N)]

def g_chain(primer, rule, mod=26, o=0):
    """chain addition / lagged Fibonacci on keyword values (letter Gromark = 'Vimark').
    rule 'gromark': x[n+L]=x[n]+x[n+1];  'fib': x[n+L]=x[n]+x[n+L-1];
         'diff': x[n+L]=x[n]-x[n+1];     'cum': x[n]=x[n-1]+w[n mod L] (running sum)"""
    L = len(primer); x = list(primer)
    if rule == "cum":
        x = [primer[0] % mod]
        while len(x) < N + o: x.append((x[-1] + primer[len(x) % L]) % mod)
    else:
        while len(x) < N + o:
            n = len(x) - L
            if rule == "gromark": v = x[n] + x[n + 1] if L > 1 else 2 * x[n]
            elif rule == "fib": v = x[n] + x[n + L - 1]
            elif rule == "diff": v = x[n] - (x[n + 1] if L > 1 else 0)
            else: raise ValueError(rule)
            x.append(v % mod)
    return [v % 26 for v in x[o:o + N]]

def g_interrupted(w, lengths, o=0):
    """interrupted key: keyword restarts at the start of each segment; segment lengths from a
    plaintext-independent rule (list, cycled). Inside a segment the keyword cycles if seg > L."""
    out = []; si = 0
    while len(out) < N + o:
        ln = max(1, lengths[si % len(lengths)]); si += 1
        out += [w[j % len(w)] for j in range(ln)]
    return out[o:o + N]

def g_colperm(kw, mode, o=0):
    """keyed columnar transposition of the position numbers 0..96 (width len(kw), cols read in key
    order). mode 'pi': k_t = pi[t] mod 26 (t-th number read out); 'inv': k_t = pi^-1[t] mod 26;
    'col': k_t = keyed column digit of the column holding t; 'row': row index of t (= floor(t/L))"""
    L = len(kw); order = colorder(kw)
    cols = sorted(range(L), key=lambda c: order[c])
    pi = [p for c in cols for p in range(c, N, L)]
    inv = [0] * N
    for r, p in enumerate(pi): inv[p] = r
    if mode == "pi": seq = pi
    elif mode == "inv": seq = inv
    elif mode == "col": seq = [order[t % L] for t in range(N)]
    else: raise ValueError(mode)
    seq = seq + seq
    return [v % 26 for v in seq[o:o + N]]

def g_linstep(a, b, m, o=0, c=0):
    """tableau traversal / clock-hand family: k_t = c + a*t + b*floor((t+o)/m)"""
    return [(c + a * t + b * ((t + o) // m)) % 26 for t in range(N)]

# ---------------------------------------------------------------- exact tests
def relations(k, model):
    """fast necessary relations (0-indexed list k, positions 1-indexed in comments)"""
    K = lambda i: k[i - 1] % 26
    if K(28) != K(66): return False
    if model == "vig1":
        return K(33) == 0 and K(74) == 0 and (K(24) + K(34) - K(29)) % 26 == 0
    r = (K(24) + K(34) - K(29) - K(33)) % 26 == 0
    if model == "beau1": return r and K(33) % 2 == 0 and K(74) % 2 == 0
    return r

def feasible(k, model, ct=CT, pairs=None):
    """EXACT: do alphabets exist making all 24 cribs encrypt correctly under key values k?"""
    pairs = pairs or crib_pairs(ct)
    par = {}
    dom = {}  # root -> set of allowed values (None = all)
    def find(x):
        if x not in par: par[x] = (x, 1, 0)
        p, s, v = par[x]
        if p == x: return x, 1, 0
        r, s2, v2 = find(p)
        res = (r, s * s2, (s * v2 + v) % 26); par[x] = res; return res
    for i, p, c in pairs:
        kv = k[i - 1] % 26
        if model == "two": a, b, sg = ("P", p), ("C", c), -1
        elif model == "vig1": a, b, sg = p, c, -1
        elif model == "beau1": a, b, sg = p, c, 1
        else: raise ValueError(model)
        # constraint: val(b) + sg*val(a) = kv
        ra, sa, va = find(a); rb, sb, vb = find(b)
        if ra == rb:
            coef = (sb + sg * sa) % 26; rhs = (kv - vb - sg * va) % 26
            allowed = {x for x in range(26) if (coef * x - rhs) % 26 == 0}
            d = dom.get(ra); dom[ra] = allowed if d is None else (d & allowed)
            if not dom[ra]: return False
        else:
            # sg*sa*ra = kv - sb*rb - vb - sg*va  ->  ra = f*(kv - vb - sg*va) - f*sb*rb, f = sg*sa (=±1)
            f = sg * sa
            par[ra] = (rb, -f * sb, (f * (kv - vb - sg * va)) % 26)
            if ra in dom:  # transfer domain constraint of ra onto rb
                allowed = {x for x in range(26) if ((-f * sb) * x + f * (kv - vb - sg * va)) % 26 in dom[ra]}
                d = dom.get(rb); dom[rb] = allowed if d is None else (d & allowed)
                del dom[ra]
                if not dom[rb]: return False
    # group nodes by root, then pack components with bitmasks (exact backtracking)
    comps = {}
    for x in list(par):
        r, s, v = find(x); comps.setdefault(r, []).append((x, s, v))
    two = model == "two"
    cand = []
    for r, nodes in comps.items():
        opts = []
        for val in sorted(dom.get(r, range(26))):
            mp = mc = 0; okc = True
            for x, s, v in nodes:
                bit = 1 << ((s * val + v) % 26)
                if two and x[0] == "C":
                    if mc & bit: okc = False; break
                    mc |= bit
                else:
                    if mp & bit: okc = False; break
                    mp |= bit
            if okc: opts.append((mp, mc))
        if not opts: return False
        cand.append(opts)
    # global shift gauge (vig1/two, no domain restriction anywhere): fix the biggest component
    cand.sort(key=lambda o: len(o))
    if model != "beau1" and not dom:
        big = max(range(len(cand)), key=lambda j: bin(cand[j][0][0]).count("1") + bin(cand[j][0][1]).count("1"))
        cand.insert(0, cand.pop(big)[:1])
    def place(ix, up, uc):
        if ix == len(cand): return True
        for mp, mc in cand[ix]:
            if mp & up or mc & uc: continue
            if place(ix + 1, up | mp, uc | mc): return True
        return False
    return place(0, 0, 0)

def fixed_ok(k, PA, CA, mode, ct=CT):
    """exact 24-crib test for concrete alphabets; mode in vig, beau, vbeau"""
    for s, w in CRIBS.items():
        for j, p in enumerate(w):
            i = s + j; kv = k[i - 1]; c = ct[i - 1]
            pc, cc = PA.index(p), CA.index(c)
            if mode == "vig": ok = (cc - pc - kv) % 26 == 0
            elif mode == "vbeau": ok = (cc - pc + kv) % 26 == 0
            else: ok = (cc + pc - kv) % 26 == 0
            if not ok: return False
    return True

def decrypt(k, PA, CA, mode, ct=CT):
    out = []
    for i, c in enumerate(ct):
        cc = CA.index(c)
        if mode == "vig": out.append(PA[(cc - k[i]) % 26])
        elif mode == "vbeau": out.append(PA[(cc + k[i]) % 26])
        else: out.append(PA[(k[i] - cc) % 26])
    return "".join(out)

def encrypt(pt, k, PA, CA, mode):
    out = []
    for i, p in enumerate(pt):
        pc = PA.index(p)
        if mode == "vig": out.append(CA[(pc + k[i]) % 26])
        elif mode == "vbeau": out.append(CA[(pc - k[i]) % 26])
        else: out.append(CA[(k[i] - pc) % 26])
    return "".join(out)

def latin_ok(sym, ct=CT):
    """alphabet-free filter (= tools/latin_filter.py) on any symbol stream (letters or values)"""
    P = crib_pairs(ct); bad = 0
    for x in range(len(P)):
        for y in range(x + 1, len(P)):
            (i, p, c), (j, q, d) = P[x], P[y]
            if p == q and c == d and sym[i - 1] != sym[j - 1]: return False
            if (p == q) != (c == d) and sym[i - 1] == sym[j - 1]: return False
    return True

def selftest():
    rnd = random.Random(1)
    # planted: random alphabets + random key must be feasible in its own model; relations must hold
    for model in ("two", "vig1", "beau1"):
        for _ in range(200):
            k = [rnd.randrange(26) for _ in range(N)]
            pt = "".join(rnd.choice(AZ) for _ in range(N))
            pt = pt[:21] + CRIBS[22] + pt[34:63] + CRIBS[64] + pt[74:]
            a = "".join(rnd.sample(AZ, 26)); b = a if model != "two" else "".join(rnd.sample(AZ, 26))
            mode = "beau" if model == "beau1" else "vig"
            ct = encrypt(pt, k, a, b, mode)
            assert feasible(k, model, ct), model
    print("selftest ok")

if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]: selftest()

# ---------------------------------------------------------------- motivated seeds & family enumeration
KEYWORDS = {  # word: rationale
    "KRYPTOS": "sculpture name; K1-K3 alphabet keyword",
    "PALIMPSEST": "K1 key", "PALIMPCEST": "K1 key as misspelt on Sanborn coding chart",
    "ABSCISSA": "K2 key", "IQLUSION": "K1 deliberate misspelling", "ILLUSION": "K1 word, corrected",
    "LAYERTWO": "K2 ending (2006 correction)", "BERLIN": "crib", "CLOCK": "crib",
    "BERLINCLOCK": "crib; shared with K5 at same position", "NORTHEAST": "crib",
    "EASTNORTHEAST": "crib", "SHADOW": "K1/Morse SHADOW FORCES", "LUCID": "Morse LUCID MEMORY",
    "MEMORY": "Morse LUCID MEMORY", "SANBORN": "artist", "SCHEIDT": "designer of the system",
    "LANGLEY": "site", "CIA": "site/owner", "TUTANKHAMUN": "K3 subject, 1986 Egypt trip",
    "CARTER": "K3 narrator", "VIRTUALLYINVISIBLE": "Morse", "SHADOWFORCES": "Morse",
    "LUCIDMEMORY": "Morse", "TISYOURPOSITION": "Morse (WHAT IS YOUR POSITION)",
    "DIGETALINTERPRETATIU": "Morse", "SOS": "Morse", "RQ": "Morse",
    "KRYPTOSABCDEFGHIJLMNQUVWXZ": "the KA tableau alphabet itself (tableau traversal)",
}
NUMBERINGS = {"AZ0": (AZ, 0), "AZ1": (AZ, 1), "KA0": (KA, 0), "KA1": (KA, 1)}

def kwvals(kw, nb):
    A, d = NUMBERINGS[nb]; return [(A.index(c) + d) % 26 for c in kw]

TABLEAUX = [(pa, ca, mode) for pa in ("AZ", "KA") for ca in ("AZ", "KA") for mode in ("vig", "beau", "vbeau")]

def required_keys(ct=CT, tableaux=TABLEAUX, alph={"AZ": AZ, "KA": KA}):
    """for each concrete tableau, the key value forced at each of the 24 crib positions"""
    out = {}
    P = crib_pairs(ct)
    for pa, ca, mode in tableaux:
        PA, CA = alph[pa], alph[ca]
        req = []
        for i, p, c in P:
            pc, cc = PA.index(p), CA.index(c)
            req.append((i - 1, (cc - pc) % 26 if mode == "vig" else (pc - cc) % 26 if mode == "vbeau" else (cc + pc) % 26))
        out[(pa, ca, mode)] = req
    return out

def families(keywords=KEYWORDS, full_offsets=True):
    """yield (family, params, keyvalues, symbolstream_or_None). Bounded, see findings/w-keygen.md §3."""
    kws = list(keywords)
    for kw in kws:
        L = len(kw)
        offs = range(L) if full_offsets else [0]
        for nb in NUMBERINGS:
            w = kwvals(kw, nb)
            # F1 progressive / counter: m in 1..26 and L, 2L ; s in Z26 (s=0 = plain periodic, once)
            for o in offs:
                yield ("F0-periodic", (kw, nb, o), g_periodic(w, o), [kw[(t + o) % L] for t in range(N)])
                for m in sorted(set(list(range(1, 27)) + [L, 2 * L])):
                    for s in range(1, 26):
                        yield ("F1-progressive", (kw, nb, o, m, s), g_progressive(w, s, m, o), None)
            # F3 chain addition on keyword values, mod 26 ; and mod 10 on keyed-columnar digits
            for rule in ("gromark", "fib", "diff", "cum"):
                for o in range(0, 2 * L + 1):
                    yield ("F3-chain26", (kw, nb, rule, o), g_chain(w, rule, 26, o), None)
        dig = [d % 10 for d in colorder(kw)]
        dig1 = [(d + 1) % 10 for d in colorder(kw)]
        for name, pr in (("ord0", dig), ("ord1", dig1)):
            for rule in ("gromark", "fib", "diff", "cum"):
                for o in range(0, 2 * L + 1):
                    yield ("F3-chain10", (kw, name, rule, o), g_chain(pr, rule, 10, o), None)
        # F4 interrupted keys (letter streams) with plaintext-independent segment rules
        rules = {"1,2,3..": list(range(1, 60)), "L,L+1..": list(range(L, L + 60)),
                 "L-1,L-2..1": list(range(max(L - 1, 1), 0, -1))}
        for kw2 in kws:
            rules["ord(" + kw2 + ")+1"] = [d + 1 for d in colorder(kw2)]
            rules["AZ(" + kw2 + ")+1"] = [AZ.index(c) + 1 for c in kw2]
        for rn, lens in rules.items():
            sym = g_interrupted(list(kw), lens)
            for nb in NUMBERINGS:
                A, d = NUMBERINGS[nb]
                yield ("F4-interrupted", (kw, nb, rn), [(A.index(c) + d) % 26 for c in sym], sym)
        # F5 keyed-columnar position streams
        for mode in ("pi", "inv", "col"):
            for o in range(0, 97 if mode != "col" else L):
                yield ("F5-colperm", (kw, mode, o), g_colperm(kw, mode, o), None)

def twokey_families(keywords=KEYWORDS):
    kws = [k for k in keywords if len(k) <= 20]
    for x, kw1 in enumerate(kws):
        for y, kw2 in enumerate(kws):
            if x == y: continue
            for nb in ("AZ0", "KA0"):
                w1, w2 = kwvals(kw1, nb), kwvals(kw2, nb)
                for sign in (1, -1):
                    if sign == 1 and y < x: continue
                    for o1 in range(len(kw1)):
                        for o2 in range(len(kw2)):
                            yield ("F2-twokey", (kw1, kw2, nb, sign, o1, o2), g_twokey(w1, w2, o1, o2, sign), None)
