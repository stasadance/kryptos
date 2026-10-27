// Annealer over the exact crib-consistent kernel (kernel.py). Cribs hold by construction.
// Penalty: alphabet collisions. usage: sak KFILE W O CT R IT seed lam
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float*QG;int N=97,W,O,NR,n,d2,d13;int ct[97];int K2[64][128],K13[64][128];int t2[64],t13[64],X[128];
unsigned long long rs;double rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (rs>>11)*(1.0/9007199254740992.0);}int ri(int m){return (int)(rnd()*m);}
void build(){for(int v=0;v<n;v++){long s=0;for(int j=0;j<d2;j++)s+=13*K2[j][v]*t2[j];for(int j=0;j<d13;j++)s+=14*K13[j][v]*t13[j];X[v]=((s%26)+26)%26;}}
double eval(int*p,int*coll){int inv[26],cnt[26]={0};for(int x=0;x<26;x++)inv[x]=0;for(int L=0;L<26;L++){cnt[X[L]]++;inv[X[L]]=L;}
 int c=0;for(int x=0;x<26;x++)if(cnt[x]>1)c+=cnt[x]-1;*coll=c;
 for(int i=0;i<N;i++){int k=X[26+(i+O)/W]+X[26+NR+(i+O)%W];p[i]=inv[((X[ct[i]]-k)%26+52)%26];}
 double s=0;for(int i=0;i+3<N;i++)s+=QG[((p[i]*26+p[i+1])*26+p[i+2])*26+p[i+3]];return s;}
int main(int argc,char**argv){FILE*f=fopen(argv[1],"r");if(fscanf(f,"%d %d %d %d",&n,&NR,&d2,&d13)!=4)return 1;
 for(int j=0;j<d2;j++)for(int v=0;v<n;v++)if(fscanf(f,"%d",&K2[j][v])!=1)return 1;for(int j=0;j<d13;j++)for(int v=0;v<n;v++)if(fscanf(f,"%d",&K13[j][v])!=1)return 1;fclose(f);
 W=atoi(argv[2]);O=atoi(argv[3]);char*C=argv[4];int R=atoi(argv[5]);long IT=atol(argv[6]);rs=strtoull(argv[7],0,10)*2654435761ULL+99;double lam=atof(argv[8]);
 for(int i=0;i<N;i++)ct[i]=C[i]-65;
 QG=malloc(4*456976);FILE*q=fopen("qg.bin","rb");if(fread(QG,4,456976,q)!=456976)return 1;fclose(q);
 int p[97],bp[97];
 for(int r=0;r<R;r++){for(int j=0;j<d2;j++)t2[j]=ri(2);for(int j=0;j<d13;j++)t13[j]=ri(13);build();int c;double s=eval(p,&c),cur=s-lam*c,best=-1e9;int bv=0;
  for(long it=0;it<IT;it++){double T=20*pow(0.3/20,(double)it/IT);int which=ri(d2+d13),old;
   if(which<d2){old=t2[which];t2[which]^=1;}else{old=t13[which-d2];t13[which-d2]=ri(13);}
   build();int nc_;double ns=eval(p,&nc_),nc=ns-lam*nc_;
   if(nc>=cur||rnd()<exp((nc-cur)/T)){cur=nc;c=nc_;if(c==0&&ns>best){best=ns;memcpy(bp,p,sizeof p);bv=1;}}
   else{if(which<d2)t2[which]=old;else t13[which-d2]=old;}}
  char out[98];for(int i=0;i<N;i++)out[i]=bv?65+bp[i]:'?';out[97]=0;printf("%.2f %s\n",bv?best:-9999.0,out);}
}
