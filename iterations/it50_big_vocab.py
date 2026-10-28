#!/usr/bin/env python3
"""it50: rerun the exact keyword-alphabet kernels it42 (PT-autokey L<=13), it43 (Quagmire I-III p<=25),
it46 (progressive periodic p<=24), it47 (CT-autokey L<=73) on a much larger keyword set:
dwyl english-words (370k) + enz german-wordlist (686k; umlauts as AE/OE/UE/SS and as plain A/O/U) +
motivated-term pairs (60x60).  Keywords are deduplicated by the resulting keyed alphabet (AZ fill)."""
import sys, re
sys.argv[1:] = sys.argv[1:] or ["/tmp/claude-0/it27/qg.bin"]
sys.path.insert(0, 'iterations')
import it42_autokey_keyword as M42, it43_quag_keyword as M43, it46_progressive_keyword as M46, it47_ctautokey_keyword as M47
from it44_quag4_keyword import MOT
from collections import Counter
def norm(w, plain):
    w = w.upper()
    w = w.replace('Ä', 'A' if plain else 'AE').replace('Ö', 'O' if plain else 'OE').replace('Ü', 'U' if plain else 'UE').replace('ß', 'SS')
    return re.sub('[^A-Z]', '', w)
W = set()
for l in open('/tmp/claude-0/wl/en.txt', errors='ignore'): W.add(norm(l.strip(), False))
for l in open('/tmp/claude-0/wl/de.txt', encoding='utf-8', errors='ignore'):
    W.add(norm(l.strip(), False)); W.add(norm(l.strip(), True))
W |= {a + b for a in MOT for b in MOT if a != b}
W = {w for w in W if len(w) >= 3}
seen = {}; 
for w in sorted(W, key=len):
    k = M42.keyed(w)
    if k not in seen: seen[k] = w
KW = list(seen.values()); print('words', len(W), 'distinct keyed alphabets', len(KW), flush=True)
qg = M42.A.qg
h42 = M42.run(M42.A.K4, KW, qg); print('it42 PT-autokey L<=13 hits:', len(h42), h42[:3], flush=True)
out = []; M43.run(M43.CT, KW, qg, out); print('it43 Quag I-III by p:', sorted(Counter(x[4] for x in out).items()), flush=True)
h46 = M46.run(M46.CT, KW); print('it46 progressive by p:', sorted(Counter(x[4] for x in h46).items()), [x for x in h46 if x[4] < 25][:10], flush=True)
h47 = M47.run(M47.CT, KW, range(1, 74)); print('it47 CT-autokey by L:', sorted(Counter(x[3] for x in h47).items()), sorted(h47, reverse=True)[:3], flush=True)
