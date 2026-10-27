# w-crib T3 — Algebraic analysis of the 24 K4 cribs   (w-crib, 2026-10-26 UTC)

Inputs: facts/ciphertext.txt, facts/cribs.md (EASTNORTHEAST @22-34, BERLINCLOCK @64-74, 1-indexed).
Tool: tools/keystream_check.py (pure Python; reproduces §0, §1, §3 and the GEN list of §2).
Other checks (z3 Quagmire model, Q4 DFS, Hill GF(2)/GF(13) solver, Gromark union-find) were scratch scripts;
each is specified below precisely enough to rebuild.
Published comparison: R. Bean, "Cryptodiagnosis of Kryptos K4", HistoCrypt 2021,
https://ecp.ep.liu.se/index.php/histocrypt/article/view/153 (code https://github.com/RichardBean/k4testing).
Everything Bean states about crib constraints that I re-derived agrees (k28=k66, Playfair, Gromark counts).

## 0. Raw crib facts
- Self-encryptions (P==C): pos 33 S->S, pos 74 K->K (kills fixed-point-free ciphers: Playfair, Enigma-like).
- Monoalphabetic impossible: E->F(22)/E->G(31); T->V(25)/T->R(29); A->L(23)/A->K(32); S->R(24)/S->S(33);
  and two PT letters -> one CT letter: N->Q(26)/O->Q(27); T->V(25)/L->V(67).
