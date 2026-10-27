# w-gromark T6 — H-301 Gromark survivors: exact solver, decrypts, significance   (w-gromark, 2026-10-26 UTC)

**No candidate.** Nothing passed tools/crib_check.py with readable English. No model produced a full decrypt to check.
The fixed-alphabet versions (KRYPTOS-keyed, K1/K2 style) are refuted for every base and primer length tested. The arbitrary-alphabet
version cannot be refuted by the cribs. However, every surviving primer forces fewer plaintext letters than it would if it were the true key.

## 0. Tools & reproducibility
- `tools/gromark.py`: exact solver. It has `expand`, `solve`, `decrypt`, `complete`, `encrypt` and `scan`. CLI: `gromark.py scan B L`, `gromark.py dec B PRIMER [--plain KA|KAr|AZ|AZr] [--cipher ..] [--same]`.
  - Model: k_{i+n} = (k_i + k_{i+1}) mod b, and posC(C_i) = posP(P_i) + k_i (mod 26). This matches Bean 2021 §2.5 ("count that many steps right in the cipher alphabet") and w-crib §7.
  - Method: weighted union-find over 26 P-nodes and 26 C-nodes. It checks cycle consistency, same-alphabet slot collisions and an exact component packing into a permutation.
  - `scan` runs an exact numpy prefilter of 2 cycle equalities and 30 slot inequalities, then confirms each survivor with `solve`.
- `tools/quadgram.py`: English quadgram model. It was built from PG #2600 (War and Peace) and PG #1342 (Pride and Prejudice): 3.07M letters and 63,958 distinct quadgrams. The model file is in scratch; rebuild it with `quadgram.py build`.
- Validation:
  - Reproduces Bean exactly: 39 primers for b10/5 (incl. 26717, 84393, 98800), 3301/6740/9903 for b10/4, and 00351/00537/40311/40577 for b8/5. This matches w-crib §7.
  - Prefilter is identical to brute-force `solve` on 6 (base, length) cases.
  - Positive control: 200/200 planted Gromark encryptions were recovered with no wrong forced letters. Modes covered: arbitrary alphabets, P=KA, P=C=KA rotated, and a single alphabet with rotation (workers/w-gromark/posctl.py).
- Scripts are in workers/w-gromark/: dec_all, score, h1, kw, basescan2, posctl. They expect the scratch layout; the paths are at the top of each script.
- The 46 partial decrypts are in workers/w-gromark/partial_decrypts.tsv.

## 1. Crib graph structure (explains why the arb model can't be killed)
- The 24 crib edges join 13 P-letters and 14 C-letters into **5 components**. Each component has the form (P,C): (2,2), (2,1), (2,2), (4,5), (3,4).
- That gives only 2 independent cycle equalities. All the rest of the constraint power comes from 30 slot inequalities.
- Each component can be shifted freely relative to the others. A non-crib position therefore decrypts only when its CT letter is in a component *and* the offset lands on one of that component's 2-4 P-letters.

## 2. Decrypts of the 46 survivors
Alphabet models tried per primer:

| model | survivors (of 46) |
|---|---|
| arb plain / arb cipher (w-crib/Bean pairing) | 46 (partial decrypts below) |
| plain ∈ {KA, KA-reversed, AZ, AZ-reversed}, cipher arbitrary | **0** |
| cipher ∈ {KA, KAr, AZ, AZr}, plain arbitrary | **0** |
| plain & cipher both fixed from {KA,KAr,AZ,AZr}² (rotation free; covers Vig/Beau/var-Beau sign conventions) | **0** |
| one arbitrary alphabet, cipher = plain rotated by r (K1/K2 structure, any keyword), r=0..25 | **0** |
| 64 keyword alphabets (keyed and ACA columnar-keyed, fwd/rev) as plain, cipher, or both | **0** of 8,832 tests |

The 16 keywords were KRYPTOS, PALIMPSEST, ABSCISSA, IQLUSION, BERLIN, CLOCK, BERLINCLOCK, SHADOW, LAYERTWO, SANBORN, SCHEIDT, EASTNORTHEAST, LANGLEY, CIA, EGYPT and WELTZEITUHR.

⇒ Under every KRYPTOS-keyed or keyword-alphabet constraint, no primer is crib-consistent. There is nothing to decrypt.

The arb/arb partial decrypts force between 1 and 13 non-crib letters each (mean 7.3). The richest examples:
```
26717  ?????????????????N???EASTNORTHEAST???I?S??LT?A?L????A????????E?BERLINCLOCK????L?O?????A??????????
00351  ??AS?????????????????EASTNORTHEAST?N?ON??NTT????????K????????O?BERLINCLOCK????L???????A?????????T
98800  ???T?????????????????EASTNORTHEAST?I?OO??O?S??L??????A?????????BERLINCLOCK???????????????????K??T
3301   ?????????????????????EASTNORTHEAST?O???S?N?????L?????????????E?BERLINCLOCK?E??T?O????????????????
```
All 46 are listed in workers/w-gromark/partial_decrypts.tsv. Packing-implied letters were deliberately not filled in.

