from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from submissions import catalog;from model import check
c,h=catalog();rows=[]
for x in c['instances']:
 assert hashlib.sha256((ROOT/x['frontier']).read_bytes()).hexdigest()==x['frontier_sha256'];v=check(ROOT/x['frontier']);assert v['score']==x['score'];rows.append({'matrix_id':x['matrix_id'],**v})
print(json.dumps({'verified':True,'version':c['version'],'catalog_sha256':h,'instances':len(rows),'checks':rows},indent=2))
