#!/usr/bin/env python3
"""it95 (coach S4c step 1): V21 / D7 for low-entropy period-21 keys: m-valued (m=2,3,4) random period-21 keys under
two alphabets (Q4) and one alphabet (Q3); binary LFSR keys with period dividing 21 (Gromark-2 recurrence and all
degree<=5 binary recurrences whose period divides 21); m-valued keys with period 7 and 3 for comparison."""
import numpy as np, itertools, s4a as S
m = 100000; i = np.arange(97); base = S.model('shuffled-K4', m); b0 = ((S.D7(base) >= 5).mean(), (S.V21(base) >= 11).mean())
def rep(name, C):
    d, v = S.D7(C), S.V21(C); pd, pv = (d >= 5).mean(), (v >= 11).mean()
    print(f'{name:24s} P(V21>=11)={pv:.2e} (x{pv/b0[1]:.0f})  P(D7>=5)={pd:.1e} (x{pd/b0[0]:.1f})  meanV21={v.mean():.2f}', flush=True)
for p in (21, 7, 3):
    for mv in (2, 3, 4):
        for same in (False, True):
            K = S.rng.integers(0, mv, (m, p))[:, i % p]; rep(f'p{p} m{mv} {"Q3" if same else "Q4"}', S.q4(S.plaintexts(m), K, same))
# binary LFSRs k_{t+L} = sum c_j k_{t+j} mod 2, L<=5, nonzero c_0; keep recurrences whose sequences have period | 21
def lfsr_period(c, L):
    best = 0
    for seed in itertools.product((0, 1), repeat=L):
        if not any(seed): continue
        s = list(seed)
        for t in range(200): s.append(sum(c[j] * s[t + j] for j in range(L)) % 2)
        for per in range(1, 100):
            if all(s[t] == s[t + per] for t in range(50, 150)): break
        best = max(best, per)
    return best
for L in range(2, 6):
    for c in itertools.product((0, 1), repeat=L):
        if c[0] == 0: continue
        per = lfsr_period(c, L)
        if 21 % per != 0 or per < 3: continue
        K = np.zeros((m, 97), dtype=np.int64); K[:, :L] = S.rng.integers(0, 2, (m, L))
        for t in range(L, 97): K[:, t] = (K[:, t - L:t] * np.array(c)).sum(1) % 2
        rep(f'LFSR L{L} c{"".join(map(str,c))} per{per} Q4', S.q4(S.plaintexts(m), K, False))
