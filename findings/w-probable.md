# w-probable T20: extending K4's known plaintext with probable words
Worker: w-probable, 2026-10-26/27 (UTC). Hypotheses: H-2001..H-2006.
Scripts: `workers/w-probable/scripts/`. Raw outputs are in `workers/w-probable/`:
- `gen_drag.tsv`, `gen_control.txt`
- `q3/*.tsv`, `ctrl/*.tsv`, `q3_analysis.txt`, `q3_binned.txt`
- `q3_base_forced.tsv`, `q3_base_forced_scores.txt`

Positions are 1-indexed. Corpus for the null words and n-grams: PG #11, #84, #1342 and #2600 (~1.4M words). It was downloaded to scratch and not copied into the workspace.

## TL;DR
1. **Under the leading surviving model the drag is vacuous, by proof.** The leading model (H-1203) is a plaintext-independent position key under one or two arbitrary alphabets, with no structure in the key. A probable word placed at non-crib positions adds one free unknown k_j per letter. Every placement is therefore consistent, and none forces a letter (false-positive rate = 1). Probable words cannot test this model until a key generator is specified, or until K5 gives a second message in depth with K4.
2. **Periodic GEN** (an arbitrary alphabet per residue class) at all 33 crib-consistent periods 8-52:
   - 122,067 placements were tested.
   - A random dictionary word of the same length is consistent at the same spot 76% of the time on average. That figure is 26-42% at p=8-13 and ≥90% at p≥35.
   - A placement forces at most 5 new letters (mean 0.3).
   - Inside every null-rate bin, probable words pass at the same rate as fresh random control words. For example, in the null<0.02 bin probable words pass 35/4110 and controls 116/12330. **No signal.**
3. **Quagmire III** (one mixed alphabet, K1/K2 structure), exact (CP-SAT, validated against z3):
   - Models: all 19 crib-consistent (style, period) pairs, i.e. Vig 27-30 and 41, and Beau 23, 26-33, 46, 47, 49, 51, 52.
   - 70,280 placements were tested.
   - Probable words vs random controls: 45/6250 vs 188/18750 in bin [0,0.02); 127/3953 vs 373/11859 in [0.02,0.05); equal in the other bins. **No probable word is preferred.**
   - The apparent excess in the lowest bins against the *estimated* null (z=+9) is a winner's-curse artefact of choosing cells by a 50-sample estimate. The control arm removes it.
   - The most letters any consistent placement forces is 3. None of the forced strings reads as English beyond chance: 5 of 71 have P≤0.05, against ≈3.5 expected.
4. **Letters the cribs alone force under Q3** (new):
   - Q3-Vig p=30 forces P3=K, P14=S, P38=I, P44=S, **P63=B (plaintext "...B BERLINCLOCK")** and P93=E.
   - Q3-Beau p=31 forces 8 letters, and p=23 forces 4.
   - For Q3-Beau p=26 the forced letters are un-English: P1=Q, P51=V, P58=K, P81=R, with P(English ≤ obs) < 2.5e-4. Beau 28, 51 and Vig 27 are also un-English (P≈0.002 each).
   - These four models are **statistically disfavoured, not excluded**.
5. **Exclusion map of motivated placements.**
   - "THE BERLINCLOCK" (THE at 61-63) is impossible under 8 of 19 Q3 models, including **both** surviving Vigenère-style ones (p=30, 41). It is also GEN-impossible at p ∈ {8,12,16,18,20,27,31,32,36,40,41}.
   - X as a separator at 21, 35, 63 or 75 is consistent everywhere except X@63 under Q3-V30.
6. **Conclusion.** Extending the cribs by probable words gives no information under any surviving model. A "consistent" placement has a likelihood ratio of at most 1/nullrate, and random words reach the same ratios equally often. The useful products are the forced-letter and exclusion tables (§5), which apply as soon as some other argument fixes a model.

