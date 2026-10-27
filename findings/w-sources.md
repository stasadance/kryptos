# w-sources: primary-source dossier of K4 method hints (T15)
Worker: w-sources | Date: 2026-10-26 | Hypotheses: H-1501..H-1506 | Scripts: workers/w-sources/scripts/

## Grading key
| Grade | Meaning |
|---|---|
| **P** | Verbatim speech, fetched and read by me from a public primary or near-primary text: transcript, the speaker's own letter, or a direct quote in a news article |
| **P\*** | Verbatim, but read only through a compilation or mirror (kryptools hints page; groups.io file mirror; blog reproduction). The wording is likely right; the chain of custody is weaker |
| **S** | A witness's notes of what was said (dinner or lunch notes, blog comment). Paraphrase-level, even when written in quotation marks |
| **J** | A journalist's paraphrase |
| **X** | Could not be verified; dropped from the constraint set |

**Provenance warning about the groups.io material.** Much S-level material (2004-2025 dinner notes) is visible only through the French research-handoff mirror https://github.com/aciderix/kryptos-research-handoff (docs/knowledge_base/07_groupsio_2026_09_24.md). That repo copies members-only kryptos.groups.io files, its README says "ne pas republier" (do not republish), and it is marked private although its raw files still load. I quote only short items from it, always mark them S, and **do not copy members-only files into this workspace**. The groups.io message Bean cites (main/message/12611) needs a login: the page is JS-gated and returned no text.

---
## 1. Scheidt: the method hints, verified

