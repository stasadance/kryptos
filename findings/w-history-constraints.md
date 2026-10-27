# w-history: constraints on K4 from K1-K3 and Sanborn/Scheidt statements (T2)
Worker: w-history, 2026-10-26. Hypotheses logged as H-201..H-212 in hypotheses/log.md. I used a separate H-2xx block so my numbers would not clash with other workers' appends.

## 1. K1-K3 methods (reproduced by script)
Script: tools/kryptos_k123.py (`python3 tools/kryptos_k123.py` prints all three plaintexts and asserts the checks).
Ciphertexts were taken from rumkin.com/reference/kryptos/k1/, /k2/, /k3/ and the plaintexts cross-checked against https://en.wikipedia.org/wiki/Kryptos

- **K1:** Vigenere with the KRYPTOS-keyed alphabet `KA = KRYPTOSABCDEFGHIJLMNQUVWXZ` used for both the plaintext and the ciphertext alphabet (Quagmire III), key PALIMPSEST (period 10). The rule is P = KA[(idx(C) - idx(k)) mod 26]. The script reproduces it exactly, ending ...NUANCEOFIQLUSION.
- **K2:** the same tableau with key ABSCISSA (period 8). The three '?' are plaintext punctuation passed through unenciphered, and the key does NOT advance over them; the script confirms this. The sculpture text gives ...WESTIDBYROWS. Inserting the S that Sanborn left out (...GE**S**WJLLAETG) gives ...WESTXLAYERTWO, which the script confirms. The X's in K2 serve as sentence or period separators.
- **K3:** pure transposition of 336 letters, with the trailing '?' excluded. The standard description is two steps: write the text in rows of 24 and rotate it 90 degrees clockwise, then write that result in rows of 8 and rotate again.
  **New compact form (verified):** PT[k] = CT[192*k mod 337] for k = 1..336 (1-indexed). In other words, K3 is a single decimation, stepping 192 positions modulo 337, where 337 = 336 letters + the '?'. The '?' sits at residue 0 and is never visited. The plaintext ends ...MISTXCANYOUSEEANYTHINGQ: an X separator, then a final Q.
- Sanborn's K3 hint, as reported: the KRYPTOS numeric key 0362514 for a keyed columnar transposition (rumkin K3 page, "reportedly"). This is UNVERIFIED as a primary statement. The NSA write-up describes K3 as a keyed columnar transposition in a 4x86 matrix (rumkin).

