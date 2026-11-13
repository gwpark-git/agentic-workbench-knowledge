"""Software and estimator checks, separate from scientific convergence."""
import json
from pathlib import Path
import numpy as np
from lammps import lammps

ROOT=Path(__file__).resolve().parents[1]
out={}

def instance(name):
    return lammps(cmdargs=['-screen','none','-log',str(ROOT/'logs'/f'verify_{name}.log')])

for periodic in [False,True]:
    l=instance(str(periodic)); L=5.; A=10.; r=.8
    x1,x2=(.2,4.4) if periodic else (1.,1.8)
    l.commands_string(f'''units lj
atom_style atomic
region box block 0 5 0 5 0 5
create_box 1 box
create_atoms 1 single {x1} 2 2
create_atoms 1 single {x2} 2 2
mass 1 1
pair_style soft 1
pair_coeff * * {A}
compute pv all pressure NULL pair
thermo_style custom step pe c_pv
thermo_modify norm no
run 0''')
    pressure=l.extract_compute('pv',0,0)
    force=np.linalg.norm(l.numpy.extract_atom('f')[0])
    energy=l.get_thermo('pe')
    expected_force=A*np.pi*np.sin(np.pi*r)
    expected_energy=A*(1+np.cos(np.pi*r))
    expected_pressure=r*expected_force/(3*L**3)
    h=1e-6
    fd=-(A*(1+np.cos(np.pi*(r+h)))-A*(1+np.cos(np.pi*(r-h))))/(2*h)
    np.testing.assert_allclose([force,energy,pressure,fd],
                               [expected_force,expected_energy,expected_pressure,expected_force],rtol=1e-9)
    out['periodic_pair' if periodic else 'pair']={'force':force,'energy':energy,'pvir':pressure,'finite_difference_force':fd,'passed':True}
    l.close()

l=instance('ideal'); n=4096; t=1.
l.commands_string(f'''units lj
atom_style atomic
region box block 0 30 0 30 0 30
create_box 1 box
create_atoms 1 random {n} 719318 box
mass 1 1
pair_style zero 1
pair_coeff * *
compute pv all pressure NULL pair
compute msd all msd
fix bd all brownian 1.0 613971 gamma_t 1.0 rng gaussian
timestep 0.001
thermo_style custom step c_pv c_msd[4]
run 1000''')
msd=l.extract_compute('msd',0,1)[3]
pv=l.extract_compute('pv',0,0)
D=msd/(6*t)
seD=np.sqrt(2/(3*n))
assert abs(D-1)<5*seD and abs(pv)<1e-12
out['ideal_diffusion']={'N':n,'time':t,'measured_D':D,'expected_D':1.,'expected_standard_error_D':float(seD),'pair_pressure':pv,'passed':True}
l.close()
(ROOT/'validation/software.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
