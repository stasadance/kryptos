// Grid-key annealer, row-optimised: anneal alphabet A (Quagmire III, beta=alpha) and column key g[W];
// each row's shift f_r is chosen optimally (crib rows: forced by cribs, mismatches penalised).
// k_i = f[(i+O)/W] + g[(i+O)%W];  A[c_i] = A[p_i] + k_i (mod 26)
// usage: sarow W O CT R IT seed lam
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float *QG; int N=97,W,O,NR; int ct[97],cr[97];
unsigned long long rs; double rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (rs>>11)*(1.0/9007199254740992.0);}
int ri(int n){return (int)(rnd()*n);}
int A[26],Ainv[26],g[64],f[64];
static inline int decl(int i,int fr){int k=fr+g[(i+O)%W];return Ainv[((A[ct[i]]-k)%26+52)%26];}
double qg4(int a,int b,int c,int d){return QG[((a*26+b)*26+c)*26+d];}
// evaluate: choose f per row, return score - lam*violations ; fill p
double eval(int*p,int*viol,double lam){
  int v=0;
  for(int r=0;r<NR;r++){
    int s=r*W-O, e=s+W; if(s<0)s=0; if(e>N)e=N;
    // crib-forced?
    int forced=-1,cnt[26]={0},nc=0;
    for(int i=s;i<e;i++) if(cr[i]>=0){int fr=((A[ct[i]]-A[cr[i]]-g[(i+O)%W])%26+52)%26;cnt[fr]++;nc++;}
    if(nc){int b=0;for(int x=1;x<26;x++)if(cnt[x]>cnt[b])b=x;forced=b;v+=nc-cnt[b];}
    if(forced>=0){f[r]=forced;}
    else{ double best=-1e18;int bf=0;
      for(int fr=0;fr<26;fr++){ int q[12];int m=0; int a0=s-3<0?0:s-3;
        // use previous row's chosen letters (already in p) for continuity
        double sc=0; for(int i=a0;i<e;i++){q[m++]= (i<s)?p[i]:decl(i,fr);} for(int j=0;j+3<m;j++)sc+=qg4(q[j],q[j+1],q[j+2],q[j+3]);
        if(sc>best){best=sc;bf=fr;} }
      f[r]=bf; }
    for(int i=s;i<e;i++)p[i]=decl(i,f[r]);
  }
  double sc=0;for(int i=0;i+3<N;i++)sc+=qg4(p[i],p[i+1],p[i+2],p[i+3]);
  *viol=v; return sc;
}
void inv(){for(int x=0;x<26;x++)Ainv[A[x]]=x;}
int main(int argc,char**argv){
 W=atoi(argv[1]);O=atoi(argv[2]);char*C=argv[3];int R=atoi(argv[4]);long IT=atol(argv[5]);rs=strtoull(argv[6],0,10)*2654435761ULL+1234567ULL;double lam=atof(argv[7]);
 NR=(96+O)/W+1;
 const char*cs[2]={"EASTNORTHEAST","BERLINCLOCK"};int st[2]={21,63};
 for(int i=0;i<N;i++){ct[i]=C[i]-65;cr[i]=-1;} for(int c=0;c<2;c++)for(int j=0;cs[c][j];j++)cr[st[c]+j]=cs[c][j]-65;
 QG=malloc(sizeof(float)*456976);FILE*fp=fopen("qg.bin","rb");if(fread(QG,4,456976,fp)!=456976)return 1;fclose(fp);
 int p[97],bp[97];
 for(int r=0;r<R;r++){
  for(int x=0;x<26;x++)A[x]=x; for(int x=25;x>0;x--){int y=ri(x+1),t=A[x];A[x]=A[y];A[y]=t;} inv();
  for(int c=0;c<W;c++)g[c]=ri(26);
  int v;double s=eval(p,&v,lam),cur=s-lam*v,best=-1e9;int bv=0;
  double T0=20,T1=0.3;
  for(long it=0;it<IT;it++){
   double T=T0*pow(T1/T0,(double)it/IT);
   int mv=ri(100),a=-1,b=-1,c=-1,old=0;
   if(mv<20){c=ri(W);old=g[c];g[c]=ri(26);}
   else{a=ri(26);b=ri(26);if(a==b)continue;int t=A[a];A[a]=A[b];A[b]=t;inv();}
   int nv;double ns=eval(p,&nv,lam),nc=ns-lam*nv;
   if(nc>=cur||rnd()<exp((nc-cur)/T)){cur=nc;v=nv;if(nv==0&&ns>best){best=ns;memcpy(bp,p,sizeof p);bv=1;}}
   else{ if(c>=0)g[c]=old; else {int t=A[a];A[a]=A[b];A[b]=t;inv();} }
  }
  char out[98];for(int i=0;i<N;i++)out[i]=bv?65+bp[i]:'?';out[97]=0;printf("%.2f %s\n",bv?best:-9999.0,out);
 }
}
