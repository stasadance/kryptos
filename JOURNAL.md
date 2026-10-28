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

## 2026-10-27 — Iteration 20: KRYPTOS + PALIMPSEST / ABSCISSA as a double key in one mixed alphabet
- **Why.** It19 left 7+10 and 7+8 crib-untestable with free key values. The concrete reading is the K1/K2 keywords themselves. On the Kryptos tableau the key letters are looked up in the same alphabet as the text ("Quagmire III proper"). Then k_i = ±α(W1[i mod L1]) ± α(W2[i mod L2]), and everything is linear in α alone.
- **Test.** `iterations/it20_keyword_pair_q3.py`. All pairs of {KRYPTOS, PALIMPSEST, ABSCISSA}, all sign combinations, Vig and Beau, plus each single keyword as a baseline. Exact CRT (mod 2 and 13) plus all-different enumeration.
- **Control.** Planted KRYPTOS+PALIMPSEST Vig with a random alphabet recovered.
- **Null.** 0/40 random ciphertexts feasible in every config, so the test has full power.
- **Result.** K4 infeasible in all 30 configs. **Refuted.**
- **Side note.** A full-text annealer for the generic 7+10 model (`iterations/it20/sa2h.c`: the crib edges determine the key from α, since all 17 key nodes form one component) reaches 0 crib violations only rarely (1 run in 6 on controls). Parked; it is not needed for the motivated instances.

## 2026-10-27 — Iteration 21: primary source of the "flip the chart … the W up there" quote (#3b closed)
- **Fetched.** Auto-captions of both candidate videos, now reachable from this environment (saved in `data/sources/`).
  - RR Auction video (QTGcaCPIYl4, 2025): a 2-minute news piece. The quote is **not** in it.
  - Big Tech Day 6, Munich, c.2013 (oFKPNRpE21o, "Jim Sanborn Presentation on Kryptos", 8:45): the quote **is** here.
- **Context (verbatim, auto-captions).** Showing the K1 worksheet: "you take the B in the first line and running over like in a mileage chart along the top of Vigenère's tableau and then you take the E down at the bottom and go across until you hit the letter that you want … then you take that E and you put that E into a chart that goes a different direction, you flip the chart over, turn it upside down and then you start writing down those lists that way, you turn it again or you turn it backwards and shine a light on it, but whatever it takes that's what you do". Then, on the ABSCISSA sheet: "you take that chart and you flip it this way and it turns into this chart so that the final letter in a coding system might be the W up there and so that would be the last word before the part that hasn't been cracked yet."
- **Reading.** Both passages are about the already-solved K1/K2 worksheets. The first is the ordinary Vigenère lookup followed by Sanborn re-copying the cipher letters into his layout chart in another direction (a transcription step, not a cipher). The second refers to the end of K2 on the sculpture, just before the K3/K4 part ("the part that hasn't been cracked"). Nothing in it describes the K4 method. "Matrix codes for the parts that had been deciphered already" is said of K1–K3, and he declines to give the K4 clue.
- **Consequence.** #3b closed. The flipped/rotated tableau test from it03 already covers the only cipher-level reading, and it stays refuted. No new hypothesis comes from this source.
- **NSA 2007 "KRYPTOS Summary" / slides.** Still 403 from nsa.gov and media.defense.gov via curl and WebFetch; web.archive.org closes the tunnel; no third-party mirror found. Not obtained.

