// it91 (coach N5): parallel-tempering annealer for periodic Quagmire IV (NA=2) / III (NA=1), p given.
// Model: B(C_i) - A(P_i) = sh[i mod p]. State A, sh; B repaired from cribs each step (w-anneal mode-10 projection),
// so B's crib letters are always locked to A+sh; residual crib violations (conflicting cribs) penalised by lam.
// Score: n-gram LM (env LM, ORD; default 6-gram). Replicas exchange between adjacent temperatures each sweep.
// usage: pt NA p CT NREP SWEEPS MOVES_PER_SWEEP seed lam  -> "best viol decrypt"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/mman.h>
#include <fcntl.h>
static float*LMT; int ORD=6; long PW; int N=97,NA,P,ct[97],crib[97];
unsigned long long rs; double rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (rs>>11)*(1.0/9007199254740992.0);}
int ri(int n){return (int)(rnd()*n);}
int ncl, clet[26], crep[26], npl, plet[26], prep[26], DIRB=0;  // distinct crib cipher letters, representative crib position
typedef struct { int A[26],Ai[26],B[26],Bi[26],sh[64],pt[97],viol; double sc; } St;
double lmscore(int*p){double s=0;long c=0;for(int i=0;i<N;i++){c=(c%PW)*26+p[i]; if(i>=ORD-1)s+=LMT[c];}return s;}
void repair(St*s){
  for(int x=0;x<26;x++) s->Ai[s->A[x]]=x;
  if(NA==1){ memcpy(s->B,s->A,sizeof s->A); }
  else if(DIRB){ for(int j=0;j<npl;j++){ int k=prep[j], Pl=plet[j], t=(s->B[ct[k]]-s->sh[k%P]+52)%26;
      for(int x=0;x<26;x++) s->Ai[s->A[x]]=x; int o=s->Ai[t]; if(o!=Pl){ int pa=s->A[Pl]; s->A[o]=pa; s->A[Pl]=t; } }
    for(int x=0;x<26;x++) s->Ai[s->A[x]]=x; }
  else { // pinned crib cipher letters get A(P)+sh; free cipher letters take the leftover values in the order of s->B ranks
    int used[26]={0}, pin[26]; for(int x=0;x<26;x++) pin[x]=-1;
    for(int j=0;j<ncl;j++){ int k=crep[j], t=(s->A[crib[k]]+s->sh[k%P])%26; if(!used[t]){ used[t]=1; pin[clet[j]]=t; } }
    // free letters (non-crib cipher letters + pinned letters that collided) ordered by their current B value (rank key)
    int fl[26], nf=0; for(int x=0;x<26;x++) if(pin[x]<0) fl[nf++]=x;
    for(int a=1;a<nf;a++){ int y=fl[a], b2=a-1; while(b2>=0 && s->B[fl[b2]]>s->B[y]){ fl[b2+1]=fl[b2]; b2--; } fl[b2+1]=y; }
    int q=0; for(int v=0;v<26;v++) if(!used[v]){ s->B[fl[q++]]=v+100; }
    for(int x=0;x<26;x++){ if(pin[x]>=0) s->B[x]=pin[x]; else s->B[x]-=100; }
  }
  for(int x=0;x<26;x++) s->Bi[s->B[x]]=x;
  int v=0; for(int i=0;i<N;i++) if(crib[i]>=0 && (s->B[ct[i]]-s->A[crib[i]]-s->sh[i%P]+52)%26) v++;
  s->viol=v;
  for(int i=0;i<N;i++) s->pt[i]=s->Ai[(s->B[ct[i]]-s->sh[i%P]+52)%26];
  s->sc=lmscore(s->pt);
}
int main(int argc,char**argv){
 NA=atoi(argv[1]); P=atoi(argv[2]); char*C=argv[3]; int R=atoi(argv[4]); long SW=atol(argv[5]); int MV=atoi(argv[6]);
 rs=strtoull(argv[7],0,10)*2654435761ULL+7; double lam=atof(argv[8]);
 char*lm=getenv("LM")?getenv("LM"):"/tmp/claude-0/lm/ng6.bin"; ORD=getenv("ORD")?atoi(getenv("ORD")):6; PW=1; for(int j=0;j<ORD-1;j++)PW*=26;
 int fd=open(lm,O_RDONLY); LMT=mmap(0,4*PW*26,PROT_READ,MAP_SHARED,fd,0);
 for(int i=0;i<N;i++){ct[i]=C[i]-65;crib[i]=-1;}
 const char*e="EASTNORTHEAST",*b="BERLINCLOCK"; for(int j=0;e[j];j++)crib[21+j]=e[j]-65; for(int j=0;b[j];j++)crib[63+j]=b[j]-65;
 int seen[26]={0}; ncl=0; for(int i=0;i<N;i++) if(crib[i]>=0 && !seen[ct[i]]){ seen[ct[i]]=1; clet[ncl]=ct[i]; crep[ncl]=i; ncl++; }
 int freeB[26],nfB=0; for(int x=0;x<26;x++) if(!seen[x]) freeB[nfB++]=x;
 DIRB=getenv("DIRB")?atoi(getenv("DIRB")):0; int seenp[26]={0}; npl=0; for(int i=0;i<N;i++) if(crib[i]>=0 && !seenp[crib[i]]){ seenp[crib[i]]=1; plet[npl]=crib[i]; prep[npl]=i; npl++; }
 int freeA[26],nfA=0; for(int x=0;x<26;x++) if(!seenp[x]) freeA[nfA++]=x;
 St*S=malloc(sizeof(St)*R); double*T=malloc(sizeof(double)*R);
 double Tlo=getenv("TLO")?atof(getenv("TLO")):0.4, Thi=getenv("THI")?atof(getenv("THI")):12;
 for(int r=0;r<R;r++){ T[r]=Tlo*pow(Thi/Tlo,(double)r/(R-1));
   for(int x=0;x<26;x++){S[r].A[x]=x;S[r].B[x]=x;} for(int x=25;x>0;x--){int y=ri(x+1),t=S[r].A[x];S[r].A[x]=S[r].A[y];S[r].A[y]=t; y=ri(x+1);t=S[r].B[x];S[r].B[x]=S[r].B[y];S[r].B[y]=t;}
   for(int j=0;j<P;j++) S[r].sh[j]=ri(26); repair(&S[r]); }
 double best=-1e18; int bv=99, bp[97]; St tmp;
 for(long sw=0;sw<SW;sw++){
  for(int r=0;r<R;r++){ St*s=&S[r];
   for(int m=0;m<MV;m++){
    tmp=*s; int mv=ri(100);
    if(getenv("GIBBS") && mv>=40 && mv<70){ // heat-bath over one shift value
      int j=ri(P); double w[26], mx=-1e18; St c[26];
      for(int v=0;v<26;v++){ c[v]=*s; c[v].sh[j]=v; repair(&c[v]); w[v]=c[v].sc-lam*c[v].viol; if(w[v]>mx) mx=w[v]; }
      double z=0; for(int v=0;v<26;v++){ w[v]=exp((w[v]-mx)/T[r]); z+=w[v]; }
      double u=rnd()*z; int v=0; while(v<25 && (u-=w[v])>0) v++;
      *s=c[v]; if(s->viol==0 && s->sc>best){best=s->sc;bv=0;memcpy(bp,s->pt,sizeof bp);} continue; }
    if(DIRB && NA==2){ if(mv<40){ int x=ri(26),y=ri(26); if(x==y) continue; int t=tmp.B[x];tmp.B[x]=tmp.B[y];tmp.B[y]=t; }
      else if(mv<70){ tmp.sh[ri(P)]=ri(26); } else { int x=freeA[ri(nfA)],y=freeA[ri(nfA)]; if(x==y) continue; int t=tmp.A[x];tmp.A[x]=tmp.A[y];tmp.A[y]=t; } }
    else if(mv<40){ int x=ri(26),y=ri(26); if(x==y) continue; int t=tmp.A[x];tmp.A[x]=tmp.A[y];tmp.A[y]=t; }
    else if(mv<70){ tmp.sh[ri(P)]=ri(26); }
    else if(NA==2 && nfB>=2){ int x=freeB[ri(nfB)],y=freeB[ri(nfB)]; if(x==y) continue; int t=tmp.B[x];tmp.B[x]=tmp.B[y];tmp.B[y]=t; }
    else { int x=ri(26),y=ri(26); if(x==y) continue; int t=tmp.A[x];tmp.A[x]=tmp.A[y];tmp.A[y]=t; int j=ri(P); tmp.sh[j]=(tmp.sh[j]+ri(25)+1)%26; }
    repair(&tmp);
    double cn=tmp.sc-lam*tmp.viol, co=s->sc-lam*s->viol;
    if(cn>=co || rnd()<exp((cn-co)/T[r])){ *s=tmp; if(s->viol==0 && s->sc>best){best=s->sc;bv=0;memcpy(bp,s->pt,sizeof bp);} }
   } }
  for(int r=0;r+1<R;r++){ double a=S[r].sc-lam*S[r].viol, c2=S[r+1].sc-lam*S[r+1].viol;
    double d=(c2-a)*(1/T[r]-1/T[r+1]); if(d>=0 || rnd()<exp(d)){ tmp=S[r]; S[r]=S[r+1]; S[r+1]=tmp; } }
 }
 char o[98]; for(int i=0;i<N;i++) o[i]=bv?'?':65+bp[i]; o[97]=0; printf("%.2f %d %s\n",bv?-9999.0:best,bv,o);
}
