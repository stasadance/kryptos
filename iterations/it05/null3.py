import random,subprocess,json
from multiprocessing import Pool
K4=open('/home/user/kryptos/data/ciphertext.txt').read().strip()
def job(seed):
    rng=random.Random(seed)
    k=[rng.randrange(26) for _ in range(97)]
    k[65]=k[27]; k[32]=(k[23]+k[33]-k[28])%26
    s=''.join(chr(65+x) for x in k)
    out=subprocess.run(['./sa','2','0',K4,s,'8','3000000',str(seed),'25'],capture_output=True,text=True).stdout.split('\n')
    res=[(float(l.split()[0]),l.split()[1]) for l in out if l.strip()]
    b=max(res)
    return dict(seed=seed,best=b[0],feasible=sum(x[0]>-9999 for x in res),dec=b[1])
with Pool(4) as P:
    for r in P.imap(job,range(40)): print(json.dumps(r),flush=True)
