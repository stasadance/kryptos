# w-errtol T10: periodic families re-tested with deliberate-error tolerance
Worker: w-errtol. Date: 2026-10-26 (UTC). Hypotheses H-1001..H-1006.
Tool: `tools/errtol.py` (solver library plus `consistency` CLI). Drivers: `workers/w-errtol/scripts/`:
- s1/s2: GEN/TAB tables
- s3: z3 SAT sweep
- s4: forced tables
- s6: scoring
- plant.py: planted-plaintext check

Raw results are in `workers/w-errtol/*.jsonl`.
English model: PG #2600 + #1342, rebuilt per the quadgram.py docstring (3.07M letters).

**No candidate.** No configuration produced forced text that is significantly English, so nothing reached crib_check.

## Error models (bounded, exact; no keyspace search)
- **SUB:** at most 2 wrong carved letters. Only errors at crib positions change crib consistency. That gives C(24,0)+C(24,1)+C(24,2) = 301 deletion sets per period and family, all enumerated. Errors at non-crib positions can only garble at most 2 forced letters.
- **SHIFT:** 1 letter omitted (d=+1) or inserted (d=-1) at carved position j. Only j in the crib gap (35..64) changes crib alignment: BERLINCLOCK's key index moves by d. The forced text was scored for every j. The null takes the maximum over j as well, so it pays for that choice.
- **Extra:** 1 shift + 1 sub, checked for GEN only.

## Families and solver
- **GEN:** an arbitrary bijection per class.
- **TAB:** Vig-style (C=P+s; this covers variant Beaufort) and Beau-style (C=s-P), with the plain and cipher alphabets each AZ or KA (8 combos).
- **Quagmire:** Q1 (cipher alphabet fixed to AZ or KA, plain arbitrary), Q2 (plain alphabet fixed to AZ or KA), Q3 (one arbitrary alphabet for both), Q4 (two arbitrary alphabets). Each in Vig and Beau style.
  - Exact z3 (Int encoding, Distinct, gauge-fixed, 60 s timeout). No check timed out.
  - Q1 and Q4 gave identical Vig and Beau results, as w-crib proved they must.
  - My Q3 results reproduce w-transpo §c: p=7 and 10 unsat with at most 2 errors; p=21 Beau unsat with at most 2; p=25 Beau SAT with 1 error at 22.
  - New: w-transpo's open case, Q3 Vig p=21 with 2 errors (z3 timed out there), is **SAT**. Solved in 0.6-1.5 s here.
- **Forced letters:**
  - A (class, CT-letter) entry is forced if it is identical in every solution. For GEN this is direct.
  - For the Quagmires, z3 solution-elimination finds the full forced table. Each table is computed once per crib configuration and does not depend on j.
- **Score:** per forced letter, the conditional English n-gram LLR (up to 4-gram, back-off; context = known preceding letters, crib letters included) minus the uniform baseline.
  - **Null:** the same config with K4's non-crib CT letters shuffled (500-1000 draws). Under the null, forced letters are drawn from the crib letters, so the null is not uniform.
  - **H1:** English windows with the identical mask (200 draws). This gives the English expectation, `engp` = P(English ≤ observed), and the power at null 95%.
  - The quadgram.py masked mean (first pass, 348 configs) agrees: minimum null p is 0.03.
- **Pipeline check (plant.py):** English was encrypted with random Q2KA p10, Q1AZ p10 and Q3V p21 keys, and errors were planted at crib positions. The solver recovered the planted configs as SAT, and every forced letter (41 and 54 in the two p=10 cases) was correct, with LLR ≈ +0.3 to +0.5 per letter. When the family is right, the method detects English.

## 1. Which focus periods error tolerance can revive (crib consistency only)
| p | GEN (any periodic subst.) | TAB 8 combos | Q1 AZ / KA | Q2 AZ / KA | Q3 Vig / Beau | Q4 |
|---|---|---|---|---|---|---|
| 7 | **dead**: needs 3 subs; 1 shift dead; 1 shift + 1 sub dead | dead | dead | dead | dead | dead |
| 10 | 1 sub {22} or {72}; shift ±1 | dead | AZ only {24,72},{33,72}; KA dead | AZ only {22,34}; KA {22},{32,72},{72,74} | dead / dead (≤2, shift) | {22},{72}, ±1 |
| 21 | 2 subs {25\|67}×{32\|74}; shift +1 | dead | AZ: 4 pairs + om; KA: 4 pairs | dead | Vig 4 pairs + om / Beau dead | 4 pairs + om |
| 42 | as p=21 | dead | as p=21 | dead | as p=21 | as p=21 |
| 25 | 1 sub {22}/{72}; ±1 | dead | {22},{72},±1 | {22},{72},±1 | Vig only 2 subs {22,24},{22,74},{24,72},{72,74} / Beau 1 sub, ±1 | 1 sub, ±1 |
| 50 | as p=25 | dead | as p=25 | as p=25 | as p=25 | as p=25 |

