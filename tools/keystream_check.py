#!/usr/bin/env python3
"""K4 crib keystream & period/autokey consistency checker (w-crib, T3, 2026-10-26).

Usage:  python3 keystream_check.py                 # full report, AZ + KRYPTOS alphabets
        python3 keystream_check.py --alph QWERTY...# add a custom 26-letter alphabet (named CUSTOM)
Import: from keystream_check import keystream, period_check, gen_periods, autokey_check

Definitions (positions 1-indexed in output; x,y,k = indices in the chosen alphabet):
  vig   C = P + K      beau  C = K - P      vbeau  C = P - K    (all mod 26)
  period_check: for each period p, any two crib positions i==j (mod p) must have equal key.
     'vacuous' periods put no two crib positions in the same residue -> cribs give no test.
  gen_periods: most general periodic polyalphabetic (independent arbitrary alphabet per
     residue class): only requires per-class injectivity. A period failing here fails for
     EVERY periodic substitution incl. Quagmire I-IV with any alphabets.
  autokey_check: CT-autokey K_i = C_{i-L}; PT-autokey K_i = P_{i-L} (direct crib pairs only;
     residue-chain propagation is stronger, see findings/w-crib-algebra.md)."""
import sys
CT = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
CRIBS = {22: "EASTNORTHEAST", 64: "BERLINCLOCK"}  # 1-indexed starts, facts/cribs.md
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
RULES = {"vig": lambda x, y: (y - x) % 26, "beau": lambda x, y: (y + x) % 26,
         "vbeau": lambda x, y: (x - y) % 26}
assert len(CT) == 97

def crib_pairs():
    return [(s - 1 + k, ch, CT[s - 1 + k]) for s, w in CRIBS.items() for k, ch in enumerate(w)]

def keystream(rule, alph):
    f = RULES[rule]
    return [(i, alph[f(alph.index(p), alph.index(c))]) for i, p, c in crib_pairs()]

def period_check(ks, maxp=97):
    """-> list of (p, status) with status 'vacuous' | 'consistent(n checks)' | 'conflict@i,j'"""
    out = []
    for p in range(1, maxp + 1):
        seen, n, st = {}, 0, None
        for i, k in ks:
            r = i % p
            if r in seen:
                n += 1
                if seen[r][1] != k:
                    st = f"conflict@{seen[r][0]+1},{i+1}"; break
            else:
                seen[r] = (i, k)
        out.append((p, st or ("vacuous" if n == 0 else f"consistent({n} checks)")))
    return out

def gen_periods(maxp=97):
    ok = []
    for p in range(1, maxp + 1):
        cls, good = {}, True
        for i, pt, c in crib_pairs():
            m = cls.setdefault(i % p, {})
            if m.get(pt, c) != c: good = False; break
            m[pt] = c
        if good and all(len(set(m.values())) == len(m) for m in cls.values()):
            ok.append(p)
    return ok

def autokey_check(rule, alph, mode):
    """mode 'ct' or 'pt'. -> list of (L, n_checks) consistent."""
    ks = dict(keystream(rule, alph)); pt = {i: p for i, p, _ in crib_pairs()}; res = []
    for L in range(1, 97):
        if mode == "ct": chk = [ks[i] == CT[i - L] for i in ks if i - L >= 0]
        else:            chk = [ks[i] == pt[i - L] for i in ks if i - L in pt]
        if all(chk): res.append((L, len(chk)))
    return res

if __name__ == "__main__":
    alphs = [("AZ", AZ), ("KA", KA)]
    if "--alph" in sys.argv:
        a = sys.argv[sys.argv.index("--alph") + 1].upper()
        assert sorted(a) == list(AZ), "custom alphabet must be a permutation of A-Z"
        alphs.append(("CUSTOM", a))
    print("self-encryptions:", [(i + 1, p) for i, p, c in crib_pairs() if p == c])
    for an, al in alphs:
        for rule in RULES:
            ks = keystream(rule, al); s = "".join(k for _, k in ks)
            pc = period_check(ks)
            good = [p for p, st in pc if st.startswith("consistent")]
            vac = [p for p, st in pc if st == "vacuous"]
            ct = [L for L, n in autokey_check(rule, al, "ct") if n]
            ptk = [L for L, n in autokey_check(rule, al, "pt") if n]
            print(f"{rule:5} {an:6} ENE={s[:13]} BC={s[13:]}")
            print(f"      periodic consistent (non-vacuous): {good or 'NONE'}; vacuous: {vac[:3]}..{vac[-1]}")
            print(f"      CT-autokey L with checks passing: {ct or 'NONE'}; PT-autokey: {ptk or 'NONE'}")
    print("general periodic (arbitrary alphabet per class) consistent periods <=52:",
          [p for p in gen_periods(52) if p not in (27, 28, 29)])
