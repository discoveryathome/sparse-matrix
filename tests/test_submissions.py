from pathlib import Path
import sys,json,copy
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from submissions import check_submission
from model import Fast
from scipy.sparse import eye
@pytest.fixture
def cert():return json.loads((ROOT/'results/donor-rehearsal/bcsstk08/candidate.json').read_text())
def test_historical_submission_is_still_verified(cert):
 v=check_submission(cert);assert v['verified'] and v['improves_submitted_frontier'];assert not v['improves_current_frontier']
@pytest.mark.parametrize('field,value',[('matrix_id','../../data'),('catalog_sha256','0'*64),('input_sha256','0'*64)])
def test_wrong_binding(cert,field,value):
 cert[field]=value
 with pytest.raises(AssertionError):check_submission(cert)
def test_score_forgery(cert):
 cert['score'][0]-=1
 with pytest.raises(AssertionError):check_submission(cert)
def test_boolean_score(cert):
 cert['score'][0]=True
 with pytest.raises(AssertionError):check_submission(cert)
def test_duplicate_permutation(cert):
 cert['order'][0]=cert['order'][1]
 with pytest.raises(AssertionError):check_submission(cert)
def test_bad_budget(cert):
 cert['budget']['seconds']=float('nan')
 with pytest.raises(AssertionError):check_submission(cert)
def test_native_rejects_unsafe_order():
 with pytest.raises(AssertionError):Fast(eye(3,format='csc'))([0,1,999])
