"""Audit extension, verify preservation, and record actual completion."""
from datetime import datetime,timezone
import hashlib,json,re,subprocess
from pathlib import Path

root=Path(__file__).resolve().parents[1]
base=root.parent

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

before=json.loads((root/'validation/previous_files_before.json').read_text())
current={str(p.relative_to(base)):p for p in base.rglob('*')
         if p.is_file() and root not in p.parents}
missing=sorted(set(before)-set(current));added=sorted(set(current)-set(before))
changed=[]
for name,info in before.items():
    if name not in current: continue
    if current[name].stat().st_size!=info['size'] or digest(current[name])!=info['sha256']:
        changed.append(name)
preservation={'checked_at':datetime.now(timezone.utc).isoformat(),
              'files_checked':len(before),'missing':missing,'added_outside_extension':added,
              'changed':changed,'passed':not(missing or added or changed)}
(root/'validation/preservation.json').write_text(json.dumps(preservation,indent=2))
assert preservation['passed'],preservation

records=[json.loads(x) for x in (root/'outputs/completed.jsonl').read_text().splitlines()]
records=list({x['name']:x for x in records}.values())
core=[x for x in records if x['kind']!='pilot']
assert len(core)==15 and len(records)==16
assert sum(x['production_sweeps']//x['sample_spacing_sweeps'] for x in core)==90000
attempts=sum(x['N']*(x['production_sweeps']+x['equilibration_sweeps']) for x in core)
assert attempts==136224000
analysis=json.loads((root/'validation/analysis.json').read_text())
software=json.loads((root/'validation/software.json').read_text())
assert software['passed']
assert len(analysis['summary'])==5 and len(analysis['runs'])==15
assert sum(x['snapshots_checked'] for x in analysis['constraints'])==465
assert all(x['sampled_constraints_pass'] and x['final_histogram_error']==0 for x in analysis['constraints'])
assert all(x['samples']==6000 for x in analysis['runs'])
for c in records:
    assert (root/'outputs'/f"{c['name']}.npz").stat().st_size>1000
    assert (root/'inputs'/f"{c['name']}_initial.npy").is_file()
for p in (root/'scripts').glob('*.py'): compile(p.read_text(),str(p),'exec')
for p in (root/'scripts').glob('*.sh'): subprocess.run(['sh','-n',str(p)],check=True)
report=(root/'REPORT.md').read_text()
assert '@@' not in report
for match in re.finditer(r'\]\(([^)]+)\)',report):
    link=match.group(1)
    if not link.startswith('https://'): assert (root/link).is_file(),link
for name in ['comparison.png','comparison.pdf','sampling.png','estimator_checks.png']:
    assert (root/'figures'/name).stat().st_size>1000
events=[json.loads(x) for x in (root/'logs/resources.jsonl').read_text().splitlines()]
required=['environment','pilot','algorithm_verification','main_simulations','size_simulations',
          'proposal_simulations','final_analysis','final_report']
for label in required:
    assert any(x['label']==label and x['returncode']==0 for x in events),label
failures=[x for x in events if x['returncode']!=0]
assert all(x['label']=='environment_metadata' for x in failures)
assert any(x['label']=='environment_metadata_retry' and x['returncode']==0 for x in events)
workspace_disk=int(subprocess.check_output(['du','-s','-B1',str(base)]).split()[0])
extension_disk=int(subprocess.check_output(['du','-s','-B1',str(root)]).split()[0])
assert workspace_disk<10_000_000_000
audit={'audited_at':datetime.now(timezone.utc).isoformat(),'completed_production_trajectories':15,
       'production_samples':90000,'attempted_moves_including_equilibration':attempts,
       'saved_configurations_independently_checked':465,'previous_files_preserved':len(before),
       'software_tests_passed':True,'report_links_checked':True,'script_syntax_checked':True,
       'known_failed_metadata_command_and_successful_retry':True,
       'workspace_disk_allocated_bytes':workspace_disk,'extension_disk_allocated_bytes':extension_disk,
       'passed':True}
(root/'validation/artifact_audit.json').write_text(json.dumps(audit,indent=2))
paths=[]
for directory in ['scripts','inputs','outputs','validation','source','figures']:
    paths.extend(p for p in (root/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
paths += [root/'README.md',root/'REPORT.template.md',root/'env/versions.json',
          root/'env/requirements-extension.lock',root/'env/base_requirements.lock']
checks={p:digest(p) for p in sorted(paths)}
assert all(digest(p)==v for p,v in checks.items())

timing=json.loads((root/'timing.json').read_text())
start=datetime.fromisoformat(timing['start'])
end=datetime.now(timezone.utc)
seconds=(end-start).total_seconds()
duration=f'{int(seconds//3600)} hours, {int(seconds%3600//60)} minutes, {seconds%60:.6f} seconds'
timing.update(end=end.isoformat(),elapsed_seconds=seconds,elapsed_hms=duration,events=events,
              interruptions=0,human_interventions=0,workbench_capabilities_used=[],
              total_workspace_disk_bytes=workspace_disk,extension_disk_bytes=extension_disk)
(root/'timing.json').write_text(json.dumps(timing,indent=2))
footer=f'\n## Completion record\n\nCompletion: **{end.isoformat()}**. Total elapsed wall-clock time: **{duration}** ({seconds:.6f} seconds). This timestamp follows scientific calculations, report preparation, preservation and artifact checks; timestamp/checksum files were then written. All {len(before)} pre-existing files were unchanged. No human intervention or Workbench-specific capability was used. Total workspace disk footprint before final metadata: {workspace_disk:,} bytes.\n'
(root/'REPORT.md').write_text(report+footer)
with (root/'execution_log.md').open('a') as f:
    f.write('\nReused: parent Python/Matplotlib, soft data and units, copied resource/statistical patterns. Replaced: Brownian integrator, potential and force-based estimator. Added: Numba/llvmlite, feasibility-only MC, contact/virtual-compression pressure estimators and independent checks.\n')
    f.write('\nFailures/retries: discovery initially raced wrapper creation (no scientific work executed), then succeeded; standalone LICENSE URL 404, embedded CC0 notice retained; pilot relative-prefix warnings corrected with absolute interpreter paths; one documentation tool-submission syntax error before execution was corrected; environment metadata used a relative-parent path incorrectly and succeeded on retry. Analysis then gained paired covariance and rerun deduplication. Scientific trajectories were not retried or adjusted.\n')
    f.write('\nNo server interruptions, human interventions, host changes, network-policy changes, or Workbench-specific capabilities.\n')
    f.write('\n| Phase | Start | End | Wall seconds | Return code |\n|---|---|---|---:|---:|\n')
    for x in events:
        f.write(f"| {x['label']} | {x['start']} | {x['end']} | {x['seconds']:.6f} | {x['returncode']} |\n")
    f.write(footer)
checks[root/'REPORT.md']=digest(root/'REPORT.md')
(root/'SHA256SUMS').write_text(''.join(f'{v}  {p.relative_to(root)}\n' for p,v in sorted(checks.items())))
assert all(digest(p)==v for p,v in checks.items())
print(json.dumps(dict(start=start.isoformat(),end=end.isoformat(),elapsed=duration,
                     elapsed_seconds=seconds,previous_files_preserved=len(before),
                     workspace_disk_bytes=workspace_disk,extension_disk_bytes=extension_disk,
                     checksummed_files=len(checks),passed=True),indent=2))
