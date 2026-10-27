# Plan

_Last updated: 2026-10-27 (it36)_

## Where we are
The first phase (2026-10-26) was a broad survey, summarised in `findings/` and `hypotheses/ruled_out.md`:
- **Facts verified** with sources (`data/known_facts.md`). Cribs: EASTNORTHEAST at 22–34, BERLINCLOCK at 64–74 (1-indexed).
- **Ruled out** (audited, see `findings/w-audit.md`): transposition alone; monoalphabetic; periodic Vigenère/Beaufort/variant (AZ and KRYPTOS alphabets) at every period the cribs reach, even with 1–2 carving errors; autokey; Hill ≤4×4; Gromark with fixed or keyword alphabets; English running keys; keyword-driven key generators; keys read off the sculpture's grids; K3-style transposed keys.
- **What is left:** a key that does not depend on the plaintext, under one or two unknown alphabets. The cribs alone cannot test that model (`findings/w-probable.md`, `findings/w-anneal.md`). Progress needs a *specific* key hypothesis drawn from evidence, or new data (K5).

Lesson from phase 1: wide sweeps gave negatives but no direction. From here on, each step is one reasoned hypothesis.

## Session 2026-10-27 (it21–28) summary
- Sources: Big Tech Day 2013 transcript (flip-the-chart quote = K1/K2 worksheets), full NSA FOIA set via archive.org (`data/sources/nsa/`), WaPo 14 Jan 1990 "modern system" half (K3+K4).
- New exact tools: `iterations/it23_scan.py` (numba; any fixed key stream under one unknown alphabet in 45 role/form models, false-pass <1e-7 on K4), `iterations/it28b_two_alph_exact.py` (fixed stream under two arbitrary alphabets, null ~1%), it05 annealer re-used for full-text decisions.
- Refuted: running keys from Carter/Book of the Dead/founding documents/K1–K3/Sanborn texts under one unknown alphabet; autokey (CT L≤31, PT L≤5,42) under one unknown alphabet; K3 matrix numeric key; Hill 2×2 under unknown numbering; Gromark survivors (full text); keyword-pair keys under two alphabets.
- Blocked: AAA 2009 oral-history transcript (aaa.si.edu 403, no mirror).

## Session 2026-10-27 (it29–36) summary
- **Two-alphabet program** (B(c) = A(p) + n(k), fixed key stream). Pipeline: an alphabet-free gate with K4's additive identity, then the exact check, then crib-exact full-text annealing (it29b plants recovered 6/8). Refuted for:
  - running keys from motivated texts (it29);
  - w-route grid/overlay keys (it30, closes H-1804);
  - w-transkey transposed keys (it31, 10,457 annealed);
  - the K3 matrix (it32, 0 pass the gate).
- **Carving-error robustness.**
  - Running key: one wrong crib (it23c) or a 1–2 letter CT slip between the cribs (it33, H-708): 0 hits.
  - All three big generator nulls (w-transkey, w-keygen, w-route) under drop-one and slips (it34–35): 2 chance hits, both gibberish. **H-2104 closed.** The new integer crib-relation gate is in `iterations/it34_transkey_err.py`.
  - Broad Gutenberg running-key scan finished: 104 texts, 137M offsets, 0 hits.
- **Open, search-limited:** PT-autokey L = 6–12 under one unknown alphabet (it36, H-2103). Annealing and CP-SAT both fail planted controls, and the windows one step from the cribs are uninformative. It needs a propagation-aware search.
- **Data still wanted:** the pre-1997 Weltzeituhr per-face city list (H-802). Wikimedia, Flickr and Openverse return 429 to this container; retry later.
- **Ops.** Long runs go as resumable harness background tasks of ≤2 h. Detached jobs die when the container is reclaimed. Loop state: `/mnt/project-files/k4/loop/thread_state.md`.

## Key facts to reason from
- K1/K2 = Vigenère with KRYPTOS-keyed alphabet (KA = KRYPTOSABCDEFGHIJLMNQUVWXZ). If K4 reuses that tableau, its key letters at the cribs are fully known:
  - pos 22–34: `RDUMRIYWOYNKY`; pos 64–74: `ELYOIECBAQK` (Vig/KA).
