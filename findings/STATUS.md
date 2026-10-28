# K4 project status (round 8 refresh by the solver, 2026-10-28 UTC; supersedes the round-7 consolidation)

Detail: `JOURNAL.md` (solver iterations it51–it92), `hypotheses/log.md`, `hypotheses/ruled_out.md`, `findings/*.md`.
The round-7 text is kept below §0. Lines changed by round 8 are marked **[r8]**.

**Bottom line.** K4 is not solved, and there is no candidate. Since round 7:
- Keyword-built alphabets are closed at dictionary scale (3.63M alphabets from 370k English + 686k German words). That covers periodic p ≤ 48, every stored key-stream library, autokey and running keys, including one carving error (it82–86).
- Quagmire I/II with ANY single arbitrary alphabet is dead against all 24M stored key streams (it87).
- Class C (concrete stream + two arbitrary alphabets) was decided by a new crib-exact full-text annealer: 1,400 survivors, null band, closed (it88).
- Classes E/G (periodic Q4/Q3 with arbitrary alphabets at the surviving periods) are PARKED as search-limited. Parallel tempering and a nested search both fail planted controls from p ≈ 4–8 up (it91–92).
- K5 depth with an unstructured key is model-limited with character n-grams (2·D = 4.52 < 4.70 bits/letter). See findings/k5_day_procedure.md.

## 0. Decidability frontier (single table, through it92) [r8]
D measured on held-out text, 58M-letter training: 4-gram 1.82, 5-gram 2.11, 6-gram 2.26 bits/letter (tools/lm/build_lm.py).

