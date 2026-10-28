#!/usr/bin/env python3
"""it65: is K4 ANY digraphic substitution (Playfair, two/four-square, Hill-2, or an arbitrary 676-table), with
or without one null letter? Such a cipher maps equal PT digraphs to equal CT digraphs at the cipher's
alignment, so the repeat count of CT digraphs at alignment a is the same as in English PT. That count does not
depend on the table. Statistic: max over a in {0,1} of the number of repeated aligned digraph pairs, for the 97
letters and for 96 letters after deleting one letter (any position = null). Null: shuffled K4. Planted control:
English with cribs and a random digraph table. Usage: it65_digraphic.py"""
import random, re
from collections import Counter
K4 = open('data/ciphertext.txt').read().strip()
eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
def rep(s, a):
    c = Counter(s[i:i + 2] for i in range(a, len(s) - 1, 2)); return sum(v * (v - 1) // 2 for v in c.values())
def stat(s):
    best = max(rep(s, a) for a in (0, 1))
    for d in range(len(s)):                      # one deleted letter (null) anywhere
        t = s[:d] + s[d + 1:]; best = max(best, rep(t, 0))
    return best
rng = random.Random(65)
def planted():
    o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 96]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
    P = ''.join(P); tab = {}
    vals = list(range(676)); rng.shuffle(vals)
    out = ''
    for i in range(0, 96, 2):
        v = vals[(ord(P[i]) - 65) * 26 + ord(P[i + 1]) - 65]; out += chr(65 + v // 26) + chr(65 + v % 26)
    k = rng.randrange(97); return out[:k] + chr(65 + rng.randrange(26)) + out[k:]   # insert a null
x = stat(K4); print('K4 letters used:', len(set(K4)), '| K4 stat =', x)
nul = [stat(''.join(rng.sample(K4, 97))) for _ in range(500)]
pl = [stat(planted()) for _ in range(500)]
print(f'null mean {sum(nul)/500:.2f} P(null>=K4)={sum(t>=x for t in nul)/500:.3f}')
print(f'planted mean {sum(pl)/500:.2f} P(planted<=K4)={sum(t<=x for t in pl)/500:.3f}')
