from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
rows=[]
from model import check
for row in json.loads((ROOT/'results/initial/summary.json').read_text()):
 result=check(ROOT/row['certificate']);assert result['verified'];rows.append({'certificate':row['certificate'],'verification':result})
for row in json.loads((ROOT/'results/round2/summary.json').read_text()):
 for trial in row['trials']:
  result=check(ROOT/trial['certificate']);assert result['verified'];rows.append({'certificate':trial['certificate'],'verification':result})
print(json.dumps({'count':len(rows),'checks':rows},indent=2))
