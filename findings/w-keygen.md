# w-keygen T14: keyword-driven, plaintext-independent key generators vs the K4 cribs
Worker: w-keygen, 2026-10-26 (UTC). Hypotheses: H-1401..H-1406.
Library: `tools/keygen.py` (generators, exact crib solver, motivated keyword list, `selftest`).
Drivers and raw outputs: `workers/w-keygen/scripts/` (drive.py, rel.py, rates2.py, linstep.py, twoalph.py, forced.py, plant.py, evalplants.py, *.out, k4_hits.jsonl.gz).
Positions are 1-indexed. Key stream index t = i-1+offset.

## TL;DR
- **No crib-passing candidate.** 900,272 motivated generator configs were screened. Each was tested against:
  - 12 concrete tableaux (Vig/Beau/vBeau with PA, CA ∈ {AZ, KA});
  - one arbitrary alphabet, Vigenère form (vig1, the K1/K2 structure) and Beaufort form (beau1);
  - two arbitrary alphabets (two, which covers Quagmire I-IV and any relabel + additive mask).
- Results:
  - **0 survivors** under the fixed tableaux, vig1 and beau1.
  - **258 survivors** under two arbitrary alphabets. That is at or below chance (iid rate ≈ 5.8e-4/config predicts ≈ 520).
  - None of the 258 passes with any pair from 62 keyword-mixed or standard alphabets (2,975,256 pair tests).
  - The 258 force only 0-9 non-crib letters (mean 3.5), so the cribs cannot test them further.
- **Pipeline validated.** Every family was planted on English in all 4 cipher models (28 plants). The screen recovered the planted config 28/28, and the fixed-tableau decrypt equals the planted plaintext 7/7.
- **Crib conditions re-derived symbolically** (rel.py). The w-mask statements are correct, and Beaufort-single is new:

| model | relations |
|---|---|
| two arbitrary alphabets | k28=k66; k24+k34=k29+k33 |
| one alphabet, Vigenère | k33=0, k74=0, k28=k66, k24+k34=k29 |
| one alphabet, Beaufort (new) | k28=k66, k24+k34=k29+k33, **k33 and k74 even** |

- **New quantitative point.** The single-alphabet models are far more selective than the 4 relations alone suggest. The 21 crib letters form essentially one component that must embed injectively in Z26:
  - P(feasible | relations) = 5e-6 for vig1 (5 of 1e6 MC; analytic ≈ 26!/(5!·26^21) ≈ 6.5e-6);
  - 0 of 1e6 for beau1.
  - So a random key passes vig1 with probability ≈ 1e-11. **Any plaintext-independent generator under a single (K1/K2-style) mixed alphabet is a sharp test.** The two-alphabet model is weak (≈ 6e-4 per key).

