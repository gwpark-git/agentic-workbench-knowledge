#!/usr/bin/env python3
"""Execute a command on one allowed CPU, with 4 GB address-space limit.

All children inherit limits. No cgroup/host configuration is changed.
"""
import datetime
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

root = Path(__file__).resolve().parents[1]
os.chdir(root)
os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS, (4_000_000_000, 4_000_000_000))
resource.setrlimit(resource.RLIMIT_FSIZE, (1_000_000_000, 1_000_000_000))
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
            'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[key] = '1'
for key, sub in [('TMPDIR','tmp'), ('UV_CACHE_DIR','env/uv-cache'),
                 ('MPLCONFIGDIR','env/matplotlib'), ('XDG_CACHE_HOME','env/cache')]:
    os.environ[key] = str(root / sub)
    (root / sub).mkdir(parents=True, exist_ok=True)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['PYTHONPATH'] = str(root/'env/site') + ':' + os.environ.get('PYTHONPATH','')
os.environ['NUMBA_CACHE_DIR'] = str(root/'env/numba-cache')
os.environ['NUMBA_NUM_THREADS'] = '1'
os.environ['UV_CONCURRENT_DOWNLOADS'] = '2'
os.environ['UV_CONCURRENT_BUILDS'] = '1'
os.environ['LD_LIBRARY_PATH'] = str(root/'env/venv/lib') + ':' + os.environ.get('LD_LIBRARY_PATH','')
label, *command = sys.argv[1:]
if '/' in command[0]:
    command[0] = os.path.abspath(command[0])
start = datetime.datetime.now(datetime.timezone.utc)
t0 = time.monotonic()
proc = subprocess.Popen(command)
peak_rss = 0
peak_threads = 0
while proc.poll() is None:
    # Sample the direct child via /proc; getrusage below also records child
    # peak RSS. RLIMIT_AS is per process, not an aggregate memory limit.
    try:
        status = Path(f'/proc/{proc.pid}/status').read_text().splitlines()
        values = {line.split(':')[0]:line.split(':')[1].strip() for line in status if ':' in line}
        peak_rss = max(peak_rss, int(values.get('VmRSS','0 kB').split()[0]))
        peak_threads = max(peak_threads, int(values.get('Threads','0')))
    except FileNotFoundError:
        pass
    time.sleep(0.2)
end = datetime.datetime.now(datetime.timezone.utc)
usage = resource.getrusage(resource.RUSAGE_CHILDREN)
row = {'label':label,'command':command,'start':start.isoformat(),'end':end.isoformat(),
       'seconds':time.monotonic()-t0,'returncode':proc.returncode,
       'child_peak_rss_kib':usage.ru_maxrss,'sampled_main_peak_rss_kib':peak_rss,
       'sampled_main_peak_threads':peak_threads,'cpu_affinity':sorted(os.sched_getaffinity(0)),
       'address_space_limit_bytes':4_000_000_000,
       'workspace_disk_allocated_bytes':int(subprocess.check_output(['du','-s','-B1',str(root.parent)]).split()[0]),
       'disk_allocated_bytes':int(subprocess.check_output(['du','-s','-B1',str(root)]).split()[0])}
with (root/'logs/resources.jsonl').open('a') as f:
    f.write(json.dumps(row)+'\n')
print(json.dumps(row), flush=True)
sys.exit(proc.returncode)
