#include <cholmod.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9;}
int bench(int n,int nz,int32_t *ap,int32_t *ai,double *ax,int32_t *perm,int reps,double *out,double *solution){
 cholmod_common c;cholmod_start(&c);c.print=0;c.nmethods=1;c.method[0].ordering=CHOLMOD_GIVEN;c.postorder=0;c.supernodal=CHOLMOD_SIMPLICIAL;c.final_ll=1;
 cholmod_sparse *a=cholmod_allocate_sparse(n,n,nz,1,1,1,CHOLMOD_REAL,&c);memcpy(a->p,ap,(n+1)*sizeof(int32_t));memcpy(a->i,ai,nz*sizeof(int32_t));memcpy(a->x,ax,nz*sizeof(double));
 double t=now();cholmod_factor *l=cholmod_analyze_p(a,perm,NULL,0,&c);out[0]=now()-t;
 if(!l){cholmod_free_sparse(&a,&c);cholmod_finish(&c);return 1;}
 out[3]=c.lnz;
 if(!cholmod_factorize(a,l,&c)||l->minor!=(size_t)n){cholmod_free_factor(&l,&c);cholmod_free_sparse(&a,&c);cholmod_finish(&c);return 2;}
 t=now();for(int k=0;k<reps;k++)if(!cholmod_factorize(a,l,&c))return 3;out[1]=(now()-t)/reps;
 cholmod_dense *b=cholmod_ones(n,1,CHOLMOD_REAL,&c);t=now();cholmod_dense *x=NULL;
 for(int k=0;k<reps;k++){if(x)cholmod_free_dense(&x,&c);x=cholmod_solve(CHOLMOD_A,l,b,&c);if(!x)return 4;}out[2]=(now()-t)/reps;memcpy(solution,x->x,n*sizeof(double));out[4]=(double)c.memory_usage;
 cholmod_free_dense(&x,&c);cholmod_free_dense(&b,&c);cholmod_free_factor(&l,&c);cholmod_free_sparse(&a,&c);cholmod_finish(&c);return 0;
}
