#include <stdint.h>
#include <stdlib.h>
#include <string.h>
// Symbolic elimination of an undirected graph. Order validity is checked in Python.
void score(int n, const uint64_t *input, const int *order, int64_t *out) {
 int w=(n+63)/64; uint64_t *a=malloc((size_t)n*w*8),*mask=malloc(w*8);
 memcpy(a,input,(size_t)n*w*8); int64_t nnz=0,flops=0,front=0;
 for(int step=0;step<n;step++) {int v=order[step]; memcpy(mask,a+(size_t)v*w,w*8);
  mask[v/64]&=~((uint64_t)1<<(v%64)); int k=0;
  for(int b=0;b<w;b++) k+=__builtin_popcountll(mask[b]);
  nnz+=k+1;flops+=(int64_t)(k+1)*(k+1);if(k+1>front)front=k+1;
  for(int b=0;b<w;b++){uint64_t bits=mask[b];while(bits){int j=b*64+__builtin_ctzll(bits);bits&=bits-1;
   for(int t=0;t<w;t++)a[(size_t)j*w+t]|=mask[t];
   a[(size_t)j*w+v/64]&=~((uint64_t)1<<(v%64));a[(size_t)j*w+j/64]&=~((uint64_t)1<<(j%64));}}
  memset(a+(size_t)v*w,0,w*8);
 }
 out[0]=nnz;out[1]=flops;out[2]=front;free(mask);free(a);
}
