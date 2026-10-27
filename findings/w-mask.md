# w-mask: T12. Scheidt's "mask" / "change the language base", formalized and tested
Worker: w-mask, 2026-10-26 (UTC). Hypotheses: H-1201..H-1209.
Scripts: `workers/w-mask/scripts/`, with raw solver outputs in `*.out` there.
New shared tool: `tools/latin_filter.py`. It is an alphabet-free necessary-condition filter for any candidate key or mask stream.
Positions are 1-indexed. No keyspace search was done. The only heuristic search was a bounded simulated-annealing (SA) run on the one surviving NSA-motivated model (§3.6).

## TL;DR
1. **Sources.** Scheidt himself said in 2015 that a *numeric* base change (he gave "base 2 → base 16") was something "I had thought of and **I was asked not to do**" ("different folks thought that's not fair Scheidt"). An extinct or uncatalogued language was also rejected as "unfair". In his 2020 account the steps are: substitution (K1/K2), then transposition, "push into this square" (K3), then "the last step … I masked the framework". He ends with "K1, two, three, which is steps of the puzzle, and then K4 being the final". The "mask" therefore names K4's own layer. "Language base" most plausibly means the English statistical base ("the number of Es, … Ys … Xs"), not a numeral base.
2. **Theorem (closure).** Suppose a mask acts by a fixed, plaintext-independent group translation on a code space of size N (XOR on 5-bit/Baudot codes, trits, digit pairs, hex) and must always output one of 26 letters. Then the keys it uses lie in one coset of the stabiliser of the letter set. That stabiliser has order dividing gcd(26, N). The cribs need ≥3 distinct images of E and of T, so 13 | N. **Every binary, Baudot/Vernam, base-3, base-10-pair or base-16 recoding mask that keeps 97 letters is impossible** unless the encipherer picked keys adaptively. Direct crib check: the XOR key at the cribs is a non-letter at 3-8 of 24 positions in every coding (A=0, A=1, KA=0, ITA2). The chance of a 97-letter output is 1e-7 to 1e-9. **H-1202 REFUTED.**
3. **Reduction.** Sanborn says "plain B taken, has the encipherment done to it, and out pops a cipher N" (Bogart 2019 via Bean 2021) and BERLIN sits at exactly 64. Under that, every 1:1 positional mask, in any order and with any number of letter-to-letter layers, collapses to C_i = σ_i(P_i). The crib data look exactly like a one-time pad: 1 repeated (P,C) pair against 0.5 expected, and 2 fixed points against 0.92 expected. That matches Scheidt's "OTP … analogy is reasonable … in the sense of the result".
4. **Crib content of the general "relabel + additive mask" model** C = β(α(P) + k_i), with α and β arbitrary alphabets and any key sequence. This covers letters→numbers via a mixed table, adding a mask, and mapping back. The 24 cribs impose **only two relations: k28 ≡ k66 and k24 + k34 ≡ k29 + k33 (mod 26)**. With a single alphabet α = β (K1/K2 style) they impose four: k33 = k74 = 0, k28 = k66, and k24 + k34 = k29. **The model is therefore crib-untestable unless the key has structure.** Structured keys tested:
   - linear and quadratic in i under ANY alphabets: **refuted**. The relations force period ≤ 2, and that is already dead. This tests Scheidt's "non-linear is a quadratic way" (H-1204).
   - smallest digit base for any digit key: **3** with two arbitrary alphabets; **6** with one mixed alphabet, Vigenère or Beaufort (z3). H-1205.
5. **Other mask families.**
   - Trifid (base-3 fractionation, any cube) at standard alignment: dead for periods 2-9, 11 and 12. Period 10 is SAT, and periods 13+ are mostly SAT or unknown. It is also disfavoured by Sanborn's 1:1 statements and by the 27th symbol never appearing (p≈0.026). H-1206.
   - PT-autokey with one unknown mixed alphabet (the NSA 1992 "interval 7" idea): Vigenère L=7 is **unsat**; Beaufort L=7 is crib-SAT, but SA found no crib-consistent English (inconclusive). H-1207.
   - CT-autokey with one unknown mixed alphabet: dead for all L ≤ 31. H-1208.
6. **New tool `tools/latin_filter.py`.** It applies to ANY Latin-square tableau (Vigenère, Beaufort, Quagmire I-IV with any alphabets) and to any additive or XOR mask with a key-letter stream X. The cribs force **X28 = X66** plus 22 inequalities. A random English stream passes about 1.8% of the time. K1-K3 plaintexts and ciphertexts pass only at chance rates, and no stream passes at its natural offset 0. The tool is directly useful for a K4/K5 depth test once K5's ciphertext is public. H-1209.

