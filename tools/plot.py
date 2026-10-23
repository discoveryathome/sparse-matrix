from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
rows=json.loads((ROOT/'results/initial/summary.json').read_text());names=sorted(set(x['case'] for x in rows));best=[min((x for x in rows if x['case']==n),key=lambda x:x['candidate']) for n in names];pct=[100*(x['initial'][0]-x['candidate'][0])/x['initial'][0] for x in best]
fig,ax=plt.subplots(figsize=(10,5));bars=ax.bar([n.replace('.mtx','') for n in names],pct,color='#226f91');ax.set_ylabel('Reduction in symbolic factor nonzeros (%)');ax.set_ylim(0,1.65);ax.set_title('Sparse ordering: modest verified gains against the strongest baseline')
for bar,v in zip(bars,pct):ax.text(bar.get_x()+bar.get_width()/2,v+.025,f'{v:.2f}%',ha='center')
fig.text(.12,.02,'8 inputs, 7 distinct patterns; bcsstk06 and bcsstk07 have identical sparsity. No runtime gain claimed.',fontsize=9);fig.tight_layout(rect=[0,.05,1,1])

fig.savefig(ROOT/'visuals/initial.png',dpi=150)
fig.savefig(ROOT/'visuals/initial.svg')
