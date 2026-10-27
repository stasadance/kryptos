// Grid-key annealer with exact crib handling.
// Model (q3v, one alphabet A): A[c_i] = A[p_i] + f[(i+O)/W] + g[(i+O)%W]  (mod 26)
// For a given alphabet, crib equations fix f,g up to one free value per connected component
// (union-find with potentials on row/col nodes, y_col = -g). v = #crib equations violated.
// Anneal: alphabet swaps + changes of the free value of a component.
// usage: sa2u W O CT R IT seed lam
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float *QG; int N=97,W,O,NR,NN; int ct[97],cr[97];
unsigned long long rs; double rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (rs>>11)*(1.0/9007199254740992.0);}
int ri(int n){return (int)(rnd()*n);}
int A[26],Ainv[26],par[200],pot[200],fre[200],val[200];
int find(int x){ if(par[x]==x) return x; int r=find(par[x]); pot[x]=(pot[x]+pot[par[x]])%26; par[x]=r; return r;}
int build(){ // returns violations; fills val[] for all nodes
  for(int x=0;x<NN;x++){par[x]=x;pot[x]=0;}
  int v=0;
  for(int i=0;i<N;i++) if(cr[i]>=0){
    int D=((A[ct[i]]-A[cr[i]])%26+26)%26; int a=(i+O)/W, b=NR+(i+O)%W; // x_a - y_b = D, y_b=-g
    int ra=find(a), rb=find(b);
    if(ra==rb){ if(((pot[a]-pot[b]-D)%26+26)%26) v++; }
    else { par[ra]=rb; pot[ra]=((D+pot[b]-pot[a])%26+26)%26; }
  }
  for(int x=0;x<NN;x++){int r=find(x); val[x]=(fre[r]+pot[x])%26;}
  return v;
}
void dec(int*p){ for(int i=0;i<N;i++){int k=(val[(i+O)/W]-val[NR+(i+O)%W]+52)%26; p[i]=Ainv[((A[ct[i]]-k)%26+26)%26];} }
double score(int*p){double s=0;for(int i=0;i+3<N;i++)s+=QG[((p[i]*26+p[i+1])*26+p[i+2])*26+p[i+3]];return s;}
void inv(){for(int x=0;x<26;x++)Ainv[A[x]]=x;}
int main(int argc,char**argv){
 W=atoi(argv[1]);O=atoi(argv[2]);char*C=argv[3];int R=atoi(argv[4]);long IT=atol(argv[5]);rs=strtoull(argv[6],0,10)*2654435761ULL+1234567ULL;double lam=atof(argv[7]);
 NR=(96+O)/W+1; NN=NR+W;
 const char*cs[2]={"EASTNORTHEAST","BERLINCLOCK"};int st[2]={21,63};
 for(int i=0;i<N;i++){ct[i]=C[i]-65;cr[i]=-1;} for(int c=0;c<2;c++)for(int j=0;cs[c][j];j++)cr[st[c]+j]=cs[c][j]-65;
 QG=malloc(sizeof(float)*456976);FILE*f=fopen("qg.bin","rb");if(fread(QG,4,456976,f)!=456976)return 1;fclose(f);
 int p[97],bp[97];
 for(int r=0;r<R;r++){
  if(argc>8){char*I=argv[8]; for(int x=0;x<26;x++)A[x]=I[x]-65;} else {for(int x=0;x<26;x++)A[x]=x; for(int x=25;x>0;x--){int y=ri(x+1),t=A[x];A[x]=A[y];A[y]=t;}}
  for(int x=0;x<NN;x++)fre[x]=ri(26);
  inv();int v=build();dec(p);double s=score(p),cur=s-lam*v,best=-1e9;int bv=0;
  double T0=(argc>9)?atof(argv[9]):30,T1=0.5;
  for(long it=0;it<IT;it++){
   double T=T0*pow(T1/T0,(double)it/IT);
   int mv=ri(100),a=-1,b=-1,node=-1,old=0;
   if(mv<25){node=find(ri(NN));old=fre[node];fre[node]=ri(26);}
   else{a=ri(26);b=ri(26);if(a==b)continue;int t=A[a];A[a]=A[b];A[b]=t;inv();}
   int nv=build();dec(p);double ns=score(p),nc=ns-lam*nv;
   if(nc>=cur||rnd()<exp((nc-cur)/T)){cur=nc;v=nv;if(nv==0&&ns>best){best=ns;memcpy(bp,p,sizeof p);bv=1;}}
   else{ if(node>=0)fre[node]=old; else {int t=A[a];A[a]=A[b];A[b]=t;inv();} build(); }
  }
  fprintf(stderr,"final v=%d\n",v);
  char out[98];for(int i=0;i<N;i++)out[i]=bv?65+bp[i]:'?';out[97]=0;printf("%.2f %s\n",bv?best:-9999.0,out);
 }
}
