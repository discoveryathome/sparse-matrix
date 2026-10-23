from pathlib import Path
import json,sys,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));from submissions import check_submission
p=argparse.ArgumentParser();p.add_argument('certificate');a=p.parse_args();f=Path(a.certificate);assert f.stat().st_size<=2000000,'Submission too large';print(json.dumps(check_submission(json.loads(f.read_text())),indent=2))
