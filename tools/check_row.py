"""Recheck one matrix of the current frontier: its order's hash and its exact symbolic score."""
from pathlib import Path
import sys,json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from submissions import catalog;from model import check
p=argparse.ArgumentParser();p.add_argument('--matrix',required=True);a=p.parse_args()
c,_=catalog();x=next((x for x in c['instances'] if x['matrix_id']==a.matrix),None);assert x,f'{a.matrix} is not in frontier {c["version"]}'
assert hashlib.sha256((ROOT/x['frontier']).read_bytes()).hexdigest()==x['frontier_sha256'],'Changed frontier order'
v=check(ROOT/x['frontier']);assert v['score']==x['score'],'Score mismatch'
print(f"PASS {a.matrix} ({c['version']}): factor nonzeros {v['score'][0]}, squared column sum {v['score'][1]}, max column {v['score'][2]}")
