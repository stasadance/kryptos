# w-synth T21: identifiability map and project consolidation (2026-10-27 UTC)
Worker: w-synth, round 7. Hypotheses: H-2101..H-2104. The main deliverable is /STATUS.md, which holds the identifiability table (§3), the ruled-out robustness table (§2), the new-information playbook (§5) and the proposed tasks (§6). This file records the method and the raw experiments.
Scripts: workers/w-synth/scripts/ (prep.py builds the quadgram table and measures entropy; sa.c is a two- or one-alphabet annealer with a known or periodic key; drv.py runs controls; null3.py runs K4 under random relation-satisfying streams). Raw results: workers/w-synth/r_*.jsonl.

## 1. Method (unicity with cribs)
- Data budget B = 24·log2(26) + 73·D.
  - Crib letters fix the CT|key relation completely, worth 4.70 bits each, 112.8 bits in total.
  - Unknown letters contribute the plaintext redundancy D.
- A class is identifiable when the key entropy H(K) (after gauge symmetries: Q4 loses ~4.7 bits for the common shift, Q3 likewise) is well below B.
- D values:
  - True English: D ≈ 3.2-3.5 (Shannon), giving B = 346-368 bits.
  - Practical value for a quadgram objective, measured here by training on PG2600 and testing on 500k letters of PG1342 (order-k conditional entropy, add-0.5): H1 4.18, H2 3.64, H3 3.22, H4 2.84 bits/letter, so D4 = 1.86 and B_q = 248.6 bits.
- The random-cipher model is only an approximation. Local key parts need a local check: a periodic class shift needs (97/p)·D > 4.7 bits, which holds for p < ~38 under true English and p < ~20 under quadgrams. This matches where w-anneal sees spurious optima.
- GEN periodic: the effective key is Σ_r log2(26!/(26−d_r)!) over the distinct CT letters d_r per class. Computed on K4: p=8: 373, p=11: 373, p=13: 407, p=16: 406, p=24: 434, p=30: 431, p=41: 433 bits. All exceed B, so GEN is not identifiable.

## 2. Synthetic experiments (97 letters, cribs inserted at K4's positions, held-out PG1342 windows)
| experiment | n | result |
|---|---|---|
| one alphabet (Vig form), key stream known, λ=5, R=4×1M | 12 | 12/12 recovered, accuracy 1.00, found = true score |
| two independent alphabets, key known, λ=5, R=8×3M | 12 | 6/12 recovered. The failures never reached crib feasibility (penalty too weak) |
| same, λ=25, R=16×3M | 12 | **11/12 recovered** (accuracy 0.90-1.00). The remaining one never reached feasibility at a good score (−525, acc 0.12). Found ≥ true only with accuracy ≥0.95, so no spurious optimum |
| NULL: K4 ciphertext, 40 random key streams satisfying the two-alphabet crib relations (k66=k28, k33=k24+k34−k29), λ=25, R=8×3M | 40 | 9 crib-feasible (injectivity rate ~0.3, as w-keygen predicts). Best scores −498 to −550, versus English controls −400 to −434. Decrypts are gibberish |
| penalty SA with unknown periodic shifts (Q4 p=8, 12; Q3 p=30, 41) | 32 | never crib-feasible. Uninformative and discarded; w-anneal's crib-exact mode 10 covers Q4 |

**Conclusion (H-2101):** a fixed key stream under two arbitrary alphabets is identifiable from 97 letters. The search succeeds when the cribs are enforced strongly, and wrong streams sit about 65 log10 units below English. The "crib-untestable" label on H-1404, H-1804 and H-601 is therefore a limit of crib algebra only, not of the data. This matches w-anneal's oracle result (posC given, 100% recovery) and its diagnosis that joint periodic-shift plus two-permutation search is the obstacle.

## 3. Cross-checks against team evidence
- **w-keygen:** the single-alphabet selectivity of 1e-11 (≈36.5 bits beyond 4 relations) and the two-alphabet selectivity of 5.8e-4 (≈10.7 bits) match the budget picture. Cribs fix 113 bits; one alphabet costs 88, two cost 172.
- **w-anneal T19:** 0/294 Q4 controls recovered. At p=16-28 the true score exceeds the found score (search-limited, predicted MARGINAL). At p≥30 spurious ≥ true (predicted NOT, since H ≥ 308 > 249 = B_q). The crossover sits where H(K) crosses B_q to 1.2·B_q, consistent with the map.
- **w-probable:** the vacuity proof H-2001 is the exact statement that class D has H(K) > B.
- **w-errtol:** power ≤0.04 at GEN/Q4 p=10, consistent with H(GEN p10) > B.

## 4. Hypotheses
- H-2101: two-alphabet known-stream models are full-text identifiable (SUPPORTED, synthetic).
- H-2102: GEN periodic p≥8, Q4 p≥30, Q3 p≥41 and unstructured position keys are information-limited at 97 letters + 24 cribs (SUPPORTED, budget + w-anneal).
- H-2103: residual single-alphabet autokey models (CT-autokey SAT L; PT-autokey Beau L=6-12) are identifiable, and earlier failures were search failures (OPEN, task 3).
- H-2104: the exact generator nulls (~21M configs) are error-fragile. A single crib-position carving error would hide a true hit (OPEN, task 2).
