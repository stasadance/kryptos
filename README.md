# Kryptos K4

Working repository for a methodical attempt on Kryptos K4.

## Method
One hypothesis at a time:
1. **Plan** — pick the top item in `PLAN.md`; state the claim, the evidence it comes from, and what it predicts.
2. **Test** — design the smallest exact test that can falsify it (no open-ended key searches). Validate the test on a planted positive control first.
3. **Record** — write the result in `JOURNAL.md` (one entry per iteration), update `hypotheses/`.
4. **Refine** — derive the next hypothesis from what was learned; re-rank `PLAN.md`.

## Layout
- `PLAN.md` — current state of knowledge and ranked hypothesis queue
- `JOURNAL.md` — iteration log (hypothesis → reasoning → test → result → next)
- `data/` — ciphertext, cribs, sourced facts
- `hypotheses/log.md`, `hypotheses/ruled_out.md` — every hypothesis and exclusion with evidence
- `findings/` — background reports from the first survey phase (2026-10-26)
- `tools/` — verified scripts (`crib_check.py`, `keygen.py` exact crib solver, etc.)
