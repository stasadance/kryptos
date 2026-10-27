// identifiability SA: P_i = A^-1((B(C_i) - k_i) mod 26); NALPH=1 => A==B ; key known stream or periodic unknown (per>0)
// usage: sa NALPH PER CT KEYSTR(26-ary letters or '-') R IT seed lam
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float *QG; int N=97, NA, PER; int ct[97], key[97], ccrib[97]; // ccrib: -1 or plaintext idx
unsigned long long rs; double rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (rs>>11)*(1.0/9007199254740992.0);}
int ri(int n){return (int)(rnd()*n);}
int A[26],B[26],Ainv[26],sh[97];
void dec(int*p){for(int i=0;i<N;i++){int k=PER?sh[i%PER]:key[i];p[i]=Ainv[((B[ct[i]]-k)%26+26)%26];}}
double score(int*p,int*viol){double s=0;for(int i=0;i+3<N;i++)s+=QG[((p[i]*26+p[i+1])*26+p[i+2])*26+p[i+3]];int v=0;for(int i=0;i<N;i++)if(ccrib[i]>=0&&p[i]!=ccrib[i])v++;*viol=v;return s;}
void sync(){ if(NA==1) for(int x=0;x<26;x++)B[x]=-1; for(int x=0;x<26;x++)Ainv[A[x]]=x; if(NA==1)for(int x=0;x<26;x++)B[x]=A[x];}
int main(int argc,char**argv){
 NA=atoi(argv[1]);PER=atoi(argv[2]);char*C=argv[3];char*K=argv[4];int R=atoi(argv[5]);long IT=atol(argv[6]);rs=strtoull(argv[7],0,10)*2654435761ULL+1234567ULL;double lam=atof(argv[8]);
 const char*cr[2]={"EASTNORTHEAST","BERLINCLOCK"};int cs[2]={21,63};
 for(int i=0;i<N;i++){ct[i]=C[i]-65;ccrib[i]=-1;key[i]=(K[0]=='-')?0:K[i]-65;}
 for(int c=0;c<2;c++)for(int j=0;cr[c][j];j++)ccrib[cs[c]+j]=cr[c][j]-65;
 QG=malloc(sizeof(float)*456976);FILE*f=fopen("qg.bin","rb");fread(QG,4,456976,f);fclose(f);
 int p[97];
 for(int r=0;r<R;r++){
  for(int x=0;x<26;x++){A[x]=x;B[x]=x;} for(int x=25;x>0;x--){int y=ri(x+1),t=A[x];A[x]=A[y];A[y]=t; y=ri(x+1);t=B[x];B[x]=B[y];B[y]=t;}
  for(int j=0;j<PER;j++)sh[j]=ri(26);
  sync();dec(p);int v;double s=score(p,&v),cur=s-lam*v;double best=-1e9;int bv=0;int bp[97];
  double T0=30,T1=0.5;
  for(long it=0;it<IT;it++){
   double T=T0*pow(T1/T0,(double)it/IT);
   int mv=ri(100);int sa1=-1,sa2=-1,which=0,oldsh=0,j=0;
   if(PER&&mv<30){j=ri(PER);oldsh=sh[j];sh[j]=ri(26);which=2;}
   else{which=(NA==2&&ri(2))?1:0;sa1=ri(26);sa2=ri(26);if(sa1==sa2)continue;int*M=which?B:A;int t=M[sa1];M[sa1]=M[sa2];M[sa2]=t;}
   sync();dec(p);double ns=score(p,&v);double nc=ns-lam*v;
   if(nc>=cur||rnd()<exp((nc-cur)/T)){cur=nc; if(v==0&&ns>best){best=ns;memcpy(bp,p,sizeof p);bv=1;}}
   else{ if(which==2)sh[j]=oldsh; else {int*M=which?B:A;int t=M[sa1];M[sa1]=M[sa2];M[sa2]=t;} sync();}
  }
  char out[98];for(int i=0;i<N;i++)out[i]=bv?65+bp[i]:'?';out[97]=0;printf("%.2f %s\n",bv?best:-9999.0,out);
 }
}
