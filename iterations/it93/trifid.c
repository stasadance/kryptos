// it93: Trifid (27-cell cube = 26 letters + '#', arbitrary arrangement) period n, block offset o: SA over the cube,
// 6-gram LM on the decrypt, crib violations and '#' in plaintext penalised. usage: trifid n o CT R IT seed lam
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/mman.h>
#include <fcntl.h>
static float*LMT; int ORD=6; long PW; int N=97,n,o,ct[97],crib[97],bs[100],bl[100],nb;
unsigned long long rs; double rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (rs>>11)*(1.0/9007199254740992.0);}
int ri(int k){return (int)(rnd()*k);}
int cell[27], sym[27];   // cell[symbol] = 0..26 code ; sym[code] = symbol (26 = '#')
int pt[97];
void dec(){ for(int b=0;b<nb;b++){ int s=bs[b], L=bl[b], tr[300];
   for(int q=0;q<L;q++){ int c=cell[ct[s+q]]; tr[3*q]=c/9; tr[3*q+1]=(c/3)%3; tr[3*q+2]=c%3; }
   for(int q=0;q<L;q++) pt[s+q]=sym[tr[q]*9+tr[L+q]*3+tr[2*L+q]]; } }
double score(int*viol){ double s=0; long c=0; int v=0, run=0;
  for(int i=0;i<N;i++){ int x=pt[i]; if(x==26){ v++; x=4; } if(crib[i]>=0 && pt[i]!=crib[i]) v++;
    c=(c%PW)*26+x; if(i>=ORD-1) s+=LMT[c]; } (void)run; *viol=v; return s; }
int main(int argc,char**argv){
 n=atoi(argv[1]); o=atoi(argv[2]); char*C=argv[3]; int R=atoi(argv[4]); long IT=atol(argv[5]); rs=strtoull(argv[6],0,10)*2654435761ULL+5; double lam=atof(argv[7]);
 char*lm=getenv("LM")?getenv("LM"):"/tmp/claude-0/lm/ng6.bin"; ORD=getenv("ORD")?atoi(getenv("ORD")):6; PW=1; for(int j=0;j<ORD-1;j++)PW*=26;
 int fd=open(lm,O_RDONLY); LMT=mmap(0,4*PW*26,PROT_READ,MAP_SHARED,fd,0);
 for(int i=0;i<N;i++){ct[i]=C[i]-65;crib[i]=-1;}
 const char*e="EASTNORTHEAST",*b="BERLINCLOCK"; for(int j=0;e[j];j++)crib[21+j]=e[j]-65; for(int j=0;b[j];j++)crib[63+j]=b[j]-65;
 nb=0; int s0=0; if(o){ bs[nb]=0; bl[nb]=o; nb++; s0=o; } while(s0<N){ bs[nb]=s0; bl[nb]=(s0+n<=N)?n:N-s0; nb++; s0+=n; }
 double gb=-1e18; int gpt[97], gv=99;
 for(int r=0;r<R;r++){
  for(int x=0;x<27;x++) sym[x]=x; for(int x=26;x>0;x--){int y=ri(x+1),t=sym[x];sym[x]=sym[y];sym[y]=t;}
  for(int x=0;x<27;x++) cell[sym[x]]=x;
  dec(); int v; double s=score(&v), cur=s-lam*v; double T0=15,T1=0.3;
  for(long it=0;it<IT;it++){ double T=T0*pow(T1/T0,(double)it/IT);
   int a=ri(27), c2=ri(27); if(a==c2) continue; int t=sym[a];sym[a]=sym[c2];sym[c2]=t; cell[sym[a]]=a; cell[sym[c2]]=c2;
   dec(); int nv; double ns=score(&nv), nc=ns-lam*nv;
   if(nc>=cur || rnd()<exp((nc-cur)/T)){ cur=nc; if(nv==0 && ns>gb){ gb=ns; gv=0; memcpy(gpt,pt,sizeof pt);} }
   else { t=sym[a];sym[a]=sym[c2];sym[c2]=t; cell[sym[a]]=a; cell[sym[c2]]=c2; }
  }
 }
 char out[98]; for(int i=0;i<N;i++) out[i]=gv?'?':(gpt[i]==26?'#':65+gpt[i]); out[97]=0; printf("%.2f %d %s\n",gv?-9999.0:gb,gv,out);
}
