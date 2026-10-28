/* it51 stage 1, v3 (degree heuristic; argv[7]=0 restores v2 ordering): exact enumeration of PT-autokey alphabets consistent with both K4 cribs, with
   bidirectional chain propagation and dynamic most-constrained-relation branching.
   Relation R_j (21+L <= j <= 73): letters p=P_j, q=P_{j-L}, c=C_j:
       form 0 vig  a(c) = a(p) + K(q);  1 beau a(c) = K(q) - a(p);  2 var a(c) = a(p) - K(q)    (mod 26)
       K(q) = a(q) (kr 0) | AZ index (kr 1) | KA index (kr 2)
   Unknowns: plaintext letters at 34..62 and alphabet values. Output: one line per consistent
   assignment of (partial alphabet, plaintext 21..73).
   Usage: akenum2 CT L form kr maxsol */
#include <stdio.h>
#include <stdlib.h>
static const char *KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int kai[26], kal[26];
static int ct[97], pt[97];
static int a[26], inv[26];
static int L, form, kr, J0, J1;
static long long nsol, maxsol, nodes, nodecap;
static int heur = 1;
static int nfreev(void) { int n = 0; for (int v = 0; v < 26; v++) n += inv[v] < 0; return n; }
static int Kof(int q) { return kr == 1 ? q : (kr == 2 ? kai[q] : a[q]); }   /* -1 if unknown (kr0) */
static int Kinv(int K) { return kr == 1 ? K : (kr == 2 ? kal[K] : inv[K]); }
static int mod(int x) { x %= 26; return x < 0 ? x + 26 : x; }
/* relation value pieces */
static int need_p(int ac, int K) { return form == 0 ? mod(ac - K) : (form == 1 ? mod(K - ac) : mod(ac + K)); }
static int need_c(int ap, int K) { return form == 0 ? mod(ap + K) : (form == 1 ? mod(K - ap) : mod(ap - K)); }
static int need_K(int ac, int ap) { return form == 0 ? mod(ac - ap) : (form == 1 ? mod(ac + ap) : mod(ap - ac)); }
static void emit(void) {
    nsol++;
    if (nsol <= maxsol) {
        for (int x = 0; x < 26; x++) printf("%d%c", a[x], x == 25 ? ' ' : ',');
        for (int i = 0; i < 97; i++) putchar(pt[i] >= 0 ? 'A' + pt[i] : '.');
        putchar('\n');
    }
}
static void dfs(void);
static void setv(int x, int v) { a[x] = v; inv[v] = x; }
static void unsetv(int x) { inv[a[x]] = -1; a[x] = -1; }
/* status of relation j: returns -2 resolved&ok, -1 contradiction, 0 inactive, else branching cost; *act = action code */
static int status(int j, int *act) {
    int p = pt[j], q = pt[j - L], c = ct[j];
    if (p < 0 && q < 0) return 0;
    if (q >= 0) {
        int K = Kof(q);
        if (K < 0) { *act = 1; return nfreev(); }                       /* branch a(q) */
        if (p >= 0) {
            int ac = a[c], ap = a[p];
            if (ac >= 0 && ap >= 0) return need_c(ap, K) == ac ? -2 : -1;
            if (ac >= 0) { int t = need_p(ac, K); if (inv[t] >= 0 && inv[t] != p) return -1; *act = 2; return 1; } /* set a(p)=t */
            if (ap >= 0) { int t = need_c(ap, K); if (inv[t] >= 0 && inv[t] != c) return -1; *act = 3; return 1; } /* set a(c)=t */
            if (c == p) { /* same letter: a(c)=need_c(a(c),K) */ *act = 4; return nfreev(); }
            *act = 4; return nfreev();                                  /* branch a(c) */
        }
        if (a[c] < 0) { *act = 4; return nfreev(); }                    /* branch a(c) */
        int t = need_p(a[c], K);
        if (inv[t] >= 0) { *act = 5; return 1; }                        /* p = inv[t] */
        *act = 6; return 26 - (26 - nfreev());                          /* branch letter p among unassigned letters */
    }
    /* q unknown, p known: backward */
    int ac = a[c], ap = a[p];
    if (ac < 0) { *act = 4; return nfreev(); }
    if (ap < 0) { *act = 7; return nfreev(); }                          /* branch a(p) */
    int K = need_K(ac, ap), x = Kinv(K);
    if (x >= 0) { *act = 8; return 1; }                                 /* q = x */
    *act = 9; return nfreev();                                          /* kr0: branch letter with value K */
}
static void dfs(void) {
    if (++nodes > nodecap || nsol >= maxsol) return;
    int best = -1, bc = 1 << 30, bact = 0, deg[26] = {0};
    for (int j = J0; j <= J1; j++) {
        int act = 0, s = status(j, &act);
        if (s == -1) return;
        if (s > 0 && s < bc) { bc = s; best = j; bact = act; if (s == 1) break; }
        if (s > 1) {   /* degree of unassigned letters in unresolved relations (variable-ordering heuristic) */
            int p = pt[j], q = pt[j - L], c = ct[j];
            if (a[c] < 0) deg[c]++;
            if (p >= 0 && a[p] < 0) deg[p]++;
            if (kr == 0 && q >= 0 && a[q] < 0) deg[q]++;
        }
    }
    if (best < 0) { emit(); return; }
    if (bc > 1 && heur) {   /* branch on the value of the most-referenced unassigned letter */
        int x = -1, bd = 0;
        for (int y = 0; y < 26; y++) if (deg[y] > bd) { bd = deg[y]; x = y; }
        if (x >= 0) {
            int none = 1; for (int y = 0; y < 26; y++) if (a[y] >= 0) none = 0;
            for (int v = 0; v < 26; v++) if (inv[v] < 0) {
                /* kr0 relations are homogeneous linear: a -> u*a (u a unit) is a symmetry, so the first value
                   chosen only needs one representative per unit-orbit {0},{13},{odd units},{even non-13} */
                if (kr == 0 && none && !(v == 0 || v == 1 || v == 2 || v == 13)) continue;
                setv(x, v); dfs(); unsetv(x);
            }
            return;
        }
    }
    int j = best, p = pt[j], q = pt[j - L], c = ct[j];
    switch (bact) {
    case 1: for (int v = 0; v < 26; v++) if (inv[v] < 0) { setv(q, v); dfs(); unsetv(q); } break;
    case 2: { int t = need_p(a[c], Kof(q)); if (a[p] >= 0) break; setv(p, t); dfs(); unsetv(p); } break;
    case 3: { int t = need_c(a[p], Kof(q)); if (a[c] >= 0) break; setv(c, t); dfs(); unsetv(c); } break;
    case 4: for (int v = 0; v < 26; v++) if (inv[v] < 0) { setv(c, v); dfs(); unsetv(c); } break;
    case 5: { int t = need_p(a[c], Kof(q)); pt[j] = inv[t]; dfs(); pt[j] = -1; } break;
    case 6: { int t = need_p(a[c], Kof(q)); for (int x = 0; x < 26; x++) if (a[x] < 0) { setv(x, t); pt[j] = x; dfs(); pt[j] = -1; unsetv(x); } } break;
    case 7: for (int v = 0; v < 26; v++) if (inv[v] < 0) { setv(p, v); dfs(); unsetv(p); } break;
    case 8: { int K = need_K(a[c], a[p]); pt[j - L] = Kinv(K); dfs(); pt[j - L] = -1; } break;
    case 9: { int K = need_K(a[c], a[p]); for (int x = 0; x < 26; x++) if (a[x] < 0) { setv(x, K); pt[j - L] = x; dfs(); pt[j - L] = -1; unsetv(x); } } break;
    }
}
int main(int argc, char **argv) {
    const char *C = argv[1]; L = atoi(argv[2]); form = atoi(argv[3]); kr = atoi(argv[4]); maxsol = atoll(argv[5]);
    nodecap = argc > 6 ? atoll(argv[6]) : 4000000000LL;
    heur = argc > 7 ? atoi(argv[7]) : 1;
    for (int i = 0; i < 26; i++) { kai[KA[i] - 'A'] = i; kal[i] = KA[i] - 'A'; }
    for (int i = 0; i < 97; i++) { ct[i] = C[i] - 'A'; pt[i] = -1; }
    const char *E = "EASTNORTHEAST", *B = "BERLINCLOCK";
    for (int i = 0; i < 13; i++) pt[21 + i] = E[i] - 'A';
    for (int i = 0; i < 11; i++) pt[63 + i] = B[i] - 'A';
    for (int x = 0; x < 26; x++) { a[x] = -1; inv[x] = -1; }
    J0 = 21 + L; J1 = 73;
    /* gauge: vig/var with kr 1/2 are shift-invariant -> fix a(ct[73]) = 0 */
    if (kr != 0 && form != 1) setv(ct[73], 0);
    dfs();
    fprintf(stderr, "L=%d form=%d kr=%d nodes=%lld%s solutions=%lld\n", L, form, kr, nodes, nodes > nodecap ? "(CAP)" : "", nsol);
    return 0;
}
