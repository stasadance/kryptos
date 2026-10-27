# w-physical — T5: Physical / ancillary clues around Kryptos and K4 (2026-10-26)

Scope: Berlin clocks, compass rose and lodestone, Morse panels, K2 coordinates, Antipodes, 1988-90 auction/archive material, tableau anomalies (extra L, YAR), petrified wood, pool.
For each item: sourced facts, how it could act as key, route or alphabet, ONE cheap falsifiable test, and the result where I ran it.
Scripts are in my scratch dir; they are short and can be copied into tools/ on request. Each is a single exact computation, not a keyspace search:
`/tmp/claude-0/-home-user/046a83fd-aa4b-57f6-97e0-639b3d9e1ef4/scratchpad/work/{keys.py,more.py,hill.py,prog.py}`.

## 0. Bottom line
- **Sanborn himself pins BERLINCLOCK to the Weltzeituhr** (Urania World Clock, Alexanderplatz). He did this in his Nov 2025 statements (SciAm, 2025-11-12) and placed it as "the gathering place for the crowds that brought down the Berlin wall" (news paraphrase, VERIFY exact letter text). Mengenlehreuhr ideas should be deprioritized.
- **The Weltzeituhr stands on a pavement mosaic shaped as a wind rose (compass rose)** (berlin.de; en.wikipedia Weltzeituhr: "a windrose is painted on the pavement"). This physically links the two confirmed crib phrases, EASTNORTHEAST and BERLINCLOCK, with Kryptos's own engraved compass rose at the entrance. My best reading is that the compass, the clock and the Morse "WHAT IS YOUR POSITION" are **plaintext themes (navigation/position)**, not key material.
- **Things that are refuted by exact, cheap computations:**
  - Hill cipher on raw K4 (motivated by the extra L, which makes "HILL" on the tableau), n=2,3,4, AZ or KA numbering, all block alignments.
  - Clock-tick progressive keys (k = a + b*floor(i/m)), all 8 tableau/mode combos.
  - Gronsfeld digit keys (K2 coordinates).
  - Any 5x5-grid output cipher (a base-5 / Mengenlehreuhr-style Polybius/Bifid/Foursquare). K4 uses all 26 letters.
  - Quagmire I/II-type periodic keys of length ≤26. Together with the existing period results, this kills every "physical keyword as periodic key" idea: Morse phrases, YAR, HILL, ENE, coordinates, city initials per facet.
- **Still alive, and the most promising physical lead:** a period-24 polyalphabetic with one arbitrary alphabet per Weltzeituhr facet. The cribs give **zero conflicts** at period 24 for arbitrary alphabets, and only 5 residues get two crib pairs each. IC does not exclude p=24 (w-stats). It is testable cheaply once a **1990-era (pre-1997) city-per-facet inventory** is obtained. The original clock had 80 names; 20 were added and some zones changed in 1997.

## 1. Berlin clocks
Facts:
- 2010: positions 64-69 decrypt to BERLIN. 2014: positions 70-74 decrypt to CLOCK. In 2014 Sanborn said: "There are several really interesting clocks in Berlin." / "You'd better delve into that particular clock." / of the Clock of Flowing Time, "There's a lot of fodder there." [NYT 2014 reprint, Cryptologic Foundation; Wikipedia Kryptos]
- Nov 2025: "BERLINCLOCK" refers to the World Clock in Berlin. Two events figure in the solution: Sanborn's late-1986 Egypt trip and the 1989 fall of the Berlin Wall. Sanborn: "Who says it is even a math solution?" [SciAm 2025-11-12]
- **Weltzeituhr**, Alexanderplatz:
  - Opened 30 Sep 1969; designer Erich John.
  - A 24-sided column (icositetragon), one face per time zone, with city names milled into etched aluminium and enamel.
  - A numbered hour ring 1-24 revolves around it once a day. A steel solar-system model on top rotates once per minute. Driven through a modified Trabant gearbox. About 10 m tall.
  - **Wind-rose mosaic on the pavement at its base.**
  - On 7 Oct 1989 the opposition demonstration started at the clock.
  - 1997 restoration: Leningrad became St Petersburg, Alma Ata became Almaty, 20 cities were added, Kyiv moved zone.
  - The **original (1969-1997) clock carried 80 city names across 24 zones**; today it carries about 146-148.
  - [en.wikipedia Weltzeituhr; berlin.de Weltzeituhr page; official history weltzeituhr-berlin.de cited in nitsuah/kryptos docs, which also cites Berliner Zeitung 1997-12-12]