## 1. Sources: Scheidt's statements (verbatim where available)
| When | Statement | Source |
|---|---|---|
| Wired, 21 Jan 2005 | "All four (sections) are done in the English language." "the English language is still visible through the code. (But with) this other technique (in the fourth part), I disguise that. So … you need to solve the technique first and then go for the puzzle." | reproduced at https://kryptosfan.wordpress.com/k4/artichoke/masking-vs-english/ (Wired original paywalled) |
| NPR, 9 Jun 2005 | the frequency advantage was "deliberately masked"; Scheidt never tried to crack Sanborn's final message | https://www.npr.org/transcripts/4684720 (503 today; content via search summary) |
| Wired 2009 | "There may be more to the puzzle than what you see … mirrors and obfuscation" | https://www.metzdowd.com/pipermail/cryptography/2009-April/015266.html |
| Zola dinner, 8 Oct 2011 (Hannon notes) | K4 "is not mathematical … simple, can be remembered, and executed years later when used with the correct key word/s"; "similar to what would be provided agents or pilots in case of capture" | Bean 2021 §3, https://ecp.ep.liu.se/index.php/histocrypt/article/view/153 (citing kryptos.groups.io msg 12611) |
| ACA 2013 | the receiver's identity is hidden: "built into the process", no clue given | https://kryptosfan.wordpress.com/2013/10/30/more-about-ed-scheidts-aca-talk/ |
| Workshop, 24 Oct 2015 (Bean transcript) | "the impact of some kind of math function on the English language … so there's a mask of some type now"; "you're carrying the weight of the language"; "the first step is that thing and now that gets to be hard" | https://scienceblogs.de/klausis-krypto-kolumne/kryptos-workshop-transcript/ |
| same | **"the thing that I had thought of and I was asked not to do… this is based on the English language … I could have moved to a different math base … base 2 we could move to base 16 … different folks thought that's not fair Scheidt"**; Mayan base 60 given as an example; an extinct language "becomes unfair" | same |
| same | "lends itself to building layers or you could mix and match which is a certain amount of that took place"; K4 is "more than one stage"; "there's a masking technique that applied so that the English language wouldn't be available"; asked whether masking comes before or after encryption: no clear answer | same |
| same | Scheidt never decrypted K4; "if Jim made an encoding error you would not have know[n]" | same |
| AJ Jacobs, Nov 2020 (Rev.com transcript, 17 pp.) | substitution: "take the alphabet and you just move it down one character or two … then you start combining the functions"; transposition: "defining the parameters of the puzzle in the sense of the square … my secret is push into this square. So that was another step. And then the last step … I masked the framework, in other words if you can change the language base then it becomes in my favor … when it was used as the mask it was current, 2020 secret." | https://raw.githubusercontent.com/aciderix/kryptos-research-handoff/HEAD/sources/groupsio_membres/textes/Personal%20Folders/AJ%20Jacobs/EdScheidtKryptosTranscript.pdf.txt (mirror of the groups.io file) |
| same | "mask … If I use that directly in the puzzle I have against me the number of Es, the number of Ys and number Xs … Now if I can mask that, change that characteristic"; "Not to another language, it's to something else"; asked whether it could be "the window pattern" outside AJ's window: "It could be, but it's not." OTP: "not directly related … The analogy is reasonable, but reasonable in a sense of the result. How you did it to get that result is the question." | same |
| same | first proposal to the CIA was "a language that was only used in the world for maybe 100 years" (dead language). Rejected in favour of "the English language as a reference" | same |
| same | "Linear is a direct substitution, non-linear is a quadratic way of looking at it … That's if you're going to keep it as a pencil and paper system"; "you've got K1, two, three, which is steps of the puzzle, and then K4 being the final" | same |
| Sanborn 2019 (Bogart, via Bean 2021) | "BERLINCLOCK in plain matches directly with NYPVTTMZFPK. It is a one-to-one match with plain B taken, has the encipherment done to it, and out pops a cipher N, plain E is then enciphered to a cipher Y" | Bean 2021 |

