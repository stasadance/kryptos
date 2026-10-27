// it20: SA for k_i = a[i%L1] + b[i%L2] under one unknown alphabet A (Q3): Vig A(c)=A(p)+k, Beau A(c)=k-A(p)
// usage: sa2p L1 L2 MODEL(v|b) CT R IT seed lam
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float *QG; int N=97,L1,L2,BEAU; int ct[97],cr[97];
unsigned long long rs; double rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (rs>>11)*(1.0/9007199254740992.0);}
int ri(int n){return (int)(rnd()*n);}
int A[26],Ai[26],a[30],b[30];
void dec(int*p){for(int i=0;i<N;i++){int k=a[i%L1]+b[i%L2];int v=BEAU?(k-A[ct[i]]):(A[ct[i]]-k);p[i]=Ai[((v%26)+26)%26];}}
double score(int*p,int*viol){double s=0;for(int i=0;i+3<N;i++)s+=QG[((p[i]*26+p[i+1])*26+p[i+2])*26+p[i+3]];int v=0;for(int i=0;i<N;i++)if(cr[i]>=0&&p[i]!=cr[i])v++;*viol=v;return s;}
void inv(){for(int x=0;x<26;x++)Ai[A[x]]=x;}
int main(int argc,char**argv){
 L1=atoi(argv[1]);L2=atoi(argv[2]);BEAU=argv[3][0]=='b';char*C=argv[4];int R=atoi(argv[5]);long IT=atol(argv[6]);rs=strtoull(argv[7],0,10)*2654435761ULL+99991ULL;double lam=atof(argv[8]);
 const char*cw[2]={"EASTNORTHEAST","BERLINCLOCK"};int cs[2]={21,63};
 for(int i=0;i<N;i++){ct[i]=C[i]-65;cr[i]=-1;} for(int c=0;c<2;c++)for(int j=0;cw[c][j];j++)cr[cs[c]+j]=cw[c][j]-65;
 QG=malloc(sizeof(float)*456976);FILE*f=fopen("qg.bin","rb");if(!f){printf("no qg\n");return 1;}fread(QG,4,456976,f);fclose(f);
 int p[97],bp[97];
 for(int r=0;r<R;r++){
  for(int x=0;x<26;x++)A[x]=x; for(int x=25;x>0;x--){int y=ri(x+1),t=A[x];A[x]=A[y];A[y]=t;}
  for(int j=0;j<L1;j++)a[j]=ri(26); for(int j=0;j<L2;j++)b[j]=ri(26);
  inv();dec(p);int v;double s=score(p,&v),cur=s-lam*v,best=-1e9;int got=0;
  for(long it=0;it<IT;it++){
   double T=20*pow(0.4/20,(double)it/IT);int mv=ri(100),w=0,j=0,old=0,x1=0,x2=0;
   if(mv<20){j=ri(L1);old=a[j];a[j]=ri(26);w=1;} else if(mv<40){j=ri(L2);old=b[j];b[j]=ri(26);w=2;}
   else {x1=ri(26);x2=ri(26);if(x1==x2)continue;int t=A[x1];A[x1]=A[x2];A[x2]=t;inv();w=3;}
   dec(p);double ns=score(p,&v),nc=ns-lam*v;
   if(nc>=cur||rnd()<exp((nc-cur)/T)){cur=nc;if(v==0&&ns>best){best=ns;memcpy(bp,p,sizeof p);got=1;}}
   else{if(w==1)a[j]=old;else if(w==2)b[j]=old;else{int t=A[x1];A[x1]=A[x2];A[x2]=t;inv();}}
  }
  char o[98];for(int i=0;i<N;i++)o[i]=got?65+bp[i]:'?';o[97]=0;printf("%.2f %s\n",got?best:-9999.0,o);fflush(stdout);
 }
}
