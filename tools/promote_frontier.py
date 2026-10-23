"""Maintainer operation: create a new immutable frontier and switch its index."""
from pathlib import Path
import json,sys,argparse,hashlib,copy,os
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from submissions import catalog,check_submission
p=argparse.ArgumentParser();p.add_argument('--version',required=True);p.add_argument('certificates',nargs='+');a=p.parse_args();assert a.version.startswith('v') and a.version[1:].isdigit();cat,_=catalog();new=copy.deepcopy(cat);new['version']=a.version;out=ROOT/'frontiers'/a.version;assert not out.exists();approved=[]
for file in a.certificates:
 c=json.loads(Path(file).read_text());v=check_submission(c);assert v['improves_current_frontier'],'Only strict current-frontier improvements may be promoted';approved.append(c)
assert len({x['matrix_id'] for x in approved})==len(approved),'One candidate per matrix per promotion';out.mkdir()
for row in new['instances']:
 match=next((x for x in approved if x['matrix_id']==row['matrix_id']),None)
 if match is not None:
  c={'input':row['input'],'input_sha256':row['input_sha256'],'order':match['order'],'score':match['score']};row['score']=match['score'];row['ordering_source']='verified contribution';row['inherited_from']='submission against '+match['frontier_version'];row['submission_sha256']=hashlib.sha256(json.dumps(match,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
 else:c=json.loads((ROOT/row['frontier']).read_text())
 dest=out/f"{row['matrix_id']}.json";dest.write_text(json.dumps(c)+'\n');row['frontier']=str(dest.relative_to(ROOT));row['frontier_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
p=out/'catalog.json';p.write_text(json.dumps(new,indent=2)+'\n');idx=json.loads((ROOT/'frontiers/index.json').read_text());idx['versions'][a.version]=hashlib.sha256(p.read_bytes()).hexdigest();idx['current']=a.version;temp=ROOT/'frontiers/index.json.tmp';temp.write_text(json.dumps(idx,indent=2)+'\n');os.replace(temp,ROOT/'frontiers/index.json');print('Promoted',len(approved),'improvements to',a.version)
