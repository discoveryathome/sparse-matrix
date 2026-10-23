from pathlib import Path
import json,hashlib,subprocess,sys
import numpy as np
from scipy.sparse import coo_matrix,diags,eye,kron,save_npz,csc_matrix
from scipy.spatial import cKDTree
from scipy.io import mmread
ROOT=Path(__file__).resolve().parents[1];assert not (ROOT/'research/round2/corpus.json').exists(),'Frozen corpus already exists; prepare a separate protocol for new inputs'
out=ROOT/'data/round2';out.mkdir(exist_ok=True);rows=[]
def save(name,a,family,split,source):
 a=csc_matrix(a);a.eliminate_zeros();a.sort_indices();p=out/f'{name}.npz';save_npz(p,a);g=a.copy();g.setdiag(0);g.eliminate_zeros();h=hashlib.sha256(g.indptr.tobytes()+g.indices.tobytes()).hexdigest();assert h not in [x['pattern_sha256'] for x in rows]
 rows.append({'name':name,'input':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pattern_sha256':h,'family':family,'split':split,'n':a.shape[0],'source':source})
for n in [1,2,3,4,5,6,8,9]:
 name=f'bcsstk{n:02d}';p=ROOT/'data'/f'{name}.mtx.gz'
 if not p.exists():
  u=f'https://math.nist.gov/pub/MatrixMarket2/Harwell-Boeing/bcsstruc1/{name}.mtx.gz';subprocess.run(['curl','--fail','--location','-A','Mozilla/5.0','-sS',u,'-o',str(out/f'{name}.mtx.gz')],check=True);p=out/f'{name}.mtx.gz'
 save(name,mmread(p),'historical_structural','heldout' if n==9 else 'exposed',str(p.relative_to(ROOT)))
for family in ['grid2d','grid3d','geometric','banded_random']:
 for idx in range(4):
  rng=np.random.default_rng(1297+idx);split='heldout' if idx>=2 else 'development'
  if family.startswith('grid'):
   dim=2 if family=='grid2d' else 3;m=([16,20,24,28] if dim==2 else [5,6,7,8])[idx];t=diags([-np.ones(m-1),2*np.ones(m),-np.ones(m-1)],[-1,0,1]);a=kron(t,eye(m))+kron(eye(m),t)
   if dim==3:a=kron(a,eye(m))+kron(eye(m*m),t)
   a=a+.1*eye(a.shape[0])
  else:
   n=([150,250,350,450] if family=='geometric' else [200,300,400,500])[idx];edges=set((i,i+1) for i in range(n-1))
   if family=='geometric':
    pts=rng.random((n,2));_,nn=cKDTree(pts).query(pts,k=7)
    edges.update(tuple(sorted((i,int(j)))) for i in range(n) for j in nn[i,1:])
   else:
    for i in range(n):
     for _ in range(4):
      j=int(np.clip(i+rng.integers(-25,26),0,n-1))
      if i!=j:edges.add(tuple(sorted((i,j))))
   pairs=[(i,j) for u,v in sorted(edges) for i,j in [(u,v),(v,u)]];adj=coo_matrix((np.ones(len(pairs)),np.array(pairs).T),shape=(n,n)).tocsc();a=diags(np.asarray(adj.sum(axis=1)).ravel()+.1)-adj
  save(f'{family}-{idx}',a,family,split,'Pilot-generated SPD discretization/graph Laplacian plus positive diagonal; not empirical application data')
(ROOT/'research/round2/corpus.json').write_text(json.dumps(rows,indent=2)+'\n')
(ROOT/'research/round2/protocol.json').write_text(json.dumps({'corpus':'24 unique patterns:8 historical structural matrices+16 explicitly synthetic across4 families; fixed sizes/seeds before optimization;9 heldout cases','method':'unchanged3-move local search512attempts each at seeds419,503; no tuning on new corpus','baseline':'best AMD,RCM,natural,4seed METIS portfolio; additional METIS restarts up to same local search wall budget or256calls (record cap)','numeric':'SuiteSparse CHOLMOD simplicial LL, given order,no postorder;7 interleaved batches of25numeric refactorizations and25solves; residual check; CHOLMOD tracked allocation peak not process RSS','acceptance':'exact symbolic agreement plus numericSPD/residual; report all nulls; no controlled runtime claim on shared host','stop':'fixed round, no budget extension'},indent=2)+'\n');print('prepared',len(rows))
