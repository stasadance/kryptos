# w-anneal T19 — crib-constrained simulated annealing for Quagmire IV / two-arbitrary-alphabet periodic ciphers
Worker: w-anneal, round 6, 2026-10-26/27 (UTC). Hypotheses H-1901..H-1904.
Code: `workers/w-anneal/scripts/` (sa.c = annealer, modes documented below; lib.py; driver.py = resumable calibration driver; analyze.py / build.py).
Raw results (one JSON line per instance, incl. ciphertext, best decrypt, all restart scores): `workers/w-anneal/results_q4.jsonl` (1,027 lines), `results_gen.jsonl` (52).

## TL;DR
- **No candidate.** No period gives a K4 score that beats the null after family-wise correction, and no K4 decrypt reads as English.
- **Calibration says the method cannot test K4 at any surviving period.** 0 of 294 synthetic 97-letter Quagmire IV controls were recovered (best median accuracy 0.18, at p=16).
  - **p = 16-28: search-limited.** The annealer's best stays 7-34 log10 units below the true plaintext's score. Separation between controls and nulls is weak: power 0-3/12 at the null's 99th percentile.
  - **p ≥ 30: information-limited.** The annealer finds wrong decrypts that score *higher* than the true English in most controls: 7/12 at p=30, 10/12 at p=32, and all controls at every period from p=37 on except p=39 (5/6). Random nulls reach the same scores, so even a perfect search could not identify the plaintext with this objective.
- **K4:** 33 periods. Smallest local p is 0.003 at p=29 (Bonferroni over 33 periods: 0.10). A follow-up with 12 independent K4 reruns against 124 nulls shows it was restart luck: median K4 run z = +0.15, P(K4 run > null run) = 0.60. Its decrypt is word salad.
- **General periodic (independent alphabet per class), p ≥ 16:** fully untestable. Annealed random nulls score −3.4 per quadgram, far *above* real English (−4.3), with the 24 cribs hard-enforced.
- **Verdict:** H-1901/H-1902 untestable, not refuted. Quagmire IV and general periodic ciphers at the surviving periods stay open. Statistical cryptanalysis of 97 letters cannot close them. The team should not trust any SA "solution" of K4 under a two-alphabet periodic model, ours or anyone else's, unless it is checked against a null like the one here.

## Method
**Model (Quagmire IV = periodic with two arbitrary alphabets, ACA sense).** posP, posC: arbitrary permutations of Z26; per-class shift s_r, r = i mod p. Encrypt C_i = posC^-1(posP(P_i) + s_r); decrypt P_i = posP^-1(posC(C_i) − s_r). Vig- and Beau-style are equivalent (negate one alphabet), so one model covers both. Keyword alphabets are a subset.

