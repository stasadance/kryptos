# w-lit: Facts verification, 2025-26 archive/auction status, published eliminations
Worker: w-lit | Date: 2026-10-26 | Task T1

## 1. Verification of facts/known_facts.md and facts/cribs.md

| Item | Status | Sources |
|---|---|---|
| K4 = 97 letters; our ciphertext.txt | VERIFIED. Our file matches Elonka's transcript character for character (checked by script) | elonka.com/kryptos/ ; Sanborn open letter Aug 2025 ("97-character K4 code section"); Bean 2021 |
| K1 = Quagmire III/Vigenere, KRYPTOS alphabet, key PALIMPSEST | VERIFIED | en.wikipedia.org/wiki/Kryptos ; Gillogly 16 Jun 1999 (packetstorm mirror) ; Stein CIA report (NSArchive EBB431) |
| K2 = same scheme, key ABSCISSA | VERIFIED. Also: 2006 correction, a missing S means the plaintext ends WESTXLAYERTWO | Wikipedia; Elonka timeline; Wired 2006 |
| K3 = transposition | VERIFIED. 336 letters, transposition only (Stein: letter frequencies are English) | Stein; Gillogly ("three columnar transpositions"); NSA per rumkin K3 page ("keyed columnar transposition in incompletely filled 4x86 matrix", secondary) |
| Hint years and positions | VERIFIED. BERLIN 64-69 (NYT 20 Nov 2010); CLOCK 70-74 (NYT 20 Nov 2014); NORTHEAST 26-34 (NYT 29 Jan 2020); EAST 22-25 (given privately Apr 2020, public Aug 2020) | elonka.com/kryptos ; Klausis Krypto Kolumne 30 Jan 2020 & 24 Aug 2020; Wikipedia. Note: the Smithsonian Magazine article of 31 Jan 2020 swaps the BERLIN and CLOCK years, so do not cite it for that |
| "Sanborn: K4 uses a masking technique" | CORRECTED. "Masking" is Scheidt's word. Sanborn was confused by it at the Mar 2019 lunch (Elonka's notes). Scheidt: NPR 9 Jun 2005 "deliberately masked" (paraphrase); 2020: "when it was used as the mask" (Jacobs transcript, quoted in Bean 2021) | rumkin.com/reference/kryptos/k4/ ; Bean 2021 |
| "K5 exists and shares method/position cribs" | PARTLY CORRECTED. K5 exists (open letter Aug 2025). It is 97 characters. "Both 97-letter messages will share some of the same coded words in the same position." Its coding is "similar but not identical" to K4, so not the same method. K5 ciphertext is held by Paradigm, which says it will "release K5 in the future" | SciAm 12 Nov 2025; AFP 19 Nov 2025; paradigm.xyz/writing/kryptos |
| 2025 archive discovery and auction | VERIFIED, with details in §2 | see §2 |
| Crib self-encryption note | CORRECTED. S->S at pos 33 and K->K at pos 74. Pos 64 is B->N, not a self-encryption | own check against ciphertext.txt; Wikipedia notes K->K |

Additional sourced facts added to known_facts.md:
- 2025 Sanborn clues: BERLINCLOCK refers to the **World Clock** in Berlin. The 1986 Egypt trip and the 1989 fall of the Berlin Wall "figure in the solution". The theme is "delivering a message".
- NSA had a team on Kryptos in 1992-93. It solved K1-K3 and reported "a successful break into part 4 has not been made".

