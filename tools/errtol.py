#!/usr/bin/env python3
"""Error-tolerant periodic-substitution crib solver for K4 (w-errtol, 2026-10-26).

Error models (positions 1-indexed in the CARVED ciphertext):
  sub D      : the carved letters at crib positions in D (|D|<=2) are wrong -> those crib
               constraints are dropped (exact relaxation; errors at non-crib positions do not
               affect crib consistency).
  om j / in j: one letter omitted before carved position j, or carved letter j is an
               inserted junk letter.  Only j in the crib gap (35..64) changes crib alignment
               (BERLINCLOCK key index shifts by d=+1/-1 relative to EASTNORTHEAST); j outside
               the gap is equivalent to no error for periodic families.
Families (period p, class r = keyindex mod p):
  GEN   arbitrary bijection per class.
  TAB   fixed tableau: posP,posC in {AZ,KA}, Vig-style posC=posP+s_r or Beau-style posC=s_r-posP
        (variant Beaufort = Vig-style with negated key: same constraints/decrypts).
  Q1/Q2 Quagmire I / II (cipher / plain alphabet fixed = AZ or KA, other arbitrary), Q3 (one
        arbitrary alphabet used for both), Q4 (two arbitrary alphabets); Vig- and Beau-style.
        Exact z3 (Int encoding, Distinct, gauge fixed), timeout per check.
Forced text: a plaintext letter at a non-crib position is FORCED if it is identical in every
  solution of the config (GEN: ct letter seen in a crib pair of the same class; Q: z3 table of
  forced (class, ct letter) entries, computed by solution-elimination).
Scoring: NG = conditional English n-gram (<=4, back-off) LLR vs uniform per forced letter (context =
  known preceding letters incl. crib letters); null = same config on K4 with non-crib CT letters
  shuffled (max over omission point j when applicable); H1 = English windows with identical mask.
Usage: python3 errtol.py consistency P [P...]   GEN/TAB min-error table (fast, no z3)
       library use: see workers/w-errtol/scripts/ (s3 = z3 SAT sweep, s4 = forced tables,
       s6 = scoring; s6 expects corpus/pg2600.txt, corpus/pg1342.txt in cwd), plant.py = planted test.
"""
import itertools, os, random, sys, math, collections
from z3 import Solver, Int, Distinct, Or, And, sat, unsat

CT = open(os.environ.get('K4CT', '/mnt/project-files/k4/facts/ciphertext.txt')).read().strip()
assert len(CT) == 97
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KA = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
CRIB = {}
for s, w in ((22, 'EASTNORTHEAST'), (64, 'BERLINCLOCK')):
    for i, ch in enumerate(w):
        CRIB[s + i] = ch            # 1-indexed carved position -> plaintext letter
CRIBPOS = sorted(CRIB)


def keyidx_map(err):
    """carved 1-idx position -> key index (1-based, true plaintext position) or None (junk)."""
    kind = err[0]
    m = {}
    for i in range(1, 98):
        if kind == 'om' and i >= err[1]:
            m[i] = i + 1
        elif kind == 'in' and i == err[1]:
            m[i] = None
        elif kind == 'in' and i > err[1]:
            m[i] = i - 1
        else:
            m[i] = i
    return m


def crib_pairs(err):
    km = keyidx_map(err)
    drop = set(err[1]) if err[0] == 'sub' else set()
    return [(km[i], CRIB[i], CT[i - 1]) for i in CRIBPOS if i not in drop]


def error_configs(maxsub=2, shifts=True):
    for n in range(maxsub + 1):
        for D in itertools.combinations(CRIBPOS, n):
            yield ('sub', D)
    if shifts:
        yield ('om', 50)   # representative of d=+1 (any j in 35..64 gives same crib alignment)
        yield ('in', 50)   # representative of d=-1 (any j in 35..63)