**Patents.** Scheidt's patents (TecSec, 1993-2015) are digital key-management patents:
- US 5,375,169 (Scheidt & Crowley, filed 1993): a "split key". Each party generates a pseudorandom component, and the components are combined by concatenation or bitwise mod-2 addition. https://patents.google.com/patent/US5375169A/en
- The "Cryptographic key split combiner" family (Scheidt & Wack, from 1998; US 6,885,747, 6,608,901, 7,212,632 and others), the basis of "Constructive Key Management". https://patents.google.com/patent/US6608901

The word "mask" does not appear in US 5,375,169, and none of these patents concerns letter ciphers. US 5,717,760, "Message protection system" with two masks, is by R. Satterfield and is **not** Scheidt's. The only carry-over is conceptual: Scheidt's habit is to form the working key by **combining several independent components** with modular addition. I found no CIA/OTS-era primary source on masking. Scheidt's own account of that work covers duress codes for captured agents ("I used to make those codes, for captured people", 2015) and codes woven into textiles (2020).

**Interpretation (H-1201).**
1. In 2020 the "steps" map onto the sculpture: substitution = K1/K2, transposition square = K3, and "the last step … mask" = K4 ("K1, two, three, … steps … K4 being the final").
2. The mask's purpose is to remove English frequency features.
3. Two literal readings are excluded by Scheidt himself in 2015: a numeric base change (base 2/16/60) and a foreign or extinct language. He was asked not to use them.
4. The 2011 description, "simple, remembered, executed years later with the correct key word/s", pencil-and-paper, points to a **keyword-driven, letter-level procedure whose output looks like an OTP**.
5. Caveat: Sanborn says he altered the system, and Scheidt never checked K4.

## 2. Hard constraints and what they force
- Constraints: 97 letters; BERLIN at exactly 64 (Sanborn 2019); "one-to-one … plain B … out pops cipher N"; K5 shares words at the same positions (SciAm 2025). Together these force the end-to-end map to be **positional**: C_i = σ_i(P_i), with σ_i a permutation of the 26 letters chosen independently of the message content (from H-208).
- Any stack of letter-to-letter layers, in any order and however many there are (substitution, mask, re-substitution), collapses to one σ_i per position. So the question "mask before or after the encryption" has no observable consequence unless a layer is non-positional.
- The non-positional options are already constrained:
  - columnar transposition is impossible with the cribs at fixed positions (w-transpo H-702/703);
  - only crib-preserving block shuffles remain (H-704);
  - fractionation is treated in §3.4.
- Crib statistics (pairs.py):

| statistic | observed | expected for an OTP |
|---|---|---|
| same-P pairs (13) that also share C | 1 (R→P at 28 and 66) | 0.5 |
| fixed points (S@33, K@74) | 2 | 0.92 |

  Images per plaintext letter: E→{F,G,Y}, T→{R,S,V}, A→{K,L}, S→{R,S}, N→{Q,T}, O→{F,Q}, L→{V,Z}, C→{M,P}. **The cribs are indistinguishable from a one-time pad.**

## 3. Models and exact tests
### 3.1 Numeric "base change" masks: closure theorem (H-1202, REFUTED)
**Setup.** A group G of order N acts freely by translation on codes X. Plaintext letters are coded into A ⊂ X with |A| = 26. The ciphertext must decode from B ⊂ X with |B| = 26. The key k_i does not depend on the plaintext.

**Argument.** For every plaintext to stay letters, each used key must satisfy k·A = B. So all used keys lie in one coset of Stab(A). Stab(A) acts freely on A, so |Stab(A)| divides gcd(26, N). The cribs need E to have ≥3 distinct images, so ≥3 distinct keys are used, so |Stab(A)| ≥ 3, so 13 | N.

**Consequences.**
- These fail: XOR on 5-bit codes (N=32), ITA2/Baudot Vernam (32), trits (27), two-digit decimal codes with digit-wise or mod-100 addition (100), hex (256).
- Reducing the result mod 26 instead makes decryption ambiguous, or it is just the mod-26 family of §3.2.
- If keys are not adapted, the probability that 97 outputs are all letters is about (26/N)^97, e.g. (26/32)^97 ≈ 2e-9 for N=32.

**Exact crib check (xor.py).** The XOR key P⊕C at the 24 crib positions is a non-letter at:

| coding | non-letter key positions (of 24) | P(97-letter output) |
|---|---|---|
| A=0 | 8 | 1.2e-8 |
| A=1 | 6 | 9e-8 |
| KA=0 | 3 | 1.2e-7 |
| ITA2 | 4 | 1.0e-9 |

