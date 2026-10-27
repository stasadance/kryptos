# w-clock — T8: Weltzeituhr (Berlin World Clock) as K4 key material (2026-10-26)

## 0. Bottom line
- **I could not obtain the pre-1997 per-face city inventory.**
  - No source among the 20+ I checked (listed in §6) publishes a per-face list: de/en Wikipedia, berlin.de, the 1997 Berliner Zeitung and taz reports, tourism pages, geocache listings, and the nitsuah/kryptos doc.
  - Reading the names myself from high-resolution photos was blocked. Wikimedia (upload + API) returned HTTP 429 to this container, and Flickr returned "CIDR range blocked".
  - Bundesarchiv pre-1990 photos on Commons are only 800 px, which is too small to read the plates. I did not try to get around these blocks.
- **The "80 original names" figure (w-physical, nitsuah) is unsourced and probably wrong.**
  - Primary press gives 146 places plus a date-line entry today (Märkische Allgemeine 24/25 Dec 1997, via de.wikipedia), or 148 (berlin.de).
  - 20 names were *added* in 1997 (Berliner Zeitung 12 Dec 1997).
  - So 1969-97 had about 126-128 names (H-805).
- **What I could refute without the list (all exact, single computations):**
  1. **Single city name per face as the keyword** of a keyed alphabet (four substitution directions, AZ or KA fill), for any face list and any alignment. **REFUTED** (H-801).
  2. **Face/zone offset plus rotating hour ring** as a non-periodic shift, k_i = a + b·i + c·((i+o) mod 24): 0 of 5.06M configs fit the cribs. **REFUTED** (H-803).
  3. **Any numeric key that depends only on i mod 24** (UTC offsets, face index, hour numbers, Berlin-relative offsets) under the AZ/KA tableaux. **REFUTED** (H-804). Together with w-crib's result (Quagmire III with any single mixed alphabet fails at p=24), **only genuinely independent per-face alphabets survive at period 24**.
- **Still open (H-802): one keyed alphabet per face, built from all names on that face.** This is now a single ready-to-run test once someone supplies 24 lines of face text: `python3 tools/w-clock/face_test.py faces.txt`.
- **Sanborn's statements (§4).**
  - The only primary 2025 wording found is "The 'BERLINCLOCK' mentioned in previous K4 clues refers to the World Clock in Berlin" (SciAm 2025-11-12).
  - **That sentence does not name Alexanderplatz.**
  - No source found says Sanborn visited Berlin.
  - In 2014, Sanborn spoke about **Dieter** (Binninger, the Mengenlehreuhr designer) and the "very interesting back story" (Wired via Slate).

## 1. Period-24 crib structure (exact, tools/w-clock/residues.py)
Residue r = (pos-1) mod 24 (pos 1-indexed):

| r | crib pairs P->C (pos) |
|---|---|
| 0 | T->V (25), C->P (73) |
| 1 | N->Q (26), K->K (74) |
| 2-9 | O->Q(27), R->P(28), T->R(29), H->N(30), E->G(31), A->K(32), S->S(33), T->S(34) |
| 10-14 | unconstrained |
| 15-20 | B->N(64), E->Y(65), R->P(66), L->V(67), I->T(68), N->T(69) |
| 21 | E->F (22), C->M (70) |
| 22 | A->L (23), L->Z (71) |
| 23 | S->R (24), O->F (72) |

- 19 residues are constrained, 5 of them by two pairs.
- Positions 48 apart (22/70, 23/71, 24/72, 25/73, 26/74) share a face.
- The cribs place **no injectivity conflict** at p=24 for arbitrary alphabets (this confirms w-physical).
- What the doubly-constrained residues require (example S1: C = K[AZ(P)], keyed alphabet = keyword + rest of A-Z): in r1, K->K and N->Q force **K to be the 11th and Q the 14th distinct keyword letter**. If Q is not in the keyword it can only move rightward (index ≥ 16), and Q must be at index 13. So K->K then forces K into slot 10. The residue-1 face therefore needs a keyword with at least 14 distinct letters. A single city name essentially never has that; a whole face's list could.

## 2. Tests run