- **Mengenlehreuhr** (Dieter Binninger, installed 17 Jun 1975 at Kurfürstendamm, moved after 1995 to Europa-Center):
  - 24 lamps in rows 1 + 4 + 4 + 11 + 4: a seconds blinker, then 5-hour, 1-hour, 5-minute and 1-minute rows. Base-5 display.
  - [en.wikipedia Mengenlehreuhr]

Possible uses, and one test each:
- (a) **One alphabet per facet (period 24)**. Each of the 24 faces (time zones) gives one cipher alphabet, for example a keyed alphabet from the facet's city names. Plaintext letter i uses facet i mod 24, possibly starting at Berlin's UTC+1 facet.
  - **Test:** with a 1990 facet inventory, build the 24 alphabets from the city names and check them only at residues 21, 22, 23, 0 and 1 (0-based i mod 24). Those are the residues where two crib pairs share a column: r21 E→F & C→M; r22 A→L & L→Z; r23 S→R & O→F; r0 T→V & C→P; r1 N→Q & K→K. Then run crib_check.py on the full decryption. One computation per alphabet-building rule.
  - **Status:** OPEN. Structured versions are refuted: facet = shifted AZ/KA alphabet (Vig/Beau/Quag I-III, period 24). The arbitrary-alphabet version has 0 crib conflicts (prog.py).
- (b) **Rotating hour ring as cipher-disk progression.** The key advances b steps every m letters.
  - **Test run:** k_i = a + b*floor((i+o)/m), m=1..24, a,b in Z26, o∈{0,1}, under Vig and Beaufort with the PA/CA tableaux STD/STD, KA/KA, STD/KA and KA/STD.
  - **Result: 0 hits. REFUTED.**
- (c) **Mengenlehreuhr base-5 used as a 5x5 grid** (Polybius, Bifid, Foursquare, Playfair).
  - **Test run:** count the distinct ciphertext letters. K4 uses **all 26** (M and Y once each), and 5x5-grid output can produce at most 25.
  - **Result: REFUTED.** The only escape is a later re-substitution layer. Playfair was already out because of self-encryption.
- (d) **Mengenlehreuhr lamp pattern (24 on/off states) as an additive mask of period 24.** This is a special case of a period-24 Vig key. **REFUTED** (w-history and w-physical period tests).
- (e) **Weltzeituhr "24" as a route (24 columns) or as transposition alone.** **REFUTED** for pure transposition: the cribs need 3 E and the ciphertext has 2 (ruled_out.md). A 24-column route combined with substitution stays OPEN under H-404.

## 2. Compass rose, lodestone, EASTNORTHEAST
Facts:
- One entrance granite slab carries an engraved compass rose. Its needle points to a nearby lodestone, not to north. [Wikipedia; CIA legacy Kryptos page: "a lodestone ... co-located with a navigational compass rose"; Elonka FAQ / KryptosAerial]
- Sanborn in the NOVA interview: the dial "is not oriented north and south. It's offset ... there's a mystery there". [thekryptosproject strata page quoting NOVA]
- Sanborn's letter to the Agency: "At the entrance a lodestone ... refers to ancient navigational compasses." [thekryptosproject stones page, quoting realmoftwelve; VERIFY primary]
- The needle runs roughly parallel to the front sidewalk (photo-overlay estimate) [thekryptosproject compass observation]. Fan sources say it indicates ENE [rumkin K4]. **No surveyed bearing has been published. UNVERIFIED.**
- EAST (positions 22-25) was revealed in Aug 2020 and NORTHEAST (26-34) on 29 Jan 2020 [Wikipedia; scienceblogs.de Klausis 2020].