**Objective.** Sum of English quadgram log10-probabilities over the 94 quadgrams of the 97-letter decrypt (dense 26^4 table; corpus PG #2600, #1342, #98, #2701, #345 = 5.25M letters; unseen quadgram = log10(0.01/N)). For comparison: mean per quadgram = total/94 (English control texts here: −4.1 to −4.4).

**Crib-exact parametrisation (sa.c mode 10).** Free state = posP (full permutation), one free shift per connected component of the "shift graph", the shifts of all classes without a crib, and the positions of the 12 cipher letters that do not occur in the cribs. Everything else is derived so that the cribs hold by construction: for each crib cipher letter C with representative crib (i, P_i): posC(C) = posP(P_i) + s_{i mod p}; two cribs sharing a cipher letter in different classes fix the shift difference (tree edges); collisions are repaired by swapping. Residual violations (crib-letter collisions, the rare cycle constraints at p = 19, 35, 38, 41) carry a penalty of 10 log10 units per wrong crib letter; every reported solution has 0 violations unless stated.
Moves: posP transposition (75%), transposition of two non-crib cipher letters (20%), heat-bath over all 26 values of one free shift (5%). Metropolis acceptance, geometric temperature 30 → 1 over 2,000,000 proposals, 4 independent restarts per instance, best of 4 kept (≈ 20-60 s per instance).

**Why this parametrisation.** Plain penalty annealing over (posP, posC, s) (sa.c mode 4/5) leaves 1-6 crib letters violated at λ = 10 and finds scores no better; mode 10 satisfies the cribs exactly and gives the best scores of the 7 search variants tried (§4).

**Instances per period** (same search, same restarts, same seeds policy for all):
- Controls: 97-letter windows of held-out English (PG #1661 Sherlock Holmes, #84 Frankenstein; not in the scoring corpus), with EASTNORTHEAST written over positions 22-34 and BERLINCLOCK over 64-74 (so the crib letters, and hence the crib constraint structure, are identical to K4's), encrypted with random posP, posC, shifts at the same period. Recovery = ≥ 80% of the 73 non-crib letters correct.
- Nulls: K4 with its 73 non-crib letters randomly permuted (crib-position ciphertext letters kept, so the crib constraint system is exactly K4's and always satisfiable where K4's is; same letter frequencies). This is "random ciphertext with the same crib constraints".
- K4 itself.

Periods (from ruled_out.md / w-crib §2 / w-audit): Q4 crib-consistent non-vacuous {16,19,20,23,24,26,30,31,32,33,35,37,38,39,40,41,46,47,48,49,51,52} plus crib-vacuous 27,28,29,53-60 = **33 periods**. Not run:
- p = 8 and 13: Q4-alive but excluded by column IC at P<0.001 (w-stats §4).
- p = 11, 12, 18, 22, 36, 44: Q4 crib-dead.
- p = 10, 21, 25, 42, 50: alive only with crib errors.
p = 23 and 26 are IC-disfavoured at P<0.01 but were included.
Controls and nulls per period: 12 controls / 24 nulls for p ≤ 35, 40 and 47; 6 controls / 12 nulls elsewhere. That gives 294 controls, 588 nulls (some periods kept extra nulls from a restarted run) and 33 K4 runs, plus the p=29 follow-up.

## 1. Results per period (Quagmire IV, crib-exact SA; scores = total log10 over 94 quadgrams)
"found ≥ true, wrong": the control's best SA decrypt scores at least as high as the true plaintext but is <80% correct (spurious optimum: the MAP solution is wrong).
"power": controls whose found score exceeds null mean + 2.326 sd (the null's 99th percentile).
"p ×33": Bonferroni over the 33 periods.

| p | controls recovered (acc≥0.8) | median acc | true-PT score (mean) | control found (mean) | found ≥ true, wrong | null n | null mean ± sd | null max | power | K4 best | nulls ≥ K4 | z | p (normal) | p ×33 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16 | 0/12 | 0.18 | -411.4 | -445.9 | 0/12 | 24 | -458.2 ± 10.5 | -429.8 | 0/12 | -464.2 | 17/24 | -0.58 | 0.718 | 1.00 |
| 19 | 0/12 | 0.14 | -400.4 | -431.0 | 0/12 | 24 | -440.2 ± 10.5 | -418.4 | 1/12 | -440.0 | 11/24 | +0.03 | 0.490 | 1.00 |
| 20 | 0/12 | 0.11 | -405.1 | -429.9 | 1/12 | 24 | -435.3 ± 6.3 | -423.5 | 1/12 | -435.9 | 13/24 | -0.11 | 0.543 | 1.00 |
| 23 | 0/12 | 0.12 | -407.2 | -424.4 | 2/12 | 24 | -426.0 ± 8.8 | -408.6 | 1/12 | -437.5 | 23/24 | -1.32 | 0.906 | 1.00 |
| 24 | 0/12 | 0.14 | -404.0 | -419.9 | 1/12 | 24 | -428.7 ± 7.5 | -413.1 | 1/12 | -426.2 | 6/24 | +0.33 | 0.372 | 1.00 |
| 26 | 0/12 | 0.14 | -409.5 | -417.7 | 3/12 | 24 | -423.6 ± 6.7 | -413.2 | 1/12 | -422.4 | 13/24 | +0.18 | 0.430 | 1.00 |
| 27 | 0/12 | 0.13 | -407.0 | -415.3 | 3/12 | 24 | -422.4 ± 6.4 | -405.3 | 3/12 | -419.7 | 8/24 | +0.43 | 0.333 | 1.00 |
| 28 | 0/12 | 0.10 | -402.2 | -413.8 | 3/12 | 24 | -418.0 ± 5.0 | -411.0 | 2/12 | -420.8 | 18/24 | -0.56 | 0.713 | 1.00 |
| 29 | 0/12 | 0.13 | -403.0 | -410.2 | 4/12 | 24 | -417.7 ± 6.1 | -407.1 | 0/12 | -400.8 | 0/24 | +2.75 | 0.003 | 0.10 |
| 30 | 0/12 | 0.11 | -408.1 | -405.7 | 7/12 | 24 | -411.6 ± 6.7 | -396.1 | 1/12 | -418.3 | 22/24 | -1.00 | 0.840 | 1.00 |
| 31 | 0/12 | 0.11 | -406.6 | -405.0 | 4/12 | 24 | -410.4 ± 4.5 | -402.6 | 3/12 | -407.4 | 6/24 | +0.68 | 0.249 | 1.00 |
| 32 | 0/12 | 0.11 | -409.6 | -399.6 | 10/12 | 24 | -407.0 ± 4.3 | -393.6 | 5/12 | -405.3 | 6/24 | +0.40 | 0.346 | 1.00 |
| 33 | 0/12 | 0.10 | -405.2 | -397.0 | 9/12 | 24 | -405.3 ± 5.8 | -393.0 | 3/12 | -401.4 | 4/24 | +0.68 | 0.250 | 1.00 |
| 35 | 0/12 | 0.10 | -400.8 | -393.4 | 7/12 | 24 | -395.8 ± 4.7 | -387.0 | 0/12 | -395.6 | 11/24 | +0.03 | 0.490 | 1.00 |
| 37 | 0/6 | 0.06 | -410.2 | -385.4 | 6/6 | 12 | -391.8 ± 5.8 | -379.8 | 0/6 | -393.4 | 7/12 | -0.28 | 0.611 | 1.00 |
| 38 | 0/6 | 0.07 | -402.9 | -379.4 | 6/6 | 12 | -386.7 ± 4.8 | -379.3 | 2/6 | -378.8 | 0/12 | +1.64 | 0.051 | 1.00 |
| 39 | 0/6 | 0.10 | -403.4 | -382.6 | 5/6 | 12 | -381.8 ± 4.4 | -373.0 | 0/6 | -388.2 | 12/12 | -1.46 | 0.928 | 1.00 |
| 40 | 0/12 | 0.08 | -405.3 | -379.3 | 12/12 | 24 | -381.1 ± 4.5 | -372.6 | 0/12 | -384.5 | 20/24 | -0.77 | 0.780 | 1.00 |
| 41 | 0/6 | 0.06 | -411.4 | -379.7 | 6/6 | 12 | -381.0 ± 4.5 | -371.1 | 0/6 | -373.1 | 1/12 | +1.74 | 0.041 | 1.00 |
| 46 | 0/6 | 0.14 | -416.4 | -368.1 | 6/6 | 12 | -373.4 ± 4.3 | -367.1 | 1/6 | -370.4 | 3/12 | +0.70 | 0.241 | 1.00 |
| 47 | 0/12 | 0.08 | -402.1 | -372.2 | 12/12 | 24 | -373.4 ± 3.9 | -366.5 | 0/12 | -368.7 | 4/24 | +1.20 | 0.115 | 1.00 |
| 48 | 0/6 | 0.05 | -411.8 | -370.6 | 6/6 | 12 | -371.4 ± 3.0 | -366.2 | 2/6 | -367.4 | 1/12 | +1.32 | 0.093 | 1.00 |
| 49 | 0/6 | 0.10 | -403.6 | -366.1 | 6/6 | 12 | -371.3 ± 4.6 | -363.2 | 1/6 | -375.9 | 9/12 | -1.00 | 0.842 | 1.00 |
| 51 | 0/6 | 0.12 | -404.4 | -366.5 | 6/6 | 12 | -369.7 ± 2.9 | -364.4 | 2/6 | -371.2 | 9/12 | -0.51 | 0.694 | 1.00 |
| 52 | 0/6 | 0.08 | -402.5 | -367.4 | 6/6 | 12 | -369.1 ± 4.9 | -363.1 | 0/6 | -374.4 | 11/12 | -1.09 | 0.862 | 1.00 |
| 53 | 0/6 | 0.08 | -411.2 | -369.8 | 6/6 | 12 | -372.6 ± 3.6 | -367.2 | 0/6 | -372.3 | 5/12 | +0.09 | 0.463 | 1.00 |
| 54 | 0/6 | 0.09 | -409.4 | -368.3 | 6/6 | 12 | -371.3 ± 4.5 | -362.5 | 0/6 | -368.2 | 3/12 | +0.69 | 0.246 | 1.00 |
| 55 | 0/6 | 0.10 | -406.4 | -365.9 | 6/6 | 12 | -370.4 ± 4.0 | -362.4 | 1/6 | -368.8 | 3/12 | +0.39 | 0.347 | 1.00 |
| 56 | 0/6 | 0.12 | -405.2 | -365.9 | 6/6 | 12 | -369.1 ± 4.7 | -360.7 | 0/6 | -360.7 | 0/12 | +1.80 | 0.036 | 1.00 |
| 57 | 0/6 | 0.09 | -406.0 | -366.6 | 6/6 | 12 | -368.8 ± 3.3 | -363.6 | 1/6 | -369.1 | 6/12 | -0.09 | 0.534 | 1.00 |
| 58 | 0/6 | 0.09 | -395.7 | -364.4 | 6/6 | 12 | -367.3 ± 5.4 | -353.4 | 0/6 | -368.8 | 9/12 | -0.28 | 0.612 | 1.00 |
| 59 | 0/6 | 0.12 | -407.0 | -360.9 | 6/6 | 12 | -364.5 ± 3.6 | -358.5 | 0/6 | -365.8 | 7/12 | -0.37 | 0.644 | 1.00 |
| 60 | 0/6 | 0.07 | -410.4 | -361.0 | 6/6 | 12 | -363.8 ± 5.0 | -353.7 | 0/6 | -363.2 | 6/12 | +0.14 | 0.445 | 1.00 |

Reading the table:
- **Recovery is 0 everywhere.** Median accuracy on the 73 non-crib letters is 0.05-0.18. The crib letters themselves are exact by construction.
- **True English scores −395 to −416 (−4.2 to −4.4 per quadgram) at every period. The annealed null rises steadily with p:** −458 (p=16), −428 (24), −412 (30), −396 (35), −381 (40), −369 (52), −364 (60).
  - From p ≈ 32 the *random* null optimum (mean) is at or above the English mean.
  - From p ≈ 37 nearly every control’s SA optimum beats its own true plaintext (125/126 controls).
  - Quadgram score cannot identify the plaintext there, whatever the search.
- **p = 16-28:** the null stays below English, so the period would be testable *if* the search could reach the true basin. It cannot. Controls end only 2-12 units above the null mean, about one null sd, and 0-3/12 controls clear the null 99th percentile.
- **K4** sits inside the null at every period. Its z ranges from −1.46 to +2.75, and the 33 values look like a standard normal sample (mean +0.18, sd 0.97). Only p=29 has a local p < 0.01 (see §2).

## 2. p = 29 follow-up (the only local p < 0.01)
The first K4 run scored −400.8, above all 24 nulls (z = +2.75 under a normal fit; Bonferroni ×33 = 0.10, not significant).
- **Follow-up:** 12 more K4 runs with fresh seeds, plus 100 more nulls, same settings.
  - Nulls: n = 124, mean −416.6, sd 6.2, max −399.8 (a null beat the "anomaly").
  - K4: 13 runs, median −415.7, range −426.1 to −400.8. Median z = +0.15; P(K4 run > null run) = 0.60.
- **Conclusion:** the −400.8 was the best of one lucky restart, and K4 at p=29 behaves like a shuffled-K4 null.
- **No stable decrypt.** The 13 K4 solutions share no non-crib text. Top run:
  `TOACHACOMPREETHEFRENCEASTNORTHEASTANATHINTTEDSILEWITREAFEALUREDBERLINCLOCKENASSALTHESSYESTTHEMNEC`
  This is English-like letter salad, not English. Every other period's K4 best is similar, e.g. p=40: `ILLESAVENLEPEATIERETHEASTNORTHEASTOTHETHEFULDNEAREWITHEMENOGREMBERLINCLOCKINAGETANTHESAYEWASSENOU`.

## 3. General periodic substitution (independent alphabet per class; sa.c mode 0, cribs exact by construction)
4 controls / 8 nulls per period, 2 restarts × 2M:

| p | controls recovered (acc≥0.8) | median acc | true-PT score (mean) | control found (mean) | found ≥ true, wrong | null n | null mean ± sd | null max | power | K4 best | nulls ≥ K4 | z | p (normal) | p ×4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16 | 0/4 | 0.22 | -405.0 | -332.4 | 4/4 | 8 | -327.5 ± 3.8 | -320.7 | 0/4 | -327.3 | 4/8 | +0.05 | 0.482 | 1.00 |
| 24 | 0/4 | 0.14 | -405.7 | -327.6 | 4/4 | 8 | -319.7 ± 4.0 | -314.7 | 0/4 | -316.4 | 1/8 | +0.81 | 0.208 | 0.83 |
| 30 | 0/4 | 0.09 | -395.4 | -319.0 | 4/4 | 8 | -318.5 ± 2.7 | -315.4 | 0/4 | -319.8 | 5/8 | -0.47 | 0.681 | 1.00 |
| 40 | 0/4 | 0.08 | -418.3 | -316.1 | 4/4 | 8 | -315.5 ± 2.2 | -311.8 | 0/4 | -314.3 | 3/8 | +0.55 | 0.290 | 1.00 |

At p ≥ 16 each class holds ≤ 7 letters, each with its own 26-letter substitution, so the model can write almost any text. Annealed random nulls reach −312 to −328, about −3.4 per quadgram. Real English gives −4.3 per quadgram, so the nulls beat English by about 80 units. **Untestable at every period ≥ 16. Any "English" decrypt under this model is meaningless.** (Already implied by w-crib §2: "consistent means cannot be refuted"; this quantifies it.)

## 4. Search diagnostics: why p = 16-28 is search-limited, not information-limited
- Seven search variants were tried on the same 97-letter p=16/20 controls. All gave 0 recoveries; the crib-exact mode 10 gave the best scores with 0 crib violations.
  1. Penalty annealing over (posP, posC, s) with crib-derived shifts, in sa.c mode 4. It was tried with T0 = 3-100, λ = 3-30, λ ramped, and move mixes of 3-40% posC.
  2. All shifts free (mode 5).
  3. Nested annealing: outer posC, inner greedy (mode 6) or inner SA (mode 7).
  4. Heat-bath moves over all 26 alternatives (modes 8, 9, 11).
  5. Compensated (class-preserving) double swaps.
  6. 30M-proposal single runs: best −448 vs true −415 at p=16.
  7. The crib-exact mode 10 used above.
- **Oracles:**
  - Given the true *cipher* alphabet (posC fixed; the problem reduces to Quagmire I), the same annealer recovers 100% of the plaintext at p=16, 97 letters (3/3 restarts, 2M proposals). The true key is also a stable local maximum: started there, the annealer stays.
  - Given the true *plain* alphabet only, it does not recover at 97 letters.
  - Free search fails even with much more text: p=16 at 200/400/800 letters gives accuracy 0.28/0.25/0.30, and p=4 at 400 letters gives 0.80 accuracy at a score of −2031 vs true −1649.
  - **So the joint two-permutation landscape is the obstacle, not the 97-letter length.**
- **What this means:**
  - At p = 16-24 a much better two-alphabet search *might* still discriminate. Spurious-dominance is low there: 0/12 at p=16 and 19, 1/12 at 20 and 24, 2/12 at 23.
  - No such search exists in this project, so these periods are **untestable by this method**.
  - At p ≥ 30 more search effort cannot help (§1).

## 5. Conclusions and hypothesis status
| H | claim | status |
|---|---|---|
| H-1901 | K4 = Quagmire IV (two arbitrary alphabets), no transposition, at a surviving period 16-60, detectable by crib-constrained SA + quadgrams | UNTESTABLE (0/294 controls recovered; p ≥ 30 spurious optima beat true English) |
| H-1902 | K4 shows excess English-likeness under Q4 at some period (K4 vs shuffled-K4 null) | NOT SUPPORTED: min local p 0.003 at p=29, Bonferroni ×33 = 0.10, not reproduced in 12 reruns |
| H-1903 | General periodic (independent alphabets) at p ≥ 16 testable by SA | NO: nulls out-score English by ~80 log10 units |
| H-1904 | Method note: 97-letter SA "solutions" for two-alphabet periodic models | Expect spurious English-like salad scoring −4.0 to −3.9 per quadgram at p ≥ 35; require a matched shuffled-ciphertext null before believing any |

Implications for the board:
- Nothing new is excluded.
- Q4 at the surviving periods and H-1404/H-1804 (keyword or route generators under two arbitrary alphabets) stay open. Neither crib algebra (w-crib, w-keygen) nor 97-letter statistical attack can close them.
- Only an extra constraint can make them testable. Options:
  - keyword-mixed alphabets (a few hundred candidates each instead of 26!), which turns Q4 into a test that can be enumerated;
  - a second ciphertext in depth (K5, H-k5);
  - a concrete key hypothesis.

## Caveats
- The model assumes no transposition and Sanborn's crib positions exactly. Error-tolerant variants (p = 10, 21, 25, 42, 50) were not annealed.
- Quadgram table built here: 5 PG books, 5.25M letters. It is not identical to tools/quadgram.py's 2-book build but uses the same formula. Controls were drawn from held-out books.
- Nulls are shuffled K4. They have K4's crib-letter structure and frequencies, but under a Q4 hypothesis they are not "Q4-encrypted random text". A uniform-random-plaintext null was not run.
- Control counts are small at high p (6 per period). The conclusion there (spurious ≥ true in 100%) does not need more.
- SA results are stochastic. Every instance kept the best of 4 restarts, identically for controls, nulls and K4, so the comparison is fair. The p=29 follow-up shows the size of restart luck: about 15 log10 units between K4 reruns.
