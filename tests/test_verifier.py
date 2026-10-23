import sys,random
from pathlib import Path
import numpy as np,pytest
from scipy.sparse import csc_matrix
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from model import exact_score,Fast,validate_order

def test_path():
 a=np.diag(np.ones(9),1)+np.diag(np.ones(9),-1)
 assert exact_score(csc_matrix(a),range(10))==[19,37,2]
def test_clique():
 a=csc_matrix(np.ones((8,8))-np.eye(8));assert exact_score(a,range(8))==[36,204,8]
def test_native_against_set_oracle():
 rng=np.random.default_rng(42)
 for n in [2,5,13,70]:
  a=np.triu(rng.random((n,n))<.13,1);a=csc_matrix(a+a.T)
  for _ in range(5):
   p=rng.permutation(n);assert Fast(a)(p)==exact_score(a,p)
def test_duplicate_order_rejected():
 with pytest.raises(AssertionError):validate_order([0,0],2)
def test_out_of_range_order_rejected():
 with pytest.raises(AssertionError):validate_order([0,2],2)

@pytest.mark.parametrize('bad',[[0.1,1.9],[False,True],['0','1']])
def test_non_integer_order(bad):
 from model import validate_order
 with pytest.raises(AssertionError):validate_order(bad,2)
