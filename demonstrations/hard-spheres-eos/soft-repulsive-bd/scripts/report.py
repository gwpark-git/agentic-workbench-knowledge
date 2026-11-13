"""Populate the technical report from archived calculation records."""
from pathlib import Path
import json
import subprocess
root=Path(__file__).resolve().parents[1]
a=json.loads((root/'validation/analysis.json').read_text())
r=[json.loads(x) for x in (root/'logs/resources.jsonl').read_text().splitlines()]
s=(root/'REPORT.template.md').read_text()
rows=sorted((x for x in a['summary'] if x['kind']=='main'),key=lambda x:(x['phi'],x['A']))
table='| φ | A/kBT | Πσ³/kBT ± SEM | Z ± SEM | CS Z | Difference from CS |\n|---:|---:|---:|---:|---:|---:|\n'
for x in rows:
    table+=f"| {x['phi']:.2f} | {x['A']} | {x['pressure']:.6f} ± {x['pressure_sem']:.6f} | {x['Z']:.4f} ± {x['Z_sem']:.4f} | {x['Z_CS']:.4f} | {x['percent_difference_CS']:.2f}% |\n"
s=s.replace('@@RESULT_TABLE@@',table)
table='| A/kBT | Base Δt | Half Δt | Half-step Z | Change in Z | Change / combined SEM |\n|---:|---:|---:|---:|---:|---:|\n'
for x in a['timestep']:
    table+=f"| {x['A']} | {x['base_dt']:.1g} | {x['half_dt']:.1g} | {x['half_Z']:.5f} | {x['delta_Z']:+.6f} | {x['standardized_difference']:+.3f} |\n"
s=s.replace('@@TIMESTEP_TABLE@@',table).replace('@@VIRIAL_ERROR@@',f"{a['max_absolute_virial_error']:.3g}")
rss=max(max(x['child_peak_rss_kib'],x['sampled_main_peak_rss_kib']) for x in r)
srss=max(max(x['child_peak_rss_kib'],x['sampled_main_peak_rss_kib']) for x in r if 'simulations' in x['label'])
disk=int(subprocess.check_output(['du','-s','-B1',str(root)]).split()[0])
resources=f"- Largest recorded process RSS: {rss:,} KiB ({rss*1024/1e6:.1f} MB).\n- Main/timestep simulation peak RSS: {srss:,} KiB ({srss*1024/1e6:.1f} MB).\n- Largest recorded disk snapshot: {max(x['disk_allocated_bytes'] for x in r):,} bytes.\n- Allocated directory footprint at report generation: {disk:,} bytes ({disk/1e9:.3f} GB)."
s=s.replace('@@RESOURCE_SUMMARY@@',resources)
table='| Timed phase | Measured wall time (s) |\n|---|---:|\n'
labels=[('setup','Installation'),('discovery','Initial package/source discovery'),('sources','Additional source and wheel archival'),('provenance','Additional provenance'),('smoke','Library/style load check'),('verification','Pair/diffusion verification'),('pilot','Pilot'),('main_simulations','Main simulations'),('timestep_simulations','Half-timestep simulations')]
for label,description in labels:
    table+=f"| {description} | {sum(x['seconds'] for x in r if x['label']==label):.3f} |\n"
table+=f"| Analysis and figure runs | {sum(x['seconds'] for x in r if 'analysis' in x['label'] or x['label']=='figure_revision'):.3f} |\n"
s=s.replace('@@TIME_TABLE@@',table)
assert '@@' not in s
(root/'REPORT.md').write_text(s)
print('Wrote REPORT.md')
