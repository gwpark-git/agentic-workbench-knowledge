"""Analyze constraint-only hard-sphere samples and compare with archived soft data."""
from collections import defaultdict
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from estimators import cs,contact_series,block_means,mean_sem,compression_curves

ROOT=Path(__file__).resolve().parents[1]

def csv_write(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def tau_int(x,spacing):
    y=x-x.mean()
    f=np.fft.rfft(y,n=2*len(y))
    ac=np.fft.irfft(f*np.conj(f))[:len(y)]/np.arange(len(y),0,-1)
    ac/=ac[0]
    stop=next((k for k in range(1,len(ac)) if ac[k]<0),len(ac)//2)
    return float(spacing*(.5+ac[1:stop].sum()))

def compression_jackknife(mins,n,block_size,contact_blocks):
    eps=np.array([.1,.2,.4,.6,.8])/n
    events=mins[:,None]>=np.exp(eps[None,:]/3)
    b=block_means(events,block_size)
    p=b.mean(axis=0)
    curves=1-np.log(p)/(n*eps)
    matrix=np.stack([np.ones_like(eps),eps],axis=1)
    projection=np.linalg.pinv(matrix)[0]
    intercept=float(projection@curves)
    leave=[]
    for j in range(len(b)):
        q=(b.sum(axis=0)-b[j])/(len(b)-1)
        leave.append(1-np.log(q)/(n*eps))
    leave=np.array(leave)
    errors=np.sqrt((len(b)-1)*np.mean((leave-leave.mean(axis=0))**2,axis=0))
    jk=leave@projection
    err=float(np.sqrt((len(b)-1)*np.mean((jk-jk.mean())**2)))
    contact_leave=(np.sum(contact_blocks)-contact_blocks)/(len(b)-1)
    difference=contact_leave-jk
    difference_error=float(np.sqrt((len(b)-1)*np.mean((difference-difference.mean())**2)))
    return dict(Z=intercept,SEM=err,epsilons=eps.tolist(),Z_finite_compression=curves.tolist(),
                SEM_finite_compression=errors.tolist(),survival=p.tolist(),blocks=len(b),
                contact_difference_SEM=difference_error)

def independent_geometry(x,box):
    dr=x[:,None,:]-x[None,:,:]
    dr-=box*np.rint(dr/box)
    distances=np.linalg.norm(dr[np.triu_indices(len(x),1)],axis=1)
    return distances

def main():
    records=[json.loads(x) for x in (ROOT/'outputs/completed.jsonl').read_text().splitlines()]
    # Reruns append execution history but overwrite each named data artifact.
    # Analyze each artifact once, using its most recent execution record.
    records=list({x['name']:x for x in records}.values())
    records=[x for x in records if x['kind']!='pilot']
    groups=defaultdict(list);runs=[];constraints=[];sensitivity=[];plots={}
    for c in records:
        d=np.load(ROOT/'outputs'/f"{c['name']}.npz")
        hist=d['histogram']; minimum=d['minimum_distance']
        z,g=contact_series(hist,c['N'],c['L'])
        b=block_means(z,200) # 200 frames x 5 sweeps = 1000 sweeps.
        m,se=mean_sem(b)
        first,second=np.split(b,2)
        sehalf=np.hypot(mean_sem(first)[1],mean_sem(second)[1])
        row=dict(name=c['name'],kind=c['kind'],N=c['N'],phi=c['phi'],seed=c['seed'],Z=m,
                 SEM_block_1000=se,SEM_block_250=mean_sem(block_means(z,50))[1],
                 SEM_block_500=mean_sem(block_means(z,100))[1],
                 SEM_block_2000=mean_sem(block_means(z,400))[1],
                 half_difference=float(second.mean()-first.mean()),
                 half_difference_standard_errors=float((second.mean()-first.mean())/sehalf),
                 tau_int_sweeps=tau_int(z,5),block_lag1=float(np.corrcoef(b[:-1],b[1:])[0,1]),
                 acceptance=c['acceptance'],delta=c['final_delta'],minimum_distance=float(minimum.min()),
                 final_MSD=float(d['msd'][-1]),samples=len(z))
        runs.append(row)
        # Independent NumPy checks of saved configurations, including all pairs.
        all_min=10.;max_hist_error=0
        for frame in d['snapshots']:
            radii=independent_geometry(frame,c['L'])
            assert radii.min()>=1.-2e-14
            all_min=min(all_min,float(radii.min()))
        radii=independent_geometry(d['positions'],c['L'])
        check_hist=np.histogram(radii,bins=1+np.arange(61)*.002)[0]
        max_hist_error=int(np.max(abs(check_hist-hist[-1])))
        assert max_hist_error==0
        assert np.min(minimum)>=1.
        constraints.append(dict(name=c['name'],snapshots_checked=len(d['snapshots']),
                                minimum_saved_distance=all_min,final_histogram_error=max_hist_error,
                                sampled_minimum_distance=float(minimum.min()),sampled_constraints_pass=True))
        for fit_range,degree in [(.03,1),(.04,2),(.06,1),(.06,2),(.08,2),(.10,2)]:
            zz,_=contact_series(hist,c['N'],c['L'],fit_range=fit_range,degree=degree)
            sensitivity.append(dict(name=c['name'],kind=c['kind'],phi=c['phi'],N=c['N'],
                                    fit_range=fit_range,degree=degree,Z=float(zz.mean()),
                                    SEM_block=mean_sem(block_means(zz,200))[1]))
        groups[(c['kind'],c['N'],c['phi'])].append((c,d,z,b))
        plots[c['name']]=(c,d,z,b)

    summaries=[]; compression_rows=[]; contact_fit_rows=[]
    for (kind,n,phi),rs in sorted(groups.items()):
        allblocks=np.concatenate([x[3] for x in rs])
        means=np.array([x[2].mean() for x in rs])
        z=float(means.mean());blocksem=mean_sem(allblocks)[1];replicasem=mean_sem(means)[1]
        se=max(blocksem,replicasem);rho=rs[0][0]['rho']
        compression=compression_jackknife(np.concatenate([x[1]['minimum_distance'] for x in rs]),n,200,allblocks)
        row=dict(kind=kind,N=n,phi=phi,replicas=len(rs),rho=rho,Z=z,Z_SEM=se,
                 SEM_blocks=blocksem,SEM_replicas=replicasem,pressure=rho*z,pressure_SEM=rho*se,
                 Z_CS=float(cs(phi)),percent_difference_CS=100*(z/cs(phi)-1),
                 compression_Z=compression['Z'],compression_SEM=compression['SEM'],
                 contact_minus_compression=z-compression['Z'],
                 contact_minus_compression_SEM=compression['contact_difference_SEM'],
                 production_samples=sum(len(x[2]) for x in rs))
        summaries.append(row)
        compression_rows.append(dict(kind=kind,N=n,phi=phi,**compression))
        for width,degree in [(.03,1),(.04,2),(.06,1),(.06,2),(.08,2),(.10,2)]:
            values=[]
            for c,d,_,_ in rs:
                zz,_=contact_series(d['histogram'],n,c['L'],fit_range=width,degree=degree)
                values.extend(block_means(zz,200))
            mean,error=mean_sem(np.array(values))
            # Paired block differences measure estimator-range sensitivity.
            diff=np.array(values)-allblocks
            contact_fit_rows.append(dict(kind=kind,N=n,phi=phi,range=width,degree=degree,Z=mean,
                                         SEM=error,delta_from_primary=mean-z,
                                         paired_SEM_difference=mean_sem(diff)[1]))

    sensitivity_groups=[]
    base=next(x for x in summaries if x['kind']=='main' and x['phi']==.3)
    for kind in ['size','proposal']:
        other=next((x for x in summaries if x['kind']==kind),None)
        if other:
            diff=other['Z']-base['Z'];se=float(np.hypot(other['Z_SEM'],base['Z_SEM']))
            sensitivity_groups.append(dict(check=kind,base_N=216,comparison_N=other['N'],
                                           base_Z=base['Z'],comparison_Z=other['Z'],delta_Z=diff,
                                           combined_SEM=se,standardized_difference=diff/se))
    csv_write(ROOT/'outputs/summary.csv',summaries)
    csv_write(ROOT/'validation/sampling.csv',runs)
    csv_write(ROOT/'validation/constraints.csv',constraints)
    csv_write(ROOT/'validation/contact_ranges.csv',contact_fit_rows)
    csv_write(ROOT/'validation/size_proposal.csv',sensitivity_groups)
    result=dict(summary=summaries,compression=compression_rows,contact_ranges=contact_fit_rows,
                runs=runs,constraints=constraints,sensitivity=sensitivity_groups)
    (ROOT/'validation/analysis.json').write_text(json.dumps(result,indent=2))

    soft=[]
    with (ROOT.parent/'outputs/summary.csv').open() as f:
        soft=[x for x in csv.DictReader(f) if x['kind']=='main']
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(10,4.3),layout='constrained')
    grid=np.linspace(0,.32,201)
    axes[0].plot(grid,cs(grid),'k--',label='Carnahan–Starling')
    axes[1].plot(grid,grid*6/np.pi*cs(grid),'k--')
    for A,color,marker in [(10,'#2878B5','o'),(100,'#CC552B','s')]:
        points=[x for x in soft if int(x['A'])==A]
        for ax,val,err in [(axes[0],'Z','Z_sem'),(axes[1],'pressure','pressure_sem')]:
            ax.errorbar([float(x['phi']) for x in points],[float(x[val]) for x in points],
                        yerr=[float(x[err]) for x in points],ls='none',marker=marker,color=color,
                        capsize=3,label=f'Soft A/kBT={A} (Brownian)')
    hard=[x for x in summaries if x['kind']=='main']
    for ax,val,err in [(axes[0],'Z','Z_SEM'),(axes[1],'pressure','pressure_SEM')]:
        ax.errorbar([x['phi'] for x in hard],[x[val] for x in hard],yerr=[x[err] for x in hard],
                    marker='D',ls='none',color='#26834A',capsize=4,label='Hard spheres N=216 (MC)')
        bigger=[x for x in summaries if x['kind']=='size']
        if bigger:
            ax.errorbar([x['phi']+.004 for x in bigger],[x[val] for x in bigger],
                        yerr=[x[err] for x in bigger],marker='D',mfc='white',ls='none',
                        color='#26834A',capsize=3,label='Hard spheres N=512 (MC)')
    axes[0].set(xlabel='Nominal volume fraction φ',ylabel='Z = Π/(ρkBT)',xlim=(0,.325),ylim=(.95,None))
    axes[1].set(xlabel='Nominal volume fraction φ',ylabel='Πσ³/(kBT)',xlim=(0,.325),ylim=(0,None))
    axes[0].legend(fontsize=8)
    fig.suptitle('Hard-sphere constraints versus soft repulsion; σ = kBT = 1\nBars: max(block SEM, replica SEM); N=512 point offset by +0.004 in φ',fontsize=10)
    fig.savefig(ROOT/'figures/comparison.png',dpi=200)
    fig.savefig(ROOT/'figures/comparison.pdf')
    plt.close(fig)

    fig,axes=plt.subplots(1,3,figsize=(11,3.5),layout='constrained')
    for j,phi in enumerate([.05,.15,.3]):
        ax=axes[j]
        for rep in range(3):
            c,d,z,b=plots[f'main_N216_phi{phi:.2f}_rep{rep}']
            ax.plot((np.arange(len(b))+.5)*1000,b,label=f'Replica {rep+1}',lw=.9)
        ax.axhline(cs(phi),color='k',ls='--',lw=.8,label='CS')
        ax.set(title=f'φ = {phi:.2f}',xlabel='Production MC sweeps',ylabel='Z (1000-sweep blocks)')
    axes[0].legend(fontsize=7)
    fig.savefig(ROOT/'figures/sampling.png',dpi=180)
    plt.close(fig)

    fig,axes=plt.subplots(1,2,figsize=(10,3.7),layout='constrained')
    for phi,color in [(.05,'#2878B5'),(.15,'#CC552B'),(.30,'#26834A')]:
        cc=next(x for x in compression_rows if x['kind']=='main' and x['phi']==phi)
        axes[0].errorbar(np.array(cc['epsilons'])*1000,cc['Z_finite_compression'],
                         yerr=cc['SEM_finite_compression'],marker='o',color=color,capsize=3,label=f'φ={phi}')
        primary=next(x for x in hard if x['phi']==phi)
        axes[0].errorbar([0],[primary['Z']],yerr=[primary['Z_SEM']],marker='D',color=color,capsize=3)
        rr=[x for x in contact_fit_rows if x['kind']=='main' and x['phi']==phi and x['degree']==2]
        axes[1].errorbar([x['range'] for x in rr],[x['Z']-primary['Z'] for x in rr],
                        yerr=[x['paired_SEM_difference'] for x in rr],marker='o',color=color,capsize=3,label=f'φ={phi}')
    axes[0].set(xlabel='Virtual compression −1000 ln(V′/V)',ylabel='Z from finite compression\n(diamonds: contact estimate at zero)')
    axes[1].axhline(0,color='k',lw=.8)
    axes[1].set(xlabel='Maximum contact-fit separation above σ',ylabel='Z(range) − Z(primary range 0.06σ)')
    axes[0].legend(fontsize=8);axes[1].legend(fontsize=8)
    fig.savefig(ROOT/'figures/estimator_checks.png',dpi=180)
    plt.close(fig)
    print(json.dumps(dict(summary=summaries,sensitivity=sensitivity_groups),indent=2))

if __name__=='__main__': main()