| ID | Model | Computation | Result |
|---|---|---|---|
| H-801 | per face: keyed alphabet from ONE city name; S1 C=K[AZ(P)], S2 C=AZ[K(P)], S3 C=K[KA(P)], S4 C=KA[K(P)]; fill AZ or KA | for each residue, which of 192 world-city keywords (German + English spellings: MOSKAU/MOSCOW, PEKING, KAIRO, HAVANNA, ULANBATOR, ALMAATA, LENINGRAD, KAPSTADT, TELAVIV, ...) satisfy its crib pairs (kwres.py) | max 13/19 residues satisfiable by *any* name, in any combo. r0, r22 unsatisfiable in all 8; r1 only by KHARTUM/KUWAIT (S3-AZ) or K-initial names (S4-KA); r21 only S2-KA; r23 only S4-KA. **REFUTED**, list-independent |
| H-803 | k_i = a + b·i + c·((i+o) mod 24) mod 26 (zone offset + ring rotation, non-periodic, period 312) | all a,b,c ∈ Z26, o ∈ 0..23, Vig/Beau/var-Beau, PA/CA ∈ {AZ,KA}² = 5,061,888 (ringkey.py) | **0 fits** |
| H-804 | any key that is a function of i mod 24 (UTC offsets, face index, 1-24 hour ring) | period_check at p=24, 12 tableau/rule combos | conflict @22/70 in all 12. **REFUTED** |
| H-802 harness | 24 face keywords (all names on the face) | face_test.py: 24 alignments × 2 directions × 4 models × 2 fills = 384 configs, score = #crib pairs satisfied | dummy random-city faces: best 4/24 (null). A true hit = 24/24. **Awaiting inventory** |

## 3. What is known about the clock (sourced)
- Opened 30 Sep 1969. Designer Erich John (Hochschule Weißensee), part of the Womacka planning group. Built with Getriebefabrik Coswig and Hans-Joachim Kunsch. [de.wikipedia Weltzeituhr (Alexanderplatz)]
- Physical form:
  - 24-sided cylinder, one side per main time zone, names of important cities milled into aluminium. [de.wikipedia; berlin.de]
  - The hour ring rotates once per day. The solar-system model rotates once per minute. [de.wikipedia; en.wikipedia]
  - A wind-rose mosaic is set into the pavement. [berlin.de; de.wikipedia]
- Name count: today 146 places plus a date-line entry [de.wikipedia citing MAZ 24/25 Dec 1997], or 148 [berlin.de, opencaching, tourism sites]. Tagesspiegel 2019 says 147.
- 1997 restoration (Oct-Dec, 350,000 DM, Kunsch):
  - **20 names added.** Oslo was "simply forgotten"; Jerusalem and Kapstadt were omitted "aus politischen Gründen". [Berliner Zeitung 12 Dec 1997]
  - Oslo, Kapstadt and Tel Aviv added; St. Petersburg updated. [taz 20 Dec 1997]
  - Seoul added. [en.wikipedia]
  - Leningrad became St. Petersburg, Alma Ata became Almaty, Bratislava became "Pressburg" (Slovak protest). Kiew moved from Moscow time. [de.wikipedia]
  - Some cities had originally been put in the wrong zones. [berlin.de]
- **Pre-1997 list implication:** the 1969-97 clock is today's list minus about 20 additions (Oslo, Jerusalem, Tel Aviv, Kapstadt, Seoul, + about 15 unknown), with the old names Leningrad, Alma Ata, Bratislava, and Kiew in the UTC+3 zone. About 126 names, NOT 80.
- Face order and Berlin:
  - The faces run in UTC order around the cylinder.
  - Berlin's own zone is UTC+1 (CET).
  - **No source found states whether "Berlin" itself is engraved, or which plate sits where relative to the pavement wind rose.** UNVERIFIED.
- Partial pre-1997 reading (UNVERIFIED, from a watermarked 1990 Bridgeman preview; nitsuah doc): GUATEMALA, MANAGUA, PANAMA, BOGOTA, GALAPAGOS-INSELN, QUITO, LIMA, CARACAS, LA-PAZ, ASUNCION, SANTIAGO, RIO DE JANEIRO, SAO PAULO, MONTEVIDEO, BUENOS AIRES.

## 4. Sanborn and the World Clock
- **SciAm 2025-11-12, the only primary 2025 wording found:** "The 'BERLINCLOCK' mentioned in previous K4 clues refers to the World Clock in Berlin." Two events figure in the solution: the 1986 Egypt trip and the 1989 fall of the Wall.
  - The identification with Alexanderplatz is very likely, since "Weltzeituhr" means "World Clock". But the text **does not name Alexanderplatz.**
- **2014 (Wired, via Slate):** "Most people have no idea who Dieter is and all of the other people who make strange clocks in Berlin ... There's a very interesting back story to [the Berlin Clock]."
  - So in 2014 Sanborn talked up the Mengenlehreuhr. The 2025 statement overrides this, or the 2014 remark was misdirection.