# ---------------- GEN ----------------
def gen_tables(pairs, p):
    """return (p2c, c2p) per class or None if inconsistent"""
    p2c = [dict() for _ in range(p)]
    c2p = [dict() for _ in range(p)]
    for k, pl, c in pairs:
        r = k % p
        if p2c[r].get(pl, c) != c or c2p[r].get(c, pl) != pl:
            return None
        p2c[r][pl] = c
        c2p[r][c] = pl
    return p2c, c2p


def gen_forced_table(pairs, p):
    t = gen_tables(pairs, p)
    if t is None:
        return None
    return {(r, c): pl for r in range(p) for c, pl in t[1][r].items()}


# ---------------- TAB ----------------
def tab_forced_table(pairs, p, PA, CA, style):
    key = {}
    for k, pl, c in pairs:
        s = (CA.index(c) - PA.index(pl)) % 26 if style == 'V' else (CA.index(c) + PA.index(pl)) % 26
        r = k % p
        if key.get(r, s) != s:
            return None
        key[r] = s
    F = {}
    for r, s in key.items():
        for c in AZ:
            x = (CA.index(c) - s) % 26 if style == 'V' else (s - CA.index(c)) % 26
            F[(r, c)] = PA[x]
    return F


# ---------------- Quagmire (z3) ----------------
class QModel:
    """model in {'Q1AZ','Q1KA','Q2AZ','Q2KA','Q3','Q4'}, style 'V' or 'B'"""

    def __init__(self, pairs, p, model, style, timeout_ms=60000):
        self.p, self.model, self.style = p, model, style
        S = Solver()
        S.set('timeout', timeout_ms)
        self.S = S
        Pv = {x: Int('P' + x) for x in AZ}
        Cv = {x: Int('C' + x) for x in AZ}
        if model in ('Q1AZ', 'Q1KA'):
            alph = AZ if model == 'Q1AZ' else KA
            self.C = {x: alph.index(x) for x in AZ}
            self.P = Pv
        elif model in ('Q2AZ', 'Q2KA'):
            alph = AZ if model == 'Q2AZ' else KA
            self.P = {x: alph.index(x) for x in AZ}
            self.C = Cv
        elif model == 'Q3':
            self.P = Pv
            self.C = Pv
        else:
            self.P, self.C = Pv, Cv
        for D in (self.P, self.C):
            vs = [v for v in D.values() if not isinstance(v, int)]
            if vs:
                for v in vs:
                    S.add(v >= 0, v < 26)
                S.add(Distinct(vs))
        # gauge fixing (valid for both styles: shift of a free alphabet absorbed by s)
        if not isinstance(self.P['A'], int):
            S.add(self.P['A'] == 0)
        if model == 'Q4' or model.startswith('Q2'):
            S.add(self.C['A'] == 0)
        self.s = [Int('s%d' % r) for r in range(p)]
        for v in self.s:
            S.add(v >= 0, v < 26)
        for k, pl, c in pairs:
            S.add(self.rel(pl, c, k % p))

    def expr(self, pl, c, r):
        # Vig: C - P - s in {0,-26};  Beau: C + P - s in {0,26}
        if self.style == 'V':
            return self.C[c] - self.P[pl] - self.s[r], (0, -26)
        return self.C[c] + self.P[pl] - self.s[r], (0, 26)

    def rel(self, pl, c, r):
        e, vals = self.expr(pl, c, r)
        return Or([e == v for v in vals])

    def nrel(self, pl, c, r):
        e, vals = self.expr(pl, c, r)
        return And([e != v for v in vals])

    def check(self):
        return self.S.check()

    def table_from_model(self, m):
        ev = lambda v: v if isinstance(v, int) else m.eval(v, model_completion=True).as_long()
        P = {x: ev(self.P[x]) for x in AZ}
        C = {x: ev(self.C[x]) for x in AZ}
        inv = {v: x for x, v in P.items()}
        s = [m.eval(v, model_completion=True).as_long() for v in self.s]
        T = {}
        for r in range(self.p):
            for c in AZ:
                pos = (C[c] - s[r]) % 26 if self.style == 'V' else (s[r] - C[c]) % 26
                T[(r, c)] = inv[pos]
        return T

    def forced_table(self, keys=None):
        """entries (r,c) whose plaintext is identical in all solutions. keys: subset to test."""
        if self.S.check() != sat:
            return None
        T = self.table_from_model(self.S.model())
        cand = set(keys if keys is not None else T)
        forced = {}
        while cand:
            rc = next(iter(cand))
            self.S.push()
            self.S.add(self.nrel(T[rc], rc[1], rc[0]))
            res = self.S.check()
            if res == sat:
                T2 = self.table_from_model(self.S.model())
                cand = {x for x in cand if T2[x] == T[x]}
                cand.discard(rc)
            elif res == unsat:
                forced[rc] = T[rc]
                cand.discard(rc)
            else:              # timeout: treat as NOT forced (conservative)
                cand.discard(rc)
            self.S.pop()
        return forced


