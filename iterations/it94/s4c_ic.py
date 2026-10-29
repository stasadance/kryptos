#!/usr/bin/env python3
"""it95b: joint check. Low-entropy keys raise V21 but also raise the CT IC. K4 IC = 0.0361.
P(V21>=11 and IC<=0.0380) for the S4c models vs shuffled K4 (IC fixed 0.0361)."""
import numpy as np, s4a as S
m = 100000; i = np.arange(97)
def ic(C):
    cnt = np.stack([(C == x).sum(1) for x in range(26)], 1); return (cnt * (cnt - 1)).sum(1) / (97 * 96)
base = S.model('shuffled-K4', m); pb = (S.V21(base) >= 11).mean()
def rep(name, C):
    v, I = S.V21(C), ic(C); j = ((v >= 11) & (I <= 0.0380)).mean()
    print(f'{name:22s} meanIC={I.mean():.4f} P(IC<=.038)={(I<=0.038).mean():.2e} P(V21>=11)={(v>=11).mean():.2e} JOINT={j:.2e} (x{j/pb:.1f} vs shuffled {pb:.1e})', flush=True)
rep('OTP', S.q4(S.plaintexts(m), S.rng.integers(0, 26, (m, 97))))
for p in (21, 7):
    for mv in (2, 3, 4, 6, 8, 13, 26):
        rep(f'p{p} m{mv} Q4', S.q4(S.plaintexts(m), S.rng.integers(0, mv, (m, p))[:, i % p]))
G = np.zeros((m, 97), dtype=np.int64); G[:, :5] = S.rng.integers(0, 2, (m, 5))
for t in range(5, 97): G[:, t] = (G[:, t - 5] + G[:, t - 4]) % 2
rep('gromark2 Q4', S.q4(S.plaintexts(m), G))