## 1. Plaintext-style model (sources)
| feature | evidence | grade |
|---|---|---|
| X separates sentences (K2 has 4 X's: "...MAGNETIC FIELD X THE INFORMATION...", "...LAST MESSAGE X THIRTY EIGHT DEGREES...", "...WEST X LAYER TWO") | K2 plaintext, tools/kryptos_k123.py; https://en.wikipedia.org/wiki/Kryptos | P |
| numbers are spelled out, in coordinate register (DEGREES, MINUTES, SECONDS, NORTH, WEST) | K2 | P |
| deliberate misspellings (IQLUSION, UNDERGRUUND, DESPARATLY) | K1-K3 | P |
| K3 is a first-person diary paraphrase (Carter, 1922), with no X separators, ending "CAN YOU SEE ANYTHING Q" | K3 | P |
| K4 contains EASTNORTHEAST (22-34) and BERLINCLOCK (64-74) | facts/cribs.md | P |
| "Two events had a significant role to play while I was writing the plain text of Kryptos in 1988": the second trip to Egypt (late 1986) and the fall of the Berlin Wall. The Berlin Clock is the World Clock (Weltzeituhr), the gathering place of the crowds | Sanborn open letter Aug 2025, via https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/ and https://www.schneier.com/blog/archives/2025/08/jim-sanborn-is-auctioning-off-the-solution-to-part-four-of-the-kryptos-sculpture.html | P (secondary quote) |
| the Kryptos codes are about "delivering a message"; K5 is thematically tied to K2's "its buried out there somewhere"; K5 has BERLINCLOCK in the same position | SciAm 12 Nov 2025 (same URL) | P |
| the plaintext found on the Smithsonian scraps "makes semantic sense"; "Berlin clock" appears near the bottom | Kobek interview, https://zonamotel.substack.com/p/interview-kryptos-k4-uncovered-jarett | P |
| "reads like it's disjointed but there's a story", "more than one sentence" (Scheidt, 2015) | findings/w-sources.md S6d | P |
| "several directions. The word directions is — I use intentionally" (Sanborn, 2010) | w-sources J11 | P |
| Morse "T IS YOUR POSITION" (probably WHAT IS YOUR POSITION) | w-physical §3 | P |
| "what's the point" | **not found in any source**, UNVERIFIED. Tested only as one low-tier phrase | X |

**Ranked probable words and slots** (tier 1 = strongest motivation; full list in scripts/words.py):
- Before EAST (ends at 21):
  - X (1)
  - THE, DEGREES, SECONDS (2): K2's "...SECONDS NORTH"
  - bearing verbs FACING, TOWARD(S), HEADING, BEARING, WALK, LOOK, GO; distances FEET, PACES, MILES (3)
- After NORTHEAST (starts at 35):
  - X (1)
  - OF, OFTHE (2)
  - BY ("ENE by E"), TO, THE, FROM, AND, THEN, FOR, DEGREES (3)
- Before BERLIN (ends at 63):
  - THE (1)
  - X, EAST/WEST ("EAST BERLIN"), ATTHE (2)
  - TO, AT, NEAR(THE), OFTHE, TOTHE, BYTHE, UNDERTHE, WALL, THEWALL, IN (3)
- After CLOCK (starts at 75):
  - X (1)
  - IS, AND (2)
  - TOWER, THE, WALL, AT, TIME, WHERE, WHICH, HOUR, MIDNIGHT, WHATISTHEPOINT (3)
- Anywhere (dragged over every non-crib start), 68 content words:
  - MESSAGE, WALL, THE, X (1)
  - EGYPT, TOMB, NORTH/SOUTH/WEST, DEGREES/MINUTES/SECONDS, COMPASS, DIRECTION, POSITION, LOCATION, SHADOW, POINT, numbers ONE-TEN, DELIVER(ING), AND, OF (2)
  - CAIRO, PYRAMID, SPHINX, NILE, DESERT, CHAMBER, CANDLE, CARTER, BURIED, SECRET, LIGHT, CLOCK, TIME, HOURS, WORLD, GERMANY, LAYER, TWENTY-HUNDRED, NINETEEN, EIGHTYNINE, BERLINWALL, BEARING, YARDS, FEET, PACES (3)

## 2. Models where a placement is checkable
- **H-1203 / vig1 / beau1 / two-alphabet with an unstructured key (H-2001: vacuity, proof).**
  - Model: C_j = β(α(P_j) + k_j).
  - A placement at a non-crib j adds the equation k_j = β⁻¹(C_j) − α(P_j). k_j appears in no other equation, so the system stays solvable for every α, β that already fit the cribs. The relations k28=k66, k24+k34=k29+k33 and k33=k74=0 involve only crib positions.
  - Result: false-positive rate 1, and 0 forced letters, for every word at every position.
  - The same holds for any key that is free per position: running key from an unknown text, or OTP.
  - Probable words help here only together with a concrete key generator. In that case they act as extra cribs for the generator, e.g. the 258 two-alphabet survivors of w-keygen (H-1404), which force ≤9 letters.
- **GEN periodic** (`scripts/gendrag.py`). Within a class, P→C must stay a bijection. This is a necessary condition for every periodic polyalphabetic cipher, Quagmire I-IV included.
- **Quagmire III** (`scripts/q3fast.py`, OR-Tools CP-SAT; `q3drag.py`).
  - Model: pos(C) = pos(P) + d_r (Vig) or d_r − pos(P) (Beau), with one arbitrary permutation pos.
  - Validation:
    - 60/60 random placements agree with errtol.QModel (z3);
    - crib-only consistent periods reproduce w-crib §2 exactly (Vig 30, 41; Beau 23, 26, 30-33, 46, 47, 49, 51, 52), plus 27-29, which are GEN-vacuous but Q3-checkable;
    - forced-letter tables equal z3's forced_table (74/74, 47/47, 81/81 entries).
  - One placement of 70,281 timed out (B23) and was excluded.
- Not run:
  - Q1, Q2 and Q4: GEN results bound them, and Q4 is as weak as GEN at these periods.
  - The error-tolerant revivals of p=7, 10, 21, 25: crib-weak (w-errtol), so probable words would be as uninformative as under GEN.

**False-positive control.** For every (model, period, start, length) cell:
- the null rate is the share of N random dictionary words (count ≥5 in the corpus; N=1000 for GEN, 50 for Q3) consistent there;
- a separate control arm draws 3 fresh random words per placement (`gen_control.py`, `control.py`);
- the evidence test compares probable words with controls inside the same null-rate bin.

## 3. Results
### 3.1 GEN (33 periods, 122,067 placements; gen_drag.tsv)
- Mean null consistency by period:
  - 8: 0.26; 11: 0.35; 12: 0.40; 13: 0.42; 16: 0.54; 20: 0.54;
  - 22-31: 0.64-0.75; 32-33: 0.82-0.85; 35-52: 0.91-1.00.
- By word length: L1 0.94, L5 0.76, L10 0.62, L14 0.50.
- New forced letters per consistent placement:

| forced letters | placements |
|---|---|
| 0 | 72,043 |
| 1 | 14,255 |
| 2 | 4,338 |
| 3 | 924 |
| 4 | 179 |
| 5 | 2 |

- Probable vs control by null-rate bin (gen_control.txt):

| null bin | probable | control |
|---|---|---|
| [0,0.02) | 0.0085 | 0.0094 |
| [0.02,0.05) | 0.028 | 0.032 |
| [0.05,0.1) | 0.066 | 0.068 |
| [0.1,0.2) | 0.156 | 0.149 |
| [0.2,0.5) | 0.387 | 0.405 |
| [0.5,1] | 0.861 | 0.870 |

  This is indistinguishable from random words.
- Best forced-letter n-gram scores (e.g. UNDERTHE@56 p=22 → "HE" at 18-19, empirical p=0.003): 1.8% of the 1,105 placements with ≥3 forced letters have p≤0.01. That is chance, and the forced letters mostly repeat letters of the placed word itself.
- GEN-impossible periods for key placements:

| placement | GEN-impossible at p = |
|---|---|
| THE@19 | 11, 22, 44 |
| DEGREES@15 | 8, 11, 12, 16, 18, 23, 24, 27, 46, 48, 49 |
| OF@35 | 8, 11, 16, 32, 33, 37 |
| THE@61 | 8, 12, 16, 18, 20, 27, 31, 32, 36, 40, 41 |
| EAST@60 | 8, 19, 20, 29, 31, 38, 40 |
| WEST@60 | 8, 13, 19, 20, 29, 30, 31, 38, 39, 40 |
| IS/AND@75 | 13, 26, 52 |
| WALL@75 | 11, 22, 23, 44, 46 |

  X is consistent at every slot and period.

### 3.2 Quagmire III (19 models, 70,280 placements; q3_analysis.txt, q3_binned.txt)
- Per-model consistent-vs-expected counts all lie within noise of the estimated null, e.g. V30: 1694 vs 1670, V41: 3663 vs 3682.
- Probable vs control by null bin:

| null bin | probable | control |
|---|---|---|
| [0,0.02) | 45/6250 = 0.0072 | 188/18750 = 0.0100 |
| [0.02,0.05) | 0.032 | 0.032 |
| [0.05,0.1) | 0.056 | 0.051 |
| [0.1,0.2) | 0.102 | 0.110 |
| [0.2,0.5) | 0.407 | 0.431 |
| [0.5,1] | 0.829 | 0.835 |

  **No preference for probable words in any model** (per-model bins also match; see q3_binned.txt).
- Consistent placements with estimated null 0 (nominal likelihood ratio ≥ 50), for example:
  - V30: TOMB@60-63 (fits the forced P63=B), EGYPT@93, EIGHT@93 (fit the forced P93=E), WEST@12;
  - B23: PYRAMID@75, LOCATION@75;
  - B26: DELIVER@75, CHAMBER@75, SECRET@78;
  - B27: CAIRO@14, BERLINWALL@47.
  
  Random words reach such ratios equally often (control arm), so these are **not evidence**. They are listed only as the post-hoc curiosities a reader might raise.
- Forced letters: 71 consistent low-null placements force 1-3 new letters, and 5 have P≤0.05 (≈3.5 expected). Best cases:
  - BERLINWALL@47 under B31 → E@80 (p=0.04);
  - FIVE@18 under V28 → E@50;
  - DIRECTION@53 under V28 → "EC" at 84-85.
  
  None of this is English signal.
- Exclusion map (Q3-inconsistent models out of 19):

| placement | inconsistent models |
|---|---|
| X@21, X@35, X@75 | none |
| X@63 | V30 only |
| THE@19 | B49, V27 |
| OF@35 | B32, B33, V29, V30 |
| OFTHE@35 | 7 models |
| **THE@61** | B27, B31, B32, V27, V28, V29, **V30, V41** |
| ATTHE@59 | 9 models |
| EAST@60 | B28, B29, B31, V27-V30 |
| WEST@60 | 8 models |
| DEGREES@15 | 8 models |
| IS@75 | B26, B52 |
| AND@75 | 5 models |
| WALL@75 | B23, B27, B46, V41 |
| TOWER@75 | 8 models |

### 3.3 Letters forced by the cribs alone under Q3 (q3_base_forced*.txt)
Exact over all alphabets. Scored by a context n-gram (≤3 known letters on each side, 4-book corpus).

| model | forced letters (position:letter) | LLR | P(null≥obs) | P(English≤obs) |
|---|---|---|---|---|
| V30 | 3K 14S 38I 44S **63B** 93E | +0.31 | 0.06 | 0.12 |
| V41 | none | | | |
| B23 | 45F 48L 78A 97P | −0.27 | 0.30 | 0.07 |
| **B26** | 1Q 51V 58K 81R | −2.67 | 0.90 | **<2.5e-4** |
| B31 | 2N 4P 38N 54A 61H 93G 94A 97P | +0.82 | 0.025 | 0.23 |
| B32 | 8F 36I 96K | −0.70 | 0.51 | 0.026 |
| **B51** | 13N 16V 17T | −1.87 | 0.55 | **0.002** |
| **V27** | 6O 18O 20B 47Z 60I 87K | −1.88 | 0.60 | **0.002** |
| V28 | 5U 18F 46K 61N 89H | −0.61 | 0.34 | 0.029 |
| V29 | 3A 4R 16L 45E 62F 91A | +1.49 | 0.006 | 0.52 |
| **B28** | 46K 81V 93Y | −1.56 | 0.76 | **0.002** |
| B30, B33, B46, B47, B52, B27, B29 | 1-2 letters each | ns | | |
| B49 | none | | | |

- Q3-Vig p=30 (one of only two Vigenère-form K1/K2-style survivors):
  - class 3 contains S→S at 33, so d=0 and positions 3, 63 and 93 are self-encrypted;
  - **the letter before BERLIN must be B** ("…B BERLINCLOCK", e.g. "…TOMB BERLIN…", "…CLUB…").
  - The n-gram cost is mild (B before "BER…" is common inside words like RUBBER). So this rules out the common readings "THE/AT/X/EAST BERLIN" under V30 but does not refute V30.
- V29's forced letters are mildly English-like (p=0.006, family-wise ≈0.1 over 17 scored models). Not significant.
- B26, B28, B51 and V27 force un-English letters. **Statistically disfavoured** (family-wise ≈0.004 for B26, ≈0.03 each for the others).

## 4. Hypotheses
- **H-2001** Probable-word dragging under an unstructured plaintext-independent key (H-1203, vig1, beau1, two-alphabet): vacuous (FP=1, 0 forced). FACT (proof).
- **H-2002** Probable words under GEN periodic p=8-52: no excess over random controls; ≤5 forced letters. NO EVIDENCE (test power low).
- **H-2003** Probable words under Q3, all 19 crib-consistent models: no excess over controls; ≤3 forced letters; no English. NO EVIDENCE.
- **H-2004** Crib-forced letters under Q3: V30 forces P63=B, which excludes "THE BERLINCLOCK"; V41 has no forced letters. FACT (exact). "THE BERLINCLOCK" is Q3-impossible under V30, V41, B27, B31, B32, V27, V28 and V29.
- **H-2005** Q3-Beau p=26, p=28, p=51 and Q3-Vig p=27 are disfavoured: their crib-forced letters are un-English. STATISTICAL.
- **H-2006** No probable placement is both consistent and statistically non-trivial once the selection effect is controlled. REFUTES the idea that crib-dragging probable words can advance K4 under current models.

## 5. Recommendations
- Do not spend more effort on probable-word dragging until a model with key structure is fixed. Under the leading model it is provably blind.
- Once K5's ciphertext is public, re-run `q3drag.py` and `gendrag.py` with K4/K5 depth, since words are shared at the same positions. A probable word placed in K4 then forces K5 letters, and vice versa. That is where these tools gain power.
- The exclusion map in §3.2 and the forced letters in §3.3 are ready-made checks for any future candidate model.

## 6. Caveats
- The null and control words come from a 4-book PG corpus (19th-century prose plus Alice). The probable list leans toward common short words and number words, which shifts the raw "expected" counts, e.g. tier-2 z=−7 against the estimated null. The control-arm comparison is the valid test.
- The Q3 null used N=50 samples per cell (resolution 0.02). The control arm (3 per placement, about 211k words in all) is what supports the conclusion.
- No error tolerance (H-209). A carving error at a crib position changes the per-model tables.
- The n-gram forced-letter test assumes ordinary English. K4 may contain deliberate misspellings, as K1-K3 do.
