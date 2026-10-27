#!/usr/bin/env python3
"""k4stats.py - small, reproducible statistics for short ciphertexts (default: K4).

Corpus used for findings/w-stats.md (letters only, Gutenberg header/footer stripped):
  curl -sSLO https://www.gutenberg.org/cache/epub/1661/pg1661.txt   # Sherlock Holmes
  curl -sSLO https://www.gutenberg.org/cache/epub/2701/pg2701.txt   # Moby Dick
Reproduce: python3 k4stats.py --corpus pg1661.txt pg2701.txt --trials 200000 --maxp 32 --compare
(~35 s, seed 1).

Usage:
  python3 k4stats.py --corpus a.txt [b.txt ...] [--text CT] [--trials 20000] [--seed 1]
                     [--maxp 30] [--compare]

Needs numpy. --corpus: any plain English text(s) (e.g. Project Gutenberg .txt);
letters are extracted, and random contiguous windows of len(CT) form the
"English" null. Other nulls: uniform random letters, and random permutations
of the ciphertext itself (preserves letter counts; tests positional structure).

Every p-value printed is a Monte Carlo tail proportion (k+1)/(N+1).
No keyspace search is done anywhere. Written by w-stats for the K4 project.
"""
import argparse, re, sys
from collections import Counter, defaultdict
import numpy as np

A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
# K1-K3 ciphertexts (letters only, '?' removed) from Elonka Dunin's sculpture
# transcript https://elonka.com/kryptos/transcript.html (lengths 63/369/336).
K1 = "EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJYQTQUXQBQVYUVLLTREVJYQTMKYRDMFD"
K2 = ("VFPJUDEEHZWETZYVGWHKKQETGFQJNCEGGWHKKDQMCPFQZDQMMIAGPFXHQRLGTIMVMZJANQLVKQEDAGDV"
      "FRPJUNGEUNAQZGZLECGYUXUEENJTBJLBQCRTBJDFHRRYIZETKZEMVDUFKSJHKFWHKUWQLSZFTIHHDDDUVH"
      "DWKBFUFPWNTDFIYCUQZEREEVLDKFEZMOQQJLTTUGSYQPFEUNLAVIDXFLGGTEZFKZBSFDQVGOGIPUFXHHDR"
      "KFFHQNTGPUAECNUVPDJMQCLQUMUNEDFQELZZVRRGKFFVOEEXBDMVPNFQXEZLGREDNQFMPNZGLFLPMRJQYA"
      "LMGNUVPDXVKPDQUMEBEDMHDAFMJGZNUPLGEWJLLAETG")
K3 = ("ENDYAHROHNLSRHEOCPTEOIBIDYSHNAIACHTNREYULDSLLSLLNOHSNOSMRWXMNETPRNGATIHNRARPESLNNE"
      "LEBLPIIACAEWMTWNDITEENRAHCTENEUDRETNHAEOETFOLSEDTIWENHAEIOYTEYQHEENCTAYCREIFTBRSPA"
      "MHHEWENATAMATEGYEERLBTEEFOASFIOTUETUAEOTOARMAEERTNRTIBSEDDNIAAHTTMSTEWPIEROAGRIEWF"
      "EBAECTDDHILCEIHSITEGOEAOSDDRYDLORITRKLMLEHAGTDHARDPNEOHMGFMFEUHEECDMRIPFEIMEHNLSST"
      "TRTVDOHW")
CRIBS = {22: "EASTNORTHEAST", 64: "BERLINCLOCK"}  # 1-indexed, = facts/cribs.md


def arr(s):
    return np.frombuffer(s.encode(), dtype=np.uint8).astype(np.int16) - 65


def load_corpus(paths):
    txt = []
    for p in paths:
        t = open(p, encoding="utf-8", errors="ignore").read()
        m1, m2 = t.find("*** START"), t.find("*** END")
        if m1 >= 0 and m2 > m1:
            t = t[t.find("\n", m1):m2]
        txt.append(re.sub("[^A-Z]", "", t.upper()))
    return arr("".join(txt))


# ---------- vectorised statistics on a (T, n) int array ----------
def autocorr(X, maxs=None):
    """c[:, s-1] = #{i : x_i == x_{i+s}} for s = 1..maxs."""
    n = X.shape[1]; maxs = maxs or n - 1
    return np.stack([(X[:, :-s] == X[:, s:]).sum(1) for s in range(1, maxs + 1)], 1)


def ic_from_ac(C, n):
    pairs = sum(n - s for s in range(1, n))
    return C[:, :n - 1].sum(1) / pairs