- Self-encryptions at 33 (S→S) and 74 (K→K): key = K (shift 0 in KA) at both.
- R→P at both 28 and 66: same key letter at 28 and 66.
- Scheidt: K4 = "more than one stage", final "masking" so English statistics vanish; "simple", "remembered", keyword-based (Hannon 2011 notes, second-hand).
- Sanborn: "matrix codes Ed gave me … visual systems for encoding … individualistic" (Wired 2005); "who says it is even a math solution" (2025).
- Statistical oddities at width 7 / 21 (doubled letters, vertical repeats); NSA 1992 saw "roughness on interval 7".

Identifiability map of every open model class: `findings/STATUS-phase1.md`.

## Hypothesis queue (ranked)
| # | Hypothesis | Why (evidence) | Decisive test | Status |
|---|-----------|----------------|---------------|--------|
| 1 | Key is a 2-D positional function on a grid layout: k = f(row) + g(col) for some width w | Sanborn's "visual/matrix" encoding; width-7/21 anomalies; NSA interval 7 | Exact linear solve on the 24 crib key values for each w and tableau; validate on planted key | REFUTED (it01) |
| 2 | The 24 known KA key letters have internal structure (tableau walk, keyword fragments, alphabet order) | If K1/K2 tableau reused, these are the actual key letters | Structural analysis of `RDUMRIYWOYNKY`/`ELYOIECBAQK` against motivated generators; one prediction per idea | NEXT |
| 3 | "Matrix codes Ed gave me" names a concrete hand system | Sanborn, Wired 2005 | Source research → concrete rule → exact crib test | it03: flipped/rotated tableaux refuted; source of the "flip the chart … W" quote still open |
| 4 | K5 in depth with K4 (shared key at same positions) | Sanborn 2025: same coding system, BERLINCLOCK at same positions | `workers/w-k5/k5_depth.py` once K5 is public | waiting on data |
| 5 | Weltzeituhr face names as per-period alphabets (H-802) | BERLINCLOCK = World Clock | Needs pre-1997 face transcription; `tools/w-clock/face_test.py` ready | waiting on data |
| 3b | Find the source of Sanborn's "flip the chart … the W up there" quote and turn it into a concrete rule | Quote in a Schneier-blog comment, Oct 2025, no source given | Locate the video/interview; derive the rule; exact crib test | CLOSED (it21): source is Big Tech Day 6 (2013, YouTube oFKPNRpE21o). Quote describes how Sanborn drew his K1/K2 worksheet charts (ABSCISSA chart flipped; 'the W up there' = end of the K2 section on the sculpture), not a K4 rule |
| 6 | One wrong crib letter hides a true hit in earlier exact screens | K1–K3 all had carving errors; every generator screen assumed error-free cribs (`findings/STATUS-phase1.md`) | Re-run the identifiable screens with each single crib position dropped (24 cases) plus a shuffled-ciphertext control | REFUTED for fixed tableaux (it04) |
| 7 | Concrete key streams under two arbitrary alphabets can be decided from the full text | Identifiability estimate in `findings/w-synth.md` (full text gives ~249 usable bits) | Full-text annealer on survivor streams, after ≥90% recovery of planted streams | REFUTED (it05) |
| 9 | Doublets come from ciphertext feedback or a copy rule at one column (c_{i+1} tied to c_i), not a key difference | it15 algebra; it06 anomaly P≈1.5e-5 | Enumerate hand mechanisms that tie c_{i+1} to c_i at one column; test each on cribs | PARKED (it16): fair look-elsewhere P≈0.01 and K2 shows similar alignment; the anomaly is weak |
| 8 | **Width-7 grid key under one unknown alphabet** (k = f(row) + g(col)) | it06: doublets aligned at i≡4 mod 7, crib pairs NO/ST/IN all doubled; P≈1e-5 under a structureless key | Crib-exact solver (CP-SAT for crib letters + annealing for the rest), calibrated on planted controls, then K4 at o=0–3 | DEMOTED (it15): the grid key makes residue doublets only ≈2.4× likelier than a random key, so it does not explain the anomaly. Keyword alphabets refuted (it08), KRYPTOS column key refuted (it12). Generic case left open but unmotivated |
