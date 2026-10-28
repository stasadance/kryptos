# Hypothesis log (append-only)


### H-401 K4 is a non-periodic (or long-period) polyalphabetic / progressive-key cipher without transposition   [status: OPEN]  w-stats 2026-10-26
- Claim: K4 = letter-for-letter substitution whose alphabet changes non-periodically (running key, autokey, Gromark/Vimark-type, progressive/clock-driven key) or with crib-consistent period p ∈ {11,16,19,20,22,24,27-32} or ≥33.
- Rationale / sources: K4 IC 0.0361 ≈ random (P=0.22); no period signal p=1..32 (family-wise P=0.94) although the same code recovers K1 p=10, K2 p=8; short periods excluded (ruled_out.md). Bean 2021 argues one-to-one, no transposition.
- Test (falsifiable, no brute force): any concrete key-generation rule must reproduce all cribs via tools/crib_check.py; for periodic p in the list, crib-derived column alphabets must be mutually consistent with a single keyed-alphabet family (w-crib).
- Result: pending.

### H-402 Width-21 vertical-bigram excess is causal (key structure with period 21 or seriation)   [status: OPEN]  w-stats 2026-10-26
- Claim: 11 repeated vertical bigrams at width 21 (perm P=1.6e-4; family-wise over w=2..48 P=0.0047) reflect the enciphering process (e.g. Gromark-like key with 21-periodic structure, as Bean shows ~1-in-10 for base-2 Gromark).
- Rationale / sources: findings/w-stats.md §5; Bean HistoCrypt 2021. Post-hoc caveat: statistic chosen after seeing data.
- Test: a candidate key-generation rule should predict the excess; if a solved method yields no width-21 structure, this was chance. Seriated digraphic at w=21 already excluded (ruled_out.md).
- Result: pending.

### H-403 Width-7 doublet alignment (BB QQ SS ZZ TT in one column) is causal   [status: OPEN]  w-stats 2026-10-26
- Claim: 5 of 6 doublets start at positions ≡ 5 (mod 7) (perm P=6e-4; family-wise w=2..21 P=0.0041), and lag-7 autocorrelation is the largest (9 vs 3.2, z=3.29, FW P=0.14) — suggests a 7-related step (e.g. width-7 transposition after substitution, or key structure).
- Rationale / sources: findings/w-stats.md §2; noted earlier by solvers, NSA analyst & Gillogly per Bean 2021. Post-hoc.
- Test: any method with a 7-step must reproduce all cribs; note periodic substitution with p=7 and no transposition is crib-excluded.
- Result: pending.

### H-404 K4 = periodic substitution followed by transposition (IC-invisible)   [status: REFUTED p<=5 any alphabets (it62 IC, P<0.02); p=6,7 marginal]  w-stats 2026-10-26
- Claim: substitution (possibly periodic) then transposition; statistics cannot see the period after transposition.
- Rationale / sources: only class of classical 2-stage systems the IC/chi² tests leave untouched; Gillogly/NSA suggestion via Bean 2021. Counter-evidence: Sanborn quoted (Bogart 2019 via Bean) that BERLINCLOCK maps "one-to-one" onto NYPVTTMZFPK.
- Test: transposition must keep crib positions' ciphertext letters consistent with a substitution; crib letter supply after substitution has no constraint, so test needs a concrete motivated transposition (e.g. width 7 or 21) + crib_check.py.
- Result: pending.

