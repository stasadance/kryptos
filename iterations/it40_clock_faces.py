#!/usr/bin/env python3
"""it40 (H-802): one keyed alphabet per Weltzeituhr face, built from ALL names on the face, on the
REAL pre-1997 face text (transcribed from Deutsche Fotothek scans; data/weltzeituhr_V*.txt).
Faces not yet read ('?') are skipped: a crib pair is scored only if its face is known.
Configs: keyword order (upper+lower, lower+upper, upper, lower) x fill AZ/KA x model S1-S4
(as tools/w-clock/face_test.py) x alignment s (K4 index 0 -> face s) x direction +-1.
A true config satisfies ALL eligible pairs.  Null: K4 with the 24 crib CT letters permuted.
Control: random face text, plant cribs under a random config, check it is found.
Usage: python3 it40_clock_faces.py data/weltzeituhr_V1.txt [...]"""
import sys, random
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; KA = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
CT = open('/mnt/project-files/k4/facts/ciphertext.txt').read().strip()
PAIRS = [(21 + i, ch) for i, ch in enumerate('EASTNORTHEAST')] + [(63 + i, ch) for i, ch in enumerate('BERLINCLOCK')]
def keyed(w, base):
    s = []
    for ch in w + base:
        if ch.isalpha() and ch not in s: s.append(ch)
    return ''.join(s)
M = {'S1': lambda K, p: K[AZ.index(p)], 'S2': lambda K, p: AZ[K.index(p)],
     'S3': lambda K, p: K[KA.index(p)], 'S4': lambda K, p: KA[K.index(p)]}
def load(fn):
    F = {}
    for l in open(fn):
        if l.startswith('#') or not l.strip(): continue
        o, u, lo = [x.strip() for x in l.split('|')]
        F[int(o) % 24] = None if u == '?' else (u.replace(' ', ''), lo.replace(' ', ''))
    return F
ORD = {'UL': lambda u, l: u + l, 'LU': lambda u, l: l + u, 'U': lambda u, l: u, 'L': lambda u, l: l}
def configs(F):
    for on, of in ORD.items():
        for bn, base in (('AZ', AZ), ('KA', KA)):
            A = {f: keyed(of(*v), base) for f, v in F.items() if v is not None}
            for mn, enc in M.items():
                for d in (1, -1):
                    for s in range(24):
                        yield (on, bn, mn, d, s), A, enc
def score(F, ct):
    out = []
    for cfg, A, enc in configs(F):
        d, s = cfg[3], cfg[4]
        el = sat = 0
        for i, p in PAIRS:
            f = (d * i + s) % 24
            if f in A:
                el += 1; sat += enc(A[f], p) == ct[i]
        out.append((sat == el, el, sat, cfg))
    return out
def best(res):
    full = [r for r in res if r[0] and r[1] >= 6]
    return max(full, key=lambda r: r[1]) if full else max(res, key=lambda r: (r[2] - r[1], r[2]))
if __name__ == '__main__':
    rng = random.Random(40)
    for fn in sys.argv[1:]:
        F = load(fn)
        known = sorted(f for f, v in F.items() if v is not None)
        # control: replace known face text by random letters, plant
        ok = 0
        for t in range(10):
            G = {f: ((''.join(rng.choice(AZ) for _ in range(20)), '') if v is not None else None) for f, v in F.items()}
            cfgs = list(configs(G)); cfg, A, enc = rng.choice(cfgs)
            ct = list(CT)
            for i, p in PAIRS:
                f = (cfg[3] * i + cfg[4]) % 24
                if f in A: ct[i] = enc(A[f], p)
            r = [x for x in score(G, ''.join(ct)) if x[3] == cfg][0]
            ok += r[0]
        res = score(F, CT)
        nfull = sum(1 for r in res if r[0] and r[1] >= 6)
        top = sorted(res, key=lambda r: (r[0], r[2], -r[1]), reverse=True)[:5]
        pos = [r for r in res]
        nulls = []
        pos_ = [i for i, _ in PAIRS]
        for _ in range(200):
            L = [CT[i] for i in pos_]; rng.shuffle(L); ct = list(CT)
            for i, x in zip(pos_, L): ct[i] = x
            rr = score(F, ''.join(ct))
            nulls.append(max(r[2] for r in rr))
        print(f'{fn}: known faces {len(known)}/24; control planted-config fully satisfied {ok}/10')
        print(f'  K4: configs fully satisfying >=6 eligible pairs: {nfull}; best sat counts: {[(r[2], r[1], r[3]) for r in top]}')
        print(f'  null (200 permuted-crib CTs): max sat mean {sum(nulls)/len(nulls):.2f}, 95% {sorted(nulls)[189]}, max {max(nulls)}; K4 max sat {max(r[2] for r in res)}')
