#!/usr/bin/env python3
"""it45b: score every conflict-free it45 config (PT-autokey L=14..96, keyword alphabets) on K4 by the mean
quadgram log-prob over fully determined non-crib quadgrams (>= 30 required).  English ~ -2.5..-2.9/quadgram
with this table (calibrated below on planted texts); random ~ -3.6 or lower."""
import sys
sys.argv[1:] = sys.argv[1:] or ["/tmp/claude-0/it27/qg.bin"]
import numpy as np, re, random, heapq
from numba import njit
sys.path.insert(0, 'iterations')
from it45_autokey_keyword_long import prop, words, keyed, A, CR, AZ, KAI
qg = A.qg
@njit(cache=True)
def qscore(p, qg):
    s = 0.0; n = 0
    for i in range(94):
        if p[i] >= 0 and p[i+1] >= 0 and p[i+2] >= 0 and p[i+3] >= 0:
            if (21 <= i and i + 3 <= 33) or (63 <= i and i + 3 <= 73): continue
            s += qg[((p[i]*26+p[i+1])*26+p[i+2])*26+p[i+3]]; n += 1
    return s, n
c = np.array([AZ.index(x) for x in A.K4], dtype=np.int64); p = np.zeros(97, dtype=np.int64)
eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
rng = random.Random(1); es = []
for _ in range(200):
    o = rng.randrange(len(eng)-100); e = np.array([AZ.index(x) for x in eng[o:o+97]], dtype=np.int64)
    s, n = qscore(e, qg); es.append(s/n)
print('English 97-letter mean qg/quadgram: min %.3f mean %.3f' % (min(es), sum(es)/len(es)))
top = []
for w in words():
    K = keyed(w); a = np.array([K.index(x) for x in AZ], dtype=np.int64); inv = np.array([AZ.index(x) for x in K], dtype=np.int64)
    for L in range(14, 97):
        for form in range(3):
            for kr in range(3):
                if prop(c, a, inv, L, form, kr, CR, p) < 0: continue
                s, n = qscore(p, qg)
                if n < 30: continue
                item = (s/n, n, w, L, form, kr, ''.join(AZ[x] if x >= 0 else '.' for x in p))
                if len(top) < 30: heapq.heappush(top, item)
                elif item[0] > top[0][0]: heapq.heapreplace(top, item)
for x in sorted(top, reverse=True)[:15]: print('%.3f n=%d %s L=%d f=%d kr=%d %s' % x)