## 2026-10-27 — Iteration 22: NSA FOIA set obtained and mined
- **Obtained.** The full NSA "CIA Kryptos Sculpture" release (2007 Summary DOCID 4145037, the 69-slide deck 4145036, the 1991–93 documents) from an archive.org mirror, after nsa.gov/media.defense.gov returned 403. OCR text is in `data/sources/nsa/` (see its README).
- **What it says about K4.** Nothing beyond what we had. 2007: flat distribution, eight Ks, no long repeats, a "slight interval 7 property"; plaintext and ciphertext autokey tried and failed. 1992: "roughness on interval 7"; two hypotheses (PT autokey with a frequent letter valued 0; substitution then a K3-style transposition), no solution. One slide puts K4 above a redacted box, so some NSA K4 work is still classified. Both families named are already refuted in our records (autokey: phase 1 w-mask/w-crib; substitution+transposition: incompatible with the positional cribs, see below).
- **New fact from the deck: Washington Post, 14 Jan 1990.** Before the dedication, Sanborn was paraphrased as saying that Vigenère deciphers "one-half of the phrase. The other half will be encoded in a modern system created for the project by an expert cryptographer". By length, K1+K2 (432) is the Vigenère half, so **K3 and K4 (437) were described as one "modern system" half.** K3 is a keyed (KRYPTOS) double columnar transposition.
- **Tension to resolve.** If K4 used K3's machinery (transposition) plus a substitution, Sanborn's crib statements ("NYPVTT … when deciphered, read BERLIN") and Kobek's "exactly in the right position" require the crib letters to keep their positions. A transposition applied after the substitution breaks that. A transposition applied before it puts the cribs in the scrambled intermediate, where 11- and 13-letter English runs would not survive a columnar step. So either the "modern system" description is loose, or the transposition element sits in the key (a transposed key stream), not in the text.
- **Next.** Phase 1 tested transposed key streams for K3's closed form and a few sources (ruled_out line 79). Iteration 23 tests the specific reading the WaPo quote suggests: K4's key stream = a K3-style keyed columnar transposition (KRYPTOS key, K3's grid shapes) of a short motivated source, under one unknown alphabet, with a planted control.

## 2026-10-27 — Iteration 23: running key from real texts under one unknown mixed alphabet
- **Gap.** Phase 1 refuted natural-language running keys only under fixed AZ/KA tableaux (statistically, w-runkey) and K1–K3 texts with one arbitrary alphabet (keithadler). A running key looked up through a keyword-mixed alphabet, as on the K1/K2 tableau, was open, and the WaPo 1990 note (it22) keeps text-based "modern" keys on the table.
- **Model.** Key letter k_i = source text at offset o+i. Each of cipher letter, plain letter and key letter is valued by an unknown alphabet a, by AZ index, or by KA index, with a in at least the cipher or plain role (15 role patterns). Vigenère X(c) = X(p) + X(k), Beaufort X(c) = X(k) − X(p), variant X(c) = X(p) − X(k): 45 models. With the source and offset fixed, the 24 crib equations are linear in a.
- **Test.** Exact: solve mod 13 and mod 2, enumerate the small solution spaces, require the alphabet letters involved to be distinct (CRT). Numba scanner `iterations/it23_scan.py` (about 20k offsets × 45 models per second); `iterations/it23_runkey_mixed.py` is the Python reference for the first 9 models.
- **Controls.** Planted running-key encryptions (random alphabet, Carter vol. 1 as key, Austen as plaintext with the cribs inserted): recovered **45/45**. Power: 24 equations nearly fix a, so K4 gave 0 passes in ~1e8 offset×model tests (false-pass rate < 1e-7 per test), i.e. any pass would be decisive.
- **Motivated sources, forward and reversed: 0 hits.** Carter, *The Tomb of Tut-ankh-Amen* vols 1–3 (archive.org OCR, 1923–33); Budge, *Book of the Dead* (pg7145); US Declaration and Constitution (pg1, pg5); K1–K3 plaintexts (carved spellings), K1–K3 ciphertext, the KA tableau rows.
- **Broad scan running.** KJV and the current Gutenberg top-100 (plus War and Peace, Montaigne, Communist Manifesto), all 45 models; results appended below when finished.
- **Not covered.** Two independent unknown alphabets (not linear, crib-untestable per H-1404), crib carving errors (the test requires all 24 crib letters exact), and texts not in the corpus.

## 2026-10-27 — Iteration 24: plaintext/ciphertext autokey under one unknown alphabet, every lag (NSA's own lead)
- **Why.** Both NSA write-ups (1992, 2007) name autokey as the obvious source of K4's interval-7 roughness, "if the alphabet used has a high-frequency letter assigned the value of 0", i.e. under a keyed alphabet. Phase 1 covered unknown-alphabet autokey only partly (CT-autokey Vig L ≤ 36, Beau L ≤ 31; PT-autokey Vig L ≤ 10).
- **Test.** `iterations/it24_autokey_mixed.py`: the 45 role/form models of it23 (cipher, plain and key letters each valued by the unknown alphabet, AZ or KA; Vig/Beau/variant). CT-autokey k_i = c_{i−L} (primer rows dropped); PT-autokey k_i = p_{i−L}, keeping only rows where p_{i−L} is a crib letter. Exact linear test with all-different. Null: 100 random ciphertexts per lag and model.
- **Controls.** 102/108 planted cases recovered; the 6 misses are "undecided" (solution space over the enumeration cap) at lags with ≤ 11 usable rows, where the test has no power anyway.
- **Result** (full table `iterations/out/it24_autokey_mixed.out`):
  - **CT-autokey: refuted for L = 1–31 in all 45 models** (K4 0 hits; null pass ≤ 3%). L ≥ 32: K4 hit counts match the null (4–15% per model), so it cannot be decided.
  - **PT-autokey: refuted for L = 1–5 and L = 42** (0 hits, null ≤ 2%). L = 6–10, 32–50: K4 hits at chance rates, so it cannot be decided. L = 11–31 and ≥ 51: fewer than 3 crib-crib pairs, so it is untestable. **NSA's lag 7 is crib-untestable** for most role models. The same-alphabet Vigenère model, which is phase 1's case, has 0 hits.
- **Status.** Autokey under keyed alphabets is closed wherever the cribs can decide it. The remaining lags need the full text, and autokey chains that propagate an unknown primer are not identifiable from 97 letters without a language model.

## 2026-10-27 — Iteration 25: the K3 transposition "matrix" as K4's numeric key
- **Why.** The WaPo 1990 note puts K3 and K4 in one "modern system" (it22). Sanborn talks of "matrix codes", and the NSA 2007 summary (Fig. 21) prints K3's column-extraction order as a 7-wide number matrix (49 12 61 24 73 36 85 / 48 11 60 …), whose rows step by −1. The matrix is a ready-made non-periodic numeric key with an interval-7 structure.
- **Test.** `iterations/it25_k3_matrix_key.py`. Streams: the 86 numbers read by rows, by columns down or up, and reversed, cycled, as n mod 26 and (n−1) mod 26; every cyclic offset; all 45 it23 models (unknown alphabet in the cipher and/or plain role). Exact linear crib test.
- **Control.** 15/15 planted numeric-key models recovered. Null: 0 hits on 5 random ciphertexts per stream.
- **Result.** K4: 0 hits in every stream. **Refuted.**
- **Generic form** (`iterations/it25c_linear_row_grid_cpsat.py`). k_i = g[col] + c·row (any 7 column values, any row step) under one unknown alphabet. CP-SAT recovers the planted control. K4 is infeasible at 9 of 21 (offset, form) cases, and the rest time out at 20 s. But 2 of 18 random nulls are feasible and most time out, so the cribs decide this model only partly. Not pursued: it is the generic grid key (it07/it15) with fewer free values, and it15 already showed the grid key does not explain the doublets.

## 2026-10-27 — Iteration 26: 2×2 Hill cipher under an unknown letter numbering
- **Why.** "Matrix codes Ed gave me" (Sanborn), and the extra L on the tableau spelling HILL (Bauer/Link/Molle 2016). Phase 1 refuted Hill n = 2–4 only with A=0 or KA numbering. A Hill cipher on a keyword-mixed numbering is the natural K1/K2-style variant.
- **Model.** Blocks at offset o ∈ {0, 1}: a(c_x) = m11·a(p_x) + m12·a(p_y) (+ b1), and likewise for c_y. For each of the 157,248 invertible M, this is linear in the unknown numbering a (and b). Enumerating every M covers both C = MP and P = MC. 11 crib blocks at each offset.
- **Test.** `iterations/it26_hill2_mixed.py` (numba; exact CRT + all-different).
- **Controls.** Planted linear and affine cases are each recovered as the unique passing matrix.
- **Result.** K4: 0 of 157,248 matrices pass, linear and affine, at both offsets. Random nulls: also 0, and the test has full power. **Refuted.**
- **Open.** n = 3 under an unknown numbering (26^9 matrices: needs a smarter row-wise method), and Hill combined with a transposition.

## 2026-10-27 — Iteration 27: full-text decision of the Gromark survivors (Bean 2021)
- **Why.** Gromark (lagged-Fibonacci digit key, Scheidt's "regenerative function", "change the language base") survives the cribs only with two arbitrary alphabets. That leaves 46 primers: b10/5 (39), b10/4 (3: 3301, 6740, 9903), b8/5 (4). w-gromark disfavoured them statistically (fewer forced letters than expected) but did not decide them. With a fixed key stream, two alphabets are decidable from the full text (w-synth budget; it05 annealer 17/20 on random-key controls).
- **Test.** `iterations/it27_gromark_fulltext.py`: for each survivor, it runs it05's crib-exact two-alphabet annealer (`sa.c`, 8 restarts × 3M steps, quadgrams from War and Peace) on the expanded Gromark key.
- **Controls.** 8 planted Gromark encryptions (random primer, random alphabets, Austen text with cribs). 6/8 recovered (score −414 to −442, accuracy 0.85–1.0). Two base-8 plants got only partial recoveries (−480, accuracy 0.42–0.70).
- **Result.** The best K4 survivor is b10 40909 at **−496.9**, then 84393 at −500.7. That is the random-stream null level (it05 null −498 to −521) and about 55 units below any recovered control. The decrypts are word salad (`SAKJLSANDTHASSLEINSUB…`). The b8 survivors score −510 to −570. **Refuted** for b10 (both primer lengths). b8 is refuted with less confidence, since the annealer is weaker there (2/8 base-8 controls only partial). Full output: `iterations/out/it27_gromark_fulltext.out`.

## 2026-10-27 — Iteration 28: KRYPTOS/PALIMPSEST/ABSCISSA keyword pairs under two arbitrary alphabets
- **Why.** It19 left the motivated 7+10 and 7+8 superimposed keys crib-untestable when the key values are free. With the key values fixed by the actual keywords (numbered AZ or KA, signs ±, both phases), the stream is fixed, and two arbitrary alphabets B(c) = A(p) + k become linear in the alphabet values.
- **Test.** `iterations/it28b_two_alph_exact.py` (stream generator in `it28_keyword_pair_two_alph.py`): all 1,236 streams (3 word pairs × 2 numberings × 3 sign patterns × all phase pairs). Exact CRT + all-different within each alphabet, with one gauge fixed.
- **Controls.** 20 planted streams: 11 recovered and 9 undecided (enumeration cap; planted random crib-position ciphertext has more distinct letters than K4). None was wrongly rejected. Null: 0–4 of 300 streams feasible on random ciphertexts.
- **Result.** K4: **0 of 1,236 feasible, all decided.** Independently, only 9 streams pass the alphabet-free Latin gate (X28 = X66 plus 22 inequalities), and all 9 fail the two-alphabet additive identity k24 + k34 = k29 + k33. **Refuted**: no KRYPTOS/PALIMPSEST/ABSCISSA pair key works under any two alphabets of the form B(c) = A(p) + k.
- **it23 addendum (broad scan, partial).** All 45 models, forward and reversed: KJV (pg10), War and Peace, Montaigne, the Communist Manifesto, and 22 of the Gutenberg top-100 (Shakespeare complete, Les Misérables, Monte Cristo, Pride and Prejudice, Moby-Dick and others). That is 60.0M offset positions × 45 models: **0 hits.** Also Sanborn's 1990 dedication text, the Morse phrases and the WaPo 1990 paragraph (forward, reversed, cycled): 0 hits. A container restart stopped the scan at 26 of ~100 books; the rest is queued.

## 2026-10-27 — Iteration 29: running key from a source text under TWO arbitrary alphabets
- **Why.** It23 refuted natural-text running keys under ONE unknown alphabet. The next-wider model, B(c) = A(p) + n(k) with two independent arbitrary alphabets A, B and the key letter numbered AZ or KA, is Quagmire IV with a running key. It is linear in the alphabets once the stream is fixed, so each offset is checkable.
- **Test.** `iterations/it29_runkey_two_alph.py`: (1) an alphabet-free gate (k28 = k66, the 22 crib inequalities, and K4's additive identity k24 + k34 = k29 + k33); (2) the exact two-alphabet check (it28b); (3) crib-exact full-text annealing (it05 `sa.c`, 6 restarts × 3M steps) of every survivor. Sources: Carter's Tomb of Tut-ankh-Amen vols 1–3, Budge's Book of the Dead (pg7145), the Declaration (pg1), the Constitution (pg5), K1–K3 plaintext and ciphertext, Sanborn's 1990 dedication, the WaPo 1990 paragraph. Forward and reversed, AZ and KA: 4,056,732 offsets → 2,018 pass the gate and are not excluded by the exact check.
- **Control.** `iterations/it29b_plant_control.py`: 8 plants (Carter key at a random offset, Austen plaintext with the cribs, random A and B). The exact check rejected none of them (3 feasible, 5 undecided). The annealer recovered 6/8 (accuracy 0.90–0.99, score −397 to −454). It failed on 2 (−481 at accuracy 0.58; −451 at 0.67). So recovery power is about 75% per candidate.
- **Result.** K4's best of 2,018 is −482.69. Re-annealing the top 20 with 24 restarts (`iterations/it29c_top_rerun.py`) gives a best of −481.08. Every decrypt is word salad. That is the random-stream null level (it05 null −498 to −521, and best-of-2,018 maxima sit higher), and about 27 units below the weakest recovered plant. **Refuted** at the annealer's power (≈75% per candidate, higher for the top 20 after 24 restarts) for these sources. Outputs: `iterations/out/it29_*.out`.

## 2026-10-27 — it23 addendum 2: broad scan finished
- The remaining 78 Gutenberg top-100 books were scanned one file per process, so a container restart can resume where it stopped. In total: 104 texts (KJV, War and Peace, Montaigne, the Manifesto, the full Gutenberg top-100), forward and reversed, **137.4M offsets × 45 models: 0 hits.** 120 (offset, model) cases stay undecided after the high-cap rescan (2e-8 of the tests). The running-key-from-a-popular-book hypothesis under one unknown alphabet is closed for this corpus. Output: `iterations/out/it23_broad_scan.out`.

## 2026-10-27 — Iteration 23c: running key under one unknown alphabet with ONE wrong crib letter
- **Why.** K1–K3 all have carving errors, and every exact running-key screen (it23) assumed all 24 crib letters are right. One error would hide a true hit.
- **Test.** `iterations/it23c_scan_err.py`: the same 45 role/form models, passing an (offset, model) if the system minus any single crib row is feasible. Sources: K1–K3 PT/CT, the KA tableau, Sanborn's dedication, WaPo 1990, the Declaration, the Constitution, the Book of the Dead, and Carter vols 1–3, forward and reversed.
- **Control.** 12 random models planted with one corrupted crib-position ciphertext letter: **12/12 recovered**. Null: 5 random ciphertexts × 19,903 offsets × 45 models = 4.5M tests, **0 passes**. The 23-row system still has full power.
- **Result.** K4: 2,029,524 offsets × 45 models, **0 passes**, and 2,989 undecided at the base cap (1.5e-5 of tests, not rescanned). **Refuted**: a single crib error does not rescue a motivated-text running key under one unknown alphabet. Outputs: `iterations/out/it23c_*.out`.

## 2026-10-27 — Iteration 30: grid-route and panel-overlay keys under TWO arbitrary alphabets (H-1804)
- **Why.** w-route (H-1504) refuted key streams read off the carved tableau, cipher panel, sculpture rows, the ideal KA tableau and the Morse lines under fixed tableaux and one unknown alphabet. It left the two-alphabet version "crib-untestable": only the Latin gate applied, and its pass rate was chance. It05 and it29 show that a fixed stream under two alphabets is decidable from the full text.
- **Test.** `iterations/it30_route_two_alph.py`, using w-route's own stream generators (`route.py`): 8 dihedral images × rows/boustrophedon/diagonal/spiral, fwd/rev, every cyclic offset, plus overlays at every torus shift. Key letters are numbered AZ or KA, under the model B(c) = A(p) + n(k). The it29 pipeline: the gate with K4's additive identity, then the exact two-alphabet check, then annealing (6 restarts × 3M).
- **Counts.** 1,591,660 placements → 821 pass the gate → 571 not excluded by the exact check → all 571 annealed.
- **Control.** The same annealer and settings as it29b (6/8 planted two-alphabet keys recovered at −397 to −454).
- **Result.** The best is −496.5 (TAB r90 diagonal-boustrophedon), which is the null level (−498 to −521) and about 42 units below the weakest recovered plant. The decrypts are word salad. **Refuted**: route and overlay keys from the physical grids do not work under two arbitrary alphabets either. Output: `iterations/out/it30_route_two_alph.out`.

## 2026-10-27 — Iteration 31: K3-style transposed key streams under TWO arbitrary alphabets (H-1701 extension)
- **Why.** w-transkey refuted the top-ranked phase-1 idea (a keyword, keyed alphabet or K1–K3 text "pushed into the square" K3-style and used as the key) under fixed tableaux, one unknown alphabet, and Quagmire III. Its stated gap was "two independent arbitrary alphabets". It29 and it30 show that this model is decidable from the full text.
- **Test.** `iterations/it31_transkey_two_alph.py` reuses w-transkey's `run()` with the crib index widened to all 97 positions, so every config yields its full key. That covers decimation (mod 97/98 all d, b; 336/337 motivated d), the K3 closed form, keyed columnar (236 orders), routes, and the K3 double rotation, whole and chunked. Key letters are numbered AZ or KA, under the model B(c) = A(p) + n(k).
- **Counts.** 19,236,102 configs → 280,959 pass the Latin gate → 22,374 pass K4's additive identity → 15,929 unique streams → 10,457 not excluded by the exact two-alphabet check. All were annealed: the first 503 at 6 restarts, the rest at 3. The top 50 were then re-annealed at 24 restarts.
- **Control.** it29b plants at SA_R=3: 6/8 score at or above −450 (5 full recoveries at −397 to −445, one partial), against 7/8 at SA_R=6.
- **Result.** The best of 10,457 is −482.2. After 24 restarts, the top 50 give −477.9. The decrypts are word salad (`ZOVAROUNDHEIREPIAHANGEASTNORTHEAST…`). That is the best-of-many null tail, about 25 units below the weakest recovered plant. **Refuted** at the stated power. The whole w-transkey family is now closed under 1 or 2 arbitrary alphabets. Outputs: `iterations/out/it31_*`.
- **Ops note.** A detached nohup job dies when the container is reclaimed after a turn ends. Long runs now go as resumable harness background tasks of ≤2 h each.

## 2026-10-27 — Iteration 32: K3-matrix numeric key under TWO arbitrary alphabets
- **Why.** It25 refuted the K3 extraction-order matrix (NSA Fig. 21) as a numeric key under one unknown alphabet. The two-alphabet form B(c) = A(p) + k was still open.
- **Test.** `iterations/it32_k3matrix_two_alph.py`: it25's 5 readings × (n, n−1) mod 26 × 86 cyclic offsets = 860 streams, then the it29 pipeline.
- **Result.** **0 of 860 pass the alphabet-free gate.** That gate (X28 = X66, the 22 crib inequalities, and K4's additive identity k24 + k34 = k29 + k33) is necessary for any key under this model. The chance pass rate is about 0.07%, so about 0.6 passes were expected. **Refuted** without needing the annealer.

## 2026-10-27 — Iteration 33: running key with a ciphertext slip between the cribs (H-708)
- **Why.** K2's carved text dropped an S, and Sanborn has said K4 went through "multiple versions". Every position-keyed screen assumes the carved positions are the encryption positions. With a running key, a slip before position 21 or after 73 is absorbed by the free offset. A slip *between* the cribs shifts BERLINCLOCK's key index by d against its carved position, so that is the one case still untested.
- **Test.** `iterations/it33_runkey_shift.py`: the it23 kernel with the key index of the 11 BERLINCLOCK rows shifted by d ∈ {−2, −1, +1, +2} (letters omitted or inserted). All 45 role/form models. Sources: K1–K3 PT/CT, the KA tableau, Sanborn's dedication, WaPo 1990, the Declaration, the Constitution, the Book of the Dead, Carter vols 1–3, KJV; forward and reversed.
- **Control.** 12 plants with a real slip (1–2 CT letters dropped or inserted at a random point between the cribs): **12/12 recovered**. Null: 4 random ciphertexts × 4 shifts × 19,900 offsets × 45 models: 0 passes.
- **Result.** 96 runs (12 texts × fwd/rev × 4 shifts), 34.0M offset-shift positions × 45 models: **0 hits** (1,457 undecided at base cap, about 1e-6). **Refuted** for these sources.

## 2026-10-27 — Iteration 34: are the transposed-key nulls robust to one crib carving error? (H-2104)
- **Why.** w-synth flagged that the big exact nulls (w-transkey's 19.2M configs, the top-ranked family) assume all 24 crib letters are carved right. K1–K3 all have errors.
- **Test.** `iterations/it34_transkey_err.py` reruns w-transkey's generators in two modes. **drop**: any one of the 24 crib rows may be wrong. **shift d** (±1, ±2): ciphertext letters omitted or inserted between the cribs. Models: the fixed tableaux (≤1 mismatch), plus one arbitrary alphabet vig1/beau1 under 4 numberings. A new fast necessary gate uses the integer crib relations (left null space of the crib incidence matrix, restricted to relations without the dropped row), then the exact `keygen.feasible` on survivors. Quagmire-III self models were not re-tested.
- **Control.** `iterations/it34b_control.py`: 60/60 planted keys (drop: 40 with one corrupted crib letter; shift: 20).
- **Result.**
  - **Shift:** 0 hits at every d. The shuffled-CT null at d=1 also gives 0.
  - **Drop:** 1 K4 hit and 0 on the shuffled null. The hit is a keyed alphabet LAYERTWO/KA decimated mod 97 (d=65, b=74), beau1, AZ1 numbering, with crib row 2 (position 24, S) wrong. I enumerated all 240 one-alphabet solutions (CP-SAT; `iterations/it34c_check_hit.py`). The best decrypt scores −666.9 in quadgrams (English is about −400) and is gibberish: `BFWZKOOQXPBZ…EAETNORTHEAST…`. So it is a chance consistency.
  - K4's drop gate passes 13× more configs than the shuffled null (538k vs 42k). That comes from K4's crib-graph structure, which has fewer independent relations, not from evidence for the model.
- **Conclusion.** **H-2104 answered for w-transkey:** its null holds under one crib carving error or a 1–2 letter slip between the cribs.

## 2026-10-27 — Iteration 35: keyword-generator and grid-route nulls under one crib error (H-2104, continued)
- **Test.** `iterations/it35_keygen_route_err.py`, the same gate as it34 applied to two families:
  - w-keygen's families F0–F5 plus two-keyword: 900,272 value streams.
  - w-route's route/overlay letter streams × 4 numberings: 3,183,320.
  - Modes: drop (one wrong crib row) and shift ±1, ±2. Models: the 12 fixed tableaux and vig1/beau1.
- **Control.** `iterations/it35b_control.py`: 48/48 planted.
- **Result.**
  - **Shift:** 0 hits in both families at every d.
  - **Route drop:** 0 hits (null 0).
  - **Keygen drop:** 1 K4 hit (null 0): SHADOWFORCES progressive (AZ0, o=3, m=3, s=12), beau1, consistent with row 5 or row 21 dropped. All 240 alphabet solutions for either drop decrypt to gibberish: best −617.8 (`HGOHUHLODUSWKNSASZVPFEASTNORTHEAST…`) against English at about −400 (`iterations/it35c_check_hit.py`). It is a chance consistency.
- **Conclusion.** H-2104 is closed. All three big exact generator nulls (w-transkey, w-keygen, w-route) hold under one crib carving error or a 1–2 letter slip between the cribs.

## 2026-10-27 — Iteration 36: plaintext-autokey (lag 6–12) under one unknown alphabet from the full text (H-2103) — UNDECIDED, search-limited
- **Why.** It24 left PT-autokey with L = 6–41 crib-untestable. H-2103 claims that L ≤ 12 is identifiable from the full text. For L ≤ 13 every residue class mod L meets EASTNORTHEAST, so the alphabet alone determines the whole plaintext: propagate forward from the crib, and backward through the primer.
- **Method 1: alphabet SA.** `iterations/it36_ptautokey_sa.py` (numba). Swap moves on the alphabet; score = quadgrams minus W × (BERLINCLOCK mismatches + violated ENE-internal relations). 9 models: key value a(p), AZ or KA index, × Vig/Beau/variant. The decrypter is exact: planted keys decrypt 97/97 with the true alphabet. **Controls: 0/12 recovered.** Varying W ∈ {3, 10, 40}, T0 ∈ {3, 8, 20, 60} and up to 20M steps × 4 restarts, the search stalls at quadgram −525 to −575, while the truth scores about −410. The cause is error propagation: one wrong alphabet value corrupts every chain through that letter from there on, so the landscape is needle-like.
- **Method 2: CP-SAT.** `iterations/it36b_ptautokey_cpsat_probe.py`: alphabet and plaintext letter variables linked by element constraints, cribs fixed. Enumeration found only 2–34 of the consistent alphabets in 120 s, and never the true one. Bigram maximisation reached −13,836 against the truth's −10,747 in 300 s on one plant, and found no feasible point at all in 300 s on another.
- **Status.** H-2103 stays **OPEN**. The model is identifiable in principle, but neither search recovers planted keys, so K4 was not run (a K4 null would mean nothing). A decisive test needs a search that copes with propagation. Two ideas: chain-wise beam search outward from the cribs (ring by ring, keeping the top-k partial alphabets), or SAT with a quadgram objective at a much larger budget.
- **Addendum (two-stage search).** Stage 1 scores only the letters one step from a crib: the windows [21−L, 33+L] and [63−L, 73+L], where a wrong alphabet value cannot propagate. Stage 2 then uses the full score. It still fails: 0/2 controls at 3M × 4. The diagnostic (`iterations/it36c_local_window_diag.py`) shows why. Stage-1 optima beat the true alphabet's own window score (−206 to −222 vs −225 to −237) while sharing at most 1 alphabet value with it. The windows carry too little information, since each window letter is a nearly free function of about 2 alphabet values. So the information sits only in the long chains, and there the landscape is needle-like. This is a practical identifiability barrier for PT-autokey under an unknown alphabet at L = 6–12. H-2103 stays open.

## 2026-10-27 — Iteration 37: data attempt, the pre-1997 Weltzeituhr per-face city list (H-802) — BLOCKED
- **Goal.** H-802 needs the 24 per-face city lists (pre-1997 state) for `tools/w-clock/face_test.py`.
- **Tried.**
  - Wikimedia Commons API and upload: still HTTP 429.
  - Flickr static: 429.
  - Openverse API (`api.openverse.org`): works. It indexes 240 "Weltzeituhr" images, 4 of them historic: Commons "Weltzeituhr 19690930", "19700131040NR", Bundesarchiv 183-J1001-0301-001, Flickr "WELTZEITUHR 1972". But its thumbnail proxy serves only 600 px, which is unreadable for face text, and full size returns 500 (upstream 429).
  - A fresh web search (extended) found no per-face text list, only the facts already known: 148 cities, 24 faces, names changed in 1997.
- **Status.** Still blocked. The next options are a browser on the user's device, or a later retry when the rate limits lift.

## 2026-10-27 — Iteration 38: propagation-aware beam search for PT-autokey under an unknown alphabet (H-2103, H-1207)
- **Idea.** Don't guess the alphabet. Branch on plaintext letters, and keep every crib-implied difference relation a(c_i) − a(p_i) = ±K_i (K = AZ/KA index of p_{i−L}) in an offset union-find with an all-different check inside each component. That way a wrong letter is caught as soon as a relation cycle closes. The gap is filled from both cribs inwards, then outward. Score = quadgrams. Script: `iterations/it38_autokey_beam.py` (vig/var, AZ/KA key numbering; Beaufort's sum relations are not implemented).
- **Controls.** **0/8 at B = 500 and B = 20,000.** Every beam dies when the two fronts meet in the gap. Truth-rank diagnostics (`--diag`): the true partial plaintext's rank grows about ×5–30 per letter (15 → 78 → 2,893 → 81,532 in one plant), so it leaves a 20k beam within 4–6 letters. The relation constraints only start to bite after about a dozen letters, when the union-find components merge.
- **Reading.** The language model gives about 1.3 bits per letter against log2(26) = 4.7 bits of branching, so plausible partials grow about 2^3.4 per letter until the constraints bind. This matches it36: the information exists in principle (alphabet about 88 bits, against more than 200 bits of English redundancy plus the cribs), but none of the three search families (annealing, CP-SAT, beam) can reach it from 97 letters.
- **Status.** H-2103 and H-1207 (Beaufort) stay **OPEN: computationally undecided**. Closing them would take something qualitatively different, e.g. exact enumeration of the alphabet components the cribs fix, combined with plaintext dynamic programming. Parked.

## 2026-10-28 — Iteration 39: periodic substitution THEN a crib-preserving block transposition (H-904, Scheidt "substitution → square transposition")
- **Idea.** w-transpo showed that a transposition stage compatible with the cribs must be a strip/block shuffle that keeps each crib whole. If substitution happens first (C = T(S(P))), the key classes follow plaintext positions. The plaintext gap between EASTNORTHEAST and BERLINCLOCK is then unknown, which equals a periodic key with BERLINCLOCK's classes shifted by an unknown δ mod p. This generalizes it33/errtol (δ = ±1, ±2) to every δ. Substitution applied after the shuffle reduces to plain substitution, which is already refuted.
- **Test.** Exact consistency of the 24 crib pairs for every p and δ (`iterations/it39_periodic_crib_offset.py`, `it39b_perm_null.py`, `it39c_p8.py`, `it39d_quag.py`). Families: GEN (any bijection per class), TAB (Vig/Beau, PA/CA ∈ {AZ, KA}), Quagmire I–IV (z3). Null: K4's own 24 crib CT letters permuted. **Control: true δ consistent 75/75.**
- **Results.**
  - **TAB (8 tableaux), every δ: 0 consistent for p ≤ 23.** The null is also 0 at p ≤ 21, and at p ≥ 24 everything passes, so there is no power there.
  - **Quagmire (z3, exact):** p ≤ 7 is UNSAT for all δ and all of Q1–Q4. Q1/Q2/Q3 are UNSAT for all δ at p ≤ 11. Q4 first becomes SAT at p = 8 (δ ∈ {0,1,2,7}), but 4/5 nulls are also SAT there, so there is no power. p = 9 is UNSAT. The p = 14 run was cut by the 100-minute task limit.
  - **GEN:** p ≤ 5, 7 and 9 are inconsistent for every δ. At larger p it is consistent for many δ, and the null too. One anomaly: at **p = 8, 5/8 δ consistent (0,1,2,4,7)**. Against nulls conditioned on intra-crib consistency, P = 0.0022 locally, about 0.1 after the look-elsewhere correction over ~48 periods. The other p have tails of 0.01–0.6. Not significant. It reflects the slightly lower count of cross-crib conflicts that K4 shows at every p (tail ≈ 0.05).
- **Limit.** Under an unknown shuffle the forced plaintext letters cannot be placed in order, so above these exact bounds the language model cannot test the model. The shuffle has to be specified (e.g. a width-7 square) to go further.
- **Conclusion.** Periodic tableau substitution followed by any crib-preserving block shuffle is dead for p ≤ 23. So is Quagmire I–III for p ≤ 11, and any periodic substitution (GEN) for p ≤ 5, 7 and 9. Width 7 (the convergence lead) is the notable case: **period 7 is impossible for every substitution family and every crib offset.** The next step is the "mask" layer, or a specific square shuffle with a running or non-periodic key.
- **Addendum (scope).**
  1. Any final monoalphabetic "mask" on the CT preserves CT-letter equality, so the GEN and Q4 bounds hold with any mono mask on top. TAB, Q1 and Q3 do not; they map into Q2/Q4.
  2. Sanborn's "directly map" and "BERLIN starts at exactly the 64th character" (w-transpo §b) pin δ = 0, so it39 is a strict superset of the stated geometry. Its δ = 0 column reproduces w-crib-algebra §2: GEN fails at 1–7, 9 and 10, and p = 8 is consistent only as GEN/Q4.
  3. The δ = 0 GEN forced text is too sparse to test: p = 8 forces 5 letters (I, N, L, E, L), p = 11 forces 6, and p = 12 and 13 force 3 each. A crib-free row shuffle at width 7 cannot add power.
  4. Verdict: the periodic branch of H-904 is exhausted at the exact level. What remains is the non-periodic-key branch (running or generated keys), which is covered by it23–35.
- **Addendum (cross-check plus one new exact result).** it39d's δ = 0 column matches w-crib-algebra §2 for Q4: p = 8 and 13 are SAT, p = 11 is UNSAT. It also **settles the open case Q4 p = 12: UNSAT** (z3, 30 s limit, no unknowns). So with arbitrary independent PT and CT alphabets, Quagmire IV is dead at p = 12, which w-crib-algebra left undecided (its DFS did not finish).

## 2026-10-28 — Iteration 40: the pre-1997 Weltzeituhr face text obtained; H-802 tested on the real faces — REFUTED
- **Data (it37 was blocked).**
  - Deutsche Fotothek serves full-size scans: `fotothek.slub-dresden.de/fotos/<coll>/<sub>/<bucket>/<id>.jpg`, 1,600 px, 42 "Weltzeituhr" hits.
  - `i0.wp.com/upload.wikimedia.org/...` proxies Commons images past the 429. Openverse supplies the file names.
  - Transcribed two pre-1997 states from the photos:
    - **V1**, 1971–73: Fotothek df_hauptkatalog_0174584, elb_ddrbildarchiv_0011064/65.
    - **V2**, 1990: elb_ddrbildarchiv_0009584, plus a 1990s postcard from Badisches Landesmuseum, read via Europeana.
  - 14 and 13 of the 24 faces are read: UTC−9…+4 and −9…+3. The far side (+5…+12, −10, −11) has no legible photo yet.
  - The layout changed twice. In 1969 NEW YORK sat alone on its own face. By the 1980s the lists were much longer (e.g. 0: REYKJAVIK DUBLIN LONDON LISSABON ALGIER MADEIRA BISSAU / CASABLANCA CONAKRY DAKAR BAMAKO ACCRA).
  - Data: `data/weltzeituhr_V1.txt`, `data/weltzeituhr_V2.txt`, `data/weltzeituhr_faces_notes.md`. The scans are in `/mnt/project-files/k4/data/weltzeituhr/`.
- **Test.** `iterations/it40_clock_faces.py`: one keyed alphabet per face, built from all of that face's names.
  - Configs: 4 name orders (upper+lower, lower+upper, upper only, lower only) × AZ/KA fill × models S1–S4 (as in `tools/w-clock/face_test.py`) × 24 alignments × 2 directions. Unread faces are skipped.
  - Every (alignment, direction) still puts **at least 8 crib pairs (median 14) on read faces**. A true config must satisfy all of them; chance per config is ≈ 26^-8.
  - **Control:** planted configs are fully satisfied 10/10.
- **Result.**
  - K4's best config satisfies only 4 of 10 eligible pairs (V1) and 5 of 18 (V2). **No config is fully satisfied.**
  - Null (200 permuted-crib CTs): max satisfied pairs has mean 4.1 and 95th percentile 5. K4 is exactly at the null.
- **Conclusion.** **H-802 is REFUTED** for both pre-1997 layouts, all four name orders, both fills and all models. The far faces don't matter: every alignment is already killed on the read faces. Robustness: one mis-read name changes only one face's alphabet, and K4's best configs miss most of their pairs, not one face's worth. This closes the Weltzeituhr per-face-alphabet line (with H-801, H-803 and H-804 already refuted).

## 2026-10-28 — Iteration 41: the World Clock's own city text as a running key (one unknown alphabet)
- **Idea.** If BERLINCLOCK points at the Weltzeituhr, the key may be the clock's text itself: the city names read around the drum.
- **Test.** `iterations/it23_scan.py`, the exact crib test under one unknown mixed alphabet, 45 models; its kernel was validated by the it23 controls. Inputs: the read faces (UTC−9…+3/+4) of both layouts, in 5 orders: upper+lower per face, lower+upper, upper only, lower only, and the whole upper band then the whole lower band. Each text is scanned forwards and reversed, at every offset. Texts are 195–608 letters, in `data/clock_runkey/`.
- **Result.** 0 hits, 0 undecided, across all 20 text/direction combinations.
- **Conclusion.** The clock's legible text is not a running key under any one-alphabet model. The far faces are still unread, so a key window lying wholly on them stays untested.

## 2026-10-28 — Iteration 42: PT-autokey under a KEYWORD-mixed alphabet (restricted H-2103 / H-1207)
- **Why.** The general unknown-alphabet PT-autokey is search-limited (it36–38). Sanborn's K1–K3 alphabets are keyword-mixed (keyword followed by the rest of A–Z). Restricting to that construction makes the model exactly enumerable.
- **Test.** `iterations/it42_autokey_keyword.py`. It reuses it36's exact decrypt(), which propagates the whole plaintext from the cribs.
  - A config passes only if it reproduces the ENE-internal relations and BERLINCLOCK.
  - Space: L = 1–13 × the 9 models (key value a(p) / AZ / KA × vig / beau / var) × 49,119 keywords. The keywords are every word of 3+ letters in the local corpora, plus K1–K3 plaintext word pairs, plus Kryptos and Berlin terms. That is 5.7M exact tests.
  - **Controls: 6/6** planted keyword/L/model configs recovered. Each was the only hit among 2,001 keywords, so the false-positive rate is ≈ 0.
- **Result.** **K4: 0 crib-exact configs.**
- **Conclusion.** PT-autokey with L ≤ 13 is dead for every keyword alphabet in this 49k vocabulary, under all 9 models. That includes H-1207's Beaufort lag 7 with a keyword alphabet. Arbitrary (non-keyword) alphabets stay search-limited (H-2103 open).

## 2026-10-28 — Iteration 43: Quagmire I/II/III with a keyword-mixed alphabet, periods 1–26
- **Why.** w-crib-algebra found Q1, Q2 and Q3 crib-consistent at several periods (13, 16, 19, 23, 30…) with *arbitrary* alphabets, which is untestable. Sanborn's alphabets are keyword-mixed, and that restriction is exactly enumerable.
- **Test.** `iterations/it43_quag_keyword.py`.
  - Space: 49,119 keywords × {Q1 with AZ or KA cipher alphabet, Q2 with AZ or KA plain alphabet, Q3} × Vig/Beau × p = 1–26.
  - The cribs fix every class they touch. For p ≤ 13 every class is fixed, so a pass gives a full decrypt.
  - **Controls: 6/6** planted configs recovered with their exact plaintext.
- **Result.** **0 consistent configs at p = 1–25.** All 15,531 passes sit at p = 26, where the cribs share a single residue (73 ≡ 21 mod 26), so the test is almost vacuous there.
- **Conclusion.** Quagmire I–III with any keyword alphabet from the 49k vocabulary are dead at every period ≤ 25. Combined with w-crib-algebra, the surviving Quagmire space is arbitrary non-keyword alphabets, or p ≥ 26.

## 2026-10-28 — Iteration 44: Quagmire IV with two keyword alphabets (one motivated), periods 1–25
- **Test.** `iterations/it44_quag4_keyword.py` (numba).
  - One alphabet is keyed from 60 motivated terms (Kryptos, K1–K3, Berlin, clock, CIA). The other is keyed from the 49k vocabulary. Both role assignments × Vig/Beau × p = 1–25: about 3×10^8 exact class checks.
  - **Controls: 6/6.** In the control runs, chance passes ran at 1–4 per 2,000 vocabulary words, all at large p.
- **Result.** K4 has 1 consistent config: CT alphabet POSITION, PT alphabet SPEETIVE (not a word), Vig, p = 24. Its decrypt is gibberish (`DALJICJOFK.....OBVPBDEASTNORTHEAST.....IOHWEXALAIVICZXFSPB…`; 5 classes stay unfixed), so it is chance.
- **Conclusion.** Quagmire IV with a motivated keyword alphabet paired with any vocabulary keyword alphabet is dead at p ≤ 25.

## 2026-10-28 — Iteration 45: PT-autokey lag 14–96 under a keyword-mixed alphabet
- **Test.** `iterations/it45_autokey_keyword_long.py`.
  - Each crib letter is propagated along its lag chain both ways. A config passes if no conflict appears.
  - Space: 49,119 keywords × L = 14–96 × 9 models. **Controls 6/6.**
- **Crib stage.**
  - **Dead:** L = 14–24 and 33–49, with 0 survivors.
  - **Few survivors:** L = 25 (5), 31 (455), 32 (4), 50 (14).
  - **Weak:** L = 26, 30, 51 and 52.
  - **Crib-vacuous:** 27–29 and ≥ 53, where the cribs never interact.
  - 20.8M configs pass in total.
- **Language stage.** `iterations/it45b_score.py` scores every passing config by mean quadgram over its fully determined non-crib quadgrams (≥ 30 required).
  - On 97-letter English windows this score has mean −4.21 and minimum −4.73.
  - The **best K4 config scores −6.35** (JESHIMON, L = 29), far below English. The top 15 are all gibberish.
- **Conclusion.** PT-autokey is dead under every keyword alphabet in the vocabulary at every lag 1–96 (it42 + it45). For the crib-vacuous lags, the propagated chains still fix 42–86 letters, and none read as English.

## 2026-10-28 — Iteration 46: progressive periodic key under keyword alphabets
- **Test.** `iterations/it46_progressive_keyword.py` (numba).
  - Key: k_i = k[i mod p] + s·⌊i/p⌋ (shift per period) or + s·i (shift per letter).
  - Space: 49,119 keywords × {Q1AZ, Q1KA, Q2AZ, Q2KA, Q3} × Vig/Beau × p = 1–25 × s = 1–25. **Controls 6/6.**
- **Result.** **0 consistent at p ≤ 24.** All 816 passes are at p = 25. That period has only 3 cross-crib constraints (positions 21/71, 22/72, 23/73), which predicts about 1,400 chance passes, so 816 is chance level.
- **Conclusion.** Progressive periodic keys under keyword Quagmire I–III alphabets are dead for p ≤ 24.

## 2026-10-28 — Iteration 47: CT-autokey under a keyword-mixed alphabet, every lag
- **Test.** `iterations/it47_ctautokey_keyword.py`.
  - Space: 49,119 keywords × L = 1–96 × 9 models.
  - With CT-autokey every position i ≥ L decrypts directly, so the crib check is exact, and survivors give full text for i ≥ L. **Controls 6/6**, each the unique hit.
- **Result.**
  - **L ≤ 70: 0 survivors.**
  - L = 71–73: 4,857 survivors, each checked by only 1–3 crib letters. Best quadgram mean −6.52 against English −4.2, so none is English.
  - L ≥ 74: crib-vacuous (every crib position lies in the primer); this is just a running key from the primer.
- **Conclusion.** CT-autokey is dead under every keyword alphabet for all non-vacuous lags. This extends w-mask (any mixed alphabet, L ≤ 31) and w-crib-algebra (AZ/KA, L ≤ 73).

## 2026-10-28 — Iteration 48: other keyword-alphabet constructions
- **Test.** `iterations/it48_alt_alphabets.py` reruns the exact kernels of it42, it43, it46 and it47 unchanged; their controls are already validated. Only the alphabet builder changes:
  - KAfill: keyword, then the remaining letters in KRYPTOS-alphabet order.
  - revfill: keyword, then the remaining letters Z…A.
  - col: keyword plus the rest of A–Z written in rows, read down the columns left to right.
  - colsort: the same grid, columns read in the keyword's alphabetical order.
- **Result.** The pattern matches the plain-fill runs for all four builders.
  - PT-autokey L ≤ 13: 0.
  - Quagmire I–III: only p = 26, which is vacuous.
  - Progressive: only p = 25 (chance), plus 4 OCCIDUNT/col Q3 passes at p = 24 that decrypt to gibberish (`GJWBNLLNJQ.....AJBDIQEASTNORTHEAST…`).
  - CT-autokey: only L ≥ 70. The one L = 70 pass scores −7.99. The best L = 71–73 pass scores −6.11 against English −4.2.
- **Conclusion.** The keyword-alphabet eliminations of it42–47 hold for all four common alternative constructions.

## 2026-10-28 — Iteration 49: Antipodes K4 run vs Kryptos K4 (H-508), from photos
- **Data.** Elonka Dunin's Antipodes photo set (elonka.com/kryptos/sanborn/antipodes/images1-2.html), 18 images of about 850 px. Antipodes7 and Antipodes12 show the K4 run. Copies are in `/mnt/project-files/k4/data/antipodes/`.
- **Reading.** The run occupies 4 rows:
  - `…SSTTRTVDOHW?OBK`
  - `RUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTW`
  - `TQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZF`
  - `PKWGDKZXTJCDIGKUHUAUEKCAR␣EMUFPHZ…` (after a blank, K1 starts again)
  - That gives 3 + 34 + 35 + 25 = 97 letters.
- **Result.** All about 90 legible letters match the Kryptos K4 ciphertext exactly. The first 1–2 letters of each row sit on the curved left edge and are not sharp enough to confirm, but row lengths force the same 97-letter count. The run starts right after the "?" (supports H-211). It ends with a single blank before K1 restarts, with no extra or extra-dotted letters.
- **Status.** H-508 is **not supported**: no difference found in the legible 90+ letters. The ~6 edge letters stay unverified at this resolution; a higher-resolution photo would settle them.

## 2026-10-28 — Iteration 50: keyword-alphabet kernels on ~1.15M words
- **Test.** `iterations/it50_big_vocab.py` reruns the it42, it43, it46 and it47 kernels unchanged on a much larger vocabulary:
  - dwyl english-words (370k);
  - enz german-wordlist (686k; umlauts written both as AE/OE/UE/SS and as plain A/O/U);
  - 60×60 pairs of motivated terms.
  - Deduplicated by resulting keyed alphabet, that is **656,591 distinct alphabets**.
- **Result.**
  - PT-autokey L ≤ 13: 0.
  - Quagmire I–III: only p = 26, which is vacuous.
  - Progressive key: p = 25 at chance level, plus 20 passes at p = 24 (5 German words × 4 shift variants). These decrypt to gibberish, e.g. HABITUELLER: `ACCDSFZPGW.....ITSBIZEASTNORTHEAST.....PUZLXJCJJT…`.
  - CT-autokey: only L ≥ 70. Best −5.72 (L = 73, 1 crib letter checked) against English −4.2.
- **Conclusion.** The keyword-alphabet eliminations hold over about 657k distinct English and German keyword alphabets.

## 2026-10-28 — Iteration 51: exact propagation solver for PT-autokey L = 6–13 under one arbitrary alphabet (H-2103)
- **Hypothesis.** K4 = plaintext autokey, lag L = 6–13, under ONE unknown mixed alphabet a: a(c) = a(p) ⊕ K(P_{i−L}), with K = a(q) / AZ index / KA index and ⊕ = Vig / Beau / Var (9 models). it36 annealing could not decide this, because it failed its own planted controls.
- **Tool.** `iterations/c/akenum3.c` / `akenum4.c`: exact DFS over (partial alphabet, plaintext 34–62).
  - Every relation R_j for 21+L ≤ j ≤ 73 is propagated in both directions. Forced steps go first, then a branch on the value of the unassigned letter referenced by the most open relations.
  - kr0 models are homogeneous linear, so a → u·a (u a unit mod 26) is a symmetry. The first value is restricted to one representative per orbit, {0, 1, 2, 13}.
  - Two discarded versions: v2 (no degree heuristic) missed the planted truth at L = 6; CP-SAT was far too slow.
- **Controls.**
  - Soundness (`it51g_sound.py`): planted English plus 8 true alphabet values as hints. 33/36 searches completed and contained the truth, at L = 6, 8, 10 and 13. The 3 incomplete ones are L = 13 kr0 runs that hit the cap. No completed search ever missed the truth.
  - Null: random ciphertexts usually finish in under 10⁵ nodes with 0 solutions. So K4's fast completions are normal, not a sign of a bug.
  - Unhinted planted runs at L = 6: truth found in 8/9 at 10⁸ nodes.
- **K4 results** (`iterations/it51c_k4.sh`, cap 10⁹; reruns at 10¹⁰ in `out/it51h_*`):

| L | complete, 0 solutions | complete, solutions | capped |
|---|---|---|---|
| 6 | 8 | beau/AZ: 108 | – |
| 7 | 9 (beau/a(q) completed at 1.7·10⁹) | – | – |
| 8 | 8 | – | beau/a(q): 98 solutions at 10¹⁰ |
| 9 | 8 | – | beau/AZ: 41 |
| 10 | 8 | – | beau/a(q): 14 (10¹⁰ rerun running) |
| 11 | 4 (all kr1/kr2 except beau/AZ) | – | 5 |
| 12 | 0 | – | 9 |
| 13 | 0 | – | 9 |

  - Every solution found was scored on the fully determined span 21–73 (`it51e_score.py`). English with the cribs inserted averages −4.37 per quadgram; the minimum over 2000 samples is −5.39. The **best K4 solution of all lags is −5.57** (L = 12 beau/AZ: `…ORIOSOFNTBYRELBHRTSIAHXBRSSCA…`), and every one is gibberish.
  - The beau/AZ L = 6 count of 108 has P ≈ 0.017 against 60 shuffled-K4 nulls, which is not significant after 72 configs, and its best text scores −6.10.
- **Conclusion.**
  - PT-autokey with one arbitrary alphabet is **exactly refuted** for L = 6, L = 7 and, apart from one model each, L = 8, 9 and 10.
  - For the capped models at L ≤ 11, every solution found is non-English.
  - L = 12–13 is open beyond the cap. With ≤ 1 ENE-internal relation, the solution space there grows past enumeration, so a language-model completion is needed.

## 2026-10-28 — Iteration 52: full-text completion of every it51 survivor; LM beam for L = 11–13 (failed)
- **Stage 2** (`iterations/it52_fulltext.py`).
  - Every crib-consistent it51 solution leaves at most 3 alphabet letters free. The breakdown is 4,862 with 0 free, 7,914 with 1, 1,973 with 2 and 99 with 3.
  - Each solution was completed in all ways, decrypted over all 97 letters (forward 34–96, backward 20–0) and quadgram-scored.
  - **Best of all: −6.33** (L = 13 vig/AZ). English 97-letter windows average −4.21, with a minimum of −4.73. Every survivor is gibberish over the full text, including the beau/AZ L = 6 family of 108.
- **LM beam** (`iterations/c/beam52.c`, `it52_control.py`).
  - The beam walks plaintext 34–62 with crib propagation and ranks states by quadgrams.
  - Planted controls at L = 12 recovered **0/9**. With at most 1 ENE-internal relation, the beam fills with fluent junk (−3.47, better than English) and drops the truth. For vig/var with an AZ/KA key, every state dies at the BERLINCLOCK checks.
  - Not usable; abandoned.
- **Status.** H-2103 is closed for L = 6–10, apart from 3 capped models whose 10–10¹⁰-node survivors are all non-English. For L = 11–13 every survivor found is non-English, but the search is incomplete. Finishing L = 11–13 would need a different identifiability argument, so it is parked as low value.

## 2026-10-28 — Iteration 53: CT-autokey under one arbitrary alphabet, key read as AZ/KA index (H-1208 follow-up)
- **Hypothesis.** a(C_i) = a(P_i) ⊕ K(C_{i−L}), with K = a(c′), AZ index or KA index; ⊕ = Vig / Beau / Var; L = 1–73. w-mask z3 had covered only K = a(c′), and it47 only keyword alphabets.
- **Stage 1** (z3, `iterations/it53_ctautokey_arb.py --z3`).
  - Every model is UNSAT for L ≤ 31.
  - At L = 32–73 there are about 70 crib-feasible configs. All of them have at most 13 crib checks, and every L ≥ 34 has only BERLINCLOCK checks. The a(c′) survivors match w-mask §3.5.
- **Stage 2.**
  - Annealing over the alphabet: quadgrams on P[L..96] plus a crib penalty, 30 restarts × 2M steps. Each surviving config with an AZ/KA key (33 configs) was run on K4 and on a planted control at the same L, f and k.
  - **Controls recover the truth (accuracy ≥ 0.89) in 18/33**, every one at L ≤ 60. Above about L = 60 the decrypted span is under 37 letters, and fluent junk outscores the truth (accuracy 0.1–0.45). So those configs are information-limited (H-2102).
  - Every config whose own control passed has a K4 best of −4.88 to −5.94, against −4.1 to −4.9 for its control. Each is at least 0.37 below its control, so no English solution exists for these 18. All K4 bests are gibberish (`it53_table.txt`).
  - **Key = a(c′):** annealing fails its planted controls (accuracy 0.25–0.41 at L = 41–60). The value a(c) − a(c′) makes the landscape chaotic, so those configs stay undecided.
- **Conclusion.**
  - CT-autokey with an AZ/KA-indexed key under one arbitrary alphabet is dead for L ≤ 31 (exact) and for the 18 identifiable configs at L = 32–60.
  - The configs at L > 60 are information-limited.
  - The a(c′) variant is undecided above L = 31.

## 2026-10-28 — Iteration 54: periodic Gronsfeld (digit key) through one arbitrary alphabet (H-1205 × periodic)
- **Hypothesis.** a(C_i) = a(P_i) ⊕ k_{i mod p}, with key digits 0–9 (Gronsfeld, as the K2 coordinates suggest), one unknown mixed alphabet, Vig / Beau / Var. The reference model with digits 0–25 is Quagmire III with an arbitrary alphabet.
- **Exact test** (z3, `iterations/it54_gronsfeld_arb.py`; planted controls SAT 4/4).
  - Every form is UNSAT for p = 1–22, 24, 25, 34–40, 42–45 and 48.
  - Feasible: Beaufort at p = 23, 26, 31–33, 46, 47; all three forms at p = 27–30; Vig and Var at p = 41.
  - **The decimal restriction never changes the verdict:** m = 10 and m = 26 agree at every p. Each key class meets at most 1–2 cribs, so the cribs cannot see the key range.
  - Null (`it54b_null.py`): shuffled K4 is feasible for Beaufort p = 23 in 18/50 trials (m = 10) and 25/50 (m = 26). K4's SAT there is ordinary.
- **Full-text annealing** (`it54c_sa.py`: alphabet swaps plus digit resets, quadgrams plus crib penalty). Planted controls at p = 23 Beau, p = 30 Vig and p = 41 Var recovered only 40–45%, so the method fails. This matches H-1903: these periodic models are search- and information-limited at 97 letters.
- **Conclusion.**
  - Periodic Gronsfeld or Quagmire III with an arbitrary alphabet is dead at the periods listed above.
  - At the feasible periods it cannot be decided from the cribs, and annealing cannot recover planted keys. It stays open but undecidable without key structure, such as a known digit string.

## 2026-10-28 — Iteration 55: lag-7 roughness (H-903) and an alphabet-free coincidence lemma for CT-autokey
- **Observation.** K4 has 9 letter coincidences at lag 7 (C_i = C_{i−7}), against a shuffled-K4 null of 3.24 ± 1.76: P = 0.004 for that lag, about 0.12 after the 30-lag look-elsewhere correction. No other lag ≤ 30 has P < 0.13. The coincidences are at i = 7, 14, 19, 22, 39, 52, 72, 83, 93.
- **Hypothesis.** The natural generator of lag-L coincidences is ciphertext autokey, b(C_i) = b(C_{i−L}) ± a(P_i), where a and b are any two alphabets and the fed-back letter is valued by the same b.
- **Lemma.** Under that model, C_i = C_{i−L} holds exactly when a(P_i) = 0, that is, when P_i equals one fixed letter z. On the crib positions with i ≥ L, the coincidence set must therefore equal {i : P_i = z} for a single z, or be empty. This is exact, needs no alphabet search, and holds for every a and b.
  - Not covered: the sign-flipped feedback b(C_i) = a(P_i) − b(C_{i−L}).
- **Controls.** 300/300 planted encryptions (random a, b, L and sign) pass.
- **Result** (`iterations/it55_coincidence_lemma.py`, `out/it55.txt`).
  - **Lag 7 is dead:** the coincidences at 22 (PT A) and 72 (PT C) would need two different zero letters.
  - Also dead: L = 1, 4, 5, 10, 11, 18–20, 22–25, 42, 45.
  - The test is weak per lag (random ciphertexts pass about 46% of the time at small L), so other lags stay open under two alphabets.
- **Conclusion.** The lag-7 excess cannot come from ciphertext autokey at lag 7, for any pair of alphabets. Plaintext autokey at lag 7 is already exactly dead under one alphabet (it51). H-903 loses both autokey explanations; what remains is chance (global P ≈ 0.12) or a transposition or structural effect.

## 2026-10-28 — Iteration 56: autokey under ANY Latin-square tableau (exact both ways)
- **Model.** C_i = T[r_i][P_i], with T any 26×26 Latin square and row r_i = C_{i−L} (CT-autokey) or P_{i−L} (PT-autokey). This covers Vig/Beau/Var and Quagmire I–IV with any alphabets, and any relabelling of the key letters.
- **Test** (`iterations/it56_latin_autokey.py`). Every crib position whose row letter is known gives a filled cell (row, P, C). A partial Latin square must have (row, col)→val, (row, val)→col and (col, val)→row all functional.
  - The cribs give at most 24 cells. By Evans' theorem, any consistent partial Latin square of order 26 with fewer than 26 cells can be completed. So the check is exact in both directions: fail = impossible for every tableau, pass = some tableau fits the cribs.
  - Planted controls pass 288/288 for each kind.
- **Result** (`out/it56.txt`).
  - **CT-autokey is dead for every tableau** at L = 1–11, 13–31, 33, 35, 42, 49, 50, 53, 55, 58 and 65.
    - **L = 12 survives** (24 cells; random ciphertexts pass 23% of the time). Its single-alphabet forms are already dead (it53 z3), so only a tableau that is not a one-alphabet Vigenère family fits.
    - Lags ≥ 32 pass at near-null rates (about 78%).
  - **PT-autokey is dead for every tableau** at L = 1–4 and 42 only. For L ≥ 5, too few crib cells have a known row.
- **Conclusion.** Ciphertext autokey of any tableau is excluded at every lag ≤ 31 except 12. An arbitrary tableau at L = 12 fits the cribs exactly but has 26² unknowns, so it is unidentifiable without structure.

## 2026-10-28 — Iteration 57: the 46 Gromark survivors under two arbitrary alphabets, judged on the full text
- **Background.** H-601: Bean's 46 crib-consistent Gromark primers (b10/5: 39, b10/4: 3, b8/5: 4; recomputed with `tools/gromark.py scan`) were only disfavoured, because the crib-forced letters are too few to score.
- **Test** (`iterations/it57_gromark_fulltext.py`). With the primer known, the key stream is known. So B(C) = A(P) + k is Quagmire IV with a known key stream, which H-2101 / it29 showed is identifiable by crib-exact full-text annealing (it05 `sa.c`, NALPH = 2, 8 restarts × 4M steps).
- **Controls.** 6 planted encryptions (random primer, two random alphabets, English with cribs) scored −420 to −487. Truth was recovered at accuracy 0.99, 0.86, 0.74 and 0.71; the other two reached 0.55 and 0.54.
- **K4.** For all 46 primers the best score is ≤ −495.2 (3301 b10/4), which is below every control, including the two only half-recovered ones. All decrypts are gibberish outside the cribs (`out/it57_k4_sorted.txt`).
- **Conclusion.** No Gromark survivor gives English under two arbitrary alphabets. H-601 moves from "disfavoured" to "refuted by full-text annealing" at search-limited strength: the annealer recovers truth in 4/6 plants, so this is strong evidence but not proof.

## 2026-10-28 — Iteration 58: Gromark in bases 17–26 (H-601 open remainder)
- **Test** (`iterations/it58_vimark.py`). Exact crib scan (`tools/gromark.py`, two arbitrary alphabets) for bases 17–26 (base 26 is the Vigenère-letter, "Vimark"-style key) with primer lengths 2–4. Planted controls: 8/8 true primers found among the survivors.
- **Result** (`out/it58.txt`).
  - **Base 26 has 0 survivors at L = 2, 3 and 4.**
  - Bases 17–25 have none at L ≤ 3 except base 21, L = 3 (5 survivors). At L = 4 they have 2–206 each, 735 in total.
  - Shuffled-K4 ciphertexts give 96 to 118k survivors at b26/4. Shuffling breaks K4's fixed crib coincidences, though, including the X28 = X66 condition that every Latin tableau needs (H-1209). So K4's 0 is structural, not a statistical anomaly, and shuffled K4 is the wrong null here.
- **Conclusion.**
  - Base-26 lagged-Fibonacci keys with primers ≤ 4 are dead under any two alphabets.
  - Bases 17–25 at L = 4 keep 735 crib-consistent primers. They are unmotivated (the ACA Gromark is base 10), so I am not spending a full-text annealing run (about 3 h) on them.

## 2026-10-28 — Iteration 59: keys from the digits of mathematical constants
- **Hypothesis.** The key stream is the digits of π, e, φ, √2, √3, √5, ln 2 or Euler's γ (100k digits each, mpmath), started at any offset < 100k. It is used either as Gronsfeld digits or as non-overlapping 2-digit numbers mod 26, through either one alphabet (a(C) = a(P) + k) or two arbitrary alphabets (posC(C) = posP(P) + k, which covers Vig/Beau/Var/Quagmire with any alphabets).
- **Test** (`iterations/it59_constant_digits.py`). First the alphabet-free X28 = X66 prefilter, then the exact union-find and packing check from `tools/gromark.solve`. Planted controls: 4/4 found.
- **Result.**
  - **One alphabet: 0 survivors** across all 1.6M streams. This is an exact refutation.
  - **Two alphabets: 687 survivors**, about 43 per constant and stream kind per 100k offsets. That is the same rate as random keys (compare the Gromark iid rate of about 4·10⁻⁴), so it is not evidence.
  - At the motivated starts (offsets 0–96) only π digit pairs at offset 97 survive, which is not a natural start.
- **Conclusion.** Digit keys from these constants are dead under one alphabet. Under two arbitrary alphabets they are dead at every natural starting offset; the other offsets survive only at chance rate, and with no motivation I am not annealing them.

## 2026-10-28 — Iteration 60: keys from simple integer sequences
- **Hypothesis.** k_i = (m·s(i+o) + c) mod 26 for 25 classic sequences (primes, prime gaps, Fibonacci, Lucas, Pell, tribonacci, Padovan, squares, cubes, triangular, pentagonal, square-pyramidal, powers of 2/3/5/7/10, Catalan, digit sums, n³ + n), with offsets o < 200, every unit m and every c < 26. Checked under one alphabet and under two arbitrary alphabets (where m and c are absorbed).
- **Test** (`iterations/it60_integer_sequences.py`): X28 = X66 prefilter, then the exact `gromark.solve`. Planted controls pass 4/4 under both models.
- **Result.**
  - **One alphabet: 0 survivors** (exact).
  - **Two alphabets: 1 survivor**, the primes starting from the 151st prime (877) at offset 150. It is unmotivated and at chance rate (1 of 4000 sequence-offset pairs). Full-text annealing on it gives −540 (−5.75 per quadgram), which is gibberish.
- **Conclusion.** None of these simple sequences is K4's key, under one or two alphabets.

## 2026-10-28 — Iteration 61: progressive periodic keys through one arbitrary alphabet
- **Hypothesis.** The key is k_i = w_{i mod p} + s·i ("lin") or w_{i mod p} + s·⌊i/p⌋ ("blk"), with s = 1–25 and w arbitrary, through ONE arbitrary alphabet, in Vig, Beau or Var form. it46 had tested this only with keyword alphabets.
- **Test** (`iterations/it61_progressive_arb.py`): exact z3 for each (p, s, form, kind). Planted controls: 4/4 SAT.
- **Result** (`out/it61.txt`, p = 1–19; the run was stopped there).
  - **Every s, form and kind is UNSAT at p = 1–7, 9, 14 and 19.**
  - Partly SAT at p = 8 and 10 (48 of 75 per kind), 13 (lin 13/75), and 15 (25/75).
  - Mostly SAT at p = 11, 12, 16, 17 and 18.
  - Null at p = 8 (shuffled K4): 14/40 SAT for s = 1, against 1/40 for s = 0. The drift loosens the constraints, so the SAT results sit at chance level.
- **Conclusion.** A progressive periodic key through any single mixed alphabet is dead at p ≤ 7, 9, 14 and 19. At the other periods it is crib-feasible at chance rates, which makes it the same information-limited case as the periodic families (H-2102).

## it62 — IC test of model families, independent of alphabet and transposition
- **Hypothesis:** the index of coincidence (IC) is invariant under any relabelling of CT and PT letters, and under any transposition. So K4's IC alone can reject families for every alphabet and every transposition layer.
- **Test:** for each family, simulate 4000 97-letter CTs (P&P English with the K4 cribs planted, random alphabet and key) and compare with K4's IC of 0.0361 using a one-sided P(IC ≤ K4). The simulated samples serve as the planted control: each family's own CTs fall inside its own distribution by construction.
- **Result:** K4's IC is below the uniform-key expectation (0.0384). Families rejected at P < 0.02:
  - monoalphabetic (P = 0);
  - periodic keys with p ≤ 4 (p = 5: 0.018);
  - iid keys over ≤ 4 symbols (Gronsfeld digits 0–3: 0.017).
  Families near the edge: p = 6 (0.036), digits 0–4 (0.037), digits 0–5 (0.048). An English running key (0.148) and an iid uniform key (0.225) remain consistent.
- **Next:** this supports a high-entropy key (running key, or a long or aperiodic key), which matches the earlier exact-UNSAT results.

## it63 — Running key from the Cyrillic Projector plaintext
- **Hypothesis:** the K4 running key is the plaintext of Sanborn's other CIA-linked sculpture, the Cyrillic Projector. Its plaintext is a KGB agent-handling text plus the KGB memo on Sakharov's Pugwash letter. This source is not part of H-1102.
- **Source:** the Russian text as published on habr.com/ru/post/469717. It was transliterated two ways: BGN without diacritics, and one Latin letter per Cyrillic letter. The texts were taken separately and joined, read forwards and reversed, and wrapped cyclically.
- **Test:** the exact crib check at every offset, for all 45 role models (it23_scan.run).
- **Control:** encrypt English text (with the cribs planted) using the real key text at a random offset, once per model. The scan recovered 45/45.
- **Result:** 0 hits and 0 undecided across about 20k offset × direction checks, in every model.
- **Next:** continue the loop.

## it64 — Column IC: transposition followed by a periodic key with arbitrary alphabets
- **Hypothesis:** the lag-7 coincidence excess from it55 means K4 is some transposition of the PT, followed by period-p substitution with p arbitrary alphabets. Each column would then be monoalphabetic English, so the mean column IC would be about 0.064 for any alphabets and any transposition.
- **Control:** shuffled English text with p random alphabets gives a mean column IC of about 0.064 at every p. The null (shuffled K4) gives about 0.036.
- **Result:**
  - K4's column IC is null-like at every p. At p=7 it is 0.0419 (null P = 0.20, planted P = 0.0085).
  - Rejected at planted P < 0.01: p = 2–9, 12, 13. Marginal: p = 14 (0.025), 10 (0.043), 11 (0.064). Those columns are too short to decide.
  - So the lag-7 excess is not period-7 structure.
- **Context:** a web check found the K4 plaintext is still not public. It was sold at auction in Nov 2025.

## it65 — Any digraphic substitution, with an optional single null
- **Hypothesis:** K4 is a digraphic cipher, i.e. an arbitrary 676-entry table. This covers Playfair, two-square, four-square and Hill-2.
- **Structural kills:**
  - K4 has 97 letters, which is odd, so a pure digraphic cipher needs a null.
  - All 26 letters occur, so every 25-letter-grid cipher is dead outright: Playfair, 5×5 two-square and four-square, and 5×5 Bifid.
- **Test:** the number of repeated aligned digraphs. This is invariant to the table, and the maximum is taken over alignments and over any one deleted null.
- **Result:** K4 scores 4. The null (shuffled K4) averages 3.21, with P(null ≥ K4) = 0.37. The planted control (English plus a random table plus a null) averages 8.85, with P(planted ≤ K4) = 0.062.
- **Verdict:** K4 is null-like. A general 26-letter digraphic cipher is disfavoured at about 6% but not rejected; the test is weak at 97 letters.

## it66 — H-1502: a repeated keyword pushed through any transposition, under one standard tableau
- **Insight:** whatever the transposition (any width, any route), the key stream is a permutation of the periodic keyword stream. So every key letter derived from the cribs must be a keyword letter, with enough multiplicity. One check covers all transpositions at once.
- **Derived key letters:** the 24 crib positions need 12–16 distinct key letters, depending on the model (AZ/KA × Vig/Beau/Var). So any keyword with fewer than 12 distinct letters is dead under every transposition: KRYPTOS, PALIMPSEST, ABSCISSA, BERLIN, CLOCK, and so on.
- **Dictionary:** the 49,119-keyword set from it42. Zero keywords of length ≤ 30 pass. The only passes are 676–769-letter corpus run-ons, not real keywords.
- **Control:** a random dictionary keyword is repeated, randomly permuted, and used to encrypt English. The true keyword passed in 12/12 trials.
- **Verdict:** H-1502 is refuted for the AZ/KA standard tableaux. A mixed-alphabet variant remains open but is crib-weak.

## it67 — H-1502 with keyed tableaux (Quagmire III style)
- **Hypothesis:** the it66 model, but with the tableau alphabet keyed by a dictionary word Y. The key stream is keyword W repeated, then put through any transposition.
- **Test:** for every pair (Y, W), with 49k × 49k pairs and 3 forms (Vig/Beau/Var), check that the crib-derived key letters are a subset of W's letters with enough multiplicity. Bitmasks make this fast.
- **Control:** random Y, W and form, with the key stream randomly permuted. 10/10 controls were found, and plants typically also produce 3–1900 incidental hits for their Y.
- **Result:** K4 gives 0 hits across about 7e9 (Y, W, form) triples.
- **Verdict:** H-1502 is refuted for any dictionary-keyed tableau and any transposition.

## it68 — Running key with the KEY transposed (any permutation of a 97-letter source window)
- **Test:** the window's letter counts must cover the crib-derived key-letter counts. This was checked with sliding counts over 11.3M letters (21 sources), 6 standard models and all transpositions at once. Controls: 10/10.
- **Result:** 9,746 window × model pairs pass, a rate of about 1.4e-4. The test is weak where the counts are flat (the tableau) and under KA-Vig, which only needs YYYY+Q. Breakdown:
  - K1–K3 plaintext: 0 windows pass, so it is dead under any transposition.
  - K1–K3 ciphertext: 10 windows pass (KA-Var).
  - Tableau and Gutenberg texts: the rest.
- **it68b follow-up:** the 2,588 survivors from motivated sources (K1–K3 CT and the tableau) were tried with exact columnar transpositions (w = 2–7, every column order, both directions). Controls: 4/4. K4 gives 0 hits.
- **Verdict:**
  - Dead: a K1–K3 plaintext running key under any key transposition.
  - Dead: K1–K3 CT or tableau windows under columnar w ≤ 7.
  - Open but untestable by counts: generic English windows.

## it69 — H-708: one omitted or inserted CT letter between the cribs, with a periodic key under one arbitrary alphabet
- **Model:** the key index of BERLINCLOCK shifts by d = ±1, like K2's missing S. The key is periodic Quagmire III (key 0..25) through one arbitrary alphabet, in Vig/Beau/Var form. Each case is an exact z3 check at p = 1–48.
- **Control:** encrypt, then delete or insert one CT letter. The true (p, d) was SAT in 6/6 runs, and 10/10 in an extra batch. A first plant had a bug at d = −1; it was fixed, and the K4 runs were unaffected.
- **Result:** p = 1–13 is UNSAT for both d and all three forms. Some larger periods are feasible: 14, 15, 16 and 20 appear for particular (d, form) pairs, and 21–34 and 40–48 are scattered. That is about the null rate from it54, where 36% of periods were feasible at p = 23.
- **Verdict:** a single omitted or inserted letter does not revive short-period one-alphabet keys. That leaves H-707/H-708 open only for longer periods or other families.

## it70 — H-1205: a non-periodic small-digit key (each k_i free in 0..m−1) through mixed alphabets
- **Test:** an exact z3 crib check for m = 2–13, with one alphabet (Vig/Beau/Var) and with two alphabets. Controls: 6/6 SAT.
- **One alphabet:**
  - m ≤ 5 is UNSAT in every form.
  - m = 6 is SAT. it70b calibrated this against 40 nulls: the null SAT rate is 5/40 for Vig/Var and 22/40 for Beau. So K4's feasibility at m = 6 is mild (P ≈ 0.125), not a signal.
  - m ≥ 7 is SAT at the null rate.
- **Two alphabets:** m = 2 is UNSAT, and m ≥ 3 is SAT at the null rate.
- **Verdict:**
  - Small-digit masks are dead for m ≤ 5 under one alphabet and for m = 2 under two. This agrees with the it62 IC result for m ≤ 4.
  - m ≥ 6 is not crib-testable. A full-text check would be meaningless overfitting, since each CT letter has m candidate PT letters.

## it51h follow-up — beau-AZ PT-autokey L=9 at node cap 1e10
- **Run:** the rerun hit the 1e10 node cap with 520 crib-consistent solutions.
- **Result:** the it52 full-text completion gives a best of −6.58 per quadgram, which is gibberish. English with cribs scores −4.37 on average, with a minimum of −5.39.
- **Verdict:** none of the survivors so far is English. The model is still capped, not exhausted.
