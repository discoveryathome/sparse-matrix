from pathlib import Path
import ctypes
import numpy as np
from scipy.sparse import csc_matrix,triu
ROOT=Path(__file__).resolve().parents[1]
def call(a,p):
 lib=ctypes.CDLL(str(ROOT/'build/cholmod_bench.dylib'));lib.bench.argtypes=[ctypes.c_int,ctypes.c_int,*([ctypes.c_void_p]*4),ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p];lib.bench.restype=ctypes.c_int
 u=triu(csc_matrix(a),format='csc');ap=np.array(u.indptr,np.int32);ai=np.array(u.indices,np.int32);ax=np.array(u.data,np.float64);order=np.array(p,np.int32);out=np.zeros(5);x=np.zeros(len(p));code=lib.bench(len(p),len(ai),ap.ctypes.data,ai.ctypes.data,ax.ctypes.data,order.ctypes.data,2,out.ctypes.data,x.ctypes.data);return code,out,x

def test_numeric_solution_and_symbolic_count():
 a=np.diag([4.,4.,4.,4.])+np.diag([-1.,-1.,-1.],1)+np.diag([-1.,-1.,-1.],-1)
 code,out,x=call(a,[0,1,2,3]);assert code==0;assert out[3]==7;assert np.allclose(x,np.linalg.solve(a,np.ones(4)),rtol=1e-12)
def test_non_spd_rejected():
 code,_,_=call(np.diag([1.,-1.]),[0,1]);assert code==2
