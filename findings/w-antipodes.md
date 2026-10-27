# w-antipodes — Antipodes transcript diff, NSA documents, Scheidt and Sanborn method statements (T9)
Worker: w-antipodes, 2026-10-26. Hypothesis IDs: H-901 to H-904.

## TL;DR
1. **The K4 text on Antipodes is letter-for-letter identical to facts/ciphertext.txt in both full copies.** I diffed a published 47-row line-level transcript of the English side (scirealm.org) and spot-checked it against Elonka's Hirshhorn photos. The photos cover all 97 positions of copy 1. There are no K4 corrections, nulls or extra letters. The only K4-related difference is layout: a double blank follows K4 in copy 1 and no blank follows it in copy 2.
2. Antipodes differences elsewhere: in K2, the ciphertext R is changed to E (`BQCRTBJ`→`BQCETBJ`), which corrects UNDERGRUUND to UNDERGROUND; I verified this by decryption. Two dots also flank an F in K2 (`ZBS.F.DQV`, at the "ONLY WW" plaintext). By 1997, then, Sanborn did fix a ciphertext typo. He changed nothing in K4, and he did not restore the K2 "missing S" (the K2 ending is identical to the CIA copy, so it still decrypts to ...IDBYROWS).
3. NSA FOIA (1992-93 documents, obtained via Elonka's Google Drive mirror, OCR'd). On K4, the NSA analysts noted "roughness on interval 7". They tried plaintext autokey and "transposed substitution", plus the hypothesis "substitution with K1-K3 alphabets, then a K3-style transposition". None worked. I reproduced the interval-7 signal: 9 coincidences against 3.5 expected, single-test p≈0.005, but family-wise over d≤24 p≈0.09, so it is weak. The 2007 "KRYPTOS Summary" is still not retrievable: nsa.gov and media.defense.gov return 403, and web.archive.org breaks the tunnel. Its content is known only from Bean 2021's citation.
4. Scheidt 2020 (AJ Jacobs phone interview, Rev.com transcript): the steps were substitution, then transposition ("push into this square"), then a final "mask" that "changes the language base". The new base is "Not to another language, it's to something else", and it is not like a one-time pad "per se" but similar "in the sense of the result". 2025-26: there is no new Sanborn method hint beyond the Nov 2025 SciAm clues. The RR lot list mentions an "original coding system for K4", "plain texts used for screen cutting K4 (2 pieces)", and an "alternate K1 plaintext and coding chart".

## (a) Antipodes (Hirshhorn, 1997; Smithsonian 98.22)

### Sources
- S1. Elonka Dunin, "Sanborn's Antipodes Sculpture", https://elonka.com/kryptos/sanborn/antipodes.html (6/20/2005 update), says the text order is K3 → K4 → *space* → K1 → K2 → K3 → K4 → (*no space*) → K1 → K2, truncated mid-K2. There are "two dots ... correspond[ing] to ... WW".
- S2. John W. (SciRealm), "Antipodes" page, https://scirealm.org/Antipodes.html (last modified 2015-04-25; older copy at austininc.com/SciRealm, cited by Wikipedia). This is the **only letter-level transcript I found**: a 47-row Kryptos-side table (plus the Cyrillic side). It notes the dots `.F.`, the blank, and the UNDERGROUND correction. Rows are copied in Appendix A.
- S3. Elonka's photo directory, https://elonka.com/kryptos/sanborn/antipodes/images1.html (+images2/3): 45 JPEGs, about 800×580 px each. Antipodes1.jpg is a mirror image (shot through the cut-outs from the back). The best files for K4 are:
  - Antipodes7.jpg and Antipodes11.jpg (copy 1, middle and right of rows 10-13, including `UEKCAR  EMUF` with the blank);
  - Antipodes9.jpg (copy 1, left of rows 10-15);
  - Antipodes1.jpg, mirrored (copy 2, rows 35-41);
  - AntipodesDetail.jpg (copy 2, rows 38-45, large letters).
- S4. Wikipedia "Antipodes (sculpture)", https://en.wikipedia.org/wiki/Antipodes_(sculpture): "select differences ... spacing, additional dots and letters". It lists no letters. Its Commons photos (Antipodes Front / Proper Right / Proper Left) could not be fetched (Commons API returned 429 and FilePath returned 404).
- S5. Kryptos Group 2005 DC trip notes, http://kryptos.yak.net/53. Per the search snippet, Sanborn called the two dots a "typo". The site returned 503 and the Wayback Machine was unreachable, so the full text is unverified.
- Searches of Reddit, blogs and GitHub (code search "Antipodes kryptos") found no other transcript. Wikipedia also links http://www.thekryptosproject.com/tjp/observations/cracks.php ("Crack positioning ... Kryptos and Antipodes"), which I did not fetch.

