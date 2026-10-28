# K4 decidability map (it51–it78)

This map sorts model families into three groups:

- **DEAD:** exact contradiction with the two cribs, or with an alphabet-free statistic, with planted controls passing.
- **CRIB-UNTESTABLE:** K4 is feasible at the null rate, because the family has too many free parameters for the 24 crib letters.
- **OPEN:** neither decided nor shown to be untestable.

## Information budget (rule of thumb)

- The cribs carry about 113 bits with a known alphabet. With unknown alphabets they carry much less, because only letter coincidences constrain.
- An arbitrary alphabet costs about 88 bits, and two cost about 177 bits.
- A periodic key costs 4.7 bits per period letter.
- An English running key costs about 31 bits over the crib span, plus the source offset.

## DEAD

### Substitution families

- Monoalphabetic substitution; periodic p ≤ 5; key alphabets with ≤ 4 symbols. Rejected by IC for ANY alphabets and ANY transposition (it62).
- Transposition followed by period-p substitution (p arbitrary alphabets): rejected by column IC at p = 2–9, 12, 13 (it64).
- Periodic Q3 / Gronsfeld through one arbitrary alphabet: p = 1–22, 24, 25, 34–40, 42–45, 48 (it54).
  - With one omitted or inserted CT letter between the cribs: p = 1–13 (it69).
- Progressive periodic key through one alphabet: p = 1–7, 9, 14, 19 (it61).
- Free small-digit key 0..m−1: m ≤ 5 with one alphabet; m = 2 with two alphabets (it70).
- Grid key r(row) + c(col):
  - one arbitrary alphabet: w = 6, 9, 19, 21 (it72);
  - fixed AZ/KA tableaux: every w ≤ 25 (it76).
- Gromark: all primers (it57). Base-26 primer ≤ 4 (it58). Constant-digit keys (it59). 25 integer sequences (it60).

### Autokey

- PT-autokey: L = 6–7 exact; L = 8–10 mostly dead (it51); L = 1–4 and 42 under any Latin tableau (it56).
- CT-autokey: under any two alphabets, L = 1, 4, 5, 7, 10, 11, 18–20, 22–25, 42, 45 (it55). Under any Latin tableau, L = 1–11, 13–31, 33, 35, 42, 49, 50, 53, 55, 58, 65 (it56). Under one alphabet, L ≤ 31 (it53).

### Keys built from keywords or texts

- Repeated keyword pushed through ANY transposition, for AZ/KA and all dictionary-keyed tableaux (it66, it67).
- K1–K3 plaintext running key under any key transposition (it68).
- Cyrillic Projector plaintext as a running key (it63).

### Grids and machines

- 25-letter grid ciphers (Playfair, two-square, four-square, Bifid 5×5): K4 uses all 26 letters (it65).
- M-94 / CSP-488 cylinder, any disk order and offset (it75).

## CRIB-UNTESTABLE (feasible at the null rate)

- Chaocipher: about 1e11 consistent wheel pairs for any CT (it74 lemma).
- Hagelin M-209 / C-38 pin-and-lug keys (it77).
- Free small-digit keys with m ≥ 6. Grid keys at w = 7 and other w at the null rate (it70, it72).
- Periodic keys through one alphabet at the feasible periods (23, 26–33, 41, 46, 47 in it54), and with two arbitrary alphabets generally.
- A generic English running key from an unknown source, with any tableau.

## Weak or disfavoured, not decided

- A general 26-letter digraphic table: planted P = 0.062 (it65).

## Open, with a concrete next test

- PT-autokey at L ≥ 11 (capped).
- Chaocipher or a running key plus language scoring. Both need brute force, which is excluded by the project rule.
- An Antipodes K4 transcript diff (H-508), blocked on a transcript.
