"""Analyze raw virial samples without fitting or changing particle diameter."""
from collections import defaultdict
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]

def cs(phi):
    return (1+phi+phi**2-phi**3)/(1-phi)**3

def blocks(x, length):
    n=len(x)//length
    return np.mean(x[:n*length].reshape(n,length),axis=1)

def sem(x):
    return float(np.std(x,ddof=1)/np.sqrt(len(x)))

def autocorr_time(x,dt):
    x=x-np.mean(x)
    transform=np.fft.rfft(x,n=2*len(x))
    corr=np.fft.irfft(transform*np.conj(transform))[:len(x)]
    corr/=np.arange(len(x),0,-1)
    corr/=corr[0]
    stop=next((i for i in range(1,len(x)) if corr[i]<0),len(x)//2)
    return float(dt*(.5+np.sum(corr[1:stop])))

def write_csv(path,rows):
    if not rows: return
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

def main():
    manifests=[]
    for mode in ['main','timestep']:
        path=ROOT/'inputs'/f'manifest_{mode}.json'
        if path.exists():
            manifests += [dict(c,kind=mode) for c in json.loads(path.read_text())]
    completed={json.loads(x)['name'] for x in (ROOT/'outputs/completed.jsonl').read_text().splitlines()}
    cases=[c for c in manifests if c['name'] in completed]
    groups=defaultdict(list); diagnostics=[]; direct_virials=[]
    all_data={}
    for c in cases:
        d=np.loadtxt(ROOT/'outputs'/f"{c['name']}.dat")
        t=d[:,0]*c['dt']; p=d[t>c['equilibration_time']+1e-8,2]
        assert len(p)==round(c['production_time']/c['sample_interval'])
        assert np.isfinite(d).all() and np.min(d[:,1])>=0
        # LAMMPS ave/time defaults to six significant digits in text output.
        np.testing.assert_allclose(d[:,2],c['rho']+d[:,1],atol=8e-6,rtol=8e-6)
        b=blocks(p,200); first,second=np.split(b,2)
        half_se=np.sqrt(sem(first)**2+sem(second)**2)
        eq_index=np.argmin(abs(t-c['equilibration_time']))
        diag=dict(name=c['name'],A=c['A'],phi=c['phi'],dt=c['dt'],kind=c['kind'],
                  mean_pressure=float(p.mean()),sem_block_1=sem(blocks(p,100)),
                  sem_block_2=sem(b),sem_block_5=sem(blocks(p,500)),
                  pressure_tau_int_time=autocorr_time(p,.01),
                  half_mean_difference=float(second.mean()-first.mean()),
                  half_difference_standard_errors=float((second.mean()-first.mean())/half_se),
                  block_2_lag1_correlation=float(np.corrcoef(b[:-1],b[1:])[0,1]),
                  msd_end_equilibration=float(d[eq_index,4]),msd_end_production=float(d[-1,4]),
                  sample_count=len(p),production_blocks=len(b))
        diagnostics.append(diag)
        final=np.load(ROOT/'outputs'/f"{c['name']}_final.npz")
        # Independent O(N^2) minimum-image sum, no LAMMPS neighbor list or forces.
        x=final['x']; dr=x[:,None,:]-x[None,:,:]; dr-=c['L']*np.rint(dr/c['L'])
        r=np.linalg.norm(dr[np.triu_indices(c['N'],1)],axis=1); r=r[r<1]
        pv=float(np.sum(r*c['A']*np.pi*np.sin(np.pi*r))/(3*c['L']**3))
        err=pv-float(final['pvir'])
        assert abs(err)<1e-10
        direct_virials.append(dict(name=c['name'],lammps_pvir=float(final['pvir']),independent_pvir=pv,error=err))
        groups[(c['kind'],c['A'],c['phi'],c['dt'])].append((c,p,b))
        all_data[c['name']]=(c,t,d)
    summary=[]
    for (kind,A,phi,dt),runs in sorted(groups.items()):
        b=np.concatenate([x[2] for x in runs]); means=np.array([x[1].mean() for x in runs])
        pressure=float(means.mean()); rho=runs[0][0]['rho']
        # Two replicas provide a noisy additional check. Use the larger SEM.
        replica_sem=sem(means) if len(means)>1 else float('nan')
        se=max(sem(b),replica_sem) if len(means)>1 else sem(b)
        row=dict(kind=kind,A=A,phi=phi,dt=dt,replicas=len(runs),N=runs[0][0]['N'],
                 rho=rho,pressure=pressure,pressure_sem=se,block_sem=sem(b),replica_sem=replica_sem,
                 Z=pressure/rho,Z_sem=se/rho,Z_CS=float(cs(phi)),pressure_CS=float(rho*cs(phi)),
                 percent_difference_CS=100*(pressure/(rho*cs(phi))-1))
        summary.append(row)
    sensitivity=[]
    for A in [10,100]:
        base=next((x for x in summary if x['kind']=='main' and x['A']==A and x['phi']==.3),None)
        half=next((x for x in summary if x['kind']=='timestep' and x['A']==A),None)
        if base and half:
            delta=half['pressure']-base['pressure']; se=np.hypot(base['pressure_sem'],half['pressure_sem'])
            sensitivity.append(dict(A=A,phi=.3,base_dt=base['dt'],half_dt=half['dt'],
                                    base_Z=base['Z'],half_Z=half['Z'],delta_Z=delta/base['rho'],
                                    combined_sem_Z=float(se/base['rho']),standardized_difference=float(delta/se),
                                    relative_change_percent=100*delta/base['pressure']))
    # Parameter-free low-density diagnostics; these do not rescale main plots.
    r=np.linspace(0,1,200001); potential_geometry=[]
    for A in [10,100]:
        mayer=1-np.exp(-A*(1+np.cos(np.pi*r)))
        potential_geometry.append(dict(A=A,BH_diameter=float(np.trapezoid(mayer,r)),
                                       B2=float(2*np.pi*np.trapezoid(mayer*r*r,r)),
                                       B2_ratio_hard_sphere=float(3*np.trapezoid(mayer*r*r,r))))
    write_csv(ROOT/'outputs/summary.csv',summary)
    write_csv(ROOT/'validation/sampling.csv',diagnostics)
    write_csv(ROOT/'validation/direct_virial.csv',direct_virials)
    write_csv(ROOT/'validation/timestep.csv',sensitivity)
    (ROOT/'validation/analysis.json').write_text(json.dumps(dict(summary=summary,sampling=diagnostics,
        timestep=sensitivity,potential_geometry=potential_geometry,max_absolute_virial_error=max(abs(x['error']) for x in direct_virials)),indent=2))

    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(10,4.1),layout='constrained')
    grid=np.linspace(0,.32,200)
    axes[0].plot(grid,6*grid/np.pi*cs(grid),'k--',label='Carnahan–Starling (nominal diameter)')
    axes[1].plot(grid,cs(grid),'k--')
    for A,color,marker in [(10,'#2878B5','o'),(100,'#CC552B','s')]:
        points=[x for x in summary if x['kind']=='main' and x['A']==A]
        for ax,value,error in [(axes[0],'pressure','pressure_sem'),(axes[1],'Z','Z_sem')]:
            ax.errorbar([x['phi'] for x in points],[x[value] for x in points],
                        yerr=[x[error] for x in points],marker=marker,color=color,capsize=4,
                        label=fr'$A/k_BT={A}$',ls='none',lw=1.3)
        halves=[x for x in summary if x['kind']=='timestep' and x['A']==A]
        for ax,value,error in [(axes[0],'pressure','pressure_sem'),(axes[1],'Z','Z_sem')]:
            if halves:
                ax.errorbar([x['phi']+.004 for x in halves],[x[value] for x in halves],
                            yerr=[x[error] for x in halves],marker=marker,mfc='white',color=color,
                            ls='none',capsize=3,label='Half timestep' if A==10 else None)
    axes[0].set(xlabel=r'Nominal volume fraction $\phi=\pi\rho\sigma^3/6$',ylabel=r'$\Pi\sigma^3/(k_BT)$',xlim=(0,.325),ylim=(0,None))
    axes[1].set(xlabel=r'Nominal volume fraction $\phi$',ylabel=r'$Z=\Pi/(\rho k_BT)$',xlim=(0,.325),ylim=(.95,None))
    axes[0].legend(fontsize=8); axes[1].legend(fontsize=8)
    fig.suptitle('Brownian cosine-repulsive particles: N=216, two independent seeds\nError bars: larger of block and replica SEM; half-timestep symbols offset by +0.004 in φ',fontsize=10)
    fig.savefig(ROOT/'figures/equation_of_state.png',dpi=200)
    fig.savefig(ROOT/'figures/equation_of_state.pdf')
    plt.close(fig)

    fig,axes=plt.subplots(2,3,figsize=(11,5.5),layout='constrained')
    for i,A in enumerate([10,100]):
        for j,phi in enumerate([.05,.15,.30]):
            ax=axes[i,j]
            for rep in [0,1]:
                name=f'A{A}_phi{phi:.2f}_rep{rep}'
                if name not in all_data: continue
                c,t,d=all_data[name]
                z=d[:,2]/c['rho']
                ax.plot(blocks(t,50),blocks(z,50),lw=.8,label=f'Seed {rep+1}')
            ax.axvline(5,color='grey',ls=':',label='Sampling starts')
            ax.axhline(cs(phi),color='black',ls='--',lw=.8,label='CS')
            ax.set(title=f'A={A}, φ={phi:.2f}',xlabel='Time (σ²/D₀)',ylabel='Z (0.5-time-unit means)')
    axes[0,0].legend(fontsize=7)
    fig.savefig(ROOT/'figures/sampling_diagnostics.png',dpi=160)
    plt.close(fig)
    print(json.dumps(dict(summary=summary,timestep=sensitivity,potential_geometry=potential_geometry),indent=2))

if __name__=='__main__': main()