| # | Date / venue | Text | Grade | Source |
|---|---|---|---|---|
| S1 | Wired, 21 Jan 2005 (Zetter) | "There are four different processes. Two of them are similar and the other two are different things. The first three processes were designed so that a person could, through cryptographic analysis, have access to the English language … And the last process, I masked the English language so it's more of a challenge now." / "(But with) this other technique (in the fourth part), I disguise that. So … you need to solve the technique first and then go for the puzzle." / "The masking technique may not be known." / "there was some masking techniques that were used … since he's the one who had the chisel in his hands, there could be some changes." | P\* | kryptools hints page (mirror) https://www.kryptools.com.about.ag/hints.htm ; kryptosfan reproduction https://kryptosfan.wordpress.com/k4/artichoke/masking-vs-english/ |
| S2 | NPR ATC, 9 Jun 2005 | Scheidt, verbatim: "if you could determine that--the number of E's vs. the number of Z's … then you would have some insight". Reporter: "Scheidt says in part four he deliberately masked that advantage … he helped with the basic structure of the code, he's never tried to crack Sanborn's final message." | P (E/Z sentence) / J ("deliberately masked") | https://www.npr.org/transcripts/4684720 (fetched) |
| S3 | Wired, Apr 2009 | "There may be more to the puzzle than what you see … Just because you broke it doesn't mean you have the answer." "The intelligence picture includes mirrors and obfuscation." Journalist: they tried "poly-alphabetic substitution, shifting matrices, and transposition" and settled on "old-school, artisanal cryptography" | P / J | https://www.metzdowd.com/pipermail/cryptography/2009-April/015266.html |
| S4 | Zola dinner, DC, **8 Oct 2011** (Ed Hannon's notes) | "[K4 cryptography] is not mathematical (although this does not preclude it being modeled mathematically), it is simple, can be remembered, and executed years later when used with the correct key word/s." / "K4 cryptography is similar to what would be provided agents or pilots in case of capture" | **S** (the brackets and the parenthetical are Hannon's or Bean's) | Bean 2021 §3, https://ecp.ep.liu.se/index.php/histocrypt/article/download/153/109 (PDF fetched, text checked), citing Hannon 2011 "Oct 8th DC Meet with Sanborn and Scheidt", kryptos.groups.io/g/main/message/12611 (login-only). **The original post could not be read.** |
| S4b | same dinner (E. Dunin's notes) | Scheidt "interested" in K4 patterns in rows of 21; a "regenerative function"; K4 is solvable by a human, "any agent would solve it with a little training"; "a very long process is probably not the right one"; it must not be solvable "by a weighting of English" | S (re-translated from a French summary) | aciderix mirror 07_groupsio §1 item 8, §2.13 |
| S5 | ACA convention dinner, Oct 2013 | The receiver's identity is "built into the process", no clue given (reporter's memory). Scheidt hesitated on "1:1"; to "could Jim have made an encoding error?" a weak "yes" | S | https://kryptosfan.wordpress.com/2013/10/30/more-about-ed-scheidts-aca-talk/ ; mirror §7.1 (B. Briere, 3 Nov 2013) |
| S6 | Schmeh/Dunin workshop, **24 Oct 2015** (Bean transcript) | "I would consider it more than one stage … there's a masking technique that applied so that the English language wouldn't be available" [47:19] | P | https://scienceblogs.de/klausis-krypto-kolumne/kryptos-workshop-transcript/ (fetched) |
| S6b | same | "the impact of some kind of math function on the English language … so there's a mask of some type now"; "you're carrying the weight of the language … the other intent was … to make the challenge so that the first step is that thing" (the Rev.com version reads "is not that"; it refers to the analyst's first step, frequency counting, not to cipher order) | P | same; correction per mirror §11.6 |
| S6c | same | "it lends itself to building layers or you could mix and match which is a certain amount of that took place"; "the thing that I had thought of and I was asked not to do … I could have moved to a different math base … base 2 we could move to base 16 … different folks thought that's not fair Scheidt" | P | same |
| S6d | same | Never decrypted K4: "Jim seems to claim he did something else on top of this — A: he may have"; worked backwards "except for K4 I didn't. I did all the others"; "if Jim made an encoding error you would not have known that he did so? — Ed: no"; plaintext "reads like it's disjointed but there's a story"; "there's more than one sentence in there" | P | same |
| S7 | AJ Jacobs, Rev.com transcript, 17 Nov 2020 | "you take the alphabet and you just move it down one character or two characters and then you starts combining the functions" / "you've got to make something that's retainable, that you can write it on a piece of paper" / "transposition … defining the parameters of the puzzle in the sense of the square … my secret is push into this square. So that was another step. And then the last step … I masked the framework, in other words if you can change the language base then it becomes in my favor … when it was used as the mask it was current, 2020 secret." | P\* | raw mirror of the groups.io file: https://raw.githubusercontent.com/aciderix/kryptos-research-handoff/HEAD/sources/groupsio_membres/textes/Personal%20Folders/AJ%20Jacobs/EdScheidtKryptosTranscript.pdf.txt ; the "language base…2020 secret" sentence is also quoted verbatim in Bean 2021 (P) |
| S7b | same | "Not to another language, it's to something else." Window pattern? "It could be, but it's not." OTP: "It's not directly related … The analogy is reasonable, but reasonable in a sense of the result. How you did it to get that result is the question." "if you figure out the mechanics of how you did it, then it gives a insight into the answer." "Linear is a direct substitution, non-linear is a quadratic way of looking at it." "you've got K1, two, three, which is steps of the puzzle, and then K4 being the final" | P\* | same |
| S8 | Northern Virginia Mag, 14 Oct 2022 | "We used voice as the medium" (to pass the scheme); wanted to "make it a real challenge"; asked for an extinct language: "They said no" | P | https://northernvirginiamag.com/culture/culture-features/2022/10/14/cia-kryptos-sculpture-cipher/ |
| S9 | NYT, 20 Nov 2014 | "But a technique that I used obviously worked." | P | NYT reprint, https://archive.cryptologicfoundation.org/…/2014/11/21/-a-new-clue-to-kryptos-new-york-times-articles |
| S10 | dinners 2004 / 2007 | 2004: "I used a bit of steganography" in part four. 2007: "the masking technique is designed to remove the bias"; the code is "reflective", not "symmetric"; binary masks "with as many 1s as 0s"; whether the K4 concept could be reused: "The concept could." | S | mirror §2.13, §7.1, §10.5 |

## 2. Sanborn: method-relevant statements, 1989-2026

| # | Date / venue | Text | Grade | Source |
|---|---|---|---|---|
| J1 | Letter to CIA employees, 15 Dec 1989 | "The right side is a text that can be partly deciphered by using the table and partly by using a potentially challenging encoding system." | P\* | kryptools hints page |
| J2 | ABC B-roll, 1991 | "the keyword for some of that text is Kryptos"; "It's in English, it's in plain English … but that isn't necessarily the whole story"; "Part of it … within years, or never" | P\* | kryptools |
| J3 | NPR, 26 Aug 1999 | "I like to use spacial systems of encoding and decoding"; light-and-shadow pattern systems not used "at least [in] what's been deciphered already, perhaps what has not been deciphered" | S/P\* (member transcription and Dr. Dobb's, Dec 1999) | mirror §10.1 #1 |
| J4 | Dunin, studio visit, 3 Nov 2003 | Surprised "no one has recovered the original matrix" and run it "through all possible 'shifts'"; "matrix system"; on the errors: "it's more the orientation of those letters … positioning"; nobody beta-tested the code, "not even Scheidt" | S | mirror §10.1 #3; quote as on https://rumkin.com/reference/kryptos/k1/ : "Those errors are deliberate. It's not what they are that's so important though, as their orientation or positioning." (S, undated there) |
| J5 | **Wired, 20 Jan 2005** | "How many (cryptographic) techniques…? — I would think five or six." / "It's also well-known that I did use some matrix codes Ed gave me, and I have also designed visual systems for encoding, which are much harder for cryptographers to crack because they're individualistic." / "I'd be modifying systems and developing my own" / "most of my things are rife with mistakes on purpose" / "I have left instructions in the earlier text that refer to later text." | P\* (Zetter transcript, no longer online; reproduced verbatim) | kryptools hints page |
| J6 | NPR, 9 Jun 2005 | "…the closer people get to cracking the last 97 characters…" (length given deliberately, per the reporter) | P | npr.org/transcripts/4684720 |
| J7 | NYT 22 Apr 2006 / NPR 21 Apr 2006 | He had "marked certain letters that could be left out" to justify the lines; "some things I chose to leave out. And I did leave an X out" | J / P\* | mirror §10.1 #4 |
| J8 | NOVA Q&A, Jul 2007 | Favourite encryption: "Matrix codes (bar codes) are special. They are more 'art-like.'" "I was mathematically illiterate." Pen and paper? "Anything is possible." | P | https://www.pbs.org/wgbh/nova/article/sanborn-puzzle/ |
| J9 | Wired, Apr 2009 | The text was scrambled by "a coding system that would unravel itself slowly over a period of time." | P | metzdowd repost |
| J10 | NYT 20 Nov 2010 (Schwartz) | "My friend says, 'What do you have in letter-position 27?' … 'If that's not the same letter, Game over'". Plaintext position 27 is the O of NORTHEAST (26-34). So the checker tests plaintext letters by absolute position | P | https://www.nbcnews.com/id/wbna40294019 (NYT reprint) |
| J11 | NPR 22 Nov 2010 | Released images "of my original decoding charts … for me they were encoding charts … once the Krypto-philes study it in a forensic manner, there might be revelations"; "a riddle within a riddle … several directions. The word directions is - I use intentionally." | P | https://www.npr.org/transcripts/131520768 |
| J12 | Zola dinner Oct 2011 / ACA dinner Oct 2013 | 2011: "Mr. Sanborn indicated this is a one-to-one mapping" (NYPVTT to BERLIN). 2013: "rattle[d] through the entire crib and say: N = B, Y = E, …" | S | kryptools page (quotes several attendees) |
| J13 | Big Techday, Munich, c.2013 | "matrix codes for the parts that have been deciphered … this shows you more or less the way I did it"; "flip the chart over, turn it upside down … shine a light on it" (about the K1-K3 sheets) | S/P\* (member transcription of YouTube oFKPNRpE21o; not checked by me) | mirror §10.1 #2 |
| J14 | NYT 20 Nov 2014 | "There are several really interesting clocks in Berlin." "You'd better delve into that particular clock." | P | cryptologicfoundation NYT reprint |
| J15 | Lunch, Mar 2019 (Dunin's notes) | "Jim said that yes the ciphertext and plaintext were connected … Jim backed off and said he would only commit to the fact that K4 is exactly 97 characters long, and that BERLIN is plaintext that starts at exactly the 64th character"; confused by "masking technique"; no particular book needed, just "to be able to read" | S | https://scienceblogs.de/klausis-krypto-kolumne/2019/03/15/cnn-documentary-about-kryptos-a-making-of-report-with-many-photographs/ (fetched) |
| J16 | Same lunch (Bob Bogart, blog comment #4, 16 Mar 2019) | "BERLINCLOCK in plain matches directly with NYPVTTMZFPK. It is a one-to-one match with plain B taken, has the encipherment done to it, and out pops a cipher N, plain E is then enciphered to a cipher Y, etc. That's at least according to Jim Sanborn" | S (it conflicts with J15 from the same lunch) | same page, comment #4 (fetched). Bean 2021 cites this |
| J17 | NPR 29 Jan 2020 | "it is very close - within days - to when I actually developed that 97-character string." "I am lousy at math to the point where I consider myself to be anathamath. Now, perhaps being an artist, **I have an advantage in that I can employ methods that don't have anything to do with mathematics.**" "It's a 97-character phrase … It's going to lead to something else." | P | https://www.npr.org/transcripts/801323608 (fetched) |
| J18 | AJ Jacobs interview, 2020 | "I came up with a system based on the materials that he had given me … There are codes that depend entirely on patterns … he gave me a few … suggestions, all of which I could then modify myself" / "I made the layout the same time for the two [NORTHEAST/EASTNORTHEAST]" / "There was nobody I could ask to proofread KRYPTOS" / "it could be done with pencil and paper" / 1990 vetting: "I cut up the plain text into pieces … they were mixed up, they weren't in order." | P | https://scienceblogs.de/klausis-krypto-kolumne/files/2020/10/KRYPTOS-Interview-Jacobs.pdf (fetched) |
| J19 | Aug 2020 (Briere) | On EAST: "It was not inadvertent." | S | mirror §11.6 |
| J20 | Open letter 14 Aug 2025 | "97-character K4 code section"; "its riddle will persist as K5" | P | https://www.elonka.com/kryptos/OpenLetterAug2025.html |
| J21 | Aug 2025 (FT via Dunin) | Scheidt designed, Sanborn changed: "It is a solid system, and I fucked with it." "I can't say." | S (FT text not found online by me) | mirror §11.2 |
| J22 | AP / NoVA Mag Nov 2025 | "They don't have the method with which it's deciphered." "nobody has the method but me." | P | https://northernvirginiamag.com/news/2025/11/19/the-secrets-to-the-cia-kryptos-sculpture-are-now-for-sale/ |
| J23 | RR blog, 2025 | "What they found was scrambled text … They did not solve K4 and they certainly did not find the key." "K4 has been discovered and it points in the direction of K5." | P | https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/ |
| J24 | **Spy Museum talk, 12 Nov 2025** (SciAm, Vergano) | Asked about the mathematics of K4: **"Who says it is even a math solution?"** (joking). Later: **"I was fortunate not to understand mathematics, probably in my ability to make the code."** He counselled "creativity". | P | https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/ (fetched, context checked) |
| J25 | Open letter 12 Nov 2025 | "The method of decryption also known as the Key is in this auction"; "Proof-of-Concept piece: In 1988 … I had to know if and how long it would take to cut 2000 letters through heavy copper plate, and would it distort the cut letters when it was rolled into a curve"; "I made multiple versions of the text, with different lengths and coding"; "K5 is 97 characters long, has a similar coding system to K4. has the words BERLINCLOCK in the same position as in K4" | P (transcription) | https://www.numberworld.blog/2025/11/jim-sanborn-open-letter.html |
| J26 | 2026 | No public Sanborn statement on method found. The Paradigm post (12 Jun 2026) has no Sanborn quotes. D. Robinson (groups.io, Jun 2026) says the verifier checked locally: 97 chars, A-Z only, EASTNORTHEAST/BERLINCLOCK at the expected positions, and that Paradigm holds a written method description | S | https://www.paradigm.xyz/writing/kryptos ; mirror §11.2 |

### Items the coordinator asked about
- **"I used a technique that hadn't been used"**: **X, not found** in any source. The nearest are Scheidt's "The masking technique may not be known" (S1, P\*) and Sanborn's "visual systems … individualistic" (J5, P\*). Do not cite it.
- **"orientation/positioning of the errors"**: Sanborn to Dunin, **S** (J4). Undated on rumkin; the mirror dates it to 3 Nov 2003.
- **"who says it's a math solution"**: **VERIFIED P**, SciAm 12 Nov 2025 (J24), as a joke. It agrees with NPR 2020 (J17, P).
- **letter-position 27 test**: **VERIFIED P**, NYT 20 Nov 2010 (J10).
- **2019 lunch "one-to-one"**: two S accounts of the same lunch conflict. Bogart says it was one-to-one; Dunin says Sanborn "backed off". The 2011 and 2013 dinner notes also say one-to-one (S). The positional reading is consistent with J10 (position-27 test) and with the Paradigm verifier check (S).
- **2025 open letters**: P (J20, J25). **Paradigm**: P (J26). **2026 remarks**: none public.

## 3. The 1988 copper plate ("J.S.1988")
- **Verified by looking at the images** (RR lot images 3507616_2.jpg and _9.jpg, cdn.rrauction.com). The plate is curved, with three rows of 8 serif letters cut through: **CDEFGHIJ / DEFGHIJK / EFGHIJKL**. The C at top left is partly clipped by the edge. The edge is stamped **"J.S.1988"**.
- RR lot item 11: "a 3/8" thick 12"x 24" Kryptos 'proof of concept' curved copper plate, 1988, signed 'J.S.1988'". Item 12 is a studio photo of it during the cutting.
- **Who is J.S.:** Jim Sanborn. He calls it his own piece: "So, I made the heavy copper 'proof-of-Concept' piece" (J25, P).
- **What it tests (Sanborn, P):** how long it takes to cut letters through heavy copper plate, and whether rolling the plate into a curve distorts the cut letters. **It is a fabrication test, not a cipher test.**
- **Does the plain tableau suggest K4/K5 use a standard alphabet? No.**
  1. Sanborn states the purpose, and it is mechanical.
  2. Rows shifted by one are simply a 3×8 window of a Vigenère tableau, the design element of the right-hand panel. In 1988 the keyed alphabet may not yet have been fixed: Dunin's 2015 notes (S) report a 1988 maquette with a malformed **GIRASOL** tableau.
  3. Standard-A-Z periodic and Gromark/Gronsfeld schemes are already crib-excluded (ruled_out.md).

  At most the plate shows that a shifted-row tableau layout was planned by 1988. It is neutral on K4's alphabet. **H-1505 SUPPORTED: the plate is not cipher evidence.**

## 4. Constraint set (only verified hints; grade in brackets)
1. **C-len/pos [P]:** 97 letters; plaintext and ciphertext share positions. Evidence: J6, J10, J17, J20, and Sanborn's NYT 2010 numbering; Paradigm 97 A-Z check [S].
2. **C-1:1 [S, conflicting]:** position i of the plaintext gives position i of the ciphertext (J12, J16), but Sanborn "backed off" in 2019 (J15). No final transposition of the text across the cribs.
3. **C-hand [P/S]:** pencil and paper, "retainable", written on paper (S7). "Simple, can be remembered, executed years later with the correct key word/s" (S4, S). Field and agent class (S4, S10).
4. **C-stages [P]:** more than one stage (S6), with "layers / mix and match" (S6c). The steps are substitution ("move it down one or two … combining the functions"), a transposition "square", then a mask (S7).
5. **C-mask [P]:** the mask removes English frequency features (S1, S2, S6). "The masking technique may not be known" (S1). OTP-like "in the sense of the result" (S7b). Not a numeric base change and not a foreign or dead language: Scheidt says he was asked not to use those (S6c, S7, S8).
6. **C-nonmath [P]:** "methods that don't have anything to do with mathematics" (J17); "Who says it is even a math solution?" (J24); "matrix codes" and "visual systems … individualistic" (J5); "codes that depend entirely on patterns" (J18). Scheidt adds "not mathematical (although … modeled mathematically)" (S4, S).
7. **C-modified [P]:** Sanborn modified Scheidt's suggestions (J5, J18, S6d; "I fucked with it" J21 is S). Scheidt never verified K4, and nobody proofread it (S6d, J18). **So 1-2 encipherment errors are plausible.**
8. **C-K5 [P]:** K5 is 97 letters, "similar coding system", BERLINCLOCK at the same position (J25).
9. **C-keywords [J/P]:** Webster received two envelopes, one with "the key words" (AP 1991 via Smithsonian 2020, J). "The method of decryption also known as the Key" (J25, P).

## 5. Ranked method families: consistent with §4 and not excluded by ruled_out.md

**Cross-cutting fact.** All five families below are Latin-tableau substitutions: Vig/Beau/vBeau or Quagmire with any alphabets. For every one of them the cribs force the key-letter equality **X28 = X66** (R→P at both positions) plus 22 inequalities (tools/latin_filter.py). Screen every generated key stream with this first.

### New exact tests run (this task; solvers validated by planted positive controls, workers/w-sources/scripts/)
- **H-1501, REFUTED.** Two superimposed periodic keywords, k_i = a[i mod L1] + b[i mod L2], under Vig/Beau/vBeau with AZ or KA alphabets (6 tableaux). This is Scheidt's "move it down … then you start combining the functions".
  - Every pair with L1+L2 ≤ 24 is inconsistent with the cribs. That includes the motivated pairs (7,8), (7,10), (8,10), (6,7), (7,11), (6,11), (5,7), (4,7), (7,9), (7,12), (7,13), (7,14) and (10,11), i.e. KRYPTOS + PALIMPSEST / ABSCISSA / BERLIN / CLOCK lengths.
  - The pairs that survive (L1+L2 ≥ 25) also survive for random ciphertexts (control: 30 random CTs give 210-217 consistent pairs vs K4's 212, minimum L1+L2 24-25). They are crib-untestable.
  - A planted (7,10) KA-Vig case is detected.
- **H-1503 (part), REFUTED.** Chain-addition / lagged-Fibonacci key mod 26 ("Vimark", base 26, Scheidt's "regenerative function"), k[j+n] = k[j] + k[j+1] or k[j] + k[j+n-1], primer length n = 2..24, 6 standard tableaux.
  - 0 consistent configurations; random controls also 0.
  - Planted cases at n = 5, 7, 10, 15, 20 (both variants) are all recovered.
  - This complements w-gromark, which covers bases 2-16. Arbitrary-alphabet Vimark is NOT covered.

### Shortlist (ranked)
1. **F1. Keyword tableau with a TRANSPOSED key: K1/K2 substitution whose key stream is "pushed into the square" (K3-style route) before use (H-1502).**
   - Why it fits:
     - Scheidt's 2020 order is substitution, then transposition square, then mask, and "K1, two, three … steps … K4 being the final" (P).
     - Sanborn's "matrix codes" (P\*) and "all possible shifts" of the "original matrix" (S).
     - The NSA's 1993 one-step K3 description ("KRYPTOS … repeated 13 times") (P via w-antipodes and the mirror).
     - Transposing the KEY leaves plaintext and ciphertext positions aligned (C-1:1), yields a non-periodic, OTP-like key from short keywords (C-mask), and is fully pencil-and-paper.
     - Columnar transposition of the TEXT is excluded (w-transpo); transposition of the KEY is not.
   - **Test:**
     - Key = keyword K repeated to 97 (or to 98 with the "?"), written in a width-w grid (w = 4..31), read by columns in the order of keyword T (KRYPTOS, PALIMPSEST, ABSCISSA, BERLIN, CLOCK and the K3 route: width 24 → 8 rotations, or the decimation 192 mod 337 style).
     - Tableaux: AZ/KA × Vig/Beau/vBeau.
     - Gate: X28 = X66, then 24/24 cribs, then English on the other 73 letters.
     - Falsified if no (K, T, w, route) passes. The mirror reports a similar 846,720-case test (T16) negative with unspecified alphabets, so replication is needed.
     - Overlaps w-keygen (T14): coordinate.
2. **F2. Matrix/tableau route key: key letters read from a physical grid (KA tableau or Kryptos left panel) by a position-determined route, with flips and rotations (H-1504).**
   - Why it fits: "matrix codes", "flip the chart over, turn it upside down" (S/P\*), "visual systems … individualistic" (P\*), "codes that depend entirely on patterns" (P), "methods that don't have anything to do with mathematics" (P). It needs no arithmetic and works with the sculpture alone ("a copy … suffices", 2011 S).
   - **Test:**
     - Enumerate the 8 dihedral orientations of (a) the 26×26 KA tableau and (b) the carved 14×31 / 4+31+31+31 layout.
     - Routes: rows, columns, diagonals, boustrophedon, start offsets.
     - Take 97-letter key streams. Gate with X28 = X66 and 24/24 under 6 tableaux plus the "key letter = column header" convention.
     - Falsified if nothing passes beyond the random-control rate.
3. **F3. Keyword-mixed two-alphabet substitution (Quagmire IV style) with a long or compound key from 2-3 keywords (H-1501 remainder, L1+L2 ≥ 25, or a keyword pair under KEYWORD-mixed alphabets).**
   - Why it fits: "combining the functions" (P), "correct key word/s" (S), the two envelopes with "key words" (J), K5 "similar coding system" (the same alphabets with a different key would give K5 ≠ K4 at 64-74).
   - **Test:**
     - Fix the alphabets to keyword-mixed alphabets from a short motivated list (KRYPTOS, GIRASOL, PALIMPSEST, ABSCISSA, BERLIN, CLOCK, SHADOW, EGYPT, WELTZEITUHR).
     - Rerun the H-1501 linear solver with L1 + L2 ≤ 24, where it is decisive.
     - For L1 + L2 ≥ 25, require the keys to be English words of those lengths and decrypt.
4. **F4. Regenerative key with an unknown mixed alphabet: chain addition / PT-autokey-like "regenerative function" (Scheidt 2011, S) (H-1503 remainder).**
   - Fixed-tableau Vimark is now dead (above).
   - Still open: Vimark with one unknown mixed alphabet (z3, as w-mask did for autokey), and Beaufort PT-autokey L=7 with a mixed alphabet (w-mask: SAT, SA inconclusive). The mirror's T18 kills L=7 error-free for any alphabet; replicate.
   - **Test:** z3 over (alphabet, primer) for n ≤ 12. Falsified by unsat or by non-English forced text.
   - Lower prior: content-dependent autokey variants conflict with K5 sharing the BERLINCLOCK position (H-208).
5. **F5 (low). A crib-preserving plaintext block shuffle (H-704) or a deliberately dropped or marked letter (J7 "letters that could be left out") on top of F1-F3.**
   - Consistent with "scrambled" 1990 strips, though those were vetting copies (w-transpo). Statistically untestable alone.
   - **Test:** only as a wrapper. Rerun F1-F3 winners with ±1 shifts between the cribs (w-errtol/mirror §10.3 protocol).

Dropped as inconsistent with the verified hints: binary/XOR/base-16 masks (Scheidt says he was asked not to change the math base; Sanborn: "no idea what ASCII or XOR is", S; w-mask closure theorem), foreign or extinct-language plaintext (S6c, S8), and anything needing heavy arithmetic ("anathamath").

## 6. Sources (31 consulted)
1 Bean 2021 PDF (ecp.ep.liu.se …/153/109) · 2 scienceblogs.de Kryptos workshop transcript (2015) · 3 Klausis CNN 2019 post + Bogart comment · 4 Klausis 2020-01-30 NORTHEAST · 5 Klausis 2020-08-24 EAST · 6 Klausis 2020-10-03 + KRYPTOS-Interview-Jacobs.pdf · 7 Jacobs–Scheidt Rev.com transcript (raw mirror) · 8 npr.org/transcripts/4684720 (2005) · 9 npr.org/transcripts/131520768 (2010) · 10 npr.org/transcripts/801323608 (2020) · 11 pbs.org NOVA Q&A 2007 · 12 nbcnews wbna40294019 (NYT 2010) · 13 cryptologicfoundation NYT 2014 reprint · 14 smithsonianmag 2020 third clue · 15 kryptools hints page (Wired 2005, ABC 1991, 1989 letter, Wired 2009) · 16 kryptosfan masking-vs-english · 17 kryptosfan ACA 2013 · 18 rumkin K4 · 19 rumkin K1 · 20 metzdowd Wired 2009 · 21 northernvirginiamag 2022 · 22 northernvirginiamag 2025 · 23 SciAm 12 Nov 2025 · 24 numberworld 12 Nov 2025 letter · 25 elonka OpenLetterAug2025 · 26 paradigm.xyz/writing/kryptos · 27 RR lot page (items list) · 28 RR blog "Discovered, Not Solved" · 29 RR CDN images _2, _4, _9 (plate, viewed) · 30 aciderix/kryptos-research-handoff README + KB 07/09 (members-only derived; S only) · 31 kryptos.groups.io msg 12611 (login-gated, unreadable).
Not found / blocked: the FT Aug 2025 article; NYT 2020 originals (only quoted via Smithsonian/Klausis); AAA 2009 oral history transcript (403); the Big Techday 2013 video (not checked).