### Method
CIA reference = the Elonka transcript (https://elonka.com/kryptos/transcript.html), 28 cipher rows, 869 characters including the 4 '?'. Its K4 equals facts/ciphertext.txt exactly. Antipodes stream = the 47 S2 rows concatenated (1594 characters including blanks and dots). I aligned them with difflib (script: `/tmp/claude-0/-home-user/046a83fd-aa4b-57f6-97e0-639b3d9e1ef4/scratchpad/diff.py`).

### Diff results (positions are indices in the CIA 869-character stream; K1 = 0-62, K2 = 63-434 including '?', K3 = 435-771, K4 = 772-868)
| # | Where | CIA | Antipodes | Antipodes copy | Meaning |
|---|-------|-----|-----------|----------------|---------|
| 1 | K2, stream idx 178 (row 6 of the CIA sheet, `BQC_TBJ`) | R | E | copy 2 (row 19) and copy 3 (row 44) | Decrypts UNDERGRUUND→UNDERGROUND (verified with ABSCISSA/KA). A deliberate error correction. |
| 2 | K2, between idx 293/294 and 294/295 (`ZBS F DQV`) | — | `.` `.` | copy 2 only (row 22) | Dots flank cipher F, at plaintext "ONLY W.W."; these are punctuation, not letters. Copy 3 is truncated before this point. |
| 3 | after K4 (copy 1) | — | 2 blanks | copy 1 (row 13 `UEKCAR  EMUF`) | Separator K4→K1; confirmed in photos Antipodes7 and 11. |
| 4 | after K4 (copy 2) | — | none | copy 2 (row 39 `UEKCAREMUF`) | No separator. |
| — | **K4, all 97 positions, both copies** | — | **identical** | rows 10-13 and 36-39 | **No difference.** |
| — | K3 (copy 1 complete, copy 2 complete), K1 (2 copies) | — | identical | | |
| — | K2 ending (the 2006 "missing S", plaintext IDBYROWS vs XLAYERTWO) | — | identical, no S added | row 26 `...JLLAETGENDYAH` (also legible in Antipodes1 mirrored) | Not corrected on Antipodes. |

Photo check of K4 (I read the stencil letters myself at 2× upscale):
- **Copy 1** (rows 10-13):
  - Antipodes11 shows the row-10 end `...VDOHW?OBK` (pos 1-3), the row-11 end `PRNGKSSOTW` (pos 28-37), the row-12 end `BNYPVTTMZF` (pos 63-72) and `EKCAR  EMUF...`.
  - Antipodes7 shows `LIFBBWFLRVQQPRNGKSSOTW` (16-37), `ZWATJKLUDIAWINFBNYPVTTMZF` (46-72) and `KUHUAUEKCAR  EMUFPHZL` (86-97).
  - Antipodes9 shows `RUOXOGHULBSOLIF` (4-18), `TQSJQSSEKZZWATJKL` (38-54) and `PKWGDKZXTJCDIGKU` (71-86).
  - Together these cover all 97 positions, and every one matches.
- **Copy 2** (rows 36-39, Antipodes1 mirrored): `?OBKRUOX`, `FBBWFLRVQQPRNGKSSOTWTQS`, `TJKLUDIAWINFBNYPVTTMZFPKW`, `GKUHUAUEKCAREMUFPHZLRFAX` all match. The row ends at the curved edges are illegible.

Line breaks: Antipodes rows are 32-37 characters wide (not fixed), so the 31-wide CIA layout is not preserved. K4 starts at the end of a row in both copies (`?OBK` in copy 1, `?OBKRUOXOGHULBS` in copy 2). SciRealm notes that "SSO" sits under the "?" in both copies. Given the variable row widths, I treat that as a coincidence (w-stats already found the 31-wide layout carries no signal).

### Assessment (H-901, H-902)
- **H-901 (REFUTED): "Antipodes carries a corrected or variant K4 ciphertext."** Both copies match exactly, with full photo coverage of copy 1. facts/ciphertext.txt stands as carved, and nothing on Antipodes suggests a K4 typo.
- **H-902 (weak inference, OPEN): "The K4 ciphertext as carved is what Sanborn intended."** In 1997 Sanborn knowingly fixed a ciphertext letter in K2 (R→E) and added WW dots, but changed nothing in K4. If K4 contained an encryption error he knew about, Antipodes would have been the place to fix it. Caveats:
  - He may not have known of K4 errors, because K4 was never decrypted publicly.
  - The K2 "missing S" was also left unfixed. Sanborn 2006 called it deliberate "for aesthetic reasons" (Wired 2006, via S1 timeline), which fits.
  - Net: this mildly favours "no carving error in K4" and weakly supports ruling out error-correction hunts as a first-line approach.
- The blank after copy-1 K4 shows that Sanborn treats `OBKR...KCAR` as one unit. The '?' before OBKR is kept in both copies, consistent with it being K3's final punctuation (CANYOUSEEANYTHING?), not part of K4.

## (b) NSA documents

### Obtained
"FOIA Results" (Elonka FOIA #61191, released 21 May 2013), 40-page scanned PDF. Source: Google Drive file linked from https://elonka.com/kryptos/foia.html (id 0B7G1aFZQuZtXRmRkcmhkNGtqQ2c; also https://elonka.com/kryptos/foia.zip). I OCR'd it with tesseract; the scratch copy is `.../scratchpad/ant/nsa/z/ocr_all.txt`. It contains DOCIDs 4050988 (memo of 9 June 1993), 4050989, 4051151 (the full write-up "KRYPTOS sculpture"), a memo of 26 March 1992/1 Dec 92, and an internal timeline.

K4-relevant content (quoted from the OCR, checked against the page images):
- Memo of 9 Jun 1993: "The final 97 characters continue to elude solution."
- Memo of 1 Dec 92: "Although ideas abound, a successful break into part 4 has not been made".
- DOCID 4051151, "DIAGNOSIS": "the data also revealed a bias in the third section [= lines 26-28, i.e. K4] at an interval of 7. There is no specific cryptography that would give such a result, but a number of them could ..."
- DOCID 4051151, "THE FOURTH BREAKTHROUGH?":
  - "A statistical analysis of this portion showed some roughness on interval 7. This could be a characteristic of plaintext auto-key, if the alphabet used has a high frequency letter assigned the value of 0."
  - "Another hypothesis is that this last section employs both of the systems already used. First the message is encrypted using some set of alphabets ... and then the cipher is put through a transposition ... If the original text had a repeat at a distance of 7 apart (or perhaps 14 or even 21 apart), then after transposing the text, the repeat would now show up in the interval statistic rather than the width statistic."
  - "There is no solution at the current time, although some attempts have been made using plaintext auto-key and other attempts using transposed substitution as the enciphering mechanism."
- RECAP: "It is highly probable that KRYPTOS plays an integral part in the solution."
- Also noted (p.26): the raised letters Y, A, R after "END" on the sculpture, and the '?' characters as possible system transitions.
- The NSA's K3 description is a keyed columnar transposition, "incompletely filled 4 X 86, using a key of KRYPTOS ... numerically keyed and repeated 13 times". This already matches facts.

Reproduction of the interval-7 signal (my computation on facts/ciphertext.txt):
- Coincidences C[i]=C[i+7] = 9 of 90 (expected 3.46) at pairs 1/8 O, 8/15 O, 13/20 B, 16/23 L, 33/40 S, 46/53 K, 66/73 P, 77/84 D, 87/94 K (1-indexed). This is the highest of any d=1..24; the next highest is d=1 with 6.
- Binomial p=0.0079 and shuffle p=0.005 for d=7 alone, but **P(max over d≤24 ≥ 9) = 0.087 under shuffle**, so it is not significant after look-elsewhere correction.
- It is related to w-stats' width-7 doublet anomaly (post-hoc, FW p=0.004). Both point at 7 with the same caveat.
- Crib overlap: pair 66/73 (ciphertext P at both, plaintext R and C) shows that, without a transposition, the distance-7 repeats are not plaintext repeats. This matches the existing elimination of period 7. Only a transposition-based model (the NSA's hypothesis) could turn the repeats into a plaintext feature. In pair 33/40 (S) pos 33 is plaintext S; in pair 16/23 (L) pos 23 is plaintext A.

### Not obtained
The 2007 "The CIA KRYPTOS Sculpture: A summary of previous work and new revelations in working toward its complete solution" (Redacted 2007; NSA DOC_7 / "KRYPTOS Summary.pdf").
- nsa.gov (Portals/70 and 75, igphoto/2002760463) and media.defense.gov return 403. web.archive.org fails at the proxy (tunnel closed). The archive.org availability API has no snapshot of yak.net/53.
- governmentattic and cryptome have no copy that I could find. MuckRock returns 403.
- GitHub has only a "quote-free" stub (malak333/kryptos-k4, sources/archives/nsa-kryptos-summary-revelations-2026-05-28.md).
- What is known secondhand (Bean 2021 §2.3, https://ecp.ep.liu.se/index.php/histocrypt/article/view/153): the 2007 analyst "suggested this property [doublets BB QQ SS ZZ TT in one column at width 7] could be due to combined polyalphabetic substitution and transposition". The Conversation (Bean 2021) adds that dozens of agency staff failed. **The team should fetch it from a network without the 403**; the URL is in Bean's references.

### Added to ruled_out.md
These are historical attempts and are labelled as non-proofs:
- plaintext autokey (NSA 1992, informal; now formally covered by w-crib §3);
- substitution+transposition attempts (NSA 1992, informal, unspecified scope, so it does not eliminate that class).

## (c) Scheidt and Sanborn statements on method

### Ed Scheidt
- **Wired Q&A, 21 Jan 2005** (reproduced at https://kryptosfan.wordpress.com/k4/artichoke/masking-vs-english/; original https://www.wired.com/2005/01/questions-for-kryptos-creator/ is paywalled and was not fetched):
  - "All four (sections) are done in the English language."
  - In K1-3 "the English language is still visible through the code. (But with) this other technique (in the fourth part), I disguise that. So … you need to solve the technique first and then go for the puzzle."
- **NPR, 9 Jun 2005**: "deliberately masked" (already in facts).
- **2011 Zola dinner** (Hannon notes, via Bean 2021): "not mathematical ... simple, can be remembered, and executed years later when used with the correct key word/s"; "similar to what would be provided agents or pilots in case of capture".
- **ACA banquet talk, 2013** (blog recap https://kryptosfan.wordpress.com/2013/10/30/more-about-ed-scheidts-aca-talk/): he showed pages of the NSA FOIA document. On hiding the receiver's identity, he said "built into the process" but gave no clue. The talk was not recorded.
- **Schmeh workshop, 2015** (via Bean): K4 is "more than one stage".
- **AJ Jacobs phone interview, Nov 2020.** Rev.com transcript, 17 pp, groups.io file PersonalFolders/AJJacobs/EdScheidtKryptosTranscript.pdf (login-walled). Readable mirror: https://raw.githubusercontent.com/aciderix/kryptos-research-handoff/HEAD/sources/groupsio_membres/textes/Personal%20Folders/AJ%20Jacobs/EdScheidtKryptosTranscript.pdf.txt. Key verbatim passages:
  - "substitution was one I had to use, another math problem is transposition ... you're defining the parameters of the puzzle in the sense of the square, and then now you have the square and you're going to transpose the characters or the letters that are in the square to something that's a secret. So my secret is push into this square. So that was another step. And then the last step ... I masked the framework, in other words if you can change the language base then it becomes in my favor".
  - "mask ... If I use that directly in the puzzle I have against me the number of Es, the number of Ys and number Xs ... Now if I can mask that, change that characteristic".
  - Changing the language base is "Not to another language, it's to something else."
  - Asked whether this is a one-time pad: "not directly related ... The analogy is reasonable, but reasonable in a sense of the result."
  - "Linear is a direct substitution, non-linear is a quadratic way of looking at it."
  - "That's if you're going to keep it as a pencil and paper system."
  - Interpretation (UNVERIFIED): this describes K1-K3 as a staircase (substitution, then a transposition square). The K4 "mask" sits on top and flattens the frequencies, possibly by recoding letters into another symbol set or base, which fits Bean's base-arithmetic and Gromark reading. That would make the K4 statistics (IC 0.036, near random) the designed effect of the mask rather than of the substitution alone.

### Sanborn and others, 2025-26
No new method hints. Facts:
- Sanborn (AFP, Oct 2025): "five pieces of scrambled texts ... without the coding method or the key". https://citizen.digital/article/auction-of-famed-cia-cipher-shaken-after-archive-reveals-code-n373254
- Kobek (Zona Motel interview, 17 Oct 2025, https://zonamotel.substack.com/p/interview-kryptos-k4-uncovered-jarett):
  - the scrap was "a piece of paper where different things have been cut up and put together";
  - it held "the text of the known parts of Kryptos that have been decoded, not the full text", and "the remainder ... seems to be the same number of characters";
  - "There's no way on earth that this is a cryptographic solve."
- RR Auction lot list (https://www.rrauction.com/jim-sanborn-kryptos-k4-solution-auction/):
  - "the original coding system for K4";
  - "handwritten signed Kryptos plain texts used for screen cutting K4 (2 pieces)";
  - "original unpublished 1988 alternate K1 plaintext and coding chart";
  - "1988 alternate K4 plaintext and coding chart now known as K5";
  - "the original scrambled texts shown to the Department of Historical Intelligence".
  - So K4 had a *coding chart* like K1-K3, and K5 was made with its own chart in 1988, the same year.
- RR "Discovered, not solved" (https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/): the method is "known only to Jim Sanborn and ... Ed Scheidt, who helped design the encryption system in 1988". Sanborn's archive practice: "he cut sentences into strips and taped them together out of order" (this refers to the scrambled texts, not to the cipher).
- Paradigm (https://www.paradigm.xyz/writing/kryptos, 12 Jun 2026): SHA256 verifier; "Sanborn also provided the ciphertext for another 97-character puzzle, known as K5, that he created at the same time"; K5 to be released later. Nothing on method, and the plaintext normalization rules are unpublished. **Not used.**
- Secondhand (search snippet only, UNVERIFIED): at a talk Sanborn joked "Who says it is even a math solution?"

## Hypotheses logged
- H-901 Antipodes K4 variant: REFUTED.
- H-902 K4 as carved is intended (no carving error): weak support, OPEN.
- H-903 NSA interval-7 roughness: reproduced, family-wise p≈0.09. OPEN as a lead, together with the w-stats width-7 doublets, for "substitution then width-7-family transposition" (the NSA 1992 hypothesis). Not tested here.
- H-904 Scheidt 2020 "mask = change of language base, not another language": interpretation only. It suggests a symbol or base recoding layer (e.g. letters→digits/base-n→letters) on top of a substitution plus a square transposition. OPEN, for the coordinator.

## Sources (26)
1. https://elonka.com/kryptos/sanborn/antipodes.html
2. https://www.elonka.com/kryptos/sanborn/temp/antipodes.html
3. https://elonka.com/kryptos/sanborn/antipodes/images1.html (+ images2, images3, 45 JPEGs)
4. https://scirealm.org/Antipodes.html
5. https://en.wikipedia.org/wiki/Antipodes_(sculpture)
6. https://en.wikipedia.org/wiki/Kryptos
7. https://elonka.com/kryptos/transcript.html
8. https://elonka.com/kryptos/foia.html
9. Google Drive FOIA PDF (id 0B7G1aFZQuZtXRmRkcmhkNGtqQ2c), NSA DOCIDs 4050988/4050989/4051151, FOIA case 61191
10. https://ecp.ep.liu.se/index.php/histocrypt/article/view/153 (Bean 2021, PDF fetched)
11. https://theconversation.com/declassified-cold-war-code-breaking-manual-has-lessons-for-solving-impossible-puzzles-161595 (snippet)
12. https://www.nsa.gov/Helpful-Links/NSA-FOIA/Declassification-Transparency-Initiatives/FOIA-Reports-and-Releases/FOIA-Reports-and-Releases-List/igphoto/2002760463/ (403)
13. https://raw.githubusercontent.com/malak333/kryptos-k4/HEAD/sources/archives/nsa-kryptos-summary-revelations-2026-05-28.md (stub)
14. https://raw.githubusercontent.com/aciderix/kryptos-research-handoff/HEAD/sources/groupsio_membres/textes/Personal%20Folders/AJ%20Jacobs/EdScheidtKryptosTranscript.pdf.txt
15. same repo, Clarke Summary v3.1 (identifies 2007 summary = NSA doc_7.pdf)
16. https://kryptosfan.wordpress.com/k4/artichoke/masking-vs-english/
17. https://kryptosfan.wordpress.com/2013/10/30/more-about-ed-scheidts-aca-talk/
18. https://kryptosfan.wordpress.com/speculations/steganography/ (snippet)
19. https://zonamotel.substack.com/p/interview-kryptos-k4-uncovered-jarett
20. https://www.rrauction.com/jim-sanborn-kryptos-k4-solution-auction/
21. https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/
22. https://www.paradigm.xyz/writing/kryptos
23. https://citizen.digital/article/auction-of-famed-cia-cipher-shaken-after-archive-reveals-code-n373254 (snippet)
24. https://elonka.com/kryptos/ (Aug 2025 status)
25. http://kryptos.yak.net/53 (snippet only, 503)
26. https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/ (via search; already in facts)

## Appendix A — Antipodes English side, 47 rows (transcribed from S2; "  " = blank, "." = dots)
 1: ENDYAHROHNLSRHEOCPTEOIBIDYSHNAIACH
 2: TNREYULDSLLSLLNOHSNOSMRWXMNETPRNG
 3: ATIHNRARPESLNNELEBLPIIACAEWMTWNDITE
 4: ENRAHCTENEUDRETNHAEOETFOLSEDTIWENH
 5: AEIOYTEYQHEENCTAYCREIFTBRSPAMHHEWE
 6: NATAMATEGYEERLBTEEFOASFIOTUETUAEOT
 7: OARMAEERTNRTIBSEDDNIAAHTTMSTEWPIER
 8: OAGRIEWFEBAECTDDHILCEIHSITEGOEAOSDD
 9: RYDLORITRKLMLEHAGTDHARDPNEOHMGFMF
10: EUHEECDMRIPFEIMEHNLSSTTRTVDOHW?OBK
11: RUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTW
12: TQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZF
13: PKWGDKZXTJCDIGKUHUAUEKCAR  EMUFPHZL
14: RFAXYUSDJKZLDKRNSHGNFIVJYQTQUXQBQV
15: YUVLLTREVJYQTMKYRDMFDVFPJUDEEHZWE
16: TZYVGWHKKQETGFQJNCEGGWHKK?DQMCPFQ
17: ZDQMMIAGPFXHQRLGTIMVMZJANQLVKQEDA
18: GDVFRPJUNGEUNAQZGZLECGYUXUEENJTBJL
19: BQCETBJDFHRRYIZETKZEMVDUFKSJHKFWHK
20: UWQLSZFTIHHDDDUVH?DWKBFUFPWNTDFIYC
21: UQZEREEVLDKFEZMOQQJLTTUGSYQPFEUNLA
22: VIDXFLGGTEZ?FKZBS.F.DQVGOGIPUFXHHDRKF
23: FHQNTGPUAECNUVPDJMQCLQUMUNEDFQELZ
24: ZVRRGKFFVOEEXBDMVPNFQXEZLGREDNQFM
25: PNZGLFLPMRJQYALMGNUVPDXVKPDQUMEBE
26: DMHDAFMJGZNUPLGEWJLLAETGENDYAHROH
27: NLSRHEOCPTEOIBIDYSHNAIACHTNREYULDSL
28: LSLLNOHSNOSMRWXMNETPRNGATIHNRARPE
29: SLNNELEBLPIIACAEWMTWNDITEENRAHCTEN
30: EUDRETNHAEOETFOLSEDTIWENHAEIOYTEYQ
31: HEENCTAYCREIFTBRSPAMHHEWENATAMATEG
32: YEERLBTEEFOASFIOTUETUAEOTOARMAEERT
33: NRTIBSEDDNIAAHTTMSTEWPIEROAGRIEWFEB
34: AECTDDHILCEIHSITEGOEAOSDDRYDLORITRKL
35: MLEHAGTDHARDPNEOHMGFMFEUHEECDMRIP
36: FEIMEHNLSSTTRTVDOHW?OBKRUOXOGHULBS
37: OLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZ
38: WATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJ
39: CDIGKUHUAUEKCAREMUFPHZLRFAXYUSDJKZ
40: LDKRNSHGNFIVJYQTQUXQBQVYUVLLTREVJY
41: QTMKYRDMFDVFPJUDEEHZWETZYVGWHKKQ
42: ETGFQJNCEGGWHKK?DQMCPFQZDQMMIAGPF
43: XHQRLGTIMVMZJANQLVKQEDAGDVFRPJUNG
44: EUNAQZGZLECGYUXUEENJTBJLBQCETBJDFH
45: RRYIZETKZEMVDUFKSJHKFWHKUWQLSZFTIH
46: HDDDUVH?DWKBFUFPWNTDFIYCUQZEREEVLD
47: KFEZMOQQJLTTUGSYQPFEUNLAVIDXFLGGTE
