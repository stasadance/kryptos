# w-transpo: T7. Width-7/21 anomalies, "scrambled plain text", and whether exclusions survive 1-2 error letters
Worker: w-transpo. Date: 2026-10-26 (UTC). Hypotheses are logged as H-701..H-708.

Scripts are in `workers/w-transpo/scripts/`. Run them from a directory that contains `corpus/pg1661.txt` and `corpus/pg2701.txt` (Project Gutenberg, the same English reference w-stats used).
- `anat.py`: anatomy of the repeats
- `mc.py` and `mc2.py`: Monte Carlo runs over generative models, 20k-40k trials each
- `colcheck.py`: columnar transpositions checked against the cribs
- `robust.py`, `fragdec.py`, `shiftvig.py`, `hillrob.py`, `hill4.py`, `q3err.py`, `wit.py`: tolerance to error letters

Positions are 1-indexed unless marked "0-idx". There was no keyspace search. The only enumerations were the 20,160 width-7 columnar maps, the existing H-205 decimation set rerun with tolerance, and exact solvers.

## (a) What generates the width-21 and width-7 anomalies?

### a1. Anatomy: the two anomalies largely share one feature
- **Doublets:** there are six, at 19 BB, 26 QQ, 33 SS, 43 SS, 47 ZZ and 68 TT. Five of them start at 0-idx 18, 25, 32, 46 and 67, which are all ≡4 (mod 7). The gaps between them are 7, 7, 14 and 21.
- **Stacked doublets:** QQ, ZZ and TT sit at exactly 21-spacing (0-idx 25, 46, 67). In the width-21 grid they stack in columns 4-5 of rows 1, 2 and 3:
  - They make 2 of the 11 width-21 vertical-bigram repeats (QZ twice, ZT twice).
  - They make the vertical trigram QZT occur twice.
  - Under the permutation null, three doublets at i, i+21, i+42 has P = 0.0025.
- **Two vertical trigrams account for 4 of the 11 repeats:** QZT and LWA (0-idx 15→36→57 and 53→74→95).
- **Only 1 of the 11 width-21 repeats is a same-column repeat** (KK in column 10). A period-21 key can only produce same-column repeats, so it explains at most one of them.
- **Three of the five aligned doublets lie inside the cribs:**
  - QQ is plaintext NO (offset 4 in EASTNORTHEAST).
  - SS is plaintext ST (offset 11).
  - TT is plaintext IN (offset 4 in BERLINCLOCK).
  - Both cribs start at 0-idx 21 and 63, which are multiples of 21. The only widths at which both cribs start a row are 3, 7 and 21.
  - So part of the mod-7 alignment simply comes from where the crib words fall. Their plaintext differences (AZ: NO +1, ST +1, IN +5; KA: +12, -2, +4) are not constant. A single period-7 key relation therefore cannot produce all three doublets.
- **Width-21 repeats that touch crib positions:** 7 of the 11 involve at least one crib position (LS, QZ, KK, SN, ZT, AZ, PK).

### a2. Candidate structures and their tests
Monte Carlo runs: English plaintext windows; the statistics are the width-21 repeat count S21 (observed 11), the largest number of doublets in one mod-7 column D7 (observed 5), and IC (observed 0.0361).