# ---------------- forced text & scoring ----------------
def forced_text(F, p, err, ct=CT):
    """plaintext in key-index coordinates; returns (text, mask of forced non-crib indices)"""
    km = keyidx_map(err)
    n = 97 + (1 if err[0] == 'om' else -1 if err[0] == 'in' else 0)
    txt = ['?'] * n
    mask = set()
    for i in range(1, 98):
        k = km[i]
        if k is None:
            continue
        if i in CRIB:
            txt[k - 1] = CRIB[i]
            continue
        x = F.get((k % p, ct[i - 1]))
        if x is not None:
            txt[k - 1] = x
            mask.add(k - 1)
    return ''.join(txt), mask


def shuffled_ct(rng):
    nc = [i for i in range(1, 98) if i not in CRIB]
    letters = [CT[i - 1] for i in nc]
    rng.shuffle(letters)
    ct = list(CT)
    for i, x in zip(nc, letters):
        ct[i - 1] = x
    return ''.join(ct)


# ---------------- English n-gram LLR scorer ----------------
class NG:
    """conditional English n-gram (n<=4) with add-0.5 smoothing; LLR vs uniform, per forced letter"""
    def __init__(self, txt):
        self.c=[collections.Counter() for _ in range(5)]
        for n in range(1,5):
            self.c[n]=collections.Counter(txt[i:i+n] for i in range(len(txt)-n+1))
        self.c[0]=collections.Counter({'':len(txt)})
        self.cache={}
    def lp(self,ctx,x):
        k=(ctx,x)
        if k in self.cache: return self.cache[k]
        while ctx and self.c[len(ctx)][ctx]<20: ctx=ctx[1:]   # back off on rare contexts
        v=math.log10((self.c[len(ctx)+1][ctx+x]+0.5)/(self.c[len(ctx)][ctx]+13))
        self.cache[k]=v; return v
    def llr(self,txt,mask):
        """sum over k in mask of log10 P(x_k|known preceding <=3 letters) + log10(26); also n"""
        s=0.0
        for k in mask:
            ctx=''
            j=k-1
            while j>=0 and len(ctx)<3 and txt[j]!='?': ctx=txt[j]+ctx; j-=1
            s+=self.lp(ctx,txt[k])+math.log10(26)
        return s


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'consistency':
        A = {'AZ': AZ, 'KA': KA}
        for p in map(int, sys.argv[2:]):
            row = []
            for n in range(3):
                ok = [D for D in itertools.combinations(CRIBPOS, n) if gen_tables(crib_pairs(('sub', D)), p)]
                if ok:
                    row.append(f'GEN min subs={n} e.g. {ok[:4]}'); break
            else:
                row.append('GEN needs >=3 subs')
            row.append('GEN shift ok: ' + str([e[0] for e in (('om', 50), ('in', 50)) if gen_tables(crib_pairs(e), p)]))
            tabs = [f'{a}{b}{s}' for a in A for b in A for s in 'VB'
                    if any(tab_forced_table(crib_pairs(e), p, A[a], A[b], s) is not None
                           for e in list(error_configs(2, True)))]
            row.append('TAB revivable(<=2 subs or 1 shift): ' + str(tabs))
            print(p, ' | '.join(row))
