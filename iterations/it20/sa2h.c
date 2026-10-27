// it20 hybrid: anneal over alphabet A and per-component offsets; a/b values derived from the crib edges
// (a[u]+b[v]=k_i, BFS potentials), penalty = number of crib edges inconsistent with the BFS tree.
// usage: sa2h L1 L2 MODEL(v|b) CT R IT seed lam
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float *QG; int N=97,L1,L2,BEAU,NN; int ct[97],cr[97],cpos[24],nc=0;
unsigned long long rs; double rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (rs>>11)*(1.0/9007199254740992.0);}
int ri(int n){return (int)(rnd()*n);}
int A[26],Ai[26],val[64],comp[64],ncomp,off[64],root[64];
int adjn[64],adj[64][24],adje[64][24];
int ekey(int e){int i=cpos[e];int c=A[ct[i]],p=A[cr[i]];return BEAU?((c+p)%26):(((c-p)%26)+26)%26;}
int build(){ // returns violations
 int seen[64];memset(seen,0,sizeof seen);int viol=0;int q[64];
 for(int c=0;c<ncomp;c++){int r=root[c];val[r]=off[c];seen[r]=1;int h=0,t=0;q[t++]=r;
  while(h<t){int u=q[h++];for(int z=0;z<adjn[u];z++){int w=adj[u][z],e=adje[u][z];int need=((ekey(e)-val[u])%26+26)%26;
    if(!seen[w]){seen[w]=1;val[w]=need;q[t++]=w;} else if(val[w]!=need) viol++;}}}
 return viol/2;
}
void dec(int*p){for(int i=0;i<N;i++){int k=val[i%L1]+val[L1+i%L2];int v=BEAU?(k-A[ct[i]]):(A[ct[i]]-k);p[i]=Ai[((v%26)+26)%26];}}
double qs(int*p){double s=0;for(int i=0;i+3<N;i++)s+=QG[((p[i]*26+p[i+1])*26+p[i+2])*26+p[i+3]];return s;}
void inv(){for(int x=0;x<26;x++)Ai[A[x]]=x;}
int main(int argc,char**argv){
 L1=atoi(argv[1]);L2=atoi(argv[2]);BEAU=argv[3][0]=='b';char*C=argv[4];int R=atoi(argv[5]);long IT=atol(argv[6]);rs=strtoull(argv[7],0,10)*2654435761ULL+777ULL;double lam=atof(argv[8]);
 const char*cw[2]={"EASTNORTHEAST","BERLINCLOCK"};int cs[2]={21,63};NN=L1+L2;
 for(int i=0;i<N;i++){ct[i]=C[i]-65;cr[i]=-1;} for(int c=0;c<2;c++)for(int j=0;cw[c][j];j++){cr[cs[c]+j]=cw[c][j]-65;cpos[nc++]=cs[c]+j;}
 memset(adjn,0,sizeof adjn);
 for(int e=0;e<nc;e++){int u=cpos[e]%L1,v=L1+cpos[e]%L2;adj[u][adjn[u]]=v;adje[u][adjn[u]++]=e;adj[v][adjn[v]]=u;adje[v][adjn[v]++]=e;}
 // components
 for(int x=0;x<NN;x++)comp[x]=-1;ncomp=0;
 for(int x=0;x<NN;x++)if(comp[x]<0){int q[64],h=0,t=0;q[t++]=x;comp[x]=ncomp;root[ncomp]=x;while(h<t){int u=q[h++];for(int z=0;z<adjn[u];z++){int w=adj[u][z];if(comp[w]<0){comp[w]=ncomp;q[t++]=w;}}}ncomp++;}
 QG=malloc(sizeof(float)*456976);FILE*f=fopen("qg.bin","rb");if(!f)return 1;if(fread(QG,4,456976,f)!=456976)return 1;fclose(f);
 int p[97],bp[97];
 for(int r=0;r<R;r++){
  for(int x=0;x<26;x++)A[x]=x;for(int x=25;x>0;x--){int y=ri(x+1),t=A[x];A[x]=A[y];A[y]=t;}
  for(int c=0;c<ncomp;c++)off[c]=ri(26);
  inv();int v=build();dec(p);double s=qs(p),cur=s-lam*v,best=-1e9;int got=0;int minv=99;
  for(long it=0;it<IT;it++){
   double T=20*pow(0.4/20,(double)it/IT);int w,j=0,old=0,x1=0,x2=0;
   if(ncomp>1&&ri(100)<15){j=ri(ncomp);old=off[j];off[j]=ri(26);w=1;}
   else{x1=ri(26);x2=ri(26);if(x1==x2)continue;int t=A[x1];A[x1]=A[x2];A[x2]=t;inv();w=2;}
   v=build();dec(p);double ns=qs(p),ncs=ns-lam*v;
   if(ncs>=cur||rnd()<exp((ncs-cur)/T)){cur=ncs;if(v<minv)minv=v;if(v==0&&ns>best){best=ns;memcpy(bp,p,sizeof p);got=1;}}
   else{if(w==1)off[j]=old;else{int t=A[x1];A[x1]=A[x2];A[x2]=t;inv();}}
  }
  char o[98];for(int i=0;i<N;i++)o[i]=got?65+bp[i]:'?';o[97]=0;printf("%.2f %s minv=%d comps=%d\n",got?best:-9999.0,o,minv,ncomp);fflush(stdout);
 }
}