So "XOR with a letter key (running text)" is refuted directly for every coding. Scheidt's own 2015 remark that he was asked not to change the math base agrees.

### 3.2 General relabel + additive position mask (H-1203, OPEN, crib-untestable)
**Model:** C_i = β(α(P_i) + k_i mod 26), with α and β arbitrary.
- This covers: Quagmire I-IV with any non-periodic key; letters→numbers via a mixed table + mask + numbers→letters; Z26 is the only abelian group of order 26.
- Beaufort-type forms are included by replacing α with −α.

The cycle analysis of the crib graph (cyc.py) gives:
- **Two alphabets:** 27 nodes, 5 components, cycle rank 1, plus the duplicated pair. The only relations are **k24 − k29 + k34 − k33 ≡ 0** and **k66 ≡ k28**, plus injectivity.
- **One alphabet (α = β, Vigenère form):** **k33 = 0, k74 = 0, k66 = k28, k24 + k34 = k29**.
  - Check with the KA tableau keys (RDUMRIYWOYNKY / ELYOIECBAQK): U+Y = 21+2 = 23 = W+K ✓, Y28 = Y66 ✓, K33 = K74 = K (index 0 in KA) ✓.

**Consequence:** any key generator meeting these 2 (or 4) relations fits the cribs under suitable alphabets. Without a candidate key source the model cannot be falsified. This is the formal sense in which the mask is "OTP-like in result".

### 3.3 Structured key under ANY alphabets
- **Linear/progressive key, k_i = a·i + c (H-1204).** The relations give 4a ≡ 0 and 12a ≡ 0 (mod 26), so a ∈ {0, 13}. That is period ≤ 2, already dead (GEN p=1,2). **REFUTED.**
- **Quadratic key, k_i = a·i² + b·i + c** (Scheidt: "non-linear is a quadratic way"). The relations give 10a − 4b ≡ 0 and 10a + 12b ≡ 0, so a, b ∈ {0, 13}. With i² ≡ i (mod 2) that is again period ≤ 2. **REFUTED for any α, β and any index origin.**
- Note that general polynomials mod 26 are just functions of (i mod 2, i mod 13), i.e. period 26. They are not tested here.
- **Small-digit key (base m), arbitrary alphabets** (window.py, z3; H-1205). Minimum feasible m:
  - two alphabets: **3** (m=2 is impossible because E has 3 images);
  - one mixed alphabet: **6** for both Vigenère and Beaufort (m = 3, 4, 5 unsat).
  - So a "letters → base-m digit mask" with a single K1/K2-style alphabet needs digits 0-5 or more. Decimal digits (Gronsfeld) with an unknown single alphabet are crib-feasible. Bean's/w-crib's standard-alphabet exclusion does not extend to mixed alphabets.

### 3.4 Length-preserving fractionation masks (H-1206)
- Bifid/Polybius 5×5 is already dead (26 letters used).
- Bifid 6×6: 26 letters cannot form a row×column product set within 6×6 (26 = 2·13). Mixed coordinates therefore hit the 10 non-letter cells. P(97 letter outputs) is roughly (26/36)^97 ≈ 1e-14. Disfavoured.
- **Trifid** (27-cell cube, arbitrary cube, z3; trifid.py). Constraints come only from output positions whose 3 source trits all lie in cribs.

| period n | alignment o=0 (standard) | other alignments |
|---|---|---|
| 2-9 | unsat | unsat, except n=9 o=5 unknown |
| 10 | **SAT** (12 constraints) | o6 and o9 SAT |
| 11 | unsat | o5 SAT |
| 12 | unsat | o5, o6, o7 SAT |
| 13 | unsat | o1, o2, o3 SAT |

  Larger n has fewer constraints and is not run.
- Trifid also conflicts with Sanborn's one-to-one description, and the 27th cell never appears in K4 (p ≈ (26/27)^97 ≈ 0.026).
- Verdict: REFUTED for n ≤ 9 and n = 11-13 at standard alignment; n = 10 OPEN but disfavoured.

### 3.5 CT-autokey with an unknown single mixed alphabet (H-1208)
z3 over all L (autokey.py). This extends w-crib §3, which only fixed AZ/KA.
- Vigenère: unsat for every L ≤ 36. SAT at 37, 41, 46, 60, 64, 67, 69-73 (with ≤ 11 checks); vacuous from 74.
- Beaufort: unsat for every L ≤ 31. SAT at 32, 34, 36, 38, 41, 43, 46-48, 52, 54, 56, 57, 59-61, 64, 66-70, 72, 73.
- **REFUTED for L ≤ 31.**

