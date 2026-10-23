"""Render the frozen six-task rehearsal; no search or promotion."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
cases=json.loads((ROOT/'research/distribution-prep/donor-protocol.json').read_text())['cases']
a={r['matrix_id']:r['score'][0] for r in json.loads((ROOT/'frontiers/v001/catalog.json').read_text())['instances']}
b={r['matrix_id']:r['score'][0] for r in json.loads((ROOT/'frontiers/v002/catalog.json').read_text())['instances']}
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(10,5.8));fig.subplots_adjust(left=.20,right=.77,bottom=.19,top=.83)
values=[100*(a[c]-b[c])/a[c] for c in cases]
ax.barh(cases,values,color='#167a79',height=.58);ax.invert_yaxis();ax.set_xlim(0,1.9)
ax.set_xlabel('Reduction in factor nonzeros from inherited frontier (%)')
for i,c in enumerate(cases):ax.text(values[i]+.035,i,f'{values[i]:.2f}%',va='center',fontsize=10)
for i,c in enumerate(cases):ax.text(1.025,i,f'{a[c]:,} → {b[c]:,}',transform=ax.get_yaxis_transform(),va='center',fontsize=11)
fig.suptitle('Sparse ordering: another step beyond the inherited best',x=.06,ha='left',fontsize=17,fontweight='bold')
fig.text(.06,.88,'All six selected tasks improved; gains are now the v002 starting frontier.',fontsize=11)
fig.text(.06,.055,'2,048 proposals per task · Fixed seed 2301 · Exact symbolic checks\nSelected tasks, not a random success-rate estimate. No general numerical speedup claim.',fontsize=10,color='#4b5563')
for suffix in ['png','svg']:fig.savefig(ROOT/f'visuals/preparation.{suffix}',dpi=160,facecolor='white')
