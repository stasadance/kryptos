# Known plaintext (1-indexed positions in 97-char K4 ciphertext)

| Pos   | Ciphertext     | Plaintext      | Source / year |
|-------|----------------|----------------|---------------|
| 22-25 | FLRV           | EAST           | Sanborn, 2020 (with NORTHEAST) |
| 26-34 | QQPRNGKSS      | NORTHEAST      | Sanborn, 2020 |
| 64-69 | NYPVTT         | BERLIN         | Sanborn, 2010 |
| 70-74 | MZFPK          | CLOCK          | Sanborn, 2014 |

Combined: 22-34 EASTNORTHEAST, 64-74 BERLINCLOCK.
Slices verified by script against facts/ciphertext.txt (2026-10-26). Hint years VERIFIED (w-lit 2026-10-26): BERLIN NYT 20 Nov 2010; CLOCK NYT 20 Nov 2014; NORTHEAST NYT 29 Jan 2020; EAST given privately Apr 2020, public Aug 2020 — https://elonka.com/kryptos/ , https://scienceblogs.de/klausis-krypto-kolumne/2020/01/30/jim-sanborn-publishes-new-kryptos-clue/ , https://scienceblogs.de/klausis-krypto-kolumne/2020/08/24/jim-sanborn-publishes-another-new-kryptos-clue/ , https://en.wikipedia.org/wiki/Kryptos . Positions: Sanborn himself only firmly committed to len 97 and BERLIN starting at 64 (Elonka 2019 notes, https://rumkin.com/reference/kryptos/k4/); 2025 Smithsonian scraps reportedly contained BERLIN CLOCK and EAST NORTHEAST (SciAm Oct 2025).
Note: CORRECTED (w-lit): self-encryption occurs at pos 33 (S->S) and pos 74 (K->K); none at 64 (B->N).
