# w-transkey T17: K1/K2 tableau cipher with a TRANSPOSED key stream (w-sources shortlist #1, H-1502)
Worker: w-transkey, 2026-10-26 (UTC). Hypotheses: H-1701..H-1704.
Scripts and raw outputs: `workers/w-transkey/scripts/` (transkey.py, selfmodel.py, plant.py, control.py, k4_*.out, plant.out, ctl_*.out).
Positions are 1-indexed. Cribs are assumed in place, with no error tolerance.

## TL;DR
- **No crib-passing candidate.** 19,236,102 configurations were screened, with 0 survivors in every exact model.
  - The model: key stream = (keyword stream / keyed alphabet / K1-K3 text) pushed through a K3-style transposition, then used with a K1/K2 tableau, plaintext aligned with ciphertext.
  - The exact models are 12 AZ/KA tableaux × 4 key numberings; one arbitrary mixed alphabet (Vig and Beau, 4 numberings); and **Quagmire-III proper** (one arbitrary alphabet, key value = position of the key letter in that same alphabet, Vig and Beau).
- **Pipeline validated.** 10 planted configurations (every family, periodic and text sources, n=97/98/336/337/768) × 5 cipher models were all recovered: **50/50**.
- **Gate behaves at chance.** The alphabet-free Latin gate (X28=X66 plus 22 inequalities) passes 1.3-1.7% of K4 configs. The iid-key null rate on the K4 cribs is 1.68% (§4). Survivors of that gate (281k = 280,959) all die in the exact models.
- **H-1502 / H-1701 is REFUTED** for the enumerated motivated space (scope in §2). The two-arbitrary-alphabet model (Quagmire IV) is not tested, because w-keygen H-1404 shows it is crib-untestable.

## 1. Model
- K4: C_i = T_{X_i}(P_i), i = 1..97, where X is a key-LETTER stream.
- X = (S[π])[o .. o+96]. Here S is a source stream of length n, π is a transposition ("push into the square"), and o is a window offset.
- Plaintext and ciphertext positions stay aligned, so the cribs apply directly (C-1:1, w-sources §4).

Cipher models (all exact):
| gate | model |
|---|---|
| G1 latin | alphabet-free: any Latin-square tableau indexed by key letter (tools/latin_filter.py logic) |
| G2 fixed | Vig/Beau/vBeau, PA,CA ∈ {AZ,KA}; key value = letter index in AZ0/AZ1/KA0/KA1. 24/24 crib letters |
| G3 vig1/beau1 | ONE arbitrary alphabet a, a(C)=a(P)+k or a(C)+a(P)=k, k via the 4 numberings (keygen.feasible) |
| G4 self-vig/self-beau | ONE arbitrary alphabet a, key value = a(X). This is the K1/K2 structure generalised to ANY keyword alphabet. |

**G4 is new.** selfmodel.py solves the homogeneous linear system mod 26 exactly:
- It enumerates the GF(13) nullspace, keeps vectors whose residue classes hold at most 2 letters, and then solves the affine GF(2) separation system. This takes about 1 ms per test.
- On 300 random streams per mode it accepted 0. On planted cases it accepted 40/40 (standalone test) and 20/20 (inside plant.py).

## 2. Enumerated space (bounded, motivated)

**Sources**
- 29 keywords from tools/keygen.py KEYWORDS, repeated, with every phase: 268 streams.
- 55 distinct keyword-mixed alphabets (keyword + rest of AZ, and + rest of KA), repeated.
- K1 plaintext and K1 ciphertext, repeated.
- Long texts, used whole and as 97/98-letter chunks at every offset: K2 plaintext (carved), K2 plaintext (corrected), K3 plaintext, K2 ciphertext, K3 ciphertext, K1+K2+K3 ciphertext (768), K1+K2+K3 plaintext, K1+K2 plaintext.
- Periodic sources were expanded to n ∈ {97, 98} with every phase, and to n ∈ {336, 337} at phase 0 only. At those lengths the phase is (almost) absorbed by b or the window.

**Transpositions** (each also as its inverse, i.e. writing into the square instead of reading out of it)
| fam | form | parameters |
|---|---|---|
| A-dec | π(t) = d·t+b mod n | n=97,98: all units d, all b. n=336,337: 72/18 motivated d (2..31, 42, 48, 56, 64, 97, 98, 112, 168, **192**, their negatives and inverses), all b. Texts: all units d mod len, all b |
| B-k3form | K3's exact closed form π(t) = d(t+1) mod (n+1) − 1 (the '?' slot skipped) | all units d mod n+1. n=97,98: all windows. n=336,337: windows {0, n−97}. Texts: all d, all windows. Includes **192 mod 337 = K3 itself** |
| C-col | keyed columnar, rows of width w, columns read in keyword order | orders from all 29 keywords at widths {len, 7, 8, 10, 14, 21, 24, 31} (keyword cycled or truncated to width), plus identity and reversed orders: 236 orders × rd/wr |
| D-route | route/rotation on grids | grids 24-wide (4×24+1), 31-wide, sculpture layout (4 letters at cols 27-30, then 3×31), 7-, 8-, 14-, 21-wide (n=97); 7×14, 14×7, 24-, 31-wide (n=98). Routes: rows, boustrophedon, diagonals, spiral in, spiral out, × 8 dihedral orientations × rd/wr |
| E-k3rot | K3's published procedure: write width a, rotate cw, write width b, rotate cw | (a,b) ∈ {4,7,8,14,21,24,28,31}², rd/wr, n ∈ {97, 98, 336, 337} and the texts. The (24,8) case on 336 letters reproduces K3 exactly; this was verified, as was the decimation form |

