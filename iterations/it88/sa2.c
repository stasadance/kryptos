// it88: crib-EXACT class-C annealer. Model: B(C_i) - A(P_i) = k_i (mod 26), A,B arbitrary permutations, key k known.
// Crib equations are solved by union-find (nodes P0-25, C0-25); each crib component moves as a rigid block
// (shift d), free letters swap. Every visited state satisfies all 24 cribs.
// usage: sa2 CT KEY(letters, value=L-'A') R IT seed  -> per restart: "score decrypt" ; "INFEASIBLE" if cribs inconsistent
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float *QG; int N=97, ct[97], key[97], ccrib[97];
unsigned long long rs; double rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (rs>>11)*(1.0/9007199254740992.0);}
int ri(int n){return (int)(rnd()*n);}
int par[52], pot[52];            // val(x) = val(root) + pot[x]
int find(int x){ if(par[x]==x) return x; int r=find(par[x]); pot[x]=(pot[x]+pot[par[x]])%26; par[x]=r; return r; }
// careful: path compression above must add parent's potential BEFORE reassigning; redo iteratively
int findc(int x,int*p){ int r=x,s=0; while(par[r]!=r){ s=(s+pot[r])%26; r=par[r]; } *p=s; return r; }
int incomp[52], comp[52], ncomp, cn[52][52], csz[52], cpot[52][52];
int val[52], own[2][26];         // val of node; own[side][value] = node
void dec(int*p){ for(int i=0;i<N;i++){ int v=((val[26+ct[i]]-key[i])%26+26)%26; p[i]=own[0][v]; } }
double score(int*p){ double s=0; for(int i=0;i+3<N;i++) s+=QG[((p[i]*26+p[i+1])*26+p[i+2])*26+p[i+3]]; return s; }
int nv[52];
int main(int argc,char**argv){
 char*C=argv[1],*K=argv[2]; int R=atoi(argv[3]); long IT=atol(argv[4]); rs=strtoull(argv[5],0,10)*2654435761ULL+1234567ULL;
 const char*cr[2]={"EASTNORTHEAST","BERLINCLOCK"}; int cs[2]={21,63};
 for(int i=0;i<N;i++){ ct[i]=C[i]-65; key[i]=K[i]-65; ccrib[i]=-1; }
 for(int c=0;c<2;c++) for(int j=0;cr[c][j];j++) ccrib[cs[c]+j]=cr[c][j]-65;
 for(int x=0;x<52;x++){ par[x]=x; pot[x]=0; incomp[x]=0; }
 for(int i=0;i<N;i++) if(ccrib[i]>=0){
   int a=ccrib[i], b=26+ct[i], k=key[i]; incomp[a]=incomp[b]=1;     // val(b) - val(a) = k
   int pa,pb; int ra=findc(a,&pa), rb=findc(b,&pb);
   if(ra==rb){ if(((pb-pa-k)%26+26)%26){ puts("INFEASIBLE"); return 0; } }
   else { par[ra]=rb; pot[ra]=((pb-k-pa)%26+26)%26; }   // val(ra)=val(rb)+pb-k-pa
 }
 ncomp=0; int rootid[52]; for(int x=0;x<52;x++) rootid[x]=-1;
 for(int x=0;x<52;x++) if(incomp[x]){ int p; int r=findc(x,&p); if(rootid[r]<0){ rootid[r]=ncomp; csz[ncomp]=0; ncomp++; }
   int c=rootid[r]; comp[x]=c; cn[c][csz[c]]=x; cpot[c][csz[c]]=p; csz[c]++; }
 // within-component injectivity check (same side, same potential => collision)
 for(int c=0;c<ncomp;c++) for(int i=0;i<csz[c];i++) for(int j=i+1;j<csz[c];j++)
   if((cn[c][i]<26)==(cn[c][j]<26) && cpot[c][i]==cpot[c][j]){ puts("INFEASIBLE"); return 0; }
 QG=malloc(sizeof(float)*456976); FILE*f=fopen(getenv("QG")?getenv("QG"):"/tmp/claude-0/it27/qg.bin","rb"); fread(QG,4,456976,f); fclose(f);
 int p[97], bp[97];
 for(int r=0;r<R;r++){
  // random valid init: random root values with injectivity, then fill free letters
  int ok=0;
  for(int tr=0;tr<200000 && !ok;tr++){
   int used[2][26]; memset(used,0,sizeof used); ok=1;
   for(int c=0;c<ncomp && ok;c++){ int rv=ri(26);
     for(int i=0;i<csz[c];i++){ int x=cn[c][i], s=x>=26, v=(rv+cpot[c][i])%26; if(used[s][v]){ok=0;break;} used[s][v]=1; val[x]=v; } }
   if(!ok) continue;
   for(int s=0;s<2;s++){ int fv[26],nf=0; for(int v=0;v<26;v++) if(!used[s][v]) fv[nf++]=v;
     for(int i=nf-1;i>0;i--){ int j=ri(i+1),t=fv[i]; fv[i]=fv[j]; fv[j]=t; }
     int q=0; for(int l=0;l<26;l++){ int x=s*26+l; if(!incomp[x]) val[x]=fv[q++]; } }
  }
  if(!ok){ puts("INFEASIBLE"); return 0; }
  for(int x=0;x<52;x++) own[x>=26][val[x]]=x;
  dec(p); double cur=score(p), best=cur; memcpy(bp,p,sizeof p);
  double T0=30,T1=0.5;
  int freeL[2][26], nfree[2]={0,0}; for(int x=0;x<52;x++) if(!incomp[x]) freeL[x>=26][nfree[x>=26]++]=x;
  for(long it=0;it<IT;it++){
   double T=T0*pow(T1/T0,(double)it/IT);
   memcpy(nv,val,sizeof val); int mv=ri(100);
   if(mv<25 && ncomp>0){            // rigid shift of one component; displaced free letters take vacated values
     int c=ri(ncomp), d=1+ri(25), bad=0; int newv[2][26], isnew[2][26], vac[2][26], nvac[2]={0,0};
     memset(isnew,0,sizeof isnew);
     for(int i=0;i<csz[c];i++){ int x=cn[c][i], s=x>=26; isnew[s][(val[x]+d)%26]=1; }
     for(int i=0;i<csz[c];i++){ int x=cn[c][i], s=x>=26; if(!isnew[s][val[x]]) vac[s][nvac[s]++]=val[x]; }
     for(int i=0;i<csz[c] && !bad;i++){ int x=cn[c][i], s=x>=26, v=(val[x]+d)%26, y=own[s][v];
       if(incomp[y] && comp[y]!=c){ bad=1; break; } }
     if(bad) continue;
     int q[2]={0,0};
     for(int i=0;i<csz[c];i++){ int x=cn[c][i], s=x>=26, v=(val[x]+d)%26, y=own[s][v]; nv[x]=v;
       if(!incomp[y]) nv[y]=vac[s][q[s]++]; }
     (void)newv;
   } else {                          // swap two free letters on one side
     int s=ri(2); if(nfree[s]<2) s=1-s; if(nfree[s]<2) continue;
     int a=freeL[s][ri(nfree[s])], b=freeL[s][ri(nfree[s])]; if(a==b) continue; nv[a]=val[b]; nv[b]=val[a];
   }
   int sv[52]; memcpy(sv,val,sizeof val); memcpy(val,nv,sizeof val);
   for(int x=0;x<52;x++) own[x>=26][val[x]]=x;
   dec(p); double ns=score(p);
   if(ns>=cur || rnd()<exp((ns-cur)/T)){ cur=ns; if(ns>best){ best=ns; memcpy(bp,p,sizeof p);} }
   else { memcpy(val,sv,sizeof val); for(int x=0;x<52;x++) own[x>=26][val[x]]=x; }
  }
  char out[98]; for(int i=0;i<N;i++) out[i]=65+bp[i]; out[97]=0; printf("%.2f %s\n",best,out);
 }
}