- **The Wall's collapse:** it was "big news" while he was "casting about" for sculpture content (Wired 2014 via Slate).
- **No source says Sanborn visited Berlin.**
- **Plausible thematic link:** the Weltzeituhr was where the 7 Oct 1989 opposition march formed, 33 days before the Wall fell [de.wikipedia]. This fits "1989 fall of the Wall" as **plaintext content** (H-507), not as key material.

## 5. Recommendation
- **Treat the World Clock as plaintext theme (H-507), not key.**
  - Every structured clock-to-key mapping that can be tested without the list is dead.
  - The only survivor (H-802, all names per face as keyword) needs about 126 names transcribed from a dated pre-1997 photo set.
- **If the coordinator wants H-802 closed,** a human or browser session can transcribe the faces into `faces.txt` (24 lines, UTC-11..UTC+12) from Commons "Historical photographs of Urania-Weltzeituhr" originals or the Bundesarchiv originals. Then run `face_test.py`; it takes seconds.
- Low prior. Arbitrary alphabets per face would also make K4 a 24-alphabet cipher whose alphabets Sanborn would have had to write out. That is consistent with an RR-auction "coding chart" but not otherwise supported.

## 6. Sources
1. https://de.wikipedia.org/wiki/Weltzeituhr_(Alexanderplatz) (raw wikitext read)
2. https://en.wikipedia.org/wiki/World_Clock_(Alexanderplatz)
3. https://www.berlin.de/sehenswuerdigkeiten/3561749-3558930-weltzeituhr.html
4. https://www.berliner-zeitung.de/20-staedtenamen-wurden-bei-der-restaurierung-ergaenzt-frisch-poliert-die-weltzeituhr-dreht-sich-bald-li.7079 (12 Dec 1997)
5. https://taz.de/!1367509/ (20 Dec 1997)
6. https://www.tagesspiegel.de/berlin/50-jahre-alex-die-weltzeituhr-kennt-jeder-niemand-ihren-erfinder/24211692.html (2019, paywalled teaser: 147 names)
7. https://www.berliner-zeitung.de/article/2154618 (2023)
8. https://blog.inberlin.de/2012/09/die-urania-weltzeituhr-am-alexanderplatz/
9. https://the-passenger.de/2010/03/19/weltzeituhr/
10. https://www.walkofberlin.com/post/the-weltzeituhr-why-alexanderplatz-has-a-world-clock (notes that the counts vary)
11. https://www.berlinstadtservice.de/xinh/Weltzeituhr_Berlin.html
12. https://www.opencaching.de/viewcache.php?cacheid=184573
13. https://geocaching.com/geocache/GC7B92Q (via search)
14. https://commons.wikimedia.org/wiki/Category:Urania-Weltzeituhr (+ Historical photographs / Details subcats, listed via API)
15. Bundesarchiv Bild 183-U0414-0014 (14 Apr 1979, Klaus Franke), viewed at 800 px: too small for names
16. https://raw.githubusercontent.com/nitsuah/kryptos/main/docs/analysis/K4_HISTORICAL_WORLD_CLOCK_PHOTOS.md and https://github.com/nitsuah/kryptos/pull/264
17. https://kryptos.today/press/2026-05-01-launch (third-party Weltzeituhr sweep: 0 verified, method and list undisclosed)
18. https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/ (2025-11-12)
19. https://en.wikipedia.org/wiki/Kryptos
20. https://www.slate.com/articles/technology/technology/2014/11/new_kryptos_clue_hint_for_solving_the_cia_s_mysterious_sculpture_puzzle.html (Wired 2014 reprint: "Dieter")
21. https://archive.cryptologicfoundation.org/community/bytes/cryptologic-bytes---codes-ciphers-computers.html/article/2014/11/21/-a-new-clue-to-kryptos-new-york-times-articles (via search)
22. https://news.artnet.com/art-world/artist-reveals-another-clue-to-24-year-old-mystery-at-cia-178462 (via search)
23. https://www.bz-berlin.de/kultur/so-tickt-die-weltzeituhr-auf-dem-alexanderplatz (cited in de.wikipedia)
- Not reachable: weltzeituhr-berlin.de (503), reddit r/KryptosK4, morgenpost.de, elonka.com (empty to the fetcher).

Scripts: tools/w-clock/{residues.py, kwres.py, ringkey.py, face_test.py, cities1.txt}
