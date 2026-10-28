#!/usr/bin/env python3
"""it51 control: plant PT-autokey (random alphabet, random L/form/kr) on English with K4's cribs, run akenum,
check the true (alphabet restricted to assigned letters, plaintext at assigned positions) is among the outputs."""
import sys, random, re, subprocess
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; KA = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
def plant(rng, L, form, kr, eng):
    a = list(range(26)); rng.shuffle(a)
    o = rng.randrange(len(eng) - 200); P = list(eng[o:o + 97]); P[21:34] = 'EASTNORTHEAST'; P[63:74] = 'BERLINCLOCK'
    pi = [AZ.index(x) for x in P]; prim = [rng.randrange(26) for _ in range(L)]
    inv = [0] * 26
    for x in range(26): inv[a[x]] = x
    ct = []
    for i in range(97):
        q = pi[i - L] if i >= L else prim[i]
        K = a[q] if kr == 0 else (q if kr == 1 else KA.index(AZ[q]))
        v = (a[pi[i]] + K) % 26 if form == 0 else ((K - a[pi[i]]) % 26 if form == 1 else (a[pi[i]] - K) % 26)
        ct.append(AZ[inv[v]])
    return ''.join(ct), a, ''.join(P)
def run(ct, L, form, kr, maxsol=2000000, gauge=1, timeout=600):
    r = subprocess.run(['iterations/c/akenum', ct, str(L), str(form), str(kr), str(maxsol), str(gauge)], capture_output=True, text=True, timeout=timeout)
    sols = [l.split() for l in r.stdout.splitlines()]
    return sols, r.stderr.strip()
def matches(sol, a, P, form, kr):
    av = list(map(int, sol[0].split(','))); pt = sol[1]
    # allow gauge shift for vig/var with kr 1/2
    shifts = range(26) if (kr != 0 and form != 1) else [0]
    for s in shifts:
        if all(av[x] < 0 or (av[x] - s) % 26 == a[x] for x in range(26)):
            if all(c == '.' or c == P[i] for i, c in enumerate(pt)): return True
    return False
if __name__ == '__main__':
    eng = re.sub('[^A-Z]', '', open('/tmp/claude-0/corpus/pg1342.txt', errors='ignore').read().upper())
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 51)
    for L in map(int, (sys.argv[2] if len(sys.argv) > 2 else '6,7,8,9,10,11,12,13').split(',')):
        for form in range(3):
            for kr in range(3):
                ct, a, P = plant(rng, L, form, kr, eng)
                try: sols, info = run(ct, L, form, kr, timeout=120)
                except subprocess.TimeoutExpired: print(f'L={L} f={form} kr={kr}: TIMEOUT'); continue
                found = any(matches(s, a, P, form, kr) for s in sols)
                print(f'L={L} f={form} kr={kr}: found={found} | {info}', flush=True)