## 3. Scoring & significance
- **Quadgram:** in every one of the 46 decrypts, no quadgram is fully known and touches a non-crib position. The quadgram score is therefore undefined; there is too little text to score. Under the null (random keys), 0/3000 decrypts had one either.
- **Monogram vs null:** the null is 3000 iid random base-10 key streams that are crib-consistent, applied to K4's real CT. It forces 7.0 letters on average, with monogram mean −1.247 ± 0.136.
  - The 46 primers force a mean of 7.3 letters, so they behave like the null.
  - Their monogram p-values are spread roughly uniformly. The minimum is 0.010 (20173) and the next is 0.012 (16953); with 46 tests that is not significant.
- **Bigram:** adjacent known pairs are rare (0-4 per primer) and none is notable.
- **Survivor counts equal the random expectation:** the iid-key rate × keyspace predicts 40.0 for b10/5 (observed 39) and 400 for b10/6 (observed 412); see the table in §4. Crib-consistency alone therefore carries **no evidence** for Gromark.
- **New per-primer H1 test (the strongest result):**
  - Setup: assume a primer is the true key. Draw random alphabets consistent with that primer's crib system, encrypt random English text (from the corpus, with cribs inserted) and count the non-crib letters the cribs force. 2000 sims per primer.
  - Under H1 the solver forces 11.6-19.5 letters on average, and all of them are correct.
  - K4 gives fewer than the H1 mean for **all 46** primers. P_H1(n ≤ obs) is below 0.05 for 37 of 46 and below 0.01 for 25 of 46.
  - The least-disfavoured primers are 22856 (obs 9 vs 12.8; p=0.14), 00537 (13 vs 17.6; p=0.13), 98800 (p=0.09), 26717/84393 (p=0.09/0.08; these two are the same key up to reversed alphabets, per Bean) and 44157/88254 (p=0.06).
  - Caveat: this assumes the plaintext has a War-and-Peace letter distribution. If the plaintext is light in the crib letters (EASTNORHBLICK), H1 would force fewer letters.

## 4. Other bases / primer lengths — exact crib-consistent survivor counts (arbitrary alphabets)
Each cell shows survivors, with the iid-random-key expectation in parentheses. Primer length L=1 is degenerate (constant key, so monoalphabetic) and is already dead.

| base | L=2 | L=3 | L=4 | L=5 | L=6 |
|---|---|---|---|---|---|
| 2 | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) |
| 3 | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) |
| 4 | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) |
| 5 | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (1) |
| 6 | 0 (0) | 0 (0) | 0 (0) | 0 (1) | 6 (7) |
| 7 | 0 (0) | 0 (0) | 0 (1) | 1 (4) | 33 (27) |
| 8 | 0 (0) | 0 (0) | 4 (1) | 4 (9) | 71 (68) |
| 9 | 0 (0) | 0 (0) | 2 (2) | 23 (19) | 219 (169) |
| 10 | 0 (0) | 0 (0) | 3 (4) | 39 (40) | 412 (400) |
| 11 | 0 (0) | 0 (1) | 0 (7) | 89 (72) | 744 (797) |
| 12 | 0 (0) | 0 (1) | 4 (8) | 52 (101) | 1362 (1217) |
| 13 | 0 (0) | 0 (1) | 0 (10) | 190 (136) | 2078 (1762) |
| 14 | 0 (0) | 0 (1) | 6 (18) | 219 (250) | 3611 (3501) |
| 15 | 0 (0) | 0 (2) | 24 (24) | 386 (363) | 5271 (5439) |
| 16 | 0 (0) | 0 (2) | 51 (29) | 415 (469) | 7964 (7508) |

- Total: 23,283 survivors.
- Bases 2-5: none at any length up to 6. Base 6: the first survivors appear at L=6 (035513, 121013, 155133, 212554, 454112, 511305).
- Small lists:
  - 7/5: 34120
  - 8/4: 3327, 3727, 5161, 5561
  - 9/4: 2787, 4575
  - 12/4: 4520, 4B20, 81A0, 87A0
  - 14/4: 0742, 07AC, 11CD, 338B, BB63, DD21
- All 23,283 were tested against the fixed-alphabet models of §2: plain/cipher/both ∈ {KA, KAr, AZ, AZr} and single alphabet + rotation. **0 survive in any base.**
- I did no decrypt-search beyond that.

## 5. Conclusions for H-301
1. **REFUTED:** Gromark (lagged-Fibonacci with first two digits, bases 2-16, primers 2-6 digits) with a KRYPTOS-keyed, standard, reversed or one-alphabet-rotated (K1/K2-style) plain and/or cipher alphabet. It is also refuted for the 64 keyword alphabets on the 46 b10/b8 primers.
2. **NOT REFUTABLE by cribs, DISFAVOURED:** Gromark with two arbitrary alphabets.
   - Survivor counts are exactly at chance.
   - The forced partial decrypts look like the random-key null.
   - Every primer forces fewer letters than it would if it were the true key (best p≈0.14).
   - Bean's simulated annealing also found nothing convincing.
3. **Not covered:**
   - Other expansion rules (Barker-type or general LFSR taps).
   - Base ≥17, or base 26 ("Vimark").
   - Primers of 7 digits or more.
   - Gromark combined with a transposition.

Sources: Bean, "Cryptodiagnosis of Kryptos K4", HistoCrypt 2021, https://ecp.ep.liu.se/index.php/histocrypt/article/view/153 ; Bean's code https://github.com/RichardBean/k4testing (gt.c, read only, not executed). Corpus: https://www.gutenberg.org/cache/epub/2600/pg2600.txt , https://www.gutenberg.org/cache/epub/1342/pg1342.txt