### H-201 K4 is not a single classical layer (needs >=2 stages)   [status: SUPPORTED]  w-history 2026-10-26
- Claim: K4 cannot be a K1/K2-style periodic tableau alone, nor pure transposition; method has >=2 stages.
- Rationale / sources: Scheidt 2015 workshop "more than one stage", "K4 may not be something as such", "building layers" (https://scienceblogs.de/klausis-krypto-kolumne/kryptos-workshop-transcript/); "change in the methodology" (Wikipedia Kryptos).
- Test (falsifiable, no brute force): crib keystream periodicity under KA/AZ Vig/Beau/VarBeau; letter counts for pure transposition.
- Result: periodic key period 1-26 and 30-48 inconsistent in all 6 variants (27-29 vacuous); pure transposition impossible (cribs need 3 E, CT has 2). findings/w-history-constraints.md §4.

### H-202 A "masking" step hides English statistics before/with classical encryption   [status: OPEN]  w-history 2026-10-26
- Claim: K4 = mask(English PT) then substitution/transposition; undoing the outer layer alone will not give English.
- Rationale / sources: Scheidt 2015 "masking technique ... so that the English language wouldn't be available"; NPR 2005 (VERIFY); Wired 2009 summary "plaintext not standard English ... second level" (metzdowd repost). Note: Sanborn was "confused" by the term (rumkin K4, 2019 lunch).
- Test: any candidate that is plain English from one classical layer contradicts; w-stats: check if K4 IC is near-flat (consistent with masking + polyalphabetic).
- Result:

### H-203 Strict 1:1 letter mapping, 97 in = 97 out, no nulls, no length-changing fractionation   [status: OPEN]  w-history 2026-10-26
- Claim: each CT letter maps to exactly one PT letter; cribs are at exact positions.
- Rationale / sources: Sanborn 2019 (Elonka lunch, via https://rumkin.com/reference/kryptos/k4/): letters map directly, exactly 97, BERLIN starts at exactly 64.
- Test: reject methods requiring nulls/expansion (binary/base-16, ADFGVX) unless they reduce to 1:1 on 97.
- Result:

### H-204 KRYPTOS-keyed alphabet (KA) is part of K4's substitution   [status: OPEN]  w-history 2026-10-26
- Claim: substitution layer uses KA = KRYPTOSABCDEFGHIJLMNQUVWXZ (tableau on sculpture, used for K1/K2).
- Rationale / sources: K1/K2 reproduced with KA Quagmire-III (tools/kryptos_k123.py).
- Test: every crib-algebra test (w-crib) must be run with KA as well as AZ; note under KA-Vig, K->K at pos 74 means shift 0 (key letter K).
- Result:

### H-205 K4 = K3-style decimation transposition + K1/K2 periodic tableau   [status: REFUTED]  w-history 2026-10-26
- Claim: K3 is exactly PT[k]=CT[192k mod 337] (verified); K4 analog a*(i+1) mod 98 or a*i+b mod 97, combined with periodic Vig/Beau/VarBeau (KA/AZ), period 1-12, either order.
- Rationale / sources: K3 decimation form derived by w-history; "two systems"/substitution+transposition (Scheidt 2015).
- Test: tools/test_k3_decimation_vig.py (1,346,976 configs, sanity-checked on planted case).
- Result: 0 hits. REFUTED.

### H-206 K4 method is a Sanborn hand-modification, not a textbook cipher   [status: OPEN]  w-history 2026-10-26
- Claim: Scheidt taught systems by voice; Sanborn modified them; Scheidt did not design/check K4. Expect idiosyncratic route/keys.
- Rationale / sources: Scheidt 2015 "except for K4 I didn't. I did all the others", "he wants to put his touch on things", Sanborn "may have" added something; Sanborn "coding systems that I could then modify in a myriad of ways", "matrix codes" (rumkin K4).
- Test: prediction only — textbook-family searches at small parameters keep failing; prioritize matrix/route ideas tied to sculpture artefacts (tableau, KRYPTOS key 0362514).
- Result:

### H-207 BERLINCLOCK = Weltzeituhr (Alexanderplatz), not Mengenlehreuhr   [status: OPEN]  w-history 2026-10-26
- Claim: clock-derived keys should come from the Weltzeituhr (24 facets/time zones, city names), deprioritize Mengenlehreuhr base-5 logic.
- Rationale / sources: Sanborn 2025 (Wikipedia Kryptos; ingenieur.de 2025-11-18 secondary).
- Test: w-physical: list Weltzeituhr facts; test derived numeric/alphabetic keys with crib_check.py.
- Result:

### H-208 Encryption position-structure is content-independent (K5 shares words at same positions)   [status: OPEN]  w-history 2026-10-26
- Claim: K5 (97 chars, same time/method) shares coded words at same positions -> key/transposition depends on position, not on plaintext (disfavors autokey/PT-feedback).
- Rationale / sources: Paradigm 2026 https://www.paradigm.xyz/2026/06/kryptos (K5 97 chars, same time); "same positions" from secondary sources (amusingplanet) — VERIFY.
- Test: weak; when K5 published, apply any K4 candidate method to K5.
- Result:

### H-209 K4 may contain 1-2 encoding/carving errors   [status: OPEN]  w-history 2026-10-26
- Claim: as in K1 (key letter S->C, PALIMPCEST -> IQLUSION) and K2 (CT E carved as R -> UNDERGRUUND; omitted S), K4 CT may carry isolated errors.
- Rationale / sources: verified mechanically in tools/kryptos_k123.py; Scheidt 2015: would not know if Jim made an encoding error; Wikipedia.
- Test: don't discard a method that reproduces all cribs but has 1-2 isolated garbles elsewhere; do not alter crib positions (Sanborn confirmed them).
- Result:

### H-210 Error positions ("orientation or positioning") encode K4 info   [status: OPEN]  w-history 2026-10-26
- Claim: misspelling positions (K1 PT pos 57, K2 idx 115, K3 DESPARATLY, Morse DIGETAL), not letters, matter.
- Rationale / sources: Sanborn to Elonka: "It's not what they are that's so important though, as their orientation or positioning" (rumkin K1).
- Test: w-physical: locate error letters on sculpture row/column grid; check alignment with K4 rows/columns. Low prior.
- Result:

### H-211 '?' marks are punctuation; K4 = exactly the 97 letters after K3's '?'   [status: SUPPORTED]  w-history 2026-10-26
- Claim: do not include the '?' in K4.
- Rationale / sources: K2 '?' do not advance the key; K3 decimation is mod 337 with '?' at residue 0 (never used) — tools/kryptos_k123.py; Sanborn "exactly 97".
- Test: done (reproduction).
- Result: consistent.

### H-212 "LAYER TWO" / "IDBYROWS" are not K4 instructions   [status: OPEN]  w-history 2026-10-26
- Claim: IDBYROWS was an error artifact (2006 correction); do not use as a K4 hint. LAYERTWO may allude to layering.
- Rationale / sources: elonka.com CorrectedK2Announcement (2006-04-19); verified by script.
- Test: interpretive; no test.
- Result:

### H-501 Weltzeituhr: period-24 polyalphabetic, one (arbitrary/keyed) alphabet per facet/time zone   [status: OPEN]  w-physical 2026-10-26
- Claim: K4 letter i uses the alphabet of World Clock facet (i+s) mod 24, alphabet built from that facet's 1969-1997 city names (keyed alphabet), possibly plus a transposition.
- Rationale / sources: Sanborn 2025: BERLINCLOCK = World Clock (SciAm 2025-11-12); Weltzeituhr = 24-sided column, original 80 city names, changed 1997 (en.wikipedia Weltzeituhr; berlin.de; nitsuah/kryptos doc citing weltzeituhr-berlin.de & Berliner Zeitung 1997-12-12). Period 24 not IC-excluded (w-stats); crib bijection at p=24 has 0 conflicts (w-physical prog.py). Structured shifts (Vig/Beau/Quag I-III, AZ/KA) at p=24 already refuted.
- Test (falsifiable, no brute force): with a pre-1997 facet inventory, build the 24 keyed alphabets by one fixed rule; check crib pairs at residues (0-based i mod 24) r21 E->F,C->M; r22 A->L,L->Z; r23 S->R,O->F; r0 T->V,C->P; r1 N->Q,K->K; then crib_check.py.
- Result: pending inventory.

### H-502 Clock-hand progressive key (Weltzeituhr hour ring / Mengenlehreuhr ticks): k_i = a + b*floor((i+o)/m)   [status: REFUTED]  w-physical 2026-10-26
- Claim: key advances like a clock, b steps every m letters.
- Rationale / sources: rotating 24-hour ring (en.wikipedia Weltzeituhr); 5-min/1-min lamp rows (en.wikipedia Mengenlehreuhr).
- Test: exact check m=1..24, a,b in Z26, o in {0,1}, Vig & Beau, PA/CA in {AZ,KA}^2.
- Result: 0 fits. REFUTED (findings/w-physical.md §1b).

### H-503 Mengenlehreuhr base-5 -> 5x5 grid cipher (Polybius/Bifid/Foursquare/Playfair output)   [status: REFUTED]  w-physical 2026-10-26
- Claim: base-5 clock suggests 5x5 grid.
- Test: count distinct CT letters.
- Result: K4 uses all 26 letters; 5x5-grid output gives <=25. REFUTED unless followed by a further substitution layer.

### H-504 Tableau extra L ("HILL" down right edge) -> Hill cipher on K4   [status: REFUTED (direct)]  w-physical 2026-10-26
- Claim: K4 = Hill n x n (Bauer, Link & Molle, Cryptologia 2016, doi 10.1080/01611194.2016.1141556; extra L per Wikipedia Kryptos).
- Test: exact per-row linear solve over Z26 against all crib blocks, n=2,3,4, all alignments, A=0 and KA-index numbering.
- Result: every case has a row with 0 solutions. Direct Hill REFUTED; Hill combined with transposition, or n>=5, still open (no cheap test).

### H-505 K2 coordinates (38 57 6.5 / 77 8 44) as Gronsfeld digit key   [status: REFUTED]  w-physical 2026-10-26
- Test: crib-derived key values must be 0-9 under some tableau.
- Result: values >9 required in all 8 PA/CA x Vig/Beau combos. REFUTED.

### H-506 Physical words (Morse phrases, YAR, HILL, ENE/compass shift, city initials per facet) as periodic keys   [status: REFUTED]  w-physical 2026-10-26
- Test: periodic consistency p=1..26 under PA/CA in {AZ,KA}^2 (adds Quagmire I/II-type mixes to w-history's result), Vig & Beau.
- Result: no consistent period in any combo. REFUTED.

### H-507 Compass rose / Morse "WHAT IS YOUR POSITION" / World Clock are plaintext themes (navigation/position), not key material   [status: OPEN]  w-physical 2026-10-26
- Claim: K4 plaintext describes a bearing/position (EASTNORTHEAST) relative to the installation and the Berlin World Clock; the Weltzeituhr itself sits on a wind-rose mosaic.
- Rationale / sources: berlin.de Weltzeituhr ("Mosaik in Form einer Windrose"); CIA legacy Kryptos page (lodestone + compass rose); NOVA via thekryptosproject ("not oriented north and south... a mystery"); rumkin K0 (Morse). Third-party reconstruction (solvekryptos.com) uses these themes: UNVERIFIED, not evidence.
- Test: interpretive; use as a secondary-crib sanity check for any partially working method (positions 1-21, 35-63, 75-97 should read as position/bearing English). No standalone test.
- Result:

### H-508 Antipodes K4 run differs from Kryptos K4 (erratum/null indicator)   [status: OPEN]  w-physical 2026-10-26
- Claim: Antipodes' English side repeats Kryptos text with "additional dots and letters" (en.wikipedia Antipodes); differences in the K4 run would flag errata/alternates.
- Test: transcribe the Antipodes K4 run from Hirshhorn photos (Elonka antipodes picture dir) and diff against facts/ciphertext.txt. No public transcript exists (elonka antipodes page).
- Result: pending transcript.

### H-301 Gromark-type (lagged-Fibonacci digit key) with mixed alphabets is crib-consistent   [status: OPEN]  w-crib 2026-10-26
- Claim: K4 = Gromark-like additive cipher, numeric key k_{i+n}=(k_i+k_{i+1}) mod b, arbitrary plain/cipher alphabets.
- Rationale / sources: Bean, HistoCrypt 2021 (https://ecp.ep.liu.se/index.php/histocrypt/article/view/153); independently reproduced: 39 primers (b10/5), 3 (b10/4), 4 (b8/5) satisfy all 24 cribs as a difference system (findings/w-crib-algebra.md §7).
- Test (falsifiable, no brute force): for each of the 46 primers, fix the key, solve the alphabet difference system, propagate to non-crib positions, require English (and keyword-derivable alphabets). Bean's SA found nothing convincing for b10/5; b10/4 and b8/5 not yet decrypted by us.
- Result: pending.

### H-302 Quagmire III (single mixed alphabet, K1/K2 structure) at period 30 or 41 (Vig-style)   [status: OPEN, low prior]  w-crib 2026-10-26
- Claim: only non-vacuous periods where a one-alphabet Quagmire fits the cribs (Beau-style also 23,26,30-33,46,47,49,51,52).
- Rationale: exact z3 result, findings/w-crib-algebra.md §2. Weak: p=30 has a single doubly-constrained residue class; p=41 constrains only crib positions.
- Test: require the alphabet to be keyword-derived (KEYWORD+remaining letters) and check whether any dictionary keyword alphabet satisfies the 24 crib equations at p=30/41; then demand English elsewhere.
- Result: pending.

### H-303 Quagmire IV / general periodic with arbitrary alphabets at GEN-consistent periods   [status: OPEN, weak]  w-crib 2026-10-26
- Claim: Q4 survives all GEN-consistent periods except 11,18,22,36,44 (p=12 undecided). Q1/Q2 survivor lists in findings/w-crib-algebra.md §2.
- Rationale: cribs are too sparse at most periods to refute two free alphabets. Combine with w-stats IC exclusions (periods 8,12,13,18,23,26 disfavoured) before investing.
- Test: restrict alphabets to keyword-derived ones (small, enumerable from a word list) — exact check, not brute force on keys.
- Result: pending.

### H-601 H-301 resolved: Gromark fixed-alphabet variants dead; arbitrary-alphabet Gromark crib-unrefutable but disfavoured   [status: REFUTED (fixed/keyword alphabets); arb two alphabets: no English on full-text annealing (it57, search-limited)]  w-gromark 2026-10-26
- Claim (tests H-301): a Gromark key (k_{i+n}=k_i+k_{i+1} mod b) with some plain/cipher alphabet pair produced K4.
- Rationale / sources: Bean HistoCrypt 2021 https://ecp.ep.liu.se/index.php/histocrypt/article/view/153 ; findings/w-crib-algebra.md §7.
- Test: exact union-find + packing solver tools/gromark.py. It reproduces Bean's 39 (b10/5), 3 (b10/4) and 4 (b8/5) and passed a 200/200 planted-cipher control.
  - Exact scan of bases 2-16 × primer lengths 2-6: 23,283 survivors, matching the iid-random expectation (b10/5: 39 vs 40.0).
  - Every survivor was re-solved with plain and/or cipher alphabet fixed to KA/KAr/AZ/AZr, and with one alphabet + rotation (K1/K2 style).
  - The 46 b10/b8 primers were also tested against 64 keyword alphabets (keyed and ACA columnar).
  - Arb-alphabet partial decrypts (cribs force only 1-13 letters) were scored against a random crib-consistent key null and against a planted-English H1.
- Result: 0 survivors under ANY fixed or keyword alphabet constraint in any base → REFUTED.
  - Arb alphabets: no quadgram is scorable. Monogram scores are at null level (min p=0.010 over 46 tests).
  - Every primer forces fewer letters than its own H1 simulation (P_H1 < 0.05 for 37/46; best 22856 p=0.14, 00537 p=0.13) → DISFAVOURED, not eliminated. Full report: findings/w-gromark.md.
- Open remainder: other expansion rules / LFSR taps, base ≥ 17 or 26 (Vimark), primers of 7+ digits, Gromark + transposition.

### H-901 Antipodes K4 is a corrected/variant ciphertext   [status: REFUTED]  w-antipodes 2026-10-26
- Claim: Antipodes' English-side K4 differs from the CIA K4 (corrections, nulls).
- Rationale / sources: Wikipedia "select differences ... dots and letters"; scirealm.org/Antipodes.html transcript; Elonka photos.
- Test: diff 47-row transcript (both K4 copies) vs facts/ciphertext.txt; read photos for all 97 positions.
- Result: identical in both copies; the differences are K2 R→E (UNDERGROUND), dots ".F.", and separator blanks. See findings/w-antipodes.md.

### H-902 K4 as carved has no known carving error   [status: OPEN, weak support]  w-antipodes 2026-10-26
- Claim: in 1997 Sanborn corrected a K2 ciphertext typo on Antipodes but left K4 unchanged, so K4 has no error that Sanborn knew of.
- Test: none beyond H-901; caveat that he may not have checked K4.
- Result: mild evidence against "fix a K4 typo first" approaches.

### H-903 NSA 1992 "roughness on interval 7" in K4   [status: OPEN; both autokey explanations REFUTED (it51 PT-autokey L7 one alphabet; it55 CT-autokey L7 any two alphabets); excess P=0.004 local, ~0.12 global]  w-antipodes 2026-10-26
- Claim: K4 has excess ciphertext repeats at distance 7 (NSA DOCID 4051151), which the NSA read as substitution followed by transposition.
- Test: count C[i]=C[i+7]: 9/90 vs 3.46 expected; shuffle p=0.005 for d=7, but family-wise over d≤24 p=0.087.
- Result: reproduced but weak. It goes in the same family as the w-stats width-7 doublets (post-hoc). Pair 66/73 (P→R and P→C) shows the repeats are not plaintext repeats without a transposition.

### H-904 Scheidt "mask = change of language base, to something else, not another language"   [status: OPEN, interpretive]  w-antipodes 2026-10-26
- Claim: K4 = substitution + "square" transposition + a final masking layer that recodes the language base (symbol/number-base recoding), designed to flatten frequencies.
- Sources: AJ Jacobs/Scheidt Rev.com transcript, Nov 2020 (mirror: raw.githubusercontent.com/aciderix/kryptos-research-handoff/.../AJ%20Jacobs/EdScheidtKryptosTranscript.pdf.txt); Wired 21 Jan 2005 Q&A.
- Test: for the coordinator; no test run here.

### H-801 Weltzeituhr face alphabets = keyed alphabet from ONE city name per face (simple keyword substitution per facet, period 24)   [status: REFUTED (single-name keywords)]  w-clock 2026-10-26
- Claim: K4 letter i is enciphered with the keyed alphabet (CITYNAME + rest of AZ or KA) of the facet that letter i falls on (period 24).
- Rationale / sources: H-501; Weltzeituhr = 24 facets, one per time zone, city names milled into aluminium (de.wikipedia Weltzeituhr (Alexanderplatz); berlin.de).
- Test: for each of the 19 crib-constrained residues mod 24, ask which of 192 world-city keywords (German+English spellings, superset of plausible clock names) satisfy that residue's crib pairs. Models: S1 C=K[AZ(P)], S2 C=AZ[K(P)], S3 C=K[KA(P)], S4 C=KA[K(P)], fill AZ or KA (tools/w-clock/kwres.py).
- Result: in all 8 model/fill combos at most 13 of 19 residues can be satisfied by ANY city name. The 5 doubly-constrained residues (r0,r1,r21,r22,r23) are unsatisfiable in 6 to 7 of 8 combos. REFUTED for single-name keywords, whatever the face list or alignment is. (S1-AZ, r1: K->K and N->Q need K as the 11th and Q as the 14th distinct keyword letter, so only a long multi-name keyword can work.)

### H-802 Weltzeituhr face alphabet = keyed alphabet from ALL city names on the facet (concatenated in engraving order)   [status: OPEN, blocked on inventory]  w-clock 2026-10-26
- Claim: same as H-801, but the keyword is the facet's full name list, which supplies the >=14 distinct letters that residue 1 requires.
- Rationale: H-801 necessary condition; a pre-1997 face inventory is needed.
- Test: tools/w-clock/face_test.py faces.txt (24 lines, one per face, in clock order). It scores 24 alignments x 2 directions x 4 models x 2 fills. The null max is about 4/24 (dummy run); only 24/24 counts, then crib_check.py.
- Result: pending. The inventory could not be obtained: no published per-face transcription was found in 20+ sources, Wikimedia upload returned HTTP 429, and Flickr returned "CIDR range blocked".

### H-803 Clock "face offset + rotating hour ring" key: k_i = a + b*i + c*((i+o) mod 24) (mod 26)   [status: REFUTED]  w-clock 2026-10-26
- Claim: the shift is the facet's zone offset (period 24) plus the ring's advance per letter (mod 26). This makes the key non-periodic (period 312), so it escapes the plain period-24 refutation.
- Test: exact check of all a,b,c in Z26, o in 0..23, Vig/Beau/var-Beau, PA/CA in {AZ,KA}^2 (5,061,888 configs; tools/w-clock/ringkey.py).
- Result: 0 configurations fit all 24 crib letters. REFUTED.

### H-804 Time-zone offsets / face index / hour numbers (1-24) as a numeric key   [status: REFUTED]  w-clock 2026-10-26
- Claim: the Weltzeituhr gives a numeric key from its UTC offsets (-11..+12, or relative to Berlin) or from the hour ring.
- Test: any such key that depends only on i mod 24 is a period-24 key. Period 24 conflicts at positions 22/70 (E->F and C->M in the same class) for all 12 combos of Vig/Beau/var-Beau x PA,CA in {AZ,KA}. w-crib also showed that Quagmire III with ANY single mixed alphabet fails at p=24.
- Result: REFUTED. Only truly independent per-face alphabets (H-501/H-802) survive at p=24.

### H-805 "80 original names" figure for the pre-1997 clock is unsourced / likely wrong   [status: OPEN, factual]  w-clock 2026-10-26
- Claim: current sources give 146 places + date-line entry (de.wikipedia, citing Märkische Allgemeine 24/25 Dec 1997) or 148 (berlin.de, tourism sites). Berliner Zeitung 12 Dec 1997 and taz 20 Dec 1997 say 20 names were ADDED (Oslo "forgotten"; Jerusalem, Kapstadt and Tel Aviv omitted for political reasons), plus renames (Leningrad, Alma Ata, Bratislava->Pressburg) and zone moves (Kiew). That implies roughly 126-128 names in 1969-97, not 80. The "80" comes only from a third-party GitHub doc (nitsuah/kryptos).
- Test: count names on a dated pre-1997 photo set.
- Result: pending. Do not use "80" as a fact.

### H-701 Width-21 and width-7 anomalies are largely one feature: doublets at 0-idx ≡4 mod 7, three stacked at 21-spacing   [status: OPEN (descriptive)]  w-transpo 2026-10-26
- Claim: 5 of 6 doublets (0-idx 18,25,32,46,67) ≡4 mod 7; QQ/ZZ/TT at 25,46,67 stack at width 21 → 2 of the 11 w21 repeats + vertical trigram QZT; QZT+LWA trigrams = 4 of 11; only 1 of 11 repeats is same-column; 3 aligned doublets are inside cribs (NO, ST, IN at crib offsets 4/11/4; crib starts 21, 63 ≡0 mod 21).
- Rationale / sources: findings/w-transpo.md §a1; scripts workers/w-transpo/scripts/anat.py, wit.py.
- Test: perm P(three doublets at i,i+21,i+42)=0.0025; no generative model in §a2 raises doublet alignment above 2e-3.
- Result: anomaly partially inherited from crib placement; no classical mechanism found.

### H-702 Substitution then columnar transposition (width 7/21) generates the anomalies   [status: REFUTED]  w-transpo 2026-10-26
- Claim: K4 = columnar_w(Sub(P)), w ∈ {7,21}.
- Rationale / sources: Gillogly/NSA suggestion via Bean 2021; w-stats H-404.
- Test: (i) cribs: no columnar transposition of any width 2-96 (either direction, any order) maps the contiguous cribs onto CT 22-34/64-74; width-7 enumeration (20,160 maps, 97 and 7x14 with null) fixes ≤2/24 crib positions, 0 preserve contiguity. (ii) MC: at K4's IC, P(S21≥11) ≤0.01 for all such models (Bayes factor ≲6 over perm), doublet alignment ≤2e-3. (iii) Bean's minor differences (1/5520, 1/240) contradict a final transposition.
- Result: REFUTED given Sanborn's position statements (NYT 2010 NYPVTT→BERLIN; 2019 "exactly 64").

### H-703 Columnar transposition (width 7/21, K3-style) then periodic substitution   [status: REFUTED]  w-transpo 2026-10-26
- Claim: K4 = Sub(columnar_w(P)).
- Test: same contiguity proof (cribs must be fixed by the transposition since Sanborn states plaintext positions); MC dirB21→Vig7 gives P(S21≥11|IC low)=0.0096, no doublet effect.
- Result: REFUTED for every columnar width; only crib-preserving block shuffles remain (H-704).

### H-704 Crib-preserving block/strip transposition BEFORE a position-keyed substitution   [status: OPEN, low prior]  w-transpo 2026-10-26
- Claim: plaintext rearranged in whole blocks (e.g. rows of width 21: both cribs start a width-21 row; widths 19-21, 37-63, 74-96 keep both cribs within one row) then enciphered in place.
- Rationale: only transposition class compatible with cribs + Bean; invisible to all statistics.
- Test: none statistical; only a concrete key method could test it. Cannot create the anomalies (column-perm keeps vertical bigrams, row-perm keeps doublet columns).
- Result: untested; no evidence for it.

### H-705 "Scrambled plain text" (Sanborn 2025) = 1990 CIA-vetting strips, not a cipher stage   [status: SUPPORTED]  w-transpo 2026-10-26
- Claim: the scrambling was sentence strips taped out of order for the CIA Dept. of Historical Intelligence review; not evidence of transposition in the cipher.
- Sources: AFP (enca.com mirror) "five pieces of scrambled texts", "scrambled plain text was found, but without the coding method or the key"; RR Auction "cut sentences into strips and taped them together out of order"; FFXnow 12 Nov 2025; NYT 2010 via nbcnews "What do you have in letter-position 27?" — URLs in findings/w-transpo.md §b.
- Result: SUPPORTED; consistent with Bean 2021 (no transposition after substitution) and Sanborn 2019 (BERLIN exactly at 64).

### H-706 Period-21/42 key component with 2 error letters   [status: OPEN, low prior]  w-transpo 2026-10-26
- Claim: a key repeating at 21 or 42 (the structure the anomalies hint at) is blocked only by T25→V/L67→V and A32→K/K74→K (both pairs 42 apart); GEN needs just 2 deletions.
- Test: Quagmire III p=21 is unsat with ≤1 error (Vig and Beau) and ≤2 (Beau); Q1/Q2/Q4 untested.
- Result: pending (w-crib solver with 2 deletions).

### H-707 GEN period 10/25/50 revived by one error at position 22 or 72   [status: OPEN]  w-transpo 2026-10-26
- Claim: the only crib conflict at p=10,25,50 is E22→F / O72→F.
- Test: Quagmire III p=10 still unsat with ≤2 errors (z3); p=25 SAT with 1 error (Beau, drop 22) but weakly determined; standard Vig/Beau/KA still dead (≥3).
- Result: Q1/Q2/Q4 at p=10 with one deletion untested.

### H-708 One omitted/inserted CT letter between cribs (as K2's missing S)   [status: OPEN]  w-transpo 2026-10-26
- Claim: BERLINCLOCK key-offset shifted by ±1/±2 vs EASTNORTHEAST.
- Test: GEN becomes consistent at p ∈ {6,10,14,15,17,21,25,34,42,43,45,50} for some shift; standard Vig/Beau/vBeau (AZ/KA) only at crib-vacuous periods.
- Result: arbitrary-alphabet periodic exclusions are omission-fragile; standard tableaux robust.

### H-1101 K4 = plaintext + natural-language running key through a standard tableau (no transposition)   [status: REFUTED (statistical)]  w-runkey 2026-10-26
- Claim: keystream at cribs is English (or German) text, under Vig/Beau/vBeau with AZ or KA alphabets (plus 12 PA≠CA mixed variants).
- Rationale: classic hand method; Sanborn says K1-K3 help with K4; K3 drew on Carter's book.
- Test: quadgram score of the 13- and 11-letter crib keystream fragments, compared with uniform, English (fragments 42 apart) and wrong-tableau nulls (100k each); forward and reversed; ≤2 free error letters; German model.
- Result: every tableau gives q24 between -7.4 and -8.5. Uniform is -8.08±0.35 and English is -4.25±0.38, so P(English ≤ obs) = 0/100k. With 2 errors chosen to help, the best is -6.6. German: P ≤ 6e-5. Details in findings/w-runkey.md §1.

### H-1102 K4 running key = a motivated source text (Carter vol.1, K1-K3 pt/ct, Morse, CIA charter/oath/John 8:32, CIA pages, Sanborn letter, KJV)   [status: REFUTED]  w-runkey 2026-10-26
- Test: exact crib check at every offset, forward and reversed, cyclic for short texts, in 6 standard plus 12 mixed tableaux. That is 52M + 104M checks. A positive control recovers 24/24.
- Result: maximum 9/24, at chance level (P(≥9) ≈ 1e-7 per check), and nothing ≥10. Independently reproduces keithadler B1/B3. Details in findings/w-runkey.md §2-3.

### H-1301 Shared K4/K5 item is PLAINTEXT BERLINCLOCK at 64-74; "same coded words" is a paraphrase   [status: SUPPORTED (wording)]  w-k5 2026-10-26
- Claim: Sanborn's primary wording (letter of 12 Nov 2025) is "has the words BERLINCLOCK in the same position as in K4". No primary source says the ciphertext is shared.
- Rationale / sources: numberworld.blog/2025/11/jim-sanborn-open-letter.html (transcribed from the documentcloud 26229389 scan); SciAm 12 Nov 2025 and AFP 19 Nov 2025 are paraphrases. See findings/w-k5.md §2.
- Test: compare against the letter scan when it is reachable.
- Result: supported by the transcription; facts K5 line should be reworded.

### H-1302 K4 and K5 are in depth at 64-74 (same position-determined key)   [status: OPEN, untestable until K5 is released]  w-k5 2026-10-26
- Claim: K5[64..74] = NYPVTTMZFPK, i.e. the key at those positions depends only on position (not on plaintext or ciphertext feedback).
- Rationale: same plaintext at the same positions plus a "similar coding system"; H-208.
- Test: workers/w-k5/k5_depth.py on the released K5. Equal implies a position-keyed system (or an identical plaintext prefix). Different means a different key, and 11 new crib letters for K5.
- Result: pending K5 release (Paradigm).

### H-1303 K5 plaintext is an alternate ending sharing long stretches with K4 plaintext   [status: OPEN]  w-k5 2026-10-26
- Claim: K5 = "alternate scenario/ending" (Sanborn 12 Nov 2025) = "1988 alternate K4 plaintext" (RR item 6). It plausibly shares more than BERLINCLOCK (SciAm: "some of the same coded words").
- Test: on release, find runs of identical ciphertext at the same positions (random expectation is about 3.7 single matches out of 97). Long runs mean a shared plaintext and a shared key.
- Result: pending.

### H-1304 Sanborn laid out K3/K4 in rows of 31 (handwritten "11 Lines 342", "3lines 93", "10.84 rows")   [status: SUPPORTED (visible on RR lot image _21)]  w-k5 2026-10-26
- Claim: K4 = OBKR + 3 rows x 31 = 93, as planned on paper. The bottom-panel geometry was a design-time constraint.
- Sources: RR lot photo cdn.rrauction.com/auction/730/medium/3507616_21.jpg (my reading; one digit of 10.84 unclear; 342 vs 341 unclear).
- Test: none needed for the cipher. It supports using the 31-wide grid for any layout-based (route or columnar) idea, but does not show one was used.

### H-1305 K4's plaintext was edited for length/fit ("multiple versions of the text, with different lengths and coding")   [status: OPEN, interpretive]  w-k5 2026-10-26
- Claim: 97 is a layout-forced length. The plaintext may contain padding, abbreviation or odd spellings to hit the length, as K1-K3 do (X separators, misspellings).
- Source: Sanborn letter 12 Nov 2025 ("Multiple Versions" paragraph).
- Test: none directly. It warns against rejecting candidate plaintexts for non-standard English or filler.

### H-1306 Public RR/Paradigm images reveal nothing of K4's coding system   [status: SUPPORTED]  w-k5 2026-10-26
- Claim: all 14 lot images and the Paradigm images show only the 1988 copper plate (plain A-Z shifted rows), K1-K3 handwritten plaintexts, contracts, badge, photos, a replica, and a hand-lettered KA tableau. The defocused background grid sheets are illegible. RR: "For reasons of secrecy, no photos will be provided of items 1–7".
- Result: nothing to extract. Do not build on "chart" images.

### H-1201 Scheidt's "mask" = K4's own final layer; "language base" = English statistics, not a numeral base   [status: OPEN (textual support)]  w-mask 2026-10-26
- Claim: Scheidt 2020 maps steps onto the sculpture (substitution=K1/K2, "push into this square"=K3, "last step ... masked the framework"=K4; "K1, two, three ... steps ... K4 being the final"). In 2015 he said numeric base change (base 2->16) and extinct languages were things he "was asked not to do".
- Rationale / sources: Bean 2015 workshop transcript (scienceblogs.de); AJ Jacobs 2020 transcript; Hannon 2011 via Bean 2021. findings/w-mask.md §1.
- Test: interpretive. Result: supports a letter-level, keyword-driven mask with OTP-like output.

### H-1202 Numeric base-change / binary-XOR / Baudot-Vernam / trit / digit-pair / hex recoding mask   [status: REFUTED]  w-mask 2026-10-26
- Claim: K4 = letters recoded into another base, a key mask added (XOR or digit-wise), then recoded to letters.
- Test: closure theorem. A plaintext-independent translation mask on N codes that always outputs letters needs 13|N, because the cribs show E and T each with 3 images. Also the crib XOR key is a non-letter at 3-8/24 positions for A=0, A=1, KA=0 and ITA2 codings.
- Result: REFUTED (workers/w-mask/scripts/xor.py).

### H-1203 General relabel+additive position mask C=b^-1(a(P)+k_i), arbitrary alphabets, non-periodic key   [status: OPEN, crib-untestable]  w-mask 2026-10-26
- Claim: the "OTP-like result" mask. Cribs impose only k28=k66 and k24-k29+k34-k33=0 (two alphabets), or k33=k74=0, k28=k66 and k24+k34=k29 (single alphabet).
- Test: needs a concrete key source. Screen candidates with tools/latin_filter.py plus these relations.

### H-1204 Linear or quadratic position key (Scheidt "non-linear is a quadratic way") under ANY alphabets   [status: REFUTED]  w-mask 2026-10-26
- Result: the relations force a,b in {0,13}, i.e. period <=2, already dead.

### H-1205 Small-digit (base m) key mask with mixed alphabets   [status: REFUTED m<=5 one alphabet, m=2 two alphabets (it70); m<=4 by IC (it62); larger m crib-untestable]  w-mask 2026-10-26
- Result (z3): minimum m=3 with two arbitrary alphabets; m=6 with one mixed alphabet (Vig and Beau). Decimal Gronsfeld with an unknown single alphabet is crib-feasible.

### H-1206 Trifid (base-3 fractionation, 27-cell cube) mask   [status: REFUTED n<=9, n=11-13 at standard alignment; n=10 OPEN/disfavoured]  w-mask 2026-10-26
- Result: z3 over arbitrary cubes (trifid.py). Also conflicts with Sanborn's 1:1 statement; 27th symbol absent (p~0.026).

### H-1207 NSA 1992: PT-autokey lag 7 with an unknown mixed alphabet   [status: REFUTED (Vig and Beau, it51 exact)]  w-mask 2026-10-26
- it51 (2026-10-28): exact propagation search (middle chain + BERLINCLOCK backward, not just crib-internal relations as in w-mask z3) completes with 0 solutions for Beau L=7 under key a(q)/AZ/KA (1.7e9 nodes for a(q)). REFUTED.
- Result: Vig unsat for L=1-10. Beau SAT for L=6,7,8,10-12. SA over the alphabet for Beau L=7 found no crib-consistent English (inconclusive). Content-dependent key conflicts with H-208.

### H-1208 CT-autokey with an unknown single mixed alphabet   [status: REFUTED for L<=31]  w-mask 2026-10-26
- Result: z3. Vig unsat for L<=36; Beau unsat for L<=31. Survivors are listed in findings/w-mask.md §3.5.

### H-1209 Alphabet-free key-stream filter for any Latin-square tableau or additive/XOR mask   [status: TOOL]  w-mask 2026-10-26
- Claim: necessary conditions X28==X66 plus 22 inequalities. Null pass rate 1.8%. The K1-K3 PT/CT streams pass at chance rates and none passes at offset 0. Usable for a K4/K5 depth test (tools/latin_filter.py).

### H-1001 Period-7 periodic substitution (any alphabets/tableau) revived by K1-K3-style errors   [status: REFUTED]  w-errtol 2026-10-26
- Claim: NSA "roughness on interval 7" = period-7 key, with ≤2 wrong CT letters or 1 omitted/inserted letter hiding it.
- Rationale / sources: K1-K3 contain deliberate errors; H-903; findings/w-transpo.md §c.
- Test: exact GEN consistency (superset of Quagmire I-IV, Vig/Beau AZ/KA) over all 301 crib-deletion sets, shift d=±1, and shift+1 sub (tools/errtol.py).
- Result: REFUTED within budget — needs 3 wrong letters (8 minimal triples, e.g. {25,32,66}); 1 shift and 1 shift+1 sub both inconsistent. findings/w-errtol.md §1.

### H-1002 Vig/Beau/vBeau with AZ/KA plain & cipher alphabets, error-revived periods (26,30-32,51,52; vacuous 27-29 with omission)   [status: REFUTED]  w-errtol 2026-10-26
- Claim: an error/omission rescues a standard or KRYPTOS-tableau periodic key.
- Test: all minimal error configs (≤2 subs, omission/insertion at every gap position j); forced text 20-64 letters scored by conditional n-gram LLR vs shuffled-CT null and English windows (power 1.0).
- Result: REFUTED — every config engp ≤0.005 (LLR −0.4..−1.2 vs English +0.5). Focus periods 7,10,21,25,42,50 not revivable at all within budget.

### H-1003 Period-10 (PALIMPSEST-length) Quagmire I/II/III with ≤2 errors   [status: REFUTED]  w-errtol 2026-10-26
- Claim: Quagmire at p=10 survives with errors at 22/72 etc.
- Test: z3 exact; Q1(KA cipher), Q3 unsat ≤2 subs and ±1 shift; Q1AZ SAT only {24,72},{33,72}; Q2AZ only {22,34}; Q2KA {22},{32,72},{72,74}. Forced text 12-35 letters, power ≥0.91.
- Result: REFUTED — forced text not English (engp ≤0.01 each), e.g. Q1AZ {33,72}: ?S?SST?T??O??T???O?R?EASTNORTHEAST?I?ISK???T?LT?IT????S??CIA?E?BERLINCLOCKRK?LA???S?HK?????KRK?CK. Q4/GEN at p=10 remain (H-1004).

### H-1004 GEN / Quagmire IV at p=10 with 1 error at 22 or 72 (or ±1 shift)   [status: OPEN, untestable by cribs]  w-errtol 2026-10-26
- Claim: two independent arbitrary alphabets, period 10, one carving error.
- Test: forced-letter English test.
- Result: only 6-10 non-crib letters forced; power ≤0.04 — consistent with anything. Needs a concrete alphabet/keyword hypothesis.

### H-1005 Period-21/42 key (H-706) with 2 errors or 1 omission between cribs   [status: OPEN, untestable by cribs]  w-errtol 2026-10-26
- Claim: Width-7/21 anomalies reflect a p=21/42 key; errors at {25|67}×{32|74} or an omission in 35..64.
- Test: z3: Q1AZ, Q1KA (subs only), Q3-Vig (new: SAT with 2 errors; w-transpo had timeout), Q4, GEN consistent; Q2 (AZ/KA), Q3-Beau, all 8 standard tableaux dead.
- Result: 0-7 non-crib letters forced per config, no English signal (best p 0.06), power ≤0.67. Not refuted, not supported. Also p=25/50: all Quagmires revivable but force ≤5 letters — same status.

### H-1006 Error tolerance yields no English-forcing periodic configuration at p ∈ {7,10,21,25,42,50}   [status: SUPPORTED]  w-errtol 2026-10-26
- Claim: over 412 minimal error configs (GEN, TAB×8, Q1-Q4×V/B), none forces significantly English text.
- Test: shuffled-CT null (500-1000) with max over omission point; min p=0.030, 9/412 < 0.05 (≈20 expected), 0 < 0.01. Pipeline validated by planted English (plant.py: 41-54 forced letters all correct, LLR +0.3..+0.5).
- Result: SUPPORTED. findings/w-errtol.md.

### H-1501 Two superimposed periodic keywords ("combining the functions", Scheidt 2020) under Vig/Beau/vBeau, AZ/KA   [status: REFUTED for L1+L2<=24]  w-sources 2026-10-26
- Claim: k_i = a[i mod L1] + b[i mod L2] (e.g. KRYPTOS+PALIMPSEST 7+10).
- Rationale / sources: Scheidt, Jacobs 2020 transcript "move it down one or two characters and then you starts combining the functions"; Hannon 2011 "correct key word/s".
- Test: exact linear consistency mod 2 and mod 13 of crib key values (workers/w-sources/scripts/dbl.py, dbl2.py); planted (7,10) KA-Vig recovered.
- Result: every pair with L1+L2<=24 inconsistent in all 6 tableaux (incl. 7+10, 7+8, 8+10, 6+7, 7+11, 6+11); L1+L2>=25 survive equally for random CTs (controls 210-217 pairs vs K4 212) -> crib-untestable. Arbitrary-alphabet version open (F3 in findings/w-sources.md).

### H-1502 K1/K2 tableau substitution with a TRANSPOSED key (keyword stream pushed into a K3-style square)   [status: REFUTED for AZ/KA and all dictionary-keyed tableaux (it66, it67: any transposition)]  w-sources 2026-10-26
- Claim: key stream = keyword repeated, written in width-w grid, read by keyed columns / K3 route; positions of PT/CT stay aligned.
- Rationale / sources: Scheidt 2020 "substitution… push into this square… last step… mask"; "K1, two, three… K4 being the final"; Sanborn "matrix codes", "original matrix… all possible shifts" (Dunin 2003, S); NSA 1993 K3 one-step form.
- Test: X28=X66 gate, then 24/24 cribs, AZ/KA x Vig/Beau/vBeau, keywords {KRYPTOS,PALIMPSEST,ABSCISSA,BERLIN,CLOCK}, w=4..31. Overlaps w-keygen T14.
- Result: pending.

### H-1503 Regenerative (chain-addition) key, "Vimark" base 26   [status: REFUTED for fixed AZ/KA tableaux, n<=24; mixed-alphabet OPEN]  w-sources 2026-10-26
- Claim: k[j+n]=k[j]+k[j+1] (or k[j]+k[j+n-1]) mod 26 from an n-letter keyword primer.
- Rationale / sources: Scheidt 2011 "regenerative function", "agents or pilots in case of capture" (S); w-gromark covered only bases 2-16.
- Test: workers/w-sources/scripts/vimark.py, exact linear solve; planted n=5,7,10,15,20 recovered (plant.py).
- Result: 0 consistent configs for K4 (and for 30 random controls) in all 6 tableaux, both recurrences, n=2..24.

### H-1504 Key read off a physical grid (KA tableau / carved panel) by a position-determined route with flips/rotations   [status: OPEN]  w-sources 2026-10-26
- Rationale / sources: Sanborn Wired 2005 "matrix codes Ed gave me… visual systems for encoding… individualistic"; NPR 2020 "methods that don't have anything to do with mathematics"; Big Techday 2013 "flip the chart over, turn it upside down" (S).
- Test: 8 dihedral orientations x routes x offsets -> 97-letter streams; latin_filter X28=X66 gate, then cribs.

### H-1505 The 1988 "J.S.1988" copper plate (rows CDEFGHIJ/DEFGHIJK/EFGHIJKL) is a fabrication test, not evidence for a standard-alphabet K4/K5   [status: SUPPORTED]  w-sources 2026-10-26
- Sources: Sanborn letter 12 Nov 2025 ("proof-of-Concept… cut 2000 letters through heavy copper plate… distort… rolled into a curve"); RR lot item 11; plate images viewed (RR CDN 3507616_2/_9).

### H-1506 Sanborn's layer is non-arithmetic table/pattern lookup (C_i = sigma_i(P_i) via charts), not number crunching   [status: OPEN, interpretive]  w-sources 2026-10-26
- Sources: NPR 29 Jan 2020 "I can employ methods that don't have anything to do with mathematics"; SciAm 12 Nov 2025 "Who says it is even a math solution?" / "I was fortunate not to understand mathematics, probably in my ability to make the code."
- Implication: prefer F1/F2 (chart/route) over arithmetic generators; any generator must be executable from a written chart.

### H-1401 Porta / any reciprocal half-alphabet tableau with a keyword-driven key   [status: REFUTED]  w-keygen 2026-10-26
- Claim: K4 is Porta-type with a generated key. Test: Porta tableaux have no fixed points; K4 cribs have S->S@33, K->K@74. Result: REFUTED for any key. findings/w-keygen.md §1.

### H-1402 Tableau-traversal / clock-hand key k=c+a*t+b*floor((t+o)/m), ANY alphabets   [status: REFUTED]  w-keygen 2026-10-26
- Claim: key read along rows/diagonals of the (KA) tableau or a stepped counter. Test: exact, m=2..40, all o,a,b,c, models fixed/vig1/beau1/two. Result: only m=10-18 satisfy the relations (528 (a,b)), all fail injectivity; 0 survivors in every model incl. two arbitrary alphabets. Extends H-502/H-803 to arbitrary alphabets. tools/keygen.py, workers/w-keygen/scripts/linstep.py.

### H-1403 Motivated keyword generators (periodic, progressive/counter, two-keyword compound, chain addition/Vimark/Gromark-on-columnar-digits, interrupted, keyed-columnar streams) under fixed AZ/KA tableaux or ONE arbitrary mixed alphabet   [status: REFUTED]  w-keygen 2026-10-26
- Claim: Scheidt's "simple, remembered, keyword-driven" key generator. Test: 900,272 configs from 29 motivated keywords x 4 numberings; exact crib solver; pipeline planted on English (28/28 recovered). Result: 0 survivors under 12 fixed tableaux, vig1, beau1. findings/w-keygen.md §4-5.

### H-1404 Same generators under TWO arbitrary alphabets (Quagmire IV / relabel+mask)   [status: OPEN, crib-untestable]  w-keygen 2026-10-26
- Result: 258 consistent configs (chance expectation ~520); 0 pass with any of 62x62 keyword/standard alphabet pairs x 3 modes; each forces only 0-9 non-crib letters. Needs an alphabet hypothesis.

### H-1405 Crib relations for single-alphabet Beaufort (a(C)+a(P)=k)   [status: SUPPORTED (derived)]  w-keygen 2026-10-26
- Result: k28=k66, k24+k34=k29+k33, k33 even, k74 even (symbolic union-find, rel.py). Vig1 relations of w-mask confirmed.

### H-1406 Single-mixed-alphabet models are ~1e-11 selective for any plaintext-independent key stream   [status: SUPPORTED]  w-keygen 2026-10-26
- Result: P(feasible | relations) = 5e-6 (vig1, 1e6 MC; analytic ~6.5e-6), 0/1e6 (beau1); two-alph 0.30. Any proposed generator can be screened with tools/keygen.py feasible().

### H-1801 Key read off a carved Kryptos grid (tableau as carved incl. header/labels/extra L; cipher panel K1-K4; side-by-side; KA26; Morse lines) along row/column/boustrophedon/diagonal/spiral routes, 8 dihedral orientations, fwd/rev, any start offset   [status: REFUTED]  w-route 2026-10-26
- Claim: K4 key stream = letters of a physical sculpture grid along a route (w-sources shortlist #2, H-1504).
- Rationale / sources: Sanborn "matrix codes", "visual systems", "flip the chart over"; grids verbatim from https://elonka.com/kryptos/transcript.html ; Morse from https://rumkin.com/reference/kryptos/k0/
- Test: 774 distinct streams x all cyclic offsets = 659,842 placements; 12 AZ/KA Vig/Beau/vBeau tableaux x 4 numberings, vig1/beau1 (keygen.feasible), letter-level vig1L/beau1L (exact lsolve.py). Plants 20/20 recovered.
- Result: 0 hits in every exact model. Latin (any-tableau) gate 1.78% vs shuffled null 1.67% (chance). findings/w-route.md

### H-1802 Same routes, letter-level K1/K2 model (key letter located in the same unknown mixed alphabet: a(C)=a(P)+a(K) or a(C)+a(P)=a(K))   [status: REFUTED]  w-route 2026-10-26
- Result: 0 / 659,842 placements + 0 / 135,988 overlays (exact backtracking solver, validated vs z3 and planted SAT instances). findings/w-route.md §3-4

### H-1803 Superimposition: K4's carved cells keyed by the tableau/panel letter at any torus shift (dr,dc) of any dihedral image of any grid   [status: REFUTED]  w-route 2026-10-26
- Result: 135,988 overlays, 0 hits in fixed/vig1/beau1/vig1L/beau1L. Latin gate 0.80%. findings/w-route.md §2,4

### H-1804 Same route/overlay keys under TWO independent arbitrary alphabets   [status: OPEN, crib-untestable]  w-route 2026-10-26
- Result: only the alphabet-free Latin gate applies; pass rate equals the shuffled null, so the cribs carry no evidence for or against it.

### H-1701 K1/K2 tableau with a K3-style TRANSPOSED keyword key stream (shortlist #1, = H-1502)   [status: REFUTED]  w-transkey 2026-10-26
- Claim: key = repeated keyword (29 keygen keywords, all phases) pushed through decimation d·t+b mod n (n=97,98 all d,b; 336/337 motivated d incl. 192), K3 closed form d(t+1) mod n+1, keyed columnar (236 orders, w=7,8,10,14,21,24,31,len), routes (rows/boustrophedon/diag/spiral x 8 dihedral on 24/31/sculpture/7/8/14/21-wide and 7x14/14x7 grids), or K3 double rotation (a,b in {4,7,8,14,21,24,28,31}); read or write direction.
- Test: exact under 12 AZ/KA tableaux x 4 numberings, one arbitrary alphabet (vig1/beau1), and Quagmire-III proper (self-vig/self-beau). Planted 50/50 recovered.
- Result: 0 survivors. findings/w-transkey.md; workers/w-transkey/scripts/.

### H-1702 Same with keyword-mixed alphabets / KA sequence as the stream   [status: REFUTED]  w-transkey 2026-10-26
- 55 keyed alphabets, same transpositions and models: 0 survivors.

### H-1703 Same with K1-K3 plaintext/ciphertext as the stream (whole text transposed, or 97/98-letter chunk pushed into the square at every offset)   [status: REFUTED]  w-transkey 2026-10-26
- 8 texts (K2PT carved/corrected, K3PT, K2CT, K3CT, K123CT, K123PT, K12PT) + K1PT/K1CT repeated: 0 survivors.

### H-1704 Quagmire-III-proper exact test (one unknown alphabet a, a(C)=a(P)±a(X))   [status: TOOL, validated]  w-transkey 2026-10-26
- workers/w-transkey/scripts/selfmodel.py: homogeneous system mod 26 via GF(13) nullspace + GF(2) separation; ~1 ms; 0/600 random, 60/60 planted.

### H-2001 Probable-word crib-dragging under an unstructured plaintext-independent key (H-1203 / vig1 / beau1 / two-alphabet)   [status: FACT (proof)]  w-probable 2026-10-27
- Claim: a placement at non-crib j only adds k_j = β⁻¹(C_j) − α(P_j), with k_j free, so every word fits everywhere and forces nothing (FP rate 1).
- Result: dragging can test this model only together with a concrete key generator or a K4/K5 depth. findings/w-probable.md §2.

### H-2002 Probable words (≈150 slot/content words from K1-K3 register + Sanborn themes) under GEN periodic p=8-52   [status: NO EVIDENCE]  w-probable 2026-10-27
- Test: 122,067 placements, null N=1000 random dictionary words per cell + 3 fresh controls per placement.
- Result: probable = control in every null-rate bin (e.g. <0.02: 0.0085 vs 0.0094); mean null consistency 0.76; ≤5 forced letters. gen_drag.tsv, gen_control.txt.

### H-2003 Same words under Quagmire III (one mixed alphabet), all 19 crib-consistent (style, period) models incl. 27-29   [status: NO EVIDENCE]  w-probable 2026-10-27
- Test: exact CP-SAT (workers/w-probable/scripts/q3fast.py; 60/60 agreement with z3, forced tables identical), 70,280 placements, null N=50 + 3 controls each.
- Result: probable vs control in null<0.02 bin 0.0072 vs 0.0100, other bins equal; ≤3 forced letters, 5/71 n-gram P≤0.05 (~3.5 expected).

### H-2004 Crib-forced letters under Q3   [status: FACT (exact)]  w-probable 2026-10-27
- Q3-Vig p=30: P3=K P14=S P38=I P44=S P63=B P93=E (class 3 self-encrypts via S→S@33) ⇒ "...B BERLINCLOCK". V41, B49: nothing forced.
- "THE BERLINCLOCK" (E@63) is Q3-impossible under V30, V41, B27, B31, B32, V27, V28, V29; GEN-impossible at p ∈ {8,12,16,18,20,27,31,32,36,40,41}. Full map: findings/w-probable.md §3.

### H-2005 Q3-Beau p=26, 28, 51 and Q3-Vig p=27 have un-English crib-forced letters   [status: DISFAVOURED (statistical)]  w-probable 2026-10-27
- B26 forces 1Q 51V 58K 81R: P(English ≤ obs) < 2.5e-4. B28, B51, V27: P ≈ 0.002 each (family-wise ≈0.03).

### H-2006 Some probable-word placement is both consistent and statistically non-trivial   [status: REFUTED]  w-probable 2026-10-27
- Nominal LR ≥ 50 hits (TOMB@60 V30, PYRAMID@75 B23, CAIRO@14 B27, …) occur at the control rate. The z=+9 excess vs the estimated null is a winner's-curse artefact.

### H-1901 K4 = Quagmire IV (two arbitrary alphabets, no transposition) at a surviving period 16-60, recoverable by crib-constrained SA + quadgrams   [status: UNTESTABLE]  w-anneal 2026-10-27
- Claim: crib-exact simulated annealing over (plain alphabet, cipher alphabet, shifts) finds K4's plaintext if K4 is Q4 at one of the 33 periods the cribs leave open.
- Rationale / sources: crib algebra cannot test Q4 at these periods (w-crib §2, w-audit). Standard statistical attack, with Bean 2021-style SA on free alphabets.
- Test: calibrate first. 294 English controls (held-out text, cribs at K4 positions, random Q4 keys) and 588 shuffled-K4 nulls, run with the same search as K4 (workers/w-anneal/scripts/sa.c mode 10).
- Result: 0/294 controls recovered at any period. At p=16-28 the search falls short (oracle with the true cipher alphabet recovers 100%). At p≥30 wrong decrypts out-score the true English (7/12 at p=30, 125/126 at p≥37), so no search can identify the plaintext. findings/w-anneal.md §1, §4.

### H-1902 K4 is more English-like than shuffled-K4 under Q4 SA at some period   [status: NOT SUPPORTED]  w-anneal 2026-10-27
- Test: K4's best-of-4 score vs 12-24 nulls per period, z under a normal fit, Bonferroni over 33 periods.
- Result: the 33 K4 z-values have mean +0.18 and sd 0.97. Minimum local p is 0.003 at p=29 (×33 = 0.10). Follow-up: 13 K4 runs vs 124 nulls give median z +0.15 and P(K4>null) 0.60, so the first run was restart luck. The decrypts are word salad. findings/w-anneal.md §2.

### H-1903 General periodic (independent alphabet per class) at p ≥ 16 is testable by SA   [status: REFUTED as a method]  w-anneal 2026-10-27
- Result: with the cribs hard-enforced, annealed random nulls reach −3.4/quadgram (−312 to −328 total), about 80 log10 units above real English (−4.3/quadgram). No 97-letter statistical test exists for this model. findings/w-anneal.md §3.

### H-1904 Method warning: SA "solutions" of K4 under two-alphabet periodic models   [status: NOTE]  w-anneal 2026-10-27
- At p≥35, annealing random shuffles of K4 reaches −3.9 to −4.2 per quadgram of English-like salad, at or above genuine English. Any claimed decrypt of this kind needs a matched shuffled-ciphertext null and controls.

### H-2101 Concrete key stream + TWO arbitrary alphabets is identifiable by full-text annealing at 97 letters   [status: SUPPORTED (synthetic)]  w-synth 2026-10-27
- Claim: H-1404/H-1804/H-601 survivors are "crib-untestable" but not data-untestable: key entropy ≈172+log2N bits vs quadgram budget 249 bits.
- Test: sa.c (workers/w-synth/scripts) on 12 controls: 11/12 recovered (acc ≥0.90); K4 under 40 random relation-satisfying streams: best −498..−550 vs English −400..−434.
- Result: supported; proposed task "decide class C" in STATUS.md §6.1. findings/w-synth.md.

### H-2102 GEN p≥8, Quagmire IV p≥30, Q3 p≥41, unstructured OTP-like position keys are information-limited (no search can decide them from 97 letters + 24 cribs)   [status: SUPPORTED]  w-synth 2026-10-27
- Test: unicity budget (cribs 112.8 bits + 73·D; D4 measured 1.86) vs key entropy; cross-checked with w-anneal T19 spurious ≥ true at p≥30 and GEN nulls beating English.
- Result: supported. Only new information (K5 depth, more cribs, alphabet/keyword restriction) can reopen them.

### H-2103 Residual single-alphabet autokey models (CT-autokey SAT L, PT-autokey Beau L=6-12) are identifiable; earlier SA failure was search failure   [status: PT-autokey L=6-10 REFUTED (it51/52, exact + full-text); L=11-13 incomplete, survivors gibberish]  w-synth 2026-10-27
- Test: vig1 known-key SA (CT-autokey) / chain-propagation search (PT-autokey) vs shuffled-K4 null.

### H-2104 Exact generator nulls (w-keygen, w-route, w-transkey; ~21M configs) are fragile to one crib-position carving error   [status: OPEN]  w-synth 2026-10-27
- Test: rerun with 24 single-deletion sets and BERLINCLOCK ±1 shift; compare to a shuffled-CT control through the same pipeline.