| Class | Status | Evidence (latest) | What would decide it |
|---|---|---|---|
| Textbook single-layer ciphers (mono, periodic AZ/KA, Playfair-type, Porta, Enigma-like, 25-letter grids, M-94, Hill n≤5 lin / n=4 aff) | DEAD | §2; it62, it65, it75; **it90: Hill n=4 affine and n=5 linear, 0 configs consistent, plants 5/5** | — |
| A. Structured generator + fixed AZ/KA tableau | DEAD for every motivated generator (~21M configs) | exact screens; it86 1-error tolerance closed for keyword alphabets | a new generator idea (cribs decide it instantly) |
| B. Structured generator + ONE mixed alphabet | DEAD for the stored libraries | w-keygen/w-route/w-transkey vig1/beau1/Q3; **it87: Q1/Q2 with any one arbitrary alphabet, 0/24M** | a new generator idea |
| Keyword-built alphabets (any tableau, Q1–Q4) | DEAD at dictionary scale | it42–47, it82–86 (3.63M alphabets; periodic, libraries, autokey, running key; 1-error tolerant) | — |
| C. Concrete stream + TWO arbitrary alphabets | CLOSED for the 258 keygen + 1,142 route survivors | **it88: crib-exact SA, plants 19/20; K4 best −478.7 vs null E[max] −456, p≈1** | 46 Gromark primers and 13.9k transkey Q4 survivors not run (low marginal value) |
| D. Unstructured / OTP-like key | NOT IDENTIFIABLE from K4 alone | H-2001 proof | K5 depth needs a word-level LM (it89) |
| E. Q4 periodic p16–28, arbitrary alphabets | PARKED (search-limited) | w-anneal 0/294; **it91 PT 0/12 @p20, 0/4 @p8; it92 nested 0/4 @p8, 0/4 @p20** | a new algorithm, more plaintext, or K5 (structured key) |
| F. Q4 periodic p≥30 | NOT IDENTIFIABLE | spurious optima beat English | — |
| G. Q3/Q1/Q2 periodic survivors (V30, V41, B23, B26–33, B46–52), arbitrary alphabet | p≤33 PARKED (search-limited), p≥41 NOT | as E | as E |
| H. GEN periodic p≥8 | NOT IDENTIFIABLE | w-anneal | — |
| Autokey (PT/CT, any tableau) | CLOSED to L=13 for PT-autokey (it51, it79, it80); CT-autokey per §2 / decidability map | it80: best −6.31 vs English ≥ −4.73 | — |
| Chaocipher, Hagelin M-209 | CRIB-UNTESTABLE | it74 lemma (~1e11 wheel pairs), it77 | more plaintext |
| L. Weltzeituhr per-face alphabets (H-802) | DEAD on the read faces (the conjunction kills every alignment; the far faces can't revive one) | it40 | — |
| M. English running key, unknown alphabet(s) | MARGINAL; dead under the standard tableaux and keyed Q3 | H-1101, it81 | word-level LM |
| N. Trifid (27th symbol absent) | partly dead (periods 2–9, 11–13) | w-mask | Trifid-27 exact (queued) |
| P. K4+K5 in depth | **[r8] structured key: IDENTIFIABLE; unstructured key: MARGINAL (model-limited with char n-grams)** | **it89: 0/56 plants with the 4- and 6-gram, found ≥ true** | findings/k5_day_procedure.md |


This file summarizes rounds 1-7 (tasks T1-T21). Detail lives in `findings/*.md`, `hypotheses/log.md` and `hypotheses/ruled_out.md`.
The identifiability calculations and synthetic experiments behind section 4 are in `findings/w-synth.md` (scripts: `workers/w-synth/scripts/`).

**Bottom line.** K4 is not solved, and we have no candidate.
- Every textbook single-layer family is excluded. So is every structured key generator we could motivate, when it runs under a fixed AZ/KA tableau or under one mixed (K1/K2-style) alphabet. That is about 21M exact configurations, with 0 hits and validated plants.
- What is still open is mostly **not identifiable from 97 letters plus 24 cribs**. This is true in principle, not just because our searches are weak.
- There is one important exception, new this round. Any **concrete key stream** under two arbitrary alphabets *is* identifiable by full-text annealing. Earlier rounds called it "crib-untestable", but it can be tested (§4, §6 task 1).

## (round-7 text follows)

## 1. What is known (sourced)
| Fact | Source |
|---|---|
| CT = 97 letters (facts/ciphertext.txt), identical on the sculpture transcript and on both Antipodes copies; all 26 letters occur; IC 0.0361 | w-lit §1, w-antipodes §a, w-stats §1 |
| Cribs: EASTNORTHEAST at 22-34, BERLINCLOCK at 64-74 (1-indexed); self-encryptions S@33, K@74; R→P at both 28 and 66 | facts/cribs.md; w-crib §0 |
| Plaintext position = ciphertext position. Sanborn: "letter-position 27" check (NYT 2010, P); "BERLIN … exactly the 64th" (2019, S); "one-to-one … plain B … out pops cipher N" (S, conflicting accounts) | w-sources J10, J15, J16 |
| K1/K2 = Quagmire III with the KA alphabet (PALIMPSEST, ABSCISSA). K3 = transposition, exactly PT[k]=CT[192k mod 337]. The K1 and K2 errors are a key-letter slip and a mis-carved CT letter | w-history §1-2; tools/kryptos_k123.py |
| Scheidt: "more than one stage"; "masking technique so the English language wouldn't be available"; OTP-like "in the sense of the result"; he was asked NOT to change the math base; "simple, can be remembered … correct key word/s" (Hannon notes, S); he never checked K4 | w-sources S1-S10; w-mask §1 |
| Sanborn: "methods that don't have anything to do with mathematics"; "matrix codes", "visual systems … individualistic"; he modified Scheidt's system; nobody proofread it | w-sources J5, J17, J18, J21, J24 |
| BERLINCLOCK = "the World Clock in Berlin". Egypt 1986 and the fall of the Wall in 1989 "figure in the solution" | SciAm 12 Nov 2025; w-clock §4 |
| K5: 97 chars, "similar coding system", BERLINCLOCK at the same position (plaintext). Paradigm holds the K5 CT and will release it. The K4 plaintext is found (sealed until 2075) but the method is not public | w-k5 §1-2; w-lit §2 |
| "Scrambled plain text" (2025) = 1990 vetting strips, not a cipher stage | w-transpo §b (H-705) |
| NSA 1992-93: "roughness on interval 7"; plaintext-autokey and transposed-substitution attempts failed. The 2007 NSA summary has not been retrieved (403) | w-antipodes §b |
| Statistics: no period signal at p=1..32 (FW P=0.94). Post-hoc anomalies: width-21 vertical bigrams (FW 0.0047), width-7 doublets (FW 0.0041), lag-7 (FW 0.09). No classical model reproduces them | w-stats §2-5; w-transpo §a |

## 2. What is ruled out (robustness and audit status)
Robust = survives ≤2 wrong CT letters and 1 omission between cribs. Audit = independently re-derived by w-audit (T16).

| Excluded class | Basis | Robust to errors? | Audit |
|---|---|---|---|
| Pure transposition; mono ± transposition | IC/chi² p<5e-6; 3E vs 2E | Yes (IC). The E-count argument alone is fragile | confirmed |
| Fixed-point-free ciphers (Playfair, Porta, Enigma-like) | S→S@33, K→K@74 | 1 error yes, 2 no | confirmed |
| Periodic Vig/Beau/vBeau, AZ/KA, PA=CA or mixed, every reachable period (incl. 27-29 by decrypt) | crib algebra + decrypts (w-crib §1, w-errtol §2) | Yes. Error-revived periods force gibberish | confirmed (also 49-52) |
| Any periodic substitution with arbitrary alphabets (GEN) p ∈ {1-7,9,10,14,15,17,21,25,34,42,43,45,50} | crib bijection conflicts | **Fragile**: p=10/25/50 revived by 1 error; most p≥6 by 1 omission. p=7 needs 3 errors (robust) | confirmed |
| Periodic (any alphabets) after a transposition, p ≤ 13 except 7, 10, 11 | pooled column IC | Yes | confirmed |
| Quagmire III (one mixed alphabet), all periods except Vig 30, 41 / Beau 23, 26-33, 46, 47, 49, 51, 52 | z3 (w-crib §2) | p=7, 10 robust to ≤2 errors | confirmed |
| Quagmire I/II/IV at the listed dead periods (Q4: 11, 12, 18, 22, 36, 44) | exact solvers | inherits GEN fragility | confirmed; Q4 p=12 added by audit |
| CT-/PT-autokey (fixed tableaux); CT-autokey L≤31 and PT-autokey Vig L≤10 with a mixed alphabet | w-crib §3, w-mask §3.5-3.6 | mostly; CT-autokey L=69-73 fragile | confirmed |
| Hill n=2,3 (linear and affine), n=4 linear | per-row solve | n≤3 robust; n=4 fragile (1 error) | confirmed |
| **[r8]** Hill n=4 affine, n=5 linear (AZ/KA, every offset, every crib letter per row) | it90 exact per-row brute force | not error-tested | plants 5/5 |
| Gromark/Gronsfeld with a standard plain alphabet; Gromark with any fixed or keyword alphabet (b2-16, primers 2-6); Vimark with AZ/KA | w-crib §7, w-gromark §2-4, w-sources §5 | std-alphabet proof fragile (1 pair) | confirmed (index slip fixed) |
| Columnar transposition (either order) with cribs in place, widths 2-75 | contiguity proof | n/a | **overclaimed**: widths 76-96 can fix the cribs (H-704 class) |
| Natural-language running key under the 18 AZ/KA tableaux | quadgram test, >5 sd below English | yes, with 2 free errors | confirmed (statistical) |
| Running keys from motivated texts (Carter, K1-K3, KJV, Morse, charter, oath, letters) | exact, every offset, max 9/24 | n/a | — |
| Numeric base-change / XOR / Baudot masks; linear and quadratic position keys under ANY alphabets | closure theorem; crib relations | n/a | confirmed (scope: plaintext-independent keys) |
| Weltzeituhr: single-city keyword per face; zone offset + ring key; any key that is a function of i mod 24 | w-clock H-801/803/804 | p=24 robust (≥5 deletions) | not audited |
| Keyword generators (periodic, progressive, compound, chain-add, interrupted, columnar streams; 29 keywords): 900k configs | exact, fixed tableaux + vig1/beau1 | **not error-tolerant** | not audited |
| Tableau-traversal / clock-hand keys under ANY alphabets | exact (w-keygen H-1402) | not error-tolerant | not audited |
| Physical-grid route keys and overlays (796k placements) | exact, fixed/vig1/beau1/letter-level | **not error-tolerant** | not audited |
| K3-style transposed key streams (19.2M configs) | exact, fixed/vig1/beau1/Q3-proper | **not error-tolerant** | not audited |
| Probable-word dragging as a method under current models | proof (vacuous) + controls | n/a | — |
| Antipodes variant K4; "scrambled = transposition" | photo diff; sources | n/a | — |

**Main residual loophole:** the ~21M-config exact generator screens (w-keygen, w-route, w-transkey) all assume error-free cribs. One carving error at a crib position would hide a true hit, and H-209 says 1-2 errors are plausible.

## 3. Identifiability map (T21)
Budgets: each crib letter gives log2 26 = 4.70 bits, so the cribs carry **112.8 bits**. Each unknown letter gives D bits.
- True English: D ≈ 3.2-3.5. Full-text budget **346-368 bits**.
- Quadgram model, measured on held-out text: D4 = 1.86 bits/letter. Practical budget **249 bits**.

H(K) is the key entropy after gauge symmetries. A ratio H/B < ~0.8 means identifiable with margin. The method column says which tool decides the class.

| Open class (hypotheses) | H(K) bits | H/368 (true) | H/249 (quadgram) | Verdict | Empirical check | Method / tool |
|---|---|---|---|---|---|---|
| A. Structured generator + fixed AZ/KA tableau (any new rule) | log2 N ≤ 30 | ≪1 | ≪1 | **IDENTIFIABLE by cribs alone** (24 equalities ≈ 2^-113) | plants 28/28, 50/50, 20/20 | tools/keygen.py, crib_check.py |
| B. Structured generator + ONE mixed alphabet (vig1/beau1/Q3-proper) | 88+log2 N ≈ 110 | 0.30 | 0.44 | **IDENTIFIABLE by cribs** (selectivity ≈1e-11 ≈ 36 bits) for N ≲ 2^30; by full text always | synthetic: 12/12 recovered (known stream) | keygen.feasible, transkey selfmodel.py |
| C. Concrete stream + TWO arbitrary alphabets (H-1404 258 survivors, H-1804 12.8k Latin passers, H-601 46 Gromark primers, Vimark-mixed, double key L1+L2≥25) | 172+log2 N ≈ 180-190 | 0.50 | 0.74 | Cribs: NOT (≈11 bits). **Full text: IDENTIFIABLE** | **new:** 11/12 controls recovered; K4 under 40 random streams: best −498..−550 vs English −400..−434 | workers/w-synth/scripts/sa.c (task 1) |
| D. Unstructured position key, 1-2 alphabets (H-1203, "OTP-like") | ≥456+88 | >1.4 | >2 | **NOT IDENTIFIABLE** (proof: H-2001, false-positive rate 1) | — | needs a generator idea or K5 depth |
| E. Quagmire IV periodic, p=16-28 | 242-299 | 0.66-0.81 | 0.97-1.20 | **MARGINAL** (in principle yes; search-limited) | w-anneal: 0/150 recovered, true > found | better two-alphabet search or keyword alphabets |
| F. Quagmire IV periodic, p≥30 (incl. vacuous 53-60) | ≥308 | ≥0.84 | ≥1.24 | **NOT** (spurious optima beat English) | w-anneal: found ≥ true in 125/126 controls at p≥37 | — |
| G. Q3/Q1/Q2 periodic survivors (Q3 V30, V41; B23, B26-33, B46-52) | 88+4.7(p−1): 192 (p23), 225 (p30), 277 (p41), 328 (p52) | 0.52-0.89 | 0.77-1.32 | p≤33 **MARGINAL**; p≥41 **NOT** | B26, B28, B51, V27 disfavoured (w-probable §3.3) | crib-exact Q3 annealer (not built) |
| H. GEN periodic p≥8 (independent alphabet per class) | 373-434 (from K4's class letters) | >1.0 | >1.5 | **NOT IDENTIFIABLE** | w-anneal §3: nulls beat English by ~80 log10 | — |
| I. Error-revived periodic (H-1004/1005: GEN/Q4 p=10, 21, 25, 42, 50) | Q4 p10 ≈ 219; p21 ≈ 266; GEN ≥ 380 | 0.6-1.0+ | 0.9-1.5 | Q4 p10 **MARGINAL**; rest **NOT** | w-errtol: power ≤0.04 | — |
| J. PT-autokey Beau, mixed alphabet, L=6-8, 10-12 (H-1207) | 88 (cribs seed every residue) | 0.24 | 0.35 | **IDENTIFIABLE** (earlier SA failure was search, not information) | — | exact/propagation search (task 3) |
| K. CT-autokey, mixed alphabet, surviving L (Vig 37+, Beau 32+) | 88 + primer (positions ≤L act like an OTP) | ~0.5 over positions >L | 0.6-0.9 | **IDENTIFIABLE/MARGINAL** (key known for i>L) | class-B experiment applies | vig1 SA with key = shifted CT (task 3) |
| L. Weltzeituhr per-face alphabets from face names (H-802) | ≈11 given the list; GEN-24 without it | — | — | **IDENTIFIABLE once the face list exists**; NOT without it | dummy null 4/24 | tools/w-clock/face_test.py |
| M. Running English key under unknown alphabet(s) | 88/172 + 97·H_E | 0.6-0.9 | >1.2 | **MARGINAL** in principle, NOT with quadgrams | — | needs a strong LM |
| N. Trifid n=10; Hill n≥5 / n=4 affine | 93; 117-141 | 0.3-0.4 | 0.4-0.6 | IDENTIFIABLE in principle (low prior; 97 prime; 27th symbol absent) | — | z3 + SA |
| O. Crib-preserving block shuffle + any of the above (H-704) | + log2(#shuffles) | — | — | NOT on its own | — | — |
| P. K4+K5 in depth (H-1302), if K5 is released | key cancels: 88-172 + 159·H_E vs 456 (data) + 35 crib letters | 0.6-0.8 | ~1 (per-position key); ≪1 (structured key) | **[r8] corrected:** IDENTIFIABLE with a structured key; with an unstructured key MARGINAL / model-limited (2·D6 = 4.52 < 4.70; it89 0/56 plants) | — | workers/w-k5/k5_depth.py, then latin_filter, q3drag/gendrag in depth |

Key consequences:
1. The project has been **hypothesis-limited in A/B** (cribs are decisive, but no motivated generator has hit) and **information-limited in D-I** (no search can help). Class C sits in between: it is decidable and has not been run.
2. Each extra known plaintext letter adds 4.7 bits for exact screens and about 2.8 net bits for full-text tests. About 15 extra crib letters would make class C crib-decidable without annealing. Five more letters would cut GEN/Q4 consistency sharply at mid periods.
3. Better language models raise D from 1.86 toward 2.5-3 (5-6-gram or word-level models). That would move E and part of G from MARGINAL toward identifiable. It would not change D, F or H.

## 4. Synthetic verification (this round; details in findings/w-synth.md)
- Quadgram redundancy measured at 1.86 bits/letter (n-gram orders 1-4: 0.52, 1.06, 1.48, 1.86). This matches Shannon's F4.
- **Class B** (one alphabet, known key stream, 97 letters, cribs as in K4): 12/12 recovered at 100% accuracy in under 1 s each.
- **Class C** (two alphabets, known stream): 11/12 recovered (accuracy ≥0.90; the found optimum scores ≥ the true plaintext only when accuracy is ≥0.95).
  - Null: K4 decrypted under 40 random streams that satisfy K4's crib relations. 9 were crib-feasible, and their best scores were −498 to −550, against −400 to −434 for English.
  - The separation is about 65 log10 units, so class C is **decidable per stream**.
- Agreement with w-anneal (T19): their oracle (cipher alphabet given) recovers 100%. The obstacle there is the joint search over unknown periodic shifts plus two permutations, not the information.
- Penalty-only SA with unknown periodic shifts never reached crib feasibility, as w-anneal found with its mode 4. Those runs are discarded.

## 5. What new information would unlock progress, and the tool to run
| New information | Expected effect | Run immediately |
|---|---|---|
| **K5 ciphertext** (Paradigm) | Decides H-1302 in one line: is K5[64..74] = NYPVTTMZFPK? If so, it gives depth (class P identifiable) and 11 more cribs | `python3 workers/w-k5/k5_depth.py <K5>`; then `tools/latin_filter.py` on C5−C4, `workers/w-probable/scripts/q3drag.py`/`gendrag.py` in depth mode, and all exact generator screens with the 35 cribs |
| **More plaintext from Sanborn/Paradigm** (new clue letters) | +4.7 bits per letter; re-tests every class | add to facts/cribs.md; rerun `tools/keygen.py` screens, `tools/errtol.py`, `workers/w-transkey/scripts/transkey.py`, `workers/w-route/scripts/route.py`, `tools/gromark.py scan` |
| **Pre-1997 Weltzeituhr face list** (24 lines, UTC order) | Decides H-802 (class L) in seconds | `python3 tools/w-clock/face_test.py faces.txt` (only 24/24 counts; null max ≈4/24) |
| **NSA 2007 "KRYPTOS Summary"** | Lists NSA-excluded families, and possibly the doublet/width-7 analysis | read it, then append to ruled_out.md as informal; no tool. Fetch via the user's device network (cloud proxy 403) |
| **Hannon 2011 notes / groups.io msg 12611** (login-only) | Exact wording of "simple … key word/s", "regenerative function"; could name a generator | encode the generator in `tools/keygen.py`; screen with `feasible()` (fixed/vig1/beau1), `selfmodel.py`, then the class-C SA |
| **Any concrete key stream idea** | Decidable (classes A-C) | `tools/latin_filter.py` → `tools/keygen.py feasible` → `workers/w-transkey/scripts/selfmodel.py` → `workers/w-synth/scripts/sa.c` (two alphabets) → `tools/crib_check.py` |
| **A full candidate plaintext** | — | `tools/crib_check.py`. Paradigm's $1 checker: **never submit without Stas's approval** |
| Physical evidence of a carving error at 22, 25, 32, 66, 67, 72 or 74 | revives specific periodic or generator configs | `tools/errtol.py`; error-tolerant reruns (task 2) |

## 6. Proposed next research tasks (ranked by expected information gain; none repeats refuted work)
1. **Decide class C by full-text annealing of every existing two-alphabet survivor stream.**
   - Inputs: the 258 keygen survivors (k4_hits.jsonl.gz), the 46 Gromark primers (b10/5, b10/4, b8/5), the 12.8k route/overlay Latin-gate passers, and a sample of the 281k transkey Latin passers. Process them in order of motivation.
   - Method: `workers/w-synth/scripts/sa.c` (NALPH=2, key stream fixed, λ=25, R=8-16). Rewrite it to be crib-exact for speed.
   - Test: a stream is a hit iff its best crib-feasible score is above the K4 random-stream null maximum (−498, n=9 feasible of 40) **and** within the English control range (≥ −440), then crib_check.
   - Falsified: all streams stay in the null band, which closes H-1404, H-1804 and H-601 instead of leaving them "untestable".
   - Calibration first: 20 planted survivors-style streams must be recovered at ≥90%.
2. **Error-tolerant rerun of the exact generator screens** (w-keygen F0-F5, w-route, w-transkey), under fixed tableaux, vig1/beau1 and Q3-proper.
   - Error budget: ≤1 wrong crib letter (24 deletion sets), or BERLINCLOCK shifted by ±1.
   - Test: count hits against a shuffled-CT control run through the same pipeline. Expect chance hits ≈ N·24·sel(23 cribs); compute this before running.
   - Falsified: hits are at the control rate and no hit decrypts to English. A survivor that decrypts to English beyond the null is a candidate.
   - This closes the largest loophole in the ~21M exact nulls.
3. **Single-alphabet residual autokey models: CT-autokey survivors (mixed alphabet, Vig L ∈ {37,41,46,60,64,67,69-73}, Beau L ∈ w-mask list) and PT-autokey Beau L=6-8, 10-12.**
   - All are class J/K (≈88 unknown bits, identifiable).
   - Method: for CT-autokey, the vig1 known-key SA (key = C shifted by L). For PT-autokey, z3 enumeration of crib-feasible alphabet fragments followed by chain decryption, or SA with the crib chain enforced.
   - Falsified: the best decrypt for every L lies inside a shuffled-K4 null. A hit means English beyond the null.
   - Low prior (content-dependent key versus K5), but cheap and decisive.
4. **K5-readiness benchmark.** Build synthetic K4/K5 pairs: same plaintext at 64-74, alternate-ending text elsewhere, under classes B, C and D. Run k5_depth.py plus a depth annealer, and measure recovery.
   - Test: recovery rate per class at 97+97 letters.
   - Falsifiable prediction (this map): classes B and C recover; class D with two alphabets is marginal.
   - Result: the team knows within hours of release which models K5 can settle.
5. **Information acquisition through the user's device or a browser session (needs Stas):**
   - (a) Fetch the NSA 2007 KRYPTOS Summary.
   - (b) Transcribe the pre-1997 Weltzeituhr faces from dated photos, then run face_test.py.
   - Each is decisive for its own question at low cost. Prior for H-802 is low; the NSA summary may prune the open list.

Deprioritized, because the map shows they cannot succeed with 97 letters: more SA on Q4 p≥30, GEN periodic, OTP-like masks (D), probable-word dragging, more running-key texts under standard tableaux, and periodic Quagmire I-III searches without a keyword-alphabet restriction.
