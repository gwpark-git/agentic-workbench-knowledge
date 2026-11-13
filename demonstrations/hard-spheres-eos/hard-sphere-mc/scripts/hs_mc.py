"""Constraint-only NVT Metropolis hard spheres, sigma=kBT=1.

Independent small implementation inspired by Allen & Tildesley's CC0 examples.
Numba accelerates the explicitly inspectable all-pairs overlap checks.
No forces, potentials, or integration timestep are used.
"""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import time
import numpy as np
from numba import njit

ROOT=Path(__file__).resolve().parents[1]
BIN_WIDTH=.002
NBINS=60

@njit(cache=True)
def feasible(trial, x, index, box):
    for j in range(len(x)):
        if j==index: continue
        r2=0.
        for k in range(3):
            d=trial[k]-x[j,k]
            d-=box*np.rint(d/box)
            r2+=d*d
        if r2<1.: return False
    return True

@njit(cache=True)
def move(x,unwrapped,box,delta,i,displacement):
    trial=np.empty(3)
    for k in range(3):
        trial[k]=(x[i,k]+displacement[k])%box
    if not feasible(trial,x,i,box): return False
    x[i]=trial
    unwrapped[i]+=displacement
    return True

@njit(cache=True)
def scan(x,box):
    hist=np.zeros(NBINS,np.int64)
    minimum=box*box*3
    for i in range(len(x)-1):
        for j in range(i+1,len(x)):
            r2=0.
            for k in range(3):
                d=x[i,k]-x[j,k]
                d-=box*np.rint(d/box)
                r2+=d*d
            minimum=min(minimum,r2)
            if r2>=1. and r2<(1+NBINS*BIN_WIDTH)**2:
                index=int((np.sqrt(r2)-1.)/BIN_WIDTH)
                if 0<=index<NBINS: hist[index]+=1
    return hist,np.sqrt(minimum)

@njit(cache=True)
def run(x,box,delta,seed,equil,production,spacing,tune_sweeps=1000):
    np.random.seed(seed)
    n=len(x); frames=production//spacing
    counts=np.zeros((frames,NBINS),np.int64)
    min_r=np.zeros(frames)
    msd=np.zeros(frames)
    accepted=np.zeros(production,np.int64)
    eq_stats=np.zeros((equil//100,4))
    snapshots=np.zeros((production//1000+1,n,3))
    unwrapped=x.copy()
    origin=x.copy()
    tune_accept=0
    eq_block_accept=0
    for sweep in range(equil+production):
        number=0
        for attempt in range(n):
            i=np.random.randint(n)
            displacement=(np.random.random(3)*2.-1.)*delta
            if move(x,unwrapped,box,delta,i,displacement): number+=1
        if sweep<equil:
            tune_accept+=number
            eq_block_accept+=number
            if (sweep+1)%100==0:
                h,m=scan(x,box)
                b=(sweep+1)//100-1
                eq_stats[b,0]=sweep+1
                eq_stats[b,1]=eq_block_accept/(100*n)
                eq_stats[b,2]=m
                eq_stats[b,3]=delta
                eq_block_accept=0
                if sweep+1<=tune_sweeps:
                    rate=tune_accept/(100*n)
                    if rate>.55: delta=min(delta*1.2,box/2)
                    elif rate<.35: delta*=.8
                tune_accept=0
            if sweep+1==equil:
                origin=unwrapped.copy()
                snapshots[0]=x
        else:
            p=sweep-equil
            accepted[p]=number
            if (p+1)%spacing==0:
                f=(p+1)//spacing-1
                counts[f],min_r[f]=scan(x,box)
                msd[f]=np.sum((unwrapped-origin)**2)/n
            if (p+1)%1000==0:
                snapshots[(p+1)//1000]=x
    return x,counts,min_r,msd,accepted,eq_stats,snapshots,delta

def case(phi,nside,rep,kind='main',production=30000,spacing=5,delta_scale=1.):
    n=nside**3
    box=(n*np.pi/(6*phi))**(1/3)
    delta={.05:1.5,.15:.55,.30:.25}[phi]*delta_scale
    seed=728193+int(phi*100)*173+n*11+rep*7919+(100000 if kind!='main' else 0)
    return dict(name=f'{kind}_N{n}_phi{phi:.2f}_rep{rep}',kind=kind,phi=phi,N=n,nside=nside,
                L=box,rho=n/box**3,seed=seed,delta_initial=delta,equilibration_sweeps=3000,
                adaptation_sweeps=1000,production_sweeps=production,sample_spacing_sweeps=spacing,
                histogram_bin_width=BIN_WIDTH,histogram_maximum=1+NBINS*BIN_WIDTH)

def execute(c):
    start=datetime.now(timezone.utc).isoformat(); t=time.monotonic()
    x=(np.indices((c['nside'],)*3).reshape(3,-1).T+.5)*(c['L']/c['nside'])
    np.save(ROOT/'inputs'/f"{c['name']}_initial.npy",x)
    final,hist,mind,msd,accept,eq,snapshots,delta=run(
        x,c['L'],c['delta_initial'],c['seed'],c['equilibration_sweeps'],
        c['production_sweeps'],c['sample_spacing_sweeps'],c['adaptation_sweeps'])
    assert np.min(mind)>=1. and np.min(eq[:,2])>=1., 'Constraint violation'
    assert np.min(mind)<c['L']/2
    np.savez_compressed(ROOT/'outputs'/f"{c['name']}.npz",positions=final,histogram=hist,
                        minimum_distance=mind,msd=msd,accepted_per_sweep=accept,
                        equilibration=eq,snapshots=snapshots,final_delta=delta)
    row=dict(c,start=start,end=datetime.now(timezone.utc).isoformat(),wall_seconds=time.monotonic()-t,
             acceptance=float(accept.mean()/c['N']),final_delta=float(delta),
             minimum_sampled_distance=float(mind.min()))
    with (ROOT/'outputs/completed.jsonl').open('a') as f: f.write(json.dumps(row)+'\n')
    print(json.dumps(row),flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['pilot','main','size','proposal'])
    args=parser.parse_args()
    if args.mode=='pilot':
        cases=[case(.3,6,0,'pilot',production=1000)]
    elif args.mode=='main':
        cases=[case(phi,6,rep) for phi in [.05,.15,.3] for rep in range(3)]
    elif args.mode=='size':
        cases=[case(.3,8,rep,'size',production=30000) for rep in range(3)]
    else:
        cases=[case(.3,6,rep,'proposal',production=30000,delta_scale=.4) for rep in range(3)]
        # Freeze a smaller proposal after equilibration; no adaptation in this check.
        for c in cases: c['adaptation_sweeps']=0
    (ROOT/'inputs'/f'manifest_{args.mode}.json').write_text(json.dumps(cases,indent=2))
    for c in cases: execute(c)

if __name__=='__main__': main()
