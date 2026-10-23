"""Build a frozen launch frontier from every verified inherited candidate."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from model import graph,exact_score
out=ROOT/'frontiers/v001';out.mkdir(parents=True,exist_ok=False);rows=[]
for case in json.loads((ROOT/'research/round2/corpus.json').read_text()):
 a=graph(ROOT/case['input']);name=case['name'];orderfile=ROOT/'results/round2'/f'{name}-orders.json';o=json.loads(orderfile.read_text());candidates=[(k,p,str(orderfile.relative_to(ROOT))) for k,p in o.items() if k!='baseline_name']
 for p in sorted((ROOT/'results/initial').glob(f'{name}.mtx-*.json')):
  c=json.loads(p.read_text())
  if 'order' in c:candidates.append(('initial',c['order'],str(p.relative_to(ROOT))))
 scored=[(exact_score(a,p),p,label,src) for label,p,src in candidates];score,order,label,src=min(scored,key=lambda x:x[0][:2]);certificate={'input':case['input'],'input_sha256':case['sha256'],'order':order,'score':score};p=out/f'{name}.json';p.write_text(json.dumps(certificate)+'\n');rows.append({'matrix_id':name,'n':a.shape[0],'family':case['family'],'origin':'empirical' if case['family']=='historical_structural' else 'synthetic','input':case['input'],'input_sha256':case['sha256'],'frontier':str(p.relative_to(ROOT)),'frontier_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'score':score,'inherited_from':src,'ordering_source':label})
for case in json.loads((ROOT/'results/empirical/summary.json').read_text()):
 cp=ROOT/case['candidate']['certificate'];c=json.loads(cp.read_text());a=graph(ROOT/c['input']);assert exact_score(a,c['order'])==c['score'];p=out/f"{case['name']}.json";p.write_text(json.dumps(c)+'\n');rows.append({'matrix_id':case['name'],'n':a.shape[0],'family':case['family'],'origin':'empirical','input':c['input'],'input_sha256':c['input_sha256'],'frontier':str(p.relative_to(ROOT)),'frontier_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'score':c['score'],'inherited_from':case['candidate']['certificate'],'ordering_source':'empirical qualification'})
catalog={'schema':'sparse-frontier/v1','version':'v001','objective':{'primary':'symbolic Cholesky factor nonzeros including diagonal','secondary':'sum of squared elimination column lengths','diagnostic':'maximum elimination column length'},'instances':rows,'claim':'Verified inherited project frontier,not literature/global record authority'};p=out/'catalog.json';p.write_text(json.dumps(catalog,indent=2)+'\n');(ROOT/'frontiers/index.json').write_text(json.dumps({'current':'v001','versions':{'v001':hashlib.sha256(p.read_bytes()).hexdigest()}},indent=2)+'\n');print('Frozen',len(rows),'frontiers')
