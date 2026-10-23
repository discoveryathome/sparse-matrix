from pathlib import Path
import sys,json,random,time,ctypes,hashlib
import numpy as np,pymetis
from scipy.sparse import load_npz,triu
from scipy.sparse.csgraph import reverse_cuthill_mckee
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from model import Fast,exact_score,amd
out=ROOT/'results/round2';out.mkdir(exist_ok=False);rows=[]
lib=ctypes.CDLL(str(ROOT/'build/cholmod_bench.dylib'));lib.bench.argtypes=[ctypes.c_int,ctypes.c_int,*([ctypes.c_void_p]*4),ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p];lib.bench.restype=ctypes.c_int
def numeric(a,p):
 upper=triu(a,format='csc');ap=np.array(upper.indptr,np.int32);ai=np.array(upper.indices,np.int32);ax=np.array(upper.data,np.float64);order=np.array(p,np.int32);v=np.zeros(5);x=np.zeros(a.shape[0]);rc=lib.bench(a.shape[0],len(ai),ap.ctypes.data,ai.ctypes.data,ax.ctypes.data,order.ctypes.data,25,v.ctypes.data,x.ctypes.data);assert rc==0,rc
 err=float(np.linalg.norm(a@x-1,np.inf)/(np.linalg.norm(a.toarray(),np.inf)*np.linalg.norm(x,np.inf)+1));assert err<1e-10,err
 return {'analysis_seconds':v[0],'factor_seconds':v[1],'solve_seconds':v[2],'symbolic_lnnz':int(v[3]),'cholmod_peak_bytes':int(v[4]),'backward_error':err}
for case in json.loads((ROOT/'research/round2/corpus.json').read_text()):
 a=load_npz(ROOT/case['input']);g=(a!=0).astype(np.int8);g.setdiag(0);g.eliminate_zeros();g.sort_indices();n=a.shape[0];f=Fast(g);adj=[g.getrow(i).indices.tolist() for i in range(n)]
 orders={};baselines={}
 funcs=[('natural',lambda:list(range(n))),('rcm',lambda:reverse_cuthill_mckee(g,symmetric_mode=True).tolist()),('amd',lambda:amd(g))]+[(f'metis-{seed}',lambda seed=seed:list(map(int,pymetis.nested_dissection(adjacency=adj,options=pymetis.Options(seed=seed))[0]))) for seed in [1,17,43,79]]
 for name,fn in funcs:
  t=time.perf_counter();p=fn();elapsed=time.perf_counter()-t;s=f(p);orders[name]=p;baselines[name]={'score':s,'ordering_seconds':elapsed}
 winner=min(orders,key=lambda x:baselines[x]['score'][:2]);initial=orders[winner];s0=f(initial);assert s0==exact_score(g,initial)
 trials=[]
 for seed in [419,503]:
  rng=random.Random(seed);p=initial.copy();best=s0;trace=[];t=time.perf_counter()
  for k in range(512):
   q=p.copy();i,j=sorted(rng.sample(range(n),2));mode=k%3
   if mode==0:q[i],q[j]=q[j],q[i]
   elif mode==1:j=min(j,i+16);q[i:j+1]=reversed(q[i:j+1])
   else:q.insert(j,q.pop(i))
   s=f(q);accepted=tuple(s[:2])<tuple(best[:2]);trace.append({'attempt':k,'kind':mode,'score':s,'accepted':accepted})
   if accepted:p=q;best=s
  elapsed=time.perf_counter()-t;assert best==exact_score(g,p)
  cert={'input':case['input'],'input_sha256':case['sha256'],'order':p,'score':best};cp=out/f"{case['name']}-{seed}.json";cp.write_text(json.dumps(cert)+'\n');(out/f"{case['name']}-{seed}-trace.json").write_text(json.dumps(trace)+'\n');trials.append({'seed':seed,'score':best,'seconds':elapsed,'certificate':str(cp.relative_to(ROOT)),'order':p})
 chosen=min(trials,key=lambda x:x['score'][:2]);budget=sum(t['seconds'] for t in trials);t=time.perf_counter();restart_best=s0;restart_order=initial;restarts=[]
 for k in range(256):
  if time.perf_counter()-t>=budget:break
  p=list(map(int,pymetis.nested_dissection(adjacency=adj,options=pymetis.Options(seed=1001+k))[0]));s=f(p);restarts.append({'seed':1001+k,'score':s})
  if tuple(s[:2])<tuple(restart_best[:2]):restart_best=s;restart_order=p
 restart_elapsed=time.perf_counter()-t;assert restart_best==exact_score(g,restart_order)
 # Save all relevant orders before numerical measurements.
 (out/f"{case['name']}-orders.json").write_text(json.dumps({'baseline':initial,'candidate':chosen['order'],'restarts':restart_order,'baseline_name':winner})+'\n')
 measurements={k:[] for k in ['baseline','candidate','restarts']};rng=random.Random(291)
 for batch in range(7):
  labels=list(measurements);rng.shuffle(labels)
  for label in labels:
   p={'baseline':initial,'candidate':chosen['order'],'restarts':restart_order}[label];v=numeric(a,p);assert v['symbolic_lnnz']==f(p)[0];measurements[label].append(v)
 medians={k:{field:float(np.median([x[field] for x in vals])) for field in vals[0]} for k,vals in measurements.items()}
 savings=medians['baseline']['factor_seconds']-medians['candidate']['factor_seconds'];row={**case,'baselines':baselines,'baseline_name':winner,'baseline_score':s0,'trials':[{k:v for k,v in x.items() if k!='order'} for x in trials],'candidate_score':chosen['score'],'restart_score':restart_best,'restart_attempts':restarts,'restart_wall_seconds':restart_elapsed,'local_search_total_seconds':budget,'restart_cap_reached':len(restarts)==256,'measurements':measurements,'medians':medians,'observed_refactorization_break_even':budget/savings if savings>0 else None};rows.append(row);(out/'summary.json').write_text(json.dumps(rows,indent=2)+'\n');print(case['name'],s0[0],chosen['score'][0],restart_best[0],flush=True)
