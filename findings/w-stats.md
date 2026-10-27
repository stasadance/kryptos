# w-stats — T4: statistical characterization of K4 (97 chars) and what it excludes
Worker w-stats, 2026-10-26 (UTC). Script: `tools/k4stats.py` (numpy; seed 1; 200,000 Monte Carlo trials per null; ~35 s).
Reproduce: `python3 tools/k4stats.py --corpus pg1661.txt pg2701.txt --trials 200000 --maxp 32 --compare`
(English reference = Project Gutenberg #1661 Sherlock Holmes + #2701 Moby Dick, letters only, 1,386,631 letters, kappa_E = 0.0652).
All p-values are Monte Carlo tail proportions (k+1)/(N+1); with N=200k the smallest reportable value is 5.0e-06 (= "none of 200k").

## Nulls used (and why)
- **perm**: random permutations of K4's own letters. Keeps letter counts, destroys position structure → right null for repeats, autocorrelation, periodicity, layout widths.
- **uniform**: 97 iid uniform letters → "looks random" null for IC/frequencies.
- **English**: random contiguous 97-letter windows of real English. A transposition (and any monoalphabetic substitution) leaves IC unchanged, and for a period-p polyalphabetic cipher with *arbitrary* per-column alphabets (applied after any transposition) the pooled column IC equals the plaintext's lag-kp coincidence rate → this null gives the power/exclusion column for those hypotheses.
- No keyspace search anywhere. Deterministic crib tests use facts/cribs.md (22-34 EASTNORTHEAST, 64-74 BERLINCLOCK).

## Sources
- Physical layout & K1-K3 ciphertexts: Elonka Dunin's sculpture transcript https://elonka.com/kryptos/transcript.html (mirrors Gwyn/Washington Post transcription; she notes rows could not be lined up exactly). Same K4 line breaks in Wikipedia https://en.wikipedia.org/wiki/Kryptos . Segmenting gives K1=63, K2=369, K3=336 letters (standard counts) and K4 = facts/ciphertext.txt exactly.
- Published stats cross-check: R. Bean, "Cryptodiagnosis of 'Kryptos K4'", HistoCrypt 2021, https://ecp.ep.liu.se/index.php/histocrypt/article/view/153 (code: https://github.com/RichardBean/k4testing). Bean: IC = 336/97/96 = 0.03608; width-21 vertical bigram repeats = 11, permutation p ≈ 1/6,750; doublets BB QQ SS ZZ TT in one column at width 7; ACA seriated Playfair IC 0.048±0.003. **All three reproduced here** (0.03608; 11 repeats, p = 1.6e-4 ≈ 1/6,250; 5 doublets in one column).

## Physical layout on the sculpture (Elonka transcript, cipher side, last 4 rows)
```
ECDMRIPFEIMEHNLSSTTRTVDOHW?OBKR     <- K3 ends ...DOHW, '?' , K4 starts OBKR at cols 28-31
UOXOGHULBSOLIFBBWFLRVQQPRNGKSSO     31
TWTQSJQSSEKZZWATJKLUDIAWINFBNYP     31
VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR     31
```
4 + 31 + 31 + 31 = 97. Physical column of K4 index i (0-based) = (i+27) mod 31, so all column/vertical statistics at the sculpture layout are exactly the width/period-31 statistics below. Other cipher-side rows vary 29-33 letters, so no wider regular grid exists.

## 1. Letter frequencies and IC
Counts: A4 B5 C2 D3 E2 F4 G4 H2 I4 J3 K8 L4 M1 N3 O5 P3 Q4 R4 S6 T6 U6 V2 W5 X2 Y1 Z4 — all 26 letters present. Top: K8, U6, S6, T6. E only 2.
| statistic | K4 | uniform null (mean, sd) | English null (mean, sd) | p (uniform) | p (English) |
|---|---|---|---|---|---|
| IC (kappa) | 0.03608 (x26 = 0.94) | 0.03847, 0.00282 | 0.06459, 0.00661 (min of 200k: 0.04446) | P(≤)=0.215 | P(≤) < 5e-06 |
| chi² vs English freqs | 603.9 | 815.7 | 25.3 (99.9% 155.8, max 490.4) | P(≥)=0.69 | P(≥) < 5e-06 |
| chi² vs flat (df 25) | 19.1 | — | — | P(≥)=0.81 | — |
K4's single-letter statistics are indistinguishable from random letters and ~4 sd below English.

## 2. Doubled letters, autocorrelation
- 6 doublets: BB@19 QQ@26 SS@33 SS@43 ZZ@47 TT@68. perm mean 3.46, P(≥6)=0.13; English mean 3.20, P=0.098. Not significant by itself.
- Autocorrelation shifts 1-48: max at lag 7 (9 coincidences vs 3.2 expected, z=3.29); family-wise over 48 lags P=0.138 → **no significant period by autocorrelation**. Lag-7 hits: O1/8 O8/15 B13/20 L16/23 S33/40 K46/53 P66/73 D77/84 K87/94.
- Doublets in one column: at width 7, 5 of 6 doublets start in the same column (pos ≡ 5 mod 7). perm P=6e-4; family-wise over w=2..21 P=0.0041. **Post-hoc** (the pattern was noticed before tested; cf. Bean citing Good on this).

## 3. Kasiski / repeats
- Repeated bigrams (10 types): DI 56/84 (d28), EK 45/93 (48), FB 18/62 (44), GK 31/86 (55), HU 10/89 (79), KZ 46/78 (32), QS 39/42 (3), SO 14/34 (20), SS 33/43 (10), TJ 51/81 (30). Spacings share no common factor (gcd of all = 1; only 28,32,48,10,20,30,44 even). perm mean 5.5, P(≥10)=0.031; English windows mean 17.1.
- **No repeated trigrams or longer** (perm mean 0.20 types, English 5.1). Kasiski gives no period.

## 4. Periodic column IC, p = 1..32 (pooled over columns)
P(≥|perm) tests for a period signal; P(≤obs|English) is the probability an English plaintext under a period-p (arbitrary-alphabet) polyalphabetic cipher would give a column IC as low as K4's.
| p | col IC x26 | P(≥|perm) | P(≤obs|English, period p) |
|---|---|---|---|
| 1 | 0.94 | 1.00 | <5e-06 |
| 2 | 0.91 | 0.63 | <5e-06 |
| 3 | 0.77 | 0.97 | <5e-06 |
| 4 | 0.85 | 0.77 | <5e-06 |
| 5 | 1.02 | 0.31 | 9.4e-04 |
| 6 | 0.78 | 0.87 | 2.0e-05 |
| 7 | 1.08 | 0.23 | 0.012 |
| 8 | 0.67 | 0.94 | 4.0e-05 |
| 9 | 0.66 | 0.94 | 5.5e-05 |
| 10 | 1.17 | 0.18 | 0.065 |
| 11 | 1.09 | 0.29 | 0.047 |
| 12 | 0.60 | 0.94 | 3.5e-04 |
| 13 | 0.58 | 0.95 | 5.6e-04 |
| 14 | 0.90 | 0.59 | 0.023 |
| 15-17 | 0.90-0.97 | ≥0.49 | 0.040-0.045 |
| 18 | 0.48 | 0.96 | 1.6e-03 |
| 19-22 | 0.77-1.02 | ≥0.46 | 0.026-0.11 |
| 23 | 0.49 | 0.93 | 7.9e-03 |
| 24 | 0.53 | 0.91 | 0.013 |
| 25 | 1.48 | 0.13 | 0.44 |
| 26 | 0.39 | 0.96 | 8.0e-03 |
| 27-30 | 0.81-1.06 | ≥0.45 | 0.08-0.20 |
| 31 (sculpture width) | 1.49 | 0.18 | 0.48 |
| 32 | 0.79 | 0.70 | 0.12 |
Best period by perm p is 25 (P=0.135); family-wise over p=1..30 P=0.94 → **no period signal at all**. Power drops past p≈13 (columns of ≤7 letters), so periods ≥14 are weakly tested.
Sanity check (method validation): same code finds K1 period 10 (PALIMPSEST; p10 x26=2.48, p20 3.39) and K2 period 8 (ABSCISSA; p8 1.79) as top periods, and K3 IC 0.0662 (English-like, transposition).

## 5. Width layouts (vertical repeated bigrams, Bean's metric)
| width | repeats | perm mean | P(≥) |
|---|---|---|---|
| 21 | 11 | 3.49 | 1.6e-04 |
| 10 | 9 | 4.53 | 0.023 |
| 7 | 9 | 4.86 | 0.036 |
| 31 (physical rows) | 3 | 2.65 | 0.51 |
Family-wise over w = 2..48: P = 0.0047. The physical sculpture layout (31 wide) shows **nothing** (vertical bigrams P=0.51, column IC P=0.18). The width-21 anomaly survives a 47-width correction but is still post-hoc; Bean shows it is ~1-in-10 under a base-2 Gromark key, so it is weak evidence for a structured key, not for transposition.

## 6. Deterministic crib consequences (exact; no statistics)
- **Pure transposition impossible**: cribs need 3 E's (EAST, NORTHEAST, BERLIN), K4 has only 2. (Also IC/chi² above, p < 5e-06.)
- **Monoalphabetic substitution (no transposition) impossible**: ct Q (pos 26, 27) must decrypt to both N and O.
- **Periodic polyalphabetic with arbitrary per-column alphabets (Vigenère, Beaufort, variant, Quagmire I-IV, Porta, keyed alphabets…), no transposition, cribs at stated positions**: inconsistent for p ∈ {1-7, 9, 10, 14, 15, 17, 21, 25, 34, 42, 43, 45, 50} (e.g. p=7: ct V must map from T (pos 25) and L (pos 67) in the same column). Consistent for 8, 11-13, 16, 18-20, 22-24, 26-33, 35-41, 44, 46-49, 51-97.
- Self-encrypting crib positions: 33 (S→S) and 74 (K→K) → excludes ciphers that never map a letter to itself (e.g. standard Playfair as noted by Bean, Enigma-like rotor without fixed points).
- Combined with §4 (α=0.01): period-p polyalphabetic (no transposition) survives only for p ∈ {11, 16, 19, 20, 22, 24, 27-32} within 1..32, plus crib-consistent p ≥ 33 (which are near-running-key; IC test has no power there). At α=0.001 add 18, 23, 26.
- With a transposition **before** a periodic substitution, cribs no longer constrain positions but §4's English column has full force: excluded at p < 0.001 for p ∈ {1,2,3,4,5,6,8,9,12,13}; at p<0.01 also 18, 23, 26.

## 7. K1-K4 comparison
| section | n | IC | x26 | chi²/n vs English | doublets (perm exp.) | top pooled periods (x26) |
|---|---|---|---|---|---|---|
| K1 | 63 | 0.0379 | 0.99 | 9.92 | 1 (2.3) | p20 3.39, p10 2.48 |
| K2 | 369 | 0.0455 | 1.18 | 9.06 | 21 (16.7) | p8 1.79, p24 1.76, p16 1.71 |
| K3 | 336 | 0.0662 | 1.72 | 0.05 | 18 (22.2) | (none meaningful; English IC) |
| K4 | 97 | 0.0361 | 0.94 | 6.23 | 6 (3.5) | p25 1.48 (n.s.) |
K4 is flatter than K2 (IC 0.036 vs 0.046) and lacks K1/K2's clear period peak even though K1 (63 letters, shorter than K4) shows its period clearly. K4 is unlike K3 (not a transposition of English).

## Conclusions (falsifiable)
1. K4 single-letter statistics are consistent with uniform random letters (IC P=0.22, flat chi² P=0.81) and inconsistent with English under any transposition and/or monoalphabetic substitution (P<5e-06 on both IC and chi²). Falsified if a plaintext of English-like letter frequency is shown to map to K4 by transposition + monoalphabetic substitution only.
2. No periodicity detectable p=1..32 (family-wise P=0.94); K1/K2 periods are detected by the same code. Any short-period (≤13) periodic polyalphabetic, with or without prior transposition, is excluded except p=7, 10, 11 statistically, and 7, 10 are killed by the cribs (no transposition), leaving p=11 only among p≤13.
3. Two positional anomalies survive multiple-width correction but are post-hoc: width-21 vertical bigrams (P=1.6e-4; FW 0.0047) and width-7 doublet alignment (P=6e-4; FW 0.0041). The sculpture's own 31-wide line layout carries no signal.
4. No repeated trigrams; Kasiski uninformative.
5. Not excluded by statistics: non-periodic polyalphabetics (running key, autokey, Gromark/Vimark, progressive keys), periodic with long period (≥14) or crib-consistent mid periods, homophonic/fractionating/multi-stage systems that flatten IC, and periodic substitution **followed by** transposition (IC tests have no power on it).

Caveats: English-window null assumes ordinary English plaintext statistics; a deliberately skewed plaintext (nulls, padding, unusual words) weakens §1 and §4 power somewhat but cannot remove the deterministic crib results. Crib-based results assume facts/cribs.md positions are exact and no transposition across those positions.
