#!/usr/bin/env python3
"""it48: re-run the exact keyword-alphabet kernels of it42 (PT-autokey L<=13), it43 (Quagmire I-III p<=25),
it46 (progressive periodic p<=24) and it47 (CT-autokey L<=73) with OTHER keyword-alphabet constructions:
  KAfill  : keyword + remaining letters in KRYPTOS-alphabet order
  revfill : keyword + remaining letters Z..A
  col     : keyword(+rest A-Z) written in rows of width len(dedup keyword), read down the columns left->right
  colsort : same, columns read in alphabetical order of the keyword letters
The kernels are unchanged (controls in it42-47); only the alphabet builder is swapped."""
import sys
sys.argv[1:] = sys.argv[1:] or ["/tmp/claude-0/it27/qg.bin"]
sys.path.insert(0, 'iterations')
import it42_autokey_keyword as M42, it43_quag_keyword as M43, it46_progressive_keyword as M46, it47_ctautokey_keyword as M47
from collections import Counter
AZ = M42.AZ; KA = M42.A.KA
def dedup(w):
    s = []
    for ch in w:
        if ch not in s: s.append(ch)
    return s
def kafill(w): d = dedup(w); return ''.join(d + [c for c in KA if c not in d])
def revfill(w): d = dedup(w); return ''.join(d + [c for c in AZ[::-1] if c not in d])
def colgrid(w, sort):
    d = dedup(w); full = d + [c for c in AZ if c not in d]; n = len(d)
    if n < 2: return ''.join(full)
    cols = list(range(n))
    if sort: cols.sort(key=lambda j: d[j])
    return ''.join(full[r] for j in cols for r in range(j, 26, n))
BUILD = {'KAfill': kafill, 'revfill': revfill, 'col': lambda w: colgrid(w, False), 'colsort': lambda w: colgrid(w, True)}
if __name__ == '__main__':
    W = M42.words(); qg = M42.A.qg
    for bn, f in BUILD.items():
        assert sorted(f('KRYPTOS')) == list(AZ)
        for m in (M42, M43, M46, M47): m.keyed = f
        h42 = M42.run(M42.A.K4, W, qg)
        out = []; M43.run(M43.CT, W, qg, out); q43 = Counter(x[4] for x in out)
        h46 = M46.run(M46.CT, W); q46 = Counter(x[4] for x in h46)
        h47 = M47.run(M47.CT, W, range(1, 74)); q47 = Counter(x[3] for x in h47)
        print(f'{bn}: it42 PT-autokey L<=13 hits={len(h42)} | it43 Quag p: {sorted(q43.items())} | it46 prog p: {sorted(q46.items())} | it47 CT-autokey L: {sorted(q47.items())}', flush=True)
        for x in sorted(h42, reverse=True)[:3]: print('   it42', x[:5], x[5][:60])
        best47 = sorted(h47, reverse=True)[:3]
        for x in best47: print('   it47', x)
