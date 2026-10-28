#!/usr/bin/env python3
"""it63: running key = Cyrillic Projector plaintext (Sanborn's other CIA sculpture, decrypted 2003): KGB
agent-handling text (pt1) and the Sakharov/Pugwash KGB memo (pt2), transliterated two ways (BGN 'bgn',
one-to-one 'one'). Exact crib test via it23_scan.run for all role models, fwd and rev, every offset.
Planted control: encrypt English (cribs planted) with the same key text at a random offset, each model.
Usage: it63_cyrillic_projector.py DIR (DIR holds {pt1,pt2,all}_{bgn,one}.txt)"""
import sys, random
sys.path.insert(0, "iterations")
import it23_scan as S
d = sys.argv[1]; eng = S.norm(open("/tmp/claude-0/corpus/pg1342.txt", errors="ignore").read())
rng = random.Random(63); ok = tot = 0
for m, model in enumerate(S.MODELS2):          # planted control on the real key text
    src = S.norm(open(f"{d}/all_bgn.txt").read()) * 2
    al = list(range(26)); rng.shuffle(al)
    o = rng.randrange(0, len(src) // 2 - 100); po = rng.randrange(len(eng) - 200)
    pt = list(eng[po:po + 97]); pt[21:34] = "EASTNORTHEAST"; pt[63:74] = "BERLINCLOCK"
    rc, rp, rk, f = S.RC[m], S.RP[m], S.RK[m], S.FM[m]; inv = {v: i for i, v in enumerate(al)}
    val = lambda ro, ch: al[S.AZ.index(ch)] if ro == 0 else (S.AZ.index(ch) if ro == 1 else S.KA.index(ch))
    out = []
    for i, p in enumerate(pt):
        kv, pv = val(rk, src[o + i]), val(rp, p); cv = ((pv + kv) if f == 0 else ((kv - pv) if f == 1 else (pv - kv))) % 26
        out.append(S.AZ[inv[cv]] if rc == 0 else (S.AZ[cv] if rc == 1 else S.KA[cv]))
    hits, und, n = S.run("".join(out), "ctl", src)
    tot += 1; ok += any(h[1] == o and h[2] == model for h in hits)
print(f"controls recovered {ok}/{tot}", flush=True)
for name in ("pt1", "pt2", "all"):
    for sch in ("bgn", "one"):
        raw = S.norm(open(f"{d}/{name}_{sch}.txt").read())
        for dr, txt in (("fwd", raw), ("rev", raw[::-1])):
            hits, und, n = S.run(S.CT, f"{name}_{sch}", txt + txt[:96])
            print(f"{name}_{sch} {dr}: offsets {n} hits {hits} undecided {und}", flush=True)