| model | mean IC | P(S21≥11) | P(S21≥11 \| IC≤.0385) | P(D7≥5 \| IC≤.0385) |
|---|---|---|---|---|
| perm(K4), the null | .0361 | 3e-4 | 4e-4 | 8e-4 |
| Vig period 7 / 21 | .042 / .040 | .013 / .0045 | (joint with IC ≤5e-5) | .002 / .001 |
| Gromark base 10 / base 8 (arbitrary alphabets) | .040 / .041 | .0037 | 9e-4 / 4e-4 | 4e-4 / 3e-4 |
| Gromark base 2 (Bean's "1 in 10") | .052 | .12 | IC never ≤.036 | 9e-4 |
| Vig7 → width-21 Dir-B transposition (sub then trans) | .042 | .053 | .010 | .0018 |
| width-21 Dir-B → Vig7 (trans then sub) | .041 | – | .0096 | .0010 |
| mono → width-21 or width-7 transposition | .065 | .95 / .55 | IC impossible | .03 |
| running key ± width-21 transposition | .040 | .003 | 3e-4 | 8e-4 |

Dir-B means the text is written into columns in key order and the rows are read out, so its bigrams become vertical bigrams. Dir-A is the textbook columnar transposition.

- **Prediction for transposition models.** A transposition can only turn existing bigram structure into vertical structure. To reach S21 ≈ 11, the pre-transposition text needs English-like bigram repeats, and that comes with English-like IC (about 0.065). K4's IC is 0.036.
  - At K4's IC, the best model is any period-7 component combined with width-21 columnar. It raises P(S21≥11) about 25-fold.
  - It must also hit the low IC, which happens with probability about 0.24. The net Bayes factor against the permutation null is therefore only about 6.
  - **No model** raises the doublet alignment above about 2e-3.
- **Period-7 or period-21 key, no transposition.** Excluded by the cribs: T25→V / L67→V and A32→K / K74→K, with both pairs 42 apart. It also predicts same-column repeats, and only 1 of the 11 is one.
- **Gromark parity.** Bean already notes that base 10 or base 8 with a 5-digit primer has key parity of period 21 (x^5+x+1 = (x^2+x+1)(x^3+x^2+1) over GF(2), orders 3 and 7). The Monte Carlo shows this parity barely moves S21 (mean 4.46 vs 4.06 uniform). So Gromark at base 8/10 does **not** explain the width-21 excess; only base 2 does, and base 2 fails both the IC and the cribs.
- **Columnar transposition (any width) vs the cribs.** Assume the plaintext contains EASTNORTHEAST and BERLINCLOCK contiguously (the scraps show both), and that carved positions 22-34 and 64-74 are their encipherments (NYT 2010; Sanborn 2019). Then any transposition stage must map each crib onto those exact positions in order. A columnar transposition sends consecutive letters to positions one column-length apart, so it cannot do this for any width from 2 to 96, either direction, any column order. Enumeration at width 7 (5040 orders × Dir-A/Dir-B × inverse, for 97 letters and for a 98-cell 7×14 grid with one null) agrees:
  - at most 2 of the 24 crib positions are fixed;
  - 0 configurations keep the cribs contiguous.
- **The crib-compatible transpositions at width 7 or 21 are only these:**
  - width 21: permuting columns 13-20 within rows (8! orders). This leaves vertical bigrams **invariant**, so it cannot create the anomaly.
  - width 21: swapping rows 0 and 2.
  - width 7: permuting the 9 full rows that contain no crib (9!). This leaves the doublet columns **invariant**, so it cannot create the anomaly.
  - widths 19-21, 37-63 and 74-96: any shuffle of row-blocks or strips that keeps each crib whole (H-704).
- **Conclusion for (a).** No tested classical structure reproduces both anomalies at K4's IC.
  - The width-21 excess is mildly favoured (Bayes factor about 6) by "period-7 component plus width-21 columnar", but that family cannot be reconciled with the cribs.
  - The doublet alignment is unexplained by every model (all ≤2e-3) and is partly inherited from the crib positions.
  - Most parsimonious reading: chance amplified by post-hoc choice of statistic and width (w-stats' family-wise 0.005 corrects for width but not for the choice of statistic), or a non-textbook hand process (H-206).
  - They are not evidence for a transposition stage.

## (b) "Scrambled plain text": does it imply a transposition stage?
**Quotes:**
- Sanborn, Nov 2025 news conference, via AFP: Kobek and Byrne "found and photographed five pieces of scrambled texts that I had accidentally placed in the archive boxes"; "The scrambled plain text was found, but without the coding method or the key. This is a very important distinction." Sources: https://www.enca.com/lifestyle/auction-famed-cia-cipher-shaken-after-archive-reveals-code and https://citizen.digital/article/auction-of-famed-cia-cipher-shaken-after-archive-reveals-code-n373254
- RR Auction: the find was "five pages of scrambled text", copies of 1990 documents in which Sanborn "cut sentences into strips and taped them together out of order"; "From these scrambled fragments" the pair "pieced together" the plaintext. Source: https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/ (auction-house marketing, secondary).
- FFXnow, Nov 2025: the "original scrambled texts", "which Sanborn said he showed to the CIA's Department of Historical Intelligence to ensure the agency understood" that the content was not untoward. Sanborn: "They don't have the method with which it's deciphered." Source: https://www.ffxnow.com/2025/11/12/solution-to-kryptos-sculpture-at-cias-mclean-hq-up-for-auction/
- SciAm, 16 Oct 2025: "taped-together scraps that revealed K4's original plaintext", containing "BERLIN CLOCK" and "EAST NORTHEAST". Source: https://www.scientificamerican.com/article/a-solution-to-the-cias-kryptos-code-is-found-after-35-years/
- NYT, 20 Nov 2010 (Schwartz, NBC mirror): "The characters that are the 64th through 69th ... read NYPVTT. When deciphered, they read BERLIN." Also: "the other 91 characters and their proper order are yet to be determined." Sanborn's check of solvers: "What do you have in letter-position 27?" Source: https://www.nbcnews.com/id/wbna40294019
- Elonka's 2019 lunch notes: "BERLIN is plaintext that starts at exactly the 64th character". Sanborn also "confirmed that the letters directly map from the cipher text to the plain text". Source: https://rumkin.com/reference/kryptos/k4/

**Assessment:**
1. "Scrambled" describes physical vetting copies: sentence strips taped out of order for a 1990 CIA review. It is not a cipher stage. The reshuffling unit is sentences, and the crib words survive intact on the strips. **It does not imply transposition** (H-705, SUPPORTED).
2. "Their proper order" in the NYT piece is the journalist's phrasing, not a Sanborn quote. It is weak at best.
3. Sanborn's statements (BERLIN "exactly" at 64, NYPVTT→BERLIN, "letter-position 27" as his check, "directly map") all assume plaintext position equals ciphertext position.
4. **Reconciling with Bean 2021.** Bean's minor-difference statistics (1/5,520 for {KRYPTOS}-letter plaintext near its ciphertext; 1/240 and 1/310 for ciphertext letters of repeated plaintext letters being close) argue that ciphertext letters at crib positions *are* the encipherments of those plaintext letters. That rules out transposition **after** substitution (a final transposition would scatter them). It says nothing about a transposition **before** a position-keyed substitution. Such a pre-transposition must still fix the crib positions, because of Sanborn's "BERLIN starts at 64 in the plaintext". So the only transpositions left are ones that move whole word-blocks around and keep the cribs in place (H-704). Those are invisible to every statistic and are unmotivated except by the coincidence that both cribs start a width-21 row.
5. **Net:** every source is consistent with no transposition stage. There is no evidence for one, and the anomalies in (a) do not require one.

## (c) Robustness of exclusions to 1-2 deliberate error letters
Error model: an error is a wrong ciphertext letter (carved or enciphered wrong) at one position, as with K2's R/E. The K1 key-letter slip also acted on one position. "Min deletions" is the smallest number of crib positions that must be dropped to make the family consistent, so it is a lower bound on how many errors are needed. An omitted or inserted letter between the cribs (like K2's missing S) shifts BERLINCLOCK by d = ±1 or ±2 relative to EASTNORTHEAST.

| exclusion (ruled_out.md) | errors needed to revive | verdict |
|---|---|---|
| Monoalphabetic, no transposition | 11 | ROBUST |
| Pure transposition: "3 E needed, 2 present" argument | 1 (one E mis-carved) | FRAGILE. The IC/chi² argument stays robust, so the exclusion holds. |
| Fixed-point-free ciphers (S→S @33, K→K @74) | 2 (both 33 and 74) | survives 1 error, fragile to 2 |
| GEN periodic, arbitrary alphabets: p = 10, 25, 50 | **1**: E22→F / O72→F is the only conflict | FRAGILE (an error at 22 or 72 revives these periods) |
| GEN: p = 4, 6, 14, 15, 17, 21, 34, 42, 43, 45 | 2. For p = 6, 14, 21, 42 the witnesses are T25→V/L67→V and A32→K/K74→K | FRAGILE to 2 errors |
| GEN: p = 5, 7 | 3 | robust to 2 |
| GEN: p = 1, 2, 3, 9 | ≥6 | ROBUST |
| GEN with an omitted or inserted letter between cribs (d = ±1, ±2) | 0 for p ∈ {6, 10, 14, 15, 17, 21, 25, 34, 42, 43, 45, 50} (each at some d) | FRAGILE. One omission revives most GEN-killed periods ≥6. |
| Quagmire III (one mixed alphabet), p = 7, 10 | unsat with ≤2 errors (z3), Vig- and Beau-style | ROBUST |
| Quagmire III, p = 21 | Beau unsat ≤2; Vig unsat ≤1, ≤2 = z3 UNKNOWN (timed out at both 120 s and 900 s; unresolved) | robust to 1 |
| Quagmire III, p = 25 | Beau SAT with 1 error (drop 22); Vig SAT with 2 | FRAGILE (but at p ≥13 most residue classes are single letters, so SAT means only "not refuted") |
| Periodic Vig/Beau/vBeau, AZ or KA, p ≤ 25 | ≥3, and an omission at d = ±1, ±2 revives only crib-vacuous periods | ROBUST |
| Same family, p = 26, 30, 52 (1 error) and 31, 32, 51 (2 errors) | revived algebraically, but every repaired key decrypts to gibberish (monogram score −0.26 to −1.1 vs English +0.36±0.07) | robust via decryption |
| K3-decimation + tableau (H-205) | 0 of 1.35M configurations within ≤2 deletions | ROBUST |
| CT-autokey, L = 1..68 | ≥5 mismatches (each error repairs at most 2) | ROBUST |
| CT-autokey, L = 69-73 | 1-4 mismatches among ≤5 checks (e.g. Beau/AZ L = 69: 2 of 5) | FRAGILE |
| PT-autokey direct crib checks, L = 11, 12, 30, 31, 51, 52 | 1-2 | FRAGILE (w-crib's chain-propagation English test still applies) |
| Hill n=2 / n=3, linear and affine | ≥12 / ≥5 | ROBUST |
| Hill n=4 linear, C=KP | **1** (AZ, offset 3); 2 (KA, offset 0) | FRAGILE. P=KC solutions are all singular, so invalid. |
| Gronsfeld/digit keys needing >9 | 11-16 of 24 positions | ROBUST |
| Bean/w-crib: "standard plain alphabet impossible for Gromark" (R28/C73→P, k72−k28≡15) | 1 (a single pair) | FRAGILE |
| Statistical exclusions (IC, chi², column IC) | 1-2 letters change IC by <0.001 | ROBUST |

**Takeaway.** With 1-2 errors allowed:
- The exclusions of mono, Vig/Beau over standard and KA tableaux (all reachable periods), Quagmire III at 7 and 10, K3-decimation, Hill n ≤ 3 and digit keys stand.
- The arbitrary-alphabet periodic exclusions (GEN, and the Quagmire I/II/IV periods w-crib listed, which inherit this) are **fragile**, especially p = 10/25/50 (1 error) and almost everything ≥6 under one omission.
- A period-21/42 component, the structure the anomalies hint at, is blocked by only two crib pairs, both 42 apart (25/67 and 32/74) (H-706).

## Hypotheses (logged in hypotheses/log.md)
- H-701 The anomalies are one feature: mod-7 doublets with 21-stacking. OPEN (descriptive).
- H-702 Substitution then columnar transposition (w = 7 or 21). REFUTED.
- H-703 Columnar transposition then periodic substitution. REFUTED, given Sanborn's crib positions.
- H-704 A block/strip transposition that preserves the cribs, before a position-keyed substitution. OPEN, low prior, statistically untestable.
- H-705 "Scrambled plain text" means 1990 vetting strips, not a cipher stage. SUPPORTED.
- H-706 Period-21/42 key component plus 2 error letters. OPEN, low prior.
- H-707 GEN p = 10/25/50 revived by one error at 22 or 72. OPEN. Quagmire III at p = 10 is still dead.
- H-708 One omitted or inserted letter between the cribs, as in K2. OPEN. It revives most GEN periods; standard tableaux stay dead.

## Next tests suggested
- Q1/Q2/Q4 (w-crib's solver) at p = 10, 21 and 42 with ≤2 deletions or with d = ±1.
- Gromark survivors (T6) rerun with one deletion: w-gromark should check whether the primer count rises sharply.
- Ask w-physical/w-antipodes whether the Antipodes K4 copy differs at 22, 25, 32, 67, 72 or 74. These are the positions whose single error would revive families.
