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
