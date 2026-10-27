import json,subprocess,sys
from multiprocessing import Pool
K4=open('/home/user/kryptos/data/ciphertext.txt').read().strip()
hits=[json.loads(l) for l in open('k4_hits.jsonl')]
two=[h for h in hits if h['hit'][0]=='two']
def job(a):
    j,h=a; s=''.join(chr(65+x%26) for x in h['k'])
    out=subprocess.run(['./sa','2','0',K4,s,'8','3000000',str(j),'25'],capture_output=True,text=True).stdout.split('\n')
    res=[(float(l.split()[0]),l.split()[1]) for l in out if l.strip()]
    b=max(res); return dict(j=j,fam=h['fam'],par=h['par'],best=b[0],dec=b[1])
with Pool(4) as P:
    for r in P.imap(job,list(enumerate(two))): print(json.dumps(r),flush=True)
