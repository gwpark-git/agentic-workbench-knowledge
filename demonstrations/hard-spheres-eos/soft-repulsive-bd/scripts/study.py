"""Generate and execute a serial LAMMPS Brownian EOS study."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import numpy as np
from lammps import lammps

ROOT = Path(__file__).resolve().parents[1]

def stamp():
    return datetime.now(timezone.utc).isoformat()

def configuration(phi, amplitude, dt, seed, name, eq=5., production=20., nside=6):
    n = nside**3
    density = 6*phi/np.pi
    box = (n/density)**(1/3)
    interval = round(.01/dt)
    nequil, nprod = round(eq/dt), round(production/dt)
    data = ROOT/'inputs'/f'{name}.data'
    coords = (np.indices((nside,)*3).reshape(3,-1).T+.5)*(box/nside)
    with data.open('w') as f:
        f.write(f'Initial simple cubic configuration\n\n{n} atoms\n1 atom types\n\n0 {box:.16g} xlo xhi\n0 {box:.16g} ylo yhi\n0 {box:.16g} zlo zhi\n\nMasses\n\n1 1\n\nAtoms # atomic\n\n')
        for i, xyz in enumerate(coords,1):
            f.write(f'{i} 1 '+' '.join(f'{x:.16g}' for x in xyz)+'\n')
    text = f'''units lj
dimension 3
boundary p p p
atom_style atomic
read_data inputs/{name}.data
pair_style soft 1.0
pair_coeff * * {amplitude} 1.0
neighbor 0.3 bin
neigh_modify every 1 delay 0 check yes
timestep {dt}
fix bd all brownian 1.0 {seed} gamma_t 1.0 rng gaussian
compute pv all pressure NULL pair
compute displacement all msd
variable osm equal {density:.16g}+c_pv
variable ep equal pe/atoms
fix samples all ave/time {interval} 1 {interval} c_pv v_osm v_ep c_displacement[4] file outputs/{name}.dat
thermo_style custom step c_pv v_osm pe c_displacement[4]
thermo_modify norm no
thermo {max(interval,round(1/dt))}
run {nequil}
write_dump all custom outputs/{name}_equilibrated.dump id type x y z modify sort id
run {nprod}
write_dump all custom outputs/{name}_final.dump id type x y z modify sort id
write_restart outputs/{name}.restart
'''
    (ROOT/'inputs'/f'{name}.in').write_text(text)
    return dict(name=name,phi=phi,A=amplitude,dt=dt,seed=seed,N=n,L=box,rho=density,
                equilibration_time=eq,production_time=production,sample_interval=.01,
                equilibration_steps=nequil,production_steps=nprod)

def run_case(case):
    name=case['name']; start=stamp(); clock=time.monotonic()
    l = lammps(cmdargs=['-log',str(ROOT/'logs'/f'{name}.log'),'-screen','none'])
    l.file(str(ROOT/'inputs'/f'{name}.in'))
    # Coordinates and pair virial at precisely the same final timestep.
    xyz = np.array(l.numpy.extract_atom('x')[:case['N']],copy=True)
    ids = np.array(l.numpy.extract_atom('id')[:case['N']],copy=True)
    pv = l.extract_compute('pv',0,0)
    np.savez(ROOT/'outputs'/f'{name}_final.npz',x=xyz,id=ids,pvir=pv)
    l.close()
    row=dict(case,start=start,end=stamp(),wall_seconds=time.monotonic()-clock)
    with (ROOT/'outputs/completed.jsonl').open('a') as f:
        f.write(json.dumps(row)+'\n')
    print(json.dumps(row),flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['pilot','main','timestep'])
    args=parser.parse_args()
    cases=[]
    if args.mode=='pilot':
        cases=[configuration(.30,100,2e-5,725191,'pilot',eq=.1,production=.1)]
    elif args.mode=='main':
        for A,dt in [(10,1e-4),(100,2e-5)]:
            for phi in [.05,.15,.30]:
                for rep in [0,1]:
                    name=f'A{A}_phi{phi:.2f}_rep{rep}'
                    seed=738191+int(A)*113+int(phi*100)*971+rep*7919
                    cases.append(configuration(phi,A,dt,seed,name))
    else:
        for A,dt in [(10,5e-5),(100,1e-5)]:
            for rep in [0,1]:
                name=f'A{A}_phi0.30_halfdt_rep{rep}'
                cases.append(configuration(.30,A,dt,983921+rep*11113+A,name))
    (ROOT/'inputs'/f'manifest_{args.mode}.json').write_text(json.dumps(cases,indent=2))
    for case in cases: run_case(case)

if __name__=='__main__': main()
