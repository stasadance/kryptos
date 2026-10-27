"""Exact parametrisation of all crib-consistent (alpha, f, g) for the grid-key Quagmire-III model.
Unknowns X = [alpha(A..Z), f(rows), g(cols)]; equations alpha(c_i) - alpha(p_i) - f_r - g_c = 0 (mod 26).
Kernel mod 2 and mod 13 by Gaussian elimination; X = 13*x2 + 14*x13 (mod 26) by CRT."""
import numpy as np
def kernel_mod_p(M, p):
    M = M.copy() % p; rows, n = M.shape; piv = []; r = 0
    for c in range(n):
        pr = next((i for i in range(r, rows) if M[i, c] % p), None)
        if pr is None: continue
        M[[r, pr]] = M[[pr, r]]; inv = pow(int(M[r, c]), -1, p); M[r] = (M[r] * inv) % p
        for i in range(rows):
            if i != r and M[i, c]: M[i] = (M[i] - M[i, c] * M[r]) % p
        piv.append(c); r += 1
        if r == rows: break
    free = [c for c in range(n) if c not in piv]; B = []
    for fc in free:
        v = np.zeros(n, dtype=np.int64); v[fc] = 1
        for i, pc in enumerate(piv): v[pc] = (-M[i, fc]) % p
        B.append(v)
    return np.array(B, dtype=np.int64)
def system(ct, w, o, beau=False):
    CR = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
    NR = (96 + o) // w + 1; n = 26 + NR + w; eqs = []
    for s, wd in CR.items():
        for j, p in enumerate(wd):
            i = s + j; e = np.zeros(n, dtype=np.int64)
            e[ord(ct[i]) - 65] += 1; e[ord(p) - 65] += (1 if beau else -1)
            e[26 + (i + o) // w] -= 1; e[26 + NR + (i + o) % w] -= 1; eqs.append(e)
    return np.array(eqs) % 26, NR, n
def write(ct, w, o, path, beau=False):
    M, NR, n = system(ct, w, o, beau); K2 = kernel_mod_p(M, 2); K13 = kernel_mod_p(M, 13)
    with open(path, "w") as f:
        f.write(f"{n} {NR} {len(K2)} {len(K13)}\n")
        for v in K2: f.write(" ".join(map(str, v)) + "\n")
        for v in K13: f.write(" ".join(map(str, v)) + "\n")
    return len(K2), len(K13)
if __name__ == "__main__":
    import sys
    ct, w, o, path = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    print(write(ct, w, o, path))