## 1. Catalogue of hand-operable, plaintext-independent generators (pre-1990)
| # | family | source repertoire | form tested | status |
|---|---|---|---|---|
| F0 | periodic keyword (Vigenère/Quagmire) | Kahn; ACA | w[(t+o) mod L] | already dead by GEN periods (w-stats, w-crib). Here also 0/1072 with arbitrary 1-alphabet; latin filter 0/268 letter streams |
| F1 | progressive key (keyword shifted +s each cycle), and keyword + position counter | ACA "Progressive Key"; Friedman MilCrypt II | w[t+o] + s·floor((t+o)/m), m ∈ 1..26 ∪ {L, 2L}, s=1..25 | 0 fixed/vig1/beau1; 192 two-alph (chance) |
| F2 | two keywords combined (compound key, period lcm) | Kahn (double Vigenère); Gaines | w1[t+o1] ± w2[t+o2], all offsets | 0 fixed/vig1/beau1; 53 two-alph |
| F3 | chain addition / lagged Fibonacci on keyword (letter Gromark, "Vimark"); running-sum key; Gromark proper on keyed-columnar digits mod 10 | ACA Gromark; Friedman (chain addition) | rules x[n+L]=x[n]+x[n+1], x[n]+x[n+L-1], x[n]-x[n+1], cumulative; o=0..2L | 0 fixed/vig1/beau1; 1 two-alph (mod 26), 0 (mod 10) |
| F4 | interrupted key (keyword restarts per segment) | Friedman; ACA | segment lengths 1,2,3,…; L,L+1,…; L-1…1; columnar order or AZ values of a 2nd keyword | 0 everywhere. Latin-filter pass 52/7076 = 0.7%, below the 1.8% null |
| F5 | keyed-columnar-derived streams (position numbers through a keyed columnar; column digits) | K3 method; Nihilist-style keyed digits | π(t), π⁻¹(t) mod 26, column digit; all offsets | 0 fixed/vig1/beau1; 12 two-alph |
| F6 | tableau traversal / clock-hand: c + a·t + b·floor((t+o)/m) | Kryptos tableau read row-wise (a=b=1, m=26), diagonals (a=2), 30/31-wide sculpture rows | **exhaustive** m=2..40, all o, a, b, c | **0 in every model incl. two-alph** (§2.3) |
| F7 | Porta / any reciprocal half-alphabet tableau, any key | Porta; ACA | — | **dead analytically**: no fixed points, contradicts S→S@33, K→K@74 |
| F8 | Nihilist additive digits (Polybius coordinates of a periodic keyword) | Nihilist | — | periodic in the keyword ⇒ subsumed by GEN periodic results (dead for L ∈ {1-7,9,10,…}) |

Slide ciphers (Saint-Cyr) and Quagmire-style alphabet sliding are Vig/Beau with mixed alphabets, so the additive models cover them. Running-sum keys equal F1 applied to prefix sums. Any generator whose output is periodic inherits the periodic exclusions.

## 2. Analytic conditions (exact)
### 2.1 Relations
rel.py runs union-find with symbolic offsets over the 24 crib (P,C) edges. It reproduces w-mask's two-alphabet and vig1 relations and gives the beau1 relations above. With P = feasibility probability:
- **two:** the 2 relations hold with probability 1/676 for iid keys, then P(injective packing) ≈ 0.30, for an overall 4.4-5.8e-4.
- **vig1:** 26^-4 × 5e-6.
- **beau1:** (1/4)(1/676) × <1e-6.

### 2.2 Per-family closed forms
F1 (progressive), with u_i = i-1+o and F_i = floor(u_i/m):
- two: w[u28] − w[u66] + s(F28 − F66) ≡ 0 and w[u24] + w[u34] − w[u29] − w[u33] + s(F24 + F34 − F29 − F33) ≡ 0.
- vig1 adds w[u33] + sF33 ≡ 0 and w[u74] + sF74 ≡ 0.
- These are linear congruences in the single free parameter s. Each (kw, o, m) therefore has gcd-many solutions or none, and the code checks all 26 values, which is the same thing.
- Periodic keywords (s=0) under any Latin tableau need w[(27+o) mod L] = w[(65+o) mod L]: equal keyword letters at cyclic distance 38 mod L. KRYPTOS (38≡3 mod 7, no repeated letters) fails at every offset.

F6 (linear + stepped):
- The relations read 38a + bΔ1 ≡ 0 and −4a + bΔ2 ≡ 0, with Δ1 = F66 − F28 and Δ2 = F24 + F34 − F29 − F33.
- For m ≥ 19, Δ2 = 0, which forces a ∈ {0,13} and then b ∈ {0,13} (period ≤ 2, dead).
- Non-trivial (a,b) solutions exist only for m = 10-18 (528 in total). **All 528 fail injectivity** (linstep.py).
- So every row-wise, column-wise or diagonal walk of a 26/30/31-wide tableau, and every clock-hand key, is dead under ANY alphabets. This extends w-physical H-502 and w-clock H-803, which covered fixed alphabets only.

### 2.3 Degrees-of-freedom caution
A family with ≥ 2 free additive parameters, e.g. the full k = W + a·t + b·floor(t/m), can satisfy the two-alphabet relations for almost any W. **Under two arbitrary alphabets such families are not testable by the cribs.** F1-F5 above have at most 1 free numeric parameter, so the two-alphabet screen still filters them (2 equations).

