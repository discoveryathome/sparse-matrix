"""Strict certificates against an immutable input/frontier registry."""
from pathlib import Path
import json,hashlib,math
from model import ROOT,graph,exact_score,validate_order

def catalog(version=None):
 registry=json.loads((ROOT/'frontiers/index.json').read_text());version=version or registry['current'];assert version in registry['versions'],'Unknown frontier version';p=ROOT/'frontiers'/version/'catalog.json';assert hashlib.sha256(p.read_bytes()).hexdigest()==registry['versions'][version],'Changed catalog';return json.loads(p.read_text()),registry['versions'][version]

def check_submission(c):
 assert c['schema']=='sparse-submission/v1';cat,ch=catalog(c['frontier_version']);assert c['catalog_sha256']==ch,'Wrong catalog digest'
 matches=[x for x in cat['instances'] if x['matrix_id']==c['matrix_id']];assert len(matches)==1,'Unknown matrix';m=matches[0];ip=(ROOT/m['input']).resolve();assert ip.is_relative_to(ROOT);assert c['input_sha256']==m['input_sha256']==hashlib.sha256(ip.read_bytes()).hexdigest(),'Input mismatch';assert hashlib.sha256((ROOT/m['frontier']).read_bytes()).hexdigest()==m['frontier_sha256'],'Changed inherited order'
 assert isinstance(c['order'],list);validate_order(c['order'],m['n']);assert isinstance(c['score'],list) and len(c['score'])==3 and all(type(x) is int and x>=0 for x in c['score']),'Integer score required'
 score=exact_score(graph(ip),c['order']);assert score==c['score'],'Incorrect symbolic score';budget=c['budget'];assert type(budget['evaluations']) is int and budget['evaluations']>=0;assert type(budget['seconds']) in [int,float] and math.isfinite(budget['seconds']) and budget['seconds']>=0;assert isinstance(c['method'],str) and 0<len(c['method'])<=2000
 current,_=catalog();now=next(x for x in current['instances'] if x['matrix_id']==c['matrix_id']);better=tuple(score[:2])<tuple(m['score'][:2]);current_better=tuple(score[:2])<tuple(now['score'][:2])
 return {'verified':True,'matrix_id':m['matrix_id'],'frontier_version':cat['version'],'score':score,'inherited_score':m['score'],'improves_submitted_frontier':better,'improves_current_frontier':current_better,'primary_reduction':m['score'][0]-score[0],'claim':'Symbolic ordering result; no automatic numerical runtime or peak-memory claim'}
