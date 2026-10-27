# Journal

One entry per iteration: hypothesis → reasoning → test → result → next.

## 2026-10-26 — Phase 1 survey (summary)
Broad survey by parallel workers. Outcome: the classical families are ruled out (see `PLAN.md` "Where we are", `hypotheses/ruled_out.md`, `findings/`). Main lesson: what remains cannot be tested by the cribs without a specific key hypothesis, so from here on the work is one hypothesis at a time.

## 2026-10-27 — Iteration 1: separable grid key
- **Hypothesis:** the key depends only on where each letter sits in a grid: k = f(row) + g(col) mod 26, width w, start offset o, fixed tableau (Vigenère / Beaufort / variant Beaufort, AZ or KRYPTOS alphabet).
- **Why:** Sanborn's "visual systems for encoding" (Wired 2005); the width-7/21 anomalies; the NSA's "interval 7". A grid key is a simple hand method that would produce exactly that kind of column signal.
- **Test:** an exact consistency check. Each crib key value links one row to one column, and the key is consistent only if every cycle in that graph sums to 0 mod 26. Script: `iterations/it01_grid_key.py`. Widths 2–48, every offset, 6 tableaux. 1,034 (w,o) configurations per tableau contain at least one cycle, so the test can decide them.
- **Control:** a key planted at w=21, o=5 on English text was recovered.
- **Result:** 0 consistent configurations for K4. **Refuted** for w ≤ 48 under fixed tableaux. Random ciphertexts give 0 hits 40% of the time (mean 15), so K4's 0 is not anomalous in itself; the refutation stands because the true configuration would have to pass.
- **Not covered:** unknown mixed alphabets; widths ≥ 49 (too few cycles to test).
- **Next:** hypothesis 2, the structure of the known KRYPTOS-alphabet key letters.

## 2026-10-27 — Iteration 2: structure in the known key letters
- **Hypothesis:** if K4 uses a standard tableau (AZ or KRYPTOS alphabet; Vigenère, Beaufort or variant), the 24 key letters at the cribs show a simple generating rule, such as an arithmetic progression or alphabet runs.
- **Key letters:** Vig/KA `RDUMRIYWOYNKY` / `ELYOIECBAQK`. Visible features: a 3-letter alphabet run (`CBA` under Vig/KA, `LMN` under variant Beaufort/KA, both at positions 70–72) and `KKK` under Beaufort/AZ at positions 31–33.
- **Test:** look-elsewhere control. Compute the same features (the longest run of equal successive differences, and the number of ±1 runs) for 20,000 random ciphertexts across all tableaux.
- **Result:** the longest run is P=0.95 and the ±1 runs are P=0.21. Both are chance-level, so there is **no internal structure**. This agrees with phase 1 (w-crib): under a standard tableau the key looks random, so it is not a progression or an alphabet walk.
- **Next:** hypothesis 3, a concrete hand system behind Sanborn's "matrix codes Ed gave me".

## 2026-10-27 — Iteration 3: flipped or rotated Kryptos tableau
- **Lead:** Sanborn's "matrix codes Ed gave me … visual systems for encoding" (Wired 2005 via [rumkin](https://rumkin.com/reference/kryptos/k5/)), and a quote attributed to him in a [Schneier-blog comment](https://www.schneier.com/blog/archives/2025/08/jim-sanborn-is-auctioning-off-the-solution-to-part-four-of-the-kryptos-sculpture.html) (withoutwax, 17 Oct 2025, source not given, so UNVERIFIED): *"You take that chart and you flip it this way and it turns into this chart, so the final letter in a coding system might be the W up there."*
- **Hypothesis:** K4 uses a transformed copy of the Kryptos tableau (any of the 8 flips/rotations of the square), with a header alphabet AZ, KA, reversed AZ or reversed KA, either lookup direction, and a periodic key.
- **Test:** an exact per-residue row intersection, for periods 1–48, across 128 tableau variants. Script: `iterations/it03_flipped_tableau.py`. Control: a planted flipped-tableau key at P=13 was recovered.
- **Result:** every variant is dead at every period except 27–29, where no two cribs share a column, so the test cannot decide. At those periods the cribs fix 24 of the key letters. The forced decrypts collapse to **18 distinct texts**, the same 18 found in phase 1, because all the flips reduce to the same three tableau families. All are gibberish: the best scores 1.29 against 1.71 for English (mean log letter frequency). **Refuted.**
- **Insight:** flipping or rotating a cyclic tableau gives nothing new. Any tableau whose rows are shifts of a single alphabet reduces to Vigenère/Beaufort with that alphabet. If the "flip" hint is real, it has to involve a non-cyclic chart (e.g. the KA tableau combined with its AZ header in a way that breaks the cyclic structure) or a key that isn't periodic.
- **Next:** pin down the source of the "flip the chart … W" quote. If it is genuine, it describes the method. Meanwhile, hypothesis 6 (one carving error in a crib).

