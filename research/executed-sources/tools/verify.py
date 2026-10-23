from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from model import check
print(json.dumps(check(sys.argv[1])))
