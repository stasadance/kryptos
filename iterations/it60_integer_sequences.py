#!/usr/bin/env python3
"""it60: key = a simple integer sequence (primes, Fibonacci, Lucas, squares, cubes, triangular, pentagonal, powers of
2/3/5/7/10, Catalan, Pell, tribonacci, Padovan, digit sums, prime gaps, n*(n+1)*(2n+1)/6 ...), k_i = (m*s(i+o) + c)
mod 26 for offsets o<200, units m, c<26. Models: TWO arbitrary alphabets posC(C)=posP(P)+k (c, m partly absorbed)
and ONE alphabet a(C)=a(P)+k. Exact union-find + packing (tools/gromark.solve) after the X28==X66 prefilter.
Control: planted sequence-key encryptions must pass. Usage: it60_integer_sequences.py"""
import sys, random, re
from sympy import prime, isprime
sys.path.insert(0, 'tools'); import gromark as g
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; N = 400
def seqs():
    S = {}
    P = []; x = 2
    while len(P) < N: 
        if isprime(x): P.append(x)
        x += 1
    S['primes'] = P; S['primegaps'] = [P[i + 1] - P[i] for i in range(N - 1)] + [0]
    f = [0, 1]; [f.append(f[-1] + f[-2]) for _ in range(N)]; S['fib'] = f[:N]
    l = [2, 1]; [l.append(l[-1] + l[-2]) for _ in range(N)]; S['lucas'] = l[:N]
    p = [0, 1]; [p.append(2 * p[-1] + p[-2]) for _ in range(N)]; S['pell'] = p[:N]
    t = [0, 0, 1]; [t.append(t[-1] + t[-2] + t[-3]) for _ in range(N)]; S['trib'] = t[:N]
    pd = [1, 1, 1]; [pd.append(pd[-2] + pd[-3]) for _ in range(N)]; S['padovan'] = pd[:N]
    S['squares'] = [n * n for n in range(N)]; S['cubes'] = [n ** 3 for n in range(N)]
    S['triangular'] = [n * (n + 1) // 2 for n in range(N)]; S['pentagonal'] = [n * (3 * n - 1) // 2 for n in range(N)]
    S['sqpyr'] = [n * (n + 1) * (2 * n + 1) // 6 for n in range(N)]
    for b in (2, 3, 5, 7, 10): S[f'pow{b}'] = [b ** n for n in range(N)]
    c = [1]; [c.append(c[-1] * 2 * (2 * n + 1) // (n + 2)) for n in range(N)]; S['catalan'] = c[:N]
    S['digitsum'] = [sum(map(int, str(n))) for n in range(N)]; S['ncubes_mod'] = [n * n * n + n for n in range(N)]
    return S
UNITS = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
def set_ct(ct): g.CT = ct; g.CRIB[:] = [(s - 1 + j, p, ct[s - 1 + j]) for s, w in g.CRIBS.items() for j, p in enumerate(w)]
if __name__ == '__main__':
    S = seqs(); K4 = g.CT; rng = random.Random(60)
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    for t in range(4):
        name = rng.choice(list(S)); o = rng.randrange(200); m = rng.choice(UNITS); c = rng.randrange(26)
        key = [(m * S[name][o + i] + c) % 26 for i in range(97)]
        q = rng.randrange(len(eng) - 200); pt = list(eng[q:q + 97]); pt[21:34] = 'EASTNORTHEAST'; pt[63:74] = 'BERLINCLOCK'
        A = rng.sample(range(26), 26); Ai = {v: i for i, v in enumerate(A)}
        set_ct(''.join(AZ[Ai[(A[AZ.index(p)] + key[i]) % 26]] for i, p in enumerate(pt)))   # one alphabet
        print(f'control {name} o={o} m={m} c={c}: one-alph pass={bool(g.solve(key, rot=0))} two-alph pass={bool(g.solve(key))}', flush=True)
    set_ct(K4); two = one = 0; hits = []
    for name, s in S.items():
        n2 = n1 = 0
        for o in range(200):
            base = s[o:o + 97]
            for m in UNITS:
                k0 = [(m * v) % 26 for v in base]
                if k0[27] != k0[65]: continue        # X28 == X66 is invariant under +c
                if g.solve(k0): n2 += 1; hits.append((name, o, m, 'two'))
                for c in range(26):
                    k = [(v + c) % 26 for v in k0]
                    if g.solve(k, rot=0): n1 += 1; hits.append((name, o, m, c, 'ONE'))
        two += n2; one += n1; print(f'{name}: two-alph {n2}, one-alph {n1}', flush=True)
    print(f'total two-alph survivors {two} (of {len(S)*200*12} (seq,o,m)), one-alph survivors {one}')
    for h in hits:
        if 'ONE' in h or h[1] < 3: print('  HIT', h)
