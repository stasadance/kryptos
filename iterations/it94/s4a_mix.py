#!/usr/bin/env python3
"""it94b: composite keys suggested by S4a: periodic-7 + Gromark base 2, periodic-7 + binary noise, periodic-7 + grid-21 rows."""
import numpy as np, s4a as S
m = 100000; i = np.arange(97); base = S.model('shuffled-K4', m); b0 = ((S.D7(base) >= 5).mean(), (S.V21(base) >= 11).mean())
def rep(name, C):
    d, v = S.D7(C), S.V21(C); pd, pv = (d >= 5).mean(), (v >= 11).mean()
    print(f'{name:16s} P(D7>=5)={pd:.2e} (x{pd/b0[0]:.1f})  P(V21>=11)={pv:.2e} (x{pv/b0[1]:.1f})  both={((d>=5)&(v>=11)).mean():.1e}', flush=True)
P = S.plaintexts(m); c7 = S.rng.integers(0, 26, (m, 7))[:, i % 7]
G = np.zeros((m, 97), dtype=np.int64); G[:, :5] = S.rng.integers(0, 2, (m, 5))
for t in range(5, 97): G[:, t] = (G[:, t - 5] + G[:, t - 4]) % 2
rep('per7+gromark2', S.q4(P, c7 + G)); P = S.plaintexts(m)
rep('per7+binary', S.q4(P, c7 + S.rng.integers(0, 2, (m, 97)))); P = S.plaintexts(m)
rep('per7+rows21', S.q4(P, c7 + S.rng.integers(0, 26, (m, 5))[:, i // 21])); P = S.plaintexts(m)
rep('gromark2 Q4', S.q4(P, G))
