# w-route T18: key stream read off a physical Kryptos grid along a route (shortlist #2, H-1504)
Worker: w-route, 2026-10-26 (UTC). Hypotheses: H-1801..H-1804.
Scripts, checkpoints and plant log: `workers/w-route/scripts/` (route.py, lsolve.py, run_ck.py, plant.py, null.py, layout.txt, plant.out) and `workers/w-route/ckpt/` (one JSON per grid and phase, with counts and hits; all hit lists are empty).
Positions are 1-indexed.

## TL;DR
- **No crib-passing candidate.**
  - 795,830 route/offset key placements were tested: 659,842 cyclic route streams × every start offset, plus 135,988 panel overlays.
  - Grids: the carved tableau, the carved cipher panel, the two side by side, the ideal KA tableau, and the Morse panels.
  - Models: 12 Vig/Beau/vBeau tableaux with PA, CA ∈ {AZ, KA}, under 4 key-letter numberings (AZ0, AZ1, KA0, KA1). Then vig1 and beau1 (one arbitrary mixed alphabet with a numeric key, `keygen.feasible`, exact).
  - New exact letter-level K1/K2 models: vig1L a(C)=a(P)+a(K) and beau1L a(C)+a(P)=a(K), where the key letter sits in the same unknown alphabet.
  - **Result: 0 / 0 / 0 / 0 / 0 hits** (fixed / vig1 / beau1 / vig1L / beau1L).
- **The Latin gate is necessary only, not sufficient.** It is alphabet-free (any Latin tableau, incl. two arbitrary alphabets with letter keys).
  - It passes 11,752 / 659,842 stream placements (1.78%). Shuffled-stream null: 1.67%. Overlays pass 1,089 / 135,988 (0.80%).
  - These are chance-level. The two-alphabet route model is crib-untestable, as in w-keygen H-1404.
- **Pipeline validated.**
  - Planted configurations were recovered 20/20 (`plant.out`). There were 4 per model: 3 routes and 1 overlay; models fixed KA-Vig, vig1, beau1, vig1L and beau1L.
  - The letter-level exact solver `lsolve.py` was checked three ways:
    - 120/120 planted SAT instances found;
    - agrees with z3 on 120 random instances;
    - decides all 24 instances where z3 timed out at 15 s (all UNSAT).
- **Selectivity.** vig1 passes a random key at ≈1e-11 (w-keygen H-1406). The fixed tableaux need 24 exact equalities. The expected chance hits over this budget are ≪ 1, so a null result is decisive for these models.

## 1. Grids (exact carved layouts)
Source: Elonka Dunin's transcript https://elonka.com/kryptos/transcript.html. It mirrors Gwyn's Washington Post transcription, was hand-verified in 2002, and the "extra L" was added in 2003. It was parsed verbatim into `layout.txt` (56 lines). There are 28 cipher-panel rows and 28 tableau rows:
- tableau top half: header + A..M;
- tableau bottom half: N..Z + footer.

Checks:
- Cipher panel letters: 865 = 63 + 369 + 336 + 97.
- The K4 cells reproduce facts/ciphertext.txt exactly (asserted in code).
- Row widths are ragged (29-33). Elonka notes that the rows "could not be lined up the same as on the sculpture".

| grid id | content | variants |
|---|---|---|
| TAB_h{0,1}l{0,1}x{0,1} | right-hand tableau as carved | with/without the header+footer rows ` ABCD…ABCD`; with/without the row-label column; with/without the extra L in row N (`NGHIJLMNQUVWXZKRYPTOSABCDEFGHIJL`, 32 chars). 8 grids, 780-867 letters |
| CIP_q{0,1}{L,R} | left cipher panel K1-K4 in carved rows | '?' kept as a hole or squeezed out; rows left- or right-aligned (column routes depend on alignment). 4 grids, 865 letters |
| SCULPT_x{0,1} | cipher row r + tableau row r side by side (speculative) | extra L kept/dropped. 1,731-1,732 letters |
| KA26 | ideal 26×26 KA tableau (uncarved) | for spirals; linear walks were already dead per w-keygen F6 |
| MORSE_E / MORSE_noE | 12 Morse lines in the rumkin/Gillogly reading order (SOS, RQ, LUCIDEEE, MEMORYE, EESHADOWEE, FORCESEEEEE, TISYOUR, POSITIONE, EDIGETALEEE, INTERPRETATI, EEVIRTUALLYE, EEEEEINVISIBLE), with/without filler E | https://rumkin.com/reference/kryptos/k0/ |