def period_ic(C, n, p):
    """pooled IC of the p columns = coincident pairs at lags kp / all pairs at lags kp."""
    lags = list(range(p, n, p))
    return C[:, [l - 1 for l in lags]].sum(1) / sum(n - l for l in lags)


def counts(X):
    return np.stack([(X == k).sum(1) for k in range(26)], 1)


def chi2(X, pe):
    E = X.shape[1] * pe
    return ((counts(X) - E) ** 2 / E).sum(1)


def repeated_types(codes):
    """number of distinct code values occurring >= 2 times, per row."""
    S = np.sort(codes, 1)
    eq = S[:, 1:] == S[:, :-1]
    start = eq.copy(); start[:, 1:] &= ~eq[:, :-1]
    return start.sum(1)


def vbigram_rep(X, w):
    return repeated_types(X[:, :-w] * 26 + X[:, w:])


def ngram_rep(X, k):
    n = X.shape[1]; c = np.zeros((X.shape[0], n - k + 1), dtype=np.int64)
    for j in range(k):
        c = c * 26 + X[:, j:n - k + 1 + j]
    return repeated_types(c)


def ptail(null, obs, upper=True):
    k = (null >= obs - 1e-12).sum() if upper else (null <= obs + 1e-12).sum()
    return (k + 1) / (len(null) + 1)


# ---------- nulls ----------
def null_perm(x, T, rng):
    return np.stack([rng.permutation(x) for _ in range(T)])


def null_uniform(n, T, rng):
    return rng.integers(0, 26, size=(T, n)).astype(np.int16)


def null_english(corp, n, T, rng):
    st = rng.integers(0, len(corp) - n, size=T)
    return corp[st[:, None] + np.arange(n)[None, :]]


# ---------- deterministic crib tests ----------
def crib_pairs():
    return [(s - 1 + i, ch) for s, w in CRIBS.items() for i, ch in enumerate(w)]


def transposition_supply(ct):
    need = Counter(ch for _, ch in crib_pairs()); have = Counter(ct)
    return {c: (need[c], have[c]) for c in sorted(need) if need[c] > have[c]}


def periodic_conflicts(ct, p):
    """Arbitrary per-column bijections (period p, no transposition): return first conflict."""
    fwd, back = defaultdict(dict), defaultdict(dict)
    for i, pc in crib_pairs():
        cc, col = ct[i], i % p
        if fwd[col].setdefault(pc, cc) != cc:
            return f"col {col}: plain {pc} -> {fwd[col][pc]} and {cc}"
        if back[col].setdefault(cc, pc) != pc:
            return f"col {col}: cipher {cc} <- {back[col][cc]} and {pc}"
    return None