- CT uses all 26 letters; CT doublets in both digraph alignments (BB,SS,SS,ZZ | QQ,TT).
- R->P at both 28 and 66: every additive scheme has k28 == k66 (Bean's k27=k65, 0-indexed). Vig/AZ key = Y at both.

## 1. Periodic Vigenere / Beaufort / variant Beaufort, AZ and KRYPTOS (KA) alphabets
| rule | alph | key @22-34 (ENE) | key @64-74 (BC) |
|---|---|---|---|
| Vig  C=P+K  | AZ | BLZCDCYYGCKAZ | MUYKLGKORNA |
| Beau C=K-P  | AZ | JLJODEGKUKKKL | OCGGBGOKTRU |
| vBeau C=P-K | AZ | ZPBYXYCCUYQAB | OGCQPUQMJNA |
| Vig   | KA | RDUMRIYWOYNKY | ELYOIECBAQK |
| Beau  | KA | WXAKGZTOAXAFD | RGTGNWRJLFK |
| vBeau | KA | ZJOBZEXPUXAKX | ICXUEILMNSK |
KA = KRYPTOSABCDEFGHIJLMNQUVWXZ (K1/K2 tableau, Vig/KA = Quagmire III/KRYPTOS).

Exact period test p=1..97 (crib positions i==j mod p must carry equal key):
- Crib-internal distances 1..12, cross distances 30..52 ⇒ periods 27,28,29 and 53..97 have NO collision
  (vacuous, 48 periods). All other periods (1-26, 30-52) conflict for all 6 rule/alphabet combos.
- NEW: vacuous p=27/28/29 are still testable: 24 of p key letters are known, so 81-89% of K4 decrypts. All 18
  decrypts are gibberish, e.g. Vig/AZ p=27 `QDEPKOY??VANRHIBUOOB?EASTNORTHEAST??KZSIYKIENXZ?VPUHHJWFCYMIO??...`.
  Eliminated (w-history listed these as untestable).
- p=53..97: the 0-24 extra letters each period exposes show no English (best 24-letter fragment monogram
  log-score -0.01; English ≈ +0.37, uniform ≈ -0.61). p ≳ 75 exposes <5 letters ⇒ indistinguishable from a
  running key/OTP; not testable by cribs.
⇒ Periodic Vig/Beau/vBeau over AZ or KA: dead for every period 1..97 that the cribs can reach.

## 2. General periodic substitution and Quagmire I-IV with ARBITRARY alphabets
GEN = independent arbitrary alphabet per residue class (constraint: within a class, P<->C bijective).
Fails exactly for p ∈ {1-7,9,10,14,15,17,21,25,34,42,43,45,50} (agrees with w-stats §6). Witnesses:
p=1 N->Q(26)/O->Q(27); p=2,4 T->V(25)/T->R(29); p=3,9 E->F(22)/E->G(31); p=5 S->R(24)/T->R(29);
p=6,7,14,21,42 T->V(25)/L->V(67); p=10,25,50 E->F(22)/O->F(72); p=15,45 O->Q(27)/O->F(72);
p=17,34 H->N(30)/B->N(64); p=43 E->F(22)/E->Y(65).

Quagmire model: posC(c) = posP(p) + s_r (Vig-style) or s_r − posP(p) (Beau-style), r = i mod p; posP,posC
arbitrary permutations (strict superset of keyword-mixed alphabets). Q1: posC = straight; Q2: posP = straight;
Q3: posP = posC (one alphabet, K1/K2 structure); Q4: independent. Exact: z3 (Q1-Q3; integer encoding
C−P−s = 26k), and for Q4 a DFS over class shifts + weighted union-find + component packing (the p=8 Q4
solution was re-verified by re-encrypting all 24 cribs). Tested every GEN-consistent non-vacuous period
{8,11,12,13,16,18,19,20,22,23,24,26,30,31,32,33,35-41,44,46,47,48,49,51,52}.
| model | crib-consistent periods (non-vacuous) |
|---|---|
| Q1 (Vig = Beau-style, provably equivalent) | 13,16,19,23,24,26,30,31,32,33,35,38,39,41,46,47,48,49,51,52 |
| Q2 (Vig = Beau-style, equivalent) | 16,19,20,23,24,26,30,31,32,33,37,38,39,40,46,47,48,49,51,52 |
| Q3 Vig-style | **30, 41 only** |
| Q3 Beau-style | 23,26,30,31,32,33,46,47,49,51,52 |
| Q4 (Vig = Beau-style) | all GEN periods EXCEPT 11,18,22,36,44 (p=12 undecided: DFS not completed; rerun if needed) |
Caveats: for p ≥ 13 most residue classes hold a single crib letter, so "consistent" means "cannot be refuted",
not "supported". Example: Q3 p=41 has a valid alphabet (YVSATUONFPZQRBCWEJGXHDMLKI) but it determines
only crib positions; Q3 p=30 has only one class with 2 crib letters. Q4 at p=8 (ABSCISSA length) IS
crib-consistent with arbitrary alphabets (example PT alph TPXJYEOIFNMGZWUVDHBKACRQLS,
CT alph LSVBZCFYTXQGIDEHOUNJKWMPAR, shifts r0..r7 = 2,1,4,1,25,1,6,0) — but w-stats §4 disfavours p=8 by IC.
Keyword periods: KRYPTOS(7), PALIMPSEST(10) dead under ANY tableau (GEN); ABSCISSA(8) dead for Q1/Q2/Q3
with any alphabets, alive only as Q4.

## 3. Autokey (Vig/Beau/vBeau × AZ/KA)
- CT-autokey K_i = C_{i−L}: checkable at every crib position with i−L ≥ 1. All L = 1..73 conflict in all 6
  combos; L ≥ 74 puts every crib position in the primer (= running key). DEAD.
- PT-autokey K_i = P_{i−L}: direct crib-crib checks kill every L that has one. Remaining L (27-29, 53-96) were
  tested by propagating each crib letter along its chain (P_{i+L} = dec(C_{i+L}, P_i); P_{i−L} = K_i):
  282 combos have no internal conflict but none gives English (best ≥20-letter fragment −0.04 vs +0.37), e.g.
  Vig/AZ L=28 `YGCKAZ.HCVGHDGEBRK...EASTNORTHEAST.MUYKLGKORNA...`. DEAD except primers the cribs cannot reach.

## 4. Hill / affine
- Affine mono (c = ap+b): special case of mono ⇒ dead (§0).
- Hill n×n, C = K·P (+b), AZ and KA numbering, every block alignment, using only blocks wholly inside a crib;
  per-row linear consistency solved over GF(2) and GF(13) (CRT ⇒ Z26; covers non-invertible K too).
  n=2, n=3 (linear and affine) and n=4 linear: INCONSISTENT at every offset, both numberings.
  n=4 affine: only offsets with 4 blocks vs 5 unknowns remain (vacuous: AZ off 0,3; KA off 3). n ≥ 5 untestable.
  Independently reproduces H-504 (w-physical) and extends it to affine Hill.

## 5. Transposition ± substitution
- Pure transposition: dead (cribs need 3 E, CT has 2 E). After removing crib letters, the other 73 PT letters
  would contain 0 E, 7 K, 6 U, 5 W.
- Transposition + mono (either order): cribs alone can't refute; IC/chi² do (w-stats).
- Transposition + polyalphabetic: crib positions move, so the positional tests above don't apply. Bean 2021's
  Monte Carlo "minor differences" tests (P/C letter distances small, ~1/5,520 and ~1/240) argue the cribs are
  enciphered in place (no transposition after substitution). Cited, not re-derived.

## 6. Structure in key fragments
- k28 == k66 forced (R->P twice, distance 38); Vig/AZ has Y at 28,29,66 and K at 32,67,70 — repeat counts are
  ordinary for 24 draws from 26 letters.
- Vig/KA BC key ELYOIECBAQK contains CBA (70-72) = three consecutive KA letters descending; Beau/AZ ENE key
  has KKK at 31-33. Neither continues into a progression (checked first differences); no 3-gram of KRYPTOS,
  PALIMPSEST, ABSCISSA, IQLUSION, LAYERTWO, DESPARATLY, SHADOW etc. appears except chance ORN/LOC.
- Running key = English text through a standard tableau: 24-letter key monogram scores Vig/AZ −0.64,
  Beau/AZ −0.59, vBeau/AZ −1.11, Vig/KA −0.19, Beau/KA −0.61, vBeau/KA −1.01 (English ≈ +0.37 ± ~0.2,
  uniform −0.61). Plain-English running key through these 6 tableaux is disfavoured (Vig/KA least so, ~2.8 sd).
  Statistical, not a proof.

## 7. Gromark — Bean's candidate, independently reproduced
Key k_{i+n} = (k_i + k_{i+1}) mod base; posC(c) = posP(p) + k_i, alphabets arbitrary. With k known this is a
pure difference system (weighted union-find + same-alphabet collision check; final packing not applied, so
survivors are necessary-condition survivors).
- Standard plain alphabet dead (R->P @28, C->P @72 need k72 − k28 ≡ 15 mod 26 with digits 0-9).
- Arbitrary alphabets: base 10 / primer 5: exactly 39 primers survive (incl. 26717, 84393, 98800) — **matches
  Bean's 39**. Base 10/4: 3301, 6740, 9903 (Bean: same). Base 8/5: 00351, 00537, 40311, 40577 (Bean: "four,
  incl. 00351, 00537"). Base 10/3 and base 2/5: none.

## Summary
| Family | Status | Evidence |
|---|---|---|
| Mono / affine / Caesar | DEAD | §0 |
| Playfair & 5×5 digraphic | DEAD | self-enc S,K; 26 letters; CT doublets in both alignments |
| Periodic Vig/Beau/vBeau, AZ or KA | DEAD for all p ≤ ~75 (incl. 27-29 by decryption) | §1 |
| Any periodic polyalphabetic, p ∈ {1-7,9,10,14,15,17,21,25,34,42,43,45,50} | DEAD | §2 |
| Quagmire III, any single mixed alphabet | Vig-style only p=30,41; Beau-style 23,26,30-33,46,47,49,51,52 | §2 |
| Quagmire I/II/IV, arbitrary alphabets | many p survive, weakly constrained | §2 |
| CT-/PT-autokey (6 tableaux) | DEAD | §3 |
| Hill n=2,3 (lin+affine), n=4 linear | DEAD | §4 |
| Pure transposition | DEAD | §5 |
| Gromark (arb. alphabets) b10/5, b10/4, b8/5 | ALIVE (39 / 3 / 4 primers) | §7 = Bean |
| Running key / OTP / non-periodic generators; transposition+poly | NOT testable by crib algebra alone | |
