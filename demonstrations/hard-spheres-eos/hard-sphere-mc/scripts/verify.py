"""Independent geometry, transition and analytic finite-N pressure checks."""
import importlib.util
import json
from pathlib import Path
import numpy as np
from hs_mc import feasible,move,scan,run
from estimators import contact_series,block_means,mean_sem,compression_curves

root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('at_reference',root/'source/allen_tildesley_mc_hs_module.py')
ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
rng=np.random.default_rng(87193)
nside=4;n=nside**3;phi=.3;box=(n*np.pi/(6*phi))**(1/3)
x=(np.indices((nside,)*3).reshape(3,-1).T+.5)*(box/nside)
u=x.copy();xr=x.copy();ur=u.copy();accepted=0
for step in range(5000):
    i=int(rng.integers(n));d=rng.uniform(-.5,.5,3);trial=(xr[i]+d)%box
    independent=not ref.overlap_1(trial/box,box,np.delete(xr,i,axis=0)/box)
    actual=move(x,u,box,.5,i,d)
    assert actual==independent
    if independent:
        xr[i]=trial;ur[i]+=d;accepted+=1
    np.testing.assert_allclose(x,xr,atol=2e-14,rtol=0)
np.testing.assert_allclose(u,ur,atol=2e-14,rtol=0)
boundary=[]
for distance,allowed in [(1-1e-10,False),(1.,True),(1+1e-10,True)]:
    pair=np.array([[.2,1.,1.],[5.2-distance,1.,1.]])
    actual=feasible(pair[0],pair,0,5.)
    assert actual==allowed
    boundary.append({'distance':distance,'allowed':bool(actual)})
# Analytic N=2 hard-sphere EOS: Q(V) proportional to V(V-v_ex).
# For L>2, v_ex=4*pi/3. This is independent of Carnahan-Starling.
box2=3.;n2=2;exclusion=4*np.pi/3
x2=np.array([[.2,.2,.2],[1.7,1.7,1.7]])
final,hist,mind,msd,acc,eq,snaps,delta=run(x2,box2,1.,79183,2000,100000,1,0)
z,_=contact_series(hist,n2,box2)
bm=block_means(z,1000)
estimate,error=mean_sem(bm)
exact=1+exclusion/(2*(box2**3-exclusion))
assert abs(estimate-exact)<5*error
assert np.min(mind)>=1.
eps=np.array([.01,.03,.05])
curves,survival=compression_curves(mind,n2,eps)
exact_survival=1-exclusion*(np.exp(eps)-1)/(box2**3-exclusion)
assert np.max(abs(survival-exact_survival))<.004
# Compare the recorded min-distance event against direct affine compression.
for frame in snaps:
    minimum=scan(frame,box2)[1]
    for e in [.01,.03,.05]:
        factor=np.exp(-e/3)
        direct=not ref.overlap(box2*factor,frame/box2)
        assert direct==bool(minimum*factor>=1.)
np.savez_compressed(root/'validation/two_particle.npz',histogram=hist,minimum_distance=mind)
result={'reference':'Allen-Tildesley CC0 mc_hs_module.py',
        'transition_test':{'proposals':5000,'accepted':accepted,'all_match_reference':True},
        'contact_boundary':boundary,
        'analytic_two_particle':{'N':2,'L':box2,'exact_Z':exact,'measured_Z':estimate,
          'SEM_1000_sweep_blocks':error,'standardized_error':(estimate-exact)/error,
          'compression_epsilons':eps.tolist(),'survival':survival.tolist(),
          'exact_survival':exact_survival.tolist(),'minimum_distance':float(mind.min())},
        'affine_compression_matches_reference':True,'passed':True}
(root/'validation/software.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