Possible uses:
- A shift equal to the compass point index (ENE = point 3 of 16, or 67.5° → shift 67.5/360*26 ≈ 5). Or a grid rotated by the deflection angle.
- **Test:** a single shift is period 1, so it is **REFUTED**. A rotation, i.e. a route over a grid, needs a second layer, so it falls under H-404.
- **Interpretation (H-507):** EASTNORTHEAST is a bearing written in the plaintext. It points from the compass/lodestone, or from the coordinate spot, toward something, and the Weltzeituhr's own wind rose echoes it. Treat the compass as a plaintext theme rather than as key material.

## 3. Morse code (K0)
Facts (Gillogly photos as transcribed on rumkin K0):
- Readings: SOS · RQ (reversed YR) · LUCID [E E E] / MEMORY E · T IS YOUR / POSITION E (probably WHAT IS YOUR POSITION) · E E SHADOW E E / FORCES E E E E E · E DIGE TAL E E E / INTERPRETATI (possibly a dropped dit, i.e. DIGITAL; cut off at the rock) · E E VIRTUALLY E / E E E E E INVISIBLE.
- The E's are fillers or word separators.
- Sanborn: Morse is "the simplest of all codes" (entrance) [Elonka KryptosAerial]. CIA: the copper "pages" carry "International Morse code and ancient ciphers" [CIA legacy page].

Possible uses:
- Phrases as keywords. **REFUTED:** every phrase is ≤26 letters, and periodic keys of 1-26 are dead for Vig, Beau and Quag I/II/III with AZ/KA.
- Filler-E counts as numbers, e.g. a transposition key. Weak.
- Error positions as pointers (H-210).
- "WHAT IS YOUR POSITION" / "T IS YOUR POSITION" thematically matches EASTNORTHEAST and the compass rose, so it may echo the K4 plaintext (H-507).
- **Test proposal:** once any method family gives a partial decryption, check the filler-E counts per panel (2,6 | 2,5 | 3,1 | 1,3) as a column order. This is only one permutation, so it is cheap. Not run, because no candidate layer exists yet.

## 4. K2 coordinates
Facts:
- K2: 38°57'6.5"N 77°8'44"W, then "LAYER TWO" (corrected 2006; it was formerly read as IDBYROWS) [Elonka CorrectedK2Announcement].
- The point is about 53 m (174 ft) SE of the sculpture on a modern datum [Wikipedia].
- Sanborn said the coordinates point either into the courtyard (the building-shadow area south of the plaza) or possibly to an area **south of the compass at the entrance** [Elonka KryptosAerial]. Nothing is published about anything found there.

Possible uses:
- Digits 3857657 7844 as a Gronsfeld key. **Test run:** the crib keystream needs values >9 under every variant. **REFUTED.**
- "LAYER TWO" supports the two-layer prior (H-201/H-212).

## 5. Antipodes (Hirshhorn, 1997)
Facts:
- The Kryptos text is repeated on the English side, with "select differences ... spacing, additional dots and letters" [Wikipedia Antipodes].
- The other side is Cyrillic Projector text plus an extra ciphertext section; it is separated by petrified wood [Elonka antipodes page].
- **No published letter-level transcript** of the Antipodes K4 portion exists in open sources (Elonka: "not yet available").

