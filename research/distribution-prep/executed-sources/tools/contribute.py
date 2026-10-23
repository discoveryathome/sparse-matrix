from pathlib import Path
import argparse,json,sys,random,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from model import graph,Fast;from submissions import catalog,check_submission
p=argparse.ArgumentParser();p.add_argument('--matrix',required=True);p.add_argument('--frontier-version');p.add_argument('--seed',type=int,default=2301);p.add_argument('--attempts',type=int,default=1024);p.add_argument('--out',required=True);args=p.parse_args();assert 1<=args.attempts<=100000;out=(ROOT/args.out).resolve();assert out.is_relative_to(ROOT);out.mkdir(parents=True,exist_ok=False)
cat,ch=catalog(args.frontier_version);row=next(x for x in cat['instances'] if x['matrix_id']==args.matrix);start=json.loads((ROOT/row['frontier']).read_text());f=Fast(graph(ROOT/row['input']));order=start['order'];best=start['score'];rng=random.Random(args.seed);trace=[];t=time.perf_counter()
for k in range(args.attempts):
 q=order.copy();i,j=sorted(rng.sample(range(len(q)),2));mode=k%3
 if mode==0:q[i],q[j]=q[j],q[i]
 elif mode==1:j=min(j,i+16);q[i:j+1]=reversed(q[i:j+1])
 else:q.insert(j,q.pop(i))
 s=f(q);accepted=tuple(s[:2])<tuple(best[:2]);trace.append({'attempt':k,'score':s,'accepted':accepted})
 if accepted:order=q;best=s
seconds=time.perf_counter()-t;c={'schema':'sparse-submission/v1','matrix_id':row['matrix_id'],'frontier_version':cat['version'],'catalog_sha256':ch,'input_sha256':row['input_sha256'],'order':order,'score':best,'budget':{'evaluations':args.attempts,'seconds':seconds},'method':'Three-move local ordering search from frozen current frontier','seed':args.seed};v=check_submission(c);(out/'candidate.json').write_text(json.dumps(c,indent=2)+'\n');(out/'trace.json').write_text(json.dumps(trace)+'\n');(out/'verification.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v))
