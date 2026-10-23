from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];rows=json.loads((ROOT/'results/round2/summary.json').read_text());values=[100*(1-x['candidate_score'][0]/x['baseline_score'][0]) for x in rows]
fig,ax=plt.subplots(figsize=(12,6));ax.bar([x['name'] for x in rows],values,color=['#db8b35' if x['split']=='heldout' else '#267a99' for x in rows]);ax.tick_params(axis='x',labelrotation=65,labelsize=8);ax.set_ylabel('Reduction in symbolic factor nonzeros (%)');ax.set_title('Sparse ordering: 20 / 24 structural gains, including 8 / 9 held-out cases');ax.spines[['top','right']].set_visible(False);fig.text(.1,.015,'Orange: held-out inputs. Corpus: 8 historical structural matrices + 16 synthetic. Broad runtime improvement not established.',fontsize=9);fig.tight_layout(rect=[0,.04,1,1]);fig.savefig(ROOT/'visuals/round2.png',dpi=150);fig.savefig(ROOT/'visuals/round2.svg')
