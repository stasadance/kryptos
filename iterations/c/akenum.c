/* it51: exact enumeration of PT-autokey alphabets consistent with BOTH K4 cribs.
   Model: lag L, unknown alphabet a (letter -> 0..25, bijection).
     key value K(q) of the plaintext letter L back: kr=0 a(q), kr=1 AZ index, kr=2 KA index
     form 0 vig  a(c) = a(p) + K;  form 1 beau a(c) = K - a(p);  form 2 var a(c) = a(p) - K   (mod 26)
   Stage 1 (this program): DFS over the chain steps that reach the cribs. Positions 21..33 (ENE) and
   63..73 (BC) are known plaintext. Steps = positions j in 34..73 whose chain (j mod L) is followed from
   ENE; ENE-internal relations (j in 21+L..33) are checked too. Chains are processed one at a time
   (shortest path to a BC check first) so the BC constraints prune early.
   Output: every consistent (partial alphabet, partial plaintext) as a line; count on stderr.
   Usage: akenum CT L form kr maxsol [gauge]   (CT = 97 letters) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int kai[26];
static int ct[97], pt[97], isc[97];
static int a[26], inv[26];           /* a[letter]=value or -1; inv[value]=letter or -1 */
static int L, form, kr, gauge;
static int steps[200], nsteps;
static long long nsol, maxsol, nodes;
static FILE *out;
static int kval(int q, int *needbranch) { /* returns key value or -1 if a[q] unassigned (kr=0) */
    if (kr == 1) return q; if (kr == 2) return kai[q];
    return a[q];
}
static void emit(void) {
    nsol++;
    if (out && nsol <= maxsol) {
        for (int x = 0; x < 26; x++) fprintf(out, "%d%c", a[x], x == 25 ? ' ' : ',');
        for (int i = 0; i < 97; i++) fputc(pt[i] >= 0 ? 'A' + pt[i] : '.', out);
        fputc('\n', out);
    }
}
static void dfs(int s);
static int target(int cv, int K) { /* value of plaintext letter */
    if (form == 0) return ((cv - K) % 26 + 26) % 26;
    if (form == 1) return ((K - cv) % 26 + 26) % 26;
    return ((cv + K) % 26 + 26) % 26;
}
/* try to place plaintext at step position j with key K known and a[ct[j]] known */
static void place(int s, int j, int K) {
    int t = target(a[ct[j]], K);
    if (isc[j]) {
        int p = pt[j];
        if (a[p] >= 0) { if (a[p] == t) dfs(s + 1); return; }
        if (inv[t] >= 0) return;
        a[p] = t; inv[t] = p; dfs(s + 1); a[p] = -1; inv[t] = -1; return;
    }
    if (inv[t] >= 0) { pt[j] = inv[t]; dfs(s + 1); pt[j] = -1; return; }
    for (int x = 0; x < 26; x++) if (a[x] < 0) {
        a[x] = t; inv[t] = x; pt[j] = x; dfs(s + 1); pt[j] = -1; a[x] = -1; inv[t] = -1;
    }
}
static void withK(int s, int j, int K) {
    int c = ct[j];
    if (a[c] >= 0) { place(s, j, K); return; }
    for (int v = 0; v < 26; v++) if (inv[v] < 0) {
        if (gauge && nodes == 0) {} 
        a[c] = v; inv[v] = c; place(s, j, K); a[c] = -1; inv[v] = -1;
    }
}
static int first = 1;
static void dfs(int s) {
    nodes++;
    if (nsol >= maxsol * 100) return;
    if (s == nsteps) { emit(); return; }
    int j = steps[s], q = pt[j - L];
    if (kr == 0 && a[q] < 0) {
        for (int v = 0; v < 26; v++) if (inv[v] < 0) { a[q] = v; inv[v] = q; withK(s, j, v); a[q] = -1; inv[v] = -1; }
        return;
    }
    withK(s, j, kval(q, 0));
}
int main(int argc, char **argv) {
    const char *C = argv[1]; L = atoi(argv[2]); form = atoi(argv[3]); kr = atoi(argv[4]);
    maxsol = atoll(argv[5]); gauge = argc > 6 ? atoi(argv[6]) : 1;
    for (int i = 0; i < 26; i++) kai[KA[i] - 'A'] = i;
    for (int i = 0; i < 97; i++) { ct[i] = C[i] - 'A'; pt[i] = -1; isc[i] = 0; }
    const char *E = "EASTNORTHEAST", *B = "BERLINCLOCK";
    for (int i = 0; i < 13; i++) { pt[21 + i] = E[i] - 'A'; isc[21 + i] = 1; }
    for (int i = 0; i < 11; i++) { pt[63 + i] = B[i] - 'A'; isc[63 + i] = 1; }
    for (int x = 0; x < 26; x++) { a[x] = -1; inv[x] = -1; }
    /* steps: ENE-internal first, then chains ordered by distance to first BC hit */
    nsteps = 0;
    for (int j = 21 + L; j <= 33; j++) steps[nsteps++] = j;
    int order[13], dist[13], used[13] = {0};
    for (int r = 0; r < L; r++) {      /* chain residue r: start at last ENE position with that residue */
        int e = -1; for (int j = 33; j >= 21; j--) if (j % L == r) { e = j; break; }
        int d = 0, j = e; while (j <= 73 && !(j >= 63)) { j += L; d++; }
        dist[r] = (j <= 73) ? d : 999;
    }
    for (int k = 0; k < L; k++) { int b = -1; for (int r = 0; r < L; r++) if (!used[r] && (b < 0 || dist[r] < dist[b])) b = r; used[b] = 1; order[k] = b; }
    for (int k = 0; k < L; k++) {
        int r = order[k]; int e = -1; for (int j = 33; j >= 21; j--) if (j % L == r) { e = j; break; }
        for (int j = e + L; j <= 73; j += L) steps[nsteps++] = j;
    }
    /* gauge: for vig/var with kr in {1,2}, shift symmetry -> fix value of ct[steps[0]]'s letter to 0 */
    if (gauge && kr != 0 && form != 1) { int c = ct[steps[0]]; a[c] = 0; inv[0] = c; }
    out = stdout;
    dfs(0);
    fprintf(stderr, "L=%d form=%d kr=%d steps=%d nodes=%lld solutions=%lld\n", L, form, kr, nsteps, nodes, nsol);
    return 0;
}
