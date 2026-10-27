# w-runkey T11: running-key hypothesis for K4   (w-runkey, 2026-10-26 UTC)

**Bottom line: no crib-passing candidate. A plain-language running key through any standard tableau is statistically excluded, and every motivated source text fails the crib check at every offset (best 9/24, which is chance level).**

Scripts and outputs are in workers/w-runkey/: common.py, part1.py, part1b.py, part2.py, plus the *.out files.
- The scripts expect a working directory containing:
  - qg.tsv, built with `tools/quadgram.py build qg.tsv pg2600.txt pg1342.txt` (3,070,172 letters, 63,958 quadgrams);
  - dl/ for the downloaded texts;
  - corp/ for the normalized corpora (A-Z only, listed in §2).
- Positions are 1-indexed. Cribs are EASTNORTHEAST at 22-34 and BERLINCLOCK at 64-74, 24 letters in all.
- Tableaux:
  - Vig: C=P+K. Beau: C=K-P. vBeau: C=P-K.
  - Each rule is run over AZ and over KA = KRYPTOSABCDEFGHIJLMNQUVWXZ.
  - The key letter is read in the same alphabet.

## 1. Keystream at the crib positions
| tableau | key @22-34 | key @64-74 |
|---|---|---|
| Vig/AZ | BLZCDCYYGCKAZ | MUYKLGKORNA |
| Beau/AZ | JLJODEGKUKKKL | OCGGBGOKTRU |
| vBeau/AZ | ZPBYXYCCUYQAB | OGCQPUQMJNA |
| Vig/KA | RDUMRIYWOYNKY | ELYOIECBAQK |
| Beau/KA | WXAKGZTOAXAFD | RGTGNWRJLFK |
| vBeau/KA | ZJOBZEXPUXAKX | ICXUEILMNSK |

All 24 crib letters re-encrypt correctly in every tableau, and the table is identical to w-crib §1. The 12 mixed tableaux are also included (PA≠CA in {AZ,KA}, key letter read in AZ or KA); see part1b.py.

### 1a. Are the fragments English? (quadgram test)
Statistic: mean log10 quadgram probability over the 10 quadgrams of the 13-letter fragment plus the 8 of the 11-letter fragment (18 in all). Each null has 100k samples:

| null | q24 mean ± sd | mono24 LLR mean ± sd |
|---|---|---|
| Uniform random letters | -8.08 ± 0.35 | -6.4 ± 3.0 |
| H1, English | -4.25 ± 0.38 | +3.8 ± 1.3 |
| Wrong tableau | -8.04 ± 0.38 | -5.9 ± 3.1 |

- **H1, English:** the true running-key situation. Two English fragments start 42 apart in one text. They were drawn from Moby Dick, Sherlock Holmes, Tale of Two Cities and Huck Finn, which are disjoint from the model corpus.
- **Wrong tableau:** an English plaintext was encrypted with an English running key under a random tableau, and the keystream was then derived with a different tableau.

Observed q24, forward and reversed:
- Vig/AZ: -8.14 / -8.31
- Beau/AZ: -8.25 / -8.07
- vBeau/AZ: -8.49 / -8.49
- Vig/KA: -8.05 / -7.66
- Beau/KA: -8.49 / -8.49
- vBeau/KA: -8.10 / -7.87
- All 12 mixed tableaux: between -7.36 and -8.49.

**Every fragment pair is typical of uniform noise.**
- Under H0, P(q24 ≥ obs) ranges from 0.12 to 1.0.
- Under H1, P(q24 ≤ obs) = 0 in 100k for every tableau. The fragments sit about 10 sd below English.
- The monogram test agrees. Its weakest case is Vig/KA at -2.24 against English +3.8±1.3, giving P1 = 2e-4. This matches w-crib §6.

**Robustness checks:**
- **1-2 encryption or carving errors.** I let the optimizer replace any 2 of the 24 key letters to maximise q24. The best results are -6.6 (Vig/KA) to -7.5, still more than 5 sd below English. This is a selection-biased upper bound (part1b_errs.out).
- **Inserted or omitted letter between the cribs.** The fragments are scored independently, so the result does not depend on the 42-letter spacing.
- **Reversed key text.** Same result as forward.
- **German key text.** This was motivated by the BERLIN crib. A German quadgram model from 4 Gutenberg-DE texts gives H1 = -4.14±0.48. The observed values are -7.30 to -7.72, so P1 ≤ 6e-5 for all 6 tableaux.

**"42 letters apart in one English text":** this only matters if each fragment is English on its own. Neither is, in any tableau, so the joint test is moot. The fragments carry no exploitable dependence across a 29-letter gap anyway, because the joint score factorizes.

**Conclusion (H-1101):** K4 is not plaintext ⊕ (natural-language running key) under any of the 18 standard or Quagmire-style tableaux with AZ/KA alphabets and no transposition. This holds whatever the source text and offset, and it tolerates ≤2 errors. The test is statistical, not a proof. Still open:
- a running key that is itself enciphered, mixed, or non-language (OTP-like);
- a running key under an arbitrary unknown alphabet;
- any scheme with a transposition stage.