Notes:
- TAB over all periods 1-60: with at most 2 subs or 1 shift, only periods 26, 30, 31, 32, 51 and 52 are revived, plus the crib-vacuous ones (27-29, 53+). This reproduces w-transpo.
- The 1-shift + 1-sub extension revives GEN at 10, 21 (om), 25, 42 (om) and 50 at every crib position. p=7 stays dead.

## 2. Forced text vs English (412 minimal configs, max over j for shifts)
| family / p | forced non-crib letters | power at null 95% | best LLR / letter (English expect.) | verdict |
|---|---|---|---|---|
| TAB, p=26-32, 51, 52 (incl. vacuous 27-29 with omission at any j) | 20-64 | 1.00 | −0.43 to −1.2 (+0.48 to +0.55) | **not English**: engp ≤ 0.005 for every config |
| Q1AZ p=10 {24,72}/{33,72} | 32-35 | 0.94 | +0.03 (+0.22) | not English (engp 0.005) |
| Q2AZ p=10 {22,34} | 21 | 0.99 | −0.12 (+0.23) | not English (engp 0.01) |
| Q2KA p=10 {22},{32,72},{72,74} | 12-21 | 0.91-0.99 | −0.16 (+0.22) | not English (engp ≤ 0.005) |
| GEN / Q4 p=10 | 6-10 | ≤0.04 | +0.21 (+0.19) | untestable (consistent with both) |
| Q1, Q3V, GEN, Q4 at p=21 | 1-7 | ≤0.67 (mostly <0.15) | ≤0.32 | untestable |
| any family at p=42, 50 | 0-3 | ~0 | n/a | untestable: nothing forced outside the cribs |
| any family at p=25 | 1-5 | ≤0.33 | ≤0.44 | untestable |

- Over all 412 configs the smallest null p-value is 0.030. There are 9 below 0.05 against about 20 expected by chance, and none below 0.01. No configuration is significantly English.
- **Example (best-powered Quagmire), Q1AZ p=10 with errors at 33 and 72:**
  `?S?SST?T??O??T???O?R?EASTNORTHEAST?I?ISK???T?LT?IT????S??CIA?E?BERLINCLOCKRK?LA???S?HK?????KRK?CK`
  The "CIA" at 57-59 is chance: the config's LLR equals the null mean.
- **Example, Q2KA p=10 with an error at 22:**
  `??YS???????F?T?Z?M???EASTNORTHEAST?I?IWD?SST?Q??????YO???????O?BERLINCLOCK???Q????????S??????K??F`

## 3. Conclusions
1. **Period 7 (H-1001).** Every periodic substitution of period 7, under any tableau or arbitrary alphabets (GEN ⊇ Quagmire I-IV, Vig/Beau, AZ/KA), stays excluded under every error model tested: at most 2 errors, 1 omission/insertion, or 1 omission/insertion plus 1 error. It needs 3 wrong letters. The 8 minimal triples are {25,32,66}, {25,32,73}, {25,66,74}, {25,73,74}, {32,66,67}, {32,67,73}, {66,67,74} and {67,73,74}. The NSA "roughness on interval 7" therefore cannot be a period-7 substitution key, even with a K1-K3-style error budget.
2. **Standard and KRYPTOS tableaux (H-1002).** All 8 TAB combos stay dead at 10, 21, 25, 42 and 50 with the error budget. The periods the budget does revive (26, 30-32, 51, 52, and vacuous 27-29 under any omission point) force 20-64 letters, and those are never English (power 1.0). This extends w-crib's 27-29 refutation and w-transpo's 26/30-32/51/52 check to quadgram-level evidence, with omissions at every j.
3. **Quagmire at period 10 (H-1003).** PALIMPSEST-length Quagmire I (AZ cipher) and II (AZ or KA plain) can be revived only by specific error pairs. Their forced text (12-35 letters, power ≥0.9) is not English. Q1 with a KA cipher alphabet and Q3 stay dead. So with errors at most 2, every period-10 Quagmire except Q4/GEN is refuted.
4. **Untestable cases (H-1004, H-1005).** GEN and Q4 at p=10, and every family at 21, 42, 25 and 50 that the budget revives, force too few letters (0-10) to test. They are **not refuted and not supported**. Only a concrete alphabet or keyword hypothesis could test them. For a period-21/42 key (H-706) the 2-error repair needs errors at one of 25/67 **and** one of 32/74. Under one omission (d=+1) it needs none.
5. **SAT here only means "not refuted" (H-1006).** Where the budget makes p ≥ 21 consistent, it adds no information. Plausibility then rests on priors: physical evidence of carving errors at the named positions (w-antipodes found none on Antipodes), and Sanborn's statements on positions.

## Caveats
- An omission or insertion **inside** a crib word, or two shifts, was not modelled. Either would contradict Sanborn's stated crib positions.
- A deleted crib is a full relaxation: the true CT letter is unconstrained. This is conservative, because it can only add SAT configs.
- Only model-minimal error sets were scored. Their supersets force a subset of the same letters.
- Q-forced tables treat z3 timeouts as "not forced". None occurred.