Other Sanborn/Scheidt statements on method (secondary, cited in Bean 2021):
- Scheidt 2011 (Hannon's notes from the DC meeting): K4 crypto "is not mathematical ..., it is simple, can be remembered, and executed years later when used with the correct key word/s". Also: "similar to what would be provided agents or pilots in case of capture".
- Scheidt 2015 (Schmeh workshop): K4 is "more than one stage".
- Bogart 2019 (secondhand): "BERLINCLOCK in plain matches directly with NYPVTTMZFPK. It is a one-to-one match". Elonka's notes from the same lunch say Sanborn "backed off" from this. Treat it as weak.
- Sanborn 2020 (Smithsonian Magazine): the clue's release is "within days" of when he developed the 97-character string.
- Sanborn Wired 2005: "I have left instructions in the earlier text that refer to later text" (via rumkin K5 page).

## 2. The 2025-26 archive, auction and Paradigm events: what is public now
- **14 Aug 2025:** Sanborn's open letter announces the auction of the K4 plaintext. AI has been "a recent curse" because of a flood of meaningless decrypts.
- **Sep 2025:** Jarett Kobek noticed that the RR Auction catalog mentioned coding charts held at the Smithsonian (Archives of American Art). Richard Byrne photographed the papers. They found taped-together scraps showing the K4 plaintext, including BERLIN CLOCK and EAST NORTHEAST. They emailed Sanborn on **3 Sep 2025** and he confirmed it. Source: SciAm 16 Oct 2025.
- Sanborn's description: "five pieces of scrambled texts"; "The scrambled plain text was found, but without the coding method or the key." RR Auction calls it "Discovered, Not Solved". LKN Law summarizes RR as saying the scraps were not the encryption charts. Source: AFP 19 Nov 2025.
- Kobek and Byrne refused to sign NDAs but say they will not publish. RR Auction sent cease-and-desist letters. At Sanborn's request the Smithsonian sealed the files for 50 years (about 2075).
- **20 Nov 2025:** RR Auction sold the whole archive (charts, documents, the K4 solution and a private meeting with Sanborn) for **$962,500** to an anonymous buyer. Sources: AP via boston.com; Wikipedia.
- **12 Jun 2026:** **Paradigm** revealed itself as the buyer. It runs a guess-checker: SHA256 of the guess, then HMAC via Google Cloud KMS, $1 per guess. Paradigm says it does not know the plaintext itself. It holds the K5 ciphertext for a future release and has set 10 side puzzles at $1,000 each. Source: paradigm.xyz/writing/kryptos.
- **Bottom line (Oct 2026):** neither the K4 plaintext nor the method is public. K4 is not publicly solved. The 24 crib letters and Sanborn's 2025 thematic hints (World Clock, Egypt 1986, Berlin Wall 1989) are still the only public plaintext information. LKN Law (6 Sep 2026): no "publicly verified reconstruction of the complete original K4 encipherment".
- **Implication for our project:** the plaintext was "scrambled" in Sanborn's words. This hints that the archive scraps may have been an intermediate (transposed) form, but it may only mean they were out of order. UNVERIFIED and ambiguous. A correct full solution can now be checked through Paradigm's checker.

## 3. Published eliminations (appended to hypotheses/ruled_out.md)
- **Bean 2021 (HistoCrypt, peer-reviewed proceedings):**
  - Seriated digraphic at widths 7 and 21 is ruled out by the cribs (already logged by w-stats).
  - Standard Playfair is ruled out (no K->K, odd length).
  - Gromark base 10 with a 5-digit primer leaves only 39 primers that fit the cribs, and none gave convincing plaintext.
  - A standard A-Z plain alphabet with any digit-key Gronsfeld/Gromark scheme is impossible (C and R both -> P).
  - Bean argues against any transposition step: the minor-difference statistics give p of about 1/5520 and 1/240.
  - The Hill cipher is disfavored only (97 is prime).
- **Kryptos Group FAQ (Elonka):** ideas already tried, not formal proofs: combining the K1-K3 methods, an Enigma machine, Jefferson cylinder, Morse code, palindromes and others. Enigma is formally excluded by K->K.
- **NSA 1992-93 FOIA, Stein 1998, Gillogly 1999:** none broke K4. Gillogly saw only a weak signal at period 25, which the cribs now exclude.
- **Unreviewed GitHub repo (keithadler/kryptos, 2026)** claims crib-proof eliminations of:
  - running keys from K1-K3, Carter's book and the Bible
  - 5x5-square ciphers
  - Hill
  - K1/K2 applied twice

  These are logged as leads to re-verify, not as authoritative.
- I found no Cryptologia paper that eliminates a K4 method. Bauer/Link/Molle 2016 (Cryptologia 40(6):541-552) only conjectures a matrix (Hill) cipher. I could not read the full text.

## 4. Recent (2024-2026) partial or complete solution claims
- **Kobek/Byrne (2025):** plaintext found in the archive and confirmed by Sanborn. This is not a cryptanalytic solve, and the text is unpublished.
- **AI/ChatGPT "solutions" (2024-25):** Sanborn rejected all of them ("fairly silly"; the open letter speaks of a "flood of meaningless decrypts").
- **Manuel Salcedo Novoa (academia.edu, 2026)** and the "Genie Replication Package" (Berlin Clock route plus "substitution funnel", ASREN aggregator, 2025) both claim full solutions. They are not peer-reviewed, have no Sanborn or Paradigm confirmation, and I did not check them against the cribs. Status: UNVERIFIED, presumed false.
- No credible verified partial solution exists beyond Sanborn's 24 crib letters.

## 5. Open questions
1. Is "scrambled plain text" (Sanborn, Nov 2025) evidence of a transposition stage, or did it only mean out-of-order scraps? This matters because Bean argues against transposition.
2. Which K4 words appear at the same positions in K5? This is undisclosed.
3. Is the Bogart "one-to-one" quote reliable? It conflicts with Elonka's notes from the same lunch.
4. The primary NSA PDFs (media.defense.gov, nsa.gov) returned 403 to our fetches. The 2007 NSA "KRYPTOS Summary" (Redacted 2007, cited by Bean) may list further K4 work that was ruled out. Fetching it from another network is worth doing.
5. The Hill cipher has never been formally excluded in a peer-reviewed source. w-crib could test it algebraically with the cribs (2x2/3x3 over Z26, positions aligned to blocks).

## Sources consulted (24)
1. https://en.wikipedia.org/wiki/Kryptos
2. https://elonka.com/kryptos/
3. https://elonka.com/kryptos/faq.html
4. https://www.elonka.com/kryptos/OpenLetterAug2025.html
5. https://elonka.com/kryptos/KryptosTimeline.html
6. https://elonka.com/kryptos/foia.html
7. https://nsarchive2.gwu.edu/NSAEBB/NSAEBB431/docs/intell_ebb_010.PDF (Stein report)
8. https://www.elonka.com/kryptos/mirrors/daw/steinarticle.html
9. https://ecp.ep.liu.se/index.php/histocrypt/article/view/153 (Bean 2021)
10. https://scienceblogs.de/klausis-krypto-kolumne/2020/01/30/jim-sanborn-publishes-new-kryptos-clue/
11. https://scienceblogs.de/klausis-krypto-kolumne/2020/08/24/jim-sanborn-publishes-another-new-kryptos-clue/
12. https://scienceblogs.de/klausis-krypto-kolumne/2019/03/15/cnn-documentary-about-kryptos-a-making-of-report-with-many-photographs/
13. https://www.scientificamerican.com/article/a-solution-to-the-cias-kryptos-code-is-found-after-35-years/ (16 Oct 2025)
14. https://www.scientificamerican.com/article/how-the-cias-kryptos-sculpture-gave-up-its-final-secret (22 Oct 2025)
15. https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/ (12 Nov 2025)
16. https://citizen.digital/article/auction-of-famed-cia-cipher-shaken-after-archive-reveals-code-n373254 (AFP 19 Nov 2025)
17. https://www.boston.com/news/local-news/2025/11/22/info-to-decipher-secret-message-in-sculpture-at-cia-hq-sells-for-close-to-1m-according-to-rr-auction-of-boston/ (AP)
18. https://www.paradigm.xyz/writing/kryptos (12 Jun 2026)
19. https://lkn-law.com/2026/09/06/kryptos/
20. https://rumkin.com/reference/kryptos/k4/
21. https://rumkin.com/reference/kryptos/k3/
22. https://rumkin.com/reference/kryptos/k5/
23. https://dl.packetstormsecurity.net/crypt/nsa/kryptos/cia-art-jg.htm (Gillogly 1999)
24. https://ciphermysteries.com/tag/kryptos ; https://www.smithsonianmag.com/smart-news/third-and-final-clue-released-ci-sculptures-last-puzzling-passage-180974102/ ; https://github.com/keithadler/kryptos (unreviewed)

Not fetchable (403/blocked): content.rrauction.com "Discovered, Not Solved" page, NYT, Wired, NSA/media.defense.gov PDFs, archive.org.
