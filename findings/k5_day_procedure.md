# K5-day procedure (from it89, 2026-10-28)

Assumption under test: K5 uses K4's system, with BERLINCLOCK at the same positions (64–74, 1-indexed; Sanborn, Nov 2025).

1. Run `python3 workers/w-k5/k5_depth.py K5CIPHERTEXT`.
   - It shows identical CT runs at the same positions.
   - It shows the key letters at 64–74 under Vig, Beau and vBeau with AZ and KA.
   - If the K4 and K5 key letters match at 64–74, the key is shared and the texts are in depth.
2. **Structured key (classes A, B, C: periodic, progressive, stream library, one or two mixed alphabets).** Rerun every exact screen on K4 and K5 jointly. That gives 2×24 crib letters at the same key positions, plus BERLINCLOCK in K5. Rerun `iterations/it88/sa2.c` (crib-exact class-C annealer) over the joint text. The evidence doubles, so classes that are marginal on K4 alone become decidable.
3. **Unstructured / OTP-like key (class D).** Depth-2 with a per-position key is NOT identifiable with character n-gram models at 97 letters:
   - The key costs log2 26 = 4.70 bits/letter.
   - Two texts supply 2·D = 4.52 bits/letter with the 6-gram (D=2.26, 58M-letter training).
   - Benchmark (iterations/it89): 0/56 planted pairs recovered with the 4- and 6-gram, and found ≥ true in most plants (model-limited).
   - What it needs: a word-level two-text decoder (D ≈ 3+), or probable-word dragging of shared content.
4. Correction to STATUS row P: "IDENTIFIABLE with standard or one alphabet" holds only for a structured key or with a word-level LM. With an unstructured key it is MARGINAL at best.

Tools: iterations/it89/{depth.c,bench.py} (benchmark); tools/lm/build_lm.py (4/5/6-gram LMs, rebuild into /tmp/claude-0/lm).