## 2026-10-27 — Iteration 4: one carving error in a crib
- **Note from it03 follow-up:** I found the NSA's 2007 "KRYPTOS SUMMARY" and "KRYPTOS SLIDES" at media.defense.gov, but both return 403 from this environment, so they still need to be fetched from another network. I could not trace the "flip the chart … W" quote to a primary source (it isn't in the Zona Motel interview; the comment cites none).
- **Hypothesis:** the phase-1 keyword-generator screen (900,272 streams: periodic, progressive, chain addition, interrupted, columnar-position, two-keyword) missed the true key because one crib letter was carved wrong. K1–K3 all contain carving or keying errors.
- **Test:** for each stream × 12 fixed tableaux × 26 constant shifts, count mismatches against the key the cribs require. A true key with one carving error gives exactly 1 mismatch. A random stream reaches ≤1 mismatch with probability ~1e-30, so the test is decisive. Script: `iterations/it04_one_error.py`. Control: a planted progressive key with a carving error at position 30 was found.
- **Result:** 0 streams within 1 mismatch. **Refuted** for these families under fixed tableaux, even allowing one carving error.
- **Next:** stop re-checking generator families. Hypothesis 7: decide the two-alphabet survivor streams from the full text.

## 2026-10-27 — Iteration 5: full-text test of two-alphabet survivors
- **Hypothesis:** one of the 258 keyword-generator streams that the cribs could not decide under two unknown alphabets (phase-1 H-1404: 192 progressive, 53 two-keyword, 12 columnar, 1 chain) is the true key.
- **Why testable:** w-synth's information budget says a *fixed* stream under two unknown alphabets is decidable from the full 97 letters.
- **Test:** crib-constrained annealing over both alphabets with the stream fixed, scored by quadgrams (`iterations/it05/`, from w-synth's `sa.c`). Calibration: 17 of 20 planted streams were recovered at ≥90% accuracy; true English scores −395 to −434. Null: 40 random streams that satisfy the crib relations.
- **Result:** the best K4 survivor scores −490.7 (`SHADOWFORCES` progressive), against a null maximum of −498. Every survivor is about 60 log10 units below the English range, and the decrypts are word salad, e.g. `HASHEHICLAPINGSAKSJUNEASTNORTHEAST…`. **Refuted.** That closes phase-1 H-1404.

## 2026-10-27 — Iteration 6: the doublets argue against a structureless key
- **Observation:** K4 has 6 doubled letters (0-indexed starts 18 BB, 25 QQ, 32 SS, 42 SS, 46 ZZ, 67 TT). Five of them sit at i ≡ 4 (mod 7). The cribs cover three pairs at that residue (25 NO→QQ, 32 ST→SS, 67 IN→TT), and **all three are doublets even though the plaintext letters differ.**
- **Why it matters:** the only model class left open is a key that does not depend on the plaintext. Under any such key, the ciphertext is a random string independent of the plaintext, so a doublet over two different plaintext letters is a coincidence.
- **Test:** Monte Carlo over 200,000 random 97-letter strings, scanning every width 2–30 and every residue. Script: `iterations/it06_doublets.py`.
- **Result:** P(≥5 doublets aligned at one width/residue) = 0.083. P(that **and** every crib-covered pair at that residue a doublet, with ≥3 such pairs) = **1.5×10⁻⁵**. This is a post-hoc statistic, so discount it generously (×100 still gives about 10⁻³).
- **Conclusion:** strong evidence that the key is **not** structureless at the residue-4→5 step. Something ties consecutive letters together every 7 positions, so the key must have period-7 structure in its successive differences. That is exactly what a grid key k = f(row) + g(col) with width 7 produces.

## 2026-10-27 — Iteration 7: width-7 grid key under an unknown alphabet (partial)
- **Hypothesis:** k_i = f(⌊(i+o)/7⌋) + g((i+o) mod 7), under one unknown mixed alphabet (Quagmire-III form). it01 only refuted it for fixed tableaux. It explains it06: doublets occur where α(p_{i+1}) − α(p_i) equals the constant column step g5 − g4. It also requires α(O)−α(N) = α(T)−α(S) = α(N)−α(I).
- **Crib test (exact, CP-SAT):** `iterations/it07_grid_key_mixed.py`. K4 is satisfiable at w=7 for offsets 0–3 (also w=14, o=0–3; w=21, o=14–17). **But** 24 random ciphertexts are satisfiable at nearly every offset too, so the cribs alone cannot decide it. The control was recovered.
- **Full-text test:** a crib-exact annealer (`iterations/it07/sa2u.c`) could not reach crib-consistent alphabets on planted controls (it stalls at 3–8 violated crib equations). The search is the limit, not the information: by budget the model is about 180 bits, against about 249 available.
- **Status:** OPEN, the leading hypothesis. **Next:** a better solver. Use CP-SAT to enumerate the crib-consistent assignments of the crib letters, then anneal the remaining letters and the free key components with the cribs held exactly; calibrate on planted controls before touching K4.

## 2026-10-27 — Iteration 8: keyword alphabets under the width-7 grid key
- **Hypothesis:** the it07 grid key uses a keyword-mixed alphabet, as K1–K3 did.
- **Filter (derived from it06):** if the key step is the same at every residue-4 boundary, the crib doublets force α(O)−α(N) = α(T)−α(S) = α(N)−α(I) (mod 26). This holds for Vigenère or Beaufort form, with one or two alphabets.
- **Test:** 2,216,106 alphabets from 370k English words (keyword+rest, keyword+continue, columnar-keyed, each also reversed). 10,126 pass the filter (7,994 distinct). Each survivor then gets the exact fixed-alphabet grid test at widths 7/14/21/28/35/42, every offset: Quagmire III (β=α), plus two alphabets with β ∈ {AZ, KA, reversed AZ, reversed KA}. Script: `iterations/it08_keyword_alphabets.py`. Control: a planted keyword alphabet at w=7 was found.
- **Result:** **0 hits at widths 7, 14, 21, 28 and 42.** The only hits are at w=35 (4 cycles): CHAVICIN, MEDALLIC, PADRINO, TINTOMETER and similar. The chance expectation there is about 0.6–2.5, so these are noise. **Refuted** for dictionary-keyword alphabets.
- **Remaining:** an arbitrary (non-dictionary) alphabet, which needs the better solver from it07; or a different mechanism for the doublets.

## 2026-10-27 — Iteration 9: solver for the generic grid key (parked)
- **Goal:** decide the generic width-7 grid key (arbitrary α, f, g) from the full text.
- **Tried, all calibrated on planted controls:**
  1. A penalty annealer over α and f, g: never reached crib consistency.
  2. A row-optimised annealer (α and g annealed, each row's f chosen optimally): never reached crib consistency.
  3. An exact kernel parametrisation: every crib-consistent (α, f, g) is X = 13·K₂t₂ + 14·K₁₃t₁₃ (mod 26), with kernels of dimension 24 mod 2 and 24 mod 13 (`iterations/it07/kernel.py`, `sak.c`). The cribs hold by construction, but annealing cannot remove the alphabet collisions (injectivity).
- **Search-limited, not information-limited.** On planted controls, all three fail before K4 is even tried.
- **Natural instances are already dead:** the obvious concrete form, a 7-letter keyword with a row progression (e.g. KRYPTOS + s·row), was refuted under fixed tableaux (it01), under one unknown alphabet (phase-1 keygen F1, exact), under two alphabets (it05), and with dictionary-keyword alphabets (it08).
- **Status:** generic version PARKED. It needs either a constraint-programming formulation with a language objective, or a source-based value for g (the 7 column shifts).

## 2026-10-27 — Iteration 10: small key range ("minor differences")
- **Evidence:** Bean 2021 §2.4. Ciphertext letters that encrypt the same plaintext letter lie close together in A–Z (mean distance 3.6; 1 in 240 under permutation). That suggests a digit-like key with a small range.
- **Hypothesis:** c = β[(α(p) + d) mod 26], with key digits d ∈ [0, B−1] for small B and β ∈ {AZ, KA, reversed}.
- **Test:** the smallest key range B that K4's cribs allow (the largest per-letter cyclic window), compared with 100,000 random ciphertexts. Script: `iterations/it10_small_key_range.py`.
- **Result:** K4 needs B ≥ 12 under every β; O→Q,F alone needs a window of 12. Random ciphertexts need B ≤ 12 with P = 0.145. **Not significant.** A digit key (B=10) is impossible under these β. Bean's mean-distance statistic is weaker evidence than it looks: the worst letter needs a 12-wide range.

## 2026-10-27 — Iteration 11: "key values are multiples of 5"
- **Evidence:** Bean 2021 footnote 2. With plain AZ and cipher numbered by the reversed Kryptos alphabet, 13 of the 24 key values are multiples of 5 (1 in 1,470). That would point to a base-5 component, i.e. the Mengenlehreuhr.
- **Check:** reproduced. It is the same as AZ/KA in the sum form: 13 of 24 ≡ 0 mod 5. Look-elsewhere: scan 4 plain × 4 cipher alphabets × 3 sign forms × moduli 3–7 and take the most surprising binomial tail, then compare with 3,000 random ciphertexts.
- **Result:** look-elsewhere **P = 0.058**. Suggestive at best and not significant once all the tableau choices are counted. Sanborn has also since said BERLINCLOCK means the World Clock, not the Mengenlehreuhr. **Not pursued.**
- **Ranking of K4's known anomalies after correction:** aligned doublets at i≡4 mod 7 (it06, ~1e-5 post hoc) ≫ width-21 vertical bigrams (FW 0.005) > multiples of 5 (0.058) > minor differences (0.145 for the max).

## 2026-10-27 — Iteration 12: KRYPTOS as the column key of a width-7 grid key
- **Hypothesis.** The doublet alignment (it06) comes from k_i = f(row) + g(col), width 7, with g = KRYPTOS (the 7-letter keyword of K1–K2), under an unknown plaintext alphabet (Quagmire III style) or with the ciphertext alphabet AZ or KA.
- **Test.** `iterations/it12_kryptos_column_key.py`. Exact CP-SAT feasibility over 4 numberings × 7 offsets × {Vig, Beau} × {same, AZ, KA} = 168 configs. Row shifts f free.
- **Control.** Planted (KA0, o=2, Vig, same) recovered.
- **Null.** Random ciphertexts: 0, 3, 0 of 168 feasible.
- **Result.** K4: 0 of 168. **Refuted.** The cheapest concrete keyword form of the grid key is dead; the generic grid model stays open (search-limited, it07).

## 2026-10-27 — Iteration 13: Stehle's DIAWINFBN lag-4 run
- **Observation.** CT[55..63] = DIAWINFBN: ct[i+4] − ct[i] = 5 (AZ) for i = 55..59, i.e. INFB = DIAW + 5 and N = I + 5. Ends on the first letter of BERLINCLOCK (pos 63).
- **Test.** `iterations/it13_lag_runs.py`. Longest run of equal lag-d differences, d = 1..12, any value, on 200k random 97-letter texts.
- **Result.** K4 max run = 5 (lag 4); all other lags ≤ 3. P(max run ≥ 5) = 0.0021; ×2 for choosing AZ vs KA ≈ 0.004. In KA indices the differences are [5,4,5,11,4]: no structure, so if real it is an AZ-arithmetic feature.
- **Reading.** Real but weaker than the doublets (1.5e-5), and partly post hoc (it was reported because it stood out). Mechanisms that would make it: plaintext with a 4-letter repeat there plus a key rising by 5 every 4 steps, or a key with a local period-4 difference. Neither is natural with the width-7 grid key. Logged as anomaly #2; not pursued alone.

## 2026-10-27 — Iteration 14: aligned doublets as copying errors
- **Hypothesis.** The second letter of each residue-4 doublet is a copy of its left neighbour (a transcription slip), so ct at 26, 33, 68 (0-idx, all in cribs) is wrong. With those 3 positions masked, a periodic cipher (missed by phase 1, which tolerated only 2 errors) would fit.
- **Test.** `iterations/it14_doublet_overwrite.py`. Vig/Beau/varBeau × AZ/KA, periods 1..48, crib consistency with the 3 positions masked.
- **Control.** Period-11 Vig/KA with planted overwrites: unmasked fails, masked recovers period 11 (and 22).
- **Result.** K4: only periods 27–30 fit, and those carry no crib collisions at all (vacuous). Every identifiable period fails. Null rate of a spurious period ≤ 20 with 3 random masks: 0/20000. **Refuted.**

## 2026-10-27 — Iteration 15: the grid key does not explain the doublets (correction to it06/it07)
- **Question.** It06 took the residue-4 doublets as evidence for a width-7 grid key k = f(row) + g(col). Does that model actually make doublets likely?
- **Algebra.** Within a row, c_i = c_{i+1} ⇔ α(p_i) − α(p_{i+1}) = g(col+1) − g(col) = D. Doublets at that residue happen only when the plaintext bigram has α-difference D, which for English and a generic α is about 1/26: the same rate as a random key.
- **Test.** `iterations/it15_grid_doublet_rate.py`, 100k English 97-letter windows (pg2600), random α, f, g vs. a structureless key.
- **Result.** P(≥ 5 doublets at one residue of width 7): grid key 0.0019, random key 0.0008. Likelihood ratio ≈ 2.4, against the ~10⁴ the anomaly needs. **The grid-key reading of the doublets is wrong.** #8 loses its motivation; it07/it08/it12 refutations stand but the line is closed.
- **What would explain it.** A mechanism with ciphertext feedback or deliberate copying at one column (c_{i+1} tied to c_i, not to a key difference), or chance/design by Sanborn. A copy-error mechanism under a periodic key is refuted (it14); under a non-periodic key it is untestable by cribs.

## 2026-10-27 — Iteration 16: K1–K3 control and a fairer look-elsewhere for the doublets
- **Question.** Is K4's aligned-doublet pattern unusual next to Sanborn's own K1–K3, and how much of it06's P≈1.5e-5 is tailoring?
- **Test.** `iterations/it16_k123_doublets.py`: the it06 alignment statistic (max doublet starts at one residue, widths 2..30) on 97-letter windows of K1–K3 and K4, vs 20k random strings. Plus a less tailored joint statistic (≥5 aligned at one residue with ≥3 of them in crib zones), 200k random strings.
- **Result.** Alignment alone: K4 = 5 (w=7, r=4), P = 0.083; K2[194:291] also reaches 5 (w=3), same P. Joint statistic: P = 0.008. Any ≥3 doublets in crib zones: P = 0.05.
- **Correction.** It06's 1.5e-5 came from requiring *all* crib-covered pairs at the chosen (w, r) to be doublets, a condition shaped after seeing the data. A fairer figure is ≈0.01, and K2 shows comparable alignment by chance. The doublets are a weak anomaly, not a lead. #9 is parked; no doublet mechanism will be pursued further without independent support.

## 2026-10-27 — Iteration 17: source of the "flip the chart … the W up there" quote (#3b)
- **Goal.** Find where Sanborn said it, so the rule can be read in context instead of guessed.
- **Found.** The quote is in a Schneier-blog comment by "withoutwax", 17 Oct 2025, with no source. The best candidate source is the RR Auction video "Jim Sanborn Reveals New Kryptos Clues Ahead of Auction — K4 and K5 Explained" (youtube.com/watch?v=QTGcaCPIYl4, channel RR Auction Official; title confirmed via oEmbed). The Kryptosfan 2011 "chart clue about direction" post has no Sanborn quote.
- **Blocked.** YouTube blocks caption requests from this cloud IP (RequestBlocked); not circumvented. Needs the transcript fetched from Stas's network, then a check of whether the quote is there and which chart and W it refers to.
- **Status.** #3b moves from "source not found" to "candidate source found, waiting on transcript".

## 2026-10-27 — Iteration 18: base-26 Gromark ("Vimark") under mixed alphabets
- **Why.** Phase 1 tested Vimark only with AZ/KA tableaux and Gromark only in bases 2–16. Base 26 with a mixed alphabet was an open gap, and Scheidt's "change the language base" hint points at the Gromark family.
- **Model.** Primer k_0..k_{n−1}, rule A k_{j+n} = k_j + k_{j+1} (ACA) or rule B k_{j+n} = k_j + k_{j+n−1}, mod 26. (i) one unknown alphabet α, Vig α(c) = α(p) + k or Beau α(c) = k − α(p); (ii) ACA shape: plain AZ or KA, unknown cipher alphabet β(c) = plain(p) + k.
- **Method.** The crib equations are linear mod 26 in (alphabet values, primer). `iterations/it18b_vimark_linear.py` checks consistency mod 2 and mod 13 (CRT). `iterations/it18c_vimark_alldiff.py` enumerates the solution spaces and enforces the alphabet's all-different constraint exactly. A direct CP-SAT model (`it18_vimark_mixed.py`) timed out even on the control, so it was replaced.
- **Control.** Planted n=5 rule-A key with a random α recovered.
- **Results.**
  - ACA shape (plain AZ/KA): K4 linearly inconsistent for n = 2..10 under both rules. Null pass rate 0–4% for n ≤ 5, 7–20% for n = 6–7, 40–80% for n = 8–10. Strong refutation for n ≤ 7 and weaker for 8–10. n ≥ 11: untestable (null ≥ 82%).
  - One alphabet (Q3v/Q3b): K4 infeasible for n = 2..7, both rules, Vig and Beau. Null pass rate 0–8%. n = 8: the K4 solution space is too large to enumerate (undecided).
- **Status.** Mixed-alphabet Vimark is **refuted** for primers up to 7 (one alphabet) and up to 10 (ACA shape). Longer primers stay open but carry no motivation beyond the general case.

## 2026-10-27 — Iteration 19: two superimposed periodic keys under one mixed alphabet
- **Why.** Phase 1 (H-1501) killed k_i = a[i mod L1] + b[i mod L2] for all L1+L2 ≤ 24, but only with AZ/KA tableaux. K1/K2 used a keyed alphabet, so the mixed-alphabet version is the natural gap (e.g. KRYPTOS 7 + PALIMPSEST 10, 7 + ABSCISSA 8).
- **Method.** The CRT enumeration from it18 blows up here (gauge freedom), so `iterations/it19b_double_periodic_cpsat.py` uses CP-SAT, with a[0] = 0 as the gauge fix and one unknown alphabet (Vig and Beau). L1 < L2, L1+L2 ≤ 20, L2 not a multiple of L1. 5 random-ciphertext nulls each. (`it19_double_periodic_mixed.py` = the failed enumeration attempt, kept for the record.)
- **Control.** Planted 7+10 Vig with a random alphabet recovered.
- **Result.** K4 infeasible (refuted) for 63 of 108 configs, including all L1+L2 ≤ 11 and 8+10, 6+14, 5+8, 5+9, 6+7, 6+9. No config is K4-feasible while the nulls are infeasible, so no signal. Untestable (nulls feasible too): 45 configs, including the motivated **7+8 and 7+10**, and every pair with L1+L2 ≥ 15 except a few.
- **Status.** Refuted where testable; KRYPTOS+PALIMPSEST / KRYPTOS+ABSCISSA under a mixed alphabet stay crib-untestable. Full lists: scratch output summarised in this entry. Same wall as before: cribs alone cannot decide models with ≥ ~15 free key values plus a free alphabet.
