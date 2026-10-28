// it89 K5-readiness: two plaintexts in depth under the SAME key stream (class D, OTP-like/unstructured key).
// Model: B(C_t) - A(P_t) = k_i for t in {K4,K5}  =>  A(P5_i) = A(P4_i) + B(C5_i) - B(C4_i).
// NA=0: A=B=AZ (known tableau); NA=1: A=B unknown (vig1); NA=2: A,B unknown (Q4-type).
// SA state: P4 non-crib letters + alphabets; P5 derived. Cribs: P4 21-33,63-73 fixed; P5 63-73 = BERLINCLOCK (penalty lam).
// usage: depth NA C4 C5 R IT seed lam  -> per restart "score viol P4 P5"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float*QG; int N=97,NA,c4[97],c5[97],fix4[97],fix5[97];
unsigned long long rs; double rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (rs>>11)*(1.0/9007199254740992.0);}
int ri(int n){return (int)(rnd()*n);}
int A[26],Ai[26],B[26],p4[97],p5[97];
void sync(){ for(int x=0;x<26;x++)Ai[A[x]]=x; if(NA==1)memcpy(B,A,sizeof A); }
void der(){ for(int i=0;i<N;i++) p5[i]=Ai[((A[p4[i]]+B[c5[i]]-B[c4[i]])%26+26)%26]; }
double qs(int*p){double s=0;for(int i=0;i+3<N;i++)s+=QG[((p[i]*26+p[i+1])*26+p[i+2])*26+p[i+3]];return s;}
int viol(){int v=0;for(int i=0;i<N;i++)if(fix5[i]>=0&&p5[i]!=fix5[i])v++;return v;}
int main(int argc,char**argv){
 NA=atoi(argv[1]); char*C4=argv[2],*C5=argv[3]; int R=atoi(argv[4]); long IT=atol(argv[5]); rs=strtoull(argv[6],0,10)*2654435761ULL+99; double lam=atof(argv[7]);
 for(int i=0;i<N;i++){c4[i]=C4[i]-65;c5[i]=C5[i]-65;fix4[i]=fix5[i]=-1;}
 const char*e="EASTNORTHEAST",*b="BERLINCLOCK"; for(int j=0;e[j];j++)fix4[21+j]=e[j]-65; for(int j=0;b[j];j++){fix4[63+j]=b[j]-65;fix5[63+j]=b[j]-65;}
 QG=malloc(4*456976); FILE*f=fopen("/tmp/claude-0/it27/qg.bin","rb"); if(fread(QG,4,456976,f)){} fclose(f);
 int free4[97],nf=0; for(int i=0;i<N;i++) if(fix4[i]<0) free4[nf++]=i;
 for(int r=0;r<R;r++){
  for(int x=0;x<26;x++){A[x]=x;B[x]=x;}
  if(NA>=1) for(int x=25;x>0;x--){int y=ri(x+1),t=A[x];A[x]=A[y];A[y]=t;}
  if(NA==2) for(int x=25;x>0;x--){int y=ri(x+1),t=B[x];B[x]=B[y];B[y]=t;}
  sync(); for(int i=0;i<N;i++) p4[i]=fix4[i]>=0?fix4[i]:ri(26); der();
  int v=viol(); double s=qs(p4)+qs(p5), cur=s-lam*v, best=-1e9; int b4[97],b5[97],bv=99;
  double T0=20,T1=0.3;
  for(long it=0;it<IT;it++){
   double T=T0*pow(T1/T0,(double)it/IT); int mv=ri(100), kind, i=0, old=0, x=0, y=0;
   if(NA==0 || mv<70){ kind=0; i=free4[ri(nf)]; old=p4[i]; p4[i]=ri(26); if(p4[i]==old) continue; }
   else { kind=(NA==2&&ri(2))?2:1; x=ri(26); y=ri(26); if(x==y) continue; int*M=kind==2?B:A; int t=M[x];M[x]=M[y];M[y]=t; sync(); }
   der(); int nv=viol(); double ns=qs(p4)+qs(p5), nc=ns-lam*nv;
   if(nc>=cur||rnd()<exp((nc-cur)/T)){ cur=nc; if(nc>best){best=nc;bv=nv;memcpy(b4,p4,sizeof p4);memcpy(b5,p5,sizeof p5);} }
   else { if(kind==0) p4[i]=old; else { int*M=kind==2?B:A; int t=M[x];M[x]=M[y];M[y]=t; sync(); } }
  }
  char o4[98],o5[98]; for(int i=0;i<N;i++){o4[i]=65+b4[i];o5[i]=65+b5[i];} o4[97]=o5[97]=0;
  printf("%.2f %d %s %s\n",best,bv,o4,o5);
 }
}
