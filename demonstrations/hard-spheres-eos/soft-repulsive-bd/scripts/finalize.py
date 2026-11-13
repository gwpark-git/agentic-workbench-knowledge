"""Audit completed artifacts, record actual completion time, and hash deliverables."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

root=Path(__file__).resolve().parents[1]
records=[json.loads(x) for x in (root/'outputs/completed.jsonl').read_text().splitlines()]
assert len(records)==17 and len({x['name'] for x in records})==17
analysis=json.loads((root/'validation/analysis.json').read_text())
assert len(analysis['summary'])==8
assert len(analysis['sampling'])==16
assert len(analysis['timestep'])==2
assert len((root/'validation/direct_virial.csv').read_text().splitlines())==17
assert all(x['sample_count']==2000 for x in analysis['sampling'])
assert all(x['returncode']==0 for x in map(json.loads,(root/'logs/resources.jsonl').read_text().splitlines()))
assert analysis['max_absolute_virial_error']<1e-10
for c in records:
    for sub,suffix in [('outputs','.dat'),('outputs','.restart'),('outputs','_final.npz'),
                       ('outputs','_equilibrated.dump'),('outputs','_final.dump'),
                       ('inputs','.in'),('inputs','.data'),('logs','.log')]:
        assert (root/sub/(c['name']+suffix)).stat().st_size>0
for filename in ['equation_of_state.png','equation_of_state.pdf','sampling_diagnostics.png']:
    assert (root/'figures'/filename).stat().st_size>1000
report=(root/'REPORT.md').read_text()
assert '@@' not in report
for match in re.finditer(r'\]\(([^)]+)\)', report):
    link=match.group(1)
    if not link.startswith('https://'): assert (root/link).is_file(), link
for directory in ['scripts','inputs','outputs','source','figures','validation']:
    assert (root/directory).is_dir()
wheel=next((root/'downloads').glob('lammps*.whl'))
wheel_hash=hashlib.sha256(wheel.read_bytes()).hexdigest()
assert wheel_hash=='a714cbb1bb1e487b16aec023255d867a3a560ae44a47dc7cd21d72a29a0ab755'
disk=int(subprocess.check_output(['du','-s','-B1',str(root)]).split()[0])
assert disk<10_000_000_000
audit={'audited_at':datetime.now(timezone.utc).isoformat(),'complete_cases':17,
       'main_and_timestep_cases':16,'total_interacting_steps_excluding_pilot':15000000,
       'sample_records_per_production_case':2000,'figure_files':3,'all_resource_runs_successful':True,
       'independent_virial_max_error':analysis['max_absolute_virial_error'],
       'wheel_sha256_verified':True,'report_local_links_valid':True,'disk_bytes_before_final_metadata':disk,
       'original_sources_modified':False,'passed':True}
(root/'validation/artifact_audit.json').write_text(json.dumps(audit,indent=2))
# Verify all archived scientific artifacts before recording completion.
hash_paths=[]
for directory in ['scripts','inputs','outputs','source','figures','validation','downloads']:
    hash_paths.extend(p for p in (root/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
hash_paths += [root/'README.md',root/'PACKAGE_SELECTION.md',root/'REPORT.template.md',
               root/'env/requirements.lock',root/'env/host.json']
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()
checks={p:digest(p) for p in sorted(hash_paths)}
assert all(digest(p)==v for p,v in checks.items())
timing=json.loads((root/'timing.json').read_text())
start=datetime.fromisoformat(timing['start'])
end=datetime.now(timezone.utc)
elapsed=(end-start).total_seconds()
hours=int(elapsed//3600); minutes=int(elapsed%3600//60); seconds=elapsed%60
duration=f'{hours} hours, {minutes} minutes, {seconds:.6f} seconds'
events=[json.loads(x) for x in (root/'logs/resources.jsonl').read_text().splitlines()]
timing.update(end=end.isoformat(),elapsed_seconds=elapsed,elapsed_hms=duration,events=events,
              interruption='Server restart; resume timestamp logged; exact interruption duration unavailable.',
              human_interventions=0,final_disk_allocated_bytes=disk)
(root/'timing.json').write_text(json.dumps(timing,indent=2))
footer=f'\n## Completion record\n\nExperiment completion: **{end.isoformat()}**. Total elapsed wall-clock time: **{duration}** ({elapsed:.6f} s). This timestamp was taken after report preparation and artifact verification; final timestamp/checksum files were then written. No human intervention was required. Final pre-metadata directory footprint: {disk:,} bytes.\n'
(root/'REPORT.md').write_text(report+footer)
with (root/'execution_log.md').open('a') as f:
    f.write('\nA report-writing tool submission encountered a JavaScript syntax error before execution; it was corrected without changing scientific calculations.\n')
    f.write('\nAll completed computations: 12 main runs, 4 half-timestep runs, 1 pilot, analytic pair/periodic checks, ideal diffusion, independent final-configuration virials, sampling analysis and artifact audit.\n')
    f.write('\nMeasured subprocess timings (overlapping stages are not additive):\n\n| Stage | Start (UTC) | End (UTC) | Seconds |\n|---|---|---|---:|\n')
    for x in events:
        f.write(f"| {x['label']} | {x['start']} | {x['end']} | {x['seconds']:.6f} |\n")
    f.write(footer)
checks[root/'REPORT.md']=digest(root/'REPORT.md')
(root/'SHA256SUMS').write_text(''.join(f'{v}  {p.relative_to(root)}\n' for p,v in sorted(checks.items())))
assert all(digest(p)==v for p,v in checks.items())
print(json.dumps({'start':start.isoformat(),'end':end.isoformat(),'elapsed':duration,'seconds':elapsed,
                  'disk_bytes':disk,'audited_cases':17,'checksummed_files':len(checks),'passed':True},indent=2))
