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
