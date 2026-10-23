from pathlib import Path
import sys,json,hashlib,time,random,ctypes
import numpy as np,pymetis
from scipy.io import mmread
from scipy.sparse import csc_matrix,save_npz,triu
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from model import Fast,exact_score,amd
out=ROOT/'results/empirical';out.mkdir(exist_ok=False);rows=[]
protocol={'inputs':'four new historical power-network admittance matrices; family selected before search','baseline':'AMD+4seedMETIS; exact scores; no transformed normal equations or diagonal shifts','trial':'fixed512proposal search at2seeds, inherited best baseline','validation':'exact Python symbolic scorer agrees with native; given-order CHOLMOD confirmsSPD and symboliccount; residual checks','limits':'one added empirical family,not a broad production benchmark; no numerical timing ranking in this gate'}
(ROOT/'research/distribution-prep/empirical-protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
lib=ctypes.CDLL(str(ROOT/'build/cholmod_bench.dylib'));lib.bench.argtypes=[ctypes.c_int,ctypes.c_int,*([ctypes.c_void_p]*4),ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p];lib.bench.restype=ctypes.c_int
for source in json.loads((ROOT/'research/distribution-prep/empirical-sources.json').read_text()):
 a=csc_matrix(mmread(ROOT/source['input']));a.eliminate_zeros();a.sort_indices();assert (a-a.T).nnz==0;g=(a!=0).astype(np.int8);g.setdiag(0);g.eliminate_zeros();g.sort_indices();n=a.shape[0];f=Fast(g);adj=[g.getrow(i).indices.tolist() for i in range(n)];orders={'amd':amd(g)}
 for seed in [1,17,43,79]:orders[f'metis-{seed}']=list(map(int,pymetis.nested_dissection(adjacency=adj,options=pymetis.Options(seed=seed))[0]))
 scores={k:f(p) for k,p in orders.items()};bestname=min(scores,key=lambda k:scores[k][:2]);initial=orders[bestname];s0=scores[bestname];assert s0==exact_score(g,initial)
 trials=[]
 for seed in [419,503]:
  rng=random.Random(seed);p=initial.copy();best=s0;trace=[];start=time.perf_counter()
  for k in range(512):
   q=p.copy();i,j=sorted(rng.sample(range(n),2));mode=k%3
   if mode==0:q[i],q[j]=q[j],q[i]
   elif mode==1:j=min(j,i+16);q[i:j+1]=reversed(q[i:j+1])
   else:q.insert(j,q.pop(i))
   s=f(q);accept=tuple(s[:2])<tuple(best[:2]);trace.append({'step':k,'score':s,'accepted':accept})
   if accept:p=q;best=s
  assert best==exact_score(g,p);cp=out/f"{source['name']}-{seed}.json";cp.write_text(json.dumps({'input':source['input'],'input_sha256':source['sha256'],'order':p,'score':best})+'\n');(out/f"{source['name']}-{seed}-trace.json").write_text(json.dumps(trace)+'\n');trials.append({'seed':seed,'score':best,'seconds':time.perf_counter()-start,'certificate':str(cp.relative_to(ROOT))})
 candidate=min(trials,key=lambda x:x['score'][:2]);p=json.loads((ROOT/candidate['certificate']).read_text())['order'];u=triu(a,format='csc');ap=np.array(u.indptr,np.int32);ai=np.array(u.indices,np.int32);ax=np.array(u.data,np.float64);perm=np.array(p,np.int32);v=np.zeros(5);x=np.zeros(n);rc=lib.bench(n,len(ai),ap.ctypes.data,ai.ctypes.data,ax.ctypes.data,perm.ctypes.data,3,v.ctypes.data,x.ctypes.data);assert rc==0,rc;assert int(v[3])==candidate['score'][0];error=float(np.linalg.norm(a@x-1,np.inf)/(float(abs(a).sum(axis=1).max())*np.linalg.norm(x,np.inf)+1));assert error<1e-10
 row={**source,'n':n,'baseline':s0,'baseline_method':bestname,'baselines':scores,'trials':trials,'candidate':candidate,'cholmod_symbolic_lnnz':int(v[3]),'backward_error':error};rows.append(row);(out/'summary.json').write_text(json.dumps(rows,indent=2)+'\n');print(source['name'],s0,candidate['score'],flush=True)
