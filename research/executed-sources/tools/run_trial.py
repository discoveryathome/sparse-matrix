from pathlib import Path
import sys,json,time,hashlib,random,platform
import numpy as np,pymetis
from scipy.sparse.csgraph import reverse_cuthill_mckee
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from model import graph,amd,Fast,exact_score,check
out=ROOT/'results/initial';out.mkdir(exist_ok=False);rows=[]
for ip in sorted((ROOT/'data').glob('*.mtx.gz')):
 a=graph(ip);n=a.shape[0];f=Fast(a);adj=[a.getrow(i).indices.tolist() for i in range(n)]
 start=time.perf_counter();nd=list(map(int,pymetis.nested_dissection(adjacency=adj)[0]));nd_time=time.perf_counter()-start
 baselines={};orders={}
 for name,fn in [('natural',lambda:list(range(n))),('rcm',lambda:reverse_cuthill_mckee(a,symmetric_mode=True).tolist()),('amd',lambda:amd(a)),('metis',lambda:nd)]:
  start=time.perf_counter();p=fn();elapsed=nd_time if name=='metis' else time.perf_counter()-start;s=f(p);assert s==exact_score(a,p)
  orders[name]=p;baselines[name]={'score':s,'ordering_seconds':elapsed}
 best_name=min(orders,key=lambda m:baselines[m]['score'][:2]);initial=orders[best_name];initial_score=f(initial)
 for seed in [419,503]:
  rng=random.Random(seed);p=initial.copy();best=initial_score;trace=[];start=time.perf_counter()
  for attempt in range(512):
   q=p.copy();i,j=sorted(rng.sample(range(n),2));mode=attempt%3
   if mode==0:q[i],q[j]=q[j],q[i]
   elif mode==1:j=min(j,i+16);q[i:j+1]=reversed(q[i:j+1])
   else:q.insert(j,q.pop(i))
   score=f(q);accepted=tuple(score[:2])<tuple(best[:2]);trace.append({'attempt':attempt,'kind':mode,'score':score,'accepted':accepted})
   if accepted:p=q;best=score
  elapsed=time.perf_counter()-start
  cert={'input':str(ip.relative_to(ROOT)),'input_sha256':hashlib.sha256(ip.read_bytes()).hexdigest(),'order':list(map(int,p)),'score':best}
  cp=out/f'{ip.stem}-{seed}.json';cp.write_text(json.dumps(cert)+'\n');verified=check(cp)
  (out/f'{ip.stem}-{seed}-trace.json').write_text(json.dumps(trace)+'\n')
  row={'case':ip.stem,'n':n,'seed':seed,'baselines':baselines,'inherited':best_name,'initial':initial_score,'candidate':best,'attempts':512,'seconds':elapsed,'verified':verified,'certificate':str(cp.relative_to(ROOT))};rows.append(row)
  (out/'summary.json').write_text(json.dumps(rows,indent=2)+'\n');print(ip.stem,seed,initial_score,best,flush=True)