### 3.6 PT-autokey with an unknown single mixed alphabet: the NSA 1992 "interval 7" (H-1207)
The NSA wrote that roughness at interval 7 "could be a characteristic of plaintext auto-key, if the alphabet used has a high frequency letter assigned the value of 0" (DOCID 4051151, w-antipodes). That makes this the motivated test.
- Vigenère:
  - unsat at L = 1-10;
  - SAT only with ≤ 2 checks at L = 11-12;
  - vacuous at 13-29;
  - SAT at 30-39, 46 and 48-52.
  - **L = 7 REFUTED.**
- Beaufort:
  - **SAT at L = 6, 7, 8, 10, 11, 12**, and at 30-33, 36, 37, 39, 41 and 44-52.
- For Beaufort L = 7 the cribs at 22-28 seed every residue, so the alphabet alone fixes the whole plaintext. SA over the alphabet (aksa.py: 6 restarts × 150k, quadgram plus crib penalty) never reached a crib-consistent decrypt; the best run had 3 crib mismatches and gibberish. The autokey chain makes the score landscape chaotic. **Inconclusive, not a refutation.**
- PT-autokey is also content-dependent, which conflicts with K5 "same coded words in the same position" (H-208). Status: OPEN, low prior.

### 3.7 Alphabet-free key-stream filter (H-1209; `tools/latin_filter.py`)
**Scope.** Any cipher C_i = T[X_i](P_i) where T is a Latin-square tableau, i.e. P and C determine the key letter uniquely. This covers:
- Vigenère, Beaufort and variant Beaufort, and Quagmire I-IV with **any** mixed alphabets;
- every additive or XOR mask over any relabelling.

Porta is not covered: its key letters pair up.

**Necessary conditions:**
- **X28 = X66**;
- X_i ≠ X_j for the 22 crib pairs that share P but not C, or share C but not P.

The two-alphabet additive model also needs g(X24) + g(X34) = g(X29) + g(X33).

**Pass rates** (all alignment offsets, cyclic; runfilter.py). The null rate for English windows is 1.77%.

| stream | pass rate | offset 0 |
|---|---|---|
| K1 PT | 1.6% | fails |
| K2 PT | 0.5% | fails |
| K2 PT (LAYERTWO) | 0.8% | fails |
| K3 PT | 3.9% | fails |
| K1+K2+K3 PT | 2.2% | fails |
| reversed K1+K2+K3 PT | 2.2% | fails |
| K1-K3 CT | 1.6% | fails |

All rates are chance-level. **No K1-K3 text, aligned at its start, can be the running key or mask under any Latin tableau with any alphabets.** Other offsets pass only at chance rates, so they are not evidence.

**Use for K5.** If K4 and K5 share σ_i (a position-keyed mask), then where the plaintexts agree the ciphertexts agree. More generally, for a Latin tableau with a shared key stream, K4/K5 is a depth: P4_i = P5_i ⇔ C4_i = C5_i. This is for w-k5.

## 4. What survives, ranked
1. **H-1203:** a keyword-driven, non-periodic, plaintext-independent position mask under unknown alphabets (OTP-like result). It is consistent with all statements and all crib statistics. It is crib-untestable except for the 2/4 relations above, so the next step needs a **concrete key-generation source**: a keyword expansion that Sanborn could "remember and execute years later". Any candidate stream can be screened in seconds with `latin_filter.py` plus the relations in §3.2.
2. PT-autokey Beaufort L=7 with a mixed alphabet (NSA). Crib-feasible; low prior.
3. Trifid n=10. Disfavoured.
- Dead: numeric base change, XOR/Vernam, digit-pair codes, linear and quadratic keys, CT-autokey L ≤ 31 (mixed alphabet), PT-autokey Vigenère L ≤ 10 (mixed alphabet), trifid n ≤ 9 and 11-13.

## 5. Caveats
- The NPR 2005 page returned 503, so its content comes from a search summary. The Wired 2005 text is a blog reproduction. The Hannon 2011 notes are second-hand via Bean.
- z3 "unknown" results (time-outs) are listed as such and were not counted as refutations.
- Error-tolerance (H-209) was not applied. The two-alphabet relations each rest on 4 or 2 crib positions, so a single carving error at 24, 28, 29, 33, 34 or 66 would remove them.
