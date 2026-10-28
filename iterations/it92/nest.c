// it92: nested search for periodic Quagmire IV. Outer SA over (b = B values of cipher letters, s = shifts);
// u_i = b[C_i] - s[i mod p]; plaintext = monoalphabetic substitution of u. Cribs pin A(P_k) = u_k (violations of
// equal/distinct structure penalised); inner = greedy hill-climb over the free plaintext letters' A values (warm start).
// usage: nest p CT R OUTER seed lam -> "best viol decrypt"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/mman.h>
#include <fcntl.h>
static float*LMT; int ORD=6; long PW; int N=97,P,ct[97],crib[97];
unsigned long long rs; double rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (rs>>11)*(1.0/9007199254740992.0);}
int ri(int n){return (int)(rnd()*n);}
double lmscore(int*p){double s=0;long c=0;for(int i=0;i<N;i++){c=(c%PW)*26+p[i]; if(i>=ORD-1)s+=LMT[c];}return s;}
int b[26], s[64], u[97], Ai[26];   // Ai: value -> plaintext letter
int pinned[26];                    // pinned[letter]=1 if crib plaintext letter
int pt[97];
// build Ai from cribs (pins) + warm-start free assignment; returns violations
int pin(int*Aw){ // Aw: previous Ai (value->letter) used to order free letters
  int val_of[26]; for(int x=0;x<26;x++) val_of[x]=-1; int usedv[26]={0}, v=0;
  for(int i=0;i<N;i++) if(crib[i]>=0){ int L=crib[i], uv=u[i];
     if(val_of[L]<0){ if(usedv[uv]){ v++; continue; } val_of[L]=uv; usedv[uv]=1; } else if(val_of[L]!=uv) v++; }
  // free letters: keep previous values when still free, else take leftover values
  int newAi[26]; for(int x=0;x<26;x++) newAi[x]=-1;
  for(int L=0;L<26;L++) if(val_of[L]>=0) newAi[val_of[L]]=L;
  int prevval[26]; for(int x=0;x<26;x++) prevval[Aw[x]]=x;
  int pend[26],np=0;
  for(int L=0;L<26;L++) if(val_of[L]<0){ int pv=prevval[L]; if(newAi[pv]<0) newAi[pv]=L; else pend[np++]=L; }
  int q=0; for(int x=0;x<26;x++) if(newAi[x]<0) newAi[x]=pend[q++];
  memcpy(Ai,newAi,sizeof Ai); return v;
}
void decode(){ for(int i=0;i<N;i++) pt[i]=Ai[u[i]]; }
double inner(){ // greedy over swaps of values between free letters
  int fv[26],nf=0; for(int x=0;x<26;x++) if(!pinned[Ai[x]]) fv[nf++]=x;
  decode(); double cur=lmscore(pt); int imp=1;
  while(imp){ imp=0;
    for(int a=0;a<nf;a++) for(int c=a+1;c<nf;c++){ int x=fv[a],y=fv[c],t=Ai[x]; Ai[x]=Ai[y]; Ai[y]=t; decode(); double ns=lmscore(pt);
      if(ns>cur+1e-9){ cur=ns; imp=1; } else { t=Ai[x]; Ai[x]=Ai[y]; Ai[y]=t; } } }
  decode(); return cur;
}
int main(int argc,char**argv){
 P=atoi(argv[1]); char*C=argv[2]; int R=atoi(argv[3]); long OUT=atol(argv[4]); rs=strtoull(argv[5],0,10)*2654435761ULL+11; double lam=atof(argv[6]);
 char*lm=getenv("LM")?getenv("LM"):"/tmp/claude-0/lm/ng6.bin"; ORD=getenv("ORD")?atoi(getenv("ORD")):6; PW=1; for(int j=0;j<ORD-1;j++)PW*=26;
 int fd=open(lm,O_RDONLY); LMT=mmap(0,4*PW*26,PROT_READ,MAP_SHARED,fd,0);
 for(int i=0;i<N;i++){ct[i]=C[i]-65;crib[i]=-1;}
 const char*e="EASTNORTHEAST",*bb="BERLINCLOCK"; for(int j=0;e[j];j++)crib[21+j]=e[j]-65; for(int j=0;bb[j];j++)crib[63+j]=bb[j]-65;
 for(int i=0;i<N;i++) if(crib[i]>=0) pinned[crib[i]]=1;
 double gbest=-1e18; int gpt[97], gv=99;
 for(int r=0;r<R;r++){
  for(int x=0;x<26;x++) b[x]=x; for(int x=25;x>0;x--){int y=ri(x+1),t=b[x];b[x]=b[y];b[y]=t;}
  for(int j=0;j<P;j++) s[j]=ri(26); s[0]=0;              // gauge: s0 = 0
  int Aw[26]; for(int x=0;x<26;x++) Aw[x]=x;
  for(int i=0;i<N;i++) u[i]=(b[ct[i]]-s[i%P]+52)%26;
  int v=pin(Aw); double sc=inner(), cur=sc-lam*v; memcpy(Aw,Ai,sizeof Ai);
  double T0=getenv("T0")?atof(getenv("T0")):8, T1=0.3;
  for(long it=0;it<OUT;it++){
   double T=T0*pow(T1/T0,(double)it/OUT);
   int sb[26], ss[64]; memcpy(sb,b,sizeof b); memcpy(ss,s,sizeof(int)*P);
   int mv=ri(100);
   if(mv<55){ int x=ri(26),y=ri(26); if(x==y) continue; int t=b[x];b[x]=b[y];b[y]=t; }
   else { int j=1+ri(P-1>0?P-1:1); if(P==1) j=0; s[j]=ri(26); if(P==1) s[0]=0; }
   for(int i=0;i<N;i++) u[i]=(b[ct[i]]-s[i%P]+52)%26;
   int nv=pin(Aw); double ns=inner(), nc=ns-lam*nv;
   if(nc>=cur || rnd()<exp((nc-cur)/T)){ cur=nc; memcpy(Aw,Ai,sizeof Ai); if(nv==0 && ns>gbest){ gbest=ns; gv=0; memcpy(gpt,pt,sizeof pt);} }
   else { memcpy(b,sb,sizeof b); memcpy(s,ss,sizeof(int)*P); }
  }
 }
 char o[98]; for(int i=0;i<N;i++) o[i]=gv?'?':65+gpt[i]; o[97]=0; printf("%.2f %d %s\n",gv?-9999.0:gbest,gv,o);
}