def kasiski(ct, kmin=2):
    out = []
    for k in range(kmin, 8):
        pos = defaultdict(list)
        for i in range(len(ct) - k + 1):
            pos[ct[i:i + k]].append(i + 1)
        for g, ps in sorted(pos.items()):
            if len(ps) > 1:
                out.append((g, ps, [b - a for a, b in zip(ps, ps[1:])]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default=K4)
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--maxp", type=int, default=30)
    ap.add_argument("--compare", action="store_true", help="also K1-K3 summary")
    a = ap.parse_args()
    ct = re.sub("[^A-Z]", "", a.text.upper()); n = len(ct); x = arr(ct)[None, :]
    rng = np.random.default_rng(a.seed); T = a.trials
    corp = load_corpus(a.corpus)
    pe = np.bincount(corp, minlength=26) / len(corp)
    kE = float((pe ** 2).sum())
    P, U, E = null_perm(x[0], T, rng), null_uniform(n, T, rng), null_english(corp, n, T, rng)
    Cx, CP, CU, CE = autocorr(x), autocorr(P), autocorr(U), autocorr(E)
    pr = lambda *s: print(*s)

    pr(f"# k4stats  n={n}  trials={T}  seed={a.seed}  corpus_letters={len(corp)}  kappa_E={kE:.4f}")
    cnt = Counter(ct)
    pr("\n## Letter counts")
    pr(" ".join(f"{c}{cnt[c]}" for c in A))
    pr("sorted:", " ".join(f"{c}{k}" for c, k in cnt.most_common()))
    pr("missing letters:", "".join(c for c in A if cnt[c] == 0) or "none",
       "| distinct:", len(cnt))
    ic = ic_from_ac(Cx, n)[0]
    icU, icE = ic_from_ac(CU, n), ic_from_ac(CE, n)
    pr("\n## IC (kappa) and chi-square vs English")
    pr(f"IC={ic:.5f}  (x26={ic*26:.3f})  pairs-coincident={int(Cx[0].sum())}")
    pr(f"uniform null: mean {icU.mean():.5f} sd {icU.std():.5f}  P(IC<=obs)={ptail(icU, ic, False):.4f}")
    pr(f"English-window null: mean {icE.mean():.5f} sd {icE.std():.5f}  min {icE.min():.5f}"
       f"  P(IC<=obs)={ptail(icE, ic, False):.2e}")
    c2x, c2U, c2E = chi2(x, pe)[0], chi2(U, pe), chi2(E, pe)
    pr(f"chi2 vs English freq = {c2x:.1f};  English null mean {c2E.mean():.1f} 99.9%={np.quantile(c2E,.999):.1f}"
       f" max {c2E.max():.1f}  P(chi2>=obs|English)={ptail(c2E, c2x):.2e}")
    pr(f"  uniform null mean chi2 {c2U.mean():.1f}  P(chi2>=obs|uniform)={ptail(c2U, c2x):.3f}")
    c2flat = ((np.array([cnt[c] for c in A]) - n / 26) ** 2 / (n / 26)).sum()
    fU = ((counts(U) - n / 26) ** 2 / (n / 26)).sum(1)
    pr(f"chi2 vs flat = {c2flat:.1f} (df 25); P(chi2flat>=obs | uniform) = {ptail(fU, c2flat):.3f}")

    pr("\n## Doubled letters (adjacent equal) / autocorrelation")
    d = int(Cx[0, 0])
    pr(f"doubles={d}: " + " ".join(f"{ct[i]*2}@{i+1}" for i in range(n - 1) if ct[i] == ct[i + 1]))
    pr(f"perm null mean {CP[:,0].mean():.2f}  P(>=obs)={ptail(CP[:,0], d):.4f};"
       f"  English null mean {CE[:,0].mean():.2f}  P(>=obs|English)={ptail(CE[:,0], d):.4f}")
    S = min(48, n - 1)
    mu, sd = CP[:, :S].mean(0), CP[:, :S].std(0) + 1e-9
    zx = (Cx[0, :S] - mu) / sd; zP = ((CP[:, :S] - mu) / sd).max(1)
    top = np.argsort(-zx)[:6]
    pr("autocorr top shifts (shift:coinc/expected z):",
       " ".join(f"{s+1}:{Cx[0,s]}/{mu[s]:.1f} z{zx[s]:.2f}" for s in top))
    pr(f"max-z over shifts 1..{S} = {zx.max():.2f}; family-wise P(max z>=obs | perm) = {ptail(zP, zx.max()):.3f}")
    for L in (7,):
        pr(f"lag-{L} coincidences (1-indexed i, i+{L}):", " ".join(f"{ct[i]}@{i+1}/{i+1+L}" for i in range(n - L) if ct[i] == ct[i + L]))
    def dcol(X, w):
        D = (X[:, :-1] == X[:, 1:])
        res = np.arange(n - 1) % w
        return np.stack([(D & (res == r)).sum(1) for r in range(w)], 1).max(1)
    pr("doublets sharing one column at width w (max over columns), perm null:")
    fam = []
    for w in range(2, 22):
        o = dcol(x, w)[0]; nP = dcol(P, w); fam.append((ptail(nP, o), w, o, nP))
        if w in (7, 14, 21): pr(f"  w={w}: {o} of {d} doublets in one column, P(>=)={ptail(nP,o):.4f}")
    Zd = np.stack([f[3] for f in fam], 1); md, sdd = Zd.mean(0), Zd.std(0) + 1e-9
    zo_ = ((np.array([f[2] for f in fam]) - md) / sdd).max(); zn_ = ((Zd - md) / sdd).max(1)
    pr(f"  family-wise over w=2..21: P(max z>={zo_:.2f})={ptail(zn_, zo_):.4f}")
    low = np.argsort(zx)[:3]
    pr("lowest shifts:", " ".join(f"{s+1}:{Cx[0,s]}/{mu[s]:.1f}" for s in low))

    pr("\n## Kasiski: repeated n-grams (1-indexed positions, spacings)")
    ks = kasiski(ct)
    for k in (2, 3, 4):
        rows = [r for r in ks if len(r[0]) == k]
        pr(f"{k}-grams repeated: {len(rows)}  " + "; ".join(f"{g}{ps} d={sp}" for g, ps, sp in rows))
    for k in (2, 3):
        o = ngram_rep(x, k)[0]; nP = ngram_rep(P, k); nE = ngram_rep(E, k)
        pr(f"repeated {k}-gram types={o}: perm mean {nP.mean():.2f} P(>=)={ptail(nP,o):.3f};"
           f" English mean {nE.mean():.2f} P(>=|Eng)={ptail(nE,o):.3f}")

    pr(f"\n## Periodic column IC (pooled), p=1..{a.maxp}")
    pr("Under (any transposition) then period-p polyalphabetic with ARBITRARY alphabets, the pooled")
    pr("column IC equals the plaintext's -> English-window null applies (power column).")
    pr(" p  ICcols  x26   P(>=|perm)  P(<=obs|English p-periodic)  English mean")
    best = []
    for p in range(1, a.maxp + 1):
        o = period_ic(Cx, n, p)[0]; nP = period_ic(CP, n, p); nE = period_ic(CE, n, p)
        best.append((ptail(nP, o), p, o))
        pr(f"{p:2d}  {o:.4f}  {o*26:.2f}   {ptail(nP,o):.4f}      {ptail(nE,o,False):.2e}            {nE.mean():.4f}")
    # family-wise over periods for the perm null: max standardized
    Mx = np.stack([period_ic(CP, n, p) for p in range(1, a.maxp + 1)], 1)
    m, s = Mx.mean(0), Mx.std(0) + 1e-9
    ox = np.array([period_ic(Cx, n, p)[0] for p in range(1, a.maxp + 1)])
    zo = ((ox - m) / s).max(); zn = ((Mx - m) / s).max(1)
    pr(f"best period by perm-p: p={min(best)[1]} (p={min(best)[0]:.4f}); family-wise P(max z>={zo:.2f})={ptail(zn, zo):.3f}")

    pr("\n## Vertical repeated bigrams at width w (Bean 2021 metric: distinct types seen >=2x)")
    rowsw = []
    for w in range(2, 49):
        o = vbigram_rep(x, w)[0]; nP = vbigram_rep(P, w)
        rowsw.append((ptail(nP, o), w, o, nP.mean()))
    for pv, w, o, mm in sorted(rowsw)[:6]:
        pr(f"w={w:2d}: {o} repeats (perm mean {mm:.2f}) P(>=)={pv:.5f}")
    for w in (7, 21, 31):
        r = [t for t in rowsw if t[1] == w][0]
        pr(f"[layout] w={w}: {r[2]} repeats, perm mean {r[3]:.2f}, P={r[0]:.4f}")
    Z = np.stack([vbigram_rep(P, w) for w in range(2, 49)], 1)
    mz, sz = Z.mean(0), Z.std(0) + 1e-9
    oz = ((np.array([t[2] for t in rowsw]) - mz) / sz).max(); nz = ((Z - mz) / sz).max(1)
    pr(f"family-wise over w=2..48: max z={oz:.2f}, P(max z>=obs | perm)={ptail(nz, oz):.4f}")

    pr("\n## Deterministic crib constraints (no statistics needed)")
    sup = transposition_supply(ct)
    pr("transposition-only letter supply shortfalls (need,have):", sup or "none")
    bad = [p for p in range(1, n + 1) if periodic_conflicts(ct, p)]
    ok = [p for p in range(1, n + 1) if not periodic_conflicts(ct, p)]
    pr(f"periodic arbitrary-alphabet substitution (no transposition): consistent periods = {ok}")
    for p in (1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 13, 14, 21, 26, 31):
        pr(f"  p={p}: {periodic_conflicts(ct, p) or 'consistent'}")
    sel = [i + 1 for i, ch in crib_pairs() if ct[i] == ch]
    pr("self-encrypting crib positions:", sel)

    if a.compare:
        pr("\n## K1-K4 comparison")
        pr("sect   n   IC     x26   chi2/n(vsEng) doubles(exp_perm) bestP(pooledIC x26, p<=30)")
        for nm, t in (("K1", K1), ("K2", K2), ("K3", K3), ("K4", ct)):
            y = arr(t)[None, :]; m = len(t); C = autocorr(y)
            icv = ic_from_ac(C, m)[0]; cc = Counter(t)
            expd = (m - 1) * sum(v * (v - 1) for v in cc.values()) / (m * (m - 1))
            pics = [(period_ic(C, m, p)[0], p) for p in range(2, 31)]
            top3 = sorted(pics, reverse=True)[:3]
            pr(f"{nm} {m:4d} {icv:.4f} {icv*26:.2f}  {chi2(y,pe)[0]/m:.2f}   {int(C[0,0])}({expd:.1f})"
               f"   " + ", ".join(f"p{p}:{v*26:.2f}" for v, p in top3))


if __name__ == "__main__":
    main()