Possible use: a difference inside K4 would flag an erratum, a null or an alternate.
- **Test proposal:** transcribe the K4 run from Hirshhorn photographs (Elonka's antipodes picture directory) and diff it against facts/ciphertext.txt. Each difference becomes a candidate correction that is re-tested with any surviving method. This is cheap (photo reading). Not run, because no transcript is available.

## 6. Tableau anomalies and misaligned letters
Facts:
- The right-hand tableau has one row with an extra L. This makes HILL read down the right edge. Bauer, Link & Molle (Cryptologia 2016, doi 10.1080/01611194.2016.1141556) suggest this is a Hill (matrix) hint. Sanborn omitted the extra L on the small models he sold [Wikipedia].
- The CIA text shows row N as 31 letters ending in "...HIJL".
- "YAR" is the only superscript, near the start of the bottom-left half (the start of K3, "ENDYAHR"). Elonka's rubbings show Y, A and R a couple of cm out of alignment [Elonka Kryptos page journal; Wikipedia].
- One letter was omitted on the left side "for aesthetic reasons" (2006), and the S missing from K2 was confirmed [Wikipedia].

Tests:
- **Hill cipher on K4 (exact linear solve, hill.py/more.py):** for an n×n matrix M over Z26, solve each row against all crib blocks. Run for n=2,3,4, every alignment offset, A=0 numbering and KRYPTOS-alphabet numbering, in both the C=MP and P=MC directions where checked.
  - **Every case has at least one row with 0 solutions.**
  - **Result: REFUTED** for direct Hill. Still open: Hill after or before a transposition, and n≥5.
- YAR / HILL / RAY as periodic keys: **REFUTED** (period ≤26).
- YAR as a positional pointer is part of H-210. Proposed test: list the sculpture row/column of Y, A and R and check whether they fall on K4's column grid. Low prior. Not run.

## 7. Auction / archive material (1988-1990)
- RR Auction lot 2001 sold on 20 Nov 2025 for $962,500. Contents: handwritten K4 plaintext; "the original coding system for K4"; K1-K3 coding charts; "original unpublished 1988 alternate K4 plaintext and coding chart now known as K5"; the scrambled texts shown to the CIA in 1990; a 1988 "proof of concept" copper plate signed J.S.1988; and a photo of the 1988 model [rrauction.com lot page; content.rrauction.com].
- **The wording "coding chart" for K4/K5 matches the K1-K3 coding charts.** This suggests K4's key material is a hand-made chart or tableau, not an external object.
- In Sep 2025 Kobek and Byrne recovered the plaintext from cut-up 1990 strips in the Smithsonian Archives of American Art. The strips were cut and taped out of order. The files are sealed until 2075. **The method is not recovered**: "There's no way on earth that this is a cryptographic solve" [Zona Motel interview; RR "Discovered, not solved"; Wikipedia].
- Paradigm (crypto VC) was the buyer [Wikipedia, NYT 2026-06-12].
- **Caution:** solvekryptos.com publishes a *reconstructed* 97-letter plaintext:
  `THECOMPASSROSEISHEREXEASTNORTHEASTTHISISYOURPOSITIONXCOMMISSIONBERLINCLOCKWHICHISNORTHEASTOFHEREX`
  - It passes crib_check.py, but only by construction.
  - The site says it is NOT the archived text and is not independently verified. **UNVERIFIED. Do not treat it as a fact.**
  - Note that it draws on the same physical themes (compass rose, "your position").

## 8. Petrified wood, pool, stones
- Sanborn/CIA: the petrified tree recalls the site's trees and "the source of the paper"; the bubbling pool symbolizes "information being disseminated with the destination being unknown" [CIA legacy page; Elonka KryptosAerial].
- The pool's whirlpool runs **clockwise** [thekryptosproject whirlpool, CNN 1991 clip].
- Sanborn said the green blob on the red granite "has no significance" [thekryptosproject stones, 2013 DC dinner notes].
- **No key content.** The only conceivable use is a clockwise spiral route. That is a transposition, so it needs a substitution layer as well (H-404). No cheap test is proposed.

## 9. Computations run (all exact, seconds)
| Test | Result |
|---|---|
| Distinct ciphertext letters | 26 (all present). Any 5x5-grid output cipher is refuted |
| Crib E supply | Cribs need 3, ciphertext has 2. Pure transposition refuted (confirms ruled_out.md) |
| Periodic key p=1..26, PA/CA ∈ {STD,KA}², Vig/Beau | 0 consistent periods in all 8 combos (adds Quagmire I/II-type mixes) |
| Gronsfeld (key 0-9) | impossible in all 8 combos |
| Progressive clock-tick key a+b⌊(i+o)/m⌋, m≤24 | 0 hits |
| Hill n=2,3,4 (STD & KA numbering, all offsets) | no matrix; refuted |
| Period-24 arbitrary alphabets (crib bijection) | 0 conflicts; OPEN (H-501) |
| Third-party reconstruction through crib_check.py | passes by construction; not evidence |

Crib keystreams for reference (positions 22-34 | 64-74):
- STD Vig: BLZCDCYYGCKAZ | MUYKLGKORNA
- KA Vig (K1/K2 style): RDUMRIYWOYNKY | ELYOIECBAQK
- KA Beau: WXAKGZTOAXAFD | RGTGNWRJLFK

## 10. Sources
1. https://en.wikipedia.org/wiki/Kryptos
2. https://en.wikipedia.org/wiki/Weltzeituhr
3. https://en.wikipedia.org/wiki/Mengenlehreuhr
4. https://en.wikipedia.org/wiki/Antipodes_(sculpture)
5. https://www.berlin.de/sehenswuerdigkeiten/3561749-3558930-weltzeituhr.html
6. https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/ (2025-11-12)
7. https://www.elonka.com/kryptos/OpenLetterAug2025.html
8. https://www.elonka.com/kryptos/ (journal: YAR misalignment, pool, petrified wood)
9. https://www.elonka.com/kryptos/KryptosAerial.html
10. https://www.elonka.com/kryptos/faq.html
11. https://elonka.com/kryptos/CorrectedK2Announcement.html
12. https://www.elonka.com/kryptos/sanborn/temp/antipodes.html
13. https://www.cia.gov/legacy/headquarters/kryptos-sculpture/
14. https://rumkin.com/reference/kryptos/k0/
15. https://rumkin.com/reference/kryptos/k4/
16. https://thekryptosproject.com/kryptos/pok/strata.php (NOVA quotes)
17. https://thekryptosproject.com/kryptos/pok/stones.php
18. https://thekryptosproject.com/kryptos/pok/whirlpool.php
19. https://thekryptosproject.com/kryptos/pok/petrified_wood.php
20. https://thekryptosproject.com/tjp/observations/compass.php
21. https://archive.cryptologicfoundation.org/community/bytes/cryptologic-bytes---codes-ciphers-computers.html/article/2014/11/21/-a-new-clue-to-kryptos-new-york-times-articles
22. https://scienceblogs.de/klausis-krypto-kolumne/2020/08/24/jim-sanborn-publishes-another-new-kryptos-clue/
23. https://www.rrauction.com/jim-sanborn-kryptos-k4-solution-auction/
24. https://content.rrauction.com/jim-sanborns-complete-kryptos-archive-sells-for-962500-at-auction/
25. https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/
26. https://zonamotel.substack.com/p/interview-kryptos-k4-uncovered-jarett
27. https://pubpeer.com/publications/F53249D16FB9850F3B80C55269E63A (Bauer/Link/Molle 2016)
28. https://raw.githubusercontent.com/nitsuah/kryptos/main/docs/analysis/K4_HISTORICAL_WORLD_CLOCK_PHOTOS.md (80 original names; 1997 changes; photo leads)
29. https://github.com/nitsuah/kryptos/pull/264
30. https://kryptos.today/press/2026-05-01-launch (third-party Weltzeituhr sweep, 0 verified)
31. https://solvekryptos.com/solution (UNVERIFIED reconstruction)

## 11. Recommended next actions
1. Get a pre-1997 Weltzeituhr facet inventory. Leads: Bridgeman 1990 photo by Lothar M. Peter; AKG c.1986/1990 photo by Pansegrau; 1976 postcard Mi-A I615 at Verein für die Geschichte Berlins. Then run H-501's single test.
2. Get an Antipodes K4 transcription and diff it against K4 (H-508).
3. Treat compass/position/clock as plaintext themes (H-507). Do not spend further effort on physical items as periodic keys; that whole class is dead.