## 2. Deliberate errors: what they are, mechanically
Computed with the script:
- **IQLUSION (K1):** the sculpture ciphertext at plaintext position 57 is K. With key letter S (PALIMPSEST) it decrypts to Q; with key letter C (PALIMPCEST) it decrypts to L. So the error lives in the **key** (S changed to C on Sanborn's chart), not in the plaintext. Wikipedia reports the same thing ("original chart misspells the keyword as PALIMPCEST").
- **UNDERGRUUND (K2):** the ciphertext R at K2 index 115 decrypts to U; the correct ciphertext E would give O. So the error is a **ciphertext transcription** error (E carved as R). Wikipedia: "an E was transcribed as an R on the sculpture".
- **DESPARATLY (K3):** a plaintext-level error, since a transposition preserves letters (E changed to A and one E dropped).
- **DIGETAL (Morse):** a plaintext-level error (I changed to E).
- **Missing S (K2):** a ciphertext omission. Sanborn first said it was left out "for aesthetic reasons", then called it an error (CorrectedK2Announcement, elonka.com, 2006-04-19).
- Misspelled-in letters: Q (K1), U (K2), A (K3), E (Morse). Letters they replace: L, O, E, I. Community observation (UNVERIFIED as intended): Q, U, A, E plus the extra L in the tableau give EQUAL; the K3 X...Q brackets around CANYOUSEEANYTHING have been read as markers.
- Sanborn on the errors (rumkin K1 page, quoting a statement to Elonka Dunin): "Those errors are deliberate. It's not what they are that's so important though, as their orientation or positioning." Sanborn in 2005: "most of my things are rife with mistakes on purpose." Sanborn in 2006: "You could not make any mistake with 1,800 letters." (Wikipedia)
- **Implication:** at least two K1-K3 anomalies are encryption-process errors made by hand: a wrong key letter and a mis-carved ciphertext letter. Scheidt said he would not know if Jim made an encoding error (2015 workshop, below). So **K4 may contain carving or encryption errors**. A correct method may fail to reproduce 1-2 isolated letters; this is relevant to H-209.

## 3. Statements about K4 (sourced)
| Statement | Who/when | Source |
|---|---|---|
| "there's a masking technique that applied so that the English language wouldn't be available" | Scheidt, 2015-10-24 workshop | https://scienceblogs.de/klausis-krypto-kolumne/kryptos-workshop-transcript/ (R. Bean transcript) |
| "I could have moved to a different math base ... this is base 2 we could move to base 16" (said hypothetically) | Scheidt, 2015 | same |
| "the math associated with the cryptography and that's some substitution transposition ... you could mix and match" | Scheidt, 2015 | same |
| "it lends itself to building layers"; K4 "more than one stage" | Scheidt, 2015 | same |
| "the others have all the intrinsics of classical cryptographic puzzles"; "the K4 may not be something as such" | Scheidt, 2015 | same |
| Scheidt designed and checked K1-K3 but NOT K4 ("except for K4 I didn't. I did all the others"); he never decrypted K4. Sanborn "may have" done something else on top | Scheidt, 2015 | same |
| Encoding scheme was passed by voice; Sanborn modified it ("he's a sculptor and he wants to put his touch on things") | Scheidt, 2015 / NoVA Mag 2022 | same; https://northernvirginiamag.com/culture/culture-features/2022/10/14/cia-kryptos-sculpture-cipher/ |
| Scheidt deliberately masked the frequency advantage in part 4 | Scheidt, NPR 2005 | via kryptools hints page (site was down, 503) - VERIFY |
| Intentional "change in the methodology"; difficulty "nine out of ten" | Scheidt | Wikipedia |
| "There may be more to the puzzle than what you see ... Just because you broke it doesn't mean you have the answer"; "mirrors and obfuscation" | Scheidt, Wired 2009 (repost) | https://www.metzdowd.com/pipermail/cryptography/2009-April/015266.html |
| Sanborn wanted "systems that didn't necessarily depend on mathematics"; Scheidt "told me about matrix codes"; "coding systems that I could then modify in a myriad of ways"; "so that even he would not know what it says" | Sanborn (undated interview) | https://rumkin.com/reference/kryptos/k4/ |
| Letters map directly from ciphertext to plaintext; K4 is exactly 97 characters; BERLIN starts at exactly character 64; Sanborn "was confused" by the term "masking technique" | Sanborn, 2019 lunch with Elonka | rumkin K4 page |
| Hints: BERLIN 64-69 (Nov 2010), CLOCK 70-74 (Nov 2014, NYT), NORTHEAST 26-34 (Jan 29 2020, NYT), EAST 22-25 (Aug 2020) | Sanborn | Wikipedia |
| "There are several really interesting clocks in Berlin" / "You'd better delve into that particular clock" | Sanborn, 2014 | Wikipedia; Slate 2014 |
| BERLINCLOCK = the Weltzeituhr (World Clock, Alexanderplatz), "not abstract time codes" | Sanborn, 2025 (open letter / Spy Museum 2025-11-12) | Wikipedia; https://www.ingenieur.de/technik/fachbereiche/rekorde/cia-skulptur-kryptos-der-code-schoepfer-verraet-neue-geheimnisse/ (secondary) |
| Kryptos is about conveying/delivering a message; historical allusions are part of the structure; two historical events influence the key | Sanborn 2025, as paraphrased | ingenieur.de (secondary, paraphrase only) - VERIFY |
| K5 exists; 97 characters; created at the same time as K4; "K5 cannot be solved without K4"; reportedly shares some coded words in the same positions as K4 | Sanborn 2005/2020/2025; Paradigm 2026 | https://www.paradigm.xyz/2026/06/kryptos ; rumkin K5; amusingplanet (secondary for "same positions") |
| "K4 has been discovered and it points in the direction of K5"; "They did not solve K4 and they certainly did not find the key" | Sanborn 2025 | https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/ |
| Plaintext reconstructed from scrambled strips in the Smithsonian archive (2025); method unknown; archive sealed until 2075; the auction lot included "coding charts showing the process" ($962,500, 2025-11-20); Paradigm bought it and runs a SHA256/HMAC verifier ($1 per guess) | 2025-26 | Wikipedia; RR Auction; Paradigm |
| "two systems"; "who says it is even a math solution" | - | **NOT FOUND** in any source I could reach. Treat as UNVERIFIED and do not build on them. |
| K4 plaintext "not standard English" and needs "a second level of cryptanalysis" | Wired 2009, the journalist's summary, not a quote | metzdowd repost |

## 4. Tests run (motivated, small)
- **T-a, K1/K2 method applied directly to K4:** a periodic key under the KA or AZ alphabet, in Vigenere, Beaufort or variant-Beaufort form, with no transposition. The crib-implied keystream (KA-Vig: pos 22-34 `RDUMRIYWOYNKY`, pos 64-74 `ELYOIECBAQK`) is inconsistent for every period 1-26 and 30-48 in all six variants. Periods 27-29 are consistent only vacuously, because no two crib positions coincide mod P. **Refuted for periods <= 26.**
- **T-b, pure transposition:** impossible. The cribs need three E's and the ciphertext has only two.
- **T-c, K3-style decimation combined with a K1/K2-style tableau:** the transposition is a*(i+1) mod 98 (exactly the K3 form, n+1 modulus) or any affine a*i+b mod 97. The substitution is periodic Vigenere, Beaufort or variant-Beaufort with the KA or AZ alphabet, period 1-12, applied either before or after the transposition. That is 1,346,976 configurations with **0 hits**. The test detects a planted synthetic case. Script: tools/test_k3_decimation_vig.py. **Refuted.**
- **Observation:** the K at position 74 is ciphertext K over plaintext K. Under the KA tableau, K is index 0, so a KA-Vigenere with no transposition would need key letter K (shift 0) at position 74.

## 5. Constraints and hypotheses (logged as H-201..H-212)
1. **H-201** K4 is not a "classical, single-layer" system. A periodic K1/K2 tableau alone is refuted (T-a), and pure transposition is refuted (T-b). Consistent with Scheidt ("K4 may not be something as such", "more than one stage", deliberate "change in methodology").
2. **H-202** K4 = (masking step on the English plaintext) + (classical substitution/transposition). "Masking" means the English letter statistics are deliberately hidden before or during encryption. Falsifiable: a candidate plaintext that is plain English and comes from a single classical layer contradicts this. Prediction: an intermediate text (after undoing the outer layer) will NOT show English IC; w-stats can check whether the K4 IC is flat.
3. **H-203** Direct letter-to-letter mapping: each of the 97 ciphertext letters corresponds to exactly one plaintext letter (Sanborn 2019, as reported). Rules out fractionation that changes length (Polybius/ADFGVX/binary expansion) unless it ends 1:1 at 97, and rules out nulls. Keep the crib positions exact.
4. **H-204** The KRYPTOS tableau (KA alphabet) is part of K4's substitution layer, because it is physically on the sculpture and was used for K1 and K2. Falsifiable: a solution method that uses no KA alphabet weakens it. The test is to rerun every crib analysis with the KA alphabet as well as the AZ alphabet.
5. **H-205** (REFUTED) K4 = K3-style decimation + K1/K2 periodic tableau (T-c).
6. **H-206** Sanborn modified a Scheidt-taught system by hand ("put his touch on things"). Scheidt did not design or check K4, so the K4 method may be idiosyncratic: a non-standard route, hand-made matrix, keyword or clock-derived numbers, rather than a textbook cipher. Prediction: textbook-family searches (w-crib) will continue to fail for all families tested at small parameters.
7. **H-207** The Berlin clock is the Weltzeituhr, by Sanborn's 2025 statement, not the Mengenlehreuhr. Any key derived from the Mengenlehreuhr's base-5 lamp logic is deprioritised. A key derived from the Weltzeituhr (24 time zones, city names, its 1969 date, column faces) is preferred. Falsifiable: w-physical can enumerate the Weltzeituhr's facts (24 facets, city list) and test them as keys via crib_check.
8. **H-208** K5 is 97 characters, created at the same time with the same method, and shares words in the same positions. So the K4 method must leave the plaintext position-to-ciphertext position relation **independent of message content**: for example, a position-dependent key or a fixed transposition, not an autokey that depends on the plaintext. Otherwise the "same position" claim would be meaningless for cribs. Falsifiable: an autokey or plaintext-feedback method contradicts this, though only weakly, because the "same position" claim rests on a secondary source.
9. **H-209** K4 may contain 1-2 encoding or carving errors, like K1 (key error) and K2 (carving error and an omitted letter). Practical rule: when a method reproduces all 24 crib letters but gives near-English elsewhere with 1-2 isolated garbles, do not discard it. Conversely, do not "fix" crib letters: Sanborn confirmed the cribs against the ciphertext as it stands.
10. **H-210** Misspellings matter by "orientation or positioning", not by letter value. Errors sit at K1 plaintext position 57 (key position 7 = S/C), at K2 index 115 (R/E), in K3 DESPARATLY (positions 7, 10), and in the Morse DIGETAL. Test: map those positions onto the 97-letter K4 grid and onto the sculpture's row/column layout (w-physical). This is low prior and exploratory.
11. **H-211** The K3-to-K4 '?' and the K2 '?' marks are punctuation, not letters, in the K1-K3 method (the key does not advance and they are excluded from K3's transposition). So K4 = exactly the 97 letters after the K3 '?'; do not prepend the '?' (this matches Sanborn's "exactly 97").
12. **H-212** K2's "LAYER TWO" (the 2006 correction) and "ID BY ROWS" was a mistake, so neither is a K4 instruction. "LAYER TWO" plausibly refers to the layered structure or to K4 ("second layer" in Scheidt's "building layers" sense). Low-confidence interpretive hypothesis. Do not use IDBYROWS as a hint.

## 6. What is NOT supported
- The "two systems" quote and the "who says it is even a math solution" quote: no source found. If the coordinator has a source, add it to facts/known_facts.md.
- The claim that K4 uses the Mengenlehreuhr: contradicted by Sanborn 2025, though his 2014 "delve into that particular clock" remains ambiguous.
- Binary or base-16 conversion: Scheidt said only that he "could have" changed the math base. That is not evidence it was done. It is also in tension with H-203, the 1:1 letter mapping.
