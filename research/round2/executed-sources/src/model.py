from pathlib import Path
import ctypes,ctypes.util,hashlib,json
from numbers import Integral
import numpy as np
from scipy.io import mmread
from scipy.sparse import csc_matrix
ROOT=Path(__file__).resolve().parents[1]
def graph(path):
 a=csc_matrix(mmread(path));a.eliminate_zeros()
 assert a.shape[0]==a.shape[1]
 assert (a-a.T).nnz==0
 a=((a!=0)+(a.T!=0)).astype(np.int8);a.setdiag(0);a.eliminate_zeros();a.sort_indices()
 return a

def validate_order(p,n):
 assert len(p)==n and all(isinstance(v,Integral) and not isinstance(v,(bool,np.bool_)) for v in p) and sorted(p)==list(range(n)), 'Not an integer permutation'
def exact_score(a,p):
 validate_order(p,a.shape[0]);g=[set(a.getrow(i).indices.tolist())-{i} for i in range(a.shape[0])]
 nnz=flops=front=0
 for v in p:
  v=int(v);neigh=g[v].copy();k=len(neigh);nnz+=k+1;flops+=(k+1)**2;front=max(front,k+1)
  for u in neigh:g[u].update(neigh-{u});g[u].discard(v)
  g[v].clear()
 return [nnz,flops,front]
class Fast:
 def __init__(self,a):
  self.n=a.shape[0];w=(self.n+63)//64;self.bits=np.zeros((self.n,w),dtype=np.uint64)
  for i,j in zip(*a.nonzero()):self.bits[i,j//64]|=np.uint64(1)<<np.uint64(j%64)
  self.lib=ctypes.CDLL(str(ROOT/'build/fill.dylib'));self.lib.score.argtypes=[ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p];self.lib.score.restype=None
 def __call__(self,p):
  order=np.asarray(p,dtype=np.int32);out=np.zeros(3,dtype=np.int64)
  self.lib.score(self.n,self.bits.ctypes.data,order.ctypes.data,out.ctypes.data);return out.tolist()
def amd(a):
 path=ctypes.util.find_library('amd') or '/opt/homebrew/opt/suite-sparse/lib/libamd.dylib';lib=ctypes.CDLL(path)
 lib.amd_order.argtypes=[ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p];lib.amd_order.restype=ctypes.c_int
 ap=np.asarray(a.indptr,dtype=np.int32);ai=np.asarray(a.indices,dtype=np.int32);p=np.empty(a.shape[0],dtype=np.int32)
 status=lib.amd_order(a.shape[0],ap.ctypes.data,ai.ctypes.data,p.ctypes.data,None,None);assert status>=0
 return p.tolist()
def check(path):
 c=json.loads(Path(path).read_text());p=ROOT/c['input'];assert hashlib.sha256(p.read_bytes()).hexdigest()==c['input_sha256'];a=graph(p)
 score=exact_score(a,c['order']);assert score==c['score'];return {'verified':True,'n':a.shape[0],'score':score}