## 3. Seeds and bounded budget
- **Keywords (29), with rationale in tools/keygen.py KEYWORDS:**
  - KRYPTOS; PALIMPSEST/PALIMPCEST (coding-chart misspelling); ABSCISSA; IQLUSION/ILLUSION; LAYERTWO;
  - BERLIN, CLOCK, BERLINCLOCK, NORTHEAST, EASTNORTHEAST;
  - SHADOW, LUCID, MEMORY, SANBORN, SCHEIDT, LANGLEY, CIA, TUTANKHAMUN, CARTER;
  - the Morse phrases VIRTUALLYINVISIBLE, SHADOWFORCES, LUCIDMEMORY, TISYOURPOSITION, DIGETALINTERPRETATIU, SOS, RQ;
  - and the KA alphabet itself (tableau traversal).
- **Numberings:** AZ or KA, each from 0 or from 1.
- **Config counts:**

| family | configs |
|---|---|
| F0 | 1,072 |
| F1 | 704,700 |
| F2 | 167,970 (AZ0/KA0, all offsets) |
| F3 | 13,560 |
| F4 | 7,076 |
| F5 | 5,894 |
| **total** | **900,272** (< 1e6) |
| F6 (separately exhaustive) | 554,320 (a,b,m,o) × 26 c |

- **Justification for the budget:** the expected chance survivor count is ≈ 1e-5 under vig1 and ≈ 0 under fixed tableaux. Any pass there would be significant, and only the two-alphabet model is noisy.

## 4. Results on K4
- workers/w-keygen/scripts/k4_screen.out: fixed 0, vig1 0, beau1 0, two 258 (F1 192, F2 53, F5 12, F3 1). Latin filter: F0 0, F4 52.
- **Two-alphabet survivors.**
  - 2,975,256 tests over PA, CA ∈ {AZ, KA, 29 keyword-mixed alphabets, plus the reverse of each} × {vig, beau, vbeau} gave **0 crib passes** (twoalph.out).
  - Survivors at the natural offset 0: CLOCK progressive (m=3, s=14), EASTNORTHEAST progressive (m=3, s=4), and KA-alphabet Gromark mod 26 at o=43.
  - These force 1-3 non-crib letters (forced.out), so they are untestable and carry no evidence.
- **Not done:** SA over two free alphabets for the two-alphabet survivors. This is ill-posed at 97 letters (~50 free alphabet cells), and the survivor count is at chance.

## 5. Validation (plants_eval.out)
- English windows (PG #1342) were planted with the cribs and encrypted with a random config of each family. The 4 models were fixed KA-Vig, random vig1, random beau1, and random two-alphabet (Vig or Beau).
- **Recovery 28/28.** For fixed tableaux the decrypt equals the planted plaintext 7/7.
- False-positive counts on planted texts vary with each text's crib-graph structure, because relations() is K4-specific and the planted runs used the exact solver only. Single-alphabet false positives were 0-7 per run, coming from equivalent streams.

## 6. Hypotheses
- H-1401 Porta/reciprocal: REFUTED (fixed points).
- H-1402 F6 traversal/clock-hand, any alphabets: REFUTED (exact).
- H-1403 F0-F5 seeded by motivated keywords under fixed or single-mixed alphabets: REFUTED (0/900k, test power validated).
- H-1404 the same under two arbitrary alphabets: OPEN, untestable (chance survivors, ≤ 9 forced letters).
- H-1405 beau1 relations: FACT (k33, k74 even).
- H-1406 a single-alphabet generator test is ~1e-11 selective: SUPPORTED (MC).

## 7. Caveats
- Only the listed generator rules and keywords were tested. Transposition before or after the key was not tested; cribs are assumed in place (w-transpo).
- No error tolerance. A single carving error at 24, 28, 29, 33, 34, 66 or 74 would change the relations.
- Two-alphabet results are consistency only.