## 2. Routes and offsets (counted in advance; all bounded)
- **Route set.** The grid is placed in its bounding frame, with holes for blanks, '?', and ragged ends. Each of the 8 dihedral images (rotations 0/90/180/270, each with or without a horizontal flip) is read 5 ways:
  - rows;
  - row boustrophedon;
  - diagonals;
  - diagonal boustrophedon;
  - clockwise inward spiral.
- Each reading is taken forward and reversed. Reversal gives the outward spirals and the routes from the other corners.
- This covers rows and columns from every corner, both diagonal families in both directions, and spirals in and out from all 4 corners in both senses.
- Duplicate streams are removed per grid, leaving **774 distinct streams**.
- **Offsets.** Every start offset, cyclic: K4 position i takes stream[(o+i-1) mod n]. All motivated alignments are therefore included as special cases:
  - the K of KRYPTOS in the tableau;
  - O of OBKR (the start of K4 on the panel);
  - the extra L;
  - the Y, A and R of YAR.
  - 659,842 placements.
- **Overlay family (superimposition).** K4's own carved cells (r_i, c_i) are those after "?" in row 25, plus rows 26-28, with '?' kept or squeezed. The key letter is G'[(r_i+dr) mod R, (c_i+dc) mod W] for every dihedral image G' of every non-Morse grid and every torus shift (dr, dc).
  - Placements that land on a hole are skipped.
  - This covers "lay the tableau panel over the cipher panel" and "key K4 with the K1-K3 letters at a shifted panel position".
  - 135,988 placements.

## 3. Cipher models and gates
- **fixed:** for each of the 12 tableaux, the 24 crib positions require exact key values (as in keygen.required_keys). The key letter is converted by AZ0, AZ1, KA0 or KA1. The carved tableau's own convention is plain = header (AZ), key = row label (AZ), cipher = body (KA). That is PA=AZ, CA=KA, AZ numbering, so it is included.
- **vig1 / beau1:** an equality prefilter derived from the CT (k28=k66; k33=k74=0 for vig1; even for beau1), then the exact `keygen.feasible`.
- **Latin gate:** an alphabet-free necessary condition for any Latin-square tableau with letter keys (= tools/latin_filter.py). Its K4 core is X28=X66 plus 22 inequalities.
- **vig1L / beau1L:** extra necessary filters.
  - vig1L: key letter = a⁻¹(0) exactly at the P=C positions, so X33=X74 and that letter is absent from the other crib keys.
  - beau1L: the same unordered {P,C} gives the same key letter; overlapping but different {P,C} gives different key letters.
  - Then the exact backtracking solver `lsolve.py`. It uses unit-multiplier gauge fixing {0,1,2,13} and propagation, and replaces z3, which timed out on 24 beau1L/vig1L instances.

## 4. Results on K4
| family | placements | fixed (×48) | vig1 (×4) | beau1 (×4) | Latin gate | vig1L | beau1L |
|---|---|---|---|---|---|---|---|
| route streams, all grids | 659,842 | 0 | 0 | 0 | 11,752 (1.78%; null 1.67%) | 0 | 0 |
| overlays | 135,988 | 0 | 0 | 0 | 1,089 (0.80%) | 0 | 0 |

Per-grid counts are in ckpt/k4_stream_*.json and ckpt/k4_overlay_*.json. Every grid is 0 in every exact model.

## 5. Hypotheses
- **H-1801 — REFUTED (exact).** The key is the carved tableau, cipher panel, side-by-side sculpture, or ideal KA tableau read along a row, column, boustrophedon, diagonal or spiral route from any corner, under any flip or rotation, at any start offset, under the 12 AZ/KA tableaux or one arbitrary mixed alphabet (numeric key, AZ/KA numbering).
- **H-1802 — REFUTED (exact).** The same routes under the letter-level K1/K2 model (key letter located in the same unknown mixed alphabet, Vig or Beau form).
- **H-1803 — REFUTED (exact) for the same models.** Superimposition: K4's carved cells keyed by the tableau or panel letter at any torus shift of any dihedral image.
- **H-1804 — not testable, chance-level.** Morse panels as a route key. Also dead in all exact models; w-runkey had already covered Morse as a linear running key.
- **OPEN / not covered:**
  - two independent arbitrary alphabets (Latin gate only, chance-level);
  - keyed-column orders (KRYPTOS-order column reading = shortlist #1 / H-1502);
  - decimated or knight-move routes;
  - routes combined with a text transposition;
  - carving errors or omissions (the tests assume error-free cribs at the stated positions);
  - other physical column alignments of the ragged cipher rows beyond left/right.

## 6. Caveats
- Morse line order follows rumkin's page. The physical order on the granite is not documented there.
- SCULPT (side by side) is speculative about the physical adjacency of the panels.
- The run was restarted twice after container restarts. Checkpoints are written per grid, and the final numbers come from a complete checkpointed pass.
