from pathlib import Path
import json,subprocess
root=Path(__file__).resolve().parents[1]
a=json.loads((root/'validation/analysis.json').read_text())
resources=[json.loads(x) for x in (root/'logs/resources.jsonl').read_text().splitlines()]
s=(root/'REPORT.template.md').read_text()
table='| φ | N | Hard-sphere Z ± SEM | Πσ³/kBT ± SEM | CS Z |\n|---:|---:|---:|---:|---:|\n'
main=[x for x in a['summary'] if x['kind']=='main']
for x in main:
    table+=f"| {x['phi']:.2f} | {x['N']} | {x['Z']:.5f} ± {x['Z_SEM']:.5f} | {x['pressure']:.6f} ± {x['pressure_SEM']:.6f} | {x['Z_CS']:.5f} |\n"
s=s.replace('@@RESULTS@@',table)
table='| φ | Contact Z ± SEM | Virtual-compression Z ± SEM | Difference / paired SEM |\n|---:|---:|---:|---:|\n'
for x in main:
    table+=f"| {x['phi']:.2f} | {x['Z']:.4f} ± {x['Z_SEM']:.4f} | {x['compression_Z']:.4f} ± {x['compression_SEM']:.4f} | {x['contact_minus_compression']/x['contact_minus_compression_SEM']:.2f} |\n"
s=s.replace('@@COMPRESSION@@',table)
table='| Check | Comparison Z | Change from N=216 main Z | Combined SEM |\n|---|---:|---:|---:|\n'
for x in a['sensitivity']:
    table+=f"| {x['check']} (N={x['comparison_N']}) | {x['comparison_Z']:.5f} | {x['delta_Z']:+.5f} | {x['combined_SEM']:.5f} |\n"
s=s.replace('@@SENSITIVITY@@',table)
rss=max(max(x['child_peak_rss_kib'],x['sampled_main_peak_rss_kib']) for x in resources)
sim=max(max(x['child_peak_rss_kib'],x['sampled_main_peak_rss_kib']) for x in resources if 'simulations' in x['label'])
disk=int(subprocess.check_output(['du','-s','-B1',str(root.parent)]).split()[0])
extension=int(subprocess.check_output(['du','-s','-B1',str(root)]).split()[0])
s=s.replace('@@RESOURCES@@',f'- One CPU, one simulation worker, no parallel Numba kernels or MPI ranks.\n- Largest recorded process RSS: {rss:,} KiB ({rss*1024/1e6:.1f} MB).\n- Production simulation peak RSS: {sim:,} KiB ({sim*1024/1e6:.1f} MB).\n- Total test_local/ workspace footprint at report generation: {disk:,} bytes ({disk/1e9:.3f} GB).\n- Extension footprint: {extension:,} bytes ({extension/1e9:.3f} GB).')
table='| Phase | Measured wall seconds |\n|---|---:|\n'
for label in ['environment','discovery_retry','pilot','algorithm_verification','main_simulations','size_simulations','proposal_simulations','analysis','paired_estimator_analysis']:
    table+=f"| {label} | {sum(x['seconds'] for x in resources if x['label']==label):.3f} |\n"
s=s.replace('@@PHASES@@',table)
assert '@@' not in s
(root/'REPORT.md').write_text(s)
print('Report generated')