## 2. Motivated source texts slid over K4 (exact crib check)
Method: key_i = T[o+i] for every offset o at which at least one crib position falls inside the text. Texts shorter than 300 letters are also repeated cyclically. Each text is run forward and reversed through all 6 tableaux and scored as the number of crib letters matched out of 24. Then 12 mixed tableaux were run as well.
- **Positive control:** a synthetic K4 built with a Carter key at offset 123456 is recovered at 24/24 in all 6 tableaux.
- **Comparison:** keithadler's planted test reports 22/24 with 2 typos.

| text (letters) | rationale |
|---|---|
| K1pt 63, K2pt corrected 370 / carved 369, K3pt 336, K1+K2+K3 concatenated (corrected and carved), K1-K3 ciphertext 768 | Sanborn says K1-K3 contain information for K4. The keystream = earlier plaintext idea is cheap. |
| Morse text: 5 readings (word order, reversed, panel order with and without filler E, "WHAT IS YOUR POSITION" normalized), 80-106 letters | It is on the sculpture and is the "first" message. |
| KA tableau rows, 676 | It is the sculpture's tableau. |
| Carter & Mace, *The Tomb of Tut.ankh.Amen* vol. 1. Two independent OCRs: Doran NY 1923 (archive.org tomboftutankhame00cart_1, 284,914 letters) and the DLI copy (in.ernet.dli.2015.106167, 281,199 letters) | This is the K3 source. The OCR is clean: the K3 passage "SLOWLYDESPERATELYSLOWLY…" was checked. PG-US does not carry vol. 1. |
| National Security Act 1947 (61 Stat. 495, govinfo; 43,954 letters), its §102 alone (CIA charter), and the current compiled NSA (COMPS-1493, 468,511 letters) | This is the CIA charter. |
| Oath of office, 5 USC 3331 | The CIA employee oath. |
| John 8:32, plus the whole KJV (PG #10) | John 8:32 is the CIA lobby inscription. The KJV also re-checks keithadler's Bible claim. |
| CIA "Kryptos" page (incl. 1988 Statement of Principles for the art commission) and the CIA mission/vision page | Agency text tied to the commission. The mission page is modern, so its prior is low. |
| Sanborn open letter, Aug 2025 | A Sanborn statement. |

**Results (part2.out):**
- **Standard tableaux.** 52,035,624 offset×tableau checks in total.
  - Match histogram from 0 to 9: 22.2M, 19.1M, 8.07M, 2.16M, 403k, 55.9k, 5.8k, 493, 34, 1. Nothing at 10 or above.
  - The single 9/24 is KJV reversed, Vig/KA, offset 260668.
  - Carter's best is 8/24. K1-K3, Morse, oath, charter and Sanborn texts all score 7 or lower.
  - The best single-fragment match anywhere is 6/13 for EASTNORTHEAST and 7/11 for BERLINCLOCK. A whole fragment matching would have exposed a local match broken by a running-head or OCR insertion; none did.
- **Mixed tableaux.** 104M checks, max 9/24.
- **Chance level.** Per-check P(≥9) is about 1e-7 to 2e-7 (Poisson-binomial with English letter frequencies), so a few 9s are expected at 5e7-1e8 checks. P(≥20) is about 1e-26.
- **No offset reaches 20/24. No offset even reaches 10/24.**

## 3. Published work (web search, 2026-10-26)
- **keithadler/kryptos** (GitHub, SEARCH.md, "status as of 2026-09-29", unreviewed, no author credentials). Its running-key section reports:
  - B1: K1-K3 plaintexts, the carved left side and the tableau, forward and reversed, every offset, 8 families → eliminated.
  - B2: K1-K3 solutions with an arbitrary alphabet on one side, including carved and corrected spellings, IDBYROWS and the K1-K3 ciphertext → 141k tests, 0 survivors.
  - B3: Carter vols 1-3, KJV, Declaration, Constitution, Bill of Rights, Poe vol. 1 and G. E. Smith's 1923 Tutankhamen account, 8 families, OCR- and typo-tolerant → 149M offsets, best 9/24 ("chance reaches about 36 times").
  - **My results independently reproduce B1 and B3 (best 9/24).** This upgrades w-lit's "treat as leads" entry for Carter, Bible and K1-K3.
  - Not covered there: Morse, CIA charter/oath/John 8:32, Sanborn letter, CIA pages, mixed key-letter conventions, and the source-independent statistical test of §1.
- **Bean, HistoCrypt 2021.** He discusses Gromark ("running key" in the ACA sense) and does not test running keys from texts.
- **Hobbyist "solutions"** (dearcipher.space: Beckett/Wordsworth multi-layer running keys; academia.edu 2026 "definitive" paper): unverified and not reproducible from what is published. Neither is a single-layer running key through a standard tableau, which §1 excludes in any case.
- No published source-independent test like §1 was found. Bean and w-crib §6 give only the monogram version.

## 4. What remains open
- A running key under an unknown or arbitrary mixed alphabet, or a keyed tableau other than KA (Quagmire with unknown alphabets). The cribs cannot test this, and keithadler B2 covers only K1-K3 texts.
- A running key combined with a transposition or other second stage, in line with Scheidt's "layers" and "masking".
- A non-language key: an enciphered text, coordinates, a numeric or clock-derived stream, or K5. If the K5 ciphertext is released, its shared-position words become a test.
