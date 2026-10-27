#!/usr/bin/env python3
"""Reproduce Kryptos K1-K3 decryptions (verification of published methods).
K1/K2: Quagmire-III style Vigenere, both alphabets = KRYPTOS-keyed alphabet.
K3: double rotation transposition (24x14 grid rotated, then 8-wide rotated)."""
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
def vig_dec(ct, key, alpha=KA):
    out, j = [], 0
    for c in ct:
        if c not in alpha: out.append(c); continue   # '?' passes through, key not advanced
        out.append(alpha[(alpha.index(c) - alpha.index(key[j % len(key)])) % 26]); j += 1
    return "".join(out)
def vig_enc(pt, key, alpha=KA):
    out, j = [], 0
    for c in pt:
        if c not in alpha: out.append(c); continue
        out.append(alpha[(alpha.index(c) + alpha.index(key[j % len(key)])) % 26]); j += 1
    return "".join(out)
K1 = "EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJYQTQUXQBQVYUVLLTREVJYQTMKYRDMFD"
K2 = ("VFPJUDEEHZWETZYVGWHKKQETGFQJNCEGGWHKK?DQMCPFQZDQMMIAGPFXHQRLG"
      "TIMVMZJANQLVKQEDAGDVFRPJUNGEUNAQZGZLECGYUXUEENJTBJLBQCRTBJDFHRR"
      "YIZETKZEMVDUFKSJHKFWHKUWQLSZFTIHHDDDUVH?DWKBFUFPWNTDFIYCUQZERE"
      "EVLDKFEZMOQQJLTTUGSYQPFEUNLAVIDXFLGGTEZ?FKZBSFDQVGOGIPUFXHHDRKF"
      "FHQNTGPUAECNUVPDJMQCLQUMUNEDFQELZZVRRGKFFVOEEXBDMVPNFQXEZLGRE"
      "DNQFMPNZGLFLPMRJQYALMGNUVPDXVKPDQUMEBEDMHDAFMJGZNUPLGEWJLLAETG")
K3 = ("ENDYAHROHNLSRHEOCPTEOIBIDYSHNAIACHTNREYULDSLLSLLNOHSNOSMRWXMNE"
      "TPRNGATIHNRARPESLNNELEBLPIIACAEWMTWNDITEENRAHCTENEUDRETNHAEOE"
      "TFOLSEDTIWENHAEIOYTEYQHEENCTAYCREIFTBRSPAMHHEWENATAMATEGYEERLB"
      "TEEFOASFIOTUETUAEOTOARMAEERTNRTIBSEDDNIAAHTTMSTEWPIEROAGRIEWFEB"
      "AECTDDHILCEIHSITEGOEAOSDDRYDLORITRKLMLEHAGTDHARDPNEOHMGFMFEUHE"
      "ECDMRIPFEIMEHNLSSTTRTVDOHW")   # final '?' excluded (336 letters)
def rot_cw(s, width):
    """write s in rows of `width`, rotate grid 90deg clockwise, read rows."""
    rows = [s[i:i+width] for i in range(0, len(s), width)]
    return "".join("".join(r[c] for r in reversed(rows)) for c in range(width))
def k3_dec(ct):
    # write in rows of 24, rotate CW; write result in rows of 8, rotate CW
    return rot_cw(rot_cw(ct, 24), 8)
def k3_dec_decimation(ct):
    # Equivalent closed form (found by w-history): PT[k] = CT[(192*k mod 337)], 1-indexed,
    # k=1..336; 337 = 336 letters + the trailing '?'. I.e. K3 is a decimation by 192 mod 337.
    return "".join(ct[(192*k) % 337 - 1] for k in range(1, 337))
if __name__ == "__main__":
    p1 = vig_dec(K1, "PALIMPSEST"); print("K1:", p1)
    p2 = vig_dec(K2, "ABSCISSA");  print("K2:", p2)
    K2c = K2[:-8] + "S" + K2[-8:]  # 2006 correction: missing S restored (...GE S WJLLAETG)
    print("K2 corrected tail:", vig_dec(K2c, "ABSCISSA")[-40:])
    print("K3 len", len(K3))
    p3 = k3_dec(K3); print("K3:", p3)
    assert p3 == k3_dec_decimation(K3)
    assert p1.endswith("IQLUSION") and p3.endswith("CANYOUSEEANYTHINGQ")
    print("all K1-K3 checks OK")