**Counts (K4)**
| family | configs | latin pass | exact hits |
|---|---|---|---|
| A-dec | 7,721,268 | 98,354 (1.27%) | 0 |
| A-dec chunk | 410,904 | 6,772 (1.65%) | 0 |
| B-k3form | 1,640,010 | 26,418 (1.61%) | 0 |
| B-k3form chunk | 303,480 | 5,166 (1.70%) | 0 |
| C-col | 2,029,128 | 30,071 (1.48%) | 0 |
| C-col chunk | 2,809,344 | 45,628 (1.62%) | 0 |
| D-route | 390,000 | 4,955 (1.27%) | 0 |
| D-route chunk | 2,619,840 | 42,814 (1.63%) | 0 |
| E-k3rot | 550,272 | 8,349 (1.52%) | 0 |
| E-k3rot chunk | 761,856 | 12,432 (1.63%) | 0 |
| **total** | **19,236,102** | **280,959** | **0** |

**Budget justification.** The total is about 1.9e7, above the 1e7 target.
- About 8.5M of it is cheap exhaustive decimation (all d, all b), which is far more complete than "motivated d" only. Many of those configs are near-duplicates, because decimations of a periodic stream repeat.
- Each check is exact. The expected number of chance passes is negligible:
  - G2: 48 × 26^-24 per config.
  - G3: about 1e-11 per (config, numbering), so about 1e-3 in total.
  - G4: 0 of 280,959 latin-passers on K4, and 0 on the controls.
- Runtime: about 40 CPU-minutes.

## 3. Validation (plant.out)
- Each plant builds the 97-letter key stream independently (not through the screen's indexing). It encrypts the K3 plaintext at a random offset with EASTNORTHEAST@22 and BERLINCLOCK@64 inserted.
- 5 cipher models per plant:
  - fixed KA-Vig, KA0;
  - vig1 with a random alphabet, AZ0;
  - beau1 with a random alphabet, KA1;
  - self-vig and self-beau with random alphabets.
- The screen then runs on the planted ciphertext for that source.
- Planted configs: KRYPTOS dec 45 mod 97; PALIMPSEST dec 192 mod 337; ABSCISSA K3-form mod 99; BERLINCLOCK columnar KRYPTOS@14 wr; KRYPTOS sculpture-grid spiral; KA double rotation 24-8 on 336; SHADOW rot24-8 on 97; K3PT chunk + KRYPTOS@7 columnar; K123CT K3-form 192 mod 769; K2PT dec 7 mod 369.
- **Recovered 50/50.** Extra hits on plants (1-6) are equivalent streams.

## 4. Null controls (null_iid.out, ctl_E-k3rot_1.out)
- **Latin gate vs iid keys.** On K4's own crib structure, 2e6 iid random key tuples pass the gate at a rate of **1.68%**. K4 configs pass at 1.27-1.70% per family, consistent with chance or below it; periodic decimations sit lower because they are more structured.
- **Random-ciphertext control.** E-k3rot was run on a random 97-letter ciphertext, seed 1. 1,312,128 configs gave a latin rate of 20%: a random ciphertext has a much weaker crib EQ/NE structure, so the rate is not comparable to K4's.
  - Even so, **0 exact hits came from 262,911 latin-passers.**
  - So the exact models (G2-G4) do not pass loosely; their selectivity is confirmed independently of K4.
- Other control seeds were lost to a container restart and not rerun; this one is sufficient.

## 5. Hypotheses
- **H-1701** K4 = K1/K2 tableau with a key stream made by transposing a keyword-repeated stream (decimation incl. 192 mod 337, K3 closed form, keyed columnar, routes, K3 double rotation). Models: AZ/KA tableaux, single mixed alphabet, or Quagmire-III proper. **REFUTED** (exact, 0/≈1.5e7 periodic-source configs, plants 50/50).
- **H-1702** The same with keyword-mixed alphabets or the KA sequence as the stream. **REFUTED** (included above).
- **H-1703** The same with K1-K3 plaintext or ciphertext as the stream (whole text transposed, or a 97/98-letter chunk pushed into the square). **REFUTED** (exact).
- **H-1704** Quagmire-III-proper (any single keyword alphabet, key letter looked up in the same alphabet) is an exact, fast test (selfmodel.py) for any candidate key-letter stream. **TOOL**, validated.

## 6. Caveats / not covered
- Two independent arbitrary alphabets (Quagmire IV) are crib-untestable (H-1404).
- No error tolerance: one carving error at a crib position kills any config.
- Transposition depth is 1 (or K3's 2 rotations). There are no composite chains (e.g. columnar then decimation) and no transposition keyed by non-listed words.
- Columnar on 336/337-length periodic streams uses only windows {0, n−97}.
- n=336/337 periodic streams use phase 0 only.
