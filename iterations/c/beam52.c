/* it52: LM-guided beam search for PT-autokey under ONE arbitrary alphabet (lags where exact DFS is capped).
   Front walks the middle plaintext 34..62 in text order. A state = (partial alphabet, plaintext 21..73).
   Each step tries all 26 letters at the front position, then propagates every crib relation R_j (21+L<=j<=73)
   until fixpoint (only forced moves: two of the three values known -> third; known value -> letter).
   Contradictions kill the state. States ranked by quadgram sum over windows ending before the front.
   Output: top states at the end, ranked by quadgram mean over 21..73, as "a0,..,a25 PT97 score".
   Usage: beam52 CT L form kr W qg.bin [nout] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int kai[26], kal[26], ct[97], L, form, kr;
static float *qg;
typedef struct { signed char a[26], inv[26], pt[97]; double s; } St;
static int mod(int x) { x %= 26; return x < 0 ? x + 26 : x; }
static int need_p(int ac, int K) { return form == 0 ? mod(ac - K) : (form == 1 ? mod(K - ac) : mod(ac + K)); }
static int need_c(int ap, int K) { return form == 0 ? mod(ap + K) : (form == 1 ? mod(K - ap) : mod(ap - K)); }
static int need_K(int ac, int ap) { return form == 0 ? mod(ac - ap) : (form == 1 ? mod(ac + ap) : mod(ap - ac)); }
static int setv(St *x, int l, int v) {           /* 1 ok/changed, 0 no change, -1 contradiction */
    if (x->a[l] >= 0) return x->a[l] == v ? 0 : -1;
    if (x->inv[v] >= 0) return -1;
    x->a[l] = v; x->inv[v] = l; return 1;
}
static int setp(St *x, int i, int l) { if (x->pt[i] >= 0) return x->pt[i] == l ? 0 : -1; x->pt[i] = l; return 1; }
static int Kof(St *x, int q) { return kr == 1 ? q : (kr == 2 ? kai[q] : x->a[q]); }
static int propagate(St *x) {
    for (int changed = 1; changed;) {
        changed = 0;
        for (int j = 21 + L; j <= 73; j++) {
            int p = x->pt[j], q = x->pt[j - L], c = ct[j], r = 0;
            if (q >= 0) {
                int K = Kof(x, q);
                if (K < 0) {                      /* kr0, a(q) unknown: solve for it when a(c), a(p) known */
                    if (p >= 0 && x->a[c] >= 0 && x->a[p] >= 0) r = setv(x, q, need_K(x->a[c], x->a[p]));
                } else if (p >= 0) {
                    int ac = x->a[c], ap = x->a[p];
                    if (ac >= 0 && ap >= 0) { if (need_c(ap, K) != ac) return 0; }
                    else if (ac >= 0) r = setv(x, p, need_p(ac, K));
                    else if (ap >= 0) r = setv(x, c, need_c(ap, K));
                } else if (x->a[c] >= 0) {
                    int t = need_p(x->a[c], K);
                    if (x->inv[t] >= 0) r = setp(x, j, x->inv[t]);
                }
            } else if (p >= 0 && x->a[c] >= 0 && x->a[p] >= 0) {
                int K = need_K(x->a[c], x->a[p]);
                if (kr == 1) r = setp(x, j - L, K);
                else if (kr == 2) r = setp(x, j - L, kal[K]);
                else if (x->inv[K] >= 0) r = setp(x, j - L, x->inv[K]);
            }
            if (r < 0) return 0;
            if (r > 0) changed = 1;
        }
    }
    return 1;
}
static double qv(St *x, int s) { return qg[((x->pt[s] * 26 + x->pt[s + 1]) * 26 + x->pt[s + 2]) * 26 + x->pt[s + 3]]; }
static int cmp(const void *u, const void *v) { double d = ((St *)v)->s - ((St *)u)->s; return d > 0 ? 1 : (d < 0 ? -1 : 0); }
int main(int argc, char **argv) {
    const char *C = argv[1]; L = atoi(argv[2]); form = atoi(argv[3]); kr = atoi(argv[4]); int W = atoi(argv[5]);
    int nout = argc > 7 ? atoi(argv[7]) : 50;
    qg = malloc(sizeof(float) * 456976); FILE *f = fopen(argv[6], "rb");
    if (!f || fread(qg, sizeof(float), 456976, f) != 456976) { fprintf(stderr, "qg\n"); return 1; } fclose(f);
    for (int i = 0; i < 26; i++) { kai[KA[i] - 'A'] = i; kal[i] = KA[i] - 'A'; }
    for (int i = 0; i < 97; i++) ct[i] = C[i] - 'A';
    St *cur = malloc(sizeof(St) * (size_t)W), *nxt = malloc(sizeof(St) * (size_t)W * 26); int nc = 0;
    St s0; memset(s0.a, -1, 26); memset(s0.inv, -1, 26); memset(s0.pt, -1, 97); s0.s = 0;
    const char *E = "EASTNORTHEAST", *B = "BERLINCLOCK";
    for (int i = 0; i < 13; i++) s0.pt[21 + i] = E[i] - 'A';
    for (int i = 0; i < 11; i++) s0.pt[63 + i] = B[i] - 'A';
    if (kr != 0 && form != 1) setv(&s0, ct[73], 0);       /* gauge (shift symmetry) */
    if (!propagate(&s0)) { fprintf(stderr, "L=%d form=%d kr=%d: contradiction at start\n", L, form, kr); return 0; }
    cur[nc++] = s0;
    for (int j = 34; j <= 62; j++) {
        int nn = 0;
        for (int k = 0; k < nc; k++) {
            if (cur[k].pt[j] >= 0) { nxt[nn] = cur[k]; nn++; continue; }
            for (int l = 0; l < 26; l++) {
                St *y = &nxt[nn]; *y = cur[k]; y->pt[j] = l;
                if (propagate(y)) nn++;
            }
        }
        for (int k = 0; k < nn; k++) {           /* score windows ending at or before j (all known) */
            double s = 0; for (int t = 21; t + 3 <= j; t++) s += qv(&nxt[k], t); nxt[k].s = s;
        }
        if (nn > W) { qsort(nxt, nn, sizeof(St), cmp); nn = W; }
        memcpy(cur, nxt, sizeof(St) * nn); nc = nn;
        if (!nc) break;
    }
    for (int k = 0; k < nc; k++) { double s = 0; for (int t = 21; t + 3 <= 73; t++) s += qv(&cur[k], t); cur[k].s = s / 50; }
    qsort(cur, nc, sizeof(St), cmp);
    for (int k = 0; k < nc && k < nout; k++) {
        for (int x = 0; x < 26; x++) printf("%d%c", cur[k].a[x], x == 25 ? ' ' : ',');
        for (int i = 0; i < 97; i++) putchar(cur[k].pt[i] >= 0 ? 'A' + cur[k].pt[i] : '.');
        printf(" %.3f\n", cur[k].s);
    }
    fprintf(stderr, "L=%d form=%d kr=%d W=%d final=%d best=%.3f\n", L, form, kr, W, nc, nc ? cur[0].s : -99.0);
    return 0;
}
